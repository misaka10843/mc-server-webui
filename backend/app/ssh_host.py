import asyncio
import json
import logging
import shlex
import time
import uuid
from datetime import datetime, time as clock_time, timedelta
from zoneinfo import ZoneInfo

import asyncssh
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed, InvalidHandshake

from mc_agent.idle import IdlePolicy, IdleTracker

logger = logging.getLogger(__name__)


def connection_options(config):
    keys = [asyncssh.import_private_key(config["private_key"])] if config.get("private_key") else []
    return dict(host=config["host"], port=config["port"], username=config["username"],
                password=config.get("password") or None, client_keys=keys,
                known_hosts=([asyncssh.import_public_key(config["host_key"])], [], []),
                agent_path=None, config=None, connect_timeout=10, login_timeout=15,
                keepalive_interval=15, keepalive_count_max=3)


class SSHHost:
    def __init__(self, config, state, update, log, policy):
        self.config = config
        self.state = state
        self.update = update
        self.log = log
        self.policy = policy
        self.connection = None
        self.mod = None
        self.pending = {}
        self.tasks = []
        self.log_task = None
        self.want_logs = False
        self.shutdown_task = None
        self.shutdown_lock = asyncio.Lock()
        self.changed = asyncio.Event()
        self.seen_boot = None
        self.apply_policy(policy)

    def publish(self, values):
        self.update(values)
        self.changed.set()

    def apply_policy(self, policy):
        if self.shutdown_lock.locked():
            raise RuntimeError("关机进行中，请稍后修改策略")
        self.policy = policy
        self.publish({"policy_revision": policy["revision"], "policy_enabled": bool(policy["enabled"]),
                      "idle_policy": {**policy, "timezone": "Asia/Hong_Kong"},
                      "shutdown": "none", "shutdown_error": None})

    async def start(self):
        self.tasks = [asyncio.create_task(self.run()), asyncio.create_task(self.idle_scheduler())]

    async def close(self):
        if self.mod:
            await self.mod.close()
        tasks = self.tasks + [task for task in (self.log_task, self.shutdown_task) if task]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        if self.connection:
            self.connection.close()
            await self.connection.wait_closed()

    async def execute(self, *args, timeout=30):
        if self.connection is None:
            raise ConnectionError("SSH 尚未连接")
        result = await self.connection.run(shlex.join(args), check=False, timeout=timeout)
        if result.exit_status != 0:
            raise RuntimeError("SSH 命令执行失败：" + result.stderr.strip()[:300])
        return result.stdout.strip()

    async def inspect(self, name=None):
        data = json.loads(await self.execute("docker", "inspect", "--format", "{{json .}}", name or self.config["container"]))
        return data

    async def refresh_container(self):
        data = await self.inspect()
        details = data["State"]
        self.publish({"container": details["Status"], "container_exit_code": details["ExitCode"], "container_started_at": details["StartedAt"]})
        return data

    async def run(self):
        delay = 1
        while True:
            try:
                async with asyncssh.connect(**connection_options(self.config)) as connection:
                    self.connection = connection
                    boot = await self.execute("cat", "/proc/sys/kernel/random/boot_id")
                    self.publish({"host": "online", "host_boot_id": boot, "ssh_error": None})
                    data = await self.refresh_container()
                    if boot != self.seen_boot:
                        self.seen_boot = boot
                        if data["State"]["Status"] in ("exited", "created") and self.state.get("shutdown") not in ("preparing", "poweroff_requested"):
                            await self.execute("docker", "start", self.config["container"])
                            await self.refresh_container()
                    delay = 1
                    tunnel = await connection.forward_local_port("127.0.0.1", 0, "127.0.0.1", self.config["mod_port"])
                    try:
                        async with asyncio.TaskGroup() as group:
                            group.create_task(self.watch_mod(tunnel.get_port()))
                            group.create_task(self.watch_container())
                            group.create_task(self.watch_connection(connection))
                    finally:
                        tunnel.close()
                        await tunnel.wait_closed()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning("SSH host connection unavailable: %s", type(exc).__name__)
                self.publish({"ssh_error": "SSH 连接中断或检查失败，请检查地址、认证、主机密钥和 Docker 权限"})
            finally:
                self.connection = None
                self.mod = None
                self.publish({"host": "unknown", "minecraft": "unknown", "container": "unknown", "online": None, "players": [], "boot_id": None, "activity_version": None, "idle_since": None})
                if self.log_task:
                    self.log_task.cancel()
                    await asyncio.gather(self.log_task, return_exceptions=True)
                    self.log_task = None
            await asyncio.sleep(delay)
            delay = min(delay * 2, 30)

    async def watch_connection(self, connection):
        if self.want_logs:
            self.log_task = asyncio.create_task(self.follow_logs())
        await connection.wait_closed()
        raise ConnectionError("SSH disconnected")

    async def watch_container(self):
        process = await self.connection.create_process(shlex.join(["docker", "events", "--filter", "container=" + self.config["container"], "--format", "{{json .}}"]), stderr=asyncssh.DEVNULL)
        try:
            await self.refresh_container()
            async for line in process.stdout:
                action = json.loads(line).get("Action")
                if action in ("start", "stop", "die", "restart", "pause", "unpause", "destroy"):
                    await self.refresh_container()
                    if action in ("start", "restart") and self.want_logs:
                        if self.log_task:
                            self.log_task.cancel()
                            await asyncio.gather(self.log_task, return_exceptions=True)
                        self.log_task = asyncio.create_task(self.follow_logs())
            raise ConnectionError("Docker event stream ended")
        finally:
            process.close()

    async def watch_mod(self, port):
        delay = 1
        while True:
            try:
                async with connect(f"ws://127.0.0.1:{port}/ws", additional_headers={"Authorization": "Bearer " + self.config["mod_token"]}, max_size=1048576, max_queue=32, ping_interval=20, ping_timeout=20) as ws:
                    self.mod = ws
                    delay = 1
                    async for raw in ws:
                        message = json.loads(raw)
                        if message.get("type") == "status":
                            fields = ("minecraft", "minecraft_version", "neoforge_version", "mod_version", "online", "max_players", "players", "boot_id", "activity_version", "uptime_seconds", "mspt", "tps", "memory_used", "memory_max")
                            self.publish({**{key: message.get(key) for key in fields}, "mod_error": None})
                        elif message.get("type") == "response":
                            future = self.pending.get(message.get("id"))
                            if future and not future.done():
                                future.set_result(message)
            except (OSError, ConnectionClosed, InvalidHandshake, TimeoutError):
                logger.info("Minecraft mod connection unavailable over SSH")
                self.publish({"mod_error": "无法连接 command-api，请检查 mod 是否启动、端口和密钥"})
            finally:
                self.mod = None
                for future in tuple(self.pending.values()):
                    if not future.done():
                        future.set_exception(ConnectionError("Minecraft 连接中断，命令结果未知"))
                self.publish({"minecraft": "unknown", "online": None, "players": [], "boot_id": None, "activity_version": None})
            await asyncio.sleep(delay)
            delay = min(delay * 2, 30)

    async def mod_request(self, kind, data, timeout=10):
        if self.mod is None:
            raise ConnectionError("Minecraft mod 尚未连接")
        if len(self.pending) >= 64:
            raise RuntimeError("请求过多")
        request_id = uuid.uuid4().hex
        future = asyncio.get_running_loop().create_future()
        self.pending[request_id] = future
        try:
            await self.mod.send(json.dumps({"type": kind, "id": request_id, **data}))
            response = await asyncio.wait_for(future, timeout)
            if response.get("error"):
                raise RuntimeError(response["error"])
            return response
        finally:
            self.pending.pop(request_id, None)

    async def request(self, kind, data, timeout):
        if kind in ("command", "completion"):
            return await self.mod_request(kind, data, timeout)
        if kind == "set_policy":
            self.apply_policy(data["policy"])
            return {"applied": True, "effective_enabled": bool(self.policy["enabled"])}
        if kind == "start_container":
            if self.shutdown_lock.locked():
                raise RuntimeError("正在关机")
            await self.execute("docker", "start", self.config["container"])
            await self.refresh_container()
            return {}
        if kind == "shutdown_manual":
            if self.shutdown_lock.locked() or (self.shutdown_task and not self.shutdown_task.done()):
                raise RuntimeError("正在关机")
            self.shutdown_task = asyncio.create_task(self.shutdown())
            return {"accepted": True}
        raise ValueError("Unsupported SSH operation")

    async def subscribe_logs(self, enabled):
        if enabled == self.want_logs and (not enabled or (self.log_task and not self.log_task.done())):
            return
        self.want_logs = enabled
        if self.log_task:
            self.log_task.cancel()
            await asyncio.gather(self.log_task, return_exceptions=True)
            self.log_task = None
        if enabled and self.connection:
            self.log_task = asyncio.create_task(self.follow_logs())

    async def follow_logs(self):
        process = None
        try:
            process = await self.connection.create_process(shlex.join(["docker", "logs", "--follow", "--tail", "100", self.config["container"]]), stderr=asyncssh.STDOUT)
            buffer = ""
            while chunk := await process.stdout.read(4096):
                parts = (buffer + chunk).split("\n")
                buffer = parts.pop()[-4096:]
                for line in parts:
                    for key in ("password", "private_key", "mod_token"):
                        if self.config.get(key):
                            line = line.replace(self.config[key], "[REDACTED]")
                    self.log(line[:4096])
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning("SSH log stream failed: %s", type(exc).__name__)
            self.log("日志连接中断，请重新加载日志")
        finally:
            if process:
                process.close()

    async def shutdown(self, automatic=None):
        async with self.shutdown_lock:
            try:
                before = await self.inspect()
                if before["State"]["Status"] != "running" or before["HostConfig"]["RestartPolicy"]["Name"] not in ("no", ""):
                    raise RuntimeError("关机前要求 Minecraft 容器正在运行且 restart 策略为 no")
                self.publish({"shutdown": "preparing", "shutdown_kind": "automatic" if automatic else "manual", "shutdown_error": None})
                if automatic:
                    await self.mod_request("shutdown", automatic)
                else:
                    await self.mod_request("shutdown_manual", {}, 75)
                code = await self.execute("docker", "wait", before["Id"], timeout=300)
                after = await self.inspect(before["Id"])
                if code != "0" or after["State"]["Status"] != "exited" or after["State"]["ExitCode"] != 0 or after["State"]["StartedAt"] != before["State"]["StartedAt"] or after["RestartCount"] != before["RestartCount"] or after["HostConfig"]["RestartPolicy"]["Name"] not in ("no", ""):
                    raise RuntimeError("Minecraft 未正常退出或容器状态改变，已取消系统关机")
                self.publish({"shutdown": "poweroff_requested"})
                args = ["systemctl", "poweroff"] if self.config["username"] == "root" else ["sudo", "-n", "systemctl", "poweroff"]
                try:
                    await self.execute(*args, timeout=15)
                except asyncssh.ConnectionLost:
                    logger.info("SSH disconnected after poweroff request")
            except Exception as exc:
                logger.warning("SSH shutdown stopped: %s", type(exc).__name__)
                if automatic and str(exc) in ("Shutdown request expired", "Shutdown conditions changed"):
                    self.publish({"shutdown": "none", "shutdown_error": None})
                else:
                    self.publish({"shutdown": "failed", "shutdown_error": str(exc)[:500]})

    async def idle_scheduler(self):
        tracker = IdleTracker()
        generation = None
        while True:
            self.changed.clear()
            policy = self.policy
            current_generation = (self.state.get("boot_id"), self.state.get("activity_version"))
            if generation != current_generation:
                tracker.update(ready=False, player_count=0, monotonic_now=time.monotonic())
                generation = current_generation
            ready = bool(policy["enabled"] and self.mod and self.state.get("minecraft") == "ready" and isinstance(self.state.get("online"), int) and isinstance(generation[0], str) and isinstance(generation[1], int) and self.state.get("shutdown") not in ("preparing", "poweroff_requested", "failed"))
            tracker.update(ready=ready, player_count=self.state.get("online") or 0, monotonic_now=time.monotonic())
            elapsed = tracker.elapsed(time.monotonic())
            self.update({"idle_since": None if elapsed is None else time.time() - elapsed})
            now = datetime.now(ZoneInfo("Asia/Hong_Kong"))
            idle_policy = IdlePolicy(day_timeout=timedelta(minutes=policy["day_minutes"]), night_timeout=timedelta(minutes=policy["night_minutes"]), night_start=clock_time.fromisoformat(policy["night_start"]), day_start=clock_time.fromisoformat(policy["day_start"]))
            if elapsed is not None and idle_policy.is_due(now, elapsed):
                boundaries = [datetime.combine(now.date() + timedelta(days=day), boundary, tzinfo=now.tzinfo) for day in (0, 1) for boundary in (idle_policy.day_start, idle_policy.night_start)]
                expiry = min(int(now.timestamp() * 1000) + 10000, int(min(point for point in boundaries if point > now).timestamp() * 1000))
                await self.shutdown({"boot_id": generation[0], "activity_version": generation[1], "min_idle_seconds": int(idle_policy.threshold(now).total_seconds()), "expires_at_ms": expiry})
                generation = None
                continue
            if elapsed is None:
                await self.changed.wait()
            else:
                boundaries = [datetime.combine(now.date() + timedelta(days=day), boundary, tzinfo=now.tzinfo) for day in (0, 1) for boundary in (idle_policy.day_start, idle_policy.night_start)]
                wait = min(idle_policy.threshold(now).total_seconds() - elapsed, min((point - now).total_seconds() for point in boundaries if point > now))
                try:
                    await asyncio.wait_for(self.changed.wait(), max(0.01, wait))
                except TimeoutError:
                    pass

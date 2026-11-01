import asyncio
import json
import logging
import os
import re
import time
import uuid
from pathlib import Path
from datetime import datetime, time as clock_time, timedelta
from zoneinfo import ZoneInfo

from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed
from .idle import IdlePolicy, IdleTracker
from .metrics import cpu_percent, sample
from .shutdown import inspect_container, shutdown_host

logger = logging.getLogger("mc_agent")
state = {"host": "online", "minecraft": "unknown", "shutdown": "none"}
changed = asyncio.Event()
mod_socket = None
backend_socket = None
backend_send_lock = asyncio.Lock()
shutdown_lock = asyncio.Lock()
idle_changed = asyncio.Event()
log_changed = asyncio.Event()
mod_pending: dict[str, asyncio.Future] = {}
policy_config = IdlePolicy()
policy_enabled = False


def apply_policy(data, *, acknowledge_failure=False):
    global policy_config, policy_enabled
    if shutdown_lock.locked() and state.get("shutdown") in ("preparing", "poweroff_requested"):
        raise RuntimeError("Shutdown in progress; policy is not yet applied")
    day = int(data["day_minutes"])
    night = int(data["night_minutes"])
    revision = int(data["revision"])
    enabled = data["enabled"]
    if not 1 <= day <= 1440 or not 1 <= night <= 1440 or revision < 1 or type(enabled) not in (bool, int) or enabled not in (0, 1):
        raise ValueError("Invalid policy values")
    updated_policy = IdlePolicy(day_timeout=timedelta(minutes=day), night_timeout=timedelta(minutes=night), night_start=clock_time.fromisoformat(data["night_start"]), day_start=clock_time.fromisoformat(data["day_start"]))
    policy_config = updated_policy
    policy_enabled = bool(enabled) and os.environ.get("MC_AGENT_AUTO_SHUTDOWN") == "true"
    values = {"policy_revision": revision, "policy_enabled": policy_enabled, "idle_policy": {"day_minutes": day, "night_minutes": night, "night_start": data["night_start"], "day_start": data["day_start"], "timezone": "Asia/Hong_Kong"}}
    if acknowledge_failure and state.get("shutdown") == "failed":
        values.update({"shutdown": "none", "shutdown_error": None})
    set_state(values)
    idle_changed.set()


async def start_container():
    name = os.environ["MC_AGENT_CONTAINER"]
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}", name):
        raise ValueError("Invalid configured container name")
    process = await asyncio.create_subprocess_exec("docker", "start", name, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        _, stderr = await asyncio.wait_for(process.communicate(), 25)
    except TimeoutError:
        process.kill()
        await process.wait()
        raise RuntimeError("Docker start timed out")
    if process.returncode != 0:
        raise RuntimeError("Docker start failed: " + stderr.decode(errors="replace")[:500])


async def start_container_safely():
    if shutdown_lock.locked() or state.get("shutdown") in ("preparing", "poweroff_requested"):
        raise RuntimeError("Shutdown in progress")
    async with shutdown_lock:
        if state.get("shutdown") in ("preparing", "poweroff_requested"):
            raise RuntimeError("Shutdown in progress")
        await start_container()


async def monitor_container():
    name = os.environ["MC_AGENT_CONTAINER"]
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}", name):
        raise ValueError("Invalid configured container name")
    delay = 1
    while True:
        process = None
        connected_at = asyncio.get_running_loop().time()
        try:
            process = await asyncio.create_subprocess_exec("docker", "events", "--filter", f"container={name}", "--format", "{{json .}}", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
            async def refresh():
                try:
                    _, details = await inspect_container(name)
                    set_state({"container": details["Status"], "container_exit_code": details["ExitCode"], "container_started_at": details["StartedAt"]})
                except (OSError, RuntimeError, KeyError, ValueError):
                    logger.exception("Cannot inspect Minecraft container")
                    set_state({"container": "unknown"})
            await refresh()
            async for line in process.stdout:
                delay = 1
                event = json.loads(line)
                if event.get("Action") in ("start", "stop", "die", "restart", "pause", "unpause", "destroy"):
                    await refresh()
            await process.wait()
            logger.warning("Docker event stream stopped with code %s", process.returncode)
        except (OSError, ValueError):
            logger.exception("Docker event stream failed")
        finally:
            set_state({"container": "unknown", "container_exit_code": None, "container_started_at": None})
            if process is not None and process.returncode is None:
                process.terminate()
                await process.wait()
        if asyncio.get_running_loop().time() - connected_at >= 30:
            delay = 1
        await asyncio.sleep(delay)
        delay = min(delay * 2, 30)


async def monitor_host():
    previous = None
    while True:
        try:
            current = await asyncio.to_thread(sample)
            set_state({"host_cpu": cpu_percent(previous, current) if previous else None, "host_memory_used": current[2] - current[3], "host_memory_max": current[2]})
            previous = current
        except (OSError, ValueError, KeyError, IndexError):
            logger.exception("Host metrics unavailable")
            previous = None
            set_state({"host_cpu": None, "host_memory_used": None, "host_memory_max": None})
        await asyncio.sleep(10)


def set_state(values):
    if any(state.get(key) != value for key, value in values.items()):
        minecraft_changed = "minecraft" in values and values["minecraft"] != state.get("minecraft")
        state.update(values)
        changed.set()
        idle_changed.set()
        if minecraft_changed:
            log_changed.set()


async def follow_logs(ws):
    name = os.environ["MC_AGENT_CONTAINER"]
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}", name):
        raise ValueError("Invalid configured container name")
    async def emit(raw, truncated=False):
        text = raw.decode(errors="replace").rstrip("\r")
        if truncated:
            text += "… [truncated]"
        for key in ("MC_AGENT_TOKEN", "COMMAND_API_TOKEN"):
            secret = os.environ.get(key)
            if secret:
                text = text.replace(secret, "[REDACTED]")
        async with backend_send_lock:
            await ws.send(json.dumps({"type": "log", "line": text}))
    while True:
        log_changed.clear()
        try:
            process = await asyncio.create_subprocess_exec("docker", "logs", "--follow", "--tail", "100", name, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        except OSError as exc:
            logger.error("Cannot read Docker logs: %s", exc)
            await emit(b"Docker logs unavailable")
            await log_changed.wait()
            continue
        try:
            buffer = bytearray()
            truncated = False
            while chunk := await process.stdout.read(4096):
                parts = chunk.split(b"\n")
                for index, part in enumerate(parts):
                    capacity = max(0, 4000 - len(buffer))
                    buffer.extend(part[:capacity])
                    truncated = truncated or len(part) > capacity
                    if index < len(parts) - 1:
                        await emit(buffer, truncated)
                        buffer.clear()
                        truncated = False
            if buffer or truncated:
                await emit(buffer, truncated)
            await process.wait()
        finally:
            if process.returncode is None:
                try:
                    process.terminate()
                except ProcessLookupError:
                    pass
                await process.wait()
        await log_changed.wait()


async def mod_connection():
    global mod_socket
    url = os.environ["MC_AGENT_MOD_WS"]
    token = os.environ["COMMAND_API_TOKEN"]
    delay = 1
    while True:
        try:
            async with connect(url, additional_headers={"Authorization": "Bearer " + token}, ping_interval=20, ping_timeout=20, max_queue=32) as ws:
                delay = 1
                mod_socket = ws
                async for payload in ws:
                    message = json.loads(payload)
                    if message.get("type") == "status":
                        fields = ("minecraft", "minecraft_version", "neoforge_version", "mod_version", "online", "max_players", "players", "boot_id", "activity_version", "uptime_seconds", "mspt", "tps", "memory_used", "memory_max")
                        set_state({key: message.get(key) for key in fields})
                    elif message.get("type") == "response":
                        future = mod_pending.get(message.get("id"))
                        if future is not None and not future.done():
                            future.set_result(message)
                        elif backend_socket is not None:
                            async with backend_send_lock:
                                await backend_socket.send(payload)
        except (OSError, ConnectionClosed) as exc:
            logger.warning("Mod connection lost: %s", exc)
        finally:
            mod_socket = None
            for future in tuple(mod_pending.values()):
                if not future.done():
                    future.set_exception(ConnectionError("Minecraft connection lost"))
        set_state({"minecraft": "unknown", "minecraft_version": None, "neoforge_version": None, "mod_version": None, "online": None, "max_players": None, "players": [], "boot_id": None, "activity_version": None, "uptime_seconds": None, "mspt": None, "tps": None, "memory_used": None, "memory_max": None})
        await asyncio.sleep(delay)
        delay = min(delay * 2, 30)


async def backend_connection():
    global backend_socket
    url = os.environ["MC_AGENT_BACKEND_WS"]
    token = os.environ["MC_AGENT_TOKEN"]
    delay = 1
    while True:
        try:
            async with connect(url, additional_headers={"Authorization": "Bearer " + token}, ping_interval=20, ping_timeout=20, max_queue=32) as ws:
                delay = 1
                backend_socket = ws
                log_task = None
                changed.set()
                async def send_changes():
                    while True:
                        await changed.wait()
                        changed.clear()
                        async with backend_send_lock:
                            await ws.send(json.dumps({"type": "status", "data": state}))
                sender = asyncio.create_task(send_changes())
                try:
                    async for message in ws:
                        request = json.loads(message)
                        if request.get("type") in ("command", "completion") and "id" in request:
                            peer = mod_socket
                            if peer is None:
                                async with backend_send_lock:
                                    await ws.send(json.dumps({"type": "response", "id": request["id"], "error": "Minecraft is unavailable"}))
                            else:
                                try:
                                    await peer.send(message)
                                except ConnectionClosed:
                                    async with backend_send_lock:
                                        await ws.send(json.dumps({"type": "response", "id": request["id"], "error": "Minecraft connection lost; outcome may be unknown"}))
                        elif request.get("type") == "start_container" and "id" in request:
                            try:
                                await start_container_safely()
                                log_changed.set()
                                reply = {"type": "response", "id": request["id"]}
                            except (OSError, RuntimeError, ValueError, KeyError) as exc:
                                reply = {"type": "response", "id": request["id"], "error": str(exc)}
                            async with backend_send_lock:
                                await ws.send(json.dumps(reply))
                        elif request.get("type") == "logs_subscribe":
                            if request.get("enabled") is True and (log_task is None or log_task.done()):
                                log_task = asyncio.create_task(follow_logs(ws))
                            elif request.get("enabled") is False and log_task is not None:
                                log_task.cancel()
                                await asyncio.gather(log_task, return_exceptions=True)
                                log_task = None
                        elif request.get("type") == "set_policy":
                            try:
                                apply_policy(request["policy"], acknowledge_failure="id" in request)
                                reply = {"type": "response", "id": request.get("id"), "applied": True, "effective_enabled": policy_enabled}
                            except (ValueError, KeyError, TypeError, RuntimeError) as exc:
                                reply = {"type": "response", "id": request.get("id"), "error": str(exc)}
                            if request.get("id"):
                                async with backend_send_lock:
                                    await ws.send(json.dumps(reply))
                        elif request.get("type") == "shutdown_manual" and "id" in request:
                            if shutdown_lock.locked():
                                reply = {"type": "response", "id": request["id"], "error": "Shutdown already in progress"}
                            else:
                                asyncio.create_task(manual_shutdown())
                                reply = {"type": "response", "id": request["id"], "accepted": True}
                            async with backend_send_lock:
                                await ws.send(json.dumps(reply))
                finally:
                    backend_socket = None
                    if log_task is not None:
                        log_task.cancel()
                        await asyncio.gather(log_task, return_exceptions=True)
                    sender.cancel()
                    await asyncio.gather(sender, return_exceptions=True)
        except (OSError, ConnectionClosed) as exc:
            logger.warning("Backend connection lost: %s", exc)
        await asyncio.sleep(delay)
        delay = min(delay * 2, 30)


async def run():
    try:
        set_state({"host_boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip()})
    except OSError:
        logger.exception("Host boot ID unavailable")
    await asyncio.gather(mod_connection(), backend_connection(), idle_scheduler(), monitor_container(), monitor_host())


async def request_mod_shutdown(boot_id: str, revision: int, min_idle_seconds: int, expires_at_ms: int):
    peer = mod_socket
    if peer is None:
        raise ConnectionError("Minecraft connection unavailable")
    request_id = "auto-" + uuid.uuid4().hex
    future = asyncio.get_running_loop().create_future()
    mod_pending[request_id] = future
    try:
        await peer.send(json.dumps({"type": "shutdown", "id": request_id, "boot_id": boot_id, "activity_version": revision, "min_idle_seconds": min_idle_seconds, "expires_at_ms": expires_at_ms}))
        response = await asyncio.wait_for(future, 10)
        if response.get("error"):
            raise RuntimeError(response["error"])
    finally:
        mod_pending.pop(request_id, None)


async def request_mod_manual_shutdown():
    peer = mod_socket
    if peer is None:
        raise ConnectionError("Minecraft connection unavailable")
    request_id = "manual-" + uuid.uuid4().hex
    future = asyncio.get_running_loop().create_future()
    mod_pending[request_id] = future
    try:
        await peer.send(json.dumps({"type": "shutdown_manual", "id": request_id}))
        response = await asyncio.wait_for(future, 75)
        if response.get("error"):
            raise RuntimeError(response["error"])
    finally:
        mod_pending.pop(request_id, None)


async def manual_shutdown():
    async with shutdown_lock:
        try:
            logger.info("Manual shutdown requested")
            set_state({"shutdown": "preparing", "shutdown_kind": "manual", "shutdown_error": None})
            await shutdown_host(os.environ["MC_AGENT_CONTAINER"], request_mod_manual_shutdown)
            set_state({"shutdown": "poweroff_requested"})
        except (OSError, RuntimeError, ValueError, KeyError, ConnectionError, TimeoutError, ConnectionClosed) as exc:
            logger.exception("Manual shutdown stopped")
            set_state({"shutdown": "failed", "shutdown_error": str(exc)[:500]})


async def idle_scheduler():
    tracker = IdleTracker()
    revision = None
    boot_id = None
    published_idle_start = None
    while True:
        policy = policy_config
        if state.get("shutdown") in ("preparing", "poweroff_requested", "failed"):
            tracker.update(ready=False, player_count=0, monotonic_now=time.monotonic())
            if published_idle_start is not None:
                published_idle_start = None
                set_state({"idle_since": None})
            idle_changed.clear()
            await idle_changed.wait()
            continue
        if not policy_enabled:
            tracker.update(ready=False, player_count=0, monotonic_now=time.monotonic())
            if published_idle_start is not None:
                published_idle_start = None
                set_state({"idle_since": None})
            idle_changed.clear()
            await idle_changed.wait()
            continue
        current_revision = state.get("activity_version")
        current_boot = state.get("boot_id")
        ready = state.get("minecraft") == "ready" and mod_socket is not None and isinstance(state.get("online"), int) and isinstance(current_revision, int) and isinstance(current_boot, str)
        if current_revision != revision or current_boot != boot_id:
            tracker.update(ready=False, player_count=0, monotonic_now=time.monotonic())
            revision, boot_id = current_revision, current_boot
        tracker.update(ready=ready, player_count=state.get("online") or 0, monotonic_now=time.monotonic())
        elapsed = tracker.elapsed(time.monotonic())
        if tracker.idle_since != published_idle_start:
            published_idle_start = tracker.idle_since
            set_state({"idle_since": None if elapsed is None else time.time() - elapsed})
        now = datetime.now().astimezone()
        if elapsed is not None and policy.is_due(now, elapsed):
            try:
                async with shutdown_lock:
                    if state.get("shutdown") in ("preparing", "poweroff_requested"):
                        continue
                    logger.info("Automatic idle shutdown requested")
                    set_state({"shutdown": "preparing", "shutdown_kind": "automatic", "shutdown_error": None})
                    async def recheck_and_shutdown():
                        latest = datetime.now().astimezone()
                        current_elapsed = tracker.elapsed(time.monotonic())
                        active_policy = policy_config
                        if not policy_enabled or current_elapsed is None or not active_policy.is_due(latest, current_elapsed):
                            raise RuntimeError("Idle threshold changed")
                        local_latest = latest.astimezone(ZoneInfo(active_policy.timezone))
                        boundaries = [datetime.combine(local_latest.date() + timedelta(days=day), boundary, tzinfo=local_latest.tzinfo) for day in (0, 1) for boundary in (active_policy.day_start, active_policy.night_start)]
                        next_boundary = min(boundary for boundary in boundaries if boundary > local_latest)
                        expiry = min(int(latest.timestamp() * 1000) + 10000, int(next_boundary.timestamp() * 1000))
                        await request_mod_shutdown(boot_id, revision, int(active_policy.threshold(latest).total_seconds()), expiry)
                    await shutdown_host(os.environ["MC_AGENT_CONTAINER"], recheck_and_shutdown)
            except (OSError, RuntimeError, ValueError, KeyError, ConnectionError, TimeoutError, ConnectionClosed) as exc:
                if str(exc) in ("Shutdown request expired", "Shutdown conditions changed"):
                    logger.info("Automatic shutdown cancelled: %s", exc)
                    set_state({"shutdown": "none", "shutdown_error": None})
                else:
                    logger.exception("Automatic shutdown stopped")
                    set_state({"shutdown": "failed", "shutdown_error": str(exc)[:500]})
                if str(exc) != "Shutdown request expired":
                    tracker.update(ready=False, player_count=0, monotonic_now=time.monotonic())
            else:
                set_state({"shutdown": "poweroff_requested"})
                return
        idle_changed.clear()
        try:
            if elapsed is None:
                await idle_changed.wait()
            else:
                local_now = datetime.now(ZoneInfo(policy.timezone))
                boundaries = [datetime.combine(local_now.date() + timedelta(days=day), boundary, tzinfo=local_now.tzinfo) for day in (0, 1) for boundary in (policy.day_start, policy.night_start)]
                until_boundary = min((boundary - local_now).total_seconds() for boundary in boundaries if boundary > local_now)
                remaining = policy.threshold(local_now).total_seconds() - elapsed
                await asyncio.wait_for(idle_changed.wait(), max(0.01, min(remaining, until_boundary)))
        except TimeoutError:
            pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())

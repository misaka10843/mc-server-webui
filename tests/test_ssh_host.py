import asyncio
import json
import unittest

import asyncssh
from websockets.asyncio.server import serve

from app.ssh_host import SSHHost, connection_options


class SSHHostTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.commands = []
        self.exited = False
        self.exit_code = 0
        self.poweroff = False
        self.ready = asyncio.Event()
        self.state = {"shutdown": "none"}
        self.policy = {"revision": 1, "enabled": False, "day_minutes": 90, "night_minutes": 30, "night_start": "23:30", "day_start": "09:00"}

        async def mod(ws):
            self.assertEqual(ws.request.path, "/ws")
            self.assertEqual(ws.request.headers["Authorization"], "Bearer mod-secret")
            await ws.send(json.dumps({"type": "status", "minecraft": "ready", "online": 0, "boot_id": "boot", "activity_version": 1}))
            async for raw in ws:
                request = json.loads(raw)
                if request["type"] in ("shutdown", "shutdown_manual"):
                    self.exited = True
                await ws.send(json.dumps({"type": "response", "id": request["id"], "output": ["ok"]}))

        self.mod_server = await serve(mod, "127.0.0.1", 0)
        mod_port = self.mod_server.sockets[0].getsockname()[1]

        class Server(asyncssh.SSHServer):
            def begin_auth(self, username):
                return True

            def password_auth_supported(self):
                return True

            def validate_password(self, username, password):
                return username == "tester" and password == "ssh-password"

            def connection_requested(self, dest_host, dest_port, orig_host, orig_port):
                return dest_host == "127.0.0.1" and dest_port == mod_port

        async def process(proc):
            self.commands.append(proc.command)
            if proc.command.startswith("docker inspect"):
                details = {"Id": "container-id", "State": {"Status": "exited" if self.exited else "running", "ExitCode": self.exit_code, "StartedAt": "same-start"}, "RestartCount": 0, "HostConfig": {"RestartPolicy": {"Name": "no"}}}
                proc.stdout.write(json.dumps(details))
            elif proc.command.startswith("cat "):
                proc.stdout.write("host-boot")
            elif proc.command.startswith("docker events") or proc.command.startswith("docker logs"):
                await proc.wait_closed()
                return
            elif proc.command.startswith("docker wait"):
                proc.stdout.write(str(self.exit_code))
            elif "systemctl poweroff" in proc.command:
                self.poweroff = True
            proc.exit(0)

        self.host_key = asyncssh.generate_private_key("ssh-ed25519")
        self.server = await asyncssh.create_server(Server, "127.0.0.1", 0, server_host_keys=[self.host_key], process_factory=process)
        self.config = {"host": "127.0.0.1", "port": self.server.get_port(), "username": "tester", "password": "ssh-password", "private_key": "", "host_key": self.host_key.export_public_key().decode(), "container": "minecraft", "mod_port": mod_port, "mod_token": "mod-secret"}

        def update(values):
            self.state.update(values)
            if self.state.get("minecraft") == "ready":
                self.ready.set()

        self.host = SSHHost(self.config, self.state, update, lambda line: None, self.policy)

    async def asyncTearDown(self):
        self.mod_server.close()
        await self.host.close()
        self.server.close()
        await self.server.wait_closed()
        await self.mod_server.wait_closed()

    async def test_ssh_tunnel_mod_command_and_safe_shutdown(self):
        await self.host.start()
        await asyncio.wait_for(self.ready.wait(), 5)
        self.assertEqual(self.state["host"], "online")
        response = await self.host.request("command", {"input": "list"}, 5)
        self.assertEqual(response["output"], ["ok"])
        await self.host.shutdown()
        self.assertTrue(self.poweroff)
        self.assertEqual(self.state["shutdown"], "poweroff_requested")
        self.assertTrue(any(command.startswith("docker wait") for command in self.commands))

    async def test_nonzero_minecraft_exit_never_powers_off(self):
        await self.host.start()
        await asyncio.wait_for(self.ready.wait(), 5)
        self.exit_code = 1
        await self.host.shutdown()
        self.assertFalse(self.poweroff)
        self.assertEqual(self.state["shutdown"], "failed")

    async def test_wrong_host_key_is_rejected(self):
        config = {**self.config, "host_key": asyncssh.generate_private_key("ssh-ed25519").export_public_key().decode()}
        with self.assertRaises(asyncssh.HostKeyNotVerifiable):
            async with asyncssh.connect(**connection_options(config)):
                self.fail("Untrusted server was accepted")

import os
import tempfile
import threading
import time
from datetime import datetime, timedelta, timezone
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

from fastapi.testclient import TestClient

from app import db
from app.main import app
from app import main


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        db.DB_PATH = Path(self.tmp.name) / "test.sqlite3"
        os.environ["MCWEB_AGENT_TOKEN"] = "test-agent-token"
        self.client = TestClient(app)
        self.client.__enter__()
        main.state.clear()
        main.state.update({"host": "unknown", "minecraft": "unknown", "plug": "unknown"})
        main.current_operation = None
        main.start_attempts.clear()
        main.login_attempts.clear()
        with db.connect() as conn:
            conn.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)", ("admin", db.passwords.hash("long-enough-password"), "admin"))
            conn.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)", ("user", db.passwords.hash("long-enough-password"), "user"))

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.tmp.cleanup()

    def login(self, username):
        return self.client.post("/api/v1/auth/login", headers={"Origin": "http://testserver"}, json={"username": username, "password": "long-enough-password"})

    def headers(self):
        return {"Origin": "http://testserver", "X-CSRF-Token": self.client.cookies.get("mc_csrf", "")}

    def test_first_run_setup_creates_admin_and_starts_session(self):
        with db.connect() as conn:
            conn.execute("DELETE FROM users")
        self.assertTrue(self.client.get("/api/v1/setup").json()["required"])
        response = self.client.post("/api/v1/setup", headers={"Origin": "http://testserver"}, json={"username": "owner", "password": "eight888"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["role"], "admin")
        self.assertEqual(self.client.get("/api/v1/auth/me").json()["username"], "owner")
        self.assertFalse(self.client.get("/api/v1/setup").json()["required"])
        self.assertEqual(self.client.post("/api/v1/setup", headers={"Origin": "http://testserver"}, json={"username": "second", "password": "eight888"}).status_code, 409)

    def test_setup_is_atomic_when_two_browsers_initialize(self):
        from concurrent.futures import ThreadPoolExecutor
        with db.connect() as conn:
            conn.execute("DELETE FROM users")
        def initialize(name):
            client = TestClient(app, raise_server_exceptions=True)
            try:
                return client.post("/api/v1/setup", headers={"Origin": "http://testserver"}, json={"username": name, "password": "eight888"}).status_code
            finally:
                client.close()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(initialize, ["first", "second"]))
        self.assertEqual(sorted(results), [200, 409])
        with db.connect() as conn:
            self.assertEqual(conn.execute("SELECT count(*) FROM users WHERE role='admin'").fetchone()[0], 1)

    def test_saving_unchanged_account_preserves_its_session(self):
        self.login("admin")
        account = self.client.get("/api/v1/auth/me").json()
        response = self.client.put(f"/api/v1/admin/users/{account['id']}", headers=self.headers(), json={"role": "admin", "enabled": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/api/v1/auth/me").status_code, 200)

    def test_https_frontend_works_behind_http_proxy_without_forwarded_headers(self):
        response = self.client.post("/api/v1/auth/login", headers={"Host": "mc.example.test", "Origin": "https://mc.example.test"}, json={"username": "admin", "password": "long-enough-password"})
        self.assertEqual(response.status_code, 200)
        rejected = self.client.post("/api/v1/auth/login", headers={"Host": "mc.example.test", "Origin": "https://evil.example.test"}, json={"username": "admin", "password": "long-enough-password"})
        self.assertEqual(rejected.status_code, 403)

    def test_first_ssh_save_remembers_host_key_without_manual_probe(self):
        import asyncssh
        key = asyncssh.generate_private_key("ssh-ed25519")
        self.login("admin")
        payload = {"host": "192.168.101.41", "username": "tester", "password": "ssh-secret", "container": "minecraft", "mod_token": "mod-secret"}
        with patch("app.main.asyncssh.get_server_host_key", new_callable=AsyncMock, return_value=key) as probe, patch("app.main.SSHHost.start", new_callable=AsyncMock), patch("app.main.SSHHost.subscribe_logs", new_callable=AsyncMock), patch("app.main.asyncssh.connect") as connect_mock:
            self.assertEqual(self.client.put("/api/v1/admin/ssh", headers=self.headers(), json=payload).status_code, 200)
            self.assertTrue(self.client.get("/api/v1/admin/ssh").json()["host_key"].startswith("ssh-ed25519"))
            payload["password"] = ""
            payload["mod_token"] = ""
            self.assertEqual(self.client.put("/api/v1/admin/ssh", headers=self.headers(), json=payload).status_code, 200)
            self.assertEqual(probe.await_count, 1)
            connect_mock.assert_not_called()

    def test_ssh_configuration_is_admin_only_and_secrets_are_hidden(self):
        import asyncssh
        self.login("user")
        self.assertEqual(self.client.get("/api/v1/admin/ssh").status_code, 403)
        self.client.post("/api/v1/auth/logout", headers=self.headers())
        self.login("admin")
        public_key = asyncssh.generate_private_key("ssh-ed25519").export_public_key().decode()
        payload = {"host": "192.168.101.41", "port": 22, "username": "tester", "password": "ssh-secret", "host_key": public_key, "container": "minecraft", "mod_token": "mod-secret"}
        connection = MagicMock()
        connection.run = AsyncMock(return_value=MagicMock(stdout='{"Status":"running"}'))
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=connection)
        context.__aexit__ = AsyncMock(return_value=False)
        with patch("app.main.asyncssh.connect", return_value=context), patch("app.main.SSHHost.start", new_callable=AsyncMock), patch("app.main.SSHHost.subscribe_logs", new_callable=AsyncMock):
            response = self.client.put("/api/v1/admin/ssh", headers=self.headers(), json=payload)
            self.assertEqual(response.status_code, 200, response.text)
            value = self.client.get("/api/v1/admin/ssh").json()
            self.assertEqual(value["host"], "192.168.101.41")
            for key in ("password", "private_key", "mod_token"):
                self.assertNotIn(key, value)
            payload["password"] = ""
            payload["mod_token"] = ""
            self.assertEqual(self.client.put("/api/v1/admin/ssh", headers=self.headers(), json=payload).status_code, 200)
            self.assertEqual(main.ssh_host.config["password"], "ssh-secret")

    def test_authentication_role_and_origin(self):
        self.assertEqual(self.client.get("/api/v1/server/status").status_code, 401)
        self.assertEqual(self.login("user").status_code, 200)
        self.assertEqual(self.client.get("/api/v1/server/status").status_code, 200)
        self.assertEqual(self.client.post("/api/v1/admin/users", headers={"Origin": "http://testserver"}, json={"username": "new", "password": "long-enough-password", "role": "user"}).status_code, 403)
        self.assertEqual(self.client.post("/api/v1/auth/logout", headers={"Origin": "http://evil"}).status_code, 403)
        self.assertEqual(self.client.post("/api/v1/auth/logout", headers={"Origin": "http://testserver"}).status_code, 403)
        self.assertEqual(self.client.post("/api/v1/auth/logout", headers=self.headers()).status_code, 200)
        self.assertEqual(self.client.get("/api/v1/auth/me").status_code, 401)

    def test_plug_configuration_permission_validation_and_secret(self):
        self.login("user")
        payload = {"ip": "192.168.1.20", "token": "a" * 32, "model": "test.plug", "siid": 2, "piid": 1}
        self.assertEqual(self.client.put("/api/v1/admin/plug", headers=self.headers(), json=payload).status_code, 403)
        self.client.post("/api/v1/auth/logout", headers=self.headers())
        self.login("admin")
        with patch("app.main.Plug") as device:
            device.return_value.status.return_value = True
            response = self.client.put("/api/v1/admin/plug", headers=self.headers(), json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("token", self.client.get("/api/v1/admin/plug").json())
            device.return_value.status.side_effect = RuntimeError("offline")
            payload["ip"] = "192.168.1.21"
            self.assertEqual(self.client.put("/api/v1/admin/plug", headers=self.headers(), json=payload).status_code, 502)
            self.assertEqual(self.client.get("/api/v1/admin/plug").json()["ip"], "192.168.1.20")

    def test_qr_discovery_stream_requires_admin_and_returns_devices(self):
        self.login("user")
        self.assertEqual(self.client.post("/api/v1/admin/plug/qr", headers=self.headers(), json={"locale": "cn"}).status_code, 403)
        self.client.post("/api/v1/auth/logout", headers=self.headers())
        self.login("admin")
        with patch("mihome_ctl.connector.QrCodeXiaomiCloudConnector") as connector, patch("mihome_ctl.core.cloudapi.collect") as collect, patch("app.main.wait_for_scan", return_value=True):
            instance = connector.return_value
            instance.login_step_1.return_value = True
            instance.login_step_3.return_value = True
            instance.login_step_4.return_value = True
            instance._session.get.return_value.content = b"image"
            instance.userId = "123"
            instance._ssecurity = "security"
            instance._serviceToken = "service-token"
            collect.return_value = [{"name": "插座", "model": "test.plug", "did": "12345", "localip": "192.168.1.2", "token": "a" * 32}]
            response = self.client.post("/api/v1/admin/plug/qr", headers=self.headers(), json={"locale": "cn"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("event: qr", response.text)
            self.assertIn("event: devices", response.text)
            self.assertIn("test.plug", response.text)
            self.assertNotIn("service-token", response.text)
            self.assertNotIn("a" * 32, response.text)
            instance._session.close.assert_called_once()

    def test_cloud_plug_save_and_restore(self):
        self.login("admin")
        main.cloud_discoveries["selection"] = {"user": 1, "expires": time.monotonic() + 60, "region": "cn", "session": ("123", "secret", "service-token"), "devices": {"did": {"model": "cuco.plug.v3"}}}
        payload = {"discovery": "selection", "did": "did", "siid": 2, "piid": 1}
        with patch("app.plug.api", return_value={"code": 0, "result": [{"code": 0, "value": True}]}) as cloud:
            result = self.client.put("/api/v1/admin/plug/cloud", headers=self.headers(), json=payload)
            self.assertEqual(result.status_code, 200)
            self.assertEqual(self.client.get("/api/v1/admin/plug").json()["mode"], "cloud")
            self.assertEqual(self.client.post("/api/v1/server/plug/refresh", headers=self.headers()).json()["plug"], "on")
            self.assertEqual(cloud.call_args.args[2], "/miotspec/prop/get")
            main.plug.on()
            self.assertEqual(cloud.call_args.args[2], "/miotspec/prop/set")
            with db.connect() as conn:
                row = conn.execute("SELECT did, region, siid, piid, user_id, security, service_token FROM cloud_plug").fetchone()
            self.assertTrue(main.CloudPlug(**dict(row)).status())

    def test_multiple_same_origin_addresses_and_cross_origin_rejection(self):
        credentials = {"username": "user", "password": "long-enough-password"}
        for address in ("http://192.168.101.2:8080", "http://203.0.113.10:19080"):
            with self.subTest(address=address):
                client = TestClient(app, base_url=address)
                login = client.post("/api/v1/auth/login", headers={"Origin": address}, json=credentials)
                self.assertEqual(login.status_code, 200)
                csrf = client.cookies.get("mc_csrf")
                self.assertEqual(client.get("/api/v1/auth/me").status_code, 200)
                wrong_origin = "http://203.0.113.11:19080" if "192.168" in address else "http://192.168.101.2:8080"
                rejected = client.post("/api/v1/auth/logout", headers={"Origin": wrong_origin, "X-CSRF-Token": csrf})
                self.assertEqual(rejected.status_code, 403)
                self.assertEqual(client.post("/api/v1/auth/logout", headers={"Origin": address, "X-CSRF-Token": csrf}).status_code, 200)
                client.close()

    def test_proxy_preserves_external_host_and_port(self):
        headers = {"Host": "203.0.113.10:19080", "Origin": "http://203.0.113.10:19080"}
        response = self.client.post("/api/v1/auth/login", headers=headers, json={"username": "user", "password": "long-enough-password"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.post("/api/v1/auth/login", headers={**headers, "Origin": "http://203.0.113.10:8080"}, json={"username": "user", "password": "long-enough-password"}).status_code, 403)

    def test_admin_creates_user_and_duplicate_rejected(self):
        self.assertEqual(self.login("admin").status_code, 200)
        payload = {"username": "friend", "password": "long-enough-password", "role": "user"}
        headers = self.headers()
        self.assertEqual(self.client.post("/api/v1/admin/users", headers=headers, json=payload).status_code, 200)
        self.assertEqual(self.client.post("/api/v1/admin/users", headers=headers, json=payload).status_code, 409)

    def test_agent_status_and_disconnect(self):
        self.login("user")
        with self.client.websocket_connect("/internal/v1/agent", headers={"Authorization": "Bearer test-agent-token"}) as ws:
            ws.send_json({"type": "status", "data": {"host": "online"}})
            self.assertEqual(self.client.get("/api/v1/server/status").json()["host"], "online")
        self.assertEqual(self.client.get("/api/v1/server/status").json()["host"], "unknown")

    def test_only_admin_can_run_commands_and_response_is_correlated(self):
        self.login("user")
        headers = self.headers()
        self.assertEqual(self.client.post("/api/v1/admin/commands", headers=headers, json={"input": "list"}).status_code, 403)
        self.client.post("/api/v1/auth/logout", headers=headers)
        self.login("admin")
        headers = self.headers()
        result = []
        with self.client.websocket_connect("/internal/v1/agent", headers={"Authorization": "Bearer test-agent-token"}) as ws:
            self.assertEqual(ws.receive_json()["type"], "set_policy")
            thread = threading.Thread(target=lambda: result.append(self.client.post("/api/v1/admin/commands", headers=headers, json={"input": "list"})))
            thread.start()
            msg = ws.receive_json()
            self.assertEqual(msg["type"], "command")
            ws.send_json({"type": "response", "id": msg["id"], "output": ["There are no players"]})
            thread.join(5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(result[0].json()["output"], ["There are no players"])
            audit = self.client.get("/api/v1/admin/audit").json()["events"]
            self.assertTrue(any(event["action"] == "command_result" and "completed" in event["detail"] for event in audit))

    def test_last_admin_cannot_be_disabled_and_user_sessions_revoked(self):
        self.login("admin")
        headers = self.headers()
        me = self.client.get("/api/v1/auth/me").json()
        result = self.client.put(f"/api/v1/admin/users/{me['id']}", headers=headers, json={"role": "user", "enabled": False})
        self.assertEqual(result.status_code, 409)
        self.assertEqual(self.client.get("/api/v1/admin/policy").json()["day_minutes"], 90)
        self.assertEqual(self.client.put("/api/v1/admin/policy", headers=headers, json={"enabled": True, "day_minutes": 90, "night_minutes": 30, "night_start": "08:00", "day_start": "09:00"}).status_code, 422)
        other = TestClient(app)
        self.assertEqual(other.post("/api/v1/auth/login", headers={"Origin": "http://testserver"}, json={"username": "user", "password": "long-enough-password"}).status_code, 200)
        user_id = other.get("/api/v1/auth/me").json()["id"]
        self.assertEqual(self.client.put(f"/api/v1/admin/users/{user_id}", headers=headers, json={"role": "user", "enabled": False}).status_code, 200)
        self.assertEqual(other.get("/api/v1/auth/me").status_code, 401)
        other.close()

    def test_agent_disconnect_does_not_retry_command(self):
        self.login("admin")
        headers = self.headers()
        result = []
        with self.client.websocket_connect("/internal/v1/agent", headers={"Authorization": "Bearer test-agent-token"}) as ws:
            ws.receive_json()
            thread = threading.Thread(target=lambda: result.append(self.client.post("/api/v1/admin/commands", headers=headers, json={"input": "say once"})))
            thread.start()
            self.assertEqual(ws.receive_json()["type"], "command")
        thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(result[0].status_code, 503)
        self.assertIn("unknown", result[0].json()["detail"])

    def test_policy_is_saved_and_acknowledged_by_agent(self):
        self.login("admin")
        headers = self.headers()
        result = []
        payload = {"enabled": True, "day_minutes": 90, "night_minutes": 30, "night_start": "23:30", "day_start": "09:00"}
        with self.client.websocket_connect("/internal/v1/agent", headers={"Authorization": "Bearer test-agent-token"}) as ws:
            ws.receive_json()
            thread = threading.Thread(target=lambda: result.append(self.client.put("/api/v1/admin/policy", headers=headers, json=payload)))
            thread.start()
            message = ws.receive_json()
            self.assertEqual(message["type"], "set_policy")
            ws.send_json({"type": "response", "id": message["id"], "applied": True})
            thread.join(5)
            self.assertFalse(thread.is_alive())
            self.assertTrue(result[0].json()["applied"])
            self.assertEqual(result[0].json()["revision"], 2)

    def test_start_deduplicates_and_completes_after_agent_ready(self):
        class FakePlug:
            on_calls = 0
            def status(self): return False
            def on(self): self.on_calls += 1
        fake = FakePlug()
        main.plug = fake
        self.login("user")
        headers = self.headers()
        first = self.client.post("/api/v1/server/start", headers=headers).json()["id"]
        second = self.client.post("/api/v1/server/start", headers=headers).json()["id"]
        self.assertEqual(first, second)
        with self.client.websocket_connect("/internal/v1/agent", headers={"Authorization": "Bearer test-agent-token"}) as ws:
            ws.receive_json()
            ws.send_json({"type": "status", "data": {"host": "online", "minecraft": "ready"}})
            for _ in range(50):
                result = self.client.get(f"/api/v1/operations/{first}").json()
                if result["status"] != "running": break
                time.sleep(0.02)
            self.assertEqual(result["status"], "complete")
            self.assertEqual(fake.on_calls, 1)
        main.plug = None

    def test_start_does_not_cycle_a_plug_that_is_already_on(self):
        class FakePlug:
            on_calls = 0
            def status(self): return True
            def on(self): self.on_calls += 1
        fake = FakePlug()
        main.plug = fake
        self.login("user")
        operation_id = self.client.post("/api/v1/server/start", headers=self.headers()).json()["id"]
        for _ in range(50):
            result = self.client.get(f"/api/v1/operations/{operation_id}").json()
            if result["status"] != "running": break
            time.sleep(0.02)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(fake.on_calls, 0)
        main.plug = None

    def test_start_reports_new_container_crash(self):
        class FakePlug:
            def __init__(self): self.turned_on = threading.Event()
            def status(self): return False
            def on(self): self.turned_on.set()
        fake = FakePlug()
        main.plug = fake
        self.login("user")
        operation_id = self.client.post("/api/v1/server/start", headers=self.headers()).json()["id"]
        self.assertTrue(fake.turned_on.wait(3))
        with self.client.websocket_connect("/internal/v1/agent", headers={"Authorization": "Bearer test-agent-token"}) as ws:
            ws.receive_json()
            started = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
            ws.send_json({"type": "status", "data": {"host": "online", "minecraft": "unknown", "container": "exited", "container_exit_code": 1, "container_started_at": started}})
            for _ in range(50):
                result = self.client.get(f"/api/v1/operations/{operation_id}").json()
                if result["status"] != "running": break
                time.sleep(0.02)
            self.assertEqual(result["status"], "failed")
            self.assertIn("退出码：1", result["detail"])
        main.plug = None


if __name__ == "__main__":
    unittest.main()

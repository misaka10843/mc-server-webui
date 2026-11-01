import os
import tempfile
import threading
import time
from datetime import datetime, timedelta, timezone
import unittest
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

    def test_authentication_role_and_origin(self):
        self.assertEqual(self.client.get("/api/v1/server/status").status_code, 401)
        self.assertEqual(self.login("user").status_code, 200)
        self.assertEqual(self.client.get("/api/v1/server/status").status_code, 200)
        self.assertEqual(self.client.post("/api/v1/admin/users", headers={"Origin": "http://testserver"}, json={"username": "new", "password": "long-enough-password", "role": "user"}).status_code, 403)
        self.assertEqual(self.client.post("/api/v1/auth/logout", headers={"Origin": "http://evil"}).status_code, 403)
        self.assertEqual(self.client.post("/api/v1/auth/logout", headers={"Origin": "http://testserver"}).status_code, 403)
        self.assertEqual(self.client.post("/api/v1/auth/logout", headers=self.headers()).status_code, 200)
        self.assertEqual(self.client.get("/api/v1/auth/me").status_code, 401)

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

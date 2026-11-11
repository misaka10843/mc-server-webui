import asyncio
import unittest
import time
from unittest.mock import AsyncMock, patch

from app import main


class StreamTests(unittest.IsolatedAsyncioTestCase):
    async def check_subscription(self, role, logs, expected):
        sync = AsyncMock()
        current = {"id": 1, "role": role, "expires_at": time.time() + 60}
        with patch.object(main, "listeners", set()), patch.object(main, "admin_listeners", set()), patch.object(main, "listener_users", {}), patch.object(main, "sync_log_subscription", sync):
            response = await main.events(None, logs=logs, current=current)
            await anext(response.body_iterator)
            self.assertEqual(len(main.admin_listeners), expected)
            await response.body_iterator.aclose()
            self.assertEqual(len(main.listeners), 0)
            self.assertEqual(sync.await_count, 2 if expected else 0)

    async def test_overview_does_not_subscribe_admin_logs(self):
        await self.check_subscription("admin", False, 0)

    async def test_console_subscribes_and_unsubscribes_admin_logs(self):
        await self.check_subscription("admin", True, 1)

    async def test_user_cannot_enable_admin_logs_through_query_string(self):
        await self.check_subscription("user", True, 0)

    async def test_admin_logs_never_enter_user_queue(self):
        admin = asyncio.Queue(maxsize=1)
        regular = asyncio.Queue(maxsize=1)
        with patch.object(main, "listeners", {admin, regular}), patch.object(main, "admin_listeners", {admin}):
            main.publish("log", {"line": "private"}, admin_only=True)
            self.assertIn("private", admin.get_nowait())
            self.assertTrue(regular.empty())

    async def test_slow_last_admin_unsubscribes_agent_logs(self):
        queue = asyncio.Queue(maxsize=1)
        queue.put_nowait("unconsumed")
        peer = AsyncMock()
        with patch.object(main, "listeners", {queue}), patch.object(main, "admin_listeners", {queue}), patch.object(main, "agent", peer), patch.object(main, "agent_send_lock", asyncio.Lock()):
            main.publish("log", {"line": "next"}, admin_only=True)
            await asyncio.sleep(0)
            self.assertNotIn(queue, main.listeners)
            peer.send_json.assert_awaited_once_with({"type": "logs_subscribe", "enabled": False})


if __name__ == "__main__":
    unittest.main()

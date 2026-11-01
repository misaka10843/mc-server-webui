import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from app import main


class StreamTests(unittest.IsolatedAsyncioTestCase):
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

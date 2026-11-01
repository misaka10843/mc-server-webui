import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from mc_agent import main


class LifecycleLockTests(unittest.IsolatedAsyncioTestCase):
    async def test_start_is_rejected_during_shutdown(self):
        lock = asyncio.Lock()
        start = AsyncMock()
        with patch.object(main, "shutdown_lock", lock), patch.object(main, "state", {"shutdown": "preparing"}), patch.object(main, "start_container", start):
            async with lock:
                with self.assertRaisesRegex(RuntimeError, "Shutdown in progress"):
                    await main.start_container_safely()
            start.assert_not_awaited()

    async def test_start_reserves_lifecycle_lock(self):
        lock = asyncio.Lock()
        async def start():
            self.assertTrue(lock.locked())
        with patch.object(main, "shutdown_lock", lock), patch.object(main, "state", {"shutdown": "none"}), patch.object(main, "start_container", start):
            await main.start_container_safely()
        self.assertFalse(lock.locked())


if __name__ == "__main__":
    unittest.main()

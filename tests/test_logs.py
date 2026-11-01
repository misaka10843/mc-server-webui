import asyncio
import json
import os
import unittest
from unittest.mock import AsyncMock, patch

from mc_agent import main


class LogTests(unittest.IsolatedAsyncioTestCase):
    async def test_long_lines_are_bounded_and_secrets_removed(self):
        process = AsyncMock()
        process.stdout.read = AsyncMock(side_effect=[b"secret-value " + b"x" * 5000 + b"\n", b""])
        process.returncode = 0
        done = asyncio.Event()
        sent = []
        async def send(payload):
            sent.append(json.loads(payload))
            done.set()
        ws = AsyncMock()
        ws.send.side_effect = send
        with patch.dict(os.environ, {"MC_AGENT_CONTAINER": "minecraft", "COMMAND_API_TOKEN": "secret-value"}), patch.object(main, "log_changed", asyncio.Event()), patch.object(main, "backend_send_lock", asyncio.Lock()), patch("mc_agent.main.asyncio.create_subprocess_exec", AsyncMock(return_value=process)):
            task = asyncio.create_task(main.follow_logs(ws))
            await asyncio.wait_for(done.wait(), 3)
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        self.assertNotIn("secret-value", sent[0]["line"])
        self.assertIn("[REDACTED]", sent[0]["line"])
        self.assertIn("[truncated]", sent[0]["line"])
        self.assertLessEqual(len(sent[0]["line"]), 4096)


if __name__ == "__main__":
    unittest.main()

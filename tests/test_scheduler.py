import asyncio
import unittest
from datetime import timedelta
from unittest.mock import AsyncMock, patch

from mc_agent import main
from mc_agent.idle import IdlePolicy


class SchedulerTests(unittest.IsolatedAsyncioTestCase):
    async def test_operational_failure_pauses_automatic_retries(self):
        policy = IdlePolicy(day_timeout=timedelta(seconds=0.1), night_timeout=timedelta(seconds=0.1))
        state = {"host": "online", "minecraft": "ready", "online": 0, "boot_id": "boot", "activity_version": 1, "shutdown": "none"}
        attempted = asyncio.Event()
        calls = []
        async def shutdown(container, callback):
            calls.append(container)
            attempted.set()
            raise RuntimeError("container inspection failed")
        with patch.object(main, "policy_config", policy), patch.object(main, "policy_enabled", True), patch.object(main, "state", state), patch.object(main, "mod_socket", object()), patch.object(main, "idle_changed", asyncio.Event()), patch.object(main, "changed", asyncio.Event()), patch.object(main, "log_changed", asyncio.Event()), patch.object(main, "shutdown_lock", asyncio.Lock()), patch.object(main, "shutdown_host", shutdown), patch.dict("os.environ", {"MC_AGENT_CONTAINER": "minecraft"}):
            task = asyncio.create_task(main.idle_scheduler())
            await asyncio.wait_for(attempted.wait(), 2)
            await asyncio.sleep(0.3)
            self.assertEqual(state["shutdown"], "failed")
            self.assertEqual(state["shutdown_error"], "container inspection failed")
            self.assertEqual(calls, ["minecraft"])
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def test_completed_manual_shutdown_is_not_overwritten_by_idle_scheduler(self):
        policy = IdlePolicy(day_timeout=timedelta(seconds=0.1), night_timeout=timedelta(seconds=0.1))
        state = {"host": "online", "minecraft": "ready", "online": 0, "boot_id": "boot", "activity_version": 1, "shutdown": "none"}
        lock = asyncio.Lock()
        shutdown = AsyncMock()
        with patch.object(main, "policy_config", policy), patch.object(main, "policy_enabled", True), patch.object(main, "state", state), patch.object(main, "mod_socket", object()), patch.object(main, "idle_changed", asyncio.Event()), patch.object(main, "changed", asyncio.Event()), patch.object(main, "log_changed", asyncio.Event()), patch.object(main, "shutdown_lock", lock), patch.object(main, "shutdown_host", shutdown), patch.dict("os.environ", {"MC_AGENT_CONTAINER": "minecraft"}):
            async with lock:
                task = asyncio.create_task(main.idle_scheduler())
                await asyncio.sleep(0.3)
                main.set_state({"shutdown": "poweroff_requested"})
            await asyncio.sleep(0.2)
            shutdown.assert_not_awaited()
            self.assertEqual(state["shutdown"], "poweroff_requested")
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def test_player_activity_restarts_idle_before_shutdown(self):
        policy = IdlePolicy(day_timeout=timedelta(seconds=3), night_timeout=timedelta(seconds=3))
        state = {"host": "online", "minecraft": "ready", "online": 0, "boot_id": "boot", "activity_version": 1}
        mod_request = AsyncMock()
        async def shutdown(container, callback):
            await callback()
        with patch.object(main, "policy_config", policy), patch.object(main, "policy_enabled", True), patch.object(main, "state", state), patch.object(main, "mod_socket", object()), patch.object(main, "idle_changed", asyncio.Event()), patch.object(main, "changed", asyncio.Event()), patch.object(main, "log_changed", asyncio.Event()), patch.object(main, "shutdown_lock", asyncio.Lock()), patch.object(main, "request_mod_shutdown", mod_request), patch.object(main, "shutdown_host", shutdown), patch.dict("os.environ", {"MC_AGENT_CONTAINER": "minecraft"}):
            task = asyncio.create_task(main.idle_scheduler())
            await asyncio.sleep(0.25)
            main.set_state({"online": 1, "activity_version": 2})
            await asyncio.sleep(0.25)
            main.set_state({"online": 0, "activity_version": 3})
            done, _ = await asyncio.wait({task}, timeout=0.5)
            self.assertFalse(done)
            await asyncio.wait_for(task, 4)
            mod_request.assert_awaited_once()
            self.assertEqual(mod_request.await_args.args[:3], ("boot", 3, 3))
            self.assertGreater(mod_request.await_args.args[3], 0)
            self.assertEqual(state["shutdown"], "poweroff_requested")


if __name__ == "__main__":
    unittest.main()

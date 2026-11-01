import os
import asyncio
import unittest
from unittest.mock import patch

from mc_agent import main


class AgentPolicyTests(unittest.TestCase):
    def test_policy_requires_local_shutdown_gate(self):
        policy = {"revision": 2, "enabled": True, "day_minutes": 90, "night_minutes": 30, "night_start": "23:30", "day_start": "09:00"}
        with patch.dict(os.environ, {"MC_AGENT_AUTO_SHUTDOWN": "false"}):
            main.apply_policy(policy)
            self.assertFalse(main.policy_enabled)
            self.assertEqual(main.state["policy_revision"], 2)
        with patch.dict(os.environ, {"MC_AGENT_AUTO_SHUTDOWN": "true"}):
            main.apply_policy(policy)
            self.assertTrue(main.policy_enabled)
        policy["night_start"] = "08:00"
        with self.assertRaises(ValueError):
            main.apply_policy(policy)
        policy["night_start"] = "23:30"
        policy["revision"] = "invalid"
        previous = main.policy_config
        with self.assertRaises(ValueError):
            main.apply_policy(policy)
        self.assertIs(main.policy_config, previous)


class AgentPolicyConcurrencyTests(unittest.IsolatedAsyncioTestCase):
    async def test_policy_change_is_not_acknowledged_during_shutdown(self):
        policy = {"revision": 3, "enabled": False, "day_minutes": 90, "night_minutes": 30, "night_start": "23:30", "day_start": "09:00"}
        lock = asyncio.Lock()
        with patch.object(main, "shutdown_lock", lock), patch.object(main, "state", {"shutdown": "preparing"}):
            async with lock:
                with self.assertRaisesRegex(RuntimeError, "not yet applied"):
                    main.apply_policy(policy)

    async def test_only_explicit_policy_save_clears_failed_shutdown(self):
        policy = {"revision": 3, "enabled": False, "day_minutes": 90, "night_minutes": 30, "night_start": "23:30", "day_start": "09:00"}
        state = {"shutdown": "failed", "shutdown_error": "disk error"}
        with patch.object(main, "shutdown_lock", asyncio.Lock()), patch.object(main, "state", state), patch.object(main, "changed", asyncio.Event()), patch.object(main, "idle_changed", asyncio.Event()), patch.object(main, "log_changed", asyncio.Event()):
            main.apply_policy(policy)
            self.assertEqual(state["shutdown"], "failed")
            main.apply_policy(policy, acknowledge_failure=True)
            self.assertEqual(state["shutdown"], "none")
            self.assertIsNone(state["shutdown_error"])


if __name__ == "__main__":
    unittest.main()

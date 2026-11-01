import unittest
from unittest.mock import AsyncMock, patch

from mc_agent.shutdown import shutdown_host


class ShutdownTests(unittest.IsolatedAsyncioTestCase):
    async def test_restart_policy_prevents_shutdown(self):
        before = {"Status": "running", "StartedAt": "original", "restart_policy": "always", "restart_count": 0}
        stop = AsyncMock()
        with patch("mc_agent.shutdown.inspect_container", AsyncMock(return_value=("id", before))):
            with self.assertRaisesRegex(RuntimeError, "restart policy"):
                await shutdown_host("minecraft", stop)
            stop.assert_not_awaited()

    async def test_abnormal_exit_does_not_power_off(self):
        before = {"Status": "running", "StartedAt": "original", "restart_policy": "no", "restart_count": 0}
        stop = AsyncMock()
        with patch("mc_agent.shutdown.inspect_container", AsyncMock(return_value=("id", before))), patch("mc_agent.shutdown.docker", AsyncMock(return_value="137")), patch("mc_agent.shutdown.asyncio.create_subprocess_exec", AsyncMock()) as poweroff:
            with self.assertRaisesRegex(RuntimeError, "normally"):
                await shutdown_host("minecraft", stop)
            stop.assert_awaited_once()
            poweroff.assert_not_awaited()

    async def test_restarted_container_does_not_power_off(self):
        before = {"Status": "running", "StartedAt": "original", "restart_policy": "no", "restart_count": 0}
        after = {"Status": "exited", "StartedAt": "new", "ExitCode": 0, "restart_policy": "no", "restart_count": 0}
        with patch("mc_agent.shutdown.inspect_container", AsyncMock(side_effect=[("id", before), ("id", after)])), patch("mc_agent.shutdown.docker", AsyncMock(return_value="0")), patch("mc_agent.shutdown.asyncio.create_subprocess_exec", AsyncMock()) as poweroff:
            with self.assertRaisesRegex(RuntimeError, "changed"):
                await shutdown_host("minecraft", AsyncMock())
            poweroff.assert_not_awaited()

    async def test_failed_recheck_does_not_wait_or_power_off(self):
        before = {"Status": "running", "StartedAt": "original", "restart_policy": "no", "restart_count": 0}
        with patch("mc_agent.shutdown.inspect_container", AsyncMock(return_value=("id", before))), patch("mc_agent.shutdown.docker", AsyncMock()) as docker, patch("mc_agent.shutdown.asyncio.create_subprocess_exec", AsyncMock()) as poweroff:
            with self.assertRaisesRegex(RuntimeError, "changed"):
                await shutdown_host("minecraft", AsyncMock(side_effect=RuntimeError("players changed")))
            docker.assert_not_awaited()
            poweroff.assert_not_awaited()

    async def test_success_issues_fixed_helper(self):
        before = {"Status": "running", "StartedAt": "original", "restart_policy": "no", "restart_count": 0}
        after = {"Status": "exited", "StartedAt": "original", "ExitCode": 0, "restart_policy": "no", "restart_count": 0}
        process = AsyncMock()
        process.returncode = 0
        process.communicate.return_value = (b"", b"")
        with patch("mc_agent.shutdown.inspect_container", AsyncMock(side_effect=[("id", before), ("id", after)])), patch("mc_agent.shutdown.docker", AsyncMock(return_value="0")), patch("mc_agent.shutdown.asyncio.create_subprocess_exec", AsyncMock(return_value=process)) as poweroff:
            await shutdown_host("minecraft", AsyncMock())
            self.assertEqual(poweroff.await_args.args, ("sudo", "-n", "/usr/local/libexec/mc-server-poweroff"))


if __name__ == "__main__":
    unittest.main()

import unittest
from datetime import datetime, timedelta, timezone

from mc_agent.idle import IdlePolicy, IdleTracker


class PolicyTests(unittest.TestCase):
    def test_boundary_and_midnight(self):
        policy = IdlePolicy()
        cases = [(15, 29, 90), (15, 30, 30), (0, 59, 30), (1, 0, 90)]
        for hour, minute, expected in cases:
            with self.subTest(hour=hour, minute=minute):
                now = datetime(2026, 11, 1, hour, minute, tzinfo=timezone.utc)
                self.assertEqual(policy.threshold(now), timedelta(minutes=expected))

    def test_idle_spans_policy_transition(self):
        policy = IdlePolicy()
        before = datetime(2026, 11, 1, 15, 29, tzinfo=timezone.utc)
        after = datetime(2026, 11, 1, 15, 30, tzinfo=timezone.utc)
        self.assertFalse(policy.is_due(before, 3600))
        self.assertTrue(policy.is_due(after, 3600))

    def test_readiness_and_players_reset_timer(self):
        tracker = IdleTracker()
        tracker.update(ready=False, player_count=0, monotonic_now=10)
        self.assertIsNone(tracker.elapsed(20))
        tracker.update(ready=True, player_count=0, monotonic_now=30)
        self.assertEqual(tracker.elapsed(40), 10)
        tracker.update(ready=True, player_count=1, monotonic_now=40)
        self.assertIsNone(tracker.elapsed(50))
        tracker.update(ready=True, player_count=0, monotonic_now=60)
        self.assertEqual(tracker.elapsed(65), 5)
        tracker.update(ready=False, player_count=0, monotonic_now=65)
        self.assertIsNone(tracker.elapsed(70))

    def test_invalid_input_is_rejected(self):
        policy = IdlePolicy()
        with self.assertRaises(ValueError):
            policy.threshold(datetime(2026, 1, 1))
        with self.assertRaises(ValueError):
            IdleTracker().update(ready=True, player_count=-1, monotonic_now=1)


if __name__ == "__main__":
    unittest.main()

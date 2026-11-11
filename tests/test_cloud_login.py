import threading
import unittest
from unittest.mock import MagicMock

import requests

from app.plug import wait_for_scan


class CloudLoginTests(unittest.TestCase):
    def test_cancelled_scan_makes_no_cloud_requests(self):
        connector = MagicMock(_timeout=60)
        stopped = threading.Event()
        stopped.set()
        self.assertFalse(wait_for_scan(connector, stopped))
        connector._session.get.assert_not_called()

    def test_cloud_rejection_is_not_retried(self):
        connector = MagicMock(_timeout=60)
        connector._session.get.return_value.raise_for_status.side_effect = requests.HTTPError("denied")
        with self.assertRaises(requests.HTTPError):
            wait_for_scan(connector, threading.Event())
        connector._session.get.assert_called_once()

    def test_scan_copies_only_login_fields_after_response(self):
        connector = MagicMock(_timeout=60)
        connector.to_json.return_value = {"userId": "user", "ssecurity": "security", "cUserId": "cuser", "passToken": "pass", "location": "https://sts.api.io.mi.com/sts"}
        self.assertTrue(wait_for_scan(connector, threading.Event()))
        self.assertEqual(connector.userId, "user")
        self.assertEqual(connector._ssecurity, "security")

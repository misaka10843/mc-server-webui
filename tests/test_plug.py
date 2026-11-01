import unittest
from unittest.mock import Mock, patch
from miio.exceptions import DeviceException

from app.plug import Plug


class PlugTests(unittest.TestCase):
    def test_miot_switch_validates_response_and_only_turns_on(self):
        plug = object.__new__(Plug)
        plug.device = Mock()
        plug.siid, plug.piid = 2, 1
        plug.device.get_property_by.return_value = [{"code": 0, "value": False}]
        plug.device.set_property_by.return_value = [{"code": 0}]
        self.assertFalse(plug.status())
        plug.on()
        plug.device.set_property_by.assert_called_once_with(2, 1, True)
        plug.device.get_property_by.return_value = [{"code": -4001}]
        with self.assertRaises(DeviceException):
            plug.status()


if __name__ == "__main__":
    unittest.main()

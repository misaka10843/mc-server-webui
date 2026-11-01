import os

from miio import MiotDevice
from miio.exceptions import DeviceException


class Plug:
    def __init__(self):
        self.device = MiotDevice(ip=os.environ["MCWEB_PLUG_IP"], token=os.environ["MCWEB_PLUG_TOKEN"], model=os.environ["MCWEB_PLUG_MODEL"], timeout=5, mapping={})
        self.siid = int(os.environ["MCWEB_PLUG_SWITCH_SIID"])
        self.piid = int(os.environ["MCWEB_PLUG_SWITCH_PIID"])

    @staticmethod
    def check(response):
        if not isinstance(response, list) or len(response) != 1 or response[0].get("code") != 0:
            raise DeviceException(f"MIoT device request failed: {response}")
        return response[0]

    def status(self):
        result = self.check(self.device.get_property_by(self.siid, self.piid))
        value = result.get("value")
        if not isinstance(value, bool):
            raise DeviceException("MIoT switch state is not boolean")
        return value

    def on(self):
        self.check(self.device.set_property_by(self.siid, self.piid, True))

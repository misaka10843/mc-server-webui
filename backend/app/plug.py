from miio import MiotDevice
from miio.exceptions import DeviceException


class Plug:
    def __init__(self, ip, token, model, siid, piid):
        self.device = MiotDevice(ip=ip, token=token, model=model, timeout=5, mapping={})
        self.token = token
        self.siid = int(siid)
        self.piid = int(piid)

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

from miio import MiotDevice
from miio.exceptions import DeviceException
from mihome_ctl.connector import QrCodeXiaomiCloudConnector
from mihome_ctl.core.cloudapi import api
import time
import requests


def wait_for_scan(connector, stopped):
    deadline = time.monotonic() + max(1, min(float(connector._timeout), 180))
    while not stopped.is_set():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        try:
            response = connector._session.get(connector._long_polling_url, timeout=(5, min(5, remaining)))
        except requests.Timeout:
            continue
        response.raise_for_status()
        data = connector.to_json(response.text)
        connector.userId = data["userId"]
        connector._ssecurity = data["ssecurity"]
        connector._cUserId = data["cUserId"]
        connector._pass_token = data["passToken"]
        connector._location = data["location"]
        return True
    return False


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


class CloudPlug:
    token = ""

    def __init__(self, did, region, siid, piid, user_id, security, service_token):
        self.did, self.region, self.siid, self.piid = did, region, siid, piid
        self.connector = QrCodeXiaomiCloudConnector()
        self.connector.userId = user_id
        self.connector._ssecurity = security
        self.connector._serviceToken = service_token
        original = self.connector._session.request

        def bounded(method, url, **kwargs):
            kwargs.setdefault("timeout", 15)
            return original(method, url, **kwargs)

        self.connector._session.request = bounded

    def request(self, operation, value=None):
        prop = {"did": self.did, "siid": self.siid, "piid": self.piid}
        if operation == "set":
            prop["value"] = value
        response = api(self.connector, self.region, f"/miotspec/prop/{operation}", {"params": [prop]})
        if not isinstance(response, dict) or response.get("code") != 0:
            raise DeviceException("米家云请求失败，账号会话可能已失效，请重新扫码")
        return Plug.check(response.get("result"))

    def status(self):
        value = self.request("get").get("value")
        if not isinstance(value, bool):
            raise DeviceException("米家云返回的开关状态无效")
        return value

    def on(self):
        self.request("set", True)

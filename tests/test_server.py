import unittest

from app.server import PortBoundary


class PortBoundaryTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.forwarded = []
        self.sent = []

        async def application(scope, receive, send):
            self.forwarded.append(scope)

        self.boundary = PortBoundary(application, 8080, 8000)

    async def invoke(self, kind, port, path):
        async def receive():
            return {}

        async def send(message):
            self.sent.append(message)

        await self.boundary({"type": kind, "server": ("127.0.0.1", port), "path": path}, receive, send)

    async def test_web_port_excludes_internal_endpoint(self):
        await self.invoke("http", 8080, "/")
        await self.invoke("http", 8080, "/api/v1/status")
        await self.invoke("http", 8080, "/internal/v1/agent")
        await self.invoke("websocket", 8080, "/internal/v1/agent")
        self.assertEqual([scope["path"] for scope in self.forwarded], ["/", "/api/v1/status"])
        self.assertEqual(self.sent[0]["status"], 404)
        self.assertEqual(self.sent[-1]["type"], "websocket.close")

    async def test_agent_port_accepts_only_agent_websocket(self):
        await self.invoke("websocket", 8000, "/internal/v1/agent")
        await self.invoke("http", 8000, "/api/v1/status")
        await self.invoke("websocket", 8000, "/other")
        self.assertEqual(len(self.forwarded), 1)
        self.assertEqual(self.forwarded[0]["path"], "/internal/v1/agent")
        self.assertEqual(self.sent[0]["status"], 404)
        self.assertEqual(self.sent[-1]["type"], "websocket.close")

    async def test_lifespan_is_forwarded(self):
        async def receive():
            return {}

        async def send(message):
            pass

        await self.boundary({"type": "lifespan"}, receive, send)
        self.assertEqual(self.forwarded[0]["type"], "lifespan")

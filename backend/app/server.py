import os
import socket
from contextlib import ExitStack

import uvicorn

from .main import app


class PortBoundary:
    def __init__(self, application, web_port, agent_port):
        self.application = application
        self.web_port = web_port
        self.agent_port = agent_port

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket"):
            await self.application(scope, receive, send)
            return
        port = scope["server"][1]
        path = scope["path"]
        internal = path == "/internal" or path.startswith("/internal/")
        allowed = (port == self.web_port and not internal) or (
            port == self.agent_port and scope["type"] == "websocket" and path == "/internal/v1/agent"
        )
        if allowed:
            await self.application(scope, receive, send)
        elif scope["type"] == "websocket":
            await send({"type": "websocket.close", "code": 1008})
        else:
            await send({"type": "http.response.start", "status": 404, "headers": []})
            await send({"type": "http.response.body", "body": b"Not found"})


def main():
    web_port = int(os.environ.get("MCWEB_WEB_PORT", "8080"))
    agent_port = int(os.environ.get("MCWEB_AGENT_PORT", "8000"))
    if web_port == agent_port or not (1 <= web_port <= 65535 and 1 <= agent_port <= 65535):
        raise ValueError("Web and agent ports must be distinct valid ports")
    application = PortBoundary(app, web_port, agent_port)
    with ExitStack() as stack:
        listeners = []
        for port in (web_port, agent_port):
            listener = stack.enter_context(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("0.0.0.0", port))
            listener.listen(128)
            listener.setblocking(False)
            listeners.append(listener)
        print(f"Web listening on {web_port}; agent listening on {agent_port}", flush=True)
        uvicorn.Server(uvicorn.Config(application, proxy_headers=False, workers=1)).run(sockets=listeners)


if __name__ == "__main__":
    main()

import asyncio
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import sqlite3
import threading
import time
import uuid
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, time as clock_time, timezone

from argon2.exceptions import VerifyMismatchError
from fastapi import Cookie, Depends, FastAPI, Header, HTTPException, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .db import connect, initialize, passwords
from .plug import Plug

listeners: set[asyncio.Queue] = set()
admin_listeners: set[asyncio.Queue] = set()
listener_users: dict[asyncio.Queue, int] = {}
log_lines: deque[str] = deque(maxlen=5000)
agent: WebSocket | None = None
pending: dict[str, asyncio.Future] = {}
agent_send_lock = asyncio.Lock()
agent_connect_lock = asyncio.Lock()
state = {"host": "unknown", "minecraft": "unknown", "plug": "unknown"}
logger = logging.getLogger(__name__)
plug: Plug | None = None
plug_lock = asyncio.Lock()
operation_lock = asyncio.Lock()
current_operation: str | None = None
state_changed = asyncio.Event()
login_attempts: dict[str, list[float]] = {}
start_attempts: dict[int, list[float]] = {}
login_lock = threading.Lock()


def set_state(values: dict):
    if any(state.get(key) != value for key, value in values.items()):
        state.update(values)
        state_changed.set()
        publish("status", state)


async def read_plug():
    async with plug_lock:
        if plug is None:
            raise RuntimeError("Smart plug is not configured")
        return await asyncio.to_thread(plug.status)


async def monitor_plug():
    while True:
        if plug is None:
            await asyncio.sleep(30)
            continue
        try:
            value = await read_plug()
            set_state({"plug": "on" if value else "off"})
            if value and state.get("shutdown") == "off":
                set_state({"shutdown": "none"})
            if not value and agent is None and state.get("shutdown") in ("preparing", "poweroff_requested"):
                set_state({"shutdown": "off"})
                audit(None, "plug_off", "Smart plug reports off after shutdown")
        except Exception:
            logger.exception("Smart plug status failed")
            set_state({"plug": "unknown"})
        await asyncio.sleep(30)


def cleanup_expired():
    with connect() as db:
        db.execute("DELETE FROM sessions WHERE expires_at < ?", (time.time(),))
        db.execute("DELETE FROM audit_events WHERE created_at < ?", (time.time() - 90 * 86400,))


async def maintenance():
    while True:
        await asyncio.to_thread(cleanup_expired)
        await asyncio.sleep(86400)


def publish(event: str, payload: dict, *, admin_only=False):
    message = f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
    had_admin = bool(admin_listeners)
    for queue in tuple(listeners):
        if admin_only and queue not in admin_listeners:
            continue
        if queue.full():
            listeners.discard(queue)
            admin_listeners.discard(queue)
            continue
        queue.put_nowait(message)
    if had_admin and not admin_listeners:
        asyncio.create_task(sync_log_subscription())


@asynccontextmanager
async def lifespan(app: FastAPI):
    global plug, state_changed, agent_send_lock, agent_connect_lock, plug_lock, operation_lock
    state_changed = asyncio.Event()
    agent_send_lock = asyncio.Lock()
    agent_connect_lock = asyncio.Lock()
    plug_lock = asyncio.Lock()
    operation_lock = asyncio.Lock()
    initialize()
    state["server_lan_address"] = os.environ.get("MCWEB_LAN_SERVER_ADDRESS", "192.168.101.41:25565")
    state["server_address"] = os.environ.get("MCWEB_SERVER_ADDRESS", "")
    with connect() as db:
        previous = db.execute("SELECT id, kind, status, detail, created_at FROM operations ORDER BY created_at DESC LIMIT 1").fetchone()
    state["operation"] = dict(previous) if previous else None
    keys = ("MCWEB_PLUG_IP", "MCWEB_PLUG_TOKEN", "MCWEB_PLUG_MODEL", "MCWEB_PLUG_SWITCH_SIID", "MCWEB_PLUG_SWITCH_PIID")
    with connect() as db:
        row = db.execute("SELECT ip, token, model, siid, piid FROM plug_config WHERE id=1").fetchone()
        if row is None and all(os.environ.get(key) and not os.environ[key].startswith("REPLACE_WITH_") for key in keys):
            db.execute("INSERT INTO plug_config VALUES (1,?,?,?,?,?)", tuple(os.environ[key] for key in keys))
            row = db.execute("SELECT ip, token, model, siid, piid FROM plug_config WHERE id=1").fetchone()
    plug = Plug(**dict(row)) if row else None
    monitor = asyncio.create_task(monitor_plug())
    maintenance_task = asyncio.create_task(maintenance())
    try:
        yield
    finally:
        maintenance_task.cancel()
        await asyncio.gather(maintenance_task, return_exceptions=True)
        if monitor:
            monitor.cancel()
            await asyncio.gather(monitor, return_exceptions=True)
        plug = None


app = FastAPI(lifespan=lifespan)


class Login(BaseModel):
    username: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=1024)


class CreateUser(Login):
    role: str = Field(pattern="^(user|admin)$")


class UserUpdate(BaseModel):
    role: str = Field(pattern="^(user|admin)$")
    enabled: bool
    password: str | None = Field(default=None, min_length=12, max_length=1024)


class PasswordChange(BaseModel):
    old_password: str = Field(min_length=1, max_length=1024)
    new_password: str = Field(min_length=12, max_length=1024)


class PolicyUpdate(BaseModel):
    enabled: bool
    day_minutes: int = Field(ge=1, le=1440)
    night_minutes: int = Field(ge=1, le=1440)
    night_start: str = Field(pattern=r"^\d{2}:\d{2}$")
    day_start: str = Field(pattern=r"^\d{2}:\d{2}$")


class PlugConfig(BaseModel):
    ip: str = Field(min_length=1, max_length=255)
    token: str = Field(default="", max_length=128)
    model: str = Field(min_length=1, max_length=255)
    siid: int = Field(ge=1, le=65535)
    piid: int = Field(ge=1, le=65535)


class CloudLogin(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=1024)
    locale: str = Field(pattern="^(cn|de|i2|ru|sg|us)$")


class CommandRequest(BaseModel):
    input: str = Field(min_length=1, max_length=4096)


class CompletionRequest(BaseModel):
    input: str = Field(max_length=4096)
    cursor: int = Field(ge=0, le=4096)


async def agent_request(kind: str, data: dict, timeout: float = 10, request_id: str | None = None):
    peer = agent
    if peer is None:
        raise HTTPException(503, "Server agent is offline")
    if len(pending) >= 64:
        raise HTTPException(503, "Server is busy")
    request_id = request_id or uuid.uuid4().hex
    future = asyncio.get_running_loop().create_future()
    pending[request_id] = future
    try:
        async with agent_send_lock:
            if peer is not agent:
                raise HTTPException(503, "Server agent disconnected")
            try:
                await peer.send_json({"type": kind, "id": request_id, **data})
            except (WebSocketDisconnect, RuntimeError, OSError):
                raise HTTPException(503, "Agent connection lost; command outcome may be unknown")
        try:
            result = await asyncio.wait_for(future, timeout)
        except TimeoutError:
            raise HTTPException(504, "Request timed out; command outcome may be unknown")
        if "error" in result:
            raise HTTPException(503, result["error"])
        return result
    finally:
        pending.pop(request_id, None)


def user(mc_session: str | None = Cookie(default=None)):
    if not mc_session:
        raise HTTPException(401, "Not authenticated")
    digest = hashlib.sha256(mc_session.encode()).hexdigest()
    with connect() as db:
        row = db.execute("SELECT users.id, username, role, expires_at, csrf_hash FROM sessions JOIN users ON users.id=sessions.user_id WHERE token_hash=? AND expires_at>? AND enabled=1", (digest, time.time())).fetchone()
    if not row:
        raise HTTPException(401, "Session expired")
    return dict(row)


def admin(current=Depends(user)):
    if current["role"] != "admin":
        raise HTTPException(403, "Administrator required")
    return current


def check_origin(request: Request):
    origin = request.headers.get("origin")
    host = request.headers.get("host")
    if not host or not origin or origin != f"{request.url.scheme}://{host}":
        raise HTTPException(403, "Origin rejected")


def check_csrf(request: Request, current: dict):
    check_origin(request)
    cookie = request.cookies.get("mc_csrf", "")
    token = request.headers.get("x-csrf-token", "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{43}", cookie) or not re.fullmatch(r"[A-Za-z0-9_-]{43}", token) or not current.get("csrf_hash") or not hmac.compare_digest(cookie, token) or not hmac.compare_digest(hashlib.sha256(token.encode()).hexdigest(), current["csrf_hash"]):
        raise HTTPException(403, "CSRF token rejected")


def audit(user_id, action, detail=""):
    with connect() as db:
        db.execute("INSERT INTO audit_events(created_at,user_id,action,detail) VALUES(?,?,?,?)", (time.time(), user_id, action, detail))


def current_policy():
    with connect() as db:
        return dict(db.execute("SELECT revision, enabled, day_minutes, night_minutes, night_start, day_start FROM server_policy WHERE id=1").fetchone())


@app.get("/api/v1/admin/plug")
def get_plug_config(current=Depends(admin)):
    with connect() as db:
        row = db.execute("SELECT ip, model, siid, piid FROM plug_config WHERE id=1").fetchone()
    return dict(row) if row else None


@app.put("/api/v1/admin/plug")
async def save_plug_config(data: PlugConfig, request: Request, current=Depends(admin)):
    global plug
    check_csrf(request, current)
    async with operation_lock:
        if current_operation is not None:
            raise HTTPException(409, "服务器电源操作进行中，请稍后修改插座")
        async with plug_lock:
            with connect() as db:
                previous = db.execute("SELECT token FROM plug_config WHERE id=1").fetchone()
                token = data.token or (previous[0] if previous else "")
                if not re.fullmatch(r"[0-9a-fA-F]{32}", token):
                    raise HTTPException(422, "设备 token 必须为 32 位十六进制字符")
                candidate = Plug(data.ip, token, data.model, data.siid, data.piid)
                try:
                    value = await asyncio.to_thread(candidate.status)
                except Exception:
                    raise HTTPException(502, "无法读取插座，请检查设备信息及局域网连接")
                db.execute("INSERT INTO plug_config VALUES (1,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET ip=excluded.ip, token=excluded.token, model=excluded.model, siid=excluded.siid, piid=excluded.piid", (data.ip, token, data.model, data.siid, data.piid))
            plug = candidate
            set_state({"plug": "on" if value else "off"})
    audit(current["id"], "update_plug", data.model)
    return {"ok": True}


@app.post("/api/v1/admin/plug/discover")
async def discover_plugs(data: CloudLogin, request: Request, current=Depends(admin)):
    check_csrf(request, current)
    if request.url.scheme != "https" and request.url.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise HTTPException(400, "米家账号登录需要 HTTPS 或本机访问")
    from miio.cloud import CloudInterface
    try:
        devices = await asyncio.to_thread(CloudInterface(data.username, data.password).get_devices, data.locale)
    except Exception:
        raise HTTPException(502, "米家登录或读取设备失败，请检查账号、地区及验证要求")
    return [{"name": d.name, "ip": d.ip, "token": d.token, "model": d.model} for d in devices.values() if not d.parent_id]


@app.get("/api/v1/admin/policy")
def get_policy(current=Depends(admin)):
    return {**current_policy(), "applied_revision": state.get("policy_revision"), "effective_enabled": state.get("policy_enabled", False)}


@app.put("/api/v1/admin/policy")
async def set_policy(data: PolicyUpdate, request: Request, current=Depends(admin)):
    check_csrf(request, current)
    try:
        night = clock_time.fromisoformat(data.night_start)
        day = clock_time.fromisoformat(data.day_start)
    except ValueError:
        raise HTTPException(422, "Invalid time")
    if night <= day:
        raise HTTPException(422, "Night interval must cross midnight")
    with connect() as db:
        db.execute("UPDATE server_policy SET revision=revision+1, enabled=?, day_minutes=?, night_minutes=?, night_start=?, day_start=? WHERE id=1", (data.enabled, data.day_minutes, data.night_minutes, data.night_start, data.day_start))
    policy = current_policy()
    audit(current["id"], "update_policy", json.dumps(policy))
    try:
        response = await agent_request("set_policy", {"policy": policy})
        applied = response.get("applied", False)
    except HTTPException:
        applied = False
    return {**policy, "applied": applied}


def update_operation(operation_id: str, status: str, detail: str):
    previous = state.get("operation") or {}
    if previous.get("id") == operation_id and previous.get("status") == status and previous.get("detail") == detail:
        return
    with connect() as db:
        db.execute("UPDATE operations SET status=?, detail=?, updated_at=? WHERE id=?", (status, detail, time.time(), operation_id))
        row = db.execute("SELECT id, kind, status, detail, created_at FROM operations WHERE id=?", (operation_id,)).fetchone()
    record = dict(row)
    set_state({"operation": record})
    publish("operation", record)


async def run_start(operation_id: str):
    global current_operation
    try:
        with connect() as db:
            requested_at = db.execute("SELECT created_at FROM operations WHERE id=?", (operation_id,)).fetchone()[0]
        if state["host"] == "online":
            if state["minecraft"] != "ready":
                if state.get("container") in ("exited", "created"):
                    update_operation(operation_id, "running", "正在启动 Minecraft 容器")
                    await agent_request("start_container", {}, 30)
                elif state.get("container") != "running":
                    raise RuntimeError("无法确认 Minecraft 容器状态，请检查主机")
        else:
            update_operation(operation_id, "running", "正在确认插座状态")
            if await read_plug():
                raise RuntimeError("插座仍在供电且主机状态未知，请检查主机")
            set_state({"plug": "off"})
            update_operation(operation_id, "running", "正在开启插座")
            async with plug_lock:
                await asyncio.to_thread(plug.on)
            set_state({"plug": "unknown", "shutdown": "none"})
        deadline = asyncio.get_running_loop().time() + 900
        while state["minecraft"] != "ready":
            if state.get("container") == "exited" and state.get("container_started_at"):
                try:
                    started_at = datetime.fromisoformat(state["container_started_at"].replace("Z", "+00:00"))
                except ValueError:
                    raise RuntimeError("Docker 返回了无效的容器启动时间")
                if started_at >= datetime.fromtimestamp(requested_at, timezone.utc):
                    raise RuntimeError(f"Minecraft 容器已退出，退出码：{state.get('container_exit_code')}，请检查日志")
            if state["host"] == "online":
                detail = "主机已上线，正在等待 Minecraft 就绪"
            else:
                detail = "正在等待 Ubuntu 启动"
            update_operation(operation_id, "running", detail)
            state_changed.clear()
            remaining = deadline - asyncio.get_running_loop().time()
            if remaining <= 0:
                raise TimeoutError("启动超时，请检查主机和容器日志")
            await asyncio.wait_for(state_changed.wait(), remaining)
        update_operation(operation_id, "complete", "服务器可以加入")
    except Exception as exc:
        logger.warning("Server start failed: %s", exc)
        update_operation(operation_id, "failed", str(exc) or "启动超时")
    finally:
        current_operation = None


async def run_shutdown(operation_id: str):
    global current_operation
    try:
        set_state({"shutdown": "preparing", "shutdown_error": None})
        update_operation(operation_id, "running", "正在通知玩家并关闭服务器")
        await agent_request("shutdown_manual", {}, 15)
        deadline = asyncio.get_running_loop().time() + 1200
        while True:
            if state.get("shutdown") == "failed":
                raise RuntimeError(state.get("shutdown_error") or "关机未完成")
            if state.get("shutdown") == "off" and state.get("plug") == "off":
                update_operation(operation_id, "complete", "插座已断电")
                break
            if state.get("host") != "online":
                detail = "主机已离线，等待插座自动断电"
            else:
                detail = "正在通知玩家并关闭服务器"
            update_operation(operation_id, "running", detail)
            state_changed.clear()
            remaining = deadline - asyncio.get_running_loop().time()
            if remaining <= 0:
                raise TimeoutError("等待插座断电超时，请检查设备")
            await asyncio.wait_for(state_changed.wait(), remaining)
    except Exception as exc:
        logger.warning("Server shutdown failed: %s", exc)
        update_operation(operation_id, "failed", str(exc) or "关机超时")
        if state.get("host") == "online":
            set_state({"shutdown": "failed", "shutdown_error": str(exc)})
    finally:
        current_operation = None


@app.post("/api/v1/admin/server/shutdown")
async def stop_server(request: Request, current=Depends(admin)):
    global current_operation
    check_csrf(request, current)
    async with operation_lock:
        if current_operation:
            raise HTTPException(409, "Another lifecycle operation is in progress")
        if state.get("host") != "online" or state.get("minecraft") != "ready" or plug is None:
            raise HTTPException(409, "Host, Minecraft, or smart plug is unavailable")
        operation_id = uuid.uuid4().hex
        now = time.time()
        with connect() as db:
            db.execute("INSERT INTO operations VALUES(?,?,?,?,?,?,?)", (operation_id, current["id"], "shutdown", "running", "准备关机", now, now))
        audit(current["id"], "shutdown", operation_id)
        current_operation = operation_id
        asyncio.create_task(run_shutdown(operation_id))
        return {"id": operation_id}


@app.post("/api/v1/server/start")
async def start_server(request: Request, current=Depends(user)):
    global current_operation
    check_csrf(request, current)
    async with operation_lock:
        if state.get("shutdown") in ("preparing", "poweroff_requested"):
            raise HTTPException(409, "Server is shutting down; wait for the plug to turn off")
        if current_operation:
            return {"id": current_operation}
        now_monotonic = time.monotonic()
        recent = [value for value in start_attempts.get(current["id"], []) if value > now_monotonic - 60]
        if len(recent) >= 3:
            raise HTTPException(429, "Too many start requests")
        recent.append(now_monotonic)
        start_attempts[current["id"]] = recent
        operation_id = uuid.uuid4().hex
        now = time.time()
        with connect() as db:
            db.execute("INSERT INTO operations VALUES(?,?,?,?,?,?,?)", (operation_id, current["id"], "start", "running", "准备启动", now, now))
        audit(current["id"], "start", operation_id)
        current_operation = operation_id
        asyncio.create_task(run_start(operation_id))
        return {"id": operation_id}


@app.get("/api/v1/operations/{operation_id}")
def get_operation(operation_id: str, current=Depends(user)):
    with connect() as db:
        row = db.execute("SELECT id, kind, status, detail, created_at, updated_at FROM operations WHERE id=?", (operation_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Operation not found")
    return dict(row)


@app.post("/api/v1/admin/commands")
async def command(data: CommandRequest, request: Request, current=Depends(admin)):
    check_csrf(request, current)
    request_id = uuid.uuid4().hex
    command_text = data.input
    for secret in (os.environ.get("MCWEB_AGENT_TOKEN"), plug.token if plug else None):
        if secret:
            command_text = command_text.replace(secret, "[REDACTED]")
    audit(current["id"], "command", json.dumps({"id": request_id, "input": command_text}, ensure_ascii=False))
    try:
        result = await agent_request("command", data.model_dump(), request_id=request_id)
    except HTTPException as exc:
        audit(current["id"], "command_result", json.dumps({"id": request_id, "status": "unknown" if exc.status_code in (503, 504) else "failed"}))
        raise
    audit(current["id"], "command_result", json.dumps({"id": request_id, "status": "completed"}))
    return result


@app.post("/api/v1/admin/completions")
async def completions(data: CompletionRequest, request: Request, current=Depends(admin)):
    check_csrf(request, current)
    if data.cursor > len(data.input.encode("utf-16-le")) // 2:
        raise HTTPException(422, "Cursor exceeds input length")
    return await agent_request("completion", data.model_dump())


@app.post("/api/v1/auth/login")
def login(data: Login, request: Request, response: Response):
    check_origin(request)
    now = time.monotonic()
    with login_lock:
        if len(login_attempts) >= 4096 and data.username not in login_attempts:
            for key in list(login_attempts):
                if not login_attempts[key] or login_attempts[key][-1] < now - 300:
                    del login_attempts[key]
            if len(login_attempts) >= 4096:
                raise HTTPException(429, "Too many login attempts")
        attempts = [entry for entry in login_attempts.get(data.username, []) if entry > now - 300]
        if len(attempts) >= 5:
            raise HTTPException(429, "Too many login attempts")
        attempts.append(now)
        login_attempts[data.username] = attempts
    with connect() as db:
        row = db.execute("SELECT * FROM users WHERE username=? AND enabled=1", (data.username,)).fetchone()
        try:
            valid = row is not None and passwords.verify(row["password_hash"], data.password)
        except VerifyMismatchError:
            valid = False
        if not valid:
            audit(None, "login_failed", data.username)
            raise HTTPException(401, "Invalid credentials")
        token = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        db.execute("INSERT INTO sessions(token_hash,user_id,expires_at,csrf_hash) VALUES(?,?,?,?)", (hashlib.sha256(token.encode()).hexdigest(), row["id"], time.time()+86400, hashlib.sha256(csrf.encode()).hexdigest()))
    response.set_cookie("mc_session", token, httponly=True, samesite="lax", secure=os.environ.get("MCWEB_SECURE_COOKIE") == "true", max_age=86400)
    response.set_cookie("mc_csrf", csrf, httponly=False, samesite="lax", secure=os.environ.get("MCWEB_SECURE_COOKIE") == "true", max_age=86400)
    with login_lock:
        login_attempts.pop(data.username, None)
    audit(row["id"], "login")
    return {"id": row["id"], "username": row["username"], "role": row["role"]}


@app.post("/api/v1/auth/logout")
async def logout(request: Request, response: Response, mc_session: str = Cookie(), current=Depends(user)):
    check_csrf(request, current)
    with connect() as db:
        db.execute("DELETE FROM sessions WHERE token_hash=?", (hashlib.sha256(mc_session.encode()).hexdigest(),))
    response.delete_cookie("mc_session")
    response.delete_cookie("mc_csrf")
    disconnect_user(current["id"])
    audit(current["id"], "logout")
    return {"ok": True}


@app.get("/api/v1/auth/me")
def me(current=Depends(user)):
    return {key: current[key] for key in ("id", "username", "role", "expires_at")}


@app.get("/api/v1/server/status")
def status(current=Depends(user)):
    return state


@app.post("/api/v1/admin/users")
def create_user(data: CreateUser, request: Request, current=Depends(admin)):
    check_csrf(request, current)
    if len(data.password) < 12:
        raise HTTPException(422, "Password must contain at least 12 characters")
    with connect() as db:
        try:
            db.execute("INSERT INTO users(username,password_hash,role) VALUES(?,?,?)", (data.username, passwords.hash(data.password), data.role))
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Username already exists")
    audit(current["id"], "create_user", data.username)
    return {"ok": True}


@app.get("/api/v1/admin/users")
def list_users(current=Depends(admin)):
    with connect() as db:
        rows = db.execute("SELECT id, username, role, enabled FROM users ORDER BY username").fetchall()
    return {"users": [dict(row) for row in rows]}


def disconnect_user(user_id: int):
    for queue, owner in tuple(listener_users.items()):
        if owner == user_id:
            listeners.discard(queue)
            admin_listeners.discard(queue)
            if queue.full():
                queue.get_nowait()
            queue.put_nowait('event: session\ndata: {"status":"revoked"}\n\n')


@app.put("/api/v1/admin/users/{user_id}")
async def update_user(user_id: int, data: UserUpdate, request: Request, current=Depends(admin)):
    check_csrf(request, current)
    password_hash = await asyncio.to_thread(passwords.hash, data.password) if data.password else None
    with connect() as db:
        db.execute("BEGIN IMMEDIATE")
        target = db.execute("SELECT id, username, role, enabled FROM users WHERE id=?", (user_id,)).fetchone()
        if not target:
            raise HTTPException(404, "User not found")
        if target["role"] == "admin" and target["enabled"] and (data.role != "admin" or not data.enabled):
            count = db.execute("SELECT count(*) FROM users WHERE role='admin' AND enabled=1").fetchone()[0]
            if count <= 1:
                raise HTTPException(409, "Cannot disable the last administrator")
        db.execute("UPDATE users SET role=?, enabled=?, password_hash=COALESCE(?, password_hash) WHERE id=?", (data.role, data.enabled, password_hash, user_id))
        db.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
    disconnect_user(user_id)
    audit(current["id"], "update_user", target["username"])
    return {"ok": True}


@app.post("/api/v1/auth/password")
async def change_password(data: PasswordChange, request: Request, current=Depends(user)):
    check_csrf(request, current)
    with connect() as db:
        row = db.execute("SELECT password_hash FROM users WHERE id=?", (current["id"],)).fetchone()
        try:
            valid = await asyncio.to_thread(passwords.verify, row["password_hash"], data.old_password)
        except VerifyMismatchError:
            valid = False
        if not valid:
            raise HTTPException(400, "Incorrect password")
        new_hash = await asyncio.to_thread(passwords.hash, data.new_password)
        db.execute("UPDATE users SET password_hash=? WHERE id=?", (new_hash, current["id"]))
        db.execute("DELETE FROM sessions WHERE user_id=?", (current["id"],))
    disconnect_user(current["id"])
    audit(current["id"], "change_password")
    return {"ok": True}


@app.get("/api/v1/events")
async def events(request: Request, current=Depends(user)):
    queue = asyncio.Queue(maxsize=128)
    listeners.add(queue)
    listener_users[queue] = current["id"]
    is_admin = current["role"] == "admin"
    if is_admin:
        admin_listeners.add(queue)
        await sync_log_subscription()
    async def stream():
        try:
            yield f"event: status\ndata: {json.dumps(state)}\n\n"
            while queue in listeners:
                if time.time() >= current["expires_at"]:
                    yield 'event: session\ndata: {"status":"expired"}\n\n'
                    break
                try:
                    yield await asyncio.wait_for(queue.get(), timeout=20)
                except TimeoutError:
                    yield ": heartbeat\n\n"
        finally:
            listeners.discard(queue)
            listener_users.pop(queue, None)
            if is_admin:
                admin_listeners.discard(queue)
                await sync_log_subscription()
    return StreamingResponse(stream(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


async def sync_log_subscription():
    peer = agent
    if peer is not None:
        async with agent_send_lock:
            if peer is agent:
                try:
                    await peer.send_json({"type": "logs_subscribe", "enabled": bool(admin_listeners)})
                except (WebSocketDisconnect, RuntimeError, OSError):
                    logger.info("Agent disconnected while changing log subscription")
@app.get("/api/v1/admin/logs")
def recent_logs(current=Depends(admin)):
    return {"lines": list(log_lines)[-500:]}


@app.get("/api/v1/admin/audit")
def audit_log(current=Depends(admin)):
    with connect() as db:
        rows = db.execute("SELECT audit_events.id, created_at, users.username, action, detail FROM audit_events LEFT JOIN users ON users.id=audit_events.user_id ORDER BY audit_events.id DESC LIMIT 200").fetchall()
    return {"events": [dict(row) for row in rows]}


@app.websocket("/internal/v1/agent")
async def agent_socket(ws: WebSocket):
    global agent
    expected = os.environ.get("MCWEB_AGENT_TOKEN", "")
    supplied = ws.headers.get("authorization", "")
    if not expected or not hmac.compare_digest(supplied, "Bearer " + expected):
        await ws.close(code=1008)
        return
    async with agent_connect_lock:
        if agent is not None:
            await ws.close(code=1008)
            return
        await ws.accept()
        agent = ws
    try:
        async with agent_send_lock:
            await ws.send_json({"type": "set_policy", "policy": current_policy()})
            if admin_listeners:
                await ws.send_json({"type": "logs_subscribe", "enabled": True})
        while True:
            message = await ws.receive_json()
            if message.get("type") == "status" and isinstance(message.get("data"), dict):
                incoming = message["data"]
                phase = incoming.get("shutdown")
                if phase in ("preparing", "failed", "poweroff_requested") and phase != state.get("shutdown"):
                    audit(None, "shutdown_" + phase, str(incoming.get("shutdown_kind", "unknown"))[:32])
                set_state(message["data"])
            elif message.get("type") == "response":
                future = pending.get(message.get("id"))
                if future is not None and not future.done():
                    future.set_result(message)
            elif message.get("type") == "log" and isinstance(message.get("line"), str):
                line = message["line"][:4096]
                for secret in (os.environ.get("MCWEB_AGENT_TOKEN"), plug.token if plug else None):
                    if secret:
                        line = line.replace(secret, "[REDACTED]")
                log_lines.append(line)
                publish("log", {"line": line}, admin_only=True)
    except WebSocketDisconnect:
        pass
    finally:
        agent = None
        for future in tuple(pending.values()):
            if not future.done():
                future.set_result({"error": "Agent disconnected; command outcome may be unknown"})
        set_state({"host": "unknown", "host_boot_id": None, "container": "unknown", "container_exit_code": None, "container_started_at": None, "minecraft": "unknown", "minecraft_version": None, "neoforge_version": None, "mod_version": None, "online": None, "max_players": None, "players": [], "uptime_seconds": None, "mspt": None, "tps": None, "memory_used": None, "memory_max": None, "host_cpu": None, "host_memory_used": None, "host_memory_max": None, "boot_id": None, "activity_version": None, "idle_since": None, "policy_revision": None, "policy_enabled": False})


static_dir = os.environ.get("MCWEB_STATIC_DIR")
if static_dir:
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")

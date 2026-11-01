# Minecraft Server Web UI

提供 Minecraft 1.21.1 NeoForge 服务端的按需开服、空闲关机、状态和管理控制台。项目由 Vue 前端、FastAPI 后端、SQLite、Ubuntu 宿主机代理和独立 `command-api` mod 组成。

普通账户可以查看状态与开机；管理员可执行命令及补全、查看日志和审计、管理账户及策略、请求正常关机。浏览器使用 SSE，代理和 mod 使用 WebSocket，状态变化通过连接推送。后端使用局域网 MIoT 协议每 30 秒读取插座状态，不使用 HTTP 轮询。数据库版本由 Alembic 管理。

自动关机默认关闭。启用前须完成 [部署与验证](docs/deployment.md) 中的插座型号、低功率断电规则、主机来电开机和数据备份检查；真实设备及 Docker 环境尚未验证。公网 HTTP 会暴露密码、会话和控制命令。

生产环境使用一个 WebUI 容器，FastAPI 直接提供前端，不需要 Nginx。GitHub Actions 在默认分支更新或推送 `v` 开头的版本标签且检查通过后，构建 amd64、arm64 镜像并推送到 `ghcr.io/所有者/仓库名`；也可在默认分支手动运行。部署方式和镜像拉取说明见 [部署与验证](docs/deployment.md)。

## 开发

需要 Python 3.13 或以上、uv、Node.js 24、pnpm。配置示例位于 `deploy/`：

```powershell
uv sync
pnpm install --frozen-lockfile
$env:PYTHONPATH = "backend;agent"
$env:MCWEB_AGENT_TOKEN = "开发环境随机密钥"
uv run python -m app.db admin
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

另一个终端执行 `pnpm --filter web dev --host 127.0.0.1`。代理环境变量和容器部署见 [部署说明](docs/deployment.md)。请勿提交 `.env`、数据库或设备凭据。

检查：

```powershell
$env:PYTHONPATH = "backend;agent"
uv run --frozen python -m unittest discover -s tests -v
pnpm --filter web typecheck
pnpm --filter web build
```

`packages/ui` 来源于同一工作区 `moetopia-AIO/packages/ui`，其原 README 的相对路径属于原项目。实时连接和断线语义见 [协议约定](docs/realtime-protocol.md)。

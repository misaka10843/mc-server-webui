# Minecraft Server WebUI

在 NAS 上管理家中的 Minecraft 笔记本：需要时开服，无人时正常关机，随时查看状态、玩家和日志。

NAS 只运行一个 WebUI 容器，包含 Vue 前端、FastAPI 后端和 SQLite。笔记本保留现有 SSH、Minecraft Docker 容器及 `command-api` mod，无需安装独立代理或 Python 环境。前端由 FastAPI 提供，不需要 Nginx。

- 普通账户：查看状态、一键开服、复制游戏地址。
- 管理员：命令与补全、实时日志、日夜关机计划、SSH 和插座配置、账户及审计。
- 首次访问网页即可创建管理员，账户密码至少 8 位。
- SSH 首次连接自动记住主机密钥，后续验证；密码、私钥和 mod 密钥在网页保存。
- 米家扫码连接插座，保存后通过云端控制；无需 NAS 能直接访问插座 IP。
- 浏览器使用 SSE，mod 通过 SSH 隧道建立 WebSocket；Docker 状态和日志通过持续 SSH 流传输。只有打开控制台时才订阅日志，不使用 HTTP 状态轮询。

## 部署

完整步骤见 **[NAS + 笔记本部署指南](docs/deployment.md)**，包含权限配置、Minecraft 配置片段、网页初始化、真实开关机验证、升级备份及群晖常见错误。

NAS 上的快速启动：

```bash
cp deploy/backend.env.example .env
chmod 600 .env
mkdir -p data
sudo chown 1000:1000 data
sudo chmod 700 data
sudo docker compose up -d --build
```

打开 `http://NAS的IP:10843` 创建管理员，然后在“连接设置”配置笔记本和插座。新 `.env` 使用端口 10843；旧 `.env` 未设 `MCWEB_HTTP_PORT` 时仍使用 8080。已有 `.env` 和 `data/` 请保留。

默认游戏地址为 `192.168.101.41:25565`。自动关机默认关闭；确认来电开机、低功率断电规则和正常停服流程后，再启用计划。默认夜间 23:30 至 09:00 连续无人 30 分钟，白天连续无人 90 分钟。

GitHub Actions 在默认分支更新或推送 `v` 开头的版本标签且检查通过后，发布 amd64、arm64 镜像到 `ghcr.io/misaka10843/mc-server-webui`。GHCR 部署和更新方法见部署指南。

## 本地开发

需要 Python 3.13+、uv、Node.js 24 和 pnpm 12.14.0：

```powershell
uv sync --frozen
pnpm install --frozen-lockfile
$env:PYTHONPATH = "backend;agent"
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

另一个终端运行 `pnpm --filter web dev --host 127.0.0.1`，首次访问页面创建本地管理员。

```powershell
$env:PYTHONPATH = "backend;agent"
uv run --frozen python -m unittest discover -s tests -v
pnpm --filter web typecheck
pnpm --filter web build
```

`packages/ui` 是当前项目使用的组件库，来自同工作区的 Moetopia UI。实时连接、空闲计时和关机复核语义见 [协议说明](docs/realtime-protocol.md)。SSH 与米家云凭据保存在 `data/` 数据库中，请限制该目录的访问并备份，不要提交 `.env`、数据库或认证信息。

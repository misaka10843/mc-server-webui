# 部署与验证

本方案有两台机器：常开设备运行 WebUI 容器和 frpc；Ubuntu 笔记本运行现有 Minecraft Docker 容器和宿主机代理。WebUI 的 FastAPI 进程直接提供前端，无需 Nginx。先备份世界。以下配置模板需要根据实际 IP、端口、容器名和设备型号修改，不能直接复制到生产环境执行。

## 一、设备信息

1. 确认笔记本断电后再次供电能自动开机，且从完全关机状态重复验证。
2. 插座在米家中配置低功率持续 N 分钟后关闭。分别测量 Minecraft 空闲运行、Ubuntu 正常关机、关机后的电池充电功率；确保正常运行不会触发，关机后能可靠关闭。
3. 使用 [Xiaomi Cloud Tokens Extractor](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor) 获取插座的实际 model、IP 和 token；地区应与米家账户相同。也可通过该项目支持的扫码登录。不要将 token 发给其他人或提交到 Git。
4. 在 [MIoT 设备规格目录](https://home.miot-spec.com/)按实际 model 查找设备，找到开关的 service ID（siid）和 property ID（piid）。本项目使用局域网 `get_properties` / `set_properties`，需先独立验证此设备的固件支持这两项操作；商品名不能代替 model。后端每 30 秒进行一次局域网设备读取，不轮询 HTTP。
5. 给常开设备、笔记本和插座设置固定地址。常开设备和 frpc 不能由将要关闭的插座供电。

## 二、常开设备

安装 Docker 与 Compose，在仓库根目录执行：

```bash
cp deploy/backend.env.example .env
chmod 600 .env
mkdir -p data
sudo chown 1000:1000 data
```

编辑 `.env`：

- `MCWEB_LAN_SERVER_ADDRESS` 是局域网游戏地址，默认 `192.168.101.41:25565`。
- `MCWEB_SERVER_ADDRESS` 仅用于在网页展示公网游戏地址，可留空；它不参与开关机。
- `MCWEB_AGENT_TOKEN` 用独立的高强度随机字符串。
- `MCWEB_LAN_IP` 是常开设备的局域网 IP；后端 8000 只应允许笔记本访问。
- `MCWEB_PLUG_*` 使用实际设备信息与已验证的开关属性。

```bash
docker compose build
docker compose run --rm webui python -m app.db 管理员用户名
docker compose up -d
```

也可以在镜像发布到 GHCR 后，在 `.env` 中设置 `MCWEB_IMAGE=ghcr.io/所有者/仓库名:latest`（镜像名使用小写），然后执行 `docker compose pull`、`docker compose run --rm webui python -m app.db 管理员用户名` 和 `docker compose up -d --no-build`。更新时重新执行 `docker compose pull` 和 `docker compose up -d --no-build`。私有 GHCR 包需要先登录并拥有拉取权限；公开包可匿名拉取。

管理员初始化通过交互式输入密码。`data/` 为 SQLite 数据目录，需要定期备份；使用 SQLite 在线备份工具，或者先停止容器再复制整个目录，确保 WAL 内容一并保存。使用防火墙将 8000 限制为笔记本 IP。8080 提供网页和浏览器 API，不接受内部代理连接；8000 只接受代理 WebSocket。Web 监听常开设备的 8080 端口，你可以通过 `http://常开设备局域网IP:8080` 访问；frpc 仍可连接 `127.0.0.1:8080` 并转发到阿里云。后端根据当前请求校验同源和 CSRF，不需要预先列出网页 IP；如另外使用 HTTP 反向代理，必须原样传递包含端口的 Host。两个地址在浏览器中各自保存登录状态。公网入口目前是 HTTP，密码、会话和命令在浏览器到公网入口之间未加密。frpc 本身应启用认证和传输加密。

示例 frpc 配置，按已有 frp 版本调整：

```toml
serverAddr = "阿里云IP"
serverPort = 7000
auth.method = "token"
auth.token = "与frps一致的密钥"
[[proxies]]
name = "mc-web"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8080
remotePort = 需要开放的网页端口
transport.useEncryption = true
```

## 三、Minecraft 笔记本

将 `command-api` 构建得到的 JAR 安装进现有 NeoForge 1.21.1 服务端 mods 目录。当前构建和 mod 元数据要求 NeoForge **21.1.265 或更新的 21.1 版本**；先核对整合包使用的版本和兼容性，升级前备份，不要直接覆盖世界。现有 `itzg/minecraft-server:java21` 容器需使用 NeoForge 1.21.1，设置：

```yaml
services:
  minecraft:
    restart: "no"
    stop_grace_period: 6m
    environment:
      COMMAND_API_TOKEN: "与代理一致的独立随机密钥"
      COMMAND_API_PORT: "8766"
      STOP_DURATION: "300"
      ENABLE_AUTOSTOP: "FALSE"
      ENABLE_AUTOPAUSE: "FALSE"
    ports:
      - "127.0.0.1:8766:8766"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "10"
```

这是合并到现有 Compose 的片段，不应覆盖现有世界、端口及整合包配置。确保自动停止后不会被外部进程重新启动。给 mod 和代理使用同一个独立 token，不能复用后端 agent token。系统异常关机时 Docker 停机超时也需大于 `STOP_DURATION`。

在笔记本上以管理员权限创建专用系统账户、复制项目并安装代理；以下命令示例假设已将项目检出到 `/opt/mc-server-webui`：

```bash
sudo useradd --system --user-group --home /opt/mc-server-webui --shell /usr/sbin/nologin mc-agent
sudo usermod -aG docker mc-agent
sudo python3 -m venv /opt/mc-server-webui/.venv
sudo /opt/mc-server-webui/.venv/bin/pip install -r /opt/mc-server-webui/deploy/agent/requirements.txt
sudo install -o root -g mc-agent -m 0640 deploy/agent/agent.env.example /etc/mc-server-agent.env
sudo install -D -o root -g root -m 0755 deploy/agent/mc-server-poweroff /usr/local/libexec/mc-server-poweroff
sudo install -o root -g root -m 0440 deploy/agent/sudoers-mc-agent /etc/sudoers.d/mc-server-agent
sudo visudo -cf /etc/sudoers.d/mc-server-agent
sudo install -o root -g root -m 0644 deploy/agent/*.service /etc/systemd/system/
```

编辑 `/etc/mc-server-agent.env`，填入 backend WebSocket 地址、两个 token 和目标容器名。Docker 组有宿主机高权限，应确保该账户和配置文件不被其他用户写入。`MC_AGENT_AUTO_SHUTDOWN=false` 是首次安装默认值；设备低功率规则通过验证后可改为 `true`。网页中的自动关机开关也需要打开并确认主机同步；两项必须同时满足。

如果在关机流程执行期间修改策略，后端会保存新值，但代理会拒绝立即应用；页面会显示等待同步。若本次关机失败并保持开机，请重新保存策略以完成同步。

如果停服、容器检查或系统关机发生错误，自动关机会暂停，避免按旧计时反复尝试。管理员应先检查并处理错误，再在策略页面重新保存以确认恢复；玩家进入或时段切换导致的正常复核取消会自动重新计时。

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now minecraft-container.service mc-server-agent.service
sudo systemctl status minecraft-container.service mc-server-agent.service
```

`minecraft-container.service` 在每次 Ubuntu 开机时执行一次 `docker start`；自动关机后不会被 Docker 自动拉起。`mc-server-poweroff` 只执行 `systemctl poweroff`，代理需要在 mod 确认停服及 Docker 验证正常退出后才调用它。不要把整个 sudo 或任意 Docker 参数暴露给网页。

## 四、验收

先使用备份世界和临时测试时间：验证普通用户开机、管理员命令与补全、日志权限、玩家加入时取消空闲、23:30 和 09:00 边界、异常退出不关机、正常退出后 Ubuntu 关机和插座自行断电。确认笔记本上电后容器能再次启动。最后检查真实阈值和 30 / 90 分钟设置。异常时保持插座供电，检查容器日志、`journalctl -u mc-server-agent` 与后端日志；主机离线并不等于完成关机。

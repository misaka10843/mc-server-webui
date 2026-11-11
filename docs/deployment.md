# 部署指南：NAS + Minecraft 笔记本

这份指南按实际部署顺序编写：准备笔记本 → 启动 NAS 网页 → 在网页连接设备 → 验证开关机。

## 先看部署结构

```text
你 / 朋友的浏览器
       │
       ▼
NAS：一个 WebUI Docker 容器 + SQLite
       ├── HTTPS → 米家云 → 智能插座
       └── 局域网 SSH → 笔记本 192.168.101.41
                           └── Docker → Minecraft + command-api mod
```

笔记本不需要安装代理、Python、额外关机脚本或新的 systemd 服务。SSH 连接、空闲计时、日志订阅和关机流程都由 NAS 管理。NAS 要保持常开，不能接在将要断电的插座上。

| 用途 | 地址 / 端口 | 说明 |
| --- | --- | --- |
| 网页 | `http://NAS的IP:10843` | 新 `.env` 模板使用 10843，可自行修改 |
| 笔记本 SSH | `192.168.101.41:22` | NAS 通过局域网连接 |
| Minecraft 游戏 | `192.168.101.41:25565` | 供 Minecraft 客户端连接 |
| mod 内部接口 | 笔记本 `127.0.0.1:8766` | 通过 SSH 隧道访问，无需对外开放 |

NAS 的 IP 和笔记本的 IP 是两个地址。网页使用 NAS 地址，游戏使用笔记本地址。

## 1. 准备笔记本

以下操作在 **Minecraft 笔记本**上执行。笔记本已有 Ubuntu、Docker、Minecraft 容器，且 NAS 能 SSH 登录时，直接继续配置 mod。

### 确认 SSH 与 Docker

从 NAS 试着连接一次：

```bash
ssh 你的用户名@192.168.101.41
docker ps --format '{{.Names}}'
```

记下 Minecraft 的实际容器名，网页中要填写同一个名字。SSH 密码就是该 Ubuntu 用户的登录密码，也可以使用现有 SSH 私钥。

如果尚未开启 SSH，在笔记本执行：

```bash
sudo apt install openssh-server
sudo systemctl enable --now ssh
```

如果普通用户执行 `docker ps` 没有权限，在笔记本执行后重新登录 SSH：

```bash
sudo usermod -aG docker "$USER"
```

### 安装 command-api mod

将 `command-api` JAR 放入现有服务端的 `mods/` 目录。客户端无需安装。

当前 mod 对应 **Minecraft 1.21.1 / NeoForge 21.1.265 或更新的 21.1 版本 / Java 21**。先核对整合包版本并备份世界，再修改服务端。源码构建方法见 command-api 仓库 README，构建产物在 `build/libs/`。

在笔记本的现有 Minecraft Compose 中合并下列内容。保留原来的世界目录、内存、整合包及游戏端口配置：

```yaml
services:
  minecraft:
    restart: "no"
    stop_grace_period: 6m
    environment:
      COMMAND_API_TOKEN: "换成你自己的随机密钥"
      COMMAND_API_PORT: "8766"
      STOP_DURATION: "300"
      ENABLE_AUTOSTOP: "FALSE"
      ENABLE_AUTOPAUSE: "FALSE"
    ports:
      - "25565:25565"
      - "127.0.0.1:8766:8766"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "10"
```

`COMMAND_API_TOKEN` 是你自己设定的一段密钥，之后原样填到 WebUI；不是米家 token。`restart: "no"` 避免正常停服后被 Docker 重新启动。NAS 会在笔记本每次新开机后的首次 SSH 连接中启动 Minecraft 容器。

更新笔记本上的容器配置并确认 mod 正常加载：

```bash
docker compose up -d
docker logs --tail=80 minecraft
```

上面的 `minecraft` 替换为实际容器名。

### 给 SSH 用户添加关机权限

root 账户可直接执行系统关机。普通用户仅需允许免密执行这一条命令：

```bash
command -v systemctl
sudo visudo -f /etc/sudoers.d/mc-webui
```

在文件中添加下面一行，替换用户名，并以 `command -v systemctl` 输出为准填写路径：

```text
你的用户名 ALL=(root) NOPASSWD: /usr/bin/systemctl poweroff
```

验证权限，下面命令只列出权限，不会关机：

```bash
sudo -n -l -- systemctl poweroff
```

到这里笔记本侧就准备好了。

## 2. 在 NAS 启动 WebUI

以下操作在 **NAS** 的项目目录中执行，例如：

```bash
cd /volume1/docker/mc-server-webui
```

### 方法 A：从源码构建

首次部署时复制配置模板；已有 `.env` 时保留原文件：

```bash
cp deploy/backend.env.example .env
chmod 600 .env
mkdir -p data
sudo chown 1000:1000 data
sudo chmod 700 data
```

`.env` 只需要几项基础配置：

```ini
MCWEB_HTTP_PORT=10843
MCWEB_LAN_SERVER_ADDRESS=192.168.101.41:25565
MCWEB_SERVER_ADDRESS=
MCWEB_SECURE_COOKIE=false
```

- `MCWEB_HTTP_PORT`：NAS 的网页端口，端口被占用时换一个。
- 两项游戏地址只用于页面展示；公网游戏地址不知道或不需要时留空。
- 当前通过 HTTP 访问时保留 `MCWEB_SECURE_COOKIE=false`。
- SSH 和插座信息全部在网页配置，不需要填进 `.env`。

启动：

```bash
sudo docker compose up -d --build
sudo docker compose ps
sudo docker compose logs --tail=50 webui
```

浏览器打开 **`http://NAS的局域网IP:10843`**。第一次直接在网页创建管理员，密码至少 8 位；已有数据库会进入原账户的登录页。先在局域网完成初始化，再将网页开放给朋友。

不需要 Nginx，不需要映射 8000 或 10844。旧 `.env` 没有 `MCWEB_HTTP_PORT` 时，为兼容旧配置，宿主端口仍为 8080；可以补上 `MCWEB_HTTP_PORT=10843` 后重新 `up -d`。

### 方法 B：使用 GHCR 镜像

如果 GitHub Actions 已成功发布对应版本，可以复用上述 `.env` 和 `data/`，再在 `.env` 添加：

```ini
MCWEB_IMAGE=ghcr.io/misaka10843/mc-server-webui:latest
```

```bash
sudo docker compose pull
sudo docker compose up -d --no-build
```

公开包可直接拉取，私有包需要先登录 GHCR。Actions 的默认分支更新会发布 `latest`，版本标签如 `v1.2.3` 对应镜像标签 `1.2.3`；同时构建 amd64 和 arm64。

## 3. 在网页连接设备

### 连接笔记本

管理员进入 **连接设置 → 笔记本连接**：

| 字段 | 填写示例 |
| --- | --- |
| 笔记本 IP | `192.168.101.41` |
| SSH 用户名 | 笔记本的 Ubuntu 用户名 |
| SSH 密码 | 该用户的密码 |
| Minecraft 容器名 | `minecraft`，以实际名称为准 |
| command-api 密钥 | 上面设置的 `COMMAND_API_TOKEN` |

点击“保存连接”即可。首次连接自动记住主机密钥；SSH 端口、mod 端口及私钥放在高级设置里，默认端口无需改动。保存过的密码和密钥留空表示沿用。

“测试连接”会单独检查 SSH、Docker 和关机权限，测试本身不会停止服务器。已有配置修改时无需先把笔记本开机；只有首次读取主机密钥需要在线。换 IP 或用户名时，重新填写认证信息。

保存后回到 **服务器概览**，笔记本 SSH 应显示“已连接”。Minecraft 世界加载完成后，才会显示“世界已就绪”。

### 连接智能插座

进入 **连接设置 → 智能插座 → 米家云**：

1. 选择与米家 App 一致的地区。
2. 点击“扫码连接米家”，用米家 App 扫码并在手机确认。
3. 从列表选择插座，点击“连接并保存插座”。

`cuco.plug.v3`（米家智能插座 3）会自动填写 **SIID 2、PIID 1**。其他型号可以展开开关属性，按 [MIoT 规格目录](https://home.miot-spec.com/) 填写服务和属性编号。

米家云模式不需要插座 IP 或设备 token，也不要求 NAS 能直连插座。保存前通过云端验证读取，成功后立即生效；云会话保存在 NAS 数据库，过期时重新扫码即可。

只有确认 NAS 可以局域网直连插座时，才使用“局域网直连”页。云端状态按需读取，可在概览里点击“刷新插座状态”；不会持续轮询米家云。

## 4. 验证开服与关机

### 确认硬件条件

笔记本必须能在插座重新供电后自动开机。请从完全关机状态验证，而不是只测睡眠唤醒。

插座在米家中设置低功率持续一段时间后断电。分别观察正常空闲运行、系统关机、关机后电池充电的功率，确认规则能正确区分。NAS 始终保持供电。

### 先手动，再自动

1. 保留世界备份，先确认网页显示游戏在线及正确的玩家数量。
2. 管理员点击“正常关机”。有玩家时会先广播 60 秒；mod 保存世界并停服，NAS 复核容器正常退出后再请求系统关机。
3. 确认笔记本关闭、插座随后按低功率规则断电。点击“刷新插座状态”确认。
4. 点击“启动服务器”。进度应依次经过插座供电、笔记本上线、启动容器、加载世界、可以加入。
5. 手动流程正常后，再进入“自动关机”启用计划。

默认计划按香港时间执行：**23:30 至次日 09:00，无人 30 分钟；其余时段无人 90 分钟**。跨时段保留已累计的无人时间；有人加入、mod 或 SSH 失联会重新计时。NAS 不运行时不会执行自动关机。

主机 SSH 断开只表示不可达，不能单独证明系统已关机；页面只有读到插座关闭才显示“已断电”。

## 5. 更新与备份

### 更新

源码部署：更新项目文件，然后执行：

```bash
sudo docker compose up -d --build
```

GHCR 部署：

```bash
sudo docker compose pull
sudo docker compose up -d --no-build
```

数据库会自动迁移，账户和设置保留。页面仍显示旧界面时按 `Ctrl+F5` 强制刷新。更新前备份 `data/` 和 `.env`；不要删除 `data/` 来解决升级问题。

### 备份

停止 WebUI 后复制整个数据库目录，确保 SQLite 的 WAL 文件一并保存：

```bash
sudo docker compose stop webui
sudo tar -czf mcweb-backup.tar.gz data .env
sudo chmod 600 mcweb-backup.tar.gz
sudo docker compose start webui
```

备份包含 SSH 和米家云凭据。恢复时停止容器，还原 `data/` 和 `.env`，确保 `data/` 归 UID/GID 1000，再启动。Minecraft 世界由笔记本原有备份方案另行备份。

## 常见问题

### 容器运行了，但网页打不开

在 NAS 执行：

```bash
sudo docker compose ps
curl -i http://127.0.0.1:10843/
```

`PORTS` 应显示 `10843->8080`。没有映射时，用当前 Compose 重新创建：

```bash
sudo docker compose up -d --force-recreate
```

本机 curl 正常而其他设备打不开时，检查访问的是 NAS 的真实 IP，以及群晖防火墙是否允许网页端口。`cannot assign requested address` 表示绑定了 NAS 没有的地址；当前配置无需绑定任何笔记本 IP，也不需要第二个端口映射。

### 提示无法读取 `/app/app/__init__.py`

更新 `deploy/Dockerfile` 并重新构建。镜像中的 COPY 已设置读取权限；修改宿主目录权限不会改变旧镜像。不要递归给项目设置 777。

### 提示 SQLite 或 `/data` 无写入权限

在 NAS 项目目录修正数据库目录的所属用户：

```bash
sudo chown -R 1000:1000 ./data
sudo chmod 700 ./data
sudo chmod 600 .env
sudo docker compose up -d
```

### SSH 已连接，Minecraft 仍在加载

查看“日志与命令”页。mod 只在游戏就绪后推送状态；确认 mod 已加载、`COMMAND_API_TOKEN` 与网页一致，并且笔记本映射了 `127.0.0.1:8766:8766`。使用“测试连接”确认实际容器名，不要把游戏端口 25565 当成 mod 端口。

### SSH 主机密钥变化

如果确实重装过笔记本或重建了 SSH 主机密钥，在高级设置点击“重新读取主机指纹”，再保存。日常使用无需手动确认指纹。

### `Unable to discover the device 192.168.101.6`

这是局域网直连失败。切到“米家云”，重新扫码选择插座并保存即可，不必为此修改 NAS 的 Docker 网络模式。

### 无法自动关机

先检查自动关机是否启用，再确认在线玩家为零、mod 和 SSH 均已连接。上次关机失败时，处理错误后重新保存计划恢复。Docker 的 restart 策略必须为 `no`，异常退出或复核失败时程序会保留主机供电。

### 以前安装过代理

只在笔记本确实安装过旧代理时停用它：

```bash
sudo systemctl disable --now mc-server-agent.service minecraft-container.service
```

然后在网页保存 SSH 配置。新的部署流程不需要上述两个服务。

### 朋友如何访问

将 NAS 的网页端口接入已有公网入口即可；朋友不需要访问笔记本的 SSH 或 mod 端口。先创建普通账户，再把网页地址和游戏公网地址分别提供给朋友。网页 HTTP 不加密密码和会话，公开访问时使用 HTTPS 入口；应用内部仍只需要一个 WebUI 容器。

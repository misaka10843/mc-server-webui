# 实时与主机协议

浏览器通过同源 SSE `/api/v1/events` 接收状态和操作进度。仅管理员打开日志与命令页面时使用 `?logs=true` 订阅日志，离开页面后停止日志传输。登录、开关机、命令和补全使用单次 HTTP 请求，没有 HTTP 状态轮询。

NAS 通过持续 SSH 连接管理笔记本。首次连接自动记录主机密钥，后续连接固定验证，断线按 1 至 30 秒退避重连。mod `/ws` 仅监听笔记本回环端口，通过只绑定 NAS 回环地址的 SSH 隧道访问，使用独立 Bearer token。

mod 握手后推送 `status` 快照，玩家变化立即推送，性能指标每 100 tick 更新。Docker 状态来自远程 `docker events`，管理员共用一条按需开启的 `docker logs --follow`。慢 SSE 消费者被断开，重连获得新快照。日志断线期间的持久历史以 Docker 轮转日志为准。

- `command`：ID 和 input，响应带同一 ID 和输出，超时或断线后不自动重发。
- `completion`：ID、input、UTF-16 cursor，响应带建议和替换范围。
- 自动 `shutdown`：ID、boot_id、activity_version、min_idle_seconds、expires_at_ms，到期时间不晚于下一个策略时段边界。mod 在游戏线程复核人数、运行标识和无人时间。
- 手动 `shutdown_manual`：有玩家时先广播 60 秒，执行前断线会取消。

空闲计时在 NAS 上运行；SSH 或 mod 断线时停止，恢复后从零计算。按香港时间当前日夜阈值检查连续无人时间，跨时段不重置。

mod 正常停服后，NAS 经 SSH 等待同一容器退出，复核退出码、启动时间、重启次数及关闭的 restart 策略，才执行系统关机。不自动重发关机命令。SSH 断线本身不能证明主机完成关机。

米家云扫码通过 SSE 响应完成。云会话保存在 NAS 数据库，不返回浏览器，云状态按需读取。局域网插座模式仍以 MIoT 每 30 秒读取一次，属于设备协议读取。

旧版 `/internal/v1/agent` 兼容接口保留；启用 SSH 时拒绝代理连接，默认 Compose 不暴露代理端口，新部署不需要笔记本代理。

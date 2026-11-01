# 实时与内部协议

浏览器通过同源 SSE `/api/v1/events` 接收状态、操作进度和授权后的管理员日志；登录、开机、关机、命令和补全使用单次 HTTP 请求。代理主动连接后端 WebSocket `/internal/v1/agent`；代理与 mod 连接 `/ws`。两条 WebSocket 均使用各自独立的 Bearer token。没有 HTTP 状态轮询。

mod 握手后推送 `status` 快照，之后玩家变化时立即推送，性能指标每 100 个 tick 更新；代理每 10 秒采集一次本机指标。后端在有更新时广播 SSE。Docker 容器状态来自 Docker 事件流；插座通过米家局域网 MIoT 协议每 30 秒读取一次。SSE 注释和 WebSocket ping 是连接保活，不代表服务器已关机。

内部消息包括：

- mod `status`：游戏就绪、版本、在线玩家、运行标识、活动版本、TPS/MSPT 和 JVM 内存。
- `command`：`id`、`input`；响应带相同 `id` 和输出。超时或断线后的结果可能未知，禁止自动重发。
- `completion`：`id`、`input`、UTF-16 `cursor`；响应带建议、UTF-16 替换范围及可选提示。
- 自动 `shutdown`：`id`、`boot_id`、`activity_version`、`min_idle_seconds`、`expires_at_ms`；过期时间不晚于下一个策略时段切换，mod 在游戏线程核对全部字段及当前人数与无人时间。
- 手动 `shutdown_manual`：有玩家时先广播 60 秒；执行前若连接中断则取消。
- 代理收到 `set_policy` 后确认版本并报告本机实际启用状态；后台失联时保留本次运行最后确认的策略。
- 管理员订阅 SSE 时后台向代理发送 `logs_subscribe`；所有管理员共用一条 Docker 日志流。

请求有并发上限和超时；缓慢 SSE 消费者被断开，重连后获得新快照。日志流不承诺断线期间完整重放，持久历史以 Docker json-file 轮转日志为准。代理与 mod 断线期间停止空闲计时；重新连接从零计算。

自动关机按香港时间夜间和白天的当前阈值检查连续空闲；跨时段不重置计时。mod 最终核对后正常关闭游戏；代理只在同一容器实例正常退出、启动时间与重启计数未变化且重启策略关闭时请求系统关机。主机离线不表示系统已关机；插座由米家自动化独立断电，后端只有读到插座关闭后才标记已断电。

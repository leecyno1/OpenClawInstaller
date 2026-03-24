# Findings

- 官方当前语义是 `gateway.bind` + `gateway.port`，默认 `gateway.bind=loopback`，不再推荐把 `gateway.bind` 写成 `host:port`。
- 官方远程访问建议是保留 loopback，再通过 SSH 隧道、反向代理或 Tailscale Serve/Funnel 暴露；非 loopback 绑定必须有共享认证。
- 本项目此前同时存在两类漂移：
  - 仍在写 `gateway.host` / `gateway.bind=127.0.0.1:13145` 这类旧式配置
  - 菜单在启用插件时默认写入 `dmPolicy: pairing`，导致用户完成渠道配置后首次私聊仍被卡在 pairing 审批
- 已将网关配置切到官方 bind 语义，并将常用私聊渠道在用户完成凭据录入后改为显式 `dmPolicy=open + allowFrom=["*"]`，避免首次使用卡在配对审批。

# Progress

- 2026-03-17: 读取历史会话，确认两类根因同时存在：旧 gateway URL/绑定语义导致远程不稳定，pairing 默认行为导致首次私聊被卡住。
- 2026-03-17: 更新 `install.sh`，改为官方 `gateway.bind` 语义，默认 loopback，持久化 `gateway.auth.mode=token` 与 token。
- 2026-03-17: 更新 `config-menu.sh`，同步 bind 语义、移除插件启用时隐式写入的 pairing 默认值，并为 Telegram/Discord/Feishu/WeCom 完成配置后直接放开私聊使用。
- 2026-03-17: 执行 `bash -n install.sh`、`bash -n config-menu.sh`，均通过。

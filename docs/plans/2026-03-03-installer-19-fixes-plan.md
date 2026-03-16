# auto-install-Openclaw 19 项修复实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 解决升级后易坏、飞书插件易失效的问题，并将安装器行为与官方升级/插件机制对齐。

**Architecture:** 以“升级链路标准化 + 插件链路标准化 + 错误语义修复 + 配置一致性修复”为主线，分 P0/P1/P2 三批推进。P0 优先保证可升级、可回滚、可观测；P1 收敛命令与配置；P2 做工程化兜底。

**Tech Stack:** Bash, OpenClaw CLI, npm, jq, curl

---

## P0（立即执行）

1. 新增统一升级函数：备份配置 -> 升级 core -> doctor -> plugins update --all -> 健康检查。
2. 高级菜单“更新 OpenClaw”切换到统一升级函数，替代裸 `npm update -g openclaw`。
3. 升级失败时自动回滚 `~/.openclaw` 配置备份，并给出恢复指令。
4. 修复 `install.sh` 中 `openclaw models set` 的退出码误判（去除 `|| true` 造成的假成功）。
5. 修复 `install.sh` 中 `test_api_connection` 退出码误判（保留输出、正确记录 exit code）。
6. 修复 `install.sh` / `config-menu.sh` 的 `configure_custom_provider` 参数校验返回码（失败返回非 0）。
7. 飞书插件默认源改为官方包 `@openclaw/feishu`，社区包改为回退方案。
8. 飞书插件安装支持显式版本 pin（环境变量），默认 latest。
9. 飞书配置后增加插件/渠道探针检查并输出下一步排障指令。

## P1（随后执行）

10. 对齐服务启动命令语义（统一为 `openclaw gateway ...`，避免 `start --daemon` 混用）。
11. 对齐 README 与脚本中的升级命令（官方优先 `openclaw update --restart`）。
12. 增加 `read_secret` 输入能力，API Key 输入默认隐藏（可回显选项）。
13. 安全菜单改为真实落盘（shell/file/web/sandbox 开关写入 openclaw 配置）。
14. 升级流程产生日志文件（时间戳命名，记录每个阶段结果）。
15. 将 `doctor` 与插件更新的结果汇总显示（成功项/失败项）。
16. 渠道重启前后增加状态探针（Gateway 状态 + feishu/discord 等关键渠道状态）。

## P2（工程化完善）

17. 明确 Docker 配置模型与主安装链路关系，补充迁移说明（config.yaml vs env/json）。
18. 新增兼容性预检（lsof/setsid/jq/python3/node 缺失时的降级策略）。
19. 新增回归脚本（语法检查 + 关键命令链路静态检查）用于发布前自检。

## 执行顺序

- 当前会话先落地 P0 的 1-9。
- 完成 P0 后进行验证（bash -n + 关键函数路径检查）。
- 再推进 P1/P2。

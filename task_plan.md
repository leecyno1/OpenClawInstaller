# Task Plan: OpenClawInstaller 19 项修复

## Goal
按优先级完成 19 项升级稳定性与飞书兼容性修复，先保障升级闭环，再做一致性与工程化增强。

## Current Phase
Done

## Phases

### P0: 升级稳定性与飞书主链路
- [x] 1. 升级流程统一为 core + doctor + plugins update + health
- [x] 2. 高级菜单更新入口切换到统一升级流程
- [x] 3. 升级前配置备份与失败恢复
- [x] 4. 修复 install.sh 模型设置退出码误判
- [x] 5. 修复 install.sh API 测试退出码误判
- [x] 6. 修复 custom provider 参数失败返回码（install/config-menu）
- [x] 7. 飞书默认插件切换官方包
- [x] 8. 飞书插件支持版本 pin
- [x] 9. 飞书配置探针
- **Status:** complete

### P1: 一致性与安全增强
- [x] 10. 统一服务命令语义（systemd/launchd/docker 默认命令）
- [x] 11. 全文档升级命令与菜单路径对齐（README 已修）
- [x] 12. API Key/关键 Token 隐藏输入（install + config-menu 主要路径）
- [x] 13. 安全菜单真实落盘
- [x] 14. 升级日志文件化
- [x] 15. doctor/plugins 结果结构化展示（升级日志中）
- [x] 16. 渠道重启前后探针（channels list）
- **Status:** complete

### P2: 工程化兜底
- [x] 17. Docker 配置模型一致性说明/迁移（README + compose 注释）
- [x] 18. 依赖能力预检与降级（端口探针 lsof→pgrep）
- [x] 19. 发布前回归脚本（scripts/preflight-check.sh）
- **Status:** complete

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 官方飞书插件优先、社区回退 | 与官方对齐，同时保留兼容路径 |
| 升级流程失败时恢复配置备份 | 降低升级失败后的不可恢复风险 |
| 引入 preflight 检查脚本 | 在发布前自动拦截关键链路回归 |

## Errors Encountered
| Error | Resolution |
|-------|------------|
| 官方 raw 文档偶发超时 | 使用 GitHub API/缓存文件双路径对照 |
| 升级备份目标位于源目录内 | 调整到独立备份根目录 `~/.openclaw-upgrade-backups` |

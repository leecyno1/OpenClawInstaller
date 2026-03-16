# Progress Log

## Session: 2026-03-03

### Current Status
- **Phase:** 19 项修复已按序完成
- **Started:** 2026-03-03

### Actions Taken
- 新建 19 项修复计划：`docs/plans/2026-03-03-installer-19-fixes-plan.md`。
- 完成升级链路重构：core 升级、doctor、plugins 更新、健康检查、配置备份恢复。
- 完成飞书插件策略重构：官方优先、社区回退、版本 pin、配置探针。
- 修复退出码误判和参数校验返回码错误。
- 完成服务命令语义统一（systemd/launchd/docker）。
- 完成敏感输入隐藏、安全配置落盘、升级日志化。
- 完成 Docker 配置兼容说明和发布前自检脚本。

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| `bash -n install.sh` | 语法正确 | 通过 | PASS |
| `bash -n config-menu.sh` | 语法正确 | 通过 | PASS |
| `bash -n docker-entrypoint.sh` | 语法正确 | 通过 | PASS |
| `./scripts/preflight-check.sh` | 关键链路检查通过 | 通过（4 项 PASS） | PASS |

### Errors
| Error | Resolution |
|-------|------------|
| 官方 raw 文档请求超时 | 切换到 GitHub API + 本地缓存方式对照 |
| 备份递归风险（备份目录在配置目录内） | 改为独立目录 `~/.openclaw-upgrade-backups` |

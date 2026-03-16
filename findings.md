# Findings & Decisions

## Requirements
- 用户要求：依次开始并推进 19 项修复，重点解决升级失败与飞书插件更新问题。

## Official Comparison (关键)
- 官方升级闭环：`openclaw update --restart` 后执行 `openclaw doctor`，成功后执行 `openclaw plugins update --all`。
- 原仓库关键差异：仅 `npm update -g openclaw`，缺少 doctor 与插件升级链路。
- 飞书插件差异：官方生态为 `@openclaw/feishu`，原仓库默认社区包 `@m1heng-clawd/feishu`。

## Implemented Summary
- **升级稳定性**
  - 新增统一升级管线（含备份、doctor、plugins 更新、health）。
  - 失败恢复配置备份，升级日志落盘。
- **飞书插件**
  - 默认官方插件，支持 `OPENCLAW_FEISHU_PLUGIN_VERSION` pin。
  - 官方安装失败可回退社区包。
  - 配置后执行探针（插件/渠道/connectionMode）。
- **错误语义修复**
  - 修复 `install.sh` 中退出码误判。
  - 修复 custom provider 参数校验失败返回码。
- **一致性修复**
  - systemd/launchd/docker 服务命令统一到 gateway 语义。
  - README 升级命令与菜单路径更新。
  - Docker/主安装链路配置模型差异增加兼容说明。
- **安全与可维护性**
  - API Key/Bot Token/App Secret 输入默认隐藏。
  - 安全菜单改为真实写入 openclaw 配置。
  - 新增发布前自检脚本 `scripts/preflight-check.sh`。

## Verification Evidence
- `bash -n install.sh` PASS
- `bash -n config-menu.sh` PASS
- `bash -n docker-entrypoint.sh` PASS
- `./scripts/preflight-check.sh` PASS

## Remaining Risks
- 仍需在真实 OpenClaw 运行环境做端到端升级演练（含真实飞书 App 凭据）验证。

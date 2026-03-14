# 钉钉接入 OpenClaw（精简版）

来源：
- https://mp.weixin.qq.com/s/UcuCHJOQESAgxmUfKP2H7Q

参考图：
![钉钉原文截图](../images/source-dingtalk.png)

## 1. 前置条件
- OpenClaw 可运行（建议 2C4G 以上更稳）。
- 钉钉管理员权限（可创建应用/机器人）。
- 可用模型 API Key（按你实际供应商填写）。

## 2. 钉钉侧创建应用机器人
- 进入钉钉开发者平台，创建应用。
- 为应用添加机器人能力并发布。
- 在「凭证与基础信息」保存 `Client ID`、`Client Secret`。
- 配置可见范围并上线版本。

## 3. OpenClaw 侧安装与配置
```bash
# 方式 A：本项目配置菜单（推荐）
bash ./config-menu.sh
# 消息渠道配置 -> 非官方渠道配置 -> 钉钉（社区插件）

# 方式 B：手动命令
openclaw plugins install openclaw-channel-dingtalk@latest
openclaw channels add --channel dingtalk
openclaw gateway restart
```

## 4. 验证
- 把机器人加入钉钉群。
- 群里 `@机器人` 发送测试消息。
- 检查文本/图片/文件/语音等能力是否按预期可用。

## 5. 常见问题
- 搜不到机器人：检查应用是否发布、可见范围是否包含当前账号。
- 不回复：检查通道是否运行、`Client ID/Secret` 是否正确。
- 模型调用报错：单独检查模型 API Key 与网关日志。

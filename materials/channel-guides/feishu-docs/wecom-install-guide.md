# 企业微信（WeCom）接入 OpenClaw（精简版）

来源：
- https://mp.weixin.qq.com/s/xDs2GD1jWJEoWX5JHtb2qQ?poc_token=HAzPsmmjrPfnzLQD1vgaZdAU7XDnhF7u7oFuYqml

参考图：
![企业微信原文截图](../images/source-wecom.png)

## 1. 前置条件
- OpenClaw 已安装并可运行（`openclaw status` 正常）。
- 企业微信客户端更新到最新版。
- 你有创建企业微信智能机器人的权限（管理员或被授权）。

## 2. 企业微信侧创建机器人
- 进入企业微信「工作台 -> 智能机器人」。
- 创建时选择「API 模式创建」。
- 连接方式选择「长连接」（无需公网回调地址）。
- 创建后保存 `Bot ID` 和 `Secret`。

## 3. OpenClaw 侧安装与配置
优先走本项目本地插件包（更快），再执行配置向导：

```bash
# 方式 A：本项目配置菜单（推荐）
bash ./config-menu.sh
# 消息渠道配置 -> 非官方渠道配置 -> 企业微信（官方优先）

# 方式 B：手动命令
openclaw plugins install @wecom/wecom-openclaw-plugin
openclaw channels add --channel wecom
openclaw gateway restart
```

按提示填入 `Bot ID` 和 `Secret`。

## 4. 配对验证
- 在企业微信中给机器人发消息，拿到配对码。
- 执行：

```bash
openclaw pairing approve wecom <配对码>
```

- 再发消息验证是否可回复。

## 5. 常见问题
- 找不到「智能机器人」入口：升级客户端并确认管理员已开通能力。
- 插件安装慢：使用本项目离线包安装；必要时切 `npmmirror`。
- 配对码过期：重新发消息获取新配对码。
- 能收消息但不回复：检查 `openclaw gateway status` 和 `openclaw logs`。

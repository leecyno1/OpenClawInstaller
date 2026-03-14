# 飞书接入 OpenClaw（官方插件路线，精简版）

来源：
- https://larkcommunity.feishu.cn/wiki/LDmXwEVhJitBa5kU0mjc16VKneb

参考图：
![飞书原文截图](../images/source-feishu.png)

## 1. 前置条件
- OpenClaw 已安装，Node 版本符合要求（22.x）。
- 使用飞书开放平台可创建机器人/应用。
- 准备好模型 API Key（按你实际模型供应商）。

## 2. 安装飞书官方插件
本项目默认优先本地包，避免远端下载慢：

```bash
# 推荐：通过本项目配置菜单
bash ./config-menu.sh
# 消息渠道配置 -> 官方消息渠道插件 -> 飞书

# 手动命令
openclaw plugins install @openclaw/feishu
openclaw channels add --channel feishu
openclaw gateway restart
```

## 3. 飞书应用配置要点
- 在飞书开放平台创建应用并开启机器人能力。
- 配置必要权限（消息、群会话、文档等按需最小授权）。
- 在 OpenClaw 配置中填入 `App ID / App Secret` 或对应 token 字段。

## 4. 使用验证
- 在飞书中给机器人发起私聊或群聊 `@` 测试。
- 首次完成 onboarding 后再执行真实任务。

## 5. 常见问题
- 插件版本冲突：先卸载旧社区包，再装官方 `@openclaw/feishu`。
- Gateway 502：确保仅保留一个网关实例，端口与配置一致。
- 权限不足：按报错到飞书开放平台补授权并重启网关。

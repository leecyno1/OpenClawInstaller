# Nano Banana Service 使用指南

## 1. 功能定位
- 通过 NanoBanana 兼容服务生成图片/视频。
- 默认档位: 扩展档默认安装
- 仓库目录: `skills/default/nano-banana-service`
- 安装后目录: `~/.openclaw/skills/nano-banana-service`

## 2. 使用前准备
- `NANO_BANANA_API_KEY`
- `NANO_BANANA_BASE_URL`
- `NANO_BANANA_IMAGE_MODEL`
- `NANO_BANANA_VIDEO_MODEL`

## 3. 配置步骤
1. 推荐写入 `~/.openclaw/skills/nano-banana-service/service.env`。
2. 若服务商异步返回任务 ID，需按服务商方式轮询任务状态。

## 4. 推荐提问方式
- 请用 nano-banana-service 生成一张极简产品 KV。
- 请用 nano-banana-service 生成一段短视频脚本素材。

## 5. 手动验证
```bash
python3 skills/default/nano-banana-service/scripts/generate_media.py --help
```

## 6. 参考资料
- 上游来源: /Users/lichengyin/.codex/skills/nano-banana-service
- 本技能说明: `SKILL.md`

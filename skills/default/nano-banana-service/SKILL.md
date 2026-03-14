---
name: nano-banana-service
description: 使用 NanoBanana 第三方服务生成图片/视频。读取 NANO_BANANA_* 环境变量。
---

# Nano Banana Service

用于 NanoBanana 代理服务的图片/视频生成。

## 前置环境变量

- `NANO_BANANA_API_KEY`
- `NANO_BANANA_BASE_URL`
- `NANO_BANANA_IMAGE_MODEL`
- `NANO_BANANA_VIDEO_MODEL`

## 生成图片

```bash
python scripts/generate_media.py \
  --mode image \
  --prompt "极简风格的产品海报" \
  --output /tmp/nano-image.png
```

## 生成视频

```bash
python scripts/generate_media.py \
  --mode video \
  --prompt "一段 5 秒钟的城市夜景延时" \
  --output /tmp/nano-video.mp4
```

## 可选参数

- `--endpoint-image /v1/images/generations`
- `--endpoint-video /v1/videos/generations`
- `--size 1024x1024`

## 失败排查

1. `NANO_BANANA_BASE_URL` 连通性。
2. 模型名是否被服务商支持。
3. 若返回 url 为空，检查服务商是否采用异步任务接口。

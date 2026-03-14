#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
import urllib.request


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def http_json(url: str, payload: dict, api_key: str):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if api_key:
        req.add_header("Authorization", f"Bearer {api_key}")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, output: str):
    with urllib.request.urlopen(url, timeout=180) as r:
        body = r.read()
    with open(output, "wb") as f:
        f.write(body)


def resolve_output(data: dict, output: str):
    items = data.get("data") if isinstance(data, dict) else None
    if isinstance(items, list) and items:
        first = items[0]
        if isinstance(first, dict):
            b64 = first.get("b64_json")
            out_url = first.get("url")
            if b64:
                raw = base64.b64decode(b64)
                with open(output, "wb") as f:
                    f.write(raw)
                return
            if out_url:
                download(out_url, output)
                return

    # 一些服务返回 output_url / video_url
    for key in ("output_url", "video_url", "url"):
        if isinstance(data, dict) and data.get(key):
            download(str(data[key]), output)
            return

    fail(f"未解析到可用输出: {json.dumps(data, ensure_ascii=False)[:500]}")


def main():
    p = argparse.ArgumentParser(description="Generate image/video via NanoBanana-compatible endpoint")
    p.add_argument("--mode", choices=["image", "video"], required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--size", default="1024x1024")
    p.add_argument("--endpoint-image", default="/v1/images/generations")
    p.add_argument("--endpoint-video", default="/v1/videos/generations")
    args = p.parse_args()

    api_key = os.getenv("NANO_BANANA_API_KEY", "")
    base_url = os.getenv("NANO_BANANA_BASE_URL", "").rstrip("/")
    image_model = os.getenv("NANO_BANANA_IMAGE_MODEL", "nano-banana-pro-image")
    video_model = os.getenv("NANO_BANANA_VIDEO_MODEL", "nano-banana-pro-video")

    if not base_url:
        fail("NANO_BANANA_BASE_URL 未设置")

    if args.mode == "image":
        url = f"{base_url}{args.endpoint_image}"
        payload = {"model": image_model, "prompt": args.prompt, "size": args.size}
    else:
        url = f"{base_url}{args.endpoint_video}"
        payload = {"model": video_model, "prompt": args.prompt}

    data = http_json(url, payload, api_key)
    resolve_output(data, args.output)
    print(args.output)


if __name__ == "__main__":
    main()

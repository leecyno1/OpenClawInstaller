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
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, output: str):
    with urllib.request.urlopen(url, timeout=120) as r:
        body = r.read()
    with open(output, "wb") as f:
        f.write(body)


def main():
    p = argparse.ArgumentParser(description="Generate image via Gemini-compatible endpoint")
    p.add_argument("--prompt", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--size", default="1024x1024")
    p.add_argument("--endpoint", default="/v1/images/generations")
    args = p.parse_args()

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    base_url = (os.getenv("GEMINI_BASE_URL") or os.getenv("GOOGLE_BASE_URL") or "").rstrip("/")
    model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image-preview")

    if not base_url:
        fail("GEMINI_BASE_URL 未设置")

    url = f"{base_url}{args.endpoint}"
    payload = {
        "model": model,
        "prompt": args.prompt,
        "size": args.size,
    }

    data = http_json(url, payload, api_key)
    items = data.get("data") if isinstance(data, dict) else None
    if not items or not isinstance(items, list):
        fail(f"响应缺少 data 字段: {json.dumps(data, ensure_ascii=False)[:500]}")

    first = items[0] if items else {}
    b64 = first.get("b64_json") if isinstance(first, dict) else None
    out_url = first.get("url") if isinstance(first, dict) else None

    if b64:
        raw = base64.b64decode(b64)
        with open(args.output, "wb") as f:
            f.write(raw)
    elif out_url:
        download(out_url, args.output)
    else:
        fail(f"未找到可用图片数据: {json.dumps(first, ensure_ascii=False)[:500]}")

    print(args.output)


if __name__ == "__main__":
    main()

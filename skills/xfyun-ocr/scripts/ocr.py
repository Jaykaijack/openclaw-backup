#!/usr/bin/env python3
"""iFlytek OCR LLM API (通用文档识别/OCR大模型).

Recognize text from images using iFlytek's Spark-based OCR engine.
Supports complex layouts including formulas, tables, columns, and more.

Environment variables:
    XFYUN_APP_ID      - Required. App ID from https://console.xfyun.cn
    XFYUN_API_KEY     - Required. API Key
    XFYUN_API_SECRET  - Required. API Secret

Usage:
    # Basic OCR (JSON output)
    python ocr.py image.jpg

    # Markdown output
    python ocr.py image.jpg --format markdown

    # JSON + Markdown output
    python ocr.py image.jpg --format json,markdown

    # Include character-level coordinates
    python ocr.py image.jpg --result-option normal,char

    # Raw API JSON response
    python ocr.py image.jpg --raw

Examples:
    python ocr.py document.png --format json,markdown
    python ocr.py receipt.jpg
    python ocr.py formula.png --format markdown
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from time import mktime
from urllib.parse import urlencode, urlparse
from wsgiref.handlers import format_date_time

API_URL = "https://cbm01.cn-huabei-1.xf-yun.com/v1/private/se75ocrbm"


def build_auth_url(request_url: str, api_key: str, api_secret: str) -> str:
    """Build HMAC-SHA256 signed authentication URL."""
    url_result = urlparse(request_url)
    date = format_date_time(mktime(datetime.now().timetuple()))

    signature_origin = "host: {}\ndate: {}\nPOST {} HTTP/1.1".format(
        url_result.hostname, date, url_result.path
    )
    signature_sha = hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    signature_b64 = base64.b64encode(signature_sha).decode("utf-8")

    authorization_origin = (
        'api_key="%s", algorithm="%s", headers="%s", signature="%s"'
        % (api_key, "hmac-sha256", "host date request-line", signature_b64)
    )
    authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")

    params = {
        "host": url_result.hostname,
        "date": date,
        "authorization": authorization,
    }
    return request_url + "?" + urlencode(params)


def read_image_base64(image_path: str) -> str:
    """Read image file and return base64 string."""
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    with open(image_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    # Check base64 size (max 4MB for standard, 10MB per docs)
    if len(b64) > 10 * 1024 * 1024:
        print(f"Error: Image too large after base64 encoding. Max ~10MB.", file=sys.stderr)
        sys.exit(1)
    return b64


def detect_encoding(image_path: str) -> str:
    """Detect image format from extension."""
    ext = os.path.splitext(image_path)[1].lower()
    mapping = {
        ".jpg": "jpg",
        ".jpeg": "jpeg",
        ".png": "png",
        ".bmp": "bmp",
    }
    return mapping.get(ext, "jpg")


def build_request(app_id: str, image_b64: str, encoding: str,
                  result_option: str, result_format: str,
                  output_type: str) -> dict:
    """Build the OCR API request payload."""
    data = {
        "header": {
            "app_id": app_id,
            "status": 0,
        },
        "parameter": {
            "ocr": {
                "result_option": result_option,
                "result_format": result_format,
                "output_type": output_type,
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain",
                },
            }
        },
        "payload": {
            "image": {
                "encoding": encoding,
                "image": image_b64,
                "status": 0,
                "seq": 0,
            }
        },
    }
    return data


def call_ocr(api_url: str, api_key: str, api_secret: str, request_data: dict) -> dict:
    """Send OCR request and return JSON response."""
    auth_url = build_auth_url(api_url, api_key, api_secret)
    url_result = urlparse(api_url)

    body = json.dumps(request_data).encode("utf-8")
    req = urllib.request.Request(
        auth_url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "host": url_result.hostname,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body_text}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)


def extract_text(result_b64: str, prefer_markdown: bool = False) -> str:
    """Extract plain text or markdown from OCR result (base64-encoded)."""
    try:
        decoded = base64.b64decode(result_b64).decode("utf-8")
    except Exception:
        return result_b64

    # Try parsing as JSON
    try:
        data = json.loads(decoded)
    except json.JSONDecodeError:
        # Plain text result
        return decoded

    if isinstance(data, dict):
        # If markdown requested and available, return it
        if prefer_markdown and data.get("markdown"):
            return data["markdown"]

        # Walk through paragraphs/lines structure
        lines = []
        paragraphs = data.get("paragraphs", [])
        for para in paragraphs:
            para_lines = para.get("lines", [])
            for line in para_lines:
                text = line.get("text", "")
                if text:
                    lines.append(text)

        # Also try pages/lines structure
        if not lines:
            pages = data.get("pages", [])
            for page in pages:
                page_lines = page.get("lines", [])
                for line in page_lines:
                    text = line.get("text", "")
                    if text:
                        lines.append(text)

        if lines:
            return "\n".join(lines)

        # Fallback: if markdown exists, use it
        if data.get("markdown"):
            return data["markdown"]

    # Fallback: return formatted JSON
    return json.dumps(data, ensure_ascii=False, indent=2) if isinstance(data, (dict, list)) else decoded


def main():
    parser = argparse.ArgumentParser(
        description="iFlytek OCR LLM (通用文档识别/OCR大模型)"
    )
    parser.add_argument("image", help="Image file path (.jpg, .jpeg, .png, .bmp)")
    parser.add_argument(
        "--format", "-f", default="json",
        help="Result format: json, json,markdown, json,sed, json,markdown,sed (default: json)"
    )
    parser.add_argument(
        "--result-option", default="normal",
        help="Result option: normal, normal,char, normal,no_line_position, normal,char,no_line_position (default: normal)"
    )
    parser.add_argument(
        "--output-type", default="one_shot",
        help="Output type: one_shot (default: one_shot)"
    )
    parser.add_argument(
        "--markdown", "-m", action="store_true",
        help="Shortcut for --format json,markdown and output markdown content"
    )
    parser.add_argument(
        "--raw", action="store_true",
        help="Output raw API JSON response"
    )
    parser.add_argument(
        "--raw-result", action="store_true",
        help="Output decoded result JSON (not the full API response)"
    )
    args = parser.parse_args()

    # Read credentials
    app_id = os.environ.get("XFYUN_APP_ID")
    api_key = os.environ.get("XFYUN_API_KEY")
    api_secret = os.environ.get("XFYUN_API_SECRET")

    if not all([app_id, api_key, api_secret]):
        missing = []
        if not app_id:
            missing.append("XFYUN_APP_ID")
        if not api_key:
            missing.append("XFYUN_API_KEY")
        if not api_secret:
            missing.append("XFYUN_API_SECRET")
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        print("Get credentials from https://console.xfyun.cn", file=sys.stderr)
        sys.exit(1)

    # Handle --markdown shortcut
    result_format = args.format
    if args.markdown:
        result_format = "json,markdown"

    # Read image
    image_b64 = read_image_base64(args.image)
    encoding = detect_encoding(args.image)

    # Build and send request
    request_data = build_request(
        app_id, image_b64, encoding,
        result_option=args.result_option,
        result_format=result_format,
        output_type=args.output_type,
    )

    print(f"Sending OCR request for {args.image}...", file=sys.stderr)
    resp = call_ocr(API_URL, api_key, api_secret, request_data)

    # Check response
    header = resp.get("header", {})
    code = header.get("code")
    if code != 0:
        msg = header.get("message", "unknown error")
        print(f"Error (code {code}): {msg}", file=sys.stderr)
        if args.raw:
            print(json.dumps(resp, ensure_ascii=False, indent=2))
        sys.exit(1)

    sid = header.get("sid", "")
    print(f"SID: {sid}", file=sys.stderr)

    if args.raw:
        print(json.dumps(resp, ensure_ascii=False, indent=2))
        return

    # Extract result
    try:
        result_b64 = resp["payload"]["result"]["text"]
    except KeyError:
        print("No result text in response.", file=sys.stderr)
        print(json.dumps(resp, ensure_ascii=False, indent=2))
        return

    if args.raw_result:
        decoded = base64.b64decode(result_b64).decode("utf-8")
        try:
            data = json.loads(decoded)
            print(json.dumps(data, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            print(decoded)
        return

    # Extract and display text
    text = extract_text(result_b64, prefer_markdown=args.markdown)
    print(text)


if __name__ == "__main__":
    main()

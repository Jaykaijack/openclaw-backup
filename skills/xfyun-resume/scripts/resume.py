#!/usr/bin/env python3
"""iFlytek Smart Resume Generator (智能简历生成).

Generate professional resumes from personal info and job requirements
using iFlytek's AI Resume API. Outputs 1-3 complete resume templates.

Environment variables:
    XFYUN_APP_ID      - Required. App ID from https://console.xfyun.cn
    XFYUN_API_KEY     - Required. API Key
    XFYUN_API_SECRET  - Required. API Secret

Usage:
    # From command-line text
    python resume.py "姓名：张三，年龄：28岁，教育经历：2018年本科毕业于合肥工业大学；工作经历：java开发工程师"

    # From a file
    python resume.py --file personal_info.txt

    # Save raw JSON result
    python resume.py "..." --raw

    # Save output to file
    python resume.py "..." --output resume_result.json
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

API_URL = "https://cn-huadong-1.xf-yun.com/v1/private/s73f4add9"


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


def build_request_body(app_id: str, text: str) -> dict:
    """Build the Resume API request payload."""
    return {
        "header": {
            "app_id": app_id,
            "status": 3,
        },
        "parameter": {
            "ai_resume": {
                "resData": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json",
                }
            }
        },
        "payload": {
            "reqData": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 3,
                "text": base64.b64encode(text.encode("utf-8")).decode("utf-8"),
            }
        },
    }


def call_api(api_url: str, api_key: str, api_secret: str, request_data: dict) -> dict:
    """Send request and return JSON response."""
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
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body_text}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="iFlytek Smart Resume Generator (智能简历生成) — generate professional resumes from personal info."
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="Personal info and job requirements as text string",
    )
    parser.add_argument(
        "--file", "-f",
        help="Read input text from a file instead of command line",
    )
    parser.add_argument(
        "--output", "-o",
        help="Save result to a file (JSON)",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw API JSON response",
    )
    args = parser.parse_args()

    # Determine input text
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    elif args.text:
        text = args.text
    else:
        # Try reading from stdin
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            print("Error: No input provided. Pass text as argument, use --file, or pipe via stdin.", file=sys.stderr)
            parser.print_help(sys.stderr)
            sys.exit(1)

    if not text:
        print("Error: Input text is empty.", file=sys.stderr)
        sys.exit(1)

    # Read credentials from environment
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

    # Build and send request
    request_data = build_request_body(app_id, text)

    print("Generating resume...", file=sys.stderr)
    resp = call_api(API_URL, api_key, api_secret, request_data)

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
        result = json.dumps(resp, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"Raw response saved to {args.output}", file=sys.stderr)
        else:
            print(result)
        return

    # Extract result
    try:
        result_b64 = resp["payload"]["resData"]["text"]
    except KeyError:
        print("No result text in response.", file=sys.stderr)
        print(json.dumps(resp, ensure_ascii=False, indent=2))
        sys.exit(1)

    decoded = base64.b64decode(result_b64).decode("utf-8")

    # Try to pretty-print if JSON
    try:
        data = json.loads(decoded)
        result = json.dumps(data, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        result = decoded

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Result saved to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()

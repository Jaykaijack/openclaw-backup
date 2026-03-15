#!/usr/bin/env python3
"""
财经新闻采集脚本
从财联社电报获取最新财经快讯，输出可读文本到stdout
可选参数: --east (同时采集东方财富)
"""
import re, sys, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

def fetch_cls():
    """Fetch 财联社电报."""
    url = "https://www.cls.cn/telegraph"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", "replace")
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '\n', text)
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line and len(line) > 10 and any('\u4e00' <= c <= '\u9fff' for c in line):
                lines.append(line)
        return '\n'.join(lines[:80])
    except Exception as e:
        print(f"Warning: CLS fetch error: {e}", file=sys.stderr)
        return ""

def fetch_east():
    """Fetch 东方财富快讯."""
    url = "https://finance.eastmoney.com/"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", "replace")
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', '\n', text)
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line and len(line) > 10 and any('\u4e00' <= c <= '\u9fff' for c in line):
                lines.append(line)
        return '\n'.join(lines[:50])
    except Exception as e:
        print(f"Warning: East fetch error: {e}", file=sys.stderr)
        return ""

if __name__ == "__main__":
    print("=== 财联社电报 ===")
    print(fetch_cls())
    if "--east" in sys.argv:
        print("\n=== 东方财富 ===")
        print(fetch_east())

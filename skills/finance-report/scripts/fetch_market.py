#!/usr/bin/env python3
"""
金融行情数据采集脚本
从新浪财经API获取A股/港股/美股/欧洲/商品/外汇/国债行情，输出JSON到stdout
支持盘前(pre)/盘中(live)/收盘(close)三种模式
"""
import json, re, sys, urllib.request
from datetime import datetime

SINA_API = "https://hq.sinajs.cn/list={}"
HEADERS = {"Referer": "https://finance.sina.com.cn"}

# ===== 标的配置 =====
A_INDICES = {
    "上证指数": "sh000001", "深证成指": "sz399001", "创业板指": "sz399006",
    "科创50": "sh000688", "沪深300": "sh000300", "上证50": "sh000016",
    "中证500": "sh000905", "中证1000": "sh000852", "中证2000": "sz399303",
    "北证50": "bj899050"
}
HK_INDICES = {"恒生指数": "rt_hsi", "恒生科技": "rt_hstech", "国企指数": "rt_hscei"}
US_INDICES = {"道琼斯": "gb_dji", "纳斯达克": "gb_ixic", "标普500": "gb_inx"}
EU_INDICES = {"富时100": "b_FTSE", "德国DAX": "b_DAX", "法国CAC40": "b_FCHI"}
COMMODITIES = {
    "COMEX黄金": "hf_GC", "COMEX白银": "hf_SI", "COMEX铜": "hf_HG",
    "WTI原油": "hf_CL", "布伦特原油": "hf_OIL", "CBOT大豆": "hf_S",
    "纽约天然气": "hf_NG", "伦敦镍": "hf_NID"
}
FOREX = {
    "美元/人民币": "fx_susdcny", "美元指数": "hf_DINIW",
    "欧元/美元": "fx_seurusd", "美元/日元": "fx_susdjpy"
}

def fetch(codes):
    url = SINA_API.format(",".join(codes.values()))
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read()
            try: return raw.decode("gbk")
            except: return raw.decode("utf-8", "replace")
    except Exception as e:
        print(f"Warning: fetch error: {e}", file=sys.stderr); return ""

def parse(text, code):
    m = re.search(rf'hq_str_{code}="([^"]*)"', text)
    return m.group(1).split(",") if m and m.group(1) else None

def sf(val, default=0.0):
    try: return float(val)
    except: return default

def calc(cur, prev):
    if prev == 0: return 0.0, 0.0
    chg = cur - prev
    return round(chg, 4), round(chg / prev * 100, 2)

def parse_a(text, name, code):
    p = parse(text, code)
    if not p or len(p) < 10: return None
    cur, prev = sf(p[3]), sf(p[2])
    chg, pct = calc(cur, prev)
    return {"name": name, "current": cur, "prev_close": prev, "open": sf(p[1]),
            "high": sf(p[4]), "low": sf(p[5]), "volume": sf(p[8]), "amount": sf(p[9]),
            "change": chg, "change_pct": pct}

def parse_gb(text, name, code):
    p = parse(text, code)
    if not p or len(p) < 4: return None
    return {"name": name, "current": sf(p[1]), "change_pct": sf(p[2])}

def parse_eu(text, name, code):
    p = parse(text, code)
    if not p or len(p) < 5: return None
    return {"name": name, "current": sf(p[1]), "change_pct": sf(p[3])}

def parse_hk(text, name, code):
    p = parse(text, code)
    if not p or len(p) < 7: return None
    cur, prev = sf(p[6]), sf(p[3])
    _, pct = calc(cur, prev)
    return {"name": name, "current": cur, "prev_close": prev, "change_pct": pct}

def parse_cm(text, name, code):
    p = parse(text, code)
    if not p or len(p) < 8: return None
    cur, prev = sf(p[0]), sf(p[7])
    _, pct = calc(cur, prev)
    return {"name": name, "current": cur, "prev_close": prev, "change_pct": pct}

def parse_fx(text, name, code):
    p = parse(text, code)
    if not p or len(p) < 3: return None
    return {"name": name, "current": round(sf(p[1]), 4), "prev_close": round(sf(p[2]), 4)}

def main():
    now = datetime.now()
    res = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y年%m月%d日"),
        "weekday": ["周一","周二","周三","周四","周五","周六","周日"][now.weekday()],
        "a_indices": [], "hk_indices": [], "us_indices": [], "eu_indices": [],
        "commodities": [], "forex": []
    }
    # A股
    t = fetch(A_INDICES)
    for n, c in A_INDICES.items():
        d = parse_a(t, n, c)
        if d: res["a_indices"].append(d)
    # 港股
    t = fetch(HK_INDICES)
    for n, c in HK_INDICES.items():
        d = parse_hk(t, n, c)
        if d: res["hk_indices"].append(d)
    # 美股
    t = fetch(US_INDICES)
    for n, c in US_INDICES.items():
        d = parse_gb(t, n, c)
        if d: res["us_indices"].append(d)
    # 欧洲
    t = fetch(EU_INDICES)
    for n, c in EU_INDICES.items():
        d = parse_eu(t, n, c)
        if d: res["eu_indices"].append(d)
    # 商品
    t = fetch(COMMODITIES)
    for n, c in COMMODITIES.items():
        d = parse_cm(t, n, c)
        if d: res["commodities"].append(d)
    # 外汇
    t = fetch(FOREX)
    for n, c in FOREX.items():
        d = parse_fx(t, n, c)
        if d: res["forex"].append(d)

    json.dump(res, sys.stdout, ensure_ascii=False, indent=2)
    print()

if __name__ == "__main__":
    main()

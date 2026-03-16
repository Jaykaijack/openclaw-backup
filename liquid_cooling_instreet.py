#!/usr/bin/env python3
"""
液冷板块龙头股分析 - 使用InStreet API
"""

import requests
import json
from datetime import datetime

API_KEY = "sk_inst_ee10754479f254bc1b2e46975be8a400"
BASE_URL = "https://instreet.coze.site/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 股票列表
stocks = [
    {"code": "002837", "name": "英维克", "exchange": "SZ"},
    {"code": "300499", "name": "高澜股份", "exchange": "SZ"},
    {"code": "301018", "name": "申菱环境", "exchange": "SZ"},
    {"code": "300990", "name": "同飞股份", "exchange": "SZ"},
    {"code": "603912", "name": "佳力图", "exchange": "SH"}
]

print("=" * 80)
print("液冷板块龙头股分析报告")
print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# 获取股票列表和行情
print("\n【一、实时行情数据】\n")

try:
    response = requests.get(f"{BASE_URL}/arena/stocks", headers=headers, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print("API响应状态:", data.get("status", "unknown"))

        # 尝试获取股票数据
        stocks_data = data.get("data", {}).get("stocks", [])

        for stock in stocks:
            code = stock["code"]
            name = stock["name"]

            # 查找对应股票
            stock_info = None
            for s in stocks_data:
                if s.get("code") == code or s.get("symbol") == code:
                    stock_info = s
                    break

            if stock_info:
                print(f"【{name} - {code}】")
                print(f"  数据: {json.dumps(stock_info, indent=2, ensure_ascii=False)}")
                print()
            else:
                print(f"【{name} - {code}】 未在返回数据中找到")
                print()
    else:
        print(f"API请求失败: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"请求失败: {e}")

# 获取排行榜数据
print("\n【二、排行榜数据】\n")

try:
    response = requests.get(f"{BASE_URL}/arena/leaderboard", headers=headers, timeout=30)
    if response.status_code == 200:
        data = response.json()
        print("排行榜数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
    else:
        print(f"排行榜API请求失败: {response.status_code}")
except Exception as e:
    print(f"排行榜请求失败: {e}")

print("\n" + "=" * 80)
print("分析完成")
print("=" * 80)

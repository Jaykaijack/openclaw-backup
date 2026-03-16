#!/usr/bin/env python3
"""
液冷板块龙头股分析 - 使用腾讯财经API
"""

import requests
import json
from datetime import datetime

# 股票列表
stocks = [
    {"code": "002837", "name": "英维克", "exchange": "sz"},
    {"code": "300499", "name": "高澜股份", "exchange": "sz"},
    {"code": "301018", "name": "申菱环境", "exchange": "sz"},
    {"code": "300990", "name": "同飞股份", "exchange": "sz"},
    {"code": "603912", "name": "佳力图", "exchange": "sh"}
]

print("=" * 80)
print("液冷板块龙头股分析报告")
print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# 腾讯财经API获取实时行情
print("\n【一、实时行情数据】\n")

for stock in stocks:
    code = stock["code"]
    name = stock["name"]
    exchange = stock["exchange"]

    try:
        # 腾讯财经API
        url = f"http://qt.gtimg.cn/q={exchange}{code}"
        response = requests.get(url, timeout=10)
        response.encoding = 'gbk'

        if response.status_code == 200:
            data = response.text
            # 解析数据
            # 格式: v_sz002837="1~英维克~..."
            if f'v_{exchange}{code}' in data:
                # 提取引号内的内容
                start = data.find('"') + 1
                end = data.rfind('"')
                content = data[start:end]
                fields = content.split('~')

                if len(fields) >= 45:
                    print(f"【{name} - {code}】")
                    print(f"  股票名称: {fields[1]}")
                    print(f"  最新价: {fields[3]}")
                    print(f"  昨收: {fields[4]}")
                    print(f"  今开: {fields[5]}")
                    print(f"  成交量(手): {fields[6]}")
                    print(f"  成交额(万): {fields[37]}")
                    print(f"  最高价: {fields[33]}")
                    print(f"  最低价: {fields[34]}")

                    # 计算涨跌幅
                    try:
                        current = float(fields[3])
                        prev_close = float(fields[4])
                        change = current - prev_close
                        change_pct = (change / prev_close) * 100
                        print(f"  涨跌额: {change:.2f}")
                        print(f"  涨跌幅: {change_pct:.2f}%")
                    except:
                        print(f"  涨跌额: {fields[31]}")
                        print(f"  涨跌幅: {fields[32]}%")

                    print(f"  换手率: {fields[38]}%")
                    print(f"  总市值: {fields[44]}万")
                    print(f"  流通市值: {fields[45]}万")
                    print()
                else:
                    print(f"【{name} - {code}】 数据字段不足")
                    print(f"原始数据: {content[:200]}")
                    print()
            else:
                print(f"【{name} - {code}】 未找到数据")
                print()
        else:
            print(f"【{name} - {code}】 请求失败: {response.status_code}")
            print()
    except Exception as e:
        print(f"【{name} - {code}】 获取失败: {e}")
        print()

print("\n" + "=" * 80)
print("分析完成")
print("=" * 80)

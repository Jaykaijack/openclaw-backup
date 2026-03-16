#!/usr/bin/env python3
"""
液冷板块龙头股分析脚本
分析标的：英维克(002837)、高澜股份(300499)、申菱环境(301018)、同飞股份(300990)、佳力图(603912)
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 股票列表
stocks = [
    {"code": "002837", "name": "英维克"},
    {"code": "300499", "name": "高澜股份"},
    {"code": "301018", "name": "申菱环境"},
    {"code": "300990", "name": "同飞股份"},
    {"code": "603912", "name": "佳力图"}
]

print("=" * 80)
print("液冷板块龙头股分析报告")
print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# 1. 获取实时行情
print("\n【一、实时行情数据】\n")

try:
    # 获取A股实时行情
    spot_df = ak.stock_zh_a_spot_em()

    for stock in stocks:
        code = stock["code"]
        name = stock["name"]

        # 根据股票代码前缀判断交易所
        if code.startswith("6"):
            full_code = f"{code}.SH"
            em_code = f"{code}.SS"
        else:
            full_code = f"{code}.SZ"
            em_code = f"{code}.SZ"

        # 查找对应股票数据
        stock_data = spot_df[spot_df["代码"] == code]

        if not stock_data.empty:
            row = stock_data.iloc[0]
            print(f"【{name} - {code}】")
            print(f"  最新价: {row.get('最新价', 'N/A')}")
            print(f"  涨跌幅: {row.get('涨跌幅', 'N/A')}%")
            print(f"  涨跌额: {row.get('涨跌额', 'N/A')}")
            print(f"  成交量: {row.get('成交量', 'N/A')}")
            print(f"  成交额: {row.get('成交额', 'N/A')} 元")
            print(f"  换手率: {row.get('换手率', 'N/A')}%")
            print(f"  总市值: {row.get('总市值', 'N/A')} 元")
            print(f"  市盈率: {row.get('市盈率-动态', 'N/A')}")
            print()
        else:
            print(f"【{name} - {code}】 未找到数据\n")

except Exception as e:
    print(f"获取实时行情失败: {e}")

# 2. 获取历史数据用于技术分析
print("\n【二、近期历史行情（近10日）】\n")

end_date = datetime.now().strftime('%Y%m%d')
start_date = (datetime.now() - timedelta(days=20)).strftime('%Y%m%d')

for stock in stocks:
    code = stock["code"]
    name = stock["name"]

    try:
        hist_df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                      start_date=start_date, end_date=end_date,
                                      adjust="qfq")
        if not hist_df.empty:
            print(f"【{name} - {code}】近5日走势:")
            recent = hist_df.tail(5)[['日期', '收盘', '涨跌幅', '成交量', '成交额']]
            print(recent.to_string(index=False))
            print()
    except Exception as e:
        print(f"获取{name}历史数据失败: {e}\n")

# 3. 获取个股资金流向
print("\n【三、个股资金流向（今日）】\n")

try:
    # 获取个股资金流向
    money_flow_df = ak.stock_individual_fund_flow(stock="002837", market="sz")
    print("资金流向数据获取成功（示例：英维克）")
    print(money_flow_df.head(3).to_string(index=False))
except Exception as e:
    print(f"获取资金流向失败: {e}")

# 4. 板块资金流向
print("\n【四、板块资金流向】\n")

try:
    # 获取概念板块资金流向
    concept_flow = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="概念")
    # 查找液冷相关板块
    liquid_cooling = concept_flow[concept_flow['名称'].str.contains('液冷|散热|温控', na=False)]
    if not liquid_cooling.empty:
        print("液冷相关板块资金流向:")
        print(liquid_cooling.to_string(index=False))
    else:
        print("概念板块资金流向（前10）:")
        print(concept_flow.head(10).to_string(index=False))
except Exception as e:
    print(f"获取板块资金流向失败: {e}")

# 5. 龙虎榜数据
print("\n【五、近期龙虎榜数据】\n")

try:
    lhb_date = (datetime.now() - timedelta(days=3)).strftime('%Y%m%d')
    lhb_df = ak.stock_lhb_detail_daily_sina(start_date=lhb_date, end_date=end_date)

    for stock in stocks:
        code = stock["code"]
        name = stock["name"]
        stock_lhb = lhb_df[lhb_df['代码'] == code]
        if not stock_lhb.empty:
            print(f"【{name} - {code}】 近期上榜:")
            print(stock_lhb.to_string(index=False))
            print()
except Exception as e:
    print(f"获取龙虎榜数据失败: {e}")

print("\n" + "=" * 80)
print("分析完成")
print("=" * 80)

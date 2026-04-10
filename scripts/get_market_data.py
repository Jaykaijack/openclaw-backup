#!/usr/bin/env python3
import sys
sys.path.append('/root/.openclaw/workspace/scripts')
from market_data import MarketData
from datetime import datetime

md = MarketData()
print(f'=== 收盘数据汇总 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ===')
limit_up = md.get_limit_up_stocks()
limit_down = md.get_limit_down_stocks()
top_gainers = md.get_top_gainers(5)
top_losers = md.get_top_losers(5)
print(f'涨停家数: {len(limit_up)}')
print(f'跌停家数: {len(limit_down)}')
print(f'\n涨幅榜TOP5:')
for stock in top_gainers:
    print(f'  {stock["name"]} ({stock["symbol"]}): +{stock["change_rate"]*100:.2f}%')
print(f'\n跌幅榜TOP5:')
for stock in top_losers:
    print(f'  {stock["name"]} ({stock["symbol"]}): {stock["change_rate"]*100:.2f}%')
print(f'\n成交量TOP5:')
top_volume = md.get_top_volume(5)
for stock in top_volume:
    print(f'  {stock["name"]} ({stock["symbol"]}): 量 {stock["volume"]:,}')
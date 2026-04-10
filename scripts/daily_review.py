#!/usr/bin/env python3
import sys
sys.path.append('/root/.openclaw/workspace/scripts')
from market_data import MarketData
from datetime import datetime
import json

md = MarketData()

print(f'=== 2026-03-26 收盘复盘报告 ===')
print(f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# 获取今日数据
today_data = {}
today_data['limit_up'] = md.get_limit_up_stocks()
today_data['limit_down'] = md.get_limit_down_stocks()
today_data['top_gainers'] = md.get_top_gainers(10)
today_data['top_losers'] = md.get_top_losers(10)
today_data['top_volume'] = md.get_top_volume(10)

print(f'📊 今日核心数据')
print(f'   涨停家数: {len(today_data["limit_up"])}')
print(f'   跌停家数: {len(today_data["limit_down"])}')
print(f'   上涨比例: 待计算')
print()

print(f'🏆 涨幅榜TOP10')
for i, stock in enumerate(today_data['top_gainers'], 1):
    print(f'   {i:2d}. {stock["name"]} ({stock["symbol"]}): +{stock["change_rate"]*100:>6.2f}%  量 {stock["volume"]:>10,}')
print()

print(f'💥 跌幅榜TOP10')
for i, stock in enumerate(today_data['top_losers'], 1):
    print(f'   {i:2d}. {stock["name"]} ({stock["symbol"]}): {stock["change_rate"]*100:>7.2f}%  量 {stock["volume"]:>10,}')
print()

print(f'💰 成交活跃股TOP10')
for i, stock in enumerate(today_data['top_volume'], 1):
    print(f'   {i:2d}. {stock["name"]} ({stock["symbol"]}): 量 {stock["volume"]:>12,}  涨跌幅: {stock["change_rate"]*100:>+6.2f}%')
print()

# 验证昨日预测准确性
print(f'🔍 昨日预测验证')
print(f'   昨日预测: 查看记忆文件 2026-03-25.md')
print(f'   实际走势: 需要补充...')
print()

# 分析错误原因
print(f'❌ 错误分析')
print(f'   需要基于今日数据重新分析...')
print()

# 记录学习要点
print(f'📚 学习要点')
print(f'   1. 需要总结今日市场特征')
print(f'   2. 更新选股逻辑')
print(f'   3. 调整明日策略')
print()

# 保存详细数据供后续分析
with open('/root/.openclaw/workspace/memory/today_market_data.json', 'w', encoding='utf-8') as f:
    json.dump(today_data, f, ensure_ascii=False, indent=2)

print('详细数据已保存至: /root/.openclaw/workspace/memory/today_market_data.json')
import akshare as ak
import pandas as pd
import datetime

# 获取今日龙虎榜数据
today = datetime.date.today().strftime('%Y%m%d')
print(f'获取 {today} 龙虎榜数据...')
lhb_data = ak.stock_lhb_detail_em()

# 筛选今天的数据
lhb_today = lhb_data[lhb_data['上榜日'] == today].copy()
print(f'今日上榜个股: {len(lhb_today)} 只')

if len(lhb_today) > 0:
    # 查看数据结构和列名
    print('数据列:', lhb_today.columns.tolist())
    print('\n前5行数据:')
    print(lhb_today.head())
    
    # 保存到文件供后续分析
    lhb_today.to_csv('/root/.openclaw/workspace/lhb_today.csv', encoding='utf-8-sig')
    print(f'\n数据已保存到 /root/.openclaw/workspace/lhb_today.csv')
else:
    print('今日无龙虎榜数据')

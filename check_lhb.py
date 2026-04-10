import akshare as ak
import pandas as pd
import datetime

# 获取最新龙虎榜数据
lhb_data = ak.stock_lhb_detail_em()
print(f'总记录数: {len(lhb_data)}')
if not lhb_data.empty:
    print(f'最早日期: {lhb_data["上榜日"].min()}')
    print(f'最晚日期: {lhb_data["上榜日"].max()}')
else:
    print('无数据')

# 查看列名
print(f'列名: {lhb_data.columns.tolist()}')
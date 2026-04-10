import akshare
import pandas as pd

print('Fetching pre-market data...')
df = akshare.stock_zh_a_spot_em()
print(f'Total A-share stocks: {len(df)}')

rise = len(df[df['涨跌幅'] > 0])
fall = len(df[df['涨跌幅'] < 0])
flat = len(df[df['涨跌幅'] == 0])

print(f'Advancing: {rise}, Declining: {fall}, Unchanged: {flat}')
if fall > 0:
    print(f'Advance-Decline Ratio: {rise/fall:.2f}:1')
else:
    print('Advance-Decline Ratio: N/A (no declining stocks)')

top_gainers = df[df['涨跌幅'] > 9.5].nlargest(10, '涨跌幅')[['名称', '最新价', '涨跌幅', '成交量', '成交额']]
print('\nTop Gainers (limit up):')
print(top_gainers)

top_losers = df[df['涨跌幅'] < -9.5].nsmallest(10, '涨跌幅')[['名称', '最新价', '涨跌幅', '成交量', '成交额']]
print('\nTop Losers (limit down):')
print(top_losers)

volume_sum = df['成交量'].sum()
amount_sum = df['成交额'].sum()
print(f'\nTotal Volume: {volume_sum:,}')
print(f'Total Amount: ¥{amount_sum:,.0f}')

try:
    sector_data = akshare.stock_board_industry_cons_em()
    print(f'\nSector Analysis:')
    sector_trend = sector_data.groupby('行业')['涨跌幅'].mean().sort_values(ascending=False).head(10)
    print(sector_trend)
except Exception as e:
    print(f'Could not fetch sector data: {e}')

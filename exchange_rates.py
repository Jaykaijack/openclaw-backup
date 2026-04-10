import requests
import json

print('=== 汇率数据 ===')
try:
    r = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
    data = r.json()
    eur = data['rates']['EUR']
    cny = data['rates']['CNY']
    jpy = data['rates']['JPY']
    print(f'美元兑欧元: {eur:.4f}')
    print(f'美元兑人民币: {cny:.4f}')
    print(f'美元兑日元: {jpy:.4f}')
except Exception as e:
    print(f'错误: {e}')
    
print('\n=== 大宗商品概览 ===')
print('从A股数据中提取主要商品相关信息...')
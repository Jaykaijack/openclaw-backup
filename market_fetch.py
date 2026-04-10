import requests
import json

print('=== 美股市场 ===')
try:
    r = requests.get('https://instreet.coze.site/api/v1/arena/leaderboard', headers={'API-KEY': 'sk_inst_ee10754479f254bc1b2e46975be8a400'}, timeout=10)
    data = r.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print(f'错误: {e}')

print('\n=== 港股市场 ===')
try:
    r = requests.get('https://instreet.coze.site/api/v1/arena/portfolio', headers={'API-KEY': 'sk_inst_ee10754479f254bc1b2e46975be8a400'}, timeout=10)
    data = r.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print(f'错误: {e}')

print('\n=== 大宗商品 ===')
try:
    r = requests.get('https://instreet.coze.site/api/v1/arena/stocks', headers={'API-KEY': 'sk_inst_ee10754479f254bc1b2e46975be8a400'}, timeout=10)
    data = r.json()
    print(json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print(f'错误: {e}')
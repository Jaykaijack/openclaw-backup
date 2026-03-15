#!/usr/bin/env python3
"""
新浪财经数据接口
通过新浪财经获取全市场数据
"""

import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

class SinaData:
    """新浪财经数据接口"""
    
    def __init__(self):
        self.base_url = "https://hq.sinajs.cn"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://finance.sina.com.cn'
        }
    
    def _request(self, url):
        """发送HTTP请求"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode('gb2312', errors='ignore')
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None
    
    def get_stock_quotes(self, symbols):
        """
        获取股票行情
        symbols: 股票代码列表，如 ['sh600519', 'sz000001']
        """
        if not symbols:
            return []
        
        # 批量获取，每次最多100只
        batch_size = 100
        all_results = []
        
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i+batch_size]
            symbol_str = ','.join(batch)
            url = f"{self.base_url}/list={symbol_str}"
            
            data = self._request(url)
            if data:
                results = self._parse_sina_data(data)
                all_results.extend(results)
        
        return all_results
    
    def _parse_sina_data(self, data):
        """解析新浪返回的数据"""
        results = []
        
        # 新浪返回格式: var hq_str_sh600519="贵州茅台,1740.00,...";
        pattern = r'var hq_str_(\w+)="([^"]*)"'
        matches = re.findall(pattern, data)
        
        for symbol, quote_str in matches:
            if not quote_str or quote_str == '':
                continue
            
            parts = quote_str.split(',')
            if len(parts) < 33:
                continue
            
            try:
                name = parts[0]
                open_price = float(parts[1])
                prev_close = float(parts[2])
                current = float(parts[3])
                high = float(parts[4])
                low = float(parts[5])
                volume = int(parts[8])
                turnover = float(parts[9])
                
                change_rate = (current - prev_close) / prev_close * 100 if prev_close > 0 else 0
                
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'price': current,
                    'open': open_price,
                    'prev_close': prev_close,
                    'high': high,
                    'low': low,
                    'change_rate': change_rate,
                    'volume': volume,
                    'turnover': turnover
                })
            except Exception as e:
                continue
        
        return results
    
    def get_hs300_list(self):
        """获取沪深300成分股列表"""
        # 使用东方财富的沪深300列表接口
        url = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=300&po=1&np=1&fltt=2&invt=2&fid=f12&fs=b:BK0500&fields=f12,f14"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                stocks = data.get('data', {}).get('diff', [])
                
                symbols = []
                for stock in stocks:
                    code = stock.get('f12')
                    if code:
                        # 判断是沪市还是深市
                        if code.startswith('6'):
                            symbols.append(f"sh{code}")
                        else:
                            symbols.append(f"sz{code}")
                
                return symbols
        except Exception as e:
            print(f"[ERROR] 获取沪深300列表失败: {e}")
            return []

if __name__ == "__main__":
    print("=== 新浪财经数据接口测试 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    sina = SinaData()
    
    # 测试获取几只股票
    test_symbols = ['sh600519', 'sz000001', 'sh601868', 'sh601611']
    print(f"\n📊 测试获取 {len(test_symbols)} 只股票:")
    
    quotes = sina.get_stock_quotes(test_symbols)
    for q in quotes:
        print(f"  {q['name']} ({q['symbol']}): {q['price']:.2f} ({q['change_rate']:+.2f}%)")

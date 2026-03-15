#!/usr/bin/env python3
"""
A股免费行情数据获取模块
支持：新浪财经、腾讯财经、东方财富
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional

class StockDataAPI:
    """A股行情数据获取类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _format_code(self, code: str) -> str:
        """格式化股票代码"""
        code = code.strip()
        if code.startswith('6'):
            return f'sh{code}'
        elif code.startswith('0') or code.startswith('3'):
            return f'sz{code}'
        return code
    
    def get_sina_quotes(self, stock_codes: List[str]) -> Dict:
        """
        获取新浪财经实时行情
        
        Args:
            stock_codes: 股票代码列表，如 ['600000', '000001']
        
        Returns:
            Dict: 股票行情数据
        """
        codes = [self._format_code(c) for c in stock_codes]
        url = f"https://hq.sinajs.cn/list={','.join(codes)}"
        
        headers = {
            'Referer': 'https://finance.sina.com.cn',
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            response.encoding = 'gb18030'
            
            result = {}
            for line in response.text.strip().split('\n'):
                if not line.strip():
                    continue
                
                # 解析 var hq_str_sh600000="...";
                if '=' in line:
                    var_part, data_part = line.split('=', 1)
                    code = var_part.replace('var hq_str_', '')
                    data = data_part.strip('";').split(',')
                    
                    if len(data) >= 33:
                        result[code] = {
                            'name': data[0],
                            'open': float(data[1]),
                            'close': float(data[2]),
                            'current': float(data[3]),
                            'high': float(data[4]),
                            'low': float(data[5]),
                            'bid': float(data[6]),
                            'ask': float(data[7]),
                            'volume': int(data[8]),
                            'amount': float(data[9]),
                            'bid1_vol': int(data[10]),
                            'bid1': float(data[11]),
                            'bid2_vol': int(data[12]),
                            'bid2': float(data[13]),
                            'bid3_vol': int(data[14]),
                            'bid3': float(data[15]),
                            'bid4_vol': int(data[16]),
                            'bid4': float(data[17]),
                            'bid5_vol': int(data[18]),
                            'bid5': float(data[19]),
                            'ask1_vol': int(data[20]),
                            'ask1': float(data[21]),
                            'ask2_vol': int(data[22]),
                            'ask2': float(data[23]),
                            'ask3_vol': int(data[24]),
                            'ask3': float(data[25]),
                            'ask4_vol': int(data[26]),
                            'ask4': float(data[27]),
                            'ask5_vol': int(data[28]),
                            'ask5': float(data[29]),
                            'date': data[30],
                            'time': data[31],
                        }
            
            return result
            
        except Exception as e:
            print(f"新浪财经 API 错误: {e}")
            return {}
    
    def get_qq_quotes(self, stock_codes: List[str]) -> Dict:
        """
        获取腾讯财经实时行情
        
        Args:
            stock_codes: 股票代码列表
        """
        codes = [self._format_code(c) for c in stock_codes]
        url = f"https://qt.gtimg.cn/q={','.join(codes)}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'gbk'
            
            result = {}
            for line in response.text.strip().split('\n'):
                if not line.strip():
                    continue
                
                if '=' in line:
                    var_part, data_part = line.split('=', 1)
                    code = var_part.replace('v_', '')
                    data = data_part.strip('";').split('~')
                    
                    if len(data) >= 45:
                        result[code] = {
                            'name': data[1],
                            'code': data[2],
                            'current': float(data[3]),
                            'close': float(data[4]),
                            'open': float(data[5]),
                            'volume': int(data[6]),
                            'outer_vol': int(data[7]),
                            'inner_vol': int(data[8]),
                            'bid1': float(data[9]),
                            'bid1_vol': int(data[10]),
                            'bid2': float(data[11]),
                            'bid2_vol': int(data[12]),
                            'bid3': float(data[13]),
                            'bid3_vol': int(data[14]),
                            'bid4': float(data[15]),
                            'bid4_vol': int(data[16]),
                            'bid5': float(data[17]),
                            'bid5_vol': int(data[18]),
                            'ask1': float(data[19]),
                            'ask1_vol': int(data[20]),
                            'ask2': float(data[21]),
                            'ask2_vol': int(data[22]),
                            'ask3': float(data[23]),
                            'ask3_vol': int(data[24]),
                            'ask4': float(data[25]),
                            'ask4_vol': int(data[26]),
                            'ask5': float(data[27]),
                            'ask5_vol': int(data[28]),
                            'datetime': data[30],
                            'change': float(data[31]),
                            'change_pct': float(data[32]),
                            'high': float(data[33]),
                            'low': float(data[34]),
                            'amount': float(data[37]),
                            'turnover': float(data[38]),
                            'pe': float(data[39]) if data[39] else None,
                            'pb': float(data[46]) if len(data) > 46 and data[46] else None,
                        }
            
            return result
            
        except Exception as e:
            print(f"腾讯财经 API 错误: {e}")
            return {}
    
    def get_quote(self, stock_codes: List[str], source: str = 'sina') -> Dict:
        """
        获取行情（统一接口）
        
        Args:
            stock_codes: 股票代码列表
            source: 数据源 ('sina' 或 'qq')
        """
        if source == 'sina':
            return self.get_sina_quotes(stock_codes)
        elif source == 'qq':
            return self.get_qq_quotes(stock_codes)
        else:
            raise ValueError(f"不支持的数据源: {source}")
    
    def get_market_summary(self) -> Dict:
        """获取大盘指数行情"""
        indices = ['sh000001', 'sz399001', 'sz399006']  # 上证、深证、创业板
        return self.get_sina_quotes(indices)


# 测试代码
if __name__ == '__main__':
    api = StockDataAPI()
    
    print("=" * 50)
    print("测试新浪财经 API")
    print("=" * 50)
    
    # 测试获取多只股票
    stocks = ['600000', '000001', '600519']
    data = api.get_sina_quotes(stocks)
    
    for code, info in data.items():
        print(f"\n{code} - {info['name']}")
        print(f"  当前价: {info['current']}")
        print(f"  涨跌幅: {((info['current'] - info['close']) / info['close'] * 100):.2f}%")
        print(f"  成交量: {info['volume'] / 10000:.0f}万手")
    
    print("\n" + "=" * 50)
    print("测试腾讯财经 API")
    print("=" * 50)
    
    data = api.get_qq_quotes(stocks)
    for code, info in data.items():
        print(f"\n{code} - {info['name']}")
        print(f"  当前价: {info['current']}")
        print(f"  涨跌幅: {info['change_pct']:.2f}%")
        print(f"  换手率: {info['turnover']:.2f}%")
    
    print("\n" + "=" * 50)
    print("测试大盘指数")
    print("=" * 50)
    
    indices = api.get_market_summary()
    for code, info in indices.items():
        change_pct = (info['current'] - info['close']) / info['close'] * 100
        print(f"{info['name']}: {info['current']:.2f} ({change_pct:+.2f}%)")
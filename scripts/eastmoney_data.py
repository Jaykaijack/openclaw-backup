#!/usr/bin/env python3
"""
东方财富数据接口
直接调用东方财富的API获取全市场数据
"""

import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

class EastMoneyData:
    """东方财富数据接口"""
    
    def __init__(self):
        self.base_url = "http://push2ex.eastmoney.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _request(self, url):
        """发送HTTP请求"""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            # 添加更多header模拟浏览器
            req.add_header('Referer', 'http://quote.eastmoney.com/')
            req.add_header('Accept', '*/*')
            req.add_header('Accept-Language', 'zh-CN,zh;q=0.9')
            req.add_header('Connection', 'keep-alive')
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode('utf-8')
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None
    
    def get_all_stocks(self):
        """
        获取全市场股票列表
        返回: 沪深A股所有股票
        """
        # 东方财富获取全部股票的接口
        url = "http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5000&po=1&np=1&fltt=2&invt=2&fid=f12&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f12,f13,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f18,f20,f21,f22,f23,f24,f25,f26,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100"
        
        data = self._request(url)
        if not data:
            return []
        
        try:
            json_data = json.loads(data)
            stocks = json_data.get('data', {}).get('diff', [])
            
            result = []
            for stock in stocks:
                # 解析字段
                code = stock.get('f12')  # 股票代码
                name = stock.get('f14')  # 股票名称
                price = stock.get('f2')  # 最新价
                change_rate = stock.get('f3')  # 涨跌幅
                change_amount = stock.get('f4')  # 涨跌额
                volume = stock.get('f5')  # 成交量
                turnover = stock.get('f6')  # 成交额
                amplitude = stock.get('f7')  # 振幅
                turnover_rate = stock.get('f8')  # 换手率
                pe = stock.get('f9')  # 市盈率
                pb = stock.get('f23')  # 市净率
                market_cap = stock.get('f20')  # 总市值
                
                # 过滤无效数据
                if not code or not name:
                    continue
                
                result.append({
                    'symbol': code,
                    'name': name,
                    'price': price / 10000 if price else 0,  # 价格需要除以10000
                    'change_rate': change_rate / 100 if change_rate else 0,  # 涨跌幅
                    'change_amount': change_amount / 100 if change_amount else 0,
                    'volume': volume or 0,
                    'turnover': turnover or 0,
                    'amplitude': amplitude / 100 if amplitude else 0,
                    'turnover_rate': turnover_rate / 100 if turnover_rate else 0,
                    'pe': pe / 100 if pe else 0,
                    'pb': pb / 100 if pb else 0,
                    'market_cap': market_cap or 0
                })
            
            return result
        except Exception as e:
            print(f"[ERROR] 解析数据失败: {e}")
            return []
    
    def get_limit_up_stocks(self):
        """获取涨停股票"""
        stocks = self.get_all_stocks()
        return [s for s in stocks if s['change_rate'] >= 9.5]
    
    def get_limit_down_stocks(self):
        """获取跌停股票"""
        stocks = self.get_all_stocks()
        return [s for s in stocks if s['change_rate'] <= -9.5]
    
    def get_top_volume(self, n=20):
        """获取成交额排名"""
        stocks = self.get_all_stocks()
        sorted_stocks = sorted(stocks, key=lambda x: x['turnover'], reverse=True)
        return sorted_stocks[:n]
    
    def get_top_gainers(self, n=20):
        """获取涨幅榜"""
        stocks = self.get_all_stocks()
        sorted_stocks = sorted(stocks, key=lambda x: x['change_rate'], reverse=True)
        return sorted_stocks[:n]
    
    def get_top_losers(self, n=20):
        """获取跌幅榜"""
        stocks = self.get_all_stocks()
        sorted_stocks = sorted(stocks, key=lambda x: x['change_rate'])
        return sorted_stocks[:n]
    
    def get_market_summary(self):
        """获取市场概况"""
        stocks = self.get_all_stocks()
        
        limit_up = len([s for s in stocks if s['change_rate'] >= 9.5])
        limit_down = len([s for s in stocks if s['change_rate'] <= -9.5])
        
        up_stocks = len([s for s in stocks if s['change_rate'] > 0])
        down_stocks = len([s for s in stocks if s['change_rate'] < 0])
        flat_stocks = len([s for s in stocks if s['change_rate'] == 0])
        
        return {
            'total': len(stocks),
            'limit_up': limit_up,
            'limit_down': limit_down,
            'up': up_stocks,
            'down': down_stocks,
            'flat': flat_stocks
        }

if __name__ == "__main__":
    print("=== 东方财富数据接口测试 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    em = EastMoneyData()
    
    # 获取市场概况
    print("\n📊 市场概况:")
    summary = em.get_market_summary()
    print(f"  总股票数: {summary['total']}")
    print(f"  涨停: {summary['limit_up']}只")
    print(f"  跌停: {summary['limit_down']}只")
    print(f"  上涨: {summary['up']}只")
    print(f"  下跌: {summary['down']}只")
    print(f"  平盘: {summary['flat']}只")
    
    # 涨停股
    if summary['limit_up'] > 0:
        print(f"\n📈 涨停股 ({summary['limit_up']}只):")
        limit_up = em.get_limit_up_stocks()
        for s in limit_up[:10]:
            print(f"  {s['name']} ({s['symbol']}): +{s['change_rate']:.2f}%")
    
    # 跌停股
    if summary['limit_down'] > 0:
        print(f"\n📉 跌停股 ({summary['limit_down']}只):")
        limit_down = em.get_limit_down_stocks()
        for s in limit_down[:10]:
            print(f"  {s['name']} ({s['symbol']}): {s['change_rate']:.2f}%")
    
    # 成交额TOP5
    print(f"\n💰 成交额TOP5:")
    top_vol = em.get_top_volume(5)
    for s in top_vol:
        print(f"  {s['name']}: {s['turnover']/100000000:.1f}亿")
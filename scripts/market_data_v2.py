#!/usr/bin/env python3
"""
量化盯盘外脑 - 综合数据接口 V2
整合多个数据源：新浪财经 + InStreet
"""

import sys
sys.path.insert(0, '.')
from sina_data import SinaData
from market_data import MarketData as InStreetData
from datetime import datetime

class MarketDataV2:
    """综合数据接口"""
    
    def __init__(self):
        self.sina = SinaData()
        self.instreet = InStreetData()
    
    def get_hs300_quotes(self):
        """获取沪深300行情"""
        # 获取沪深300代码列表
        symbols = self.sina.get_hs300_list()
        if symbols:
            # 通过新浪财经获取行情
            quotes = self.sina.get_stock_quotes(symbols)
            if quotes:
                return quotes
        
        # 备用：使用InStreet数据
        return self.instreet.get_all_stocks()
    
    def get_limit_up_stocks(self):
        """获取涨停股票"""
        stocks = self.get_hs300_quotes()
        return [s for s in stocks if s.get('change_rate', 0) >= 9.5]
    
    def get_limit_down_stocks(self):
        """获取跌停股票"""
        stocks = self.get_hs300_quotes()
        return [s for s in stocks if s.get('change_rate', 0) <= -9.5]
    
    def get_top_volume(self, n=20):
        """获取成交额排名"""
        stocks = self.get_hs300_quotes()
        sorted_stocks = sorted(stocks, key=lambda x: x.get('turnover') or x.get('volume') or 0, reverse=True)
        return sorted_stocks[:n]
    
    def get_top_gainers(self, n=20):
        """获取涨幅榜"""
        stocks = self.get_hs300_quotes()
        sorted_stocks = sorted(stocks, key=lambda x: x.get('change_rate') or 0, reverse=True)
        return sorted_stocks[:n]
    
    def get_top_losers(self, n=20):
        """获取跌幅榜"""
        stocks = self.get_hs300_quotes()
        sorted_stocks = sorted(stocks, key=lambda x: x.get('change_rate') or 0)
        return sorted_stocks[:n]
    
    def get_market_summary(self):
        """获取市场概况"""
        stocks = self.get_hs300_quotes()
        
        limit_up = len([s for s in stocks if (s.get('change_rate') or 0) >= 9.5])
        limit_down = len([s for s in stocks if (s.get('change_rate') or 0) <= -9.5])
        
        up_stocks = len([s for s in stocks if (s.get('change_rate') or 0) > 0])
        down_stocks = len([s for s in stocks if (s.get('change_rate') or 0) < 0])
        flat_stocks = len([s for s in stocks if (s.get('change_rate') or 0) == 0])
        
        # 计算平均涨跌幅
        if stocks:
            avg_change = sum(s.get('change_rate') or 0 for s in stocks) / len(stocks)
        else:
            avg_change = 0
        
        return {
            'total': len(stocks),
            'limit_up': limit_up,
            'limit_down': limit_down,
            'up': up_stocks,
            'down': down_stocks,
            'flat': flat_stocks,
            'avg_change': avg_change
        }
    
    def get_stock_by_symbol(self, symbol):
        """获取单只股票行情"""
        stocks = self.get_hs300_quotes()
        for stock in stocks:
            if stock.get('symbol') == symbol:
                return stock
        return None

if __name__ == "__main__":
    print("=== 综合数据接口 V2 测试 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    md = MarketDataV2()
    
    # 获取市场概况
    print("\n📊 沪深300市场概况:")
    summary = md.get_market_summary()
    print(f"  总股票数: {summary['total']}")
    print(f"  涨停: {summary['limit_up']}只")
    print(f"  跌停: {summary['limit_down']}只")
    print(f"  上涨: {summary['up']}只")
    print(f"  下跌: {summary['down']}只")
    print(f"  平盘: {summary['flat']}只")
    print(f"  平均涨跌幅: {summary['avg_change']:+.2f}%")
    
    # 涨停股
    if summary['limit_up'] > 0:
        print(f"\n📈 涨停股 ({summary['limit_up']}只):")
        limit_up = md.get_limit_up_stocks()
        for s in limit_up[:10]:
            print(f"  {s['name']} ({s['symbol']}): +{s['change_rate']:.2f}%")
    
    # 跌停股
    if summary['limit_down'] > 0:
        print(f"\n📉 跌停股 ({summary['limit_down']}只):")
        limit_down = md.get_limit_down_stocks()
        for s in limit_down[:10]:
            print(f"  {s['name']} ({s['symbol']}): {s['change_rate']:.2f}%")
    
    # 成交额TOP5
    print(f"\n💰 成交额TOP5:")
    top_vol = md.get_top_volume(5)
    for s in top_vol:
        turnover = s.get('turnover') or s.get('volume', 0)
        print(f"  {s['name']}: {turnover/10000:.1f}万")
    
    # 涨幅TOP5
    print(f"\n🔥 涨幅TOP5:")
    top_gainers = md.get_top_gainers(5)
    for s in top_gainers:
        change = s.get('change_rate') or 0
        # InStreet数据是0.10表示10%，新浪数据是10表示10%
        if abs(change) < 1:  # 可能是小数形式
            change = change * 100
        print(f"  {s['name']}: +{change:.2f}%")

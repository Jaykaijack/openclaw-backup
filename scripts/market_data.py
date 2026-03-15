#!/usr/bin/env python3
"""
量化盯盘外脑 - 行情数据获取模块
实时接入 InStreet API 获取 A 股行情数据
纯标准库实现，无需 pip 安装
"""

import urllib.request
import urllib.error
import json
from datetime import datetime

# InStreet API 配置
API_KEY = "sk_inst_ee10754479f254bc1b2e46975be8a400"
BASE_URL = "https://instreet.coze.site/api/v1"

class MarketData:
    """行情数据类"""
    
    def __init__(self):
        self.base_url = BASE_URL
    
    def _request(self, path, use_auth=False):
        """发送 HTTP 请求"""
        url = f"{self.base_url}{path}"
        try:
            req = urllib.request.Request(url)
            if use_auth:
                req.add_header("Authorization", f"Bearer {API_KEY}")
            req.add_header("Content-Type", "application/json")
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return {}
    
    def get_all_stocks(self, limit=300):
        """获取所有股票行情"""
        data = self._request(f"/arena/stocks?limit={limit}", use_auth=True)
        return data.get("data", {}).get("stocks", [])
    
    def get_leaderboard(self, limit=20):
        """获取排行榜"""
        data = self._request(f"/arena/leaderboard?limit={limit}")
        return data.get("data", {}).get("leaderboard", [])
    
    def get_top_gainers(self, n=10):
        """获取涨幅榜"""
        stocks = self.get_all_stocks(limit=300)
        sorted_stocks = sorted(stocks, key=lambda x: x.get("change_rate") or 0, reverse=True)
        return sorted_stocks[:n]
    
    def get_top_losers(self, n=10):
        """获取跌幅榜"""
        stocks = self.get_all_stocks(limit=300)
        sorted_stocks = sorted(stocks, key=lambda x: x.get("change_rate") or 0)
        return sorted_stocks[:n]
    
    def get_top_volume(self, n=10):
        """获取成交额榜（按成交量近似）"""
        stocks = self.get_all_stocks(limit=300)
        sorted_stocks = sorted(stocks, key=lambda x: x.get("volume") or 0, reverse=True)
        return sorted_stocks[:n]
    
    def get_limit_up_stocks(self):
        """获取涨停股票"""
        stocks = self.get_all_stocks(limit=300)
        limit_up = []
        for stock in stocks:
            change_rate = stock.get("change_rate") or 0
            if change_rate >= 0.095:
                limit_up.append(stock)
        return limit_up
    
    def get_limit_down_stocks(self):
        """获取跌停股票"""
        stocks = self.get_all_stocks(limit=300)
        limit_down = []
        for stock in stocks:
            change_rate = stock.get("change_rate") or 0
            if change_rate <= -0.095:
                limit_down.append(stock)
        return limit_down
    
    def get_stock_by_symbol(self, symbol):
        """获取单只股票行情"""
        stocks = self.get_all_stocks(limit=300)
        for stock in stocks:
            if stock.get("symbol") == symbol:
                return stock
        return None

if __name__ == "__main__":
    # 测试数据获取
    md = MarketData()
    print("=== 行情数据测试 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取涨停股
    limit_up = md.get_limit_up_stocks()
    print(f"\n涨停股数量: {len(limit_up)}")
    for stock in limit_up[:5]:
        print(f"  {stock['name']} ({stock['symbol']}): +{stock['change_rate']*100:.2f}%")
    
    # 获取成交额TOP5
    top_volume = md.get_top_volume(5)
    print(f"\n成交量TOP5:")
    for stock in top_volume:
        print(f"  {stock['name']} ({stock['symbol']}): 量 {stock['volume']:,}")

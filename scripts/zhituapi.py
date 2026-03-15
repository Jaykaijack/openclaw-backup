#!/usr/bin/env python3
"""
智途 API 数据获取模块
获取 A股全市场股票列表
"""

import requests
import json
from typing import List, Dict

class ZhituAPI:
    """智途 API 数据获取类"""
    
    def __init__(self, token: str = None):
        self.token = token or "CFEEEC10-1353-49FA-8705-4180E842B0CD"
        self.base_url = "https://api.zhituapi.com/hs"
    
    def get_all_stocks(self) -> List[Dict]:
        """
        获取全市场股票列表
        
        Returns:
            List[Dict]: 股票列表，每个元素包含 dm(代码), mc(名称), jys(交易所)
        """
        url = f"{self.base_url}/list/all?token={self.token}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data
            
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return []
    
    def get_sh_stocks(self) -> List[Dict]:
        """获取上海交易所股票"""
        all_stocks = self.get_all_stocks()
        return [s for s in all_stocks if s.get('jys') == 'SH']
    
    def get_sz_stocks(self) -> List[Dict]:
        """获取深圳交易所股票"""
        all_stocks = self.get_all_stocks()
        return [s for s in all_stocks if s.get('jys') == 'SZ']
    
    def get_stock_by_code(self, code: str) -> Dict:
        """
        根据代码查找股票
        
        Args:
            code: 股票代码，如 '600000' 或 '600000.SH'
        """
        all_stocks = self.get_all_stocks()
        
        for stock in all_stocks:
            if stock.get('dm') == code or stock.get('dm').startswith(code):
                return stock
        
        return {}
    
    def get_stock_by_name(self, name: str) -> List[Dict]:
        """
        根据名称查找股票（模糊匹配）
        
        Args:
            name: 股票名称关键词
        """
        all_stocks = self.get_all_stocks()
        
        results = []
        for stock in all_stocks:
            if name in stock.get('mc', ''):
                results.append(stock)
        
        return results
    
    def get_statistics(self) -> Dict:
        """获取市场统计信息"""
        all_stocks = self.get_all_stocks()
        
        sh_stocks = [s for s in all_stocks if s.get('jys') == 'SH']
        sz_stocks = [s for s in all_stocks if s.get('jys') == 'SZ']
        
        return {
            'total': len(all_stocks),
            'shanghai': len(sh_stocks),
            'shenzhen': len(sz_stocks)
        }


# 测试代码
if __name__ == '__main__':
    api = ZhituAPI()
    
    print("=" * 60)
    print("智途 API 测试")
    print("=" * 60)
    
    # 获取统计信息
    print("\n1. 市场统计")
    stats = api.get_statistics()
    print(f"   总股票数: {stats['total']}")
    print(f"   上海交易所: {stats['shanghai']}")
    print(f"   深圳交易所: {stats['shenzhen']}")
    
    # 获取前10只股票
    print("\n2. 前10只股票")
    stocks = api.get_all_stocks()[:10]
    for stock in stocks:
        print(f"   {stock['dm']}: {stock['mc']} ({stock['jys']})")
    
    # 查找特定股票
    print("\n3. 查找股票代码 600000")
    stock = api.get_stock_by_code('600000')
    if stock:
        print(f"   找到: {stock['dm']} - {stock['mc']}")
    
    # 模糊搜索
    print("\n4. 搜索包含'茅台'的股票")
    results = api.get_stock_by_name('茅台')
    for stock in results:
        print(f"   {stock['dm']}: {stock['mc']}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

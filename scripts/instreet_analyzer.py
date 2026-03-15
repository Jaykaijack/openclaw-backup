#!/usr/bin/env python3
"""
二郎 InStreet 炒股分析系统
基于官方界面结构设计
"""

import requests
import json
from datetime import datetime

API_KEY = 'sk_inst_ee10754479f254bc1b2e46975be8a400'
BASE_URL = 'https://instreet.coze.site'

class InStreetAnalyzer:
    """InStreet 炒股分析器"""
    
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
    
    def get_portfolio(self):
        """获取持仓信息"""
        try:
            resp = requests.get(f'{BASE_URL}/api/v1/arena/portfolio', 
                              headers=self.headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return data.get('data', {})
            return None
        except Exception as e:
            print(f'获取持仓失败: {e}')
            return None
    
    def get_leaderboard(self, limit=10):
        """获取排行榜"""
        try:
            resp = requests.get(f'{BASE_URL}/api/v1/arena/leaderboard?limit={limit}', 
                              headers=self.headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    return data.get('data', {}).get('leaderboard', [])
            return []
        except Exception as e:
            print(f'获取排行榜失败: {e}')
            return []
    
    def analyze_portfolio(self):
        """分析持仓健康度"""
        portfolio = self.get_portfolio()
        if not portfolio:
            print('❌ 无法获取持仓信息')
            return
        
        print('=' * 70)
        print('📊 账户概览')
        print('=' * 70)
        
        total_value = portfolio.get('total_value', 0)
        cash = portfolio.get('cash', 0)
        invested = portfolio.get('total_invested', 1000000)
        
        # 计算收益率
        return_rate = (total_value - invested) / invested * 100 if invested > 0 else 0
        
        print(f"总资产: ¥{total_value:,.2f}")
        print(f"收益率: {return_rate:+.2f}% {'🔥' if return_rate > 0 else '💧'}")
        cash_pct = cash/total_value*100 if total_value > 0 else 0
        print(f"现金: ¥{cash:,.2f} ({cash_pct:.1f}%)")
        print(f"持仓数: {portfolio.get('holdings_count', 0)}")
        print(f"总手续费: ¥{portfolio.get('total_fees', 0):.2f}")
        
        # 持仓明细
        holdings = portfolio.get('holdings', [])
        if holdings:
            print('\n' + '-' * 70)
            print('📈 持仓明细')
            print('-' * 70)
            print(f"{'代码':<12} {'名称':<10} {'数量':>10} {'成本':>8} {'现价':>8} {'盈亏':>10}")
            print('-' * 70)
            
            for h in holdings:
                symbol = h.get('symbol', '')
                name = h.get('stock_name', '')[:8]
                shares = h.get('shares', 0)
                cost = h.get('avg_cost', 0)
                price = h.get('current_price', 0)
                pnl = (price - cost) * shares
                pnl_pct = (price - cost) / cost * 100 if cost > 0 else 0
                
                print(f"{symbol:<12} {name:<10} {shares:>10,} ¥{cost:>7.2f} ¥{price:>7.2f} {pnl_pct:>+9.2f}%")
        else:
            print('\n💡 暂无持仓，建议建仓')
        
        print('\n' + '=' * 70)
    
    def analyze_leaderboard(self):
        """分析排行榜高手"""
        leaders = self.get_leaderboard(5)
        if not leaders:
            print('❌ 无法获取排行榜')
            return
        
        print('=' * 70)
        print('🏆 排行榜 TOP 5')
        print('=' * 70)
        
        for i, agent in enumerate(leaders, 1):
            name = agent.get('agent', {}).get('username', 'Unknown')
            total = agent.get('total_value', 0)
            rate = agent.get('return_rate', 0) * 100
            holdings = agent.get('holdings_count', 0)
            
            print(f"\n{i}. {name}")
            print(f"   总资产: ¥{total:,.2f} | 收益率: {rate:+.2f}%")
            print(f"   持仓数: {holdings} | 现金: ¥{agent.get('cash', 0):,.2f}")
        
        print('\n' + '=' * 70)
    
    def generate_trade_plan(self):
        """生成交易计划"""
        print('=' * 70)
        print('🎯 今日交易计划')
        print('=' * 70)
        print()
        
        # 获取当前状态
        portfolio = self.get_portfolio()
        if not portfolio:
            return
        
        cash = portfolio.get('cash', 0)
        holdings_count = portfolio.get('holdings_count', 0)
        
        print('【账户状态】')
        print(f"可用现金: ¥{cash:,.2f}")
        print(f"当前持仓: {holdings_count} 只")
        print()
        
        print('【策略建议】')
        if holdings_count == 0:
            print("✅ 空仓状态，建议建仓")
            print("   目标: 单票满仓或70%仓位")
            print("   方向: 电力/新能源/AI板块")
        elif holdings_count == 1:
            print("⚡ 单票持仓，可加仓或持有")
            print("   建议: 观察盘中走势再决策")
        else:
            print("📊 多票持仓，建议集中仓位")
            print("   方向: 卖出弱势股，加仓强势股")
        
        print()
        print('【风险控制】')
        print("   • 单票不超过总资金80%")
        print("   • 止损线: -5%")
        print("   • 止盈线: +10%/+20%")
        
        print('\n' + '=' * 70)


def main():
    """主函数"""
    analyzer = InStreetAnalyzer()
    
    print('\n')
    print('🐺 二郎 InStreet 炒股分析系统')
    print(f'时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    # 1. 分析持仓
    analyzer.analyze_portfolio()
    
    # 2. 分析排行榜
    analyzer.analyze_leaderboard()
    
    # 3. 生成交易计划
    analyzer.generate_trade_plan()


if __name__ == '__main__':
    main()

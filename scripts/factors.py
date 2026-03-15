#!/usr/bin/env python3
"""
量化盯盘外脑 - 因子计算模块
实现基础因子：动量、成交量、波动率等
"""

import sys
sys.path.insert(0, '.')
from market_data import MarketData
from datetime import datetime

class FactorCalculator:
    """因子计算器"""
    
    def __init__(self):
        self.md = MarketData()
    
    def momentum_factor(self, n=5):
        """
        动量因子：N日涨跌幅
        原理：强者恒强，弱者恒弱
        """
        stocks = self.md.get_all_stocks(limit=300)
        momentum_scores = []
        
        for stock in stocks:
            symbol = stock.get('symbol')
            name = stock.get('name')
            change_rate = stock.get('change_rate') or 0
            
            momentum_scores.append({
                'symbol': symbol,
                'name': name,
                'momentum': change_rate,
                'score': change_rate * 100  # 转换为百分比
            })
        
        # 按动量排序
        momentum_scores.sort(key=lambda x: x['momentum'], reverse=True)
        return momentum_scores
    
    def volume_factor(self, n=5):
        """
        成交量因子：成交量放大倍数
        原理：量价齐升确认趋势
        """
        stocks = self.md.get_all_stocks(limit=300)
        volume_scores = []
        
        for stock in stocks:
            symbol = stock.get('symbol')
            name = stock.get('name')
            volume = stock.get('volume') or 0
            price = stock.get('price') or 0
            
            # 计算成交额（万元）
            turnover = volume * price / 10000
            
            volume_scores.append({
                'symbol': symbol,
                'name': name,
                'volume': volume,
                'turnover': turnover,
                'score': turnover / 10000  # 简化评分
            })
        
        # 按成交额排序
        volume_scores.sort(key=lambda x: x['turnover'], reverse=True)
        return volume_scores
    
    def volatility_factor(self):
        """
        波动率因子：日内振幅
        原理：高波动可能预示变盘
        """
        stocks = self.md.get_all_stocks(limit=300)
        volatility_scores = []
        
        for stock in stocks:
            symbol = stock.get('symbol')
            name = stock.get('name')
            high = stock.get('high') or 0
            low = stock.get('low') or 0
            prev_close = stock.get('prev_close') or 0
            
            if prev_close > 0:
                amplitude = (high - low) / prev_close
            else:
                amplitude = 0
            
            volatility_scores.append({
                'symbol': symbol,
                'name': name,
                'high': high,
                'low': low,
                'amplitude': amplitude,
                'score': amplitude * 100
            })
        
        # 按振幅排序
        volatility_scores.sort(key=lambda x: x['amplitude'], reverse=True)
        return volatility_scores
    
    def limit_up_factor(self):
        """
        涨停因子：涨停强度
        原理：涨停越早、封单越大，强度越高
        """
        limit_up_stocks = self.md.get_limit_up_stocks()
        
        scores = []
        for stock in limit_up_stocks:
            scores.append({
                'symbol': stock.get('symbol'),
                'name': stock.get('name'),
                'change_rate': stock.get('change_rate') or 0,
                'volume': stock.get('volume') or 0,
                'score': 100  # 涨停基础分100
            })
        
        return scores
    
    def composite_score(self, weights=None):
        """
        综合评分：多因子加权
        默认权重：动量40% + 成交量30% + 波动率20% + 涨停10%
        """
        if weights is None:
            weights = {
                'momentum': 0.4,
                'volume': 0.3,
                'volatility': 0.2,
                'limit_up': 0.1
            }
        
        # 获取各因子数据
        momentum_data = {s['symbol']: s for s in self.momentum_factor()}
        volume_data = {s['symbol']: s for s in self.volume_factor()}
        volatility_data = {s['symbol']: s for s in self.volatility_factor()}
        limit_up_data = {s['symbol']: s for s in self.limit_up_factor()}
        
        # 计算综合得分
        all_symbols = set(momentum_data.keys())
        composite_scores = []
        
        for symbol in all_symbols:
            m_score = momentum_data.get(symbol, {}).get('score', 0)
            v_score = volume_data.get(symbol, {}).get('score', 0)
            vol_score = volatility_data.get(symbol, {}).get('score', 0)
            lu_score = limit_up_data.get(symbol, {}).get('score', 0)
            
            # 归一化处理（简化版）
            m_norm = min(m_score / 10, 10)  # 涨10%得10分
            v_norm = min(v_score / 1000, 10)  # 成交额1亿得10分
            vol_norm = min(vol_score / 5, 10)  # 振幅5%得10分
            lu_norm = lu_score / 10  # 涨停100分->10分
            
            total_score = (
                m_norm * weights['momentum'] +
                v_norm * weights['volume'] +
                vol_norm * weights['volatility'] +
                lu_norm * weights['limit_up']
            )
            
            composite_scores.append({
                'symbol': symbol,
                'name': momentum_data.get(symbol, {}).get('name', ''),
                'total_score': total_score,
                'momentum_score': m_norm,
                'volume_score': v_norm,
                'volatility_score': vol_norm,
                'limit_up_score': lu_norm
            })
        
        # 按综合得分排序
        composite_scores.sort(key=lambda x: x['total_score'], reverse=True)
        return composite_scores

if __name__ == "__main__":
    fc = FactorCalculator()
    
    print("=== 因子计算测试 ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 动量因子TOP5
    print("\n📈 动量因子TOP5:")
    momentum = fc.momentum_factor()
    for s in momentum[:5]:
        print(f"  {s['name']}: +{s['score']:.2f}%")
    
    # 成交量因子TOP5
    print("\n💰 成交额TOP5:")
    volume = fc.volume_factor()
    for s in volume[:5]:
        print(f"  {s['name']}: {s['turnover']/10000:.1f}亿")
    
    # 综合评分TOP5
    print("\n🎯 综合评分TOP5:")
    composite = fc.composite_score()
    for s in composite[:5]:
        print(f"  {s['name']}: {s['total_score']:.2f}分")

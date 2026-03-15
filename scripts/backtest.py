#!/usr/bin/env python3
"""
量化盯盘外脑 - 简单回测框架
实现T+1交易逻辑、涨跌停限制、成本计算
"""

import sys
sys.path.insert(0, '.')
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Trade:
    """交易记录"""
    date: str
    symbol: str
    name: str
    action: str  # 'buy' or 'sell'
    shares: int
    price: float
    amount: float
    commission: float
    stamp_tax: float
    reason: str

@dataclass
class Position:
    """持仓记录"""
    symbol: str
    name: str
    shares: int
    avg_cost: float
    buy_date: str  # T+1限制用

class BacktestEngine:
    """回测引擎"""
    
    def __init__(self, initial_capital=1000000):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}  # symbol -> Position
        self.trades: List[Trade] = []
        self.current_date = None
        
        # 交易成本
        self.commission_rate = 0.00025  # 万分之2.5
        self.min_commission = 5  # 最低佣金5元
        self.stamp_tax_rate = 0.001  # 印花税千分之一（仅卖出）
    
    def set_date(self, date: str):
        """设置当前日期"""
        self.current_date = date
    
    def can_buy(self, symbol: str, price: float, change_rate: float) -> bool:
        """
        检查是否可以买入
        - 涨停无法买入
        - 资金充足
        """
        # A股涨停约10%
        if change_rate >= 0.095:
            return False
        return True
    
    def can_sell(self, symbol: str, change_rate: float, buy_date: str) -> bool:
        """
        检查是否可以卖出
        - T+1限制：买入次日才能卖出
        - 跌停无法卖出
        """
        # T+1检查
        if buy_date == self.current_date:
            return False
        
        # 跌停检查
        if change_rate <= -0.095:
            return False
        
        return True
    
    def calculate_cost(self, action: str, amount: float) -> tuple:
        """
        计算交易成本
        返回: (commission, stamp_tax)
        """
        # 佣金
        commission = max(amount * self.commission_rate, self.min_commission)
        
        # 印花税（仅卖出）
        stamp_tax = 0
        if action == 'sell':
            stamp_tax = amount * self.stamp_tax_rate
        
        return commission, stamp_tax
    
    def buy(self, symbol: str, name: str, price: float, 
            shares: int, change_rate: float, reason: str = "") -> bool:
        """买入股票"""
        # 检查是否可以买入
        if not self.can_buy(symbol, price, change_rate):
            return False
        
        # 计算金额
        amount = price * shares
        commission, _ = self.calculate_cost('buy', amount)
        total_cost = amount + commission
        
        # 检查资金
        if total_cost > self.cash:
            return False
        
        # 执行买入
        self.cash -= total_cost
        
        if symbol in self.positions:
            # 加仓，更新成本
            pos = self.positions[symbol]
            total_shares = pos.shares + shares
            total_cost_basis = pos.avg_cost * pos.shares + price * shares
            pos.avg_cost = total_cost_basis / total_shares
            pos.shares = total_shares
        else:
            # 新建仓位
            self.positions[symbol] = Position(
                symbol=symbol,
                name=name,
                shares=shares,
                avg_cost=price,
                buy_date=self.current_date
            )
        
        # 记录交易
        self.trades.append(Trade(
            date=self.current_date,
            symbol=symbol,
            name=name,
            action='buy',
            shares=shares,
            price=price,
            amount=amount,
            commission=commission,
            stamp_tax=0,
            reason=reason
        ))
        
        return True
    
    def sell(self, symbol: str, price: float, 
             change_rate: float, reason: str = "") -> bool:
        """卖出股票"""
        # 检查持仓
        if symbol not in self.positions:
            return False
        
        pos = self.positions[symbol]
        
        # 检查是否可以卖出（T+1、跌停）
        if not self.can_sell(symbol, change_rate, pos.buy_date):
            return False
        
        # 计算金额
        amount = price * pos.shares
        commission, stamp_tax = self.calculate_cost('sell', amount)
        total_proceeds = amount - commission - stamp_tax
        
        # 执行卖出
        self.cash += total_proceeds
        
        # 记录交易
        self.trades.append(Trade(
            date=self.current_date,
            symbol=symbol,
            name=pos.name,
            action='sell',
            shares=pos.shares,
            price=price,
            amount=amount,
            commission=commission,
            stamp_tax=stamp_tax,
            reason=reason
        ))
        
        # 移除持仓
        del self.positions[symbol]
        
        return True
    
    def get_portfolio_value(self, prices: Dict[str, float]) -> float:
        """计算账户总价值"""
        holdings_value = 0
        for symbol, pos in self.positions.items():
            price = prices.get(symbol, pos.avg_cost)
            holdings_value += price * pos.shares
        return self.cash + holdings_value
    
    def get_report(self, prices: Dict[str, float]) -> dict:
        """生成回测报告"""
        portfolio_value = self.get_portfolio_value(prices)
        return_rate = (portfolio_value - self.initial_capital) / self.initial_capital
        
        return {
            'initial_capital': self.initial_capital,
            'cash': self.cash,
            'holdings_value': portfolio_value - self.cash,
            'portfolio_value': portfolio_value,
            'return_rate': return_rate,
            'positions_count': len(self.positions),
            'trades_count': len(self.trades)
        }

if __name__ == "__main__":
    print("=== 回测引擎测试 ===")
    
    # 创建回测引擎
    engine = BacktestEngine(initial_capital=1000000)
    engine.set_date("2026-03-14")
    
    # 模拟买入
    print("\n📈 模拟交易:")
    
    # 买入中国能建（未涨停）
    result = engine.buy(
        symbol="sh601868",
        name="中国能建",
        price=3.8,
        shares=100000,
        change_rate=0.05,  # 涨5%，未涨停
        reason="测试买入"
    )
    print(f"买入中国能建 10万股 @ 3.8元: {'成功' if result else '失败'}")
    
    # 尝试买入涨停股（应该失败）
    result = engine.buy(
        symbol="sh601611",
        name="中国核电",
        price=10.0,
        shares=10000,
        change_rate=0.10,  # 涨停
        reason="测试涨停买入"
    )
    print(f"买入涨停股中国核电: {'成功' if result else '失败（涨停无法买入）'}")
    
    # 尝试当日卖出（应该失败，T+1限制）
    result = engine.sell(
        symbol="sh601868",
        price=3.9,
        change_rate=0.02,
        reason="测试T+1"
    )
    print(f"当日卖出中国能建: {'成功' if result else '失败（T+1限制）'}")
    
    #
#!/usr/bin/env python3
"""
二郎经验库系统
Experience Base System for Erlang Quant System

功能：
1. 交易记录：每日操作记录
2. 经验总结：成功/失败分析
3. 模式识别：重复模式发现
4. 智能推荐：基于历史推荐
"""

import json
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class TradeType(Enum):
    """交易类型"""
    BUY = "买入"
    SELL = "卖出"
    HOLD = "持有"
    WATCH = "观察"


class TradeResult(Enum):
    """交易结果"""
    SUCCESS = "成功"
    FAILURE = "失败"
    BREAKEVEN = "持平"
    PENDING = "待验证"


@dataclass
class TradeRecord:
    """交易记录"""
    id: str
    date: date
    stock_code: str
    stock_name: str
    trade_type: TradeType
    price: float
    quantity: int
    reason: str  # 交易理由
    emotion: str  # 当时情绪
    result: TradeResult = TradeResult.PENDING
    profit_pct: Optional[float] = None
    review: str = ""  # 复盘总结
    lessons: List[str] = field(default_factory=list)  # 教训
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'stock_code': self.stock_code,
            'stock_name': self.stock_name,
            'trade_type': self.trade_type.value,
            'price': self.price,
            'quantity': self.quantity,
            'reason': self.reason,
            'emotion': self.emotion,
            'result': self.result.value,
            'profit_pct': self.profit_pct,
            'review': self.review,
            'lessons': self.lessons,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TradeRecord':
        return cls(
            id=data['id'],
            date=date.fromisoformat(data['date']),
            stock_code=data['stock_code'],
            stock_name=data['stock_name'],
            trade_type=TradeType(data['trade_type']),
            price=data['price'],
            quantity=data['quantity'],
            reason=data['reason'],
            emotion=data['emotion'],
            result=TradeResult(data['result']),
            profit_pct=data.get('profit_pct'),
            review=data.get('review', ''),
            lessons=data.get('lessons', []),
            created_at=datetime.fromisoformat(data['created_at'])
        )


@dataclass
class Experience:
    """经验总结"""
    id: str
    date: date
    category: str  # 情绪判断/策略执行/风险控制/数据使用
    situation: str  # 情境描述
    action: str  # 采取行动
    outcome: str  # 结果
    analysis: str  # 分析
    insight: str  # 洞察
    is_positive: bool  # 正面经验
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'category': self.category,
            'situation': self.situation,
            'action': self.action,
            'outcome': self.outcome,
            'analysis': self.analysis,
            'insight': self.insight,
            'is_positive': self.is_positive,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Experience':
        return cls(
            id=data['id'],
            date=date.fromisoformat(data['date']),
            category=data['category'],
            situation=data['situation'],
            action=data['action'],
            outcome=data['outcome'],
            analysis=data['analysis'],
            insight=data['insight'],
            is_positive=data['is_positive'],
            usage_count=data.get('usage_count', 0),
            created_at=datetime.fromisoformat(data['created_at'])
        )


class ExperienceBase:
    """经验库"""
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path.home() / ".openclaw/workspace/memory/experience-base.json"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.trades: Dict[str, TradeRecord] = {}
        self.experiences: Dict[str, Experience] = {}
        self.load()
    
    def load(self):
        """加载经验库"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get('trades', []):
                    t = TradeRecord.from_dict(item)
                    self.trades[t.id] = t
                for item in data.get('experiences', []):
                    e = Experience.from_dict(item)
                    self.experiences[e.id] = e
    
    def save(self):
        """保存经验库"""
        data = {
            'trades': [t.to_dict() for t in self.trades.values()],
            'experiences': [e.to_dict() for e in self.experiences.values()],
            'updated_at': datetime.now().isoformat()
        }
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 交易记录管理
    def add_trade(self, stock_code: str, stock_name: str, trade_type: TradeType,
                  price: float, quantity: int, reason: str, emotion: str) -> TradeRecord:
        """添加交易记录"""
        id = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}"
        t = TradeRecord(
            id=id,
            date=date.today(),
            stock_code=stock_code,
            stock_name=stock_name,
            trade_type=trade_type,
            price=price,
            quantity=quantity,
            reason=reason,
            emotion=emotion
        )
        self.trades[t.id] = t
        self.save()
        return t
    
    def update_trade_result(self, trade_id: str, result: TradeResult,
                           profit_pct: float = None, review: str = "",
                           lessons: List[str] = None) -> Optional[TradeRecord]:
        """更新交易结果"""
        t = self.trades.get(trade_id)
        if not t:
            return None
        
        t.result = result
        t.profit_pct = profit_pct
        t.review = review
        t.lessons = lessons or []
        self.save()
        return t
    
    # 经验总结管理
    def add_experience(self, category: str, situation: str, action: str,
                      outcome: str, analysis: str, insight: str,
                      is_positive: bool) -> Experience:
        """添加经验总结"""
        id = f"E{datetime.now().strftime('%Y%m%d%H%M%S')}"
        e = Experience(
            id=id,
            date=date.today(),
            category=category,
            situation=situation,
            action=action,
            outcome=outcome,
            analysis=analysis,
            insight=insight,
            is_positive=is_positive
        )
        self.experiences[e.id] = e
        self.save()
        return e
    
    # 查询功能
    def get_trades_by_date(self, d: date) -> List[TradeRecord]:
        """按日期获取交易"""
        return [t for t in self.trades.values() if t.date == d]
    
    def get_trades_by_stock(self, stock_code: str) -> List[TradeRecord]:
        """按股票获取交易"""
        return [t for t in self.trades.values() if t.stock_code == stock_code]
    
    def get_experiences_by_category(self, category: str) -> List[Experience]:
        """按类别获取经验"""
        return [e for e in self.experiences.values() if e.category == category]
    
    def get_positive_experiences(self) -> List[Experience]:
        """获取正面经验"""
        return [e for e in self.experiences.values() if e.is_positive]
    
    def get_negative_experiences(self) -> List[Experience]:
        """获取负面经验（教训）"""
        return [e for e in self.experiences.values() if not e.is_positive]
    
    # 统计分析
    def get_trade_stats(self) -> Dict[str, Any]:
        """获取交易统计"""
        completed = [t for t in self.trades.values() if t.result != TradeResult.PENDING]
        
        if not completed:
            return {'total': 0, 'win_rate': None, 'avg_profit': None}
        
        wins = [t for t in completed if t.result == TradeResult.SUCCESS]
        profits = [t.profit_pct for t in completed if t.profit_pct is not None]
        
        return {
            'total': len(self.trades),
            'completed': len(completed),
            'pending': len(self.trades) - len(completed),
            'wins': len(wins),
            'losses': len(completed) - len(wins),
            'win_rate': len(wins) / len(completed) if completed else None,
            'avg_profit': sum(profits) / len(profits) if profits else None
        }
    
    def get_experience_stats(self) -> Dict[str, Any]:
        """获取经验统计"""
        positive = self.get_positive_experiences()
        negative = self.get_negative_experiences()
        
        categories = {}
        for e in self.experiences.values():
            categories[e.category] = categories.get(e.category, 0) + 1
        
        return {
            'total': len(self.experiences),
            'positive': len(positive),
            'negative': len(negative),
            'categories': categories
        }
    
    def get_report(self) -> str:
        """生成经验库报告"""
        trade_stats = self.get_trade_stats()
        exp_stats = self.get_experience_stats()
        
        win_rate_str = f"{trade_stats['win_rate']:.1%}" if trade_stats.get('win_rate') else 'N/A'
        avg_profit_str = f"{trade_stats['avg_profit']:.2%}" if trade_stats.get('avg_profit') else 'N/A'
        
        report = f"""# 二郎经验库报告

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 交易统计

| 指标 | 数值 |
|------|------|
| 总交易数 | {trade_stats.get('total', 0)} |
| 已完成 | {trade_stats.get('completed', 0)} |
| 待验证 | {trade_stats.get('pending', 0)} |
| 盈利次数 | {trade_stats.get('wins', 0)} |
| 亏损次数 | {trade_stats.get('losses', 0)} |
| 胜率 | {win_rate_str} |
| 平均收益 | {avg_profit_str} |

## 经验统计

| 指标 | 数值 |
|------|------|
| 总经验数 | {exp_stats['total']} |
| 正面经验 | {exp_stats['positive']} |
| 负面教训 | {exp_stats['negative']} |

### 按类别分布

"""
        for cat, count in exp_stats['categories'].items():
            report += f"- {cat}: {count}条\n"
        
        # 最近教训
        negative = self.get_negative_experiences()
        if negative:
            report += "\n## 最近教训\n\n"
            for e in negative[-3:]:
                report += f"- **{e.category}**: {e.insight}\n"
        
        return report
    
    # 智能推荐
    def get_similar_situations(self, situation_keywords: List[str]) -> List[Experience]:
        """获取相似情境的经验"""
        results = []
        for e in self.experiences.values():
            if any(kw in e.situation or kw in e.analysis for kw in situation_keywords):
                results.append(e)
        
        # 按使用次数排序
        results.sort(key=lambda e: -e.usage_count)
        return results
    
    def recommend_action(self, situation: str) -> Optional[str]:
        """推荐行动"""
        # 简单关键词匹配
        keywords = situation.split()
        similar = self.get_similar_situations(keywords)
        
        if similar:
            # 优先返回正面经验
            positive = [e for e in similar if e.is_positive]
            if positive:
                return f"建议: {positive[0].action}\n理由: {positive[0].insight}"
            
            # 返回负面教训的反面
            negative = [e for e in similar if not e.is_positive]
            if negative:
                return f"避免: {negative[0].action}\n教训: {negative[0].insight}"
        
        return None


# 使用示例
if __name__ == "__main__":
    eb = ExperienceBase()
    
    print("=== 添加交易记录 ===")
    t = eb.add_trade(
        stock_code="000001",
        stock_name="平安银行",
        trade_type=TradeType.BUY,
        price=10.50,
        quantity=1000,
        reason="情绪修复，板块强势",
        emotion="谨慎乐观"
    )
    print(f"交易ID: {t.id}")
    
    print("\n=== 添加经验总结 ===")
    e = eb.add_experience(
        category="情绪判断",
        situation="昨日涨停股竞价差，但权重股走强",
        action="判断为冰点，建议防守",
        outcome="实际市场修复，错过机会",
        analysis="只看小票情绪，忽略权重股",
        insight="退潮期≠冰点，需区分大小票情绪",
        is_positive=False
    )
    print(f"经验ID: {e.id}")
    
    print("\n" + eb.get_report())

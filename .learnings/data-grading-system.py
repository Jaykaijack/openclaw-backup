#!/usr/bin/env python3
"""
二郎数据分级体系
Data Grading System for Erlang Quant System

数据源分级标准：
- S级：官方数据、交易所数据（99%+可信度）→ 核心决策
- A级：主流财经媒体、权威机构（95%+可信度）→ 辅助决策
- B级：一般财经网站、自媒体（80%+可信度）→ 参考信息
- C级：社交媒体、论坛（60%+可信度）→ 情绪感知
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class DataGrade(Enum):
    """数据等级"""
    S = "S级"  # 官方数据、交易所数据
    A = "A级"  # 主流财经媒体、权威机构
    B = "B级"  # 一般财经网站、自媒体
    C = "C级"  # 社交媒体、论坛
    UNKNOWN = "未分级"


class DataType(Enum):
    """数据类型"""
    QUOTE = "行情数据"
    FINANCIAL = "财务数据"
    NEWS = "新闻资讯"
    SENTIMENT = "情绪数据"
    FLOW = "资金流向"
    LHB = "龙虎榜"
    BLOCK = "板块数据"
    MACRO = "宏观数据"


@dataclass
class DataSourceConfig:
    """数据源配置"""
    name: str
    grade: DataGrade
    data_types: List[DataType]
    reliability: float  # 历史可靠性 0-1
    latency_ms: int  # 平均延迟毫秒
    update_frequency: int  # 更新频率秒
    coverage: float  # 覆盖率 0-1
    cost: str  # 成本：free/low/medium/high
    status: str = "active"  # active/degraded/inactive
    last_success: Optional[datetime] = None
    success_rate_7d: float = 0.0


class DataGradingSystem:
    """数据分级体系"""
    
    # 数据源配置表
    DATA_SOURCES: Dict[str, DataSourceConfig] = {
        # ============ S级数据源 ============
        "sse": DataSourceConfig(
            name="上交所",
            grade=DataGrade.S,
            data_types=[DataType.QUOTE, DataType.FLOW, DataType.BLOCK],
            reliability=0.999,
            latency_ms=50,
            update_frequency=3,
            coverage=0.5,  # 只覆盖沪市
            cost="free"
        ),
        "szse": DataSourceConfig(
            name="深交所",
            grade=DataGrade.S,
            data_types=[DataType.QUOTE, DataType.FLOW, DataType.BLOCK],
            reliability=0.999,
            latency_ms=50,
            update_frequency=3,
            coverage=0.5,  # 只覆盖深市
            cost="free"
        ),
        "cffex": DataSourceConfig(
            name="中金所",
            grade=DataGrade.S,
            data_types=[DataType.QUOTE, DataType.MACRO],
            reliability=0.999,
            latency_ms=100,
            update_frequency=60,
            coverage=0.1,
            cost="free"
        ),
        
        # ============ A级数据源 ============
        "akshare": DataSourceConfig(
            name="AKShare",
            grade=DataGrade.A,
            data_types=[DataType.QUOTE, DataType.FINANCIAL, DataType.LHB, DataType.BLOCK],
            reliability=0.95,
            latency_ms=500,
            update_frequency=60,
            coverage=0.95,
            cost="free"
        ),
        "tushare": DataSourceConfig(
            name="Tushare",
            grade=DataGrade.A,
            data_types=[DataType.QUOTE, DataType.FINANCIAL, DataType.MACRO],
            reliability=0.96,
            latency_ms=300,
            update_frequency=300,
            coverage=0.90,
            cost="low"
        ),
        "eastmoney": DataSourceConfig(
            name="东方财富",
            grade=DataGrade.A,
            data_types=[DataType.QUOTE, DataType.FLOW, DataType.LHB, DataType.NEWS],
            reliability=0.95,
            latency_ms=200,
            update_frequency=30,
            coverage=0.98,
            cost="free"
        ),
        "sina": DataSourceConfig(
            name="新浪财经",
            grade=DataGrade.A,
            data_types=[DataType.QUOTE, DataType.NEWS],
            reliability=0.92,
            latency_ms=300,
            update_frequency=30,
            coverage=0.95,
            cost="free"
        ),
        "wind": DataSourceConfig(
            name="Wind",
            grade=DataGrade.A,
            data_types=[DataType.QUOTE, DataType.FINANCIAL, DataType.MACRO, DataType.FLOW],
            reliability=0.98,
            latency_ms=100,
            update_frequency=10,
            coverage=0.99,
            cost="high"
        ),
        
        # ============ B级数据源 ============
        "cls": DataSourceConfig(
            name="财联社",
            grade=DataGrade.B,
            data_types=[DataType.NEWS, DataType.SENTIMENT],
            reliability=0.88,
            latency_ms=1000,
            update_frequency=60,
            coverage=0.80,
            cost="low"
        ),
        "wallstreetcn": DataSourceConfig(
            name="华尔街见闻",
            grade=DataGrade.B,
            data_types=[DataType.NEWS, DataType.MACRO],
            reliability=0.85,
            latency_ms=1000,
            update_frequency=60,
            coverage=0.70,
            cost="free"
        ),
        "xfyun-search": DataSourceConfig(
            name="讯飞搜索",
            grade=DataGrade.B,
            data_types=[DataType.NEWS],
            reliability=0.85,
            latency_ms=2000,
            update_frequency=300,
            coverage=0.90,
            cost="low"
        ),
        "instreet": DataSourceConfig(
            name="InStreet",
            grade=DataGrade.B,
            data_types=[DataType.QUOTE],
            reliability=0.80,
            latency_ms=500,
            update_frequency=1800,  # 半小时更新
            coverage=0.30,  # 沪深300
            cost="free"
        ),
        
        # ============ C级数据源 ============
        "guba": DataSourceConfig(
            name="股吧",
            grade=DataGrade.C,
            data_types=[DataType.SENTIMENT],
            reliability=0.65,
            latency_ms=5000,
            update_frequency=300,
            coverage=0.95,
            cost="free"
        ),
        "xueqiu": DataSourceConfig(
            name="雪球",
            grade=DataGrade.C,
            data_types=[DataType.SENTIMENT, DataType.NEWS],
            reliability=0.70,
            latency_ms=3000,
            update_frequency=300,
            coverage=0.80,
            cost="free"
        ),
        "weibo": DataSourceConfig(
            name="微博",
            grade=DataGrade.C,
            data_types=[DataType.SENTIMENT],
            reliability=0.60,
            latency_ms=5000,
            update_frequency=300,
            coverage=0.90,
            cost="free"
        ),
    }
    
    # 数据类型优先级（用于决策权重）
    DATA_TYPE_WEIGHTS = {
        DataType.QUOTE: 1.0,      # 行情数据最重要
        DataType.FINANCIAL: 0.9,  # 财务数据
        DataType.FLOW: 0.85,      # 资金流向
        DataType.LHB: 0.8,        # 龙虎榜
        DataType.BLOCK: 0.75,     # 板块数据
        DataType.MACRO: 0.7,      # 宏观数据
        DataType.NEWS: 0.6,       # 新闻资讯
        DataType.SENTIMENT: 0.5,  # 情绪数据
    }
    
    # 决策场景数据要求
    DECISION_REQUIREMENTS = {
        "核心决策": {
            "min_grade": DataGrade.A,
            "min_reliability": 0.95,
            "cross_validate": True,
            "min_sources": 2
        },
        "辅助决策": {
            "min_grade": DataGrade.B,
            "min_reliability": 0.85,
            "cross_validate": True,
            "min_sources": 2
        },
        "参考信息": {
            "min_grade": DataGrade.B,
            "min_reliability": 0.80,
            "cross_validate": False,
            "min_sources": 1
        },
        "情绪感知": {
            "min_grade": DataGrade.C,
            "min_reliability": 0.60,
            "cross_validate": False,
            "min_sources": 1
        }
    }
    
    def __init__(self, log_file: Optional[Path] = None):
        if log_file is None:
            log_file = Path.home() / ".openclaw/workspace/memory/data-grading-log.json"
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get_source(self, source_name: str) -> Optional[DataSourceConfig]:
        """获取数据源配置"""
        return self.DATA_SOURCES.get(source_name)
    
    def get_sources_by_grade(self, grade: DataGrade) -> List[DataSourceConfig]:
        """按等级获取数据源"""
        return [s for s in self.DATA_SOURCES.values() if s.grade == grade]
    
    def get_sources_by_type(self, data_type: DataType) -> List[DataSourceConfig]:
        """按数据类型获取数据源"""
        return [s for s in self.DATA_SOURCES.values() if data_type in s.data_types]
    
    def get_best_source(self, data_type: DataType, 
                       max_cost: str = "high") -> Optional[DataSourceConfig]:
        """获取最佳数据源"""
        candidates = self.get_sources_by_type(data_type)
        
        # 过滤成本
        cost_order = {"free": 0, "low": 1, "medium": 2, "high": 3}
        max_cost_level = cost_order.get(max_cost, 3)
        candidates = [s for s in candidates if cost_order.get(s.cost, 3) <= max_cost_level]
        
        # 过滤状态
        candidates = [s for s in candidates if s.status == "active"]
        
        if not candidates:
            return None
        
        # 按可靠性和等级排序
        def score(s: DataSourceConfig) -> float:
            grade_score = {"S级": 4, "A级": 3, "B级": 2, "C级": 1}.get(s.grade.value, 0)
            return s.reliability * 0.6 + grade_score * 0.1 + s.coverage * 0.2 - s.latency_ms * 0.00001
        
        return max(candidates, key=score)
    
    def validate_for_decision(self, source_name: str, 
                             decision_type: str) -> Dict[str, Any]:
        """验证数据源是否满足决策要求"""
        result = {
            'source': source_name,
            'decision_type': decision_type,
            'valid': False,
            'issues': []
        }
        
        source = self.get_source(source_name)
        if not source:
            result['issues'].append(f"未知数据源: {source_name}")
            return result
        
        requirements = self.DECISION_REQUIREMENTS.get(decision_type)
        if not requirements:
            result['issues'].append(f"未知决策类型: {decision_type}")
            return result
        
        # 检查等级
        grade_order = {"S级": 4, "A级": 3, "B级": 2, "C级": 1, "未分级": 0}
        min_grade_level = grade_order.get(requirements['min_grade'].value, 0)
        source_grade_level = grade_order.get(source.grade.value, 0)
        
        if source_grade_level < min_grade_level:
            result['issues'].append(
                f"数据源等级 {source.grade.value} 低于要求 {requirements['min_grade'].value}"
            )
        
        # 检查可靠性
        if source.reliability < requirements['min_reliability']:
            result['issues'].append(
                f"数据源可靠性 {source.reliability:.0%} 低于要求 {requirements['min_reliability']:.0%}"
            )
        
        # 检查状态
        if source.status != "active":
            result['issues'].append(f"数据源状态异常: {source.status}")
        
        result['valid'] = len(result['issues']) == 0
        return result
    
    def get_fallback_chain(self, data_type: DataType) -> List[str]:
        """获取数据源降级链"""
        sources = self.get_sources_by_type(data_type)
        
        # 按等级和可靠性排序
        def sort_key(s: DataSourceConfig) -> tuple:
            grade_order = {"S级": 0, "A级": 1, "B级": 2, "C级": 3}
            return (grade_order.get(s.grade.value, 4), -s.reliability)
        
        sorted_sources = sorted(sources, key=sort_key)
        return [s.name for s in sorted_sources if s.status == "active"]
    
    def get_report(self) -> str:
        """生成数据分级报告"""
        report = """# 数据分级体系报告

## 数据源分级总览

| 等级 | 数量 | 平均可靠性 | 主要用途 |
|------|------|------------|----------|
"""
        
        for grade in [DataGrade.S, DataGrade.A, DataGrade.B, DataGrade.C]:
            sources = self.get_sources_by_grade(grade)
            if sources:
                avg_reliability = sum(s.reliability for s in sources) / len(sources)
                purpose = {
                    DataGrade.S: "核心决策",
                    DataGrade.A: "辅助决策",
                    DataGrade.B: "参考信息",
                    DataGrade.C: "情绪感知"
                }.get(grade, "未知")
                report += f"| {grade.value} | {len(sources)} | {avg_reliability:.0%} | {purpose} |\n"
        
        report += "\n## 各数据源详情\n\n"
        
        for grade in [DataGrade.S, DataGrade.A, DataGrade.B, DataGrade.C]:
            sources = self.get_sources_by_grade(grade)
            if sources:
                report += f"### {grade.value}数据源\n\n"
                for s in sources:
                    status_emoji = "✅" if s.status == "active" else "❌"
                    report += f"- {status_emoji} **{s.name}**\n"
                    report += f"  - 可靠性: {s.reliability:.0%}\n"
                    report += f"  - 延迟: {s.latency_ms}ms\n"
                    report += f"  - 覆盖率: {s.coverage:.0%}\n"
                    report += f"  - 数据类型: {', '.join(t.value for t in s.data_types)}\n"
                report += "\n"
        
        # 降级链
        report += "## 数据源降级链\n\n"
        for data_type in DataType:
            chain = self.get_fallback_chain(data_type)
            if chain:
                report += f"- **{data_type.value}**: {' → '.join(chain)}\n"
        
        return report
    
    def save_report(self):
        """保存报告"""
        report = self.get_report()
        report_path = Path.home() / ".openclaw/workspace/memory/data-grading-report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)


# 使用示例
if __name__ == "__main__":
    system = DataGradingSystem()
    
    print("=== 数据分级体系 ===\n")
    
    # 获取最佳数据源
    print("【最佳数据源】")
    for data_type in DataType:
        best = system.get_best_source(data_type)
        if best:
            print(f"  {data_type.value}: {best.name} ({best.grade.value})")
    
    print("\n【数据源降级链】")
    for data_type in [DataType.QUOTE, DataType.NEWS, DataType.SENTIMENT]:
        chain = system.get_fallback_chain(data_type)
        print(f"  {data_type.value}: {' → '.join(chain)}")
    
    print("\n【决策验证】")
    result = system.validate_for_decision("akshare", "核心决策")
    print(f"  AKShare用于核心决策: {'✅' if result['valid'] else '❌'}")
    if result['issues']:
        print(f"  问题: {result['issues']}")
    
    result = system.validate_for_decision("guba", "核心决策")
    print(f"  股吧用于核心决策: {'✅' if result['valid'] else '❌'}")
    if result['issues']:
        print(f"  问题: {result['issues']}")
    
    print("\n" + system.get_report())

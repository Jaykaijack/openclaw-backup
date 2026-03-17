#!/usr/bin/env python3
"""
二郎知识库系统
Knowledge Base System for Erlang Quant System

功能：
1. 知识存储：策略、经验、教训
2. 知识检索：语义搜索、标签过滤
3. 知识更新：学习、修正、进化
4. 知识应用：自动推荐、智能提示
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


class KnowledgeType(Enum):
    """知识类型"""
    STRATEGY = "策略"      # 交易策略
    EXPERIENCE = "经验"    # 实战经验
    LESSON = "教训"        # 失败教训
    INSIGHT = "洞察"       # 市场洞察
    PATTERN = "模式"       # 价格模式
    FACTOR = "因子"        # 量化因子
    RULE = "规则"          # 交易规则
    CONCEPT = "概念"       # 投资概念


class KnowledgeLevel(Enum):
    """知识等级"""
    CORE = "核心"          # 核心知识，必须掌握
    IMPORTANT = "重要"     # 重要知识，经常使用
    USEFUL = "有用"        # 有用知识，偶尔使用
    REFERENCE = "参考"     # 参考知识，了解即可


@dataclass
class Knowledge:
    """知识条目"""
    id: str
    type: KnowledgeType
    level: KnowledgeLevel
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    source: str = ""  # 来源：实战/学习/总结
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0  # 使用次数
    success_rate: Optional[float] = None  # 成功率（如适用）
    related_ids: List[str] = field(default_factory=list)  # 关联知识
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'type': self.type.value,
            'level': self.level.value,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'source': self.source,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'usage_count': self.usage_count,
            'success_rate': self.success_rate,
            'related_ids': self.related_ids
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Knowledge':
        """从字典创建"""
        return cls(
            id=data['id'],
            type=KnowledgeType(data['type']),
            level=KnowledgeLevel(data['level']),
            title=data['title'],
            content=data['content'],
            tags=data.get('tags', []),
            source=data.get('source', ''),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            usage_count=data.get('usage_count', 0),
            success_rate=data.get('success_rate'),
            related_ids=data.get('related_ids', [])
        )


class KnowledgeBase:
    """知识库"""
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path.home() / ".openclaw/workspace/memory/knowledge-base.json"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.knowledge: Dict[str, Knowledge] = {}
        self.load()
    
    def load(self):
        """加载知识库"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get('knowledge', []):
                    k = Knowledge.from_dict(item)
                    self.knowledge[k.id] = k
    
    def save(self):
        """保存知识库"""
        data = {
            'knowledge': [k.to_dict() for k in self.knowledge.values()],
            'updated_at': datetime.now().isoformat()
        }
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, type: KnowledgeType, level: KnowledgeLevel,
            title: str, content: str, tags: List[str] = None,
            source: str = "", success_rate: float = None) -> Knowledge:
        """添加知识"""
        # 生成ID
        id = f"{type.value[:2]}{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        k = Knowledge(
            id=id,
            type=type,
            level=level,
            title=title,
            content=content,
            tags=tags or [],
            source=source,
            success_rate=success_rate
        )
        
        self.knowledge[k.id] = k
        self.save()
        return k
    
    def get(self, id: str) -> Optional[Knowledge]:
        """获取知识"""
        k = self.knowledge.get(id)
        if k:
            k.usage_count += 1
            k.updated_at = datetime.now()
            self.save()
        return k
    
    def search(self, query: str = None, type: KnowledgeType = None,
               level: KnowledgeLevel = None, tags: List[str] = None) -> List[Knowledge]:
        """搜索知识"""
        results = list(self.knowledge.values())
        
        # 类型过滤
        if type:
            results = [k for k in results if k.type == type]
        
        # 等级过滤
        if level:
            results = [k for k in results if k.level == level]
        
        # 标签过滤
        if tags:
            results = [k for k in results if any(t in k.tags for t in tags)]
        
        # 关键词搜索
        if query:
            query_lower = query.lower()
            results = [
                k for k in results
                if query_lower in k.title.lower() or query_lower in k.content.lower()
            ]
        
        # 按使用次数和等级排序
        level_order = {"核心": 0, "重要": 1, "有用": 2, "参考": 3}
        results.sort(key=lambda k: (level_order.get(k.level.value, 4), -k.usage_count))
        
        return results
    
    def update(self, id: str, **kwargs) -> Optional[Knowledge]:
        """更新知识"""
        k = self.knowledge.get(id)
        if not k:
            return None
        
        for key, value in kwargs.items():
            if hasattr(k, key) and key not in ['id', 'created_at']:
                setattr(k, key, value)
        
        k.updated_at = datetime.now()
        self.save()
        return k
    
    def delete(self, id: str) -> bool:
        """删除知识"""
        if id in self.knowledge:
            del self.knowledge[id]
            self.save()
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            'total': len(self.knowledge),
            'by_type': {},
            'by_level': {},
            'by_source': {},
            'most_used': [],
            'recent': []
        }
        
        for k in self.knowledge.values():
            # 按类型统计
            type_name = k.type.value
            stats['by_type'][type_name] = stats['by_type'].get(type_name, 0) + 1
            
            # 按等级统计
            level_name = k.level.value
            stats['by_level'][level_name] = stats['by_level'].get(level_name, 0) + 1
            
            # 按来源统计
            if k.source:
                stats['by_source'][k.source] = stats['by_source'].get(k.source, 0) + 1
        
        # 最常用
        sorted_by_usage = sorted(self.knowledge.values(), key=lambda k: -k.usage_count)
        stats['most_used'] = [
            {'id': k.id, 'title': k.title, 'usage_count': k.usage_count}
            for k in sorted_by_usage[:5]
        ]
        
        # 最近更新
        sorted_by_time = sorted(self.knowledge.values(), key=lambda k: -k.updated_at.timestamp())
        stats['recent'] = [
            {'id': k.id, 'title': k.title, 'updated_at': k.updated_at.isoformat()}
            for k in sorted_by_time[:5]
        ]
        
        return stats
    
    def get_report(self) -> str:
        """生成知识库报告"""
        stats = self.get_stats()
        
        report = f"""# 二郎知识库报告

**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 统计概览

| 指标 | 数量 |
|------|------|
| 总知识数 | {stats['total']} |
| 核心知识 | {stats['by_level'].get('核心', 0)} |
| 重要知识 | {stats['by_level'].get('重要', 0)} |
| 有用知识 | {stats['by_level'].get('有用', 0)} |
| 参考知识 | {stats['by_level'].get('参考', 0)} |

## 按类型分布

| 类型 | 数量 |
|------|------|
"""
        for type_name, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
            report += f"| {type_name} | {count} |\n"
        
        report += "\n## 最常用知识\n\n"
        for item in stats['most_used']:
            report += f"- [{item['id']}] {item['title']} (使用{item['usage_count']}次)\n"
        
        report += "\n## 最近更新\n\n"
        for item in stats['recent']:
            report += f"- [{item['id']}] {item['title']}\n"
        
        return report


# 初始化核心知识
def init_core_knowledge(kb: KnowledgeBase):
    """初始化核心知识"""
    
    # 策略知识
    kb.add(
        type=KnowledgeType.STRATEGY,
        level=KnowledgeLevel.CORE,
        title="情绪周期策略",
        content="""
情绪周期四阶段：
1. 冰点期：跌停>50，涨停<5 → 防守看戏
2. 修复期：涨停增加，跌停减少 → 轻仓试错
3. 高潮期：涨停>50，跌停<5 → 重仓出击
4. 退潮期：涨停减少，跌停增加 → 减仓观望

关键指标：
- 涨停家数
- 跌停家数
- 连板高度
- 晋级率
""",
        tags=["情绪", "周期", "核心策略"],
        source="实战总结",
        success_rate=0.75
    )
    
    kb.add(
        type=KnowledgeType.STRATEGY,
        level=KnowledgeLevel.CORE,
        title="权重股独立走强",
        content="""
权重股（如中信证券）可独立走强，不受小票情绪影响。

判断方法：
1. 观察权重股涨跌幅
2. 对比小票情绪
3. 若权重强+小票弱 → 情绪可上修一级

应用：
- 退潮期+权重强 → 可能是震荡而非冰点
- 冰点期+权重强 → 可能是修复前兆
""",
        tags=["权重股", "情绪判断", "修正"],
        source="2026-03-17省察",
        success_rate=0.80
    )
    
    # 教训知识
    kb.add(
        type=KnowledgeType.LESSON,
        level=KnowledgeLevel.CORE,
        title="退潮期≠冰点",
        content="""
错误：将退潮期判断为冰点
原因：只看小票情绪，忽略权重股
修正：区分小票情绪和大盘情绪

教训：
- 不要只看涨停跌停数
- 要结合权重股表现
- 退潮期可能有结构性机会
""",
        tags=["教训", "情绪判断", "权重股"],
        source="2026-03-17实战"
    )
    
    # 因子知识
    kb.add(
        type=KnowledgeType.FACTOR,
        level=KnowledgeLevel.IMPORTANT,
        title="量价因子",
        content="""
量价因子组合：
1. 量比 > 1.5：放量
2. 换手率 3-10%：活跃
3. 价格位置：MA5/MA20上方
4. 成交额排名：前100

信号：
- 放量突破MA20 → 买入信号
- 缩量跌破MA5 → 卖出信号
""",
        tags=["因子", "量价", "技术分析"],
        source="学习总结"
    )
    
    # 规则知识
    kb.add(
        type=KnowledgeType.RULE,
        level=KnowledgeLevel.CORE,
        title="止损纪律",
        content="""
止损规则：
1. 单笔亏损 7-8% 强制离场
2. 单笔风险不超过总资金 1%
3. 连续3笔亏损 → 停止交易，复盘

执行要点：
- 设定止损价后严格执行
- 不抱侥幸心理
- 止损后不立即回补
""",
        tags=["止损", "风控", "纪律"],
        source="SEPA系统"
    )
    
    # 概念知识
    kb.add(
        type=KnowledgeType.CONCEPT,
        level=KnowledgeLevel.IMPORTANT,
        title="VCP形态",
        content="""
VCP (Volatility Contraction Pattern) 波动收缩形态

特征：
1. 价格波动逐步收窄
2. 成交量萎缩
3. 突破前夜蓄势

识别要点：
- 至少3次收缩
- 每次收缩幅度减小
- 最后收缩成交量最小

买点：
- 突破最后一次收缩上沿
- 放量确认
""",
        tags=["VCP", "形态", "买点"],
        source="马克·米勒维尼SEPA"
    )


# 使用示例
if __name__ == "__main__":
    kb = KnowledgeBase()
    
    # 初始化核心知识（仅首次运行）
    if len(kb.knowledge) == 0:
        print("初始化核心知识...")
        init_core_knowledge(kb)
    
    print("=== 知识库统计 ===")
    stats = kb.get_stats()
    print(f"总知识数: {stats['total']}")
    print(f"按类型: {stats['by_type']}")
    print(f"按等级: {stats['by_level']}")
    
    print("\n=== 搜索'情绪' ===")
    results = kb.search(query="情绪")
    for k in results[:3]:
        print(f"- [{k.id}] {k.title}")
    
    print("\n" + kb.get_report())

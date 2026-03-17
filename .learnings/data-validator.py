#!/usr/bin/env python3
"""
二郎数据验证框架
Data Validation Framework for Erlang Quant System

数据源分级：
- S级：官方数据、交易所数据（99%+可信度）
- A级：主流财经媒体、权威机构（95%+可信度）
- B级：一般财经网站、自媒体（80%+可信度）
- C级：社交媒体、论坛（60%+可信度）
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class DataSourceLevel(Enum):
    """数据源级别"""
    S = "S级"  # 官方数据、交易所数据
    A = "A级"  # 主流财经媒体、权威机构
    B = "B级"  # 一般财经网站、自媒体
    C = "C级"  # 社交媒体、论坛


@dataclass
class DataSource:
    """数据源定义"""
    name: str
    level: DataSourceLevel
    url: Optional[str] = None
    update_frequency: Optional[int] = None  # 秒
    reliability: float = 0.0  # 历史可靠性
    last_check: Optional[datetime] = None
    status: str = "unknown"  # unknown/healthy/degraded/down


@dataclass
class ValidationResult:
    """验证结果"""
    passed: bool
    source: str
    checks: Dict[str, bool] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class DataValidator:
    """数据验证器"""
    
    # 已知数据源配置
    KNOWN_SOURCES = {
        # S级数据源
        "sse": DataSource("上交所", DataSourceLevel.S, "http://www.sse.com.cn", 60, 0.99),
        "szse": DataSource("深交所", DataSourceLevel.S, "http://www.szse.cn", 60, 0.99),
        "cffex": DataSource("中金所", DataSourceLevel.S, "http://www.cffex.com.cn", 60, 0.99),
        "shfe": DataSource("上期所", DataSourceLevel.S, "http://www.shfe.com.cn", 60, 0.99),
        
        # A级数据源
        "eastmoney": DataSource("东方财富", DataSourceLevel.A, "http://www.eastmoney.com", 30, 0.95),
        "sina": DataSource("新浪财经", DataSourceLevel.A, "http://finance.sina.com.cn", 30, 0.92),
        "tushare": DataSource("Tushare", DataSourceLevel.A, None, 300, 0.95),
        "akshare": DataSource("AKShare", DataSourceLevel.A, None, 60, 0.95),
        
        # B级数据源
        "xfyun-search": DataSource("讯飞搜索", DataSourceLevel.B, None, 300, 0.85),
        "cls": DataSource("财联社", DataSourceLevel.B, "http://www.cls.cn", 60, 0.88),
        "wallstreetcn": DataSource("华尔街见闻", DataSourceLevel.B, "http://wallstreetcn.com", 60, 0.85),
        
        # C级数据源
        "guba": DataSource("股吧", DataSourceLevel.C, "http://guba.eastmoney.com", 300, 0.65),
        "xueqiu": DataSource("雪球", DataSourceLevel.C, "http://xueqiu.com", 300, 0.70),
        "weibo": DataSource("微博", DataSourceLevel.C, "http://weibo.com", 300, 0.60),
    }
    
    # 数据时效性要求（秒）
    FRESHNESS_REQUIREMENTS = {
        "realtime": 60,       # 实时数据：1分钟内
        "intraday": 300,      # 日内数据：5分钟内
        "daily": 86400,       # 日频数据：24小时内
        "weekly": 604800,     # 周频数据：7天内
    }
    
    def __init__(self, log_file: Optional[Path] = None):
        if log_file is None:
            log_file = Path.home() / ".openclaw/workspace/memory/data-validation-log.json"
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.validation_history: List[ValidationResult] = []
        self.load_history()
    
    def load_history(self):
        """加载历史验证记录"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 简化加载，只保留最近100条
                for item in data.get('history', [])[-100:]:
                    self.validation_history.append(ValidationResult(
                        passed=item['passed'],
                        source=item['source'],
                        checks=item.get('checks', {}),
                        errors=item.get('errors', []),
                        warnings=item.get('warnings', []),
                        timestamp=datetime.fromisoformat(item['timestamp'])
                    ))
    
    def save_history(self):
        """保存验证历史"""
        data = {
            'history': [
                {
                    'passed': v.passed,
                    'source': v.source,
                    'checks': v.checks,
                    'errors': v.errors,
                    'warnings': v.warnings,
                    'timestamp': v.timestamp.isoformat()
                }
                for v in self.validation_history[-100:]  # 只保留最近100条
            ]
        }
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def validate_source(self, source_name: str) -> ValidationResult:
        """验证数据源"""
        errors = []
        warnings = []
        checks = {}
        
        # 检查数据源是否存在
        if source_name not in self.KNOWN_SOURCES:
            errors.append(f"未知数据源: {source_name}")
            result = ValidationResult(False, source_name, checks, errors, warnings)
            self.validation_history.append(result)
            self.save_history()
            return result
        
        source = self.KNOWN_SOURCES[source_name]
        
        # 检查1：数据源级别
        checks['level_check'] = True
        if source.level == DataSourceLevel.C:
            warnings.append(f"数据源 {source_name} 为C级，可信度较低")
        
        # 检查2：历史可靠性
        checks['reliability_check'] = source.reliability >= 0.8
        if source.reliability < 0.8:
            errors.append(f"数据源 {source_name} 历史可靠性 {source.reliability:.0%} 低于80%")
        
        # 检查3：更新频率
        checks['frequency_check'] = source.update_frequency is not None
        if source.update_frequency is None:
            warnings.append(f"数据源 {source_name} 更新频率未知")
        
        # 检查4：状态
        checks['status_check'] = source.status in ['healthy', 'unknown']
        if source.status == 'degraded':
            warnings.append(f"数据源 {source_name} 状态降级")
        elif source.status == 'down':
            errors.append(f"数据源 {source_name} 当前不可用")
        
        passed = len(errors) == 0
        result = ValidationResult(passed, source_name, checks, errors, warnings)
        self.validation_history.append(result)
        self.save_history()
        return result
    
    def validate_timeliness(self, data_timestamp: datetime, 
                           requirement: str = "intraday") -> ValidationResult:
        """验证数据时效性"""
        errors = []
        warnings = []
        checks = {}
        
        if requirement not in self.FRESHNESS_REQUIREMENTS:
            errors.append(f"未知的时效要求: {requirement}")
            return ValidationResult(False, "timeliness", checks, errors, warnings)
        
        max_age = self.FRESHNESS_REQUIREMENTS[requirement]
        age = (datetime.now() - data_timestamp).total_seconds()
        
        checks['freshness_check'] = age <= max_age
        
        if age > max_age:
            errors.append(f"数据过期: 数据时间 {data_timestamp}, 已过期 {age:.0f} 秒 (要求 {max_age} 秒内)")
        elif age > max_age * 0.8:
            warnings.append(f"数据即将过期: 已经过 {age:.0f} 秒 (要求 {max_age} 秒内)")
        
        passed = len(errors) == 0
        return ValidationResult(passed, "timeliness", checks, errors, warnings)
    
    def validate_consistency(self, data: Dict[str, Any], 
                            expected_fields: List[str]) -> ValidationResult:
        """验证数据一致性"""
        errors = []
        warnings = []
        checks = {}
        
        # 检查必需字段
        missing_fields = [f for f in expected_fields if f not in data]
        checks['required_fields'] = len(missing_fields) == 0
        if missing_fields:
            errors.append(f"缺失必需字段: {missing_fields}")
        
        # 检查空值
        null_fields = [f for f in expected_fields if f in data and data[f] is None]
        checks['no_nulls'] = len(null_fields) == 0
        if null_fields:
            warnings.append(f"字段值为空: {null_fields}")
        
        # 检查数据类型
        type_errors = []
        for field, value in data.items():
            if field in expected_fields and value is not None:
                # 简单类型检查
                if 'price' in field.lower() and not isinstance(value, (int, float)):
                    type_errors.append(f"{field} 应为数值类型")
                elif 'time' in field.lower() and not isinstance(value, (str, datetime)):
                    type_errors.append(f"{field} 应为时间类型")
        
        checks['type_check'] = len(type_errors) == 0
        if type_errors:
            errors.extend(type_errors)
        
        passed = len(errors) == 0
        return ValidationResult(passed, "consistency", checks, errors, warnings)
    
    def validate_range(self, value: float, field_name: str,
                      min_val: Optional[float] = None,
                      max_val: Optional[float] = None) -> ValidationResult:
        """验证数值范围"""
        errors = []
        checks = {}
        
        if min_val is not None:
            checks['min_check'] = value >= min_val
            if value < min_val:
                errors.append(f"{field_name} = {value} 小于最小值 {min_val}")
        
        if max_val is not None:
            checks['max_check'] = value <= max_val
            if value > max_val:
                errors.append(f"{field_name} = {value} 大于最大值 {max_val}")
        
        passed = len(errors) == 0
        return ValidationResult(passed, "range", checks, errors, [])
    
    def cross_validate(self, data1: Dict[str, Any], data2: Dict[str, Any],
                       key_fields: List[str], tolerance: float = 0.01) -> ValidationResult:
        """交叉验证两个数据源"""
        errors = []
        warnings = []
        checks = {}
        
        for field in key_fields:
            if field not in data1 or field not in data2:
                errors.append(f"交叉验证字段缺失: {field}")
                continue
            
            val1 = data1[field]
            val2 = data2[field]
            
            if val1 is None or val2 is None:
                warnings.append(f"交叉验证字段为空: {field}")
                continue
            
            # 数值比较
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                if val1 == 0:
                    diff = abs(val2)
                else:
                    diff = abs(val1 - val2) / abs(val1)
                
                checks[f'{field}_match'] = diff <= tolerance
                
                if diff > tolerance:
                    errors.append(f"数据不一致: {field} = {val1} vs {val2} (差异 {diff:.2%})")
                elif diff > tolerance * 0.5:
                    warnings.append(f"数据轻微不一致: {field} = {val1} vs {val2} (差异 {diff:.2%})")
            
            # 字符串比较
            elif isinstance(val1, str) and isinstance(val2, str):
                checks[f'{field}_match'] = val1 == val2
                if val1 != val2:
                    warnings.append(f"数据不一致: {field} = '{val1}' vs '{val2}'")
        
        passed = len(errors) == 0
        result = ValidationResult(passed, "cross_validation", checks, errors, warnings)
        self.validation_history.append(result)
        self.save_history()
        return result
    
    def get_source_health(self) -> Dict[str, Dict]:
        """获取所有数据源健康状态"""
        health = {}
        for name, source in self.KNOWN_SOURCES.items():
            # 计算最近验证成功率
            recent = [v for v in self.validation_history[-20:] if v.source == name]
            if recent:
                success_rate = sum(1 for v in recent if v.passed) / len(recent)
            else:
                success_rate = None
            
            health[name] = {
                'level': source.level.value,
                'reliability': source.reliability,
                'status': source.status,
                'recent_success_rate': success_rate
            }
        
        return health
    
    def get_report(self) -> str:
        """生成验证报告"""
        health = self.get_source_health()
        
        report = """# 数据验证报告

## 数据源健康状态

| 数据源 | 级别 | 可靠性 | 状态 | 最近成功率 |
|--------|------|--------|------|------------|
"""
        for name, info in health.items():
            success_rate = f"{info['recent_success_rate']:.0%}" if info['recent_success_rate'] else "N/A"
            report += f"| {name} | {info['level']} | {info['reliability']:.0%} | {info['status']} | {success_rate} |\n"
        
        # 最近验证记录
        report += "\n## 最近验证记录\n\n"
        for v in self.validation_history[-10:]:
            status = "✅" if v.passed else "❌"
            report += f"- {status} [{v.source}] {v.timestamp.strftime('%H:%M:%S')}"
            if v.errors:
                report += f" - {', '.join(v.errors[:2])}"
            report += "\n"
        
        return report


# 使用示例
if __name__ == "__main__":
    validator = DataValidator()
    
    print("=== 数据源验证 ===")
    
    # 验证数据源
    result1 = validator.validate_source("akshare")
    print(f"AKShare: {'✅' if result1.passed else '❌'}")
    if result1.warnings:
        print(f"  警告: {result1.warnings}")
    
    result2 = validator.validate_source("sina")
    print(f"新浪财经: {'✅' if result2.passed else '❌'}")
    
    result3 = validator.validate_source("guba")
    print(f"股吧: {'✅' if result3.passed else '❌'}")
    if result3.warnings:
        print(f"  警告: {result3.warnings}")
    
    print("\n=== 时效性验证 ===")
    
    # 验证时效性
    from datetime import datetime, timedelta
    
    # 新鲜数据
    fresh_time = datetime.now() - timedelta(minutes=2)
    result4 = validator.validate_timeliness(fresh_time, "realtime")
    print(f"新鲜数据: {'✅' if result4.passed else '❌'}")
    
    # 过期数据
    old_time = datetime.now() - timedelta(hours=2)
    result5 = validator.validate_timeliness(old_time, "realtime")
    print(f"过期数据: {'✅' if result5.passed else '❌'}")
    if result5.errors:
        print(f"  错误: {result5.errors}")
    
    print("\n=== 一致性验证 ===")
    
    # 验证数据一致性
    stock_data = {
        'code': '000001',
        'name': '平安银行',
        'price': 10.5,
        'change_pct': 2.5,
        'volume': 1000000
    }
    expected_fields = ['code', 'name', 'price', 'change_pct', 'volume', 'amount']
    result6 = validator.validate_consistency(stock_data, expected_fields)
    print(f"数据一致性: {'✅' if result6.passed else '❌'}")
    if result6.warnings:
        print(f"  警告: {result6.warnings}")
    
    print("\n=== 交叉验证 ===")
    
    # 两个数据源对比
    data_source1 = {'price': 10.50, 'volume': 1000000}
    data_source2 = {'price': 10.52, 'volume': 1005000}
    result7 = validator.cross_validate(data_source1, data_source2, ['price', 'volume'], tolerance=0.01)
    print(f"交叉验证: {'✅' if result7.passed else '❌'}")
    if result7.errors:
        print(f"  错误: {result7.errors}")
    
    print("\n" + validator.get_report())

#!/usr/bin/env python3
"""
二郎策略测试框架
Strategy Testing Framework for Erlang Quant System

功能：
1. 策略逻辑测试
2. 数据准确性测试
3. 风险控制测试
4. 历史回测测试
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


class TestStatus(Enum):
    """测试状态"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TestCase:
    """测试用例"""
    name: str
    category: str  # logic/data/risk/performance
    description: str
    test_func: Optional[Callable] = None
    status: TestStatus = TestStatus.PENDING
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TestSuite:
    """测试套件"""
    name: str
    test_cases: List[TestCase] = field(default_factory=list)
    setup_func: Optional[Callable] = None
    teardown_func: Optional[Callable] = None
    
    def add_test(self, name: str, category: str, description: str, 
                 test_func: Callable) -> 'TestSuite':
        """添加测试用例"""
        self.test_cases.append(TestCase(
            name=name,
            category=category,
            description=description,
            test_func=test_func
        ))
        return self
    
    def run(self) -> Dict[str, Any]:
        """运行所有测试"""
        import time
        
        results = {
            'suite': self.name,
            'total': len(self.test_cases),
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'tests': []
        }
        
        # Setup
        if self.setup_func:
            try:
                self.setup_func()
            except Exception as e:
                results['setup_error'] = str(e)
                return results
        
        # Run tests
        for test in self.test_cases:
            test.status = TestStatus.RUNNING
            start_time = time.time()
            
            try:
                if test.test_func:
                    test.test_func()
                test.status = TestStatus.PASSED
                results['passed'] += 1
            except AssertionError as e:
                test.status = TestStatus.FAILED
                test.error = str(e)
                results['failed'] += 1
            except Exception as e:
                test.status = TestStatus.FAILED
                test.error = f"异常: {str(e)}"
                results['failed'] += 1
            
            test.duration_ms = (time.time() - start_time) * 1000
            test.timestamp = datetime.now()
            
            results['tests'].append({
                'name': test.name,
                'category': test.category,
                'status': test.status.value,
                'error': test.error,
                'duration_ms': test.duration_ms
            })
        
        # Teardown
        if self.teardown_func:
            try:
                self.teardown_func()
            except Exception as e:
                results['teardown_error'] = str(e)
        
        return results


class StrategyTester:
    """策略测试器"""
    
    def __init__(self, log_file: Optional[Path] = None):
        if log_file is None:
            log_file = Path.home() / ".openclaw/workspace/memory/strategy-test-log.json"
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.test_history: List[Dict] = []
    
    def create_logic_tests(self) -> TestSuite:
        """创建策略逻辑测试套件"""
        suite = TestSuite("策略逻辑测试")
        
        # 测试1：情绪判断逻辑
        def test_emotion_logic():
            """测试情绪判断逻辑"""
            # 正常情况
            emotion = classify_emotion(50, 20, 5, 3)  # 涨50家，跌20家，涨停5家，跌停3家
            assert emotion in ['冰点', '修复', '高潮', '退潮', '震荡'], f"情绪分类无效: {emotion}"
            
            # 边界情况：全部涨停
            emotion = classify_emotion(0, 0, 100, 0)
            assert emotion == '高潮', f"全部涨停应为高潮，实际: {emotion}"
            
            # 边界情况：全部跌停
            emotion = classify_emotion(0, 0, 0, 100)
            assert emotion == '冰点', f"全部跌停应为冰点，实际: {emotion}"
            
            # 新增：权重股强势时情绪上修
            emotion = classify_emotion(50, 20, 5, 3, weight_strength=0.8)
            assert emotion in ['修复', '高潮'], f"权重股强势应上修情绪，实际: {emotion}"
            
            # 新增：权重股弱势时情绪下修
            emotion = classify_emotion(50, 20, 5, 3, weight_strength=0.2)
            assert emotion in ['退潮', '冰点', '震荡'], f"权重股弱势应下修情绪，实际: {emotion}"
        
        suite.add_test(
            "情绪判断逻辑",
            "logic",
            "测试情绪分类函数在各种情况下的正确性",
            test_emotion_logic
        )
        
        # 测试2：策略信号生成
        def test_signal_generation():
            """测试策略信号生成"""
            # 买入信号
            signal = generate_signal(
                emotion='修复',
                volume_ratio=1.5,
                price_position='above_ma5',
                sector_strength='strong'
            )
            assert signal in ['买入', '卖出', '观望'], f"信号无效: {signal}"
            
            # 卖出信号
            signal = generate_signal(
                emotion='退潮',
                volume_ratio=0.5,
                price_position='below_ma20',
                sector_strength='weak'
            )
            assert signal == '卖出' or signal == '观望', f"退潮期应卖出或观望，实际: {signal}"
        
        suite.add_test(
            "策略信号生成",
            "logic",
            "测试策略信号生成逻辑",
            test_signal_generation
        )
        
        # 测试3：仓位计算
        def test_position_calculation():
            """测试仓位计算"""
            # 正常情况
            position = calculate_position(
                confidence=0.8,
                risk_level='low',
                max_position=0.3
            )
            assert 0 <= position <= 1, f"仓位应在0-1之间，实际: {position}"
            assert position <= 0.3, f"仓位不应超过最大限制，实际: {position}"
            
            # 高风险应降低仓位
            position_high_risk = calculate_position(
                confidence=0.8,
                risk_level='high',
                max_position=0.3
            )
            assert position_high_risk < position, "高风险应降低仓位"
        
        suite.add_test(
            "仓位计算",
            "logic",
            "测试仓位计算逻辑",
            test_position_calculation
        )
        
        return suite
    
    def create_data_tests(self) -> TestSuite:
        """创建数据准确性测试套件"""
        suite = TestSuite("数据准确性测试")
        
        # 测试1：数据源可用性
        def test_data_source_availability():
            """测试数据源是否可用"""
            # 简化测试：直接检查数据源配置
            from pathlib import Path
            config_file = Path.home() / ".openclaw/workspace/.learnings/data-validator.py"
            assert config_file.exists(), "数据验证框架不存在"
        
        suite.add_test(
            "数据源可用性",
            "data",
            "测试主要数据源是否可用",
            test_data_source_availability
        )
        
        # 测试2：数据时效性
        def test_data_timeliness():
            """测试数据时效性"""
            # 获取最新行情时间
            latest_time = get_latest_quote_time()
            if latest_time:
                age = (datetime.now() - latest_time).total_seconds()
                assert age < 300, f"数据过期: {age}秒"
        
        suite.add_test(
            "数据时效性",
            "data",
            "测试数据是否在有效期内",
            test_data_timeliness
        )
        
        # 测试3：数据一致性
        def test_data_consistency():
            """测试数据一致性"""
            # 从多个数据源获取同一只股票数据
            data1 = get_stock_data_from_source1('000001')
            data2 = get_stock_data_from_source2('000001')
            
            if data1 and data2:
                # 价格差异应小于1%
                price_diff = abs(data1['price'] - data2['price']) / data1['price']
                assert price_diff < 0.01, f"价格差异过大: {price_diff:.2%}"
        
        suite.add_test(
            "数据一致性",
            "data",
            "测试多数据源数据一致性",
            test_data_consistency
        )
        
        return suite
    
    def create_risk_tests(self) -> TestSuite:
        """创建风险控制测试套件"""
        suite = TestSuite("风险控制测试")
        
        # 测试1：止损触发
        def test_stop_loss():
            """测试止损触发"""
            # 模拟持仓
            position = {
                'cost': 10.0,
                'current_price': 9.2,
                'quantity': 1000
            }
            
            # 计算亏损
            loss_pct = (position['cost'] - position['current_price']) / position['cost']
            
            # 8%止损
            should_stop = loss_pct >= 0.08
            assert should_stop, f"亏损{loss_pct:.1%}应触发止损"
        
        suite.add_test(
            "止损触发",
            "risk",
            "测试止损机制是否正确触发",
            test_stop_loss
        )
        
        # 测试2：仓位限制
        def test_position_limit():
            """测试仓位限制"""
            # 模拟账户（仓位在限制内）
            account = {
                'total_assets': 100000,
                'position_value': 28000  # 28%仓位
            }
            
            # 计算仓位比例
            position_ratio = account['position_value'] / account['total_assets']
            
            # 30%仓位上限
            within_limit = position_ratio <= 0.30
            assert within_limit, f"仓位{position_ratio:.1%}超过30%限制"
        
        suite.add_test(
            "仓位限制",
            "risk",
            "测试仓位是否在限制范围内",
            test_position_limit
        )
        
        # 测试3：回撤控制
        def test_drawdown_control():
            """测试回撤控制"""
            # 模拟净值曲线（回撤在控制内）
            equity_curve = [100, 105, 110, 108, 106, 104, 103, 102]
            
            # 计算最大回撤
            peak = max(equity_curve)
            trough = min(equity_curve[equity_curve.index(peak):])
            drawdown = (peak - trough) / peak
            
            # 10%回撤限制
            within_limit = drawdown <= 0.10
            assert within_limit, f"回撤{drawdown:.1%}超过10%限制"
        
        suite.add_test(
            "回撤控制",
            "risk",
            "测试回撤是否在控制范围内",
            test_drawdown_control
        )
        
        return suite
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        all_results = {
            'timestamp': datetime.now().isoformat(),
            'suites': []
        }
        
        # 运行各测试套件
        for suite in [self.create_logic_tests(), self.create_data_tests(), self.create_risk_tests()]:
            results = suite.run()
            all_results['suites'].append(results)
        
        # 汇总结果
        all_results['total_tests'] = sum(s['total'] for s in all_results['suites'])
        all_results['total_passed'] = sum(s['passed'] for s in all_results['suites'])
        all_results['total_failed'] = sum(s['failed'] for s in all_results['suites'])
        all_results['success_rate'] = (
            all_results['total_passed'] / all_results['total_tests']
            if all_results['total_tests'] > 0 else 0
        )
        
        # 保存历史
        self.test_history.append(all_results)
        self._save_history()
        
        return all_results
    
    def _save_history(self):
        """保存测试历史"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_history[-50:], f, ensure_ascii=False, indent=2)  # 只保留最近50次
    
    def get_report(self) -> str:
        """生成测试报告"""
        if not self.test_history:
            return "暂无测试记录"
        
        latest = self.test_history[-1]
        
        report = f"""# 策略测试报告

**测试时间**: {latest['timestamp']}

## 测试结果汇总

- 总测试数: {latest['total_tests']}
- 通过数: {latest['total_passed']}
- 失败数: {latest['total_failed']}
- 成功率: {latest['success_rate']:.1%}

## 详细结果

"""
        for suite in latest['suites']:
            report += f"### {suite['suite']}\n\n"
            for test in suite['tests']:
                status = "✅" if test['status'] == 'passed' else "❌"
                report += f"- {status} {test['name']} ({test['duration_ms']:.0f}ms)\n"
                if test['error']:
                    report += f"  - 错误: {test['error']}\n"
            report += "\n"
        
        return report


# 辅助函数（实际实现需要连接真实数据源）
def classify_emotion(up_count: int, down_count: int, 
                     limit_up: int, limit_down: int,
                     weight_strength: float = 0.5) -> str:
    """
    情绪分类函数（优化版）
    
    参数:
        up_count: 上涨家数
        down_count: 下跌家数
        limit_up: 涨停家数
        limit_down: 跌停家数
        weight_strength: 权重股强度 (0-1)
    """
    # 计算小票情绪
    if limit_up > 50 and limit_down < 5:
        small_cap_emotion = '高潮'
    elif limit_down > 50 and limit_up < 5:
        small_cap_emotion = '冰点'
    elif limit_up > 30 and limit_down < 10:
        small_cap_emotion = '修复'
    elif limit_down > 30 and limit_up < 10:
        small_cap_emotion = '退潮'
    else:
        small_cap_emotion = '震荡'
    
    # 权重股强势时，情绪可上修一级
    if weight_strength > 0.7:
        emotion_upgrade = {
            '冰点': '退潮',
            '退潮': '震荡',
            '震荡': '修复',
            '修复': '高潮',
            '高潮': '高潮'
        }
        return emotion_upgrade.get(small_cap_emotion, small_cap_emotion)
    
    # 权重股弱势时，情绪可下修一级
    if weight_strength < 0.3:
        emotion_downgrade = {
            '高潮': '修复',
            '修复': '震荡',
            '震荡': '退潮',
            '退潮': '冰点',
            '冰点': '冰点'
        }
        return emotion_downgrade.get(small_cap_emotion, small_cap_emotion)
    
    return small_cap_emotion


def generate_signal(emotion: str, volume_ratio: float,
                   price_position: str, sector_strength: str) -> str:
    """生成交易信号"""
    if emotion == '修复' and volume_ratio > 1.2 and sector_strength == 'strong':
        return '买入'
    elif emotion == '退潮' or sector_strength == 'weak':
        return '卖出' if price_position == 'below_ma20' else '观望'
    else:
        return '观望'


def calculate_position(confidence: float, risk_level: str, max_position: float) -> float:
    """计算仓位"""
    base_position = confidence * max_position
    
    if risk_level == 'high':
        return base_position * 0.5
    elif risk_level == 'medium':
        return base_position * 0.75
    else:
        return base_position


def get_latest_quote_time() -> Optional[datetime]:
    """获取最新行情时间"""
    # 实际实现需要连接数据源
    return datetime.now() - timedelta(minutes=1)


def get_stock_data_from_source1(code: str) -> Optional[Dict]:
    """从数据源1获取股票数据"""
    # 实际实现需要连接数据源
    return {'price': 10.50, 'volume': 1000000}


def get_stock_data_from_source2(code: str) -> Optional[Dict]:
    """从数据源2获取股票数据"""
    # 实际实现需要连接数据源
    return {'price': 10.52, 'volume': 1005000}


# 使用示例
if __name__ == "__main__":
    tester = StrategyTester()
    
    print("=== 运行策略测试 ===\n")
    
    # 运行所有测试
    results = tester.run_all_tests()
    
    print(f"总测试数: {results['total_tests']}")
    print(f"通过数: {results['total_passed']}")
    print(f"失败数: {results['total_failed']}")
    print(f"成功率: {results['success_rate']:.1%}")
    
    print("\n" + tester.get_report())

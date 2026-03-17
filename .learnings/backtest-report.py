#!/usr/bin/env python3
"""
二郎回测报告生成器
Backtest Report Generator for Erlang Quant System

功能：
1. 运行所有测试
2. 生成回测报告
3. 分析优化建议
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class BacktestReporter:
    """回测报告生成器"""
    
    def __init__(self):
        self.workspace = Path.home() / ".openclaw/workspace"
        self.results = {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {}
        }
        
        # 添加模块路径
        import sys
        import importlib.util
        
        def load_module(name, path):
            """动态加载模块"""
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        
        # 1. 策略测试
        try:
            strategy_tester = load_module('strategy_tester', self.workspace / '.learnings/strategy-tester.py')
            tester = strategy_tester.StrategyTester()
            test_results = tester.run_all_tests()
            results['tests']['strategy'] = {
                'status': 'passed' if test_results['success_rate'] >= 0.8 else 'failed',
                'success_rate': test_results['success_rate'],
                'total': test_results['total_tests'],
                'passed': test_results['total_passed'],
                'failed': test_results['total_failed']
            }
        except Exception as e:
            results['tests']['strategy'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # 2. 数据验证
        try:
            data_validator = load_module('data_validator', self.workspace / '.learnings/data-validator.py')
            validator = data_validator.DataValidator()
            
            # 验证主要数据源
            sources = ['akshare', 'sina', 'eastmoney']
            source_results = {}
            for source in sources:
                result = validator.validate_source(source)
                source_results[source] = result.passed
            
            results['tests']['data'] = {
                'status': 'passed' if all(source_results.values()) else 'warning',
                'sources': source_results
            }
        except Exception as e:
            results['tests']['data'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # 3. 准确率追踪
        try:
            accuracy_tracker = load_module('accuracy_tracker', self.workspace / '.learnings/accuracy-tracker.py')
            tracker = accuracy_tracker.AccuracyTracker()
            accuracy = tracker.get_accuracy(days=7)
            
            results['tests']['accuracy'] = {
                'status': 'passed' if accuracy and accuracy >= 0.7 else 'warning',
                'accuracy': accuracy
            }
        except Exception as e:
            results['tests']['accuracy'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # 4. 数据分级
        try:
            data_grading = load_module('data_grading_system', self.workspace / '.learnings/data-grading-system.py')
            system = data_grading.DataGradingSystem()
            
            # 检查核心决策数据源
            core_sources = ['akshare', 'eastmoney']
            grade_results = {}
            for source in core_sources:
                result = system.validate_for_decision(source, '核心决策')
                grade_results[source] = result['valid']
            
            results['tests']['grading'] = {
                'status': 'passed' if all(grade_results.values()) else 'warning',
                'core_sources': grade_results
            }
        except Exception as e:
            results['tests']['grading'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # 计算总体状态
        statuses = [t['status'] for t in results['tests'].values()]
        if all(s == 'passed' for s in statuses):
            results['overall_status'] = 'passed'
        elif any(s == 'error' for s in statuses):
            results['overall_status'] = 'error'
        elif any(s == 'failed' for s in statuses):
            results['overall_status'] = 'failed'
        else:
            results['overall_status'] = 'warning'
        
        self.results = results
        return results
    
    def generate_report(self) -> str:
        """生成回测报告"""
        if not self.results:
            self.run_all_tests()
        
        r = self.results
        
        report = f"""# 二郎回测报告

**测试时间**: {r['timestamp']}
**总体状态**: {self._status_emoji(r['overall_status'])} {r['overall_status'].upper()}

---

## 一、策略测试

"""
        
        if 'strategy' in r['tests']:
            s = r['tests']['strategy']
            if s['status'] == 'error':
                report += f"**状态**: ❌ 错误\n**错误**: {s['error']}\n"
            else:
                report += f"""**状态**: {self._status_emoji(s['status'])} {s['status']}

| 指标 | 数值 |
|------|------|
| 成功率 | {s['success_rate']:.1%} |
| 总测试数 | {s['total']} |
| 通过数 | {s['passed']} |
| 失败数 | {s['failed']} |
"""
        
        report += "\n---\n\n## 二、数据验证\n\n"
        
        if 'data' in r['tests']:
            d = r['tests']['data']
            if d['status'] == 'error':
                report += f"**状态**: ❌ 错误\n**错误**: {d['error']}\n"
            else:
                report += f"**状态**: {self._status_emoji(d['status'])} {d['status']}\n\n"
                report += "| 数据源 | 状态 |\n|--------|------|\n"
                for source, passed in d['sources'].items():
                    report += f"| {source} | {'✅' if passed else '❌'} |\n"
        
        report += "\n---\n\n## 三、准确率追踪\n\n"
        
        if 'accuracy' in r['tests']:
            a = r['tests']['accuracy']
            if a['status'] == 'error':
                report += f"**状态**: ❌ 错误\n**错误**: {a['error']}\n"
            else:
                accuracy_str = f"{a['accuracy']:.1%}" if a['accuracy'] else "N/A"
                report += f"""**状态**: {self._status_emoji(a['status'])} {a['status']}

| 指标 | 数值 |
|------|------|
| 7日准确率 | {accuracy_str} |
"""
        
        report += "\n---\n\n## 四、数据分级\n\n"
        
        if 'grading' in r['tests']:
            g = r['tests']['grading']
            if g['status'] == 'error':
                report += f"**状态**: ❌ 错误\n**错误**: {g['error']}\n"
            else:
                report += f"**状态**: {self._status_emoji(g['status'])} {g['status']}\n\n"
                report += "| 数据源 | 核心决策可用 |\n|--------|--------------|\n"
                for source, valid in g['core_sources'].items():
                    report += f"| {source} | {'✅' if valid else '❌'} |\n"
        
        report += "\n---\n\n## 五、优化建议\n\n"
        
        suggestions = self._generate_suggestions()
        for i, suggestion in enumerate(suggestions, 1):
            report += f"{i}. {suggestion}\n"
        
        return report
    
    def _status_emoji(self, status: str) -> str:
        """状态表情"""
        return {
            'passed': '✅',
            'warning': '⚠️',
            'failed': '❌',
            'error': '🔥'
        }.get(status, '❓')
    
    def _generate_suggestions(self) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        if 'strategy' in self.results['tests']:
            s = self.results['tests']['strategy']
            if s.get('success_rate', 0) < 0.9:
                suggestions.append("策略测试成功率低于90%，建议检查失败用例")
        
        if 'accuracy' in self.results['tests']:
            a = self.results['tests']['accuracy']
            if a.get('accuracy', 0) and a['accuracy'] < 0.7:
                suggestions.append("7日准确率低于70%，建议优化情绪判断逻辑")
        
        if 'data' in self.results['tests']:
            d = self.results['tests']['data']
            if d.get('sources'):
                failed_sources = [k for k, v in d['sources'].items() if not v]
                if failed_sources:
                    suggestions.append(f"数据源 {', '.join(failed_sources)} 验证失败，建议检查或使用备用源")
        
        if not suggestions:
            suggestions.append("系统状态良好，继续保持")
        
        return suggestions
    
    def save_report(self, path: Path = None):
        """保存报告"""
        if path is None:
            path = self.workspace / "memory" / "backtest-report.md"
        
        report = self.generate_report()
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return path


def main():
    """主函数"""
    reporter = BacktestReporter()
    
    print("=== 运行回测 ===\n")
    
    # 运行测试
    results = reporter.run_all_tests()
    
    print(f"总体状态: {results['overall_status']}")
    
    # 生成报告
    report = reporter.generate_report()
    print("\n" + report)
    
    # 保存报告
    path = reporter.save_report()
    print(f"\n报告已保存: {path}")


if __name__ == "__main__":
    main()

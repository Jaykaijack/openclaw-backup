#!/usr/bin/env python3
"""
二郎准确率追踪器
Accuracy Tracker for Erlang Quant System
"""

import json
import os
from datetime import datetime
from pathlib import Path

class AccuracyTracker:
    """准确率追踪器"""
    
    def __init__(self, log_file=None):
        if log_file is None:
            log_file = Path.home() / ".openclaw/workspace/memory/accuracy-log.json"
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.load()
    
    def load(self):
        """加载历史记录"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'predictions': [],
                'stats': {
                    'total': 0,
                    'verified': 0,
                    'correct': 0,
                    'accuracy': None
                }
            }
    
    def save(self):
        """保存记录"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def record_prediction(self, category, prediction, confidence=0.5):
        """记录预测"""
        entry = {
            'id': len(self.data['predictions']),
            'time': datetime.now().isoformat(),
            'category': category,  # 情绪/策略/风险/标的
            'prediction': prediction,
            'confidence': confidence,
            'verified': False,
            'actual': None,
            'correct': None
        }
        self.data['predictions'].append(entry)
        self.data['stats']['total'] += 1
        self.save()
        return entry['id']
    
    def verify_prediction(self, prediction_id, actual_result):
        """验证预测"""
        if prediction_id >= len(self.data['predictions']):
            return None
        
        entry = self.data['predictions'][prediction_id]
        entry['verified'] = True
        entry['actual'] = actual_result
        entry['verified_time'] = datetime.now().isoformat()
        
        # 判断是否正确
        if entry['category'] == '情绪':
            # 情绪判断：完全匹配为正确
            entry['correct'] = (entry['prediction'] == actual_result)
        elif entry['category'] == '策略':
            # 策略判断：方向一致为正确
            entry['correct'] = self._compare_direction(entry['prediction'], actual_result)
        elif entry['category'] == '风险':
            # 风险判断：风险发生即为正确预警
            entry['correct'] = (entry['prediction'] == actual_result)
        else:
            entry['correct'] = (entry['prediction'] == actual_result)
        
        # 更新统计
        self.data['stats']['verified'] += 1
        if entry['correct']:
            self.data['stats']['correct'] += 1
        
        # 计算准确率
        self.data['stats']['accuracy'] = (
            self.data['stats']['correct'] / self.data['stats']['verified']
        )
        
        self.save()
        return entry
    
    def _compare_direction(self, pred, actual):
        """比较方向是否一致"""
        # 情绪方向映射
        emotion_positive = ['修复', '高潮', '回暖', '反弹']
        emotion_negative = ['退潮', '冰点', '下跌', '调整']
        
        # 策略方向映射
        strategy_positive = ['涨', '强', '多', '买', '进攻', '重仓']
        strategy_negative = ['跌', '弱', '空', '卖', '防守', '轻仓', '看戏']
        
        # 检查情绪方向
        pred_emotion_pos = any(w in pred for w in emotion_positive)
        pred_emotion_neg = any(w in pred for w in emotion_negative)
        actual_emotion_pos = any(w in actual for w in emotion_positive)
        actual_emotion_neg = any(w in actual for w in emotion_negative)
        
        # 检查策略方向
        pred_strategy_pos = any(w in pred for w in strategy_positive)
        pred_strategy_neg = any(w in pred for w in strategy_negative)
        actual_strategy_pos = any(w in actual for w in strategy_positive)
        actual_strategy_neg = any(w in actual for w in strategy_negative)
        
        # 情绪方向一致
        if pred_emotion_pos and actual_emotion_pos:
            return True
        if pred_emotion_neg and actual_emotion_neg:
            return True
        
        # 策略方向一致
        if pred_strategy_pos and actual_strategy_pos:
            return True
        if pred_strategy_neg and actual_strategy_neg:
            return True
        
        # 完全匹配
        return pred == actual
    
    def get_accuracy(self, category=None, days=7):
        """获取准确率"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        filtered = [
            p for p in self.data['predictions']
            if p['verified'] and datetime.fromisoformat(p['time']) >= cutoff
        ]
        
        if category:
            filtered = [p for p in filtered if p['category'] == category]
        
        if not filtered:
            return None
        
        correct = [p for p in filtered if p['correct']]
        return len(correct) / len(filtered)
    
    def get_report(self, days=7):
        """生成报告"""
        accuracy_total = self.get_accuracy(days=days)
        accuracy_emotion = self.get_accuracy(category='情绪', days=days)
        accuracy_strategy = self.get_accuracy(category='策略', days=days)
        accuracy_risk = self.get_accuracy(category='风险', days=days)
        
        report = f"""# 准确率报告 (最近{days}天)

## 总体准确率
- 总预测数: {self.data['stats']['total']}
- 已验证数: {self.data['stats']['verified']}
- 正确数: {self.data['stats']['correct']}
- 准确率: {accuracy_total*100:.1f}% (如有)

## 分类准确率
| 类别 | 准确率 |
|------|--------|
| 情绪判断 | {accuracy_emotion*100:.1f}% (如有) |
| 策略方向 | {accuracy_strategy*100:.1f}% (如有) |
| 风险预警 | {accuracy_risk*100:.1f}% (如有) |

## 最近预测
"""
        # 最近5条预测
        recent = self.data['predictions'][-5:]
        for p in recent:
            status = "✅" if p.get('correct') else ("❌" if p['verified'] else "⏳")
            report += f"- {status} [{p['category']}] {p['prediction'][:30]}...\n"
        
        return report


# 使用示例
if __name__ == "__main__":
    tracker = AccuracyTracker()
    
    # 记录今日预测
    print("=== 今日预测记录 ===")
    
    # 情绪判断
    id1 = tracker.record_prediction('情绪', '退潮→冰点', confidence=0.6)
    print(f"记录情绪预测 ID: {id1}")
    
    # 策略方向
    id2 = tracker.record_prediction('策略', '防守看戏，轻仓试错', confidence=0.7)
    print(f"记录策略预测 ID: {id2}")
    
    # 风险预警
    id3 = tracker.record_prediction('风险', '化工板块补跌', confidence=0.8)
    print(f"记录风险预测 ID: {id3}")
    
    # 验证预测
    print("\n=== 验证预测 ===")
    tracker.verify_prediction(id1, '修复')  # 实际是修复，预测冰点，错误
    tracker.verify_prediction(id2, '防守正确')  # 策略正确
    tracker.verify_prediction(id3, '化工补跌')  # 风险预警正确
    
    # 生成报告
    print("\n" + tracker.get_report(days=1))

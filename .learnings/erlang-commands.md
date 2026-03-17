# 二郎命令系统 (Erlang Commands)

> 基于 Garry Tan gstack 工作流理念
> 创建时间: 2026-03-17 23:50

---

## 命令总览

| 命令 | 用途 | 执行时机 |
|------|------|----------|
| `/erlang-pre-market` | 盘前策略规划 | 09:00 |
| `/erlang-auction` | 竞价分析 | 09:30 |
| `/erlang-noon-check` | 午盘校准 | 11:30 |
| `/erlang-review` | 收盘复盘 | 15:00 |
| `/erlang-scoring` | 策略打分 | 19:00 |
| `/erlang-maintenance` | 系统维护 | 23:00 |
| `/erlang-reflect` | 每日省察 | 22:00 |

---

## /erlang-pre-market (盘前策略规划)

**执行时机**: 每日 09:00

**输入**:
- 隔夜全球市场数据
- 昨日A股收盘数据
- 隔夜新闻资讯

**输出**:
- 情绪水位定性
- 初步策略方向
- 重点关注标的

**流程**:
1. 扫描隔夜美股、亚太、商品
2. 获取昨日涨停股、连板梯队
3. 过滤隔夜消息（S/A/B级）
4. 生成情绪判断
5. 输出盘前预热报告

**数据源优先级**:
- 行情: AKShare → 新浪财经 → InStreet
- 新闻: 讯飞搜索 → 财联社 → 华尔街见闻

---

## /erlang-auction (竞价分析)

**执行时机**: 每日 09:30

**输入**:
- 09:25-09:30 集合竞价数据
- 最高连板股竞价表现
- 板块竞价强度

**输出**:
- 竞价红绿灯
- 策略修正
- 开盘关注点

**流程**:
1. 获取竞价最终数据
2. 分析核心股竞价表现
3. 检测板块竞价强度
4. 识别竞价异常
5. 修正盘前预判

---

## /erlang-noon-check (午盘校准)

**执行时机**: 每日 11:30

**输入**:
- 早盘行情数据
- 持仓股表现
- 午间新闻

**输出**:
- 预判vs实际对比
- 下午操作纪律
- 持仓体检结果

**流程**:
1. 对比早盘预判vs实际
2. 确认上午成交额TOP3板块
3. 检测主线强度
4. 持仓量价背离检测
5. 输出午盘校准报告

---

## /erlang-review (收盘复盘)

**执行时机**: 每日 15:00

**输入**:
- 全天行情数据
- 龙虎榜数据（17:00后）
- 收盘新闻

**输出**:
- 全天情绪清算
- 游资机构动向
- 次日关注标的

**流程**:
1. 全天情绪清算
2. 获取龙虎榜数据
3. 拆解游资/机构动向
4. 验证早盘预判准确率
5. 锁定次日主线

---

## /erlang-scoring (策略打分)

**执行时机**: 每日 19:00

**输入**:
- 今日所有决策
- 实际市场表现
- 准确率追踪数据

**输出**:
- 决策准确率
- 错误归因分析
- 改进建议

**流程**:
1. 汇总今日所有预测
2. 验证预测结果
3. 计算准确率
4. 分析错误原因
5. 生成改进建议

---

## /erlang-maintenance (系统维护)

**执行时机**: 每日 23:00

**输入**:
- 今日所有文件变更
- 学习日志
- 记忆文件

**输出**:
- 备份文件
- Git提交
- 同步到GitHub

**流程**:
1. 打包核心配置文件
2. 打包记忆文件
3. 打包学习日志
4. Git提交
5. 推送到GitHub

---

## /erlang-reflect (每日省察)

**执行时机**: 每日 22:00

**输入**:
- 今日所有决策
- 数据使用情况
- 学习收获

**输出**:
- 每日省察报告
- 自我评分
- 明日改进

**流程**:
1. 回顾今日关键决策
2. 分析决策准确率
3. 审查数据准确性
4. 总结学习收获
5. 制定明日改进

---

## 命令执行规范

### 数据验证
每次命令执行前，必须验证数据源：
```python
from data_validator import DataValidator
validator = DataValidator()
result = validator.validate_source("akshare")
if not result.passed:
    # 使用备用数据源
    pass
```

### 准确率追踪
每次预测必须记录：
```python
from accuracy_tracker import AccuracyTracker
tracker = AccuracyTracker()
prediction_id = tracker.record_prediction('情绪', '修复', confidence=0.7)
# 验证时
tracker.verify_prediction(prediction_id, '实际结果')
```

### 策略测试
策略变更前必须测试：
```python
from strategy_tester import StrategyTester
tester = StrategyTester()
results = tester.run_all_tests()
if results['success_rate'] < 0.8:
    # 策略测试未通过，需要优化
    pass
```

---

## 命令输出格式

所有命令输出遵循以下格式：

```markdown
🎯 二郎[命令名] [日期] [时间]

【核心结论】
一句话总结

【详细分析】
...

【操作建议】
...

【风险提示】
...
```

---

*创建时间: 2026-03-17 23:50*
*目标: 标准化二郎工作流程*

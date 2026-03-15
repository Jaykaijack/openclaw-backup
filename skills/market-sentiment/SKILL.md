---
name: market-sentiment
description: "市场情绪分析 - 分析A股市场情绪指标，包括涨跌家数、涨停跌停、成交量、资金流向等。Use when: 需要判断市场情绪、寻找转折点、辅助决策。"
metadata:
  version: "1.0.0"
  author: "二郎"
---

# 市场情绪分析技能

## 功能

- 涨跌家数统计
- 涨停跌停分析
- 成交量分析
- 资金流向追踪
- 情绪指标计算

## 情绪指标

### 1. 涨跌比
```
涨跌比 = 上涨家数 / 下跌家数
> 2: 极度乐观
1-2: 乐观
0.5-1: 中性
< 0.5: 悲观
```

### 2. 涨停家数
```
> 100家: 情绪高涨
50-100家: 情绪积极
20-50家: 情绪平稳
< 20家: 情绪低迷
```

### 3. 资金流向
```
北向资金净流入 > 50亿: 外资看好
北向资金净流出 > 50亿: 外资看空
```

## 使用方法

```python
from scripts.market_sentiment import MarketSentiment

sentiment = MarketSentiment()
report = sentiment.get_daily_report()
print(report)
```

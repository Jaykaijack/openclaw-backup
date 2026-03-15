#!/usr/bin/env python3
"""
每日股票复盘模板
"""

from datetime import datetime

class DailyReview:
    """每日复盘"""
    
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
    
    def generate_template(self):
        """生成复盘模板"""
        template = f"""
# {self.date} 股票交易复盘

## 一、盘面回顾

### 大盘走势
- 上证指数: 
- 深证成指: 
- 创业板指: 

### 板块热点
1. 
2. 
3. 

### 个股表现
- 涨幅最大: 
- 跌幅最大: 

## 二、操作回顾

### 买入
| 股票 | 价格 | 数量 | 理由 |
|-----|------|------|------|
| | | | |

### 卖出
| 股票 | 价格 | 数量 | 理由 |
|-----|------|------|------|
| | | | |

### 持仓
| 股票 | 成本 | 现价 | 盈亏 | 占比 |
|-----|------|------|------|------|
| | | | | |

## 三、盈亏分析

- 当日盈亏: 
- 累计盈亏: 
- 胜率: 

## 四、策略评估

### 执行情况
- 是否按计划操作: 
- 偏离原因: 

### 得失分析
- 做得好的: 
- 需要改进: 

## 五、明日计划

### 目标股票
1. 
2. 

### 操作计划
- 买入: 
- 卖出: 
- 持有: 

### 风险控制
- 止损位: 
- 仓位控制: 

---
复盘时间: {datetime.now().strftime("%H:%M")}
"""
        return template

if __name__ == '__main__':
    review = DailyReview()
    print(review.generate_template())

---
name: akshare
description: "Akshare财经数据接口 - 获取A股、港股、美股、期货、基金等全市场数据。无需注册，完全免费。Use when: 需要股票行情、财务数据、宏观经济数据、期货数据等。"
metadata:
  version: "1.0.0"
  author: "二郎"
---

# Akshare 财经数据技能

## 功能

- A股实时行情和历史数据
- 港股、美股数据
- 期货、期权数据
- 基金、债券数据
- 宏观经济数据
- 新闻舆情数据

## 使用方法

```python
import akshare as ak

# A股实时行情
stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()

# 个股历史数据
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20240101", end_date="20241231", adjust="qfq")

# 龙虎榜数据
stock_lhb_detail_daily_sina_df = ak.stock_lhb_detail_daily_sina(start_date="20240101", end_date="20240131")
```

## 安装

```bash
pip install akshare
```

## 数据源

- 东方财富
- 新浪财经
- 腾讯财经
- 网易财经

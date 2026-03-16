# 技能快速调用指南

> 每次生成报告时，必须先调用相应技能获取数据

---

## 📊 技能调用速查表

### 1. xfyun-search（讯飞万搜）
**用途**：搜索新闻、资讯、政策
```bash
python3 ~/.openclaw/workspace/skills/xfyun-search/scripts/search.py "搜索关键词" --limit 10
```

### 2. akshare（A股数据）
**用途**：获取行情、涨跌停、连板数据
```bash
# 查看可用脚本
ls ~/.openclaw/workspace/skills/akshare/scripts/
```

### 3. market-sentiment（市场情绪）
**用途**：分析市场情绪指标
```bash
ls ~/.openclaw/workspace/skills/market-sentiment/scripts/
```

### 4. stock-research（股票研究）
**用途**：多维度股票分析
```bash
ls ~/.openclaw/workspace/skills/stock-research/scripts/
```

### 5. stock-review（股票复盘）
**用途**：每日交易复盘
```bash
ls ~/.openclaw/workspace/skills/stock-review/scripts/
```

### 6. hot-finder（热点雷达）
**用途**：多源热门内容搜索
```bash
ls ~/.openclaw/workspace/skills/hot-finder/scripts/
```

### 7. industry-report（行业研报）
**用途**：生成专业行业研究报告
```bash
ls ~/.openclaw/workspace/skills/industry-report/scripts/
```

### 8. news-report（资讯报告）
**用途**：聚合资讯生成报告
```bash
ls ~/.openclaw/workspace/skills/news-report/scripts/
```

### 9. tushare-data（Tushare数据）
**用途**：专业财经数据库
```bash
ls ~/.openclaw/workspace/skills/tushare-data/scripts/
```

---

## 🎯 报告生成流程

### 盘前预热（09:00）
```
1. xfyun-search → 搜索隔夜新闻
2. akshare → 获取涨跌停数据
3. 整合数据 → 生成报告
```

### 竞价分析（09:30）
```
1. akshare → 获取竞价数据
2. market-sentiment → 分析情绪
3. 整合数据 → 生成报告
```

### 午盘校准（11:30）
```
1. akshare → 获取实时行情
2. stock-research → 分析持仓
3. xfyun-search → 搜索午间新闻
4. 整合数据 → 生成报告
```

### 收盘复盘（15:00）
```
1. akshare → 获取全天数据
2. stock-review → 复盘分析
3. hot-finder → 热点挖掘
4. xfyun-search → 搜索龙虎榜
5. 整合数据 → 生成报告
```

---

## ⚠️ 注意事项

1. **先调技能，后写报告**：不要凭空编造数据
2. **多源验证**：重要数据用多个技能交叉验证
3. **记录来源**：报告中标注数据来源
4. **失败处理**：技能调用失败时，明确告知用户

---

**更新时间**：2026年3月17日 01:20

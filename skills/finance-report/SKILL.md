---
name: finance-report
description: "生成专业级金融行情分析与投研日报HTML页面（深色金融仪表盘风格）。支持六大报告类型：(1) A股盘前速递/收盘总结，(2) 行业专题研报，(3) 大宗商品周报，(4) 宏观经济月报，(5) 全球市场联动分析，(6) 自定义金融主题研报。触发词：投研日报、A股日报、股市报告、finance report、每日行情、盘前分析、收盘总结、行业研报、金融分析、商品周报、宏观月报、market analysis。自动采集A股/港股/美股/欧洲/商品/外汇行情数据，抓取财联社电报等新闻源，生成1280px宽暗色主题HTML文件并直接发送。"
---

# 金融行情分析 · 投研日报生成器

生成专业级金融研报HTML页面（深色仪表盘风格），覆盖日报/周报/月报/行业专题。

## 快速流程

1. **采集行情** — `python3 scripts/fetch_market.py` → JSON（A股10+港股3+美股3+欧洲3+商品8+外汇4）
2. **抓取新闻** — `web_fetch https://www.cls.cn/telegraph maxChars=15000`（财联社电报）
3. **补充数据** — `web_search`/`web_fetch` 获取板块、个股、行业专题数据（按需）
4. **生成HTML** — 参照 `assets/template.html` 样式 + `references/design-guide.md` 组件规范
5. **发送HTML文件** — 直接将生成的 `.html` 文件发送给用户

详细工作流见 `references/workflow.md`，组件与配色规范见 `references/design-guide.md`。

## 报告类型

| 类型 | 触发条件 | 核心模块 |
|------|----------|----------|
| 盘前速递 | 09:15前/"盘前" | 隔夜全球+竞价+今日看点 |
| 收盘总结 | 15:00后/"收盘" | 全日行情+涨跌停+龙虎榜+策略 |
| 行业专题 | "XX行业研报" | 产业链+竞争+估值+趋势 |
| 商品周报 | "商品周报" | 商品周线+宏观驱动+持仓 |
| 宏观月报 | "宏观月报" | 经济数据+政策+利率汇率 |
| 自定义 | 指定主题 | 灵活组合模块库 |

## 数据采集

```bash
python3 scripts/fetch_market.py > /tmp/market_data.json
```

新闻来源优先级:
1. `web_fetch https://www.cls.cn/telegraph` — 财联社电报
2. `web_fetch https://finance.eastmoney.com/` — 东方财富
3. `python3 scripts/fetch_news.py` — 备用
4. `web_search` — 专题补充

## HTML生成要点

- 参考 `assets/template.html` 获取完整CSS + 布局骨架
- **1280px宽，暗色主题，红涨绿跌**
- 中文: PingFang SC / Microsoft YaHei，数字: Menlo / Courier New
- ❌ 不用 Google Fonts / CSS动画 / 外部图片
- 组件详细用法见 `references/design-guide.md`

**模块库**（按需选用，详见 `references/workflow.md`）:
- 必选: Hero头部 + 免责声明Footer
- 行情: 指数卡片(grid) + 全球市场 + 商品期货 + 外汇
- 分析: 板块排行 + 涨跌停 + 资金流向 + 龙虎榜
- 资讯: 新闻快讯 + 事件追踪 + 紧急告警
- 策略: 观点总结 + 风险提示 + 关注标的
- 专题: 产业链图 + 竞争格局 + 估值分析 + KPI仪表盘 + 时间线

## 输出

- 生成HTML文件: `finance_daily_MMDD.html` / `industry_{topic}_MMDD.html` / `commodity_weekly_MMDD.html`
- 保存到工作目录

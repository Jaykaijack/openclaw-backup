---
name: stock-research
description: "Multi-agent stock/company research analysis system. Activate when user asks to analyze a stock (A-share, HK, US), research a company, compare stocks, evaluate investment value, generate stock research reports, or build research dashboards. Triggers: stock analysis, company research, 股票分析, 个股研究, 上市公司分析, 投研报告, 行业对比, 估值分析, research report, fundamental analysis, 看涨看跌分析. Supports parallel sub-agent orchestration for deep multi-dimensional analysis."
---

# Stock Research — Multi-Agent Analysis System

Orchestrate a team of specialized sub-agents to produce professional-grade company research reports with interactive dashboards.

## Architecture

```
Chief Analyst (you)
├── fundamentals_analyst  — Financial statements, valuation, profitability
├── news_analyst          — Company news, policy, management changes
├── sentiment_analyst     — Market sentiment, analyst ratings, fund flows
├── technical_analyst     — Price trends, volume, key levels
├── bullish_researcher    — Growth thesis, competitive moat, upside catalysts
├── bearish_researcher    — Risk identification, downside scenarios
├── risk_manager          — Comprehensive risk assessment
└── fact_checker          — Data verification, cross-reference
```

## Workflow

### Phase 1: Parallel Data Collection

Spawn 4 sub-agents simultaneously:

```
sessions_spawn(task="[fundamentals_analyst] {ROLE_PROMPT}\n\nAnalyze: {STOCK}", label="fundamentals")
sessions_spawn(task="[news_analyst] {ROLE_PROMPT}\n\nAnalyze: {STOCK}", label="news")
sessions_spawn(task="[sentiment_analyst] {ROLE_PROMPT}\n\nAnalyze: {STOCK}", label="sentiment")
sessions_spawn(task="[technical_analyst] {ROLE_PROMPT}\n\nAnalyze: {STOCK}", label="technical")
```

Each sub-agent task prompt MUST include the full role description from `references/agent-roles.md`.

**Wait for all 4 to complete** (they will auto-announce results).

### Phase 2: Bull/Bear Debate

After Phase 1 completes, spawn 2 sub-agents with Phase 1 results:

```
sessions_spawn(task="[bullish_researcher] {ROLE_PROMPT}\n\nBased on:\n{PHASE1_RESULTS}\n\nBuild bull case for {STOCK}", label="bull")
sessions_spawn(task="[bearish_researcher] {ROLE_PROMPT}\n\nBased on:\n{PHASE1_RESULTS}\n\nBuild bear case for {STOCK}", label="bear")
```

### Phase 3: Risk Assessment

```
sessions_spawn(task="[risk_manager] {ROLE_PROMPT}\n\nAssess risks for {STOCK} based on:\n{ALL_RESULTS}", label="risk")
```

### Phase 4: Fact Check

```
sessions_spawn(task="[fact_checker] Verify key data points and claims:\n{KEY_CLAIMS}", label="factcheck")
```

### Phase 5: Compile Report

Synthesize all sub-agent results into the report format defined in `references/report-format.md`.

### Phase 6: Generate Dashboard

Build an interactive HTML dashboard following `references/dashboard-spec.md`. Deploy if deploy tool available.

## Data Sources

### A-Share / HK — akshare

```python
import akshare as ak
stock_info = ak.stock_individual_info_em(symbol="600519")
balance = ak.stock_balance_sheet_by_report_em(symbol="600519")
income = ak.stock_profit_sheet_by_report_em(symbol="600519")
cashflow = ak.stock_cash_flow_sheet_by_report_em(symbol="600519")
indicators = ak.stock_financial_analysis_indicator(symbol="600519")
fund_hold = ak.stock_report_fund_hold(symbol="600519")
hk_hist = ak.stock_hk_hist(symbol="00700", period="daily", adjust="qfq")
```

### US Stocks — yfinance

```python
import yfinance as yf
stock = yf.Ticker("AAPL")
info, financials = stock.info, stock.financials
```

### Supplementary
- Web search: analyst reports, target prices, earnings forecasts
- Eastmoney / Tonghuashun: ratings, research summaries
- Company announcements: earnings releases, material events

## Quick Modes

| User Request | Agents Used | Output |
|---|---|---|
| Full research | All 8 agents | Complete report + dashboard |
| Financial analysis only | fundamentals | Financial section only |
| Quick overview | fundamentals + news | Summary report |
| Industry comparison | Multiple full runs | Comparison table |

## Key Rules

1. **Financial depth first** — Statements are the core
2. **Cite institutions** — Analyst reports, target prices, consensus
3. **Identify moats** — Competitive advantages, industry position
4. **Flag risks clearly** — Earnings risk, industry risk, policy risk
5. **Stay objective** — Present facts, not speculation
6. **Disclaimer required** — Always include AI-generated disclaimer

## Reference Files

- `references/agent-roles.md` — Detailed prompts for each sub-agent
- `references/report-format.md` — Output report template
- `references/dashboard-spec.md` — Dashboard HTML design spec

## Platform Constraints

If Gateway restart is needed, do NOT restart yourself. Tell user to click restart in settings, then resume.

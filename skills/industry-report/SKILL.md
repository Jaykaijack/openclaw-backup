---
name: industry-report
description: "Generate professional industry research reports as Word documents (.docx). Use when the user requests an industry report, sector analysis, market research report, or 行业研报/行业研究报告. Produces formatted .docx with cover page, table of contents, KPI cards, data tables, charts, headers/footers, and page numbers. Supports any industry (semiconductor, AI, biotech, energy, etc.). Triggers: industry report, 行业研报, sector report, market research, 研究报告, deep dive report."
---

# Industry Report Generator

Generate professional industry research reports as formatted Word documents (.docx).

## Quick Start

1. Gather data: web_fetch news sources + market data APIs
2. Read the template script: `scripts/gen_report.js`
3. Customize the data config object with industry-specific content
4. Run: `NODE_PATH=$(npm root -g) node scripts/gen_report.js`
5. Validate: `python3 <docx-skill>/scripts/office/validate.py output.docx`
6. Deliver the .docx file

## Workflow

### Step 1: Data Collection

Gather industry data from authoritative sources:
- Market size & growth (Gartner, IDC, SEMI, Statista)
- Company financials (official filings, earnings)
- News & events (财联社, 东方财富, Bloomberg)
- Policy & regulation (government announcements)
- Stock/index data (Sina Finance API, market scripts)

### Step 2: Configure Report Content

Edit the DATA object in `scripts/gen_report.js` or create a wrapper script that requires the generator module. The DATA object structure:

```javascript
const DATA = {
  // Meta
  title: "半导体产业",          // Industry name
  subtitle: "行业研究报告",      // Report type
  date: "2026年3月4日",         // Date
  keywords: "AI芯片 · 存储芯片 · 先进制程", // Keywords
  color: "2563EB",              // Theme color (hex, no #)
  
  // Sections (array of section objects)
  sections: [
    { type: "summary", title: "执行摘要", points: [...] },
    { type: "kpi", title: "核心指标", items: [...] },
    { type: "table", title: "市场规模", headers: [...], rows: [...] },
    { type: "chain", title: "产业链", layers: [...] },
    { type: "news", title: "重要资讯", items: [...] },
    { type: "strategy", title: "投资建议", items: [...] },
    { type: "risk", title: "风险因素", headers: [...], rows: [...] },
  ]
};
```

See `references/data-schema.md` for the complete DATA schema with all section types.

### Step 3: Generate & Deliver

```bash
NODE_PATH=$(npm root -g) node scripts/gen_report.js
```

Output: `{title}_report_{YYYYMMDD}.docx` in current working directory.

### Step 4: Validate

```bash
python3 <docx-skill-path>/scripts/office/validate.py output.docx
```

## Report Structure (10 Sections)

Standard industry report template (customize per industry):

1. **封面** — Title, date, keywords, disclaimer
2. **目录** — Auto-generated TOC
3. **执行摘要** — KPI cards + 5 key findings
4. **市场规模** — Size & growth data tables
5. **产业链分析** — Three-layer chain diagram
6. **核心驱动力** — Key growth driver deep-dive
7. **竞争格局** — Company comparison tables
8. **政策环境** — Policy & regulation overview
9. **风险因素** — Risk assessment table
10. **投资建议** — Strategy + allocation + risk warnings

## Design Specs

- **Page**: A4, 1-inch margins
- **Fonts**: Microsoft YaHei (body), Menlo (numbers)
- **Tables**: Blue header row (#1E3A5F), light gray alternating rows
- **KPI Cards**: Colored top-border, centered value with monospace font
- **Colors**: Configurable theme color; default blue (#2563EB)
  - Up/positive: red (#DC2626) — Chinese market convention
  - Down/negative: green (#059669)
- **Header**: Report title right-aligned, blue underline
- **Footer**: Date left, page number right

## Customization

To adapt for different industries, modify:
- `DATA.color` — Theme color (e.g., green for biotech, gold for finance)
- `DATA.sections` — Add/remove/reorder sections as needed
- Table column widths in section configs
- KPI card colors and labels

## Dependencies

- `docx` npm package (`npm install -g docx`)
- Node.js 18+
- `NODE_PATH=$(npm root -g)` required when running scripts

# Data Schema Reference

## Top-Level Structure

```javascript
const DATA = {
  title: String,        // Industry name (e.g., "半导体产业")
  subtitle: String,     // Report type (default: "行业研究报告")
  date: String,         // Report date (e.g., "2026年3月4日")
  keywords: String,     // Keywords separated by " · "
  disclaimer: String,   // Footer disclaimer text
  sources: String,      // Data sources line
  color: String,        // Theme color hex without # (default: "2563EB")
  sections: Section[]   // Array of section objects
};
```

## Section Types

### type: "summary"
Executive summary with bold-title paragraphs.
```javascript
{ type: "summary", title: "执行摘要", points: [
  { label: "要点一：标题", text: "详细描述..." },
  { label: "要点二：标题", text: "详细描述..." },
]}
```

### type: "kpi"
KPI metric cards in a 3-column table row. Multiple rows supported.
```javascript
{ type: "kpi", title: "核心指标", rows: [
  // Each row has 3 items
  [
    { label: "市场规模", value: "$7,800亿", sub: "2026E", bg: "DBEAFE", color: "2563EB" },
    { label: "AI芯片", value: "$1,350亿", sub: "+46.7%", bg: "FEE2E2", color: "DC2626" },
    { label: "大基金", value: "¥3,440亿", sub: "史上最大", bg: "EDE9FE", color: "7C3AED" },
  ],
]}
```

### type: "table"
Data table with header row and data rows.
```javascript
{ type: "table", title: "市场规模", 
  columns: [
    { header: "细分市场", width: 2100 },
    { header: "2025年", width: 1400, mono: true },
    { header: "2026年E", width: 1400, mono: true },
  ],
  rows: [
    ["全球半导体", "$6,800亿", "$7,800亿"],
    ["AI芯片", "$920亿", "$1,350亿"],
  ],
  note: "数据来源：SEMI、Gartner"  // optional footer note
}
```

### type: "chain"
Industry chain layers (typically 3: upstream, midstream, downstream).
```javascript
{ type: "chain", title: "产业链", layers: [
  { name: "🔵 上游：设备/材料", color: "2563EB", items: [
    { label: "EDA", detail: "Synopsys · Cadence · 华大九天" },
    { label: "设备", detail: "ASML · 北方华创 · 中微公司" },
  ]},
  { name: "🟢 中游：设计/制造", color: "0891B2", items: [...] },
  { name: "🟣 下游：应用", color: "7C3AED", items: [...] },
]}
```

### type: "news"
News/events list with colored tags.
```javascript
{ type: "news", title: "重要资讯", items: [
  { tag: "AI芯片", tagColor: "2563EB", tagBg: "DBEAFE",
    headline: "NVIDIA营收超预期", detail: "FY2026 Q1..." },
]}
```

### type: "strategy"
Investment strategy bullet points.
```javascript
{ type: "strategy", title: "投资建议", items: [
  { label: "方向一：AI算力芯片", text: "确定性最高..." },
  { label: "配置建议", text: "总仓位15-25%..." },
]}
```

### type: "risk"
Risk factor table (same as "table" type but typically with colored impact column).
```javascript
{ type: "risk", title: "风险因素",
  columns: [
    { header: "风险类型", width: 2000 },
    { header: "具体内容", width: 5000 },
    { header: "影响程度", width: 2026, colorMap: { "高": "DC2626", "中": "D97706", "低": "059669" } },
  ],
  rows: [
    ["地缘政治", "中美科技脱钩深化", "高"],
  ]
}
```

### type: "text"
Free-form paragraph text.
```javascript
{ type: "text", title: "市场概述", content: "全球半导体产业正处于..." }
```

### type: "bullets"
Bullet point list.
```javascript
{ type: "bullets", title: "对华出口管制", items: [
  "GPU禁运：H100/A100/B200系列对华禁售",
  "光刻机限制：ASML EUV禁止出口中国",
]}
```

## Column Width Reference (A4, 1-inch margins)

Total content width: **9,026 DXA** (1 DXA = 1/1440 inch)

Common layouts:
- 2 columns: 4513 + 4513
- 3 columns: 3008 + 3009 + 3009
- 7 columns: varies, sum must = 9026

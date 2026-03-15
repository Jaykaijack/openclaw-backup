# Dashboard Specification

## Design Requirements

### Visual Style
- Background: black `#0a0a0a` (default) or white `#ffffff`
- **No blue-purple color schemes**
- Notion-inspired minimalist aesthetic
- Professional trader feel: clean, data-first
- Chinese market convention: red = up, green = down

### Typography
- Chinese: PingFang SC / Microsoft YaHei
- Numbers: Menlo / Courier New (monospaced)
- No Google Fonts or external font CDNs

### Layout (1280px width)
```
┌─────────────────────────────────────────────┐
│  Header: Company Name + Code + Price Badge  │
├──────────┬──────────────────────────────────┤
│ Sidebar  │  Main Content Area               │
│ - Search │  ┌────────────────────────────┐  │
│ - Nav    │  │  KPI Cards (4-col grid)    │  │
│          │  │  Revenue | Profit | ROE    │  │
│          │  │  | PE | PB | Rating        │  │
│          │  ├────────────────────────────┤  │
│          │  │  Valuation Chart           │  │
│          │  │  (PE/PB historical)        │  │
│          │  ├────────────────────────────┤  │
│          │  │  Risk Radar Chart          │  │
│          │  ├────────────────────────────┤  │
│          │  │  Bull/Bear Arguments       │  │
│          │  ├────────────────────────────┤  │
│          │  │  Fact Check Results        │  │
│          │  ├────────────────────────────┤  │
│          │  │  Investment Rating Card    │  │
│          │  └────────────────────────────┘  │
└──────────┴──────────────────────────────────┘
```

## Functional Modules

### 1. Header
- Company name (Chinese + English if available)
- Stock code with market identifier
- Current price with change badge (red/green)
- Report generation timestamp

### 2. KPI Cards (grid)
- Revenue (with YoY %)
- Net Profit (with YoY %)
- Gross Margin %
- ROE %
- PE-TTM (with historical percentile bar)
- PB (with historical percentile bar)
- Analyst Rating distribution (mini bar chart)

### 3. Valuation Section
- PE/PB historical chart (use Chart.js)
- Current position marker on chart
- Industry average comparison line

### 4. Risk Radar Chart
- 5-axis radar: Business / Financial / Valuation / Market / Event
- Score 1-5 per axis
- Overall risk level badge

### 5. Bull/Bear Section
- Two-column layout
- Green left (bull), Red right (bear)
- Numbered arguments with conviction indicators

### 6. Fact Check Panel
- Verified ✅ / Unverified ⚠️ / Corrected ❌ items
- Collapsible detail view

### 7. Investment Rating
- Large rating badge: 🟢 High / 🟡 Medium / 🔴 Low
- Core logic summary
- Suggested position size

## Technical Implementation

```html
<!-- Single HTML file, no external dependencies except Chart.js CDN -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Company} Research Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
  <style>
    /* All CSS inline - dark theme, no animations, no Google Fonts */
    :root {
      --bg: #0a0a0a;
      --card: #141414;
      --border: #222;
      --text: #e0e0e0;
      --muted: #888;
      --up: #ef4444;    /* red = up */
      --down: #22c55e;  /* green = down */
      --accent: #f59e0b;
    }
  </style>
</head>
```

### Chart.js Usage
- Line chart for price/valuation history
- Radar chart for risk assessment
- Bar chart for analyst ratings
- Keep charts simple and readable

### Responsive
- Min-width: 1024px (desktop-focused)
- Sidebar collapses on smaller screens

## No-Fly Rules
- No CSS animations or transitions
- No external images
- No Google Fonts
- No blue-purple gradients
- Chart.js CDN is the ONLY external resource allowed

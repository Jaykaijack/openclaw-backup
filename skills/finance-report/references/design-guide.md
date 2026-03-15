# 金融研报 HTML 设计指南

## 色彩体系

### 主色
| 变量 | 色值 | 用途 |
|------|------|------|
| --bg-deep | #0a0e1a | 页面背景 |
| --bg-card | #111827 | 卡片背景 |
| --bg-card-alt | #1a2332 | 卡片背景（交替） |
| --accent-red | #ff4757 | 涨/警告/紧急 |
| --accent-green | #2ed573 | 跌/安全/正面 |
| --accent-gold | #ffa502 | 重点/策略/金融 |
| --accent-blue | #3742fa | 信息/科技 |
| --accent-cyan | #00d2d3 | 实时/数据 |
| --accent-purple | #a855f7 | 行业/创新 |
| --text-primary | #f1f2f6 | 主文字 |
| --text-secondary | #a4b0be | 次要文字 |
| --text-dim | #57606f | 暗淡文字 |
| --border | rgba(255,255,255,0.06) | 边框分隔线 |

### 行业配色映射
- 能源/石油: gold + red
- 贵金属: gold + #ffd700
- 科技/AI: blue + cyan
- 医药: green + cyan
- 金融/银行: blue + gold
- 消费: purple + green
- 地产: red + blue
- 军工: red + blue

## 组件规范

### 指数卡片 (.idx-card)
```html
<div class="idx-card up">
  <div class="idx-name">上证指数</div>
  <div class="idx-val up">3,234.56</div>
  <div class="idx-chg up">+45.23 (+1.42%)</div>
  <span class="idx-tag live">实时</span>
</div>
```
- 涨: class="up", 底部渐变红色
- 跌: class="down", 底部渐变绿色
- 平: class="flat"

### 商品期货卡片 (.fut-card)
```html
<div class="fut-card">
  <div class="fut-label">COMEX黄金</div>
  <div class="fut-val up">2,345.60</div>
  <div class="fut-chg up">+1.25%</div>
</div>
```

### 新闻条目 (.news-item)
```html
<div class="news-item">
  <span class="news-tag red">政策</span>
  <div class="news-content"><strong>央行</strong>宣布降准0.5个百分点</div>
</div>
```
标签颜色: red=政策/紧急, gold=行业, blue=公司, green=利好, cyan=数据

### 数据表格 (.data-table)
- th: 大写字母, 暗色, 底部分隔线
- td: 数值右对齐, 数字用.mono类
- 涨跌用.up/.down着色

### 策略卡片 (.strategy-card)
- 背景渐变, 左侧金色强调
- 列表项用金色圆点标记

### 告警横幅 (.alert-banner)
- 仅在重大事件(跌>3%, 黑天鹅等)时使用
- 红色半透明背景 + 图标 + 粗体文字

### 标签/芯片 (.chip)
```html
<span class="chip chip-fire">🔥 热门</span>
<span class="chip chip-gold">⚡ 异动</span>
<span class="chip chip-limit">涨停</span>
```
类型: chip-fire/chip-oil/chip-gold/chip-cold/chip-blue/chip-cyan/chip-limit

### 情绪指标 (.sentiment-wrap)
```html
<div class="sentiment-wrap">
  <div class="sentiment-meta">
    <span>上涨: 2,456 (56%)</span><span>下跌: 1,944 (44%)</span>
  </div>
  <div class="sentiment-bar">
    <div class="bar-up" style="width:56%"></div>
    <div class="bar-down" style="width:44%"></div>
  </div>
</div>
```

## 响应式网格

所有grid布局在1280px宽度下固定，不做响应式。
使用gap:12px（紧凑）或gap:20px（宽松）。

## 字体规范

- 标题: PingFang SC, 700-900 weight
- 正文: PingFang SC, 400 weight
- 数字: Menlo, Courier New (等宽)
- 数字大小: 卡片主数字24px, 辅助13px, 表格13px
- 行高: 正文1.7, 标题1.3

## SVG图表指南

当需要简单趋势图时，用内联SVG：
```html
<svg viewBox="0 0 100 30" style="width:100px;height:30px">
  <polyline points="0,25 20,20 40,15 60,18 80,10 100,5"
    fill="none" stroke="#ff4757" stroke-width="1.5"/>
</svg>
```
- 涨趋势: stroke=#ff4757
- 跌趋势: stroke=#2ed573
- 宽度100px, 高度30px, 放在卡片角落

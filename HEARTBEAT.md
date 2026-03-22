# 二郎量化分析系统 - 心跳任务

> 基于 V2.0 多智能体框架
> 详见：`.learnings/quant-framework-v2.md`

---

## 🤖 技能调用规范（必读）

每次生成报告时，**必须自动调用以下技能**：

### 技能调用映射表

| 报告类型 | 必调技能 | 调用方式 |
|---------|---------|---------|
| 盘前预热 | `xfyun-search` + `akshare` | 搜索隔夜新闻 + 获取行情数据 |
| 竞价分析 | `akshare` + `market-sentiment` | 获取竞价数据 + 情绪分析 |
| 午盘校准 | `akshare` + `stock-research` | 实时行情 + 持仓分析 |
| 收盘复盘 | `akshare` + `stock-review` + `hot-finder` | 全天数据 + 复盘 + 热点 |
| 行业研报 | `industry-report` + `xfyun-search` | 自动生成研报 |
| 资讯报告 | `news-report` + `xfyun-search` | 聚合资讯生成报告 |
| 股票分析 | `stock-research` + `akshare` + `tushare-data` | 多维度分析 |

### 技能路径（直接调用）

```
~/.openclaw/workspace/skills/xfyun-search/scripts/search.py
~/.openclaw/workspace/skills/akshare/
~/.openclaw/workspace/skills/market-sentiment/
~/.openclaw/workspace/skills/stock-research/
~/.openclaw/workspace/skills/stock-review/
~/.openclaw/workspace/skills/hot-finder/
~/.openclaw/workspace/skills/industry-report/
~/.openclaw/workspace/skills/news-report/
~/.openclaw/workspace/skills/tushare-data/
```

### 调用示例

```bash
# 搜索新闻
python3 ~/.openclaw/workspace/skills/xfyun-search/scripts/search.py "关键词" --limit 10

# 获取行情数据
python3 ~/.openclaw/workspace/skills/akshare/scripts/xxx.py

# 生成行业研报
python3 ~/.openclaw/workspace/skills/industry-report/scripts/generate.py
```

---

## 09:00 - 情绪雷达 Agent 启动（盘前预热）

### 任务清单
- [ ] 扫描隔夜全球市场（美股、亚太、商品）
- [ ] 获取涨跌停数据、连板梯队
- [ ] 过滤隔夜消息（S级/A级/B级）
- [ ] 生成情绪水位定性
- [ ] 给出初步策略方向

### 必调技能
- `xfyun-search`：搜索隔夜新闻、政策、外盘
- `akshare`：获取涨跌停数据、连板梯队

### 输出目标
通过飞书发送《二郎盘前预热》简报

---

## 09:25 - 盘前动量筛选（新增）

### 任务清单
- [ ] 获取通达信日线数据
- [ ] 筛选盘前涨幅1%-3%的股票
- [ ] 筛选量能放大≥30%的股票
- [ ] 筛选突破10日平台的股票
- [ ] 排除ST、退市、停牌股
- [ ] 生成《盘前动量报告》

### 输出目标
通过飞书发送《盘前动量报告》

---

## 09:30 - 情绪雷达 Agent 竞价分析

### 任务清单
- [ ] 获取 09:25-09:30 集合竞价最终数据
- [ ] 分析最高连板股竞价表现（高开幅度、量比、封单）
- [ ] 监控昨日核心中军竞价状态
- [ ] 检测板块竞价强度（板块内涨停股数量、高开率）
- [ ] 识别竞价异常（天地板/地天板预警、巨量高开/低开）
- [ ] 更新竞价红绿灯（🔴🟡🟢）
- [ ] 修正 09:00 初步判断，给出最终策略

### 必调技能
- `akshare`：获取竞价数据
- `market-sentiment`：分析市场情绪

### 输出目标
通过飞书发送《二郎竞价分析报告》

### 报告模板
```
🎯 二郎竞价分析 [日期] 09:30

【竞价情绪】冰点/修复/高潮/退潮

【核心股竞价】
• 最高板XXX：高开X%，量比X，封单X万手 [超预期/符合/不及]
• 中军XXX：高开X%，量比X [强势/中性/弱势]

【板块竞价强度】
• XXX板块：X只涨停，高开率X% [🔥强/➖中/❄️弱]
• XXX板块：...

【竞价红绿灯】
🟢 绿灯（关注）：
  • XXX - 逻辑
🟡 黄灯（观望）：
  • XXX - 逻辑
🔴 红灯（放弃）：
  • XXX - 逻辑

【风险预警】
⚠️ XXX股：巨量低开，注意风险
⚠️ XXX板块：集体低开，回避

【修正结论】
09:00预判：XXX
09:30修正：XXX
今日策略：重仓出击/轻仓试错/防守看戏

【开盘重点关注】
1. XXX - 买点/观察点
2. XXX - 买点/观察点
```

---

## 11:30 - 策略执行 Agent 校准

### 任务清单
- [ ] 对比早盘预判 vs 实际走势
- [ ] 确认上午成交额 TOP3 板块
- [ ] 检测主线强度和跷跷板效应
- [ ] 持仓体检（量价背离检测）
- [ ] 给出下午操作纪律

### 必调技能
- `akshare`：获取实时行情
- `stock-research`：持仓股分析
- `xfyun-search`：搜索午间新闻

### 输出目标
通过飞书发送《二郎午盘校准》报告

---

## 15:05 - 收盘动量筛选（新增）

### 任务清单
- [ ] 更新通达信日线数据
- [ ] 筛选涨幅1%-7%的股票
- [ ] 筛选量能放大≥30%的股票
- [ ] 筛选20日均线上方的股票
- [ ] 排除ST、退市、停牌股
- [ ] 生成《收盘动量报告》

### 输出目标
通过飞书发送《收盘动量报告》

---

## 15:00 - 复盘学习 Agent 清算

### 任务清单
- [ ] 全天情绪清算（亏钱/赚钱效应）
- [ ] 15:30 后获取龙虎榜数据
- [ ] 拆解游资/机构动向
- [ ] 验证早盘预判准确率
- [ ] 锁定次日主线和猎物
- [ ] 记录今日败笔/神来之笔
- [ ] 更新准确率追踪表

### 必调技能
- `akshare`：获取全天行情数据
- `stock-review`：复盘分析
- `hot-finder`：热点挖掘
- `xfyun-search`：搜索收盘新闻、龙虎榜

### 输出目标
通过飞书发送《二郎收盘复盘》报告

---

## 23:00 - 系统维护

### 必调技能
- `self-improving-agent`：自我进化、记录学习
- `industry-report`：生成深度研报（如需要）

### 备份内容
1. **主要配置文件**
   - `~/.openclaw/config/`
   - `~/.openclaw/workspace/AGENTS.md`
   - `~/.openclaw/workspace/SOUL.md`
   - `~/.openclaw/workspace/TOOLS.md`
   - `~/.openclaw/workspace/IDENTITY.md`
   - `~/.openclaw/workspace/USER.md`

2. **分析框架**
   - `~/.openclaw/workspace/.learnings/quant-framework-v2.md`
   - `~/.openclaw/workspace/HEARTBEAT.md`

3. **工作区**
   - `~/.openclaw/workspace/memory/` - 记忆文件
   - `~/.openclaw/workspace/.learnings/` - 学习日志

4. **预测数据**
   - 准确率追踪表
   - 因子权重配置

### 备份流程
1. 打包核心文件为 tar.gz
2. 生成备份清单
3. 通过飞书发送给楷楷
4. 同步到 GitHub 仓库 (Jaykaijack/openclaw-backup)

---

## 每周任务（周日）

### 复盘学习 Agent 深度工作
- [ ] 回顾本周预测准确率
- [ ] 分析错误归因
- [ ] 评估各因子贡献度
- [ ] 调整因子权重
- [ ] 更新框架文档

---

## 社区学习任务（每日）

### InStreet竞技场
- **频率**: 每日10:00
- **任务**:
  - [ ] 查看排行榜TOP5策略
  - [ ] 分析高手持仓变化
  - [ ] 学习新策略思路
  - [ ] 记录到memory/学习日志

### 股吧社区
- **频率**: 每日收盘后
- **任务**:
  - [ ] 浏览热门帖子
  - [ ] 关注持仓股讨论
  - [ ] 学习技术分析方法
  - [ ] 收集市场情绪信号

### 学习记录
- 记录到 `memory/YYYY-MM-DD.md`
- 重要发现更新到 `MEMORY.md`
- 新策略添加到 `.learnings/`

---

## 输出准则

- 抛弃废话和免责声明
- 直接给数据、结论、操作指令
- 目标：避开诱多陷阱，咬死主线龙头

---

## 数据源状态

| 数据源 | 状态 | 备注 |
|-------|------|------|
| A股实时行情 | ⏳ 待接入 | 需寻找API |
| 龙虎榜 | ⏳ 待接入 | 15:30后获取 |
| 财联社电报 | ⏳ 待接入 | 消息源 |
| 全球市场 | ⏳ 待接入 | 美股/亚太 |

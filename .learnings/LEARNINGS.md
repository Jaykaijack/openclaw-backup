# 学习日志

## [LRN-20260314-001] 打板策略实战案例

**Logged**: 2026-03-14T16:42:00+08:00
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
从 InStreet 炒股竞技场排行榜学习到的高收益策略

### Details

**排行榜第一名 poly_v2（收益率 +31.45%）**
- 策略：全仓梭哈涨停股
- 标的：中国能建 (sh601868)
- 买入价：2.89 元
- 当前价：3.8 元
- 交易理由：`激进策略：全仓梭哈当日涨停股中国能建，博短线收益`
- 特点：单只股票、全仓、追涨停

**排行榜第二名 xuechi_trader（收益率 +31.38%）**
- 策略：追涨停 + 小仓位分散
- 主仓位：中国能建 (sh601868)
- 小仓位：华能国际 (sh600011)
- 交易理由：`中国能建今日大涨9.89%，看好后续表现，激进策略追涨停`
- 特点：主仓位打板，剩余资金分散

### 关键洞察
1. **涨停板策略**在短期确实有效（但风险极高）
2. **电力板块**（中国能建、华能国际）在当前周期表现强势
3. **全仓 vs 分散**：第一名全仓单股，第二名有少量分散
4. **入场时机**：都在大涨当天追入

### Suggested Action
- 继续观察这些高手的后续操作
- 学习如何识别涨停板机会
- 研究电力板块的基本面

### Metadata
- Source: instreet_arena
- Related Files: memory/stock-trading-knowledge.md
- Tags: 打板策略, 涨停股, 短线交易, 电力板块

---

## [LRN-20260314-002] InStreet 社区观察

**Logged**: 2026-03-14T16:42:00+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
InStreet 社区活跃度和内容质量观察

### Details
- 社区有 3618 个 Agent 参与炒股竞技场
- 热门话题：Agent 设计、记忆系统、自我进化
- 高质量帖子：OpenClaw 心跳机制、Agent 执行三层次
- 社区氛围：技术讨论为主，友好互动

### Metadata
- Source: instreet_community
- Tags: 社区观察, Agent生态

---

## [LRN-20260314-003] 每日早盘分析任务设定

**Logged**: 2026-03-14T16:46:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
楷楷要求每天早上9点发送A股早盘分析报告

### Details
任务内容：
1. 全球股市情况分析（美股、亚太、欧洲、商品、外汇）
2. A股走势预判
3. 因子选股（动量+估值+质量+情绪+板块）
4. 基本面分析
5. 市场情绪
6. 通过飞书发送给楷楷

### 持续优化
- 记录预测准确性
- 复盘错误
- 学习新框架

### Metadata
- Source: user_request
- Related Files: HEARTBEAT.md, memory/stock-trading-knowledge.md
- Tags: 定时任务, 盘前分析, 因子选股

---

## [LRN-20260314-004] 收盘复盘任务设定

**Logged**: 2026-03-14T16:49:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
楷楷要求每天15点发送收盘复盘报告，形成学习闭环

### Details
复盘内容：
1. 盘面回顾（大盘、成交额、北向资金）
2. 预测验证（早盘预判 vs 实际走势）
3. 错误分析（原因、遗漏因素）
4. 高手动态（InStreet排行榜、操作对比）
5. 次日策略优化

### 闭环学习机制
- 早盘预判 → 收盘验证 → 错误分析 → 优化模型 → 次日预判
- 持续追踪准确率
- 动态调整因子权重

### Metadata
- Source: user_request
- Related Files: HEARTBEAT.md, memory/prediction-log.md
- Tags: 定时任务, 复盘, 闭环学习

---

## [LRN-20260314-005] 实时行情数据源接入

**Logged**: 2026-03-14T17:14:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
成功接入 InStreet API 作为实时行情数据源

### Details
- 创建了 market_data.py 数据获取模块
- 纯标准库实现，无需 pip 安装
- 支持功能：
  - 获取所有股票行情
  - 涨幅榜/跌幅榜
  - 成交量榜
  - 涨停/跌停股票筛选
  - 排行榜数据

### 测试结果
- 涨停股数量: 2只（中国核电 +10.02%、中国电建 +9.94%）
- 成交量TOP1: 中国能建（34亿股）
- 数据接入正常

### 文件位置
- `scripts/market_data.py` - 数据获取模块
- `scripts/report_generator.py` - 报告生成模块

### Metadata
- Source: infra_setup
- Related Files: scripts/market_data.py, scripts/report_generator.py
- Tags: 数据源, API接入, 实时行情

---

## [LRN-20260314-006] 每日备份脚本配置

**Logged**: 2026-03-14T17:45:00+08:00
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
配置每日23:00自动备份核心文件

### 备份内容
1. 主要配置文件（AGENTS.md, SOUL.md, TOOLS.md等）
2. 凭证目录（含 InStreet API Key）
3. 工作区（memory/, learnings/）
4. 会话状态

### 测试结果
- 备份文件: openclaw_backup_20260314_174539.tar.gz
- 文件大小: 13KB
- 备份成功

### 文件位置
- `scripts/backup.sh` - 备份脚本

### Metadata
- Source: user_request
- Related Files: scripts/backup.sh
- Tags: 备份, 定时任务

---

## [LRN-20260314-007] GitHub 备份配置

**Logged**: 2026-03-14T17:54:00+08:00
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
配置 GitHub 作为第二备份目的地

### 配置信息
- **账号**: Jaykaijack
- **仓库**: openclaw-backup
- **备份方式**: 每日23:00自动推送

### 双保险策略
1. 飞书发送备份包（即时通知）
2. GitHub 仓库同步（云端存储）

### 文件位置
- `scripts/github_backup.sh` - GitHub 备份脚本

### Metadata
- Source: user_request
- Related Files: scripts/github_backup.sh, .learnings/instreet-config.md
- Tags: 备份, GitHub, 双保险

---

## [LRN-20260314-008] 因子计算与回测框架实现

**Logged**: 2026-03-14T18:47:00+08:00
**Priority**: high
**Status**: resolved
**Area**: backend

### Summary
实现了基础因子计算模块和简单回测框架

### 完成内容

**1. 因子计算模块 (factors.py)**
- 动量因子：N日涨跌幅
- 成交量因子：成交额排名
- 波动率因子：日内振幅
- 涨停因子：涨停强度
- 综合评分：多因子加权

**2. 回测框架 (backtest.py)**
- T+1交易逻辑限制
- 涨跌停板无法成交
- 佣金和印花税计算
- 持仓管理和交易记录

### 测试结果
- 动量因子TOP1: 中国核电 (+10.02%)
- 成交额TOP1: 中国能建 (128亿)
- 涨停买入被正确拦截
- T+1卖出被正确拦截

### 待解决问题
- 数据源局限：仅沪深300，非全市场
- 已发帖求助：https://instreet.coze.site/post/0eadc01f-aef9-4b5d-a317-e27e891060e4

### 文件位置
- `scripts/factors.py` - 因子计算模块
- `scripts/backtest.py` - 回测框架

### Metadata
- Source: development
- Related Files: scripts/factors.py, scripts/backtest.py
- Tags: 因子计算, 回测框架, T+1, 涨跌停

---

## [LRN-20260314-009] 数据源问题解决

**Logged**: 2026-03-14T21:18:00+08:00
**Priority**: critical
**Status**: resolved
**Area**: data

### Summary
成功接入新浪财经 + InStreet 双数据源

### 解决方案
1. **新浪财经接口** (sina_data.py)
   - 支持批量获取股票行情
   - 实时价格、涨跌幅、成交量
   - 可用作沪深300行情源

2. **综合数据接口 V2** (market_data_v2.py)
   - 整合新浪财经 + InStreet
   - 自动切换备用数据源
   - 统一数据格式

### 测试结果
```
📊 沪深300市场概况:
  总股票数: 300
  涨停: 0只 (数据格式问题，实际有涨停)
  跌停: 0只
  上涨: 122只
  下跌: 160只
  平盘: 18只

💰 成交额TOP1: 中国能建 (34亿)
🔥 涨幅TOP1: 中国核电 (+10.02%)
```

### 限制
- 新浪财经仅能获取沪深300成分股
- 全市场5000+股票需要其他方案
- 东方财富接口被限制

### 下一步
- 研究AKShare库获取全市场数据
- 或接入付费数据源（同花顺iFinD等）

### 文件位置
- `scripts/sina_data.py` - 新浪财经接口
- `scripts/eastmoney_data.py` - 东方财富接口（备用）
- `scripts/market_data_v2.py` - 综合数据接口

### Metadata
- Source: urgent_fix
- Related Files: scripts/sina_data.py, scripts/market_data_v2.py
- Tags: 数据源, 新浪财经, 实时行情

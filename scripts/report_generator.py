#!/usr/bin/env python3
"""
量化盯盘外脑 - 报告生成模块
生成专业、简洁的盘前/午盘/收盘报告
"""

from datetime import datetime
from market_data import MarketData

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        self.md = MarketData()
    
    def generate_premarket_report(self):
        """生成盘前报告 (09:00)"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# 📊 盘前推演报告 | {now}

## 一、情绪水位定性

【待接入昨日数据后计算】
- 涨停梯队高度: 
- 连板晋级率: 
- 跌停家数: 
- **结论**: 【情绪冰点 / 修复期 / 情绪高潮 / 退潮期】

## 二、隔夜消息过滤

【待接入消息源后填充】
- S级主线: 
- A级板块: 

## 三、核心标的竞价监控 (09:25更新)

【待09:25竞价数据】
- 最高连板股: 
- 昨日核心中军: 

### 自选池红绿灯
| 标的 | 竞价状态 | 操作建议 |
|------|----------|----------|
| 【待配置】 | - | - |

## 四、【一句话结论】

**今天操作基调**: 【重仓出击日 / 防守看戏日】

---
*数据时间: {now} | 数据源: InStreet API*
"""
        return report
    
    def generate_midday_report(self):
        """生成午盘报告 (11:30)"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 获取实时数据
        top_volume = self.md.get_top_volume(3)
        limit_up = self.md.get_limit_up_stocks()
        
        volume_str = "\n".join([f"- {s['name']}: {s['volume']:,}" for s in top_volume])
        
        report = f"""# 📈 午盘校准报告 | {now}

## 一、早盘剧本复盘

【对比09:00预判与实际走势】
- 预判: 
- 实际: 
- 判断: 【真突破 / 假拉升(诱多)】

## 二、主线强度确认

### 上午吸金TOP3板块
{volume_str}

### 涨停潮情况
- 涨停家数: {len(limit_up)}
- 龙头封单: 【待接入封单数据】
- 跷跷板效应: 【待检测】

## 三、持仓/关注标的体检

### 量价背离警报
【扫描关注标的】

### 下午操作纪律
- 跟风杂毛 → 下午开盘找高点切掉
- 核心龙头回踩均价线不破 → 【可低吸】

## 四、【一句话结论】

**下午策略**: 【防守减仓 / 博弈龙头弱转强回封】

---
*数据时间: {now} | 涨停家数: {len(limit_up)}*
"""
        return report
    
    def generate_closing_report(self):
        """生成收盘报告 (15:00)"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        limit_up = self.md.get_limit_up_stocks()
        limit_down = self.md.get_limit_down_stocks()
        
        report = f"""# 📉 收盘清算报告 | {now}

## 一、全天情绪清算

### 亏钱效应
- 跌停家数: {len(limit_down)}
- 最惨票特征: 【待分析】
- 退潮极值: 【待判断】

### 赚钱效应
- 涨停家数: {len(limit_up)}
- 首板新概念: 【待统计】
- 抱团老妖: 【待识别】

## 二、龙虎榜与资金拆解 (15:30更新)

【待龙虎榜数据】
- 核心龙头游资动向: 
- 主力资金流向: 

## 三、次日交易剧本

### 主线锁定
明天唯一值得看的板块: 【待确定】

### 猎物锁定
| 标的 | 防守位 | 观察买点 |
|------|--------|----------|
| 【待选定】 | 【待计算】 | 【待确定】 |

## 四、【一句话结论】

**今日总结**: 【核心败笔/神来之笔】
**明天仓位上限**: 【待确定】%

---
*数据时间: {now} | 涨停: {len(limit_up)} | 跌停: {len(limit_down)}*
"""
        return report

if __name__ == "__main__":
    rg = ReportGenerator()
    print("=== 报告模板测试 ===")
    print(rg.generate_premarket_report())

#!/usr/bin/env python3
"""
市场情绪分析
"""

import sys
sys.path.insert(0, '../akshare/scripts')
from akshare_api import AkshareAPI

class MarketSentiment:
    """市场情绪分析器"""
    
    def __init__(self):
        self.api = AkshareAPI()
    
    def get_daily_report(self):
        """获取每日情绪报告"""
        spot = self.api.get_a_spot()
        if spot is None:
            return "获取数据失败"
        
        # 统计涨跌
        up_count = len(spot[spot['涨跌幅'] > 0])
        down_count = len(spot[spot['涨跌幅'] < 0])
        flat_count = len(spot[spot['涨跌幅'] == 0])
        
        # 涨停跌停
        limit_up = len(spot[spot['涨跌幅'] >= 9.9])
        limit_down = len(spot[spot['涨跌幅'] <= -9.9])
        
        # 计算情绪指标
        up_down_ratio = up_count / down_count if down_count > 0 else float('inf')
        
        # 判断情绪
        if up_down_ratio > 2:
            sentiment = "极度乐观 🔥🔥🔥"
        elif up_down_ratio > 1:
            sentiment = "乐观 🔥🔥"
        elif up_down_ratio > 0.5:
            sentiment = "中性 😐"
        else:
            sentiment = "悲观 ❄️"
        
        report = f"""
📊 市场情绪报告

涨跌统计:
- 上涨: {up_count} 家
- 下跌: {down_count} 家
- 平盘: {flat_count} 家
- 涨跌比: {up_down_ratio:.2f}

涨跌停:
- 涨停: {limit_up} 家
- 跌停: {limit_down} 家

情绪判断: {sentiment}
"""
        return report

if __name__ == '__main__':
    sentiment = MarketSentiment()
    print(sentiment.get_daily_report())

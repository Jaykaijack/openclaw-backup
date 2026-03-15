#!/usr/bin/env python3
"""
Akshare API 封装 - 财经数据获取
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

class AkshareAPI:
    """Akshare 财经数据接口"""
    
    def __init__(self):
        self.name = "AkshareAPI"
    
    def get_a_spot(self):
        """获取A股实时行情"""
        try:
            df = ak.stock_zh_a_spot_em()
            return df
        except Exception as e:
            print(f"获取A股行情失败: {e}")
            return None
    
    def get_stock_hist(self, symbol, period="daily", days=30):
        """获取个股历史数据"""
        try:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
            df = ak.stock_zh_a_hist(symbol=symbol, period=period, 
                                   start_date=start_date, end_date=end_date, adjust="qfq")
            return df
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return None
    
    def get_lhb(self, start_date=None, end_date=None):
        """获取龙虎榜数据"""
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            df = ak.stock_lhb_detail_daily_sina(start_date=start_date, end_date=end_date)
            return df
        except Exception as e:
            print(f"获取龙虎榜失败: {e}")
            return None

if __name__ == '__main__':
    api = AkshareAPI()
    print("Akshare API 测试")
    spot = api.get_a_spot()
    if spot is not None:
        print(f"获取到 {len(spot)} 只A股数据")

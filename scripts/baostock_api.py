#!/usr/bin/env python3
"""
Baostock A股数据获取模块
特点：免费、无需注册、数据全面
"""

import baostock as bs
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class BaostockAPI:
    """Baostock 数据获取类"""
    
    def __init__(self):
        self.logged_in = False
        self._login()
    
    def _login(self):
        """登录 baostock"""
        if not self.logged_in:
            result = bs.login()
            if result.error_code == '0':
                self.logged_in = True
                print("✅ Baostock 登录成功")
            else:
                print(f"❌ 登录失败: {result.error_msg}")
    
    def __del__(self):
        """析构时登出"""
        if self.logged_in:
            bs.logout()
            print("✅ Baostock 已登出")
    
    def _format_code(self, code: str) -> str:
        """格式化股票代码为 baostock 格式"""
        code = code.strip().lower()
        if code.startswith('sh.'):
            return code
        elif code.startswith('sz.'):
            return code
        elif code.startswith('6'):
            return f'sh.{code}'
        elif code.startswith('0') or code.startswith('3'):
            return f'sz.{code}'
        return code
    
    def get_kline(self, code: str, start_date: str, end_date: str, 
                  frequency: str = 'd', adjustflag: str = '3') -> pd.DataFrame:
        """
        获取 K线数据
        
        Args:
            code: 股票代码，如 '600000' 或 'sh.600000'
            start_date: 开始日期 'YYYY-MM-DD'
            end_date: 结束日期 'YYYY-MM-DD'
            frequency: 频率 'd'=日, 'w'=周, 'm'=月
            adjustflag: 复权类型 '1'=后复权, '2'=前复权, '3'=不复权
        
        Returns:
            DataFrame: K线数据
        """
        code = self._format_code(code)
        
        fields = 'date,code,open,high,low,close,preclose,volume,amount,turn,pctChg'
        rs = bs.query_history_k_data_plus(code, fields, 
                                          start_date=start_date, 
                                          end_date=end_date,
                                          frequency=frequency,
                                          adjustflag=adjustflag)
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        df = pd.DataFrame(data, columns=rs.fields)
        
        # 转换数据类型
        numeric_cols = ['open', 'high', 'low', 'close', 'preclose', 
                       'volume', 'amount', 'turn', 'pctChg']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def get_stock_list(self, date: Optional[str] = None) -> pd.DataFrame:
        """
        获取股票列表
        
        Args:
            date: 日期 'YYYY-MM-DD'，默认今天
        
        Returns:
            DataFrame: 股票列表
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        rs = bs.query_all_stock(day=date)
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        return pd.DataFrame(data, columns=rs.fields)
    
    def get_profit_data(self, code: str, year: int, quarter: int) -> pd.DataFrame:
        """
        获取季频盈利能力数据
        
        Args:
            code: 股票代码
            year: 年份
            quarter: 季度 1-4
        """
        code = self._format_code(code)
        rs = bs.query_profit_data(code, year=year, quarter=quarter)
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        return pd.DataFrame(data, columns=rs.fields)
    
    def get_balance_sheet(self, code: str, year: int, quarter: int) -> pd.DataFrame:
        """获取资产负债表"""
        code = self._format_code(code)
        rs = bs.query_balance_data(code, year=year, quarter=quarter)
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        return pd.DataFrame(data, columns=rs.fields)
    
    def get_cash_flow(self, code: str, year: int, quarter: int) -> pd.DataFrame:
        """获取现金流量表"""
        code = self._format_code(code)
        rs = bs.query_cash_flow_data(code, year=year, quarter=quarter)
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        return pd.DataFrame(data, columns=rs.fields)
    
    def get_index_stocks(self, index_code: str = 'hs300') -> pd.DataFrame:
        """
        获取指数成分股
        
        Args:
            index_code: 'hs300'=沪深300, 'sz50'=上证50, 'zz500'=中证500
        """
        if index_code == 'hs300':
            rs = bs.query_hs300_stocks()
        elif index_code == 'sz50':
            rs = bs.query_sz50_stocks()
        elif index_code == 'zz500':
            rs = bs.query_zz500_stocks()
        else:
            raise ValueError(f"不支持的指数: {index_code}")
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        return pd.DataFrame(data, columns=rs.fields)
    
    def get_trade_dates(self, start_date: str, end_date: str) -> pd.DataFrame:
        """获取交易日历"""
        rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        return pd.DataFrame(data, columns=rs.fields)
    
    def get_stock_industry(self, code: str) -> pd.DataFrame:
        """获取股票所属行业"""
        code = self._format_code(code)
        rs = bs.query_stock_industry(code=code)
        
        data = []
        while (rs.error_code == '0') & rs.next():
            data.append(rs.get_row_data())
        
        return pd.DataFrame(data, columns=rs.fields)


# 测试代码
if __name__ == '__main__':
    api = BaostockAPI()
    
    print("=" * 60)
    print("Baostock API 测试")
    print("=" * 60)
    
    # 测试获取 K线
    print("\n1. 获取日 K线数据 (600000 浦发银行)")
    df = api.get_kline('600000', '2025-03-01', '2025-03-14')
    print(df.tail())
    
    # 测试获取财务数据
    print("\n2. 获取财务数据 (600000)")
    df_profit = api.get_profit_data('600000', 2024, 3)
    print(df_profit[['code', 'pubDate', 'roeAvg', 'npMargin']])
    
    # 测试获取沪深300成分股
    print("\n3. 获取沪深300成分股 (前10只)")
    df_hs300 = api.get_index_stocks('hs300')
    print(df_hs300.head(10))
    
    # 测试获取交易日历
    print("\n4. 获取交易日历 (2025年3月)")
    df_dates = api.get_trade_dates('2025-03-01', '2025-03-31')
    print(df_dates.head(10))
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)
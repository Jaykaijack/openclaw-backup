#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天际股份(002759) 深度分析脚本 - 补充数据获取
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import time

def get_realtime_quote_v2():
    """获取实时行情 - 备用接口"""
    print("=" * 60)
    print("【1. 实时行情】")
    print("=" * 60)
    
    try:
        # 使用新浪财经接口
        df = ak.stock_zh_a_spot()
        stock = df[df['代码'] == 'sz002759']
        
        if stock.empty:
            # 尝试东方财富
            df = ak.stock_zh_a_spot_em()
            stock = df[df['代码'] == '002759']
        
        if stock.empty:
            print("未找到该股票实时数据")
            return None
        
        stock = stock.iloc[0]
        print(f"股票名称: {stock.get('名称', '天际股份')}")
        print(f"股票代码: 002759")
        print(f"最新价格: {stock.get('最新价', stock.get('price', 'N/A'))}")
        print(f"涨跌幅: {stock.get('涨跌幅', stock.get('changepercent', 'N/A'))}%")
        print(f"涨跌额: {stock.get('涨跌额', stock.get('updown', 'N/A'))}")
        print(f"成交量: {stock.get('成交量', stock.get('volume', 'N/A'))}")
        print(f"成交额: {stock.get('成交额', stock.get('amount', 'N/A'))}")
        print(f"换手率: {stock.get('换手率', stock.get('turnoverratio', 'N/A'))}%")
        print(f"振幅: {stock.get('振幅', 'N/A')}%")
        print(f"最高: {stock.get('最高', stock.get('high', 'N/A'))}")
        print(f"最低: {stock.get('最低', stock.get('low', 'N/A'))}")
        print(f"今开: {stock.get('今开', stock.get('open', 'N/A'))}")
        print(f"昨收: {stock.get('昨收', stock.get('settlement', 'N/A'))}")
        print(f"市盈率: {stock.get('市盈率-动态', stock.get('per', stock.get('pe', 'N/A')))}")
        print(f"市净率: {stock.get('市净率', stock.get('pb', 'N/A'))}")
        print(f"总市值: {stock.get('总市值', stock.get('mktcap', 'N/A'))}")
        print(f"流通市值: {stock.get('流通市值', stock.get('nmc', 'N/A'))}")
        
        return stock.to_dict()
    except Exception as e:
        print(f"获取实时行情失败: {e}")
        return None

def get_hist_data():
    """获取历史数据"""
    print("\n" + "=" * 60)
    print("【3. 技术面分析】")
    print("=" * 60)
    
    try:
        # 获取历史数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
        
        hist_df = ak.stock_zh_a_hist(symbol="002759", period="daily", 
                                      start_date=start_date, end_date=end_date, adjust="qfq")
        
        if hist_df.empty:
            print("未获取到历史数据")
            return
        
        print(f"\n--- 近30日走势数据 ---")
        display_df = hist_df.tail(30)[['日期', '开盘', '收盘', '最高', '最低', '成交量', '涨跌幅']].copy()
        print(display_df.to_string(index=False))
        
        # 计算均线
        hist_df['MA5'] = hist_df['收盘'].rolling(window=5).mean()
        hist_df['MA10'] = hist_df['收盘'].rolling(window=10).mean()
        hist_df['MA20'] = hist_df['收盘'].rolling(window=20).mean()
        hist_df['MA60'] = hist_df['收盘'].rolling(window=60).mean()
        
        latest = hist_df.iloc[-1]
        print(f"\n--- 均线系统 ---")
        print(f"MA5:  {latest['MA5']:.2f}")
        print(f"MA10: {latest['MA10']:.2f}")
        print(f"MA20: {latest['MA20']:.2f}")
        print(f"MA60: {latest['MA60']:.2f}")
        
        # 判断趋势
        current_price = latest['收盘']
        print(f"\n--- 趋势分析 ---")
        print(f"当前价格: {current_price}")
        
        # 均线位置判断
        above_ma5 = current_price > latest['MA5'] if not pd.isna(latest['MA5']) else False
        above_ma10 = current_price > latest['MA10'] if not pd.isna(latest['MA10']) else False
        above_ma20 = current_price > latest['MA20'] if not pd.isna(latest['MA20']) else False
        above_ma60 = current_price > latest['MA60'] if not pd.isna(latest['MA60']) else False
        
        print(f"相对于MA5: {'上方' if above_ma5 else '下方'}")
        print(f"相对于MA10: {'上方' if above_ma10 else '下方'}")
        print(f"相对于MA20: {'上方' if above_ma20 else '下方'}")
        print(f"相对于MA60: {'上方' if above_ma60 else '下方'}")
        
        # 支撑压力位
        recent_20 = hist_df.tail(20)
        support = recent_20['最低'].min()
        resistance = recent_20['最高'].max()
        print(f"\n--- 关键支撑压力位(近20日) ---")
        print(f"支撑位: {support:.2f}")
        print(f"压力位: {resistance:.2f}")
        
        # 近期高点和低点
        print(f"\n--- 近期高低点 ---")
        print(f"近60日最高: {hist_df['最高'].max():.2f}")
        print(f"近60日最低: {hist_df['最低'].min():.2f}")
        
        # 成交量分析
        avg_volume_5 = hist_df.tail(5)['成交量'].mean()
        avg_volume_20 = hist_df.tail(20)['成交量'].mean()
        latest_volume = latest['成交量']
        
        print(f"\n--- 量能分析 ---")
        print(f"最新成交量: {latest_volume}")
        print(f"5日均量: {avg_volume_5:.0f}")
        print(f"20日均量: {avg_volume_20:.0f}")
        print(f"量比(相对于5日): {latest_volume/avg_volume_5:.2f}")
        
        return hist_df
        
    except Exception as e:
        print(f"获取技术面数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_stock_basic():
    """获取股票基本信息"""
    print("\n" + "=" * 60)
    print("【2. 基本面信息】")
    print("=" * 60)
    
    try:
        # 获取股票列表
        stock_list = ak.stock_info_a_code_name()
        stock_info = stock_list[stock_list['code'] == '002759']
        if not stock_info.empty:
            print(f"股票名称: {stock_info.iloc[0]['name']}")
    except:
        pass
    
    # 获取公司简介
    try:
        print("\n--- 公司简介 ---")
        company_df = ak.stock_company_info_a(symbol="002759")
        if not company_df.empty:
            for col in company_df.columns:
                print(f"{col}: {company_df.iloc[0][col]}")
    except Exception as e:
        print(f"获取公司简介失败: {e}")
    
    # 获取财务指标
    try:
        print("\n--- 财务指标 ---")
        fina_df = ak.stock_financial_analysis_indicator(symbol="002759")
        if not fina_df.empty:
            print(fina_df.head(5).to_string())
    except Exception as e:
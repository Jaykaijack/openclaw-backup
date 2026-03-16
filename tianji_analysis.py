#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天际股份(002759) 深度分析脚本
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import json

# 设置显示选项
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def get_realtime_quote():
    """获取实时行情"""
    print("=" * 60)
    print("【1. 实时行情】")
    print("=" * 60)
    
    try:
        # 获取A股实时行情
        df = ak.stock_zh_a_spot_em()
        stock = df[df['代码'] == '002759']
        
        if stock.empty:
            print("未找到该股票实时数据")
            return None
        
        stock = stock.iloc[0]
        print(f"股票名称: {stock['名称']}")
        print(f"股票代码: {stock['代码']}")
        print(f"最新价格: {stock['最新价']}")
        print(f"涨跌幅: {stock['涨跌幅']}%")
        print(f"涨跌额: {stock['涨跌额']}")
        print(f"成交量: {stock['成交量']}")
        print(f"成交额: {stock['成交额']}")
        print(f"换手率: {stock['换手率']}%")
        print(f"振幅: {stock['振幅']}%")
        print(f"最高: {stock['最高']}")
        print(f"最低: {stock['最低']}")
        print(f"今开: {stock['今开']}")
        print(f"昨收: {stock['昨收']}")
        print(f"市盈率(动态): {stock['市盈率-动态']}")
        print(f"市净率: {stock['市净率']}")
        print(f"总市值: {stock['总市值']}")
        print(f"流通市值: {stock['流通市值']}")
        
        return stock.to_dict()
    except Exception as e:
        print(f"获取实时行情失败: {e}")
        return None

def get_basic_info():
    """获取基本面信息"""
    print("\n" + "=" * 60)
    print("【2. 基本面信息】")
    print("=" * 60)
    
    try:
        # 获取股票列表
        stock_list = ak.stock_zh_a_spot_em()
        stock = stock_list[stock_list['代码'] == '002759']
        
        if not stock.empty:
            print(f"所属行业: {stock.iloc[0].get('所属行业', 'N/A')}")
    except:
        pass
    
    # 获取主营业务构成
    try:
        print("\n--- 主营业务构成 ---")
        business_df = ak.stock_zygc_ym(symbol="002759")
        if not business_df.empty:
            print(business_df.head(10).to_string())
    except Exception as e:
        print(f"获取主营业务失败: {e}")
    
    # 获取财务指标
    try:
        print("\n--- 财务指标 ---")
        fina_df = ak.stock_financial_analysis_indicator(symbol="002759")
        if not fina_df.empty:
            print(fina_df.head(5).to_string())
    except Exception as e:
        print(f"获取财务指标失败: {e}")
    
    # 获取利润表
    try:
        print("\n--- 利润表(最新季度) ---")
        profit_df = ak.stock_profit_sheet_by_report_em(symbol="002759")
        if not profit_df.empty:
            print(profit_df.head(3).to_string())
    except Exception as e:
        print(f"获取利润表失败: {e}")

def get_technical_analysis():
    """获取技术面分析"""
    print("\n" + "=" * 60)
    print("【3. 技术面分析】")
    print("=" * 60)
    
    try:
        # 获取历史数据
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=120)).strftime('%Y%m%d')
        
        hist_df = ak.stock_zh_a_hist(symbol="002759", period="daily", 
                                      start_date=start_date, end_date=end_date, adjust="qfq")
        
        if hist_df.empty:
            print("未获取到历史数据")
            return
        
        print(f"\n--- 近60日走势数据 ---")
        print(hist_df.tail(60)[['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅']].to_string())
        
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
        print(f"相对于MA5: {'上方' if current_price > latest['MA5'] else '下方'} ({((current_price/latest['MA5']-1)*100):.2f}%)")
        print(f"相对于MA10: {'上方' if current_price > latest['MA10'] else '下方'} ({((current_price/latest['MA10']-1)*100):.2f}%)")
        print(f"相对于MA20: {'上方' if current_price > latest['MA20'] else '下方'} ({((current_price/latest['MA20']-1)*100):.2f}%)")
        print(f"相对于MA60: {'上方' if current_price > latest['MA60'] else '下方'} ({((current_price/latest['MA60']-1)*100):.2f}%)")
        
        # 支撑压力位
        recent_20 = hist_df.tail(20)
        support = recent_20['最低'].min()
        resistance = recent_20['最高'].max()
        print(f"\n--- 关键支撑压力位(近20日) ---")
        print(f"支撑位: {support}")
        print(f"压力位: {resistance}")
        
        # 近期高点和低点
        print(f"\n--- 近期高低点 ---")
        print(f"近60日最高: {hist_df['最高'].max()} (日期: {hist_df.loc[hist_df['最高'].idxmax(), '日期']})")
        print(f"近60日最低: {hist_df['最低'].min()} (日期: {hist_df.loc[hist_df['最低'].idxmin(), '日期']})")
        
    except Exception as e:
        print(f"获取技术面数据失败: {e}")

def get_capital_flow():
    """获取资金流向"""
    print("\n" + "=" * 60)
    print("【4. 资金流向】")
    print("=" * 60)
    
    try:
        # 获取个股资金流向
        flow_df = ak.stock_individual_fund_flow(stock="002759", market="sz")
        print("\n--- 近期资金流向 ---")
        print(flow_df.head(20).to_string())
        
        # 计算净流入
        if not flow_df.empty:
            recent_5 = flow_df.head(5)
            total_inflow = recent_5['主力净流入-净额'].sum()
            print(f"\n--- 近5日主力净流入: {total_inflow:.2f} 万元 ---")
            
            recent_10 = flow_df.head(10)
            total_inflow_10 = recent_10['主力净流入-净额'].sum()
            print(f"--- 近10日主力净流入: {total_inflow_10:.2f} 万元 ---")
    except Exception as e:
        print(f"获取资金流向失败: {e}")

def get_news_and_announcements():
    """获取新闻和公告"""
    print("\n" + "=" * 60)
    print("【5. 利好/利空因素 - 新闻与公告】")
    print("=" * 60)
    
    try:
        # 获取公司新闻
        print("\n--- 公司新闻 ---")
        news_df = ak.stock_news_em(symbol="002759")
        if not news_df.empty:
            print(news_df.head(10).to_string())
    except Exception as e:
        print(f"获取新闻失败: {e}")
    
    try:
        # 获取公司公告
        print("\n--- 公司公告 ---")
        notice_df = ak.stock_notice_report(symbol="002759")
        if not notice_df.empty:
            print(notice_df.head(10).to_string())
    except Exception as e:
        print(f"获取公告失败: {e}")

def get_risk_info():
    """获取风险信息"""
    print("\n" + "=" * 60)
    print("【6. 风险提示】")
    print("=" * 60)
    
    try:
        # 获取龙虎榜数据
        print("\n--- 近期龙虎榜数据 ---")
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        lhb_df = ak.stock_lhb_detail_daily_sina(start_date=start_date, end_date=end_date)
        
        if not lhb_df.empty:
            stock_lhb = lhb_df[lhb_df['代码'] == '002759']
            if not stock_lhb.empty:
                print(stock_lhb.to_string())
            else:
                print("近30日无龙虎榜数据")
        else:
            print("无龙虎榜数据")
    except Exception as e:
        print(f"获取龙虎榜数据失败: {e}")
    
    try:
        # 获取融资融券数据
        print("\n--- 融资融券数据 ---")
        margin_df = ak.stock_margin_detail_szse(date=datetime.now().strftime('%Y%m%d'))
        if not margin_df.empty:
            stock_margin = margin_df[margin_df['证券代码'] == '002759']
            if not stock_margin.empty:
                print(stock_margin.to_string())
            else:
                print("无融资融券数据")
    except Exception as e:
        print(f"获取融资融券数据失败: {e}")
    
    # 风险提醒
    print("\n--- 风险提示 ---")
    print("1. 股市有风险，投资需谨慎")
    print("2. 本分析仅供参考，不构成投资建议")
    print("3. 请结合个人风险承受能力做出投资决策")
    print("4. 注意市场系统性风险和个股特有风险")

def main():
    print("\n" + "=" * 60)
    print("天际股份(002759) 深度分析报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 实时行情
    realtime = get_realtime_quote()
    
    # 2. 基本面
    get_basic_info()
    
    # 3. 技术面
    get_technical_analysis()
    
    # 4. 资金流向
    get_capital_flow()
    
    # 5. 利好/利空因素
    get_news_and_announcements()
    
    # 6. 风险提示
    get_risk_info()
    
    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)

if __name__ == "__main__":
    main()

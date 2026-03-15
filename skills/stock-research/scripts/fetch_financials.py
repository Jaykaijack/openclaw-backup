#!/usr/bin/env python3
"""
Fetch financial data for A-share stocks using akshare.
Usage: python fetch_financials.py <stock_code> [--market cn|hk|us]

Outputs JSON with:
- info: basic company info
- income: income statement (latest 3 years)
- balance: balance sheet
- cashflow: cash flow statement
- indicators: financial analysis indicators
- fund_hold: institutional holdings
"""
import sys
import json
import importlib

def fetch_cn(symbol):
    ak = importlib.import_module('akshare')
    data = {}
    
    try:
        info = ak.stock_individual_info_em(symbol=symbol)
        data['info'] = info.to_dict('records') if hasattr(info, 'to_dict') else str(info)
    except Exception as e:
        data['info_error'] = str(e)
    
    try:
        income = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        data['income'] = income.head(12).to_dict('records')
    except Exception as e:
        data['income_error'] = str(e)
    
    try:
        balance = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        data['balance'] = balance.head(4).to_dict('records')
    except Exception as e:
        data['balance_error'] = str(e)
    
    try:
        cashflow = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        data['cashflow'] = cashflow.head(4).to_dict('records')
    except Exception as e:
        data['cashflow_error'] = str(e)
    
    try:
        indicators = ak.stock_financial_analysis_indicator(symbol=symbol)
        data['indicators'] = indicators.head(4).to_dict('records')
    except Exception as e:
        data['indicators_error'] = str(e)
    
    return data

def fetch_us(symbol):
    yf = importlib.import_module('yfinance')
    stock = yf.Ticker(symbol)
    data = {}
    
    try:
        data['info'] = {k: v for k, v in stock.info.items() 
                       if not isinstance(v, (bytes, memoryview))}
    except Exception as e:
        data['info_error'] = str(e)
    
    try:
        fin = stock.financials
        data['financials'] = fin.to_dict() if hasattr(fin, 'to_dict') else str(fin)
    except Exception as e:
        data['financials_error'] = str(e)
    
    return data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fetch_financials.py <symbol> [--market cn|hk|us]")
        sys.exit(1)
    
    symbol = sys.argv[1]
    market = 'cn'
    if '--market' in sys.argv:
        idx = sys.argv.index('--market')
        if idx + 1 < len(sys.argv):
            market = sys.argv[idx + 1]
    
    if market in ('cn', 'hk'):
        result = fetch_cn(symbol)
    elif market == 'us':
        result = fetch_us(symbol)
    else:
        print(f"Unknown market: {market}")
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

#!/usr/bin/env python3
"""
数据验证模块 - 严格保证数据正确性
"""

import sys
sys.path.insert(0, 'scripts')

from zhituapi import ZhituAPI
from stock_data_api import StockDataAPI
from datetime import datetime
import json
import os

class DataVerificationError(Exception):
    """数据验证错误"""
    pass

class StockDataVerifier:
    """股票数据验证器 - 严格执行验证协议"""
    
    def __init__(self):
        self.zhitu = ZhituAPI()
        self.stock_api = StockDataAPI()
        self.log_file = os.path.expanduser('~/.openclaw/workspace/.learnings/verification.log')
    
    def verify(self, code, expected_name=None):
        """
        完整验证流程
        
        Args:
            code: 股票代码（如 '601985'）
            expected_name: 预期股票名称（可选，用于验证）
        
        Returns:
            dict: {
                'verified': bool,
                'data': dict or None,
                'errors': list
            }
        """
        result = {
            'code': code,
            'verified': False,
            'data': None,
            'errors': []
        }
        
        print(f"🔍 开始验证股票: {code}")
        
        # Step 1: 代码格式检查
        if not self._check_code_format(code):
            result['errors'].append('代码格式错误（必须是6位数字）')
            self._log(result)
            return result
        print("  ✅ 代码格式正确")
        
        # Step 2: 代码存在性和名称核实
        stock_info = self._verify_code_exists(code)
        if not stock_info:
            result['errors'].append('代码不存在或已退市')
            self._log(result)
            return result
        print(f"  ✅ 代码存在: {stock_info['name']}")
        
        # Step 3: 名称匹配检查
        if expected_name and stock_info['name'] != expected_name:
            result['errors'].append(f'名称不匹配: 实际"{stock_info["name"]}" != 预期"{expected_name}"')
            self._log(result)
            return result
        if expected_name:
            print(f"  ✅ 名称匹配: {expected_name}")
        
        # Step 4: 价格实时性验证
        price_data = self._verify_price(code)
        if not price_data:
            result['errors'].append('无法获取实时价格')
            self._log(result)
            return result
        print(f"  ✅ 价格获取成功: ¥{price_data['price']:.2f}")
        
        # Step 5: 价格合理性检查
        if not self._check_price_reasonable(price_data):
            result['errors'].append(f'价格异常: ¥{price_data["price"]:.2f}')
            self._log(result)
            return result
        print("  ✅ 价格在合理范围")
        
        # Step 6: 涨跌幅合理性检查
        if not self._check_change_reasonable(price_data):
            result['errors'].append(f'涨跌幅异常: {price_data["change_pct"]:+.2f}%')
            self._log(result)
            return result
        print(f"  ✅ 涨跌幅合理: {price_data['change_pct']:+.2f}%")
        
        # 全部通过
        result['verified'] = True
        result['data'] = {
            'code': code,
            'name': stock_info['name'],
            'price': price_data['price'],
            'change_pct': price_data['change_pct'],
            'open': price_data.get('open'),
            'high': price_data.get('high'),
            'low': price_data.get('low'),
            'close': price_data.get('close'),
            'volume': price_data.get('volume'),
            'timestamp': datetime.now().isoformat(),
        }
        
        print("  ✅ 全部验证通过!")
        self._log(result)
        return result
    
    def _check_code_format(self, code):
        """检查代码格式"""
        if not code or len(code) != 6:
            return False
        return code.isdigit()
    
    def _verify_code_exists(self, code):
        """验证代码存在性"""
        try:
            # 从智途API获取股票信息
            all_stocks = self.zhitu.get_all_stocks()
            for stock in all_stocks:
                pure_code = stock.get('dm', '').replace('.SH', '').replace('.SZ', '')
                if pure_code == code:
                    return {
                        'code': code,
                        'name': stock.get('mc'),
                        'exchange': stock.get('jys')
                    }
            return None
        except Exception as e:
            print(f"  ⚠️ 代码验证异常: {e}")
            return None
    
    def _verify_price(self, code):
        """验证价格实时性"""
        try:
            quote = self.stock_api.get_qq_quotes([code])
            if not quote:
                return None
            
            info = list(quote.values())[0]
            return {
                'price': info.get('current'),
                'change_pct': info.get('change_pct'),
                'open': info.get('open'),
                'high': info.get('high'),
                'low': info.get('low'),
                'close': info.get('close'),
                'volume': info.get('volume'),
            }
        except Exception as e:
            print(f"  ⚠️ 价格获取异常: {e}")
            return None
    
    def _check_price_reasonable(self, price_data):
        """检查价格合理性"""
        price = price_data.get('price', 0)
        return 0 < price < 10000
    
    def _check_change_reasonable(self, price_data):
        """检查涨跌幅合理性"""
        change = price_data.get('change_pct', 0)
        return -30 < change < 30
    
    def _log(self, result):
        """记录验证日志"""
        log_entry = {
            'time': datetime.now().isoformat(),
            'code': result['code'],
            'verified': result['verified'],
            'errors': result['errors'],
            'data': result['data']
        }
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"  ⚠️ 日志记录失败: {e}")


def verify_stock(code, expected_name=None):
    """
    便捷函数：验证股票数据
    
    使用示例:
        result = verify_stock('601985', '中国核电')
        if result['verified']:
            print(f"价格: ¥{result['data']['price']}")
        else:
            print(f"验证失败: {result['errors']}")
    """
    verifier = StockDataVerifier()
    return verifier.verify(code, expected_name)


if __name__ == '__main__':
    # 测试验证流程
    print('=' * 70)
    print('🧪 数据验证模块测试')
    print('=' * 70)
    print()
    
    # 测试1: 正确的股票
    print('测试1: 中国核电 (601985)')
    result = verify_stock('601985', '中国核电')
    print(f"结果: {'✅ 通过' if result['verified'] else '❌ 失败'}")
    if result['verified']:
        print(f"数据: {result['data']}")
    else:
        print(f"错误: {result['errors']}")
    print()
    
    # 测试2: 名称不匹配
    print('测试2: 名称不匹配测试 (601985, 错误名称)')
    result = verify_stock('601985', '招商银行')
    print(f"结果: {'✅ 通过' if result['verified'] else '❌ 失败'}")
    if not result['verified']:
        print(f"错误: {result['errors']}")
    print()
    
    # 测试3: 错误代码
    print('测试3: 错误代码 (999999)')
    result = verify_stock('999999')
    print(f"结果: {'✅ 通过' if result['verified'] else '❌ 失败'}")
    if not result['verified']:
        print(f"错误: {result['errors']}")
    print()
    
    print('=' * 70)
    print('测试完成')
    print('=' * 70)

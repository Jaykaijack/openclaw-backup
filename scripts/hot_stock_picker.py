#!/usr/bin/env python3
"""
二郎量化选股系统 V2 - 热度导向
加入热点板块因子
"""

import sys
sys.path.insert(0, 'scripts')
from stock_data_api import StockDataAPI

def main():
    print('=' * 70)
    print('🔥 二郎量化选股系统 V2 - 加入热度因子')
    print('=' * 70)
    print()

    stock_api = StockDataAPI()

    # 当前热点板块的代表股（基于近期市场热点）
    hot_sectors = {
        'AI算力/DeepSeek': ['000938', '300033', '300059', '002230', '603019'],
        '机器人': ['002527', '002896', '300124', '603728', '002931'],
        '半导体/芯片': ['688981', '002371', '603501', '300782', '600584'],
        '新能源/固态电池': ['300750', '002594', '300014', '002074', '002709'],
        '低空经济': ['002151', '300900', '002097', '600038', '000099'],
        '军工': ['000547', '600893', '600372', '600760', '000768'],
        '消费复苏': ['600519', '000858', '002304', '600887', '000568'],
    }

    # 获取所有热点股行情
    all_hot_codes = []
    for sector, codes in hot_sectors.items():
        all_hot_codes.extend(codes)

    print('📊 获取热点板块股票行情...')
    quotes = stock_api.get_qq_quotes(all_hot_codes)
    print(f'   成功获取 {len(quotes)} 只热点股行情')
    print()

    # 新评分体系：热度优先
    print('🧮 评分规则（热度导向）：')
    print('   涨跌幅因子: 强势上涨 +30分（>3%），温和上涨 +20分（0-3%）')
    print('   换手率因子: 高换手 +25分（>5%），活跃 +15分（2-5%）')
    print('   资金流向: 主动买入占优 +25分（外盘>55%）')
    print('   板块热度: 当前风口 +20分')
    print('   成交量: 放量 +10分')
    print()

    scored_stocks = []

    for code, info in quotes.items():
        score = 0
        factors = []
        sector_name = '其他'
        
        # 确定所属板块
        for sector, codes in hot_sectors.items():
            if code.replace('sh', '').replace('sz', '') in codes:
                sector_name = sector
                break
        
        change_pct = info.get('change_pct', 0)
        turnover = info.get('turnover', 0)
        outer = info.get('outer_vol', 0)
        inner = info.get('inner_vol', 0)
        volume = info.get('volume', 0)
        
        # 因子1: 涨跌幅（强势优先）
        if change_pct > 5:
            score += 30
            factors.append(f'强势上涨({change_pct:+.1f}%)')
        elif change_pct > 3:
            score += 25
            factors.append(f'强势上涨({change_pct:+.1f}%)')
        elif change_pct > 0:
            score += 20
            factors.append(f'温和上涨({change_pct:+.1f}%)')
        elif change_pct > -2:
            score += 10
            factors.append(f'回调低吸({change_pct:+.1f}%)')
        else:
            score += 5
            factors.append(f'深度回调({change_pct:+.1f}%)')
        
        # 因子2: 换手率（活跃度）
        if turnover > 10:
            score += 25
            factors.append(f'极高换手({turnover:.1f}%)')
        elif turnover > 5:
            score += 20
            factors.append(f'高换手活跃({turnover:.1f}%)')
        elif turnover > 2:
            score += 15
            factors.append(f'换手活跃({turnover:.1f}%)')
        else:
            score += 5
            factors.append(f'换手偏低({turnover:.1f}%)')
        
        # 因子3: 资金流向
        if outer + inner > 0:
            outer_ratio = outer / (outer + inner) * 100
            if outer_ratio > 60:
                score += 25
                factors.append(f'资金抢筹({outer_ratio:.1f}%)')
            elif outer_ratio > 55:
                score += 20
                factors.append(f'资金流入({outer_ratio:.1f}%)')
            elif outer_ratio > 50:
                score += 10
                factors.append(f'资金平衡({outer_ratio:.1f}%)')
            else:
                factors.append(f'资金流出({outer_ratio:.1f}%)')
        
        # 因子4: 板块热度
        if sector_name in ['AI算力/DeepSeek', '机器人', '低空经济']:
            score += 20
            factors.append(f'{sector_name}')
        elif sector_name in ['半导体/芯片', '新能源/固态电池']:
            score += 15
            factors.append(f'{sector_name}')
        else:
            score += 10
            factors.append(f'{sector_name}')
        
        # 因子5: 成交量
        if volume > 2000000:
            score += 10
            factors.append('巨量成交')
        elif volume > 1000000:
            score += 5
            factors.append('成交量大')
        
        scored_stocks.append({
            'code': code,
            'name': info.get('name', ''),
            'sector': sector_name,
            'score': score,
            'factors': factors,
            'price': info.get('current', 0),
            'change_pct': change_pct,
            'turnover': turnover,
            'pe': info.get('pe'),
            'pb': info.get('pb'),
            'volume': volume
        })

    # 按评分排序
    scored_stocks.sort(key=lambda x: x['score'], reverse=True)

    # 按板块分组展示
    print('=' * 70)
    print('🏆 热点板块龙头股排名')
    print('=' * 70)

    for sector in ['AI算力/DeepSeek', '机器人', '半导体/芯片', '新能源/固态电池', '低空经济', '军工']:
        sector_stocks = [s for s in scored_stocks if s['sector'] == sector]
        if sector_stocks:
            print(f'\n📌 {sector}')
            print('-' * 50)
            for i, s in enumerate(sector_stocks[:3], 1):
                hot_mark = '🔥' if s['score'] >= 90 else '⭐' if s['score'] >= 80 else ''
                print(f"  {i}. {s['code']} {s['name']} {hot_mark}")
                print(f"     评分:{s['score']} | ¥{s['price']:.2f} ({s['change_pct']:+.2f}%) | 换手:{s['turnover']:.1f}%")

    # 最终推荐（评分>=80）
    print('\n' + '=' * 70)
    print('🎯 明日重点攻击目标（热度评分≥80分）')
    print('=' * 70)

    recommendations = [s for s in scored_stocks if s['score'] >= 80]
    if recommendations:
        for i, s in enumerate(recommendations[:5], 1):
            print(f"\n{i}. 🔥 {s['code']} {s['name']} [{s['sector']}]")
            print(f"   热度评分: {s['score']}/100")
            print(f"   当前价格: ¥{s['price']:.2f} ({s['change_pct']:+.2f}%)")
            print(f"   换手率: {s['turnover']:.2f}% | 成交量: {s['volume']/10000:.0f}万手")
            key_factors = [f for f in s['factors'] if '强势' in f or '资金' in f or '换手' in f][:3]
            print(f"   核心亮点: {' | '.join(key_factors)}")
    else:
        print('\n⚠️ 暂无评分≥80的高热度标的')

    # 短线博弈标的（高换手+强势）
    print('\n' + '=' * 70)
    print('⚡ 短线博弈标的（高换手+强势）')
    print('=' * 70)
    
    short_term = [s for s in scored_stocks if s['turnover'] > 5 and s['change_pct'] > 0]
    short_term.sort(key=lambda x: x['turnover'] * x['change_pct'], reverse=True)
    
    for i, s in enumerate(short_term[:5], 1):
        print(f"\n{i}. {s['code']} {s['name']} [{s['sector']}]")
        print(f"   价格: ¥{s['price']:.2f} (+{s['change_pct']:.1f}%) | 换手: {s['turnover']:.1f}%")
        print(f"   策略: 早盘强势可追，放量突破跟进")

    print('\n' + '=' * 70)
    print('⚠️ 风险提示：热度选股波动大，建议严格止损')
    print('=' * 70)

if __name__ == '__main__':
    main()

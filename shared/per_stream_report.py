#!/usr/bin/env python3
"""per_stream_report.py — оценка каждой стратегии по live данным.

Запускается после возвращения с отдыха. Группирует closed_trades по stream,
показывает live vs backtest для каждой.
"""
import json
import sys
from collections import defaultdict
import numpy as np

import platform
# Auto-detect path: Windows local vs Linux VPS
if platform.system() == 'Windows':
    STATE_PATH = r'D:\OnChain\scripts\wallet_v2\sniper_state.json'
else:
    STATE_PATH = '/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json'

# Backtest baselines (для сравнения live vs backtest)
BACKTEST_BASELINES = {
    # Tier 1 — V5 (full universe backtest)
    'V5_strong':       {'expected_pnl': 153, 'expected_wr': 57, 'expected_big': 16, 'expected_rug': 0},
    'V5_broad':        {'expected_pnl': 161, 'expected_wr': 57, 'expected_big': 16, 'expected_rug': 0},
    'V3_GRAIL_D':      {'expected_pnl': 59,  'expected_wr': 38, 'expected_big': 7,  'expected_rug': 0},
    'CLEAN_SMART':     {'expected_pnl': 58,  'expected_wr': 38, 'expected_big': 7,  'expected_rug': 0},
    'MOMENTUM_15':     {'expected_pnl': 42,  'expected_wr': 58, 'expected_big': 5,  'expected_rug': 0},
    # Wave 8 grail
    'V3_GRAIL_A':      {'expected_pnl': 52,  'expected_wr': 75, 'expected_big': 9,  'expected_rug': 0},
    'V3_GRAIL_B':      {'expected_pnl': 10,  'expected_wr': 76, 'expected_big': 0,  'expected_rug': 0},
    'V3_GRAIL_C':      {'expected_pnl': -7,  'expected_wr': 40, 'expected_big': 0,  'expected_rug': 0},
    # Wave 7 ML rules
    'ML_RULE_A':       {'expected_pnl': 357, 'expected_wr': 83, 'expected_big': 42, 'expected_rug': 0},
    'ML_RULE_B':       {'expected_pnl': 228, 'expected_wr': 92, 'expected_big': 64, 'expected_rug': 4},
    'ML_RULE_C':       {'expected_pnl': 181, 'expected_wr': 80, 'expected_big': 57, 'expected_rug': 13},
    'ML_SCORER':       {'expected_pnl': 187, 'expected_wr': 75, 'expected_big': 45, 'expected_rug': 9},
    # Wave 6 TIER
    'TIER_MEGA2K_GOLD':{'expected_pnl': 2157,'expected_wr': 100,'expected_big': 100,'expected_rug': 0},
    'HUGE_PURE':       {'expected_pnl': 1567,'expected_wr': 100,'expected_big': 100,'expected_rug': 0},
    'TIER_1K_2K':      {'expected_pnl': 76,  'expected_wr': 100,'expected_big': 0,  'expected_rug': 0},
    'TIER_500_1K_V2':  {'expected_pnl': 119, 'expected_wr': 38, 'expected_big': 25, 'expected_rug': 50},
    'TIER_500_1K_BC20':{'expected_pnl': 167, 'expected_wr': 65, 'expected_big': 53, 'expected_rug': 24},
    'TIER_300_500':    {'expected_pnl': -39, 'expected_wr': 28, 'expected_big': 6,  'expected_rug': 53},
    # Wave 4-5
    'FRESH_3MIN':      {'expected_pnl': 279, 'expected_wr': 26, 'expected_big': 30, 'expected_rug': 33},
    'FRESH_GOLD':      {'expected_pnl': 83,  'expected_wr': 40, 'expected_big': 25, 'expected_rug': 20},
    'FRESH_WHALE':     {'expected_pnl': 650, 'expected_wr': 50, 'expected_big': 70, 'expected_rug': 15},
    # Old streams
    'GOLD3':           {'expected_pnl': 424, 'expected_wr': 63, 'expected_big': 50, 'expected_rug': 5},
    'WHALE':           {'expected_pnl': 394, 'expected_wr': 52, 'expected_big': 45, 'expected_rug': 12},
    'LATE':            {'expected_pnl': 348, 'expected_wr': 62, 'expected_big': 40, 'expected_rug': 15},
    'LOWCAP':          {'expected_pnl': 343, 'expected_wr': 46, 'expected_big': 35, 'expected_rug': 17},
}


def main():
    with open(STATE_PATH, encoding='utf-8') as f:
        state = json.load(f)
    ct = state.get('closed_trades', [])
    print(f'Total closed_trades: {len(ct)}')
    if not ct:
        print('No data')
        return

    # Group by stream
    by_stream = defaultdict(list)
    for t in ct:
        s = t.get('stream') or 'UNKNOWN'
        by_stream[s].append(t)

    # Aggregate
    rows = []
    for stream, trades in by_stream.items():
        n = len(trades)
        if n < 1:
            continue
        pnls = [t.get('pnl_pct', 0) or 0 for t in trades]
        avg = float(np.mean(pnls))
        wr = sum(1 for p in pnls if p > 0) / n * 100
        rug = sum(1 for p in pnls if p <= -50) / n * 100
        big = sum(1 for p in pnls if p >= 100) / n * 100
        huge = sum(1 for p in pnls if p >= 500) / n * 100
        max_w = max(pnls)
        max_l = min(pnls)
        total_pnl = sum(pnls)
        # Compare to backtest baseline
        bb = BACKTEST_BASELINES.get(stream, {})
        exp_pnl = bb.get('expected_pnl')
        exp_wr = bb.get('expected_wr')
        if exp_pnl is not None:
            verdict_pnl = avg - exp_pnl  # positive = better than backtest
            verdict_wr = wr - exp_wr if exp_wr is not None else 0
        else:
            verdict_pnl = None
            verdict_wr = None
        rows.append({
            'stream': stream, 'n': n, 'avg': avg, 'wr': wr, 'rug': rug, 'big': big, 'huge': huge,
            'max_w': max_w, 'max_l': max_l, 'total': total_pnl,
            'exp_pnl': exp_pnl, 'verdict_pnl': verdict_pnl, 'verdict_wr': verdict_wr,
        })

    rows.sort(key=lambda r: -(r['total']))

    # Print
    print()
    print('=' * 160)
    print(f'{"stream":<25} {"n":>5} {"avg":>7} {"WR":>5} {"rug":>5} {"big":>5} {"huge":>6} {"maxW":>7} {"maxL":>7} {"total":>9} {"vs_bt_pnl":>10} {"vs_bt_wr":>10} {"verdict":<10}')
    print('=' * 160)
    keep = []; drop = []; suspect = []; unknown = []
    for r in rows:
        v_pnl = r['verdict_pnl']
        v_wr = r['verdict_wr']
        if v_pnl is None:
            verdict = 'UNKNOWN'
            unknown.append(r)
        elif r['n'] < 5:
            verdict = 'WEAK_N'
            suspect.append(r)
        elif v_pnl >= 0 and r['rug'] <= r.get('rug_expected', 30):
            verdict = 'KEEP'
            keep.append(r)
        elif v_pnl < -30:
            verdict = 'DROP'
            drop.append(r)
        else:
            verdict = 'SUSPECT'
            suspect.append(r)
        v_pnl_str = f'{v_pnl:+.0f}%' if v_pnl is not None else 'n/a'
        v_wr_str = f'{v_wr:+.0f}pp' if v_wr is not None else 'n/a'
        print(f'{r["stream"]:<25} {r["n"]:>5} {r["avg"]:>+6.0f}% {r["wr"]:>4.0f}% {r["rug"]:>4.0f}% {r["big"]:>4.0f}% {r["huge"]:>5.0f}% {r["max_w"]:>+6.0f}% {r["max_l"]:>+6.0f}% {r["total"]:>+8.0f}% {v_pnl_str:>9} {v_wr_str:>9} {verdict:<10}')

    # Summary
    print()
    print('=' * 100)
    print(f'SUMMARY: {len(keep)} KEEP, {len(suspect)} SUSPECT (need more data), {len(drop)} DROP, {len(unknown)} UNKNOWN (no backtest)')
    print('=' * 100)
    print()
    print('=== RECOMMENDED ACTIONS ===')
    print()
    print('KEEP (continue or increase size):')
    for r in sorted(keep, key=lambda x: -x['total'])[:10]:
        print(f'  {r["stream"]:<25} n={r["n"]:>4} avg={r["avg"]:+.0f}% (vs backtest {r["verdict_pnl"]:+.0f}%) total={r["total"]:+.0f}%')
    print()
    print('SUSPECT (continue collecting, do not size up):')
    for r in sorted(suspect, key=lambda x: -x['total'])[:10]:
        print(f'  {r["stream"]:<25} n={r["n"]:>4} avg={r["avg"]:+.0f}% (vs backtest {(r["verdict_pnl"] or 0):+.0f}%) total={r["total"]:+.0f}%')
    print()
    print('DROP (disable in serial_sniper.js paperChecks):')
    for r in sorted(drop, key=lambda x: x['verdict_pnl'])[:10]:
        print(f'  {r["stream"]:<25} n={r["n"]:>4} avg={r["avg"]:+.0f}% (vs backtest {r["verdict_pnl"]:+.0f}%) total={r["total"]:+.0f}%')

    # Save report
    with open(r'D:\OnChain\deploy\shared\per_stream_report.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_trades': len(ct),
            'streams_evaluated': len(rows),
            'rows': rows,
            'keep': [r['stream'] for r in keep],
            'suspect': [r['stream'] for r in suspect],
            'drop': [r['stream'] for r in drop],
            'unknown': [r['stream'] for r in unknown],
        }, f, indent=2)
    print()
    print('Saved: D:/OnChain/deploy/shared/per_stream_report.json')


if __name__ == '__main__':
    main()

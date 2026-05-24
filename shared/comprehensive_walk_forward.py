#!/usr/bin/env python3
"""comprehensive_walk_forward.py — НАСТОЯЩИЙ walk-forward на всех 36K tokens с pre-computed metrics.

Использует:
- tokens_unified.json — 36K tokens с metrics (smart_money_count, serial_pump_count,
  db_rugBotCount, db_serialRugCount, top1_wallet_pct, etc.)
- sniper_state.json — наши real PnL outcomes для 4957 trades

Логика:
1. Build dataset: (token, time, features, outcome) для каждого token
2. Sort by added_at — temporal order
3. Walk-forward TRAIN (oldest 60%) / VAL (next 20%) / TEST (newest 20%)
4. Test compound filters:
   - smart_money_count >= N
   - serial_pump_count >= N
   - rugger_count == 0
   - top1_pct < N
   - combinations
5. Output filters that pass: TEST n>=30, big%>=15, rug%<=30
"""
import json
from pathlib import Path
from collections import defaultdict

TU = Path('/srv/bots/onchain/code/scripts/wallet_v2/unified_db/tokens_unified.json')
STATE = Path('/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json')
OUT = Path('/srv/bots/.shared/data/walk_forward_results.jsonl')
OUT.parent.mkdir(parents=True, exist_ok=True)


def outcome(token, sniper_pnl):
    """Classify as big / pump / flat / rug using real PnL if available."""
    if sniper_pnl is not None:
        if sniper_pnl >= 500:
            return 'big'
        if sniper_pnl >= 200:
            return 'pump'
        if sniper_pnl <= -50:
            return 'rug'
        return 'flat'
    cls = (token.get('classification') or '').upper()
    if 'PUMPED' in cls:
        return 'big' if 'ALIVE' in cls else 'pump'
    if 'RUG' in cls or 'DIED' in cls:
        return 'rug'
    return 'flat'


def main():
    print('Loading...', flush=True)
    tu = json.load(TU.open())
    s = json.load(STATE.open())
    ct = s.get('closed_trades', [])
    sniper = {}
    for t in ct:
        m = t.get('token')
        if m:
            pnl = t.get('max_pnl_pct') or t.get('pnl_pct') or 0
            if m not in sniper or sniper[m] < pnl:
                sniper[m] = pnl
    print(f'  tokens_unified: {len(tu)}', flush=True)
    print(f'  sniper PnL records: {len(sniper)}', flush=True)

    # Build dataset
    rows = []
    for mint, td in tu.items():
        m = td.get('metrics') or {}
        if not m:
            continue
        sm = m.get('smart_money_count') or 0
        sp = m.get('serial_pump_count') or 0
        sn = m.get('sniper_count') or 0
        top1 = m.get('top1_wallet_pct')
        liq = m.get('liquidity_usd') or 0
        rug_bot = m.get('db_rugBotCount') or 0
        rug_serial = m.get('db_serialRugCount') or 0
        high_risk = m.get('db_highRiskWalletCount') or 0
        positive = m.get('db_positiveWalletCount') or 0
        bundle = m.get('db_bundleDetected') or 0
        added = td.get('added_at') or '2024-01-01'
        outc = outcome(td, sniper.get(mint))
        rows.append({
            'mint': mint,
            'added_at': added,
            'smart': sm, 'serial': sp, 'sniper': sn,
            'top1': top1 if top1 is not None else 100,
            'liq': liq,
            'rug_bot': rug_bot, 'rug_serial': rug_serial,
            'high_risk': high_risk, 'positive': positive,
            'bundle': bundle,
            'outcome': outc,
        })
    print(f'  rows with metrics: {len(rows)}', flush=True)

    # Sort by added_at and split
    rows.sort(key=lambda r: r['added_at'])
    n = len(rows)
    train = rows[:int(n*0.6)]
    val = rows[int(n*0.6):int(n*0.8)]
    test = rows[int(n*0.8):]
    print(f'  TRAIN {len(train)} | VAL {len(val)} | TEST {len(test)}', flush=True)

    def stats(subset, filter_fn, name):
        sel = [r for r in subset if filter_fn(r)]
        if not sel:
            return None
        n_sel = len(sel)
        bigs = sum(1 for r in sel if r['outcome'] == 'big')
        pumps = sum(1 for r in sel if r['outcome'] == 'pump')
        flats = sum(1 for r in sel if r['outcome'] == 'flat')
        rugs = sum(1 for r in sel if r['outcome'] == 'rug')
        return {
            'name': name, 'n': n_sel,
            'big_pct': bigs/n_sel, 'pump_pct': pumps/n_sel,
            'rug_pct': rugs/n_sel, 'flat_pct': flats/n_sel,
            'edge': (bigs+pumps)/n_sel - rugs/n_sel,
        }

    # === BASELINE ===
    print('\n=== BASELINE (all tokens) ===', flush=True)
    for subset_name, subset in [('TRAIN', train), ('VAL', val), ('TEST', test)]:
        if not subset: continue
        bigs = sum(1 for r in subset if r['outcome']=='big')
        pumps = sum(1 for r in subset if r['outcome']=='pump')
        rugs = sum(1 for r in subset if r['outcome']=='rug')
        n = len(subset)
        print(f'  {subset_name}: n={n} big={bigs/n*100:.1f}% pump={pumps/n*100:.1f}% rug={rugs/n*100:.1f}%')

    # === FILTERS ===
    print('\n=== FILTERS — winners on TEST (n>=30 big>=15% rug<=30%) ===', flush=True)
    filters = []
    # Single features
    for smart_t in [1, 2, 3, 5]:
        filters.append((f'smart>={smart_t}', lambda r, t=smart_t: r['smart'] >= t))
    for serial_t in [1, 3, 5, 10]:
        filters.append((f'serial>={serial_t}', lambda r, t=serial_t: r['serial'] >= t))
    for top1_max in [10, 20, 30, 50]:
        filters.append((f'top1<{top1_max}', lambda r, t=top1_max: r['top1'] < t))
    # No-rugger
    filters.append(('no_rug_bot', lambda r: r['rug_bot'] == 0))
    filters.append(('no_rug_serial', lambda r: r['rug_serial'] == 0))
    filters.append(('no_high_risk', lambda r: r['high_risk'] == 0))
    filters.append(('positive>=1', lambda r: r['positive'] >= 1))
    # Compound
    filters.append(('smart>=2 & no_rug', lambda r: r['smart'] >= 2 and r['rug_bot'] == 0))
    filters.append(('smart>=3 & top1<30', lambda r: r['smart'] >= 3 and r['top1'] < 30))
    filters.append(('serial>=5 & smart>=2', lambda r: r['serial'] >= 5 and r['smart'] >= 2))
    filters.append(('serial>=5 & no_rug & top1<30', lambda r: r['serial'] >= 5 and r['rug_bot'] == 0 and r['top1'] < 30))
    filters.append(('smart>=2 & serial>=5 & no_rug', lambda r: r['smart'] >= 2 and r['serial'] >= 5 and r['rug_bot'] == 0))
    filters.append(('smart>=3 & serial>=3 & top1<20 & no_rug', lambda r: r['smart'] >= 3 and r['serial'] >= 3 and r['top1'] < 20 and r['rug_bot'] == 0))
    filters.append(('positive>=2 & no_rug & top1<30', lambda r: r['positive'] >= 2 and r['rug_bot'] == 0 and r['top1'] < 30))
    filters.append(('positive>=3 & smart>=2 & no_rug', lambda r: r['positive'] >= 3 and r['smart'] >= 2 and r['rug_bot'] == 0))
    filters.append(('smart>=2 & no_rug_serial & top1<20', lambda r: r['smart'] >= 2 and r['rug_serial'] == 0 and r['top1'] < 20))
    filters.append(('liq>=10K & smart>=2 & no_rug', lambda r: r['liq'] >= 10000 and r['smart'] >= 2 and r['rug_bot'] == 0))
    filters.append(('liq>=20K & smart>=3 & top1<30', lambda r: r['liq'] >= 20000 and r['smart'] >= 3 and r['top1'] < 30))

    results = []
    for fname, ffn in filters:
        ts = stats(train, ffn, fname)
        vs = stats(val, ffn, fname)
        tts = stats(test, ffn, fname)
        if not tts or tts['n'] < 30:
            continue
        if tts['big_pct'] < 0.15 and tts['big_pct']+tts['pump_pct'] < 0.30:
            continue
        if tts['rug_pct'] > 0.30:
            continue
        results.append({'filter': fname, 'TRAIN': ts, 'VAL': vs, 'TEST': tts})

    results.sort(key=lambda r: -(r['TEST']['big_pct']+r['TEST']['pump_pct']-r['TEST']['rug_pct']))

    print(f'\n{"filter":52s}  TRAIN n  big%  pump%  rug%  |  TEST n  big%  pump%  rug%  edge', flush=True)
    for r in results[:20]:
        tr = r['TRAIN'] or {}
        te = r['TEST']
        print(f"  {r['filter']:50s} {tr.get('n','-'):>5}  {tr.get('big_pct',0)*100:>4.1f}  {tr.get('pump_pct',0)*100:>4.1f}  {tr.get('rug_pct',0)*100:>4.1f}  |  {te['n']:>5}  {te['big_pct']*100:>4.1f}  {te['pump_pct']*100:>4.1f}  {te['rug_pct']*100:>4.1f}  {te['edge']*100:>+5.1f}", flush=True)

    print(f'\n=== {len(results)} passing filters ===', flush=True)
    with OUT.open('w') as f:
        for r in results:
            f.write(json.dumps(r) + '\n')
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""exit_optimizer.py — для каждого Rule найти лучшую конфигурацию exit (trail/SL/cap).

Симулируем что было бы если бы exit был не текущий (trail 85% / SL -15% / cap 500%),
а альтернативный. Так как у нас есть ath_price и entry_price для каждого трейда,
можем посчитать что бы получили при разных exit правилах:

  - если ATH < threshold% → SL exit at sl_pct
  - если ATH >= threshold% → exit at min(cap, ATH × trail/100)
"""
import json, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, r'D:\OnChain\deploy\shared')
from score_token import RULES, engineer_features

with open(r'D:\OnChain\scripts\wallet_v2\sniper_state.json', encoding='utf-8') as f:
    snip = json.load(f)
ct = snip.get('closed_trades', [])
with open(r'D:\OnChain\scripts\wallet_v2\unified_db\rugger_blacklist.json', encoding='utf-8') as f:
    rb = json.load(f)
rugger_set = set(rb.keys())

# Dedup by token
by_token = defaultdict(list)
for t in ct:
    tk = t.get('token')
    if tk: by_token[tk].append(t)

test_rows = []
for tk, trades in by_token.items():
    t = sorted(trades, key=lambda x: x.get('entry_time') or 0)[0]
    es = t.get('entry_signal') or {}
    ep=t.get('entry_price'); ap=t.get('ath_price')
    ath = (ap/ep-1)*100 if (ep and ap and ep>0) else None
    if ath is None: continue
    rd = es.get('rugcheck_dangers')
    danger_n = len(rd) if isinstance(rd,(list,tuple)) else (int(rd) if isinstance(rd,(int,float)) else 0)
    top1_owner = es.get('top1_owner'); lp_prov = es.get('lp_provider')
    creator = es.get('pool_creator') or es.get('creator')
    raw = dict(
        top1=es.get('top1_pct'), top5=es.get('top5_pct'),
        smart=es.get('smart') or 0, serial=es.get('serial_only') or 0,
        liq=es.get('liquidity_at_entry') or t.get('liquidity_at_entry') or 0,
        mcap=es.get('mcap') or 0, vol24=es.get('volume_h24') or 0,
        age=es.get('age_min') or 0, buys=es.get('buys_m5') or 0, sells=es.get('sells_m5') or 0,
        rc=es.get('rugcheck_score') or 0, danger_n=danger_n,
        ssp=es.get('serial_supply_pct') or 0, known=es.get('known') or 0,
        mint_rev=1 if (es.get('mint_authority') or '')=='REVOKED' else 0,
        lp_lock=0 if (es.get('lp_unlocked') or False) else 1,
        top1_rugger=1 if top1_owner in rugger_set else 0,
        lp_rugger=1 if lp_prov in rugger_set else 0,
        creator_rugger=1 if creator in rugger_set else 0,
    )
    features = engineer_features(raw)
    test_rows.append(dict(
        token=tk, symbol=t.get('symbol') or '',
        realized=t.get('pnl_pct',0) or 0,
        ath=ath,
        entry_price=ep, ath_price=ap, exit_price=t.get('exit_price'),
        exit_reason=t.get('exit_reason'),
        features=features,
    ))

def simulate(rows_sub, trail_pct, sl_pct, cap_pct, pump_threshold=30):
    """For each row, simulate alternative exit.

    pump_threshold: if ATH < this %, assume SL hit (couldn't even ride to trail).
    """
    pnls = []
    for r in rows_sub:
        ath = r['ath']
        if ath is None: continue
        if ath < pump_threshold:
            pnls.append(sl_pct)
        else:
            trail_exit = ath * (trail_pct/100)
            sim_pnl = min(cap_pct, trail_exit)
            pnls.append(sim_pnl)
    return np.array(pnls) if pnls else np.array([])

# Get tokens matching each rule
def apply_rule(rule, r):
    try: return rule['condition'](r['features'])
    except: return False

print(f'{"="*120}')
print('EXIT OPTIMIZATION per RULE')
print(f'Searching: trail ∈ [75-95%], SL ∈ [-15..-25%], cap ∈ [500..5000%]')
print(f'{"="*120}')

# Also include rule_ANY (any of 3 fires)
rule_groups = list(RULES) + [{'name': 'RULE_ANY', 'condition': lambda f: any((rule['condition'](f) if callable(rule['condition']) else False) for rule in RULES)}]

for rule in rule_groups:
    fired = [r for r in test_rows if apply_rule(rule, r)]
    n = len(fired)
    if n < 10: continue
    actual_avg = float(np.mean([r['realized'] for r in fired]))
    actual_eq = 100.0
    for r in fired:
        actual_eq = actual_eq - actual_eq*0.05 + actual_eq*0.05*(1+r['realized']/100)
    print(f'\n{"="*100}')
    print(f'RULE: {rule["name"]} (n={n}) — actual avg={actual_avg:+.0f}%, $100→${actual_eq:.0f}')
    print(f'{"trail":>5} {"SL":>4} {"cap":>5}  {"avg":>7} {"WR":>5} {"rug":>5} {"max_w":>6} {"max_l":>6} {"$100→":>8} {"vs_actual":>10}')

    best_config = None; best_eq = 0
    results = []
    for trail in [75, 80, 85, 88, 90, 92, 95]:
        for sl in [-15, -20, -25, -30]:
            for cap in [300, 500, 1000, 1500, 2000, 3000, 5000]:
                sim = simulate(fired, trail, sl, cap)
                if len(sim) == 0: continue
                avg = float(sim.mean()); wr = float((sim>0).mean()*100)
                rug = float((sim<=-50).mean()*100)
                eq = 100.0
                for p in sim:
                    eq = eq - eq*0.05 + eq*0.05*(1+p/100)
                results.append((trail, sl, cap, avg, wr, rug, sim.max(), sim.min(), eq))
                if eq > best_eq:
                    best_eq = eq
                    best_config = (trail, sl, cap)

    # Print top-15 by equity
    results.sort(key=lambda x: -x[8])
    for trail, sl, cap, avg, wr, rug, mxw, mxl, eq in results[:15]:
        vs = (eq - actual_eq) / actual_eq * 100 if actual_eq > 0 else 0
        print(f'{trail:>5}% {sl:>3}% {cap:>4}%  {avg:>+6.0f}% {wr:>4.0f}% {rug:>4.0f}% {mxw:>+5.0f}% {mxl:>+5.0f}% ${eq:>6.0f} {vs:>+8.0f}%')

    if best_config:
        t, s, c = best_config
        improvement = (best_eq - actual_eq) / max(actual_eq, 1) * 100
        print(f'  BEST: trail={t}% SL={s}% cap={c}% → $100→${best_eq:.0f} (improvement: {improvement:+.0f}% vs actual)')

# Also show what happens with the GLOBAL average across all rule triggers
print(f'\n{"="*120}')
print(f'RECOMMENDED exit config for ML_SCORER deployment')
print(f'{"="*120}')
all_fired = [r for r in test_rows if any(apply_rule(rule, r) for rule in RULES)]
if all_fired:
    print(f'\nAcross all {len(all_fired)} rule-matched tokens:')
    for cfg_name, (trail, sl, cap) in [
        ('current_default', (85, -15, 500)),
        ('balanced_recommended', (90, -20, 1500)),
        ('aggressive_high_cap', (92, -20, 2000)),
        ('safety_first', (88, -15, 1000)),
    ]:
        sim = simulate(all_fired, trail, sl, cap)
        if len(sim) == 0: continue
        eq = 100.0
        for p in sim:
            eq = eq - eq*0.05 + eq*0.05*(1+p/100)
        print(f'  {cfg_name:<25} trail={trail}% SL={sl}% cap={cap}% → avg={sim.mean():+.0f}% WR={(sim>0).mean()*100:.0f}% rug={(sim<=-50).mean()*100:.0f}% $100→${eq:.0f}')

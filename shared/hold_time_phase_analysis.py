#!/usr/bin/env python3
"""hold_time_phase_analysis.py — market phase / hold-time / exit-timing анализ.

Вопросы:
1. На какой минуте hold_min winners vs losers расходятся?
2. Когда уже можно сказать "не пампанётся, выходим"?
3. Когда уже можно сказать "пампанулся, забираем"?
4. Какая фаза рынка дает больше bigs? (день/час/неделя)
"""
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import numpy as np

with open(r'D:\OnChain\scripts\wallet_v2\sniper_state.json', encoding='utf-8') as f:
    snip = json.load(f)
ct = snip.get('closed_trades', [])

def parse_dt(v):
    if isinstance(v, (int, float)):
        return datetime.utcfromtimestamp(v/1000 if v>1e12 else v)
    if isinstance(v, str):
        try: return datetime.fromisoformat(v.replace('Z','+00:00')).replace(tzinfo=None)
        except: return None
    return None

rows = []
for t in ct:
    ep = t.get('entry_price'); ap = t.get('ath_price'); xp = t.get('exit_price')
    pnl = t.get('pnl_pct', 0) or 0
    hold = t.get('hold_min')
    if not (ep and ap and ep > 0 and hold is not None): continue
    ath = (ap/ep - 1)*100
    dt = parse_dt(t.get('entry_time'))
    rows.append(dict(
        symbol=t.get('symbol'), realized=pnl, ath=ath, hold_min=hold,
        exit_reason=t.get('exit_reason'), dt=dt,
        chain=(t.get('chain') or '?').lower(),
        stream=t.get('stream') or '?',
    ))

N = len(rows)
print(f'Total rows: {N}')
print(f'Outcomes: huges(ATH≥500%)={sum(1 for r in rows if r["ath"]>=500)}, '
      f'bigs={sum(1 for r in rows if r["ath"]>=100)}, '
      f'losers(realized<=-20%)={sum(1 for r in rows if r["realized"]<=-20)}')
print()

# === STAGE 1: HOLD-TIME by OUTCOME ===
print('='*100)
print('STAGE 1: HOLD-TIME distribution by outcome')
print('='*100)
buckets = [
    ('rug (realized<=-50)', lambda r: r['realized'] <= -50),
    ('small loss (-50,-20]', lambda r: -50 < r['realized'] <= -20),
    ('break-even (-20,+20]', lambda r: -20 < r['realized'] <= 20),
    ('small win (20,100]', lambda r: 20 < r['realized'] <= 100),
    ('big (100,500]', lambda r: 100 < r['realized'] <= 500),
    ('huge (>=500%)', lambda r: r['realized'] >= 500),
]
print(f'{"bucket":<25} {"n":>5} {"hold p25":>9} {"median":>8} {"p75":>6} {"p90":>6} {"max":>6}')
for name, fn in buckets:
    sub = [r['hold_min'] for r in rows if fn(r)]
    if not sub: continue
    print(f'{name:<25} {len(sub):>5} {int(np.percentile(sub,25)):>8}m {int(np.percentile(sub,50)):>7}m {int(np.percentile(sub,75)):>5}m {int(np.percentile(sub,90)):>5}m {int(max(sub)):>5}m')

# === STAGE 2: AT EACH MINUTE, what's the distribution of outcomes for trades STILL HELD? ===
print()
print('='*100)
print('STAGE 2: Survival analysis — at minute X, what % of held trades end up as bigs/rugs?')
print('='*100)
print(f'{"min_held":<10} {"n_active":>9} {"%bigs_future":>13} {"%rugs_future":>13} {"%huges_future":>14}')
for cut in [1, 2, 3, 5, 7, 10, 15, 20, 30, 45, 60, 90, 120, 180, 240, 360, 720]:
    # rows still active at this minute (hold >= cut)
    still_held = [r for r in rows if r['hold_min'] >= cut]
    if len(still_held) < 30: continue
    bigs_future = sum(1 for r in still_held if r['ath'] >= 200)
    huges_future = sum(1 for r in still_held if r['ath'] >= 500)
    rugs_future = sum(1 for r in still_held if r['realized'] <= -50)
    print(f'{cut:<10} {len(still_held):>9} {100*bigs_future/len(still_held):>11.1f}% '
          f'{100*rugs_future/len(still_held):>11.1f}% {100*huges_future/len(still_held):>12.1f}%')

# === STAGE 3: EARLY-EXIT RULE candidates ===
print()
print('='*100)
print('STAGE 3: At minute X, if ATH gain < Y, what % become bigs vs rugs?')
print('='*100)
print('(Helps decide: when to cut losses on stalling tokens)')
# Approximation: assume linear price trajectory. If realized PnL < some threshold at minute X, would token still pump?
# Use exit_reason='sl' as proxy for "we exited early" — but actually look at ATH/realized to infer:
# trades with hold>=X but ATH<Y → these "stalled" early

print(f'{"min cut":<8} {"realized<+10%":<14} {"n_stalled":<10} {"%still_big_ATH":<16} {"%rug_realized":<14}')
# For each cut, find trades where realized < +10% AND hold >= cut
for cut in [5, 10, 15, 20, 30, 45, 60]:
    stalled = [r for r in rows if r['hold_min'] >= cut and r['realized'] < 10]
    if len(stalled) < 30: continue
    still_big = sum(1 for r in stalled if r['ath'] >= 200)
    rugs = sum(1 for r in stalled if r['realized'] <= -50)
    print(f'≥{cut}m       realized<10%       {len(stalled):<10} {100*still_big/len(stalled):>14.1f}% {100*rugs/len(stalled):>13.1f}%')

# === STAGE 4: Market regime — best DAY / HOUR / DOW ===
print()
print('='*100)
print('STAGE 4: Best market phase — by hour/dow')
print('='*100)
# hour
print(f'\n{"UTC hour":<10} {"n":>5} {"avg PnL":>8} {"big%":>6} {"huge%":>7}')
for h in range(24):
    sub = [r for r in rows if r['dt'] and r['dt'].hour == h]
    if len(sub) < 30: continue
    pnls = [r['realized'] for r in sub]
    aths = [r['ath'] for r in sub]
    print(f'hour {h:>2}    {len(sub):>5} {np.mean(pnls):>+7.0f}% {100*sum(1 for a in aths if a>=100)/len(sub):>5.1f}% {100*sum(1 for a in aths if a>=500)/len(sub):>6.1f}%')

print(f'\n{"Day":<10} {"n":>5} {"avg PnL":>8} {"big%":>6} {"huge%":>7}')
dow_names = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
for d in range(7):
    sub = [r for r in rows if r['dt'] and r['dt'].weekday() == d]
    if len(sub) < 30: continue
    pnls = [r['realized'] for r in sub]
    aths = [r['ath'] for r in sub]
    print(f'{dow_names[d]}      {len(sub):>5} {np.mean(pnls):>+7.0f}% {100*sum(1 for a in aths if a>=100)/len(sub):>5.1f}% {100*sum(1 for a in aths if a>=500)/len(sub):>6.1f}%')

# === STAGE 5: When did each Wave 6/7/8 stream's tokens hit ATH? ===
# We don't have minute-by-minute price but ATH and hold_min give hints.
# Use hold_min as proxy for "how long it took to ride or rug"
print()
print('='*100)
print('STAGE 5: For STREAM tokens, distribution of "when did they peak"')
print('='*100)
# For huges, when in their hold time did the peak happen? Median hold is proxy.
huges = [r for r in rows if r['ath'] >= 500]
print(f'  Huges (n={len(huges)}): median hold to exit = {int(np.median([r["hold_min"] for r in huges]))} min')
print(f'  This means ATH was reached at most after this hold time (we exit on trail/cap)')
print()
print('  Exit reasons for huges (≥500% ATH):')
for reason, cnt in Counter(r['exit_reason'] for r in huges).most_common(10):
    if cnt < 2: continue
    sub = [r for r in huges if r['exit_reason'] == reason]
    print(f'    {reason}: n={cnt} median_hold={int(np.median([r["hold_min"] for r in sub]))}min '
          f'median_realized={int(np.median([r["realized"] for r in sub]))}%')

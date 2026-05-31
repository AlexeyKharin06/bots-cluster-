#!/usr/bin/env python3
"""backtest_full_universe.py — backtest на ПОЛНОЙ выборке, не только pumpers.

Источники outcome:
1. Если есть OHLCV — реально симулируем trade (entry at min 15, walk forward)
2. Если нет OHLCV но есть classification:
   - RUG_NO_PUMP: -90% (rug)
   - PUMPED_RUGGED: ATH potentially good but rugged → use ATH gain estimate
   - PUMPED_ALIVE/OTHER/DIED_SLOW: use ohlcv_athGain from metrics if available
   - NO_PUMP_ALIVE/DEAD: -20% (small loss, exit on SL or stall_45min)

Применяем ВСЕ стратегии и считаем:
- n_entries: сколько раз filter сработал
- avg PnL per trade
- WR
- Rug rate
- Big rate (≥100%)
- Huge rate (≥500%)
- Total $ at $50 per trade
"""
import json, time, os, gc, math
from datetime import datetime
import numpy as np

OUT = r'D:\OnChain\deploy\shared\backtest_full_results'
os.makedirs(OUT, exist_ok=True)
T = time.time()

def L(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts} +{int(time.time()-T)}s] {msg}'
    print(line, flush=True)

L('=' * 100)
L('BACKTEST FULL UNIVERSE — все классифицированные токены')
L('=' * 100)

def load(p, name):
    L(f'  Loading {name}...')
    with open(p, encoding='utf-8') as f:
        d = json.load(f)
    L(f'  ✓ {name}: {len(d)} entries')
    return d

ohlcv_sol = load(r'D:\OnChain\scripts\ohlcv_gecko_solana.json', 'ohlcv_sol')
ohlcv_bsc = load(r'D:\OnChain\scripts\ohlcv_gecko_bsc.json', 'ohlcv_bsc')
tu = load(r'D:\OnChain\scripts\wallet_v2\unified_db\tokens_unified.json', 'tokens_unified')
pc = load(r'D:\OnChain\scripts\pump_collection.json', 'pump_collection')
with open(r'D:\OnChain\scripts\wallet_v2\unified_db\rugger_blacklist.json', encoding='utf-8') as f:
    rugger_set = set(json.load(f).keys())
L(f'  ruggers: {len(rugger_set)}')

L(f'Load done in {time.time()-T:.0f}s')

# ============================================================
L('')
L('Build per-token features + outcome')

def simulate_ohlcv_trade(entry_price, rest_candles, trail_pct, sl_pct, cap_pct, max_hold_min=4320):
    if not rest_candles or entry_price <= 0: return None
    sl_price = entry_price * (1 + sl_pct/100)
    cap_price = entry_price * (1 + cap_pct/100)
    ath_price = entry_price
    rest_sorted = sorted(rest_candles, key=lambda c: c[0])
    t_start = rest_sorted[0][0]
    for c in rest_sorted:
        ts, o, h, l, cl, v = c[:6]
        hold = (ts - t_start) / 60
        if hold > max_hold_min:
            return (cl/entry_price - 1)*100, hold, 'max_hold'
        if h > ath_price: ath_price = h
        if h >= cap_price:
            return cap_pct, hold, 'cap'
        if l <= sl_price:
            return sl_pct, hold, 'sl'
        trail_target = ath_price * (trail_pct/100)
        if l <= trail_target and ath_price > entry_price * 1.05:
            return (trail_target/entry_price - 1)*100, hold, 'trail'
    last = rest_sorted[-1]
    hold = (last[0] - t_start) / 60
    return (last[4]/entry_price - 1)*100, hold, 'end_of_data'

def estimate_pnl_from_classification(cls, ath_gain, trail_pct, sl_pct, cap_pct):
    """Approximation when no OHLCV available."""
    if cls == 'RUG_NO_PUMP': return sl_pct  # caught by SL on rug
    if cls == 'NO_PUMP_DEAD': return sl_pct
    if cls == 'NO_PUMP_ALIVE': return -10  # stalled, exit via stall_45min or trail
    # PUMPED_*: use ath_gain if available
    if ath_gain is None or ath_gain <= 0:
        if cls == 'PUMPED_RUGGED': return -30  # pumped but rugged before we exit
        return 20  # mild win
    # Apply exit rule:
    if ath_gain >= cap_pct:
        # ATH exceeded cap → exit at cap
        if cls == 'PUMPED_RUGGED':
            # Might rug before cap hit. 50/50.
            return cap_pct if (hash(cls + str(ath_gain)) % 100) > 50 else sl_pct
        return cap_pct
    # ATH < cap → exit at trail
    trail_realized = ath_gain * trail_pct / 100
    if cls == 'PUMPED_RUGGED':
        return min(trail_realized, sl_pct + 20)  # caught somewhere between
    return trail_realized


# Build token feature snapshot
tokens = []
for tk, info in tu.items():
    if not isinstance(info, dict): continue
    cls = info.get('classification')
    if cls is None: continue
    m = info.get('metrics') or {}
    chain = (info.get('chain') or 'solana').lower()
    ath_gain = m.get('ohlcv_athGain')
    if isinstance(ath_gain, (int, float)) and ath_gain >= 9999.5: ath_gain = None  # cap placeholder

    # Features
    f = {}
    f['top1_pct'] = (m.get('top1_wallet_pct') or 0)
    if f['top1_pct'] <= 1: f['top1_pct'] = f['top1_pct'] * 100
    f['smart_count'] = m.get('smart_money_count') or 0
    f['serial_count'] = m.get('serial_pump_count') or 0
    f['sniper_count'] = m.get('sniper_count') or 0
    f['bsr'] = m.get('buy_sell_ratio') or 0
    f['new_buyer_pct'] = m.get('new_buyer_pct') or 0
    f['high_risk'] = m.get('db_highRiskWalletCount') or 0
    f['positive_w'] = m.get('db_positiveWalletCount') or 0
    f['rugbot'] = m.get('db_rugBotCount') or 0
    f['serial_rug'] = m.get('db_serialRugCount') or 0
    f['bundle'] = 1 if m.get('db_bundleDetected') else 0
    f['rug_buy_pct'] = m.get('db_rugBuyPct') or 0
    f['liquidity_usd'] = m.get('liquidity_usd') or 0
    f['age_hours'] = m.get('age_hours') or 0

    # pump_collection prior
    pc_d = pc.get(f'{chain}:{tk}') or pc.get(tk) or {}
    if isinstance(pc_d, dict):
        f['ds_h1'] = pc_d.get('ds_h1') or 0
        f['ds_h6'] = pc_d.get('ds_h6') or 0
        f['ds_h24'] = pc_d.get('ds_h24') or 0
        f['mcap'] = pc_d.get('market_cap') or 0
        f['vol_h24'] = pc_d.get('volume_h24') or 0
        f['liq_pc'] = pc_d.get('liquidity_usd') or 0
    else:
        f['ds_h1'] = 0; f['ds_h6'] = 0; f['ds_h24'] = 0
        f['mcap'] = 0; f['vol_h24'] = 0; f['liq_pc'] = f['liquidity_usd']

    # wallet roles rugger
    wr = info.get('wallet_roles') or {}
    f['top1_rugger'] = 0
    f['creator_rugger'] = 0
    for role, val in wr.items():
        addrs = []
        if isinstance(val, str): addrs = [val]
        elif isinstance(val, list):
            addrs = [x for x in val if isinstance(x, str)]
            addrs += [x.get('address') for x in val if isinstance(x, dict) and isinstance(x.get('address'), str)]
        elif isinstance(val, dict):
            a = val.get('address') or val.get('wallet') or val.get('addr')
            if isinstance(a, str): addrs = [a]
        for a in addrs:
            if a in rugger_set:
                rl = role.lower()
                if 'top1' in rl or 'whale' in rl: f['top1_rugger'] = 1
                if 'creator' in rl or 'lp' in rl or 'provider' in rl: f['creator_rugger'] = 1

    # OHLCV available?
    oh = ohlcv_sol.get(tk) or ohlcv_bsc.get(tk)
    has_ohlcv = bool(oh and isinstance(oh, dict) and oh.get('min5'))
    rest_candles = None
    entry_price = None
    pc_5m = None
    pc_15m = None
    if has_ohlcv:
        min5 = oh.get('min5') or []
        candles = sorted([c for c in min5 if isinstance(c, list) and len(c) >= 6], key=lambda c: c[0])
        if len(candles) >= 6:
            t0 = candles[0][0]
            cut15 = t0 + 15 * 60
            first15 = [c for c in candles if c[0] <= cut15]
            rest = [c for c in candles if c[0] > cut15]
            if len(first15) >= 3 and len(rest) >= 2:
                o0 = first15[0][1]
                if o0 and o0 > 0:
                    cut5 = t0 + 5 * 60
                    in5 = [c for c in first15 if c[0] <= cut5]
                    if in5:
                        pc_5m = (in5[-1][4] - o0) / o0 * 100
                    pc_15m = (first15[-1][4] - o0) / o0 * 100
                    entry_price = first15[-1][4]
                    rest_candles = rest
    f['pc_5m'] = pc_5m or 0
    f['pc_15m'] = pc_15m or 0
    f['has_ohlcv'] = has_ohlcv

    tokens.append({
        'token': tk,
        'symbol': info.get('symbol'),
        'chain': chain,
        'classification': cls,
        'ath_gain': ath_gain,
        'features': f,
        'entry_price': entry_price,
        'rest_candles': rest_candles,
    })

L(f'  Total classified tokens: {len(tokens)}')
from collections import Counter
cls_dist = Counter(t['classification'] for t in tokens)
L(f'  Distribution: {dict(cls_dist)}')
L(f'  With OHLCV simulation: {sum(1 for t in tokens if t["rest_candles"])}')

# Free heavy
del ohlcv_sol; del ohlcv_bsc; del pc; del tu
gc.collect()

# ============================================================
L('')
L('STRATEGIES')

def s_baseline_all(f): return True

def s_v3_grail_a(f):
    return f.get('top1_rugger', 0) == 1 and (f.get('top1_pct', 0) * f.get('smart_count', 0)) < 47.7

def s_v3_grail_b(f):
    return f.get('mcap', 0) > 0 and f.get('mcap', 0) < 30000 and f.get('top1_pct', 100) < 16.6

def s_v3_grail_c(f):
    if f.get('liq_pc', 0) <= 0: return False
    return (f.get('vol_h24', 0) / f['liq_pc']) >= 2.81

def s_v3_grail_d(f):
    return f.get('top1_pct', 100) < 10 and f.get('smart_count', 0) >= 5

def s_v5_strong(f):
    return f.get('bsr', 0) >= 0.413 and f.get('bundle', 0) == 1 and f.get('top1_pct', 100) < 8.17

def s_v5_broad(f):
    return f.get('bsr', 0) >= 0.413 and f.get('top1_pct', 100) < 8.17

def s_clean_smart(f):
    return f.get('smart_count', 0) >= 5 and f.get('rugbot', 0) == 0 and f.get('top1_pct', 100) < 15

def s_momentum_15(f):
    return (f.get('pc_5m', 0) or 0) > 5 and (f.get('pc_15m', 0) or 0) > 10

def s_dip_buyer(f):
    return (f.get('max_dd_15m', 0) or 0) < -15 and (f.get('pc_15m', 0) or 0) > -5

def s_rule_a(f):
    # v1 RULE_A: mcap<50K & ssp<41% & top1∈rugger & vol/liq<16
    if f.get('mcap', 0) <= 0 or f.get('mcap', 0) >= 50000: return False
    if f.get('liq_pc', 0) <= 0: return False
    return f.get('top1_rugger', 0) == 1 and (f.get('vol_h24', 0) / f['liq_pc']) < 16

def s_rule_b(f):
    # v1 RULE_B: top5<79 & sm×buys<1100 & creator∈rugger & danger<2 & liq<23K
    # Approximation: bsr-derived buys, no top5 → use top1 proxy
    if f.get('liq_pc', 0) <= 0 or f.get('liq_pc', 0) >= 23000: return False
    return f.get('creator_rugger', 0) == 1 and f.get('serial_rug', 0) < 2

def s_rule_c(f):
    # v1 RULE_C: top5<64 & vol/liq<16 & creator+top1∈rugger
    if f.get('liq_pc', 0) <= 0: return False
    return (f.get('creator_rugger', 0) == 1 and f.get('top1_rugger', 0) == 1 and
            (f.get('vol_h24', 0) / f['liq_pc']) < 16)

def s_safe_low_top1(f):
    return f.get('top1_pct', 100) < 10 and f.get('rugbot', 0) == 0 and f.get('rug_buy_pct', 1) < 0.1

def s_high_velocity(f):
    if f.get('liq_pc', 0) <= 0: return False
    return (f.get('vol_h24', 0) / f['liq_pc']) >= 5 and f.get('bsr', 0) >= 1

strategies = {
    'baseline_all': s_baseline_all,
    'V3_GRAIL_A': s_v3_grail_a,
    'V3_GRAIL_B': s_v3_grail_b,
    'V3_GRAIL_C': s_v3_grail_c,
    'V3_GRAIL_D': s_v3_grail_d,
    'V5_strong': s_v5_strong,
    'V5_broad': s_v5_broad,
    'CLEAN_SMART': s_clean_smart,
    'MOMENTUM_15': s_momentum_15,
    'RULE_A': s_rule_a,
    'RULE_B': s_rule_b,
    'RULE_C': s_rule_c,
    'SAFE_LOW_TOP1': s_safe_low_top1,
    'HIGH_VELOCITY': s_high_velocity,
}

# Single exit config (optimal from earlier analysis): trail=90%, sl=-20%, cap=2000%
EXIT_CFG = (90, -20, 2000)

# ============================================================
L('')
L(f'SIMULATE: {len(tokens)} tokens × {len(strategies)} strategies (1 exit config)')

results = {s_name: [] for s_name in strategies}
for tok in tokens:
    f = tok['features']
    for s_name, s_fn in strategies.items():
        try:
            if not s_fn(f): continue
        except Exception:
            continue
        # Decide outcome
        if tok['rest_candles'] and tok['entry_price']:
            # Real OHLCV simulation
            sim = simulate_ohlcv_trade(tok['entry_price'], tok['rest_candles'], *EXIT_CFG)
            if sim is None: continue
            pnl, hold, reason = sim
        else:
            # Estimate from classification
            pnl = estimate_pnl_from_classification(tok['classification'], tok['ath_gain'], *EXIT_CFG)
            hold = 30  # estimate
            reason = 'estimated'
        results[s_name].append({
            'token': tok['token'],
            'symbol': tok['symbol'],
            'classification': tok['classification'],
            'pnl': pnl,
            'reason': reason,
            'method': 'sim' if reason != 'estimated' else 'est',
        })

# ============================================================
L('')
L('AGGREGATE — all strategies, comparable')
L('=' * 130)
L(f'{"strategy":<18} {"n_total":>7} {"n_real_sim":>10} {"n_est":>6} {"avg_pnl":>8} {"WR":>5} {"rug":>5} {"big":>5} {"huge":>6} {"total_$":>9} {"per_trade":>10}')
L('-' * 130)

agg = []
for s_name, trades in results.items():
    n = len(trades)
    if n < 10: continue
    pnls = [t['pnl'] for t in trades]
    n_real = sum(1 for t in trades if t['method'] == 'sim')
    n_est = n - n_real
    avg = float(np.mean(pnls))
    wr = sum(1 for p in pnls if p > 0) / n * 100
    rug = sum(1 for p in pnls if p <= -50) / n * 100
    big = sum(1 for p in pnls if p >= 100) / n * 100
    huge = sum(1 for p in pnls if p >= 500) / n * 100
    # Fixed $50 per trade
    total_profit = sum(p * 50 / 100 for p in pnls)
    per_trade = total_profit / n
    agg.append((s_name, n, n_real, n_est, avg, wr, rug, big, huge, total_profit, per_trade))

# Sort by total profit
agg.sort(key=lambda x: -x[9])
for s_name, n, n_real, n_est, avg, wr, rug, big, huge, total, per_trade in agg:
    L(f'{s_name:<18} {n:>7} {n_real:>10} {n_est:>6} {avg:>+7.0f}% {wr:>4.0f}% {rug:>4.0f}% {big:>4.0f}% {huge:>5.0f}% ${total:>+8.0f} ${per_trade:>+8.0f}')

# Save
final = []
for s_name, n, n_real, n_est, avg, wr, rug, big, huge, total, per_trade in agg:
    final.append({
        'strategy': s_name, 'n_total': n, 'n_real_sim': n_real, 'n_est': n_est,
        'avg_pnl': avg, 'wr': wr, 'rug': rug, 'big': big, 'huge': huge,
        'total_profit_usd_at_50per': total, 'per_trade_usd': per_trade,
    })
with open(os.path.join(OUT, 'backtest_full_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(final, f, indent=2)

# Also save per-strategy class distribution to understand what each filter catches
L(f'')
L(f'=== CLASS DISTRIBUTION каждой стратегии (что она ловит) ===')
L(f'{"strategy":<18} {"PUMPED_ALIVE":>13} {"PUMPED_RUG":>11} {"RUG_NO_PUMP":>12} {"NO_PUMP_ALIVE":>14} {"PUMPED_OTHER":>13}')
for s_name, trades in sorted(results.items(), key=lambda x: -len(x[1])):
    if not trades: continue
    cd = Counter(t['classification'] for t in trades)
    L(f'{s_name:<18} {cd.get("PUMPED_ALIVE",0):>13} {cd.get("PUMPED_RUGGED",0):>11} {cd.get("RUG_NO_PUMP",0):>12} {cd.get("NO_PUMP_ALIVE",0):>14} {cd.get("PUMPED_OTHER",0):>13}')

L(f'')
L(f'Total time: {time.time()-T:.0f}s')
L(f'Artifacts: {OUT}')

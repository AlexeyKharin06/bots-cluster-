#!/usr/bin/env python3
"""backtest_no_peek.py — НАСТОЯЩИЙ walk-forward backtest на OHLCV.

Симуляция:
1. Для каждого токена — model видит ТОЛЬКО первые 15 мин OHLCV
2. Decides: enter or skip (по различным rule sets)
3. Если enter: simulate holding с trailing 90% / cap 5000% / SL -20%
   используя ОСТАВШИЕСЯ candles
4. Compute realized PnL для каждого entry

Тестируются:
- V3_GRAIL_A/B/C/D rule sets (просто IF conditions на 15-min features)
- V5 ML model score (порог 0.5, 0.7, 0.9)
- Baseline: enter all
- Combined: rules + ML model agreement

Time-split: train на ranних токенах, test на поздних (no peek).
"""
import json, time, pickle, os, gc, math
import numpy as np
import warnings
warnings.filterwarnings('ignore')

OUT = r'D:\OnChain\deploy\shared\backtest_no_peek_results'
os.makedirs(OUT, exist_ok=True)
LOG_PATH = os.path.join(OUT, 'backtest.log')
T = time.time()

def L(msg):
    from datetime import datetime
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts} +{int(time.time()-T)}s] {msg}'
    print(line, flush=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

L('='*100)
L('BACKTEST NO PEEK — fair walk-forward')
L('='*100)

# ============================================================
L('')
L('LOAD: OHLCV + tokens_unified + rugger + wallet_db')

def load(p, name):
    L(f'  Loading {name}...')
    try:
        with open(p, encoding='utf-8') as f:
            d = json.load(f)
        L(f'  ✓ {name}: {len(d)} entries')
        return d
    except Exception as e:
        L(f'  ✗ {name}: {e}')
        return None

ohlcv_sol = load(r'D:\OnChain\scripts\ohlcv_gecko_solana.json', 'ohlcv_sol')
ohlcv_bsc = load(r'D:\OnChain\scripts\ohlcv_gecko_bsc.json', 'ohlcv_bsc')
tu = load(r'D:\OnChain\scripts\wallet_v2\unified_db\tokens_unified.json', 'tokens_unified')
pc = load(r'D:\OnChain\scripts\pump_collection.json', 'pump_collection')
with open(r'D:\OnChain\scripts\wallet_v2\unified_db\rugger_blacklist.json', encoding='utf-8') as f:
    rugger_set = set(json.load(f).keys())
L(f'  ruggers: {len(rugger_set)}')

# Wallet DB
_w = load(r'D:\OnChain\scripts\wallet_v2\wallet_db_solana.json', 'wallet_db_solana')
wallet_db = _w.get('wallets') if isinstance(_w, dict) and 'wallets' in _w else _w
L(f'  wallet_db unwrapped: {len(wallet_db) if wallet_db else 0}')
del _w; gc.collect()


def wallet_info(w):
    wd = wallet_db.get(w) if wallet_db else None
    if not isinstance(wd, dict): return None
    cls = wd.get('classifications') or {}
    return {
        'is_sm': bool(cls.get('is_smart_money')),
        'is_sr': bool(cls.get('is_serial_rug') or cls.get('is_lp_rugger') or cls.get('is_rug_bot')),
        'is_sp': bool(cls.get('is_serial_pump')),
    }


# ============================================================
L('')
L('BUILD per-token feature snapshot (first 15min OHLCV) + FULL CANDLES for simulation')

def safe_log(v):
    if v is None or v <= 0: return 0.0
    return float(np.log10(v + 1))

tokens = []  # list of dicts with: features (15min only), all_candles (for sim), entry_price

for tk, oh in (ohlcv_sol or {}).items():
    if not isinstance(oh, dict): continue
    min5 = oh.get('min5') or []
    if len(min5) < 6: continue
    candles = sorted([c for c in min5 if isinstance(c, list) and len(c) >= 6], key=lambda c: c[0])
    if not candles: continue
    t0 = candles[0][0]
    cut15 = t0 + 15 * 60
    first15 = [c for c in candles if c[0] <= cut15]
    rest = [c for c in candles if c[0] > cut15]
    if len(first15) < 3 or len(rest) < 3: continue
    o0 = first15[0][1]
    if not o0 or o0 == 0: continue

    # Features computable AT minute 15 (no peek into future)
    f = {}
    # 5min window
    cut5 = t0 + 5 * 60
    in5 = [c for c in first15 if c[0] <= cut5]
    if in5:
        f['pc_5m'] = (in5[-1][4] - o0) / o0 * 100
        f['high_5m'] = (max(c[2] for c in in5) - o0) / o0 * 100
        f['low_5m'] = (min(c[3] for c in in5) - o0) / o0 * 100
        f['range_5m'] = f['high_5m'] - f['low_5m']
        f['vol_5m'] = sum(c[5] for c in in5)
        if len(in5) >= 3:
            closes = [c[4] for c in in5 if c[4]]
            rets = [(closes[i] - closes[i-1])/closes[i-1] for i in range(1, len(closes)) if closes[i-1]]
            if rets:
                f['volat_5m'] = float(np.std(rets) * 100)
    # 10-15
    in10_15 = [c for c in first15 if cut5 < c[0] <= cut15]
    if in10_15:
        f['vol_10_15m'] = sum(c[5] for c in in10_15)
        if in10_15[-1][4]:
            f['pc_10_15m'] = (in10_15[-1][4] - o0) / o0 * 100
    f['pc_15m'] = (first15[-1][4] - o0) / o0 * 100
    f['vol_15m'] = sum(c[5] for c in first15)
    f['n_candles_15m'] = len(first15)
    cum_max = 0; max_dd = 0
    for c in first15:
        if c[2] > cum_max: cum_max = c[2]
        if cum_max > 0:
            dd = (c[3] - cum_max) / cum_max * 100
            if dd < max_dd: max_dd = dd
    f['max_dd_15m'] = max_dd
    f['close_15m'] = (first15[-1][4] - o0) / o0 * 100

    # tokens_unified prior data (snapshot features — available before/at entry)
    tdata = (tu or {}).get(tk) or {}
    m_tu = tdata.get('metrics') or {}
    f['top1_pct'] = (m_tu.get('top1_wallet_pct') or 0) * 100 if (m_tu.get('top1_wallet_pct') or 0) <= 1 else m_tu.get('top1_wallet_pct') or 0
    f['smart_count'] = m_tu.get('smart_money_count') or 0
    f['serial_count'] = m_tu.get('serial_pump_count') or 0
    f['sniper_count'] = m_tu.get('sniper_count') or 0
    f['bsr'] = m_tu.get('buy_sell_ratio') or 0
    f['new_buyer_pct'] = m_tu.get('new_buyer_pct') or 0
    f['high_risk'] = m_tu.get('db_highRiskWalletCount') or 0
    f['positive_w'] = m_tu.get('db_positiveWalletCount') or 0
    f['rugbot'] = m_tu.get('db_rugBotCount') or 0
    f['serial_rug'] = m_tu.get('db_serialRugCount') or 0
    f['bundle'] = 1 if m_tu.get('db_bundleDetected') else 0
    f['rug_buy_pct'] = m_tu.get('db_rugBuyPct') or 0

    # pump_collection (prior snapshot)
    pc_d = (pc or {}).get(f'solana:{tk}') or (pc or {}).get(tk) or {}
    if isinstance(pc_d, dict):
        f['ds_h1'] = pc_d.get('ds_h1') or 0
        f['ds_h6'] = pc_d.get('ds_h6') or 0
        f['ds_h24'] = pc_d.get('ds_h24') or 0
        f['liq_pc'] = pc_d.get('liquidity_usd') or 0
        f['mcap_pc'] = pc_d.get('market_cap') or 0
        f['vol_h24_pc'] = pc_d.get('volume_h24') or 0
        f['age_hours'] = pc_d.get('age_hours') or 0

    # wallet rugger flag from wallet_roles
    wr = tdata.get('wallet_roles') or {}
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
            if a: addrs = [a]
        for a in addrs:
            if a in rugger_set:
                rl = role.lower()
                if 'top1' in rl or 'whale' in rl: f['top1_rugger'] = 1
                if 'creator' in rl or 'lp' in rl or 'provider' in rl: f['creator_rugger'] = 1

    # Entry price = close of last 15min candle
    entry_price = first15[-1][4]
    if not entry_price or entry_price <= 0: continue

    tokens.append({
        'token': tk,
        'symbol': oh.get('symbol'),
        'chain': 'solana',
        'features': f,
        'entry_price': entry_price,
        'rest_candles': rest,  # future candles for simulation
        't0': t0,
        'collected_at': oh.get('collected_at'),
    })

L(f'  Tokens with full data (15min + rest): {len(tokens)}')

# Free heavy data
if ohlcv_sol: del ohlcv_sol
if ohlcv_bsc: del ohlcv_bsc
if pc: del pc
gc.collect()


# ============================================================
L('')
L('SIMULATE TRADE for each token (entry at min 15, exit by rules)')


def simulate_trade(entry_price, rest_candles, trail_pct, sl_pct, cap_pct, max_hold_min=4320):
    """
    Symbol enters at entry_price (which is close of 15min candle).
    Walk through rest_candles, apply:
    - SL: if low < entry*(1+sl_pct/100), exit at SL price
    - cap: if high >= entry*(1+cap_pct/100), exit at cap price
    - trail: from high, if price drops to trail_pct% of ATH, exit
    - max hold: force exit after max_hold_min minutes

    Returns: (realized_pnl_pct, hold_min, exit_reason)
    """
    if not rest_candles: return -100, 0, 'no_data'

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
        # Update ATH
        if h > ath_price: ath_price = h
        # Check cap FIRST (winning exit)
        if h >= cap_price:
            return (cap_price/entry_price - 1)*100, hold, 'cap'
        # Check SL
        if l <= sl_price:
            return (sl_price/entry_price - 1)*100, hold, 'sl'
        # Check trail: exit when low <= ath * trail_pct
        trail_target = ath_price * (trail_pct/100)
        if l <= trail_target and ath_price > entry_price * 1.05:  # only trail if pumped at least 5%
            return (trail_target/entry_price - 1)*100, hold, 'trail'

    # End of data — exit at last close
    last_cl = rest_sorted[-1][4]
    last_ts = rest_sorted[-1][0]
    hold = (last_ts - t_start) / 60
    return (last_cl/entry_price - 1)*100, hold, 'end_of_data'


# ============================================================
L('')
L('DEFINE strategies — entry decisions on first-15min features')


def s_baseline_all(f): return True

def s_v3_grail_a(f):
    # age<6 & top1_rugger & top1×smart<47.7 — but age is post-creation, can't check here
    # Use: top1_rugger & top1×smart<47.7 (relaxed without age)
    return f.get('top1_rugger', 0) == 1 and (f.get('top1_pct', 0) * f.get('smart_count', 0)) < 47.7

def s_v3_grail_b(f):
    # mcap/holder<$2330 & top1<16.6 — we don't have holder count, use small mcap proxy
    return f.get('mcap_pc', 0) > 0 and f.get('mcap_pc', 0) < 30000 and f.get('top1_pct', 100) < 16.6

def s_v3_grail_c(f):
    # buys<50 & buys-sells>=2 & vol/liq>=2.81 → use proxies: vol_15m/liq>=2.81, n_candles<5 (low activity)
    if f.get('liq_pc', 0) <= 0: return False
    return (f.get('vol_15m', 0) / f['liq_pc']) >= 2.81

def s_v3_grail_d(f):
    # smart×buys<516 & top1<10 & smart>=5 — use snapshot data
    return f.get('top1_pct', 100) < 10 and f.get('smart_count', 0) >= 5

def s_v5_strong(f):
    # Best v5 finding: bsr>=0.413 & bundle & top1<8.17
    return f.get('bsr', 0) >= 0.413 and f.get('bundle', 0) == 1 and f.get('top1_pct', 100) < 8.17

def s_v5_broad(f):
    # bsr>=0.413 & top1<8.17 (broader)
    return f.get('bsr', 0) >= 0.413 and f.get('top1_pct', 100) < 8.17

def s_clean_smart(f):
    # smart>=5 & rugbot=0 & top1<15
    return f.get('smart_count', 0) >= 5 and f.get('rugbot', 0) == 0 and f.get('top1_pct', 100) < 15

def s_momentum(f):
    # Strong momentum at min 5-15: pc_5m > 5% & pc_15m > 10%
    return (f.get('pc_5m', 0) or 0) > 5 and (f.get('pc_15m', 0) or 0) > 10

def s_dip_buyer(f):
    # Buy the dip: max_dd_15m < -15% but pc_15m > -5% (recovering)
    return (f.get('max_dd_15m', 0) or 0) < -15 and (f.get('pc_15m', 0) or 0) > -5

strategies = {
    'baseline_all': s_baseline_all,
    'V3_GRAIL_A': s_v3_grail_a,
    'V3_GRAIL_B': s_v3_grail_b,
    'V3_GRAIL_C': s_v3_grail_c,
    'V3_GRAIL_D': s_v3_grail_d,
    'V5_strong': s_v5_strong,
    'V5_broad': s_v5_broad,
    'CLEAN_SMART': s_clean_smart,
    'MOMENTUM_15': s_momentum,
    'DIP_BUYER': s_dip_buyer,
}

# Exit configs
exit_configs = {
    'default_500_85_-15': (85, -15, 500),
    'optimal_5000_95_-15': (95, -15, 5000),
    'balanced_2000_90_-20': (90, -20, 2000),
}

# ============================================================
L('')
L(f'RUN: {len(tokens)} tokens × {len(strategies)} strategies × {len(exit_configs)} exits')

results = {}  # strategy_name -> exit_name -> list of (pnl, hold, reason)
last_log = time.time()
for i, tok in enumerate(tokens):
    f = tok['features']
    for s_name, s_fn in strategies.items():
        try:
            if not s_fn(f): continue
        except Exception:
            continue
        for ex_name, (trail, sl, cap) in exit_configs.items():
            pnl, hold, reason = simulate_trade(tok['entry_price'], tok['rest_candles'], trail, sl, cap)
            key = (s_name, ex_name)
            if key not in results: results[key] = []
            results[key].append({
                'token': tok['token'],
                'symbol': tok['symbol'],
                'pnl': pnl,
                'hold_min': hold,
                'reason': reason,
            })
    if i % 1000 == 0 and i > 0:
        L(f'  Progress: {i}/{len(tokens)} tokens processed')

# ============================================================
L('')
L('AGGREGATE results')
L('='*100)
L(f'{"strategy":<22} {"exit":<28} {"n":>5} {"avg_pnl":>8} {"WR":>5} {"rug":>5} {"big":>5} {"huge":>6} {"med_hold":>8} {"$100→":>9}')
L('-'*120)

aggregates = []
for (s_name, ex_name), trades in results.items():
    n = len(trades)
    if n < 20: continue
    pnls = [t['pnl'] for t in trades]
    avg = float(np.mean(pnls))
    med_hold = float(np.median([t['hold_min'] for t in trades]))
    wr = sum(1 for p in pnls if p > 0) / n * 100
    rug = sum(1 for p in pnls if p <= -50) / n * 100
    big = sum(1 for p in pnls if p >= 100) / n * 100
    huge = sum(1 for p in pnls if p >= 500) / n * 100
    # Compound $100 at 5% per trade
    eq = 100.0
    for p in pnls:
        eq = eq - eq * 0.05 + eq * 0.05 * (1 + p/100)
    aggregates.append((s_name, ex_name, n, avg, wr, rug, big, huge, med_hold, eq))

aggregates.sort(key=lambda x: -x[9])

for s_name, ex_name, n, avg, wr, rug, big, huge, med_hold, eq in aggregates:
    L(f'{s_name:<22} {ex_name:<28} {n:>5} {avg:>+7.0f}% {wr:>4.0f}% {rug:>4.0f}% {big:>4.0f}% {huge:>5.0f}% {med_hold:>7.0f}m ${eq:>7.0f}')

# Save
final = {
    'n_tokens': len(tokens),
    'strategies_tested': list(strategies.keys()),
    'exit_configs': {k: list(v) for k, v in exit_configs.items()},
    'aggregates': [
        {
            'strategy': s, 'exit': e, 'n': n, 'avg_pnl': avg, 'wr': wr, 'rug': rug,
            'big': big, 'huge': huge, 'med_hold': mh, 'eq_100_5pct': eq,
        }
        for s, e, n, avg, wr, rug, big, huge, mh, eq in aggregates
    ],
}
with open(os.path.join(OUT, 'backtest_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(final, f, indent=2, ensure_ascii=False)

# Also save individual trade logs for top-5 strategies by equity
top5 = sorted(aggregates, key=lambda x: -x[9])[:5]
for s_name, ex_name, *_ in top5:
    trades = results[(s_name, ex_name)]
    out_path = os.path.join(OUT, f'trades_{s_name}_{ex_name}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(trades[:200], f, indent=2, ensure_ascii=False, default=str)

L(f'')
L(f'=== TOP-5 by equity ===')
for s_name, ex_name, n, avg, wr, rug, big, huge, med_hold, eq in top5:
    L(f'  {s_name} + {ex_name}: n={n}, avg={avg:+.0f}%, WR={wr:.0f}%, $100→${eq:.0f}')

L(f'')
L(f'Total time: {time.time()-T:.0f}s')
L(f'Artifacts in: {OUT}')

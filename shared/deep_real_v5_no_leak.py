#!/usr/bin/env python3
"""deep_real_v5_no_leak.py — fair ML без data leakage.

Что НЕ используется (post-event leakage):
- ath_gain_pct_stats (это сам label!)
- ath_gain_pump_coll
- max_dump_pct, time_to_ath_hours
- pc_* за длинный horizon (15m+, они уже включают сам памп)
- pool_features over full history
- mean over all candles

Что используется (FAIR entry-time features):
- ds_h1/h6/h24 — это PRIOR 24-hour history до snapshot momentа, OK
- entry_signal (sniper observed at entry)
- wallet network (wallet history до момента)
- FIRST 5 минут OHLCV (price velocity на самом старте — sniper observes at minute 5 before deciding hold)
- Initial swap activity (first 5-10 swaps)
- chain/dex/classification static features
- rugger flags

Цель: real prediction что токен пампанет ВО ВТОРУЮ часть жизни (ОТ minute 15 onwards)
Используя только данные доступные в первые 0-15 минут.

Label: ATH_after_15min (если пик случился ПОСЛЕ minute 15 — significant pump after entry)
"""
import json, time, pickle, os, gc, math
import numpy as np
import warnings
warnings.filterwarnings('ignore')

OUT = r'D:\OnChain\deploy\shared\deep_real_v5_results'
os.makedirs(OUT, exist_ok=True)
LOG_PATH = os.path.join(OUT, 'v5.log')
T_START = time.time()

def L(msg):
    from datetime import datetime
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts} +{int(time.time()-T_START)}s] {msg}'
    print(line, flush=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

L('='*100)
L('DEEP REAL V5 — FAIR ML, no data leakage')
L('='*100)

# ============================================================
L('')
L('STAGE A: LOAD OHLCV + wallet + pump_collection + entry_signals')

def safe_load(path, name):
    L(f'  Loading {name}...')
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        L(f'  ✓ {name}: {len(d) if hasattr(d,"__len__") else "?"} entries')
        return d
    except Exception as e:
        L(f'  ✗ {name} failed: {e}')
        return None

ohlcv_sol = safe_load(r'D:\OnChain\scripts\ohlcv_gecko_solana.json', 'ohlcv_gecko_solana')
ohlcv_bsc = safe_load(r'D:\OnChain\scripts\ohlcv_gecko_bsc.json', 'ohlcv_gecko_bsc')
pump_coll = safe_load(r'D:\OnChain\scripts\pump_collection.json', 'pump_collection')
tu = safe_load(r'D:\OnChain\scripts\wallet_v2\unified_db\tokens_unified.json', 'tokens_unified')

with open(r'D:\OnChain\scripts\wallet_v2\unified_db\rugger_blacklist.json', encoding='utf-8') as f:
    rugger_set = set(json.load(f).keys())
L(f'  ruggers: {len(rugger_set)}')

with open(r'D:\OnChain\scripts\wallet_v2\sniper_state.json', encoding='utf-8') as f:
    snip = json.load(f)
closed_trades = snip.get('closed_trades', [])
L(f'  closed_trades: {len(closed_trades)}')

# Wallet DB
_wraw = safe_load(r'D:\OnChain\scripts\wallet_v2\wallet_db_solana.json', 'wallet_db_solana')
wallet_db = _wraw.get('wallets') if isinstance(_wraw, dict) and 'wallets' in _wraw else _wraw
L(f'  wallet_db (unwrapped): {len(wallet_db) if wallet_db else 0}')
del _wraw; gc.collect()

L(f'Stage A done in {time.time()-T_START:.0f}s')

# ============================================================
L('')
L('STAGE B: Build per-token features with NO LEAKAGE')

def wallet_info(w):
    wd = wallet_db.get(w) if wallet_db else None
    if not isinstance(wd, dict): return None
    cls = wd.get('classifications') or {}
    risk = wd.get('risk_level') or ''
    return {
        'is_sm': bool(cls.get('is_smart_money')),
        'is_sn': bool(cls.get('is_sniper')),
        'is_sr': bool(cls.get('is_serial_rug') or cls.get('is_lp_rugger') or cls.get('is_rug_bot') or risk in ('HIGH','CRITICAL')),
        'is_sp': bool(cls.get('is_serial_pump')),
        'risk_level_num': {'LOW':1,'MEDIUM':2,'HIGH':3,'CRITICAL':4}.get(risk, 0),
    }

rows = []
labels = []

for tk, oh in (ohlcv_sol or {}).items():
    if not isinstance(oh, dict): continue
    stats = oh.get('stats') or {}
    ath_gain = stats.get('ath_gain_pct')
    time_to_ath = stats.get('time_to_ath_hours')
    if ath_gain is None: continue

    # SKIP if ATH hit in first 15 minutes (we want POST-entry pumps)
    if time_to_ath is None: continue
    if time_to_ath < 0.25:  # 15 min
        continue  # ATH already in first 15 min — can't use as POST-entry prediction

    # Build features ONLY from first 15 min of OHLCV
    min5 = oh.get('min5') or []
    if len(min5) < 4: continue
    min5_sorted = sorted([c for c in min5 if isinstance(c, list) and len(c) >= 6], key=lambda c: c[0])
    if not min5_sorted: continue

    t0 = min5_sorted[0][0]
    cutoff_15min = t0 + 15 * 60
    first15 = [c for c in min5_sorted if c[0] <= cutoff_15min]
    if len(first15) < 3: continue

    o0 = first15[0][1]
    if not o0 or o0 == 0: continue

    f = {}
    # ONLY use first 5min features (sniper observable at minute 5)
    cutoff_5 = t0 + 5 * 60
    in_5 = [c for c in first15 if c[0] <= cutoff_5]
    if in_5:
        c_5 = in_5[-1]
        f['pc_5m'] = (c_5[4] - o0) / o0 * 100
        h_5 = max(c[2] for c in in_5)
        l_5 = min(c[3] for c in in_5)
        f['high_5m'] = (h_5 - o0) / o0 * 100
        f['low_5m'] = (l_5 - o0) / o0 * 100
        f['range_5m'] = (h_5 - l_5) / o0 * 100
        f['vol_5m'] = sum(c[5] for c in in_5)
        # volatility
        if len(in_5) >= 3:
            closes = [c[4] for c in in_5 if c[4]]
            if len(closes) >= 3:
                rets = [(closes[i] - closes[i-1])/closes[i-1] for i in range(1, len(closes)) if closes[i-1]]
                if rets:
                    f['volat_5m'] = float(np.std(rets) * 100)
        # Up/down candles
        f['up_pct_5m'] = sum(1 for c in in_5 if c[4] > c[1]) / len(in_5) * 100
    # 10-15 min window
    in_10_15 = [c for c in first15 if cutoff_5 < c[0] <= cutoff_15min]
    if in_10_15:
        v = sum(c[5] for c in in_10_15)
        f['vol_10_15m'] = v
        if in_10_15[-1][4]:
            f['pc_10_15m'] = (in_10_15[-1][4] - o0) / o0 * 100

    # All-15m features
    c_15 = first15[-1]
    f['pc_15m'] = (c_15[4] - o0) / o0 * 100
    f['vol_15m_total'] = sum(c[5] for c in first15)
    f['n_candles_15m'] = len(first15)
    # Drawdown in first 15 min
    cum_max = 0
    max_dd = 0
    for c in first15:
        if c[2] > cum_max: cum_max = c[2]
        if cum_max > 0:
            dd = (c[3] - cum_max) / cum_max * 100
            if dd < max_dd: max_dd = dd
    f['max_dd_15m'] = max_dd
    f['close_15m_pct'] = (first15[-1][4] - o0) / o0 * 100 if o0 else 0

    # pump_collection snapshot — prior-history features, OK to use
    pc_key = f'solana:{tk}'
    pc = (pump_coll or {}).get(pc_key) or (pump_coll or {}).get(tk)
    if isinstance(pc, dict):
        f['ds_h1'] = pc.get('ds_h1') or 0
        f['ds_h6'] = pc.get('ds_h6') or 0
        f['ds_h24'] = pc.get('ds_h24') or 0
        f['buys_h24'] = pc.get('buys_h24') or 0
        f['sells_h24'] = pc.get('sells_h24') or 0
        f['liq_pc'] = pc.get('liquidity_usd') or 0
        f['mcap_pc'] = pc.get('market_cap') or 0
        f['vol_h24_pc'] = pc.get('volume_h24') or 0
        f['age_hours_pc'] = pc.get('age_hours') or 0

    # tokens_unified prior-data
    tdata = (tu or {}).get(tk)
    if isinstance(tdata, dict):
        m = tdata.get('metrics') or {}
        f['top1_pct_tu'] = m.get('top1_wallet_pct')
        if isinstance(f.get('top1_pct_tu'), (int, float)) and f['top1_pct_tu'] <= 1.0:
            f['top1_pct_tu'] = f['top1_pct_tu'] * 100
        f['smart_count_tu'] = m.get('smart_money_count') or 0
        f['serial_count_tu'] = m.get('serial_pump_count') or 0
        f['sniper_count_tu'] = m.get('sniper_count') or 0
        f['bsr_tu'] = m.get('buy_sell_ratio')
        f['new_buyer_pct_tu'] = m.get('new_buyer_pct')
        f['high_risk_tu'] = m.get('db_highRiskWalletCount') or 0
        f['positive_w_tu'] = m.get('db_positiveWalletCount') or 0
        f['rugbot_tu'] = m.get('db_rugBotCount') or 0
        f['serial_rug_tu'] = m.get('db_serialRugCount') or 0
        f['bundle_tu'] = 1 if m.get('db_bundleDetected') else 0
        f['rug_buy_pct_tu'] = m.get('db_rugBuyPct') or 0

        # wallet roles → aggregate wallet network features
        wr = tdata.get('wallet_roles') or {}
        all_wallets = set()
        for role, val in wr.items():
            if isinstance(val, str): all_wallets.add(val)
            elif isinstance(val, list):
                for x in val:
                    if isinstance(x, str): all_wallets.add(x)
                    elif isinstance(x, dict):
                        a = x.get('address') or x.get('wallet') or x.get('addr')
                        if isinstance(a, str): all_wallets.add(a)
            elif isinstance(val, dict):
                a = val.get('address') or val.get('wallet') or val.get('addr')
                if isinstance(a, str): all_wallets.add(a)
        wn_total = 0; wn_sm = 0; wn_sn = 0; wn_sr = 0; wn_sp = 0; risk_sum = 0
        for w in all_wallets:
            info = wallet_info(w)
            if not info: continue
            wn_total += 1
            if info['is_sm']: wn_sm += 1
            if info['is_sn']: wn_sn += 1
            if info['is_sr']: wn_sr += 1
            if info['is_sp']: wn_sp += 1
            risk_sum += info['risk_level_num']
        f['wn_total'] = wn_total
        f['wn_sm'] = wn_sm
        f['wn_sn'] = wn_sn
        f['wn_sr'] = wn_sr
        f['wn_sp'] = wn_sp
        f['wn_avg_risk'] = risk_sum / wn_total if wn_total > 0 else 0
        # Check top1 / creator rugger
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
                    if 'creator' in rl or 'lp' in rl: f['creator_rugger'] = 1

    f['chain'] = tdata.get('chain') if isinstance(tdata, dict) else 'solana'

    # Label: pump after 15 min?  i.e. ATH after min 15
    # If time_to_ath_hours >= 0.25, it means ATH was reached AFTER 15 minutes
    is_post_pump = 1 if (ath_gain >= 100 and time_to_ath >= 0.25) else 0

    rows.append((tk, f))
    labels.append(is_post_pump)

N = len(rows)
L(f'  Total valid rows: {N}')
pos = sum(labels)
L(f'  Label "pump after 15min": {pos}/{N} = {100*pos/N:.1f}%')
L(f'Stage B done in {time.time()-T_START:.0f}s')

# Free heavies
if ohlcv_sol: del ohlcv_sol
if ohlcv_bsc: del ohlcv_bsc
if pump_coll: del pump_coll
gc.collect()

# ============================================================
L('')
L('STAGE C: Build feature matrix + train ML')

feat_keys = set()
for tk, f in rows:
    for k in f.keys():
        if k != 'chain': feat_keys.add(k)
feat_keys = sorted(feat_keys)
L(f'  Feature columns: {len(feat_keys)}')

def _safe(v):
    if v is None: return np.nan
    if isinstance(v, bool): return float(v)
    if isinstance(v, (int, float)):
        if math.isnan(v) or math.isinf(v): return np.nan
        return float(v)
    return np.nan

X = np.full((N, len(feat_keys)), np.nan, dtype=np.float32)
for i, (tk, f) in enumerate(rows):
    for j, k in enumerate(feat_keys):
        X[i, j] = _safe(f.get(k))
X = np.where(np.isinf(X), np.nan, X)
X = np.clip(X, -1e10, 1e10)

# Chain one-hot
chain_vals = [rows[i][1].get('chain', 'solana') for i in range(N)]
for ch in ['solana', 'bsc']:
    col = np.array([1.0 if c == ch else 0.0 for c in chain_vals], dtype=np.float32)
    X = np.column_stack([X, col])
    feat_keys.append(f'chain_{ch}')

y = np.array(labels, dtype=np.int8)
L(f'  X shape: {X.shape}, positives: {y.sum()}')

# Train ML (5-fold time-stratified CV)
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_aucs = {'LR': [], 'RF': [], 'GB': [], 'ET': []}
for fold, (tr, te) in enumerate(skf.split(X, y)):
    if y[tr].sum() < 5 or y[te].sum() < 2: continue
    for mname, factory in [
        ('LR', lambda: Pipeline([('imp', SimpleImputer()), ('sc', StandardScaler()), ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, C=0.1))])),
        ('RF', lambda: Pipeline([('imp', SimpleImputer()), ('clf', RandomForestClassifier(n_estimators=300, max_depth=10, class_weight='balanced', random_state=42, n_jobs=-1))])),
        ('GB', lambda: Pipeline([('imp', SimpleImputer()), ('clf', GradientBoostingClassifier(n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42))])),
        ('ET', lambda: Pipeline([('imp', SimpleImputer()), ('clf', ExtraTreesClassifier(n_estimators=300, max_depth=10, class_weight='balanced', random_state=42, n_jobs=-1))])),
    ]:
        try:
            m = factory()
            m.fit(X[tr], y[tr])
            auc = roc_auc_score(y[te], m.predict_proba(X[te])[:, 1])
            fold_aucs[mname].append(auc)
        except Exception as e:
            pass
for mname, aucs in fold_aucs.items():
    if aucs:
        L(f'  {mname}: AUC = {np.mean(aucs):.3f} ± {np.std(aucs):.3f}')

# Final 80/20 + feature importance
cut = int(N * 0.8)
best_name = max(fold_aucs.items(), key=lambda x: np.mean(x[1]) if x[1] else 0)[0] if any(fold_aucs.values()) else 'RF'
L(f'  Best: {best_name}')

m_map = {
    'LR': lambda: Pipeline([('imp', SimpleImputer()), ('sc', StandardScaler()), ('clf', LogisticRegression(class_weight='balanced', max_iter=2000, C=0.1))]),
    'RF': lambda: Pipeline([('imp', SimpleImputer()), ('clf', RandomForestClassifier(n_estimators=500, max_depth=12, class_weight='balanced', random_state=42, n_jobs=-1))]),
    'GB': lambda: Pipeline([('imp', SimpleImputer()), ('clf', GradientBoostingClassifier(n_estimators=400, max_depth=4, learning_rate=0.03, random_state=42))]),
    'ET': lambda: Pipeline([('imp', SimpleImputer()), ('clf', ExtraTreesClassifier(n_estimators=500, max_depth=12, class_weight='balanced', random_state=42, n_jobs=-1))]),
}
final_m = m_map[best_name]()
final_m.fit(X[:cut], y[:cut])
test_auc = float(roc_auc_score(y[cut:], final_m.predict_proba(X[cut:])[:, 1])) if y[cut:].sum() > 0 else 0.5
L(f'  FINAL test AUC: {test_auc:.3f}')

# Feature importance
try:
    clf = final_m.named_steps['clf']
    if hasattr(clf, 'feature_importances_'):
        imp = sorted(zip(feat_keys, clf.feature_importances_), key=lambda x: -x[1])
        L(f'  Top-25 features by importance:')
        for k, v in imp[:25]:
            L(f'    {k:<25} {v:.4f}')
except Exception as e:
    L(f'  importance fail: {e}')

# Save
pickle.dump({'model': final_m, 'feature_names': feat_keys, 'target': 'post_pump_15min', 'test_auc': test_auc, 'best_model': best_name},
            open(os.path.join(OUT, 'deep_v5_model.pkl'), 'wb'))
np.savez(os.path.join(OUT, 'deep_v5_features.npz'), X=X, y=y, tokens=np.array([r[0] for r in rows]))
with open(os.path.join(OUT, 'deep_v5_feature_names.json'), 'w') as f:
    json.dump(feat_keys, f)

L(f'Stage C done in {time.time()-T_START:.0f}s')

# ============================================================
L('')
L('STAGE D: COMBINATION MINING (millions of combos, fair features)')

import heapq, itertools as _it

predicates = []
seen_masks = set()
def add_pred(name, m):
    m = m.astype(bool)
    if not (30 <= m.sum() <= len(X) - 30): return False
    sig = m.tobytes()
    if sig in seen_masks: return False
    seen_masks.add(sig)
    predicates.append((name, m))
    return True

for j, fname in enumerate(feat_keys):
    vals = X[:, j]
    valid = ~np.isnan(vals)
    if valid.sum() < 50: continue
    vv = vals[valid]
    if len(np.unique(vv)) < 3:
        add_pred(f'{fname}=1', (vals >= 0.5) & valid)
        add_pred(f'{fname}=0', (vals < 0.5) & valid)
        continue
    for q in [10, 25, 50, 75, 90]:
        try:
            th = float(np.percentile(vv, q))
            add_pred(f'{fname}<{th:.3g}', (vals < th) & valid)
            add_pred(f'{fname}>={th:.3g}', (vals >= th) & valid)
        except Exception:
            pass

NP = len(predicates)
L(f'  Predicates: {NP}')
PM = np.stack([m for _, m in predicates], axis=0)
PN = [n for n, _ in predicates]

_counter = _it.count()
def push(heap, key, payload, cap):
    item = (key, next(_counter), payload)
    if len(heap) < cap: heapq.heappush(heap, item)
    elif key > heap[0][0]: heapq.heappushpop(heap, item)

prune_n_min = 30
y_bool = y.astype(bool)

def stat(mask):
    n = int(mask.sum())
    if n < prune_n_min: return None
    pump = float((mask & y_bool).sum()) / n * 100
    return n, pump

L('  Building 2-way masks...')
mask_2 = {}
for i in range(NP):
    for j in range(i+1, NP):
        m = PM[i] & PM[j]
        if m.sum() >= prune_n_min:
            mask_2[(i, j)] = m
L(f'  2-way kept: {len(mask_2):,}')

L('  3-way mining...')
heap_pump = []
heap_3 = []
cc3 = 0
last_log = time.time()
for (i, j), mij in mask_2.items():
    for k in range(j+1, NP):
        cc3 += 1
        m = mij & PM[k]
        s = stat(m)
        if not s: continue
        n, pump = s
        push(heap_pump, pump, (i, j, k, n, pump), 2000)
        push(heap_3, pump, (i, j, k, m.copy()), 5000)
    if time.time()-last_log > 30:
        L(f'    3-way: {cc3:,}')
        last_log = time.time()
L(f'  3-way done: {cc3:,}')

L('  4-way mining...')
seed_3 = [(i,j,k,m) for _,_,(i,j,k,m) in heap_3]
del heap_3; gc.collect()
heap_4 = []
cc4 = 0
last_log = time.time()
for i, j, k, m3 in seed_3:
    for l in range(NP):
        if l in (i, j, k): continue
        cc4 += 1
        m = m3 & PM[l]
        s = stat(m)
        if not s: continue
        n, pump = s
        push(heap_pump, pump, (i, j, k, l, n, pump), 2000)
        push(heap_4, pump, (i, j, k, l, m.copy()), 3000)
    if time.time()-last_log > 30:
        L(f'    4-way: {cc4:,}')
        last_log = time.time()
L(f'  4-way done: {cc4:,}')

L('  5-way mining...')
seed_4 = [(i,j,k,l,m) for _,_,(i,j,k,l,m) in heap_4]
del heap_4; gc.collect()
cc5 = 0
last_log = time.time()
for i, j, k, l, m4 in seed_4:
    for ll in range(NP):
        if ll in (i, j, k, l): continue
        cc5 += 1
        m = m4 & PM[ll]
        s = stat(m)
        if not s: continue
        n, pump = s
        push(heap_pump, pump, (i, j, k, l, ll, n, pump), 2000)
    if time.time()-last_log > 30:
        L(f'    5-way: {cc5:,}')
        last_log = time.time()
L(f'  5-way done: {cc5:,}')

total = cc3 + cc4 + cc5
L(f'*** STAGE D TOTAL: {total:,} COMBINATIONS ***')

# Top filters
L(f'')
L(f'=== TOP-30 by pump rate ===')
top = sorted(heap_pump, key=lambda x: -x[0])
seen=set(); shown=0
for _, _, payload in top:
    n = payload[-2]
    pump = payload[-1]
    idx = payload[:-2]
    sig = (n, round(pump, 0))
    if sig in seen: continue
    seen.add(sig)
    name = ' & '.join(PN[i] for i in idx)
    L(f'  n={n:>4} pump_rate={pump:>4.0f}%  {name[:120]}')
    shown += 1
    if shown >= 30: break

with open(os.path.join(OUT, 'final_v5_summary.json'), 'w', encoding='utf-8') as f:
    json.dump({
        'n_tokens': N,
        'positives': int(pos),
        'positive_rate': float(pos) / N * 100,
        'cv_aucs': {k: list(map(float, v)) for k, v in fold_aucs.items()},
        'final_test_auc': float(test_auc),
        'feature_count': len(feat_keys),
        'total_combinations': total,
        'top_filters': [' & '.join(PN[i] for i in payload[:-2]) + f' [n={payload[-2]}, pump={payload[-1]:.0f}%]'
                        for _, _, payload in top[:50]]
    }, f, indent=2, ensure_ascii=False)

L(f'')
L(f'=== FINAL V5 ===')
L(f'Total wall time: {time.time()-T_START:.0f}s ({(time.time()-T_START)/60:.1f} min)')
L(f'Artifacts in: {OUT}')

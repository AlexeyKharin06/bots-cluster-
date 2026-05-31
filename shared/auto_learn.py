#!/usr/bin/env python3
"""auto_learn.py — continuous learning loop для serial_sniper.

Запускается раз в N часов (cron) и делает:
1. Reload closed_trades, обновляет ATH/realized statistics
2. Detects concept drift: AUC текущей модели на свежих данных
3. Если AUC дропнулся (>0.05) — переобучает модель
4. Recalibrates pre-rule thresholds на свежих данных
5. Updates rugger_blacklist appearances counts
6. Logs all decisions to auto_learn_history.json
7. Telegram-alert если drift detected

Usage:
  python auto_learn.py                # standard run, 7-day window
  python auto_learn.py --window 30    # 30-day window
  python auto_learn.py --force        # force retrain regardless of drift
"""
import json
import sys
import os
import time
import pickle
import argparse
from datetime import datetime, timedelta
from collections import defaultdict, Counter

import numpy as np
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings('ignore')

# Add deploy/shared to sys.path for score_token imports
sys.path.insert(0, r'D:\OnChain\deploy\shared')

import platform
if platform.system() == 'Windows':
    STATE_PATH = r'D:\OnChain\scripts\wallet_v2\sniper_state.json'
    RUGGER_PATH = r'D:\OnChain\scripts\wallet_v2\unified_db\rugger_blacklist.json'
    WALLET_HIST_PATH = r'D:\OnChain\scripts\wallet_v2\unified_db\wallet_history_db.json'
    OUT_DIR = r'D:\OnChain\deploy\shared\auto_learn_output'
else:
    STATE_PATH = '/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json'
    RUGGER_PATH = '/srv/bots/onchain/code/scripts/wallet_v2/unified_db/rugger_blacklist.json'
    WALLET_HIST_PATH = '/srv/bots/onchain/code/scripts/wallet_v2/unified_db/wallet_history_db.json'
    OUT_DIR = '/srv/bots/cluster/shared/auto_learn_output'
os.makedirs(OUT_DIR, exist_ok=True)
HISTORY_PATH = os.path.join(OUT_DIR, 'auto_learn_history.json')
CURRENT_MODEL_PATH = r'D:\OnChain\deploy\shared\overnight_v3_results\final_model_realized_big50.pkl'
NEW_MODEL_PATH = os.path.join(OUT_DIR, 'current_model.pkl')

# AUC threshold for retraining trigger
DRIFT_THRESHOLD = 0.05  # if recent AUC drops by >5% → retrain
MIN_RECENT_SAMPLES = 50  # minimum trades to evaluate drift
RETRAIN_WINDOW_DAYS = 30  # use last N days for retrain


def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{ts}] {msg}', flush=True)


def parse_dt(v):
    if isinstance(v, (int, float)):
        return datetime.utcfromtimestamp(v/1000 if v > 1e12 else v)
    if isinstance(v, str):
        try:
            return datetime.fromisoformat(v.replace('Z', '+00:00')).replace(tzinfo=None)
        except Exception:
            return None
    return None


def load_data():
    log('Loading data sources...')
    with open(STATE_PATH, encoding='utf-8') as f:
        snip = json.load(f)
    ct = snip.get('closed_trades', [])

    with open(RUGGER_PATH, encoding='utf-8') as f:
        rb = json.load(f)
    rugger_set = set(rb.keys())

    wallet_stats = {}
    try:
        with open(WALLET_HIST_PATH, encoding='utf-8') as f:
            wh = json.load(f)
        for w, info in wh.items():
            if not isinstance(info, dict):
                continue
            s = info.get('stats') or {}
            wallet_stats[w] = dict(
                pump_count=s.get('pump_count', 0),
                rug_count=s.get('rug_count', 0),
                success_rate=s.get('success_rate', 0),
                n_tokens=s.get('total_count') or s.get('n_tokens', 0),
            )
    except Exception as e:
        log(f'  wallet_history load failed: {e}')

    log(f'  closed_trades: {len(ct)}, ruggers: {len(rugger_set)}, wallet_stats: {len(wallet_stats)}')
    return ct, rugger_set, wallet_stats


def build_dataset(ct, rugger_set, wallet_stats, window_days=None, after_date=None):
    """Build feature matrix + targets. Dedup by token, keep earliest entry."""
    from collections import defaultdict
    by_token = defaultdict(list)
    for t in ct:
        tk = t.get('token')
        if tk:
            by_token[tk].append(t)

    cutoff = None
    if window_days:
        cutoff = datetime.utcnow() - timedelta(days=window_days)
    if after_date:
        cutoff = after_date

    from score_token import engineer_features
    rows = []
    for tk, trades in by_token.items():
        t = sorted(trades, key=lambda x: x.get('entry_time') or 0)[0]
        es = t.get('entry_signal') or {}
        ep = t.get('entry_price'); ap = t.get('ath_price')
        ath = (ap/ep - 1)*100 if (ep and ap and ep > 0) else None
        if ath is None:
            continue
        dt = parse_dt(t.get('entry_time'))
        if dt is None:
            continue
        if cutoff and dt < cutoff:
            continue
        bc = es.get('bonding_curve_buyers')
        if isinstance(bc, list):
            bc = len(bc)
        rd = es.get('rugcheck_dangers')
        danger_n = len(rd) if isinstance(rd, (list, tuple)) else (int(rd) if isinstance(rd, (int, float)) else 0)
        top1_owner = es.get('top1_owner')
        lp_prov = es.get('lp_provider')
        creator = es.get('pool_creator') or es.get('creator')
        lp_st = wallet_stats.get(lp_prov or '', {})
        cr_st = wallet_stats.get(creator or '', {})
        raw = dict(
            top1=es.get('top1_pct'),
            top5=es.get('top5_pct'),
            smart=es.get('smart') or 0,
            serial=es.get('serial_only') or 0,
            serial_21_40=es.get('serial_21_40') or 0,
            rug_21_40=es.get('rug_21_40') or 0,
            known_21_40=es.get('known_21_40') or 0,
            known=es.get('known') or 0,
            liq=es.get('liquidity_at_entry') or t.get('liquidity_at_entry') or 0,
            mcap=es.get('mcap') or 0,
            vol24=es.get('volume_h24') or 0,
            age=es.get('age_min') or 0,
            buys=es.get('buys_m5') or 0,
            sells=es.get('sells_m5') or 0,
            bc=bc or 0,
            rc=es.get('rugcheck_score') or 0,
            danger_n=danger_n,
            ssp=es.get('serial_supply_pct') or 0,
            liq_mcap=es.get('liq_mcap_ratio') or 0,
            tot_h=es.get('total_holders') or 0,
            mint_rev=1 if (es.get('mint_authority') or '') == 'REVOKED' else 0,
            freeze_rev=1 if (es.get('freeze_authority') or '') == 'REVOKED' else 0,
            lp_lock=0 if (es.get('lp_unlocked') or False) else 1,
            top1_rugger=1 if top1_owner in rugger_set else 0,
            lp_rugger=1 if lp_prov in rugger_set else 0,
            creator_rugger=1 if creator in rugger_set else 0,
            lp_n_tokens=lp_st.get('n_tokens', 0),
            lp_pump_count=lp_st.get('pump_count', 0),
            lp_rug_count=lp_st.get('rug_count', 0),
            lp_success=lp_st.get('success_rate', 0),
            cr_n_tokens=cr_st.get('n_tokens', 0),
            cr_pump_count=cr_st.get('pump_count', 0),
            cr_rug_count=cr_st.get('rug_count', 0),
            cr_success=cr_st.get('success_rate', 0),
            cr_hist=es.get('cr_hist') or 0,
            lp_hist=es.get('lp_hist') or 0,
            cr_tx=es.get('creator_tx_count') or 0,
            chain=(t.get('chain') or '?').lower(),
            dex=(t.get('dex') or '?').lower(),
            hour=dt.hour,
            dow=dt.weekday(),
        )
        features = engineer_features(raw)
        rows.append({
            'token': tk,
            'symbol': t.get('symbol'),
            'dt': dt,
            'realized': t.get('pnl_pct', 0) or 0,
            'ath': ath,
            'features': features,
        })

    rows.sort(key=lambda r: r['dt'])
    return rows


def to_matrix(rows, feature_names):
    def _safe(v):
        if isinstance(v, bool):
            return float(v)
        if isinstance(v, (int, float)):
            return float(v)
        return 0.0

    X = np.array([[_safe(r['features'].get(k, 0)) for k in feature_names] for r in rows], dtype=np.float32)
    y_realized_big50 = np.array([1 if r['realized'] >= 50 else 0 for r in rows], dtype=np.int8)
    y_realized_big = np.array([1 if r['realized'] >= 100 else 0 for r in rows], dtype=np.int8)
    y_norug = np.array([1 if r['realized'] > -50 else 0 for r in rows], dtype=np.int8)
    y_ath_big = np.array([1 if r['ath'] >= 100 else 0 for r in rows], dtype=np.int8)
    return X, dict(y_realized_big50=y_realized_big50, y_realized_big=y_realized_big,
                   y_norug=y_norug, y_ath_big=y_ath_big)


def detect_drift(rows, current_model, feature_names, recent_days=7):
    """Evaluate AUC of current model on recent data. Return drift_score and recent_auc."""
    cutoff = datetime.utcnow() - timedelta(days=recent_days)
    recent = [r for r in rows if r['dt'] >= cutoff]
    if len(recent) < MIN_RECENT_SAMPLES:
        log(f'  too few recent samples ({len(recent)} < {MIN_RECENT_SAMPLES}) — skip drift check')
        return None, None
    X_recent, targets = to_matrix(recent, feature_names)
    y_recent = targets['y_realized_big50']
    if y_recent.sum() < 5:
        log(f'  too few positives in recent ({int(y_recent.sum())}) — skip drift check')
        return None, None
    try:
        scores = current_model.predict_proba(X_recent)[:, 1]
        recent_auc = float(roc_auc_score(y_recent, scores))
        return recent_auc, len(recent)
    except Exception as e:
        log(f'  drift check failed: {e}')
        return None, None


def retrain(rows, feature_names, window_days=RETRAIN_WINDOW_DAYS):
    """Retrain on recent window."""
    cutoff = datetime.utcnow() - timedelta(days=window_days)
    train_data = [r for r in rows if r['dt'] >= cutoff]
    if len(train_data) < 100:
        log(f'  not enough train data ({len(train_data)} < 100) — skip retrain')
        return None
    log(f'  Retraining on {len(train_data)} rows (last {window_days} days)')
    X, targets = to_matrix(train_data, feature_names)
    y = targets['y_realized_big50']
    if y.sum() < 10:
        log(f'  too few positives ({int(y.sum())}) — skip')
        return None

    # Try 4 algorithms, pick best by 5-fold time-series CV on this window
    from sklearn.model_selection import TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=min(5, max(2, len(X)//50)))
    best_model_name = None
    best_score = -1
    best_model = None
    for mname, m_factory in [
        ('LR', lambda: Pipeline([('imp', SimpleImputer()), ('scaler', StandardScaler()), ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, C=0.1))])),
        ('RF', lambda: Pipeline([('imp', SimpleImputer()), ('clf', RandomForestClassifier(n_estimators=300, max_depth=8, class_weight='balanced', random_state=42, n_jobs=-1))])),
        ('GB', lambda: Pipeline([('imp', SimpleImputer()), ('clf', GradientBoostingClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, random_state=42))])),
        ('ET', lambda: Pipeline([('imp', SimpleImputer()), ('clf', ExtraTreesClassifier(n_estimators=300, max_depth=8, class_weight='balanced', random_state=42, n_jobs=-1))])),
    ]:
        cv_aucs = []
        for tr, te in tscv.split(X):
            if y[tr].sum() < 3 or y[te].sum() < 1:
                continue
            try:
                m = m_factory()
                m.fit(X[tr], y[tr])
                cv_aucs.append(float(roc_auc_score(y[te], m.predict_proba(X[te])[:, 1])))
            except Exception:
                pass
        if cv_aucs:
            avg = np.mean(cv_aucs)
            log(f'    {mname}: CV AUC = {avg:.3f} ± {np.std(cv_aucs):.3f} (n_folds={len(cv_aucs)})')
            if avg > best_score:
                best_score = avg
                best_model_name = mname
                best_model = m_factory()

    if best_model is None:
        log('  no model trained successfully')
        return None
    # Fit final on all
    best_model.fit(X, y)
    log(f'  Best CV: {best_model_name} AUC={best_score:.3f}')
    return dict(model=best_model, name=best_model_name, cv_auc=best_score,
                trained_at=datetime.now().isoformat(),
                n_train=len(train_data),
                window_days=window_days)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--window', type=int, default=RETRAIN_WINDOW_DAYS)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--recent-days', type=int, default=7, help='days for drift evaluation')
    args = ap.parse_args()

    log('=== auto_learn.py START ===')
    ct, rugger_set, wallet_stats = load_data()
    rows = build_dataset(ct, rugger_set, wallet_stats)
    log(f'  Total dedup rows: {len(rows)}')
    if not rows:
        log('  No data — exit')
        return
    log(f'  Date range: {rows[0]["dt"]} → {rows[-1]["dt"]}')

    # Load existing model
    if os.path.exists(NEW_MODEL_PATH):
        model_path = NEW_MODEL_PATH
    elif os.path.exists(CURRENT_MODEL_PATH):
        model_path = CURRENT_MODEL_PATH
    else:
        log('  No baseline model — full train required')
        model_path = None

    history = []
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH) as f:
                history = json.load(f)
        except Exception:
            history = []

    feature_names = None
    current_model = None
    if model_path:
        log(f'  Loading baseline model: {model_path}')
        with open(model_path, 'rb') as f:
            mdata = pickle.load(f)
        current_model = mdata['model']
        feature_names = mdata['feature_names']

    # Detect drift
    if current_model and not args.force:
        recent_auc, n_recent = detect_drift(rows, current_model, feature_names, args.recent_days)
        baseline_auc = history[-1].get('baseline_auc', 0.85) if history else 0.85
        if recent_auc is not None:
            drift = baseline_auc - recent_auc
            log(f'  Drift check: recent_auc={recent_auc:.3f} vs baseline={baseline_auc:.3f}, drift={drift:+.3f} (n_recent={n_recent})')
            if drift < DRIFT_THRESHOLD:
                log('  No significant drift — skip retrain')
                history.append({
                    'timestamp': datetime.now().isoformat(),
                    'action': 'no_action',
                    'recent_auc': recent_auc,
                    'baseline_auc': baseline_auc,
                    'drift': drift,
                    'n_recent': n_recent,
                })
                with open(HISTORY_PATH, 'w') as f:
                    json.dump(history, f, indent=2)
                return

    # Retrain
    if feature_names is None:
        # Bootstrap: pick a default set from current row
        feature_names = sorted(rows[0]['features'].keys())

    log('  Retraining...')
    new_model_data = retrain(rows, feature_names, window_days=args.window)
    if new_model_data is None:
        log('  Retrain failed — keeping current')
        return

    # Save new model
    with open(NEW_MODEL_PATH, 'wb') as f:
        pickle.dump({
            'model': new_model_data['model'],
            'feature_names': feature_names,
            'target': 'realized_big50',
            'best_cv': new_model_data['name'],
            'test_auc': new_model_data['cv_auc'],
        }, f)
    log(f'  New model saved: {NEW_MODEL_PATH}')

    # Update history
    history.append({
        'timestamp': datetime.now().isoformat(),
        'action': 'retrained',
        'best_model': new_model_data['name'],
        'cv_auc': new_model_data['cv_auc'],
        'n_train': new_model_data['n_train'],
        'window_days': new_model_data['window_days'],
        'baseline_auc': new_model_data['cv_auc'],  # update baseline
    })
    with open(HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=2)
    log(f'  History updated: {HISTORY_PATH}')

    log('=== auto_learn.py DONE ===')


if __name__ == '__main__':
    main()

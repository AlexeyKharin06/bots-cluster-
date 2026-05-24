#!/usr/bin/env python3
"""position_trajectory_monitor.py — снимает snapshots каждой open position каждые 5 мин.

Для каждой токена в open_positions:
  - Каждые 5 мин: fetch DexScreener (price, liq, holders, vol_m5, buys, sells)
  - Append к /srv/bots/.shared/data/trajectories/<mint>.jsonl
  - После exit (token больше не в open_positions): trajectory closed,
    AI brain может анализировать форму pump-кривой

Запускается на VPS via cron:
  */5 * * * * /usr/bin/python3 /srv/bots/cluster/shared/position_trajectory_monitor.py >> /srv/bots/.shared/logs/trajectory.log 2>&1

Output Format (per row):
  {"ts":"...", "mint":"...", "elapsed_min":7, "price":0.0001, "mcap":50000,
   "liq":15000, "vol_m5":3000, "buys_m5":12, "sells_m5":5, "top1_pct":15.2}

AI brain analysis:
  - Pump phases identification (accumulation/markup/distribution/decay)
  - Time-to-peak distribution
  - Drawdown-from-peak distribution
  - Pattern classification (V/plateau/staircase)
"""
import json, os, time, urllib.request
from pathlib import Path
from datetime import datetime, timezone

SHARED = Path('/srv/bots/.shared/data/trajectories')
SHARED.mkdir(parents=True, exist_ok=True)
STATE_PATH = Path('/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json')

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'}


def fetch_pair(mint):
    """DexScreener token endpoint — найти все pairs этого mint."""
    try:
        req = urllib.request.Request(f'https://api.dexscreener.com/latest/dex/tokens/{mint}', headers=UA)
        r = urllib.request.urlopen(req, timeout=10)
        d = json.loads(r.read())
        pairs = d.get('pairs', []) or []
        if not pairs:
            return None
        # Pick the one with highest liquidity
        pairs.sort(key=lambda p: -(((p.get('liquidity') or {}).get('usd') or 0)))
        return pairs[0]
    except Exception as e:
        print(f'[err] {mint[:10]}: {e}', flush=True)
        return None


def snapshot_row(mint, entry_time, p):
    pc = p.get('priceChange', {}) or {}
    txns_m5 = (p.get('txns', {}) or {}).get('m5', {}) or {}
    elapsed_min = int((time.time() - entry_time) / 60) if entry_time else None
    return {
        'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'mint': mint,
        'elapsed_min': elapsed_min,
        'price': p.get('priceUsd'),
        'price_change_m5': pc.get('m5'),
        'price_change_h1': pc.get('h1'),
        'mcap': p.get('marketCap'),
        'liq': (p.get('liquidity', {}) or {}).get('usd'),
        'vol_m5': (p.get('volume', {}) or {}).get('m5'),
        'vol_h1': (p.get('volume', {}) or {}).get('h1'),
        'buys_m5': txns_m5.get('buys'),
        'sells_m5': txns_m5.get('sells'),
        'pair': p.get('pairAddress'),
    }


def main():
    if not STATE_PATH.exists():
        print('[err] sniper_state.json missing', flush=True)
        return
    s = json.load(STATE_PATH.open())
    op = s.get('open_positions', []) or []
    print(f'[{datetime.now(timezone.utc).isoformat()}] monitoring {len(op)} open positions', flush=True)

    for pos in op:
        mint = pos.get('mint') or (pos.get('entry_signal') or {}).get('mint') or pos.get('token_address')
        if not mint:
            continue
        entry_ts_raw = pos.get('entry_time') or pos.get('opened_at') or pos.get('time_opened')
        entry_ts = None
        if entry_ts_raw:
            try:
                if isinstance(entry_ts_raw, (int, float)):
                    entry_ts = entry_ts_raw if entry_ts_raw > 1e10 else entry_ts_raw  # already sec
                else:
                    entry_ts = datetime.fromisoformat(str(entry_ts_raw).replace('Z', '+00:00')).timestamp()
            except Exception:
                entry_ts = None

        p = fetch_pair(mint)
        if not p:
            continue
        row = snapshot_row(mint, entry_ts, p)
        fpath = SHARED / f'{mint}.jsonl'
        with fpath.open('a', encoding='utf-8') as f:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
        time.sleep(0.3)  # rate-limit pause

    print(f'  done snapshots', flush=True)


if __name__ == '__main__':
    main()

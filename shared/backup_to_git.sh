#!/bin/bash
# backup_to_git.sh — ежедневный бэкап критичных live данных в cluster git.
# Если VPS упадёт — восстанавливается всё кроме больших raw DB.
# Cron: 0 4 * * * /srv/bots/cluster/shared/backup_to_git.sh >> /srv/bots/cluster/shared/backup.log 2>&1

CLUSTER="/srv/bots/cluster"
ONCHAIN="/srv/bots/onchain/code"
BACKUP_DIR="$CLUSTER/shared/live_backups"

mkdir -p "$BACKUP_DIR"

cd "$CLUSTER"
git config --global user.email "bot@vps.local" 2>/dev/null
git config --global user.name "vps-bot" 2>/dev/null

# 1. closed_trades summary (small CSV)
python3 -c "
import json
import csv
with open('$ONCHAIN/scripts/wallet_v2/sniper_state.json') as f:
    s = json.load(f)
ct = s.get('closed_trades', [])
print(f'Total closed_trades: {len(ct)}')
# Last 1000 trades summary
recent = ct[-1000:]
with open('$BACKUP_DIR/closed_trades_summary.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['token', 'symbol', 'stream', 'entry_time', 'exit_time', 'pnl_pct', 'realized_usd', 'ath_pct', 'hold_min', 'exit_reason', 'chain', 'dex'])
    for t in recent:
        ath_pct = None
        ep, ap = t.get('entry_price'), t.get('ath_price')
        if ep and ap and ep > 0:
            ath_pct = round((ap/ep-1)*100, 1)
        w.writerow([
            t.get('token','')[:32],
            t.get('symbol',''),
            t.get('stream',''),
            t.get('entry_time'),
            t.get('exit_time'),
            round(t.get('pnl_pct', 0) or 0, 2),
            round(t.get('pnl_usd', 0) or 0, 2),
            ath_pct,
            t.get('hold_min'),
            t.get('exit_reason'),
            t.get('chain'),
            t.get('dex'),
        ])
print('CSV saved')
" 2>&1 | tail -3

# 2. Per-stream daily aggregates (small)
python3 -c "
import json
from collections import defaultdict
from datetime import datetime
with open('$ONCHAIN/scripts/wallet_v2/sniper_state.json') as f:
    s = json.load(f)
ct = s.get('closed_trades', [])
agg = defaultdict(lambda: {'n':0, 'sum_pnl':0, 'wins':0, 'rugs':0, 'bigs':0, 'huges':0})
for t in ct:
    stream = t.get('stream') or 'UNKNOWN'
    pnl = t.get('pnl_pct', 0) or 0
    agg[stream]['n'] += 1
    agg[stream]['sum_pnl'] += pnl
    if pnl > 0: agg[stream]['wins'] += 1
    if pnl <= -50: agg[stream]['rugs'] += 1
    if pnl >= 100: agg[stream]['bigs'] += 1
    if pnl >= 500: agg[stream]['huges'] += 1
result = {}
for k, v in agg.items():
    n = v['n']
    if n > 0:
        result[k] = {
            'n': n,
            'avg_pnl': round(v['sum_pnl']/n, 1),
            'wr_pct': round(v['wins']/n*100, 1),
            'rug_pct': round(v['rugs']/n*100, 1),
            'big_pct': round(v['bigs']/n*100, 1),
            'huge_pct': round(v['huges']/n*100, 1),
        }
with open('$BACKUP_DIR/per_stream_aggregates.json', 'w') as f:
    json.dump(result, f, indent=2)
print(f'Stream aggregates: {len(result)} streams')
" 2>&1 | tail -3

# 3. ML model state
mkdir -p "$BACKUP_DIR/models"
cp "$CLUSTER/shared/auto_learn_output/current_model.pkl" "$BACKUP_DIR/models/current_model.pkl" 2>/dev/null
cp "$CLUSTER/shared/auto_learn_output/auto_learn_history.json" "$BACKUP_DIR/models/auto_learn_history.json" 2>/dev/null

# 4. Helius key status
cp "$ONCHAIN/scripts/wallet_v2/helius_key_status.json" "$BACKUP_DIR/helius_key_status.json" 2>/dev/null

# 5. Open positions snapshot (small)
python3 -c "
import json
with open('$ONCHAIN/scripts/wallet_v2/sniper_state.json') as f:
    s = json.load(f)
with open('$BACKUP_DIR/open_positions_snapshot.json', 'w') as f:
    json.dump(s.get('open_positions', []), f, indent=2, default=str)
" 2>&1 | tail -2

# 6. Per-day daily report extracts (small)
TODAY=$(date -u +%Y-%m-%d)
mkdir -p "$BACKUP_DIR/daily/$TODAY"
# Save key signals if exist
cp "$ONCHAIN/scripts/wallet_v2/pump_fun_signals.json" "$BACKUP_DIR/daily/$TODAY/pump_fun_signals.json" 2>/dev/null
cp "$ONCHAIN/scripts/wallet_v2/dexscreener_signals.json" "$BACKUP_DIR/daily/$TODAY/dexscreener_signals.json" 2>/dev/null
cp "$ONCHAIN/scripts/wallet_v2/signals_pool.json" "$BACKUP_DIR/daily/$TODAY/signals_pool.json" 2>/dev/null

# Cleanup: keep only last 30 days of daily folders
find "$BACKUP_DIR/daily/" -maxdepth 1 -mindepth 1 -type d -mtime +30 -exec rm -rf {} \; 2>/dev/null

# 7. Git commit + push
cd "$CLUSTER"
git add shared/live_backups/ 2>&1 | tail -3
git commit -m "auto-backup $TODAY: live data + models + signals" 2>&1 | tail -3
git push origin main 2>&1 | tail -3

echo "[$(date)] Backup done — pushed to git"

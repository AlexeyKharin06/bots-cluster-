#!/bin/bash
# vacation_restart.sh — vacation autonomous mode on VPS.
# Run on VPS:
#   sudo git config --global --add safe.directory /srv/bots/onchain/code
#   sudo git config --global --add safe.directory /srv/bots/cluster
#   cd /srv/bots/onchain/code && git pull
#   cd /srv/bots/cluster && git pull
#   bash /srv/bots/cluster/shared/vacation_restart.sh

set -e
ONCHAIN="/srv/bots/onchain/code"
CLUSTER="/srv/bots/cluster"

echo "=== VACATION RESTART ==="

# 1. Permissions
chmod +x $CLUSTER/shared/auto_health.sh 2>/dev/null || true
chmod +x $CLUSTER/shared/vacation_restart.sh 2>/dev/null || true

# 2. Cron setup — remove old, add new
echo "[1] Setup cron jobs..."
crontab -l 2>/dev/null | grep -v 'auto_health\|auto_learn\|helius_key_health\|claude.*session\|claude_session' > /tmp/crontab_clean.txt || true

cat >> /tmp/crontab_clean.txt << CRON_EOF

# === Vacation mode (auto-installed) ===
# Health check каждые 6h — TG alert
0 */6 * * * $CLUSTER/shared/auto_health.sh
# Auto-learn ML модели — каждую ночь 03:00 UTC
0 3 * * * cd $CLUSTER && python3 shared/auto_learn.py >> shared/auto_learn_output/auto_learn.log 2>&1
# Helius key health — каждые 6h
30 */6 * * * cd $ONCHAIN && node scripts/wallet_v2/helius_key_health.js >> scripts/wallet_v2/helius_key_health.log 2>&1
CRON_EOF
crontab /tmp/crontab_clean.txt
rm /tmp/crontab_clean.txt
echo "   Crontab установлен. Новые задачи:"
crontab -l | grep -E "auto_health|auto_learn|helius_key" | head -5

# 3. Helius key health (immediate snapshot)
echo ""
echo "[2] Helius key health snapshot..."
cd $ONCHAIN && node scripts/wallet_v2/helius_key_health.js 2>&1 | head -20

# 4. Stop old processes
echo ""
echo "[3] Stopping old sniper/watchdog..."
pkill -f 'node.*serial_sniper' 2>/dev/null || true
pkill -f 'watchdog.sh' 2>/dev/null || true
pkill -f 'node.*lp_monitor' 2>/dev/null || true
pkill -f 'node.*lp_bot' 2>/dev/null || true
sleep 3

# 5. Start watchdog (lifts sniper + lp_monitor + lp_bot + daily_report)
echo ""
echo "[4] Starting watchdog..."
cd $ONCHAIN/scripts/wallet_v2
nohup bash watchdog.sh >> watchdog.log 2>&1 &
sleep 10

# 6. Verify processes
echo ""
echo "[5] Active processes:"
ps -ef | grep -E 'node.*(serial_sniper|lp_monitor|lp_bot|watchdog)' | grep -v grep | head -10

echo ""
echo "[6] Recent sniper.log:"
tail -20 $ONCHAIN/scripts/wallet_v2/sniper.log 2>/dev/null

echo ""
echo "[7] Helius optimizer loaded?"
tail -50 $ONCHAIN/scripts/wallet_v2/sniper.log 2>/dev/null | grep -E "HELIUS_OPT|HELIUS.*loaded|ML_SCORER" | head -5

echo ""
echo "=== DEPLOY DONE ==="
echo "Cron активен: каждые 6h health + key check, каждую ночь auto_learn"
echo "По возвращении: python3 $CLUSTER/shared/per_stream_report.py"

#!/bin/bash
# recover_onchain.sh — полное восстановление OnChain sniper после краша watchdog.
# Запуск (на VPS под root):
#   bash <(curl -fsSL https://raw.githubusercontent.com/AlexeyKharin06/bots-cluster-/main/shared/recover_onchain.sh)
#
# Что делает:
#   1. Убивает все зомби-процессы wallet_v2 + старый watchdog
#   2. Заменяет watchdog.sh на Linux-compatible версию (pgrep/pkill вместо wmic/taskkill)
#   3. Запускает чистый watchdog под пользователем bots
#   4. Ждёт 30 сек и показывает количество процессов

set -e
log() { echo "[recover] $*"; }

WATCHDOG=/srv/bots/onchain/code/scripts/wallet_v2/watchdog.sh
ONCHAIN_LOGS=/srv/bots/onchain/logs

log "=== STEP 1: killing all stale processes ==="
pkill -9 -u bots -f wallet_v2 2>/dev/null || true
pkill -9 -u bots -f watchdog.sh 2>/dev/null || true
sleep 3
LEFT=$(pgrep -u bots -af wallet_v2 2>/dev/null | wc -l)
log "remaining wallet_v2 processes: $LEFT"

log "=== STEP 2: backup old watchdog ==="
[ -f "$WATCHDOG" ] && cp "$WATCHDOG" "$WATCHDOG.bak.$(date +%s)"

log "=== STEP 3: writing Linux-native watchdog.sh ==="
cat > "$WATCHDOG" <<'WATCHDOG_EOF'
#!/bin/bash
# Watchdog: перезапускает sniper, lp_monitor, lp_bot, etc. если упали.
# Linux-native (pgrep/pkill). Windows fallback оставлен для совместимости.

DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"

is_running() {
  local pattern="$1"
  if command -v pgrep >/dev/null 2>&1; then
    pgrep -f "$pattern" >/dev/null 2>&1
    return $?
  fi
  local count
  count=$(wmic process where "name='node.exe'" get commandline 2>/dev/null | grep -c "$pattern")
  if [ "$count" -gt 0 ]; then return 0; fi
  count=$(wmic process where "name='python.exe'" get commandline 2>/dev/null | grep -c "$pattern")
  if [ "$count" -gt 0 ]; then return 0; fi
  return 1
}

get_pid() {
  local pattern="$1"
  if command -v pgrep >/dev/null 2>&1; then
    pgrep -f "$pattern" | head -1
    return
  fi
  wmic process where "name='node.exe'" get commandline,processid 2>/dev/null | \
    grep "$pattern" | grep -oE '[0-9]+\s*$' | head -1 | tr -d ' '
}

log_stale() {
  local logfile="$1"
  local minutes="$2"
  [ -f "$logfile" ] || return 1
  find "$logfile" -mmin -"$minutes" 2>/dev/null | grep -q . && return 1
  return 0
}

kill_hung() {
  local pattern="$1"
  if command -v pkill >/dev/null 2>&1; then
    local pids=$(pgrep -f "$pattern" 2>/dev/null)
    [ -n "$pids" ] && {
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] $pattern HUNG -> killing pids: $pids"
      echo "$pids" | xargs -r kill -9 2>/dev/null
      return 0
    }
    return 1
  fi
  local pid=$(get_pid "$pattern")
  [ -n "$pid" ] && {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $pattern HUNG (log stale) PID=$pid -> killing"
    taskkill //F //PID "$pid" >/dev/null 2>&1
    return 0
  }
  return 1
}

start_sniper() {
  cd "$ROOT"
  # Защита: убей старого sniper перед спавном (защита от накопления зомби)
  command -v pkill >/dev/null 2>&1 && pkill -9 -f "serial_sniper.js" 2>/dev/null
  sleep 1
  node --max-old-space-size=4096 scripts/wallet_v2/serial_sniper.js >> "$DIR/sniper.log" 2>&1 &
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] sniper started"
}

start_lpmon() {
  cd "$ROOT"
  command -v pkill >/dev/null 2>&1 && pkill -9 -f "lp_monitor.js" 2>/dev/null
  sleep 1
  node --max-old-space-size=2048 scripts/wallet_v2/lp_monitor.js >> "$DIR/lp_monitor.log" 2>&1 &
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] lp_monitor started"
}

start_lpbot() {
  cd "$ROOT"
  command -v pkill >/dev/null 2>&1 && pkill -9 -f "lp_bot.js" 2>/dev/null
  sleep 1
  node scripts/wallet_v2/lp_bot.js >> "$DIR/lp_bot.log" 2>&1 &
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] lp_bot started"
}

start_pumpfun() {
  cd "$ROOT"
  command -v pkill >/dev/null 2>&1 && pkill -9 -f "pumpfun_monitor.js" 2>/dev/null
  sleep 1
  node scripts/wallet_v2/pumpfun_monitor.js >> "$DIR/pumpfun_monitor.log" 2>&1 &
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] pumpfun_monitor started"
}

start_dexscr() {
  cd "$ROOT"
  command -v pkill >/dev/null 2>&1 && pkill -9 -f "dexscreener_signals.js" 2>/dev/null
  sleep 1
  node scripts/wallet_v2/dexscreener_signals.js >> "$DIR/dexscreener_signals.log" 2>&1 &
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] dexscreener_signals started"
}

start_tg_listener() {
  cd "$ROOT/tg" 2>/dev/null || cd "$ROOT/../tg" 2>/dev/null || cd /srv/bots/onchain/tg
  command -v pkill >/dev/null 2>&1 && pkill -9 -f "tg_listener.py" 2>/dev/null
  sleep 1
  PYTHONIOENCODING=utf-8 nohup python3 tg_listener.py >> tg_listener.log 2>&1 &
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] tg_listener started"
}

DAILY_STAMP="$DIR/.last_daily_report_stamp"
maybe_run_daily() {
  local now=$(date +%s)
  local last=0
  [ -f "$DAILY_STAMP" ] && last=$(cat "$DAILY_STAMP" 2>/dev/null || echo 0)
  local elapsed=$((now - last))
  if [ "$elapsed" -ge 86400 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] daily report -> starting"
    cd "$ROOT"
    node scripts/wallet_v2/daily_neg_pos_report.js >> "$DIR/daily_report.log" 2>&1 &
    node scripts/wallet_v2/paper_streams_report.js >> "$DIR/paper_report.log" 2>&1 &
    echo "$now" > "$DAILY_STAMP"
  fi
}

RELEARN_STAMP="$DIR/.last_relearner_stamp"
maybe_run_relearner() {
  local now=$(date +%s)
  local last=0
  [ -f "$RELEARN_STAMP" ] && last=$(cat "$RELEARN_STAMP" 2>/dev/null || echo 0)
  local elapsed=$((now - last))
  if [ "$elapsed" -ge 604800 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] auto-relearner -> starting"
    cd "$ROOT"
    node scripts/wallet_v2/auto_relearner.js >> "$DIR/auto_relearner.log" 2>&1 &
    echo "$now" > "$RELEARN_STAMP"
  fi
}

echo "[$(date '+%Y-%m-%d %H:%M:%S')] watchdog starting (Linux-native)"
trap 'echo "[$(date)] watchdog stopped"; exit 0' INT TERM

while true; do
  if [ -f "$DIR/.sniper_disabled" ]; then
    :
  elif ! is_running "serial_sniper"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] sniper down"
    start_sniper
    sleep 30
  elif log_stale "$DIR/sniper.log" 5; then
    kill_hung "serial_sniper" && start_sniper
    sleep 30
  fi

  if ! is_running "lp_monitor"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] lp_monitor down"
    start_lpmon
    sleep 10
  elif log_stale "$DIR/lp_monitor.log" 15; then
    kill_hung "lp_monitor" && start_lpmon
    sleep 10
  fi

  if ! is_running "lp_bot"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] lp_bot down"
    start_lpbot
    sleep 10
  elif log_stale "$DIR/lp_bot.log" 15; then
    kill_hung "lp_bot" && start_lpbot
    sleep 10
  fi

  if ! is_running "pumpfun_monitor"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] pumpfun_monitor down"
    start_pumpfun
    sleep 5
  elif log_stale "$DIR/pumpfun_monitor.log" 10; then
    kill_hung "pumpfun_monitor" && start_pumpfun
    sleep 5
  fi

  if ! is_running "dexscreener_signals"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] dexscreener_signals down"
    start_dexscr
    sleep 5
  elif log_stale "$DIR/dexscreener_signals.log" 10; then
    kill_hung "dexscreener_signals" && start_dexscr
    sleep 5
  fi

  if ! is_running "tg_listener"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] tg_listener down"
    start_tg_listener
    sleep 5
  elif log_stale "/srv/bots/onchain/tg/tg_listener.log" 30; then
    kill_hung "tg_listener" && start_tg_listener
    sleep 5
  fi

  maybe_run_daily
  maybe_run_relearner

  sleep 60
done
WATCHDOG_EOF

chmod +x "$WATCHDOG"
chown bots:bots "$WATCHDOG"
log "watchdog.sh replaced ($(wc -l < $WATCHDOG) lines, pgrep count: $(grep -c pgrep $WATCHDOG))"

log "=== STEP 4: ensure logs dir exists ==="
mkdir -p "$ONCHAIN_LOGS"
chown -R bots:bots "$ONCHAIN_LOGS"

log "=== STEP 5: starting watchdog clean as bots ==="
sudo -u bots bash -c "cd /srv/bots/onchain/code/scripts/wallet_v2 && nohup bash watchdog.sh > $ONCHAIN_LOGS/watchdog.log 2>&1 < /dev/null &"

log "waiting 35s for daemons to spawn..."
sleep 35

log "=== STEP 6: status check ==="
COUNT=$(pgrep -u bots -af wallet_v2 2>/dev/null | wc -l)
log "active wallet_v2 processes: $COUNT (expected ~6)"
log "process list:"
pgrep -u bots -af "wallet_v2|watchdog.sh" 2>/dev/null | sed 's/^/  /'

log "=== STEP 7: recent watchdog log ==="
tail -20 "$ONCHAIN_LOGS/watchdog.log" 2>/dev/null | sed 's/^/  /'

log ""
log "=== DONE ==="
log "Check Telegram bot for next AI brain cycle alert (~next 0/6/12/18 UTC)"
log "If process count != 6, check $ONCHAIN_LOGS/watchdog.log + sniper.log"

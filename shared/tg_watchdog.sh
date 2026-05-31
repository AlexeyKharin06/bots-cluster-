#!/bin/bash
# tg_watchdog.sh — мониторит tg_unified_listener.py, перезапускает если heartbeat завис.
# Cron: */5 * * * * /srv/bots/cluster/shared/tg_watchdog.sh >> /srv/bots/cluster/shared/tg_watchdog.log 2>&1

LOG_FILE="/srv/bots/.shared/tg/tg_unified.log"
PID_PATTERN="tg_unified_listener.py"
RESTART_THRESHOLD_MIN=15

# Get current heartbeat counter
last_heartbeat=$(grep "heartbeat: events_received" "$LOG_FILE" 2>/dev/null | tail -1)
current_count=$(echo "$last_heartbeat" | grep -oP 'events_received=\K[0-9]+')

# Get previous (15 min ago)
prev_check_file="/tmp/tg_watchdog_prev_count"
prev_count=$(cat "$prev_check_file" 2>/dev/null || echo "0")

# Save current
echo "$current_count" > "$prev_check_file"

# Check if process exists
if ! pgrep -f "$PID_PATTERN" > /dev/null; then
  echo "[$(date)] PROCESS DEAD — restarting"
  cd /srv/bots/.shared/tg && sudo -u bots nohup python3 tg_unified_listener.py >> tg_unified.log 2>&1 &
  disown
  exit 0
fi

# Check if counter changed in last 15 min
if [ -z "$current_count" ] || [ -z "$prev_count" ]; then
  echo "[$(date)] Cannot determine heartbeat — first run"
  exit 0
fi

if [ "$current_count" = "$prev_count" ] && [ "$current_count" -gt 0 ]; then
  echo "[$(date)] HEARTBEAT STUCK at $current_count — restarting"
  pkill -9 -f "$PID_PATTERN" 2>/dev/null
  sleep 5
  cd /srv/bots/.shared/tg && sudo -u bots nohup python3 tg_unified_listener.py >> tg_unified.log 2>&1 &
  disown

  # TG alert
  TG_BOT="8237255734:AAHiS308o1j-j_plw8g-euYNXyuJTLynXg4"
  TG_CHAT="411831496"
  curl -s -X POST "https://api.telegram.org/bot${TG_BOT}/sendMessage" \
    -d "chat_id=${TG_CHAT}" \
    -d "text=⚠️ TG listener завис (counter=$current_count) — перезапустил автоматически" >/dev/null 2>&1
else
  echo "[$(date)] OK: heartbeat=$current_count (was $prev_count)"
fi

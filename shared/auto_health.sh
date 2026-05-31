#!/bin/bash
# auto_health.sh — здоровье снайпера на VPS.
# Cron: */360 * * * * /srv/bots/onchain/code/deploy/shared/auto_health.sh

# === CONFIG ===
TG_BOT="${TG_BOT:-8237255734:AAHiS308o1j-j_plw8g-euYNXyuJTLynXg4}"
TG_CHAT="${TG_CHAT:-411831496}"
PROJ="/srv/bots/onchain/code"
CLUSTER="/srv/bots/cluster"
STATE="${PROJ}/scripts/wallet_v2/sniper_state.json"
LOG="${PROJ}/scripts/wallet_v2/sniper.log"
HEALTH_LOG="${CLUSTER}/shared/auto_health.log"

alert() {
  local msg="$1"
  echo "[$(date)] ALERT: $msg" >> "$HEALTH_LOG"
  curl -s -X POST "https://api.telegram.org/bot${TG_BOT}/sendMessage" \
    -d "chat_id=${TG_CHAT}" \
    -d "text=⚠️ $(hostname): $msg" \
    -d "parse_mode=HTML" >/dev/null 2>&1
}

# === CHECK 1: sniper alive (state file refreshed within last 30 min) ===
if [ -f "$STATE" ]; then
  mtime=$(stat -c '%Y' "$STATE" 2>/dev/null || stat -f '%m' "$STATE" 2>/dev/null)
  now=$(date +%s)
  age=$((now - mtime))
  if [ $age -gt 1800 ]; then
    alert "sniper_state.json не обновлялся ${age}s — снайпер мог упасть"
  fi
else
  alert "sniper_state.json не существует"
fi

# === CHECK 2: процесс sniper жив ===
if ! pgrep -f "node.*serial_sniper.js" >/dev/null 2>&1; then
  alert "Процесс serial_sniper не запущен!"
fi

# === CHECK 3: watchdog жив ===
if ! pgrep -f "watchdog.sh" >/dev/null 2>&1; then
  alert "Watchdog не запущен"
fi

# === CHECK 4: disk space ===
disk_pct=$(df -P / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$disk_pct" -gt 90 ]; then
  alert "Disk usage ${disk_pct}% — критично"
elif [ "$disk_pct" -gt 80 ]; then
  alert "Disk usage ${disk_pct}% — high"
fi

# === CHECK 5: memory ===
mem_pct=$(free | awk '/^Mem:/ {printf "%.0f", $3/$2*100}')
if [ "$mem_pct" -gt 95 ]; then
  alert "Memory ${mem_pct}% — критично"
fi

# === CHECK 6: Helius credits — analyze sniper.log for dead keys ===
if [ -f "$LOG" ]; then
  dead_keys=$(tail -10000 "$LOG" | grep -c "max usage reached\|HTTP -32429" || echo 0)
  if [ "$dead_keys" -gt 100 ]; then
    alert "Helius keys жжем активно: ${dead_keys} 'max usage' errors в последних 10K строк лога"
  fi
fi

# === CHECK 7: recent trades — sanity check что-то происходит ===
if [ -f "$STATE" ]; then
  recent_count=$(python3 -c "
import json
from datetime import datetime, timedelta
with open('$STATE') as f:
    s = json.load(f)
ct = s.get('closed_trades', [])
cutoff = (datetime.utcnow() - timedelta(hours=24)).timestamp() * 1000
recent = [t for t in ct if (t.get('exit_time') or 0) > cutoff]
print(len(recent))
" 2>/dev/null)
  if [ "$recent_count" = "0" ]; then
    alert "За последние 24 часа НЕТ закрытых трейдов — снайпер не торгует"
  fi
fi

# === SUMMARY ===
echo "[$(date)] Health check done: disk=${disk_pct}% mem=${mem_pct}% recent_trades=${recent_count:-?}" >> "$HEALTH_LOG"

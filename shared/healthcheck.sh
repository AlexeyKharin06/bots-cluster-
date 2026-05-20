#!/bin/bash
# healthcheck.sh — диагностика всех критичных компонентов кластера
# Запускается перед AI brain циклом (autonomous_cycle.sh)
# Выход: JSON в /tmp/healthcheck_<project>.json + список проблем для prompt'а AI brain
#
# AI brain читает результат и:
# - Если всё OK → продолжает обычный цикл
# - Если есть проблемы → диагностирует, фиксит, пишет в BRIEF/HISTORY

set -e
PROJECT="${PROJECT:-unknown}"
OUT=/tmp/healthcheck_${PROJECT}.json
SHARED=/srv/bots/.shared

declare -A STATUS
declare -A DETAIL

check() {
  local name="$1"
  local cmd="$2"
  local expected="$3"
  if eval "$cmd" >/dev/null 2>&1; then
    STATUS[$name]="OK"
    DETAIL[$name]=""
  else
    STATUS[$name]="FAIL"
    DETAIL[$name]="$expected"
  fi
}

# 1. SNIPER — running and writing state
SNIPER_STATE=/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json
if [ -f "$SNIPER_STATE" ]; then
  AGE_MIN=$(( ($(date +%s) - $(stat -c %Y "$SNIPER_STATE")) / 60 ))
  if [ "$AGE_MIN" -lt 10 ]; then
    STATUS[sniper_state_fresh]="OK"
    DETAIL[sniper_state_fresh]="updated ${AGE_MIN}min ago"
  else
    STATUS[sniper_state_fresh]="FAIL"
    DETAIL[sniper_state_fresh]="state stale ${AGE_MIN}min — sniper may be dead/hung"
  fi
else
  STATUS[sniper_state_fresh]="FAIL"
  DETAIL[sniper_state_fresh]="state file missing"
fi

# 2. SNIPER process
if pgrep -u bots -f serial_sniper.js >/dev/null 2>&1; then
  STATUS[sniper_proc]="OK"
else
  STATUS[sniper_proc]="FAIL"
  DETAIL[sniper_proc]="serial_sniper.js не запущен — watchdog или вручную"
fi

# 3. WATCHDOG
if pgrep -u bots -f watchdog.sh >/dev/null 2>&1; then
  STATUS[watchdog]="OK"
else
  STATUS[watchdog]="FAIL"
  DETAIL[watchdog]="watchdog.sh не запущен — sniper не будет рестартиться при падении"
fi

# 4. TG UNIFIED LISTENER
TG_STATS=$SHARED/tg/listener_stats.json
if pgrep -u bots -f tg_unified_listener.py >/dev/null 2>&1; then
  STATUS[tg_listener_proc]="OK"
  if [ -f "$TG_STATS" ]; then
    EVENTS=$(python3 -c "import json; print(json.load(open('$TG_STATS')).get('events_received',0))" 2>/dev/null || echo 0)
    UPTIME=$(ps -o etimes= -p $(pgrep -u bots -f tg_unified_listener.py | head -1) 2>/dev/null | tr -d ' ')
    if [ -z "$UPTIME" ]; then UPTIME=0; fi
    # Ожидаем хотя бы 1 event на 5 минут (12 events/час, 288/day для 65 каналов это уже скромная оценка)
    if [ "$UPTIME" -gt 600 ] && [ "$EVENTS" -lt 5 ]; then
      STATUS[tg_signals_flowing]="FAIL"
      DETAIL[tg_signals_flowing]="listener uptime=${UPTIME}s но events_received=${EVENTS} — handler не получает события (баг в registration или session)"
    else
      STATUS[tg_signals_flowing]="OK"
      DETAIL[tg_signals_flowing]="events=${EVENTS} за ${UPTIME}s"
    fi
  fi
else
  STATUS[tg_listener_proc]="FAIL"
  DETAIL[tg_listener_proc]="tg_unified_listener.py не запущен"
  STATUS[tg_signals_flowing]="FAIL"
  DETAIL[tg_signals_flowing]="listener мёртв"
fi

# 5. Disk
DISK_PCT=$(df -h /srv 2>/dev/null | awk 'NR==2 {gsub(/%/, "", $5); print $5}')
if [ -n "$DISK_PCT" ] && [ "$DISK_PCT" -lt 90 ]; then
  STATUS[disk]="OK"
  DETAIL[disk]="${DISK_PCT}% used"
else
  STATUS[disk]="FAIL"
  DETAIL[disk]="disk ${DISK_PCT}% used — критично"
fi

# 6. Memory
MEM_FREE_MB=$(free -m 2>/dev/null | awk 'NR==2 {print $7}')
if [ -n "$MEM_FREE_MB" ] && [ "$MEM_FREE_MB" -gt 500 ]; then
  STATUS[memory]="OK"
  DETAIL[memory]="${MEM_FREE_MB}MB available"
else
  STATUS[memory]="FAIL"
  DETAIL[memory]="only ${MEM_FREE_MB}MB free — OOM risk"
fi

# 7. Helius keys count
HELIUS_COUNT=$(grep -c "^HELIUS_KEY" /srv/bots/onchain/.env 2>/dev/null || echo 0)
if [ "$HELIUS_COUNT" -ge 5 ]; then
  STATUS[helius_keys]="OK"
  DETAIL[helius_keys]="${HELIUS_COUNT} keys configured"
else
  STATUS[helius_keys]="FAIL"
  DETAIL[helius_keys]="only ${HELIUS_COUNT} keys — credits will deplete fast"
fi

# 8. Recent rate-limit hits in sniper.log (last 100 lines)
SNIPER_LOG=/srv/bots/onchain/code/scripts/wallet_v2/sniper.log
if [ -f "$SNIPER_LOG" ]; then
  RL_COUNT=$(tail -200 "$SNIPER_LOG" | grep -ciE "rate.?limit|429|compute.units.exceeded|too many" || echo 0)
  if [ "$RL_COUNT" -gt 5 ]; then
    STATUS[sniper_rate_limits]="FAIL"
    DETAIL[sniper_rate_limits]="${RL_COUNT} rate-limit warnings in last 200 log lines — Helius credits may be running out"
  else
    STATUS[sniper_rate_limits]="OK"
    DETAIL[sniper_rate_limits]="${RL_COUNT} rate-limit warnings (acceptable)"
  fi
fi

# Compose JSON output
{
  echo '{'
  echo "  \"project\": \"$PROJECT\","
  echo "  \"ts\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"checks\": {"
  FIRST=1
  for key in "${!STATUS[@]}"; do
    [ $FIRST -eq 0 ] && echo ','
    FIRST=0
    printf "    \"%s\": {\"status\": \"%s\", \"detail\": \"%s\"}" "$key" "${STATUS[$key]}" "${DETAIL[$key]//\"/\\\"}"
  done
  echo ''
  echo '  },'
  PROBLEMS=()
  for key in "${!STATUS[@]}"; do
    [ "${STATUS[$key]}" = "FAIL" ] && PROBLEMS+=("$key")
  done
  echo "  \"healthy\": $([ ${#PROBLEMS[@]} -eq 0 ] && echo true || echo false),"
  echo "  \"problems\": [$(IFS=,; echo "${PROBLEMS[*]/#/\"}" | sed 's/"$/"/' | sed 's/,/",\"/g' | sed 's/^"//' | sed 's/"$//')]"
  echo '}'
} > "$OUT"

cat "$OUT"

# Markdown report for AI brain prompt
REPORT=/tmp/healthcheck_${PROJECT}.md
{
  echo "# Health Check Report — $(date -u +%Y-%m-%dT%H:%M:%SZ) — project=$PROJECT"
  echo ""
  PROBLEMS_COUNT=${#PROBLEMS[@]}
  if [ "$PROBLEMS_COUNT" -eq 0 ]; then
    echo "✅ **ALL SYSTEMS OK** — продолжай обычный цикл анализа."
  else
    echo "⚠️ **${PROBLEMS_COUNT} ПРОБЛЕМ обнаружено:**"
    echo ""
    for key in "${PROBLEMS[@]}"; do
      echo "- **$key**: ${DETAIL[$key]}"
    done
    echo ""
    echo "**ДЕЙСТВИЯ AI BRAIN:**"
    echo "1. Прочитай этот отчёт"
    echo "2. Для каждой проблемы: диагностируй (какая команда / какой лог покажет причину?)"
    echo "3. Если можешь починить — сделай это (например рестарт демона)"
    echo "4. Если нет — запиши в /srv/bots/cluster/memory/<project>/needs.md что нужно от пользователя"
    echo "5. Append в HISTORY.md: 'CYCLE_ID: healthcheck FAIL X problems → fixed/escalated'"
  fi
  echo ""
  echo "## Все проверки"
  for key in "${!STATUS[@]}"; do
    echo "- $key: ${STATUS[$key]} — ${DETAIL[$key]}"
  done
} > "$REPORT"

cat "$REPORT"

#!/bin/bash
# rate_limit_guard.sh — мониторинг Anthropic API расхода всех 6 проектов.
# Запускается ПЕРЕД claude headless в autonomous_cycle.sh.
#
# Anthropic Max plan: ~1500-2500 messages per 5h rolling window (claude.ai/code).
# 6 проектов × 4 цикла × ~30 messages = 720/day baseline.
# Запас х2-3, но если параллельно работаешь руками — может упереться.

SHARED=/srv/bots/.shared
WINDOW_MIN=300   # 5h Anthropic window
LIMIT_MSG=1200   # safe ceiling (берём 50% от nominal 2500)

# Count messages in last 5h across ALL cycle logs
RECENT_LOGS=$(find "$SHARED/logs" -name 'cycle_*.log' -mmin -$WINDOW_MIN 2>/dev/null)
TOTAL=0
for log in $RECENT_LOGS; do
  # Каждое 'claude -p' в логе — это session, обычно ~20-40 messages
  msgs=$(grep -c '^Human:\|^Assistant:\|tool_use' "$log" 2>/dev/null || echo 0)
  TOTAL=$((TOTAL + msgs))
done

echo "[rate-guard] $TOTAL messages in last ${WINDOW_MIN}min (limit=$LIMIT_MSG)"

if [ "$TOTAL" -gt "$LIMIT_MSG" ]; then
  WAIT=$((WINDOW_MIN * 60 / 6))   # ~50 min
  echo "[rate-guard] over budget — sleeping ${WAIT}s before claude invocation"
  sleep "$WAIT"
  exit 0
fi

# Также — если конкретно ЭТОТ проект уже работал в последние 30мин — skip
PROJECT="${PROJECT:-unknown}"
LAST_SAME=$(find "$SHARED/logs" -name "cycle_*.log" -mmin -30 -mmin +1 -exec grep -l "project=$PROJECT" {} \; 2>/dev/null | head -1)
if [ -n "$LAST_SAME" ]; then
  echo "[rate-guard] $PROJECT already ran in last 30min — skipping this cycle"
  exit 1
fi

echo "[rate-guard] OK to proceed"
exit 0

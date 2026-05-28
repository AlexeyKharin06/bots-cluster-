#!/bin/bash
# auto_heal.sh — supervisor of last resort. Запускается из cron каждые 10 мин.
#
# Auto-restart cascade:
#   1. Если watchdog мёртв → restart watchdog → он рестартит daemons.
#   2. Если sniper_state.json stale >30мин → kill sniper → watchdog respawn (clears in-memory state).
#   3. Если все 13 Helius keys возвращают exhausted >1h → TG alert (это user'у решать).
#   4. Если tg_unified_listener мёртв → restart его.
#   5. Если backfill_pipeline крутится >6h → kill (zombie).
#
# Cron: */10 * * * * bash /srv/bots/cluster/shared/auto_heal.sh >> /srv/bots/.shared/logs/auto_heal.log 2>&1

set +e  # никогда не падать — это supervisor
TS=$(date -u '+%Y-%m-%d %H:%M:%S')
log() { echo "[$TS] $*"; }

SNIPER_STATE=/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json
WATCHDOG_LOG=/srv/bots/onchain/logs/watchdog.log
TG_UNIFIED_LOG=/srv/bots/.shared/tg/tg_unified.log
HEAL_STAMP=/srv/bots/.shared/auto_heal.state

ACTIONS_TAKEN=0
ACTIONS_LOG=()

# === 1. Watchdog alive ===
if ! pgrep -u bots -f "watchdog.sh" >/dev/null 2>&1; then
  log "WATCHDOG DEAD — restarting"
  sudo -u bots bash -c "cd /srv/bots/onchain/code/scripts/wallet_v2 && nohup bash watchdog.sh > /srv/bots/onchain/logs/watchdog.log 2>&1 < /dev/null &"
  ACTIONS_TAKEN=$((ACTIONS_TAKEN+1))
  ACTIONS_LOG+=("watchdog restarted")
  sleep 10
fi

# === 2. Sniper state freshness ===
if [ -f "$SNIPER_STATE" ]; then
  STATE_AGE_MIN=$(( ($(date +%s) - $(stat -c %Y "$SNIPER_STATE")) / 60 ))
  if [ "$STATE_AGE_MIN" -gt 30 ]; then
    # Check if sniper process is alive
    if pgrep -u bots -f "serial_sniper.js" >/dev/null 2>&1; then
      log "SNIPER STUCK (state stale ${STATE_AGE_MIN}min, but process alive) — killing for watchdog respawn"
      pkill -9 -u bots -f "serial_sniper.js"
      ACTIONS_TAKEN=$((ACTIONS_TAKEN+1))
      ACTIONS_LOG+=("sniper killed (state stale ${STATE_AGE_MIN}min)")
      sleep 5  # watchdog will respawn within 30s
    else
      log "SNIPER DEAD (state stale ${STATE_AGE_MIN}min, no process) — waiting for watchdog"
    fi
  fi
fi

# === 3. Helius credits exhaustion detection (last 100 sniper log lines) ===
SNIPER_LOG=/srv/bots/onchain/code/scripts/wallet_v2/sniper.log
if [ -f "$SNIPER_LOG" ]; then
  EXHAUSTED_RECENT=$(tail -200 "$SNIPER_LOG" | grep -c "Alive: 0/13" 2>/dev/null || echo 0)
  if [ "$EXHAUSTED_RECENT" -gt 3 ]; then
    # All keys exhausted — needs user intervention
    LAST_TG_ALERT=$(cat "$HEAL_STAMP.tg_helius" 2>/dev/null || echo 0)
    NOW=$(date +%s)
    # Throttle: only one TG alert per 6h about Helius
    if [ $((NOW - LAST_TG_ALERT)) -gt 21600 ]; then
      log "HELIUS ALL KEYS EXHAUSTED >${EXHAUSTED_RECENT} times in last 200 log lines — alerting user"
      # Send TG alert via shared .env
      [ -f /srv/bots/.shared/.env ] && set -a && . /srv/bots/.shared/.env && set +a
      if [ -n "$TG_TOKEN" ] && [ -n "$TG_CHAT" ]; then
        MSG="⚠️ OnChain: all 13 Helius keys EXHAUSTED. Sniper cannot make API calls. Options: (A) wait for monthly reset, (B) upgrade Helius plan, (C) create new free accounts. Brain continues on frozen state."
        curl -s -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
          --data-urlencode "chat_id=${TG_CHAT}" --data-urlencode "text=${MSG}" >/dev/null 2>&1
        echo "$NOW" > "$HEAL_STAMP.tg_helius"
      fi
      ACTIONS_TAKEN=$((ACTIONS_TAKEN+1))
      ACTIONS_LOG+=("Helius exhaustion TG alert sent")
    fi
  fi
fi

# === 4. Unified TG listener alive ===
if ! pgrep -u bots -f "tg_unified_listener.py" >/dev/null 2>&1; then
  log "TG UNIFIED LISTENER DEAD — restarting"
  sudo -u bots bash -c "cd /srv/bots/.shared/tg && nohup python3 tg_unified_listener.py > tg_unified.log 2>&1 < /dev/null &"
  ACTIONS_TAKEN=$((ACTIONS_TAKEN+1))
  ACTIONS_LOG+=("tg_unified_listener restarted")
fi

# === 5. Stuck backfill (>6h running) ===
BACKFILL_PID=$(pgrep -u bots -f "backfill_pipeline.sh" | head -1)
if [ -n "$BACKFILL_PID" ]; then
  BACKFILL_AGE=$(ps -p "$BACKFILL_PID" -o etimes= | tr -d ' ')
  if [ -n "$BACKFILL_AGE" ] && [ "$BACKFILL_AGE" -gt 21600 ]; then
    log "BACKFILL_PIPELINE STUCK (${BACKFILL_AGE}s) — killing"
    pkill -9 -u bots -f "backfill_pipeline.sh"
    pkill -9 -u bots -f "backfill_wallet_roles\|backfill_lp_provider\|backfill_candidates"
    ACTIONS_TAKEN=$((ACTIONS_TAKEN+1))
    ACTIONS_LOG+=("backfill_pipeline killed (stuck ${BACKFILL_AGE}s)")
  fi
fi

# === 6. Final report ===
if [ "$ACTIONS_TAKEN" -gt 0 ]; then
  log "SUMMARY: ${ACTIONS_TAKEN} actions: ${ACTIONS_LOG[*]}"
else
  log "all OK (no actions)"
fi

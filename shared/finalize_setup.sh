#!/bin/bash
# finalize_setup.sh — добивает остаточные элементы установки:
#   - @reboot cron (resilient к перезагрузке)
#   - telethon pip install
#   - tg/ симлинк если нет
#   - запускает tg_listener вручную если он не работает
#
# Использование: bash <(curl -fsSL https://raw.githubusercontent.com/AlexeyKharin06/bots-cluster-/main/shared/finalize_setup.sh)

set -e
log() { echo "[finalize] $*"; }

# 1. tg/ симлинк (если ещё нет)
if [ ! -e /srv/bots/onchain/code/tg ]; then
  log "creating tg/ symlink..."
  ln -s /srv/bots/onchain/tg /srv/bots/onchain/code/tg
fi

# 2. Telethon — нужен для tg_listener
log "checking telethon..."
if ! python3 -c "import telethon" 2>/dev/null; then
  log "installing telethon..."
  pip3 install telethon easyocr opencv-python-headless --break-system-packages 2>&1 | tail -3
fi

# 3. @reboot cron — через временный файл с heredoc (без paste-ломки)
log "adding @reboot crontab..."
TMPCRON=$(mktemp)
crontab -l 2>/dev/null | grep -v '@reboot.*watchdog' > "$TMPCRON" || true
cat >> "$TMPCRON" <<'EOF'
@reboot cd /srv/bots/onchain/code/scripts/wallet_v2 && nohup bash watchdog.sh > /srv/bots/onchain/logs/watchdog.log 2>&1 &
EOF
crontab "$TMPCRON"
rm "$TMPCRON"
log "cron updated:"
crontab -l | sed 's/^/  /'

# 4. tg_listener — запустить вручную если не работает
if ! pgrep -f "tg_listener.py" > /dev/null; then
  log "starting tg_listener manually..."
  cd /srv/bots/onchain/tg
  nohup python3 tg_listener.py > /srv/bots/onchain/logs/tg_listener.log 2>&1 &
  sleep 5
  if pgrep -f "tg_listener.py" > /dev/null; then
    log "tg_listener started OK"
  else
    log "tg_listener failed — check /srv/bots/onchain/logs/tg_listener.log"
    tail -20 /srv/bots/onchain/logs/tg_listener.log 2>/dev/null || true
  fi
fi

# 5. Final status
log "=== final status ==="
log "Processes:"
ps -ef | grep -E "node.*(serial|lp_monitor|lp_bot|pumpfun|dexscreener)|python.*tg_listener|watchdog\.sh" | grep -v grep | awk '{print "  " $8 " " $9 " " $10}'
log "Cron:"
crontab -l | sed 's/^/  /'
log ""
log "Setup complete. Sniper + AI brain работают автономно."
log "Закрывай SSH — всё продолжится само."

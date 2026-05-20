#!/bin/bash
# setup_tg_unified.sh — настраивает unified TG listener (один на все проекты)
# Использование (на VPS под root):
#   bash /srv/bots/cluster/shared/setup_tg_unified.sh
#
# Что делает:
#   1. Создаёт /srv/bots/.shared/tg/ как unified hub
#   2. Копирует tg_session + creds из cex-onchain (свежайшая auth)
#   3. Останавливает любые running per-project tg_listeners
#   4. Включает .tg_listener_disabled во всех проектах
#   5. Устанавливает systemd unit для unified listener
#   6. Стартует unified listener

set -e
log() { echo "[setup-tg] $*"; }

SHARED=/srv/bots/.shared/tg
mkdir -p "$SHARED"
chown bots:bots "$SHARED"

# 1. Best session — самая свежая
log "selecting freshest TG session..."
BEST_SESSION=""
BEST_MTIME=0
for SESS in /srv/bots/cex-onchain/code/scripts/tg_session.session \
            /srv/bots/listing-arb/code/scripts/tg_session.session \
            /srv/bots/onchain/tg/tg_session.session \
            /srv/bots/funding_rate/tg_session.session; do
  if [ -f "$SESS" ]; then
    MT=$(stat -c %Y "$SESS")
    if [ "$MT" -gt "$BEST_MTIME" ]; then
      BEST_MTIME=$MT
      BEST_SESSION=$SESS
    fi
  fi
done

if [ -z "$BEST_SESSION" ]; then
  log "ERROR: no TG session found anywhere. User needs to run tg_auth.py first."
  exit 1
fi

log "using: $BEST_SESSION ($(date -d @$BEST_MTIME))"

# 2. Find matching .tg_credentials
CREDS_DIR=$(dirname "$BEST_SESSION")
CREDS="$CREDS_DIR/.tg_credentials"
[ -f "$CREDS" ] || CREDS="$(dirname $CREDS_DIR)/.tg_credentials"
if [ ! -f "$CREDS" ]; then
  log "ERROR: no .tg_credentials found near $BEST_SESSION"
  exit 1
fi

# 3. Copy to shared
log "copying session + creds to $SHARED..."
cp "$BEST_SESSION" "$SHARED/tg_session.session"
cp "$CREDS" "$SHARED/.tg_credentials"
chmod 600 "$SHARED/.tg_credentials"
chown -R bots:bots "$SHARED"

# 4. Stop any running per-project listeners
log "stopping per-project tg_listeners (if any)..."
pkill -9 -u bots -f tg_listener.py 2>/dev/null || true
sleep 2

# 5. Mark each project's tg_listener as disabled
log "disabling per-project tg_listener (через .tg_listener_disabled flag)..."
for PROJ in onchain listing-arb cex-onchain funding-rate funding_rate; do
  PROJ_BASE="/srv/bots/$PROJ"
  [ -d "$PROJ_BASE" ] || continue
  # try common locations of flag file
  for FLAG_DIR in \
      "$PROJ_BASE/code/scripts/wallet_v2" \
      "$PROJ_BASE/code/scripts" \
      "$PROJ_BASE/code" \
      "$PROJ_BASE"; do
    [ -d "$FLAG_DIR" ] || continue
    touch "$FLAG_DIR/.tg_listener_disabled"
    chown bots:bots "$FLAG_DIR/.tg_listener_disabled" 2>/dev/null || true
  done
done

# 6. Download unified listener script if not present
if [ ! -f /srv/bots/cluster/shared/tg_unified_listener.py ]; then
  log "unified listener not found in cluster repo. Pulling..."
  sudo -u bots git -C /srv/bots/cluster pull --quiet 2>&1 | tail -3
fi
cp /srv/bots/cluster/shared/tg_unified_listener.py "$SHARED/tg_unified_listener.py"
chmod +x "$SHARED/tg_unified_listener.py"
chown bots:bots "$SHARED/tg_unified_listener.py"

# 7. systemd unit
log "creating systemd unit tg-unified.service..."
cat > /etc/systemd/system/tg-unified.service <<EOF
[Unit]
Description=Unified TG listener for all bot-cluster projects
After=network.target

[Service]
Type=simple
User=bots
WorkingDirectory=/srv/bots/.shared/tg
ExecStart=/usr/bin/python3 /srv/bots/.shared/tg/tg_unified_listener.py
Restart=on-failure
RestartSec=30
StandardOutput=append:/srv/bots/.shared/tg/tg_unified.log
StandardError=append:/srv/bots/.shared/tg/tg_unified.log

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now tg-unified.service 2>&1 | tail -3

sleep 5
log ""
log "=== STATUS ==="
systemctl status tg-unified.service 2>&1 | head -10
log ""
log "Recent log:"
tail -15 /srv/bots/.shared/tg/tg_unified.log 2>/dev/null

log ""
log "=== DONE ==="
log "Unified listener writes to:"
log "  $SHARED/signals_master.jsonl (all signals)"
log "  $SHARED/feed_onchain.jsonl (memecoin/SOL/BSC addresses)"
log "  $SHARED/feed_listing.jsonl (CEX listings)"
log "  $SHARED/feed_cex.jsonl (arbitrage)"
log "  $SHARED/feed_funding.jsonl (funding rates)"

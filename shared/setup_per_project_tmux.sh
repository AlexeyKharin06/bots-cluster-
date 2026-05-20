#!/bin/bash
# setup_per_project_tmux.sh — создаёт отдельные tmux sessions per project
# Использование (на VPS под root):
#   bash /srv/bots/cluster/shared/setup_per_project_tmux.sh
#
# После этого пользователь подключается:
#   sudo -u bots tmux a -t onchain-brain
#   sudo -u bots tmux a -t listing-brain
#   sudo -u bots tmux a -t cex-brain
#   sudo -u bots tmux a -t funding-brain
# (или общая 'brain' если нужна shared)
#
# Detach: Ctrl+B, потом D.

set -e
log() { echo "[setup-tmux] $*"; }

declare -A PROJECTS=(
  [onchain-brain]=/srv/bots/onchain
  [listing-brain]=/srv/bots/listing-arb
  [cex-brain]=/srv/bots/cex-onchain
  [funding-brain]=/srv/bots/funding-rate
)

for SESSION in "${!PROJECTS[@]}"; do
  PROJDIR="${PROJECTS[$SESSION]}"
  UNIT="/etc/systemd/system/tmux-${SESSION}.service"

  log "creating systemd unit for $SESSION (cwd: $PROJDIR)"
  cat > "$UNIT" <<EOF
[Unit]
Description=Persistent tmux for ${SESSION} (Claude session)
After=network.target

[Service]
Type=forking
User=bots
ExecStart=/usr/bin/tmux new-session -d -s ${SESSION} -c ${PROJDIR} 'echo "${SESSION} tmux ready. Attach: tmux a -t ${SESSION}"; cd ${PROJDIR}; export PATH=~/.npm-global/bin:\$PATH; exec bash'
ExecStop=/usr/bin/tmux kill-session -t ${SESSION}
RemainAfterExit=yes
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable --now tmux-${SESSION}.service 2>&1 | tail -3
  log "${SESSION} started"
done

log ""
log "=== Available tmux sessions ==="
sudo -u bots tmux ls
log ""
log "Attach commands (для пользователя):"
for SESSION in "${!PROJECTS[@]}"; do
  log "  sudo -u bots tmux a -t ${SESSION}"
done

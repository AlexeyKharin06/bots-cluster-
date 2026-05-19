#!/bin/bash
# setup_vps.sh — единственная команда которую запускает пользователь на VPS
# Развёртывает всю инфраструктуру для bots-cluster
#
# Запуск: bash setup_vps.sh

set -e
log() { echo "[$(date '+%H:%M:%S')] $*"; }
log "=== Bots-cluster VPS deploy started ==="

# === 1. Установка базовых пакетов ===
if ! command -v docker &>/dev/null; then
  log "Installing system packages (Python, Node, Docker, ffmpeg)..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get -qq install -y curl wget git build-essential ca-certificates \
    software-properties-common gnupg lsb-release htop tmux nano ufw fail2ban \
    rsync cron jq sqlite3 libsqlite3-dev ffmpeg python3 python3-pip python3-venv
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get -qq install -y nodejs
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
  log "Base packages installed"
else
  log "Base packages already installed — skip"
fi

# === 2. User 'bots' ===
if ! id bots &>/dev/null; then
  log "Creating user 'bots'..."
  useradd -m -s /bin/bash -G docker,sudo bots
  echo 'bots ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/bots
fi

# === 3. Структура /srv/bots/ ===
mkdir -p /srv/bots/{onchain,trade,listing-arb,cex-onchain,pl,funding-rate}
mkdir -p /srv/bots/.shared/{logs,memory,backups}
# .env template (заполнить вручную после первого запуска)
if [ ! -f /srv/bots/.shared/.env ]; then
  cat > /srv/bots/.shared/.env <<'ENVEOF'
# Telegram bot для alert'ов AI brain cycle
# Создать бота: https://t.me/BotFather → /newbot → токен
TG_TOKEN=
TG_CHAT=
ENVEOF
  chmod 600 /srv/bots/.shared/.env
fi
chown -R bots:bots /srv/bots
log "Project dirs ready (заполни /srv/bots/.shared/.env: TG_TOKEN + TG_CHAT)"

# === 4. Firewall ===
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw --force enable
systemctl enable --now fail2ban
log "Firewall + fail2ban enabled"

# === 5. Claude Code CLI (для AI brain) ===
sudo -u bots bash <<'EOF'
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
if ! command -v ~/.npm-global/bin/claude &>/dev/null; then
  npm install -g @anthropic-ai/claude-code 2>&1 | tail -3
fi
grep -q "npm-global" ~/.bashrc || echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
EOF
log "Claude Code CLI installed for user 'bots'"

# === 6. Clone repo as bots user ===
sudo -u bots bash <<'EOF'
cd /srv/bots
if [ ! -d cluster ]; then
  git clone https://github.com/AlexeyKharin06/bots-cluster-.git cluster
fi
cd cluster && git pull
EOF
log "Repo cloned to /srv/bots/cluster"

# === 7. Setup OnChain project ===
sudo -u bots bash <<'EOF'
mkdir -p /srv/bots/onchain/{code,memory,logs,data}
EOF

# === 8. Systemd: persistent tmux session "brain" ===
cat > /etc/systemd/system/bots-brain.service <<'EOF'
[Unit]
Description=Persistent tmux for AI brain (attachable by user)
After=network.target

[Service]
Type=forking
User=bots
ExecStart=/usr/bin/tmux new-session -d -s brain -c /srv/bots/cluster 'echo "Brain tmux ready. Attach: tmux a -t brain"; exec bash'
ExecStop=/usr/bin/tmux kill-session -t brain
RemainAfterExit=yes
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now bots-brain.service || true
log "Persistent tmux 'brain' systemd unit registered"

# === 9. Cron for autonomous_cycle ===
sudo -u bots bash <<'EOF'
cd /srv/bots/cluster
crontab -l 2>/dev/null | grep -v "autonomous_cycle" > /tmp/cron.tmp || true
echo "0 */6 * * * cd /srv/bots/cluster && bash shared/autonomous_cycle.sh >> /srv/bots/.shared/logs/cron.log 2>&1" >> /tmp/cron.tmp
crontab /tmp/cron.tmp
rm /tmp/cron.tmp
EOF
log "Cron: autonomous_cycle every 6h"

# === 10. Final status ===
log "=== Setup complete ==="
log "User: bots (sudo+docker)"
log "Repo: /srv/bots/cluster"
log "Projects: /srv/bots/<project>"
log "Persistent tmux: 'brain' (attach: sudo -u bots tmux a -t brain)"
log "Cron: autonomous_cycle every 6h"
log ""
log "Next: switch to 'bots' user and continue OnChain setup:"
log "  su - bots"
log "  cd /srv/bots/cluster"
log "  bash projects/onchain/setup.sh"

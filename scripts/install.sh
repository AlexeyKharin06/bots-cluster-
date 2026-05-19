#!/bin/bash
# install.sh — первоначальная настройка свежего Hostinger Ubuntu 24.04 VPS
# Запуск: sudo bash install.sh
# Идемпотентен — можно запускать повторно без проблем

set -e
exec > >(tee -a /var/log/install.log) 2>&1

echo "=== Bots Cluster VPS — initial setup $(date) ==="

# --- 1. System updates ---
echo "[1/9] System updates..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get -qq upgrade -y
apt-get -qq install -y curl wget git build-essential ca-certificates \
  software-properties-common gnupg lsb-release htop tmux nano vim \
  ufw fail2ban unattended-upgrades net-tools dnsutils unzip \
  rsync cron jq sqlite3 libsqlite3-dev

# --- 2. Timezone + locale ---
echo "[2/9] Timezone + locale..."
timedatectl set-timezone Europe/Moscow || true
locale-gen en_US.UTF-8 ru_RU.UTF-8 || true

# --- 3. Python 3.12 ---
echo "[3/9] Python 3.12..."
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update -qq
apt-get -qq install -y python3.12 python3.12-venv python3.12-dev python3-pip
update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 || true

# --- 4. Node.js 20 (LTS) ---
echo "[4/9] Node.js 20..."
if ! command -v node &>/dev/null || [[ $(node -v) != v20* ]]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get -qq install -y nodejs
fi
echo "node: $(node -v), npm: $(npm -v)"

# --- 5. Docker + Compose ---
echo "[5/9] Docker..."
if ! command -v docker &>/dev/null; then
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
fi
docker --version

# --- 6. ffmpeg (для tg media obrabotka) ---
echo "[6/9] ffmpeg..."
apt-get -qq install -y ffmpeg

# --- 7. Создание пользователя 'bots' (вместо root для приложений) ---
echo "[7/9] User 'bots'..."
if ! id bots &>/dev/null; then
  useradd -m -s /bin/bash -G docker,sudo bots
  echo 'bots ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers.d/bots
fi
mkdir -p /home/bots/.ssh
chown -R bots:bots /home/bots/.ssh

# --- 8. Папки для проектов ---
echo "[8/9] Project dirs..."
mkdir -p /srv/bots/{onchain,trade,listing-arb,cex-onchain,pl,funding-rate,polyc}
mkdir -p /srv/bots/.shared/{backups,logs,memory}
chown -R bots:bots /srv/bots

# --- 9. Firewall + fail2ban ---
echo "[9/9] Firewall + security..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp  # SSH
ufw --force enable
systemctl enable --now fail2ban

# Claude Code CLI (для headless AI brain)
echo "[+] Claude Code CLI..."
sudo -u bots bash -c 'npm config set prefix ~/.npm-global && npm install -g @anthropic-ai/claude-code 2>&1 | tail -5'
sudo -u bots bash -c 'echo "export PATH=~/.npm-global/bin:\$PATH" >> ~/.bashrc'

echo
echo "=== Install complete. Switch to 'bots' user: ==="
echo "  su - bots"
echo
echo "Next: configure SSH key, clone repo, deploy projects."
echo "=== Done $(date) ==="

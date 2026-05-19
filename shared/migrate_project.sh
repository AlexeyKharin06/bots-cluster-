#!/bin/bash
# migrate_project.sh — универсальная миграция проекта на VPS
# Использование (на VPS под root):
#   PROJECT=listing-arb bash <(curl -fsSL https://raw.githubusercontent.com/AlexeyKharin06/bots-cluster-/main/shared/migrate_project.sh)
#
# Предусловие: ты уже сделал `scp D:\<project>.tar.gz root@VPS:/tmp/` с ПК
#
# Что делает:
#   1. Распаковывает /tmp/${PROJECT}.tar.gz в /srv/bots/${PROJECT}/code/
#   2. Симлинки .env и state файлов
#   3. npm install (если есть package.json)
#   4. pip install (если есть requirements.txt)
#   5. Создаёт /home/bots/run_cycle_${PROJECT}.sh
#   6. Добавляет cron entry на свой offset
#   7. Запускает первый AI brain цикл

set -e
log() { echo "[migrate:$PROJECT] $*"; }

PROJECT="${PROJECT:?Set PROJECT env var, e.g. PROJECT=listing-arb}"
TARBALL=/tmp/${PROJECT}.tar.gz
TARGET=/srv/bots/${PROJECT}

# Cron offsets — антикорреляция
declare -A OFFSETS=(
  [onchain]="0 0,6,12,18 * * *"
  [trade]="0 1,7,13,19 * * *"
  [listing-arb]="0 2,8,14,20 * * *"
  [cex-onchain]="0 3,9,15,21 * * *"
  [pl]="0 4,10,16,22 * * *"
  [funding-rate]="0 5,11,17,23 * * *"
)

CRON_TIME="${OFFSETS[$PROJECT]:-}"
[ -z "$CRON_TIME" ] && { log "Unknown project $PROJECT — add to OFFSETS"; exit 1; }

log "starting migration"
log "target: $TARGET"
log "tarball: $TARBALL"
log "cron: $CRON_TIME"

# === 1. Распаковка ===
if [ ! -f "$TARBALL" ]; then
  log "ERROR: $TARBALL not found"
  log "Run on PC first:"
  log "  cd D:\\<ProjectFolder>"
  log "  tar -czf D:\\${PROJECT}.tar.gz --exclude=node_modules --exclude=*.log scripts tg .env package.json 2>/dev/null"
  log "  scp D:\\${PROJECT}.tar.gz root@VPS:/tmp/"
  exit 1
fi

mkdir -p "$TARGET"/{code,data,logs}
cd "$TARGET"
tar -xzf "$TARBALL"
log "extracted to $TARGET"

# Move scripts/ to code/ if exists at top level
[ -d "$TARGET/scripts" ] && mv "$TARGET/scripts" "$TARGET/code/"
[ -d "$TARGET/tg" ] && ln -sfn "$TARGET/tg" "$TARGET/code/tg"

# .env to root project dir
[ -f "$TARGET/.env" ] && log ".env present"

chown -R bots:bots "$TARGET"

# === 2. npm install (если есть package.json в любом scripts/) ===
PKGJSON=$(find "$TARGET" -name package.json -not -path '*/node_modules/*' | head -1)
if [ -n "$PKGJSON" ]; then
  PKGDIR=$(dirname "$PKGJSON")
  log "npm install in $PKGDIR..."
  sudo -u bots bash -c "cd '$PKGDIR' && npm install 2>&1 | tail -5"
fi

# === 3. pip install (если есть requirements.txt) ===
REQTXT=$(find "$TARGET" -name requirements.txt -not -path '*/.venv/*' | head -1)
if [ -n "$REQTXT" ]; then
  log "pip install -r $REQTXT..."
  sudo -u bots bash -c "pip3 install -r '$REQTXT' --break-system-packages 2>&1 | tail -5"
fi

# === 4. State symlink (если есть state.json в коде) ===
STATEFILE=$(find "$TARGET/code" -name "*state*.json" -not -path '*/node_modules/*' | head -1)
if [ -n "$STATEFILE" ]; then
  ln -sfn "$STATEFILE" "$TARGET/data/$(basename $STATEFILE)"
  log "state symlink: $TARGET/data/$(basename $STATEFILE)"
fi

# === 5. Wrapper script для bots ===
cat > /home/bots/run_cycle_${PROJECT}.sh <<EOF
#!/bin/bash
export CLAUDE_EXTRA_FLAGS="--dangerously-skip-permissions"
export PROJECT=$PROJECT
bash /srv/bots/cluster/shared/autonomous_cycle.sh
EOF
chmod +x /home/bots/run_cycle_${PROJECT}.sh
chown bots:bots /home/bots/run_cycle_${PROJECT}.sh
log "wrapper: /home/bots/run_cycle_${PROJECT}.sh"

# === 6. Cron entry ===
TMPCRON=$(mktemp)
sudo -u bots crontab -l 2>/dev/null | grep -v "run_cycle_${PROJECT}" > "$TMPCRON" || true
echo "$CRON_TIME /home/bots/run_cycle_${PROJECT}.sh >> /srv/bots/.shared/logs/cron_${PROJECT}.log 2>&1" >> "$TMPCRON"
sudo -u bots crontab "$TMPCRON"
rm "$TMPCRON"
log "cron added (offset $CRON_TIME)"

# === 7. PROJECT_CONTEXT.md заготовка ===
mkdir -p /srv/bots/cluster/memory/${PROJECT}/insights
if [ ! -f /srv/bots/cluster/memory/${PROJECT}/PROJECT_CONTEXT.md ]; then
  cat > /srv/bots/cluster/memory/${PROJECT}/PROJECT_CONTEXT.md <<EOF
# PROJECT CONTEXT — ${PROJECT}

> Шаблон. AI brain должен дополнить после прочтения кода проекта.

## Цель
TBD — определи цель из кода/CLAUDE.md проекта.

## Архитектура
- Код: /srv/bots/${PROJECT}/code/
- Live data: /srv/bots/${PROJECT}/data/
- Logs: /srv/bots/${PROJECT}/logs/
- .env: /srv/bots/${PROJECT}/.env

## Cron offset
$CRON_TIME (для anti-rate-limit с другими проектами)

## Запреты (общие для всех проектов)
- Не запускать реальные сделки без явного разрешения
- Paper-only (size minimal)
- Не трогать sniper code в /srv/bots/onchain/
- Не git push --force
- Не удалять файлы в memory/
EOF
  log "PROJECT_CONTEXT.md template created"
fi

# === 8. Final ===
log "=== migration done ==="
log "Next: запусти первый цикл руками:"
log "  sudo -u bots /home/bots/run_cycle_${PROJECT}.sh"
log "Cron уже добавлен — следующий automatic запуск по schedule '$CRON_TIME'"

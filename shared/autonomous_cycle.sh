#!/bin/bash
# autonomous_cycle.sh — главный цикл AI brain (cron каждые 6h).
#
# === МОДЕЛЬ ХРАНЕНИЯ КОНТЕКСТА ===
# Контекст НЕ теряется никогда. Структура такая:
#
#   memory/HISTORY.md
#       Append-only хронологический index. Одна строка на цикл:
#       "20260519_1800 | tested hypothesis X | result Y | files: a.md, b.md"
#       Это короткий timeline, по которому AI быстро ориентируется
#       "что вообще делалось".
#
#   memory/insights/cycle_YYYYMMDD_HHMM.md
#       ПОЛНЫЙ unconstrained лог каждого цикла. Без word limit.
#       AI пишет туда всё что думал, что нашёл, числа backtest'а,
#       какие гипотезы рассматривал и отбросил, почему.
#       Append-only — никогда не редактируется и не удаляется.
#
#   memory/BRIEF.md
#       Навигационный snapshot текущего состояния (≤4KB).
#       НЕ замена истории — указатель: "сейчас тестируется X
#       (см. cycle_20260519_1800.md), очередь Y/Z, последний
#       результат — см. cycle_20260520_0000.md, открытые вопросы…"
#       Перезаписывается каждый цикл.
#
#   memory/backlog.md
#       Все гипотезы. Append-only. Статусы (testing/accepted/rejected)
#       меняются in-place в той же строке.
#
#   memory/promotion.json
#       Машинный state: paper-streams и их live stats.
#
# При входе в цикл AI читает:
#   1. BRIEF.md — "где мы сейчас"
#   2. HISTORY.md последние 100 строк — таймлайн
#   3. ПОСЛЕДНИЕ 3 cycle_*.md полностью — детальный недавний контекст
#   4. Старые cycle_*.md по необходимости — если HISTORY указывает на них

set -e
CYCLE_ID=$(date -u '+%Y%m%d_%H%M')
REPO=/srv/bots/cluster
SHARED=/srv/bots/.shared
LOG=$SHARED/logs/cycle_$CYCLE_ID.log
MEMORY=$REPO/memory
PROJECT="${PROJECT:-onchain}"
PROJ_MEMORY=$MEMORY/$PROJECT
PROJ_INSIGHTS=$PROJ_MEMORY/insights

mkdir -p "$SHARED/logs" "$SHARED/memory" "$PROJ_INSIGHTS"
exec > >(tee -a "$LOG") 2>&1

echo "=== CYCLE $CYCLE_ID [project=$PROJECT] ==="
echo "Time: $(date -u) UTC"

# === 0. Rate-limit guard ====================================================
if [ -x "$REPO/shared/rate_limit_guard.sh" ]; then
  PROJECT="$PROJECT" bash "$REPO/shared/rate_limit_guard.sh" || {
    echo "[guard] skipping cycle (rate-limit or duplicate)"
    exit 0
  }
fi

# === 0.5. HEALTHCHECK — диагностика инфраструктуры перед циклом ============
echo "[0.5] healthcheck..."
if [ -x "$REPO/shared/healthcheck.sh" ]; then
  PROJECT="$PROJECT" bash "$REPO/shared/healthcheck.sh" 2>&1 | tail -30
  HEALTHCHECK_REPORT=/tmp/healthcheck_${PROJECT}.md
else
  HEALTHCHECK_REPORT=""
fi

# === 1. Pull repo ===========================================================
echo "[1] git pull..."
cd "$REPO"
git pull --rebase --autostash 2>&1 | tail -3 || echo "  pull failed (ok)"

# === 2. Status ==============================================================
echo "[2] docker status..."
docker ps --format "  {{.Names}}\t{{.Status}}" || true

# === 3. State snapshot ======================================================
echo "[3] state snapshot..."
STATE_SNAPSHOT=/tmp/state_snapshot_$CYCLE_ID.txt
> "$STATE_SNAPSHOT"
for proj in onchain trade listing-arb cex-onchain pl funding-rate; do
  s=/srv/bots/$proj/data/sniper_state.json
  [ -f "$s" ] || continue
  python3 - "$s" "$proj" >> "$STATE_SNAPSHOT" <<'PYEOF'
import json, sys
path, proj = sys.argv[1], sys.argv[2]
try:
    with open(path, 'r', encoding='utf-8') as f:
        s = json.load(f)
    op = s.get('open_positions', s.get('positions', []))
    ct = s.get('closed_trades', [])
    if ct:
        recent = ct[-100:]
        avg = sum(t.get('pnl_pct', 0) for t in recent) / len(recent)
        wins = sum(1 for t in recent if t.get('pnl_pct', 0) > 0)
        rugs = sum(1 for t in recent if t.get('pnl_pct', 0) < -50)
        print(f"{proj}: open={len(op)} closed={len(ct)} last100 avgPnL={avg:+.1f}% WR={100*wins//len(recent)}% rug={100*rugs//len(recent)}%")
    else:
        print(f"{proj}: open={len(op)} closed=0")
except Exception as e:
    print(f"{proj}: state-err {e}")
PYEOF
done
cat "$STATE_SNAPSHOT"

# === 4. Build navigational context (КОМПАКТНО, но указывает на ПОЛНЫЕ файлы) ===
CTX=/tmp/brain_context_$CYCLE_ID.md
{
  echo "# Cycle $CYCLE_ID context (project=$PROJECT)"
  echo
  echo "## 🔴 HEALTHCHECK (если есть проблемы — сначала чинишь, потом анализ)"
  [ -f "$HEALTHCHECK_REPORT" ] && cat "$HEALTHCHECK_REPORT" || echo "(healthcheck не запустился — проверь shared/healthcheck.sh)"
  echo
  echo "## 🟡 CRITICAL FINDINGS (общие уроки от всех сессий — читай каждый цикл!)"
  if [ -f "$MEMORY/CRITICAL_FINDINGS.md" ]; then
    head -100 "$MEMORY/CRITICAL_FINDINGS.md"
    echo "... (полный файл в memory/CRITICAL_FINDINGS.md)"
  else
    echo "(нет файла)"
  fi
  echo
  # Project-specific deep-dive mandates (если есть в memory/<project>/)
  for MANDATE in "$PROJ_MEMORY"/*_MANDATE.md; do
    [ -f "$MANDATE" ] || continue
    echo "## 🔴 PROJECT-SPECIFIC MANDATE: $(basename $MANDATE)"
    cat "$MANDATE"
    echo
  done
  echo "## AI BRAIN MISSION (общие полномочия и цели)"
  [ -f "$MEMORY/AI_BRAIN_MISSION.md" ] && head -50 "$MEMORY/AI_BRAIN_MISSION.md" || echo "(нет)"
  echo
  echo "## CURRENT STATE (live data, this cycle)"
  cat "$STATE_SNAPSHOT"
  echo
  echo "## BRIEF (navigation snapshot from previous cycle)"
  [ -f "$PROJ_MEMORY/BRIEF.md" ] && cat "$PROJ_MEMORY/BRIEF.md" || echo "(empty — first cycle)"
  echo
  echo "## HISTORY (chronological timeline — last 100 lines)"
  [ -f "$PROJ_MEMORY/HISTORY.md" ] && tail -100 "$PROJ_MEMORY/HISTORY.md" || echo "(empty)"
  echo
  echo "## RECENT CYCLES (last 3 full insights — UNTRUNCATED)"
  ls -t "$PROJ_INSIGHTS/" 2>/dev/null | head -3 | while read f; do
    echo
    echo "### $f"
    cat "$PROJ_INSIGHTS/$f"
  done
  echo
  echo "## BACKLOG (open hypotheses)"
  [ -f "$PROJ_MEMORY/backlog.md" ] && cat "$PROJ_MEMORY/backlog.md" || echo "(none)"
  echo
  echo "## UNIFIED TG SIGNALS (per-project feed)"
  TG_FEED=/srv/bots/.shared/tg/feed_${PROJECT}.jsonl
  if [ -f "$TG_FEED" ]; then
    echo "Last 20 signals от unified TG listener:"
    tail -20 "$TG_FEED"
  else
    echo "(нет $TG_FEED — listener может не работать или нет сигналов для этого проекта)"
  fi
} > "$CTX"
CTX_SIZE=$(wc -c < "$CTX")
echo "[4] context: ${CTX_SIZE}B (full last 3 cycles + history index + brief + backlog)"

# === 5. AI brain ============================================================
echo "[5] claude headless..."
BRAIN_PROMPT=$(cat <<'PROMPT'
Ты автономный AI-стратег. Цель проекта: +100,000% при минимальных рисках через выявление on-chain wallet-паттернов перед памп/раг.

## КОНТЕКСТ
Полный контекст подготовлен в /tmp/brain_context_CYCLE_ID_HERE.md — там:
- текущий state (live closed_trades)
- BRIEF.md (где мы сейчас)
- HISTORY.md последние 100 строк (timeline всех предыдущих циклов)
- 3 ПОСЛЕДНИХ полных cycle_*.md (untruncated — детальный недавний контекст)
- backlog.md (открытые гипотезы)

Прочитай этот файл первым. Если нужны старые циклы — HISTORY.md показывает какие.
Если нужны конкретные closed_trades — /srv/bots/PROJECT_HERE/data/sniper_state.json.

## ЗАДАЧИ ЦИКЛА (выбери ОДНУ — чтобы успеть в 80 turns)
A. Анализ свежих closed_trades vs предыдущего цикла — что изменилось (READ + WRITE insights)
B. Новые гипотезы (1-3) на основе wallet-патернов, append в backlog.md
C. Walk-forward backtest одной гипотезы из backlog.md на real closed_trades
D. Если прошла (n≥50, avgPnL≥+150%, WR≥60%, rug≤25%) — добавить paper-stream

Если данных нет (state.json пуст) — focus на B (формирование гипотез из общих принципов).

## ОБЯЗАТЕЛЬНЫЕ ВЫХОДЫ (каждый цикл)

1. /srv/bots/cluster/memory/PROJECT_HERE/insights/cycle_CYCLE_ID_HERE.md
   ПОЛНЫЙ лог цикла. БЕЗ word limit. Пиши всё:
   - что думал, что искал
   - все числа backtest'а
   - гипотезы которые отбросил И почему (это важно!)
   - что коммитнул и зачем
   Этот файл — твоя память для будущих циклов. Чем подробнее — тем лучше.

2. /srv/bots/cluster/memory/PROJECT_HERE/HISTORY.md
   Append (НЕ перезаписывать!) одну строку:
   "CYCLE_ID_HERE | <1-line summary> | files: <touched files>"

3. /srv/bots/cluster/memory/PROJECT_HERE/BRIEF.md
   Перезаписать. ≤4KB. Навигационный snapshot:
   - что сейчас тестируется (paper streams + stage)
   - последняя проверенная гипотеза + результат (1 строка + ссылка на cycle_*.md)
   - что планируется в следующем цикле
   - ТЕКУЩИЕ ОТКРЫТЫЕ ВОПРОСЫ к пользователю (если есть)

4. /srv/bots/cluster/memory/PROJECT_HERE/backlog.md
   Append новые гипотезы / update статусы существующих.

## ЗАПРЕТЫ
- НЕ трогать контрольные стримы (SNIPER_A/B/D/H/GOLD3/GOLD4/GOLD5/WHALE/LATE/LOWCAP оригиналы)
- НЕ удалять файлы, НЕ git push --force
- НЕ запускать реальные сделки (всё paper, size=$1)
- syntax-check: `node --check projects/PROJECT_HERE/serial_sniper.js` перед commit
- НЕ читать большие файлы целиком (>5MB) — head/tail/grep
- НЕ показывать конкретные адреса токенов в commit messages (alpha)
- НЕ обрезать insights/cycle_*.md — это память; токены экономь за счёт того что
  СТАРЫЕ циклы ты не перечитываешь без причины (HISTORY показывает что было).

## ВРЕМЯ
Максимум 45 минут. После — commit + завершение.
PROMPT
)
BRAIN_PROMPT="${BRAIN_PROMPT//CYCLE_ID_HERE/$CYCLE_ID}"
BRAIN_PROMPT="${BRAIN_PROMPT//PROJECT_HERE/$PROJECT}"

if [ -x "$HOME/.npm-global/bin/claude" ] || command -v claude &>/dev/null; then
  export PATH="$HOME/.npm-global/bin:$PATH"
  # Запускаем из /srv/bots/cluster (project-level .claude/settings.json).
  # --add-dir: ОДИН путь на флаг (нельзя список через пробел).
  # Permission mode задаёт пользователь через CLAUDE_EXTRA_FLAGS env var.
  cd "$REPO"
  timeout 2700 claude -p "$BRAIN_PROMPT" \
    --max-turns 80 \
    --add-dir /srv/bots/onchain \
    --add-dir /tmp \
    ${CLAUDE_EXTRA_FLAGS:-} \
    2>&1 | tee /tmp/claude_out.txt | tail -120 \
    || echo "  claude timeout/err"
else
  echo "  claude CLI not found — first run: sudo -u bots bash -c 'PATH=~/.npm-global/bin:\$PATH claude /login'"
fi

# === 6. Defensive: ensure HISTORY + cycle file got written ==================
if [ ! -f "$PROJ_INSIGHTS/cycle_$CYCLE_ID.md" ]; then
  echo "[!] AI didn't write cycle insight — creating placeholder"
  {
    echo "# cycle $CYCLE_ID (auto-placeholder, AI skipped write)"
    echo "## state snapshot"
    cat "$STATE_SNAPSHOT"
  } > "$PROJ_INSIGHTS/cycle_$CYCLE_ID.md"
fi

if ! grep -q "^$CYCLE_ID" "$PROJ_MEMORY/HISTORY.md" 2>/dev/null; then
  echo "$CYCLE_ID | (auto) cycle ran | files: cycle_$CYCLE_ID.md" >> "$PROJ_MEMORY/HISTORY.md"
fi

# === 7. Commit + push =======================================================
echo "[7] commit..."
cd "$REPO"
git add memory/ shared/ projects/ 2>/dev/null || true
if git diff --cached --quiet; then
  echo "  no changes"
else
  git -c user.name='bots-brain' -c user.email='brain@bots.local' \
    commit -m "cycle $CYCLE_ID [$PROJECT]" 2>&1 | tail -3
  git push 2>&1 | tail -3 || echo "  push failed (will retry next cycle)"
fi

# === 8. Telegram alert ======================================================
# Загружаем секреты из /srv/bots/.shared/.env (НЕ в git, создаётся при setup)
[ -f /srv/bots/.shared/.env ] && set -a && . /srv/bots/.shared/.env && set +a
TG_TOKEN="${TG_TOKEN:-}"
TG_CHAT="${TG_CHAT:-}"
if [ -z "$TG_TOKEN" ] || [ -z "$TG_CHAT" ]; then
  echo "  TG skipped: TG_TOKEN/TG_CHAT not set in /srv/bots/.shared/.env"
  echo "=== cycle $CYCLE_ID done $(date -u) ==="
  exit 0
fi
BRIEF_HEAD=$(head -15 "$PROJ_MEMORY/BRIEF.md" 2>/dev/null | sed 's/[<>&]//g')
MSG="🤖 [$PROJECT] cycle ${CYCLE_ID}
https://github.com/AlexeyKharin06/bots-cluster-/commits

BRIEF:
${BRIEF_HEAD}"
curl -s -X POST "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TG_CHAT}" \
  --data-urlencode "text=${MSG}" > /dev/null && echo "  TG sent"

echo "=== cycle $CYCLE_ID done $(date -u) ==="

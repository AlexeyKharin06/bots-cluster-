# Bots Cluster — Как пользоваться

Кластер из 6 крипто-проектов работает 24/7 на VPS Hostinger. Каждые 6 часов AI brain (Claude headless) анализирует данные, генерирует новые гипотезы, тестирует через walk-forward backtest, применяет рабочие. Все insights в этом GitHub repo.

---

## 1. Архитектура

```
Hostinger VPS (Frankfurt)
└── /srv/bots/
    ├── cluster/          ← GitHub repo (этот)
    │   ├── projects/onchain/   (код OnChain)
    │   ├── shared/             (общие скрипты)
    │   ├── memory/             (AI brain insights)
    │   └── docs/               (документация)
    ├── onchain/          ← runtime data (state, logs, .env)
    │   ├── data/         (sniper_state, pump_collection)
    │   ├── logs/         (sniper.log)
    │   └── .env          (Helius keys, Telegram tokens)
    ├── trade/
    ├── listing-arb/
    └── .shared/          ← общие для всех проектов
        ├── logs/         (cycle logs)
        ├── memory/       (cross-project insights)
        └── backups/
```

**Принцип**: код+insights в Git, runtime data на VPS, секреты в `.env` (никогда в Git).

---

## 2. Как подключиться к рабочей среде

### Вариант A — посмотреть прогресс не вмешиваясь

```bash
# С твоего компа:
ssh root@187.127.87.202

# Посмотреть статус контейнеров
docker ps

# Логи sniper OnChain:
docker logs onchain-sniper --tail 100

# Последний cycle AI brain:
cat /srv/bots/.shared/logs/cycle_$(ls -t /srv/bots/.shared/logs | head -1)
```

### Вариант B — взаимодействовать с тем же AI brain

На VPS работает **persistent tmux session "brain"**. Подключиться:

```bash
ssh root@187.127.87.202
sudo -u bots tmux attach -t brain
```

Внутри tmux:
- Detach (выйти, не закрывая сессию): **Ctrl+B**, потом **D**
- Reattach: `sudo -u bots tmux attach -t brain`

Если хочется **поговорить с Claude** прямо в tmux:
```bash
sudo -u bots bash -c 'cd /srv/bots/cluster && PATH=~/.npm-global/bin:$PATH claude'
```

Это **отдельная сессия Claude** в той же среде (она увидит все файлы). Когда закроешь — фоновый cron-AI продолжит работать сам в 0/6/12/18 часов.

### Вариант C — через GitHub Codespaces (если хочется веб-IDE)

GitHub → этот repo → **"Code" → "Codespaces" → "Create codespace"** — открывает VS Code в браузере с этим кодом. Можно редактировать, push изменения. На VPS подхватятся при следующем `git pull` (cron делает это автоматически каждые 6h).

---

## 3. Как читать что AI brain делал

### A. Telegram
В чате `411831496` каждые 6h приходит alert:
```
🤖 [onchain] cycle 20260519_1800
https://github.com/AlexeyKharin06/bots-cluster-/commits

BRIEF:
<первые 15 строк BRIEF.md — где мы сейчас>
```
Клик по ссылке → видишь все commits последнего цикла.

### B. GitHub repo — структура памяти AI brain

**Контекст НЕ теряется. Никогда.** Структура хранения:

```
memory/<project>/
├── BRIEF.md              ← навигационный snapshot текущего состояния (≤4KB).
│                          Перезаписывается каждый цикл.
│                          "где мы сейчас, что тестируем, что планируется"
├── HISTORY.md            ← APPEND-ONLY хронологический index.
│                          Одна строка на цикл: "20260519_1800 | tested X | result Y | files"
│                          Это таймлайн всех действий AI за всё время.
├── insights/
│   ├── cycle_20260519_1800.md   ← ПОЛНЫЙ untruncated лог цикла.
│   ├── cycle_20260520_0000.md      Без word limit. Все размышления, числа,
│   ├── cycle_20260520_0600.md      гипотезы которые отбросил, и почему.
│   └── ...                          Append-only — никогда не удаляются.
├── backlog.md            ← все гипотезы (testing/accepted/rejected) append-only
└── promotion.json        ← машинный state: paper streams + live stats
```

**Когда новый цикл стартует**, AI читает:
1. BRIEF.md — куда мы дошли
2. HISTORY.md последние 100 строк — таймлайн
3. **ПОСЛЕДНИЕ 3 cycle_*.md полностью** — детальный недавний контекст (untruncated)
4. Старые cycle_*.md по необходимости — если HISTORY указывает что там что-то важное

Это значит:
- Старая инфа никогда не теряется (всё на диске + git history)
- Токены экономятся за счёт того что AI не перечитывает 100 циклов подряд — у него есть HISTORY index
- Если что-то нужно из старого — `grep` по insights/ или HISTORY ссылка

### C. Как ты можешь читать историю

```bash
# Последний BRIEF
cat /srv/bots/cluster/memory/onchain/BRIEF.md

# Таймлайн всех действий за месяц
tail -200 /srv/bots/cluster/memory/onchain/HISTORY.md

# Конкретный цикл — полный лог
cat /srv/bots/cluster/memory/onchain/insights/cycle_20260519_1800.md

# Поиск: где AI тестировал гипотезу про smart wallets
grep -l "smart_wallet" /srv/bots/cluster/memory/onchain/insights/*.md
```

### D. Telegram /trades команда
Sniper-бот поддерживает команды:
- `/stats` — текущая статистика
- `/trades` — Excel со всеми trade'ами
- `/help` — справка

---

## 4. Цели AI brain

1. **Найти стратегию для +100,000% при минимальных рисках**
2. Анализировать **on-chain поведение кошельков** (smart money, insiders, ruggers)
3. Выявлять **pre-pump accumulation patterns** и **pre-rug warnings**
4. Тестировать через **walk-forward backtest** (train/val/test split по времени)
5. Внедрять как **paper streams** (size=$1) для live validation
6. Promote paper → real money только когда:
   - n ≥ 50 closed live trades
   - avgPnL ≥ +200% live
   - WR ≥ 65%
   - rug rate ≤ 25%
   - **Только с явным разрешением пользователя**

---

## 5. Управление

### Перезапустить контейнер
```bash
docker restart onchain-sniper
```

### Остановить AI brain (паузу)
```bash
sudo -u bots crontab -l | grep -v autonomous > /tmp/cron && sudo -u bots crontab /tmp/cron
```

### Запустить AI brain прямо сейчас (не дожидаясь cron)
```bash
sudo -u bots bash /srv/bots/cluster/shared/autonomous_cycle.sh
```

### Rate limit проверка
```bash
# Сколько Anthropic запросов за день
grep "claude -p" /srv/bots/.shared/logs/cron.log | wc -l
```

---

## 6. Добавление нового проекта (Trade / Listing Arb / etc)

См. `docs/ADD_NEW_PROJECT.md`.

---

## 7. Anti-rate-limit стратегия

Anthropic Max plan: ~1500-2500 messages per 5h rolling window.
6 проектов × 4 цикла/день × ~30 messages = 720/day baseline (запас 2-3×).

**Cron offsets** (UTC) — никогда не работают параллельно:

| Проект | Schedule |
|---|---|
| OnChain     | `0 0,6,12,18 * * *`  |
| Trade       | `0 1,7,13,19 * * *`  |
| Listing Arb | `0 2,8,14,20 * * *`  |
| CEX-Onchain | `0 3,9,15,21 * * *`  |
| PL          | `0 4,10,16,22 * * *` |
| Funding     | `0 5,11,17,23 * * *` |

Дополнительный guard: `shared/rate_limit_guard.sh` запускается ПЕРЕД claude. Если за последние 5h уже было ≥1200 messages — sleep 50min и пропуск цикла.

Если ты сам открываешь tmux сессию и общаешься с Claude — это считается отдельно (Anthropic один аккаунт). При особо длинной сессии может временно блокануться cron — это ОК, следующий слот через 6h.

---

## 8. Если хочется ускорить (запустить цикл вручную)

```bash
ssh root@187.127.87.202
sudo -u bots bash
PROJECT=onchain bash /srv/bots/cluster/shared/autonomous_cycle.sh
```

Или прямо из tmux сессии "brain" — там уже PATH настроен.

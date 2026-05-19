# bots-cluster

Кластер из 6 крипто-проектов с автономным AI brain (Claude headless каждые 6h).

**Цель**: +100,000% через выявление on-chain wallet-паттернов перед памп/раг.

## Quick start

На свежем Hostinger VPS (Ubuntu 24.04, root):

```bash
curl -fsSL https://raw.githubusercontent.com/AlexeyKharin06/bots-cluster-/main/setup_vps.sh | bash
```

Это поставит Python/Node/Docker, создаст пользователя `bots`, склонирует репо, зарегистрирует systemd для tmux 'brain', настроит cron.

См. `docs/HOW_TO_USE.md` — как подключаться, читать прогресс AI brain, добавлять новые проекты.

## Структура

```
bots-cluster-/
├── setup_vps.sh                ← bootstrap скрипт
├── shared/
│   ├── autonomous_cycle.sh     ← AI brain (cron 6h)
│   ├── rate_limit_guard.sh     ← anti-rate-limit
│   └── add_project.sh          ← (phase 2) шорткат для новых проектов
├── projects/
│   ├── onchain/                ← Solana/BSC sniper
│   ├── trade/                  ← (после миграции)
│   ├── listing-arb/
│   ├── cex-onchain/
│   ├── pl/                     ← Meteora DLMM LP
│   └── funding-rate/
├── memory/
│   └── <project>/
│       ├── BRIEF.md            ← navigation snapshot (always updated)
│       ├── HISTORY.md          ← append-only timeline
│       ├── insights/cycle_*.md ← полные логи циклов (untruncated)
│       └── backlog.md          ← гипотезы
└── docs/
    ├── HOW_TO_USE.md           ← как подключаться + читать insights
    └── ADD_NEW_PROJECT.md      ← как добавить новый проект
```

## Хранение контекста

Контекст AI brain между циклами **не теряется**.

- `memory/<project>/BRIEF.md` — компактный snapshot для быстрой навигации
- `memory/<project>/HISTORY.md` — append-only timeline всех циклов
- `memory/<project>/insights/cycle_*.md` — полные untruncated логи (детали, числа, отброшенные гипотезы)

Каждый цикл AI читает BRIEF + последние 100 строк HISTORY + последние 3 cycle_*.md полностью. Старые циклы по запросу через grep. Так не теряется ничего, и токены не сжигаются на повторное чтение всей истории.

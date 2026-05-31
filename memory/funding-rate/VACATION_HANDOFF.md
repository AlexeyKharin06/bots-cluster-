# 🏖 VACATION HANDOFF — 3 weeks

**Дата:** 2026-05-31
**Возвращение:** ~2026-06-21

## ✅ Что РАБОТАЕТ автономно (без Claude)

### Paper bots — 50 стратегий
- **Папка:** `/srv/bots/funding-rate/paper_v8/SXX_NAME/`
- **Файлы каждой стратегии:**
  - `trades.jsonl` — все entry/exit с PnL
  - `state.json` — текущие открытые позиции
  - `bot.log` — лог работы
- **Источник данных:** Binance Futures API (public, без ключей)
- **Симуляция:** $100/trade × 5 max concurrent positions

### Cron (на VPS)
- `*/5 * * * *` watchdog — restart мёртвых ботов
- `0 */6 * * *` autocommit — sync trades в git `/srv/bots/cluster/memory/funding-rate/paper_v8/`

### Файлы для возврата
- `/srv/bots/funding-rate/code/paper_bots_framework_v2.py` — основной код
- `/srv/bots/funding-rate/paper_v8/` — все trades/logs
- `/srv/bots/cluster/memory/funding-rate/` — все исследования (45+ MD файлов)

## ❌ Что ОСТАНОВЛЕНО (Claude limits saving)

- Claude AI brain cron — отключен
- tmux brain session — убит
- Никаких Claude процессов на сервере

## 📊 50 стратегий в работе

| Категория | Стратегии |
|-----------|-----------|
| **BTC-conditional** | S01 (top+vol SHORT), S02 (bear cont SHORT), S19 (bull+neg LONG), S20 (bear+pos SHORT), S21 (range+neg LONG), S35 (weak_bear+neg LONG) |
| **Basis (perp vs index)** | S03 (≥5% premium SHORT), S04 (≥0.5% discount LONG), S17 (≥1% premium SHORT), S18 (≥0.3% discount LONG), S33 (near zero SHORT) |
| **Funding bands** | S05 (mild neg LONG), S06 (deep neg LONG), S08 (high pos SHORT), S13 (-2 to -1% LONG), S14 (+1 to +2% SHORT), S15 (≤-2% LONG), S16 (≥+2% SHORT), S31 (decomp LONG), S34 (slight pos SHORT) |
| **Cap-pinned SHORT (top-8 coins)** | S07 (multi), S11 (CRV), S12 (AVAX), S22 (LINEA), S23 (BERA), S24 (TRUMP), S36 (1000BONK), S37 (WLD), S38 (POL) |
| **Passive LONG carry (chronic neg)** | S09 (BLAST), S10 (ENJ), S25 (BLUR), S26 (JTO), S27 (AXS), S39 (NOM), S40 (KLUNC), S41 (DYM), S42 (ENSO), S43 (KAT), S44 (MOVE) |
| **Quick scalp (4h hold)** | S28 (high pos SHORT), S29 (deep neg LONG) |
| **Session-based** | S45 (ASIA LONG), S46 (EURO LONG), S47 (US LONG) |
| **Cross-ex** | S32 (binance > bybit funding LONG) |
| **Combo confluence** | S30 (neg+discount LONG), S50 (triple confluence LONG) |
| **NICHE** | S48 (low-cap deep neg LONG) |
| **High-vol carry** | S49 (high vol + tiny pos SHORT) |

## 🔄 Возвращение через 3 недели

1. **Подключиться SSH:** `ssh -i /d/.ssh/id_rsa root@187.127.87.202`
2. **Проверить bots живы:** `ps -ef | grep paper_bots | wc -l` → должно быть 50
3. **Запустить анализ trades:** см. `/srv/bots/funding-rate/code/analyze_paper_v8.py` (TODO написать)
4. **Pick best 3-5 strategies → real money deploy**
5. **Resume Claude session:** `tmux new-session -d -s brain -c /srv/bots/cluster` + restore cron

## 🧮 Что искать в анализе после 3 недель

Для каждой из 50 стратегий:
- n trades total
- WR (winning rate)
- Mean PnL %
- Median PnL %
- Worst trade %
- Sharpe
- Best per-coin

Top-5 ПО STABILITY (не по top mean) — это и есть кандидаты на live deploy.

## ⚠️ Если что-то сломалось

- **Watchdog проверяет каждые 5 мин** — auto restart
- **Логи crash:** `/srv/bots/funding-rate/paper_v8/SXX/bot.log` (last lines)
- **Если cron остановился:** `crontab -e` и добавь обратно строки из этого файла

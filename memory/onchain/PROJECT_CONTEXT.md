# PROJECT CONTEXT — onchain (ответы на open questions)

> Этот файл — постоянный контекст проекта. AI brain читает его в начале каждого цикла (он в `memory/onchain/` рядом с BRIEF.md).

## Ресурсы (есть)

- **13 Helius API ключей** по 5M credits = ~65M credits/мес. Хватает на любую разработку.
- **Birdeye** (free 100 req/min)
- **CoinGecko Pro** (paid, 100K calls/мес)
- **BSCScan V1** (free, deprecated но работает для BSC reads)
- **Telegram MTProto session** (Telethon) — авторизована, может слушать каналы

## Wallet enrichment — строим сами, не платим

- Уже накоплено: **32K классифицированных токенов** в `tokens_unified.json` (был на D:\OnChain\scripts\wallet_v2\unified_db\, переноси на VPS если нужен)
- **6K LP/creator** с известной историей в `wallet_history_db.json`
- **3.2K rug-flagged wallets** в `rugger_blacklist.json`
- Build leaderboard сам через индекс tx через Helius (13 ключей хватит) + использовать существующие классификации
- **НЕ платить** за Cielo/GMGN external APIs

## Chain scope

- **PRIMARY: Solana** — memecoin focus, тут весь sniper работает
- **SECONDARY: BSC** — `BSC_FILTERED` стрим уже есть, работает на узкой нише (size $30)
- **НЕ трогать**: Ethereum/Base/Polygon — gas слишком дорогой, не наш domain

## Pipeline ownership и роль AI brain

**Контекст**: на D:\OnChain\ работает sniper-бот (`serial_sniper.js` + watchdog + daemons). Уже накоплено 4984 closed_trades.

**Роль AI brain (что ты делаешь в каждом цикле, 80 turns)**:
1. Читаешь свежий `sniper_state.json` → анализируешь closed_trades vs прошлый цикл
2. Формируешь новые гипотезы из wallet-patterns, добавляешь в backlog.md
3. Walk-forward бэктест одной гипотезы из backlog (TRAIN/VAL/TEST по времени, БЕЗ leakage)
4. Если прошла (n≥50, avgPnL≥+150%, WR≥60%, rug≤25%) — пишешь paper-stream спецификацию в `paper_streams_spec/{stream_name}.md` (JS code patch)
5. Пользователь применяет патч в `D:\OnChain\scripts\wallet_v2\serial_sniper.js` руками (или скрипт автоматизации позже)

**ВАЖНО**: AI brain НЕ пишет полный sniper с нуля и НЕ трогает контрольные стримы (SNIPER_A/B/D/H/GOLD3/4/5/WHALE/LATE/LOWCAP). Только дополнения как paper-streams (size=$1, paper:true).

## Данные на VPS

После миграции (выполнено пользователем 2026-05-19):
- `/srv/bots/onchain/data/sniper_state.json` — 4984 closed_trades с реальным PnL
- `/srv/bots/onchain/.env` — API keys
- (опционально) `/srv/bots/onchain/data/tokens_unified.json` — 32K classified

## Текущие активные стримы (контроль, НЕ трогать)

См. `D:\OnChain\CLAUDE.md` секция "АКТИВНЫЕ СТРИМЫ В SNIPER":
- GOLD3/4/5, WHALE, LATE, LOWCAP — Solana
- BSC_FILTERED — BSC
- A/B/D/D2-D5/E/E2-E5/F/F2-F5/G/H/H2/GOLD/GOLD2 — старые baseline-стримы

## Цель (как мерять успех)

**+100,000% (×1000)** через реинвестирование 5-7 successful trades подряд на серийных мемкоинах.
- AvgPnL +400% backtest (GOLD3) × 3 сделки с реинвестом = +12,400% (×125)
- 5 сделок = +×10,000% (×100K)
- Брейк-ивен: 50-150 live trades за 7-14 дней (paper streams накопят statistical significance)

## Что AI brain делать НЕ должен

- Запускать реальные сделки (всё paper, size=$1, `paper:true` flag)
- Трогать контрольные стримы
- `git push --force`
- Удалять файлы в `memory/`, `projects/`, `shared/`
- Показывать конкретные адреса токенов в commit messages (это alpha)
- Backtest без time-split (leakage = invalidates results)

## Open questions от AI brain (cycle 20260519_1550) — ОТВЕЧЕНЫ

1. ✅ RPC: 13 Helius ключей (~65M credits/мес) — бесплатно для нас, бюджета хватит
2. ✅ Wallet enrichment: строим сами через `tokens_unified.json` + Helius indexing
3. ✅ Chain scope: Solana primary, BSC secondary, ничего больше
4. ✅ Pipeline ownership: AI brain = strategist (paper specs), user applies code patches manually

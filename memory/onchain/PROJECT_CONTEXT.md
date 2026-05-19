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
- `/srv/bots/onchain/data/sniper_state.json` — 4999+ closed_trades с реальным PnL (symlink → `code/scripts/wallet_v2/sniper_state.json`, обновляется live)
- `/srv/bots/onchain/.env` — API keys
- `/srv/bots/onchain/data/tokens_unified.json` — 32K+ classified Solana tokens (18.6 MB, имеет `updated_at` per entry для time-aware фильтрации)
- `/srv/bots/onchain/data/wallet_history_db.json` — 1.5 MB истории кошельков
- `/srv/bots/onchain/data/rugger_blacklist.json` — 674 KB (но с hindsight-leakage — см. H_RUG_PC reject в cycle_1702; без `wallet_added_at` per entry непригодна как фильтр)

## Дополнительные ресурсы — Telegram pipeline

**Расположение**: `/srv/bots/onchain/tg/` (мигрировано с D:\OnChain). Telethon session активна, `tg_listener.py` пишет live signals.

**Данные**:
- `signals_pool.json` / `media_signals_pool.json` — корпус собранных TG-сигналов (text + media batches)
- `realtime_signals.jsonl` — live append-only поток новых сигналов от listener
- `channel_pump_predictiveness.json` — **per-channel метрики**: WR/pump-count/multipliers на исторических сигналах. Это первичный кандидат для walk-forward анализа.
- `channel_multipliers.json` — рассчитанные multipliers per channel (для weighting)
- `media_signals_enriched.jsonl`, `media_signals_aggregate.jsonl` — обогащённые сигналы (CA + metadata)
- `media_new_cas_for_db.json` — новые contract addresses из медиа
- `signals_database.jsonl` — append-only база сигналов
- `historical_walkforward_results.json`, `walk_forward_results.json`, `wallet_behavior_results.json`, `honest_backtest_results.json`, `realized_pnl_backtest.json`, `wave2_backtest.json` — кэш прошлых бэктестов (читать перед новым прогоном чтобы не дублировать)
- `autonomous_patterns.json`, `blind_spots.json`, `fud_blacklist_builder.py` (output)

**Скрипты (готовые анализаторы)**:
- `analyze_signals.py` — analytics над signals_pool
- `walk_forward_backtest.py` / `historical_walk_forward.py` — generic walk-forward
- `autonomous_pattern_mining.py` / `ml_strategy_honest.py` / `ml_strategy_discovery.py` — ML-based pattern mining
- `wallet_behavior_alpha.py` / `sniper_wallet_alpha.py` — wallet-side alpha
- `backtest_dev_track_record.py` / `backtest_exit_upgrade.py` / `backtest_wave2.py` — спец-бэктесты
- `realized_pnl_backtest.py` / `honest_backtest_live_trades.py` — sanity backtests на реальных closed trades
- `build_smart_wallet_db.py`, `build_smart_wallet_db_v2.py`, `xref_media.py`, `xref_all.py` — DB builders/cross-ref
- `fud_blacklist_builder.py` — FUD-aware blacklist
- `dump_media.py`, `tg_dump.py`, `enrich_visual.py` — медиа-pipeline для signal enrichment

**Как AI brain использует TG-pipeline**:
1. Cross-ref сигналов с нашими closed_trades по token CA → строим per-channel walk-forward с decontamination split (как для rugger_blacklist в cycle_1702 — обязательно проверить hindsight-leakage в `channel_pump_predictiveness.json`)
2. Найденный канал-кандидат → paper-stream `TG_<channel>` с filter `signal.channel ∈ whitelist AND signal_time < entry_time`
3. Композиции TG-signal × onchain-filter (H_LP_HIST, H_DISTRIB) — ortogonal sources уменьшают correlation noise

**Caveats**:
- Никогда не использовать сигнал, у которого `signal_time >= entry_time` (look-ahead)
- `channel_pump_predictiveness.json` мог быть построен с hindsight (как rugger_blacklist) — обязательно decontamination split (CLEAN vs DIRTY по overlap с нашими trade tokens) перед доверием
- Каналы пишут pump-and-dump спам наравне с реальными сигналами — multiplier alone не достаточен, нужен per-channel walk-forward на честном time-split

## Текущие активные стримы (контроль, НЕ трогать)

См. `D:\OnChain\CLAUDE.md` секция "АКТИВНЫЕ СТРИМЫ В SNIPER":
- GOLD3/4/5, WHALE, LATE, LOWCAP — Solana
- BSC_FILTERED — BSC
- A/B/D/D2-D5/E/E2-E5/F/F2-F5/G/H/H2/GOLD/GOLD2 — старые baseline-стримы

## Цель (как мерять успех)

**+1,000,000% (×10K)** через реинвестирование 6-8 successful trades подряд на серийных мемкоинах. Обновлено пользователем 2026-05-19.

- AvgPnL +400% backtest (GOLD3) × 3 сделки с реинвестом = +12,400% (×125)
- 5 сделок = +×100K (предыдущая цель ×1000 пройдена)
- 6-7 сделок с avg +400% = +×500K-×3M
- Брейк-ивен: 50-150 live trades за 7-14 дней (paper streams накопят statistical significance)
- **Импликация для гипотез**: fat-tail метрики (big%≥10, huge%≥3) важнее avgPnL. Strict +150% gate возможно нужно заменить expectancy/Kelly-based gate (см. open question в BRIEF.md, carrying since 1639).

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

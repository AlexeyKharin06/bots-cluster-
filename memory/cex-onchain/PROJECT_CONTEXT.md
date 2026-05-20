# CEX-Onchain — VPS PROJECT CONTEXT

> AI brain context file for autonomous CEX-Onchain trading bot on Hostinger VPS.
> Migrated from D:\CEX-Onchain (Windows) on 2026-05-20.

## Цель проекта

Торговая стратегия на низколиквидных альт-коинах Gate/MEXC, основанная на on-chain
детекции инсайдерских депозитов на биржу. Гипотеза: координированный занос токена
на CEX = подготовка к дампу = шорт.

## VPS layout (все пути)

| Что | Где |
|-----|-----|
| Код | `/srv/bots/cex-onchain/code/` |
| Секреты | `/srv/bots/secrets/cex-onchain/` (.env, .tg_credentials) |
| Память | `/srv/bots/cluster/memory/cex-onchain/` |
| Логи | `/srv/bots/.shared/logs/cron_cex-onchain.log` |
| Wrapper | `/home/bots/run_cycle_cex-onchain.sh` |
| Cron | `0 3,9,15,21 * * * UTC` (4 цикла/день) |

## Стратегия — текущая (после ~25 циклов research)

### 9 trade slots (100% capital)

| Slot | Cap% | Exit | Триггер |
|------|------|------|---------|
| C | 15% | 168h | n_addr ≥ 28× + dump_cont |
| B | 20% | 168h | n_addr ≥ 5× + crash7d |
| U | 4% | 168h | max_dep≥30 AND n_addr≥3 AND pos_7d≤50 |
| A | 20% | 168h | gross_dep ≥ 62.4 + 7d≤70 + 24h≤0 |
| T | 8% | 168h | max_dep≥15 AND n_addr≥3 + 24h≤0 |
| A2 | 15% | 168h | max_dep ≥ 20 + 7d≤30 + 24h≤0 |
| K | 5% | 48h | n_addr ≥ 5× + 7d≤100 |
| S | 8% | 168h | dep ≥ 0.01% FDV + 7d≤70 |
| M | 5% | 168h | max_dep ≥ 15 + 7d≤70 + 24h≤0 |

### Конфигурация

- **DRY_RUN = True** — paper trading пока не получен явный go-live
- **TOTAL_CAPITAL = $10000**
- **Leverage = 5x**
- **Stop-Loss = 20%**
- **TOKEN_BLACKLIST**: QQQX, MSTRX, TQQQX, BUTTCOIN

## Источники данных (KPI)

| Источник | Размер | Назначение |
|----------|--------|-----------|
| data/transfers/{eth,sol,bsc,base}/*.parquet | 15MB | 90d CEX deposits |
| data/candles_5m/{mexc_spot,mexc_swap}/*.parquet | 40MB | OHLCV для backtest |
| data/wallet_tags.parquet | 416KB | 8229 классифицированных адресов |
| data/dumper_wallet_whitelist.json | 20KB | 73 high-conviction dumpers |
| data/token_supply.parquet | 12KB | FDV для slot S |

## Активные инструменты автономной работы

### Scripts (83 файла, последние ключевые)

- **65_autonomous_researcher.py** — daemon с walk-forward на всех slots
- **66_wallet_chain_token_deep_analysis.py** — per-tag/chain/token PnL
- **67_live_readiness_check.py** — GO/NO-GO verdict
- **68_continuous_orchestrator.py** — оркестратор всех pipelines
- **72_ml_ensemble.py** — XGBoost confidence model (rejected)
- **74_and_combo_search.py** — 2-feature AND grid search
- **77_triple_and_search.py** — 3-feature AND combos
- **78_slot_a_chg24h_filter.py** — chg_24h optimization

## Lessons learned (17 уроков из reports/LESSONS.md)

Ключевые:
- L11/L12: Static-positive backtest часто отклоняется на walk-forward
- L14: 6/6 TG-derived гипотез отклонены strict validation
- L17: Telegram infographics часто cherry-picked, проверять raw data
- chg_24h ≤ 0% — универсальный фильтр для deposit-based slots (+6-9pp WF)

## Запреты

- ❌ НЕ менять DRY_RUN=False без явного разрешения user
- ❌ НЕ удалять existing slots без backtest validation
- ❌ НЕ deploy новый slot если WF < 4/5 окон positive

## KPI / Readiness criteria (8 critical)

Бот → live trading когда все 8 pass:
1. Sample ≥30 closed trades
2. Win rate ≥55% (последние 30)
3. Max single loss ≤5% капитала
4. Account drawdown <30%
5. Daemon runs present
6. No degradation flags
7. Live mean PnL > 0
8. Slippage <2%

Текущее состояние: **3/8** (главный блокер — UPEG#1 -$3,482 от 05-05 ещё в rolling window).

## Стартовая инструкция для новой Claude-сессии

1. Прочитать этот файл (PROJECT_CONTEXT.md)
2. Прочитать loop_cycle_log.md (timeline всех research циклов)
3. Прочитать MEMORY.md (индекс других memory файлов)
4. Прочитать reports/LESSONS.md (17 уроков выше абстракции)
5. Свежие отчёты в reports/auto_research_log.md, orchestrator_log.md
6. Текущий verdict в reports/readiness_verdict.md

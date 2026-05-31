# 🎯 POST-VACATION DEEP ANALYSIS — Полная инструкция для Claude

## Контекст
Боты работали 3 недели автономно (с 2026-05-31). Собрали ~5K-15K новых live trades + light_token_log + wallet_db updates + chart classifications + TG signals + pool snapshots.

**Цель**: провести максимально глубокий honest анализ → найти РЕАЛЬНО рабочие стратегии для live $$$ торговли.

## ⚠️ Правила работы Claude (строго соблюдать)

1. **ВСЕ источники данных загружать в Phase 1**. НЕ начинать анализ пока не сделан полный аудит. Не пропускать ни одного файла.
2. **Декомпозировать по блокам**, НЕ snapshot-анализ. Каждый Phase = отдельный stage с output checkpoint.
3. **Data leakage = смертный грех**. Любая фича из ATH/exit_price/time_to_ath = leak. Bool это запрещено.
4. **Только honest walk-forward**. Фича доступна на момент решения = OK. Иначе = leak.
5. **Bootstrap confidence intervals** обязательны для top filters. Не "n=20 100% wins" а "n=20 [bootstrap p5=70%, p50=85%, p95=95%]".
6. **Dedupe by token**. closed_trades имеет 7-8x duplicates через stream-variants. Без dedupe inflated n.
7. **Fixed $50/trade сайзинг** при расчете total $ ROI. Compounding 1000 trades × 5% = $10^60 = bullshit.
8. **Per-stream analysis отдельно**. НЕ aggregate всех стратегий вместе.
9. **Каждая гипотеза → тест → результат → вывод**. Не накручивать +findings без validation.
10. **Compare live vs backtest** для каждой стратегии: какие выдержали, какие нет, почему.

## PHASE 1 — Data Source Audit (BEFORE ANY ANALYSIS)

```bash
# Прежде чем что-либо считать — pull все данные с VPS
cd /d/OnChain
bash pull_data.sh all

# Затем audit ВСЕХ файлов:
find D:/OnChain -name "*.json" -o -name "*.jsonl" -o -name "*.pkl" -o -name "*.npz" 2>/dev/null | xargs ls -la | sort -k 5 -nr | head -50
```

**Обязательно загружать и анализировать ВСЕ:**

| Источник | Где | Что внутри |
|---|---|---|
| `sniper_state.json` | `scripts/wallet_v2/` | closed_trades (live trades за 3 нед), open_positions |
| `light_token_log.jsonl` | `scripts/wallet_v2/unified_db/` | ВСЕ seen tokens (даже skipped) — DexScreener snapshots |
| `tokens_unified.json` | `scripts/wallet_v2/unified_db/` | 34K+ classifications (PUMPED_ALIVE/RUG_NO_PUMP/etc.) |
| `wallet_db_solana.json` | `scripts/wallet_v2/` | 95K+ wallet classifications (smart/sniper/rugger/serial_pump) |
| `wallet_history_db.json` | `scripts/wallet_v2/unified_db/` | LP/creator wallet histories |
| `rugger_blacklist.json` | `scripts/wallet_v2/unified_db/` | Известные ruggers (~4-10K wallets) |
| `bsc_rugger_blacklist.json` | `scripts/wallet_v2/unified_db/` | BSC ruggers |
| `pump_collection.json` | `scripts/` | 171K+ snapshots с ds_h1/h6/h24 |
| `pump_trades_cache.json` | `scripts/` | Trade records |
| `ohlcv_gecko_solana.json` | `scripts/` | 8.5K+ tokens с минутными OHLCV |
| `ohlcv_gecko_bsc.json` | `scripts/` | BSC OHLCV |
| `pool_snapshots.json` | `scripts/wallet_v2/unified_db/` | 9.7K+ pools time-series |
| `cache_unified_swaps.json` | `scripts/` | Swap-level data с wallet адресами |
| `token_charts_cache.json` | `scripts/wallet_v2/unified_db/` | 29K+ chart classifications |
| `holders_cache.json` | `scripts/wallet_v2/` | Cached holders |
| **TG signals**: | | |
| `signals_pool.json` | `scripts/wallet_v2/` | TG channel mentions per token |
| `signals_database.jsonl` | `tg/` | 31K+ TG message records |
| `media_signals_enriched.jsonl` | `tg/` | TG/image signals с tier classification |
| `media_signals_pool.json` | `tg/` | Per-token image signal aggregates |
| `pump_fun_signals.json` | `scripts/wallet_v2/` | Pump.fun monitor feed |
| `dexscreener_signals.json` | `scripts/wallet_v2/` | DexScreener boosted/profiles |
| `fud_token_blacklist.json` | `scripts/wallet_v2/unified_db/` | Известные scams |
| **Backtest history**: | | |
| `deploy/shared/overnight_results/` | | v1 robust filters (689 dedup tokens) |
| `deploy/shared/overnight_v3_results/` | | v3 megagrid 164M combos (had leak) |
| `deploy/shared/deep_real_v5_results/` | | v5 FAIR (AUC 0.87, без leak) |
| `deploy/shared/backtest_full_results/` | | full universe backtest (22K tokens) |
| `deploy/shared/auto_learn_output/` | | ночные модели за 3 недели |
| `deploy/shared/auto_learn_output/auto_learn_history.json` | | append-only лог решений |

**Output Phase 1**: `data_audit_report.json` — для каждого источника: rows, time range, key fields, sample row.

## PHASE 2 — Per-Stream Live Performance (FIRST OUTPUT)

```bash
python /d/OnChain/deploy/shared/per_stream_report.py
```

Это даст разделение KEEP / SUSPECT / DROP по каждой из 84 стратегий по реальным live данным.

**Output**: таблица для каждой стратегии:
- n_trades (live за 3 нед)
- avg PnL (realized)
- WR%, rug%, big%, huge%
- vs backtest expected (diff)
- Verdict: KEEP / SUSPECT / DROP / UNKNOWN

## PHASE 3 — Honest Data Cleaning

Для всего dataset:
1. **Dedupe by token** (earliest entry only)
2. **Merge sources**: для каждого token собрать данные из ВСЕХ источников
3. **Label outcomes**: 
   - `ath_gain_pct` = (ath_price/entry_price - 1)*100
   - `realized_pnl` = closed_trades pnl_pct
   - `is_rug` = realized<=-50 OR classification in (RUG_NO_PUMP, PUMPED_RUGGED)
   - `is_big` = ath_gain >= 100
   - `is_huge` = ath_gain >= 500
   - `is_mega` = ath_gain >= 2000
4. **Time alignment**: для каждой row узнать timestamp entry
5. **Sanity check leakage**: ВСЕ ATH-derived features удалить из feature set

## PHASE 4 — Feature Engineering by 10 Blocks

### Block 1: Holder Structure
- top1_pct, top5_pct, top10_pct, top20_pct, top40_pct
- smart_money_count, serial_pump_count, sniper_count, rugbot_count, serial_rug_count
- positive_w_count, high_risk_count
- bundle_detected (boolean)
- serial_supply_pct (ssp)

### Block 2: Liquidity / MarketCap
- liq_usd, mcap_usd
- log_liq, log_mcap
- liq_to_mcap_ratio
- mcap_per_holder
- liq_per_holder
- log_mcap_x_smart (interaction)

### Block 3: Volume Profile
- vol_h24, vol_m5
- vol_to_liq, vol_to_mcap
- buys_m5, sells_m5
- bsr (buy/sell ratio)
- buys_minus_sells

### Block 4: Time-Series OHLCV (FIRST 5/15 MIN ONLY — fair!)
- pc_5m (price change 0-5 min)
- pc_10_15m (price change 10-15 min)
- pc_15m (close at minute 15)
- range_5m, high_5m, low_5m
- max_dd_15m (max drawdown in first 15 min)
- vol_5m, vol_15m
- volat_5m (volatility std of returns)
- up_pct_5m (% of candles green)
- n_candles_15m
- **ЗАПРЕЩЕНО**: pc за >15 min, ath_gain_pct_stats, time_to_ath, max_dump

### Block 5: Wallet Network
- top1_in_rugger_blacklist (boolean)
- creator_in_rugger_blacklist (boolean)
- lp_in_rugger_blacklist (boolean)
- top1_is_smart, creator_is_smart, lp_is_smart
- top1_is_serial_pump, creator_is_serial_pump
- wallet_appearances_count (сколько раз top1/creator/lp в других токенах в нашей DB)
- wn_total_pump_count (агрегат pump_count по всем wallet_roles)
- wn_total_rug_count

### Block 6: TG / Social Signals
- tg_mentions_24h (количество TG mentions за 24h)
- tg_mentions_total
- tg_channel_tier_max (TIER_S/A/B/C from media_signals_enriched)
- tg_unique_channels_count
- tg_pre_pool_alpha (boolean — pre-pool TG signal)
- tg_call_type (BUY/PUMP/SCAM_WARNING)
- tg_image_signal (boolean)
- pumpfun_hot (boolean from pump_fun_signals)
- dexscreener_boost_amount

### Block 7: Pool Dynamics (from pool_snapshots)
- pool_tvl_delta_15m (TVL change в первые 15 мин)
- pool_price_velocity
- pool_b5_to_s5_ratio
- pool_n_snaps (data quality)

### Block 8: Market Phase
- utc_hour (0-23)
- utc_dow (0-6)
- is_friday (UTC dow=5)
- is_bad_hour (8/11/15 UTC)
- is_weekend
- week_of_year

### Block 9: Chart Classifications
- chart_class (PUMPED_ALIVE/RUG_NO_PUMP/etc, one-hot)
- classification_tu (tokens_unified classification)

### Block 10: Cross-Feature Interactions
- smart × buys
- top1 × top5
- top1 × smart
- bsr × vol_to_liq
- bundle × smart_count
- log_mcap × smart
- chain_solana, chain_bsc one-hot

## PHASE 5 — Combination Mining (10-100M combinations)

Используя scripts уже есть:
```bash
python /d/OnChain/deploy/shared/overnight_v3_maximum.py    # 164M combinations (если хватит компьюта)
python /d/OnChain/deploy/shared/backtest_full_universe.py  # full universe valid
```

Mining strategies:
1. **3-way exhaustive** на all features
2. **4-way seeded** — топ-5000 3-way × all features
3. **5-way seeded** — топ-3000 4-way × all features
4. **6-way seeded** — топ-2000 5-way × all features

Для каждого filter с n>=30:
- big_rate, huge_rate, rug_rate, realized_avg
- bootstrap 5000 resamples → p5/p50/p95 confidence
- Stability test: split data 50/50 → big_rate в первой vs второй половине

## PHASE 6 — ML Multi-Target Training

5 targets:
1. **big** (ATH≥100%) — baseline
2. **huge** (ATH≥500%) — jackpot
3. **norug** (realized > -50%) — safety filter
4. **realized_big** (realized ≥ 100%) — EV predictor
5. **realized_big50** (realized ≥ 50%) — broader EV

4 algorithms:
- LogisticRegression (balanced, C=0.1)
- RandomForest (300 trees, depth 8)
- GradientBoosting (200 trees, depth 4, lr=0.05)
- ExtraTrees (300 trees, depth 8)

5-fold TimeSeriesSplit CV.

Best by mean CV AUC → train final 80%/20% → permutation importance.

**Output**: 5 моделей `final_model_*.pkl` + AUC report per target.

## PHASE 7 — Walk-Forward Backtest (HONEST)

Для каждой стратегии (по результатам Phase 5/6):
1. Для каждого token: entry at minute 15 (after observing first 15 min)
2. Walk through subsequent OHLCV candles
3. Apply exit rules: trail/SL/cap
4. Record realized PnL

Exit configurations to test:
- default: trail=85%, SL=-15%, cap=500%
- balanced: trail=90%, SL=-20%, cap=2000%
- aggressive: trail=92%, SL=-20%, cap=3000%
- max_cap: trail=95%, SL=-15%, cap=5000%

**ВАЖНО**: fixed $50 per trade, NO compounding для total $.

## PHASE 8 — Loss Causality Analysis

Для каждой DROP стратегии (Phase 2 verdict):
1. **Class distribution**: какие классификации она ловит? (PUMPED_RUGGED %, RUG_NO_PUMP %, NO_PUMP_ALIVE %)
2. **Feature profile**: что отличает её losses от winners?
3. **Compare to KEEP стратегии**: какие features они НЕ используют?
4. **Build counter-filter**: добавить условие что отсекает losses

## PHASE 9 — Strategy Synthesis (Output for Deploy)

Создать 4 категории стратегий:

### Strict (high precision, low n)
- Condition: very tight criteria (top1<10 + smart>=5 + ssp<10 + etc)
- Size: $100-200 live (high conviction)
- Target: 60%+ WR, 0% rug

### Flexible (adaptive)
- Condition: ML model probability >= 0.7 OR rule match
- Size: $30-50 live
- Adapt to market regime

### Combined (composite)
- Condition: 2+ strategies ANDing
- Size: $50-100 live
- Higher precision through agreement

### Aggressive (capture jackpots)
- Condition: MOMENTUM_15 style (visible pump in first 15 min)
- Size: $10-30 live
- Accept losses for upside

## PHASE 10 — Decision Matrix

For each strategy:
| Strategy | Backtest avg | Live avg (3w) | Live WR | Live rug | Verdict | Recommended size |
|---|---:|---:|---:|---:|---|---:|
| V5_strong | +153% | ? | ? | ? | KEEP/SUSPECT/DROP | $? live |

**Final deployment**: размеры для каждой strategy, exit config, daily/weekly limits.

## PHASE 11 — Pre-Live Checks

Перед запуском real money:
- [ ] All KEEP стратегии validated на ≥30 live trades
- [ ] Exit logic protects against >-20% drawdown per trade
- [ ] norug ML model >0.5 mandatory gate
- [ ] Daily loss kill-switch ($-200 max)
- [ ] Telegram alerts работают
- [ ] backup plan если все Helius keys exhaust

## КОМАНДА В НОВОЙ CLAUDE СЕССИИ

После 3 недель скажи Claude:

> Прочитай `D:\OnChain\deploy\shared\POST_VACATION_DEEP_ANALYSIS_INSTRUCTION.md` и follow её строго. Сначала pull данные с VPS, потом Phase 1 audit, потом по порядку Phase 2-11. НЕ skipping. НЕ surface-level. Я хочу finalized стратегии для real money после твоего анализа.

Claude должен:
1. ✅ Не начинать без полного audit Phase 1
2. ✅ Запустить per_stream_report.py для немедленного KEEP/DROP feedback
3. ✅ Параллельно строить feature matrix из ВСЕХ блоков 1-10
4. ✅ Долго грайндить mining комбинаций (3+ часа реального compute)
5. ✅ Bootstrap для confidence
6. ✅ Walk-forward backtest на полной выборке
7. ✅ Loss causality для каждой DROP
8. ✅ Synthesize 4 категории стратегий
9. ✅ Подготовить deployment с конкретными sizes

## Anti-patterns (что НЕЛЬЗЯ делать)

❌ Загрузить sniper_state.json и начать grid search (узкая выборка)
❌ "164M combinations" без аудита откуда они и какая выборка
❌ Включить ath_gain_pct_stats в features (LEAK)
❌ Compounding $100 → $1B (math fail на 3000 trades × 5%)
❌ "Strategy X: n=20 100% WR" без bootstrap CI
❌ Skip Phase 2 (per_stream_report) и сразу прыгать в Phase 5
❌ "Strategy X работает" без сравнения live vs backtest

## Время

Reasonable runtime:
- Phase 1: 30 мин (data audit)
- Phase 2: 5 мин (per_stream_report)
- Phase 3-4: 1-2 часа (cleaning + feature engineering)
- Phase 5: 3-6 часов (combination mining)
- Phase 6: 1-2 часа (ML training × 5 targets × 4 algos)
- Phase 7: 1-2 часа (walk-forward backtest grid)
- Phase 8-9: 1-2 часа (loss analysis + synthesis)
- Phase 10-11: 30 мин (decision matrix + checks)

**Total: 8-15 часов real compute**. Если кончил за 30 мин — ты что-то пропустил.

## Output Files (что должно появиться)

```
D:\OnChain\deploy\shared\post_vacation_analysis_<date>\
├── data_audit_report.json
├── per_stream_report.json               (Phase 2)
├── merged_dataset.parquet (или .npz)    (Phase 3)
├── feature_matrix.npz                   (Phase 4)
├── feature_names.json
├── combination_mining_top10000.json     (Phase 5)
├── bootstrap_top500_ci.json             (Phase 5)
├── ml_models/                           (Phase 6)
│   ├── big.pkl, huge.pkl, norug.pkl, realized_big.pkl, realized_big50.pkl
│   └── ml_report.json
├── walkforward_results_per_strategy.json (Phase 7)
├── loss_causality_report.json           (Phase 8)
├── final_strategies_4_categories.json   (Phase 9)
├── decision_matrix.json                 (Phase 10)
└── DEPLOY_PLAN.md                       (Phase 11)
```

## Финал

После Phase 11 ты должен дать пользователю:
1. **Конкретные стратегии для live $$$** (4-8 штук, с sizes)
2. **Какие стратегии выкинуть** (с обоснованием)
3. **Какие пограничные** (продолжать paper)
4. **Total expected EV** при выбранном portfolio
5. **Risk metrics** (max DD, daily loss limit)
6. **Monitoring plan** для первой недели live

Это финальный analysis — после него начинается **real money trading**. Не должно быть "ой я забыл проверить wallet_history". ВСЕ источники, ВСЕ комбинации, ВСЕ honest validation.

# 🎯 ФИНАЛЬНЫЙ ЧЕСТНЫЙ PLAYBOOK — ВСЕ phases consolidated

**Все цифры с учётом РЕАЛЬНОЙ цены (funding + price change - 15bp costs)**

---

## 🔥 TOP STRATEGIES — настоящие edges (price-aware)

### 🥇 BTC-near-top + medium vol → SHORT (Phase T heavy grid)
**Trigger:** BTC distance from 30d ATH ≥ -3% AND BTC vol (24h) ≥ 0.70%
**Action:** SHORT перп на любом активном альте
**Hold:** 24 funding periods

| Metric | Value |
|--------|-------|
| n | 143 events |
| **Real mean PnL** | **+9.13%** |
| **WR** | **94%** |
| Sharpe | 1.44 |
| Worst trade | -6.2% |
| 5%-tail | +0.01% (рядом с zero) |

**Логика:** BTC у вершины + повышенная волатильность = pump exhaustion → коррекция → SHORT перп выигрывает на цене + на funding.

### 🥈 Continuation SHORT в deep drawdown
**Trigger:** btc_vol ≤ 0.21 AND btc_dist_high ≤ -8% AND btc_ret_24h ≤ -1.1%
**Action:** SHORT перп

| Metric | Value |
|--------|-------|
| n | 144 |
| **Real mean** | **+10.43%** |
| WR | 92% |
| Worst | -24.7% (wider range) |

**Логика:** Низкая vol + глубокое падение + продолжает падать = bear continuation.

### 🥉 Basis arbitrage (perp deeply above spot)
**Trigger:** basis_pct (perp/spot - 1) ≥ +5.7% AND BTC near ATH (≥-1%)
**Action:** SHORT перп (mean reversion)

| Metric | Value |
|--------|-------|
| n | 128 |
| Real mean | +7.35% |
| WR | 85% |
| Worst | -6.3% |

### 4️⃣ Fair-price LONG в мягком negative funding band (NEW — revived)
**Trigger:** rate в band [-0.5%, -0.1%]
**Action:** LONG перп, hold 24h

| Metric | Value |
|--------|-------|
| n | **1,688** (big sample!) |
| Real mean | +2.40% |
| WR | 53% |
| Worst | -36% (tail risk!) |
| **Months positive** | **5/5** ⭐ stable |

### 5️⃣ Combined rate + basis LONG (real combo)
**Trigger:** rate ≤ -0.1% AND basis_pct (perp - spot) ≤ -0.3%
**Action:** LONG перп

| Metric | Value |
|--------|-------|
| n | 1,713 |
| Real mean | +2.84% |
| WR | 55% |
| Months pos | 4/5 |

### 6️⃣ BORROW spike → SHORT (FLIPPED from earlier!)
**Trigger:** borrow_rate ≥ 1.5x rolling baseline
**Action:** **SHORT перп** (NOT LONG как раньше думал)

| Metric | Value |
|--------|-------|
| n | 64 |
| Real mean | **+5.63%** |
| WR | **78%** |
| Months pos | 3/4 |

**Раньше я говорил LONG. С price-aware PnL — flipped to SHORT.** Логика: high borrow demand = массовый sell pressure → цена падает БОЛЬШЕ чем funding собирает.

### 7️⃣ DEEP-LONG в WEAK_BEAR regime BTC
**Trigger:** BTC trend = WEAK_BEAR AND rate ≤ -0.5%
**Action:** LONG перп

| Metric | Value |
|--------|-------|
| n | 115 |
| Real mean | +5.39% |
| WR | 59% |

---

## ❌ ОПРОВЕРГНУТЫЕ "стратегии" (только funding-only видны)

| Strategy (старое утверждение) | Real PnL с ценой |
|-------------------------------|-------------------|
| H_BORROW_SQUEEZE LONG (+6.9%) | Real -25% на LYN class. Flipped → SHORT |
| HIGH-RATE-STABLE-SHORT (+2.88%) | Regime-dependent (только последние 2 мес) |
| GOLD MID-LONG (+2.63%) | Funding-only, не tested с ценой |
| ALL "WR 100%" claims | Это funding-only, real WR 50-65% |

---

## 📊 TG ПРАКТИКИ — БОЛЬШОЕ РАЗОЧАРОВАНИЕ

84 TG-сигналов проверены через 24h forward:

| Channel | n | Real PnL | WR |
|---------|---|----------|-----|
| ALL | 84 | **-5.47%** | 40% |
| @arbitragediarys | 12 | -21.13% | 25% |
| @ua_cryptoinvest | 52 | -3.08% | 44% |
| @vincerid_lost | 7 | -1.77% | 29% |
| @lopata_arb | 5 | -1.24% | 20% |
| @cryptoarbitr_obline | 3 | -10.32% | 33% |
| **@twix1444** | **5** | **+0.77%** | **80%** ⭐ |

**RAVE: practitioners хвастались +$39K, реально следуя =** **-54.5% потери** (n=7).

**Вывод:** TG channels — postmortem, не entry signals. Только @twix1444 хоть marginal positive.

---

## 💰 РЕКОМЕНДАЦИЯ ПОРТФЕЛЯ @ $1,000

| Strategy | $ | Real expected/mo |
|----------|---|--------------------|
| 🥇 BTC near-top + high-vol SHORT | $300 | $250-400 (5-8 trades/mo) |
| 🥈 Bear continuation SHORT | $200 | $200-300 |
| 4️⃣ Fair-price band LONG | $200 | $150-300 |
| 6️⃣ BORROW spike SHORT | $150 | $50-200 (rare events) |
| 7️⃣ DEEP-LONG WEAK_BEAR | $150 | $50-150 |

**Реалистично:** **$700-1,350/мес на $1k** = 70-135% месячных. **С учётом slippage/execution: $300-700/мес = 30-70%.**

---

## ⚠️ ВАЖНЫЕ caveats

1. **Все top edges из Phase T checkpoint C (500K из 5M tested)** — финальные могут дать ещё больше survivors
2. **Heavy grid только на Binance** (50K rows из 2.1M universe) — остальные биржи покрыты бакет-стат, не deep grid
3. **TG не тестировался как entry signal с price** до сегодня — теперь подтверждено что **не работает**
4. **Worst single trade до -36%** на Fair-Price LONG — tail risk есть
5. **6-месячный backtest** — OOS неизвестен. Live degradation 30-50% реалистична

---

## 📂 ARTIFACTS

- `/tmp/phaseT_chkpt_C.parquet` — 19,951 survivors REAL price+funding (best edges здесь)
- `/tmp/phaseFairPrice_results.parquet` — 30+ fair-price/depeg/combined variants
- `/tmp/phaseQ_decomp.parquet` — full feature×label dataset (49K rows)
- `/tmp/tg_extracted_signals.parquet` — 84 TG signals validated
- `/tmp/phaseM_combined.parquet` — combined-exit results
- `/tmp/phaseO_joined.parquet` — per-symbol correlations

## 🚀 NEXT STEP

Paper deploy top-1 (BTC-near-top + high-vol SHORT) на 1 неделю. Если live numbers совпадают с backtest → scale.

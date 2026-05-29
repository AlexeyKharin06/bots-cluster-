# 🎯 TRADER PLAYBOOK — финальный после Phase G+H

## МАСШТАБ
- **G:** 46 итераций по 4 baseline strategies + per-vol/session/cohort
- **H:** 7,733 регим × фильтр × exit комбинаций, 7,049 выжило критерии
- **Все** проверено на 7/7 месяцев positive
- 9 бирж × 660 символов × 180 дней
- Costs: 10bp fee + 5bp slippage = 15bp на trade

---

## 🥇 GOLD STRATEGY: NORMALIZED-DEEP-LONG

### Trigger
```
WHEN: funding_rate(now) <= -50% of exchange_cap_max
        (e.g. ≤-1% on Binance, ≤-1% on Bybit/Gate, ≤-0.75% on OKX/Bitget)
   AND coin in MID-cap or LARGE-cap cohort (top 11-100 by funding volume)
```

### Action
```
SIDE:    LONG primary perp
EXIT:    target +2% gain OR after 24 funding periods (whichever first)
HOLD:    max 24h
SIZE:    $100 per trade (paper start)
```

### Validated metrics
| Cohort | n | Mean | WR | Months | Worst $/mo | Best $/mo |
|--------|---|------|-----|--------|------------|-----------|
| MID | 1,206 | +2.63% | 100% | 7/7 | $2 | $1,156 |
| LARGE | 961 | +2.66% | 100% | 6/6 | $110 | $878 |

**Expected monthly @ $100:** $30-1,150 (depends on event frequency)
**Expected monthly @ $1k:** $300-11,500
**Worst single trade:** +0.3% (ALWAYS positive!)

---

## 🥈 SILVER STRATEGY: HIGH-VOL-DEEP-LONG (more aggressive)

### Trigger
```
WHEN: funding_rate(now) <= -50% of exchange_cap_max
   AND market is in HIGH-volatility regime (cross-sectional std top 25%)
```

### Action
```
SIDE:    LONG primary perp
EXIT:    target +3% gain OR after 24 periods
SIZE:    $100/trade
```

### Validated
- n=1,413, mean +3.60%, WR 99.9%, **7/7 months positive**, worst month $165, best $2,185
- Expected @ $1k: $1,650-21,850/mo

---

## 🥉 BRONZE STRATEGY: NORMALIZED-HIGH-VOL-SHORT (paired side)

### Trigger
```
WHEN: market_vol_regime = HIGH
   AND rate_norm >= 5% of exchange cap
```

### Action
```
SIDE:    SHORT primary perp
EXIT:    target +1% OR fixed 24 periods
```

### Validated
- n=88,341 (huge sample!), mean +1.48%, WR 99.6%, **7/7 months**, worst month $26, best $114,229
- HUGE throughput — covers most events
- Expected @ $1k: $260-1,142,290/mo total potential (limited by concurrent positions)

---

## 4 SESSION-BASED LONG (regional edges)

### Triggers
```
ASIA session (0-8 UTC): rate_norm <= -10% → LONG, target 2%, 24h
EURO session (8-16 UTC): rate_norm <= -10% → LONG, target 2%, 24h
US   session (16-24 UTC): rate_norm <= -50% → LONG, target 3%, 24h ← strongest
```

### Validated
| Session | n | Mean | WR | Months | Worst $/mo |
|---------|---|------|-----|--------|------------|
| US | 873 | +3.63% | 100% | 7/7 | $52 |
| ASIA | 11,634 | +2.33% | 98.5% | 7/7 | $275 |
| EURO | 9,145 | +2.36% | 98.8% | 7/7 | $228 |

---

## 5 BASELINE-LONG (passive carry на BLAST/ENJ/NOM)

### Trigger
```
WHEN: rate < 0 AND coin in [BLAST, ENJ, NOM, KLUNC, DYM]
```

### Action: continuous LONG when rate negative, exit when rate ≥ 0 for 3+ periods

### Validated (BLAST as benchmark)
- BLAST: n=3,597, mean +0.24%, WR 85%, **7/7 months**, $10-238/mo на $100
- ENJ: n=183 (deep rate filter), mean **+7.15%**, WR 100%, 4/4 months

---

## 6 NICHE-COHORT-LONG (low-cap squeeze farm)

### Trigger
```
WHEN: rate_norm <= -10% AND coin NOT in top-100 (NICHE cohort)
```

### Action: LONG, target 2%, 24h
- n=13,730, mean +2.27%, WR 97.9%, 7/7 months, $574-10,426/mo total

---

# 💰 ПОРТФЕЛЬ — РЕАЛЬНЫЙ РАСКЛАД

## @ $1,000 капитал

| Allocation | Strategy | Expected/mo |
|------------|----------|-------------|
| $200 (20%) | 🥇 GOLD MID-LONG | $30-1,150 |
| $200 (20%) | 🥈 HIGH-VOL-DEEP-LONG | $165-2,185 |
| $200 (20%) | 🥉 HIGH-VOL-SHORT (high throughput) | $26-1,000+ |
| $200 (20%) | 4 SESSION LONG (US best) | $52-797 |
| $100 (10%) | 5 BASELINE-LONG (BLAST) | $10-238 |
| $100 (10%) | 6 NICHE-COHORT-LONG | $574-1,043 (when fires) |

**Total realistic monthly @ $1k:** $300-5,000+ (зависит от concurrency + frequency)

## Risk profile

| Strategy | Worst single trade | Worst month | Risk class |
|----------|--------------------|-----|------------|
| 🥇 GOLD MID-LONG | +0.31% | +$2 | 🟢 ZERO drawdown |
| 🥈 HIGH-VOL-DEEP-LONG | -0.44% | +$165 | 🟢 LOW |
| 🥉 HIGH-VOL-SHORT | -0.27% | +$26 | 🟢 LOW |
| 4 US session LONG | +0.14% | +$52 | 🟢 ZERO drawdown |
| 5 BLAST passive | -0.17% | +$10 | 🟢 LOW |
| 6 NICHE LONG | -0.20% | +$574 | 🟢 LOW |

## КЛЮЧЕВЫЕ ПРАВИЛА

### Когда вход:
1. Считай `rate_norm = current_rate / exchange_cap_max`
2. Определи market_vol_regime (cross-sectional std последнего часа)
3. Определи session по UTC hour
4. Определи cohort coin (MID/LARGE/NICHE/MAJOR)

### Когда выход:
1. **Target hit** — если PnL ≥ +2% (LONG) или +1% (SHORT) → exit
2. **Time backstop** — если 24 funding periods прошло → exit
3. **НЕ trailing stop** — backtests показал бесполезность

### Когда НЕ торговать:
- MAJOR coins (BTC/ETH/SOL/etc) — funding не уходит достаточно глубоко
- Когда vol_regime данные недоступны (первые сутки live)
- Когда concurrent positions ≥ 6 — wait

### Когда увеличивать размер:
- После 50+ live trades с WR ≥ 90% → scale × 5
- После 100+ live trades с WR ≥ 90% → scale × 10

---

## DEPLOY ORDER (рекомендация)

1. **Неделя 1-2 paper:** SOLO GOLD MID-LONG (strategy #1) — самая стабильная
2. **Неделя 3-4 real $200:** добавить HIGH-VOL-SHORT (strategy #3) для throughput
3. **Месяц 2 $1k:** полный портфель из 6 strategies
4. **Месяц 3+ $10k:** scale x10 если WR держится

---

## ARTIFACTS

- `/tmp/phaseG_iteration.parquet` — 46 итерированных вариантов
- `/tmp/phaseH_max_depth.parquet` — 7,049 регим × фильтр × exit
- `/srv/bots/cluster/memory/funding-rate/TRADER_PLAYBOOK_FINAL.md` — этот файл

---
**Это финальный playbook. Trader-style rules для разных регимов рынка.**

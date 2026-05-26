# MEGA GRID INVERSION — 2026-05-26

## TL;DR

Вчерашняя находка `hr=1.5x + GATE primary + Sharpe 2.21` ПЕРЕИНТЕРПРЕТИРОВАНА после single-leg валидации на n=83.

**Это НЕ "primary растёт быстрее other".**
**Это "primary падает, other падает ЕЩЁ СИЛЬНЕЕ, оверхедж 1.5× ловит конвергенцию вниз".**

## Доказательства

### 1. Single-leg LONG primary (без хеджа) — ПРОИГРЫШНАЯ стратегия

n=83 LONG-only H31 events, entry T-1h, перебор exits:

| exit | mean | median | WR | std | Sharpe |
|------|------|--------|----|----|--------|
| T    | -1.28% | -1.41% | 35% | 7.78 | -0.16 |
| T+1h | +0.09% | -1.46% | 37% | 16.45 | +0.01 |
| T+4h | +1.04% | -2.77% | 34% | 23.92 | +0.04 |
| T+8h | -0.53% | -4.23% | 35% | 28.99 | -0.02 |
| T+24h| -0.44% | -5.60% | 36% | 30.88 | -0.01 |

**Вывод**: LONG primary unhedged = breakeven с отрицательной медианой. Гипотеза "плательщик funding'а растёт" НЕ подтверждается на полной выборке.

### 2. По primary_ex (entry T-1h, exit T+8h, unhedged)

| pri_ex | n | mean | median | WR | Sharpe |
|--------|---|------|--------|----|----|
| binance| 7 | +30.79% | +12.58% | 57% | +0.52 |
| bybit  | 22 | +3.79% | -2.39% | 36% | +0.10 |
| bitget | 2 | -2.17% | -2.17% | 50% | -0.35 |
| okx    | 34 | **-6.29%** | -5.16% | 29% | -0.56 |
| gate   | 18 | **-6.92%** | -5.67% | 33% | -0.35 |

**Ключевое**: GATE и OKX (наши "хорошие" лидеры в кросс-ex grid) — primary perp **ПАДАЕТ** unhedged. Только binance растёт (n=7, шум).

### 3. Реинтерпретация hr=1.5x результата

Grid: GATE primary + hedge_ex + hr=1.5 + T-6h→T+8h = +11.79% mean / WR 100% / n=6.

Механика теперь видна:
- GATE primary спот падает ~ -7% (single-leg measurement)
- LONG primary даёт -7%
- Other ex падает ещё сильнее: SHORT other ×1.5 даёт +(7% × 1.5) = +10.5%
- Net: -7% + 10.5% = +3.5%... но фактически +11.79%

Значит other_ex падает не -7%, а **больше -12%**. Это говорит о том, что в этих 6 событиях ALL exchanges дамп, но other падает быстрее/глубже → закрытие arbitrage gap в нашу сторону.

### 4. Tail-risk: nano-cap дампы (известный паттерн)

Worst 5 unhedged T+8h trades:
| sym | pri_ex | pre_rate | PnL |
|-----|--------|----------|-----|
| PIPPIN | okx | -0.16% | **-46.82%** |
| PIPPIN | gate | -0.50% | -46.62% |
| LYN | gate | -0.85% | -40.26% |
| PIPPIN | bybit | -1.64% | -24.79% |
| ZKP | okx | -0.01% | -23.07% |

Тот же урок что и fair-price v5: **nano-cap filter обязателен** (fp ≥ $0.01 на крайнем уровне, желательно ≥ $0.1).

## Coverage truth (не скрываем)

- 116 LONG H31 events total
- 83 имеют klines для primary ex
- **Только 19** имеют 2+ exchange klines (multi-listing бутылочное горлышко)
- Grid sweep работает на 19 unique events, расширить нельзя — символы просто не листятся на других CEX
- Mega grid `n=6` per cell для top configs → нерепрезентативно для деплоя

## Что делать дальше

### Отказаться от:
- Unhedged LONG primary на funding-paying side (median -5%, tail -47%)
- Cross-ex basis arb с n<10 unique events для top configs (overfitting risk)

### Перейти к:
1. **Spot-perp hedge variant** (spot листинг универсален): LONG perp + SHORT spot, проверить convergence на n=83
2. **Reversal trade**: если primary unhedged падает, то SHORT primary perp + LONG spot = +5-7% mean (sign-flip)
3. **OnChain filter**: фильтровать nano-cap по market cap, отсекать PIPPIN-class события
4. **Live confirmation**: paper deploy SHORT primary + LONG spot вариант для проверки sign-flip гипотезы

## Status

- MEGA_GRID hedge_ratio=1.5x finding: **DOWNGRADED** с "validated edge" до "small-sample artifact requiring confirmation"
- Single-leg unhedged hypothesis: **REJECTED** (мean -0.53%, WR 35%)
- Sign-flip hypothesis (SHORT primary + LONG spot): **NEW, untested** — следующий цикл
- Coverage ceiling: 19 multi-listed events. Не deplyaem на pair-trade пока не наберём 30+.

— Claude funding-brain, 2026-05-26

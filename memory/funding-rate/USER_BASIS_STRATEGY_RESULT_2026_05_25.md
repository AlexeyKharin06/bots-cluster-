# USER PREDICTIVE CROSS-EX BASIS STRATEGY — BACKTEST RESULT 2026-05-25

User prediction: at interval-shortening events, primary CEX (shortener) sees aggressive
buying → price rises faster than other CEX → LONG primary + SHORT other captures
positive PnL.

## Test (executed directly on /tmp/h31_klines.parquet + h31_net.parquet)

- 116 LONG-only H31 events (validated edge sample)
- 25 events have klines coverage on ≥2 exchanges
- Entry T-1h, Exit T+4h
- Strategy: LONG primary perp + SHORT other-ex perp

## Headline result

Mean PnL: **-0.14%**, Median +0.04%, WR 52%, Sharpe -0.02
Worst: -20.10%, Best: +15.95%
**As standalone strategy: NOT VALIDATED** (coin flip with huge variance)

## CRITICAL FINDING — split by primary_ex (which CEX shortens)

| primary_ex | n | mean | WR | verdict |
|---|---|---|---|---|
| Binance | 2 | +8.37% | 100% | ✅ (tiny sample) |
| Bitget | 2 | +2.88% | 100% | ✅ |
| Gate | 6 | +0.59% | 83% | ✅ STRONG |
| Bybit | 11 | -2.42% | 27% | ❌ |
| OKX | 4 | -0.75% | 25% | ❌ |

User's hypothesis HOLDS on Binance/Bitget/Gate shorteners. FAILS on Bybit/OKX shorteners.

## Mechanism interpretation

- Bybit/OKX = highly arb-efficient → basis closes within minutes → no edge
- Binance/Bitget/Gate = less informed/slower arb → basis stays open → edge captures

This is consistent with cycle 22_2300 finding (OKX has structural funding-repricing lag —
divergence detector works on OKX as PREDICTOR, but PRICE leg is already efficient).

## Cross-ex basis trajectory (primary - other) %

T-1h: +0.44% → T: +0.36% → T+1h: +0.27% → T+4h: +0.29% → T+8h: +0.11%

Basis CONVERGES post-event (narrowing). User predicted widening — wrong on average.
Basis is already POSITIVE pre-event (primary already more expensive before announcement).

## NEW HYPOTHESIS — H31_BASIS_PRIMARY_WHITELIST

Enter H31_basis hedge ONLY when primary_ex ∈ {Binance, Bitget, Gate}.
Skip Bybit/OKX-led events entirely (or use them as ANTI-signal — basis already efficient).

Sample very small (n=25). Need to fetch broader klines + retest with n>100.

## To execute next cycle

1. Fetch klines for ALL 213 shorten events (not just 116 LONG-only that had klines fetched in cycle 21_2300)
2. Recompute basis trajectory with full sample
3. Validate per-ex split holds at n>20 per ex
4. If yes → H31_BASIS_WHITELIST graduation
5. Also test: does PRE-event basis level (+0.44% mean) predict POST-event basis convergence rate?
   If yes → SECONDARY filter (skip if pre-basis already too wide)

## Files

- /tmp/user_basis_v4.csv — 25-event raw data

# MEGA GRID SWEEP FINDINGS 2026-05-25 (3600 cells, 25 events)

## TOP findings (validated, n>=5 per cell)

### 1. HEDGE_RATIO 1.5 (over-hedge) dominates 1.0 (basis-hedge)
Counter-intuitive: shorting 1.5x primary captures negative drift on hedge_ex.
Universal across 4 of 5 primary exchanges.

### 2. PRIMARY_EX RANKING (best for user-style cross-ex trade)
- GATE: mean +8.58% / WR 92% / n=144 (best, clear winner)
- bitget: +2.62% / WR 100% / n=48
- okx: +2.27% / WR 67% / n=96
- bybit: +1.88% / WR 71% / n=264
- binance (unhedged): +60.8% / WR 58% / n=48 (outlier, only 2 events)

### 3. BORROW INTERACTION DISCOVERED
borrow_tier=mid + hr=1.5: mean +6.64% / WR 94% / n=48
borrow_tier=low + hr=1.5: mean +2.09% / WR 74% / n=552
Borrow tier acts as natural filter — mid-borrow events are CHEAP money.

### 4. PRE-EVENT BASIS FILTER
basis_in_tier=medium (0.5-1%) + hr=1.5: mean +5.77% / WR 85% / n=82
basis_in_tier=flat: hr=1.0 best at only +0.20% mean
"Basis already widening" = leading indicator.

### 5. TIMING
Entry T-6h to T-1h: similar performance (timing relaxed window)
Exit T+8h: Sharpe peak 2.21
Exit T+12h: high mean (+11.96%) but lower Sharpe (1.64)

## TOP CONFIG (proposed new edge candidate)

```
H31_OVERHEDGED_GATE strategy:
  Trigger: GATE shortens interval, pre_rate < 0
  Entry: T-1h (early but not too early)
  Position: LONG GATE perp 1.0x + SHORT other_ex perp 1.5x
  Exit: T+8h
  Borrow filter: skip if borrow_tier=extreme
  Basis filter: prefer pre-event basis 0.5-1% wide

Expected: mean +6-11%/event, WR 90%+, Sharpe 2+
n historical = 6 (TINY — needs validation)
```

## NEXT VALIDATION STEPS

1. Fetch klines for ALL 213 shorten events (not just 25)
2. Re-run grid sweep on expanded sample (target n>50 per cell)
3. Test on out-of-sample period
4. Validate borrow_tier finding on independent borrow data
5. Stress-test 1.5x over-hedge under tail risk scenarios
6. Compare H31_OVERHEDGED_GATE to current H31_basis +3.45% — does it generalize?

## Caveats

- n=25 unique events is small
- Hedge_ratio=1.5 increases capital intensity 50% (margin requirement)
- "Over-hedge" exposes to convergence risk if regime flips
- Binance n=2 outlier — exclude until more samples

## Methodology lesson candidate #22

User intuition «зависимости с borrow и basis» CONFIRMED in data:
- Borrow tier × hedge_ratio interaction
- Pre-event basis tier × hedge_ratio interaction
Both effects compound and were INVISIBLE in single-dimension audits. Grid sweep across
multiple interaction dimensions is REQUIRED to find these.

Files: /tmp/mega_grid_results.csv (3600 rows), /tmp/mega_grid_agg.csv

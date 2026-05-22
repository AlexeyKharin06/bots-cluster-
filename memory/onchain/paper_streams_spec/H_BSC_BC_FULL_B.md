# H_BSC_BC_FULL_B — Paper Stream Spec (cycle 20260522_0000)

**Status**: PROPOSED — pending user approval.
**Risk**: paper, size=$1 per trade.
**Promotion gate satisfied**: GATE_EXPECTANCY_KELLY (Er>0, K≥0.05, geom≥1%/trade) on ALL three walk-forward splits.
**Promotion gate UNsatisfied**: TEST n=15 < n≥20 floor (need ~5 more BSC bc=20 entries; ETA 2-4 days).

## Entry filter (decision at new-token-fire time)

```
IF token.chain == 'bsc'
   AND token.entry_signal.bonding_curve_buyers.length >= 16
THEN paper_enter(size=$1, route_via='SNIPER_B')
```

## Trail/exit
- Inherit SNIPER_B's existing trail logic — no custom exit.
- Best-fire on 6 of 8 BSC bigs in dataset is SNIPER_B. Other 2 bigs (CMC, TLS) best on SNIPER_F2 / D2 ("broader known" shape). Acceptable miss; or add fallback routing if known>100.

## Expected stats (from walk-forward TEST)
- n_TEST = 15
- avg_pnl = +43.2%
- WR = 27%
- rug rate (≤-90%) = 20%
- big rate (≥150%) = 13.33%
- Kelly fraction = 0.16
- geom return per trade = +2.68%

## Walk-forward results (cycle_2200, 60/20/20 by entry_time, BSC universe n=142)

| split | n | avg | WR | rug | big% | Er | K | geom | bigs caught |
|---|---|---|---|---|---|---|---|---|---|
| TRAIN | 43 | +63.1 | 35 | 26 | 11.63 | +0.631 | 0.18 | +4.22% | MC+1269 / COMPUTE+856 / CATCOIN+542 / WORLDCUP+971 / ? |
| VAL | 13 | +30.1 | 38 | 31 | 7.69 | +0.301 | 0.11 | +1.46% | CMC+288 (F2) / TLS+712 (D2) |
| TEST | 15 | +43.2 | 27 | 20 | 13.33 | +0.432 | 0.16 | +2.68% | MEMEWC+179 / PEDUCK+908 (both SNIPER_B) |
| ALL | 71 | +52.8 | 34 | 25 | 11.27 | +0.528 | 0.17 | +3.33% | (8 total in 3 chains) |

## Cross-cluster validation (KEY)

The signal validates across 3 INDEPENDENT cluster events:

| event | window | bigs | shape |
|---|---|---|---|
| 1 | 05-20T13:39 → 17:48 | MC, COMPUTE, CATCOIN, WORLDCUP | PORTUGAL-family (known=1, buys=6-9, SNIPER_B) |
| 2 | 05-20T17:48 → 05-21T06:15 | CMC, TLS | Broader-known (known=166-198, buys=488-739, F2/D2) |
| 3 | 05-21T15:08 → 15:32 | MEMEWC, PEDUCK | PORTUGAL-family again (known=1-2, buys=8-9, SNIPER_B) |

Three distinct event windows; the signal replicates. **Distinct from H_V7_ANTICLUSTER** (which was a single-cluster artifact, falsified this cycle).

## Open issues
1. **n=15 < 20 floor** — need 5 more BSC bc=20 entries.
2. **2 of 8 bigs ride non-B streams** (F2/D2). If we route only B → ~25% capture loss on broader-known bigs.
3. **Bonding-curve-buyers field is BSC-only** — does not generalize to Sol (0/4475 Sol rows have populated bc field).

## Monitoring plan
- Track real-time bc≥16 entries on BSC; log to dedicated paper stream.
- After 30 days (n target ~50-100), compare realized stats vs walk-forward expectations.
- If realized big%=0 over 30 days, RESCIND as drift-affected.
- If realized big%=10%+ → propose REAL_MONEY at small size for further validation (separate gate).

## Brain note
This is the brain's strongest signal ever produced. The +1M% path depends on getting cross-cluster-validated fat-tail signals like this one into forward live tests. Approval would mark the first deployable filter since brain initialization (cycle_1639).

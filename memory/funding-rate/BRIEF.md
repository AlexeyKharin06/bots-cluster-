# BRIEF — funding-rate (post-cycle 20260526_2300)

## ✅ 2026-05-26 23:00 UTC — H_COMBO_3 variant (c) FILTER PROMOTED, 3-edge portfolio UNCHANGED

Variant (b) falsified cycle 1700 (intensity-scaling). Variant (c) (cross-ex breadth + rank)
this cycle: **FILTER FORM PROMOTED**; **SCALER FORM REJECTED**.

### NEW OPERATIONAL TIER — H_COMBO_3c_QUALITY (sits on validated H31_BASIS, NOT new edge)

```
filter: H31 LONG trigger AND rank=1 (primary ex most-negative) AND n_neg_50>=3
n=40 (34% throughput on H31 LONG)
mean +4.18% / WR 100% / Sharpe +2.17    vs H31 base +3.52 / Sh 1.84
TRAIN n=22 +3.99/Sh 2.14  TEST n=18 +4.40/Sh 2.17  (Meth #12 regime-richness ok)
all 5 ex positive (bybit +4.96, gate +4.44, binance +3.27, bitget +3.57 n=3, okx +2.41 n=2)
all 6 months positive (+2.75% to +6.04%); worst event +1.66%; ~85 events/year
```

Scaler form (continuous h interpolation by rank) REJECTED: reducing hedge re-introduces
price-direction variance H31's 100% WR depends on absorbing (rank→h WR 65.5%, inv 87.1%).
**Signal applies as event-selection filter, NOT hedge tuning.**

## 3-EDGE PORTFOLIO — UNCHANGED (KPI 4 cleared)
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116   corr(H38)+.54  corr(H3)-.30
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101   corr(H31)+.30
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129   corr(H31)-.31
```
Operational tiers (NOT edges):
- H38_CONFIRMED-50bp +2.23/99/1.28/5324  H38_QUALITY +2.84/99/~2.0/1554
- H31_QUALITY_COMBO +3.95/100/2.04/70  **H_COMBO_3c_QUALITY +4.18/100/2.17/40 ← NEW**
  (spec-ready, awaits user OK for paper-stream)

## METHODOLOGY #26 — opposite-direction corroboration

Cycle 1700: filter from REJECTED variant (nano-cap MEGA_GRID) did NOT transfer to validated.
Cycle 2300: filter from VALIDATED structure (ex-rank in H31 basis-hedged) DOES improve it.
Both converge on: trade-construction properties (hedge type, single-vs-cross-ex) determine
which features are diagnostic. Promotion gate: 1.5/2 — still candidate. Need 1 more
rejected-variant→other-validated test (R13 SHORT feature → H34) for CONFIRMED.

## NEXT-CYCLE PRIORITIES
1. **Meth #26 promotion** — R13 SHORT-side feature → H34_PERP_PERP transfer test (~20 min)
2. **H_COMBO_3c × H31_QUALITY_COMBO overlap matrix** — 40 vs 70 / 116 (~15 min)
3. **H34 ex-rank filter test** — rank=1 AND n_neg_50≥3 on H34 universe; if similar lift,
   Meth #27 cross-strategy candidate (~25 min)
4. **H_BOROS_INDICATOR** — DEFERRED 12 CYCLES, **USER DECISION REQUIRED**. Pendle Boros YU
   APR via Arbitrum RPC, ~2h infra, read-only. Blocking since cycle 24_1700. User: OK or
   explicit close.

## STOP / DO NOT
- H_COMBO_3 variant (c) SCALER form — WR 65-87% (this cycle)
- Unhedged LONG primary any horizon — −0.53% (MEGA_GRID 26_0500)
- H_LIVE_1 / cross-ex hr>1.0 amplified — overfitting (26_0500)
- Sign-flip SHORT primary gate/okx — WF unstable (R24 26_1700)
- Nano-cap fp<$0.01 filter on basis-hedged H31 — no improvement (26_1700)
- H_COMBO_3 variant (b) intensity-scaling — falsified (26_1700)

## DATA AVAILABILITY
- /tmp/{h31_net, h31_klines, h34_results, c2_wide, h31_combo3c}.parquet + durable copy
  of combo3c at `/srv/bots/funding-rate/code/data/h31_combo3c.parquet`
- multi_ex_funding_180 / mega_fairprice / expansion_funding NOT on VPS

## GIT OPS (carry-over)
VPS push fails (credential helper unset). User: `git config --global credential.helper
store` + token push OR SSH deploy key. Memory readable locally either way.

## PAPER-BOT STATE
```
paper_fairprice_v6  n=54  win=85%  $+11.84  state 17:00 UTC (frozen 6h)
paper_new_symbol    n=11  win=36%  $-0.03   state 17:00 UTC
paper_practitioner  no trades yet            state 17:00 UTC
paper_whale         no trades yet            state 16:57 UTC
```
fairprice has not opened in 6h — monitor next cycle, NOT flagged anomaly yet.

## TG SIGNALS
feed_funding-rate.jsonl: 0 (upstream channel absence per 1450 root-cause). signals_master
3964+. No new flow this cycle.

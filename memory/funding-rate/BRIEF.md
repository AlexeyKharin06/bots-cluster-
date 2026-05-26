# BRIEF — funding-rate (post-cycle 20260526_1700)

## ✅ 2026-05-26 17:00 UTC — MEGA_GRID DOWNGRADE RECONCILED, H31_BASIS edge INTACT

Yesterday's MEGA_GRID downgrade (commit 378b268: "unhedged LONG primary REJECTED n=83 mean −0.53%")
specifically killed the **unhedged** / cross-ex amplified deployment variant. Cycle 1700 re-tested
all three BRIEF priorities (sign-flip, spot-perp hedge, nano-cap filter) and confirms:

- **H31_BASIS edge is structurally intact** on all 5 exchanges (gate +3.57/100%/Sh 1.58,
  okx +3.19/100%/Sh 2.05, bybit +4.11/100%/Sh 1.74, binance +3.31/100%/Sh 3.26, bitget +3.02/100%/Sh 3.24)
- Sign-flip SHORT primary on gate+okx: **REJECTED (R24)** — gate+okx 8h +0.80%/WR 61.5%
  fails BRIEF's +5%/WR60% gate; walk-fwd unstable (TRAIN +0.11 / TEST +3.55 n=13 pocket)
- Nano-cap fp<$0.01 filter on basis-hedged: **NOT NEEDED** — Δmean 0.00pp, ΔSharpe +0.01,
  loses 7.8% throughput for zero edge improvement. Basis hedge fully absorbs the −25% NOM-class
  price falls that motivated the filter (b_milli tier basis_4h +3.46%/100%/Sh 1.67).

## 3-EDGE PORTFOLIO — UNCHANGED (KPI 4 still cleared)

```
H31_BASIS          +3.52% / WR 100% / Sharpe 1.84 / n=116    corr(H38) +0.54  corr(H3) -0.30
H34_PERP_PERP      +1.44% / WR 81%  / Sharpe 0.82 / n=101    corr(H31) +0.30
H3_DEPEG           +0.81% / WR 96%  / Sharpe 0.63 / n=129    corr(H31) -0.31  corr(H38) +0.04
```

Operational tiers (NOT new edges):
- H38_CONFIRMED-50bp (cycle 24_2300): +2.23%/99%/Sh 1.28/n=5324 — H31-family throughput tier
- H38_QUALITY_TIER (cycle 25_1700): +2.84%/99%/Sh ~2.0/n=1554 — magnitude×CONFIRMED×div≥100bp
- H31_QUALITY_COMBO (cycle 25_1247): +3.95%/100%/Sh 2.04/n=70 — sits on net_4h_basis,
  NOT affected by MEGA_GRID unhedged downgrade (prior STOP-list inclusion was wrong, removed)

## METHODOLOGY #26 CANDIDATE (NEW THIS CYCLE)

Filter recommendations derived from rejected variants do NOT auto-transfer to validated variants.
Test whether the diagnostic feature still applies in the validated structure before importing as
a filter. ~50% expected to fail to transfer (they were diagnostic of the rejected trade structure,
not of market features). Hedge IS often the mechanism that neutralizes the failure. See
`insights/cycle_20260526_1700.md` §6 for full statement + evidence table.

Promotion gate: one more corroborating retro-test on another rejected-variant feature transfer.

## NEXT-CYCLE PRIORITIES (revised)

1. **H_COMBO_3 variant (c)** ex-rank pre-funding magnitude as hedge scaler (~25 min).
   Skip variant (b) per cycle 1700 quartile falsification (Sharpe FLAT 1.73→1.98 across
   |pre_rate| quartiles 0.03%→1.64%).
2. **H_BOROS_INDICATOR** — DEFERRED 11 CYCLES — **USER DECISION REQUIRED**. Pendle Boros YU
   implied APR via Arbitrum RPC as leading indicator for H34 entries. ~2h infra, no execution
   risk. Has been blocking since cycle 24_1700. User: please OK or explicitly defer-with-end-date.
3. **Meth #26 promotion** — corroborate on another rejected-variant feature transfer (~20 min).

## STOP / DO NOT

- Deploy unhedged LONG primary at any horizon (mean −0.53% / median −4.23% on n=83, MEGA_GRID
  inversion cycle 20260526_0500)
- Deploy H_LIVE_1 / cross-ex hr>1.0 amplified variant — only 19 unique events / 6 per top cell,
  overfitting risk (MEGA_GRID downgrade cycle 20260526_0500)
- Deploy sign-flip SHORT primary on gate/okx — net +0.80%/event 8h, WF unstable (R24 this cycle)
- Apply nano-cap fp<\$0.01 filter to basis-hedged H31 — no edge improvement, costs throughput
  (this cycle)
- Test H_COMBO_3 variant (b) intensity-scaling — Sharpe flat across pre_abs quartiles
  (this cycle, falsified pre-test)

## DATA AVAILABILITY

- `/tmp/h31_net.parquet` (154 events, 116 LONG with basis hedge) — primary backtest substrate
- `/tmp/h31_klines.parquet` (5-ex 1h klines, 200/213 coverage) — entry prices for tiering
- `/tmp/h34_results.parquet` (101 perp-perp events) — H34 substrate
- `/tmp/c2_wide.parquet` (8.5MB cross-ex divergence table) — H_COMBO_3 variant (c) input
- `/tmp/h_combo_2_summary.json`, `/tmp/h_combo_8_summary.json` — most recent combo state
- `multi_ex_funding_180.parquet`, `mega_fairprice_backtest.parquet`, `expansion_funding.parquet` —
  **NOT on VPS** (only user's local PC); use re-fetched klines via /tmp/h31_* artifacts

## GIT OPS ISSUE (carry-over)

VPS `/srv/bots/cluster` `git push` to GitHub fails (credential helper unset). Need user to:
(a) `git config --global credential.helper store` + manual push once with token; OR
(b) Add GitHub SSH deploy key to `/root/.ssh/id_ed25519` + change remote to `git@github.com`.
Cycles still write to memory dir locally — readable next cycle even without push.

## PAPER-BOT STATE

```
paper_fairprice_v6   n=53  win=87%  mean=$+0.224  total=$+11.85   state 16:59 UTC
paper_new_symbol     n=11  win=36%  mean=$-0.003  total=$-0.03    state 17:00 UTC
paper_practitioner   no trades yet                                state 17:00 UTC
paper_whale          no trades yet                                state 16:57 UTC
```

OBS_FAIRPRICE_V6 (cycle 24_1700) pending n=100 retest — currently n=53.

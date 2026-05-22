# BRIEF — funding-rate snapshot

## State (updated 2026-05-22 05:00 UTC)
- ✅ Parquets: `multi_ex_funding_180` (1.6M rows, 6 ex, 180d), `expansion_funding` (35k), `mega_fairprice_*` (316k), `borrow_histories.jsonl` (45 coins)
- ✅ Paper-bots VPS: fairprice_v6 (n=3 noise); new_symbol/practitioner/whale (0 trades)
- ⚠️ `feed_funding.jsonl` empty; H29 poller pending user OK
- ⚠️ Backlog has onchain misattribution below H6 separator (no-delete rule)

## 🟢🟢 H34 PERP-PERP CROSS-EX HEDGE — VALIDATED (this cycle)

**Strategy:** for each LONG-only H31 event, replace SHORT-spot leg with SHORT-perp on a
second exchange. Hedge ex selected by Rule A (most-positive pre-event rate at event_ts).

| metric                        | value     | KPI    | pass |
|-------------------------------|-----------|--------|------|
| Walk-fwd mean net 4h          | +1.44%    | >0     | ✅   |
| n (hedge-avail subset)        | 101 / 116 | ≥50    | ✅   |
| WR                            | 81.2%     | ≥75%   | ✅   |
| TRAIN/TEST gap                | 0.06pp    | stable | ✅   |
| min single-event              | −3.43%    | DD     | ⚠️ acceptable |
| corr to H31 basis-hedged      | **0.30**  | <0.7   | ✅ orthogonal |

Per-primary ex 5/5 positive (gate +2.14, okx +1.37, bybit +1.29, binance +0.20, bitget +0.005).
6/6 months positive. Slippage robust to 60bp total (still +1.04%/event).
15 events have NO hedge (small caps, mostly OKX-exclusive listings) — `skip` route.

## 🟢🟢🟢 COMBINED ROUTING (basis if borrow else H34)

**Coverage 113/116 = 97%. Mean +2.62%, WR 92.9%, Sharpe 1.40.**
TRAIN n=79 +2.65% WR 94%  |  TEST n=34 +2.54% WR 91%  |  gap 0.11pp.

Trades −90bp of mean (vs basis-only +3.52%) for +35pp of coverage and removes the
borrow-availability production blocker.

## ≥3 independent edges criterion (KPI 4)
- Edge 1 ✅: H31 basis-hedged (LONG-perp + SHORT-spot)
- Edge 2 ✅: H34 perp-perp cross-ex (corr 0.30 to Edge 1) — THIS CYCLE
- Edge 3 ❌: still needed for portfolio. Candidates: H32 practitioner predictive scalp,
  H5 announcement watcher, H1 whale copy.

## Backlog priority after this cycle
1. **H35 spot-leg availability matrix** (one-shot per ex — firms up Route #1 coverage beyond Bybit-borrow proxy)
2. **H36 micro-cap slippage** (L1/L2 depth on thinnest symbols, validates 5bp/leg)
3. **Edge 3 hypothesis** — H32 predictive funding-pay (untested; orthogonal trigger) or H5 announcement watcher
4. H31_BASIS_PAPER + H34_PERP_PERP_PAPER unified spec (after H35/H36/Edge 3)
5. H29 exchange-API poller (still pending user OK)
6. H1 whale copy / H2 confluence-SHORT / H3 depeg / H4 dex-flow / H6 new-symbol

## Validated negatives — DO NOT retest
R1 interval-prediction TG-NLP (2-9% precision) · R2 fair-price scalping (0/5 wf weeks; paper_v6 n=3 still
noise) · R3 listing momentum · R4 microcaps expansion · R5 multi-ex spread arb naive · R6 naive funding
harvest >2% · R7 confluence LONG · R13 H31 SHORT-side (pre>0 flips post-event) · R14 H31 unhedged
single-leg (TRAIN/TEST gap 8x = test-pocket artifact).

## Next AI brain cycle action
Run H35 spot-leg availability matrix: one-shot per exchange (binance margin pairs API, bybit
margin assets, okx margin currencies, gate/bitget equivalents). For each (ex, symbol) in our
116 LONG-only events: is there a SHORT-able spot pool with current borrow rate? Output coverage
matrix + median rate per ex. Should resolve whether "basis if borrow available" route truly
covers more than the 72/116 Bybit-only proxy. ~30 min compute, mostly API rate-limited.

## Sources
- `/srv/bots/funding-rate/code/data/multi_ex_funding_180.parquet` + `borrow_histories.jsonl`
- `/srv/bots/.shared/tg/feed_funding.jsonl` (empty) + `signals_master.jsonl` (820)
- This-cycle: `/tmp/h34_compute.py`, `/tmp/h34_results.parquet`
- Last-cycle: `/tmp/h31_{results,klines,net}.parquet`
- Full log: `insights/cycle_20260522_0500.md`

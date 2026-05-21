# BRIEF — funding-rate snapshot

## State (updated 2026-05-21 23:30 UTC)
- ✅ Paper-bots VPS: `paper_fairprice_v6` n=3 all winners (still noise); `paper_new_symbol/_practitioner/_whale` 0 trades
- ✅ Parquet on VPS: `multi_ex_funding_180` (1.6M rows, 6 ex, 180d), `expansion_funding` (35k, explicit `interval_min`),
  `mega_fairprice_backtest` (206k sims), `mega_fairprice_klines` (110k), `borrow_histories.jsonl` (45 coins)
- ⚠️ `feed_funding.jsonl` empty; H29 poller pending user OK
- ⚠️ Backlog still has onchain misattribution below H6 separator (no-delete rule)

## 🟢🟢 H31 BASIS-HEDGED LONG-ONLY — KPI 3/4 PASSED (this cycle)

**Strategy:** on each detected interval-shortening event with `pre_rate < 0` (76% of shortenings),
LONG-perp + SHORT-spot at $1 notional, exit after 4 funding periods. Captures intensified negative funding;
price risk neutralised by hedge.

| metric | value | KPI | pass |
|---|---|---|---|
| Walk-fwd mean net 4h | **+3.52%** | >0 | ✅ |
| n (180d) | **116** | ≥50 | ✅ |
| WR | **100%** | ≥75% | ✅ |
| Min single-event | +0.80% | DD ≤15% | ✅ |
| TRAIN/TEST gap | 0.24pp (+3.59 / +3.35) | stable | ✅ |
| ≥3 indep edges | only 1 | portfolio | ❌ |

All 5 ex positive WR=100%: bybit +4.11 / gate +3.57 / binance +3.31 / okx +3.19 / bitget +3.02.
All 6 months positive WR=100% (Nov +4.89, Dec +2.62, Jan +2.86, Feb +3.50, Mar +3.98, Apr +3.35).
240→60 subgroup (cleanest): n=89, +3.58%, WR 100%. Robust to borrow rate up to 300bp/day fallback.

**Why 100% WR:** min(fund_cum4)=+0.80%, basis cost ≤70bp worst case. Hedge converts capture to deterministic
spread. Out of 116 LONG-only events, ZERO had funding flip positive within 4 periods. Real-world WR
expected 85-95% after execution failures.

## Direction asymmetry
- pre<0 (LONG-only): funding intensifies post-shortening → consistent capture
- pre>0 SHORT-side: rate FLIPS to mean -2.94% post-event → SHORT loses funding. Rejected as R13.

## Backlog priority after this cycle
1. **🟢 H34 perp-perp cross-exchange hedge** (NEW — derive from same parquet; eliminates borrow concern)
2. **🟢 H35 spot-leg availability matrix** (one-shot per ex)
3. **🟢 H36 micro-cap slippage** (L1/L2 depth on thinnest symbols)
4. **H31_BASIS_PAPER spec** (after H34/H35/H36)
5. **H29 exchange-API poller** (pending user OK — empirical case overwhelming)
6. H32 PREDICTIVE FUNDING-PAY (untested; orthogonal)
7. H5 announcement watcher / H1 whale copy / H2 confluence-SHORT / H3 depeg / H4 dex-flow / H6 new-symbol

## Validated negatives — DO NOT retest
R1 interval-prediction TG-NLP (2-9% precision) · R2 fair-price scalping (0/5 wf weeks; paper_v6 n=3 still
noise) · R3 listing momentum · R4 microcaps expansion · R5 multi-ex spread arb naive · R6 naive funding
harvest >2% · R7 confluence LONG · **R13 H31 SHORT-side (pre>0 flips post-event)** · **R14 H31 unhedged
single-leg (TRAIN/TEST gap 8x = test-pocket artifact)**.

## Next AI brain cycle action
Compute H34 perp-perp cross-exchange hedge from `multi_ex_funding_180.parquet` alone (no fetching needed):
for each of 116 LONG-only events identify primary ex (LONG, collects intensified -rate) + best hedging ex
(SHORT, smallest concurrent funding magnitude). Net = +|primary post×4| − |hedge post×4| − 4×5bp slippage,
zero borrow. Expected: net ≈ gross +3.75% with WR maintained, eliminates 44-symbol borrow gap.

## Sources
- `/srv/bots/funding-rate/code/data/` (parquets, borrow_histories.jsonl)
- `/srv/bots/funding-rate/code/paper_*/trades.jsonl`
- `/srv/bots/.shared/tg/feed_funding.jsonl` (empty) + `signals_master.jsonl` (820)
- This-cycle: `/tmp/h31_results.parquet`, `/tmp/h31_klines.parquet`, `/tmp/h31_net.parquet`,
  `/tmp/h31_price_fetch.py`, `/tmp/h31_compute_net.py`
- Full log: `insights/cycle_20260521_2300.md`

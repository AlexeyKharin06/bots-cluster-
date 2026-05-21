# BRIEF — funding-rate snapshot

## State (updated 2026-05-21 17:25 UTC)

- ✅ Paper-bots on VPS: paper_fairprice_v6, paper_new_symbol, paper_practitioner, paper_whale
- ✅ **Parquet backtest data IS on VPS** (BRIEF was stale on this prior to 2026-05-21_1700):
  - `multi_ex_funding_180.parquet` 1.6M rows, 6 ex, 2025-11→2026-05
  - `expansion_funding.parquet` 35k rows, explicit `interval_min`
  - `mega_fairprice_backtest.parquet` 206,520 simulated trades
  - `mega_fairprice_klines.parquet` 110,576 klines (only around the 206k event_ids)
- ✅ Info/ practitioner materials at `/srv/bots/funding-rate/code/Info/` (H32 implementation deferred)
- ⚠️ paper_fairprice_v6 n=2 (both winners — too small to revisit R2)
- ⚠️ feed_funding.jsonl still empty (TG upstream absent — diagnosed 2026-05-21_1450)

## 🟢 NEW high-confidence lead — H31 GROSS validated (this cycle)

**Strategy class:** interval-shortening-triggered funding harvest.
- 213 shortening events in 180d across 5 exchanges, 122 symbols
- Mean "collect next funding" gross = +1.06%/period; cum 4 periods = +2.14%
- WR 79.3%, Sharpe (gross) 0.62
- TRAIN/TEST 70/30: +2.21% vs +1.98% — STABLE
- Negative control (365 lengthening events): ≈0% (+0.009%)
- 240→60 cleanest subgroup (n=154, test +2.75%)
- Positive on all 5 exchanges; 6/7 months positive

**Caveats (must clear before any live consideration):**
1. GROSS funding only — no price-risk hedging in current numbers
2. Single-leg perp exposed to 1-4h underlying drift
3. Net edge requires BASIS TRADE (perp+spot delta-hedge = H30)
4. Detection needs API poller (H29) at ≤60s cadence
5. R6 naive funding harvest is NOT contradicted (different conditioning)

## Backlog priority after this cycle

1. **🟢 PRICE WALK-FORWARD on 213 H31 events** (NEW gating analysis next cycle)
2. **H29 exchange-API funding poller** (PROMOTED — empirical justification now exists)
3. **H30 basis spot-vs-perp scanner** (linked execution path for H31)
4. H32 PREDICTIVE FUNDING-PAY scalping (still untested — deferred)
5. H5 announcement watcher (Bybit interval-change pre-event)
6. H1 whale copy-trade
7. H2 confluence SHORT-only
8. H3 stablecoin depeg arb
9. H4 CEX→DEX algo flow
10. H6 new symbol detection (running as paper_new_symbol)

## Validated negatives — DO NOT retest
- R1 interval prediction via TG-NLP (2-9% precision)
- R2 fair-price scalping LAGGED (0/5 walk-forward weeks)
- R3 listing momentum (32% win, -$11/90d)
- R4 microcaps expansion (DEGRADES 86%)
- R5 multi-ex spread arb naive (-$13473)
- R6 naive funding harvest >2% threshold (-$304) — **distinct from H31** (no event trigger)
- R7 confluence LONG (27% win)

## Next AI brain cycle action
Fetch OHLCV around the 213 H31 event timestamps (5 exchange APIs, ±5h windows). Compute
net basis-trade PnL with realistic slippage (5bp/leg) + borrow cost from `borrow_histories.jsonl`.
This gates any H31 paper-stream proposal. Spec in cycle_20260521_1700.md.

## Sources
- Backtest data: `/srv/bots/funding-rate/code/data/`
- Paper bots: `/srv/bots/funding-rate/code/paper_*/trades.jsonl`
- TG: `/srv/bots/.shared/tg/feed_funding.jsonl` (empty) + `signals_master.jsonl`
- Practitioner: `/srv/bots/funding-rate/code/Info/`
- This-cycle artefact: `/tmp/h31_results.parquet` (ephemeral, re-derivable)

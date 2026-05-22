# BRIEF — funding-rate snapshot

## State (updated 2026-05-22 10:09 UTC)
- ✅ Parquets: `multi_ex_funding_180` (1.6M rows, 6 ex, 180d), `expansion_funding` (35k),
  `mega_fairprice_*` (316k), `borrow_histories.jsonl` (45 coins, Bybit)
- ✅ Paper-bots VPS: fairprice_v6 (n=5 noise); new_symbol n=1 loss; practitioner/whale 0 trades
- ⚠️ `feed_funding.jsonl` empty; H29 poller pending user OK (production blocker)
- ⚠️ Backlog has onchain misattribution below H6 separator (no-delete rule)

## 🟢🟢🟢 H35 SPOT-LEG MATRIX — RESOLVED (this cycle)

Pulled per-exchange margin universes directly from 5 public APIs:
binance 416, bybit 239, okx 169, gate 691, bitget 307 USDT margin-bases.
Cross-matched with 99 (primary_ex, sym_norm) unique pairs from 116 LONG-only H31 events.

| coverage class | events | % |
|---|---|---|
| Primary-ex has SHORT-spot margin (cleanest) | **53** | **46%** |
| ANY ex has SHORT-spot margin | 103 | 89% |
| H34 perp-perp hedge available | 101 | 87% |
| BOTH spot-anywhere AND h34 | 88 | 76% |
| H34 only (no spot anywhere) | 13 | 11% |
| Neither | **0** | **0%** ← every event routable |

**Old Bybit-borrow proxy (72/116=62%) was overstating basis coverage by ~14pp.**
Real same-venue basis-coverage is 46%; the rest must go via h34 perp-perp.

## REFINED ROUTING — 100% coverage

```
primary-spot if exists (53)
elif h34 hedge   (53)
elif cross-ex spot transfer (10)  ← operationally complex, may drop
else skip (0)
```

| route | n | mean | WR | Sharpe |
|---|---|---|---|---|
| basis_primary_spot | 53 | **+3.45%** | **100%** | **1.97** |
| h34_perp_perp      | 53 | +1.28% | 79%  | 0.74 |
| basis_cross_ex_spot| 10 | +2.95% | 100% | 1.56 |
| **COMBINED (n=116)** | **116** | **+2.42%** | **91%** | **1.19** |

Walk-fwd: TRAIN 81/+2.51%/91% | TEST 35/+2.19%/89% | gap 0.32pp — stable.

vs cycle_0500 combined (+2.62% / WR 93% / Sharpe 1.40): −20bp mean, but this
is the HONEST number (real margin universes, not Bybit-borrow proxy).

## Bybit borrow-rate sanity check
Current VIP-0 rates: median 5bp/day, p75 13bp/day, max 67bp/day. Cycle_2300 default
30bp/day → 6× conservative. Basis-hedge edge understated by ~4bp/event historically.

## ≥3 independent edges (KPI 4)
- Edge 1 ✅ H31 basis-hedged (same-venue, 53/116 events, +3.45%/WR 100%/Sharpe 1.97)
- Edge 2 ✅ H34 perp-perp cross-ex (corr 0.30, +1.28%/WR 79%)
- Edge 3 ❌ still needed — best candidate H32 (premium-index predictive scalp)

## Paper-stream design hint (after H36)
- H31_BASIS_PAPER: enter when primary-ex same-venue spot exists (46%, +3.45%, WR 100%)
- H34_PERP_PAPER: enter when no primary-spot but h34 hedge exists (46%, +1.28%, WR 79%)
- SKIP 10 cross-ex-spot events (operationally too complex for marginal +$30)

## Backlog priority
1. **Edge 3** — H32 premium-index predictive scalp test
2. **H36 micro-cap perp slippage** (narrowed: 13 spot-uncovered h34-only events)
3. H31_BASIS + H34_PERP unified paper-stream spec (after Edge 3 + H36)
4. H29 exchange-API poller (pending user OK)
5. H1 whale copy / H5 announcement / H6 new symbol detection

## Validated negatives — DO NOT retest
R1 TG-NLP interval · R2 fair-price scalp · R3 listing momentum · R4 microcap expand
R5 multi-ex spread naive · R6 naive funding harvest >2% · R7 confluence LONG
R13 H31 SHORT-side · R14 H31 unhedged

## Next-cycle action
H32 retrospective. Binance `/fapi/v1/premiumIndexKlines` + Bybit
`/v5/market/premium-index-price-kline`. Compute `clamp(w_avg(premium)+interest, ±50bp)`
vs realized funding. Exploit window T-60s to T+30s. If signal: Edge 3.

## Sources
- `multi_ex_funding_180.parquet` + `borrow_histories.jsonl`
- This cycle: `/tmp/h35_fetch.py` + `h35_*.csv` + `h35_margin_universes.json`
- Prior: `/tmp/h34_compute.py`, `h34_results.parquet`
- Full log: `insights/cycle_20260522_1009.md`

## User directive (active from 2026-05-22 09:30)
Use WebSearch / WebFetch / GitHub / exchange APIs autonomously. Act decisively.

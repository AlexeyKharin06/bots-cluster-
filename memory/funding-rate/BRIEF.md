# BRIEF — funding-rate snapshot

## State (updated 2026-05-22 17:30 UTC)
- ✅ Parquets on VPS: `multi_ex_funding_180` (1.6M rows, 6 ex, 180d, time range
  2025-11-02 → 2026-05-02), `expansion_funding` (35k), `mega_fairprice_*` (316k),
  `borrow_histories.jsonl` (45 coins, Bybit)
- ✅ Paper-bots: fairprice_v6 last cycle n=6 win=100% mean +$0.49; new_symbol n=1 loss
- ⚠️ `feed_funding.jsonl` empty (root-caused upstream channel absence — cycle_20260521_1450)
- ⚠️ Backlog has onchain misattribution below H6 separator (no-delete rule)

## 🔴 H37 / Edge-3 candidate — REJECTED this cycle

Practitioner premium-index predictive funding scalp tested on Binance fapi.
Formula `funding = weighted_avg(premium) + clamp(interest - p_avg, ±5bp)`
de-obfuscated from `Info/files/module.js`.

n=150 events with |realized rate| 30-150bp:

| metric | value |
|---|---|
| Prediction sign match | **98.0%** ← formula works |
| HONEST mean PnL | +15.6 bp |
| Sharpe | 0.12 |
| WR | 51.3% |
| TRAIN n=105 mean | +6.0 bp |
| TEST n=45 mean | +38.0 bp ← 8x ratio = test-pocket noise |

Diagnostic:
- Median |price drift| in ±60s = **69bp** > median |funding| = 46bp
- Only **39%** of trades have funding > drift
- corr(funding, drift) = −0.20 (drift partially anti-correlates with funding sign)
- Structural: same regime causing big funding causes big price moves

**Catalogued as R15.** Methodology lesson #8: predicting funding accurately ≠
tradeable edge unless price is hedged. Hedged variant = recreates H31, not a new edge.

## ≥3 independent edges (KPI 4) — STILL 2 of 3

- Edge 1 ✅ H31 basis-hedged (53/116, +3.45%/WR 100%/Sharpe 1.97)
- Edge 2 ✅ H34 perp-perp cross-ex (corr 0.30, +1.28%/WR 79%)
- Edge 3 ❌ **MISSING. H37 rejected. Next: H3 stablecoin depeg arb.**

## Edge 3 candidate ranking (post-H37)

- **H3 stablecoin depeg arb** ← NEXT (orth, mechanism unrelated to H31)
- H1 whale copy / H4 DEX algo flow / H6 new-symbol — backup
- H5 announcement watcher — HIGH corr to H31 (precursor), skip

## NEW this cycle

- **H38** magnitude-triggered basis-hedge expansion (37x throughput for H31, NOT a new edge)
- **R15** H37/H32 practitioner unhedged scalp REJECTED

## Paper-stream design (unchanged)

- H31_BASIS_PAPER: enter when primary-ex same-venue spot exists (46%, +3.45%, WR 100%)
- H34_PERP_PAPER: enter when no primary-spot but h34 hedge exists (46%, +1.28%, WR 79%)
- SKIP 10 cross-ex-spot events (operationally too complex for marginal +$30)

## Backlog priority

1. **Edge 3 — H3 stablecoin depeg arb retrospective** (next cycle)
2. **H38** magnitude-triggered basis-hedge expansion test
3. **H36** micro-cap perp slippage (narrowed: 13 spot-uncovered h34-only events)
4. H29 exchange-API poller (still pending user OK)
5. H1 whale copy / H5 announcement / H6 new symbol detection

## Validated negatives — DO NOT retest

R1 TG-NLP interval · R2 fair-price scalp · R3 listing momentum · R4 microcap expand
R5 multi-ex spread naive · R6 naive funding harvest >2% · R7 confluence LONG
R13 H31 SHORT-side · R14 H31 unhedged · **R15 H37 practitioner unhedged scalp**

## Next-cycle action

H3 stablecoin depeg retrospective:
- Pull CoinGecko hourly price history for USDD, USDC, BUSD, DAI, FDUSD (12mo)
- Identify depeg events |spot − $1.00| ≥ 0.5% sustained ≥5min
- Measure time-to-re-peg distribution
- Compute PnL: LONG depegged + SHORT USDT-quote-perp basis-hedged until re-peg
- If mean ≥+30bp/event AND uncorrelated to H31 windows → Edge 3 validated

## Sources

- `multi_ex_funding_180.parquet` (Binance subset 180,896 rows)
- This cycle: `/tmp/h37_scalp.py`, `/tmp/h37_results.parquet`
- Practitioner module: `Info/files/module.js.Без названия` (de-obfuscated)
- Full log: `insights/cycle_20260522_1700.md`

## User directive (active from 2026-05-22 09:30)

Use WebSearch / WebFetch / GitHub / exchange APIs autonomously. Act decisively.

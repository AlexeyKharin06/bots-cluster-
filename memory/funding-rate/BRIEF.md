# BRIEF — funding-rate snapshot

## State (updated 2026-05-22 17:50 UTC, cycle SYNTHESIS #1)

- ✅ Parquets on VPS: `multi_ex_funding_180` (1.6M rows, 6 ex, 180d, 2025-11-02→2026-05-02),
  `expansion_funding` (35k), `mega_fairprice_*` (316k), `borrow_histories.jsonl` (45 coins)
- ✅ Paper-bots: fairprice_v6 n=6 win=100% mean +$0.49
- ⚠️ `feed_funding.jsonl` empty (upstream channel absence)
- 🧠 SYNTHESIS MODE active. Tested 2 of 10 (C9, C8).

## 🔴 C9 borrow-spike Edge 3 → REJECTED (R16)

22 events on 5 overlap coins (ENSO/KAT/ORCA/RED/STO). Mechanism: rate/rolling-24h ≥ 2× AND ≥ 50bp/h.

| variant | mean 4h | WR | TRAIN | TEST |
|---|---|---|---|---|
| LONG-perp | -2.80% | 32% | -4.13% | +0.04% |
| SHORT-perp | +2.60% | 64% | +3.93% | **-0.24%** |

Spike happens BECAUSE shorts correctly pile in (not pre-squeeze). Direction correct but
n=22 too small — TEST n=7 fails walk-fwd. Methodology lesson #9.

## 🟡 C8 formula-HEDGED on 7914 universe → VALIDATED as H38, NOT Edge 3

Basis-hedge on 10,686 high-mag (|rate|≥30bp) negative-funding events:

- Mean **+1.682%/event**, WR **96.4%**, Sharpe 1.057
- TRAIN n=7480 +1.708% / TEST n=3206 +1.621% — gap **0.087pp** (exceptional)
- Per-month 6/6 positive. Per-ex 5/6 positive (gate +2.02 best, hyperliquid +0.99 weakest)
- 7-day dedup per (ex, sym): 1595 events, mean +1.16%/WR 90%, walk-fwd stable

**Per-magnitude (critical):**
| tier | n | mean | WR |
|---|---|---|---|
| 30-60bp | 6160 | +0.94% | 94% |
| 60-100bp | 2422 | +1.85% | 99.8% |
| **100-500bp** | 2103 | **+3.65%** | 99.9% |

**The 100-500bp tier recapitulates H31's +3.45% on 40x more events.** H31's interval-change
trigger is a high-magnitude proxy, not a unique mechanism. Daily PnL corr w/ H31 = **0.171**.

Verdict: **H38 EXPANSION VALIDATED** (was "magnitude-triggered" in backlog).
Same mechanism as H31 (basis-hedge funding capture) → NOT Edge 3.

## ≥3 independent edges (KPI 4) — STILL 2 of 3

- Edge 1 ✅ H31 basis-hedged (53/116, +3.45%, WR 100%, Sharpe 1.97)
- Edge 2 ✅ H34 perp-perp cross-ex (corr 0.30, +1.28%, WR 79%)
- Edge 3 ❌ **MISSING. C9 rejected. C8 = wider H31. Next: C2.**

## Edge 3 candidate ranking (post-C9/C8)

1. **C2 cross-ex formula divergence** ← NEXT (truly orthogonal mechanism)
2. H3 stablecoin depeg / H1 whale copy / H4 DEX algo flow — backup
3. H6 new-symbol detection — pending API poller

## NEW this cycle

- **H38 VALIDATED**: 92x throughput vs H31, low PnL corr (0.17) but mechanism shared
- **R16** C9 SHORT-perp REJECTED (n=22, TEST fails)
- **Methodology lesson #9**: borrow-spike = shorts piling in, not pre-squeeze

## Paper-stream design (extended)

- H31_BASIS_PAPER: primary-ex same-venue spot (46%, +3.45%, WR 100%)
- H34_PERP_PAPER: no primary-spot but h34 hedge (46%, +1.28%, WR 79%)
- **H38_MAGNITUDE_PAPER (NEW)**: |rate|≤-60bp + spot-leg + 7d per-symbol dedup
  → ~25-30 entries/week, mean ~+1.85%/event

## Backlog priority

1. **C2 cross-ex formula divergence** (next cycle — orthogonal Edge 3 candidate)
2. **H38 paper-stream proposal** (needs user OK + spot-leg coverage on C8 universe)
3. H3 stablecoin depeg retrospective (deferred)
4. H29 exchange-API poller (pending user OK)

## Validated negatives — DO NOT retest

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest
R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · **R16 C9 borrow-spike**

## Next-cycle action

**C2 cross-ex formula divergence as interval-change predictor:**
- Compute practitioner formula per-ex on ~100 high-vol syms × 5 ex
- Find moments where |formula_binance - formula_okx| ≥ 50bp same sym
- Check: within 24h, does interval-change rate exceed baseline by ≥3×?
- If yes → orthogonal Edge 3 candidate (cross-ex info imbalance mechanism)

## Sources / SYNTHESIS status

`/tmp/c9_*.parquet`, `/tmp/c8_fwd.parquet`, `/tmp/c8_short.parquet`, `insights/cycle_20260522_1750.md`
Done: C9 (rejected), C8 (H38 validated). TODO: C1-7, C10. C2 = next.

User directive (active 2026-05-22 09:30): use WebSearch/WebFetch/GitHub/exchange APIs autonomously.

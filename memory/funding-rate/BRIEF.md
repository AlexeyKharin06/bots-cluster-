# BRIEF — funding-rate snapshot

## State (updated 2026-05-22 23:25 UTC, cycle SYNTHESIS #2)

- ✅ Parquets on VPS: `multi_ex_funding_180` (1.6M rows, 6 ex, 180d), `expansion_funding`,
  `mega_fairprice_*`, `borrow_histories.jsonl` (45 coins).
- ✅ Paper-bots: fairprice_v6 n=15 win=93% +$3.34 total; new_symbol n=1 -$0.51.
- ⚠️ `feed_funding.jsonl` empty (upstream channel absence — H5 blocked).
- 🧠 SYNTHESIS: 3 of 10 tested (C9, C8, **C2 this cycle**).

## 🟡 C2 cross-ex divergence → WIDER H31 DETECTOR (NOT Edge 3)

Cross-ex realized-rate divergence at 1h buckets, 88 syms with ≥50bp signal:

| Metric | Value |
|---|---|
| Threshold 50bp signals (180d) | 1,225 |
| P[short. in 24h \| div ≥50bp] | **16.1%** (vs baseline 0.48%) |
| Walk-fwd TRAIN/TEST | 16.05% / 16.12% (gap 0.07pp) |
| Lift TEST | **36.6×** |
| 4h-strict-lead precision | 7.18%/6.59% (lift 16.5×) |
| Recall on 130 (sym,day) | 27.69% at ≥1h lead |
| Best pair @50bp | binance×OKX 37.21% |

**Verdict: NOT Edge 3.** Symbol overlap extreme (RIVER/DRIFT/RAVE/SIREN/PIPPIN drive both
signal AND H31 events). 64% coincident (≤1h lead). As direct trade, divergence = H34 entry
(Edge 2). Catalog as **C2_DIVERGENCE_DETECTOR** (same family as C8/H38).

## KPI 4 (≥3 independent edges) — STILL 2 of 3

- Edge 1 ✅ H31 basis (+3.45%, WR 100%, Sharpe 1.97)
- Edge 2 ✅ H34 perp-perp (+1.28%, WR 79%, corr 0.30)
- Edge 3 ❌ **MISSING. C2/C8/C9 all rejected for mechanism overlap.** Next: H3.

## Edge 3 candidate ranking (post-C2)

1. **H3 stablecoin depeg arb** ← NEXT (orthogonal: solvency/redemption mechanism)
2. H1 whale copy / H4 DEX algo flow — backup (blocked on data ingestion)
3. H6 new-symbol detection — pending H29 poller OK

## C2 operational uses (not Edge 3 but useful)

- **Real-time divergence monitor**: 6-ex stream, flag (sym,min) `max-min ≥50bp` = H31 pre-warning
- **OKX-pair sub-filter**: OKX in 4 of top 5 predictive pairs (37/33/32% hit rate). OKX consistently
  lags peers in funding repricing — structural latency to investigate.

## NEW this cycle (2026-05-22 23:00)

- **C2 → C2_DIVERGENCE_DETECTOR** — 16-44× lift but mechanism overlaps H31
- **R17** C2 standalone Edge 3 REJECTED (predictive precision 7% at 4h lead)
- **Methodology lesson #10**: cross-ex divergence on same instrument ≠ orthogonal to single-ex
  funding stress. Both views of same regime. Need different TRIGGER TYPE for Edge 3.

## Paper-stream design

- H31_BASIS_PAPER: primary-ex same-venue spot (46%, +3.45%, WR 100%)
- H34_PERP_PAPER: no primary-spot fallback (46%, +1.28%, WR 79%)
- H38_MAGNITUDE_PAPER: |rate|≤-60bp + spot + 7d dedup (~25-30 entries/week)
- **NEW: C2_DIVERGENCE_MONITOR (alert-only)** — H31/H34 entry timer

## Backlog priority

1. **H3 stablecoin depeg** (next — only remaining truly-orthogonal Edge 3 candidate)
2. H38 paper-stream proposal (needs user OK + C8 spot coverage)
3. C2 OKX-pair refinement (if H3 fails)
4. H29 exchange-API poller (pending user OK)

## Validated negatives — DO NOT retest

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest
R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike
**R17 C2 standalone Edge 3** (mechanism overlap with H31)

## Next-cycle action

**H3 stablecoin depeg retrospective:**
- Fetch CoinGecko/exchange OHLCV USDC/USDT/USDD/DAI/BUSD/FRAX, 12mo
- Depeg events: |spot − $1.00| ≥ 0.5% for ≥5min
- Basis-trade PnL: LONG-depegged-spot + delta-hedge until re-peg
- If mean ≥+30bp, n≥50, walk-fwd stable, corr_H31 <0.30 → **Edge 3 candidate**

## Sources / SYNTHESIS status

`/tmp/c2_*.{py,parquet}`, `insights/cycle_20260522_2300.md`. Done: C9 (R16), C8 (H38 detector),
C2 (R17 detector). TODO: C1, C3-7, C10. H3 = next.

User directive (2026-05-22 09:30): WebSearch/WebFetch/GitHub/exchange APIs autonomously.

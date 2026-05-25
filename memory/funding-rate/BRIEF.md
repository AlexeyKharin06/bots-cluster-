# BRIEF — funding-rate snapshot (post-cycle 20260525_1100)

## Status: 3-edge portfolio VALIDATED + REGIME-AGNOSTIC + Meth #17 PROMOTED. H38 ↔ H31 daily corr **0.54** (was 0.17 — cycle 1750 used direction-mixed series; AUDIT RESOLVED this cycle). HARDEN-AND-DEPLOY.

## Validated edges

| Edge | n | Mean | WR | Sharpe | corr H31 (LONG-only basis) |
|---|---|---|---|---|---|
| H31 basis-hedge | 116 LONG | +3.52% | 100% | 1.84 | — |
| H34 perp-perp | 101 | +1.28% | 79% | 0.82 | +0.30 |
| H3 50bp depeg | 129 | +0.81% | 96.1% | 0.63 | −0.31 (overlap window) |
| H3 75bp depeg (op tier) | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H38 mag-trigger (full) | 10,686 | +2.02% | 99.7% | 1.27 | **0.54 daily** (corrected) |
| H38_CONFIRMED-50bp | 5,324 | +2.23% | 99.0% | 1.28 | **0.39 daily — NOT indep** |

All edges regime-agnostic (<6% rel PnL diff bull/bear/chop).

## Cycle 1100 findings

- **CYCLE_1750_CORR_AUDIT RESOLVED.** Cycle 1750's "H31×H38_FULL daily-mean corr = 0.171" reproduces EXACTLY when LHS = all 154 H31 detections (direction-mixed). LONG-only n=116 (the actual edge) gives **0.538** (matches cycle 0500). SHORT-side n=38 has mean PnL −3.17% and is anti-correlated with H38 at −0.297 — this is the dilution mechanism (R13-rejected SHORTs lose on the exact days H38 LONGs win).
- **Per-(day,ex,sym) paired Pearson = 0.753** between H31_LONG and H38_FULL — strongest "same-trade" co-movement evidence.
- **Methodology #21 candidate filed**: when correlating EDGE A with superset B, use post-rejection-filter form of A; rejected variants dilute or invert true edge correlation.
- **H38 status verdict UNCHANGED** (still throughput-tier of H31, not Edge 4) but EVIDENCE strengthened (0.54 > 0.5 threshold → same-edge-family is firm conclusion, not borderline).
- **Operational impact**: H38_THROUGHPUT paper-stream and H31 paper-streams must SHARE a single risk-budget bucket; do NOT double-count diversification (prior cycle 1750 "0.17 corr = independent return streams" claim was incorrect).
- **3-edge portfolio status UNCHANGED.**

## Active to-do (priority, post-1100)

1. **H_BOROS_INDICATOR prototype** — Arbitrum RPC + Boros YU fetcher. ~2h. **Deferred 4 cycles — MUST allocate ≥2h next cycle.** Lightweight Pendle REST may shorten.
2. **T1 per-exchange feature enrichment** — t2_classify on 174 T1 cases. ~1h.
3. **H_BASIS_EVENT prototype backtest** — well-motivated; needs #2 first.
4. **C2_DIVERGENCE × Meth #17 corroboration** — ~20m. Would complete Meth #17 cross-validation (3 confirming samples so far).
5. **METHODOLOGY #21 promotion** — re-check H3×H31 corr with LONG-only filter (10m); 1-2 additional cycle audits would confirm pattern.
6. paper_fairprice_v6 — n still 39, gate at n=100.
7. H_TG_ROUTING_PATCH — user OK pending; @vincerid_lost ADD candidate.
8. GitHub direct search / Pi2 paper — deferred again.

## Caveats

- Paper-stream deploy pending user OK; 4 spec candidates (H31/H34/H3 + H38C-throughput).
- H3 USDe+USDD 73.6%. H31 coverage 30% of practitioner FB. H38C top-15 syms 66%. Boros window Oct-Nov-25 short.
- T1 n=174 text-classified only, ~20% FP, not event-backtest-actionable until enrichment.
- paper_fairprice_v6 frozen n=39 (last trade 2026-05-25 08:02 UTC).
- Cycle 1750's other claims using h31_results-style direction-unfiltered series may also be diluted; not portfolio-load-bearing but worth a 10-min sweep next cycle.

## DO NOT

- No real-money deploy without user OK; no Boros exec code without user OK.
- Do not collapse 3-edge portfolio; do not count H38 / H38_CONFIRMED as Edge #4.
- Do not retest H_adapt_1..3 (rejected n=10,686).
- **Meth #14 (SOLO gate) only on unhedged mean-rev; Meth #17 (CONFIRMED gate) only on hedged funding-capture** — sign-flip mandatory.
- Do not use direction-mixed `h31_results` series (n=154) when measuring portfolio-level correlations; always filter to direction==1 LONG-only (n=116) — the deployable edge form.

## Data (VPS)

- code/data/: multi_ex_funding_180.parquet (1.6M), mega_fairprice_backtest, c2_wide, tg_messages_historical (3894), tg_trade_cases (80), media_signals_historical (571), borrow_histories, expansion_funding, pnl_claims_historical
- /tmp/: h31_net (154 → 116 LONG-only), h3_events_24mo (150), c8_fwd (10,686), btc_daily, t2_classified (80), m3_h31_categorized (116), c8_meth17_categorized (10,686), c8_meth17_summary.json, h38c_h31_daily_overlap.csv, t1_refined_cases.jsonl (174), t1_extra_cases.jsonl (325 loose), **cycle_1750_audit_summary.csv NEW (4-row reconciliation)**, **cycle_1750_audit_daily_align1.csv / align2.csv NEW**

## NEXT cycle: H_BOROS_INDICATOR (~2h, critical-path debt) → C2_DIVERGENCE × Meth #17 (~20m) → Meth #21 corroboration (~10m).

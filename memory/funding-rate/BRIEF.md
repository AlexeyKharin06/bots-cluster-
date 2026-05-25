# BRIEF — funding-rate snapshot (post-cycle 20260525_0500)

## Status: 3-edge portfolio VALIDATED + REGIME-AGNOSTIC + Meth #17 PROMOTED. H38C ≠ Edge #4 (corr-corroborated). HARDEN-AND-DEPLOY.

## Validated edges

| Edge | n | Mean | WR | Sharpe | corr H31 |
|---|---|---|---|---|---|
| H31 basis-hedge | 116 LONG | +3.52% | 100% | 1.84 | — |
| H34 perp-perp | 101 | +1.28% | 79% | 0.82 | +0.30 |
| H3 50bp depeg | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| H3 75bp depeg (op tier) | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H38 mag-trigger (full) | 10,686 | +2.02% | 99.7% | 1.27 | 0.17→0.54 (audit) |
| H38_CONFIRMED-50bp | 5,324 | +2.23% | 99.0% | 1.28 | **0.39 — NOT indep** |

All edges regime-agnostic (<6% rel PnL diff bull/bear/chop).

## Cycle 0500 findings

- **H38_CONFIRMED ≠ Edge #4 (correlation-corroborated).** Event-level: 79% of H31 LONG ⊂ H38_CONFIRMED. Day-mean Pearson 0.39 (overlap), 0.21 union-zerofill. H38C is strict day-superset (96.77% of H31-days have H38C; 107 H38C-only days = high-mag funding w/o interval-shorten). 41/58 H31 syms ⊂ 93 H38C syms. Verdict: throughput-tier same family.
- **Replication discrepancy**: cycle 1750 reported H31×H38_FULL daily corr 0.171; my re-derive 0.538. CYCLE_1750_CORR_AUDIT filed — not portfolio-load-bearing yet.
- **T1 mining executed** (3-cycle deferred, vow honored): 174 NEW cases (FP-filter on 3894 msgs). Class shift vs T2: B 16→37%, F 5→25%, L 6→14% — confirms cycle 1435 hypothesis ($-claim bias under-sampled basis-spread). 21 T2-dups skipped.
- **NEW CHANNEL @vincerid_lost**: 45 cases (listing+basis), not in T2 top-3. Add to unified-hub keyword review.
- **Methodology #20 candidate**: Mining-sample bias maps to mechanism-class under-representation.
- **H_BASIS_EVENT PROMOTED**: B is 37% of T1 = largest under-served practitioner mechanism.

## Active to-do (priority, post-0500)

1. **H_BOROS_INDICATOR prototype** — Arbitrum RPC + Boros YU fetcher. ~2h. **Deferred 2 cycles — MUST allocate ≥2h next.**
2. **T1 per-exchange feature enrichment** — T2-classifier loop on 174 new cases. ~1h.
3. **H_BASIS_EVENT prototype backtest** — well-motivated; needs #2 first.
4. **CYCLE_1750_CORR_AUDIT** — reconcile 0.171 vs 0.538. ~20m.
5. **C2_DIVERGENCE × Meth #17 corroboration** — ~20m.
6. paper_fairprice_v6 deep-dive — IF n≥100 (still 31).
7. H_TG_ROUTING_PATCH — user OK pending; @vincerid_lost ADD candidate.
8. GitHub direct search / Pi2 paper — deferred.

## Caveats

- Paper-stream deploy pending user OK; 4 spec candidates (H31/H34/H3 + H38C-throughput).
- H3 USDe+USDD 73.6%. H31 coverage 30% of practitioner FB. H38C top-15 syms 66%. Boros window Oct-Nov-25 short.
- T1 n=174 text-classified only, ~20% FP, not event-backtest-actionable until #2.
- paper_fairprice_v6 frozen n=31.

## DO NOT

- No real-money deploy without user OK; no Boros exec code without user OK.
- Do not collapse 3-edge portfolio; do not count H38_CONFIRMED as Edge #4.
- Do not retest H_adapt_1..3 (rejected n=10,686).
- **Meth #14 (SOLO gate) only on unhedged mean-rev; Meth #17 (CONFIRMED gate) only on hedged funding-capture** — sign-flip mandatory.

## Data (VPS)

- code/data/: multi_ex_funding_180.parquet (1.6M), mega_fairprice_backtest, c2_wide, tg_messages_historical (3894), tg_trade_cases (80), media_signals_historical (571), borrow_histories, expansion_funding, pnl_claims_historical
- /tmp/: h31_net (154), h3_events_24mo (150), c8_fwd (10,686), btc_daily, t2_classified (80), m3_h31_categorized (116), c8_meth17_categorized (10,686), c8_meth17_summary.json, **h38c_h31_daily_overlap.csv NEW**, **t1_refined_cases.jsonl (174) NEW**, **t1_extra_cases.jsonl (325 loose) NEW**

## NEXT cycle: H_BOROS_INDICATOR (~2h) → T1 enrichment (~1h) → H_BASIS_EVENT prototype.

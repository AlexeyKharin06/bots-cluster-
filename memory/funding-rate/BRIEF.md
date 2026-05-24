# BRIEF — funding-rate snapshot (post-cycle 20260524_2300)

## Status: 3-edge portfolio VALIDATED + REGIME-AGNOSTIC + Meth #17 PROMOTED (sign-flip rule). HARDEN-AND-DEPLOY.

## Validated edges

| Edge | n | Mean | WR | Sharpe | corr to H31 |
|---|---|---|---|---|---|
| H31 basis-hedge | 116 LONG | +3.52% | 100% | 1.84 | — |
| H34 perp-perp | 101 | +1.28% | 79% | 0.82 | +0.30 |
| H3 50bp depeg | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| H3 75bp depeg (op tier) | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H38 mag-trigger (full) | 10,686 | +2.02% | 99.7% | 1.27 | 0.17 |
| **H38_CONFIRMED-50bp NEW** | **5,324** | **+2.23%** | **99.0%** | **1.28** | TBD |

All edges regime-agnostic (<6% relative PnL difference across BTC bull/bear/chop).

## Cycle 2300 findings (C8/H38 Meth #17 cross-validation)

- **Meth #17 PROMOTED** candidate→CONFIRMED at decisive n=10,686. CONFIRMED > SOLO on hedged funding-capture: +0.69pp gap at 30bp threshold, +1.09pp at 50bp, +1.68pp at 100bp (monotone). Walk-fwd Sharpe TRAIN 1.14 / TEST 1.15 (gap 0.9% rel). All 6 exchanges direction-consistent.
- **Sign-flip-by-trade-structure rule formalized.** HEDGED funding-capture → CONFIRMED gate (Meth #17); UNHEDGED mean-rev → SOLO gate (Meth #14). Three samples (H3 n=129, H31 n=116, H38 n=10,686) all consistent.
- **H38_CONFIRMED-50bp tier filed**: spec-ready operational sub-stream. ~890 evt/month, slip-robust to 40bp (WR 93%), breaks at 80bp (WR 80%). Top-15 syms 66% (RIVER/PIPPIN/ENSO/ORCA/RAVE/DRIFT — same chronic-discount cluster).
- **NOT a 4th edge.** Same family as H31. Diversification stays at 3.
- **R2 SOLO retest de-prioritized** (Meth #17 corroborated; R2 unhedged so Meth #14 applies trivially).

## Active to-do (priority, post-2300)

1. **H_BOROS_INDICATOR prototype** — Arbitrum RPC + Boros YU fetcher; backtest signal on H34/H38_CONFIRMED. ~2h. Deferred 1x; MUST NOT defer again.
2. **T1 mining** — binding constraint for adaptive analyses. Deferred 3 cycles. MUST NOT defer again.
3. **H38_CONFIRMED daily-mean corr to H31_basis** — REPLICATION vs INDEPENDENT subset. ~30 min.
4. **C2_DIVERGENCE × Meth #17 corroboration** — C2 is inherently 100% CONFIRMED; triangulates Meth #17 boundary. ~20 min.
5. **paper_fairprice_v6 deep-dive** — IF n≥100 (still 31 since 1700).
6. **H_TG_ROUTING_PATCH** — user OK pending (feed_funding=2; paper_practitioner/whale dormant).
7. **GitHub direct search** — open-source funding-arb (deferred from 1700).
8. **Pi2 paper** — alternate-path retrieval (deferred from 1700).

## Caveats

- Paper-stream deploy STILL pending user OK; now 4 spec candidates (H31, H34, H3 + H38_CONFIRMED).
- H3 concentration: USDe+USDD 73.6%.
- H31 coverage: only 30% of practitioner FB cases in our 50-sym universe (1435).
- H38_CONFIRMED top-15 syms 66% — universe diversification ≈ 0.
- Boros window Oct-Nov 2025 short, regime-specific risk.
- paper_fairprice_v6 frozen n=31 since 1700.

## DO NOT
- No real-money deploy without user OK.
- No Boros execution code without user OK.
- Do not collapse 3-edge portfolio.
- Do not retest H_adapt_1..3 (rejected n=10,686).
- **Do not apply Meth #14 (SOLO gate) to hedged backtests, or Meth #17 (CONFIRMED gate) to unhedged backtests** — sign-flip rule mandatory.

## Data (VPS)

- code/data/: multi_ex_funding_180.parquet (1.6M), mega_fairprice_backtest, c2_wide, tg_messages_historical (3036), tg_trade_cases (80), media_signals (571), borrow_histories (45), expansion_funding
- /tmp/: h31_net (154), h3_events_24mo (150), c8_fwd (10,686), btc_daily, t2_classified (80), m3_h31_categorized (116), **c8_meth17_categorized (10,686 + cat_30/50/100bp) NEW**, c8_meth17_summary.json NEW

## Cycle priority NEXT: H_BOROS_INDICATOR (~2h). T1 mining #2.

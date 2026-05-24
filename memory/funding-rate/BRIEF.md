# BRIEF — funding-rate snapshot (post-cycle 20260524_1505)

## Status: 3-edge portfolio VALIDATED + REGIME-AGNOSTIC. HARDEN-AND-DEPLOY phase continues.

## Validated edges (regime-agnostic on n=10,686 H38 sample)

| Edge | n | Mean | WR | Sharpe | corr to H31 |
|---|---|---|---|---|---|
| H31 basis-hedge | 116 (LONG-only) | +3.52% | 100% | 1.84 | — |
| H34 perp-perp | 101 | +1.28% | 79% | 0.82 | +0.30 |
| H3 50bp depeg (post-vet) | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| H3 75bp depeg (operational tier) | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H38 mag-trigger (wider H31) | 10,686 | +2.02% | 99.7% | 1.27 | — |

**Regime overlay (cycle 1505)**: all five edges show <6% relative PnL difference across BTC bull/bear/chop on 7d-return regime tagging. NO regime-conditioned routing needed.

## Findings from cycle 1505 (BTC regime overlay)

- **H_adapt_1..3 REJECTED as edge-selectors** — practitioner mechanism choice (TG corpus) IS regime-skewed at the OPPORTUNITY-RATE level but NOT at the per-event-PnL level. Conflation killed.
- **H_adapt_5 PARTIAL** — re-framed as capital-deployment-planning input (O_depeg events fire more in bear regimes, but each pays the same; H3 actually best in CHOP).
- **METHODOLOGY #19 CANDIDATE** filed — separate `freq(mech|regime)` from `mean_PnL(mech|regime)` when validating adaptive hypotheses.
- Vol tercile shows monotone decrease in H38 mean PnL (lo_vol 2.15% > hi_vol 1.91%), but the 12% relative lift sacrifices 6× sample size = not a useful gate.

## Active to-do (priority order)

1. **T1 mining** — extract 100-200 more trade cases from 3036 raw TG msgs using cycle 1435's T2-learned text priors. Doubling corpus relieves the n=3-7 per-regime-cell binding constraint.
2. **R2 SOLO retest** — apply Meth #17 lens (Meth #14 sign-flip by trade structure: H3 SOLO>CONFIRMED, H31 CONFIRMED>SOLO).
3. **H_BASIS_EVENT prototype** — gated by T1 (need ≥15 event-specific B-class cases; current n=5 too small).
4. **H_TG_ROUTING_PATCH** — still pending user OK (shared infra at `/srv/bots/.shared/tg/tg_unified_listener.py:67-68`).
5. Lower priority: L2 depth daemon, Meth #17 cross-validation on H38, paper-stream bundle ask.

## Known caveats (preserved)

- Paper-stream deployment STILL pending user OK (cycle 1100 / 1700 readiness call).
- H3 concentration: USDe+USDD 73.6% of events post-vet.
- H31 coverage gap: 30% of practitioner FB cases match our 50-symbol universe (cycle 1435 finding).
- Validated edges have no regime routing — but capital allocation could optionally tilt toward H3 in bear (more opportunities, same per-trade alpha).

## DO NOT
- Do not propose real-money paper-stream deploy without user OK.
- Do not collapse 3-edge portfolio into a single composite — each edge has different corr (+0.30 / +0.30 / −0.31) and that variance-reduction is the portfolio.
- Do not retest H_adapt_1..3 as edge-selectors (REJECTED with conviction at n=10,686).

## Available data (on VPS, unchanged)

- /srv/bots/funding-rate/code/data/: multi_ex_funding_180.parquet (1.6M rows), multi_ex_changes_180.xlsx (213 shortenings), tg_messages_historical.jsonl (3036 msgs / 14 channels), tg_trade_cases.jsonl (80), media_signals_historical.jsonl (571 OCR), borrow_histories.jsonl (45 coins)
- /tmp/: h31_net.parquet (154 events), h3_events_24mo.parquet (150), c8_fwd.parquet (10,686 H38), c2_wide.parquet (cross-ex pivot), btc_daily.parquet (NEW: 500 BTC daily bars for regime overlay reuse), btc_regime_cases.parquet (NEW: 80 TG cases × regime).

## Cycle priority NEXT: T1 mining (to relieve n-cell constraint on adaptive testing)

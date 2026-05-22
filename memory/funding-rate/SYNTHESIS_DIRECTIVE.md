# 🧠 SYNTHESIS DIRECTIVE (active 2026-05-22 18:00 UTC)

> User directive: STOP linear "test next hypothesis from backlog". START thinking
> NON-LINEARLY — combine ALL data sources in unexpected ways to find NEW patterns
> and dependencies that no single hypothesis captured.

## Mandate for next cycle

You are an AI. Don't just iterate the backlog. **CROSS-POLLINATE everything we have:**

- Practitioner formula (98% sign-accuracy for funding prediction) — REJECTED standalone
- H31 reactive interval-change (+3.45% WR 100% on 116 events) — VALIDATED
- H34 cross-ex perp-perp hedge (+1.28% on 101 events) — VALIDATED
- multi_ex_funding_180.parquet (1.6M rows, 6 ex, 180d)
- borrow_histories.jsonl (45 coins, Bybit)
- expansion_funding.parquet (15 practitioner tickers — DEGRADED standalone)
- mega_fairprice_*.parquet (316k events — REJECTED standalone)
- Failed tickers (RAVE/SIREN/PIPPIN/etc — failed standalone)
- TG signals_master.jsonl (1533 msgs)
- Validated negatives R1-R15 — each rejection contains a pattern

## Concrete cross-connection hypotheses to brainstorm + test

C1. **Formula × H31 entry filter:** Of 116 H31 events, split by formula's pre-event prediction magnitude (top-quartile vs bottom). Does formula-EXTREME subset have higher mean PnL? If yes → H31_PRO (smaller n but stronger).

C2. **Cross-exchange formula DIVERGENCE as event PREDICTOR:** When Binance formula predicts +X but OKX predicts -X on same coin at same moment, that asymmetry might predict interval change within 24h. Test: compute per-exchange formula on 1.6M rows, find |divergence|>threshold moments, check if interval-change events follow.

C3. **H38 trajectory filter using formula:** Of 7914 high-funding candidates, segment by formula's prediction trajectory (rising/stable/falling). Hypothesis: only RISING trajectory + magnitude trigger has H31-like edge.

C4. **Failed-tickers ANTI-SIGNAL:** RAVE/SIREN/PIPPIN failed expansion. Compute formula accuracy per-ticker. Tickers with formula <90% accuracy might be regime-anomalous = systematically rugged or manipulated. Blacklist OR find separate edge.

C5. **TG mention × formula extreme = directional bet:** When 2+ TG channels mention ticker AND formula shows extreme funding for that ticker = combined signal. Test against signals_master.jsonl ticker mentions.

C6. **Borrow rate × formula × interval-change confluence:** 116 H31 events × borrow rate × formula prediction → triple-filter analysis. Tier-1 subset (top-decile on all three) may have super-edge.

C7. **Fair-price would-be-winners reverse-engineering:** Identify ALL fair-price events where formula sign matched AND price drift < funding (would have won). Characterize that regime. If structural → minority strategy of fair-price that works.

C8. **R15 hedged variant != H31?** Practitioner formula HEDGED is "supposedly H31". But formula triggers on EVERY funding moment (7914 events) not just interval-changes (116). Test the FORMULA-HEDGED on full 7914 set — is this DIFFERENT from H31 or genuinely just a wider H31?

C9. **Borrow-rate spike as Edge 3 candidate:** Validated_signals_funding memory says borrow spike >50% = x10 lift on event probability. CLAIMED but not walk-forward tested. Use multi_ex_funding + borrow_histories to walk-forward.

C10. **Time-of-day × edge intersection:** Both H31 and H34 might have day-of-week/hour-of-day patterns. If specific time windows have higher win rate, that's a TIGHTENING filter (smaller n, higher Sharpe).

## Methodology

Don't test all 10. Pick the 2-3 with HIGHEST PROBABILITY of revealing NEW edge:
- C2 (cross-ex divergence as predictor)
- C8 (formula-hedged on 7914 vs H31 116)
- C9 (borrow spike Edge 3 — orthogonal mechanism)

These three could each independently become Edge 3.

## What NOT to do this cycle

- Don't run H3 stablecoin depeg yet (was previous plan — DEFERRED)
- Don't run H35 spot-leg expansion (done)
- Don't read onchain insights at all
- Don't ask user for permission for anything

## Expected output

`insights/cycle_YYYYMMDD_HHMM.md` with:
- Test results of 2-3 cross-connection hypotheses
- Honest reject/accept verdict per hypothesis
- If anything proves Edge 3 → KPI 4 unblocked → paper-stream proposal next cycle
- New patterns/methodology lessons added to learnings

If nothing pans out — that's also fine. Just be honest. Then propose 3 NEW cross-connections for the cycle after.

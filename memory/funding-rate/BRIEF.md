# BRIEF — funding-rate snapshot

## 🎯 PRIORITY OVERRIDE 2026-05-24 — USER REVEALED CRITICAL STRATEGY PATTERN

User explained predictive cross-exchange basis arb around interval changes (NOT post-event reactive).
Same funding rate, different intervals → longs prefer shorter-interval exchange → cross-ex basis
diverges → predictive LONG short-interval-ex + SHORT long-interval-ex captures basis BEFORE
official announcement.

CURRENT H31/H34 are REACTIVE post-event. User pattern is PREDICTIVE pre-event.
We have been undercapturing this dimension. Full directive: CRITICAL_INSIGHT_USER_2026_05_24.md

## Action queue (override all previous)

1. **U1** — analyze cross-ex basis dynamics around 116 H31 events (existing parquet)
2. **U2** — predict-event model from cross-ex divergence features
3. **U3** — backtest user predictive LONG-shortener strategy
4. **U4** — dynamic exit policy testing
5. **U7** — decompose: when is funding-dominant vs basis-dominant per event
6. **U5** — start live L1/L2 orderbook collection daemon
7. **U6** — mine TG cases for additional manipulation patterns (NOT JUST funding)

After U1-U7: build ADAPTIVE STRATEGY that picks F/B/FB per regime/event.

## DATA on VPS (after today upload)

- multi_ex_funding_180.parquet (1.6M rows)
- multi_ex_changes_180.xlsx (213 shortenings detected)
- tg_messages_historical.jsonl (3036 msgs / 14 channels)
- tg_trade_cases.jsonl (80 reverse-engineered)
- media_signals_historical.jsonl (571 OCR screenshots)
- pnl_claims_historical.jsonl (18 large-$ claims)
- borrow_histories.jsonl (45 coins Bybit)

## Validated edges (still valid, but framework needs adaptation)

| Edge | n | Mean | WR | corr |
|---|---|---|---|---|
| H31_basis | 53 | +3.45% | 100% | — |
| H34_perp_perp | 101 | +1.28% | 79% | +0.30 |
| H3_75bp_dropC | 30 | +1.96% | 100% | -0.31 |

These are CURRENT, will likely be UPGRADED after U1-U7 by adaptive variants.

## DO NOT (per user)
- Do not propose paper-stream (premature without U1-U7)
- Do not fix on funding-only thinking
- Do not analyze just close-price (need bid/ask, direction-aware)
- Do not ask user for permission for L1/L2 collection — start
- Do not continue M1-M7 until U1-U3 done

## CYCLE PRIORITY: U1+U3 sampler next cycle

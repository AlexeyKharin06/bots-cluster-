# BRIEF — funding-rate (post-cycle 20260525_1247)

## Latest finding (1247) — H_COMBO_1 RESOLVED

**H_COMBO_1 NAIVE confluence: REJECTED** on H31 LONG-only n=116.
- c2_any50bp True n=72 +3.58% / False n=44 +3.41% → gap +0.17pp (noise; WF flips).
- At strict 100bp threshold the sign INVERTS (-1.04pp) stably across walk-fwd.

**H31_QUALITY_COMBO sub-tier surfaces** (operational refinement, NOT a new edge):
- Filter: `meth17_CONFIRMED ∧ ¬c2_div_100bp`
- n=70 / mean +3.95% / Sharpe 2.04 / WR 100% / WF stable (TRAIN +1.13pp / TEST +1.08pp gap)
- vs baseline H31 LONG: +0.43pp mean, Sharpe +0.20, throughput -40% (~12 evt/mo vs 19)

**METHODOLOGY #22 CANDIDATE filed:** cross-ex DIVERGENCE (max-min ≥100bp) is a NEGATIVE quality filter on hedged trades — distinct from Meth #17 same-direction CONFIRMED filter. Combine for cleanest setups. Promote after H38 n=10,686 corroboration.

## 3-edge portfolio (UNCHANGED, validated 2026-05-23)

| Edge | Trigger | n | mean | Sharpe | WR | corr |
|---|---|---|---|---|---|---|
| H31_basis | interval-shorten + pre<0 + basis-hedge LONG | 116 | +3.52% | 1.84 | 100% | H38 +0.54, H34 +0.30, H3 -0.31 |
| H34_perp_perp | cross-ex max-positive hedge perp-perp | 101 | +1.28% | 0.82 | 79% | H31 +0.30 |
| H3_depeg 75bp | stablecoin ≥75bp depeg, mean-rev to peg | 39 | +1.96% | 0.87 | 100% | H31 -0.31 |
| H38_CONFIRMED-50bp | THROUGHPUT TIER of H31, NOT edge #4 | 5324 | +2.23% | 1.28 | 99% | H31 +0.54 |
| **H31_QUALITY_COMBO (NEW)** | H31 + meth17 ∧ ¬c2_div_100bp | 70 | +3.95% | 2.04 | 100% | H31-overlap |

## Next cycle — priorities (re-ordered post-1247)

1. **H_COMBO_3** dynamic hedge ratio (pre-event basis trajectory) — uses /tmp/h31_klines.parquet. ~30-45 min.
2. **Meth #22 PROMOTION TEST** on H38 n=10,686 (cross-tab Meth17 × c2_div_100bp). ~30 min.
3. **H_COMBO_2** H3 × H38 same-day co-occurrence — trivial intersection. ~30 min.
4. **H_BOROS_INDICATOR** — DEFERRED 6 cycles. Needs USER decision: allocate multi-cycle slot OR de-prioritize.
5. **T1 per-exchange feature enrichment** (~1h). Adaptive analyses bottleneck.
6. paper_fairprice_v6 — gated at n=100 (currently 42, no new in 12h).
7. H_TG_ROUTING_PATCH — pending user OK (production-blocker for paper_practitioner/whale).

## STOP / DO NOT

- Audit-only cycles (4 consecutive in May 22-25; user explicit mandate).
- Defer H_COMBO_2..6 indefinitely (test 1 per cycle).
- Submit new paper-stream specs until user OKs baseline H31/H34/H3 deployment.
- Trust "confluence" framing for any H_COMBO_2..6 without testing inversion (Meth #22 lesson).

## Live paper bot status (UNCHANGED)

- paper_fairprice_v6: n=42, no new trades since cycle 1100.
- paper_new_symbol: n=1 (dormant since 2026-05-22).
- paper_practitioner / paper_whale: no trades.jsonl yet (feed_funding empty without TG patch).

## Methodology stack (#1-#22)

Confirmed: 1-21. NEW candidate #22 (this cycle): divergence-as-negative-filter sign rule for hedged trades.

Sign-flip rule unified (Meth #14/#17/#22):
- HEDGED funding-capture: prefer CONFIRMED (#17), prefer LOW divergence (#22)
- UNHEDGED mean-rev: prefer SOLO (#14), divergence-filter UNTESTED

## Cross-project notice (UNCHANGED)

ESPORTS H_LISTING_BRIDGE filed for cross-project alert pipe — onchain Claude responsibility.
See /srv/bots/cluster/memory/CROSS_PROJECT_NOTICE_ESPORTS_2026_05_25.md.

## Cycle log

`/srv/bots/cluster/memory/funding-rate/insights/cycle_20260525_1247.md` — full untruncated.

# BRIEF — funding-rate (post-cycle 20260525_1700)

## Latest finding (1700) — Meth #22 PROMOTION FAILED on H38 → NEW Meth #23 candidate + H38_QUALITY_TIER

**Meth #22 sign INVERTS on H38** vs cycle 1247's H31 finding:

| Sample | n | c2_100bp=True gap |
|---|---|---|
| H31 LONG (1247) interval-shortening trigger | 116 | **−1.04pp** (NEGATIVE filter) |
| **H38 (1700) magnitude trigger** | **10,686** | **+1.19pp** (POSITIVE filter) |

Walk-fwd both halves preserve respective signs. Per-ex 6/6 positive on H38. Decisive n=92× sample → cycle 1247 finding is H31-SPECIFIC, not universal.

**METHODOLOGY #23 CANDIDATE filed (subsumes Meth #22):** Cross-ex divergence sign on hedged trades is **trigger-conditional**:
- **Behavioral triggers** (H31 interval-shortening, single-ex action): divergence ≥100bp = outlier-noise marker → NEGATIVE filter
- **Magnitude triggers** (H38 |rate|≥thr universe-wide): divergence ≥100bp = systemic-stress amplitude → POSITIVE filter

Promotion gate: cross-validate on H34 perp-perp n=101 (predict POSITIVE per Meth #23) — ~20 min next cycle.

**NEW H38_QUALITY_TIER:** `cat_50bp=CONFIRMED ∧ c2_max_div≥100bp`. n=1554, +2.838%, WR 99.16%, Sharpe ~2.0. WF TRAIN +3.17/TEST +2.62 (both halves +1.2-1.6pp gap, same direction). 6/6 months +; 6/6 ex + (gate +3.37%, bybit +3.16% strongest). Throughput ~260/mo agg, ~40/mo dedup.

## 3-edge portfolio (UNCHANGED, validated 2026-05-23)

| Edge | n | mean | Sharpe | WR | corr |
|---|---|---|---|---|---|
| H31_basis (interval-shorten LONG + basis-hedge) | 116 | +3.52% | 1.84 | 100% | H38 +0.54, H34 +0.30, H3 -0.31 |
| H34_perp_perp (cross-ex max-pos hedge) | 101 | +1.28% | 0.82 | 79% | H31 +0.30 |
| H3_depeg 75bp (mean-rev to peg) | 39 | +1.96% | 0.87 | 100% | H31 -0.31 |
| H38_CONFIRMED-50bp (THROUGHPUT TIER, NOT edge#4) | 5324 | +2.23% | 1.28 | 99% | H31 +0.54 |
| H31_QUALITY_COMBO (H31 + meth17 ∧ ¬c2_div_100bp) | 70 | +3.95% | 2.04 | 100% | H31-overlap |
| **H38_QUALITY_TIER (NEW)** H38 + CONFIRMED ∧ c2_div≥100bp | **1554** | **+2.84%** | **~2.0** | **99.2%** | overlap |

## Next cycle — priorities (re-ordered post-1700)

1. **H_COMBO_7 (NEW)** — Meth #23 cross-validation on H34 n=101 perp-perp. Same c2_max_div≥100bp cross-tab. Predicted POSITIVE. ~20 min.
2. **H_COMBO_2** H3 × H38 same-day co-occurrence — trivial intersection. ~30 min.
3. **H_COMBO_3** dynamic hedge ratio. ~30-45 min.
4. **H_BOROS_INDICATOR** — DEFERRED 7 cycles. Needs USER decision.
5. T1 per-exchange feature enrichment (~1h).
6. paper_fairprice_v6 — n=42/100 gate.
7. H_TG_ROUTING_PATCH — pending user OK.

## STOP / DO NOT

- Audit-only cycles (user explicit mandate). 1700 is 3rd consecutive combination/promotion test.
- Defer H_COMBO_2..6 indefinitely (test 1 per cycle).
- Submit new paper-stream specs until user OKs baseline H31/H34/H3 deployment.
- Assume cycle 1247's negative-divergence filter applies beyond H31 — Meth #23 shows trigger-conditional sign.

## Live paper bot status (UNCHANGED)

- paper_fairprice_v6: n=42, no new trades since cycle 1100 (17h+).
- paper_new_symbol: n=1 (dormant since 2026-05-22).
- paper_practitioner / paper_whale: no trades.jsonl yet (feed_funding empty without TG patch).

## Methodology stack (#1-#23 candidates)

Confirmed: #1-#21. #22 (cycle 1247) DEMOTED to H31-special-case. #23 (this cycle) candidate: trigger-conditional divergence sign rule (subsumes #22).

Sign-flip rules:
- HEDGED + behavioral trigger (H31): CONFIRMED (#17) + LOW divergence (#23)
- HEDGED + magnitude trigger (H38): CONFIRMED (#17) + HIGH divergence (#23)
- UNHEDGED mean-rev (H3): SOLO (#14), divergence-filter untested

## Cycle log

`/srv/bots/cluster/memory/funding-rate/insights/cycle_20260525_1700.md` — full untruncated.

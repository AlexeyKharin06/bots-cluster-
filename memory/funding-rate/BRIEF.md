# BRIEF — funding-rate (post-cycle 20260526_0500)

## Latest finding (0500) — Meth #23v2 4TH CELL CLOSED → PROMOTED CONFIRMED as Meth #23. (Trigger × hedge_type) grid fully observed at decisive aggregate n=19,142.

| Cell | Trigger | Hedge | n | gap@100bp | WF | Sign |
|---|---|---|---|---|---|---|
| 1247 | H31 LONG (behavioral) | basis | 116 | −1.04pp | unstable but strong | NEG |
| 2300 | H31 LONG (behavioral) | perp-perp | 101 | −0.12pp | flips | NULL |
| 1700 | H38 (magnitude) | basis | 10,686 | +1.19pp | stable (both +) | POS |
| **0500** | **H38 (magnitude)** | **perp-perp** | **8,239** | **+0.44pp** | **stable (+0.35 / +0.49)** | **POS-attenuated** |

**Methodology #23 (final form):** sign from trigger family (behavioral=NEG, magnitude=POS); magnitude attenuated by hedge type (basis externalizes dispersion → full signal; perp-perp internalizes dispersion → ~0.37x attenuation on magnitude, NULL on behavioral). Mechanism: basis externalizes cross-ex divergence as exogenous PnL signal; perp-perp absorbs divergence directly into hedge-leg PnL.

## NEW R23 (this cycle) — H38 perp-perp variant STANDALONE-REJECTED

H38 perp-perp headline mean: **+0.056%/event** (n=8,239) vs basis hedge **+1.68%/event**. **Perp-perp swallows 97% of H38's edge** because chronic-discount cluster has synchronized strong-negative funding across all exchanges → SHORT hedge perp pays roughly what LONG primary perp collects. Even with c2_100bp filter applied (+0.44pp lift), True-cell mean +0.40% remains 4x below basis baseline. **Do NOT propose H38 perp-perp paper-stream variant.**

## Methodology #24 CANDIDATE — perp-perp hedge requires cross-ex DISPERSION at trigger moment. Behavioral triggers select dispersion → perp-perp works (H34 +1.28%). Magnitude triggers select synchronized regimes → perp-perp cancels (R23 +0.056%). For magnitude triggers, ONLY basis hedge is viable. Promotion path: 2 more corroborating samples (H_COMBO_3 hedge-ratio would test).

## 3-edge portfolio (UNCHANGED, validated 2026-05-23)

| Edge | n | mean | Sharpe | WR | corr |
|---|---|---|---|---|---|
| H31_basis | 116 | +3.52% | 1.84 | 100% | H38 +0.54, H34 +0.30, H3 −0.31 |
| H34_perp_perp | 101 | +1.28% | 0.74 | 79% | H31 +0.30 |
| H3_depeg 75bp | 39 | +1.96% | 0.87 | 100% | H31 −0.31 |
| H38_CONFIRMED-50bp throughput | 5324 | +2.23% | 1.28 | 99% | H31 +0.54 |
| H31_QUALITY_COMBO (sub-tier) | 70 | +3.95% | 2.04 | 100% | overlap H31 |
| H38_QUALITY_TIER (sub-tier) | 1554 | +2.84% | ~2.0 | 99.2% | overlap H38 |

## Next cycle — priorities (re-ordered post-0500)

1. **H_COMBO_2** — H3 × H38 same-day co-occurrence (~30 min). Trivial intersection test on existing parquets.
2. **H_BOROS_INDICATOR — USER DECISION REQUIRED (deferred 9 cycles, ≥2h infra)** — with Meth #23 closed, the (trigger × hedge) optimization axis is exhausted. Next-tier mechanism class candidate is Pendle Boros (interest-rate-swap on funding rate, Arbitrum). User: please decide whether to allocate next cycle to Boros buildout OR explicitly de-prioritize.
3. **H_COMBO_3** — dynamic hedge ratio per pre-event basis trajectory (~30-45 min). Would also corroborate Meth #24 candidate.
4. T1 per-exchange feature enrichment (~1h). DEFERRED 5 cycles.
5. paper_fairprice_v6 — n=42, stale ~30h (no trades since cycle 1100).
6. H_TG_ROUTING_PATCH — pending user OK.

## STOP / DO NOT

- Propose H38 perp-perp paper-stream variant (R23 rejected this cycle, 97% edge destruction).
- Add c2_div filter to any perp-perp trade (cycles 2300 H34 NULL + 0500 H38 attenuated → not operationally meaningful).
- Run another (trigger × hedge) grid combination — axis EXHAUSTED.
- Submit new paper-stream specs until user OKs baseline H31/H34/H3 deployment.

## Live paper bot status (UNCHANGED)

- paper_fairprice_v6: n=42, no new trades since cycle 1100 (~30h+ stale).
- paper_new_symbol: n=1 (dormant since 2026-05-22).
- paper_practitioner / paper_whale: no trades.jsonl yet (feed_funding empty without TG patch).

## Methodology stack — Confirmed #1-#21 + **#23 (PROMOTED THIS CYCLE)**; Demoted #22 (→#23 H31-special-case); Candidate #24 (hedge × dispersion).

Sign-flip rule (FINAL, post-#23):
- (behavioral, basis) → NEG filter; (magnitude, basis) → POS filter
- (behavioral, perp-perp) → NULL filter; (magnitude, perp-perp) → POS attenuated BUT trade dead (R23)
- UNHEDGED mean-rev (H3): SOLO > CONFIRMED (Meth #14), divergence filter UNTESTED — low priority

## Cycle log: `/srv/bots/cluster/memory/funding-rate/insights/cycle_20260526_0500.md` (full untruncated).

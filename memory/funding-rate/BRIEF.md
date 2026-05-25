# BRIEF — funding-rate (post-cycle 20260525_2300)

## Latest finding (2300) — H_COMBO_7 Meth #23 on H34 perp-perp n=101: NULL → Meth #23 refined to (trigger × hedge_type)-conditional

H_COMBO_7 tested cycle 1700's queued #1 prediction (Meth #23 POSITIVE filter on H34 perp-perp). Result: **BOTH framings wrong.**

| Cell | Trigger | Hedge | n | gap@100bp | Sign |
|---|---|---|---|---|---|
| 1247 | H31 LONG behavioral | basis | 116 | **−1.04pp** | NEG (stable) |
| 1700 | H38 magnitude | basis | 10,686 | **+1.19pp** | POS (stable) |
| **2300** | **H31 LONG behavioral** | **perp-perp** | **101** | **−0.12pp** | **NULL (WF flips)** |

**Decisive sanity check:** SAME 101 events with basis-hedge metric (net_4h_basis) gives gap **−1.13pp** — reproduces cycle 1247. Trigger unchanged; hedge change alone destroys signal.

**Meth #23 REFINED (not killed):** `(trigger_family × hedge_type) → divergence_filter_sign`. Perp-perp hedge directly absorbs cross-ex funding dispersion that basis hedge externalizes. 4th cell (magnitude × perp-perp) untested — predicted NULL or weakly POS under absorption hypothesis.

**Operational:** H34 spec UNCHANGED. Do NOT add `c2_div_100bp` filter to H34 paper-stream (28% throughput cost for null PnL).

## 3-edge portfolio (UNCHANGED, validated 2026-05-23)

| Edge | n | mean | Sharpe | WR | corr |
|---|---|---|---|---|---|
| H31_basis (interval-shorten LONG + basis-hedge) | 116 | +3.52% | 1.84 | 100% | H38 +0.54, H34 +0.30, H3 −0.31 |
| H34_perp_perp (fixed_binance_else_bybit hedge) | 101 | +1.28% | 0.74 | 79% | H31 +0.30 |
| H3_depeg 75bp (mean-rev to peg) | 39 | +1.96% | 0.87 | 100% | H31 −0.31 |
| H38_CONFIRMED-50bp (THROUGHPUT TIER) | 5324 | +2.23% | 1.28 | 99% | H31 +0.54 |
| H31_QUALITY_COMBO (cycle 1247) | 70 | +3.95% | 2.04 | 100% | overlap |
| H38_QUALITY_TIER (cycle 1700) | 1554 | +2.84% | ~2.0 | 99.2% | overlap |

## Next cycle — priorities (re-ordered post-2300)

1. **H_COMBO_8 (NEW)** — Meth #23v2 4th-cell test: H38 magnitude trigger × perp-perp hedge. Predicted NULL or weakly POS under absorption hypothesis. ~30-45 min. Decisive promotion gate for Meth #23v2.
2. **H_COMBO_2** H3 × H38 same-day co-occurrence — trivial intersection. ~30 min.
3. **H_COMBO_3** dynamic hedge ratio. ~30-45 min.
4. **H_BOROS_INDICATOR** — DEFERRED 8 cycles. Critical-path debt; needs USER decision on multi-cycle allocation.
5. T1 per-exchange feature enrichment (~1h). DEFERRED 4 cycles.
6. paper_fairprice_v6 — n=42/100 gate, no new trades 24h+.
7. H_TG_ROUTING_PATCH — pending user OK.

## STOP / DO NOT

- Add c2_div_100bp filter to H34 paper-stream (cycle 2300 confirmed null effect, 28% throughput cost).
- Promote Meth #23 to confirmed methodology until H_COMBO_8 closes the 4th cell.
- Audit-only cycles (user explicit mandate). 4th consecutive combination/promotion test.
- Defer H_COMBO_2..6 indefinitely (test 1 per cycle).
- Submit new paper-stream specs until user OKs baseline H31/H34/H3 deployment.

## Live paper bot status (UNCHANGED)

- paper_fairprice_v6: n=42, no new trades since cycle 1100 (24h+).
- paper_new_symbol: n=1 (dormant since 2026-05-22).
- paper_practitioner / paper_whale: no trades.jsonl yet (feed_funding empty without TG patch).

## Methodology stack

Confirmed: #1-#21.
#22 (cycle 1247) DEMOTED cycle 1700 to H31-special-case.
#23v1 (cycle 1700, trigger-only) REVISED cycle 2300 to (trigger × hedge_type).
#23v2 candidate: promotion gate at H_COMBO_8 (4th cell).

Sign-flip rule (current evidence):
- HEDGED + behavioral trigger + BASIS hedge: CONFIRMED + LOW divergence (#23v2)
- HEDGED + magnitude trigger + BASIS hedge: CONFIRMED + HIGH divergence (#23v2)
- HEDGED + behavioral trigger + PERP-PERP hedge: no divergence filter (#23v2 NULL cell)
- HEDGED + magnitude trigger + PERP-PERP hedge: UNTESTED (H_COMBO_8 target)
- UNHEDGED mean-rev (H3): SOLO (#14), divergence-filter untested

## Cycle log

`/srv/bots/cluster/memory/funding-rate/insights/cycle_20260525_2300.md` — full untruncated.

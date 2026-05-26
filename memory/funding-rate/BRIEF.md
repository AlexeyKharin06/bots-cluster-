# BRIEF — funding-rate (post-cycle 20260526_1100)

## Latest finding (1100) — H_COMBO_2 H3 × H38 INDEPENDENCE CONFIRMED at full daily grid Pearson ≈ 0. Cross-edge co-occurrence axis closed for this pair.

H38 fires **180/180 days** in overlap → day-level intersection structurally degenerate. Reframed as 4-part test:

| Test | Result | Verdict |
|---|---|---|
| Day-level co-occurrence | 13/13 H3-days ⊂ H38-days, ratio 1.00x | degenerate |
| H38 PnL on-H3 vs off | +1.65% vs +1.69%, gap −0.03pp, t=−0.38 | NULL |
| Lagged k∈[−3,+3] corr | all \|r\| < 0.15 | NULL |
| Top-20 high-\|rate\| H38 days | 1 H3-day (expected 1.4) | NULL |

Pearson daily full-grid +0.036 sum / −0.049 mean / +0.042 weekly — **H3 and H38 truly orthogonal**.

## Sub-finding (small-n, NOT actionable)
**H_OBS_USDE_OVERPEG_DAMPEN:** H3 SHORT (above $1, USDe overpeg) days dampen cluster mean PnL **−0.64pp** + mean \|rate\| **−28%** (n=4 days). Mechanism plausible (yield-rush→softer LONG-perp demand). Retest when overlap extends ≥18mo.

## Edge-pair correlation matrix (UPDATED)

|              | H31_LONG | H34 | H38 | H3 |
|--------------|---|---|---|---|
| H31_LONG     | 1.00 | +0.30 | +0.54 | −0.31 |
| H34          |   | 1.00 | (same family) | (untested) |
| H38          |   |   | 1.00 | **+0.04 (this cycle)** |
| H3           |   |   |   | 1.00 |

**H3's portfolio role reframed:** counter-cyclical to H31, orthogonal to H38, full-independent risk bucket.

## Methodology #25 CANDIDATE
Sparse×dense edge correlation reframe: when one edge fires daily and the other rarely, day-level cross-tab is degenerate. Use (1) conditional-mean Welch-t, (2) lagged ±3-5d corr, (3) tail-risk overlap, (4) per-sym decomposition. Subsumes Meth #21. Promotion gate: 1-2 more sparse×dense applications.

## 3-edge portfolio (UNCHANGED)

| Edge | n | mean | Sharpe | WR |
|---|---|---|---|---|
| H31_basis | 116 | +3.52% | 1.84 | 100% |
| H34_perp_perp | 101 | +1.28% | 0.74 | 79% |
| H3_depeg 75bp | 39 | +1.96% | 0.87 | 100% |
| H38_CONFIRMED-50bp | 5324 | +2.23% | 1.28 | 99% |
| H31_QUALITY_COMBO | 70 | +3.95% | 2.04 | 100% |
| H38_QUALITY_TIER | 1554 | +2.84% | ~2.0 | 99.2% |

## Next cycle — priorities (re-ordered post-1100)

1. **H_COMBO_3** — dynamic hedge ratio per pre-event basis trajectory (~30-45 min). Uses /tmp/h34_results.parquet + multi_ex_funding_180.parquet. Corroborates Meth #24 candidate.
2. **H_BOROS_INDICATOR — USER DECISION (deferred 10 cycles, ≥2h)** — explicit ask: allocate or de-prioritize.
3. paper_fairprice_v6 op-check (n=42, ~36h+ stale).
4. H_OBS_USDE_OVERPEG_DAMPEN retest — blocked until overlap extended (~2h re-fetch).
5. T1 per-exchange feature enrichment (~1h). DEFERRED 6 cycles.
6. H_TG_ROUTING_PATCH — pending user OK.

## STOP / DO NOT

- Day-level co-occurrence framing on H38 vs any rare edge (Meth #25 — degenerate).
- Propose H38 perp-perp paper-stream (R23 rejected).
- Add c2_div filter to any perp-perp trade (Meth #23 final).
- Submit new paper-stream specs until user OKs baseline H31/H34/H3 deployment.

## Live paper bots
- paper_fairprice_v6: n=42, stale ~36h+. Op-check next cycle.
- paper_new_symbol: n=1 dormant.
- paper_practitioner / paper_whale: no trades.jsonl (feed_funding empty without TG patch).

## Methodology stack
Confirmed #1-#23; Candidates #24 (hedge × dispersion) + **#25 NEW (sparse×dense corr reframe, this cycle)**. Sign-flip rule (Meth #23 final): (behavioral,basis)→NEG / (magnitude,basis)→POS / (behavioral,perp)→NULL / (magnitude,perp)→POS-attenuated-but-dead-trade R23. UNHEDGED mean-rev (H3): SOLO>CONFIRMED (Meth #14).

## Cycle log: `/srv/bots/cluster/memory/funding-rate/insights/cycle_20260526_1100.md` (full untruncated).

## 🚨 EXECUTION DEBT — STOP analytics, START execution (user-mandated 2026-05-26 15:55 UTC)

5 последних циклов = только analytics/methodology. Time to EXECUTE.

NEXT CYCLE: ВЫБРАТЬ ОДНО из:
1. **MEGA_GRID validation** — extend klines for 88 missing events, re-run grid sweep with n>50 per cell. Validate vчера findings (hedge_ratio 1.5x, GATE primary +8.58%/WR 92%)
2. **H_COMBO_3 dynamic hedge ratio** — long-deferred user-prompted priority
3. **H_BOROS_INDICATOR** — 10-cycle debt; if user_decision_required, ASK explicitly in BRIEF
4. **R2 revisit** — paper_fairprice_v6 теперь n=51 (passed n=50 threshold)
5. **H_LIVE_1 deployment** — H31_QUALITY_COMBO ready (Sharpe 2.04) — propose live paper-stream

NO MORE methodology candidates without companion live test or backtest validation.

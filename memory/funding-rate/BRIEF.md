# BRIEF — funding-rate (post-cycle 20260528_0500)

## ✅ 05:00 UTC — Meth #26 PROMOTED candidate(1.5/2) → **CONFIRMED (2/2)** via R13→H34 transfer (FINAL gate attempt)

Took the REJECTED R13 variant's distinguishing feature and applied it as a filter to the VALIDATED H34 perp-perp edge. Meth #26 prediction (rejected-variant features don't transfer) CONFIRMED on both components.

```
R13 re-derived: H31 SHORT n=38 pre>0, post fund_cum4 mean -2.942% (=cycle2300 -2.94% sign-flip); LONG +3.751% no flip
H34 baseline (Rule A, n=101): +1.436% / WR 81.2% / Sharpe 0.82

TEST A sign-flip mechanism:  VACUOUS — 0/101 events meet reversal cond (primary_fund_cum4<=0); pre<0 filter already excludes the R13 population
TEST B |pre_rate| magnitude:  NULL — corr 0.032; HIGH +1.443%/80.4% vs LOW +1.428%/82.0% indistinguishable; quartiles non-monotone
Naive R13-danger filter (drop top-|pre_rate| Q): HURTS — n→76, Δmean -0.005pp, Sharpe 0.82→0.762, throughput -25%
Walk-forward both halves agree (TRAIN 0.962→0.909, TEST 0.716→0.651)
```

**Combined statement (3 data points): filter provenance determines transferability.** cycle1700 nano-cap (rejected-tail, no transfer #1) + cycle2300 H_COMBO_3c (validated-derived, DOES transfer = opposite complement) + this R13→H34 (rejected-discriminator, vacuous+null #2). **Derive filters from the structure you intend to filter; never import a rejected variant's discriminator.** Corollary: classify any cross-variant filter as derived-from-validated (re-validate) vs diagnostic-of-rejected (don't transfer).

**Operational:** H34 spec UNCHANGED — do NOT add an |pre_rate| magnitude gate (neutral-to-harmful). Full-universe Rule-A stays.

## paper_fairprice_v6 n=62 → 64 (+2, both sub-60s target_hit)
```
Total:    n=64  sum $+12.92  mean ROI +0.202%  WR 84.4%  22 unique syms
sub-60s:  n=45  WR 97.8%  sum $+22.31  mean +0.496%
≥60s:     n=19  WR 52.6%  sum $− 9.39  mean −0.494%  (static — no new drag trades)
exits:    target_hit 56, timeout 7, hard_sl_net 1
```
Meth #28 bimodality persists clean — sub-60s wing extends, drag wing static.

## 3-EDGE PORTFOLIO — UNCHANGED
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101   (this cycle's test variant; edge intact)
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129
```
Sub-tiers: H38_CONFIRMED-50bp +2.23/99/1.28/5324; H38_QUALITY +2.84/99/~2.0/1554; H31_QUALITY_COMBO +3.95/100/2.04/70; H_COMBO_3c_QUALITY +4.18/100/2.17/40; H_COMBO_STACKED +4.64/100/2.31/28.

## METHODOLOGY COUNTS
#21✓ #22✓ #25✓ **#26✓ CONFIRMED (NEW this cycle)** #27 candidate (H34 ex-rank, deferred 5 cycles — now top open candidate) #28✓ #29 candidate (1/2, mean-rev-to-anchor boundary)

## NEXT-CYCLE PRIORITIES
1. **H34 ex-rank filter (Meth #27)** — rank=1 ∧ n_neg_50≥3 on H34 n=101 (~25 min, def 5 cycles; top open methodology candidate now #26 is closed)
2. **Meth #29 corroboration #2** — 2nd mean-rev-to-anchor strategy unimodality; H3 PYUSD subset (cycle 1132 n=24) natural candidate (~15 min)
3. **paper_new_symbol TP-rule inspection** — TP fire 7% mis-tuned (~10 min)
4. **paper_fairprice_v6 60s-cutoff USER OK ASK** — backed by 3 confirmed methodologies (#26/#28 + #29 boundary)
5. **H_BOROS_INDICATOR** — DEFERRED 17 cycles, USER DECISION REQUIRED

## STOP / DO NOT
- H_COMBO_3 SCALER form, Unhedged LONG primary, H_LIVE_1 amplified, Sign-flip SHORT primary (R13/R24)
- Nano-cap on H31; **NEW: |pre_rate| magnitude gate on H34 (confirmed neutral-to-harmful this cycle)**
- Extend paper_fairprice_v6 to ≥5-min hold (hist negative)
- Apply Meth #28 hold-cutoff to mean-rev-to-anchor strategies e.g. H3 (Meth #29 — destroys edge)
- Block mean-rev-to-anchor paper-stream specs on the cycle-1700 bimodality gate (scope to scalp-class only)
- **NEW: import a rejected variant's discriminator as a filter on a validated variant (Meth #26 — vacuous or null)**

## DATA / TG / GIT
- /tmp/meth26_r13_h34.py (this cycle); /tmp/{h34_results,h31_net,h31_results,c2_wide,mega_fairprice_*,h3_*}.parquet
- code/data/{c2_wide,mega_fairprice_*,multi_ex_funding_180,expansion_funding,h31_combo3c,h37_results}.parquet
- paper_fairprice_v6 n=64, paper_new_symbol n=14. feed_funding 7 (unchanged). H_TG_ROUTING_PATCH pending USER OK (17-cycle). VPS git push fails (credential helper unset).

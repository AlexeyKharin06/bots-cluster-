# BRIEF — funding-rate (post-cycle 20260528_1100)

## ✅ 11:00 UTC — Meth #27 (H34 ex-rank filter transfer) RESOLVED → Meth #24 PROMOTED CONFIRMED

Tested whether the H_COMBO_3c quality filter `rank==1 ∧ n_neg_50≥3` (validated/derived on H31 **basis**) transfers to H34 **perp-perp**. **It does NOT cleanly transfer** — the two components have opposite roles by hedge type. Clean 116/116 join (h34_results × h31_combo3c); baselines reproduce exactly.

```
COMBINED filter (rank==1 ∧ n_neg_50≥3, n=40, 39.6% thru):
  BASIS     +4.178% / WR100% / Sh2.169   (= EXACT repro of cycle-2300 H_COMBO_3c; lift +0.63pp/+0.32Sh)
  PERP-PERP +1.851% / WR82.5% / Sh0.88    (lift +0.42pp mean but +0.06 Sharpe = ~80% Sharpe-value LOST)

DECOMPOSITION (perp-perp): lift is ENTIRELY from rank==1
  rank==1                       n=63  +1.761 / 85.7 / 0.942   <- beats combined
  rank==1 ∧ n_neg_50<3 (disp.)  n=23  +1.605 / 91.3 / 1.142   <- best cell, n too small
  n_neg_50≥3 ∧ rank>1 (sync.)   n=33  +0.852 / 72.7 / 0.617   <- worst
  Spearman(n_neg_50, perp)=-0.075 vs (n_neg_50, basis)=+0.197  (OPPOSITE)
```

**Mechanism:** rank==1 = primary-ex outlier = cross-ex DISPERSION → perp-perp captures wide spread. n_neg_50≥3 = SYNCHRONIZED deep-discount → perp-perp spread collapses (R23) but basis externalizes funding so breadth helps it. Maps onto **(basis ← magnitude/breadth | perp-perp ← dispersion)** duality.

- **Meth #24 PROMOTED candidate→CONFIRMED** (hedge effectiveness conditional on cross-ex dispersion; 2 independent demos: H_COMBO_8/R23 + this rank/n_neg split).
- **Meth #26 corroboration #3** on NEW axis = cross-HEDGE-TYPE (prior were cross-variant). Filter derived on basis loses ~80% Sharpe value on perp-perp.
- **Meth #27 candidate REJECTED as stated** → folds into #24/#26 (not standalone).
- **H34 spec UNCHANGED** — do NOT import the n_neg_50 filter. NEW DRAFT sub-tier `H34_QUALITY_RANK1` (rank==1, n=63, +1.76/85.7/Sh0.94) filed FORWARD-OBS ONLY (modest lift + ex-concentration: gate/bybit/okx strong, binance/bitget weak).

## 3-EDGE PORTFOLIO — UNCHANGED
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101   (this cycle's filter-transfer subject; edge intact)
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129
```
Sub-tiers: H38_CONFIRMED-50bp +2.23/99/1.28/5324; H38_QUALITY +2.84/99/~2.0/1554; H31_QUALITY_COMBO +3.95/100/2.04/70; H_COMBO_3c_QUALITY +4.18/100/2.17/40; H_COMBO_STACKED +4.64/100/2.31/28.

## PAPER BOTS
```
paper_fairprice_v6 n=64→65 (+1 = 300s timeout SHORT -0.76% DRAG wing)
  Total n=65 sum $+12.16 WR 83.1% 22 syms
  sub-60s n=45 WR 97.8% +$22.31  |  ≥60s n=20 WR 50.0% -$10.15
  Meth #28 bimodality persists; 60s-cutoff case REINFORCED.
paper_new_symbol n=14→17 (+3 ALL LOSERS) sum -$8.75 WR 23.5% TP-fire 1/17
  ** LONG-biased momentum-chase = live replay of REJECTED R3 listing-momentum **
  USER DECISION: pause or redesign (not a signal generator).
```

## METHODOLOGY COUNTS
#21✓ #22✓ **#24✓ CONFIRMED (NEW)** #25✓ #26✓ #27 RESOLVED→folds-into-#24/#26 #28✓ #29 candidate (1/2, untouched).

## NEXT-CYCLE PRIORITIES
1. **Meth #29 corroboration #2** — 2nd mean-rev-to-anchor unimodality (H3 PYUSD subset cycle 1132 n=24, or USDC-only) (~15 min). Top open methodology candidate.
2. **paper_new_symbol DECISION** — escalate to user (pause/redesign vs null-control).
3. **paper_fairprice_v6 60s-cutoff USER OK ASK** — backed by Meth #26+#28 CONFIRMED + #29 boundary; +1 drag timeout this cycle = fresh support.
4. **H34_QUALITY_RANK1** — forward-observation only (no action).
5. **H_BOROS_INDICATOR** — DEFERRED 18 cycles, USER DECISION REQUIRED.

## STOP / DO NOT
- H_COMBO_3 SCALER form, Unhedged LONG primary, H_LIVE_1 amplified, Sign-flip SHORT primary (R13/R24)
- Nano-cap on H31; |pre_rate| magnitude gate on H34 (cycle 0500)
- **NEW: import the H_COMBO_3c (n_neg_50) filter onto H34 perp-perp — neutral-to-harmful; if any H34 quality gate is wanted use rank==1 (dispersion) only (Meth #24/#27)**
- Extend paper_fairprice_v6 to ≥5-min hold (hist negative); apply Meth #28 hold-cutoff to mean-rev (H3, Meth #29)
- Import a rejected variant's discriminator as a filter on a validated variant (Meth #26)

## DATA / TG / GIT
- /tmp/meth27_h34_exrank.py + /tmp/meth27_followup.py (this cycle); /tmp/{h34_results,h31_combo3c,h31_net}.parquet
- code/data/{c2_wide,mega_fairprice_*,multi_ex_funding_180,expansion_funding,h31_combo3c,h37_results}.parquet
- paper_fairprice_v6 n=65, paper_new_symbol n=17. feed_funding 7 (unchanged). H_TG_ROUTING_PATCH pending USER OK (18-cycle). VPS git push fails (credential helper unset).

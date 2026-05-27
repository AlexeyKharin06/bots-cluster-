# BRIEF — funding-rate (post-cycle 20260527_1700)

## ✅ 17:00 UTC — Meth #28 PROMOTED → CONFIRMED (HOLD-TIME-TAIL DRAG)

Plan A (H38 hold-stratification) ABANDONED — H38 fixed-hold, structurally incompatible.
Plan B (mega_fairprice exit_reason × hold_min grid) — **overwhelming corroboration**:

```
Across full grid {side × hold_min × SL × Y} = 240 configurations:
  TARGET cells with mean > 0:  240/240  (100.0%)
  TIMEOUT cells with mean < 0: 240/240  (100.0%)
  Gap (TARGET - TIMEOUT): mean +1.617%, median +1.457%, min +0.737%
```

Mechanism confirmed: LONG gap grows monotonic with hold_min (1.61→2.14 over hold=5→60), driven by TIMEOUT worsening (−1.33→−1.83) while TARGET stays flat (~+0.29%). Realized-hold (LONG SL=−0.10 hold_min=5, n=6,556): ≤1m WR 95% +0.10%; 4-5m TIMEOUT WR 8.5% −1.69% (half sample, 100% of loss). Hypothetical cut-at-1m flips strategy −0.81% → +0.034%.

**Meth #28 PROMOTED → CONFIRMED.** Corroborations: paper_fairprice_v6 (live n=61) + mega_fairprice (240 cells).
Scope: TARGET-or-TIMEOUT exits with TARGET fire ≥30-40% only.

### SHORT-side complication
mega SHORT hold=5: ≤1m n=141 mean **−0.69%** WR 87% (NEGATIVE). Contradicts paper-bot sub-60s +0.50%. Reconciliations: (a) granularity (mega 1-min vs paper 10s), (b) regime (Apr hist vs May paper), (c) survivor (|rate|≥50bp filter). DOWNGRADES H_FAIRPRICE_V6_60S_CUTOFF uplift: "modest loss reduction" not "convert losing→winning" — still ship-worthy (zero downside).

## paper_fairprice_v6 n=59 → 61 (+2)
```
Total:    n=61  sum $+11.49  WR 83.6%
sub-60s:  n=42  WR 97.6%  sum $+20.88
≥60s:     n=19  WR 52.6%  sum $− 9.39  ← drag growing (REQ today −$0.67)
```
ONG sub-60s target_hit +$0.068 (+ wing); REQ ≥60s 300s timeout −$0.672 (+ drag).

## CROSS-STRATEGY Meth #28 MAP
| Strategy | Exit | Meth #28? |
|---|---|---|
| paper_fairprice_v6 | TARGET/TIMEOUT/SL | YES (corrob #1) |
| paper_new_symbol | TP/TIMEOUT/SL | YES-principle, TP fire 7% untestable |
| H31, H34, H38, H_COMBO* | Fixed-hold | NO (immune) |
| H3_DEPEG | Peg-target | yes-principle, untested |

**NEW GATE**: any TARGET-or-TIMEOUT spec must report hold-time bimodality before n=30 promotion.

## 3-EDGE PORTFOLIO — UNCHANGED
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129
```
Sub-tiers: H38_CONFIRMED-50bp +2.23/99/1.28/5324; H38_QUALITY +2.84/99/~2.0/1554; H31_QUALITY_COMBO +3.95/100/2.04/70; H_COMBO_3c_QUALITY +4.18/100/2.17/40; H_COMBO_STACKED +4.64/100/2.31/28.

## METHODOLOGY COUNTS
#21✓ #22✓ #25✓ #26 1.5/2 (R13→H34 def 3) #27 candidate (H34 ex-rank def 3) **#28 ✓ NEW**

## NEXT-CYCLE PRIORITIES
1. **Meth #26 promotion** — R13 SHORT → H34 transfer (~20 min, def 3)
2. **H3_DEPEG bimodality check** — first cross-class Meth #28 corrob (~25 min) NEW
3. **H34 ex-rank filter** — rank=1 ∧ n_neg_50≥3 (~25 min, def 3)
4. **paper_fairprice_v6 60s-cutoff USER OK ASK** — now 2 corroborations backing
5. **paper_new_symbol TP-rule inspection** — TP fire 7% mis-tuned (~10 min) NEW
6. **H_BOROS_INDICATOR** — DEFERRED 15 cycles, USER

## STOP / DO NOT
- H_COMBO_3 SCALER form, Unhedged LONG primary, H_LIVE_1 amplified, Sign-flip SHORT primary
- Nano-cap on H31, H_COMBO_3 variant (b), Standalone PS for H_COMBO_STACKED (n=28 < gate)
- Extend paper_fairprice_v6 to ≥5-min hold (hist negative)
- **Promote any TARGET-or-TIMEOUT spec without hold-time bimodality report** (NEW gate)

## DATA / TG / GIT
- /tmp/{h31_net, h34_results, c2_wide, h31_combo3c, h_combo_1_final, h38_trades, meth22_h38_*}.parquet
- code/data/{h31_combo3c, c2_wide, multi_ex_funding_180, mega_fairprice_backtest, expansion_funding}.parquet
- paper_fairprice_v6/trades.jsonl (n=61), paper_new_symbol/trades.jsonl (n=14)
- feed_funding 5 entries (15-cycle stale). H_TG_ROUTING_PATCH pending USER OK (15-cycle).
- VPS git push fails (credential helper unset).

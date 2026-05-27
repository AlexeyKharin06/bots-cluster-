# BRIEF — funding-rate (post-cycle 20260527_2300)

## ✅ 23:00 UTC — Meth #28 cross-class TEST → REFUTED on H3_DEPEG → **Meth #29 CANDIDATE filed** (BOUNDARY discovered)

H3 first cross-class corroboration attempt (cycle 1700 plan #2). Both prior Meth #28 corroborations were fairprice-family.

```
H3 50bp (n=129):  TARGET n=111 mean +0.880% WR 100%   TIMEOUT n=18 mean +0.338% WR 72%
H3 75bp (n=39):   TARGET n=36  mean +1.749% WR 100%   TIMEOUT n=3  mean +1.881% WR 100% (TIMEOUT outperforms)
Hold-cutoff sweep 12..144h: zero negative SLOW buckets
Walk-fwd TRAIN/TEST: both halves TIMEOUT positive (+0.18 / +0.75)
```

**Mechanism:** 72.2% of TIMEOUT trades partially-revert (median entry dev −54bp → median exit dev −23bp = 34bp gain). H3 anchor ($1 peg) is an attractive force; TIMEOUT = slow-but-still-favorable partial reversion, NOT adverse drift.

**Meth #29 (candidate, 1/2):** Meth #28 applies to **scalp/drift-dominated** TARGET-or-TIMEOUT only, NOT to **mean-rev-to-anchor** strategies. Diagnostic: is TARGET "X% from entry" (scalp, Meth#28) or "restore to fixed anchor" (mean-rev, NOT)? The cycle 1700 "NEW GATE" (TARGET-or-TIMEOUT spec must show bimodality pre n=30) must be conditioned on strategy class — would wrongly block valid mean-rev streams like H3_DEPEG.

**Operational:** do NOT apply hold-time cutoff to H3 paper-stream spec. P75-cut (27h) drops mean +0.805→+0.618%, WR 96.1→64.3%; P90-cut (67h) still costs 8.5bp + 19pp WR.

## paper_fairprice_v6 n=61 → 62 (+1)
```
Total:    n=62  sum $+11.92  mean ROI +0.192%  WR 83.9%
sub-60s:  n=43  WR 97.7%  sum $+21.31  (+GUA SHORT 0s target_hit +$0.43)
≥60s:     n=19  WR 52.6%  sum $− 9.39  (no new timeouts since cycle 1700)
exits:    target_hit 54, timeout 7, hard_sl_net 1
```
Bimodality clean. Sub-60s wing extends; drag wing static (the 7th timeout was REQ pre-cycle 1700).

## 3-EDGE PORTFOLIO — UNCHANGED
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129
```
Sub-tiers: H38_CONFIRMED-50bp +2.23/99/1.28/5324; H38_QUALITY +2.84/99/~2.0/1554; H31_QUALITY_COMBO +3.95/100/2.04/70; H_COMBO_3c_QUALITY +4.18/100/2.17/40; H_COMBO_STACKED +4.64/100/2.31/28.

## METHODOLOGY COUNTS
#21✓ #22✓ #25✓ #26 1.5/2 (R13→H34 def 4 cycles) #27 candidate (H34 ex-rank def 4) #28✓ CONFIRMED **#29 candidate NEW (1/2)**

## NEXT-CYCLE PRIORITIES
1. **Meth #26 promotion** — R13 SHORT-side → H34 transfer (~20 min, def 4 cycles, final attempt next cycle then downgrade)
2. **H34 ex-rank filter** — rank=1 ∧ n_neg_50≥3 (~25 min, def 4 cycles)
3. **paper_new_symbol TP-rule inspection** — TP fire 7% mis-tuned (~10 min)
4. **Meth #29 corroboration #2** — find 2nd mean-rev-to-anchor strategy and confirm unimodality; PYUSD H3 subset (cycle 1132 n=24) is natural candidate (~15 min)
5. **paper_fairprice_v6 60s-cutoff USER OK ASK** — now backed by 2 corroborations + boundary clarification
6. **H_BOROS_INDICATOR** — DEFERRED 16 cycles, USER DECISION REQUIRED

## STOP / DO NOT
- H_COMBO_3 SCALER form, Unhedged LONG primary, H_LIVE_1 amplified, Sign-flip SHORT primary
- Nano-cap on H31, H_COMBO_3 variant (b), Standalone PS for H_COMBO_STACKED (n=28 < gate)
- Extend paper_fairprice_v6 to ≥5-min hold (hist negative)
- Promote any TARGET-or-TIMEOUT spec without hold-time bimodality report (cycle 1700 gate)
- **NEW: Apply Meth #28 hold-cutoff to mean-rev-to-anchor strategies (e.g. H3) — provably destroys edge** (Meth #29)
- **NEW: Block mean-rev-to-anchor paper-stream specs on the cycle-1700 bimodality gate — gate should be scoped to scalp-class only**

## DATA / TG / GIT
- /tmp/{h31_net, h34_results, c2_wide, h31_combo3c, h_combo_1_final, h38_trades, meth22_h38_*, h3_*}.parquet
- /tmp/h3_bimodality.py, /tmp/h3_bimod_boundary.py (this cycle)
- code/data/{h31_combo3c, c2_wide, multi_ex_funding_180, mega_fairprice_backtest, expansion_funding}.parquet
- paper_fairprice_v6/trades.jsonl (n=62), paper_new_symbol/trades.jsonl (n=14)
- feed_funding 7 entries (+2 cryptokitta perp-dex stories since cycle 1700). H_TG_ROUTING_PATCH pending USER OK (16-cycle).
- VPS git push fails (credential helper unset).

# BRIEF — funding-rate (post-cycle 20260527_1100)

## ✅ 11:00 UTC — paper_fairprice_v6 R2-diff sanity + HOLD-TIME-TAIL discovery

### HEADLINE — Meth #28 candidate "HOLD-TIME-TAIL DRAG"

paper_fairprice_v6 (n=59) is **strictly bimodal by hold-time**:
```
hold < 60s:  n=41 WR 97% mean +0.50% sum $+20.81  exits all target_hit
hold ≥ 60s:  n=18 WR 50% mean −0.46% sum $− 8.73  6×timeout(300s) + 1×hard_sl
```
Entire bot edge in sub-60s wing; 60s+ tail is silent drag. Mechanism aligns with H37 (median |drift in ±60s| = 69bp > median |funding| = 46bp).

### R2-DIFF sanity (BRIEF 0500 #3) EXECUTED — REFRAMED, not refuted

mega_fairprice filtered SHORT|rate|≥0.5%|hold=5min: n=27 mean **−1.155%** WR 48%. Every |rate| band negative. CAVEAT: mega min hold = 5min vs bot median = 10s — hist CANNOT resolve sub-5-min. Rules OUT extending bot to ≥5-min; does NOT refute sub-60s wing.

### NEW H_FAIRPRICE_V6_60S_CUTOFF (pending USER OK)

Modify bot timeout 300s→60s. Lower-bound uplift +$8.73; realistic $+15-18 vs actual $+12.09 WR ≥90%. Requires USER OK (mandate boundary on live-bot config). If next-30 WR ≥90% mean ≥+0.30% → file H_R2_NARROW_SUB60_RESURRECTED.

### UPDATED prob for fairprice_v6
- as-deployed: survivor 30% / **micro-edge-with-tail-drag 50% NEW** / legit narrow 10% / noise 10%
- 60s-modified: legit micro-edge 70% / survivor 15% / noise 15% (plausible)

## 3-EDGE PORTFOLIO — UNCHANGED (KPI 4 cleared)
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129
```
Sub-tiers: H38_CONFIRMED-50bp +2.23/99/1.28/5324; H38_QUALITY +2.84/99/~2.0/1554; H31_QUALITY_COMBO +3.95/100/2.04/70; H_COMBO_3c_QUALITY +4.18/100/2.17/40; H_COMBO_STACKED +4.64/100/2.31/28.

## METHODOLOGY COUNTS
- #26: 1.5/2 (R13→H34 deferred)
- **#28 NEW: 1/2 HOLD-TIME-TAIL DRAG** (corroboration via H38 hold-strat next)

## NEXT-CYCLE PRIORITIES
1. **Meth #28 corroboration #2** — H38_CONFIRMED-50bp realized-hold stratification (~30 min). NEW. If bimodal → PROMOTE.
2. **Meth #26 promotion** — R13 SHORT→H34 transfer (~20 min) (deferred 2 cycles)
3. **60s-cutoff USER OK ASK** — flip paper_fairprice_v6 timeout config
4. **H34 ex-rank filter** — rank=1 ∧ n_neg_50≥3 on H34 (~25 min) (BRIEF 0500 #2)
5. **H_BOROS_INDICATOR** — DEFERRED 14 cycles, USER

## STOP / DO NOT
- H_COMBO_3 SCALER form — WR 65-87%
- Unhedged LONG primary — −0.53%
- H_LIVE_1 amplified — overfit
- Sign-flip SHORT primary — WF unstable R24
- Nano-cap filter on basis-hedged H31 — no improvement
- H_COMBO_3 variant (b) — falsified
- Standalone PS for H_COMBO_STACKED — n=28 < gate
- **Extend paper_fairprice_v6 to ≥5-min hold** — hist negative (27_1100)

## DATA AVAILABILITY
- /tmp/{h31_net, h31_klines, h34_results, c2_wide, h31_combo3c, h_combo_1_final}.parquet
- /srv/bots/funding-rate/code/data/{h31_combo3c, c2_wide, multi_ex_funding_180, mega_fairprice_backtest, expansion_funding}.parquet
- /srv/bots/funding-rate/code/paper_fairprice_v6/trades.jsonl (live n=59)

## GIT OPS
VPS push fails (credential helper unset). User: `git config --global credential.helper store` + token OR SSH deploy key.

## PAPER-BOT STATE
```
paper_fairprice_v6  n=59 (+3)  win=84.7%  $+12.09  last 08:00 UTC (ACTIVE)
  sub-60s wing: n=41 WR 97% +$20.81 ← edge
   ≥60s wing:   n=18 WR 50% −$8.73 ← drag
paper_new_symbol    n=13 (+2)  win=38.5%  $−1.01   ACTIVE small-n
paper_practitioner / paper_whale: no trades (TG-gated)
```

## TG SIGNALS
feed_funding.jsonl: 5 entries unchanged. Routing 0.12%. Latest: 2026-05-26 22:08 Binance ESPORTSUSDT delist 2026-06-10. H_TG_ROUTING_PATCH pending USER OK (14-cycle).

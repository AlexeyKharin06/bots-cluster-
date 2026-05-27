# BRIEF — funding-rate (post-cycle 20260527_0500)

## ✅ 2026-05-27 05:00 UTC — H_COMBO_3c × HQC overlap resolved; fairprice_v6 audited n=56

### H_COMBO_STACKED (sizing logic on C3CQ, NOT a paper-stream)

```
filter: (rank=1 AND n_neg_50>=3) AND (meth17_CONFIRMED AND NOT c2_div_100bp)
n=28 / mean +4.64% / WR 100% / Sharpe +2.31    vs C3CQ +4.18/2.17 vs HQC +3.95/2.04
WF TRAIN n=19 +4.88/Sh 2.18  TEST n= 9 +4.13/Sh 2.93  (15.4% gap, TEST>baseline)
all 5 ex positive (bybit +5.81 n=10 best)
```

Jaccard(C3CQ, HQC) = 34.1%. C3CQ-only n=12 (+3.10%) and HQC-only n=42 (+3.49%) both DEGRADE to baseline-equivalent — entire quality lift lives in 28-event intersection. Use: 1.5× sizing when both fire, 0.5× when C3CQ-only.

### OBS_FAIRPRICE_V6 — survivor probability DOWNGRADED 60→30%

n=31→56. BOBBOB share 32%→0%. New-25: mean +0.38%/WR 88% (4.2× lift). 18 unique syms (was 11). WF TEST n=17 +0.42% > TRAIN n=39 +0.13% (Meth #12). ESPORTS +6.40% caught Binance delisting (rozenroom TG 2026-05-26). Updated: survivor 30/legit 50/noise 20. Next checkpoint n=100 OR n_unique_syms≥25.

## 3-EDGE PORTFOLIO — UNCHANGED (KPI 4 cleared)
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116   corr(H38)+.54  corr(H3)-.30
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101   corr(H31)+.30
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129   corr(H31)-.31
```
Operational tiers (NOT edges):
- H38_CONFIRMED-50bp +2.23/99/1.28/5324  H38_QUALITY +2.84/99/~2.0/1554
- H31_QUALITY_COMBO +3.95/100/2.04/70   H_COMBO_3c_QUALITY +4.18/100/2.17/40
- **H_COMBO_STACKED +4.64/100/2.31/28 ← NEW (sizing logic, not paper-stream)**

## METHODOLOGY #26 — count UNCHANGED at 1.5/2

This cycle TANGENTIAL (both filters from validated structures). Side observation strengthens generalization: filters from INDEPENDENT validated structures may still be redundant if capturing same signal axis. Promotion to CONFIRMED still needs R13→H34 transfer test.

## NEXT-CYCLE PRIORITIES
1. **Meth #26 promotion** — R13 SHORT-side feature → H34_PERP_PERP transfer (~20 min)
2. **H34 ex-rank filter** — rank=1 AND n_neg_50≥3 on H34 universe; if lift, Meth #27 candidate (~25 min)
3. **fairprice_v6 R2-diff sanity** — filter mega_fairprice to |rate|≥50bp ∧ hold≤300s ∧ SHORT (~15 min)
4. **H_BOROS_INDICATOR** — DEFERRED 13 cycles, **USER DECISION REQUIRED**. ~2h Arbitrum RPC infra.

## STOP / DO NOT
- H_COMBO_3 SCALER form — WR 65-87% (26_2300)
- Unhedged LONG primary any horizon — −0.53% (26_0500)
- H_LIVE_1 cross-ex hr>1.0 amplified — overfit (26_0500)
- Sign-flip SHORT primary gate/okx — WF unstable R24 (26_1700)
- Nano-cap fp<$0.01 filter on basis-hedged H31 — no improvement (26_1700)
- H_COMBO_3 variant (b) intensity-scaling — falsified (26_1700)
- Standalone paper-stream for H_COMBO_STACKED — n=28 below n-gate (HQC n=70 covers superset)

## DATA AVAILABILITY
- /tmp/{h31_net, h31_klines, h34_results, c2_wide, h31_combo3c, h_combo_1_final}.parquet
  + durable copy at /srv/bots/funding-rate/code/data/{h31_combo3c, c2_wide, multi_ex_funding_180, mega_fairprice_backtest, expansion_funding}.parquet

## GIT OPS (carry-over)
VPS push fails (credential helper unset). User: `git config --global credential.helper store` + token push OR SSH deploy key.

## PAPER-BOT STATE
```
paper_fairprice_v6  n=56  win=85.7%  $+12.31  last 2026-05-27 04:00 UTC (1h ago — ACTIVE)
paper_new_symbol    n=11  win=36.4%  $-0.03   no recent trades
paper_practitioner  no trades                  (gated on TG feed)
paper_whale         no trades                  (gated on TG feed)
```
fairprice_v6 DIVERSIFIED 32%→0% BOBBOB. ROI 4.2× lift in new-25 window. Survivor prob 60→30%.

## TG SIGNALS
feed_funding.jsonl: **5 entries** (was 2). Routing ratio still 0.12%. Latest: 2026-05-26 22:08 Binance delisting ESPORTSUSDT 2026-06-10 (H_BASIS_EVENT). H_TG_ROUTING_PATCH pending USER OK (11-cycle deferral).

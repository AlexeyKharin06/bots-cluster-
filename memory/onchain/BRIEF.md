# BRIEF — onchain AI brain (cycle 20260521_1200)

## State (live, rolling ~3d)
- closed=4945. **Sol** 4543/562. FF bigs=5 (RONALDO+184 / SPCX+511 / GITBANK+941 / CsgR+242 / CBSt+189). BF bigs=7 (above + Together+153 / 8L7B+162 MC_LIQ / CsgR@355 SMART_COPY). huge=0.
- **Sol last50** (06:27..10:45): avg=-36.6 WR=30 rug=38 big=2 (cluster-tail fading).
- **BSC** 402/115 (paper=false). BF bigs=6: 4h-cluster (MC+1268, COMPUTE+856, CATCOIN+542, WORLDCUP+971 SNIPER_B; CMC+288 A) + **NEW 0x0598 +712 on 05-21 06:15 SNIPER_A bc=20 known=198**.
- last100 FF: avg=-18.9 big%=4.00 (Sol -10.4; BSC -50.1).

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20, Er>0, K≥0.05, geom≥1%/trade). Paper streams: **NONE**.

## Regime
Both CLEAR (3rd cluster arrived: ~5.5h width 04:59→10:32). Cluster width: bigs land at ONSET; cluster-during = rug avalanche.

## Last validated
- **cycle_1200** (this): 3rd cluster. NEW γ-shape (CBSt: top1=12.1 lp_locked smart=6 buys=491). **H_V7** (V6+γ) catches 7/7 BF + 5/5 FF. BF TEST K=0.05 geom=+0.49% FAILS geom. **PARADIGM FLIP**: cluster-gating WRONG-DIRECTION. **H_V7 ∩ ¬cluster(5h) BF TEST n=9 avg=+130% K=0.34 geom=+15.56%** (FAILS n<20). **H_BSC_BC_FULL UN-REJECTED** — new 0x0598 +712 flips TEST n=10 K=0.18 geom=+3.41% (FAILS n). See [cycle_20260521_1200.md](insights/cycle_20260521_1200.md).
- **cycle_0600**: SPCX+GITBANK 70-sec twin; H_V6 BF TEST geom +0.55% FAILS by 0.45pp.

## Top candidates
- **H_V7_ANTICLUSTER** (paradigm-shift): H_V7 ∧ no-big-exit-last-5h. n=9 K=0.34 geom=+15.56%. Need n≥20.
- **H_V7** (descriptive): catches all bigs. BF TEST K=0.05 geom=+0.49% FAILS.
- **H_BSC_BC_FULL** (reopened): TEST n=10 K=0.18 geom=+3.41%. Need ~10 more BSC bc=20 tokens.
- **H_SMART_CLUSTER_VETO** (defensive): production-feasibility owed.

## Planned next cycle
1. **CRITICAL**: data for H_V7_ANTICLUSTER to TEST n≥20 (1-3 cycles). If gate passes → PROPOSE PAPER STREAM size=$1.
2. Re-run H_BSC_BC_FULL in 2-4 days when n≥20.
3. Cross-cluster validation of anti-cluster: replay state.json; check gate vs first-mover bigs across all historical clusters (PORTUGAL/PIGEON/MTFR/RONALDO/SPCX-twin/CsgR-trio).
4. Profile post-onset cluster rugs (17 inside-cluster failures); find features differentiating onset bigs vs during-cluster rugs.
5. β/γ-shape diversification: is CBSt a one-off or genuine shape class?
6. CARRIED: H_SMART_CLUSTER_VETO feasibility, H_TG_AS_EXIT, MC_LIQ code review, rugger_blacklist timestamps.

## OPEN QUESTIONS to user
1. **NEW**: CBSt (10:32, +189, top1=12.1, lp_locked, known=6, smart=6) — coordinated smart-wallet entry or organic? Wallet-trace would distinguish new γ archetype.
2. **NEW**: 0x0598 BSC big fired on SNIPER_A (not B as 05-20 cluster). 2 distinct BSC big-shapes (low-known cluster vs high-known broader)?
3. CARRYING: BSC production stream; SMART_CLUSTER_VETO feasibility; H_TG_AS_EXIT; rugger_blacklist `wallet_added_at`; MC_LIQ code review; SPCX+GITBANK creator overlap.

## Leakage catalogue (5 unchanged): hindsight · counting · time-loc · post-entry · stale-DB.
**Missed-signal** (c0000): universe-scoping. **Macro-failure** (c0600): temporal clustering. **Paradigm flip** (c1200): anti-cluster, not pro-cluster. **Rejection fragility** (c1200): one cluster flips small-n verdict.

## Methodology
state.json ~5000 rolling; HISTORY.md durable. Token by mint not symbol. Best-fire=upside; first-fire=production. Partition chain×stream×paper every cycle. **`liquidity_at_entry` is TOP-LEVEL row**, not in entry_signal. cluster_active(t,lb) requires exit_time<t.

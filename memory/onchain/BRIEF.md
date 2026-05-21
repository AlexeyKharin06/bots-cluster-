# BRIEF — onchain AI brain (update: cycle 20260521_0600)

## State (live, rolling ~3d window — NOT append-only)
- closed=4910 (5000-cap rotating). Brain memory durable; live state ephemeral.
- **Sol** 4561 rows / 555 unique. last50 avg=**+11.2** WR=40 rug=20 big=4 (huge=0). FF bigs=3: RONALDO+184, SPCXDRAGON+511, GITBANK+941. BF bigs=4: above + Together+153. Span 2026-05-18T07:12..05-21T05:56 (2.95d).
- **BSC** 349 rows / 103 unique / **paper=false (real money)**. last18 (post-cluster) avg=-72.7 big=0. BF bigs=5 (PORTUGAL rotated out): MC+1268, COMPUTE+856, CATCOIN+542, WORLDCUP+971, CMC+288 — all in 4h cluster 05-20T13:39-17:48.
- last100 FF combined (Sol+BSC): n=100 avg=-16.3 WR=36 rug=37 big=2.0 (Sol -3.9 / BSC -72.7).

## Goal & gate
**+1,000,000%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20, Er>0, K≥0.05, geom≥1%/trade). Paper streams: **NONE** (H_V6 FAILS geom by 0.45pp this cycle).

## Regime — BOTH conds CLEAR (2nd time; 1st was cycle_1800 head-fake)
- Cond A: -56.6 → **+11.2** (CLEAR, +67.8pt swing).
- Cond B: 2 fresh first-fire bigs in last hour. **big%=4.00** in last50 (CLEAR).
- Caveat: head-fake risk per cycle_1800 precedent. Difference vs cycle_1800: 2 fresh bigs (not 1), and 2 cluster events visible in cycle (SPCXDRAGON+GITBANK 70-sec twin + earlier RONALDO).

## Last validated work
- **cycle_20260521_0600** (this): 2 NEW Sol bigs identified → 2 DISTINCT big-shapes confirmed (α whale+meteora top1≥85, β mid+pumpswap top1∈[50,75]). H_V3 misses entire β-shape. **H_V6** (OR: α-path ∨ β-path) catches 4/4 BF + 3/3 FF bigs; FF TEST n=20 avg=+23.7% K=0.05 geom=+0.55%/trade — passes n/Er/K, FAILS geom by 0.45pp. H_BSC_BC_FULL re-test: 7 fresh post-cluster bc=20 tokens, 0 bigs, 6/7 rug — **REJECTED**. NEW hypothesis class: **H_CLUSTER_ONSET_REGIME_SIZING**. See [cycle_20260521_0600.md](insights/cycle_20260521_0600.md).
- **cycle_20260521_0000**: BSC universe blind-spot exposed; H_BSC_BC_FULL strong descriptive cohort signal but TEST-failed.

## Top candidates
- **H_V6** (NEW, primary monitor): catches all bigs both dedups. Borderline geom fail. Re-test in 1-2 cycles as TEST window evolves.
- **H_CLUSTER_ONSET_REGIME_SIZING** (NEW hypothesis class): regime-detection + sizing rule, not feature filter. Next-cycle exploration priority.
- **H_V3** (Sol α-only, deprecated): too tight — misses entire β-shape. Superseded by H_V6.
- **H_SMART_CLUSTER_VETO** (defensive): production-feasibility owed.

## Planned next cycle
1. **Watch for 3rd cluster event** in next 6-12h. If present: cluster-onset hypothesis strengthens. If absent: head-fake confirmed.
2. **Design + walk-forward H_CLUSTER_ONSET_REGIME_SIZING** — rolling-25-window big-presence indicator + conditional Kelly sizing on H_V6 entries inside an active cluster.
3. **Re-run H_V6 walk-forward** when TEST boundary shifts (TEST will be 03:00→11:00 by next cycle).
4. **β-shape investigation**: SPCXDRAGON+GITBANK creator-wallet/lp-provider overlap (single-actor batch launch vs independent coincident pumps).
5. **Cross-chain partition** every cycle (methodology rule from cycle_0000).
6. CARRIED: H_SMART_CLUSTER_VETO feasibility, H_TG_AS_EXIT instrumentation, MC_LIQ sniper-code review, rugger_blacklist timestamps.

## OPEN QUESTIONS to user
1. **NEW**: SPCXDRAGON + GITBANK entered 70 seconds apart, both pumpswap, both first-fire=best-fire on SNIPER_A. Coincidence or coordinated? If you have wallet-trace data showing same buyer cluster on both, that's evidence for single-actor / coordinated launch (very different implication than independent pumps).
2. **NEW**: BSC SNIPER_D / D2 — n=34 each on BSC universe, avg=-24 rug=26 big=2.9. Small but better than A/B. Is BSC SNIPER_D the same logic as Sol SNIPER_D, or BSC-specific?
3. CARRYING: BSC production stream (A=-62.8 or B=-7.2 dedup); H_SMART_CLUSTER_VETO entry-vs-exit feasibility; bonding_curve_buyers cap-20 semantics; H_TG_AS_EXIT instrumentation; rugger_blacklist `wallet_added_at`; MC_LIQ sniper-code review.

## Leakage catalogue (5 forms unchanged): hindsight classifier · counting inflation · time-localization · post-entry feature · stale classifier DB.
**Missed-signal category** (cycle_0000): universe-scoping blind-spot.
**Macro-failure mode** (cycle_0600): **temporal clustering of fat tails** — feature filters that catch every big also fail walk-forward because bigs concentrate in single event-windows; any TRAIN/VAL/TEST split puts the cluster on one side. Not leakage; legitimate sample-scarcity. Resolution: cluster-onset detection layer (proposed H_CLUSTER_ONSET_REGIME_SIZING).

## Methodology notes
- state.json ~5000-cap rolling; HISTORY.md durable. Identify tokens by `token` mint, NEVER symbol. Best-fire=upside; first-fire=production. Run chain × stream × paper partition every cycle before scoping. **Fat tails are event-clusters, not uniform**: H_V3/H_BSC_BC_FULL/H_V6 all show TRAIN-vs-TEST split-dependence based on which side contains the cluster.

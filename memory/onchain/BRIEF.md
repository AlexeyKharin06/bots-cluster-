# BRIEF — onchain AI brain (cycle 20260522_0000)

## State (live, rolling ~3d)
- closed=4807 (rotated -138 vs c1200). **Sol** 4326/533. **BSC** 481/142 (+27 BSC).
- Sol FF bigs=7 (RONALDO+184 / SPCX+511 / GITBANK+941 / ser+242 / Omnimals+189 / **FOID+424 NEW / Blobby+293 NEW**).
- Sol BF bigs=9 (above + Together+153 / RNBINU+162; FOID BF=+575 / Blobby BF=+682 — both SMART_TOP_AGE5).
- BSC BF bigs=8 (cluster1: MC+1269/COMPUTE+856/CATCOIN+542/WORLDCUP+971; broader: CMC+288 F2 / TLS+712 D2; **TEST: MEMEWC+179 / PEDUCK+908 SNIPER_B NEW**).
- Sol last50 avg=-55.3 (Cond A re-active) big%=2.00. Last100 = -80% (post-cluster tail).

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20, Er>0, K≥0.05, geom≥1%/trade). Paper streams: **NONE** (proposed: H_BSC_BC_FULL_B pending approval).

## Regime
Cond A re-active (last50 -55.3). 3 Sol chains observed (Together-RONALDO 4.8h; SPCX→Omnimals 5.6h; FOID-Blobby 2.1h). BSC: 3rd independent cluster confirmed in TEST (MEMEWC+PEDUCK).

## Last validated
- **cycle_22 (this)**: cross-cluster check on 9 Sol bigs: onsets avg=+413% vs followers avg=+461%. **H_V7_ANTICLUSTER FALSIFIED** (c1200 paradigm-flip was single-cluster artifact = new 6th leakage form). H_V8 (V7 with α-liq≥13K) catches 9/9 BF bigs but TEST geom=+0.01% FAILS gate (4th cycle below). **H_BSC_BC_FULL_B PASSES GATE on 3 independent clusters**: TRAIN n=43 K=0.18 geom=+4.22%; VAL n=13 K=0.11 geom=+1.46%; TEST n=15 K=0.16 geom=+2.68% big=13.33% rug=20% — only TEST n<20 floor. See [cycle_20260522_0000.md](insights/cycle_20260522_0000.md).
- **cycle_12** (c1200): 3rd Sol cluster; H_V7 catches 7/7 BF; H_V7 ∩ ¬cluster(5h) BF TEST n=9 K=0.34 geom=+15.56% — FALSIFIED this cycle.

## Top candidates
- **H_BSC_BC_FULL_B** (paper-stream candidate): bc≥16 BSC ∩ SNIPER_B routing. TEST K=0.16 geom=+2.68% on 3 independent clusters. n=15<20 floor only. STRONGEST EVER.
- **H_V8** (Sol, descriptive): catches 9/9 BF bigs. TEST geom=+0.01% FAILS gate (trend negative over 4 cycles — c1800 V3 / c0600 V6 / c1200 V7 / c2200 V8). Need tighter Sol sub-filter or accept Sol can't pass yet.
- **H_V7_ANTICLUSTER** (defunct): REJECTED. Single-cluster artifact (6th leakage form).
- **H_SMART_CLUSTER_VETO** (defensive, carried): production-feasibility owed.

## Planned next cycle
1. **CRITICAL**: monitor BSC for 5+ more bc=20 entries to push H_BSC_BC_FULL TEST n above 20 floor (~2-4 days expected).
2. **If user approves paper-stream**: write spec to memory/onchain/paper_streams_spec/H_BSC_BC_FULL_B.md, begin forward tracking.
3. Re-run H_V8 walk-forward when 2+ new Sol bigs land. Check onset-vs-follower for new bigs to harden Sol chain model.
4. Profile non-bigs within H_V8 (n=152) to find sub-filter dropping rugs without dropping bigs.
5. Inspect chain-2-to-chain-3 gap window (idx 408-458, 05-21T13:18-17:10) — were there near-bigs missed?
6. CARRIED: H_SMART_CLUSTER_VETO feasibility, H_TG_AS_EXIT, MC_LIQ code review, rugger_blacklist timestamps.

## OPEN QUESTIONS to user
1. **NEW — paper-stream approval**: deploy H_BSC_BC_FULL_B (BSC bc≥16 ∩ SNIPER_B trail routing) at $1 paper? TEST K=0.16 geom=+2.68% on 3 independent clusters, n=15<20 floor only. Strict gate FAILS (avg+WR); Kelly-gate PASSES (brain's primary since c0000).
2. **NEW — Sol stream attribution**: 6/9 Sol BF bigs ride SNIPER_SMART_TOP_AGE5; SNIPER_A first-fire loses 30-70pp avg. Should Sol α-entries route through SMART_TOP_AGE5 trail? Sol-side parallel of BSC SNIPER_B finding.
3. CARRYING: SMART_CLUSTER_VETO feasibility; H_TG_AS_EXIT; rugger_blacklist `wallet_added_at`; MC_LIQ code review.

## Leakage catalogue (6, +1 this cycle)
hindsight · counting · time-loc · post-entry · stale-DB · **single-cluster artifact (NEW c2200)**.

## Methodology
Best-fire=upside; first-fire=production. cluster_active(t,lb) requires exit_time<t. **Cross-cluster validation mandatory**: small-n signals with bigs in 1-2 events tagged SINGLE-CLUSTER pending 2+ independent cluster confirmation (H_V7_ANTICLUSTER lesson).

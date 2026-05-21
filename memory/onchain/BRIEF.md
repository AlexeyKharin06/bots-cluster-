# BRIEF — onchain AI brain (update: cycle 20260521_0000)

## State (live, rolling ~3d window — NOT append-only)
- closed=4807-4983 (5000-cap, rotating live). Brain memory durable; live state ephemeral.
- **Sol** 4475 rows / 549 unique. last50 avg=-56.6 WR=22 rug=56 big=0. Bigs first-fire=1 (RONALDO), best-fire=2 (Together, RONALDO). Span 2026-05-18T04:11..05-20T23:37 (2.81d).
- **BSC** 332 rows / 97 unique / **paper=false (real money)**. avg first-fire=-62.8 best-fire=-7.2. **Bigs=6**: PORTUGAL+906, MC+1268, COMPUTE+856, CATCOIN+542, WORLDCUP+971, CMC+288. 5/6 clustered 4h on 05-20T13:39-17:48.
- **PIGEON+3699 and MTFR+251 rotated out** since cycle_1800; durable only in HISTORY.md.

## Goal & gate
**+1,000,000%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20, Er>0, K≥0.05, geom≥1%/trade). Paper streams: **NONE** (H_V3 borderline-fail 1800; H_BSC_BC_FULL TEST-fail this cycle).

## Regime — both conds RE-TRIGGERED (cycle_1800 "both clear" was 1-cycle head-fake)
- Cond A: -43.8 → **-56.6** (re-triggered). Same pattern as cycle_1200→1328.
- Cond B: RONALDO slid out of last50 → big%=0 (re-triggered). Guard ON.

## Last validated work
- **cycle_20260521_0000** (this): BSC universe blind-spot exposed (332 trades silently excluded since cycle_1639 by `!startsWith('0x')`). **H_BSC_BC_FULL** (`chain=bsc AND bonding_curve_buyers.length≥16`): best-fire n=45 avg=+75.6 WR=33 rug=29 **big=13.3% huge=2.2%** — strongest descriptive cohort yet, catches 6/6 BSC bigs. Walk-forward TEST n=9 avg=-50 big=0 → FAILS (temporal clustering of bigs in VAL). bonding_curve_buyers confirmed BSC-only (0/4475 Sol, 332/332 BSC) — closes cycle_1639+ pending. SNIPER_A vs B BSC trail differential 55pp (mirrors cycle_1800 MC_LIQ finding). See [cycle_20260521_0000.md](insights/cycle_20260521_0000.md).
- **cycle_20260520_1800**: H_V3 borderline-fail (TEST Er=-0.031, catches 4/4 best-fire Sol bigs).

## Top candidates
- **H_BSC_BC_FULL** (NEW, descriptive): re-test trigger = 2-4 cycles more BSC data → 05-20 cluster rolls into TRAIN/VAL, TEST gets fresh window.
- **H_V3** (Sol, carried): n=1 first-fire big now, re-test waiting for 2+ new bigs.
- **H_SMART_CLUSTER_VETO** (Sol, defensive): production-feasibility owed.

## Planned next cycle
1. Re-run H_BSC_BC_FULL when BSC data has rolled past the 05-20 cluster.
2. **Cross-chain partition at every cycle start**: `chain × stream × paper` table on last100 — catches universe-scoping blind-spots.
3. Investigate BSC A vs B trail differential (-62.8 vs -7.2 on same 97 tokens).
4. Sol regime monitoring + H_V3 re-test queued for 2nd Sol big.
5. CARRIED: H_SMART_CLUSTER_VETO feasibility, H_TG_AS_EXIT instrumentation, rugger_blacklist `wallet_added_at`.

## OPEN QUESTIONS to user
1. **CRITICAL NEW**: BSC trades all `paper=false` (real money) — intentional? Live positions? 6 bigs (+288..+1268%).
2. **NEW**: BSC production stream = SNIPER_A (avg -62.8) or B (avg -7.2)? Determines whether H_BSC_BC_FULL is reachable.
3. **NEW**: `bonding_curve_buyers` returns max 20 — hard API cap or natural ceiling? Affects bc≥16 vs bc=20 interpretation.
4. CARRYING: MC_LIQ vs A (Sol, 1800); H_V3 "shadow paper" tier; H_SMART_CLUSTER_VETO entry-vs-exit; Track A re-scope; regime-guard sniper patch; H_TG_AS_EXIT; rugger_blacklist timestamps.

## Leakage catalogue (5 forms unchanged): hindsight classifier · counting inflation · time-localization · post-entry feature · stale classifier DB.
**NEW (0000)**: **universe-scoping blind-spot** — silent subset restriction (e.g. chain=solana) without probing excluded universe. Not a leakage form; **missed signal**. Prevention: partition chain×stream×paper before deeper analysis.

## Methodology notes
- state.json ~5000-cap rolling; HISTORY.md durable. Identify tokens by `token` mint, NEVER symbol. Best-fire=upside; first-fire=production. Walk-forward can fail via temporal fat-tail clustering — re-test when cluster rolls into TRAIN/VAL.

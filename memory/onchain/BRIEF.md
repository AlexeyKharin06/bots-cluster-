# BRIEF — onchain AI brain (last update: cycle 20260520_1800)

## Current state (live)
- closed=4888 / Solana=4627 rows / **561 unique tokens** per-token dedup. Rotating ~10/cycle.
- **last50 best-fire avg=-43.8% WR=22% rug=40% big=2.00%** — both H_REGIME_GUARD conditions clear simultaneously for the first time since the 05-18 collapse.
- last100 -48.6%/21/46/1.00. Span 2026-05-17T21:51Z → 05-20T17:44Z (2.83 days).
- **4 best-fire bigs**: PIGEON +3699 (huge), RONALDO +436 (NEW; SNIPER_MC_LIQ; SNIPER_A only 184), MTFR +256, Together +153 (SMART_COPY; SNIPER_A only 75).
- Last big = RONALDO @ 2026-05-20T15:41Z (~2h ago).

## Goal
**+1,000,000% (×10K)** via fat-tail compounding. Gate: **GATE_EXPECTANCY_KELLY** (TEST n≥20, Er>0, Kelly≥0.05, geom≥1%/trade).

## Paper streams in flight
**NONE.** No hypothesis passed gate this cycle (H_V3 borderline-fail).

## Regime status
- Cond A (rolling-50 avg<-55%): **CLEAR** (-43.8). Cond B (big%=0 ≥24h): **CLEAR** (RONALDO). Guard OFF.
- **Caveat**: cycle_1200→1328 was a similar partial clear that head-faked. Opportunistic, not confirmed. Re-trigger in next 1-2 cycles = head-fake.

## Last validated work
- **cycle_20260520_1800** (this): regime BOTH CLEAR; H_DEDUP_BEST_STREAM_BIG_ATTR executed (4 bigs revealed vs 3 first-fire); **H_BIG_WINNER_SHAPE_V3** (known≥11 smart≥2 liq≥17K unlocked top1≥85) catches 4/4 bigs, TRAIN n=44 Er=+0.449 K=0.03 geom=+0.49%, **TEST n=26 avg=-3.1 WR=50 rug=31 big=7.69% Er=-0.031 K=0 — BORDERLINE FAIL gate by ~3pp**. See [cycle_20260520_1800.md](insights/cycle_20260520_1800.md).
- **cycle_1328**: H_SMART_CLUSTER_VETO clean walk-forward NEG (92/100/100% rug TRAIN/VAL/TEST n=41); per-stream Track A audit NEGATIVE.
- **cycle_1200**: H_BIG_WINNER_SHAPE original proposed (3/3 first-fire bigs, TEST big=0); anti-fat-tail lesson on H_DISTRIB/H_LOCKED/H_QUIET/H_FAT_HUNTER.

## Top candidate (descriptive)
**H_BIG_WINNER_SHAPE_V3** — `known≥11 ∧ smart≥2 ∧ liq≥17K ∧ lp_unlocked=true ∧ top1≥85`. Best-fire walk-forward: TRAIN n=44 Er=+0.449 K=0.03; VAL n=20 Er=-0.786; TEST n=26 Er=-0.031 K=0 big=7.69. Captures 4/4 best-fire bigs. One more huge → Kelly>0. **Realism gap**: live = 3/4 on SNIPER_A first-fire. Next cycle re-run on first-fire pnl.

## Top candidate (defensive)
**H_SMART_CLUSTER_VETO** (1328): SMART_CLUSTER ∈ stream-fire-set → abandon. 92/100/100% rug TRAIN/VAL/TEST n=41. Entry-side vs exit-side deployment owed.

## Planned for next cycle
1. **Re-run H_V3 walk-forward on FIRST-FIRE pnl** (production-realistic). If TEST avg/big still beats baseline, propose paper at size=$1.
2. Monitor regime stability (1-2 cycles → confirm or head-fake).
3. Investigate SNIPER_MC_LIQ trail/exit differential vs SNIPER_A (RONALDO 184→436 is the largest first→best gap observed; could be zero-cost upgrade for H_V3 tokens).
4. H_SMART_CLUSTER_VETO production-feasibility check — still owed.
5. Carrying: pumpfun_monitor + dexscreener_signals null-check, bonding_curve_buyers field.

## OPEN QUESTIONS to user
1. **NEW (1800)**: SNIPER_MC_LIQ trail/exit vs SNIPER_A — RONALDO 184→436 is largest first→best gap. Small param delta? Zero-cost upgrade for H_V3 routing.
2. **NEW (1800)**: H_V3 borderline gate-fail (TEST Er=-0.031). Worth "shadow paper" tier? First hypothesis catching all known bigs + positive TRAIN Kelly.
3. CARRYING: H_SMART_CLUSTER_VETO entry-side vs exit-side deployment (1328); Track A re-scope to Kelly-sized regime exposure (1328); regime-guard PATCH for serial_sniper.js + macro 05-18T10:51Z context (0000); H_TG_AS_EXIT instrumentation (1826); rugger_blacklist `wallet_added_at` (1702); SMART_COPY duplicate metrics + ULTRA_TRIPLE/H2 filter logic (1800-orig).

## Leakage catalogue (5 forms, unchanged this cycle)
Hindsight classifier · counting inflation · time-localization artifact · post-entry feature · stale classifier DB with reactive updates.

**Methodology note (cycle_1800)**: best-fire dedup = *measurement* not deployment. Production enters on first-fire. H_V3 4/4 is theoretical; live = 3/4 unless MC_LIQ trail wired onto SNIPER_A. Deployment-realism gap, NOT leakage.

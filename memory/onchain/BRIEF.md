# BRIEF — onchain AI brain (cycle 20260523_1200)

## State (live, rolling ~38h)
- closed=**4883** (-64 vs c0600=4947 — rotation > new closes). Sol uniq **560 (-5)**. BSC uniq **134 (-6, includes MEMEWC+PEDUCK aged out)**. **25 open positions (-26 vs c0600=51)** — closing rapidly.
- **2 NEW BSC bigs in 6h** (C7 PRODUCTIVE): **RICH +847 SNIPER_B k=2 PORTUGAL** (06:44), + near-bigs **WOJCUP +136 k=1 PORTUGAL** (06:17) and **MARSCITY +146 k=115 broader-wave BF=SNIPER_BSC_FILTERED!** (10:00).
- **ELON -86 (11:25) = 2nd PORTUGAL rug** ever (after CTM C4). PORTUGAL rug-floor ~17%.
- Sol: 0 new bigs. FATU gap 30.5h (Cond B firmly TRIGGERED).

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade). Paper streams: **NONE deployed**; PAPER_BSC_TG2 headline candidate (gate-passing despite weakening).

## Regime
- **Cond A**: oscillating, currently CLEAR (-47.8) but volatile (briefly hit -70 mid-cycle then recovered to -36).
- **Cond B**: **TRIGGERED** (FATU 30.5h gap > 24h threshold).
- **Guard ON via Cond B alone.**

## Last validated
- **c1200-day2 (this)**: **C7 productive — RICH +847 BIG (PORTUGAL k=2 at 06:44, 6h40min after BabyAsteroid onset)**. H_CLUSTER_PORTUGAL_PRESENCE re-confirmed (5/7 cluster productivity). TG-2h TEST n=31 K=0.127 geom=+4.31% big%=19.4% **STILL GATE-PASSING**; weakened c0600→c1200 partly due to state.json rotation (MEMEWC+PEDUCK aged out — lost +179, +908 anchors). C7 PORTUGAL big-rate 17% (1/6) is weakest productive cluster observed (vs C3/C5=100%, C6=67%) — watch alpha cooling. **NEW Methodology Lesson #9 candidate**: state-window rotation bias systematically drags cross-cycle TEST stats. See [cycle_20260523_1200.md](insights/cycle_20260523_1200.md).
- **c0600-day2**: TG-2h DETHRONES TG-3h. C7 with 2 PORTUGAL +33/+109 but 0 bigs — partial-falsification stress test (resolved POSITIVELY this cycle).
- **c0000-day2**: H_BSC_BC_TIME_GATED_PORTUGAL_3H NEW headline.

## Top candidates
- **H_BSC_BC_TIME_GATED_PORTUGAL_2H** (HEADLINE, still gate-passing): TEST n=31 K=0.127 geom=+4.31% big=19.4% rug=29 — 6/6 currently-visible bigs caught. Routing {B,F2,D2,A,H}. Spec: bc≥16 ∩ (k≤10 OR within 2h of prior bc≥16∩k≤10).
- **H_BSC_BC_PORTUGAL** (strict k≤10): TEST n=12 K=0.268 geom=+36.22% big=41.7. 8 more PORTUGAL entries needed for n≥20 floor.
- **H_BSC_BC_FULL_B** (DEMOTED): TEST n=55 K=0.101 geom=+1.60% — barely above gate. Descriptive-only.
- **H_CLUSTER_PORTUGAL_PRESENCE**: re-confirmed 5/7 productive clusters; lag-to-first-big now wider distribution (0-400min).
- **H_PORTUGAL_RUG_FLOOR**: NEW descriptive ~17% rug rate on PORTUGAL TEST (2/12).
- **H_CLUSTER_TIME_OF_DAY**: DEMOTED (C7 overnight onset broke pattern).

## Methodology — 8 leakage forms + macro modes + NEW #9 candidate
1. Hindsight classifier · 2. Counting inflation · 3. Time-localization · 4. Post-entry feature · 5. Stale classifier DB · 6. Single-cluster artifact · 7. Percentile-redraw boundary drift · 8. (regime-context separation).
**NEW #9 candidate**: state.json rolling-window rotation biases TEST stats downward over time as oldest fat-tail bigs rotate out while dormant tails accumulate. Flag rotation events when reporting cross-cycle weakening.

Best-fire=upside; first-fire=production. Cross-cluster ≥3 events mandatory. FIXED TEST boundary mandatory. SNIPER_BSC_FILTERED anti-fat-tail (MARSCITY anomaly noted, n=1). Variance-Kelly preferred.

## Planned next cycle
1. **C7 wind-down monitoring** (does C7 produce another big after RICH? ELON-rug suggests winding down).
2. C8 detection (next PORTUGAL bc≥16∩k≤10 onset after >3h gap).
3. TG-2h forward validation target n≥40 (currently 31).
4. Sol Cond A re-trigger watch (-47.8 vs -55 threshold).
5. Sol Cond B duration tracking (30.5h and counting).
6. PAPER_BSC_TG2 deterministic spec doc if approved.
7. Methodology #9 formalization — adopt rotation-flag in cross-cycle reporting.
8. PORTUGAL alpha cooling watch (C7 big-rate 17% lowest yet; track C8).
9. CARRIED: SMART_CLUSTER_VETO, MC_LIQ review, PORTUGAL creator wallet audit (WORLDCUP/WORLDCUP-2/WOJCUP shared creator?), External BSC volume fetcher.

## OPEN QUESTIONS to user
1. **PAPER_BSC_TG2 deploy approval (UNCHANGED HEADLINE, still gate-passing)**: TEST n=31 K=0.127 geom=+4.31% big=19.4% rug=29% — weakened from c0600 partly due to state-window rotation (MEMEWC+PEDUCK aged off), partly C7 dilution; catches 6/6 currently-visible TEST bigs. Routing {B,F2,D2,A,H}. Spec: bc≥16 ∩ (k≤10 OR within 2h of prior bc≥16∩k≤10). Auto-stop K<0.05 after 30 OR cum<0 after 50 OR 10-streak no-big avg<-30%. $1 paper.
2. **PAPER_BSC_PORTUGAL strict (k≤10) parallel?** n=12 (was 8) K=0.268 geom=+36.22% — still sub-floor on n=20. Brain leans wait.
3. **Methodology #9 adoption** — track state.json rotation events in BRIEF cross-cycle reports? ~10min/cycle overhead.
4. CARRIED: External BSC chain-volume fetcher (~2h); PORTUGAL-family creator wallet audit (~1h); SMART_CLUSTER_VETO; rugger_blacklist `wallet_added_at`; MC_LIQ vs SNIPER_A code review.

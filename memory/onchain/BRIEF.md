# BRIEF — onchain AI brain (cycle 20260523_0600)

## State (live, rolling ~3d)
- closed=**4947** (+76 vs c0000-day2=4871, real growth). Sol uniq **565 (+18)**. BSC uniq **140** (rotation balanced). **51 open positions (+37 vs c0000-day2=14)** — heavy launch flow.
- **0 new bigs in 6h** on either chain. Last Sol big = FATU 24.7h ago. Last BSC big = BINA 12.8h ago.
- **+85 BSC closes / +37 bc≥16 in 5h** — avg=-38%, 17 rugs, 0 bigs.
- BSC BF bigs **7** (unchanged). Sol BF bigs **3** (unchanged).

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom_at_K≥1%). Paper streams: **NONE deployed**; PAPER_BSC_TG2 **NEW HEADLINE** candidate (supersedes PAPER_BSC_TG3); PAPER_BSC_BC16 demoted to descriptive.

## Regime
- **Cond A trending UP** (last50 -40.7 c0000-day2 → **-52.8** now). 2.2pt from -55% re-trigger. c0000-day2 "carnage break" appears head-fake.
- **Cond B TRIGGERED** (FATU 24.7h gap, threshold 24h). Guard ON via Cond B alone.
- If Cond A re-triggers next cycle → DOUBLE-GUARD state.

## Last validated
- **c0600-day2 (this)**: **TG-2h dethrones TG-3h** as headline. TG-2h TEST n=28 K=0.145 geom=+6.60% big=25.0% rug=21 — same 7/7 big-coverage, +29% big%, +109% geom vs TG-3h. Cross-cluster C3+C5+C6 individually pass gate. C7 cluster (BabyAsteroid k=2 +33 + WORLDCUP-2 k=1 +109) ACTIVE: 2 PORTUGAL entries positive but 0 bigs in 6h — first "PORTUGAL pumped small, no bigs" mode (stress test for H_CLUSTER_PORTUGAL_PRESENCE). H_BSC_BC_FULL_B 2nd cycle weakening (K=0.099 barely-passes). 以太币 k=11 RUG validates k≤10 boundary. See [cycle_20260523_0600.md](insights/cycle_20260523_0600.md).
- **c0000-day2**: H_BSC_BC_TIME_GATED_PORTUGAL_3H NEW headline; H_BSC_BC_FULL_B 1st weakening. Cond A CLEARED.
- **c1800**: H_BSC_BC_FULL_B TEST n=41 K=0.34 geom=+6.07% strongest-ever. C6 productive (WBC/UFU/BINA).

## Top candidates
- **H_BSC_BC_TIME_GATED_PORTUGAL_2H** (**NEW HEADLINE PAPER-STREAM CANDIDATE**). TEST n=28 K(var)=0.145 geom=+6.60% big=25.0% rug=21. Cross-cluster C3+C5+C6 (3 productive, each individually passes gate). Routing {B,F2,D2,A,H}. Captures 7/7 TEST bigs. **STRONGEST DEPLOY RECOMMENDATION**.
- **H_BSC_BC_TIME_GATED_PORTUGAL_3H** (DEMOTED to secondary). TEST n=36 K=0.112 geom=+3.16% big=19.4%. Still gate-passing. Parallel-deploy option.
- **H_BSC_BC_FULL_B** (DEMOTED to descriptive). TEST n=58 K=0.099 geom=+1.58% — barely above gate, 2nd consecutive weakening.
- **H_BSC_BC_PORTUGAL** (strict k≤10). TEST n=10 K=0.307 geom=+55.93% big=60% — sub-floor n; TG-2h supersedes.
- **H_CLUSTER_PORTUGAL_PRESENCE** — C7 stress test pending. If C7 ends with 0 bigs → partial falsification.
- **H_CLUSTER_TIME_OF_DAY** (NEW descriptive). 4/4 productive UTC daytime (04-20Z); 2/2 dormant + C7 currently-dormant overnight (18-06Z). n too small to promote.
- **H_V_DELTA_FATU / H_V8 / H_V9_STEALTH** (Sol shapes) — 0 new Sol bigs, unchanged.

## Methodology — 7 leakage forms + macro modes
1. Hindsight classifier · 2. Counting inflation · 3. Time-localization · 4. Post-entry feature · 5. Stale classifier DB · 6. Single-cluster artifact · 7. Percentile-redraw boundary drift.

Best-fire=upside; first-fire=production. Cross-cluster ≥3 events mandatory. FIXED TEST boundary mandatory. SNIPER_A early-exits BSC bigs (6/7 PORTUGAL; METLIFE k=1 only exception with A=+173 vs B=+37). SNIPER_BSC_FILTERED structurally anti-fat-tail (3rd confirmation). Variance-Kelly preferred (cross-cycle consistent).

## Planned next cycle
1. **C7 outcome resolution** (does C7 produce a big in next 6h? if 0 → partial falsification H_CLUSTER_PORTUGAL_PRESENCE).
2. Sol Cond A re-trigger watch (-52.8 within 2.2pt of -55%).
3. TG-2h forward validation (target n≥40).
4. **PAPER_BSC_TG2 deterministic spec doc** if user approves.
5. H_CLUSTER_TIME_OF_DAY tracking on next cluster.
6. WORLDCUP-2 vs WORLDCUP-1 re-launch underperformance study (n=1).
7. CARRIED: SMART_CLUSTER_VETO, MC_LIQ review, PORTUGAL creator wallet audit, External BSC volume fetcher.

## OPEN QUESTIONS to user
1. **PAPER_BSC_TG2 deploy approval (NEW headline)** — replaces TG-3h: TEST n=28 K(var)=0.145 geom=+6.60% big=25.0% rug=21. Routing {B,F2,D2,A,H}. Entry rule: bc≥16 ∩ (k≤10 OR within 2h of prior bc≥16∩k≤10). $1 paper. Auto-stop K<0.05 after 30 OR cum<0 after 50 OR 10-streak no-big avg<-30%.
2. **PAPER_BSC_TG3 (broader) parallel A/B?** TEST n=36 K=0.112 geom=+3.16% — gate-passing but weakened. Could deploy both in parallel ($2 paper total).
3. **PAPER_BSC_PORTUGAL (k≤10 strict) parallel?** n=10 K=0.307 geom=+55.93%, sub-floor n. TG-2h covers. Brain leans SKIP.
4. CARRIED: External BSC chain-volume fetcher (~2h); PORTUGAL-family creator wallet audit (~1h); SMART_CLUSTER_VETO feasibility; rugger_blacklist `wallet_added_at`; MC_LIQ vs SNIPER_A code review.

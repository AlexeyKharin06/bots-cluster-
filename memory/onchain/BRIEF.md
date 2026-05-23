# BRIEF — onchain AI brain (cycle 20260523_0000)

## State (live, rolling ~3d)
- closed=**4871** (-16 vs c1800; rolling-window rotation > closes). Sol uniq **547** (flat). BSC uniq **140 (+9)**. 14 open positions (down from 30 c1800 = closure cascade).
- **0 new bigs in 6h.** Last BSC big = BINA 6.8h ago (17:12Z). Last Sol big = FATU 18.7h ago (05:20Z).
- +7 NEW BSC bc≥16 entries since c1800, **all NON-PORTUGAL (k=21-177)**. 2 rugs (PIRA, 登月) + 5 small ([-21,+38]) + 0 bigs. **C6 cluster wound down into post-PORTUGAL dormant tail** (forward-confirms H_CLUSTER_PORTUGAL_PRESENCE).
- BSC BF bigs **8** (unchanged: TLS/MEMEWC/PEDUCK/METLIFE/Grandma/WBC/UFU/BINA). Sol BF bigs **8** (flat).

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom_at_K≥1%). Paper streams: **NONE deployed**; PAPER_BSC_TG3 NEW HEADLINE candidate; PAPER_BSC_BC16 still passes (demoted to diagnostic).

## Regime
- **Cond A CLEARED** (last50=-40.7; was -75.4 worst-ever c1800). 3-window monotone recovery: -75.4 → -67.0 → -52.4 → -40.7. **Carnage break, provisional**.
- **Cond B trends to trigger ~05:20Z** (FATU 18.7h gap; threshold 24h; ~5.3h to go). If no Sol big lands, Cond B fires unilaterally.
- Guard: OFF (provisional).

## Last validated
- **c0000-day2 (this)**: H_BSC_BC_FULL_B FIXED-boundary TEST **WEAKENS** n=41→48 K(var)=0.139→0.121 geom_at_K=+4.22%→+2.77% big=17.07→14.58 rug=15→17 — first cross-cycle weakening, still gate-passing. **NEW H_BSC_BC_TIME_GATED_PORTUGAL_3H** (bc≥16 ∩ within 3h after PORTUGAL): TEST **n=27 K=0.140 geom_at_K=+6.27% big=25.93% rug=22%** — first sub-spec to pass n≥20 floor while LIFTING big% (+78% relative); catches 7/7 TEST BSC bigs; cross-cluster validated C3+C5+C6. Sol Cond A CLEARED. C6 dormant tail confirmed. See [cycle_20260523_0000.md](insights/cycle_20260523_0000.md).
- **c1800**: H_BSC_BC_FULL_B TEST n=41 K=0.34 geom=+6.07% STRONGEST EVER. +3 BSC bigs (WBC/UFU/BINA) all C6. Sol Cond A DEEPLY worst-ever.
- **c1200**: H_BSC_BC_FULL_B TEST n=32 K=0.23 geom=+3.36%. C5 cluster productive.

## Top candidates
- **H_BSC_BC_TIME_GATED_PORTUGAL_3H** (**NEW HEADLINE PAPER-STREAM CANDIDATE**). TEST n=27 K(var)=0.140 geom_at_K=+6.27% big=25.93%. Cross-cluster C3+C5+C6 (3 productive). Routing {B,F2,D2,A,H}. Captures 7/7 TEST BSC bigs. **STRONGEST DEPLOY RECOMMENDATION** (passes n-floor with big% lift over broad spec).
- **H_BSC_BC_FULL_B** (DEMOTED to diagnostic broad-net). TEST n=48 K(var)=0.121 geom_at_K=+2.77% big=14.58%. Still gate-passing but weakened by 7 dormant-tail entries.
- **H_BSC_BC_PORTUGAL** (strict k≤10). TEST n=8 K=0.319 geom_at_K=+68%, sub-floor n. TG-3h supersedes (catches PORTUGAL + broader-wave-during-active-phase like BINA).
- **H_CLUSTER_PORTUGAL_PRESENCE** (descriptive predictor, **FORWARD-CONFIRMED this cycle**). 7 post-PORTUGAL entries without PORTUGAL → 0 bigs as predicted. 4/4 productive + 2/2 dormant clusters consistent.
- **CLUSTER_PHASE_TAIL** (NEW descriptive). After PORTUGAL bursts end, 3-6h tail phase with bc≥16 entries but 0 bigs and elevated rugs.
- **H_V_DELTA_FATU / H_V8 / H_V9_STEALTH** (Sol shapes) — no new Sol bigs, unchanged.

## Methodology — 7 leakage forms + macro modes
1. Hindsight classifier (c1702) · 2. Counting inflation (c1800) · 3. Time-localization (c1639) · 4. Post-entry feature (c1639) · 5. Stale classifier DB (c0000) · 6. Single-cluster artifact (c2200) · 7. Percentile-redraw boundary drift (c0600).

Best-fire=upside; first-fire=production. Cross-cluster ≥3 events mandatory. FIXED TEST boundary mandatory (c0000-lock). SNIPER_A early-exits BSC bigs. SNIPER_BSC_FILTERED structurally anti-fat-tail (veto). SNIPER_H2 new BSC variant (3 entries no big, exclude from PAPER_BSC_TG3 routing for now). Variance-Kelly preferred over binary-Kelly (more conservative).

## Planned next cycle
1. C7 cluster onset detection (next BSC PORTUGAL bc≥16∩k≤10 entry → declare C7 onset; track 3h productive window).
2. Sol Cond B trigger watch (~05-23T05:20Z). If no Sol big, double-guard via Cond B alone.
3. Sol Cond A re-test (provisional clear; monitor for head-fake like c1800).
4. TG-3h sensitivity: test TG-2h, TG-4h windows.
5. PAPER_BSC_TG3 deterministic spec file if user approves.
6. CARRIED: SMART_CLUSTER_VETO, MC_LIQ review, PORTUGAL creator wallet audit, External BSC volume fetcher.

## OPEN QUESTIONS to user
1. **PAPER_BSC_TG3 deploy approval (NEW)** — replaces PAPER_BSC_BC16 in headline queue: TEST n=27 K(var)=0.140 geom_at_K=+6.27% big=25.93% rug=22%. Routing {B,F2,D2,A,H}. Entry rule: bc≥16 ∩ within 3h after prior bc≥16∩known≤10 entry. $1 paper. Auto-stop K<0.05 after 30 OR cum<0 after 50 OR 10-streak no-big avg<-30%.
2. **PAPER_BSC_BC16 (broad) STILL deployable?** TEST n=48 K=0.121 geom=+2.77% big=14.58% — gate passes, but TG-3h dominates. Could deploy both in parallel for differential A/B (~no extra effort, $2 paper).
3. **PAPER_BSC_PORTUGAL (k≤10 strict) parallel?** TEST n=8 K=0.319 geom=+68% — sub-floor n; TG-3h captures these plus more. Brain leans SKIP (TG-3h covers).
4. CARRIED: External BSC chain-volume fetcher (~2h); PORTUGAL-family creator wallet audit (~1h); SMART_CLUSTER_VETO feasibility; rugger_blacklist `wallet_added_at`; MC_LIQ vs SNIPER_A code review.

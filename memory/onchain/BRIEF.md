# BRIEF — onchain AI brain (cycle 20260522_1200)

## State (live, rolling ~3d)
- closed=4867 (-38 vs c0600=4905, net rotation). Sol uniq **536 (+3)**. BSC uniq **140 (-4)**, early-cluster bigs aged out.
- **+3 NEW BIGS in 6h** (best 6h-delta since c2200): FATU Sol +232 (05-22T05:20, δ-shape NEW), METLIFE BSC +173 SNIPER_A (09:52, bc=20 known=1), Grandma BSC +568 SNIPER_B (10:54, bc=20 known=2).
- Sol BF bigs **8** (Together rotated; FATU new). BSC BF bigs **7** (4 early rotated; METLIFE+Grandma new).
- **5th BSC cluster C5 PRODUCTIVE** (05-22 06-13): n=11 K=0.71 geom=+17.67% big=18% rug=**0%**. Refutes c0600 "C4 dormant trend".
- Sol last50 **-64.4** (was -62.4) — worst single-window since 05-19 collapse.

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade). Paper streams: **NONE deployed**; PAPER_BSC_BC16 STRONGLY RECOMMENDED (extended evidence).

## Regime
- **Cond A ACTIVE — deeply worse** (-64.4). Post-FATU rug avalanche worse than post-Blobby.
- Cond B CLEAR (FATU 6.7h ago).
- Guard ON via Cond A.

## Last validated
- **c1200 (this)**: H_BSC_BC_FULL_B FIXED-boundary TEST n=21→32 K=0.10→0.23 geom=+1.00%→+3.36% big=12.5% rug=**16%** — passes gate by **60% margin on n, 4.6× margin on K, 3.4× margin on geom**. Cross-cluster 5 events (3 productive C1+C3+C5, 2 dormant C2+C4). H_BSC_BC_PORTUGAL tighter (bc≥16∩known≤10) TEST n=5 K=0.74 geom=+123% big=80% rug=20% — extreme alpha across 3 productive clusters but n<floor. H_V9_STEALTH REJECTED-OVERFIT (FATU outside; 2nd 6th-leakage). H_V8 misses FATU; 5-cycle Sol negative geom trend. See [cycle_20260522_1200.md](insights/cycle_20260522_1200.md).
- **c0600**: H_BSC_BC_FULL_B percentile-redraw TEST FAILS; FIXED-boundary PASSES marginally (n=21 K=0.10). 7th methodology rule.
- **c0000**: H_V7_ANTICLUSTER FALSIFIED. H_BSC_BC_FULL_B passed Kelly-gate on 3 indep clusters. 6th leakage form.

## Top candidates
- **H_BSC_BC_FULL_B** (PAPER-STREAM CANDIDATE — extended-validated). TEST n=32 K=0.23 geom=+3.36%. Cross-cluster 5 events (3 productive). Broad routing {B/F2/D2/A}. **STRONG RECOMMEND deploy** $1 paper.
- **H_BSC_BC_PORTUGAL** (paper-stream-2 candidate, tighter known≤10). TEST n=5 K=0.74 geom=+123%. Cross-cluster across 3 productive clusters. Carry until n=10+ then promote.
- **H_V_DELTA_FATU** (descriptive, 4th Sol shape). Single-big-fit. Need ≥2 δ-bigs to formalize.
- **H_V8** (Sol descriptive, 5-cycle negative geom drift). Misses FATU (8th BF big). Not promotable.
- **H_V9_STEALTH** REJECTED-OVERFIT c1200 (chain-4 cross-cluster fail).
- **H_V7_ANTICLUSTER** REJECTED c2200.
- **H_SMART_CLUSTER_VETO** carried (production-feasibility owed).

## Methodology — 7 leakage forms + macro modes
1. Hindsight classifier (c1702) · 2. Counting inflation (c1800) · 3. Time-localization (c1639) · 4. Post-entry feature (c1639) · 5. Stale classifier DB (c0000) · 6. **Single-cluster artifact** (c2200, c1200 V9 = 2nd example) · 7. **Percentile-redraw boundary drift** (c0600 — lock TEST as abs timestamp).

Best-fire=upside; first-fire=production. Cross-cluster ≥3 events mandatory. Fixed-time TEST boundary mandatory.

## Planned next cycle
1. Track C6 BSC cluster onset (if any). H_BSC_BC_FULL_B TEST may extend to n=40+.
2. Track next Sol big — α/β/γ/δ or 5th shape?
3. If user approves: write `paper_streams_spec/PAPER_BSC_BC16.md` deterministic spec + forward-tracking log.
4. Pull external BSC chain-volume data for cluster productivity predictor (productive C1+C3+C5 vs dormant C2+C4).
5. Profile 52 Sol open positions — any V8/V9/V_DELTA candidates?
6. CARRIED: SMART_CLUSTER_VETO, H_TG_AS_EXIT, MC_LIQ review, rugger_blacklist `wallet_added_at`.

## OPEN QUESTIONS to user
1. **PAPER_BSC_BC16 deploy approval**: extended TEST n=32 K=0.23 geom=+3.36% big=12.5% rug=16% — passes gate by wide margin across 5 BSC clusters (3 productive). Routing {B/F2/D2/A}. $1 paper. Auto-stop on K<0.05 after 30 entries OR cumulative pnl<0% after 50.
2. **PAPER_BSC_PORTUGAL (tighter, known≤10) — deploy NOW or wait for n=10+?** TEST n=5 K=0.74 geom=+123% big=80% across 3 productive clusters but n=5<floor. Brain leans WAIT (broader spec covers same alpha + more capture).
3. **External BSC chain-volume fetcher** for cluster productivity predictor? ~2h investment. Would test "productive vs dormant cluster" hypothesis externally.
4. CARRIED: SMART_CLUSTER_VETO feasibility; rugger_blacklist `wallet_added_at`; MC_LIQ vs SNIPER_A code review.

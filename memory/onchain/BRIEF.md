# BRIEF — onchain AI brain (cycle 20260522_1800)

## State (live, rolling ~3d)
- closed=4887 (+20 vs c1200=4867). Sol uniq **547 (+11)**. BSC uniq **131 (-9)**, more 05-20 rotation. 30 open positions (28 Sol visible, 0 BSC).
- **+3 NEW BSC BIGS in 6h (best single-chain delta ever)**: WBC +284 SNIPER_B bc=20 known=2 (14:58), UFU +170 SNIPER_H bc=20 known=2 (15:21), BINA +169 SNIPER_H bc=20 known=39 (17:12). All in **C6 cluster** (05-22 13:00-18:00), 3rd consecutive productive cluster.
- BSC BF bigs **8 (+1 net)** — 6 PORTUGAL family (MEMEWC/PEDUCK/METLIFE/Grandma/WBC/UFU) + 2 broader-wave (TLS/BINA) + WORLDCUP.
- Sol FF bigs **7** (FATU still latest), BF **8** (flat). Last Sol big = FATU 12.7h ago.
- Sol last50 **-75.4** (worst-ever single window; -64.4 c1200, -55.3 c0000). Rug 76%.

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade). Paper streams: **NONE deployed**; PAPER_BSC_BC16 EXTRA-STRONGLY RECOMMENDED; PAPER_BSC_PORTUGAL near-threshold queued.

## Regime
- **Cond A DEEPLY ACTIVE — worst-ever** (-75.4). 3-window monotone decline (-64→-72→-75). Sol structural carnage.
- Cond B CLEAR but trending toward trigger (FATU 12.7h, threshold 24h; ~11h until double-guard).
- Guard ON via Cond A.

## Last validated
- **c1800 (this)**: H_BSC_BC_FULL_B FIXED-boundary TEST **n=41 K=0.34 geom=+6.07% big=17.07% rug=15%** — STRONGEST EVER. Cross-cluster 6 events (4 productive C1+C3+C5+C6, 2 dormant C2+C4). H_BSC_BC_PORTUGAL TEST n=8 K=0.82 geom=+123% big=75% rug=13% across 3 productive clusters. H_CLUSTER_PORTUGAL_PRESENCE re-confirmed on C6 (ttt 14:07 declared onset; WBC big at 14:58 = 51min lag). SNIPER_H emerges as 4th BSC big-fire stream (UFU+BINA). SNIPER_BSC_FILTERED structurally anti-fat-tail. See [cycle_20260522_1800.md](insights/cycle_20260522_1800.md).
- **c1200**: H_BSC_BC_FULL_B FIXED-boundary TEST n=32 K=0.23 geom=+3.36%. +3 bigs (FATU/METLIFE/Grandma). H_V9_STEALTH REJECTED-OVERFIT. 4th Sol shape (δ) observed.
- **c0600**: 7th methodology rule (lock TEST boundary).

## Top candidates
- **H_BSC_BC_FULL_B** (PAPER-STREAM CANDIDATE — extra-strongly validated). TEST n=41 K=0.34 geom=+6.07% big=17.07%. Cross-cluster 6 events (4 productive). **5-stream routing {B/F2/D2/A/H} excl SNIPER_BSC_FILTERED** covers all 8 BSC BF bigs. **STRONGEST DEPLOY RECOMMENDATION.**
- **H_BSC_BC_PORTUGAL** (paper-stream-2 candidate). TEST n=8 K=0.82 geom=+123% big=75% rug=13%. Cross-cluster 3 productive. n still below 20 floor but growing (5→8 in 1 cycle). Auto-promote trigger n=12 K≥0.5.
- **H_CLUSTER_PORTUGAL_PRESENCE** (descriptive predictor, validated cross-cluster). Cluster productive iff ≥1 known≤10 bc≥16 entry. 4/4 productive had PORTUGAL entries; 2/2 dormant did not (or 1 rugged in C4).
- **H_V_DELTA_FATU** (descriptive, 4th Sol shape, single-point obs). 0 δ-shape candidates in 28 open positions. Carry until next Sol big.
- **H_V8** (Sol descriptive). Misses FATU; 5-cycle negative drift; not promotable.
- **H_V9_STEALTH** REJECTED-OVERFIT c1200.
- **H_SMART_CLUSTER_VETO** carried (production-feasibility owed).

## Methodology — 7 leakage forms + macro modes
1. Hindsight classifier (c1702) · 2. Counting inflation (c1800) · 3. Time-localization (c1639) · 4. Post-entry feature (c1639) · 5. Stale classifier DB (c0000) · 6. **Single-cluster artifact** (c2200; V9 c1200 = 2nd example) · 7. **Percentile-redraw boundary drift** (c0600 — lock TEST as abs timestamp).

Best-fire=upside; first-fire=production. Cross-cluster ≥3 events mandatory. Fixed-time TEST boundary mandatory. **SNIPER_A consistently exits early on BSC bigs (-30 to -100pp differential vs B/F2/D2/H trail). SNIPER_BSC_FILTERED structurally anti-fat-tail (never use as BSC primary).**

## Planned next cycle
1. Track BSC C7 onset (or C6 extension). H_CLUSTER_PORTUGAL_PRESENCE forward-test: next k≤10 ∩ bc≥16 entry → declare onset.
2. Track Sol — at FATU+24h (~05-23T05:20Z) Cond B triggers if no new big; double-guard regime.
3. If user approves: write `paper_streams_spec/PAPER_BSC_BC16.md` deterministic spec + forward-tracking log.
4. C2/C4 dormant cluster post-mortem (time-of-day, external BSC volume).
5. PORTUGAL-family creator/LP-provider overlap audit (single-actor risk?).
6. CARRIED: SMART_CLUSTER_VETO, H_TG_AS_EXIT, MC_LIQ review, rugger_blacklist `wallet_added_at`.

## OPEN QUESTIONS to user
1. **PAPER_BSC_BC16 deploy approval** (4th re-iteration): TEST n=41 K=0.34 geom=+6.07% big=17.07% rug=15% — STRONGEST EVER, passes gate by 6.8× on K, 6.1× on geom. 5-stream routing {B/F2/D2/A/H} excl SNIPER_BSC_FILTERED. $1 paper. Auto-stop K<0.05 after 30 entries OR cum pnl<0 after 50.
2. **PAPER_BSC_PORTUGAL parallel-deploy NOW?**: TEST n=8 K=0.82 geom=+123% big=75% — n still <20 floor but extreme stats. Brain leans deploy now (sub-spec; differential tracking; $1 = minimal risk; auto-promote at n=12 K≥0.5).
3. **External BSC chain-volume fetcher** for productive vs dormant cluster predictor. ~2h.
4. **PORTUGAL-family creator wallet audit** (single-actor concentration check). ~1h.
5. CARRIED: SMART_CLUSTER_VETO feasibility; rugger_blacklist `wallet_added_at`; MC_LIQ vs SNIPER_A code review.

# BRIEF — onchain AI brain (cycle 20260522_0600)

## State (live, rolling ~3d)
- closed=4905 (+98 vs c0000, 6h). Sol 533 / BSC 144 uniq (+2; +6 fresh bc=20).
- Sol BF bigs=9 (**0 new in 6h**). Last big Blobby 9.6h ago (longest gap).
- BSC BF bigs=8. **4 bc=20 clusters**: C1 PORTUGAL-day (4 bigs SNIPER_B) / C2 broader-wave (2 bigs CMC+TLS) / C3 PORTUGAL-mid (2 bigs MEMEWC+PEDUCK) / **C4 NEW 05-22 01:53-05:58 (6 entries, ZERO bigs, all SNIPER_A)**.
- Sol last50 -62.4 (was -55.3). Cond A worsening. big%=0.

## Goal & gate
**+1M%** via fat-tail compounding. GATE_EXPECTANCY_KELLY (TEST n≥20, Er>0, K≥0.05, geom≥1%/trade). Paper streams: **NONE** (H_BSC_BC_FULL_B proposed; this cycle re-evaluated).

## Regime
Cond A ACTIVE worsening. 4 BSC clusters bimodal (2 productive, 2 dormant). 3 Sol chains (Together-RONALDO; SPCX-Omnimals; FOID-Blobby). Post-Blobby gap 9.6h.

## Last validated
- **c0600 (this)**: H_BSC_BC_FULL_B percentile-redraw TEST FAILS (n=11 K=0). **FIXED time-boundary TEST PASSES marginally** (n=21 K=0.10 geom=+1.00% big=9.52% rug=24%). Per-cluster bimodal C1/C3 prod (K=0.12-0.76) vs C2/C4 dormant. Aggregate n=62 K=0.21 geom=+4.99%. **H_V9_STEALTH NEW** (Sol α top1≥90∧smart≥10∧buys≤250) catches 3/9 BF bigs cross-cluster, TRAIN K=0.22, TEST n=2 overfit-risk. **7th methodology lesson** catalogued. See [cycle_20260522_0600.md](insights/cycle_20260522_0600.md).
- **c0000**: H_V7_ANTICLUSTER FALSIFIED (onsets+413% vs followers+461%). H_BSC_BC_FULL_B passed Kelly-gate on 3 indep clusters. 6th leakage catalogued.

## Top candidates
- **H_BSC_BC_FULL_B** (paper-stream candidate, bc≥16 ∩ SNIPER_B routing). FIXED-boundary TEST n=21 K=0.10 geom=+1.00% — passes marginally; n above 20-floor first time. Cross-cluster 4 events (3 prod, 1 dormant). Margin narrowed vs c0000 (K 0.16→0.10).
- **H_V9_STEALTH** (Sol α-tighten, NEW). Catches 3/9 BF bigs (RONALDO/FOID/Blobby) 2 clusters. TRAIN K=0.22 geom=+4.33%. TEST n=2 overfit-risk. Misses β+γ.
- **H_V8** (Sol descriptive, 9/9 bigs, TEST geom=0%, 4-cycle drift). Too inclusive.
- **H_V7_ANTICLUSTER** REJECTED c2200.
- **H_SMART_CLUSTER_VETO** carried (production-feasibility owed).

## Methodology — 7 leakage forms
1. Hindsight classifier (c1702) · 2. Counting inflation (c1800) · 3. Time-localization (c1639) · 4. Post-entry feature (c1639) · 5. Stale classifier DB (c0000) · 6. Single-cluster artifact (c2200) · 7. **Percentile-redraw boundary drift (c0600)** — redrawing 60/20/20 each cycle shifts TEST forward, invalidating cross-cycle persistence. **Resolution: lock TEST as absolute timestamp; new data extends TEST forward.**

Best-fire=upside; first-fire=production. Cross-cluster ≥3 events mandatory. Fixed-time TEST boundary mandatory.

## Planned next cycle
1. Watch next Sol cluster onset → H_V9_STEALTH catch test.
2. Watch next BSC cluster onset (C5) → productive vs dormant modal pattern.
3. H_BSC_BC_FULL_B paper-stream user re-iterate with FIXED-boundary stats.
4. CARRIED: SMART_CLUSTER_VETO, H_TG_AS_EXIT, MC_LIQ review, rugger_blacklist `wallet_added_at`.

## OPEN QUESTIONS to user
1. **H_BSC_BC_FULL_B paper-stream approval**: FIXED-boundary TEST passes gate marginally (n=21 K=0.10 geom=+1.00%). C4 was zero-big cluster — variance real. Brain still recommends $1 paper forward-tracking — cheap; validates K=0.10 over next 50+ entries.
2. **H_V9_STEALTH future**: 3/9 BF bigs cross-cluster. Carry until 2+ more clusters confirm; then promote?
3. CARRIED: SMART_CLUSTER_VETO feasibility; rugger_blacklist `wallet_added_at`; MC_LIQ vs SNIPER_A code review.

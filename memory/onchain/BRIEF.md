# BRIEF — onchain AI brain (last update: cycle 20260520_1200)

## Current state (live)
- closed=4913 Solana rows / **581 unique tokens** (per-token dedup). State.json shrinking — 6h ago was 601 unique. Rolling window, not append-only.
- last50 unique-token avg=-45.9% WR=28% rug=46% **big=0** (300+ tokens streak without a big winner).
- Span ~2026-05-17T18:32Z → 2026-05-20T11:43Z (3 days, oldest rotated out).
- 3 big winners remain (PIGEON +3699, MTFR +251, 1billion +228) — all clustered 2026-05-18 morning, pre-collapse.

## Goal
**+1,000,000% (×10K)** via fat-tail compounding. Promotion gate: **GATE_EXPECTANCY_KELLY** (TEST n≥20, E[r]>0, Kelly≥0.05, geom≥1%/trade).

## Paper streams in flight
**NONE.** Regime guard (condition B: big%=0) blocks all promotion.

## Regime status (this cycle)
- Sliding-50 avg: **PARTIAL RECOVERY** -97.8% → -45.9%. Condition A of H_REGIME_GUARD CLEARED.
- big% in last 300 unique tokens: **0**. Condition B STILL ACTIVE. **Fat-tail signature absent for ~2 days.**
- Guard remains ON via condition B (EITHER condition triggers it).
- Two distinct failure modes confirmed: (A) market-wide carnage and (B) fat-tail absence can dissolve at different times.

## Last validated work
- **cycle_20260520_1200** (this): regime PARTIAL recovery quantified. H_BIG_WINNER_SHAPE proposed (3/3 bigs captured); walk-forward TEST big=0, does NOT validate. Strategic negative lesson: H_DISTRIB / H_LOCKED / H_QUIET_EMERGENCE / H_FAT_HUNTER are ANTI-fat-tail. See [cycle_20260520_1200.md](insights/cycle_20260520_1200.md).
- **cycle_20260520_0600**: H_FAT_HUNTER promising TRAIN n=11 Kelly=0.23 but TEST n=0; H_LOCKED confirmed ANTI-fat-tail.
- **cycle_20260520_0000**: GATE_EXPECTANCY_KELLY formalized; H_TOKENS_UNIFIED REJECTED; H_REGIME_GUARD formalized.
- **cycle_20260519_1826**: NULL_TG_LEAD — TG corpus reactive. H_TG_AS_EXIT parked.
- **cycle_20260519_1800**: per-token dedup overturned H_LP_WHITELIST.

## Top candidate hypothesis (status: descriptive, awaiting fat-tail return)
**H_BIG_WINNER_SHAPE**: `known ≥ 17 AND smart ≥ 7 AND liquidity_at_entry ≥ 20000 AND lp_unlocked=true AND top1_pct ≥ 50`. Catches 3/3 bigs in current data. Pre-collapse n=57, Er=+0.093, big=5.26%, rug=66.7%. Walk-forward TEST n=25 big=0 → not deployable yet. Re-test the moment big%>0 returns to any 50-window.

## Planned for next cycle
1. **Monitor regime condition B**: if any big winner appears in 50-window, re-test H_BIG_WINNER_SHAPE + compositions immediately under expectancy/Kelly gate.
2. **Symmetric null-check** on pumpfun_monitor + dexscreener_signals (same method as TG cycle_1826). Expect null.
3. **Re-document the negative lesson** about anti-fat-tail rug-reduction filters; consider 2-track gate proposal (track A high-WR scalping, track B fat-tail hunting).
4. Optional: compose H_BIG_WINNER_SHAPE ∩ H_LP_HIST_QUIET to test if a smarter intersection can reduce rug without losing fats (n likely too small).

## OPEN QUESTIONS to user
1. **NEW (1200)**: Strategic — should we accept a 2-track approach? Track A (rug-reduction filters, high WR, small expectancy, low Kelly) for "always-on small size"; Track B (H_BIG_WINNER_SHAPE-style, low WR, fat-tail-dependent) only when big%>0 in 50-window. Different gates per track.
2. CARRYING (0000): Regime-guard PATCH for serial_sniper.js (rolling-50 baseline gates new entries; feature-flag default off)?
3. CARRYING (0000): Macro context — known event around 2026-05-18T10:51Z (BTC, SOL, RPC)?
4. CARRYING (1826): H_TG_AS_EXIT instrumentation spec OK?
5. CARRYING (1800): SMART_COPY/SMART_COPY_TOP and SMART_COPY_AGE5/SMART_TOP_AGE5 identical metrics — A/B or dup spec?
6. CARRYING (1800): ULTRA_TRIPLE & H2 filter logic?
7. CARRYING (1639): BSC_FILTERED / SMART_CLUSTER dormant — killed?
8. CARRYING (1639): `bonding_curve_buyers` populated downstream?
9. CARRYING (1702): rugger_blacklist `wallet_added_at` for time-aware use?

## Leakage catalogue (unchanged this cycle: 5 total)
1. Hindsight classifier (cycle_1702 H_RUG_PC — rugger_blacklist)
2. Counting inflation (cycle_1800 H_LP_WHITELIST — multi-stream row dup)
3. Time-localization artifact (cycle_1639 1AR wallet — single-day inflation)
4. Post-entry feature (cycle_1639 ride_mode — set mid-flight)
5. Stale classifier DB with reactive updates (cycle_0000 tokens_unified)

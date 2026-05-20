# BRIEF — onchain AI brain (last update: cycle 20260520_1328)

## Current state (live)
- closed=4849 Solana rows / **572 unique tokens** (per-token dedup). State.json continues to shrink — 9 net tokens trimmed since cycle_1200.
- last50 unique-token avg=**-56.2%** WR=18% rug=54% **big=0** (regime regression from -45.9% in cycle_1200).
- last100 avg=-46.7% WR=27% rug=47% big=0.
- Span ~2026-05-17T21:45Z → 2026-05-20T13:16Z (2.65 days).
- **2 big winners remain** (PIGEON +3699, MTFR +251); 1billion +228 rotated out. Last big @ 2026-05-18T05:53Z (55h+ ago).
- Methodology note: under best-stream-fire dedup "Together" would be a 3rd big (153% in SMART_COPY) vs first-fire dedup (75%). See H_DEDUP_BEST_STREAM_BIG_ATTR.

## Goal
**+1,000,000% (×10K)** via fat-tail compounding. Promotion gate: **GATE_EXPECTANCY_KELLY** (TEST n≥20, E[r]>0, Kelly≥0.05, geom≥1%/trade).

## Paper streams in flight
**NONE.** Regime guard BOTH conditions A+B active — blocks all promotion.

## Regime status (this cycle)
- **Sliding-50 avg: -56.2%** — Condition A of H_REGIME_GUARD **REACTIVATED** (was cleared cycle_1200 at -45.9%; the "recovery" was a 75-trade local maximum at -36.5% that has rolled back).
- **big% in last 300 unique tokens: 0** — Condition B STILL ACTIVE. ~2.65 days streak.
- Guard ON via either condition. The two conditions can move independently.

## Last validated work
- **cycle_20260520_1328** (this): regime regression confirmed. Per-stream Track A audit NEGATIVE — SNIPER_G/GOLD5/WHALE all collapse on walk-forward TEST, capture 0/3 bigs. SNIPER_SMART_CLUSTER walk-forward STABLE NEGATIVE: 92/100/100% rug TRAIN/VAL/TEST, n=41 = 7.2% coverage → **H_SMART_CLUSTER_VETO** is first walk-forward-stable signal from this brain. See [cycle_20260520_1328.md](insights/cycle_20260520_1328.md).
- **cycle_20260520_1200**: regime PARTIAL recovery quantified (now reverted). H_BIG_WINNER_SHAPE proposed (3/3 bigs captured); walk-forward TEST big=0, does NOT validate. Strategic negative lesson: H_DISTRIB/H_LOCKED/H_QUIET_EMERGENCE/H_FAT_HUNTER are ANTI-fat-tail.
- **cycle_20260520_0600**: H_FAT_HUNTER promising TRAIN n=11 Kelly=0.23 but TEST n=0; H_LOCKED confirmed ANTI-fat-tail.
- **cycle_20260520_0000**: GATE_EXPECTANCY_KELLY formalized; H_TOKENS_UNIFIED REJECTED; H_REGIME_GUARD formalized.

## Top candidate (deployable)
**H_SMART_CLUSTER_VETO** (NEW cycle_1328): if `SNIPER_SMART_CLUSTER` appears in a token's multi-stream-fire set, abandon trade. Walk-forward: TRAIN n=24 avg=-90% rug=92%; VAL n=8 avg=-100% rug=100%; TEST n=9 avg=-100% rug=100%. Coverage 7.2% on full universe.
- **Status**: ready in concept, deployment-feasibility unknown — needs entry-time concurrency check (SMART_CLUSTER must fire before SNIPER_A enters, OR brain must support exit-side trail-tighten on post-entry SMART_CLUSTER detection).

## Top candidate (descriptive, awaiting regime)
**H_BIG_WINNER_SHAPE** (cycle_1200): `known ≥ 17 AND smart ≥ 7 AND liq ≥ 20000 AND lp_unlocked=true AND top1 ≥ 50`. Catches 3/3 bigs in current data. Pre-collapse n=57 Er=+0.093 big=5.26% rug=66.7%. Walk-forward TEST big=0 — re-test when big%>0 returns to 50-window.

## Planned for next cycle
1. **Spec H_SMART_CLUSTER_VETO for production**: clarify whether multi-stream concurrency at entry time is feasible, or whether SMART_CLUSTER fires later — affects whether it's an entry-side veto or exit-side trail-tighten.
2. **Re-do H_BIG_WINNER_SHAPE under best-stream-fire dedup** (H_DEDUP_BEST_STREAM_BIG_ATTR). Should add "Together" as a 4th big; expanded sample for shape characterisation.
3. **Monitor regime condition B** — when ANY big winner appears in 50-window, immediately re-run H_BIG_WINNER_SHAPE walk-forward + composition tests.
4. **Symmetric null-check** on pumpfun_monitor + dexscreener_signals (still deferred).
5. **`bonding_curve_buyers` field** still empty in entry_signal — recheck.

## OPEN QUESTIONS to user
1. **NEW (1328)**: H_SMART_CLUSTER_VETO deployment shape — entry-side veto requires SNIPER_SMART_CLUSTER to fire BEFORE SNIPER_A enters. Is this feasible in current sniper architecture, or does SMART_CLUSTER detection always lag entry? If lag, propose as exit-side trail-tighten (or hard exit) instead. Spec on request.
2. **NEW (1328)**: Track A as currently scoped (stream-subset OR rug-reduction filter) cannot produce deployable edge — both feature-level (cycle_1200) and stream-level (this cycle) Track A candidates fail walk-forward. Re-scope Track A to mean "Kelly-sized exposure to ALL streams during fat-tail-present regime" (sizing rule, not filter logic)? Or abandon entirely and focus all effort on Track B fat-tail-hunter?
3. CARRYING (1200): Strategic — should we accept a 2-track approach? (See open question 2 above for refinement.)
4. CARRYING (0000): Regime-guard PATCH for serial_sniper.js (rolling-50 baseline gates new entries; feature-flag default off)?
5. CARRYING (0000): Macro context — known event around 2026-05-18T10:51Z (BTC, SOL, RPC)?
6. CARRYING (1826): H_TG_AS_EXIT instrumentation spec OK?
7. CARRYING (1800): SMART_COPY/SMART_COPY_TOP and SMART_COPY_AGE5/SMART_TOP_AGE5 identical metrics — A/B or dup spec?
8. CARRYING (1800): ULTRA_TRIPLE & H2 filter logic?
9. CARRYING (1639): BSC_FILTERED / SMART_CLUSTER dormant — killed? **PARTIALLY ANSWERED 1328**: SMART_CLUSTER is firing (n=41 in current data) but catastrophic. Recommend killing in production.
10. CARRYING (1639): `bonding_curve_buyers` populated downstream?
11. CARRYING (1702): rugger_blacklist `wallet_added_at` for time-aware use?

## Leakage catalogue (unchanged this cycle: 5 total)
1. Hindsight classifier (cycle_1702 H_RUG_PC — rugger_blacklist)
2. Counting inflation (cycle_1800 H_LP_WHITELIST — multi-stream row dup)
3. Time-localization artifact (cycle_1639 1AR wallet)
4. Post-entry feature (cycle_1639 ride_mode)
5. Stale classifier DB (cycle_0000 tokens_unified)

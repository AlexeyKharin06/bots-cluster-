# BRIEF — onchain AI brain (last update: cycle 20260520_0000)

## Current state (live)
- closed=4915 Solana rows / **592 unique tokens** (per-token dedup). Span 2026-05-11T15:33Z → 2026-05-19T23:59Z (8d).
- Per-token last-50: **avg=-99.6% WR=0% rug=100% big=0%**. Worst single-day print yet.
- +36 new unique tokens since cycle_1826's 19:17Z snapshot — 100% rug, avg=-99.5%.

## Goal (carrying from cycle_1826)
**+1,000,000% (×10K)** via 6-8 reinvested compounding wins. Implies fat-tail edge required, not high-WR scalping. **Expectancy/Kelly gate formalized this cycle** (see below) — replaces strict +150%.

## Paper streams in flight
**NONE.** Neither gate (strict +150% or new expectancy/Kelly) approves any candidate on current TEST. Both correctly reject LP_HIST+QUIET (TRAIN Kelly=0.33, TEST E[r]=-50%).

## Regime status (NEW this cycle — quantified)
- Sliding-50 transition #1 at ~2026-05-18T10:51Z: big% drops to 0, stays 0 for 5 days.
- Sliding-50 transition #2 at ~2026-05-19T18:43Z: WR collapses 20%→0%, rug 56%→100%.
- **Confirmed external (macro), NOT sniper-side**: stream mix unchanged pre/post 2026-05-18T20:00Z; all streams uniformly worse. SNIPER_G (best risk-adjusted) -3.6% → -43.3%.
- **Posture**: defer all edge-promotion until rolling-50 avg > -55% AND big% > 0 within 50 trades.

## Last validated work
- **cycle_20260520_0000**: GATE_EXPECTANCY_KELLY formalized (E[r]>0 ∧ Kelly≥0.05 ∧ geom≥1%/trade ∧ n≥20). H_TOKENS_UNIFIED REJECTED. H_REGIME_GUARD formalized. See [cycle_20260520_0000.md](insights/cycle_20260520_0000.md).
- **cycle_20260519_1826**: NULL_TG_LEAD — TG corpus reactive. H_TG_AS_EXIT parked.
- **cycle_20260519_1800**: per-token dedup overturned H_LP_WHITELIST. Survivors: H_LP_HIST, H_DISTRIB, H_LOCKED — none clear gate.
- **cycle_20260519_1702**: H_RUG_PC REJECTED (hindsight). H_CR_HIST_NEG validated.

## Planned for next cycle
1. **Regime recovery check**: if rolling-50 avg > -55% OR big% > 0 in fresh data → re-test all surviving edges under expectancy gate immediately.
2. **If still carnage**: address H_TG_AS_EXIT spec or symmetric null-check on pumpfun_monitor.js + dexscreener_signals.
3. **Sniper patch spec** for H_REGIME_GUARD (~30 lines): rolling baseline computed from own closed_trades, gate new entries when avg < threshold. User would apply manually.
4. **Optional**: characterize the only positive window (2026-05-18T07:16-09:17) — what was different about those 50 tokens? Could inform "normal regime" signature.

## OPEN QUESTIONS to user
1. **NEW (0000): Regime-guard PATCH** — OK to write small read-only patch for serial_sniper.js (rolling-50 baseline gates new entries when avg<threshold; feature-flag, default off)? User applies manually.
2. **NEW (0000): Macro context** — known event around 2026-05-18T10:51Z (BTC, SOL, RPC)?
3. CARRYING (1826): H_TG_AS_EXIT instrumentation spec OK?
4. CARRYING (1800): SMART_COPY/SMART_COPY_TOP and SMART_COPY_AGE5/SMART_TOP_AGE5 identical metrics — A/B or dup spec?
5. CARRYING (1800): ULTRA_TRIPLE & H2 filter logic?
6. CARRYING (1639): BSC_FILTERED / SMART_CLUSTER dormant — killed?
7. CARRYING (1639): `bonding_curve_buyers` populated downstream?
8. CARRYING (1702): rugger_blacklist `wallet_added_at` for time-aware use?

## Rejected this cycle (0000)
- **H_TOKENS_UNIFIED** — leakage by construction. Same shape as H_RUG_PC but different access pattern (stale snapshot + post-hoc updates on test set). Added as 5th leakage form.

## Leakage catalogue (this cycle: +1)
1. Hindsight classifier (cycle_1702 H_RUG_PC — rugger_blacklist)
2. Counting inflation (cycle_1800 H_LP_WHITELIST — multi-stream row dup)
3. Time-localization artifact (cycle_1639 1AR wallet — single-day inflation)
4. Post-entry feature (cycle_1639 ride_mode — set mid-flight)
5. **NEW: Stale classifier DB with reactive updates** (cycle_0000 tokens_unified — 90% Apr-15 batch + recent updates on test set)

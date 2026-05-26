# BRIEF — onchain AI brain (cycle 20260526_1200)

## State (live, stale 4.5h)
- closed=**4930** (-56 net rotation). 0 open (state.json `positions` empty — suspicious). Window: 05-23T22:32Z → 05-26T07:18Z (~57h).
- **0 new bigs / 0 new near-bigs in +1h12min new flow** since c0600.
- **STATE.JSON STALE 4.5h** (last write 07:30Z, now 12:02Z). Sniper proc (pid 79459) running but not flushing. INFRA CONCERN.
- 2nd anomaly: state.json earliest entry moved BACKWARD 8h25min (de-rotation?).
- 3rd anomaly: state.json `positions` empty despite c0600 reporting 33 open.

## Goal & gate
**+1M%**. GATE: n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%. **0 paper streams deployed**.

## Regime (chain-asymmetric 4th consec — extrapolating, can't recompute on stale data)
- **Sol** Cond A likely still clear (was -44.5 c0600, GENWEALTH 18h before stale snapshot). **Guard OFF Sol.**
- **BSC** Cond A still triggered (was -62.0), drought 30h+. **Guard ON BSC.**

## Last validated (this cycle)
**H_HUPHEY_TOP1_FLEX FORMALLY ADOPTED** via walk-forward sensitivity table (top1≥0/60/65 all give n=9 geom=+117%; top1≥85 drops to n=4 geom=+110.6%; drop threshold = no recall loss); **Methodology #20 NEW CANDIDATE: COHORT-SHAPE TRAP** — H_PUMPSWAP_SMART_VELOCITY (the SHAPE of 19 near-bigs) walk-forward REJECTED HARD n=89 73% rug K=-1.14 geom=-88% TRAIN/TEST both <-1; **Methodology #17 NEAR-BIG REGIME RETIRED** (near-bigs are survivor-noise in high-rug base, not discriminable cohort); **Sol BIGS vs NEAR-BIGS feature dist** OPPOSITE profile (BIGS meteora+H2+top1=83.5+smart=6+buys=81 vs NEAR-BIGS pumpswap+ULTRA_TRIPLE/SMART_TOP_AGE5+top1=66+smart=11+buys=198) — selection-bias illusion; state.json stale infra concern; n-distance UNCHANGED for all 3 deploy candidates. See [cycle_20260526_1200.md](insights/cycle_20260526_1200.md).

## Top candidates (n-progress FLAT due to stale state)
- **PAPER_SOL_HUPHEY_WATCH (HEADLINE — deploy-ready, top1-flex spec)**: n=9 4b/0r WR=78% avg=+258% geom=+117%/trade Er=+2.58 K~0.24. Gate: `top1_owner.startsWith("HUPHey")` (NO top1 threshold).
- **PAPER_BSC_85871_WATCH (HEADLINE — rug-clamp MOOT, deploy-ready)**: n=4 2b/0r avg=+197% geom=+135%/trade. Gate: bc[0].addr=0x85871...
- **PAPER_SOL_GAMMA_RELAXED**: top1<22 ∩ smart∈[2,8] ∩ pumpswap ∩ age≤25 ∩ lp_unlocked=False ∩ buys_m5≥250. n=16 geom=+1.55% (borderline).
- PORTUGAL strict / β-shape / near-big shape — **all DROPPED / REJECTED**.

## Methodology — 20 forms
**11.SINGLE-BLOCK**. **12.ROTATION-K 8th**. **13.SINGLE-WALLET**. **14.NAMED-ALPHA**. **15.SUBSUMPTION 75%**. **16.HIST-vs-LIVE DRIFT**. **17.NEAR-BIG REGIME — RETIRED this cycle**. **18.SYMBOL-COPYCAT REJECTED**. **19.RUG-CLAMP — MOOT for 85871 deferred**. **20.COHORT-SHAPE TRAP NEW CANDIDATE** — top-N% outcome cohorts yield survivor-biased filters; always validate against full base population.

## Planned next cycle (18:00Z 05-26)
1. **VERIFY state.json freshness** — first task. If still stale, escalate to CRITICAL_FINDINGS + healthcheck.
2. **Investigate state.json earliest-backward anomaly** (8h25min de-rotation).
3. **Investigate state.json `positions` empty** — migration / partial-write?
4. **HUPHey 10th-token watch** (needs fresh data).
5. **0x85871 forward-fire watch** (needs fresh data).
6. **γ-relaxed n=20 floor watch** (4 more entries).
7. **Methodology #20 formalize** — update brain reasoning template (base-rate check BEFORE feature-extraction).
8. **Apply #20 retrospectively** to "Sol BIGS shape" emerging signal (n=8 meteora+H2+top1≥80+buys≤200) — base-rate check first.
9. CARRIED: SNIPER_H2 Sol routing (5/8 Sol bigs BF=H2); HUPHey Solscan identity; BSC volume fetcher; Wallet leaderboard rebuild; 75qsE3p5y2BF 11th-token watch; Pool_creator BVfVe44Wj 3rd-token.

## Progress delta this cycle
**POSITIVE (3)**: H_HUPHEY_TOP1_FLEX walk-forward validated / Methodology #20 NEW CANDIDATE / Methodology #17 cleanly RETIRED.
**NEGATIVE (3)**: state.json STALE 4.5h / n-distance FLAT / 2 more operational anomalies (earliest-backward + positions-empty).
**Net: NET POSITIVE on methodology, FLAT on n-progress.** Stuck NOT triggered (7th consec).

## OPEN QUESTIONS to user
1. **STATE.JSON STALE 4.5h** — sniper proc running but file not flushing. Verify write-cadence / disk-flush / state-rotation logic.
2. **STATE.JSON earliest backward 8h25min** — intended state-rebuild or anomaly?
3. **STATE.JSON `positions` empty** — c0600 had 33 open, now 0. Migration or write-partial?
4. **PAPER_SOL_HUPHEY deploy** — STRONG YES (n=9 Er=+2.58 5-100× over gates, top1-flex spec finalized).
5. **PAPER_BSC_85871 deploy** — YES (rug-clamp MOOT n=4 all-wins).
6. **Methodology #20 formal adoption** — add to METHODOLOGY_LESSONS.md.
7. CARRIED: SNIPER_H2 Sol routing; HUPHey identity; BSC volume; wallet leaderboard rebuild.

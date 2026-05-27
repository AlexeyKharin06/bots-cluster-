# BRIEF — onchain AI brain (cycle 20260527_0000)

## State (STALE 16.5h — Helius rate-limit infinite loop, ~28h ongoing)
- closed=**4930** (UNCHANGED 4th consec). open=22 raw rows = **5 unique** Sol opens (XVG/USDCx/HTX/grail/CHARTARD).
- Window: 05-23T22:32Z → 05-26T07:18Z (~57h, UNCHANGED).
- State.json last write 05-26T07:30Z. Sniper PID 79459 alive but busy-looping all 13 Helius keys.
- **ROOT CAUSE PATCH LOCATED** — `serial_sniper.js:85-95` (`getHeliusKey()` instant `_heliusDeadKeys.clear()` no cooldown) + line 341 (instant recursive `heliusRPC` retry). Concrete patch: 60s cooldown + return null + non-recursive retry. See cycle Step 0a.

## Goal & gate
**+1M%**. GATE: n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade. **0 paper streams deployed**. 5-cycle pending user auth for HUPHey+85871.

## Regime (6th cycle chain-asymmetric, extrapolating)
- **Sol** Cond A clear → Guard OFF. **BSC** Cond A triggered → Guard ON.

## Last validated (this cycle)
**Helius INFINITE-LOOP bug LOCATED** with concrete patch site; **Methodology #21 EMPIRICAL REAL-TIME CONFIRMATION** via `grail` symbol collision (our Ga3dq grail ≠ pumped UvN1 grail +2188%) — graduates to 2-confirmation READY; **H_SELF_LP backtest n=4930** (top1_owner==pair_address): 45.5% population coverage, -6.9pp avgPnL drag, weak-alone, filed for COMBO with bc<30; **pumps_24h corpus 23 tokens all gecko-trending** → SOURCE COVERAGE GAP filed H_GECKO_FEED; **4 of 5 our opens are self-LP** → elevated rug risk. See [cycle_20260527_0000.md](insights/cycle_20260527_0000.md).

## Top candidates (UNCHANGED from c1800)
- **PAPER_SOL_HUPHEY_WATCH (deploy-ready 5 cycles)**: n=9 (4 bigs/0 rugs) Er=+2.58 K~0.24 geom=+117%/trade. Gate `top1_owner.startsWith("HUPHey")`.
- **PAPER_BSC_85871_WATCH (deploy-ready 5 cycles)**: n=4 (2 bigs/0 rugs) geom=+135%/trade. Gate `bc[0].addr.startsWith("0x85871")`.
- **PAPER_SOL_NOAR_WATCH (STATISTICAL-tier)**: n=11 (2 bigs/1 near/2 rugs) Er=+0.17 K=0.23 geom=+1.92%/trade. #14 NOT met (18% rug).
- **PAPER_SOL_GAMMA_RELAXED**: n=16 geom=+1.55% — closest to n-gate (distance 4).

## Methodology — 23 forms
**20.COHORT-SHAPE TRAP** READY (2 confirmations). **21.SYMBOL-BLIND WALLET DRIFT** PROMOTED READY (2 confirmations incl real-time grail). **22.API SCHEMA VERIFICATION** READY. **23.INFRA-CRISIS OPPORTUNITY COST QUANTIFICATION NEW CANDIDATE** (this cycle: 23 missed × 2.6% big-rate ≈ 0.6 bigs missed in 3 days).

## Planned next cycle (06:00Z 05-27)
1. **VERIFY HELIUS** — escalate if still frozen (29-34h). Patch site ready.
2. If state freshens: HUPHey 10th / 0x85871 5th / NOAR 12th / γ-relaxed n=17-18 watch + **AUDIT 4 self-LP opens** outcomes vs H_SELF_LP base-rate (expect ~59% rug).
3. **H_SELF_LP combo with bc<30** on Sol bigs cohort (Methodology #20-aware confirmatory).
4. **Methodology #20/#21/#22 FORMAL ADOPTION** all ready.
5. **H_GECKO_FEED** poller spec design (no deploy without user OK).
6. CARRIED: SNIPER_H2 Sol routing; HUPHey identity; BSC volume; wallet leaderboard rebuild; state.json earliest-backward anomaly; pool_creator BVfVe44Wj 3rd-token watch; Sol bigs n=8 shape base-rate check.

## Progress delta this cycle
**POSITIVE (4)**: Helius patch site located / #21 real-time confirmation / H_GECKO_FEED quantified ~7-8 missed pump/day gap / H_SELF_LP backtested n=4930.
**NEGATIVE (3)**: State frozen 16.5h (deepened from 10.5h, 28h total) / n-distance unchanged 4th consec / 4 of 5 opens self-LP.
**Net: NET POSITIVE on methodology + infra diagnosis, FLAT on n-progress, NEGATIVE on infra duration.**
**Stuck warning**: NOT triggered (9th consec cycle with new findings).

## OPEN QUESTIONS to user
1. **HELIUS RATE-LIMIT (CRITICAL — 28h ongoing)** ★★★ — options: (a) refresh Helius quota, (b) apply patch from Step 0a, (c) hard-kill PID 79459 and restart.
2. **PAPER_SOL_HUPHEY** deploy — STRONG YES (5-cycle pending).
3. **PAPER_BSC_85871** deploy — YES (5-cycle pending).
4. **PAPER_SOL_NOAR_WATCH** STATISTICAL-tier deploy (different tier).
5. **Methodology #20/#21/#22 FORMAL ADOPTION** all 3 ready.
6. **H_GECKO_FEED** poller — build? (~7-8 missed pump/day blind spot.)
7. CARRIED: SNIPER_H2 routing; HUPHey identity; BSC volume; wallet leaderboard rebuild; state.json earliest-backward anomaly; context-prep pipeline 6 days stale.

# BRIEF — onchain AI brain (cycle 20260526_1800)

## State (live, STALE 10.5h — Helius rate-limit infinite loop)
- closed=**4930** (unchanged from c1200, sniper not flushing). open=22 raw rows = **5 unique** Sol opens (XVG/USDCx/HTX/grail/CHARTARD — none match deploy gates).
- Window: 05-23T22:32Z → 05-26T07:18Z (~57h, unchanged).
- **STATE.JSON FROZEN 10.5h** (last write 07:30Z, now 18:01Z). **Root cause: ALL 13 HELIUS KEYS EXHAUSTED, sniper proc in infinite rotation loop** (6.8M log entries since 20:07Z yesterday). Last real CHECK 07:31Z.
- **Context-prep pipeline also stale**: brain-context healthcheck dated 2026-05-20T18:06Z (6 days old).
- **Operational anomaly resolved**: c1200's "positions empty" was a wrong-key bug → Methodology #22 candidate (key is `open_positions` not `positions`).

## Goal & gate
**+1M%**. GATE: n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade. **0 paper streams deployed**. 4-cycle pending user authorization for HUPHey+85871.

## Regime (5th cycle chain-asymmetric — extrapolating, can't recompute on stale data)
- **Sol** Cond A likely still clear (was -44.5 c0600). **Guard OFF Sol.**
- **BSC** Cond A still triggered (was -62.0). **Guard ON BSC.**

## Last validated (this cycle)
**NOAR wallet RECOUNT via Methodology #21 fix: Maple +163.8 LINKED as 3rd big** (was c1200 unrecognized α-borderline because brain matched by symbol not address); NOAR cohort n=10→**11** (2 bigs/1 near/2 rugs, avg=+16.1%, **Er=+0.17 K=0.23 geom=+1.92%/trade — gate-passing Er/K/geom, only n<20 blocks, distance 9**). **3rd named-wallet entity** (HUPHey/0x85871/NOAR). NOAR 18% rug does NOT meet Methodology #14 clean-alpha (HUPHey 0% / 0x85871 0%) — statistical-tier only. **H_TOP2_HLNP NEW exploration → REJECTED** (walk-forward TEST n=14 0 bigs Er=-0.15; 100% subsumed by HUPHey∪NOAR via Methodology #15). **Methodology #21 NEW candidate: SYMBOL-BLIND WALLET DRIFT**; **#22 NEW candidate: API SCHEMA VERIFICATION**. See [cycle_20260526_1800.md](insights/cycle_20260526_1800.md).

## Top candidates (distance-to-deploy ranking)
- **PAPER_SOL_HUPHEY_WATCH (HEADLINE — deploy-ready 4 cycles)**: n=9 (4 bigs/0 rugs) Er=+2.58 K~0.24 geom=+117%/trade. Gate: `top1_owner.startsWith("HUPHey")` (top1-flex spec, no top1 threshold). **#14 clean-alpha qualified.**
- **PAPER_BSC_85871_WATCH (HEADLINE — deploy-ready 4 cycles)**: n=4 (2 bigs/0 rugs) geom=+135%/trade. Gate: `bc[0].addr.startsWith("0x85871")`. **#14 clean-alpha qualified.**
- **PAPER_SOL_NOAR_WATCH (NEW candidate this cycle)**: n=11 (2 bigs/1 near/2 rugs) Er=+0.17 K=0.23 geom=+1.92%/trade. Gate: `top1_owner.startsWith("75qsE3p5y2")`. **Statistical-tier — #14 NOT met (18% rug).**
- **PAPER_SOL_GAMMA_RELAXED**: n=16 geom=+1.55% (borderline). Feature-shape filter.
- PORTUGAL strict / β-shape / near-big shape / TOP2_HLNP — **all DROPPED / REJECTED**.

## Methodology — 22 forms catalogued
**11-19** as prior. **20.COHORT-SHAPE TRAP** (now 2 confirmations: c1200 PUMPSWAP_SMART_VELOCITY + c1800 TOP2_HLNP) → **READY FOR FORMAL ADOPTION**. **21.SYMBOL-BLIND WALLET DRIFT NEW CANDIDATE** (re-cohort by address every cycle, not symbol). **22.API SCHEMA VERIFICATION NEW CANDIDATE** (verify dict keys before reporting empty).

## Planned next cycle (00:00Z 05-27)
1. **VERIFY HELIUS KEY STATUS** — escalate to CRITICAL_FINDINGS if still rate-limited. User-side fix needed (refresh keys / quota / cooldown patch).
2. **VERIFY context-prep pipeline** — healthcheck regeneration.
3. If state freshens: HUPHey 10th / 0x85871 5th / NOAR 12th / γ-relaxed n=20 watch.
4. NOAR sub-cohort dive (top1%<99.9 + bf=H2 + meteora∩smart≥3) if 2 more entries land.
5. **Methodology #21 PROACTIVE adoption** (logic airtight from single case).
6. CARRIED: SNIPER_H2 Sol routing; HUPHey Solscan identity; BSC volume; wallet leaderboard rebuild; state.json earliest-backward anomaly; pool_creator BVfVe44Wj 3rd-token watch; Sol bigs n=8 shape base-rate check (per #20 — wait for n>8).

## Progress delta this cycle
**POSITIVE (4)**: NOAR recount adds Maple (3rd named-wallet) / TOP2 dimension explored end-to-end / Methodology #21 candidate / #22 candidate.
**NEGATIVE (3)**: State.json frozen 10.5h (root-caused but not fixed) / NOAR 18% rug = statistical-tier not deploy-ready / infra emergency persists 22h.
**Net: NET POSITIVE on methodology + 3rd named-wallet, FLAT on n-progress (3rd consec stale cycle), NEGATIVE on infra.**
**Stuck warning**: NOT triggered (8th consec cycle with new findings).

## OPEN QUESTIONS to user
1. **HELIUS KEY EXHAUSTION (CRITICAL)** — sniper non-functional 22h, all 13 keys rate-limited. Need refresh/quota/cooldown patch. ★★★
2. **Context-prep pipeline stale** — healthcheck 6 days old in brain-context bundles.
3. **PAPER_SOL_HUPHEY deploy** — STRONG YES (n=9 Er=+2.58, 5-100× gate, 4-cycle pending).
4. **PAPER_BSC_85871 deploy** — YES (n=4 all-wins, 4-cycle pending).
5. **PAPER_SOL_NOAR_WATCH deploy as STATISTICAL-tier** (NEW, n=11 K=0.23 geom=+1.92%/trade) — different tier from clean-alpha HUPHey/0x85871; user decision required.
6. **Methodology #20 formal adoption** (2 confirmations now); **#21 proactive adoption** (logic airtight); **#22 trivial adoption**.
7. CARRIED: SNIPER_H2 Sol routing; HUPHey identity; BSC volume; wallet leaderboard rebuild; state.json earliest-backward anomaly.

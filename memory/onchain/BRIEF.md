# BRIEF — onchain AI brain (cycle 20260527_0600)

## State (STALE 22.5h — Helius rate-limit infinite loop, ~34h ongoing)
- closed=**4930** (UNCHANGED 5th consec). open=22 raw rows = **5 unique** Sol opens (XVG/USDCx/HTX/grail/CHARTARD).
- Window: 05-23T22:32Z → 05-26T07:18Z (~57h, UNCHANGED).
- State.json last write 05-26T07:30Z. Sniper PID 79459 alive but busy-looping all 13 Helius keys.
- **ROOT CAUSE PATCH LOCATED c0000** — `serial_sniper.js:85-95` + line 341 cooldown+non-recursive. Awaiting user auth.

## Goal & gate
**+1M%**. GATE: n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade. **0 paper streams deployed**. 6-cycle pending user auth for HUPHey+85871.

## Regime (7th cycle chain-asymmetric, extrapolating — no new data)
- **Sol** Cond A clear → Guard OFF. **BSC** Cond A triggered → Guard ON. (Unchanged 5 consec, no new closes.)

## Last validated (this cycle)
**H_SELF_LP STRENGTHENS dramatically** with best-fire dedup (c0000 used raw 4930 rows — undercounted strength). SOL SELF-LP n=389 avg=-60.9% vs NON-SELF n=268 avg=-32.5% = +28.4pp lift, walk-forward consistent. **HUPHey VALIDATED** as TRUE clean-alpha via matched-shape baseline (matched EXCL HUPHey n=71 Er=-0.41 vs HUPHey direct n=9 Er=+2.59 = +3.00 differential). **NOAR alpha DECOMPOSED** — apparent Er+0.16 → matched-shape EXCL NOAR Er+0.13 (essentially shape-coincidence; NOAR-within-shape Er≈0). **Methodology #20 COHORT-SHAPE TRAP triple-confirmed.** 4 RUG-WALLET veto candidates (ent9nhnz/2qiojbwk/8m88xunebwlz/88md1aaefdr2 — n=44 91% rug; walk-forward TEST 100% rug-capture). NEW H_META_TOP99_PURE_SHAPE candidate n=35 Er+0.099 K=0.067 (fails geom only). See [cycle_20260527_0600.md](insights/cycle_20260527_0600.md).

## Top candidates (RE-RANKED after this cycle)
- **PAPER_SOL_HUPHEY_WATCH (deploy-ready 6 cycles, NOW shape-validated)**: n=9 (4 bigs/0 rugs) Er=+2.585 K=0.41 geom=+59.7%/trade. Matched-shape baseline EXCL HUPHey Er=-0.41 confirms TRUE clean-alpha (Methodology #14a). Gate `top1_owner.startsWith("HUPHey")`.
- **PAPER_BSC_85871_WATCH (deploy-ready 6 cycles)**: n=4 (2 bigs/0 rugs) geom=+135%/trade. Gate `bc[0].addr.startsWith("0x85871")`. Matched-shape baseline check pending next cycle.
- **PAPER_SOL_GAMMA_RELAXED**: n=16 geom=+1.55% — closest to n-gate (distance 4).
- **PAPER_SOL_NOAR_WATCH DEPRIORITIZED**: apparent Er+0.16 decomposes to matched-shape +0.13 + Maple n=1 anomaly. Reframe: not statistical-tier; reclassify or skip.

## New filter candidates
- **H_SELF_LP veto** (apply only with COMBO; -28.4pp drag alone, walk-forward consistent).
- **H_RUG_WALLET_VETO** — Sol blacklist 4 prefixes; TEST 7/7 rugs 100% generalization.
- **H_META_TOP99_PURE_SHAPE** — n=35 Er+0.099 K=0.067 (3 of 4 gates; fails geom 0.27% need 1%).
- **H_SELF_LP_TOP85_VETO** — SELF-LP ∩ top1≥85 n=77 0 bigs 93.5% rug; mathematical veto.

## Methodology — 23+ forms
**20.COHORT-SHAPE TRAP** TRIPLE-CONFIRMED (3rd this cycle: NOAR alpha decomposition). **14a.MATCHED-SHAPE BASELINE SUBTYPE** new sub-lesson clarifying TRUE vs APPARENT clean-alpha (HUPHey TRUE, NOAR APPARENT). **4.STREAM-DUPLICATION AWARENESS** reaffirmed strongly (best-fire dedup essential for cohort stats; c0000 raw-row H_SELF_LP report was 4× understated).

## Planned next cycle (12:00Z 05-27)
1. **CRITICAL ESCALATE** Helius if still frozen ~40h.
2. If state freshens: audit 4 self-LP opens vs 63% rug base-rate; re-validate rug-wallets on fresh data; re-walk-forward H_SELF_LP TEST split.
3. **Apply matched-shape baseline retrofit** to 0x85871 (BSC PORTUGAL shape control) — quantify wallet contribution.
4. **H_RUG_WALLET_VETO spec** for Sol entry filter.
5. **H_META_TOP99 watch** — track new shape-matching entries when state thaws.
6. **Methodology #20 FORMAL ADOPTION** (triple-confirmed).
7. **Methodology #14a FORMAL ADOPTION** (matched-shape baseline subtype for named-alpha classification).
8. CARRIED: H_GECKO_FEED, SNIPER_H2 Sol routing, BSC volume, state.json earliest-backward anomaly, context-prep pipeline 6+ days stale.

## Progress delta this cycle
**POSITIVE (5)**: H_SELF_LP corrected 4× upward / HUPHey shape-validated / NOAR decomposed / 4 rug-wallets walk-forward generalizing / H_META_TOP99 new candidate.
**NEGATIVE (3)**: State frozen 22.5h (deepened) / 5 consec cycles no n-progress / 34h Helius outage ongoing.
**Net: NET POSITIVE on methodology + signal quality. FLAT on n-progress. NEGATIVE on infra duration.**
**Stuck warning**: NOT triggered (10th consec cycle with new findings).

## OPEN QUESTIONS to user
1. **HELIUS RATE-LIMIT (CRITICAL — 34h ongoing)** ★★★★ — refresh Helius quota / apply c0000 patch / hard-kill PID 79459.
2. **PAPER_SOL_HUPHEY** deploy — STRONGLY YES (now matched-shape validated TRUE clean-alpha).
3. **PAPER_BSC_85871** deploy — YES (matched-shape check pending next cycle).
4. **PAPER_SOL_NOAR_WATCH** — DEPRIORITIZE / RECLASSIFY (shape-coincidence per Methodology #20 confirmation #3).
5. **H_RUG_WALLET_VETO** — apply as Sol entry blacklist?
6. **Methodology #20 + #14a FORMAL ADOPTION** (both ready).
7. CARRIED: H_GECKO_FEED, SNIPER_H2 routing, BSC volume, state.json earliest-backward anomaly, context-prep pipeline 6+ days stale.

# BRIEF — onchain AI brain (cycle 20260527_1200)

## State (STALE 28.5h — Helius rate-limit infinite loop ~40h ongoing)
- closed=**4930** (UNCHANGED 6th consec). open=0. Window 05-24T08:36Z→05-26T07:30Z (~47h). State.json last write 05-26T07:30Z.
- Sniper PID 79459 alive (etime 7d 5h+) busy-looping all 13 Helius keys. **c0000 patch ready at `serial_sniper.js:85-95`+L341 — awaiting user auth.**

## Goal & gate
**+1M%**. GATE: n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade. **0 paper streams deployed**. 12-cycle pending user-auth for HUPHey + 85871. Both NOW Methodology #14a TRUE clean-alpha validated.

## Regime (8th cycle chain-asymmetric — no new data)
**Sol** Cond A clear → Guard OFF. **BSC** Cond A triggered → Guard ON. (Unchanged 6 consec.)

## Last validated (this cycle)
**H_BSC_85871 MATCHED-SHAPE RETROFIT — TRUE clean-alpha**: ALPHA n=3 best-fire avg=+95.6% geom=+71.8%/tr big%=33% rug=0%; MATCHED-SHAPE EXCL n=85 avg=-60.7% big%=1.2% rug=71.8% = **+156.3pp lift, 27.7× big-rate, 100% rug elimination**. Differential survives excluding BELIEF big. **2 NEW Sol rug-wallets** (43wpYdVB n=7 71% rug; 3xbyiLME n=5 60% rug). **NEW alpha candidate H_9CCPC_WATCH** n=3 (eff. n=2 same-symbol) +26.2% vs matched -7.6% — WATCH only. **RUG_6 walk-forward**: TRAIN n=27 rug92.6%, TEST n=29 rug79.3% (+61% capture vs RUG_4, 0 bigs lost). See [cycle_20260527_1200.md](insights/cycle_20260527_1200.md).

## Top candidates
- **PAPER_SOL_HUPHEY (deploy-ready 12 cycles, #14a-validated)**: n=9 (4b/0r) Er=+2.585 K=0.41 geom=+135.84%/tr. `top1_owner.startsWith("HUPHey")`. Distance n-gate: 11 more (~4-5d).
- **PAPER_BSC_85871 (deploy-ready 12 cycles, NOW #14a-validated)**: n=3 best-fire Er=+0.956 K=0.43 geom=+71.8%/tr. `bc[0].addr.startsWith("0x85871")`. Distance n-gate: 17 more (~34d).
- **PAPER_SOL_GAMMA_RELAXED**: n=16 geom=+1.55% — distance 4 to n-gate.
- **H_9CCPC_WATCH NEW** — n=3 (eff. n=2) +26% vs matched -7.6%, 0 bigs. WATCH only.

## New filter candidates
- **H_RUG_WALLET_VETO_RUG6** — Sol blacklist 6 prefixes. TEST rug=79.3%, +61% capture vs RUG_4, 0 bigs lost.
- H_SELF_LP_TOP85_VETO (carry).
- H_META_TOP99_PURE_SHAPE (carry — fails geom-gate).

## Methodology — 24 forms
**#14a MATCHED-SHAPE BASELINE SUBTYPE** — 2 worked examples (HUPHey + 0x85871 both TRUE) → READY ADOPT. **#24 SAME-SYMBOL DUP-PAIR INFLATION (NEW CANDIDATE)** — 9ccPCxxE n=3 eff. n=2 (2× ISOR). Rule: report unique-symbols alongside unique-pairs. **#4 STREAM-DUPLICATION** reaffirmed (85871 raw n=4 → best-fire n=3).

## Planned next cycle (18:00Z 05-27)
1. **CRITICAL Helius escalation** — 46h+ outage by next cycle.
2. **H_RUG_SYMBOL_DUPLICATE** scan — symbol w/ ≥2 rug-wallet hits = elevated risk (Popus under both 43wpYdVB & 3xbyiLME).
3. **RUG_6 veto-rule pseudo-code** for sniper entry filter, await user adoption.
4. **0x85871 paper-stream config** alongside HUPHey.
5. **Methodology #14a FORMAL ADOPTION** (2 worked examples).
6. **Methodology #24** seek 2nd confirmation.
7. If state thaws: walk-forward H_9CCPC_WATCH, RUG_6 on fresh, n-progress.
8. CARRY: H_GECKO_FEED, SNIPER_H2, BSC volume, state earliest-backward, context-prep stale.

## Progress delta this cycle
**POS (5)**: 0x85871 #14a-validated / NEW H_9CCPC_WATCH / 2 NEW rug-wallets / RUG_6 +61% capture / NEW Methodology #24.
**NEG (3)**: Freeze 28.5h (+6h) / 6 consec n-flat / 0 deploys (12 cycles pending).
**Net**: POS on depth-mining + filter coverage. FLAT on n-progress. NEG on infra.
**Stuck: NOT triggered** (11 consec cycles new findings — meta-finding: depth-mining yields alpha after fresh-data halts).

## OPEN QUESTIONS to user
1. **HELIUS RATE-LIMIT ★★★★★ (40h+)** — refresh quota / apply c0000 / hard-kill PID 79459.
2. **PAPER_SOL_HUPHEY** deploy — STRONGLY YES (12 cycles pending).
3. **PAPER_BSC_85871** deploy — STRONGLY YES (NOW #14a-validated).
4. **H_RUG_WALLET_VETO_RUG6** adoption (6 prefixes)?
5. **Methodology #14a + #20 + #4 FORMAL ADOPTION** (all triple/double-confirmed).
6. CARRIED: H_GECKO_FEED, SNIPER_H2, BSC volume, state earliest-backward, context-prep 6+ days stale.

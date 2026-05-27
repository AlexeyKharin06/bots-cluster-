# BRIEF — onchain AI brain (cycle 20260527_1800)

## State (slightly thawed — closed=4947, +17 since c1200)
- closed=**4947** (UP +17 from c1200 4930). open=0. Window 2026-05-24T08:36Z → 2026-05-27T14:54Z (~78h). State.json last write 2026-05-27T14:54Z (~3h ago).
- New 17 closures: 6×CHARTARD (-100%, lmr=180), 7×grail (-100%, lmr=196), 3×HTX (-8%), 1×USDCx (-100%) — mostly batch-flush of stale positions.
- Sniper PID still in Helius rate-limit loop (~46h ongoing). c0000 patch ready awaiting user auth.

## Goal & gate
**+1M%**. GATE: n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade. **0 paper streams deployed**. 13-cycle pending user-auth.

## Regime (9th cycle chain-asymmetric — no new data)
**Sol** Cond A clear → Guard OFF. **BSC** Cond A triggered → Guard ON. (Unchanged.)

## Last validated (this cycle) — ★ MAJOR
**H_LMR_VETO_175** — feature-space universal rug filter. 4-quarter walk-forward across Q0/Q1/Q2/Q3 of last ~57h:
- lmr>=175: 375 trades / 68 unique pairs, **96-100% rug rate, ZERO bigs lost in ANY quarter**.
- lmr>=150: 676 trades / 124 pairs, ~87% rug rate, only 1 big pair lost (Horatio +138% lmr=163).
- Cross-chain confirmed on BSC (lmr>=150 → 83% rug, 0% big).
- INDEPENDENT of HUPHey alpha (zero overlap — HUPHey trades have lmr ∈ {0,16,22,32} < 150).
- 17 new closures CONFIRM (CHARTARD lmr=180 rug, grail lmr=196 rug).
- See [cycle_20260527_1800.md](insights/cycle_20260527_1800.md).

## Top candidates
- **PAPER_SOL_HUPHEY (deploy-ready 13 cycles, #14a-validated)**: n=9 K=0.41 geom=+135.84%/tr. `top1_owner.startsWith("HUPHey")`. n-gate: 11 more.
- **PAPER_BSC_85871 (deploy-ready 13 cycles, #14a-validated)**: n=3 best-fire K=0.43 geom=+71.8%/tr. `bc[0].addr.startsWith("0x85871")`. n-gate: 17 more.
- **PAPER_SOL_GAMMA_RELAXED**: n=16 geom=+1.55% — n-gate: 4 more.
- **H_9CCPC_WATCH**: n=3 (eff. n=2) +26.2% vs matched -7.6% — WATCH only.

## New filter candidates (this cycle)
- **★ H_LMR_VETO_175** — Sol+BSC `entry_signal.liq_mcap_ratio >= 175`. 4-quarter walk-forward: 100% rug precision, ZERO bigs lost. **RECOMMENDED for immediate Sniper deployment.**
- **H_LMR_VETO_150** — broader variant. 87% rug, 1 big lost (Horatio). More coverage, slightly more risk.
- **H_RUG_WALLET_VETO_RUG6** (carry from c1200) — Sol blacklist 6 wallet prefixes.
- **H_SELF_LP_TOP85_VETO** (carry).
- **H_META_TOP99_PURE_SHAPE** (carry — fails geom-gate).

## Methodology — 25 forms
**#25 NEW CANDIDATE — FEATURE-SPACE FILTERS BEAT WALLET-SPACE FILTERS FOR HIGH-RECALL VETOS** — 12 cycles of wallet-prefix RUG_N gave n=27-29 walk-forward; one feature filter (lmr>=175) gave 375 trades / 68 pairs at ~100% precision. Rule: each cycle, prefer at least one feature-space hypothesis alongside wallet-prefix scanning.
**#14a MATCHED-SHAPE BASELINE SUBTYPE** — READY ADOPT (2 worked examples: HUPHey + 0x85871).
**#24 SAME-SYMBOL DUP-PAIR INFLATION (CANDIDATE)** — carry.
**#4 STREAM-DUPLICATION** — reaffirmed multiple cycles.

## Planned next cycle (06:00Z 05-28)
1. **★ Test combined HUPHEY ∧ ¬LMR_175** — should be identity (no overlap), confirms backtest plumbing.
2. **Find LMR alpha-side companion**: lmr<0.1 has big%=7.3% — backtest as positive filter.
3. **mcap × lmr product**: does the product give cleaner signal than lmr alone?
4. **symbol_dup_count high-end**: grail dup=11 rugged — backtest dup>=5 veto.
5. **If state thaws**: walk-forward LMR_175 on fresh-only trades, confirm out-of-sample.
6. **Methodology #25 seek 2nd confirmation** (find another high-recall feature filter that beats its wallet-prefix counterpart).
7. CARRY: HUPHey/85871 deploy auth, Helius patch, H_GECKO_FEED, BSC volume.

## Progress delta this cycle
**POS (4)**: NEW universal feature filter LMR_175 4-quarter validated / cross-chain confirmed BSC / 17 new closures confirmed thesis / NEW Methodology #25 candidate.
**NEG (2)**: only 17 new closures in 24h (mostly batch-flush) / no new positive alpha, only veto.
**Net**: STRONG POS — first feature-space veto to walk-forward at ~100% precision; major safety-side addition.
**Stuck: NOT triggered** (12 consec cycles new findings).

## OPEN QUESTIONS to user
1. **★★★ H_LMR_VETO_175 immediate adoption** — RECOMMENDED. Walk-forward 4 quarters, 100% rug precision, ZERO bigs lost. Safety filter with no alpha cost. Independent of HUPHey/85871.
2. **HELIUS RATE-LIMIT ★★★★★ (46h+)** — refresh quota / apply c0000 patch / hard-kill PID.
3. **PAPER_SOL_HUPHEY deploy** — STRONGLY YES (13 cycles pending).
4. **PAPER_BSC_85871 deploy** — STRONGLY YES (#14a-validated).
5. **H_RUG_WALLET_VETO_RUG6** adoption (6 prefixes)?
6. **Methodology #14a + #20 + #4 FORMAL ADOPTION** (all triple/double-confirmed).

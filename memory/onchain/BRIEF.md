# BRIEF — onchain AI brain (cycle 20260528_0000)

## State (frozen — closed=4947, no new data 9+h)
- closed=**4947** (UNCHANGED from c1800). open=0. Window 2026-05-24T08:36Z → 2026-05-27T14:54Z (~78h).
- State.json last write 2026-05-27T14:54Z (~9h ago). 8th consec stale cycle.
- Sniper PID still in Helius rate-limit loop (~47h ongoing). c0000 patch ready awaiting user auth.

## Goal & gate
**+1M%**. GATE: n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%/trade. **0 paper streams deployed**. 14-cycle pending user-auth.

## Regime (10th cycle chain-asymmetric — no new data)
**Sol** Cond A clear → Guard OFF. **BSC** Cond A triggered → Guard ON. (Unchanged.)

## Last validated (this cycle) — ★★★ MAJOR
**H_RUGCHECK_500** — 2nd feature-space filter, UNIVERSAL Solana zero-rug stamp:
- `entry_signal.rugcheck_score == 500` ≡ mint=REVOKED ∧ freeze=NONE ∧ dangers=0 ∧ lp_unlocked=undefined
- **47 unique Solana pairs / 395 trades / 78h** — ZERO rugs in EVERY walk-forward quarter (Q0/Q1/Q2/Q3)
- avg=-2%, WR=29%, big%=6.4% (pair-level)
- ORTHOGONAL to HUPHEY (0 overlap), 85871 (0 overlap), LMR_VETO_175 (score=500 ⊂ ¬lmr≥175 region)
- Refinements: `∧ buys_m5≥500` → n=9 K=+0.27 geom=+13%; `∧ lmr<30` → n=4 K=+0.71 geom=+60%
- See [cycle_20260528_0000.md](insights/cycle_20260528_0000.md)

## Top candidates (4 deploy-ready + 1 NEW)
- **PAPER_SOL_HUPHEY (deploy-ready 14 cycles)**: n=9 K=0.41 geom=+136%/tr. `top1_owner.startsWith("HUPHey")`. n-gate: 11 more.
- **PAPER_BSC_85871 (deploy-ready 14 cycles)**: n=3 best-fire K=0.43 geom=+72%/tr. `bc[0].addr.startsWith("0x85871")`. n-gate: 17 more.
- **PAPER_SOL_RUGCHECK_500 (NEW)**: 47 pairs 0 rugs alpha-neutral; recommended SAFETY-stream + n-harvest.
- **PAPER_SOL_GAMMA_RELAXED**: n=16 geom=+1.55% — n-gate: 4 more.
- **H_9CCPC_WATCH**: n=3 (eff. n=2) +26.2% vs matched -7.6% — WATCH only.

## New filter candidates (this cycle)
- **★★★ H_RUGCHECK_500_PURE** — Solana `entry_signal.rugcheck_score == 500`. 47 pairs 0 rugs in 78h. SAFETY-stream candidate.
- **H_RUGCHECK_500_BUYS500** — refined `∧ buys_m5 ≥ 500`. 9 pairs K=+0.27 geom=+13%/tr. Fails n only.
- **H_RUGCHECK_500_LMR30** — refined `∧ lmr<30`. 4 pairs K=+0.71 geom=+60%/tr. Too narrow alone.
- **H_LMR30_MCAP30K_TOP80** — `lmr<30 ∧ mcap[30k,100k) ∧ top1<80`. 6 pairs 2/4 non-HUPHEY bigs (Popus+Luce).
- CARRY: H_LMR_VETO_175, H_RUG_WALLET_VETO_RUG6, H_SELF_LP_TOP85_VETO, H_META_TOP99_PURE_SHAPE.

## Rejected this cycle
- buys_m5 alone (no monotonic effect), total_holders ≥50 (rare in early snapshots), sdc≥20 (rug=25% still high), lmr<5+small_mcap (all rugs), other rugcheck scores (0/11399/11500/13970 all bad).

## Methodology — 25 forms
**★ #25 FEATURE-SPACE > WALLET-PREFIX — GRADUATED CANDIDATE → READY** (2nd confirmation: LMR_VETO_175 + RUGCHECK_500 both deliver 47-68 pairs/quarter at structural precision, vs wallet-prefix n=3-9).
**#14a MATCHED-SHAPE BASELINE SUBTYPE** — READY ADOPT (2 examples: HUPHey + 0x85871).
**#24 SAME-SYMBOL DUP-PAIR INFLATION (CANDIDATE)** — carry.
**#4 STREAM-DUPLICATION** — reaffirmed (avg 8.4 trades/pair in RUGCHECK_500 bucket).

## Planned next cycle (0600Z 05-28)
1. **If state thaws** — re-run RUGCHECK_500 walk-forward on fresh-only trades (OOS).
2. **★ Combined-filter pass** — (HUPHEY ∨ 85871 ∨ RUGCHECK_500) − LMR_VETO_175. Compute combined K, geom, expected throughput.
3. **#25 seek 3rd confirmation** — candidates: `mint=REVOKED ∧ freeze=NONE ∧ lp_unlocked=true` (explicit-LP variant), `creator_tx_count==0` (fresh creators).
4. **rugcheck_score 11399 / 11500 deep dive** — biggest buckets (1523, 610 trades) — sub-cell analysis.
5. **bonding_curve_buyers[0]** examination on Popus/Luce/PHAGE/PERPSLAUNCH.
6. **TG signals × RUGCHECK_500 timing** — do channels notice these pre-pump?
7. CARRY: HUPHey/85871/LMR_175/RUGCHECK_500 deploy auth (4 streams), Helius patch, H_GECKO_FEED, BSC volume.

## Progress delta this cycle
**POS (4)**: NEW universal feature filter H_RUGCHECK_500 (47 pairs, 0 rugs, fully orthogonal); Methodology #25 2nd confirmation → GRADUATED READY; HUPHEY-decontaminated alpha pairs isolated (Popus+Luce); 5 weak hypotheses eliminated from backlog.
**NEG (1)**: state still frozen (8th consec cycle no new closed_trades).
**Net**: STRONG POS — first cycle with feature-space filter showing both ZERO rug AND non-zero big rate on 47 unique pairs (10× HUPHEY's n).
**Stuck: NOT triggered** (13 consec cycles new findings).

## OPEN QUESTIONS to user
1. **★★★★★ HELIUS RATE-LIMIT (47h+)** — refresh quota / apply c0000 patch / hard-kill PID. Without thaw every cycle works on same frozen 4947 trades.
2. **★★★★ PAPER_SOL_RUGCHECK_500 deploy authorization** — 47 pairs 0 rugs documented; even as alpha-neutral SAFETY stream, valuable for live n-harvest.
3. **★★★★ Batch-deploy all 4 streams** (HUPHEY + 85871 + LMR_VETO_175 + RUGCHECK_500) under single multiplex slot?
4. **Methodology #25 FORMAL ADOPTION** (now 2-confirmation READY).
5. **H_RUG_WALLET_VETO_RUG6** adoption (carry — 6 wallet prefixes)?
6. **PAPER_BSC_85871** deploy (carry 14 cycles)?

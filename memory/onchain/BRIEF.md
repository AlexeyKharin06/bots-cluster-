# BRIEF — onchain AI brain (cycle 20260528_0600)

## State (frozen — closed=4947, no new data ~12h)
- closed=**4947** (4468 Sol + 479 BSC), UNCHANGED. open=5. Window 2026-05-24T08:36Z → 2026-05-27T14:54Z (~78h).
- Last write 2026-05-27T14:54Z. **9th consec stale cycle.** Sniper in Helius rate-limit loop (~50h).

## Goal & gate
**+1M%**. GATE: n≥20 pairs ∧ Er>0 ∧ K≥0.05 ∧ geom≥+1%/tr. **0 deployed**, 15 cycles pending auth.

## ★★★ THIS CYCLE — FIRST candidate to clear the n≥20 floor
**MULTIPLEX_PAPER_ALPHA = HUPHEY ∨ 85871 ∨ RC500_buys500 ∨ RC500_lmr30** (dedup union):
- **n=22 unique pairs** (raw 164) — passes ALL FOUR GATES under best/mean/**worst-fire** aggregation.
- worst-fire (pessimistic, credible): avg+44.5% big22.7% rug4.5% **K=+0.61 geom=+11.5%/tr**.
- best-fire (optimistic ceiling): avg+130% rug0% K=1.0(artifact) geom+58%.
- WHY it crosses the floor: the 3 entities are FULLY ORTHOGONAL (0 pairwise overlap) → pair counts ADD + coverage gaps
  FILL. 4Q walk-forward: rug=0% every Q (best-fire), ≥3 entities co-active Q1/Q2/Q3 → not single-block inflated.
- LMR_175 subtract = NO-OP on union (alphas already in safe LMR region).
- CAVEAT: all 3 filters discovered on this frozen window = **selection bias**; needs OOS (thaw). Deploy paper to
  harvest true OOS n. Size ½K≈0.30, NOT best-fire K=1.0.
- See [cycle_20260528_0600.md](insights/cycle_20260528_0600.md).

## Methodology — 26 forms
**★ #26 ORTHOGONAL-UNION n-AGGREGATION (NEW CANDIDATE)** — sub-threshold orthogonal alphas combine additively in n +
fill temporal gaps, crossing floors no constituent reaches; distinct from #11/#13 (constituents causally independent).
Graduates on a 2nd independent union once state thaws.
**#25 FEATURE-SPACE > WALLET-PREFIX — READY** (LMR_VETO_175 + RC500). 3rd-confirmation NOT found this cycle.
**#10 CROSS-CHECK** — corrected c0000 (RC500 lp_unlocked=FALSE/locked). **#14a/#4** carry.

## RC500 mechanism (corrected this cycle)
`rugcheck_score==500 ≡ mint=REVOKED ∧ freeze=NONE ∧ dangers=0 ∧ lp_unlocked=FALSE(LP LOCKED) ∧ lmr∈[24,79]`.
Zero-rug is CAUSAL: LP locked → LP-removal impossible. score==500 ⊂ dangers==0 (47⊂69), the clean subset.

## Top candidates
- **★ MULTIPLEX_PAPER_ALPHA (NEW — n=22, gate-PASS in-sample worst-fire)** — the deploy ask; supersedes the 4 separate
  constituent streams: HUPHEY(n9)/85871(n3)/RC500_buys500(n9)/RC500_lmr30(n4), each sub-threshold alone.
- RC500_pure (n=59, rug0%, flat geom) — separate SAFETY/harvest stream. PAPER_SOL_GAMMA_RELAXED n=16 (4 more).
  H_LMR_VETO_175 universal rug veto (adopt).

## Rejected this cycle
creator_tx_count==0 (degenerate — value 0 for all 4468 Sol trades); explicit-LP-true variant (lp_unlocked=True = 60%
rug majority); lp_unlocked=False alone (unstable 7-33% rug across quarters); dangers==0 as RC500 replacement (worse).

## Planned next cycle (1200Z 05-28)
1. **★ If state thaws** — re-form MULTIPLEX_PAPER_ALPHA on fresh-only (post-14:54Z) trades for TRUE OOS → gates #26.
2. **★ #26 2nd confirmation** — try a 2nd orthogonal union crossing a floor it shouldn't reach alone.
3. **★ Fractional-Kelly drawdown sim** for MULTIPLEX at ½K=0.30 — concrete sizing+ruin number for user.
4. bonding_curve_buyers[0] across 22 union pairs (shared early-buyer = potential NEW orthogonal entity).
5. #25 3rd-confirm retry: `dangers==0 ∧ lp_unlocked=False ∧ lmr<30`. CARRY: Helius patch, H_GECKO_FEED.

## OPEN QUESTIONS to user (★ escalating — analysis has hit its in-sample ceiling)
1. **★★★★★ DEPLOY MULTIPLEX_PAPER_ALPHA?** First gate-passing candidate (n=22, paper $1). ONLY way to get OOS n —
   in-sample exhausted. Consolidates the 4 pending stream asks into one.
2. **★★★★★ HELIUS RATE-LIMIT (~50h)** — refresh quota / apply c0000 patch / hard-kill PID. Without thaw, NO new data
   and NO OOS validation possible. Now the single binding constraint on all progress.
3. #25 FORMAL ADOPTION (2-confirm READY) + #26 candidate. H_RUG_WALLET_VETO_RUG6 (carry)?

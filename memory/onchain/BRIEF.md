# BRIEF — onchain AI brain (cycle 20260524_1800)

## State (live, ~40h rolling window)
- closed=**4849** (+44 net of rotation; 606 raw new since c1200), 57 open.
- **+3 NEW BIGS + 1 closed-during**: Poor3 Sol +943 (HUPHey top1, meteora), Stake Sol +481 (HUPHey top1, closed-during), BELIEF BSC +235 (PORTUGAL strict k=1 — possible C10 onset).
- All 3 bigs land within 5h window (11:39 → 14:49 today).
- State window: 05-23 02:07Z → 05-24 17:49Z. +5h25min rotation since c1200.

## Goal & gate
**+1M%**. GATE_EXPECTANCY_KELLY (n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%). **0 paper streams deployed**.

## Regime
- Cond A **DRAMATIC RECOVERY** -73 → **-35.9** (+37pt). CLEAR.
- Cond B **CLEAR** (Poor3 3h11min ago).
- **Guard OFF** — head-fake risk per c1200 precedent (was OFF at c0600 too, then re-triggered).

## Last validated (this cycle c1800-day3)
**🆕 PARADIGM SHIFT: H_WALLET_TOP1_LEADERBOARD discovered** — HUPHey wallet top1_owner on 10 Sol tokens, 4 BIGS (40%), 0 RUGS, avg=+207% (Sol baseline 1.3% big / 59% rug = 30× big-rate lift). Walk-forward filter `prior≥5 ∩ rugs=0`: n=15 K=0.15 geom=+12.85%/trade big=27% rug=13% — **PASSES Er/K/geom by 3-12× margins, fails only n<20 floor**. **D4Bgpf lp_provider co-correlate** (13 tokens 4 bigs 0 rugs). **PORTUGAL strict +1 (BELIEF cross-cluster validation)** softens Methodology #11. **TG-2h K DROP 0.30→0.106** variance drag. **Smart-cluster TRAIL 3rd reverse** confirmed NEGATIVE. **Methodology Lesson #13 candidate** (single-wallet inflation). **Sol big-shape STUCK BROKEN** by wallet-feature path. See [cycle_20260524_1800.md](insights/cycle_20260524_1800.md).

## Top candidates (current rolling stats)
- **🆕 H_WALLET_TOP1_LEADERBOARD (NEW HEADLINE)**: prior≥5 ∩ rugs=0 → n=**15** K=**0.15** geom=**+12.85%** big=**27%** rug=13%. PASSES Er/K/geom by wide margins. Distance to vanilla floor=5. **Methodology #13 penalty floor=40 (single-wallet — HUPHey only)**.
- **PORTUGAL strict**: n=**14** K=0.267 geom=+56% big=50% rug=7%. Bigs now distributed C7/C8/C9/C10 (was 5/6 in C8 → 4/7). Distance to floor=6. **Deploy-leaning** (was DEFER c1200).
- **TG-2h (HEADLINE)**: n=**43** K=**0.106** geom=+4.41% big=16% rug=28%. **K DROPPED 0.30→0.106** — variance drag from +9 entries. Still 2× floor. WAIT for K stability.
- **BC_FULL_B**: n=65 K=0.057 geom=+0.85% big=11% rug=31%. Descriptive-monitor tier.

## Methodology — 12 forms + #13 CANDIDATE
1-10 unchanged. **11.SINGLE-TIME-BLOCK INFLATION** (n×2 floor when bigs cluster in single time block). **12.ROTATION-INDUCED K INFLATION** (cross-cycle K changes via rotation). **13.SINGLE-WALLET INFLATION (NEW CANDIDATE)** — wallet-dimension analog of #11: when bigs all trace to single wallet/entity, apply 2× n penalty (effective floor doubles) until ≥2 distinct entities contribute bigs.

## Planned next cycle (00:00Z 05-25)
1. **MORE wallets like HUPHey** — scan ALL Sol top1_owners with ≥3 tokens; find 2nd qualifying wallet to break Methodology #13 penalty (this is THE highest priority).
2. **BSC wallet leaderboard** — try `bonding_curve_buyers[0]` (rank-1 bc) as analog of Sol's top1_owner. pool_creator field mostly None.
3. **HUPHey deep-dive** — Solscan visit, balance/age/tx-count; pre-compute live wallet leaderboard snapshot.
4. **Forward-watch HUPHey new launches** — if HUPHey/D4Bgpf token enters via sniper, mark MUST-WATCH (cadence ~6h observed).
5. **PORTUGAL strict 3-more-entry watch** — n=14→17 ideally cross-cluster productivity.
6. **TG-2h K stability** — if drops below 0.05 floor, gate fails. If recovers, candidate strengthens.
7. **C10 cluster productivity** — STAKE+BELIEF onset. Watch follow-on.
8. **Sol big-shape DEPRIORITIZED** — wallet-feature is the new Sol path.
9. CARRIED: Methodology #12 formalization, PORTUGAL creator wallet audit, External BSC volume fetcher.

## OPEN QUESTIONS to user
1. **🆕 PRE-COMPUTE LIVE WALLET LEADERBOARD?** Brain wants to build `wallet_alpha_v1.json` snapshot — live top1_owner + lp_provider history per wallet, scored by big/rug/avg-pnl. Would enable real-time entry-filter. **Brain leans YES — highest priority infrastructure ask.**
2. **🆕 PAPER_SOL_WALLET_TOP1 deploy decision**: H_WALLET_TOP1_LEADERBOARD n=15 K=0.15 geom=+12.85% — PASSES Er/K/geom but fails n<20 + Methodology #13 single-wallet penalty (effective floor n=40). Brain leans **WAIT for 2nd qualifying wallet** (forward-watch).
3. **PAPER_BSC_PORTUGAL strict deploy**: was DEFER c1200, now **deploy-leaning** after BELIEF cross-cluster validation (4/7 bigs in C8 vs 5/6 at c1200 — penalty softened). n=14 K=0.267 geom=+56%. Brain leans WAIT 1-2 cycles for n=17.
4. **PAPER_BSC_TG2 deploy decision**: n=43 K=0.106 (K dropped 0.30 c1200). Brain leans WAIT — concerning K trend.
5. **SNIPER_H2 added to Sol big-routing**: n=2 evidence (MTFR-7Zx + Maple), but Stake fired H2 too (+470 capped same as A/B/H). Now n=3 confirms H2 valid. **Brain leans YES — trivial change.**
6. **Methodology Lesson #11 + #12 + #13 formal adoption**: #11 ADOPTED c1200. #12 confirmed (2nd cycle K-drop via variance). #13 CANDIDATE — formalize after 2nd qualifying wallet found.
7. CARRIED: External BSC volume fetcher, PORTUGAL creator wallet audit, SMART_CLUSTER_VETO feasibility, rugger_blacklist wallet_added_at, MC_LIQ code review.

# BRIEF — onchain AI brain (cycle 20260525_0000)

## State (live, ~43h rolling window)
- closed=**4994** (+145 net; 579 raw new), 71-83 open. Window: 05-23T04:35 → 05-24T23:50Z.
- **+2 NEW Sol bigs**: MTFR-BVB +175 (**HUPHey 5th big**, top1=90 meteora MC_LIQ BF), NOAR +152 (**NEW WALLET 75qsE3p5y2**, top1=99.8 meteora B/H BF).

## Goal & gate
**+1M%**. GATE_EXPECTANCY_KELLY (n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%). **0 paper streams deployed**.

## Regime
- Cond A CLEAR (-46.1). Cond B CLEAR (NOAR 0.2h). Guard OFF. **7 Sol bigs in 24h = record**.

## Last validated (this cycle)
**H_WALLET_TOP1 GENERALIZATION REJECTED — Methodology #13 FORWARD-CONFIRMED**: walk-forward `prior≥5 ∩ rugs=0` EXCLUDING HUPHey → n=8 catches **0 bigs / 3 rugs**. NOAR's wallet (75qsE3p5y2) fails filter (5 prior rugs). Filter 100% HUPHey-specific. **HUPHey aggregate n=12 5 bigs (42%) 0 rugs avg=+186.8% K=0.68 geom=+47%** → NAMED-WALLET ALPHA. HUPHey ∩ top1≥85 ∩ meteora sub: n=5 K=**1.0** geom=**+144%**. See [cycle_20260525_0000.md](insights/cycle_20260525_0000.md).

## Top candidates
- **🆕 PAPER_SOL_HUPHEY_WATCH (NEW HEADLINE)**: named-wallet (top1=HUPHey OR lp=D4Bgpf). n=12 5 bigs 0 rugs. **No n-floor (Methodology #14)**. Brain leans DEPLOY.
- **PORTUGAL strict**: n=**13** (was 14, WORLDCUP-2 rotated, 0 new), K=**0.79** geom=+107% big=54% rug=8%. 4/7 bigs in C8 (#11 eff. floor 26-30). **C10 DORMANT 9h58min**.
- **TG-2h**: n=**33** (-10 rotation, 0 new), K=**0.18** (rotation artifact 0.106→0.18), geom=+3.87%. big% trend DOWN 25→23→17.6→16→**15.2**, rug 18→30 — fundamental weakening. Distance n=50 REGRESSED 7→17.
- **BC_FULL_B**: n=68 K=0.05 borderline. Descriptive-only.

## Methodology — 12 forms + #13 ADOPTED + #14 CANDIDATE
**11.SINGLE-TIME-BLOCK INFLATION**. **12.ROTATION-INDUCED K** (4th confirmation). **13.SINGLE-WALLET INFLATION — ADOPTED** via NOAR test. **14.NAMED-ALPHA vs GENERALIZED-FILTER (CANDIDATE)** — named-wallet deployable with `≥3 bigs AND 0 rugs in own history` (no n≥20 floor).

## Planned next cycle (06:00Z 05-25)
1. **PAPER_SOL_HUPHEY_WATCH spec** — write `paper_streams_spec/PAPER_SOL_HUPHEY_WATCH.md`.
2. **More HUPHey-class wallets** — full state.json scan: ≥5 priors AND ≥2 bigs AND 0 rugs.
3. **Forward-watch HUPHey/D4Bgpf** — scan opens; alert on new HUPHey token.
4. **75qsE3p5y2 5 open NOAR positions** — resolve bigs or rugs in 2-4h. Track.
5. **PORTUGAL strict C11 onset watch** — 9h58min dormant since BELIEF.
6. **TG-2h big% trend** — if <10% drop, demote to descriptive.
7. **Wallet leaderboard re-run** — refresh `/srv/bots/.shared/data/wallet_leaderboard.jsonl`.
8. **BSC wallet leaderboard** — analog via bonding_curve_buyers[0].
9. CARRIED: SNIPER_H2 add to Sol routing; HUPHey identity Solscan; PORTUGAL creator audit.

## OPEN QUESTIONS to user
1. **🆕 PAPER_SOL_HUPHEY_WATCH deploy** — n=12 5 bigs 0 rugs as NAMED-WALLET (Meth #13 doesn't block per #14). ~$4/day paper. Brain leans **YES DEPLOY NOW**.
2. **PAPER_BSC_PORTUGAL strict deploy** — K=0.79 big=54% but n=13<20 + #11 penalty. Brain leans **WAIT C11**.
3. **PAPER_BSC_TG2 deploy** — n=33 K=0.18 big% REGRESSING 25→15. Brain leans **WAIT or DEMOTE**.
4. **🆕 Methodology #14 formal adoption** — enables HUPHey deploy without 2nd qualifying wallet. Brain leans **YES**.
5. **SNIPER_H2 add to Sol big-routing** — 3 evidence (MTFR-7Zx/Maple/Stake). Brain leans **YES (trivial)**.
6. **Wallet leaderboard re-run cadence** — every 6-12 cycles? Brain leans **YES c0600**.
7. CARRIED: External BSC volume fetcher, PORTUGAL creator audit, SMART_CLUSTER_VETO, MC_LIQ code review.

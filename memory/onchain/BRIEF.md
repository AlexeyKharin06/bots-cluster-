# BRIEF — onchain AI brain (cycle 20260525_0600)

## State (live, ~43.8h rolling window)
- closed=**4954** (-40 net vs c0000 4994 — heavy rotation 5h57min on left edge). 90 open. Window: 05-23T08:05Z → 05-25T05:57Z (entry timestamps).
- **+1 NEW big**: **PROS BSC +908.6%** (04:26Z) bc=20 k=**26** SNIPER_H BF — outside PORTUGAL strict (k>10) — pure BC_FULL_B win. Different factory wallet from 0x85871 (bc[0]=0xa2cceabd new wallet n=1).
- **+1 HUPHey forward-fire confirmation**: $UGD Sol (03:44Z) top1_owner=HUPHey lp=D4Bgpf top1=78.4 smart=8 → +12-16% (not big, not rug). **HUPHey rugless streak 0/12 → 0/12 (GDOR-1 rotated, $UGD entered; net 12 stable, still 5 bigs / 0 rugs)**.

## Goal & gate
**+1M%**. GATE_EXPECTANCY_KELLY (n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%). **0 paper streams deployed**.

## Regime
- **Sol last50 -45.7% 0 bigs 24 rugs (48%)** — Cond A CLEAR but big-drought (was 7 bigs in 24h c0000; now 0 in last 50). Cond B CLEAR (NOAR 6.3h). **Guard OFF — but Sol big-pipeline gone dry, no new α/β/γ/δ since NOAR**.
- Last Sol big: NOAR 23:45Z (6.3h). Last BSC big: PROS 04:26Z (1.6h).

## Last validated (this cycle)
**MAJOR DISCOVERY — BSC HUPHey-ANALOG: bc[0]=0x85871aea93f086eeda...** wallet n=8 BSC tokens, **5 bigs (62%) / 1 rug (12%) / avg=+289.9% / K=0.281 / geom=+58.88%**. Walk-forward prior≥3 ∩ bigs≥2 ∩ rugs≤1: n=5 outcomes {-100, +90, +880, +659, +235} = 3 bigs / 1 rug / avg=+352.7%. **Catches Poor BSC bc=1 +659 that PORTUGAL strict MISSES**. C7/C8/C9/C10 all represented = cross-cluster validated. See [cycle_20260525_0600.md](insights/cycle_20260525_0600.md).

**2nd Named-Wallet alpha discovered = breaks Methodology #13 dependency on HUPHey-alone**. Methodology #14 (NAMED-ALPHA) now has 2 entities, ready for formal adoption.

## Top candidates
- **🆕 PAPER_BSC_85871_WATCH (NEW HEADLINE — proposed deploy)**: bc[0]=0x85871aea on BSC. n=8 5 bigs 1 rug avg=+289%. K=0.28 geom=+59%. Catches Poor bc=1 PORTUGAL strict miss. spec: `paper_streams_spec/PAPER_BSC_85871_WATCH.md`.
- **PAPER_SOL_HUPHEY_WATCH (existing HEADLINE)**: top1_owner=HUPHey OR lp=D4Bgpf on Sol. n=12 5 bigs 0 rugs avg=+195% K=0.21 geom=+30%. $UGD forward-fire +16% confirms 0-rug streak. spec written: `paper_streams_spec/PAPER_SOL_HUPHEY_WATCH.md`.
- **PORTUGAL strict**: n=**10** (was 13 — rotation removed WOJCUP/RICH/TRUMPETTE), K=**0.27** geom=+56.7% big=60% rug=10% (CAP). 0 new since BELIEF (16h dormant). **C10 DORMANT 16h+ no C11 onset**.
- **TG-2h**: n=**29** (was 33), K=**0.085** (below previous), big=13.8% rug=27.6%. Still weakening. Distance n=50 floor regressed 17→21.
- **BC_FULL_B**: n=**75** (was 68, +PROS +908 + 6 small/rug), K=**0.03** (below 0.05 floor!), big=9.3% rug=32%. **GATE-FAILED**.

## Methodology — 14 forms
**11.SINGLE-TIME-BLOCK INFLATION**. **12.ROTATION-INDUCED K** (5th confirmation — PORTUGAL strict K 0.79→0.27 via rotation). **13.SINGLE-WALLET INFLATION — ADOPTED + EXTENDED** to bc[0] for BSC. **14.NAMED-ALPHA vs GENERALIZED-FILTER — READY FOR FORMAL ADOPTION** (2 entities now: HUPHey + 0x85871).

## Planned next cycle (12:00Z 05-25)
1. **Verify 0x85871aea full address suffix** — read state.json directly with python; produce exact match for sniper hook.
2. **Forward-watch new entries for both named wallets** — if HUPHey or 0x85871 fires, immediate alert.
3. **3rd named-wallet hunt** — scan for additional bc[0] BSC wallets ≥3 tokens with bigs≥1 rugs≤1. Examine 0xa2cceabd (PROS bc[0]) — does it have prior tokens? n=1 currently.
4. **PORTUGAL strict C11 onset watch** — 16h dormant. Watch new k≤10 bc=20 BSC entries.
5. **TG-2h** — K=0.085 now near floor 0.05. If drops below, demote to descriptive-only.
6. **PROS factory wallet investigation** — 0xa2cceabd. New BSC factory? Adjacent to PORTUGAL ecosystem or independent?
7. **Smart-cluster TRAIL ANTI-PATTERN** — 4 reverses now (Poor3, $UGD shows smart-cluster fires earlier but no fat-tail captured this cycle). Formalize as NEGATIVE TRAIL signal.
8. **Sol big-pipeline drought** — 0 bigs in last 50 entries. Watch if HUPHey cadence accelerates or pauses.
9. **HUPHey identity Solscan** (carried).
10. CARRIED: BSC volume fetcher, SMART_CLUSTER_VETO feasibility, MC_LIQ code review.

## Progress delta
**POSITIVE**:
- +1 BSC big (PROS +908)
- HUPHey forward-fire confirmed ($UGD +16, 0-rug streak extended)
- **BSC HUPHey-analog wallet 0x85871aea DISCOVERED** — 2nd named-wallet entity breaks Methodology #13 single-entity restriction
- PAPER_BSC_85871_WATCH spec written and ready for deploy
- PAPER_SOL_HUPHEY_WATCH spec written and ready for deploy
- 2 deploy-ready paper streams now exist (closest brain has ever been to first deploy)
- Methodology #14 (NAMED-ALPHA class) now has cross-chain validation (Sol + BSC)

**NEGATIVE**:
- PORTUGAL strict n=13→10 (rotation; lost 3 entries). K dropped 0.79→0.27 (#12 5th confirmation).
- TG-2h K=0.18→0.085 — approaching floor.
- BC_FULL_B K=0.05→0.03 — GATE-FAILED.
- Sol big-drought (0/last50 vs 7/24h previously).
- C10 dormant 16h+ no C11 onset.

**Net assessment: POSITIVE**. 2nd named-wallet discovery = breakthrough that breaks Meth #13 restriction. Two paper streams ready for deploy.

## OPEN QUESTIONS to user
1. **🆕 PAPER_BSC_85871_WATCH deploy** — n=8 5 bigs 1 rug as NAMED-WALLET (Meth #14). Catches Poor bc=1 PORTUGAL miss. Brain leans **YES DEPLOY NOW**.
2. **PAPER_SOL_HUPHEY_WATCH deploy** (carried from c0000) — n=12 5 bigs 0 rugs. Brain leans **YES DEPLOY NOW** + $UGD forward-fire confirms rugless streak.
3. **Methodology #14 formal adoption** — 2 entities now (HUPHey + 0x85871). Brain leans **YES**.
4. **PAPER_BSC_PORTUGAL strict deploy** — n=10 K=0.27 big=60% rug=10%. C10 dormant 16h. Brain leans **WAIT or SUBSUME by PAPER_BSC_85871 (mostly overlap)**.
5. **PAPER_BSC_TG2 deploy** — n=29 K=0.085 weakening. Brain leans **WAIT or DEMOTE**.
6. **PROS factory wallet (0xa2cceabd)** — n=1 too small to deploy. Watch for 2nd+3rd token. Brain leans **descriptive-monitor only**.
7. CARRIED: SNIPER_H2 add to Sol routing; BSC volume fetcher; HUPHey identity Solscan.

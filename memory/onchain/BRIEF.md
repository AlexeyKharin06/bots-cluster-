# BRIEF — onchain AI brain (cycle 20260523_1800)

## State (live, rolling ~38h)
- closed=**4982** (+99 vs c1200). BSC uniq 138 (+4). Sol uniq 586 (+26). **11 open** (-14).
- **+6 NEW BIGS (largest single-cycle delta ever)**:
  - **C8 BSC PORTUGAL EXPLOSION — 4 bigs in 3h12min, all SNIPER_B BF, 100% conversion**: VELVET +636 (12:25 k=7), xing +293 (13:16 k=1), TRUMPBANK +349 (15:13 k=1), BABYTROLL +663 (15:37 k=1)
  - **TKLV +254 first bc<16 broader-band big** (17:09 k=15 bc=13 SNIPER_H, inside active TG window)
  - **GIVE +308 first Sol big in 31h** (12:25 BF=SNIPER_SMART_TOP_AGE5 — breaks Cond B)
- state.json earliest: 2026-05-22T03:56Z (C4 CTM aged out).

## Goal & gate
**+1M%**. GATE_EXPECTANCY_KELLY (n≥20 ∧ Er>0 ∧ K≥0.05 ∧ geom≥1%). 0 paper streams deployed. **PAPER_BSC_TG2 outlier-strong + PAPER_BSC_PORTUGAL deploy-ready-at-sub-floor** both pending user.

## Regime
- **Cond A TRIGGERED -63.3** (c1200 head-fake confirmed; was CLEAR -47.8).
- **Cond B CLEARED** (GIVE breaks 31h FATU).
- Guard ON via Cond A alone (cross-condition swap).

## Last validated (this cycle, c1800-day2)
**C8 EXPLOSION + TKLV + GIVE**. **TG-2h TEST n=40 K=0.181 geom=+11.73% big=25% rug=18% — STRONGEST EVER**, exceeds c0600 peak; 10/10 TG-eligible bigs; 4 productive clusters (C5+C6+C7+C8) individually pass gate. **PORTUGAL strict n=15 K=0.372 geom=+82.63% big=60% rug=0%** — all strengthen further. H_BSC_BC_FULL_B UN-DEMOTED (K 0.101→0.149). METLIFE A-wins-on-k=1 REJECTED-OVERFIT (3 new k=1 SNIPER_B BF refute). C7 alpha-cooling CANCELLED (C8 100% refutes). H_CLUSTER_PORTUGAL_PRESENCE 6/8=75%. **Distance to first deploy closest ever**. See [cycle_20260523_1800.md](insights/cycle_20260523_1800.md).

## Top candidates
- **H_BSC_BC_TIME_GATED_PORTUGAL_2H** (HEADLINE OUTLIER-STRONG): n=40 K=0.181 geom=+11.73% big=25% rug=18%, 10/10 bigs caught, 4-cluster validated. Spec: bc≥16 ∩ (k≤10 OR within 2h of prior bc≥16∩k≤10), routing {B,F2,D2,A,H}.
- **H_BSC_BC_PORTUGAL** strict k≤10 (DEPLOY-READY-AT-SUB-FLOOR): n=15 K=0.372 geom=+82.63% big=60% rug=0%. 5 below n=20 floor.
- **H_BSC_BC_FULL_B** UN-DEMOTED: n=61 K=0.149 geom=+5.60% big=16.4%.
- **H_SOL_EPSILON_SHAPE** NEW n=1 (GIVE): smart=8 k=15 liq=$23K meteora top1=null buys=null.
- **H_SMART_CLUSTER_TRAIL_EDGE** NEW n=1: smart-cluster streams beat A/H by 137pp trail on GIVE (distinct from c1328 entry-VETO direction).
- **H_BSC_BC<16_BROADER_BIG** NEW n=1: TKLV bc=13 k=15 in active TG window → big.

## Methodology — 9 forms (lesson #9 FORMALIZED this cycle)
1.Hindsight·2.Counting·3.Time-loc·4.Post-entry·5.Stale-DB·6.Single-cluster·7.Percentile-redraw·8.Regime-ctx·**9.STATE-ROTATION (FORMALIZED)**: symmetric — no-big-rotates + new-bigs-land = un-masked recovery; both = cancel. Track rotation log.

Best-fire=upside; first-fire=production. Cross-cluster ≥3 mandatory (TG-2h has 4). FIXED TEST boundary. Variance-Kelly.

## Planned next cycle (00:00Z 05-24)
1. C8 wind-down monitoring (last C8 PORTUGAL BABYTROLL 15:37; TKLV 17:09 in window).
2. C9 detection (next bc≥16∩k≤10 onset after >3h gap).
3. TG-2h n≥50 (now 40 = 80%).
4. PORTUGAL strict → n=17-18 if any new PORTUGAL.
5. Sol Cond A monitoring.
6. GIVE-shape replication check (next Sol big).
7. Smart-cluster trail edge replication (next Sol big).
8. PAPER_BSC_TG2 + PAPER_BSC_PORTUGAL spec docs if user approves.
9. CARRIED: PORTUGAL creator wallet audit (12+ tokens), SMART_CLUSTER_VETO, External BSC volume fetcher, MC_LIQ vs A code review (MC_LIQ caught GIVE).

## OPEN QUESTIONS to user
1. **PAPER_BSC_TG2 deploy (NOW OUTLIER-STRONG)**: n=40 K=0.181 geom=+11.73% big=25 rug=18 — strongest ever. Routing {B,F2,D2,A,H}. Auto-stop K<0.05 after 30 OR cum<0 after 50 OR 10-streak no-big avg<-30%. $1 paper.
2. **PAPER_BSC_PORTUGAL strict deploy at SUB-FLOOR n=15** parallel? K=0.372 geom=+82.63% big=60% rug=0%. Brain leans deploy with disclosure.
3. A-stream drop experiment (METLIFE refuted) — keep A as hedge (brain leans yes)?
4. H_SMART_CLUSTER_TRAIL_EDGE retroactive audit ~30min?
5. Methodology #9 ADOPTED — notify user.
6. CARRIED: External BSC volume fetcher; PORTUGAL creator wallet audit (12+ tokens); rugger_blacklist `wallet_added_at`; MC_LIQ vs A code review.

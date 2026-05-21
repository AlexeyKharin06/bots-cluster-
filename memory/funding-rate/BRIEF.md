# BRIEF — funding-rate snapshot (last update: 2026-05-21 11:00 UTC)

## State
- Data: `/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json` (38MB, ms-int timestamps; `buy_sell_ratio_m5` stored as str)
- **4826 closed_trades** (was 4993 — state TRIMMED, sliding ~2.5d window), 0 open, cycle=30531
- 20+ paper streams active. NONE production-promoted, NO real money.

## Regime — slight degradation, lottery returned
- last_100: **avg -36.1%, WR 30%, rug 37%, 3x 0%** (was -27.7% prev cycle, -8.4pp drift)
- last_200: avg -31.7%, rug 43%, 2x 6.5%, 3x 0%
- 0-6h: avg -17.1%, rug 31%, **2x 5.0%, 3x 2.3%** ← lottery hits returned
- Current live gate value: **0.37** (above ≤0.20 threshold → gate would PAUSE)
- 3-day arc: -35% → -52% → +pos → -63% → -27.7% → **-36.1%** (6-12h cycle confirmed again)

## 🔴 WALLET-TAGGER recovered (drift was transient pocket)
- Newest 165 trades: smart_avg 4.12→**6.84**, known_avg 12.79→**21.18**, both_avg 1.26→**2.08**
- BUT `top1=0` HALVED (10.4%→4.8%) — fewer fully-decentralized tokens. H17 strict still fires ZERO.
- Lesson: single-cycle drift detection needs 2+ cycle confirmation before action.

## STRONGEST validated edges (this cycle, anchored cut 2026-05-20 15:35Z)
| signal | n_test | n_unique | avg test | rug | 2x/3x | Verdict |
|---|---|---|---|---|---|---|
| **Regime gate ≤0.20** | 271 | — | **+6.5** | 22 | 8/5.0 | **POSITIVE-abs, +40pp lift, validated** |
| Regime gate ≤0.25 | 351 | — | +1.5 | 28 | 9/5.0 | also positive-abs |
| **H25 RELAXED (smart=0 ∧ top1=0 ∧ both≥5)** | 75 | **29** | **+28.2 dedup** | 45 | **14/10.3** | **promising_high_priority — near-promotable lottery** |
| H24 (rugcheck_score 100-1000) | 108 | 15 | -5.8 dedup | **0** | 0/0 | promising rug-filter (Sharpe) |
| H20 MID-CLUSTER | 80 | 9 | +28.0 dedup | 0 | 11/0 | promising_needs_accum (target 20) |
| H26 (H25 + gate ≤0.20) | 8 | 4 | **+328 dedup** | 50 | 50/50 | extreme lottery, n too small |

## H25 vs H17 — relaxation insight
- H17 strict `known≤1` was a CONFOUND. Drop it → 23 MORE unique lottery candidates. Same big winners (MC +1268, WORLDCUP +971, CATCOIN +542, COMPUTE +856) PLUS 币安队长 +105, CMC +288, 马维斯 +15, etc.
- Stream attribution (test, H25 entries): **SNIPER_B +28% vs SNIPER_A -62% (+90pp gap)** confirms exit-side dominance (H18). SNIPER_F/F2/D/D2 +136% (n=3 each, WR 100%, rug 0%) — possibly even stronger exit.

## Notable stream observations (last 500)
- SNIPER_VOL_VEL: rug 12%, n=17 (cleanest) — **audit filter**
- SNIPER_ULTRA_TRIPLE: rug 18%, n=11 — new clean stream
- SNIPER_D/D2: **+20.9% avg**, n=13 each — best raw avg
- SNIPER_LOWCAP: rug 62% — confirmed bad
- SNIPER_MC_LIQ: name misleading (only 35% of trades in $50-200k range)

## Validated negatives — DON'T retest
- interval-prediction (2-9% live precision); fair-price scalping (0/5wk); listing momentum (32% WR); microcaps expansion (-86%); known<5+smart 3-5 (R8 regime artifact); single-feature filter alone (R10); H11 lottery cluster (R11 rug 79%); H12 both≥5 standalone (R12 rug 82%); H15 both=0 standalone (-46% test); **H17 strict known≤1** (DEPRECATED — confound; use H25)
- bsr_m5 >5 = rug signal (89% rug ≥10); rugcheck_dangers=2 = -80% avg / 71% rug

## Next cycle priorities
1. **Draft H25 paper stream `SNIPER_PURE_BOTH_RELAXED_B_EXIT`** if user permits
2. **SNIPER_D/F-family exit logic audit** (may outperform B on lottery archetype)
3. **Validate rugcheck_score=500 semantics** (sentinel vs low-risk tier)
4. **H28 IDEA**: H25 + rugcheck_dangers ≤1 + bsr 0.5-2 joint filter
5. **H20 accumulation** to n_unique≥20 (currently 13)
6. **Feature mine** serial_supply_pct, lp_unlocked, freeze_authority, creator_tx_count
7. **Re-validate gate ≤0.20** as test split grows past n=271

## Open questions for user (BLOCKERS)
1. Permission to propose paper stream `SNIPER_PURE_BOTH_RELAXED_B_EXIT` (H25+B-exit)? n_unique=29, 10.3% 3x.
2. Permission to read shared serial_sniper code? Need it for SNIPER_D/F exit logic + VOL_VEL/ULTRA_TRIPLE filters + rugcheck pipeline docs.
3. KPI revision (4th cycle): allow promotion if **rug≤30% OR 3x_rate≥10%** (H25 hits 3x bound)?
4. PROJECT_CONTEXT.md still says funding-rate arb — formally pivot or split memory dir?
5. Treat gate threshold as regime-dynamic vs fixed ≤0.20?

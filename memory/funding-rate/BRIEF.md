# BRIEF — funding-rate snapshot (last update: 2026-05-20 23:00 UTC)

## State
- Data: `/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json` (38MB)
- 4877 closed_trades (count dropped from 4978 — state.json was trimmed), 25 open, cycle=30290
- 20+ paper streams active. NONE production-promoted, NO real money.

## Regime — REVERTED to hostile (clean pocket was transient)
- **last 100: avg -63%, WR 18%, rug 66%** — back to baseline-hostile
- 0-1h: -68%/70% rug; 0-3h: -57%/55% rug; 0-12h: -47%/48% rug
- 3-day arc: -35% → -52% → +pos pocket → -63% (current)
- Confirmed: regime DOES flip on 4-6h timescale. Regime gate is a necessary feature.

## Discovered this cycle: H17 PURE_BOTH archetype
- Signature: **smart=0 ∧ known≤1 ∧ both≥5 ∧ top1=0 ∧ liq_mc≥50 ∧ mcap≤25k ∧ age≤15min**
- Test split (13h): 6 unique tokens, 0% rug, 17% 3x rate
- 4 top winners ALL match (MC +1268%, WORLDCUP +971%, CATCOIN +542%, COMPUTE +856%)
- Sample too small for promotion (train n=2 PORTUGAL only). Need accumulation.
- Distinct from REJECTED H12 (any `both≥5`): H17 requires smart∧known counts near-zero so `both` is the WHOLE wallet signal. The wallet-tagger classifier matters here.
- See `insights/cycle_20260520_2300.md`

## EXIT-LOGIC alpha — `early_exit_ratio_99` (SNIPER_B)
- 16 same-entry A vs B pairs: B beat A by **+344pp avg**
- Mechanism: rug-avoidance (exits +10-30% on tokens A holds to rug_no_data -100%) AND big-winner capture (+500 to +1268%)
- Likely THE most important alpha — same entry, different exit logic, 6-figure %% lift
- Implication: H17 + B-exit is the target combo

## Hypothesis frontier
| H | Filter | n_test | dedup | avg | rug | 3x | Verdict |
|---|--------|--------|-------|-----|-----|-----|---------|
| Regime gate ≤0.25 | trail100 rug ≤0.25 | 112 | 19 | -6.9% raw / -27 dedup | 26% | 4.5% | **Persistent +39pp lift** |
| **H17 PURE_BOTH** | smart=0 ∧ known≤1 ∧ both≥5 + tight | 12 raw | 6 | +318 raw / +21 A-dedup / **+614 B-dedup** | 0% | 17% | **NEW high-priority** |
| H12 both≥5 standalone | bucket | 177 | 43 | -34% / -59 dedup | 69-90% | 6.2 | **REJECTED** cluster-rug |
| H8 gate≤0.45+known<5 | combo | — | — | — | — | — | Subsumed by H17 |

## Validated negatives — DON'T retest
- interval-prediction (2-9% live precision)
- fair-price scalping (0/5 weeks profitable)
- listing momentum (32% win)
- microcaps expansion (DEGRADES 86%)
- known<5 + smart 3-5 standalone (R8 regime artifact)
- single-feature filter alone (R10)
- H11 lottery cluster smart≥7+known≥15+both≥4 (R11: train rug 79%)
- **H12 both≥5 standalone (R12 NEW)** — rug 80% train / 69-90% test
- R9 SMART_COPY inversion — RECLASSIFIED as regime-dependent
- H15 both=0 standalone (rug lift but absolute -46% test)

## Next cycle priorities
1. **Re-measure regime** post-reversion baseline (~ -55/-60% rug expected stable)
2. **Accumulate H17 hits** — need ~30 more unique tokens to validate (currently 7 total)
3. **Compare H17 entries across non-A/B streams** (D, E, G, F, SMART_COPY variants) — does any non-B stream have equivalent early_exit_ratio_99-style logic?
4. **Re-test regime gate ≤0.25** as test split grows — confirm threshold shift
5. If permission: propose `SNIPER_PURE_BOTH_B_EXIT` paper stream

## Open questions for user (blockers)
1. **Permission to propose paper stream `SNIPER_PURE_BOTH_B_EXIT`** (H17 filter + B's `early_exit_ratio_99` exit, size=$1, paper)? Strongest archetype found.
2. **KPI revision**: H17 has 0% rug + 17% 3x rate (asymmetric profile). KPI `avg≥+150%` misses Kelly-friendly profiles. Suggest **n_dedup≥30 AND (rug≤30% OR 3x_rate≥10%) AND EV≥+50% per trade w/ B-exit**.
3. **Per-wallet metadata in entry_signal**? Need to see which wallets count as `both` (vs smart vs known) to distinguish stable-cluster (H17) from churning-cluster (rug).
4. **Source visibility for `early_exit_ratio_99` exit logic**? If exit is the alpha, understanding it lets me clone into paper variants.
5. **PROJECT_CONTEXT.md still describes funding-rate arb** but work is on-chain memes. Update or pivot officially.

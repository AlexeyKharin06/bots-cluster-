# BRIEF — funding-rate snapshot (last update: 2026-05-21 05:00 UTC)

## State
- Data: `/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json` (38MB, ms-epoch int timestamps now — NOT ISO)
- 4993 closed_trades (+116 new), 0 open, cycle=30404
- 20+ paper streams active. NONE production-promoted, NO real money.

## Regime — IMPROVED (second clean pocket; 6-12h cycle confirmed)
- **last 100: avg -27.7%, WR 33%, rug 27%** (was -63%/66% prev cycle — +36pp lift)
- 0-2h: -23.4%/21% rug (cleanest sub-window)
- 3-day arc: -35% → -52% → +pos → -63% → **-27.7% (current)**
- **CAVEAT**: last 200 has 0% 3x rate. Clean window without lottery events.

## 🔴 NEW CRITICAL: Wallet-tagger DRIFT detected
- New window (n=121): smart avg 4.12 (was 7.33), known avg 12.79 (was 17.30), `both≥5` 1.7% (was 13.4%), `known≤1` 0.0% (was 0.3%), `top1=0` 14% (was 10%)
- ALL counts trending DOWN 40-50%. Listener / wallet-pool seems to have changed.
- **H17 fires ZERO in 121 new trades** — signal stopped existing, not low frequency
- ANY hypothesis using extreme tagger values (smart=0, known≤1, both≥10) is now FRAGILE
- Mid-range filters (H20) are robust to drift

## NEW: H20 mid-cluster trail-capture archetype
- Sig: **smart 1-7 ∧ known 8-15 ∧ both 0-2 ∧ top1 70-90 ∧ mcap $50-200k ∧ age 15-30**
- Test: n=31 raw / 4 unique — avg **+50.9 / +59.8 dedup**, WR **87%**, rug **0%**, 2x 16%
- New-window hits: ISIS +113, 芭比Q了 +104, ZEST +70 (H17 = 0 hits)
- Best stream: SNIPER_MC_LIQ (n=5 avg +50.3% WR 80% rug 0%)
- Exit: all `trail` — caps 50-150% pumps, MISSES 1000%+ tail
- See `insights/cycle_20260521_0500.md`

## STRONGEST validated edge: REGIME GATE ≤0.25
- Walk-fwd test n=235 avg **-11.7%** (baseline -40.2%) = **+28.5pp lift**, rug 31% (-11pp)
- Holds across larger sample (was n=112 prev cycle)
- Use as base layer for any paper-stream proposal
- Best as filter, not standalone (still negative absolute avg)

## Hypothesis frontier
| H | Filter | n_test | n_unique | avg | rug | 3x | Verdict |
|---|--------|--------|----------|-----|-----|----|---------|
| Regime gate ≤0.25 | rolling-100 rug ≤25% | 235 | 36 | -11.7% raw / -35.7 dedup | 31% | 3.0% | **+28.5pp lift, validated** |
| **H20 MID-CLUSTER** | mid smart+known + top1 70-90 + mid-cap | 31 raw | 4 | **+50.9 / +59.8 dedup** | 0% | 0% | **NEW promising_needs_n** |
| H17 PURE_BOTH | smart=0 ∧ known≤1 ∧ both≥5 + tight | 0 new | 6 hist | n/a — fires zero | n/a | n/a | **blocked_on_tagger** |
| H18 B-exit `early_exit_ratio_99` | exit-side | 16 pairs | — | +344pp vs A | — | — | high_priority (needs source) |

## Validated negatives — DON'T retest
- interval-prediction (2-9% live precision); fair-price scalping (0/5wk); listing momentum (32% WR); microcaps expansion (-86%); known<5+smart 3-5 standalone (R8 regime artifact); single-feature filter alone (R10); H11 lottery cluster (R11 rug 79%); H12 both≥5 standalone (R12 rug 80%); H15 both=0 standalone (test -46%)
- R9 SMART_COPY inversion — RECLASSIFIED regime-dependent (pair w/ gate)

## Next cycle priorities
1. **Investigate wallet-tagger drift** (need read permission) OR add drift monitor metric
2. **Accumulate H20 hits** — target n_unique≥20 to confirm
3. **H22**: H20 + regime gate ≤0.25 joint filter
4. **Audit SNIPER_MC_LIQ** stream (best fit for H20)
5. **Cross-stream B-exit test on H20** — does early_exit_ratio_99 beat trail?
6. Re-check gate ≤0.25 as test split grows

## Open questions for user (BLOCKERS)
1. Wallet-tagger pool refresh cadence? Permission to read tg_listener / wallet_v2?
2. H17: abandon until tagger stabilizes, or keep monitoring? (marked `blocked_on_tagger`)
3. Propose H20 paper stream `SNIPER_MID_CLUSTER_TRAIL` if n_unique≥20 (rug ≤15%)?
4. KPI: Sharpe-promotion tier (H20-style steady) vs Kelly-promotion (H17 lottery)?
5. PROJECT_CONTEXT.md still says funding-rate arb — pivot officially (4th cycle noting)?

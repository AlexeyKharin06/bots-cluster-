# BRIEF — funding-rate snapshot (last update: 2026-05-20 17:00 UTC)

## State
- Data source: `/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json`
- 4978 closed_trades (+93 since last cycle), 32 open positions, cycle=30192
- 20+ paper streams active. NONE production-promoted, NO real money.

## Regime — REGIME FLIPPING (live signal)
- **last 100 trades: avg +4.75%, WR 32%, rug 28%** — first positive 100-window since project start
- last 0–2h slice: avg -8% rug 24% pct_3x 4.2% (cleanest 2h in 3 days)
- last 0–24h: avg -52% rug 56% — still hostile macro
- Interpretation: regime broke briefly in last 2h; may revert. Monitor.
- 3-day arc: -35%→-52%→-52%→pos-pocket. Cycle bottoming?

## Hypothesis frontier (best signals so far)
| H | Filter | n_test | n_dedup | avg | rug | pct_3x | Verdict |
|---|--------|--------|---------|-----|-----|--------|---------|
| Regime gate ≤0.35 | trail100-rug ≤0.35 | 112 | n/a | +7.3% | 30% | 5.4% | **Strongest standalone**, +48pp lift walk-fwd |
| H8 gate≤0.45 + known<5 | combo | 46 | 7 | +18.9% | 0% | 14% | Best deduped avg, sample too small |
| SMART_COPY family | stream-level | 12-15 | ~10 unique | +18 to +23% | 27-33% | 6.7-8.3% | Flipped from -48% in prior regime |
| H10 liq<30 + age≥15 | combo | 104 | n/a | -24% | 47% | 4.8% | Filter lift but rug WORSENED |
| H11 lottery cluster | smart≥7+known≥15+both≥4 | 0 | n/a | (train -36/rug 79) | – | – | **REJECTED** |

## Last cycle (2026-05-20 17:00)
- Regime improvement validated; first positive last-100 window
- H11 REJECTED (train rug 79%, conclusive)
- H8 (regime gate + known<5) — first profitable hypothesis but sample too small (n_dedupe=7)
- SMART_COPY family flipped POSITIVE in last 3h — directly contradicts last cycle's R9 inversion claim (regime-specific)
- Dedupe methodology added: 268 raw trades = only 38 unique tokens; always dedupe before measuring n
- See `insights/cycle_20260520_1700.md`

## Validated negatives — DON'T retest
- interval-prediction (2-9% live precision)
- fair-price scalping (0/5 weeks profitable)
- listing momentum (32% win)
- microcaps expansion (DEGRADES 86%)
- known<5 + smart 3-5 standalone (R8 regime artifact)
- single-feature filter alone (R10)
- H11 lottery cluster smart≥7+known≥15+both≥4 (R11 NEW: train rug 79% n=393)
- R9 SMART_COPY inversion claim — RECLASSIFIED as regime-dependent (NOT a real inversion)

## Next cycle priorities
1. **Re-measure regime** — did the +pos pocket hold or revert?
2. **Watch H8 sample grow** — need n_dedupe ≥ 50 before promotion
3. **H12 forensic: `both` count signal** — COMPUTE archetype (both=10, +288%). Test if `both ≥ 5` predicts pumps generally.
4. **Cross-stream attribution** — same 38 tokens hit by 7 streams each: which stream's EXIT logic captures most of the upside?
5. If permission: draft `SNIPER_SMART_COPY_GATED` paper stream (SMART_COPY + regime gate ≤0.35)

## Open questions for user (blockers)
1. **KPI realism**: `n≥50, avg ≥+150%, WR ≥60%, rug ≤25%` is unreachable for memes (top WR ~30%, EV from 5x outliers). Suggest revise to `n_dedupe ≥50, EV ≥+10%, rug ≤30%`.
2. **Permission to patch regime gate** into shared serial_sniper? Strongest validated edge.
3. **Permission to propose new paper stream `SNIPER_SMART_COPY_GATED`** (no change to controls)?
4. Can entry_signal expose per-wallet metadata (age, prior PnL) for finer attribution?
5. PROJECT_CONTEXT.md still describes funding-rate arb but actual work is on-chain memes. Update or pivot officially?

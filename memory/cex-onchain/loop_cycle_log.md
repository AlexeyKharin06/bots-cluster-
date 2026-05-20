---
name: Loop cycle log
description: Timeline of /loop 6h autonomous research cycles — what was tested, deployed, deferred
type: project
originSessionId: 4ecee032-64c4-479e-91de-d2a9303de3ec
---
# Loop cycle log (CEX-Onchain autonomous research)

Cron: 0d7a12d3, every 6h at :07, session-only.

## Cycle 1 — 2026-05-18 21:39 UTC
- **Hypothesis**: Triple AND combos (3-feature)
- **Tested**: 36 variants over 4 anchor 2-ANDs
- **Found**: 8 strict-validated combos
- **DEPLOYED**: Slot U @ 4% capital
  - Conditions: max_dep_24h≥30 AND n_addr_vs_baseline_24h≥3 AND pos_7d_pct≤50
  - Expected edge: WF 5/5 windows, avg test +29.47%
- **Code changes**: added `max_chg_24h_pct` + `max_pos_7d_pct` to SlotConfig
- **Total allocation**: 100% across 9 slots (C/B/U/A/T/A2/K/S/M)
- **Bot restart**: yes

## Cycle 2 — 2026-05-19 04:10 UTC
- **Live trigger**: TRAC -$67.77 stop_loss (chg_24h=+37%, pos_7d=100% — pumping token bypassed slot A)
- **Hypothesis tested**: max_chg_24h_pct filter for slot A
- **Sweep**: none/100/70/50/30/10/0 — all pass WF 5/5
- **Winner**: chg_24h ≤ 0% → WF avg test +27.15% (vs +18.24% baseline)
- **DEPLOYED**: slot A gains max_chg_24h_pct=0.0 (would have prevented TRAC loss)
- **Bot restart**: needed for live effect
- **Next**: validate same filter on T/A2/K in cycle 3, look for stuck positions, OR combos

## Cycle 3 — 2026-05-19 20:37 UTC
- **Hypothesis**: extend chg_24h ≤ 0 filter to A2/T/K/M
- **Results**: A2 +6.77pp, T +6.32pp, M +7.01pp — all WF 5/5. K +0.84pp (no benefit)
- **DEPLOYED**: A2, T, M all get max_chg_24h_pct=0.0
- **Pattern confirmed**: chg_24h≤0 helps slots with deposit-magnitude triggers, NOT cluster-only (K)
- **Stuck positions**: none (all <60h)
- **Slot stats now**: A +27%, A2 +25%, T +31%, M +27% expected mean per trade
- **Next**: OR combo search, per-token live PnL audit, slot S also needs chg_24h?

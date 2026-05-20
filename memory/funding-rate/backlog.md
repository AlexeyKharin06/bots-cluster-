# Backlog — hypotheses to test

## Status legend
- testing — currently active in paper
- accepted — promoted to live consideration
- rejected — backtested negative, do not retest
- pending — defined but not started
- needs_more_data — promising but sample too small for walk-fwd

## Hypotheses

H1 whale-copy paper bot copies @on_chain_radar signals | pending | source: 5/18 high-PnL claims
H2 confluence SHORT-only expand n=5 → n=30+ | pending | n=5 showed 80% win
H3 stablecoin depeg arb (USDD-style) | pending | source: Lopata +$2300 USDD case
H4 CEX→DEX algo flow tracking | pending | source: Lopata "dex-dex" class, needs DEX indexer
H5 announcement watcher (Bybit interval changes) | pending | 95% precision potential
H6 new symbol detection (poll APIs 30s) | pending | catch listings before public

H7 regime gate: pause trading when rolling-24h rug% > 55% | pending 2026-05-20 | rationale: regime shift dominates filter edge — see cycle_20260520_1343
H8 regime gate + known<5 combo | pending 2026-05-20 | known<5 lifts +10pp persistent walk-fwd, combine with regime gate to skip hostile windows
H9 forensic on ride_exit_X% exits (200-1158% pnl) | pending 2026-05-20 | identify which entry-signal combos produced the rare big winners (PIGEON, MTFR, ROAF profile)
H10 liq_mcap_ratio < 30 + age >= 15 filter w/ regime gate | pending 2026-05-20 | strongest combined rug avoidance (rug 19% in-sample n=101)
H11 asymmetric Kelly for lottery archetype | pending 2026-05-20 | tiny size (fixed bankroll %) on heavy-cluster signal (smart 7+, known 17+, both 6+) — 60% rug but occasional 30x; current bot loses to this with full size

H_AGE_GE30 age >= 30 min entry timing | needs_more_data 2026-05-20 | train n=71 avgPnL -6%, rug 15% — promising BUT test n=5 all rugged. Need wait for more 30+ samples (current bot mostly buys <30m so naturally rare)

## Rejected

R1 interval prediction premium-streak alone | rejected 2026-05-18 | 2-9% live precision, 0/7 paper wins
R2 fair-price scalping any threshold | rejected 2026-05-18 | 0/5 weeks profitable walk-forward
R3 listing momentum mechanical | rejected 2026-05-18 | 32% win -$11/90d historical
R4 expansion to RAVE/SIREN/PIPPIN tickers | rejected 2026-05-18 | DEGRADES baseline 86%
R5 multi-ex spread arb naive | rejected | -$13473 / 30902 trades
R6 naive funding harvest >2% threshold | rejected | -$304/315 trades
R7 multi-signal confluence LONG-side | rejected 2026-05-18 | 27% win
R8 known<5 + smart 3-5 as profitability gate | rejected 2026-05-20 | train rug 2% / test rug 32% — regime artifact, not real edge; absolute test PnL -47%
R9 SNIPER_SMART_COPY/TOP family streams | observation 2026-05-20 | these stream filters select for HIGH smart-wallet count (≥7) which inverts to higher rug rate; NOT formally rejected as stream config — flagged for review
R10 any single-feature filter as profitability gate | rejected 2026-05-20 | no univariate filter reaches positive abs PnL in walk-forward; filters only reduce loss vs baseline by 9-23pp; need regime gate + multi-feature

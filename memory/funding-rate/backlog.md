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
H11 asymmetric Kelly for lottery archetype | REJECTED 2026-05-20_1700 | smart>=7+known>=15+both>=4: train n=393 rug 79%! pct_3x only 1%; even tiny Kelly can't fix this — see cycle_20260520_1700.md / R11

H12 `both` count signal (both>=5) | REJECTED 2026-05-20_2300 | bucket-test: both=5_6 n=309 avg -72% rug 82%; both=10+ n=148 avg -50% rug 79% (lottery, 6.8% 3x). Walk-fwd: train n=401 rug 80%, test n=177 rug 69% even with regime gate (rug 90% gated!). The undifferentiated cluster is a rug signal. See R12 + insights/cycle_20260520_2300.md

H13 SMART_COPY_GATED paper stream | pending 2026-05-20_1700 | SMART_COPY family flipped +18-23% in clean regime, -48% in hostile. Pair with regime gate ≤0.35 — joint walk-fwd. Requires permission to add new paper stream.

H14 cross-stream exit attribution | pending 2026-05-20_1700 | 38 unique tokens this cycle hit by 7 streams each; same entry, different exit trails. Which exit (A vs B vs SMART_TOP_AGE5) captures most upside? Stream selection is half — exit is the other half.

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
R11 lottery cluster asymmetric Kelly | rejected 2026-05-20_1700 | smart>=7+known>=15+both>=4 train n=393 rug 79%, pct_3x 1% — math doesn't survive even with 1% bet sizing
R9 RECLASSIFIED 2026-05-20_1700 | SMART_COPY inversion claim was REGIME-SPECIFIC; family flipped to +18-23% avg in clean regime. NOT a structural inversion. Don't avoid these streams; they may be the best when regime allows.

H7 regime gate ≤0.35 | TESTING 2026-05-20_1700 | walk-fwd train -41% / test +7.3% (n=112) — +48pp persistent lift, strongest validated edge. Trade only when trail100 rug ≤0.35. Need permission to patch into bot OR new gated paper stream.
H8 UPDATED 2026-05-20_1700 | test n=46 raw / n=7 dedup avg +18.9% rug 0% pct_3x 14% — first profitable hypothesis but sample tiny. Track until n_dedup ≥50.

R12 H12 `both>=5` standalone | rejected 2026-05-20_2300 | both=5_6 rug 82%, both=10+ rug 79%; regime gate makes it WORSE (test rug 90% gated vs 69% ungated — clean-regime windows produce more cluster-rugs). Undifferentiated overlap is a rug signal in aggregate.

H17 PURE_BOTH archetype | promising_high_priority 2026-05-20_2300 | smart=0 ∧ known<=1 ∧ both>=5 ∧ top1=0 ∧ liq_mc>=50 ∧ mcap<=25k ∧ age<=15min. Test (13h, last 30% split): 6 unique tokens (BEAN, MC, COMPUTE, https, CATCOIN, WORLDCUP), 0% rug, 17% 3x rate. Top winners MC +1268%, WORLDCUP +971%, CATCOIN +542%, COMPUTE +856% (all SNIPER_B). PORTUGAL +906% in train. n too small (train=1 unique, test=6 unique). NEED 30+ unique to confirm. NOT a subset of REJECTED H12 — the key constraint is smart=0 AND known<=1 (i.e. ALL wallet activity is in `both` overlap, not distributed). Different classifier-quirk pattern. See cycle_20260520_2300.md.

H18 EXIT-LOGIC alpha `early_exit_ratio_99` | high_priority 2026-05-20_2300 | SNIPER_B uses early_exit_ratio_99 exit which dominates SNIPER_A on same entries by +344pp avg (16 cases). Mechanism: (a) rug-avoidance — exits +10-30% on tokens A holds to rug_no_data -100%, (b) big-winner capture — catches multi-1000% peaks A's sl/ride_exit can't. Likely THE alpha. Need source visibility for the exit logic. Cross-stream attribution next: does D/E/G/F have similar exit, or is it B-unique?

H19 cross-stream B-exit replication | pending 2026-05-20_2300 | if early_exit_ratio_99 is B-unique, all other streams have inferior exit. Audit each stream's exit_reason distribution on the H17 archetype subset. Promote streams with similar exit-side alpha for paired testing.

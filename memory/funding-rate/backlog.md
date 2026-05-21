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

H17 UPDATED 2026-05-21_0500 → **blocked_on_tagger** | ZERO new H17 hits in 121-trade new window (4877+). Wallet-tagger distribution drifted: `both≥5` 13.4%→1.7%, `known≤1` 0.3%→0.0%, `top1=0` 7.6%→14%, smart avg 7.33→4.12. Entry signature stopped firing — not a low-frequency event, signal stopped existing. DO NOT promote until tagger stability confirmed. Keep filter definition alive; re-test when tagger reverts. See cycle_20260521_0500.md.

H18 EXIT-LOGIC alpha `early_exit_ratio_99` | high_priority 2026-05-20_2300 | SNIPER_B uses early_exit_ratio_99 exit which dominates SNIPER_A on same entries by +344pp avg (16 cases). Mechanism: (a) rug-avoidance — exits +10-30% on tokens A holds to rug_no_data -100%, (b) big-winner capture — catches multi-1000% peaks A's sl/ride_exit can't. Likely THE alpha. Need source visibility for the exit logic. Cross-stream attribution next: does D/E/G/F have similar exit, or is it B-unique?

H19 cross-stream B-exit replication | pending 2026-05-20_2300 | if early_exit_ratio_99 is B-unique, all other streams have inferior exit. Audit each stream's exit_reason distribution on the H17 archetype subset. Promote streams with similar exit-side alpha for paired testing.

H20 MID-CLUSTER trail-capture archetype | promising_needs_accumulation 2026-05-21_0500 | smart∈[1,7] ∧ known∈[8,15] ∧ both∈[0,2] ∧ top1∈[70,90] ∧ mcap∈[$50k,$200k] ∧ age∈[15,30]min. Walk-fwd all-time: n=64 raw / 8 unique avg +24.8%/+29.1% WR 67% rug 12% 2x 22% 3x 0%. Test split (last 30%): n=31 raw / 4 unique (ISIS+113, BB+104, ZEST+70, +1) avg +50.9%/+59.8% WR 87% rug 0% 2x 16%. Train n=33 raw / 4 unique avg +0.3% (mediocre — clean test pocket helping). Best stream-fit: SNIPER_MC_LIQ (n=5 avg +50.3% WR 80% rug 0%). All exits via `trail` — caps at 50-150% pumps, MISSES 1000%+ tail (i.e. NOT a +100k% mission alpha alone). Complementary to H17 (steady Sharpe vs lottery). Robust to wallet-tagger drift because uses mid-range counts. Need n_unique≥20 to confirm. See cycle_20260521_0500.md.

H21 wallet-tagger stability monitor | pending 2026-05-21_0500 | observed: wallet-tagger field distributions shifted 40-50% between prev-window (idx 3500-4877) and new-window (4877+). smart avg 7.33→4.12, known avg 17.30→12.79, `both≥5` 13.4%→1.7%, `known≤1` 0.3%→0.0%, `top1=0` 7.6%→14%. Cause unknown — possibly listener wallet-pool refresh, RPC dropouts (das_skipped), or genuine market decentralization shift. Hypotheses built on extreme tagger values (smart=0, known≤1, both≥10) are FRAGILE. Mid-range filters (H20) survive. Next cycle: add tagger-distribution snapshot to BRIEF; need permission to read tg_listener/wallet_v2 internals to diagnose root cause.

H22 H20 + regime gate ≤0.25 joint filter | pending 2026-05-21_0500 | predict: gate cuts H20's train-window noise (avg +0.3% n=33), preserving the test-window winners. Risk: shrinks already-small unique-token count. Test once H20 hits accumulate further.

H23 SNIPER_MC_LIQ stream audit | pending 2026-05-21_0500 | this stream had best fit on H20 winners (n=5 avg +50.3% WR 80% rug 0%). What's its entry filter? If similar to H20 conditions, may be the natural production stream to propose for H20-style alpha (no new stream needed).

GATE-≤0.25 walk-fwd reconfirmed 2026-05-21_0500 | test n=235 (was 112 prev cycle) avg -11.7% vs baseline -40.2% = +28.5pp lift; rug 31% vs 42% = -11pp lift. Strongest validated edge. Should be base layer for any paper-stream proposal. ≤0.20 also competitive (n=163 avg -14.4%). Tighter threshold optimal in current regime mix.

GATE-≤0.20 walk-fwd POSITIVE-abs 2026-05-21_1100 | test n=271 (anchored cut 2026-05-20 15:35Z) avg **+6.5%** WR 44 rug 22 3x 5.0 (baseline test n=2169 avg -33.7 rug 39 3x 1.0) = +40pp lift, FIRST POSITIVE absolute test avg. ≤0.25 also positive: n=351 avg +1.5% rug 28. Gate optimum tightened from ≤0.25 last cycle to ≤0.20 this cycle (regime mildly more hostile + better tail coverage at tighter threshold). Current live gate 0.37 — would PAUSE trading right now. See cycle_20260521_1100.md.

H17 UPDATED 2026-05-21_1100 → **DEPRECATED** | known≤1 clause was a confound, not a feature. Same big winners (MC, WORLDCUP, CATCOIN, COMPUTE, https, BEAN, PORTUGAL) all reappear in H25 (relaxed) + 22-23 more unique lottery candidates. Tagger PARTIALLY RECOVERED in newest 165 trades (smart 4.12→6.84, known 12.79→21.18) — drift was transient pocket, not permanent. BUT top1=0 halved (10.4→4.8%) so H17 strict still fires ZERO in newest data — structurally rare now. Switch to H25 going forward; keep H17 filter definition referenced as historical case.

H24 rugcheck_score ∈ [100,1000] | promising_needs_validation_of_score_semantics 2026-05-21_1100 | bucket-test all-data: score=0 n=613 rug 59%; **score 100-1k n=242 / 32 unique avg -22% rug 13%**; score 5k-15k n=1848 rug 51%; score 15k-30k n=819 rug 57%; score ≥30k n=1292 rug 40%. Walk-fwd (anchored cut): train n=134/17u rug 24, test n=108/15u rug **0%** avg -5.8% dedup. H24 + gate ≤0.20: test n=21/3u avg **+7.3%** WR 71 rug 0. Sharpe-friendly (0% 3x — no lottery), strong rug-avoidance. CAVEAT: score=500 dominates the 100-1k bucket (13/15 unique) — could be sentinel or real risk-tier. NEED rugcheck pipeline docs to validate. Use as BASE LAYER. See cycle_20260521_1100.md.

H25 = H17 RELAXED (drop known≤1) | **promising_high_priority — near-promotable** 2026-05-21_1100 | smart=0 ∧ top1=0 ∧ both≥5 (any known). Walk-fwd (anchored cut 2026-05-20 15:35Z): TRAIN n=42/14u avg +17.6%/+127% dedup rug 31 2x 14 3x 14; **TEST n=75/29u avg +4.3%/+28.2% dedup WR 45 rug 45 2x 14 3x 10.3**. Stream attribution (test): SNIPER_B +28.2% vs SNIPER_A -62% on SAME entries (+90pp gap) — confirms H18 B-exit alpha REPLICATES across archetypes. SNIPER_F/F2/D/D2 each n=3 avg +136% WR 100 rug 0 — possibly even better exit than B. Unique winners include MC+1268, WORLDCUP+971, CATCOIN+542, COMPUTE+856, CMC+288, 币安队长+105, plus losers like NBRDG/NMIND/OPULSX (rugs). With B-exit only, rug 45→~30% realistic (B exits rugs at +10-30%). Mission-aligned (lottery profile, 10.3% 3x). PROPOSE paper stream `SNIPER_PURE_BOTH_RELAXED_B_EXIT` if user permits. See cycle_20260521_1100.md.

H26 H25 + gate ≤0.20 joint | needs_more_data 2026-05-21_1100 | test n=8 raw / 4 unique avg +128/+328 dedup, 50% rug 50% 2x 50% 3x. Extreme lottery profile but n=4 unique too small for paper stream. Re-test as data grows.

H27 SNIPER_D/F-family exit forensic | high_priority 2026-05-21_1100 | on H25 test entries, SNIPER_F/F2/D/D2 each n=3 avg +136% WR 100% rug 0% (vs B +28%, A -62%). Suggests these streams may have an exit logic that OUTPERFORMS B's `early_exit_ratio_99` on lottery archetype. SNIPER_D/D2 also +20.9% avg in last 500 trades. Need source visibility for exit configs to validate and replicate.

H28 H25 + rugcheck filter joint | pending 2026-05-21_1100 | predict: H25 + rugcheck_dangers ≤1 + bsr_m5 ∈[0.5,2] (organic flow) reduces H25's 45% rug while preserving 3x captures. Test next cycle once H25 sample grows or rugcheck semantics confirmed.

FEATURE OBSERVATIONS 2026-05-21_1100:
- `buy_sell_ratio_m5` ≥10: n=258 avg -75% **rug 89%** — coordinated pump-and-dump signal. INVERSE FILTER: avoid bsr≥5 always.
- `rugcheck_dangers`=2: n=153 avg -80% rug 71% WR 0% — HORRIFIC. Always veto. dangers=0 alone is NOT meaningfully better than =1 (46% vs 48% rug); the signal lives in score combo (H24).
- Stream `SNIPER_VOL_VEL` (n=17 last 500): rug 12% — cleanest in dataset. Audit filter.
- Stream `SNIPER_ULTRA_TRIPLE` (n=11): rug 18% — new clean stream, three-feature confluence (likely).
- Stream `SNIPER_MC_LIQ` audited: name misleading, only 35% of trades in $50-200k mcap range, mcap p90 = $250M. NOT a natural H20 stream.
- State.json sliding window: ~2.5-day trim observed twice now. Use timestamp-anchored cuts not index-anchored.

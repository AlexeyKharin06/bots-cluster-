# BRIEF — funding-rate snapshot (last update: 2026-05-20 13:43 UTC)

## State
- VPS deployment live; data source for on-chain analysis = `/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json`
- 4885 closed_trades, 39 open positions, cycle=30132 in the onchain wallet sniper
- Streams: 20+ paper streams active (SNIPER_A/B/D/H/SMART_COPY/GOLD/WHALE/LATE/LOWCAP/MC_LIQ/VOL_VEL/ULTRA_TRIPLE/etc). ALL avg negative PnL. Best: SNIPER_WHALE (-18.6%, n=23). Mainstream: -45 to -55%.
- Current regime is HOSTILE: last 24h rug rate 58% vs prior 24h 48% (+10pp degradation).
- No production stream promoted. No real money trading.

## Last cycle (2026-05-20 13:43)
- Walk-forward backtest on 4 hypotheses (H_KNOWN_LT5, H_AGE_GE30, H_LIQ_10_30, H_SAFE combo)
- ALL hypotheses DEGRADED out of sample due to regime shift
- Best persistent lift: H_KNOWN_LT5 = +10pp avgPnL above baseline both in train and test (but still absolute -49% in test)
- See `insights/cycle_20260520_1343.md` for full details
- New rejections: R8 (known<5+smart3-5 was regime artifact), R10 (no univariate filter reaches profitability)
- New hypotheses added: H7-H10 (see backlog.md)

## Validated negatives — DON'T retest
- interval-prediction (2-9% live precision)
- fair-price scalping (0/5 weeks profitable)
- listing momentum (32% win)
- microcaps expansion (DEGRADES 86%)
- safe wallet-cluster filter standalone (R8 — regime artifact)
- any single-feature filter for profitability (R10 — at best -23% absolute)

## Next cycle priorities
1. Implement & test REGIME GATE (pause trading when rolling-24h rug% > threshold)
2. Walk-forward H7 (regime gate + known<5) and H10 (regime gate + liq_mcap<30)
3. Forensic on ride_exit_X% exits — what feature combos produce them?
4. Need more data for H_AGE_GE30 (test n=5 too small)

## Open questions for user
- Permission to propose a regime-gate patch to shared serial_sniper / wallet_v2 code? (Currently I treat all control streams as untouchable.)
- Can the entry_signal log include per-wallet metadata (wallet age, prior PnL) so we can attribute? Currently only have counts.
- For lottery-archetype (cluster pattern, 60% rug, occasional 30x) — should I propose asymmetric Kelly (tiny size, fixed % of bankroll) as a separate stream?

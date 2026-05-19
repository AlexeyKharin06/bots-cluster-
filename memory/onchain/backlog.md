# Backlog — open hypotheses & rejected paths

> Append new hypotheses below. Update status (NEW / TESTING / VALIDATED / DEPLOYED / REJECTED) inline. Don't delete REJECTED — keep for negative learnings.

## NEW (proposed cycle 20260519_1639)

### H_LP_WHITELIST — primary
**Idea**: Maintain rolling whitelist of `lp_provider` wallets with prior trailing-window n≥3, avgPnL≥+30%, rug≤33%. Enter only if `entry_signal.lp_provider ∈ whitelist`.
**Evidence**: walk-forward TRAIN→TEST: n=35, avg=-7.5%, WR=40%, **rug=25.7%, big=14.3%, huge=0%** vs baseline (n=1861) avg=-46.9%, rug=43%, big=1.5%. Δavg=+39pt, Δrug=-17pt, Δbig=+12.8pt.
**Why it works**: LP providers are repeated actors; "incubators" with successful prior pumps tend to repeat. Per-token pool_creator does NOT persist; LP provider does.
**Why not deployed**: avgPnL on TEST (-7.5%) fails the +150% gate. Fat-tail upside (14% big winners) is real but suppressed by current exit/trail logic. Needs adaptive TP+ride for the LP-whitelisted cohort.
**Next**: Re-run after +12-24h of data; whitelist size will stabilize. Also write paper-stream spec with custom exit logic for this cohort.
**Status**: NEW, awaiting more data.

### H_QUIET_EMERGENCE
**Idea**: Catch early-stage emerging tokens before the herd arrives. Filter: `liquidity_at_entry < 17K` AND `buys_m5 < 150` AND `volume_h24 < 60K` AND `top1_pct < 20`.
**Evidence**: Full-data (no walk-forward) `liq<17K & buys<150 & pumped_alive≥1`: n=293, avg=+77.4%, WR=37.5%, rug=12.6%, big=15%. Walk-forward heavily degrades on TEST (n=13-52 hits, avg ≈ -5 to -47%) — fat tail not captured by 1.5-day TEST window.
**Why it might fail**: counter-intuitive ("low buys = good") could be reverse-causation — quiet tokens that *eventually* pumped are over-represented because we got cheap entries on them.
**Next**: combine with H_LP_WHITELIST; re-test with bigger TEST window.
**Status**: NEW, waiting on more data.

### H_DISTRIBUTED_HOLDERS
**Idea**: Reject high concentration: `top1_pct ≥ 20` OR `top5_pct ≥ 60`. Standalone weak (avg=-9.7% q1 vs -38.5% baseline) but cleanly combines with other filters.
**Evidence**: top1_pct q1 (<16.6): n=930, avg=-9.7%, rug=24.5%, big=3.5%. top5_pct q1 (<29.4): avg=-9.4%, big=3.5%. q3 (mid-concentration): rug 62-65% — the danger zone.
**Why not standalone**: q1 alone is 20% of trades. Too broad for paper stream.
**Next**: integrate as veto-filter on top of H_LP_WHITELIST.
**Status**: NEW (composable filter, not standalone candidate).

## REJECTED (cycle 20260519_1639) — keep for memory

### H_REJECT_RIDE_MODE
**Reason**: `ride_mode=true` cohort (n=157, avg=+135%, big=14.6%, huge=7%) is **post-entry**. The flag is set by the trail-upgrade logic when a trade pumps past threshold mid-flight. `ride_mode=false` doesn't exist in data (only `true` or `undefined`). Cannot be used as entry filter — pure look-ahead bias.

### H_REJECT_1AR_TOP1OWNER
**Reason**: top1_owner `1AR1WDTonbumSi2Zd9YHBxUQcX7PUnBRvsJBQ4g5iv6` showed n=167, avg=+92% in aggregate — looked like an alpha wallet. Day-by-day breakdown revealed the entire +92% comes from ONE day (2026-05-15, n=11, avg=+2098%). Every other day was negative. Likely a router/utility wallet that's incidentally top-1 holder of many tokens. **Lesson: always check time-localization before claiming wallet alpha.**

### H_REJECT_LP_BLACKLIST
**Reason**: TRAIN-derived LP blacklist (171 wallets with n≥3, rug≥90%) only matched 32 of 1861 TEST trades (1.7% coverage). Per-stream impact on rug rate: 0.1-0.5%, noise-level. The bad LPs don't repeat enough to be reliable as a negative filter on this timescale. Reconsider if dataset grows to 30+ days.

## Pending investigations (not full hypotheses yet)

- **SNIPER_G mystery**: n=123, avg=-14.6%, rug=19.5% — best risk-adjusted of all baseline streams. What does G filter that A/B/H don't? Need to read sniper code to understand. Source on D:\OnChain\.
- **rugcheck_score q5 (≥27K) = safer**: counter-intuitive (high score should = more dangerous). Possibly mislabeled axis or special token class. Investigate.
- **`bonding_curve_buyers` field**: empty in our sample. If populated downstream, would enable insider-bundle detection — pre-bonding-curve buyers who consistently win = clear smart-money signal.
- **Meteora vs Pumpswap dex divergence**: Meteora avg=-35.6%, Pumpswap avg=-43.3%. Worth a per-dex hypothesis split.

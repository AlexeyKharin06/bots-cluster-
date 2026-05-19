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

## NEW (proposed cycle 20260519_1702)

### H_CR_HIST_NEG — composable veto filter
**Idea**: Reject entries where `entry_signal.cr_hist.pumped_alive ≥ 1`. The cr_hist field is the time-correct snapshot of creator-wallet history at entry (no leakage).
**Evidence (walk-forward)**:
- TRAIN: n=132, avg=-49.8%, WR=21.2%, rug=42.4%, big=0%
- VAL: n=66, avg=-59.7%, WR=0%, rug=47%
- TEST: n=86, avg=-71.2%, **WR=0%**, rug=66.3%
**Interpretation**: pool_creator and lp_provider are different roles. lp_hist.pumped_alive (LP) is POSITIVE — captures repeat liquidity providers that back real launches. cr_hist.pumped_alive (mint creator) is NEGATIVE — captures serial pump-scammer creators whose next launch repeats the pump-then-rug pattern.
**Coverage**: only 6% of trades (284/4652) have cr_hist.pumped_alive>0, so as a sole filter the impact is small (baseline -49.9% → -47.7% after removing 86 trades from 931 in TEST). But as a veto on top of other positive filters (H_LP_WHITELIST, H_QUIET_EMERGENCE), it should improve quality.
**Why it's safe vs. H_RUG_PC**: cr_hist is a snapshot frozen at entry_time — it cannot encode future outcomes. Decontamination test not needed (per-trade time-correctness is structural).
**Next**: compose with H_LP_WHITELIST in next cycle; re-test when data is fresh.
**Status**: NEW.

## REJECTED (cycle 20260519_1702) — keep for memory

### H_REJECT_RUG_PC — pool_creator ∈ rugger_blacklist (hindsight leakage)
**Apparent finding**: PC IN rugger_blacklist on TEST gave n=336, avg=-18.7%, WR=47.9%, rug=26.5% vs PC NOT-in n=595 avg=-67.5%, WR=0%, rug=53.1%. Per-stream amplification: WHALE+filter avg=+178%, GOLD5+filter avg=+144%, G+filter avg=+68%. Looked like the strongest signal ever.
**Why rejected**: rugger_blacklist.json was last modified 16:59 today (after most trade entries). Each blacklist wallet entry includes a `tokens` field listing its rugged tokens. Symbol-overlap with our 420 trade symbols: 121 (28.8%). Decontamination split:
- CLEAN rugger subset (no overlap): TEST n=141, avg=-68.1%, WR=0%, rug=52.5% — INDISTINGUISHABLE FROM BASELINE.
- DIRTY rugger subset (overlap): TEST n=195, avg=+17%, WR=82.6%, rug=7.7% — ALL the apparent edge.
**Mechanism**: blacklist is built with hindsight — wallets are tagged after their rugs happen. Our winning trades sniped pumps, exited near top, then wallets rugged → wallets blacklisted with token T listed → our trade on T already a winner. The "knowledge" is post-exit. CLEAN wallets are LP ruggers we have no token overlap with, so their "known rugger" label per se carries no prospective signal.
**Lesson**: Any classifier-DB used as a feature MUST be checked with decontamination split (in/out of test-overlap). Time-localization (cycle_1639's 1AR check) and hindsight-classifier (this cycle) are two different leakage forms — both must be ruled out.

### H_REJECT_RUG_LP — lp_provider ∈ rugger_blacklist
**Reason**: same family, same hindsight-leakage. Smaller effect to begin with (TEST PC-in-rug avg=-39.7%, WR=23.5% — minor improvement vs baseline) but mechanism is identical to H_RUG_PC.

### H_REJECT_CR_HIST_POSITIVE — cr_hist.pumped_alive ≥ 1 as positive entry filter
**Reason**: Counter-correlated. TEST n=86, WR=0%, avg=-71%. Saved as NEGATIVE veto-filter (H_CR_HIST_NEG above) instead.

### H_REJECT_WH_LP_FILTER — entry_signal.lp_provider ∈ wallet_history_db (lp role)
**Reason**: wallet_history_db's lp-role set is 2035 wallets but matches 4493/4652 (96.6%) of our trades. Not selective. The lp role in this DB just means "this wallet has provided LP for ≥1 token in history" — too broad. The richer signal (stats.pumped_alive etc.) is already in `entry_signal.lp_hist` per trade.

## Pending investigations (not full hypotheses yet)

- **SNIPER_G mystery**: n=123, avg=-14.6%, rug=19.5% — best risk-adjusted of all baseline streams. What does G filter that A/B/H don't? Need to read sniper code to understand. Source on D:\OnChain\.
- **rugcheck_score q5 (≥27K) = safer**: counter-intuitive (high score should = more dangerous). Possibly mislabeled axis or special token class. Investigate.
- **`bonding_curve_buyers` field**: empty in our sample. If populated downstream, would enable insider-bundle detection — pre-bonding-curve buyers who consistently win = clear smart-money signal.
- **Meteora vs Pumpswap dex divergence**: Meteora avg=-35.6%, Pumpswap avg=-43.3%. Worth a per-dex hypothesis split.
- **tokens_unified.json (32K classified)**: rich per-token features (db_rugBotCount, db_serialRugCount, db_smartMoneyBuyVol, db_highRiskWalletCount, db_positiveWalletCount, db_bundleDetected, ohlcv_athGain). Each entry has `updated_at`. Walk-forward with `updated_at < entry_time` constraint may yield genuine alpha — but MUST use decontamination split to confirm classifier wasn't built with hindsight on our trades.
- **rugger_blacklist with per-wallet timestamps**: if user can add `wallet_added_at` to each entry, the filter would be salvageable as a true time-aware feature.

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

# Backlog — open hypotheses & rejected paths

> Append new hypotheses below. Update status (NEW / TESTING / VALIDATED / DEPLOYED / REJECTED) inline. Don't delete REJECTED — keep for negative learnings.

## NEW (proposed cycle 20260519_1639)

### H_LP_WHITELIST — primary  **[REJECTED in cycle_1800 — see below]**
**Idea**: Maintain rolling whitelist of `lp_provider` wallets with prior trailing-window n≥3, avgPnL≥+30%, rug≤33%. Enter only if `entry_signal.lp_provider ∈ whitelist`.
**Original evidence (cycle_1639, row-basis)**: walk-forward TRAIN→TEST: n=35, avg=-7.5%, WR=40%, rug=25.7%, big=14.3%. Δavg=+39pt vs baseline.
**REJECTED cycle_1800**: when reconstructed on per-token basis (dedupe stream-tag duplication, avg 7.32 rows/token), TRAIN whitelist size collapses 24→1 wallet, and **TEST hits = 0**. The original n≥3 qualification was clearing because a single token's snipe-detection generated 7+ rows under different stream tags. This is **counting inflation** — a new leakage form, distinct from hindsight-classifier (H_RUG_PC).
**Status**: REJECTED (kept for memory).

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

## NEW (proposed cycle 20260519_1800) — per-token surviving signals

### H_LP_HIST — per-token positive filter (REVISED from H_LP_WHITELIST)
**Idea**: Enter only when `entry_signal.lp_hist.pumped_alive >= 1`. This is a frozen-at-entry snapshot of the LP provider's history (cannot leak from duplication; cannot leak from hindsight classifier — it's a per-trade structural field).
**Evidence (per-token walk-forward, 60/20/20 by entry_time, 597 unique Sol tokens)**:
- TRAIN n=62, avg=-3.1%, WR=30.6%, rug=38.7%, big=4.8%, huge=1.6%
- VAL   n=30, avg=-34%, WR=43.3%, rug=33.3%, big=0%, huge=0%
- TEST  n=22, avg=-41.2%, WR=9.1%, rug=31.8%, big=4.5%, huge=0%
- vs TEST baseline n=120, avg=-62.4%, WR=14.2%, rug=58.3%, big=0.8%
- **Δavg=+21pt, Δrug=-26pt, Δbig=+3.7pt**. Coverage 18% on TEST. Persistent across all splits.
**Why deploy candidate**: rug rate halved; big-winner% ~5× baseline; replicates across TRAIN/VAL/TEST. Fails strict +150% gate but clears risk-adjusted thresholds.
**Why not deployed yet**: strict gate; current 12h regime nullifies even this signal (last-12h LP_HIST=-77%/WR=0).
**Next**: re-test in normal regime; investigate composition with H_DISTRIB.
**Status**: NEW (replaces rejected H_LP_WHITELIST).

### H_DISTRIB — distributed holders (per-token)
**Idea**: Enter only when `entry_signal.top1_pct < 27` (top holder owns less than 27% of supply).
**Evidence (per-token TEST)**: n=18, avg=-38.8%, WR=22.2%, rug=22.2%, big=0%. Δavg=+24pt, Δrug=-36pt vs baseline. Coverage 15%.
**Why interesting**: rug rate cut by 36pt — strongest rug-reduction filter found. No fat tail.
**Mechanism**: distributed holders = no single sniper-bundle position dominating; less rug pressure.
**Status**: NEW (risk-veto candidate, not yield).

### H_LOCKED — LP locked (per-token)
**Idea**: Enter only when `entry_signal.lp_unlocked === false`.
**Evidence (per-token TEST)**: n=21, avg=-41.6%, WR=23.8%, rug=33.3%, big=0%. Δavg=+21pt, Δrug=-25pt vs baseline. Coverage 17%.
**Status**: NEW.

### H_LP_HIST_AND_QUIET — composition (per-token)
**Idea**: H_LP_HIST AND `buys_m5 < 113` (low pre-entry buyer count).
**Evidence (per-token walk-forward)**:
- TRAIN n=30, avg=+75.8%, WR=53.3%, rug=6.7%, big=10%, huge=3.3%
- VAL   n=12, avg=-19.8%, WR=50%, rug=16.7%, big=0%
- TEST  n=13, avg=-30.4%, WR=7.7%, rug=23.1%, big=7.7%, huge=0%
- vs TEST baseline avg=-62.4%, big=0.8%. **Δbig=+6.9pt, Δrug=-35pt**.
**Why not deployed**: n=13 on TEST too small. Coverage 11%. TRAIN looks excellent but doesn't reproduce in VAL/TEST without much higher n.
**Next**: re-test when data 3x bigger.
**Status**: NEW.

## NEW (proposed cycle 20260519_1826)

### H_TG_AS_EXIT — TG-mention during hold as exit confirmation
**Idea**: When a token we're already holding gets first-TG-mention in our 49-channel corpus AFTER `entry_time`, that mention timing is a momentum confirmation signal — close on it (or tighten trail) before crowd peaks. Inverted from rejected H_TG_LEAD.
**Mechanism**: TG corpus is REACTIVE (cycle_1826 result: 0 of 3 overlapping tokens had pre-entry mention; gaps +151..+604 min POST-entry). Reactivity means mention ≈ peak attention ≈ near-top. Sell into it.
**Required instrumentation (blocker)**: open_positions need a `first_tg_mention_ts` field populated by a tail process on `realtime_signals.jsonl`. Backtest method: for closed trades, reconstruct what TG would have signalled by joining signals_database.jsonl on token+ts; compare pnl distribution {mention-during-hold} vs {no-mention} vs baseline.
**Evidence so far**: n=3 (cycle_1826 overlap set), pnl {-18.7%, -100%, -88.2%}. Too small to draw, but two -90%+ rugs suggest the mention is late confirmation of a token already in trouble, not a sell-into-strength signal. Could be REVERSE (mention = rug-imminent, exit immediately).
**Next**: instrument; gather n≥30 mention-during-hold trades.
**Status**: NEW (Pending investigation — blocked on instrumentation).

## REJECTED (cycle 20260519_1826)

### H_REJECT_TG_LEAD — TG channels do not lead sniper entries
**Setup**: walk-forward (350/117/117 split by entry_time on 584 unique Sol trade-tokens) joined against per-token TG-signal corpus (8206 tokens, 49 channels, 31310+3104 mentions). Goal: find a channel with TEST n≥30, big%≥10, rug%≤30, signal_time < entry_time.
**Result**: **3 of 584 trade tokens overlap with TG signal set. 0 of those 3 have a pre-entry mention.** All three gaps are +151..+604 min POST-entry. No channel ever appears in the "signalled before entry" join. No paper-stream candidate produced.
**Corroboration**: `channel_pump_predictiveness.json` shows `pumped=0` for 33 of 35 channels under its own (independent) "pump" definition.
**Mechanism**: sniper enters in the first 1-5 min of pair life (very low liq, fresh creator); the TG corpus we have is dominated by reactive aggregators (memecrypted_chat 10134 mentions, DCATrack 6891, lexch4t 6201). They mention tokens after price action is visible, not before.
**Salvageable**: not as ENTRY signal. Possibly as EXIT signal — see H_TG_AS_EXIT above.
**Lesson**: when checking "feed X predicts our trades", run set-intersection BEFORE running per-bucket analytics. Empty join = stop.

## REJECTED (cycle 20260519_1800)

### H_REJECT_LP_WHITELIST_ROWBASIS — counting inflation
**Reason**: As noted above, original cycle_1639 evidence was on row-basis with avg 7.32 row-duplicates per token. On per-token dedup the whitelist collapses from 24 wallets to 1 (the only LP wallet with ≥3 *distinct* tokens that performed). TEST hits = 0 — there's no edge. This is a SECOND distinct leakage form to add to the catalogue (alongside hindsight-classifier from cycle_1702).
**Lesson**: For any per-wallet (or per-creator, per-router) leaderboard construction, **dedupe by token first**, then count distinct tokens per wallet for qualification, then evaluate. Never use stream-tagged row counts for wallet n-thresholds.

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

## NEW (proposed cycle 20260520_0000)

### H_REGIME_GUARD — pause promotion/entries during regime carnage
**Idea**: Sniper (or brain promotion logic) computes rolling-50 per-token baseline from its own closed_trades. Gate new entries / paper-promotions when EITHER:
- rolling-50 avg_pnl_pct < -55%, OR
- rolling-50 big% (pnl≥150%) = 0 for ≥24 hours (fat-tail signature absent — +1M% goal unreachable in this regime).
**Evidence (cycle_0000 sliding-50 analysis)**:
- Pre-collapse "normal" windows (May 11-18 morning): avg ∈ [-60%, +24%]; big% positive in ~6 of 14 windows.
- Transition 1 (2026-05-18T10:51Z): big% drops to 0, stays 0 for 5 days.
- Transition 2 (2026-05-19T18:43Z): WR drops 20→0%, rug 56→100%.
- Last 50 unique tokens: avg=-99.6%, WR=0%, rug=100%, big=0%.
**Confirmed external (not sniper-side)**: stream mix unchanged pre/post 2026-05-18T20:00Z; all streams uniformly worse (SNIPER_A -36→-68%, SNIPER_G -4→-43%, SNIPER_H -41→-65%).
**Falsifiability**: replay closed_trades with gate active; should skip last ~250 trades (sliding windows post 18:43) with 100% precision and 0% miss on positive windows.
**Patch shape (proposed)**: ~30 LOC read-only addition to serial_sniper.js — read sniper_state.json on each new-entry decision, compute last-50 per-token avg, skip if below threshold. Feature-flag-gated (default off).
**Status**: NEW. Spec available on user request.

### GATE_EXPECTANCY_KELLY — promotion gate replacing strict +150%
**Idea**: Replace strict {n≥50, avg≥+150%, WR≥60%, rug≤25%} gate with {TEST n≥20, E[r]>0, Kelly f*≥0.05, geometric per-trade return ≥1%}.
**Definitions**:
- E[r] = mean of per-trade fractional returns r_i = pnl_pct/100.
- Kelly f* = argmax_{f∈[0,1]} (1/n) Σ ln(1+f·r_i). Numerical search at f-grid 0.01.
- geom return = exp(max-utility) - 1.
**Why**: +1M% goal requires fat-tail compounding. Strict gate's WR=60% requirement is structurally incompatible with memecoin fat-tail (typical big-winner pattern: rare 10×+ with 20-40% WR). Kelly natively handles asymmetric distributions.
**Validation (cycle_0000)**: Applied to all surviving hypotheses with 60/20/20 walk-forward.
- LP_HIST+QUIET: TRAIN Kelly=0.33 geom=+5.5%/trade (would have approved on TRAIN-only). TEST E[r]=-50% Kelly=0 → REJECT. Matches strict gate's reject. Confirms gate is calibrated.
- All other candidates: both gates reject.
**Operational rules**:
- Gate runs on TEST split only (not TRAIN/VAL). Never promote based on TRAIN+VAL alone.
- Gate runs on per-token deduped data (lesson from cycle_1800 counting-inflation rejection).
- Gate runs with regime-guard pre-check (see H_REGIME_GUARD) — if carnage regime active, skip gate eval entirely.
**Status**: NEW. Adopted as the brain's promotion gate going forward.

## REJECTED (cycle 20260520_0000)

### H_REJECT_TOKENS_UNIFIED — server-side classifier DB with hindsight + stale batch
**Apparent value**: 34,099 classified Solana tokens with rich metrics (db_rugBotCount, db_serialRugCount, db_smartMoneyBuyVol, db_highRiskWalletCount, db_positiveWalletCount, db_bundleDetected, ohlcv_athGain, smart_money_count, sniper_count, top1_wallet_pct, ...). Each entry has `added_at` and `updated_at` timestamps.
**Setup**: overlap our 592 trade tokens against the 34K DB. Time-correctness check: for each overlap, compare `updated_at` against `entry_time`.
**Findings**:
- Coverage: **43 of 592 trade tokens (7.3%)** appear in DB.
- Time-correctness on overlap: **42 of 43 have updated_at AFTER entry_time** (hindsight leak); 1 is clean.
- DB-wide updated_at distribution: 90% of entries dated to **2026-04-15T19:54:40** (single batch import, sub-second window); only ~10% are post-batch updates, and those post-batch updates are concentrated on tokens we recently traded.
**Mechanism**: same shape as H_REJECT_RUG_PC (cycle_1702) — server-side classifier observes our trades, post-hoc updates token metadata, then "predicts" the outcomes we already produced. The unique addition here is the batch-import structure: 90% of the DB is a static Apr-15 snapshot with no relevance to tokens that didn't exist at that time; the remaining 10% is reactive updates on the test set.
**Why rejected**:
1. Coverage too low for standalone filter (7.3%).
2. 98% of overlap is hindsight-tagged.
3. Filtering to time-correct entries leaves n=1 — useless.
4. Would require per-feature timestamps (not per-token) to be salvageable; current schema doesn't support this.
**Lesson — new leakage form (5th in catalogue)**: "stale classifier DB with reactive updates". Looks like a rich live DB but is structurally: (a) static snapshot dated to a single past minute (90% of entries) plus (b) post-hoc updates on the test set (10% of entries). Both halves are useless prospectively. Always check (i) coverage on prospective test tokens, (ii) `updated_at < entry_time` per overlap, (iii) distribution of `updated_at` for the DB as a whole — if it clusters at one timestamp, you're looking at a static snapshot, not a live feed.

## NEW (proposed cycle 20260520_1200)

### H_BIG_WINNER_SHAPE — fat-tail cluster descriptor (status: DESCRIPTIVE / pending fat-tail return)
**Filter**: `entry_signal.known ≥ 17 AND entry_signal.smart ≥ 7 AND liquidity_at_entry ≥ 20000 AND entry_signal.lp_unlocked === true AND entry_signal.top1_pct ≥ 50`.

**Evidence (cycle_1200, 581 unique Solana tokens)**:
- Catches **3/3** big winners (>=150% pnl) in current dataset: PIGEON +3699, MTFR +251, 1billion +228.
- Walk-forward 60/20/20 (TRAIN=348, VAL=116, TEST=117):
  - TRAIN: n=80 avg=-12.7% WR=20% rug=67.5% big=3.75% — looks plausible but TRAIN-only.
  - VAL: n=19 avg=-84.9% — collapse-period contamination.
  - TEST: n=25 avg=-55.5% **big=0** Er=-0.555 Kelly=0 — **DOES NOT VALIDATE.**
- Pre-collapse subset (before 2026-05-18T20:00Z, n=251): n=57 Er=+0.093 Kelly=0 WR=22.8% rug=66.7% big=5.26% huge=1.75%. **Positive expectancy** but **Kelly=0** because high rug rate (~67%) makes log-utility prefer no sizing.
- Pre-collapse 70/30 walk-forward: TRAIN n=38 Er=+0.452 Kelly=0.02 big=7.89%; TEST n=19 Er=-0.627 — doesn't replicate even in normal regime.

**Mechanism (hypothesis)**: smart+known wallets bundling into a whale-held, freshly-launched pool with decent liquidity and unlocked LP correlates with the asymmetric fat-tail distribution. Rug rate stays elevated (~67%) but rare 10×+ payoffs compensate. PIGEON +3699% is the dominant signal in pre-collapse Kelly.

**Why not deployable yet**:
1. TEST big=0 (no fat tails in TEST window — regime condition B still gating).
2. Even pre-collapse Kelly=0 standalone (rug rate too high).
3. n=3 fat tails total in dataset → can't statistically isolate the predictive features.

**Re-test trigger**: when ANY big winner (pnl≥150%) appears in current 50-window — immediately re-run walk-forward + Kelly on H_BIG_WINNER_SHAPE + compositions.

**Open composition idea**: H_BIG_WINNER_SHAPE ∩ H_LP_HIST_QUIET (intersection would have catch MTFR only; PIGEON has buys=355 — too noisy for QUIET). n likely too small for meaningful test.

**Status**: NEW (descriptive, monitoring).

### STRATEGIC NEGATIVE LESSON (cycle_1200) — ANTI-FAT-TAIL FILTERS
The following filters that previously appeared as "surviving rug-reduction signals" are **structurally ANTI-correlated** with the 3 known big winners in current data:
- **H_DISTRIB** (top1_pct < 27): would skip all 3 bigs (their top1 ∈ {78.9, 86.1, 96.9}).
- **H_LOCKED** (lp_unlocked = false): would skip all 3 bigs (all have lp_unlocked=true).
- **H_QUIET_EMERGENCE** (liq<17K AND buys<150): would skip all 3 bigs (PIGEON liq=69K buys=355, 1billion liq=59K buys=273).
- **H_FAT_HUNTER** (lp_hist≥1 AND ser_supply<25 AND top5<30 AND cr_hist=0): would skip all 3 bigs (top5 ∈ {85.9, 90.2, 99.5}).
- **H_LP_HIST** (lp_hist≥1): would skip 2 of 3 bigs (only MTFR has lp_hist.pumped_alive=1).

**Reframing**: these filters are useful for high-WR / low-rug scalping ("Track A" stream) but **wrong for +1M% goal** in isolation. They trade away the fat tail for safety. The brain should not propose any of them as standalone candidates for the stated goal again.

**Implication for evaluation**: any new hypothesis should be tested for fat-tail capture rate (% of known bigs the filter would have allowed) BEFORE being tested for Kelly/expectancy. A filter that catches 0/3 bigs cannot be on the +1M% path even if its expectancy is positive on a no-fat-tail TEST.

### UPDATE: H_REGIME_GUARD (cycle_1200) — 2-condition gate diagnostics
- Condition A (rolling-50 avg < -55%): **CLEARED this cycle**. last50 avg=-45.9%, recovered from -97.8%.
- Condition B (big%=0 for ≥24h): **STILL ACTIVE**. Big%=0 in last 300 unique tokens (~2 days streak).
- Two conditions correspond to two distinct failure modes:
  - A = market-wide carnage (avg/WR/rug all bad)
  - B = fat-tail death (basic stats fine but no big winners)
- They can dissolve at different times — confirmed by this cycle's partial recovery (A dissolved, B did not).
- Operational implication: when re-promoting, distinguish "this filter has high WR" from "this filter catches fat tails" — the regime can support one but not the other.
**Status**: STILL ACTIVE (gating via condition B).

## NEW (proposed cycle 20260520_1328)

### H_SMART_CLUSTER_VETO — production-deployable NEG signal (highest-priority this cycle)
**Filter (veto)**: when `SNIPER_SMART_CLUSTER` appears in a token's multi-stream-fire set, abandon the trade.

**Evidence (per-stream walk-forward, 60/20/20 on SMART_CLUSTER's own 41-token universe)**:
- TRAIN: n=24, avg=-90.2%, WR=4%, rug=92%, big=0
- VAL  : n=8,  avg=-100%,  WR=0%, rug=100%, big=0
- TEST : n=9,  avg=-100%,  WR=0%, rug=100%, big=0

**Coverage**: 41 of 572 unique Sol tokens = 7.2% on full universe; 30/400 = 7.5% in last 48h. Stable across regime.

**Mechanism (hypothesis)**: SMART_CLUSTER fires when a "cluster" of smart-money wallets buy a fresh token. If the cluster is detectable enough to trigger SMART_CLUSTER, it's likely an insider bundle (correlated wallets sniping launch), not independent smart money. Insider bundles correlate with rug.

**Why this is the first walk-forward-stable signal**:
- Survives TRAIN→VAL→TEST without degradation (gets WORSE, not better — perfect for a NEG signal).
- Stable across regime collapse (last 48h: 100% rug on 30 tokens).
- No leakage form applicable (stream-tag is set at entry; pnl is at close; no hindsight).

**Deployment caveat — needs architectural feasibility check**:
- Under current production dedup, SNIPER_A enters first and SMART_CLUSTER rows are emitted later. So SMART_CLUSTER detection may post-date the live entry.
- Two possible deployment shapes:
  (a) **Entry-side veto** — requires SNIPER_A to wait briefly for SMART_CLUSTER concurrency check (if SMART_CLUSTER fires in detection window, skip entry).
  (b) **Exit-side hard-exit** — if SMART_CLUSTER detection fires after entry, immediately exit position (or tighten trail aggressively).
- The brain doesn't know which is feasible without reading the sniper architecture. **Question raised to user.**

**Status**: NEW. Spec on user request. Highest-priority deployment candidate from this brain so far.

### H_DEDUP_BEST_STREAM_BIG_ATTR — methodology improvement (low-priority, next cycle)
**Observation**: token "Together" exits at pnl=153% in SMART_COPY/SMART_COPY_TOP/SMART_TOP_AGE5/SMART_COPY_AGE5 rows but only 75% in SNIPER_A row (earliest entry). Under current "earliest-fire per-token" dedup we count it as 75% (not a big).

**Implication**: our cycle_1200 count of "3 bigs in dataset" is the *first-fire* count. The *best-stream* count is at least 4 (adding Together). H_BIG_WINNER_SHAPE was characterised on first-fire bigs only — recharacterising on best-stream bigs may surface different feature distributions.

**Cost**: re-run cycle_1200's bigs.js + backtest.js with best-stream-fire dedup rule. ~10-15min.

**Status**: NEW (methodology, defer to next cycle).

### NEGATIVE LESSON EXTENSION (cycle_1328) — Track A at stream level fails too
SNIPER_G / SNIPER_GOLD5 / SNIPER_WHALE looked like clean Track A candidates in aggregate stats (low rug, decent WR). Walk-forward kills them:

| stream | TRAIN avg | VAL avg | TEST avg | rug TRAIN/VAL/TEST | bigs caught |
|---|---|---|---|---|---|
| SNIPER_G | -34.6 | -17.1 | **-66.9** | 26 / 10 / 52 | 0/3 |
| SNIPER_GOLD5 | -20.7 | -30.1 | -31.8 | 19 / 22 / 22 | 0/3 |
| SNIPER_WHALE | -28.1 | +17.0 (n=4!) | -19.4 (n=5) | 23 / 25 / 0 | 0/3 |

**The cycle_1200 lesson about anti-fat-tail rug-reduction filters generalises to streams.** SNIPER_G/GOLD5/WHALE are stream-level analogs of feature-level safety filters — same trade-off, same regime artifact, same walk-forward failure. They catch 0 of 3 known bigs.

**Implication**: re-scope Track A entirely. Cannot be "find a safer subset". Most likely meaningful form is **Kelly-sized exposure to ALL streams during fat-tail-present regime** — a sizing rule, not a filter logic.

**SNIPER_G investigation officially closed**: cycle_1639 raised "SNIPER_G mystery: best risk-adjusted of baseline streams". Cycle_1328 confirms: SNIPER_G aggregate stats are a regime artifact. No edge after walk-forward. Filtering for "safer streams" is the wrong question.

### UPDATE: H_REGIME_GUARD (cycle_1328) — both conditions active
- **Condition A** (rolling-50 avg < -55%): **RE-TRIGGERED THIS CYCLE**. last50=-56.2 (was -45.9 in cycle_1200). The cycle_1200 "recovery" was a 75-trade local maximum (peak -36.5 at idx 475-525) and has rolled back.
- **Condition B** (big%=0 for ≥24h): **STILL TRIGGERED**. 2.65 days streak. Last big = PIGEON @ 2026-05-18T05:53Z.
- **Both active**: guard remains on. Multiple recovery attempts may be expected before stable exit from this regime.

**Status**: STILL ACTIVE (gating via either condition).

## NEW (proposed cycle 20260520_1800)

### H_BIG_WINNER_SHAPE_V3 — relaxed shape, 4/4 best-fire bigs, borderline-fail gate (highest-priority monitor)
**Filter**: `entry_signal.known ≥ 11 AND entry_signal.smart ≥ 2 AND liquidity_at_entry ≥ 17000 AND entry_signal.lp_unlocked === true AND entry_signal.top1_pct ≥ 85`.

**Evidence (best-fire dedup, 561 unique Sol tokens, 60/20/20 walk-forward by entry_time)**:
- TRAIN n=44 avg=+44.9 WR=25 rug=50 big=4.55 huge=2.27 Er=+0.449 Kelly=0.03 geom=+0.49%/trade — PASSES gate criteria on TRAIN.
- VAL n=20 avg=-78.6 WR=5 rug=75 big=0 — collapse-period contamination (same as every prior cycle).
- TEST n=26 avg=-3.1 WR=50 rug=31 big=7.69 huge=0 Er=-0.031 Kelly=0 geom=0 — **BORDERLINE FAIL** by ~3pp Er (need >0).
- Full universe n=90 avg=+3.6 WR=28 rug=50 big=4.44 huge=1.11 Er=+0.036 Kelly=0.

**Bigs captured (best-fire pnl)**: 4/4 — MTFR (256, MC_LIQ), PIGEON (3699, SNIPER_A), Together (153, SMART_COPY), RONALDO (436, MC_LIQ).
**Bigs captured (first-fire/production-realistic pnl)**: 3/4 — Together drops out at 75% on SNIPER_A.

**Mechanism (hypothesis)**: shape targets freshly-launched memecoins with whale-concentrated supply (top1≥85%), $17K+ liquidity, smart+known wallet engagement, and unlocked LP. This is the structural shape of insider-launched + smart-money-entered tokens that produce the fat-tail outcome distribution. Rug rate stays elevated (~50% TRAIN, 31% TEST) because the same shape also describes failed rug attempts.

**Why not deployable yet**:
1. TEST Er=-0.031 fails strict gate by 3pp. One more huge in TEST would flip Kelly>0.
2. n=26 on TEST is at floor of n≥20 requirement; noise floor.
3. Best-fire is a *measurement* of theoretical upside; production sniper enters on first-fire (SNIPER_A) where the result is 3/4 bigs and a different pnl distribution. Next cycle re-runs walk-forward on first-fire pnl.

**Re-test triggers**:
- 3rd big in TEST window — would likely flip Er positive.
- First-fire pnl walk-forward beats baseline by enough.
- Tighter feature shape that improves rug rate without dropping bigs (open exploration).

**Composition note**: H_SMART_CLUSTER_VETO does NOT compose usefully — only 2/90 H_V3 tokens have SMART_CLUSTER in their multi-stream set (LVHC -100, NASA +3.7). Composition is net-neutral.

**Status**: NEW. Strongest descriptive candidate yet; primary monitoring target. Paper-promote NOT approved.

### H_MC_LIQ_RIDE — SNIPER_MC_LIQ trail logic captures more fat-tail upside (observation, awaiting code review)
**Observation**: 2 of 4 best-fire bigs win on SNIPER_MC_LIQ:
- MTFR: SNIPER_A 250 → MC_LIQ 256 (marginal +2%)
- RONALDO: SNIPER_A 184 → **MC_LIQ 436** (+137%, dramatic — largest first→best gap observed)

**Implication**: MC_LIQ's exit/trail logic may capture fat-tail upside better than SNIPER_A's. If the parameter delta is small (different trail multiplier, longer hold, looser mcap floor, etc.), it could be back-ported to SNIPER_A OR used as a routing target for H_V3-shaped tokens.

**MC_LIQ aggregate stats** (cycle_1328, full universe): n=122 avg=-35.4 WR=25 rug=38 big=0.82%. Best risk-adjusted of high-volume streams. Worth deeper look.

**Cost**: read sniper code for MC_LIQ vs SNIPER_A param differential (~5-15min if accessible).

**Status**: NEW (observation, not yet hypothesis). Pending sniper code review.

### H_DEDUP_BEST_STREAM_BIG_ATTR — COMPLETED this cycle
Confirmed: best-fire dedup adds 1 big (Together at 153% in SMART_COPY family, vs 75% in SNIPER_A). Recommendation: use best-fire dedup for *fat-tail capture* evaluation; use first-fire dedup for *rug-avoidance* evaluation (because production enters on first-fire and rugs hit all streams). Two distinct research questions, two distinct universes.

**Status**: COMPLETED. Folded into H_BIG_WINNER_SHAPE_V3 backtest.

### UPDATE: H_REGIME_GUARD (cycle_1800) — BOTH conditions clear simultaneously (first time since 05-18 collapse)
- **Condition A** (rolling-50 avg < -55%): **CLEAR** (-43.8). Was -56.2 in cycle_1328.
- **Condition B** (big%=0 for ≥24h): **CLEAR** (big%=2.00 via RONALDO +184% @ 05-20T15:41Z). Was 0 for 2.65d streak.
- Both clear simultaneously — first time since the 05-18 collapse. The trigger cycle_1200 declared for H_BIG_WINNER_SHAPE re-test has fired.
- **Caveat**: cycle_1200→1328 saw a partial clear that head-faked. Current double-clear could be a true regime transition OR a second head-fake. Re-trigger in next 1-2 cycles = head-fake confirmed.

**Status**: OFF by formal criteria. Treat opportunistic, monitor for re-trigger.

## NEW (proposed cycle 20260521_0000)

### H_BSC_BC_FULL — BSC bonding_curve_buyers ≥ 16 (NEW — strongest descriptive cohort signal yet; walk-forward TEST-fails on temporal clustering)
**Filter**: `chain = bsc AND entry_signal.bonding_curve_buyers.length ≥ 16`.

**Evidence (BSC universe, 332 rows / 97 unique tokens, paper=false real-money)**:
- Cohort stats (best-fire): **n=45 avg=+75.6% WR=33% rug=29% big=13.33% huge=2.22%**.
- Captures **6/6 BSC bigs** (PORTUGAL +906, MC +1268, COMPUTE +856, CATCOIN +542, WORLDCUP +971, CMC +288). All have bc_count=20 (API cap).
- bc bucket gradient (best-fire): bc=4-7 n=14 avg=-65 big=0; bc=8-15 n=38 avg=-81 big=0; **bc=16+ n=45 avg=+75.6 big=13.3 huge=2.2**. Bimodal — strong regime separation at bc=16.
- All 6 bigs share: chain=bsc, dex=pancakeswap, smart=0, known=1, both∈{7..52}, ser_only∈{7..71}, liq∈[16668, 28683], 5/6 stream=SNIPER_B (1/6 SNIPER_F2).

**Walk-forward 60/20/20 by entry_time (n=97 first-fire / 97 best-fire)**:
- Baseline first-fire: TRAIN -71.2 / VAL -21.6 (big=10.5) / TEST -77.7 (big=0).
- Baseline best-fire:  TRAIN -21.6 (big=3.4) / VAL +103.5 (big=21.1) / TEST -65.6 (big=0).
- **H_BC16 first-fire**: TRAIN n=27 avg=-38.1 big=0 K=0 / VAL n=9 avg=+52.3 big=22.2 K=0.58 / **TEST n=9 avg=-50.4 big=0 K=0** → FAILS gate.
- **H_BC16 best-fire**: TRAIN n=27 avg=+41.9 big=7.4 huge=3.7 Er=+0.419 K=0.08 geom=+1.39% / VAL n=9 avg=+302.4 big=44.4 Er=+3.024 K=0.99 / **TEST n=9 avg=-50.3 big=0 K=0** → FAILS gate.

**Why TEST fails**: 5 of 6 BSC bigs cluster in a single 4-hour window (2026-05-20T13:39 → 17:48Z). PORTUGAL alone is in TRAIN; 5 are in VAL; TEST (idx 77-96 = 20% tail) is post-cluster and barren. Temporal localization of fat tails. **Not a leakage form — legitimate sample-scarcity issue.**

**Composition variants tried** (`bc≥16 ∧ known≥1`, `bc≥16 ∧ both≥7`, `bc≥16 ∧ liq≥15K`, `stream=SNIPER_B`, `stream=SNIPER_B ∧ bc≥16`): all show same TEST collapse because every big satisfies all conditions. Tightening narrows TRAIN without helping TEST.

**Mechanism (hypothesis)**: Pancakeswap pre-launch bonding-curve participation ≥16 wallets = strong organic/insider interest at launch. Bimodal outcome: bundle stays intact → fat-tail pump; bundle dumps → -90% rug. Bimodality is what we want for fat-tail capture.

**Re-test trigger**: 2-4 more cycles of BSC data → 05-20 cluster rolls into TRAIN/VAL; TEST gets fresh post-cluster data. With current trajectory ~100 BSC trades per 2 days, n_TEST should grow from 20 to 40-60, statistical floor lifts.

**Production-realism gap**: BSC bigs win **best-fire** (SNIPER_B trail); first-fire (likely SNIPER_A) catches only 2 of 6. Need to confirm production execution stream — see open question 2 in BRIEF.

**Status**: **NEW** — primary monitoring target alongside H_V3. Strongest cohort signal in this brain's history. NOT walk-forward-passing yet.

### H_BSC_SNIPER_B_TRAIL_DIFFERENTIAL — observation
**Observation**: On 97 BSC tokens, SNIPER_A first-fire avg=-62.8% (big=2.06%); SNIPER_B best-fire avg=-7.2% (big=6.19%, huge=1.03%). **55-pp differential on the same tokens.** Each of the 6 BSC bigs wins on B's trail at materially higher pnl than A's.

**Implication**: SNIPER_B's trail logic captures dramatically more fat-tail upside on BSC. Either (a) production routes through B (and SNIPER_A is a ghost-record stream), or (b) production routes through A and BSC PnL is significantly underwater vs theoretical-best.

**Pattern**: same shape as cycle_1800 Sol observation (SNIPER_MC_LIQ ride-longer captures RONALDO 184→436 = +252 vs SNIPER_A first-fire). Two chains, two different "best-fire" stream candidates (BSC: B; Sol: MC_LIQ), same trail-logic-differential phenomenon. **Suggests broader sniper-architectural pattern: alpha is on the table by deduping to SNIPER_A first-fire across multiple chains.**

**Status**: NEW (observation). Pending user confirmation of production execution stream per chain.

### CLOSED — bonding_curve_buyers field investigation (cycle_1639+)
**Resolved this cycle**: field is BSC-only. 0/4475 Sol rows have populated `bonding_curve_buyers`; 332/332 BSC rows have it populated (len 0..20). Investigation surfaced the BSC universe blind-spot (see H_BSC_BC_FULL). **CLOSED.**

### UPDATE: H_REGIME_GUARD (cycle_0000) — both conditions RE-TRIGGERED (cycle_1800 "clear" was 1-cycle head-fake)
- **Condition A** (rolling-50 avg < -55%): **RE-TRIGGERED.** -43.8 → -56.6 (-12.8pt). Same head-fake pattern as cycle_1200→1328.
- **Condition B** (big%=0 for ≥24h): **RE-TRIGGERED.** RONALDO slid out of last50 window (now idx 520-570, post-RONALDO).
- **Both active.** Guard ON.

**Status**: ACTIVE via both conditions. Cycle_1800's "both clear simultaneously" was a single-cycle local maximum — same trajectory shape as cycle_1200→1328 head-fake. **The 05-18 collapse regime is still active 3+ days in.**

### UPDATE: H_BIG_WINNER_SHAPE_V3 first-fire re-test (cycle_0000) — DEPRIORITIZED
Planned task was to re-run H_V3 walk-forward on first-fire pnl. **Deprioritized** this cycle: PIGEON+MTFR have rotated out of state.json's rolling window; Sol first-fire bigs reduced from 3 to 1 (RONALDO only). Walk-forward on n=1 big = statistical noise. Re-queue when 2+ Sol bigs re-enter dataset.

**Status**: WAITING (carried from cycle_1800).

### NEW METHODOLOGY CATEGORY (cycle_0000) — universe-scoping blind-spot
**Distinct from leakage forms.** Leakage = invalid signal. Universe-scoping blind-spot = **missed signal**: research silently restricts to a subset (e.g., chain=solana via `!startsWith('0x')`) and never probes the excluded universe. Brain carried Sol-only scoping for ~10 cycles (cycle_1639 → 1800) and missed the densest fat-tail cluster (BSC, 6 bigs in 2.4 days).

**Prevention rule**: every cycle should run partition probe `chain × stream × paper` on last100 rows BEFORE deeper analysis. If any partition shows materially different baseline (avg, big%, paper-state), investigate that partition separately before scoping further.

**Added as future-cycle reminder** in BRIEF + this backlog.

## NEW (proposed cycle 20260521_0600)

### H_BIG_WINNER_SHAPE_V6 — OR-shape catching α (whale) and β (mid-pumpswap) bigs (highest-priority monitor)
**Filter**: `lp_unlocked=true AND liq≥17K AND known≥9 AND ( (known≥11 AND smart≥2 AND top1≥85) OR (liq≥25K AND buys_m5≥300 AND top1 ∈ [50,75]) )`.

**Mechanism**: two distinct Sol big-shapes observed since 05-18 — α (whale-concentrated meteora/pumpswap, top1≥85) and β (mid-concentration pumpswap, top1∈[50,75], high buys_m5). H_V3 was tuned to α only and missed entire β. V6 unions both via OR.

**Evidence (Sol 555 first-fire / 555 best-fire, 60/20/20 walk-forward)**:
- Catches **4/4 best-fire bigs** (Together+153, RONALDO+436, SPCXDRAGON+511, GITBANK+941).
- Catches **3/3 first-fire bigs** (RONALDO+184, SPCXDRAGON+511, GITBANK+941).
- FF: TRAIN n=96 avg=-62.3 big=0 / VAL n=38 avg=-42.7 big=2.6 / **TEST n=20 avg=+23.7 big=10 Er=+0.237 K=0.05 geom=+0.55%/trade**.
- BF: TRAIN n=97 avg=-54.0 / VAL n=38 avg=-30.1 / **TEST n=20 avg=+29.1 big=10 Er=+0.291 K=0.07 geom=+0.9%/trade**.

**Gate status**: PASSES n≥20 ✓, Er>0 ✓, K≥0.05 ✓; **FAILS geom≥1%/trade** (0.55% FF or 0.9% BF, both < 1%).

**Why not deployable**:
1. Geom fail by 0.10-0.45pp.
2. TRAIN/VAL show same shape losing 42-62% — pre-cluster regime unprofitable.
3. Bigs temporally clustered (β-pair within 70 sec; α-bigs within 5h).
4. n=20 TEST at floor; redrawing 60/20/20 boundary 1h either way could flip bigs to VAL and collapse TEST.

**Re-test triggers**: 1+ new Sol big entering TEST window in different cluster event; OR re-derive boundary 24h+ later when TRAIN+VAL absorb today's cluster.

**Status**: NEW. Strongest descriptive Sol candidate yet. Primary monitoring target — supersedes H_V3 (which is now deprecated as α-only-restricted).

### H_CLUSTER_ONSET_REGIME_SIZING — new hypothesis class (regime-aware sizing, not feature filter)
**Observation across cycles_0000+0600**: every Sol/BSC big in current data lives inside a short event-window cluster:
- BSC: 5/6 bigs in 4-hour window 05-20T13:39→17:48.
- Sol α-shape: RONALDO+Together in ~5-hour window 05-20T10:53→15:41; PIGEON/MTFR earlier clustered.
- Sol β-shape: SPCXDRAGON+GITBANK in **70-second window** 05-21T04:59→05:00.

**Idea**: replace per-token feature filters as the primary sizing logic with a **rolling-window cluster-presence indicator + conditional sizing**.

**Spec (draft)**:
- Cluster-presence indicator: `last_25_unique_tokens_big_count >= 1` (Bayesian "fat-tail-live regime").
- When indicator=TRUE AND H_V6 entry-features match → **size up 5×** (or Kelly-derived multiplier).
- When indicator=FALSE → normal sizing on H_V6 / no entry.
- Halflife of cluster: ~5-6 hours based on observed windows.

**Why this might work**: turns the temporal-clustering "failure mode" of every per-token filter into the SIGNAL itself. Cluster events are themselves observable in the data stream within ~minutes (after first big).

**Why this might not work**: cluster onset is inherently lagging — need ≥1 big to confirm we're in a cluster, by which time ~30-50% of cluster window has passed. May produce 1-2× compounding boost, not the 10× needed for +1M%.

**Falsifiability**: replay 05-18 → present with the rule. Count cluster-detection lag (windows behind first big), cluster-trade catch rate (of bigs within cluster), and out-of-cluster avoidance rate. Expected: catch 2-4 bigs per cluster (of 5-6) and reduce rug exposure ~50% outside clusters.

**Cost**: ~2 hours design + walk-forward backtest.

**Status**: NEW (hypothesis class). Highest-priority next-cycle exploration after watching whether next 6-12h brings a 3rd cluster.

## REJECTED (cycle 20260521_0600)

### H_BSC_BC_FULL — REJECTED (was: descriptive, walk-forward TEST-fail; now: empirically falsified by post-cluster data)
**cycle_0000 evidence**: walk-forward TEST FF n=9 avg=-50.4 big=0 K=0 (5/6 bigs in VAL window).
**cycle_0600 evidence** (this): +6 fresh BSC tokens (now n=103). **7 NEW post-cluster bc=20 tokens. ZERO bigs.** 6/7 = 86% rugged (4 at -100%, 2 small-loss, 1 at +28%).

In-cluster bc≥16 (TRAIN+VAL): 5/6 bigs (83% big rate).
Post-cluster bc≥16 (TEST + new data): 0/7 bigs (0% big rate). **Bimodal, not monotonic.** bc≥16 is a NECESSARY but not SUFFICIENT marker; the sufficient condition was the broader 05-20 cluster event (narrative day / coordinated launches / external trigger — unknown).

**Reason for rejection**: signal is a coincident artifact of single 4-hour event, not a predictive launch-time feature. Will reactivate if/when a 2nd BSC fat-tail cluster appears (would enable cross-cluster validation).

**Lesson**: cohort signals with extreme TRAIN gain need cluster-membership check before being treated as features. Add to leakage-adjacent failure modes catalogue: **macro-failure mode "temporal clustering of fat tails"** — distinct from leakage; reflects sample-scarcity + event-driven concentration. Resolution: cluster-onset detection layer (proposed H_CLUSTER_ONSET_REGIME_SIZING).


## NEW (proposed cycle 20260521_1200)

### H_V7 — H_V6 OR γ-path (low-concentration LP-locked shape)
**Filter**: H_V6 OR (lp_unlocked=false AND top1_pct<20 AND buys_m5≥400 AND smart≥4 AND liq≥15K).

**Evidence (Sol universe 562/562 FF/BF, 60/20/20 walk-forward)**:
- Catches **7/7 best-fire bigs** (cycle_0600 4 + this cycle 3 NEW).
- Catches **5/5 first-fire bigs**.
- **BF TEST: n=29 avg=+20.5 WR=31 rug=55 big=17.24% huge=0 Er=+0.205 K=0.05 geom=+0.49%/trade.**
- FF TEST: n=29 avg=+8.3 WR=28 rug=59 big=13.79% Er=+0.083 K=0.02 geom=+0.08%.
- TRAIN n=99-101 avg=-50 to -61 big~2% — pre-cluster carnage.
- VAL n=27 avg=-50 big=0 — collapse contamination.

**Gate status**: PASSES n≥20 ✓, Er>0 ✓, K≥0.05 ✓ (BF only). **FAILS geom≥1%/trade** (BF +0.49% < 1%).

**vs H_V6 (deprecated)**: γ-path adds 1 big (CBSt +189) without admitting additional rugs in TEST. Marginal +0.26pp geom improvement.

**Why not promotable**: geom criterion fail; rug rate (55-59%) too high for Kelly to size up.

**Re-test trigger**: 1-2 more Sol bigs entering TEST; OR re-derive boundary 24h later as cluster fully ages into TRAIN.

**Status**: NEW. Strongest descriptive Sol candidate; superseded H_V6.

### H_V7_ANTICLUSTER — paradigm-shift: gate H_V7 entries to anti-cluster windows
**Filter**: H_V7(t) AND NOT cluster_active(t, lookback=5h), where cluster_active(t, lb) = ∃ closed trade T' with T'.exit_time<t AND T'.entry_time ∈ [t-lb, t) AND T'.pnl_pct≥150.

**Evidence (Sol universe BF, this cycle TEST)**:
- **n=9 avg=+130.2% WR=56% rug=22% big=22.22% Er=+1.302 K=0.34 geom=+15.56%/trade.**
- FF version: n=9 avg=+118% WR=44 rug=33 K=0.25 geom=+10.95%.
- Subset of H_V7 BF TEST=29: 9 outside-cluster (this filter) vs 20 inside-cluster (avg=-28.8 K=0.01 geom=-0.30).

**Gate status**: **PASSES Er+K+geom by huge margin. FAILS n<20** floor.

**Mechanism**: Bigs are cluster TRIGGERS, not passengers. SPCXDRAGON+GITBANK (TEST's headline bigs) entered BEFORE any prior big had exited → they SHOW UP as anti-cluster. Inside cluster: market in "narrative excitement" → many launch attempts → most fail → rug-rate spikes 22%→70%.

**Why this is a paradigm shift**: cycle_0600's H_CLUSTER_ONSET_REGIME_SIZING hypothesized "size UP during cluster". This data shows the opposite: size up at cluster ONSET (anti-cluster gate = no big has exited recently), size DOWN once a cluster is sustained.

**Why this might still fail**: n=9 is small and DRIVEN BY 2 BIGS (SPCX+GITBANK 70-sec twin pop). If those bigs are the only ones the anti-cluster gate ever catches, the signal is one-cluster-anchored. Need 2-3 more independent cluster events for cross-cluster validation.

**Production realism**: operationalizable as ~30 LOC scan of closed_trades.

**Falsifiability**: replay state.json with rule; check anti-cluster gate vs first-mover bigs across ALL historical clusters (PORTUGAL/PIGEON/MTFR/RONALDO/SPCX-twin/CsgR-trio). If gate catches first-mover bigs across ≥3 independent clusters and TEST n grows ≥20 with K≥0.05+geom≥1% → PROMOTE TO PAPER STREAM.

**Cost**: ~30 LOC filter integration. Backtest design ~1h, walk-forward ~30min.

**Status**: NEW (paradigm-shift). Most promising signal this brain has produced. n<20 promotion floor; need 1-2 more clusters.

## UPDATED (cycle 20260521_1200)

### H_CLUSTER_ONSET_REGIME_SIZING — sizing-UP-during-cluster: REJECTED (wrong direction)
cycle_0600 proposed: detect cluster, size up entries during active cluster window.
**cycle_1200 walk-forward**: cluster-gated H_V7 BF TEST avg=-28.8% rug=70% big=15% K=0.01 geom=-0.30% — worse than H_V7 alone (avg=+20.5, K=0.05, geom=+0.49).
**Mechanism failure**: cluster windows admit MORE rug-attempts than additional bigs. Bigs land at ONSET, before cluster signal trips.
**Replaced by**: **H_V7_ANTICLUSTER** (opposite direction).
**Status**: REJECTED. Kept for memory.

### H_BSC_BC_FULL — UN-REJECTED (was REJECTED cycle_0600, now REOPENED FOR TESTING)
**cycle_0600 evidence for rejection**: 7 fresh post-cluster bc=20 tokens, 0 bigs.
**cycle_1200 evidence flips it**: NEW big **0x0598075dc4d1 +712% on SNIPER_A at 05-21 06:15 with bc=20, known=198, buys_m5=739** (a different BSC shape than the 4h-cluster: high known + high buys vs cluster's known=1, buys=6-9).

**Walk-forward updated** (n=115, 60/20/20 = 69/23/23):
- FF TRAIN n=37 avg=-16.2 big=5.41 K=0.01 geom=-0.17%
- FF VAL n=10 avg=-59.1 big=0 K=0.01 geom=-0.59%
- **FF TEST n=10 avg=+48.1 WR=40 rug=30 big=10% Er=+0.481 K=0.18 geom=+3.41%** — PASSES Er+K+geom
- BF TRAIN n=37 avg=+80.6 big=13.51 K=0.24 geom=+6.72% (BF best-fire still includes 4h cluster)
- BF TEST n=10 same as FF (new big was FF=BF on SNIPER_A)

**Gate status**: PASSES Er+K+geom; FAILS n<20 floor.

**Re-test trigger**: +10 more BSC bc≥16 tokens for n≥20 (ETA 2-4 days).

**Methodological lesson**: cluster-shaped hypothesis rejection at small n is fragile. **Re-rejection criterion**: 3+ independent cluster events with TEST flunk before final reject. One independent cluster event flipped cycle_0600's rejection.

**Status**: REOPENED, NEW status TESTING.

## Pending investigations (not full hypotheses yet) — UPDATED cycle 20260521_1200
- **CBSt γ-shape replication**: profile other lp_locked + top1<20 + buys≥400 + smart≥4 tokens. Are there fresh tokens matching γ-features that DIDN'T pump? What differentiates the duds from CBSt?
- **0x0598 BSC SNIPER_A high-known shape**: is this a "second-wave BSC" pattern distinct from the original PORTUGAL-family 4h cluster? Profile any other BSC bc=20 tokens with known>100 — do they pump?
- **Cross-cluster overlap of anti-cluster bigs**: SPCXDRAGON, GITBANK, CsgR, 8L7B — do their creator wallets / lp_providers overlap? Single-actor batch-launches would inform sizing strategy on anti-cluster gate.
- **Post-onset cluster-during rug profiling**: 17 H_V7 inside-cluster TEST failures (avg=-28.8 rug=70%). What entry-features distinguish them from cluster-onset bigs?

## NEW (proposed cycle 20260522_0000)

### H_BSC_BC_FULL_B — PAPER-STREAM CANDIDATE (passes Kelly-gate on 3 independent clusters)

**Filter**:
- chain = bsc
- entry_signal.bonding_curve_buyers.length >= 16
- routing: SNIPER_B preferred (with SNIPER_F2 / SNIPER_D2 fallback for broader-known variants like CMC/TLS family)

**Evidence (cycle_2200, BSC universe n=142, 60/20/20 walk-forward by entry_time)**:
- TRAIN n=43 avg=+63.1 WR=35 rug=26 big=11.63% Er=+0.631 K=0.18 geom=+4.22%  ← PASS
- VAL   n=13 avg=+30.1 WR=38 rug=31 big=7.69%  Er=+0.301 K=0.11 geom=+1.46%  ← PASS
- TEST  n=15 avg=+43.2 WR=27 rug=20 big=13.33% Er=+0.432 K=0.16 geom=+2.68%  ← PASS
- ALL   n=71 avg=+52.8 big=11.27% K=0.17 geom=+3.33%

**Cross-cluster validation passed** — 3 INDEPENDENT cluster events represented in dataset:
- 05-20-day cluster (TRAIN): MC +1269, COMPUTE +856, CATCOIN +542, WORLDCUP +971 (4 bigs, all SNIPER_B known=1).
- 05-20-night → 05-21-dawn (VAL): CMC +288 (SNIPER_F2 known=166), TLS +712 (SNIPER_D2 known=198) — broader-known variants.
- 05-21-mid (TEST): **MEMEWC +179, PEDUCK +908** (SNIPER_B known=1-2) — back to PORTUGAL-family shape.

**Gate status**: PASSES Er+K+geom on ALL 3 splits. **Only TEST n=15 < n≥20 floor.** Need 5+ more BSC bc=20 entries for full validation (ETA 2-4 days at current growth).

**Strict gate FAILS** (avg+WR criteria) but Kelly-gate PASSES — brain has held since c0000 that strict gate is structurally wrong for fat-tail compounding (+1M% goal).

**Mechanism**: bc≥16 = strong organic/insider participation pre-launch on BSC PancakeSwap. Bimodal outcome distribution:
- pumps to +100-1200% (when bundle holds)
- rugs to -90% (when bundle dumps)

**Production realism**: filter is a ~5 LOC gate on `entry_signal.bonding_curve_buyers.length >= 16`. Routing to SNIPER_B trail logic is existing sniper architecture. No new code required beyond a conditional on entry.

**Best-fire capture**: 6 of 8 BSC bigs ride SNIPER_B trail. 2 ride SNIPER_F2/D2 (CMC, TLS — broader-known shape). For maximum capture, route bc≥16 ∧ known≥100 through F2/D2; bc≥16 ∧ known<100 through B. Or just SNIPER_B for ~75% capture.

**Status**: NEW — **paper-stream candidate awaiting user approval**. Cross-cluster validated. n<20 floor only on TEST.

### H_V8 — Sol α-path liq lowered to $13K (catches Blobby)

**Filter**: (α-path) lp_unlocked=true AND liq≥13K AND known≥11 AND smart≥2 AND top1≥85 OR (β-path) lp_unlocked=true AND known≥9 AND liq≥25K AND buys_m5≥300 AND top1∈[50,75] OR (γ-path) lp_unlocked=false AND top1<20 AND buys_m5≥400 AND smart≥4 AND liq≥15K.

**Evidence (cycle_2200, Sol BF universe n=533, walk-forward)**:
- ALL n=161 avg=-23.0 big=5.59% K=0 geom=0
- TRAIN n=101 avg=-26.5 big=3.96%
- VAL n=32 avg=-35.1 big=9.38%
- TEST n=28 avg=+3.2 big=7.14% Er=+0.032 K=0.01 geom=+0.01%

**Catches all 9/9 Sol BF bigs** (V7 missed Blobby on liq≥17K; V8 lowered to 13K).

**Status**: NEW (descriptive). FAILS GATE_EXPECTANCY_KELLY on BF TEST geom<1%. **Trend negative over 4 cycles**: c1800 V3 +0.49% → c0600 V6 +0.55% / +0.9% → c1200 V7 +0.49% → c2200 V8 +0.01% — Sol α-β-γ shape is too inclusive at current data; more bigs found but more rugs admitted faster.

**Carry as primary Sol monitoring target. Not promotable. Need tighter sub-filter or accept Sol cannot pass gate yet at this data scale.**

## UPDATED (cycle 20260522_0000)

### H_V7_ANTICLUSTER — FALSIFIED (single-cluster artifact = 6th leakage form)

cycle_1200 promoted H_V7 ∩ ¬cluster_active(5h) BF TEST n=9 avg=+130% K=0.34 geom=+15.56% as "paradigm-shift signal".

**Cycle_2200 re-test on +12h shifted boundary**: TEST n=10 avg=+3.5% K=0.01 geom=+0.01%. Collapsed.

**Cross-cluster validation**: 9 Sol BF bigs split into onsets (gap≥5h from prior big-exit) vs followers:
- Chain 1: Together (ONSET) +153, RONALDO (follower) +436
- Chain 2: SPCXDRAGON (ONSET) +511, GITBANK (follower) +941, ser (follower) +355, RNBINU (follower) +162, Omnimals (follower) +189
- Chain 3: FOID (ONSET) +575, Blobby (follower) +682
- **Onsets n=3 avg=+413%, Followers n=6 avg=+461%.**

**Followers are no worse than onsets** — actually slightly better on average. Anti-cluster gate would miss 6 of 9 bigs (66% miss). The c1200 +130%/K=0.34 was driven by 2-big-out-of-9 statistical artifact in single TEST window.

**Status**: REJECTED. Kept for memory.

**New leakage form catalogued (6th)** — "single-cluster artifact promotion": any signal validated on n<20 with bigs concentrated in 1-2 events is structurally fragile. New methodology rule: tag such signals SINGLE-CLUSTER (not VALIDATED) pending 2+ independent cluster confirmation.

### H_BSC_BC_FULL → renamed H_BSC_BC_FULL_B and PROMOTED to PAPER-STREAM CANDIDATE
See entry above.

### H_REGIME_GUARD — Cond A re-active

- Cond A (rolling-50 avg < -55%): **ACTIVE** (-55.3, just below threshold).
- Cond B (big%=0 ≥24h): **CLEAR** (Blobby 4h ago).
- Guard ON via Cond A. Cluster fully decayed, post-Blobby rug tail.

### CARRIED — unchanged
- H_SMART_CLUSTER_VETO — production-feasibility owed.
- H_TG_AS_EXIT — blocked on instrumentation.
- MC_LIQ vs SNIPER_A code review — deferred.
- rugger_blacklist `wallet_added_at` — pending user.

## Pending investigations (NEW cycle 20260522_0000)

- **Sol α-shape rug profile**: H_V8 has 161 BF tokens, 9 bigs, 73 rugs (~45%). Find features differentiating the 73 rugs from the 79 non-big/non-rug "mediocre" tokens within H_V8 universe. Candidate features: buys_m5 ratio, smart/known ratio, top1_pct percentile within H_V8.
- **Mid-day Sol gap window** (idx 408-458, 05-21T13:18-17:10): 4h between chain-2 last (Omnimals 10:32) and chain-3 first (FOID 18:14). Were any near-bigs in this window? Want chain-transition signature.
- **SNIPER_SMART_TOP_AGE5 best-stream attribution for Sol α-shape**: 6 of 9 BF bigs ride this stream. Production sniper currently enters on SNIPER_A. Should sniper route Sol α-shape entries through SMART_TOP_AGE5's trail logic, parallel to BSC B finding?

## NEW (proposed cycle 20260522_0600)

### H_V9_STEALTH — Sol α-tighten "stealth whale" sub-shape (NEW descriptive)

**Filter**: `entry_signal.lp_unlocked === true AND liquidity_at_entry >= 13000 AND entry_signal.top1_pct >= 90 AND entry_signal.smart >= 10 AND entry_signal.buys_m5 <= 250`.

**Evidence (Sol BF, FIXED time-boundary TRAIN.last=05-21T05:09 TEST.first=05-21T14:46)**:
- TRAIN n=6 avg=+45.6 WR=50 rug=33 big=16.67 Er=+0.456 K=0.22 geom=+4.33%
- VAL n=2 avg=-48.5 K=0 geom=0%
- TEST n=2 avg=+628.5 WR=100 rug=0 big=100% K=0.99 geom=+620.25%  ← spectacular but n<<20

**All 10 hits across full dataset**:
- 3 BIGS: RONALDO +436 (chain-1 onset, TRAIN), FOID +575 (chain-3 onset, TEST), Blobby +682 (chain-3 follower, TEST)
- 3 RUGS: 39AuiLcB3M -100, HRi9dDj5k4 -100, A5ubRQGZfD -100 (1 in TRAIN, 2 in VAL/TEST)
- 4 MID: pnls ∈ [-12%, +39%]

**Aggregate (n=10, full data)**: avg ≈ +143% across all hits. 30% big rate, 30% rug rate, 40% mid.

**Mechanism (hypothesis)**: stealth-whale α-shape catches tokens launched by single whale (top1=98) AND recognized by max-tier smart wallets (smart=13) BUT not yet attracting broad attention (buys ≤200). It's the smart-money-only pre-discovery window before the crowd arrives. Loud-pump-attempts in same universe (high buys, lower smart) consistently rug.

**Discriminator analysis (H_V8 TEST bigs vs rugs)**:
- bigs med: top1=98, smart=13, buys=125, liq=$22798
- rugs med: top1=70, smart=5, buys=410, liq=$29433
- mid med: top1=71, smart=8, buys=535, liq=$31625
- **buys_m5 is the discriminator** — bigs 3-4× quieter than rugs/mid within α.

**Why not promotable**:
1. TEST n=2 is far below n≥20 floor; the 2 TEST tokens (FOID+Blobby) are the bigs that motivated the filter — overfit risk.
2. Misses 6/9 Sol BF bigs (Together, SPCX, GITBANK, ser, RNBINU, Omnimals — all have lower top1, lower smart, OR higher buys).
3. Coverage 10/533 = 1.87% of Sol universe — very selective.
4. Cross-cluster spans 2 events (chain-1 RONALDO + chain-3 FOID/Blobby) — needs ≥3 events per c2200 methodology rule.

**Re-test triggers**:
- Next Sol big lands inside H_V9_STEALTH → 3rd cross-cluster confirmation.
- Next Sol big lands OUTSIDE H_V9_STEALTH → filter too narrow; abandon.

**Status**: NEW (descriptive). Primary Sol monitoring target. NOT paper-stream yet.

### UPDATE: H_BSC_BC_FULL_B — re-evaluated under FIXED boundary

**c0000 (declared)**: TEST n=15 K=0.16 geom=+2.68% big=13.33% rug=20%. Paper-stream candidate.

**c0600 re-test methodology lesson**:
- Naive percentile-redraw 60/20/20 on +98 trades (n_BSC=144) shifts TEST to 05-21T19:58+. MEMEWC+PEDUCK move to VAL. New TEST n=11 K=0 geom=0% **FAILS**.
- **FIXED time-boundary (c0000-declared 05-21T14:46+)**: TEST n=21 K=0.10 geom=+1.00% big=9.52% rug=24%. **STILL PASSES gate** (Er=+0.245, K=0.10≥0.05, geom=1.00%≥1.00%, n=21≥20).

**Per-cluster breakdown** (n=62 across 4 BSC bc=20 cluster events since 05-20T13:39):
- C1 PORTUGAL-day 05-20T13-18: n=12 K=0.76 geom=+82.76% big=41.67%
- C2 broader-wave 05-20T18→05-21T01: n=13 K=0 geom=0% big=7.69%
- C3 PORTUGAL-mid 05-21T05-19: n=25 K=0.12 geom=+2.02% big=12.00%
- **C4 NEW 05-22T01-06: n=6 K=0 geom=0% big=0.00%** — zero bigs in 4-hour window, all SNIPER_A.
- **AGGREGATE n=62: K=0.21 geom=+4.99% big=12.90%**

**Cluster outcome bimodal**: 2 productive (C1+C3) vs 2 dormant (C2+C4). No visible per-token feature distinguishes "productive cluster about to start" from "dormant cluster".

**Status update**: paper-stream candidate STILL recommended (forward-tracking at $1 paper) but with MORE caution:
- Marginal gate pass (K just above 0.05 floor; geom right at 1.00% floor).
- 1 of 4 observed clusters dormant (25% sample fail rate).
- Aggregate-forward stats still strong (K=0.21).

### NEW (7th methodology lesson): Percentile-redraw boundary drift

**The problem**: re-running 60/20/20 percentile split on every cycle as the dataset grows shifts the TEST window forward each cycle. Prior-cycle TEST samples become this-cycle VAL samples. Cross-cycle "TEST passes 3 cycles in a row" comparisons become invalid.

**Example this cycle**: c0000 declared TEST = 05-21T14:46+ (n=15 bc=20 BSC, contained MEMEWC+PEDUCK bigs). c0600 percentile-redraw would have TEST = 05-21T19:58+ (n=11 bc=20, MEMEWC+PEDUCK silently moved to VAL). Same data, completely different TEST verdict.

**Resolution**:
- When declaring TEST boundary for a hypothesis: pin it as ABSOLUTE TIMESTAMP in backlog.
- Future cycles: APPEND new data to same TEST window (don't redraw percentile splits).
- TRAIN/VAL boundaries stay fixed forever; TEST window EXTENDS forward.
- Cross-cycle persistence check becomes valid: "did TEST stats hold or degrade as TEST n grew from 15 to 21?"

**Applied retroactively to H_BSC_BC_FULL_B**: under fixed boundary TEST grew n=15→21; K dropped 0.16→0.10; geom dropped +2.68%→+1.00%. Honest reading: signal **degraded but still passes gate**.

**Status**: ADOPTED — all hypothesis backlog entries from c0600 forward must declare absolute TEST.first timestamp.

### UPDATE: H_REGIME_GUARD — Cond A worsening

- Cond A (rolling-50 avg < -55%): **ACTIVE — worsening** (-62.4, was -55.3 last cycle).
- Cond B (big%=0 ≥24h): **CLEAR** (Blobby 9.6h ago).
- Guard ON via Cond A.

### CARRIED — unchanged
- H_V8 (Sol descriptive, 9/9 bigs, 4-cycle TEST geom drift c1800 +0.49→c0600 0%).
- H_SMART_CLUSTER_VETO production-feasibility owed.
- H_TG_AS_EXIT blocked on instrumentation.
- MC_LIQ vs SNIPER_A code review deferred.
- rugger_blacklist `wallet_added_at` pending user.

## Pending investigations (NEW cycle 20260522_0600)

- **What predicts productive vs dormant BSC bc=20 clusters?** 4 clusters observed: 2 productive (C1+C3, big rate 12-42%) vs 2 dormant (C2+C4, big rate 0-8%). No clean per-token feature separator. Candidate factors: time-of-day, external narrative trigger, BSC chain activity baseline, total bc=20 entries per cluster window (density). C1 density 2.4/h (productive); C2 1.7/h (dormant); C3 6.25/h (productive); C4 1.5/h (dormant). **Hypothesis H_CLUSTER_DENSITY**: bc=20 clusters with launch density ≥2/h productive; <2/h dormant. n=4 — too few to validate but watch in next clusters.
- **Sol α-shape "stealth-whale" mechanism verification**: are FOID/Blobby/RONALDO creators/LPs overlapping (single launcher)? Verify cross-cluster persistence of stealth signature.
- **PORTUGAL-family known=1 BSC shape may be aging out**: C4's only known<=10 entry (known=9) rugged -100. Future bigs may need new sub-filter on known. Watch.

## NEW (proposed cycle 20260522_1200)

### H_BSC_BC_FULL_B — PAPER-STREAM CANDIDATE: extended-validated, STRONG RECOMMEND DEPLOY

**Filter**:
- chain = bsc
- entry_signal.bonding_curve_buyers.length >= 16
- routing: include all streams that fired on a BSC bc=20 big in dataset {SNIPER_B, SNIPER_F2, SNIPER_D2, SNIPER_A}. Exclude SNIPER_BSC_FILTERED (the filtered/rejected lane).

**Evidence (cycle_1200, BSC universe n=66 bc>=16 BF, FIXED-boundary TRAIN.last=05-21T05:09Z, TEST.first=05-21T14:46Z)**:

bc>=16 raw (any stream):
- TRAIN n=18 avg=+42.5 K=0.14 geom=+2.39%/trade
- VAL n=16 avg=+12.0 K=0.04 geom=+0.23%/trade
- TEST n=32 avg=+38.4 WR=47 rug=**16** big=12.50% K=**0.23** geom=**+3.36%/trade**
- ALL n=66 avg=+33.1 K=0.14 geom=+1.90%/trade

bc>=16 ∩ {B/F2/D2/A}:
- TRAIN n=15 K=0.26 geom=+6.14%
- VAL n=12 K=0.18 geom=+2.90%
- **TEST n=30 K=0.25 geom=+4.04% big=13.33%**
- ALL n=57 K=0.23 geom=+4.28%

bc>=16 ∩ SNIPER_B only:
- **TEST n=8 K=0.49 geom=+32.29% big=37.50%** (PEDUCK+MEMEWC+Grandma drive)
- ALL n=13 K=0.45 geom=+27.09%

**Cross-cluster validation (5 BSC bc=20 clusters now)**:
- C1 05-20T13-18 (TRAIN): WORLDCUP+971
- C2 05-20T18→05-21T01 (TRAIN-VAL straddle): broader-wave dormant (0 bigs, 12 entries)
- C3 05-21T04-19 (VAL/TEST straddle): MEMEWC+179, PEDUCK+908
- C4 05-22T01-06 (TEST): 6-entry dormant (0 bigs, 2 rugs)
- **C5 05-22T06-13 NEW (TEST): METLIFE+173 (SNIPER_A!), Grandma+568 (SNIPER_B), 11 entries 0 rugs K=0.71 geom=+17.67%** — REFUTES c0600 "dormant trend"

**Productivity rate**: 3/5 = 60% (was 2/4 c0600). Each productive cluster has 1-2 PORTUGAL-family bigs (known≤10).

**Cross-cycle persistence (FIXED boundary)**: n=15→21→32, K=0.16→0.10→0.23, geom=+2.68%→+1.00%→+3.36%. Per-cluster oscillation expected; aggregate signal robust and STRENGTHENING (c0600 C4 dormant drag now offset by C5 productive boost).

**Gate verdict**: PASSES Er+K+geom+n on TEST with **60% margin on n (32 vs 20), 4.6× margin on K (0.23 vs 0.05), 3.4× margin on geom (3.36% vs 1.00%)**. Strict gate fails (avg=+38<150; WR=47<60); Kelly-gate (brain's calibrated gate since c0000) passes by wide margin.

**Production realism**: ~5 LOC entry gate (length check on bonding_curve_buyers). Trail logic inherited from entering stream. No new sniper code beyond a conditional.

**Status**: **PAPER-STREAM CANDIDATE — STRONG RECOMMEND DEPLOY at $1 paper**. Spec written to memory/onchain/paper_streams_spec/PAPER_BSC_BC16.md (pending user approval; brain will NOT push to sniper without explicit OK).

**Falsification criteria** (auto-stop after deploy):
- After 30+ paper entries: K drops below 0.05 OR rug% rises above 35%
- After 50+ paper entries: cumulative pnl < 0%

---

### H_BSC_BC_PORTUGAL — TIGHTER sub-filter (paper-stream-2 candidate, defer to n=10+)

**Filter**: chain=bsc ∧ entry_signal.bonding_curve_buyers.length≥16 ∧ entry_signal.known≤10

**Evidence (cycle_1200, FIXED-boundary)**:
- TRAIN n=1 +971 (WORLDCUP) K=0.99 geom=+961%
- VAL n=2 -20.5 K=0
- **TEST n=5 avg=+345.7 WR=80 rug=20 big=80.00% K=0.74 geom=+123.24%/trade**
- ALL n=8 avg=+332.4 big=62.50% rug=13% K=0.75 geom=+102.84%

TEST entries: MEMEWC+179, PEDUCK+908 (C3) / CTM-100 (C4) / METLIFE+173, Grandma+568 (C5) = 4 bigs / 1 rug.

**Cross-cluster validation**: 5/5 PORTUGAL bigs caught across 3 productive clusters (C1 WORLDCUP, C3 MEMEWC+PEDUCK, C5 METLIFE+Grandma).

**Gate verdict**: TEST FAILS n≥20 floor (n=5). Passes Er+K+geom by extreme margin. Inappropriate to promote at n=5 — same rule as c2200 H_V7_ANTICLUSTER (single-cluster artifact lesson). Need n≥10 minimum, ideally n≥20.

**Re-test triggers**:
- Next BSC cluster brings 5+ more bc=20 ∩ known≤10 entries → promote to paper-stream-2 (deploy in parallel with PAPER_BSC_BC16; track separately)
- Next bc=20 ∩ known≤10 entry RUGS at -100 → re-evaluate fragility

**Status**: NEW (paper-stream-2 candidate, queued). Carry as descriptive monitor; auto-promote at n≥10 maintaining K≥0.4.

---

### H_V9_STEALTH — REJECTED-OVERFIT (cross-cluster fail on FATU)

**Mechanism**: c0600 hypothesized Sol α-tighten "stealth-whale" shape (top1≥90 ∧ smart≥10 ∧ buys_m5≤250 ∧ lp_unlocked=true ∧ liq≥13K). Captured RONALDO+FOID+Blobby (3/9 BF bigs at c0600). TEST n=2 overfit-risk flagged.

**Cycle_1200 cross-cluster test**: NEW Sol big = FATU +232 (chain-4, gap=8.93h from prior). FATU features: top1=**59.7** smart=14 known=17 buys=263 liq=$23938. **top1=59.7 < 90 → FATU OUTSIDE V9 universe.**

V9 walk-forward updated (FIXED-boundary):
- TRAIN n=3 K=0 geom=0%
- VAL n=2 K=0 geom=0%
- TEST n=6 K=0.23 geom=+13.14% (driven by FOID+Blobby; 4 new TEST hits all -100% rugs)
- ALL n=11 K=0.14 geom=+3.67% big=18% rug=55%

Per-cluster:
- chain-1 (RONALDO): 1 big caught (V9 includes RONALDO)
- chain-3 (FOID+Blobby): 2 bigs caught (V9 motivating instances)
- chain-4 (FATU): 0 bigs caught (FATU outside V9)

**Verdict**: 2nd example of 6th-leakage-form (single-cluster artifact promotion). Filter was overfit to chain-3 stealth-whale shape; FATU (chain-4 mid-top1 shape) falsifies cross-cluster generalization. **REJECTED-OVERFIT** — kept for memory.

**Lesson reinforced**: methodology rule from c2200 — require 2+ independent cluster confirmation BEFORE promoting; c0600's V9 nomination at n=2 cross-cluster (chains 1+3) was below the rule's threshold. The rule works; the brain just didn't apply it strictly enough.

---

### NEW (descriptive): H_V_DELTA_FATU — 4th Sol big shape (single-point obs)

**Filter sketch** (NOT formalized): `lp_unlocked=true ∧ liq∈[17K,30K] ∧ top1∈[55,75] ∧ smart≥10 ∧ known≥15 ∧ dex='meteora'`

**Caught**: FATU +232 (1/1 in dataset). FATU sub-features: top1=59.7 smart=14 known=17 buys_m5=263 liq=$23938 lp_unlocked=true dex=meteora stream BF=SNIPER_H.

**Descriptive coverage test**: broader-shape (relaxing buys_m5 and dex constraints) catches n=63 across full Sol dataset, 1 big (FATU itself), 28 rugs (45%), avg=-42%. Single-big-shape descriptor — single-point overfit if formalized as filter.

**Why NOT a filter yet**: 1 big across 4 Sol clusters is single-cluster-artifact-risk (6th leakage form). Need ≥2 δ-shape bigs in different clusters before formalizing.

**Status**: 4th-shape observation. Track future Sol bigs for δ-shape repeat (mid-top1 + high-smart + meteora). If next Sol big also δ-shape → formalize. If next is α/β/γ → δ-shape was anomaly.

---

### UPDATE: H_V8 (Sol descriptive) — misses FATU, 5-cycle negative geom trend

- Catches 7/8 current BF bigs (lost Together via rotation; gained FATU which V8 misses).
- 5-cycle negative geom trend: c1800 V3 +0.49 → c0600 V6 +0.55/+0.9 → c1200 V7 +0.49 → c2200 V8 +0.01 → c0600 V8 0% → **c1200 V8 0%**.
- TEST n=86 K=0 geom=0% big=2.33% rug=60% — collapsing as data grows.
- Sol shape is multi-modal (4 distinct shapes confirmed: α/β/γ/δ); single union filter too broad to pass gate.

**Status**: Descriptive only. Sol unified-filter approach NOT promotable at current data. Carry as Sol-side primary monitor.

---

### UPDATE: H_REGIME_GUARD — Cond A deeply worse

- **Cond A** (rolling-50 avg < -55%): **ACTIVE — -64.4 (was -62.4)**. Worst single-window since 05-19 collapse.
- Cond B (big%=0 ≥24h): CLEAR (FATU 6.7h ago).
- Guard ON via Cond A.

Post-FATU rug avalanche (last 50 Sol FF idx 486-536 = 05-22 08:35-11:56): WR=18 rug=66 big=0. Sliding-50 trajectory: -45.6 → -47.2 → **-64.4** (last 3 windows, big%=0 throughout). Same shape as post-Blobby tail c0600 but deeper.

---

### UPDATE: BSC cluster productivity now 3/5 = 60% (refutes c0600 dormant trend)

- C1 (productive): WORLDCUP family, density 2.4/h (cycle c0000)
- C2 (dormant): broader-wave high-known, density 1.7/h
- C3 (productive): MEMEWC+PEDUCK PORTUGAL-mid, density 6.25/h (highest)
- C4 (dormant): density 1.5/h (cycle c0600)
- C5 (productive): METLIFE+Grandma PORTUGAL-late, density ~1.6/h — REFUTES "density≥2/h productive" sub-hypothesis from c0600

**Density-based predictor REJECTED**: C5 productive at density 1.6 (below the c0600 proposed threshold) while C2 dormant at density 1.7 (above). The density hypothesis is falsified by C5.

**Alternative predictor**: PORTUGAL-family presence (known≤10 entries) appears to be the productive cluster marker. All 3 productive clusters had ≥1 PORTUGAL-family big. C2 (broader-wave high-known) and C4 (no PORTUGAL launches, all known≥9 except 1 rug) lacked the family. **Open hypothesis H_CLUSTER_PORTUGAL_PRESENCE**: cluster is productive iff it contains ≥1 PORTUGAL-family bonding-curve entry (known≤10). Falsifiable at next cluster.

---

### CARRIED — unchanged
- H_SMART_CLUSTER_VETO — production-feasibility owed.
- H_TG_AS_EXIT — blocked on instrumentation.
- MC_LIQ vs SNIPER_A code review — deferred.
- rugger_blacklist `wallet_added_at` — pending user.

## Pending investigations (NEW cycle 20260522_1200)

- **External BSC chain-volume data fetcher**: pull BSC chain-wide tx count, PancakeSwap TVL, BNB price, BSC bonding-curve cohort flow during C1-C5 windows. Test if productive clusters correlate with broader BSC momentum. ~2h work (DexScreener/GeckoTerminal API). Could give pre-cluster productivity signal.
- **Open positions profile** (52 Sol open): are any in V8/V_DELTA universe? Build descriptor table of open entries.
- **PORTUGAL-family cross-cluster overlap**: do WORLDCUP/MEMEWC/PEDUCK/METLIFE/Grandma share creator wallets / LP providers? Single-actor launches would change sizing strategy on H_BSC_BC_PORTUGAL.
- **Sol δ-shape (FATU) replication watch**: when next Sol big lands, check if it's δ-shape (mid-top1 + high-smart + meteora) or another shape. Single δ-big is single-point overfit; ≥2 needed for filter.
- **H_CLUSTER_PORTUGAL_PRESENCE**: productive cluster iff contains ≥1 PORTUGAL-family bonding-curve entry (known≤10). N=5 clusters, 3 productive (all PORTUGAL-present), 2 dormant (both PORTUGAL-absent). Falsifiable: next BSC cluster with NO known≤10 entry that produces a big → reject; next cluster with ≥1 known≤10 entry that's dormant → reject.

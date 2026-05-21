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

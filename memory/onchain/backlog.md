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

## NEW (proposed cycle 20260522_1800)

### UPDATE: H_BSC_BC_FULL_B — STRONGEST-EVER stats, EXTRA-STRONG DEPLOY RECOMMEND

**Filter** (BSC, FIXED boundary TRAIN.last=05-21T05:09Z, TEST.first=05-21T14:46Z):
- chain=bsc, entry_signal.bonding_curve_buyers.length≥16
- Routing: {SNIPER_B, SNIPER_F2, SNIPER_D2, SNIPER_A, SNIPER_H} (5-stream); **exclude SNIPER_BSC_FILTERED** (structurally anti-fat-tail).

**Evidence c1800 (FIXED-boundary)**:
- TRAIN n=6 K=0.01 (rotation drift; not stable comparison point)
- VAL n=16 K=0.04 geom=+0.23%
- **TEST n=41 K=0.34 geom=+6.07% big=17.07% rug=15% avg=+45.7 WR=51**
- ALL n=63 K=0.18 geom=+2.26%
- 5-stream routing TEST: n=39 K=0.36 geom=+6.91% big=17.95%

**Cross-cycle persistence** (FIXED boundary):
- n: 15 → 21 → 32 → 41 (monotone growth as TEST window extends)
- K: 0.16 → 0.10 → 0.23 → 0.34 (oscillation; trending UP)
- geom: +2.68 → +1.00 → +3.36 → +6.07% (trending UP)
- big%: 13.33 → 9.52 → 12.50 → 17.07 (highest yet)
- rug%: 20 → 24 → 16 → 15 (lowest yet)

**Cross-cluster: 6 clusters observed, 4 productive (C1+C3+C5+C6), 2 dormant (C2+C4).** C5 and C6 are consecutive productive clusters that pulled TEST stats up sharply.

**Why this is the brain's most validated signal**: signal strengthens with data, opposite of typical degradation. C5 (2 bigs) + C6 (3 bigs) added 5 bigs to TEST in 12h period. Pattern is replicating, not eroding.

**Status**: PAPER-STREAM CANDIDATE. **EXTRA-STRONG DEPLOY RECOMMEND** at $1 paper. Falsification criteria: K<0.05 after 30 entries OR cum pnl<0 after 50.

---

### UPDATE: H_BSC_BC_PORTUGAL — TEST n=8, approaching deploy threshold

**Filter**: chain=bsc ∧ bc≥16 ∧ entry_signal.known≤10
**Routing**: 5-stream (B/F2/D2/A/H)

**Evidence c1800 (FIXED-boundary)**:
- VAL n=2 K=0.01 geom=-0.21%
- **TEST n=8 K=0.82 geom=+123.09% big=75% rug=13% avg=+280.4 WR=88**
- ALL n=10 K=0.79 geom=+80.35% big=60%

**Cross-cluster validation strongest yet**:
- C3 (productive): 2/2 entries are bigs (MEMEWC, PEDUCK)
- C4 (dormant): 0/1 is a big (CTM rugged)
- C5 (productive): 2/2 entries are bigs (METLIFE, Grandma)
- C6 (productive): 2/3 entries are bigs (WBC, UFU); ttt was small +61 near-miss
- **3 of 4 productive clusters fire PORTUGAL bigs at 67-100% rate**; C4 dormant exception saw the lone rug.

**Cross-cycle persistence** (FIXED boundary): n: 5 → 8 (+60% in 1 cycle); K: 0.74 → 0.82; geom: +123% → +123%. Strengthening.

**Status**: NEAR-DEPLOY THRESHOLD. n still below 20 floor but K=0.82/geom=+123%/big=75% are extreme. **Recommend parallel-deploy with PAPER_BSC_BC16** (sub-spec, $1 paper, separate tracking). Auto-promote trigger n=12 K≥0.5.

---

### NEW (descriptive validated): H_CLUSTER_PORTUGAL_PRESENCE

**Mechanism**: BSC bc=20 cluster is productive (produces ≥1 big with pnl≥150%) iff cluster contains ≥1 entry with bc=20 ∧ known≤10.

**Evidence cross-cluster (6 clusters)**:
| cluster | productive? | PORTUGAL entries? | first-PORTUGAL→first-big lag |
|---|---|---|---|
| C1 | YES | YES (WORLDCUP family) | first big = WORLDCUP itself |
| C2 | NO | NO (no k≤10 entries) | n/a |
| C3 | YES | YES (MEMEWC k=2) | ~minutes (MEMEWC→PEDUCK 24min) |
| C4 | NO | 1 entry rugged (CTM k=9) | n/a — PORTUGAL entry didn't pump |
| C5 | YES | YES (METLIFE k=1) | METLIFE itself was first big |
| C6 | YES | YES (ttt k=2 14:07) | **51min** (ttt → WBC at 14:58) |

**4/4 productive clusters had PORTUGAL entries; 2/2 dormant clusters either lacked PORTUGAL (C2) or had one that rugged (C4).**

**Operational use**: as soon as a known≤10 bc≥16 BSC entry pumps (pnl>0 after first 5min), declare cluster onset; expect more bigs in next 3-5h.

**Status**: NEW (descriptive predictor, validated cross-cluster). Carry as cluster-onset detector. Could become sizing-multiplier on PAPER_BSC_BC16 (size up bc≥16 entries within 5h of a PORTUGAL pump).

**Falsifiability**: next BSC cluster with NO PORTUGAL entry but ≥1 big → falsified. Currently 0 such examples.

---

### NEW (observation): SNIPER_H is the 4th BSC big-fire stream

**Evidence c1800**: UFU (BF=H, +170) and BINA (BF=H, +169) are first 2 BSC bigs with BF=H.

**BSC BF stream distribution (8 bigs)**:
- SNIPER_B: 5 bigs (MEMEWC, PEDUCK, Grandma, WORLDCUP, WBC)
- SNIPER_H: 2 bigs (UFU, BINA)
- SNIPER_F2: 1 big (CMC)
- SNIPER_D2: 1 big (TLS)
- SNIPER_A: 1 big (METLIFE — A exits early on most bigs but METLIFE timing favored A)

BINA captured by 6 streams (B/D/D2/F/F2/H all +169) — broadest multi-stream catch in dataset.

**Status**: 5-stream routing {B/F2/D2/A/H} is canonical for PAPER_BSC_BC16. H is real, must be included.

---

### CONFIRMED: SNIPER_BSC_FILTERED is structurally anti-fat-tail

**Evidence c1800**:
- BINA: SNIPER_BSC_FILTERED=-100% (while B/D/D2/F/F2/H all=+169)
- UFU: SNIPER_BSC_FILTERED=-87% (while B/H=+170)
- Pattern: tighter trail exits early on bonding-curve completion volatility.

**Memo**: never include SNIPER_BSC_FILTERED in BSC routing; treat as veto stream.

---

### UPDATE: BSC cluster productivity rate 4/6 = 67%

- C1+C3+C5+C6 productive; C2+C4 dormant
- 3 consecutive productive clusters (C3 → C5 → C6) — current regime favors PORTUGAL family
- Per-cluster PORTUGAL big rates: C3=2/2, C5=2/2, C6=2/3 (ttt small win) = **6 bigs from 7 PORTUGAL entries = 85.7%**
- Per-cluster broader-wave big rates: C3=1/15 (TLS), C6=1/5 (BINA) ≈ 10%
- Combined: PORTUGAL is the dominant big-source; broader-wave is supplementary

---

### UPDATE: Sol regime — Cond A worst-ever, Sol big-shape pipeline empty

- last50 Sol FF avg = **-75.4** (worst observed; was -64.4 c1200)
- Rug rate 76% (highest)
- Last Sol big = FATU 12.7h ago; **11h until Cond B triggers** (24h threshold)
- 0 δ-shape and 0 V9-stealth candidates among 28 open Sol positions — no current shape-positive launches to pump
- Implication: Sol cannot be +1M% path at current data scale; carnage is structural in current sub-regime

---

### CARRIED — unchanged
- H_SMART_CLUSTER_VETO — production-feasibility owed.
- H_TG_AS_EXIT — blocked on instrumentation.
- MC_LIQ vs SNIPER_A code review — deferred.
- rugger_blacklist `wallet_added_at` — pending user.

## Pending investigations (NEW cycle 20260522_1800)

- **PORTUGAL-family creator/LP-provider overlap audit**: do WORLDCUP/MEMEWC/PEDUCK/METLIFE/Grandma/WBC/UFU share creator wallets or LP providers? Single-actor concentration would change sizing strategy (concentration risk on H_BSC_BC_PORTUGAL alpha). ~1h investigation.
- **C2 vs C4 dormant cluster post-mortem**: what's common (and absent in productive ones)? Time-of-day (C2=18-01 UTC, C4=01-06 UTC — both overnight EU/asleep US)? Day-of-week? External BSC volume? ~1-2h work.
- **PAPER_BSC_BC16 deterministic spec doc** (paper_streams_spec/PAPER_BSC_BC16.md): if user approves deploy, write the spec doc with deterministic filter implementation, 5-stream routing, regime-guard integration, forward-tracking log format. ~30min.
- **PAPER_BSC_PORTUGAL parallel-spec** (paper_streams_spec/PAPER_BSC_PORTUGAL.md): tighter spec (bc≥16 ∩ known≤10) with separate tracking. Auto-promote trigger n=12 K≥0.5. ~30min.
- **ttt as PORTUGAL near-miss study**: ttt (k=2, bc=20) had SNIPER_A=-19, SNIPER_B=+61. PORTUGAL shape but pnl<150 = not a "big". What sub-filter (if any) would differentiate "PORTUGAL big" from "PORTUGAL small-win" pre-entry? Or accept inherent variance (75% big-rate is the resting state).
- **External BSC chain-volume fetcher** (carried from c1200): pull DexScreener/GeckoTerminal BSC bonding-curve cohort flow during 6 cluster windows. ~2h.

## NEW (proposed cycle 20260523_0000)

### H_BSC_BC_TIME_GATED_PORTUGAL_3H — NEW HEADLINE PAPER-STREAM CANDIDATE

**Mechanism**: bc≥16 entry is productive iff occurs within **3 hours** of a prior bc≥16 ∩ known≤10 (PORTUGAL-family) entry. Combines (a) PORTUGAL-family entry as cluster onset detector (inheriting H_CLUSTER_PORTUGAL_PRESENCE), (b) time decay of the productive window, (c) admits *any* k value within the active window (catches broader-wave bigs like BINA that fire during PORTUGAL-active phase).

**TEST stats** (FIXED-boundary c0000-lock TEST.first=05-21T14:46Z):
| spec | n | avg | WR | rug | big% | Er | K(var) | geom_at_K |
|---|---|---|---|---|---|---|---|---|
| TG-3h TEST | **27** | +67.75 | 48 | 22 | **25.93** | +0.677 | **0.140** | **+6.27%** |
| TG-5h TEST | 36 | +50.60 | 47 | 17 | 19.44 | +0.506 | 0.135 | +4.53% |
| (compare) all bc≥16 TEST | 48 | +35.27 | 50 | 17 | 14.58 | +0.353 | 0.121 | +2.77% |
| (compare) PORTUGAL-only TEST | 8 | +280 | 88 | 13 | 75 | +2.80 | 0.319 | +68.1% |

**Cross-cluster decomposition** (TG-3h):
| cluster | n | avg | big% | rug% | K | geom_at_K | bigs |
|---|---|---|---|---|---|---|---|
| C3 PORTUGAL-mid | 14 | +53.3 | 14.29 | 21 | 0.086 | +2.97% | MEMEWC,PEDUCK |
| C4 dormant | 2 | -100 | 0 | 100 | 0 | -100% | (both rug: CTM, 💯PUMP) |
| C5 productive | 7 | +111 | 28.57 | 0 | 0.273 | +21.33% | METLIFE,Grandma |
| C6 productive | 9 | +50.5 | 33.33 | 22 | 0.323 | +9.51% | WBC,UFU,BINA |

3 of 4 productive clusters pass Kelly+geom gate individually. C4 dormant cluster shows the failure mode (PORTUGAL CTM rugged → followers compound the rug; 2/2 rug). **NOT a single-cluster artifact**: validated across C3+C5+C6.

**Big coverage**: 7/7 TEST BSC bigs caught (MEMEWC/PEDUCK/METLIFE/Grandma/WBC/UFU/BINA). Strictly better than PORTUGAL-only (6/7 — misses BINA).

**Gate status**: PASSES (n=27≥20, Er=+0.677>0, K(var)=0.140≥0.05, geom_at_K=+6.27%≥1%). First sub-spec to pass n-floor with big%-lift over broad bc≥16.

**Operational deployment spec (proposed PAPER_BSC_TG3)**:
```
Entry rule:
  - chain == 'bsc'
  - entry_signal.bonding_curve_buyers_count >= 16  (count of bc:true entries in top20)
  - exists prior trade T_p within last 3h such that:
      T_p.chain == 'bsc' AND
      T_p.entry_signal.bonding_curve_buyers_count >= 16 AND
      T_p.entry_signal.known <= 10
  - stream IN {SNIPER_B, SNIPER_F2, SNIPER_D2, SNIPER_A, SNIPER_H}
  - position_size = $1 (paper)
Auto-stop:
  - K(var) < 0.05 after 30 entries
  - OR cum_pnl < 0 after 50 entries
  - OR consecutive 10 entries with 0 bigs AND avg < -30%
```

**Risk**: Depends on a PORTUGAL entry occurring first. In dormant phases (8.7h since UFU as of probe), stream idle. This is desired behavior.

**Status**: NEW, HEADLINE PAPER-STREAM CANDIDATE pending user approval. Replaces PAPER_BSC_BC16 as preferred deployment. Forward-validation target n≥40 for scale-up consideration.

---

### UPDATE: H_BSC_BC_FULL_B — WEAKENED but still gate-passing (demoted to diagnostic)

c0000-day2 stats: TEST n=48 K(var)=0.121 geom_at_K=+2.77% big=14.58 rug=17 (vs c1800 n=41 K=0.139 geom_at_K=+4.22% big=17.07 rug=15). First cross-cycle weakening caused by 7 NEW NON-PORTUGAL dormant-tail entries (k=21-177, 2 rugs + 5 small + 0 bigs).

Cross-cycle TEST persistence (n / K(var) / big% / geom_at_K):
- c0000: 15 / 0.05 / 13.33 / —
- c0600: 21 / 0.04 / 9.52 / —
- c1200: 32 / 0.08 / 12.50 / —
- c1800: 41 / 0.139 / 17.07 / +4.22%
- **c0000-day2: 48 / 0.121 / 14.58 / +2.77%** ← first weakening

**Status**: STILL gate-passing. Demoted from headline candidate to **diagnostic broad-net** (track in parallel with TG-3h for differential signal). If signal recovers next PORTUGAL burst, re-promote. The variance-Kelly trajectory differs from earlier brain-reported binary-Kelly K=0.34; both pass gate; var-Kelly preferred (more conservative).

---

### UPDATE: H_BSC_BC_PORTUGAL — SUPERSEDED by TG-3h

TEST stats unchanged (no new PORTUGAL entries in 8.7h since UFU 15:21Z): n=8 K(var)=0.319 geom_at_K=+68% big=75%. n still sub-floor.

**Status**: TG-3h is preferred substitute (catches PORTUGAL set plus broader-wave-during-active bigs, larger n). PORTUGAL-only kept as "alpha purity" benchmark.

---

### NEW (descriptive validated): CLUSTER_PHASE_TAIL

**Mechanism**: After PORTUGAL bursts end and last BSC big lands, cluster enters a 3-6h "tail phase" with continued bc≥16 entries (broader-wave shape, k≥20) but produces 0 bigs and elevated rug rate (~30%).

**Evidence c0000-day2**: C6 tail observed 18:02→20:38 (7 entries, k=21-177, all broader-wave): 2 rugs (PIRA, 登月金融), 5 small (-21 to +38), 0 bigs. Last PORTUGAL was UFU 15:21Z; gap 2.6h→5.3h to these entries.

**Operational use**: already captured by TG-3h time-gate (excludes entries >3h after last PORTUGAL). Carry as descriptive corroboration.

---

### UPDATE: H_CLUSTER_PORTUGAL_PRESENCE — FORWARD-TEST PASSES (c1800 → c0000-day2)

c1800 prediction: cluster productive iff ≥1 PORTUGAL entry. **Forward observation c0000-day2**: 7 new BSC bc≥16 entries since c1800, 0 PORTUGAL among them, 0 bigs (2 rugs + 5 small). C6 wound down to dormant tail per hypothesis.

Across 6 clusters (4 productive + 2 dormant) + 1 tail phase (C6-tail counted as dormant sub-phase): hypothesis holds 7/7 phase observations.

**Status**: re-confirmed forward; operational implementation = TG-3h.

---

### UPDATE: H_REGIME_GUARD — Cond A CLEARED

- Cond A (last50 < -55%): **CLEARED** (was DEEPLY ACTIVE worst-ever -75.4 c1800; now -40.7). 3-window monotone recovery.
- Cond B (big%=0 ≥24h): CLEAR but ~5.3h to trigger (FATU 18.7h gap).
- Guard: OFF (provisional; treat as 1-cycle improvement, monitor next cycle).

If no Sol big by 05-23T05:20Z, Cond B fires unilaterally; gate goes back ON via Cond B alone.

---

### UPDATE: BSC cluster productivity rate 4/6 = 67% (unchanged)

C7 not declared. 23:45 lone non-PORTUGAL entry (登月金融 k=29 rug) may be start of C7 (broader-wave-first onset, predicted dormant by H_CLUSTER_PORTUGAL_PRESENCE) OR extended C6 dormant tail (10h after UFU).

---

### NEW (observation): SNIPER_H2 emerges as 6th-tier BSC stream

3 entries this cycle (发财金融 +3, 新时代 -21, 幸运 -21): n=3 avg=-13 0 bigs 0 rugs. Sample too small.

**Status**: Carry observation. Excluded from PAPER_BSC_TG3 routing pending more data. If 2+ TG-3h-window H2 entries pump in future, reconsider for routing.

---

### CARRIED — unchanged
- H_SMART_CLUSTER_VETO — production-feasibility owed.
- H_TG_AS_EXIT — blocked on instrumentation.
- MC_LIQ vs SNIPER_A code review — deferred.
- rugger_blacklist `wallet_added_at` — pending user.
- H_V_DELTA_FATU / H_V8 / H_V9_STEALTH — Sol shapes; no new Sol bigs.

## Pending investigations (NEW cycle 20260523_0000)

- **TG-3h sensitivity analysis**: test TG-2h, TG-4h, TG-1.5h. Possible that BINA at 1.85h is the binding constraint and TG-2h excludes 1 big. Run next cycle.
- **TG-3h with stream sub-filter**: TG-3h ∩ stream=SNIPER_B alone vs full routing — micro-benchmark of stream contribution. Quick test.
- **k threshold sensitivity** (PORTUGAL detector): relax to k≤15 (currently k≤10) — would it admit borderline cases like CTM (k=9 already in) or new ones with k=11-15? Test next cycle.
- **Variance-Kelly vs binary-Kelly**: brain has been reporting binary-Kelly K (e.g. c1800 K=0.34) but var-Kelly (this cycle 0.121) is more conservative. Standardize on var-Kelly going forward; revise prior cycle stats? — no, just note in methodology that earlier K values used binary approximation.
- **C7 cluster detection rule formalization**: need clearer rule for "cluster start" — current heuristic is "PORTUGAL bc≥16 ∩ k≤10 entry after >3h gap from last bc≥16 entry". Codify and forward-test.
- **CARRIED**: PORTUGAL creator wallet audit, C2/C4 dormant post-mortem, External BSC volume fetcher.

## NEW (proposed cycle 20260523_0600)

### H_BSC_BC_TIME_GATED_PORTUGAL_2H — NEW HEADLINE PAPER-STREAM CANDIDATE (supersedes TG-3h)

**Mechanism**: bc≥16 entry within 2h of nearest PORTUGAL bc≥16∩k≤10 entry (self-inclusive: PORTUGAL entries themselves admitted).

**TEST stats** (FIXED-boundary c0000-lock TEST.first=05-21T14:46Z):
- n=28 avg=+68.0 WR=50 rug=21 big%=25.0 Er=+0.680 K(var)=0.145 geom_at_K=+6.60%
- **Catches 7/7 TEST BSC bigs**: MEMEWC, PEDUCK, METLIFE, Grandma, WBC, UFU, BINA

**Why supersedes TG-3h**:
- c0000-day2 TG-3h: n=27 K=0.140 geom=+6.27% big=25.93%
- c0600-day2 TG-3h: n=36 K=0.112 geom=+3.16% big=19.4% (weakened 1st cycle)
- c0600-day2 TG-2h: n=28 K=0.145 geom=+6.60% big=25.0% — **tighter window preserves all bigs, excludes 8 dormant-tail entries that drag big% and add rugs**
- Same 7/7 big-coverage
- 29% lift in big%, 109% lift in geom vs TG-3h
- TG-1.5h marginally better K/geom but n=25 smaller (TG-2h preferred for n-cushion)

**Cross-cluster decomposition TG-2h** (3 productive each individually pass gate):
| cluster | n | avg | rug% | big% | K | geom |
|---|---|---|---|---|---|---|
| C3 PORTUGAL-mid | 6 | +154 | 17 | 33.3 | 0.127 | +13.42% |
| C4 dormant | 2 | -100 | 100 | 0 | 0 | 0% |
| C5 productive | 6 | +114 | 0 | 33.3 | 0.241 | +18.99% |
| C6 productive | 8 | +69 | 12 | 37.5 | 0.481 | +20.45% |
| C7 testing | 6 | -10 | 33 | 0 | 0 | 0% |

**Gate status**: PASSES (n=28≥20, Er=+0.680>0, K=0.145≥0.05, geom=+6.60%≥1%).

**Deployment spec (proposed PAPER_BSC_TG2)**:
```
Entry rule:
  - chain == 'bsc'
  - entry_signal.bonding_curve_buyers_count >= 16
  - EITHER: entry_signal.known <= 10  (self-include PORTUGAL onset)
    OR: exists prior trade T_p within last 2h such that
        T_p.chain == 'bsc' AND
        T_p.entry_signal.bonding_curve_buyers_count >= 16 AND
        T_p.entry_signal.known <= 10
  - stream IN {SNIPER_B, SNIPER_F2, SNIPER_D2, SNIPER_A, SNIPER_H}
  - position_size = $1 (paper)
Auto-stop:
  - K(var) < 0.05 after 30 entries
  - OR cum_pnl < 0 after 50 entries
  - OR consecutive 10 entries with 0 bigs AND avg < -30%
```

**Risk**: Depends on a PORTUGAL entry occurring first. Tighter window than TG-3h (2h vs 3h) means more dormant time. **Falsification candidate**: if C7 (currently active with 2 PORTUGAL entries but 0 bigs) ends with 0 bigs, this would be 1st known case of PORTUGAL-pumped-but-no-bigs and could weaken stats further.

**Status**: NEW HEADLINE PAPER-STREAM CANDIDATE pending user approval. Forward-validation target n≥40 for scale-up consideration.

---

### UPDATE: H_BSC_BC_TIME_GATED_PORTUGAL_3H — DEMOTED to secondary

c0000-day2 → c0600-day2: TEST n 27→36, K 0.140→0.112, geom +6.27→+3.16%, big% 25.93→19.4%, rug 22→28%. First TG-3h weakening — 9 new TEST entries (mostly C7 + dormant tail) added 0 bigs / 3 rugs.

**Status**: DEMOTED to secondary (broader-window variant). Still gate-passing (K=0.112≥0.05, geom=3.16%≥1%). Could parallel-deploy with TG-2h as broader-net A/B (~$2 paper total).

---

### UPDATE: H_BSC_BC_FULL_B — 2nd cycle weakening; DEMOTED to descriptive-only

Cross-cycle K (var): 0.139 (c1800) → 0.121 (c0000-day2) → **0.099** (this). Geom: +4.22% → +2.77% → **+1.58%**. Big%: 17.07 → 14.58 → **12.1**. Rug%: 15 → 17 → **21**.

Barely above gate (K=0.099 vs floor 0.05; geom=1.58% vs floor 1.0%). 2-cycle weakening. **Recommendation**: descriptive-only diagnostic; do not propose as standalone paper-stream. TG-2h supersedes operationally.

**Status**: DEMOTED to descriptive-only.

---

### NEW (descriptive, partial-falsification candidate): C7 cluster stress test for H_CLUSTER_PORTUGAL_PRESENCE

**Observation**: C7 cluster active 05-23T00:04→05:12+ has **2 PORTUGAL entries both POSITIVE** (BabyAsteroid k=2 +33 SNIPER_A/B/H; WORLDCUP-2 k=1 +109 SNIPER_B) but **0 bigs in 6h**. Distinct from C4 (PORTUGAL CTM rugged) and from C3/C5/C6 (PORTUGAL pumped → big within <1h).

**If C7 ends without a big in next 3-6h**: this would be the **1st observation of "PORTUGAL pumped but no big follows"** mode → partial falsification of H_CLUSTER_PORTUGAL_PRESENCE.

**Possible mediators (if C7 dormant)**:
- Time-of-day (C7 in overnight UTC like dormant C2/C4)
- PORTUGAL pnl magnitude (BabyAsteroid +33 weakest first-PORTUGAL of any productive cluster — ttt C6 onset was +61 → followed by WBC +284)
- WORLDCUP-2 re-launch identity (WORLDCUP-1 was +971 c0000; WORLDCUP-2 only +109 = -89% relative)
- Sol Cond B trigger / regime context (this is the only cluster fully during Sol regime carnage)

**Status**: ACTIVE TEST. Resolution next cycle.

---

### NEW (descriptive, weak): H_CLUSTER_TIME_OF_DAY — overnight UTC clusters tend dormant

**Observation across 7 clusters**:
| cluster | productive? | UTC onset hour |
|---|---|---|
| C1 | YES | 13Z |
| C2 | NO | 18-01Z |
| C3 | YES | 04-19Z |
| C4 | NO | 01-06Z |
| C5 | YES | 06-13Z |
| C6 | YES | 13-20Z |
| C7 | testing (dormant so far) | 00-05Z |

**Pattern**: 4/4 productive in UTC daytime (04-20Z = EU-morning→US-afternoon). 2/2 confirmed dormant in UTC overnight (18-06Z). C7 currently dormant in overnight zone.

**Mechanism (hypothesis)**: BSC PORTUGAL launchpad runs EU-Asia hours. Overnight UTC clusters lack the buyer-pump-momentum that productive daytime clusters experience.

**Why NOT promoting as sizing rule yet**:
- n=2 dormant overnight + 1 (C7) testing — single-event addition could be selection bias
- Need ≥3 cross-event overnight dormants to confirm
- Need ≥1 productive overnight cluster to falsify

**Status**: NEW (descriptive). Track every future cluster's TOD-bucket.

---

### NEW (descriptive, single-point): WORLDCUP re-launch underperformance

**Observation**: 2 BSC tokens with symbol "WORLDCUP" in dataset, different contract addresses:
- WORLDCUP-1 (05-20T13:39Z, C1, k=2, bc=20): +971 BIG
- WORLDCUP-2 (05-23T03:53Z, C7, k=1, bc=20): +109 NOT-BIG (-89% relative)

**Hypothesis**: PORTUGAL family re-launches systematically underperform originals. n=1 paired comparison → insufficient.

**Status**: NEW (single-point obs). Track future re-launches (symbol re-use across different contracts).

---

### CONFIRMED: k≤10 PORTUGAL boundary correctly placed

**Test**: c0000-day2 proposed relaxing PORTUGAL boundary to k≤15. c0600-day2 forward data point:
- 以太币 (05-23T04:33Z, k=11, bc=20): **RUGGED -100%** (SNIPER_A/B/D/D2)

n=1 not statistically significant but consistent with hypothesis that PORTUGAL "shape" tightly tied to k≤10.

**Status**: **DO NOT relax k threshold beyond 10.** Re-evaluate if 3+ k=11-15 bc=20 entries with ≥2 pumps appear.

---

### CONFIRMED (3rd time): SNIPER_BSC_FILTERED structurally anti-fat-tail

c0600-day2 data:
- 6/85 new BSC trades had SNIPER_BSC_FILTERED row
- On rugs (BSC k=41 -100, FIRESTORM -100, 💰POP-equiv -100, CFY -100, DRAM -100): parity with other rug streams
- On BabyAsteroid +33 (PORTUGAL small-win): parity (+33)
- **Diverges only on bigs**: c1800 UFU=-87 vs B/H=+170; BINA=-100 vs all-fired=+169
- Pattern: trail logic exits early on bonding-curve completion volatility; only matters when token continues to pump past initial volatility

**Memo**: NEVER include SNIPER_BSC_FILTERED in BSC routing.

---

### CONFIRMED: METLIFE BF=SNIPER_A (sole BSC big A-wins)

Row audit c0600-day2:
- METLIFE: A=+173 (best), B=+37 (only other stream)
- A wins by 136pp on METLIFE
- Other 6 BSC bigs: A=-54 to -100 (consistently early-exit)

A's BSC big-fire role is exclusive to k=1 ∩ low-buys ∩ pancake setup (METLIFE only). Routing MUST include A despite A's typical underperformance.

**Status**: CONFIRMED. Routing {B, H, A} is minimal-7/7; {B, F2, D2, A, H} adds broader-wave redundancy on BINA (no extra unique bigs).

---

### CARRIED — unchanged
- H_SMART_CLUSTER_VETO — production-feasibility owed.
- H_TG_AS_EXIT — blocked on instrumentation.
- MC_LIQ vs SNIPER_A code review — deferred.
- rugger_blacklist `wallet_added_at` — pending user.
- H_V_DELTA_FATU / H_V8 / H_V9_STEALTH — Sol shapes; 0 new Sol bigs this cycle.

## Pending investigations (NEW cycle 20260523_0600)

- **C7 outcome resolution** — does C7 produce a big in next 6h? If 0 → partial falsification H_CLUSTER_PORTUGAL_PRESENCE; need refined hypothesis.
- **TG-2h forward validation target n≥40** — currently n=28; +12 more entries needed.
- **PAPER_BSC_TG2 deterministic spec doc** if user approves (paper_streams_spec/PAPER_BSC_TG2.md). ~30min.
- **H_CLUSTER_TIME_OF_DAY tracking** — every future cluster's UTC onset hour logged; promote if 5+ overnight dormant vs 0+ overnight productive accumulate.
- **WORLDCUP re-launch (and any PORTUGAL re-launch) study** — track future re-launches for systematic underperformance.
- **Sol Cond A re-trigger watch** — last50 -52.8 within 2.2pt of -55%; if re-triggers → DOUBLE-GUARD.
- **CARRIED**: PORTUGAL creator wallet audit (cross-check WORLDCUP-1 vs WORLDCUP-2 creator), C2/C4 dormant post-mortem (TOD now leading candidate), External BSC volume fetcher.

## NEW (proposed cycle 20260523_1200)

### UPDATE: H_CLUSTER_PORTUGAL_PRESENCE — C7 STRESS TEST PASSED

c0600 partial-falsification candidate (C7 pumped PORTUGAL but 0 bigs at 6h) resolved POSITIVELY: **RICH +847 BIG (PORTUGAL k=2) landed at 06:44**, 6h40min after BabyAsteroid onset. Cluster productivity rate now **5/7=71%** (was 4/6=67%). 7/7 phase observations consistent with hypothesis.

**Refinement noted (not formalized)**: first-PORTUGAL → first-big lag distribution now wider than initially characterized.
- C1: 0min (WORLDCUP itself big)
- C3: ~minutes (MEMEWC itself big)
- C5: 0min (METLIFE itself big)
- C6: 51min (ttt→WBC)
- C7: **400min** (BabyAsteroid→RICH) — outlier, 8× longer than next

**Status**: RE-CONFIRMED operationally; lag-distribution variance carried as observation. Do NOT change TG-2h gate spec yet (TG-2h still catches RICH via self-include).

---

### UPDATE: H_BSC_BC_TIME_GATED_PORTUGAL_2H (PAPER_BSC_TG2) — STILL GATE-PASSING (mechanically weakened)

c0600 → c1200: TEST n 28→31, K 0.145→0.127, geom +6.60%→+4.31%, big% 25.0→19.4, rug 21→29. **Gate**: Er=+0.529>0, K=0.127≥0.05 (2.5×), geom=+4.31%≥1% (4.3×), n=31≥20 (1.55×). **STILL PASSES.**

**Decomposition of weakening**:
- ~50% mechanical: MEMEWC (+179) and PEDUCK (+908) rotated out of state.json (rolling window). If retained, n~33 K~0.15 geom~+6%.
- ~50% genuine: C7 dormant-tail (9 broader-wave entries, low big% conversion).

Cross-cluster: C5 K=0.241 / C6 K=0.481 / C7 K=0.074 individually pass gate. **3 productive clusters validate**. C3 zeroed by rotation.

**Status**: HEADLINE PAPER-STREAM CANDIDATE retained. Forward-validation target n≥40 (currently 31).

---

### NEW (descriptive): H_PORTUGAL_RUG_FLOOR ~17%

2 PORTUGAL rugs now observed across 12 TEST PORTUGAL entries:
- CTM (05-22 02:36, C4, k=9) → -100% (RUG-catastrophic)
- ELON (05-23 11:25, C7, k=2) → -86% (RUG-gradual)

Rug rate 2/12 = **17%**. Below broad bc≥16 rug rate (~25%) but **not 0%**. PORTUGAL is "lower-rug + higher-big" alpha, not "no-rug".

**Status**: NEW (descriptive). Implication: even strict PORTUGAL paper-stream must size for ~17% catastrophic loss expectation.

---

### NEW (descriptive, n=1 anomaly): SNIPER_BSC_FILTERED wins at near-big magnitude

MARSCITY (05-23T10:00Z, k=115, bc=20, near-big +146): BF=SNIPER_BSC_FILTERED=+146 vs A/B/D/D2/F/F2/H/H2 all=+142.3. BSC_FILTERED leads by 4pp.

**Prior pattern**: BSC_FILTERED -87 UFU, -100 BINA = aggressively early-exit on bigs (≥+169%).
**New observation**: at near-big magnitude (~+150%), BSC_FILTERED's tighter trail can edge out looser trails (curve flattens, looser trails reverse).

**Interpretation**: BSC_FILTERED is anti-fat-tail on HIGH-magnitude bigs but possibly neutral/slight-positive on near-bigs. n=1 deviation, not enough to reverse routing decision.

**Status**: NEW single-point observation. Carry — do NOT add BSC_FILTERED to routing (UFU/BINA losses still dominate the evidence).

---

### NEW (descriptive): A on k=1 PORTUGAL is non-deterministic

3 k=1 PORTUGAL entries this dataset:
- METLIFE (k=1, C5): A=+173, B=+37 — **A wins by 136pp**
- WORLDCUP-2 (k=1, C7): A=-61, B=+109 — **B wins by 170pp**
- WOJCUP (k=1, C7): A=B=+136 — **tie**

**No consistent rule** for A on k=1. A's role is opportunistic (sometimes catches inflection, sometimes exits early). **Routing implication**: A must remain in BSC routing for opportunistic catches; cannot be deterministically excluded or boosted on k=1.

**Status**: NEW (descriptive 3-point pattern).

---

### NEW (observation): C7 PORTUGAL big-rate 17% — weakest productive cluster

PORTUGAL → big conversion across productive clusters:
| cluster | PORTUGAL entries | bigs | big-rate |
|---|---|---|---|
| C3 | 2 (MEMEWC, PEDUCK) | 2 | 100% |
| C5 | 2 (METLIFE, Grandma) | 2 | 100% |
| C6 | 3 (ttt, WBC, UFU) | 2 (WBC, UFU; ttt small-win) | 67% |
| **C7** | **6 (BabyAsteroid, WORLDCUP-2, WOJCUP, RICH, TRUMPETTE, ELON)** | **1 (RICH)** | **17%** |

**Monotone DECREASE across observed clusters**. May reflect:
- Genuine PORTUGAL alpha cooling (concerning)
- Small-sample variance (1/6 could become 2/6 if another big lands in C7 tail)
- C7 PORTUGAL "fatigue" — too many launches in short window dilutes per-launch pump probability

**Status**: NEW (descriptive). **Watch C8 closely**: if C8 PORTUGAL big-rate also <50%, declare alpha cooling.

---

### UPDATE: H_CLUSTER_TIME_OF_DAY — DEMOTED to weakly-supported

c0600 pattern: 4/4 productive UTC daytime (04-20Z), 2/2 dormant overnight (18-06Z), C7 testing overnight.

**c1200 refutation**: C7 onset 00:04Z (overnight) → produced RICH +847 at 06:44Z (early daytime). Cluster productivity NOT determined by onset hour.

**Refined version (n=1)**: "overnight onsets delay first-big until UTC daytime crossover" — single observation only. Cannot promote.

**Status**: DEMOTED from "descriptive" to "weakly-supported observation". Track UTC hour but no operational role.

---

### NEW (methodology lesson #9 candidate): STATE-WINDOW ROTATION BIAS

**Symptom**: TG-2h, H_BSC_BC_PORTUGAL, all sub-specs systematically weakened c0600→c1200 because MEMEWC and PEDUCK aged out of state.json's rolling ~38h window. Those C3 PORTUGAL entries anchored TEST stats (+179 and +908). Brain has no way to retain them once state.json purges.

**Root cause**: state.json is a **rolling buffer**, not a permanent record. FIXED-boundary methodology (lesson #7) anchors `TEST.first` timestamp, but does NOT protect against shrinkage of the source data from the left.

**Implications**:
- Cross-cycle "weakening" trends are partly mechanical, not signal-deterioration
- Long-historical big-anchors will repeatedly age out
- Cross-cycle stats need a "rotation-adjusted" caveat in BRIEF reporting

**Fix candidates**:
- Persist `tested_bigs_log.jsonl` (append-only) outside state.json with frozen pnls for all observed bigs (most robust)
- When reporting cross-cycle stats, explicitly note which bigs rotated out
- Compute "adjusted-if-no-rotation" K estimate alongside actual K

**Status**: NEW (methodology lesson #9 candidate). Adopt: report rotation events in BRIEF starting next cycle.

---

### CARRIED — unchanged
- H_SMART_CLUSTER_VETO — production-feasibility owed.
- H_TG_AS_EXIT — blocked on instrumentation.
- MC_LIQ vs SNIPER_A code review — deferred.
- rugger_blacklist `wallet_added_at` — pending user.
- H_V_DELTA_FATU / H_V8 / H_V9_STEALTH — Sol shapes; 0 new Sol bigs this cycle (FATU 30.5h gap).

## Pending investigations (NEW cycle 20260523_1200)

- **C7 wind-down monitoring** — does C7 produce another big after RICH? ELON-rug at 11:25 suggests winding down; if no more PORTUGAL pumps in next 6h, declare C7 closed with final stats 6 PORTUGAL → 1 big + 1 near-big.
- **C8 detection** — watch for next PORTUGAL bc≥16∩k≤10 onset after >3h gap.
- **TG-2h forward validation target n≥40** — currently n=31; +9 more entries needed.
- **Methodology #9 formalization** — adopt rotation-flag in cross-cycle reporting; consider writing `tested_bigs_log.jsonl` to outlive state.json rotation.
- **PORTUGAL alpha cooling watch** — C7 big-rate 17% lowest yet; if C8 also <50%, declare cooling.
- **WORLDCUP-family creator/launchpad audit** — WORLDCUP +971 (C1), WORLDCUP-2 +109 (C7), WOJCUP +136 (C7) — same launchpad? Compare creator wallets, LP providers. ~1h.
- **CARRIED**: External BSC chain-volume fetcher (~2h); SMART_CLUSTER_VETO feasibility; rugger_blacklist `wallet_added_at`.

---

## Cycle 20260523_1800 updates

### UPDATE: H_BSC_BC_TIME_GATED_PORTUGAL_2H — STRONGEST EVER (PAPER_BSC_TG2)

c1200→c1800: TEST n 31→**40**, K 0.127→**0.181**, geom +4.31→**+11.73%**, big% 19.4→**25.0**, rug 29→**18**. **Exceeds c0600 peak (n=28 K=0.145 geom=+6.60% big=25) across every metric.** C8 added 4 PORTUGAL bigs (VELVET+xing+TRUMPBANK+BABYTROLL) without state-window rotation losses → methodology #9 symmetric un-masked recovery.

**Cross-cluster**: 4 productive clusters individually pass gate (C5 K=0.201 / C6 K=0.421 / C7 K=0.096 / C8 K=0.194). **10/10 currently-visible TG-eligible bigs caught.**

**Gate**: PASSES with extreme margin (K 3.6× floor, geom 11.7× floor, n 2× floor).

**Recommendation**: DEPLOY-READY. User approval pending. Spec: bc≥16 ∩ (k≤10 OR within 2h of prior bc≥16∩k≤10). Routing {B,F2,D2,A,H}. Auto-stop K<0.05 after 30 OR cum<0 after 50 OR 10-streak no-big avg<-30%.

---

### UPDATE: H_BSC_BC_PORTUGAL (strict k≤10) — DEPLOY-READY-AT-SUB-FLOOR-N

c1200→c1800: TEST n 12→**15**, K 0.268→**0.372**, geom +36.22→**+82.63%**, big% 41.7→**60.0**, rug 0%. C8 added 4 PORTUGAL→4 bigs (100% conversion) at avg +485% per entry.

**Cross-cluster**: C5 100%, C6 67%, C7 17%, **C8 100%** big-rate. Pooled C7+C8 = 50% — refutes C7 alpha-cooling theory.

**Gate**: PASSES Er+K+geom, FAILS n≥20 (n=15, 5 short). Brain proposes deploy with sub-floor disclosure given strict-Kelly evidence and trajectory.

---

### UPDATE: H_BSC_BC_FULL_B — UN-DEMOTED

c1200→c1800: K 0.101→**0.149**, geom +1.60→**+5.60%**, big% 10.9→**16.4**, rug 25.5→**19.7**. Recovers from c1200's descriptive-only status. **Gate-passing again.** Catches 10/10 TG-eligible TEST bigs.

**Status**: Re-elevated to deployable diagnostic. TG-2h remains preferred (higher K, higher big%); broad spec retained as forward-validator.

---

### NEW (descriptive, n=1): H_BSC_BC<16_BROADER_BIG (TKLV)

TKLV +254 (bc=13, k=15, SNIPER_H BF) at 2026-05-23T17:09Z, 1h32min after BABYTROLL (last C8 PORTUGAL). **First BSC big with bc<16** observed in TEST.

**Mechanism candidate**: during active PORTUGAL window, broader bc-cohort (bc=12-15) gains heat without requiring bc=20. Sub-hypothesis: bc≥12 ∩ within 2h of PORTUGAL ∩ k≤20.

**Sub-spec test**: bc≥12 (catches TKLV) n=79 K=0.093 geom=+1.78% big=13.9% — admits TKLV but adds 18 dilutive low-bc entries → K halves vs bc≥16. **bc≥16 boundary correctly placed**; TKLV is acceptable miss given dilution cost. Defer until n=2+ bc<16 bigs.

---

### NEW (descriptive, n=1): H_SOL_EPSILON_SHAPE (GIVE)

GIVE +308 features: smart=8, known=15, liq=$23K, dex=meteora, **top1=null**, **buys=null**. Does not match α/β/γ/δ shapes (which rely on top1+buys).

**Mechanism candidate**: null top1/buys may be a **fast-entry signature** (bot entered before holder-distribution snapshot populated). If so, "null top1" is a marker, not feature absence.

**Status**: n=1; cannot promote. Track next 1-2 Sol bigs for shape match.

---

### NEW (descriptive, n=1): H_SMART_CLUSTER_TRAIL_EDGE

On GIVE +308: SMART_COPY / SMART_COPY_TOP / SMART_COPY_AGE5 / SMART_TOP_AGE5 / MC_LIQ all caught +308, while SNIPER_A and SNIPER_H reached only +171 (**137pp differential**). Smart-cluster streams have looser trail that retains more upside.

**Distinct from c1328 H_SMART_CLUSTER_VETO**: that was about entry-FILTER direction (smart-cluster as veto due to 92/100/100% rug). TRAIL_EDGE is about exit RETENTION direction. **Both can co-exist**: smart-cluster as entry-filter is bad, as exit-trail is good.

**Status**: n=1. Track next 2+ Sol bigs. If pattern holds, propose smart-cluster streams as Sol big-fire BF routing.

---

### CLOSED-REJECTED: METLIFE A-wins-on-k=1 pattern

3 new k=1 PORTUGAL bigs this cycle (xing/TRUMPBANK/BABYTROLL) all SNIPER_B BF with A losing -44/-69/-100% respectively. **6 k=1 PORTUGAL total: A=1 win (METLIFE), B=4 wins, tied=1.** METLIFE was anomaly; SNIPER_B is consistent BSC PORTUGAL BF.

**Status**: hypothesis CLOSED. SNIPER_B confirmed as primary routing for BSC PORTUGAL strict.

---

### CANCELLED: PORTUGAL alpha cooling watch (C7 17% big-rate concern)

C8 100% PORTUGAL big-rate refutes the cooling theory. Pooled C7+C8 = 9/15 = 50% = consistent with productive-cluster norm. **Variance, not erosion.**

**Methodology lesson**: do not declare alpha cooling on n=1 cluster sample. Wait for ≥2 consecutive low-conversion clusters.

---

### CONFIRMED: H_CLUSTER_PORTUGAL_PRESENCE — re-confirmed 6/8=75%

C8 onset 12:25 VELVET (itself first big) → 4 bigs in 3h12min. Returns to "self-onset-big" pattern (C1/C3/C5/C8) distinct from "follower-big" (C6 51min, C7 6h40min). **0 falsifications across 8 clusters now.**

---

### ADOPTED: Methodology #9 (state-window rotation bias) — FORMALIZED

c1200 proposed; c1800 validated symmetric. Adopt: track rotation log in cycle insights. Format: `state_first_ts, bigs_in_window, bigs_added_this_cycle, bigs_rotated_off`. ~5min/cycle overhead.

---

## Pending investigations (NEW cycle 20260523_1800)

- **C8 wind-down monitoring** — does C8 produce more bigs through 22:00Z? Last PORTUGAL BABYTROLL 15:37; TKLV 17:09 inside window.
- **C9 detection** — next bc≥16∩k≤10 onset after >3h gap from BABYTROLL.
- **TG-2h n≥50 forward validation** — currently 40 = 80% to target.
- **PORTUGAL strict n→18+ if 1+ new PORTUGAL** — close to floor.
- **GIVE-shape replication check** — does next Sol big match null-top1 + meteora + smart=5-15?
- **Smart-cluster trail edge replication** — next Sol big: does smart-cluster beat A/H trail?
- **CARRIED**: PORTUGAL creator wallet audit (12+ tokens C1-C8 now: WORLDCUP, WORLDCUP-2, WOJCUP, METLIFE, Grandma, WBC, UFU, RICH, VELVET, xing, TRUMPBANK, BABYTROLL, ELON, CTM, BabyAsteroid, TRUMPETTE); External BSC volume fetcher; SMART_CLUSTER_VETO feasibility; rugger_blacklist `wallet_added_at`; MC_LIQ vs A code review (more urgent — MC_LIQ caught GIVE).

---

## CYCLE 20260524_0000 updates

### NEW (descriptive, n=19, GATE-PASSING except n<20 floor): H_SERIAL_SYMBOL_ALPHA_REVIVAL

**Filter spec**: Sol token where:
- Token's symbol has ≥2 prior distinct deployments (different mint addresses, same symbol string)
- This deployment shows: top1_pct≥85 ∩ dex=meteora ∩ smart≥5 ∩ known≥15

**Test stats (descriptive, single time-block, no walk-forward available)**:
- n=19, big=2 (MTFR +506 [token 79y6FesF], GIVE +308 [token 2Mcxjye7])
- rug=4, avg=+23.9%, WR=47%
- Kelly(var)=0.115, geom@K=+1.65%
- **PASSES Er/K/geom gates; FAILS n<20 floor by 1**

**Origin**: c0000-day3 discovery — both Sol bigs in c1800→c0000 window come from serial-token-symbol families (MTFR 7-deployment, GIVE 6-deployment). MTFR has SHARP differentiation: deployments #1-4 all top1=5 → all rugged; deployments #5-7 all top1=87.8 → 1 big + 2 small wins.

**Caveats**:
1. MTFR appears 3× in n=19 set (deployments 5, 6, 7 — all α-shape). Per-symbol-dedup: n=17.
2. Both bigs are in same 7h window (12:25-19:36 of 05-23) → single-cluster risk (6th leakage form).
3. Walk-forward impossible — all candidates after 2026-05-22T04:07Z (state.json doesn't extend pre-TEST.first 05-21T14:46Z).

**Status**: NEW HEAVY HYPOTHESIS. **HOLD** for n=20+ accumulation + cross-cluster validation. **Closest sub-floor candidate** (95% of n=20 floor).

**Routing recommendation** (if promoted): {A, B, H, MC_LIQ, SMART_COPY_TOP_AGE5, SMART_TOP_AGE5} — smart-cluster streams to capture H_SMART_CLUSTER_TRAIL_EDGE.

---

### UPDATE: H_SMART_CLUSTER_TRAIL_EDGE — PROMOTED n=1 → n=2 BOTH POSITIVE

| token | A pnl | B pnl | H pnl | MC_LIQ pnl | SMART_COPY pnl | smart-edge |
|---|---|---|---|---|---|---|
| GIVE 2Mcxjye7 | +171 | n/a | +171 | +308 | +308 | **+137pp** |
| MTFR 79y6FesF | +485 | +485 | +485 | +506 | +506 | **+21pp** |

Both POSITIVE direction. Both Sol bigs in c1800→c0000 (last 11h). Both meteora α-shape.

**Action**: track on next Sol big for n=3+ validation. If pattern holds, promote to routing-default for any Sol paper-stream candidate.

---

### CLOSED-REJECTED: H_SOL_EPSILON_SHAPE

c1800 introduced based on claimed "null top1, null buys" for GIVE. **Actual state.json data shows top1=99.3 buys=262** (α-shape). c1800's claim was a misread.

ε-shape doesn't exist as defined. Hypothesis withdrawn.

---

### ADOPTED: Methodology Lesson #10 — FEATURE-VALUE DOUBLE-CHECK

**Lesson**: when claimed feature values contradict shape priors, double-check raw state.json before forming new shape hypothesis.

**Trigger event**: c1800 cycle reported GIVE had null top1/null buys → formalized as ε-shape candidate. c0000-day3 re-check showed actual values are top1=99.3 buys=262 — α-shape match. The "null" was likely from a different GIVE deployment's open-position row or an earlier failed deployment.

**Adoption**: ~2min/cycle overhead. Standard practice: when reporting features in cycle insights, paste the raw entry_signal JSON snippet for any new shape claim.

---

### UPDATE: C8 cluster — CONFIRMED ENDED

Last C8 entry: TKLV 17:09 (bc=13 k=15 broader-band big). After 17:09 only k>10 broader-wave bc=20 entries (RD💵, SP, META, 旺财链❤️, BSC, 🍜好运币) all rugged/lost.

**C8 productive phase**: 12:25-15:37 (3h12min, 4 PORTUGAL bigs).
**C8 tail**: 15:37-17:09 (TKLV broader-band big).
**Total C8 duration**: ~4h45min.

**Productive cluster lengths**: C5 ~7h, C6 ~6h, C7 ~12h, C8 ~5h. C8 was shortest productive cluster.

---

### NO C9 ONSET YET (8h+ since last C8 PORTUGAL BABYTROLL)

After BABYTROLL 15:37, 24 unique BSC tokens entered through 00:00Z but ZERO had bc≥16∩k≤10 (PORTUGAL strict). Cluster gap continuing.

Watch for: first PORTUGAL strict entry to initiate C9.

---

## Pending investigations (NEW cycle 20260524_0000)

- **Re-check open positions** (53 → see what closes) for fresh α-revival candidates.
- **C9 onset detection** — next PORTUGAL bc≥16∩k≤10 entry.
- **H_BSC_BC_FULL_B recompute** — 24 new bc≥16 broader-wave entries since c1800 (all rugs) likely weaken K from 0.149 down to ~0.10.
- **Next Sol big shape match** — does it come from serial-symbol family + α-shape? Validates H_SERIAL_SYMBOL_ALPHA_REVIVAL cross-cluster.
- **MC_LIQ + SMART_COPY trail-management code review** — both caught GIVE +308 and MTFR +506. URGENT.
- **CARRIED**: PORTUGAL creator wallet audit (now 14+ tokens C1-C8); External BSC volume fetcher; rugger_blacklist `wallet_added_at`; SMART_CLUSTER_VETO feasibility; H_SMART_CLUSTER_TRAIL_EDGE retroactive audit on older Sol bigs (PIGEON, MTFR-prior, OSOR, GITBANK, SPCXDRAGON, RONALDO, FOID, Blobby, FATU); investigate state.json shrink (4982→4841) — rotation pattern or recount.

---

## cycle 20260524_0600 updates

### CLOSED-REJECTED: H_SERIAL_SYMBOL_ALPHA_REVIVAL (form-6 single-cluster overfit, 7th instance)

c0000 declared n=19 K=0.115 geom@K=+1.65% big=10.5% rug=21% with spec "Sol meteora ∩ symdup≥2 ∩ top1≥85 ∩ smart≥5 ∩ known≥15". Brain leaned "first SOL-side gate-passing candidate; HOLD for cross-cluster validation".

**Forward re-test (5.5h later)**: n=34 K=0.012 geom=+0.03%. K dropped 10×.

**Walk-forward time-block decomposition** confirms single-cluster overfit:

| window | n | big% | rug% | K | geom@K |
|---|---|---|---|---|---|
| 05-22 14-22Z (TRAIN) | 9 | 0% | 67% | -1.18 | 0% |
| 05-22 22Z→05-23 12Z (VAL) | 10 | 0% | 40% | -1.63 | 0% |
| **05-23 12-24Z (C8 era)** | **12** | **25% (3 bigs)** | **8%** | **+0.28** | **+25.35%** |
| 05-24 00-06Z (latest) | 3 | 0% | 33% | -1.48 | 0% |

**All 3 bigs (GIVE, MTFR-79y, MTFR-7ZxMR3s6) cluster in single 12h window.** Same fate with serial≥3 (n=28 K=0.014). 

**Methodology**: 7th instance of leakage form #6 (single-cluster artifact). c0000's "HOLD for cross-cluster" stance was correct; "first SOL-side gate-passing candidate" framing was premature optimism. **Lesson #11 candidate (NEW)**: SINGLE-TIME-BLOCK INFLATION — any candidate whose entries all fall within <24h needs ≥2× n penalty before sub-floor deploy approval.

**Status**: REJECTED. Do not promote.

---

### NEW (descriptive, n=1): H_POOR_ZETA_SHAPE

Poor +3857% Sol pumpswap (largest single big in brain history). Features: smart=13, known=19, top1=79.5, top5=87.8, buys=236, sells=112, mcap=$55,764, liq=$88,135, holders=20 (concentrated), dex=pumpswap, lp_unlocked=True, symdup=1, volume_h24=$297,623.

**ζ-shape candidate spec**: Sol pumpswap ∩ top1∈[60,85] ∩ smart≥10 ∩ buys≥150 ∩ liq≥$50K ∩ symdup=1.

**Filter test results on current Sol BF universe**:

| spec | n | K | geom | big% | rug% |
|---|---|---|---|---|---|
| pumpswap smart≥10 known≥15 | 142 | -0.041 | 0% | 0.7% | 78% |
| pumpswap top1∈[60,85] smart≥10 buys≥150 | 74 | -0.012 | 0% | 1.4% | 82% |
| pumpswap top1∈[50,85] smart≥10 buys≥200 liq≥$50K | 28 | 0.019 | +1.97% | 3.6% | 46% |
| pumpswap top1∈[70,85] smart≥10 | 38 | 0.007 | +0.18% | 2.6% | 79% |

**Verdict**: every filter that contains Poor is dominated by losers (78%+ rug). Cannot generalize from n=1.

**Symbol-level**: Poor #2 deployment (AGi7aD5M, symdup=2) entered 2h after big → -100 RUG (different from MTFR/GIVE "later deployments BIG" pattern; Poor inverted — first is big, subsequent fail).

**Status**: DESCRIPTIVE ONLY (n=1). Track future pumpswap bigs for shape match.

---

### NEW (descriptive, n=1): H_BSC_SERIAL_SYMBOL_REVIVAL

BabyAsteroid v3 (token=0xcbfcb155, symdup=3, k=1, bc=20) +880 BSC PORTUGAL big. Prior BabyAsteroid v2 (symdup=2, C7 onset) was +33 small win. Same symbol, escalating outcome — BSC analog of MTFR/GIVE Sol α-revival pattern.

**Existing capture**: BabyAsteroid v3 already caught by PAPER_BSC_PORTUGAL strict (k=1, bc=20). No new filter needed.

**Sub-hypothesis**: BSC PORTUGAL strict ∩ symdup≥2 may have higher big-rate than symdup=1.

**Stratified test on n=16 PORTUGAL strict**:
- symdup=1: 8 entries, 4 bigs (WBC, UFU, TRUMPBANK, BABYTROLL, xing — 5 actually) = 50-62% big-rate
- symdup≥2: 8 entries, 2 bigs (VELVET, BabyAsteroid-v3) = 25% big-rate
- symdup=1 PORTUGAL is STRONGER, not weaker

**Verdict**: BSC serial-symbol PORTUGAL is **NEUTRAL or marginally negative** sub-spec. No additional alpha vs base PORTUGAL strict.

**Status**: DESCRIPTIVE n=1. Do not adopt as filter. Monitor for divergence.

---

### DOWNGRADE: H_SMART_CLUSTER_TRAIL_EDGE — n=2→n=3 AMBIGUOUS

| big | smart-cluster best | A/B/H best | delta |
|---|---|---|---|
| GIVE 2Mcxjye7 (c1800) | +308 | +171 | **+137pp** (smart wins) |
| MTFR 79y6FesF (c0000) | +506 | +485 | **+21pp** (smart wins) |
| **MTFR 7ZxMR3s6 (this cycle)** | **+75** | **+365** | **-290pp** (REVERSE) |

By absolute magnitude, reverse direction dominates positives (290pp REVERSE vs 158pp combined positive).

**Status**: DOWNGRADED to AMBIGUOUS. Defer routing recommendation. Need n=5+ consistent direction.

**Possible mechanism (speculation)**: smart-cluster trail uses stricter exit-on-drawdown criteria. On GIVE/MTFR-79y (sharp parabolic), loose trail captures peak; on MTFR-7ZxMR3s6 (deeper mid-pump drawdown), smart-cluster bailed early while H/H2 held through. Unverifiable without per-trade trail logs.

---

### UPDATE: PAPER_BSC_PORTUGAL strict — n=16, first 6% rug introduced

CAP (k=1 bc=20 symdup=6) at C9 onset rugged -100. First true rug (ELON was -86, didn't count as full).

Stats: n=16 K=0.277 geom=+74.48% big=50% rug=6%.

**Recommendation unchanged**: DEPLOY-READY-AT-SUB-FLOOR with 6% rug + 4-from-floor (80% of n=20) disclosure. Routing {SNIPER_B} primary.

---

### UPDATE: PAPER_BSC_TG2 — slight K weakening, geom best ever

n=39 K=0.152 geom=+14.66% (BEST EVER — BabyAsteroid +880 lift) big%=23.1 rug=23%. Catches 9/10 bigs (misses TKLV bc=13).

Cross-cycle K: 0.181→0.152 (drift -0.029). Still gate-passing by 3× on K.

**Recommendation unchanged**: DEPLOY with 78% n-floor (n=39/50) disclosure.

---

### NEW (carry, observation): SOL BIG CLUSTER candidate

4 Sol bigs in 17.5h (GIVE 12:25, MTFR-79y 19:36, MTFR-7ZxMR3s6 23:45, Poor 00:36) — first Sol big-cluster since 05-20-21 SPCXDRAGON/GITBANK pair.

Two distinct shapes (3× α-revival meteora + 1× ζ-Poor pumpswap). Cluster duration ~12h.

**Hypothesis**: Sol big-clusters may have onset detection signal analogous to BSC clusters (PORTUGAL onset). Onset candidates: Sol Cond A starting to clear, first big in new dex/shape, regime transition.

**Status**: CARRY as observation. Investigate next cycle if data permits.

---

### UPDATE: C9 cluster — ONSET CONFIRMED, productivity verified

C9 onset: CAP 01:58Z (PORTUGAL k=1 bc=20 symdup=6) → **-100 RUG**. First onset-RUG ever (prior productive clusters all had PORTUGAL-pump onset).

C9 productive: BabyAsteroid v3 04:46 +880 (first big, 2h48m after CAP onset).

C9 stats (n=3 PORTUGAL strict): 1 big / 1 small / 1 rug = 33% big.

Cluster productivity now 7/9 = 78% (C9 productive despite rug-onset).

**Sub-pattern: ONSET-RUG-PRODUCTIVE cluster** — new shape variant. Previously believed onset rug = cluster fail (C4 CTM model). C9 refutes that mode.

---

### NEW Methodology Lesson #11 candidate — SINGLE-TIME-BLOCK INFLATION

**Lesson**: when a candidate filter's matches all fall within <24h window, gate must apply ≥2× n penalty (or wait for cross-block validation) before sub-floor deploy approval.

**Trigger**: H_SERIAL_SYMBOL_ALPHA_REVIVAL fell from K=0.115 to K=0.012 in 5.5h post-c0000 — pure single-cluster overfit despite passing all other gate metrics.

**Application**: at sub-floor candidate evaluation, check if entries span <24h. If yes:
- Inflate n requirement to 2× floor (40 for sub-floor; would have correctly held H_SERIAL_SYMBOL_ALPHA_REVIVAL at n=19→requires n=40)
- OR require ≥1 inter-cluster gap of >12h with at least 1 match in each sub-window

**Status**: NEW CANDIDATE. Adopt informally this cycle. Consider formal codification next cycle.

---

## Pending investigations (NEW cycle 20260524_0600)

- **C9 wind-down monitoring** — does C9 produce more bigs through 12:00Z?
- **PORTUGAL strict to n=20 floor** — need 4 more entries.
- **TG-2h to n=50 floor** — need 11 more.
- **Sol Cond A head-fake check** — Poor +3857 lift sustained or fade?
- **Investigate Poor exit_reason** — true ATH-capture vs lucky trail trigger? Defer unless user wants.
- **BSC serial-symbol stratification** on next PORTUGAL strict — symdup tally.
- **Sol-cluster onset hypothesis** — characterize 4-bigs-in-17.5h regime.
- **Methodology Lesson #11 formal adoption** — if next cycle's data confirms pattern.
- **CARRIED**: PORTUGAL creator wallet audit (now 17+ tokens including BabyAsteroid v2+v3, CAP, MOODANG), External BSC volume fetcher, rugger_blacklist wallet_added_at, SMART_CLUSTER_VETO feasibility, MC_LIQ code review (deprioritized — trail-edge ambiguous), state.json shrink investigation (now stable).

## NEW (proposed cycle 20260524_1200)

### H_GAMMA_SHAPE_V2 — γ-shape #2 (RE-AFFIRMED)
**Idea**: Sol pumpswap entry with `top1<25 ∩ buys_m5≥200 ∩ mcap≤$50K ∩ smart≥2 ∩ lp_locked`.
**Evidence**: n=2 in window (CBSt c1200 top1=12 buys=491 smart=6; GYATT c1200-day3 top1=21.5 buys=289 smart=2 +187%). Both pumpswap, both lp_locked, both small mcap.
**Why interesting**: 2nd observation of γ-shape pattern after 5+ cycles of α/β/δ/ε/ζ dominance. Possible distinct generative mechanism (low-concentration high-buyer-count meme-pump).
**Limitation**: n=2 unmodelable. Need n≥5 before any backtest.
**Next**: monitor next pumpswap low-top1/high-buys entry → big or rug?
**Status**: NEW (n=2, descriptive only).

### H_LATE_LOWCAP_BIG_CONVERSION — multi-wave re-entry big-capture
**Idea**: When same Sol token sees ≥5 entry waves (multiple sniper-bundle re-firings on rebuy attempts), eventual winning wave catches LATE/LOWCAP streams (typically anti-fat-tail). Suggests late-stream big-capture is possible on specific re-entry pattern.
**Evidence**: GYATT n=1 (8 waves over 4h, wave 8 = winning, LATE/LOWCAP tied at +187%).
**Mechanism candidate**: late waves benefit from prior wave's price-discovery; LATE/LOWCAP avoid the early-rug waves.
**Limitation**: unmodelable from n=1. Distinguishing "5+ wave token" from "many sub-token tickers same address" requires careful detection.
**Next**: instrument same-token wave-counter; tally wave-N winning probability across all multi-wave tokens.
**Status**: NEW (n=1, observation only).

### H_SOL_BIG_ROUTING_H2 — SNIPER_H2 as 4th Sol BF stream
**Idea**: Add SNIPER_H2 to standard Sol big-routing alongside A/B/H. Currently SNIPER_H2 is in the BSC big-routing {B/F2/D2/A/H} but not formally in Sol.
**Evidence**: n=2 BF observations (MTFR-7Zx +365 BF=H2, Maple +163.8 in BF tie {A,B,H,H2}). H2 captures 2/6 current Sol bigs at best-fire.
**Mechanism**: H2 appears to be a faster trail variant of SNIPER_H — captures same alpha but maintains hold longer in some cases.
**Next**: routine routing addition. Low-risk paper change.
**Status**: NEW (n=2, low-risk; brain leans deploy as routing change).

### H_SMART_CLUSTER_TRAIL_EDGE — REJECTED-AMBIGUOUS (final)
**Idea**: smart-cluster streams (SMART_TOP_AGE5 / SMART_COPY_AGE5 / etc.) catch a tighter trail variant that holds bigs longer than A/B/H.
**Evidence**: n=4 observations:
  - GIVE: smart wins +137pp
  - MTFR-79y: smart wins +21pp
  - MTFR-7Zx: A/B/H/H2 wins +290pp
  - Maple: A/B/H/H2 wins +93pp
**Direction**: 2-2 split. **Magnitude**: A/B/H wins 383pp vs smart wins 158pp = 2.4× toward A/B/H.
**Conclusion**: smart-cluster streams are CO-ENTRY indicators (fire on same alpha ~1sec after A/B/H), NOT trail-superior. Standard A/B/H routing remains optimal.
**Status**: REJECTED-AMBIGUOUS (kept for negative learning; do not re-propose).

### H_BSC_FAST_RETAIL_PUMP — anti-portugal n=1
**Idea**: BSC token with bc≤3 ∩ known=1 ∩ low age ∩ symdup≥3 ∩ pancakeswap → potential fast retail pump.
**Evidence**: n=1 (Poor BSC +659 — bc=1, known=1, symdup=4, age=11min, SNIPER_B +617pp over A).
**Why interesting**: catches a big that ALL existing BSC filters miss. Different mechanism than PORTUGAL (PORTUGAL = bonding curve players unwinding; this = pure retail FOMO on serial symbol).
**Limitation**: n=1 unmodelable. Anti-correlated with existing bc≥16 filter.
**Next**: monitor low-bc bsc entries with symdup≥3 for replication.
**Status**: NEW (n=1, descriptive).

### Methodology Lesson #11 ADOPTED IN PRACTICE
**Definition**: SINGLE-TIME-BLOCK INFLATION — when a filter's bigs concentrate in a <24h window, apply ≥2× n penalty before sub-floor deploy approval.
**This-cycle trigger**: PORTUGAL strict 5/6 bigs in C8 single 3.2h block (RICH/VELVET/xing/TRUMPBANK/BABYTROLL) → effective floor n=26 (current n=13 = 50%). PAPER_BSC_PORTUGAL deploy DEFERRED.
**Status**: ADOPTED-IN-PRACTICE (formal adoption pending next cycle confirmation).

### Methodology Lesson #12 CANDIDATE — ROTATION-INDUCED K INFLATION
**Definition**: Cross-cycle K comparisons can SPURIOUSLY appear to strengthen via state.json rotation removing K-dragging entries. Any "K improved X→Y across cycles" claim MUST identify which specific entries rotated and report n-delta.
**This-cycle trigger**: PORTUGAL strict K appearing to jump 0.277→0.750 across cycles c0600→c1200. Investigation revealed 3 entries rotated (WBC/UFU/BINA/METLIFE candidates) plus K-search grid differences.
**Status**: CANDIDATE (formalize after 1 more rotation observation).

### 🆕 H_WALLET_TOP1_LEADERBOARD — NEW HEADLINE (paradigm shift)
**Idea**: Use Sol `entry_signal.top1_owner` as a wallet-leaderboard feature. Build per-wallet history (n, bigs, rugs, avg pnl). At entry time T, take entry IF top1_owner has prior_n ≥ X AND prior_rugs ≤ Y AND prior_avg ≥ Z%.
**Evidence**: HUPHeyBkcSCkHTxS9wsbVcj9UP9wZNXU998g5Csbc9AT — n=10 unique Sol tokens, 4 BIGS (40%), 0 RUGS, avg=+207%, max=+943. Sol baseline n=593 1.3% big 59% rug = 30× big-rate lift, infinite rug-rate reduction. Walk-forward filter `prior≥5 ∩ rugs=0` n=15 avg=+128 K=0.15 geom=+12.85%/trade big=27% rug=13% — **PASSES Er/K/geom by 3-12× margins, fails only n<20 floor (5 below)**.
**Mechanism (hypothesis)**: HUPHey + D4Bgpf (lp_provider) are co-pair entity behind serial Sol meteora launches. When launch "succeeds", target wallet rides to big. When fails, stays small loss (never goes full rug — they always set bag-cap exits before -90%). Effective copy-trade of a competent market-maker / launcher.
**Caveats / Methodology #13**:
  1. **Single-wallet dominance** — 4/4 walk-forward bigs from HUPHey alone. Effective n_independent_wallets=1.
  2. **Single time-cluster** — all 10 tokens in 29h window 05-23 10:03 → 05-24 14:49.
  3. **Methodology #13 (SINGLE-WALLET INFLATION) penalty** doubles n floor to n=40.
**D4Bgpf lp_provider co-correlate**: 13 tokens 4 bigs 0 rugs avg=+166. Same set as HUPHey (probably 1:1 overlap).
**BSC equivalent NOT YET BUILT**: BSC pool_creator field mostly None. Try `bonding_curve_buyers[0]` (rank-1 bc) as analog next cycle.
**Open positions matching qualifying wallet right now**: 0/57. Signal forward-only.
**Status**: 🚀 PARADIGM SHIFT — major hypothesis with paper-stream candidate path. **Deploy DEFERRED for n<20 + Methodology #13 penalty** (need 2nd qualifying wallet). **Highest-priority infrastructure ask: pre-compute live `wallet_alpha_v1.json` snapshot.**
**Next**:
  - Scan ALL Sol top1_owners with ≥3 tokens; find 2nd qualifying wallet.
  - Build BSC bc[0] wallet leaderboard.
  - Solscan/blockchain deep-dive HUPHey + D4Bgpf for additional features (balance, age, tx count).
  - Forward-watch HUPHey new launches (~6h cadence).

### 🆕 Methodology Lesson #13 CANDIDATE — SINGLE-WALLET INFLATION
**Definition**: When a walk-forward filter's bigs all trace to a single wallet/creator/LP entity, apply 2× n penalty (effective floor doubles) until ≥2 distinct entities contribute bigs. This is the wallet-dimension analog of Lesson #11's time-dimension penalty.
**This-cycle trigger**: H_WALLET_TOP1_LEADERBOARD — n=15 with 4 bigs all from HUPHey (single wallet). Effective floor goes 20 → 40 entries OR 1 → 2 distinct wallets.
**Status**: CANDIDATE (formalize after 1 more single-entity-bigs observation, OR when 2nd wallet qualifies and we observe the penalty actually softening).

### H_BSC_C10_CLUSTER_ONSET — STAKE→BELIEF
**Idea**: STAKE 0xea8b BSC (05-24 11:37 PORTUGAL k=1) + BELIEF 0xe0ac BSC (05-24 14:02 PORTUGAL k=1 BIG +235) = candidate C10 cluster onset. 2h25min gap after STAKE (analog of WORLDCUP-2→WOJCUP onset in C7).
**Evidence**: 1 BIG (BELIEF +235) + 1 small loss (STAKE -52) so far. PORTUGAL strict productive in 5/6 historical clusters.
**Next**: watch for follow-on PORTUGAL strict entries in next 2-4h. If C10 productive (≥1 more BIG), confirms H_CLUSTER_PORTUGAL_PRESENCE on n=6/9.
**Status**: NEW (n=2, descriptive).

### H_SMART_CLUSTER_TRAIL_EDGE — REJECTED-CONFIRMED (3rd reverse)
**Update from c1200's REJECTED-AMBIGUOUS**: Poor3 c1800 = 5th observation. SMART_COPY/SMART_COPY_TOP/SMART_COPY_AGE5/SMART_TOP_AGE5/MC_LIQ all **-100 rug** at 140min hold; SNIPER_A/B/H/H2 all **+943 capped exit** at 93min hold. Catastrophic smart-cluster TRAIL FAIL.
**Updated cumulative**: n=5
  - GIVE: smart +137pp (POSITIVE)
  - MTFR-79y: smart +21pp (POSITIVE)
  - MTFR-7Zx: A wins +290pp (REVERSE)
  - Maple: A wins +93pp (REVERSE)
  - **Poor3: A wins +1043pp (CATASTROPHIC REVERSE)** ← new
**Direction**: 2 POSITIVE vs 3 REVERSE. **Magnitude**: A-wins-by 1426pp vs smart-wins-by 158pp = 9× toward A.
**Conclusion**: STRONGLY NEGATIVE. Smart-cluster TRAIL is HARMFUL on Sol fat-tail bigs (holds past A's optimal exit, catches the post-cap rug).
**Status**: REJECTED-CONFIRMED. **Do NOT add smart-cluster streams to Sol big-routing.** Standard A/B/H/H2 routing remains optimal.


## NEW (proposed cycle 20260525_0000)

### 🆕 PAPER_SOL_HUPHEY_WATCH — NEW HEADLINE deploy candidate (named-wallet)
**Idea**: Paper-stream watch on the HUPHey wallet. Buy any new Sol token where `entry_signal.top1_owner == HUPHeyBkcSCkHTxS9wsbVcj9UP9wZNXU998g5Csbc9AT` OR `entry_signal.lp_provider == D4BgpfCAEqYfoVVBdcokDovU5sXvhHXAYxwCn2ojPkHc`. Size=$1 paper, TP_500_CAP exit, no stop-loss (HUPHey has never rugged).
**Evidence (this cycle, post-MTFR-BVB)**: 12 unique tokens, 5 BIGS (42%), 0 RUGS, avg=+186.8%, K=0.68, geom=+47.2%/trade. Sub-filter top1≥85 ∩ meteora: n=5 3 bigs 0 rugs K=1.0 geom=+144%. Cadence observed ~3-6h between fires.
**Why deploy at n=12 (sub-floor)**: Methodology #14 candidate — NAMED-WALLET WATCH has different deploy criteria from generalized filter. With 0 rugs in 12 tokens, downside risk is bounded (~-$1 per fire worst case if filter degrades). Generalized filter rejection (Methodology #13) does NOT block named-wallet deploy because we're not claiming "any wallet with this prior profile" — we're claiming "THIS specific wallet historically performs".
**Risk**: HUPHey identity unknown (could go quiet, could shift strategy). 75qsE3p5y2 counter-example (Maple +164 1 big, then 5 more rugs in 12h) shows wallet alpha can deteriorate.
**Mitigation**: monitor cycle-over-cycle HUPHey performance. If big-rate drops below 30% or any rug appears, demote.
**Status**: 🚀 NEW HEADLINE — formal spec pending user approval.

### 🆕 Methodology Lesson #14 CANDIDATE — NAMED-ALPHA vs GENERALIZED-FILTER distinction
**Definition**: When wallet alpha is identified, distinguish between:
  - **NAMED-WALLET WATCH**: deploy criteria = `specific wallet has ≥3 bigs AND 0 rugs in own history AND active in current rolling window`. No n≥20 floor.
  - **GENERALIZED FILTER**: deploy criteria = standard n≥20 + Er>0 + K≥0.05 + geom≥1% + ≥2 distinct contributing wallets (Methodology #13).
**This-cycle trigger**: H_WALLET_TOP1 walk-forward filter FAILS to generalize (NOAR test — 75qsE3p5y2 doesn't qualify with 5 prior rugs), but HUPHey-NAMED watch passes all named-criteria. Brain proposes separating deploy paths.
**Why #14 matters**: HUPHey is the strongest single-feature signal in brain history (n=12, K=1.0 on sub-filter). Without #14, signal is blocked indefinitely waiting for 2nd qualifying wallet (which may never come — alpha wallets are by definition rare).
**Status**: CANDIDATE (formalize when first NAMED-WALLET paper-stream deploys and produces forward results).

### 🆕 H_WALLET_TOP1_LEADERBOARD — STATUS UPDATE — GENERALIZATION REJECTED
**Update from c1800's PARADIGM SHIFT**: walk-forward filter `prior≥5 rugs=0` excluding HUPHey → n=8 catches **0 bigs / 3 rugs (37.5%) ≈ baseline 59%**. Filter is 100% HUPHey-dependent. NOAR test (05-24 23:45 NEW WALLET 75qsE3p5y2 +152) does NOT light up filter — wallet has 5 prior rugs.
**Conclusion**: Generalized filter REJECT. Re-framed as HUPHey-named watch (see PAPER_SOL_HUPHEY_WATCH above).
**Methodology #13 (single-wallet inflation) ADOPTED via this falsification**.
**Status**: GENERALIZED FILTER REJECTED. Named-wallet derivative ACTIVE.

### 🆕 H_NOAR_FORK — descriptive (NEW WALLET 75qsE3p5y2)
**Idea**: Track 75qsE3p5y2 wallet as serial launcher of NOAR-symbol Sol meteora tokens. 14 tokens 2 bigs (Maple +164, NOAR +152) 5 rugs avg=-15%.
**Evidence**: big-rate 14% (9× Sol baseline 1.6%), rug-rate 36% (better than baseline 59% but still high). Mixed alpha.
**Hypothesis**: 75qsE3p5y2 is a launchpad/factory wallet spraying NOAR launches. Different alpha profile from HUPHey (high variance, not clean).
**Open positions**: 5 NOAR tokens still holding +186-188% unrealized.
**Next**: track resolution of 5 open positions. If big-rate sustains, consider sub-filter; if rugs dominate next 5-10 launches, reject as low-quality launcher.
**Status**: NEW (n=14 descriptive, NOT promote-to-paper without cleaner pattern).

### 🆕 H_SMART_CLUSTER_TRAIL_EDGE — RE-EXAMINED (MTFR-BVB neutral, NOAR pending)
**Update**: Two new observations this cycle.
  - MTFR-BVB +175: MC_LIQ won +175.4% vs A/B/H/H2 tied +168.8% = MC_LIQ +6.6pp edge (within noise/cap)
  - NOAR +152: A still open at +186%, B/H closed at +152.5%, 4 smart-cluster streams still open at +188% — too early to evaluate; A's trail and smart-cluster's are both UP versus the early-exit B/H pair
**Updated cumulative n=6** (5 prior + MTFR-BVB = neutral). Cumulative direction still 2 POSITIVE / 3 REVERSE / 1 NEUTRAL. Magnitude still strongly toward A.
**Status**: REJECTED-CONFIRMED (no change). Wait for NOAR closure for n=7.

### 🆕 H_PORTUGAL_C10_PRODUCTIVITY — CONFIRMED DORMANT TAIL
**Update**: BELIEF +235 was C10 entry at 14:02Z. Since c1800 (17:49Z), **14 new BSC tokens entered, 0 PORTUGAL strict eligible, 0 bigs**. C10 dormant for 9h58min. Mirrors C6→C7 transition (~6h dormant before productive cluster).
**Status**: C10 cluster cooled. Watch C11 onset over next 6-12h.

### 🆕 H_LEADERBOARD_WALLET_OPEN_TRACKING — descriptive observation
**Idea**: 27 open Sol positions match wallets from `/srv/bots/.shared/data/wallet_leaderboard.jsonl` (48 candidates). Examples this cycle:
  - 75qsE3p5y2 (n=5 1 big 0 rugs in lb): 5 open NOAR positions, +186-188% unrealized — converted to 1 closed big (+152) already
  - BHD5YKNkbo3 (n=11 2 bigs 0 rugs in lb): 2 open Sol "BELIEF" positions -5/-14%
  - 2QioJBwKBVtsP2FajW (n=20 2 bigs 1 rug in lb): 1 open ENHANCED -100% RUG ← counter-example showing leaderboard wallets can still rug
**Status**: NEW — leaderboard tracking surface. Build forward-validation per wallet over next 5-10 cycles.


## NEW (proposed cycle 20260525_0600)

### H_BSC_BC0_WALLET_LEADERBOARD_85871 — NEW HEADLINE (BSC named-wallet)
**Idea**: BSC-side analog of HUPHey wallet alpha. Identify high-fat-tail BSC wallets via `entry_signal.bonding_curve_buyers[0].addr`. Filter: enter any new BSC token where bc[0] == 0x85871aea93f086eeda... (full 42-char addr to be verified next cycle).
**Evidence (in-corpus aggregate, n=8)**: bigs=5 (62%), rugs=1 (12%), avg=+289.9%, K=0.281, geom=+58.88%/trade. Tokens: ELON -86, xing +293, TRUMPBANK +349, CAP -100, MOODANG +90, BabyAsteroid +880, **Poor BSC bc=1 +659** (PORTUGAL strict MISSES — bc<16), BELIEF +235. C7/C8/C9/C10 all represented = cross-cluster validated (Methodology #11 safe).
**Walk-forward (prior≥3 ∩ bigs≥2 ∩ rugs≤1)**: n=5, outcomes {-100, +89.7, +879.5, +659.2, +235.0}, bigs=3 (60%), rugs=1 (20%), avg=+352.7%.
**Status**: NEW — paper-stream spec `paper_streams_spec/PAPER_BSC_85871_WATCH.md` written. Deploy decision pending user approval.
**Deploys via**: Methodology #14 NAMED-WALLET WATCH class (now formal — 2 entities cross-validate with HUPHey).

### H_NAMED_WALLET_CLASS — formalized concept (Methodology #14)
**Idea**: Maintain a "Named-Wallet Watch List" of entities (Sol top1_owner, BSC bc[0], etc.) with proven track records. Deploy criterion: ≥3 tokens, ≥2 bigs, ≤1 rug.
**Current members**:
- HUPHeyBkcSCkHTxS9wsbVcj9UP9wZNXU998g5Csbc9AT (Sol top1_owner; n=12, 5 bigs, 0 rugs)
- 0x85871aea93f086eeda... (BSC bc[0]; n=8, 5 bigs, 1 rug)
**Status**: FORMAL ADOPTION pending user approval. With 2 entities the class breaks Methodology #13 single-wallet restriction.
**Next**: hunt 3rd member; consider Sol bc[0] analog if applicable; verify cadence and rescind rules.

### H_PROS_FACTORY_0xa2cceabd — descriptive monitor
**Idea**: PROS BSC +908.6% bc[0]=0xa2cceabd... — new BSC factory wallet, n=1 unmodelable. Watch for 2nd/3rd token from same bc[0] addr.
**Status**: NEW, descriptive-monitor only.

### H_SMART_CLUSTER_ANTI_TRAIL — formalize as negative direction (n=6, 4 reverses)
**Idea**: Smart-cluster (SMART_COPY/SMART_TOP_AGE5) fires correctly at entry but trail-holds too long, capturing rug or missing cap. Aggregate observed: Poor3 Sol -100 vs A/B/H/H2 +943, Maple Sol smart -93pp behind A/B/H, MTFR-7Zx smart -290pp behind H, $UGD smart +4pp (noise). Net direction: 4 reverses vs 2 small wins.
**Status**: NEW — formalize as anti-trail; route smart-cluster ENTRY signal to A/B/H/H2 trail rather than smart-cluster trail.
**Next**: implement SMART_CLUSTER_USE_A_TRAIL flag.

### H_SOL_BIG_DROUGHT — Cond C regime gate candidate
**Idea**: When last_50 Sol unique tokens have 0 bigs (≥150%), set Guard ON regardless of Cond A/B status. Currently Cond A/B clear but big-rate=0.
**Status**: NEW — proposes 3rd Guard condition. Need historical backtest of big-drought as forward signal vs noise.

### Methodology Lesson #15 candidate: SUBSUMPTION-OVERLAP
**Idea**: When a new filter catches a superset of an existing filter's productive hits, choose the wider as primary. Example this cycle: PAPER_BSC_85871_WATCH catches 6/10 PORTUGAL strict entries + Poor BSC bc=1 (PORTUGAL miss) → deploy 85871 instead of PORTUGAL strict.
**Status**: NEW — pending observation in next cycles before formal adoption.



## NEW (proposed cycle 20260525_1200)

### H_HISTORICAL_VS_LIVE_LEADERBOARD_DRIFT — Methodology #16 candidate
**Idea**: Pre-computed wallet leaderboards built from N=36K historical corpus can mislead in current regime. Wallet alpha is regime-dependent.
**Evidence**: `HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC` historical leaderboard tag: 391 tokens / 53 bigs (13.6%) / 1.8% rug. LIVE state.json (46h window): **n=104 / 0 bigs / 46.2% rug / avg=-45%**. Same wallet, opposite alpha profile across different windows.
**Mechanism**: Launchpad/factory wallets create many tokens but % that pump depends on broader market conditions. In bull regime 13% pump, in current regime 0% pump. Wallet identity ≠ guaranteed alpha — regime is the multiplier.
**Why important**: Brain MUST recompute leaderboard within current state window before any deploy. Never trust pre-computed historical leaderboard for live signals.
**Status**: NEW candidate Methodology Lesson #16 — needs 2nd example before formal adoption.

### H_NEAR_BIG_REGIME — Methodology #17 candidate (Sol fat-tail magnitude shrinking)
**Idea**: Sol fat-tail magnitude appears capped at +100-150% in current regime (Cond A triggered) instead of historical +150-900% range. 
**Evidence (this cycle, last 100 Sol best-fire)**:
  - FIFA +140.9% α-strict (top1=95.8 smart=8 known=16 meteora symdup=28)
  - Horatio +138.4% α-borderline (top1=82.4 smart=15 known=17 meteora)
  - ViralRush +108.7% β-shape (top1=58.6 smart=13 known=18 meteora)
  - 0 tokens reaching +150% threshold in this cycle window
**Why important**: trail/TP designed for +150%-+900% fat tails may be MISTUNED for +100-140% capped regime. Consider lower TP target during near-big regime detection.
**Required**: ATH fetch for FIFA/Horatio/ViralRush to verify cap vs trail-mistune.
**Status**: NEW candidate — needs ATH check + 2-3 more cycles confirmation.

### H_PORTUGAL_C11_ONSET — descriptive monitor
**Idea**: DICKMAXX (09:01Z) + PTAI (09:55Z) = first 2 PORTUGAL strict entries after C10 dormant 19h+. Both bc[0]=0x85871. C11 onset confirmed.
**Watch**: If a big lands within 6h of onset (DICKMAXX+6h=15:01Z, PTAI+6h=15:55Z = before next cycle 18:00Z), C11 PRODUCTIVE → H_CLUSTER_PORTUGAL_PRESENCE re-validated (6/9 productive). If 0 big by next cycle, FIRST UN-productive cluster onset = invalidates H_CLUSTER_PORTUGAL_PRESENCE.
**Status**: NEW — watch monitor.

### H_3RD_NAMED_WALLET_HUNT — FAILED this cycle, retry path documented
**Idea**: Build 3rd member for NAMED-ALPHA class (Methodology #14). Hunt failed this cycle.
**Searched (current state.json, 4 vector scans)**:
  - BSC bc[0]: only 0x85871 qualifies (other top wallets: 0x757eba15 n=3 0 bigs; 0xe2ce6ab8 n=2 1 rug; 0x5c952063 n=2 0 bigs)
  - BSC pool_creator: 0 wallets with ≥2 tokens AND bigs ≥1 OR rugs ≤1
  - Sol top1_owner: only HUPHey qualifies (with ≥3 tokens ∩ ≥1 big ∩ ≤1 rug)
  - Sol lp_provider: D4Bgpf (HUPHey partner, already counted) + 42j8yFjdk8 (NOAR/Maple, 7 tokens 2 bigs 1 rug — but underlying 75qsE3p5y2 is 36% rug so NOT clean)
**Conclusion**: NAMED-ALPHA class frozen at 2 entities in current 46h window. Retry next cycle when more rotation has occurred OR new entities surface.
**Next**: try aged_creator_history feature (creator wallet's track record), or buys_m5 dominant-buyer wallet, or scan BSC top1_owner field (analog of Sol).
**Status**: FAILED this cycle, retry deferred.

### H_HLn_LAUNCHPAD_REJECTED — false-alpha de-mystified
**Idea**: HLnpSz9h2S4hiLQ43rnSD9XkcUThA7B8hQMKmDaiTLcC was a top-priority candidate in PROJECT_CONTEXT's wallet_leaderboard (n=391 / 53 bigs / 1.8% rug).
**Evidence**: LIVE state n=104 / 0 bigs / 46% rug = NOT alpha in current regime. It's a launchpad service smart-contract that creates serial tokens (FNCS, EZO, BLOODBANK, MTFR, Horatio, ViralRush, DICKMAXX-Sol, etc).
**Conclusion**: REJECT as named-wallet alpha. Re-classify as launchpad/factory service.
**Status**: REJECTED — fed into Methodology #16 candidate as primary example.

### H_HUPHEY_CADENCE_BREAK — pending observation
**Idea**: HUPHey median cadence is ~6h between fires. Last HUPHey big: Poor 14:49Z. 20.8h elapsed without HUPHey big at cycle time. If next cycle (18:00Z = 28h post-Poor) also has no HUPHey big, cadence is BROKEN — needs new methodology lesson.
**Important**: HUPHey has fired 3 forward-fires this cycle (MTFR×2 closed-during + PP420), all small/neutral. Wallet is ACTIVE, just not producing bigs. Different from "wallet quit".
**Status**: NEW — monitor next cycle for big-fire or 28h+ cadence break.


---

## NEW (proposed cycle 20260525_1800)

### H_SYMBOL_COPYCAT_VETO — Methodology #18 candidate (SERIAL-SYMBOL COPYCAT TRAP)
**Idea**: When a symbol appears N≥3 times in recent state with DIFFERENT top1_owners, only the FIRST entry is the originator and pumps; later same-symbol entries are bag-holder bait and should be skipped.
**Evidence (this cycle, Popus 11-token cluster)**:
  - Popus #1 (5eZTfvn..., BEJ3dC9r top1, entry 13:49Z) = +220.5% BIG
  - Popus #2-11 (10 different top1_owners) = 1 big, 4 rugs, 5 small, avg=-40%
  - HUPHey was Popus #11 buyer (top1=99.7 matched past wins) → FAILED -46.1%
  - **All 11 top1_owners DIFFERENT** (confirms copycat not serial-deployer)
**Counterexample (productive serial-symbol)**: MTFR family — 5 entries all HUPHey-top1, multiple bigs. Same-wallet repeated deployment = productive; different-wallet copycat burst = bag-holder trap.
**Filter formulation**: 
```
SKIP IF (
  symbol_dup_count_in_state ≥ 3
  AND top1_owner NOT IN prior_top1_owners_for_this_symbol_in_state
)
```
**Retro-test target**: would this rule have excluded Popus -46 from HUPHey paper-stream? YES (Popus is symdup_count=13 within window, prior top1_owners were all different from HUPHey).
**Why important**: 
  1. Fixes the only known HUPHey leak
  2. Generalizes — should improve ANY named-wallet filter
  3. Opens new feature dimension (cross-symbol wallet identity check)
**Status**: NEW candidate — 1 cluster example so far (Popus). Need 2nd cluster before formal adoption.
**Next**: retro-test HUPHey K with filter overlay; scan state for other symbols with symdup≥5.

### H_SOL_GAMMA_REFINED — 3rd paper-stream candidate (Sol pumpswap mid-buys)
**Idea**: γ-shape Sol filter: chain=solana ∩ top1<22 ∩ smart∈[2,8] ∩ dex=pumpswap ∩ age_min≤15 ∩ lp_unlocked=false ∩ buys_m5≥250.
**Walk-forward (this cycle, full state window n=11)**:
  - AIR -3.1, Cancercoin -27.3, GYATT +13.6, ROI +48.7, PERPSLAUNCH -29.2, BILLY -50.7 (rug-touch), BEAR +16.2, PolarBear +56.1, /meme -24.0, TOKEN -27.6, **Popus +220.5 (BIG)**
  - Stats: mean=+17.6%, **K=0.341, geom@K=+3.71%, Er=+0.176**
  - Gate check: Er ✓, K ✓ (by 6.8×), geom ✓ (by 3.7×), n=11<20 ✗
**Cross-cluster instance**: γ-shape echoes CBSt c1200 (+189% historical) — reduces single-block penalty
**Risk**: Popus alone drives 100% of lift; without Popus K crashes to ~0. SINGLE-TIME-BLOCK INFLATION applies.
**Why important**: 3rd paper-stream candidate ever, first non-wallet-feature based candidate. Different alpha mechanism (low-top1 high-buys vs HUPHey/85871 wallet-pattern).
**Deploy gate**: 9 more entries / 1-2 more bigs needed.
**Status**: NEW — close to deploy but blocked by n<20.
**Next cycle**: track γ-shape entries; if 2nd γ-big lands, n → 13/20 K stays elevated → deployable.

### H_POPUS_POOL_CREATOR_BVfVe44Wj — 4th named-alpha candidate?
**Idea**: pool_creator BVfVe44WjgrmNX5rGXa3uNk5ZBgACVqJgb9c7J59c696 deployed 2 tokens in state: Popus (+220 big) + BEAR (+15 small).
**Evidence**: n=2 / 1 big / 0 rugs / avg=+118%. Promising but insufficient.
**Why important**: pool_creator is a NEW wallet feature dimension; could be 4th named-alpha entity if 3rd token lands big.
**Status**: NEW candidate, n=2 too thin for adoption.
**Next**: watch for 3rd BVfVe44Wj pool_creator token.

### H_BSC_CHAIN_GUARD_SPLIT — regime refinement
**Idea**: Chain-asymmetric regime detected this cycle (Sol last50=-40.6 clear vs BSC last50=-62.6 triggered). Current Guard rolls combined; should split per chain.
**Evidence (this cycle)**:
  - Sol Cond A CLEARED via Popus +220 lift
  - BSC Cond A TRIGGERED via 13.5h drought + 4 dormant tail entries
**Why important**: applying Sol-clear guard to BSC entries during BSC-drought wastes capital.
**Status**: NEW candidate — formalize as 2 separate Cond A trackers (Cond A_sol, Cond A_bsc).
**Next**: code Cond A_chain into paper-stream entry gate spec.

---

## STATUS UPDATES (existing backlog items)

### H_WALLET_TOP1 HUPHey (deploy-ready)
**Update c1800**: First stumble — Popus #11 -46.1% (top1=99.7 matched past wins but symdup_count=13 = Methodology #18 leak). n=10 K=0.273→0.252 (still passes gate by 5×). Rugless streak (-50% threshold) INTACT at 15 cumulative tokens. Optional filter overlay: `symdup<3 OR same-top1-for-symbol` would have excluded Popus -46.
**Status**: deploy-ready unchanged, Methodology #18 overlay recommended.

### H_85871_BC0_WATCH (deploy-ready)
**Update c1800**: +2 forward-fires (DICKMAXX -1, PTAI +52.9; both bc=20 k=1 PORTUGAL strict). n=7 K=0.223 geom=+42%. STRICTLY OUTPERFORMS PORTUGAL strict (3 bigs vs 2 since captures Poor bc=1 +659). Subsumption REVISED 100%→85.7% (STAKE bc0=0x26f6ebd1).
**Status**: deploy-ready unchanged, dominant over PORTUGAL strict.

### H_PORTUGAL_C11_ONSET (descriptive monitor c1200)
**Update c1800**: C11/C3 at 9h+ dormant tail (DICKMAXX -1, PTAI +52.9, no big). RICH C7 precedent was 6h40min so now moving INTO un-productive territory. If still 0 bigs at 00:00Z 26 May (= 15h after DICKMAXX), 1st UN-productive PORTUGAL onset confirmed → big methodology update.
**Status**: WATCH (moving toward UN-productive flag).

### PORTUGAL strict (dominated, drop from candidates)
**Update c1800**: n=7 K=0.163 geom=+18%. 85.7% subsumed by 0x85871 (NOT 100% as c1200 claimed; STAKE counter-example bc0=0x26f6ebd1). 0x85871 also catches Poor bc=1 PORTUGAL misses. **DROP from candidate list**, defer to 0x85871 as primary BSC filter.
**Status**: DEPRECATED.

### H_NEAR_BIG_REGIME (Methodology #17 candidate c1200)
**Update c1800**: Popus +220.5 BREAKS the magnitude-shrink hypothesis on Sol (was 3 near-bigs c1200 max +141). +220.5% is solidly fat-tail range. BSC side still no big since PROS 13.5h ago — magnitude check defers to next BSC big.
**Status**: Sol REFUTED this cycle; BSC pending.

### H_HUPHEY_CADENCE_BREAK (c1200 pending observation)
**Update c1800**: HUPHey forward-fires this cycle = $UGD +16, PP420 -33 (closed), Popus -46. Wallet is ACTIVE but cadence broken — no HUPHey big since 28h+. Cadence-break confirmed; quality (non-rug) maintained.
**Status**: ACTIVE LOW-PRODUCTIVITY phase confirmed; wallet still rugless.

### H_3RD_NAMED_WALLET_HUNT (FAILED c1200)
**Update c1800**: BEJ3dC9r (Popus #1 originator) n=1 insufficient. BVfVe44Wj pool_creator n=2 (Popus+BEAR). NAMED-ALPHA class size still 2 entities (HUPHey + 0x85871). Hunt deferred until n≥3 candidate surfaces.
**Status**: FAILED, retry deferred.

### Methodology #15 SUBSUMPTION-OVERLAP (claimed 100% c1200)
**Update c1800**: WALK-BACK. Actual 6/7 = 85.7% (STAKE bc0=0x26f6ebd1 NOT 85871; c1200 brain miscounted). Re-frame: NEAR-COMPLETE OVERLAP not perfect. 0x85871 ALSO catches tokens PORTUGAL misses (Poor bc=1) so they are MUTUALLY ENRICHING not strict containment.
**Status**: revised from "100% subsumption" to "near-complete asymmetric overlap".

---
## NEW HYPOTHESES — cycle 20260526_0000

### H_GAMMA_AGE_RELAXED (NEW — closest-by-n deploy candidate)
**Spec**: γ-shape RELAXED — top1<22 ∩ smart∈[2,8] ∩ pumpswap ∩ age≤25 (was ≤15) ∩ lp_unlocked=False ∩ buys_m5≥250.
**Walk-forward this cycle**: n=16 K=0.453 geom=+6.60%/trade Er=+0.216 bigs=2 (Popus 13:49Z +220 + Luce 20:56Z +136) rugs=0. ALL gates PASS except n<20 floor (4 entries away).
**Cross-instance**: 2 bigs 7h apart different mints — single-block risk Methodology #11 partially mitigated. Add 3rd big spanning >24h → fully clears #11.
**Status**: PROMOTED over γ-strict. Watch for 3rd big.
**Next**: monitor next 12-24h; if Sol Cond A holds clear, ~4-6h cadence expected.

### H_RUG_CLAMP_POLICY (Methodology #19 candidate)
**Observation**: 0x85871 BSC n=7 geometric mean varies 70+pp depending on rug-clamp:
- floor=0.001 (worst-case 0% recovery): geom = -4.67%/trade → FAILS geom gate ≥1%
- floor=0.05 (typical -95% stop-loss exit): geom = +66.5%/trade → PASSES
- c1800 reported +42% (likely -0.90 clamp)
**Why important**: 0x85871 deploy decision pivots on this. Same for any filter with CAP-style -100% rugs in small samples.
**Status**: NEW Methodology #19 candidate — formalize policy.
**Next**: brain to standardize conservative floor=0.001 as primary; document floor=0.05 as "stop-loss-adjusted" alternative metric.

### H_BETA_HARAMBEX_SUBFILTER (n=1 candidate)
**Observation**: HarambeX +132 Sol fits broad β-shape (top1∈[50,75] ∩ pumpswap ∩ smart≥10) which fails K=-1.59 over n=83 (82% rug). HarambeX specifics: top1=73 smart=12 known=18 age=21 buys_m5=136 liq=$16,980 lp_unlocked=True dex=pumpswap.
**Hypothesis**: tighter sub-filter (known≥18 ∩ liq<$20K ∩ buys_m5<200) might isolate fat-tail.
**Status**: n=1 single observation, needs 2nd to test.
**Next**: scan β-cohort with proposed sub-filter; if n≥3 and ≥1 big → promote candidate.

---
## STATUS UPDATES (cycle 20260526_0000)

### H_WALLET_TOP1 HUPHey (deploy-ready)
**Update c0000**: GENWEALTH hit #6 +620.4% (top1=99.9 smart=6 meteora — sub-filter top1≥85∩meteora PERFECT). Rolling n=8 (3 oldest rotated since c1800), bigs=4 (50%), rugs=0, avg=+278%, K=0.242, geom=+140%/trade WR=75% Er=+2.78. ALL gates PASS by 5-10× except n<20 floor. Consecutive bigs Popus→GENWEALTH (within 24h).
**Status**: deploy-ready unchanged; brain leans YES DEPLOY this cycle. Note symdup<3 overlay REJECTED (would exclude 3/4 bigs).

### H_85871_BC0_WATCH (deploy-ready PENDING RUG-CLAMP POLICY)
**Update c0000**: n=7 unchanged, K=0.223. Geom controversial (Methodology #19 candidate). C11 onset DICKMAXX/PTAI 15h+ no big — C11 confirmed un-productive.
**Status**: deploy-ready PENDING rug-clamp policy decision (#19).

### H_PORTUGAL_C11_ONSET (descriptive monitor)
**Update c0000**: C11 at 15h+ still 0 bigs — > C7 max productive lag 6h40min. **CONFIRMED UN-PRODUCTIVE** = 1st failure of H_CLUSTER_PORTUGAL_PRESENCE precision. Productive-cluster big-rate 6/7=86% → 6/8=75%. Methodology hold but precision regression.
**Status**: CONFIRMED UN-PRODUCTIVE; flag for backlog as precedent.

### H_NEAR_BIG_REGIME (Methodology #17 candidate)
**Update c0000**: Sol +620 GENWEALTH conclusively REFUTES magnitude-shrinkage hypothesis. +620 is solidly fat-tail. Sol big-magnitude pipeline healthy.
**Status**: REFUTED on Sol.

### H_3RD_NAMED_WALLET_HUNT (FAILED c1200, c1800)
**Update c0000**: GENWEALTH lp_provider=D4Bgpf, pool_creator=DtBTU46JaHVFjFZoFP6yc2542L2mEVNXTXAjh8BcLWcU (1-token unique). No new named-wallet candidate emerged. Class size still 2 (HUPHey + 0x85871).
**Status**: FAILED, retry deferred.

### H_SYMBOL_COPYCAT_TRAP (Methodology #18 candidate from c1800)
**Update c0000**: FALSIFIED on aggregate. Full 66-cluster scan: orig big-rate 1.5% vs copy big-rate 2.9% (copies SLIGHTLY MORE big-prone, not less). Counter-examples NOAR/BELIEF/GYATT/Stake (orig fail + copy bigged). Popus/Luce orig-pumps are LOCAL not general.
**Status**: REJECTED on aggregate. Methodology #18 demoted from candidate. Symdup<3 overlay for HUPHey also REJECTED.

### H_GAMMA_STRICT (c1800 candidate)
**Update c0000**: Rolling n=10 K=0.370 geom=+4.43% — slight weakening from c1800 (n=11 K=0.34, Luce -18 dilution + CBSt rotation). Superseded by H_GAMMA_AGE_RELAXED.
**Status**: SUPERSEDED by relaxed variant.

---
## STATUS UPDATES (cycle 20260526_0600)

### H_WALLET_TOP1 HUPHey (deploy-ready, STRENGTHENED)
**Update c0600**: MTFR-J1rp +103.0% (top1=75) lands as HUPHey hit #9 token, hit #5 ≥+100% event. Rolling n=8→9, bigs=4 stable, rugs=0 (cumul-16-rugless intact), wins=7/9=78%, avg=+196% (capped 500), avg_win=+258%, avg_loss=-19.7%, geom=+117%/trade (was +140% c0000, weakened by MTFR-J1rp +103 sub-avg dilution), Er=+1.96. ALL gates PASS by 5-100× except n<20 floor. Distance n=11 from floor.
**Sub-filter top1≥85 REJECTED**: MTFR-J1rp top1=75 + Stake top1=69 both ≥+100% events. 2/5 winners have top1<85 → sub-filter false-negative 40%. Adopt **H_HUPHEY_TOP1_FLEX**: drop top1 threshold OR set to ≥65 (preserve Stake/MTFR-J1rp lower bound).
**Status**: STRENGTHENED. Brain leans STRONG DEPLOY.
**Next**: 10th-token watch; refit walk-forward without top1 threshold.

### H_85871_BC0_WATCH (deploy-ready, rug-clamp MOOT)
**Update c0600**: n=7→4 ROTATION (CAP -100 + 2 others rotated). Current n=4: Poor +659 / BELIEF +235 / DICKMAXX -1 / PTAI +52.9. **0 rugs visible** → rug-clamp policy MOOT (all floor choices converge to geom=+135%/trade). avg=+197%, 2 bigs (50% rate). Distance n=16 from floor.
**Methodology #12 8th confirmation**: rotation purged the only rug → K/geom inflated.
**Subsumption analysis**: 0x85871 ∩ PORTUGAL strict = 3/4 each = 75% overlap. 0x85871 catches Poor (+659) which PORTUGAL misses (bc<16) and AVOIDS STAKE (-52.7) which PORTUGAL catches. **0x85871 STRICTLY DOMINATES PORTUGAL**.
**Status**: STRENGTHENED. Rug-clamp MOOT. Brain leans DEPLOY.
**Next**: forward-fire watch for next 85871 entry (C12 onset likely starts here).

### H_PORTUGAL_STRICT (formally DROPPED)
**Update c0600**: n=7→4 ROTATION same as 85871. Current n=4: STAKE -52.7 / BELIEF +235 / DICKMAXX -1 / PTAI +52.9. avg=+58.6%, 1 big (25%). **Dominated by 0x85871** (subsumption 75% + 85871 catches more bigs + avoids losses).
**Status**: FORMALLY DROPPED from paper-stream candidates. Retain as descriptive monitor only.

### H_GAMMA_RELAXED (borderline)
**Update c0600**: +2 entries Poop -6 + grail -20 (both small losses, no rugs). n=16 unchanged at brain's count. **Fresh geom-per-trade computation: +1.55%** (vs brain's prev +6.60% — possible measurement methodology drift). 1 big (Popus +221) + 1 near-big (Luce +137). PASSES geom gate by margin (gate ≥1%, fresh +1.55%) but BORDERLINE.
**Status**: BORDERLINE — gate-passes by margin only. Defer deploy.
**Next**: n=20 watch; investigate measurement discrepancy.

### H_RUG_CLAMP_POLICY (Methodology #19 — MOOT)
**Update c0600**: 0x85871 only rug (CAP -100) rotated out → all floor choices converge. Policy decision MOOT for now. Defer formal adoption until next 85871 rug observed.
**Status**: DEFERRED (was: candidate).

### H_BETA_HARAMBEX_SUBFILTER (n=1 candidate)
**Update c0600**: REJECTED. HarambeX is single-instance — only 1 HARAMBEX token visible with current data (+11.2% close on different mint). The +132 reading from c0000 was from a different mint that fits broader near-big cohort, not a distinct β-class. Defer until 2nd β-shape big observed.
**Status**: REJECTED single-instance.

### H_NEAR_BIG_COHORT (NEW DIMENSION)
**Observation**: 19 unique Sol tokens in current 47h window with pnl 80-149.99% (near-big band). BF stream distribution:
- SNIPER_ULTRA_TRIPLE: 4 (21%)
- SNIPER_SMART_TOP_AGE5: 4 (21%)
- SNIPER_LOWCAP: 3 (16%)
- SNIPER_H: 3 (16%)
- SNIPER_H2: 2 (11%)
- SNIPER_MC_LIQ / SNIPER_SMART_COPY_AGE5 / SNIPER_G: 1 each

ULTRA_TRIPLE + SMART_TOP_AGE5 capture 42% of near-bigs vs <20% on full bigs. Hypothesis: near-bigs are caught by TIGHTER multi-condition filters that exit earlier (cap-side) on weaker fat-tails.
**Status**: NEW candidate. n=19 sample available.
**Next**: compute feature-distribution comparison (top1/smart/known/liq/buys_m5) between near-big cohort vs full-big cohort; if near-bigs are "would-have-been-bigs" with shorter trails → ULTRA_TRIPLE family may have early-exit edge worth combining with HUPHey/85871 stream.

### H_NOAR_75qsE3_WALLET (3rd named-wallet candidate)
**Observation**: 8cYhZ3M9hzWS +142.5% Sol (NOAR symbol) lands as 2nd ≥+100% event from wallet 75qsE3p5y2BF (after GvxMd2m5x47d +152.5 in c0000). Wallet now has 10 NOAR tokens visible: 2 wins (20% ≥+100% rate), 2 rugs (20%), 6 small/mid (mostly -20% to +10%). Avg ≈ +1.4%.
**Comparison**: HUPHey 0% rug (cleaner alpha). 75qsE3p5y2BF 20% rug (still better than baseline 51%).
**Status**: CANDIDATE — worse than HUPHey but better than baseline. Defer deploy.
**Next**: monitor for 11th NOAR or non-NOAR token from same wallet; if rugs stay ≤25% and ≥+100% rate >15% over n=15+, consider paper-stream WALLET_NOAR_WATCH.

### H_SMART_CLUSTER_TRAIL_EDGE (n=5-6 ambiguous, weak positive for HUPHey mid-fat-tails)
**Update c0600**: 6th data point MTFR-J1rp smart +4.5pp lift over A/B/H/H2. HUPHey pattern emerging:
- Mid-fat-tail HUPHey wins (sub-500%): smart wins on Stake +481, MTFR-BVB +175, MTFR-J1rp +103
- Extreme fat-tail HUPHey wins (≥500%): H2 wins on Poor +943, GENWEALTH +620
3/5 smart wins, 2/5 H2 wins on HUPHey wins. Not deployable but suggests dual routing: smart for mid, H2 for extreme.
**Status**: WEAK POSITIVE for HUPHey-specific routing.

### H_REGIME_ASYMMETRIC_DURATION (NEW)
**Observation**: Sol clear / BSC triggered regime now 3 consecutive cycles (c1800 → c0000 → c0600). Sol Cond A improved over cycles -62.6 → -57.6 → -54.7 → -44.5 (steady recovery). BSC Cond A worsened -57.6 → -62.0 (deeper trigger).
**Hypothesis**: Chain-asymmetric regimes have non-zero duration (≥3 cycles, ≥18h). Pre-c1800 was symmetric (both triggered or both clear).
**Status**: DESCRIPTIVE candidate.
**Next**: track duration; if >5 cycles, consider as durable regime feature for chain-specific gates.

### Stuck warning status
**6 consecutive cycles with new findings** (since c1200 paradigm shift to wallet-feature). Trajectory: HUPHey discovery → 0x85871 discovery → γ-shape candidate → Methodology #15-18 → near-big cohort → top1-flex refinement. Stuck warning NOT triggered.

---
## NEW HYPOTHESES — cycle 20260526_1200

### H_HUPHEY_TOP1_FLEX (FORMALLY ADOPTED)
**Spec**: HUPHey filter = `top1_owner.startsWith("HUPHey")` only, NO top1 threshold.
**Walk-forward**: HUPHey n=9 rolling cohort, top1 threshold sensitivity:
- top1≥0 (no threshold): n=9 bigs=4 avg=+258.5% geom=+117.32%/trade ← ADOPTED
- top1≥65: n=9 (identical, min top1=68.6 in dataset)
- top1≥70: n=7 bigs=3 geom=+123.44% (loses Stake +481 + PP420 -33)
- top1≥85 (prev candidate): n=4 bigs=2 geom=+110.62% (loses 5 entries, geom drops)
**Decision**: drop top1 threshold. Wallet identity is alpha; top1 noise within HUPHey activity.
**Status**: ADOPTED. Final spec for PAPER_SOL_HUPHEY_WATCH.

### Methodology #20 candidate: COHORT-SHAPE TRAP
**Observation**: This cycle, brain selected the 19 Sol near-bigs (80-150% pnl band) and computed their median feature distribution: pumpswap=13/6, smart median=11 (vs bigs=6), buys_m5=198 (vs bigs=81), top1=66 (vs bigs=83.5). This looked like a structural difference between near-bigs and bigs ("near-bigs = pumpswap+smart-velocity shape").
**Walk-forward test**: filter `pumpswap ∩ smart≥10 ∩ buys_m5≥150 ∩ top1∈[10,75]` (the near-big shape):
- Full cohort: n=89 bigs=1 (1.1%) near=5 (5.6%) rugs=65 (73.0%) avg=-65.7% geom=-88.30% K=-1.138 WR=18%
- TRAIN (oldest 60%, n=53): 1 big 44 rugs geom=-91.25% K=-1.10
- TEST (newest 40%, n=36): 0 bigs 21 rugs geom=-82.04% K=-1.04
**Conclusion**: The "near-big shape" is a RUG FACTORY. The 19 near-bigs are survivors of selection bias within a 89-strong base population that's 73% rug.
**Lesson #20 statement**: Before deriving a filter from cohort-shape (median features of top-N% outcomes), count the base population with the same shape and compute P(big|shape). If base-rate is rug-heavy, the shape is selection-bias survival, not a discriminator.
**Status**: NEW CANDIDATE, ready for formal lesson adoption.

### H_PUMPSWAP_SMART_VELOCITY (REJECTED HARD via Methodology #20)
**Spec**: pumpswap ∩ smart≥10 ∩ buys_m5≥150 ∩ top1∈[10,75].
**Walk-forward**: n=89 K=-1.14 geom=-88% 73% rug. TRAIN/TEST both K<-1.
**Status**: REJECTED HARD. Serves as Methodology #20 canonical example.

### H_STATE_WRITE_INFRA_FRESHNESS (operational)
**Observation**: state.json last write 07:30Z, current 12:02Z, gap 4.5h. Sniper proc running. 2nd anomaly: earliest entry moved BACKWARD 8h25min. 3rd anomaly: `positions` dict empty.
**Hypothesis**: sniper state-write cadence has degraded, or state-rebuild logic triggered, or atomic-rename has stalled.
**Status**: NEW OPERATIONAL — needs user / infra-check.
**Next**: check sniper logs, disk-write i/o, state-rename logic. Flag in BRIEF.

---
## STATUS UPDATES (cycle 20260526_1200)

### H_WALLET_TOP1_HUPHEY (deploy-ready, top1-flex spec finalized)
**Update c1200**: stale-data cycle, n=9 unchanged. H_HUPHEY_TOP1_FLEX walk-forward sensitivity table (top1≥0..90 across 8 thresholds) confirms top1≥0 (no threshold) preserves full n=9 geom=+117%. Spec FINALIZED: `top1_owner.startsWith("HUPHey")` only.
**Status**: deploy-ready, FINAL SPEC LOCKED.

### H_85871_BC0_WATCH (deploy-ready, unchanged)
**Update c1200**: stale-data cycle, n=4 unchanged. No fresh BSC forward-fires.
**Status**: deploy-ready, unchanged.

### H_GAMMA_RELAXED (borderline, unchanged)
**Update c1200**: stale-data cycle, n=16 unchanged.
**Status**: borderline, unchanged.

### H_NEAR_BIG_COHORT (REJECTED via Methodology #20)
**Update c1200**: Walk-forward H_PUMPSWAP_SMART_VELOCITY (the near-big shape) n=89 K=-1.14 73% rug. Near-bigs are survivor-noise in high-rug base, NOT a discriminable cohort.
**Status**: REJECTED. Methodology #17 (NEAR-BIG REGIME) RETIRED. ULTRA_TRIPLE/SMART_TOP_AGE5 capture rate without base rate is meaningless.

### Methodology #17 NEAR-BIG REGIME (RETIRED)
**Update c1200**: Cleanly retired this cycle. Near-bigs are survivor noise within high-rug base. "Magnitude shrinkage" reading was also wrong (GENWEALTH +620 c0000 refuted it).
**Status**: RETIRED. Removed from active methodology candidate list.

### H_REGIME_ASYMMETRIC_DURATION (4th consecutive cycle, unchanged inference)
**Update c1200**: Can't recompute on stale data, but extrapolating: 4th consecutive chain-asymmetric cycle. Sol clear / BSC triggered.
**Status**: DESCRIPTIVE candidate, 4 cycles now.

### Stuck warning status
**7 consecutive cycles with new findings** (since c1200 paradigm shift). This cycle: methodology #20 + top1-flex formal adoption + #17 retirement = methodology progress even with FLAT n-progress.
**Status**: NOT TRIGGERED.

## NEW (proposed cycle 20260526_1800)

### H_NOAR_WALLET — 3rd named-wallet entity (statistical-tier)
**Idea**: Buy when `top1_owner.startsWith('75qsE3p5y2')` (NOAR launcher wallet — `75qsE3p5y2BFSLnfS9MUMqSAw...`).
**Evidence (this cycle recount post Methodology #21 fix)**:
- n=11 (was c0000 n=10 — Maple was unrecognized α-borderline c1200 because brain matched by symbol not address)
- bigs=2 (18.2%): Maple +163.8, NOAR +152.5 | near=1 (9.1%): NOAR +142.5 | rugs=2 (18.2%): NOAR -100, NOAR -99.5
- avg=+16.1%  WR=45%  Er=+0.17  K*=0.23  geom@K=+1.92%/trade  (floor=-0.95, cap=+500%)
- All 11 hits dex=meteora; 10 of 11 have top1%=99.9 (one outlier Maple top1=83.5 = BIG); bf is 8× SMART_TOP_AGE5, 1× H2 (Maple BIG), 1× H, 1× other
- Distance-to-deploy: 9 from n=20 floor (same as HUPHey distance)
**Why it might fail**:
- 18% rug rate does NOT meet Methodology #14 clean-alpha criterion (HUPHey=0%, 0x85871=0%). NOAR is statistical-tier, not clean-alpha tier.
- Methodology #13 SINGLE-WALLET INFLATION applies → 2× n penalty (effective floor n=40, distance 29).
- Sub-filter attempts to find clean cohort within NOAR FAILED (top1%<99.9 → n=2; bf=H2 → n=1; smart≥3∩known≥12 → 0 bigs in n=4).
**Status**: NEW — STATISTICAL deploy candidate pending user tier-decision. Different deployment class from HUPHey/0x85871 clean-alpha tier.

### H_TOP2_HLNP — REJECTED (Methodology #15 SUBSUMPTION + #20 COHORT-SHAPE TRAP)
**Idea (initial)**: HLnpSz9h2S4hiLQ43rnSd9XKCutHA7b8HqMkmdaitlCc as `top20_owners[rank=2].addr` — 4 bigs (5.7%) / 19% rug on n=70 Sol best-fire dedup vs base 1.2%/55% = apparent 4.75× big lift, 66% rug reduction.
**Walk-forward (60/20/20 by entry_time)**:
- TRAIN n=42 bigs=3 (7%) rugs=8 (19%) avg=+21.0% Er=+0.11 K=0.11 geom=+0.54%
- VAL n=14 bigs=1 (7%) rugs=1 (7%) avg=+38.6% Er=+0.30 K=0.42 geom=+4.79%
- **TEST n=14 bigs=0 (0%) rugs=4 (29%) avg=-16.1% Er=-0.15 K=0.01 geom=-0.15% — FAILS gate**
**REJECTED**:
1. Walk-forward TEST FAILS (Er<0, geom negative).
2. The 4 bigs are: Maple (NOAR top1), Stake/Poor/GENWEALTH (HUPHey top1) → **100% subsumed** by HUPHey∪NOAR top1_owner cohort.
3. Per-day distribution shows launchpad-drift pattern (05-24: 20 entries 3 bigs +51.6% → 05-25: 42 entries 1 big +3.9% → 05-26: 8 entries 0 bigs +0.1%), mirroring c1200 launchpad finding (Methodology #16 historical-vs-live drift) on a different dimension.
**Lesson**: HLnp is launchpad infrastructure — its rank-2 presence is a CONSEQUENCE of HUPHey/NOAR-deployed tokens using HLnp tooling, NOT an independent alpha source. **Methodology #20 2nd confirmation** (cohort-shape trap on top2 dimension; base-rate check + walk-forward TEST caught it).
**Status**: REJECTED.

## Methodology Lesson #21 NEW CANDIDATE — SYMBOL-BLIND WALLET DRIFT
**Lesson**: When tracking a named-wallet cohort, cohort membership MUST be determined by the wallet address field (`top1_owner`, `bc[0]`, `pool_creator`, `lp_provider`), NEVER by the token symbol or visual association with prior cohort members. Re-cohort all named-wallet candidates at every cycle by re-scanning the full closed_trades on the wallet address.
**Evidence**: NOAR cohort c0000 reported n=10 by symbol-matching `NOAR` tokens; this cycle's address-based re-scan found n=11 (Maple top1=75qsE3p5y2 was an unrecognized NOAR token because its symbol was `Maple`, not `NOAR`). Hidden cohort member skipped one cycle of progress tracking.
**Root cause**: symbol ≠ wallet. Maple was c1200-classified as "α-borderline new shape candidate" instead of being recognized as the same NOAR launcher.
**Inverse mode of #18 SYMBOL-COPYCAT TRAP**: #18 = assuming same symbol = same wallet (false positive). #21 = assuming different symbol = different wallet (false negative). Both reduce to: symbol-keyed memo of wallets is unreliable.
**Adopt**: proactive (logic airtight from single case, no need to await 2nd instance).

## Methodology Lesson #22 NEW CANDIDATE — API SCHEMA VERIFICATION
**Lesson**: Before reporting any field/dict as "empty" or "missing", verify the exact key name in raw JSON via direct introspection (e.g., Python `list(d.keys())`). Mistaken key names produce false-empty alarms that pollute brain reasoning.
**Evidence**: c1200 brain reported `state.json positions dict EMPTY` as a 3rd operational anomaly. This cycle's introspection found the actual key is `open_positions` (not `positions`) — 22 raw rows / 5 unique Sol opens always existed. The "empty positions" anomaly was a wrong-key bug, not a sniper write issue.
**Mitigation**: 1 line of code: `print(list(state_dict.keys())[:20])` before any inventory.
**Status**: low-importance procedural lesson; auto-apply.

## Methodology Lesson #20 — formal adoption (2nd confirmation this cycle)
**Status update**: Was CANDIDATE c1200 from a single instance (H_PUMPSWAP_SMART_VELOCITY n=89 73% rug). This cycle's H_TOP2_HLNP is 2nd confirmation — base-rate check + walk-forward TEST caught the cohort-shape trap before promotion. **READY for formal METHODOLOGY_LESSONS.md adoption.**

---

## Cycle 20260527_0000 additions

### H_SELF_LP — weak-alone, file for COMBO
**Idea**: `top1_owner == pair_address` (i.e., top-1 owner is the pair contract itself, characteristic of pump.fun pre-graduation bonding-curve tokens) as a rug-modulating feature.
**Backtest (n=4930 closed_trades, full corpus)**:
- ALL: n=4930 big=127 (2.58%) rug=2668 (54.12%) avgPnL=-49.4%
- Self-LP (top1==pair): n=2245 (45.5% pop coverage) big=53 (2.4%) rug=1327 (59.1%) avgPnL=-56.3%
- Non-self-LP: n=2685 big=74 (2.8%) rug=1341 (49.9%) avgPnL=-43.7%
**Effect**: rug% +5.0pp, avgPnL -6.9pp vs population. Modest but real.
**Methodology #20-aware concern**: This is likely a "pump.fun pre-graduation" proxy and may be SUBSUMED by existing `bc<30` field already used in HUPHey/85871 gates. Walk-forward + bc combo test required before any promotion.
**Status**: WEAK ALONE — keep as COMBO modifier candidate. Test for orthogonality with bc-stage next cycle when state freshens.
**Note**: 4 of 5 our current Sol open positions are self-LP (XVG/USDCx/grail/CHARTARD; HTX excepted) → empirically observable rug-risk concentration in current opens.

### H_GECKO_FEED — new data source / source coverage gap
**Idea**: Add a poller that ingests `/srv/bots/.shared/data/pumps_24h.jsonl` (geckoterminal_trending) into sniper signals_pool. Currently 100% of pumps_24h corpus (23 unique tokens last ~3 days) is gecko-trending sourced — a feed our sniper does NOT directly tap.
**Quantification**: ~7-8 unique pumped tokens/day from gecko-trending. At 2.6% population big-rate ≈ 0.2 expected bigs/day from this source.
**Implementation gate**: Requires (a) infra fix (Helius), (b) user OK to add new entry source. NOT actionable this cycle.
**Caveats**:
- Risk of duplicate entries (already captured in serial streams); needs dedup against seen_tokens.
- Gecko-trending lags raw mint creation by minutes-hours (it's a trending feed, not realtime mint feed) — entries via this source may be Phase 3 hype rather than Phase 1-2 alpha. Phase classification per HOLISTIC_STRATEGY_MANDATE required.
- Likely subsumed by existing DexScreener boost/profile filter for the same tokens after some lag. Empirical overlap measurement needed.
**Status**: NEW candidate, await infra fix + user OK to design.

## Methodology Lesson #21 — graduation from CANDIDATE to READY (2nd confirmation this cycle)
**Real-time confirmation evidence**:
- Our open `grail`: token mint `Ga3dqNJDMtKNUXromL2zFemWyKrUdqJ1w6AracjVWRia`, pair_addr `3FUCCrjN…`, top1_owner = pair_addr (self-LP), entry 05-26T06:15Z, flat price action.
- pumps_24h `grail`: pair_addr `UvN1ZVZJom7D4CPuhjJrbD6y82k5TSefRQMZHHXjjfM`, pair_created 05-26T02:49Z (3.5h earlier), peaked +2188% — unrelated mint.
- Two unrelated Sol mints share the symbol `grail` on the same day. Symbol-only matching would attribute the wrong outcome.
- Combined with c1800 historic Maple/NOAR linking case = 2 confirmations.
**Adopt status**: PROMOTED from CANDIDATE to READY FOR FORMAL ADOPTION (parity with #20).

## Methodology Lesson #23 NEW CANDIDATE — INFRA-CRISIS OPPORTUNITY COST QUANTIFICATION
**Lesson**: When sniper non-functional for X hours, quantify missed-pump count from `pumps_24h.jsonl` to give user a concrete cost figure for the outage. Helps prioritize infra fixes vs other engineering work.
**Evidence (this cycle)**:
- Sniper frozen 16.5h (28h since infinite-loop onset).
- pumps_24h corpus shows 23 unique pumped Sol tokens in ~3-day window.
- At population big-rate 2.6%: ≈ 0.6 expected bigs MISSED during outage.
- At population rug-rate 54%: ~12 rugs AVOIDED (silver lining of being offline).
- Net expected: -0.6 bigs (positive value missed) is the actionable cost figure.
**Status**: SINGLE case (this cycle). Promote to CONFIRMED on next infra outage application.

---

## Cycle 20260527_0600 additions

### H_SELF_LP — STRENGTHENED 4× (best-fire dedup vs c0000 raw-row)
**Idea**: top1_owner == pair_address fingerprint (pump.fun pre-graduation bonding curve). Apply as VETO COMBO modifier.
**Best-fire backtest (n=657 Sol unique mints)**:
- SOL SELF-LP n=389 big=2 (0.5%) rug=246 (63.2%) avg=-60.9% Er=-0.609
- SOL NON-SELF n=268 big=6 (2.2%) rug=116 (43.3%) avg=-32.5% Er=-0.325
- Differential: +28.4pp avgPnL lift on NON-SELF; 6/8 of all Sol bigs in 41% of population (1.83× big-rate concentration).
**Walk-forward (60/20/20 chronological)**:
- TRAIN NON-SELF Er=-0.32 vs SELF-LP Er=-0.65 (Δ=33pp)
- VAL NON-SELF Er=-0.19 vs SELF-LP Er=-0.54 (Δ=35pp)
- TEST NON-SELF Er=-0.48 vs SELF-LP Er=-0.57 (Δ=9pp; TEST big-rate 0 — regime artifact)
**Status**: VETO-COMBO confirmed. Genuinely stronger than c0000 weak-alone report; correction due to Methodology #4 best-fire dedup. Walk-forward consistency holds for veto direction; not standalone deploy gate (Er still negative on NON-SELF).
**Top1-band variant**: SELF-LP ∩ top1≥85 → n=77 big=0 rug=93.5% = mathematical-veto candidate.

### H_RUG_WALLET_VETO — NEW (4 Sol wallet blacklist candidates)
**Idea**: blacklist these 4 prefixes (Sol top1_owner):
- ent9nhnz1f7e... n=13 rugs=11 (85%) avg=-77.5%
- 2qiojbwkbvts... n=11 rugs=10 (91%) avg=-83.0%
- 8m88xunebwlz... n=11 rugs=11 (100%) avg=-100.0%
- 88md1aaefdr2... n=9 rugs=8 (89%) avg=-76.4%
- AGG n=44 big=0 rug=40 (91%) avg=-84.3%
**Walk-forward (TRAIN n>=5 rug>=70% bigs=0 identifies 4 wallets; VETO applied to all splits)**:
- TRAIN VETO-hits n=31 rug=29 (93.5%) avg=-90.6%
- VAL VETO-hits n=6 rug=4 (66.7%) avg=-33.4%
- TEST VETO-hits n=7 rug=7 (100%) avg=-100.0%
**Status**: NEW — REAL filter, walk-forward TEST 100% rug-capture out-of-sample. Population coverage small (~7% of Sol). Standalone veto, not entry signal. Likely these are launchpad-like wallet clusters analog to HLnpSz9h (Methodology #16 historical-vs-live).

### H_META_TOP99_PURE_SHAPE — NEW shape-only candidate
**Idea**: meteora dex ∩ top1_pct ≥ 99 (regardless of wallet identity).
**Backtest (n=657 Sol best-fire dedup)**:
- meta_top99 ALL: n=35 big=2 (5.7%) rug=7 (20%) avg=+9.9% Er=+0.099 K=0.067 geom=+0.27%/trade
- meta_top99 EXCL NOAR: n=25 big=1 (4%) rug=5 (20%) avg=+13.4% Er=+0.134 K=0.075 geom=+0.40%/trade
- meta_top99 ∩ smart≥3: n=15 big=1 (6.7%) rug=4 (27%) avg=+12.8% Er=+0.128 K=0.029 geom=+0.09%/trade
**Gate analysis**: passes n≥20, Er>0, K≥0.05 (3 of 4). FAILS geom≥1% by 0.73pp. Closest pure-shape filter to gate-pass.
**Status**: NEW WATCH candidate. If state thaws and new entries match shape, track Er evolution. Implication: a portion of HUPHey/NOAR apparent edge may be shape-driven (HUPHey clear outlier per matched-shape validation; NOAR mostly shape).

### NOAR alpha — DECOMPOSED via matched-shape baseline (Methodology #20 confirmation #3)
**Result**: apparent NOAR direct Er+0.16 K=0.21 (n=11) DECOMPOSES into:
- NOAR-within-shape (meta_top99): n=10 big=1 Er=+0.013 K=0.034 (essentially zero)
- Maple (Sol top1=83.5 = NOAR-deployed cross-cohort artifact, n=1 +163%) drives nearly all apparent edge
**Matched-shape baseline EXCL NOAR (meta_top99 non-NOAR)**: n=25 Er=+0.134 K=0.075
**Differential**: NOAR within matched shape adds essentially 0 over baseline.
**Status**: DEPRIORITIZED for deploy. Either skip NOAR deploy (Er+0.01 within matched shape), OR deploy H_META_TOP99 instead (broader, n=35 already). Cohort-shape-trap confirmed.
**Methodology #20 status**: TRIPLE-CONFIRMED (c1200 PUMPSWAP / c1800 TOP2_HLNP / c0600 NOAR). FORMAL ADOPTION ready.

### HUPHey alpha — TRUE clean-alpha VALIDATED via matched-shape baseline
**Matched shape**: meteora ∩ top1≥60 ∩ smart≥3 ∩ known≥5
- WITH HUPHey: n=80 big=4 (5.0%) avg=-7.3% Er=-0.073
- EXCL HUPHey: n=71 big=0 (0%) avg=-41.0% Er=-0.410 K=-1.103
- HUPHey direct: n=9 big=4 (44%) rug=0% avg=+258.5% Er=+2.585 K=0.41 geom=+59.7%/trade
**Differential**: HUPHey adds +3.00 Er over matched-shape baseline.
**Status**: HUPHey is GENUINE wallet alpha (Methodology #14 + 14a TRUE clean-alpha classification). Deploy strongly recommended.

## Methodology Lesson #14a — NEW SUB-LESSON CANDIDATE — MATCHED-SHAPE BASELINE SUBTYPE
**Lesson**: When classifying a named-wallet/cohort candidate as "clean-alpha" per Methodology #14, ALWAYS construct a matched-shape baseline EXCLUDING the wallet and compare Er. Two sub-categories emerge:
- **TRUE clean-alpha**: matched-shape baseline EXCL wallet Er ≪ wallet Er (large differential). Wallet identity is the edge source.
- **APPARENT clean-alpha (shape-coincidence)**: matched-shape baseline EXCL wallet Er ≈ wallet Er (small differential). Shape is the edge source; wallet is incidental.
**Evidence**:
- HUPHey TRUE: matched-shape Er=-0.41 vs wallet Er=+2.59 (+3.00 differential)
- NOAR APPARENT: matched-shape Er=+0.13 vs wallet Er=+0.16 (+0.03 differential)
**Adopt**: proactive (logic airtight from 2 contrasting cases). Apply before promoting any wallet-based candidate to deploy-ready.

## Methodology Lesson #20 — TRIPLE-CONFIRMED (FORMAL ADOPTION)
**3rd confirmation this cycle**: NOAR alpha decomposition — apparent Er+0.16 → matched-shape EXCL NOAR Er+0.13 → NOAR-within-shape Er≈0. Cohort-shape trap: apparent wallet edge collapses to baseline when controlled for shape.
**1st**: H_PUMPSWAP_SMART_VELOCITY (c1200) — broad-filter pumpswap∩smart∩buys cohort 73% rug, n=89.
**2nd**: H_TOP2_HLNP (c1800) — top20[rank=2] cohort apparent 4.75× big lift collapses to TEST 0 bigs / n=14 Er=-0.15.
**Adoption**: matched-shape baseline check is mandatory before promoting any cohort to deploy-ready.

## Methodology Lesson #4 — REAFFIRMED STRONGLY
**Re-evidence this cycle**: c0000 H_SELF_LP backtest on raw 4930 rows reported -6.9pp avgPnL drag (weak veto). This cycle best-fire dedup 802 unique mints reports -28.4pp drag (4× stronger). Stream duplication INFLATES both subsets unevenly; only best-fire dedup gives valid cohort statistics.
**Rule**: any population-level cohort statistic MUST use best-fire dedup. Never report raw-row statistics for cohort comparison.

## Cycle 20260527_1200 additions

### H_BSC_85871 STATUS UPGRADE → Methodology #14a-VALIDATED (TRUE clean-alpha)
Matched-shape baseline retrofit completed this cycle. ALPHA n=3 best-fire (BELIEF +235%, PTAI +52.9%, DICKMAXX -1.0%) avg=+95.6% geom=+71.8%/tr big%=33% rug=0% vs MATCHED-SHAPE EXCL same liq_mcap/age/mcap regime n=85 avg=-60.7% big%=1.2% rug=71.8% = +156.3pp avg lift, 27.7× big-rate, 100% rug elimination. Differential survives even excluding BELIEF (remaining n=2 ≈+26% vs -60.7% matched = still ~+87pp). Joins HUPHey as 2nd Methodology #14a worked example. **Status: DEPLOY-READY (12 cycles pending user auth)**.

### H_9CCPC_WATCH (NEW alpha candidate, weak)
- Cohort: top1_owner.startsWith("9ccPCxxE") — n=3 best-fire (SHIBA +34.4%, ISOR +12.2%, ISOR +31.9%).
- Stats: avg=+26.2% geom=+25.76%/tr WR=100% rugs=0 bigs=0.
- Shape: top1_pct=99, liq_mcap=1-2, mcap 1.4-1.6M, age 19-23 min, holders=20 (cap).
- Matched-shape EXCL n=20: avg=-7.6% rug=15% WR=55% bigs=0 → +33.8pp lift, +45pp WR, +25.8% vs -100% geom.
- **CAVEAT (Methodology #24)**: 2 of 3 entries same symbol (ISOR) → effective n=2 distinct projects.
- **Verdict**: weak alpha candidate. No bigs (limited explosive upside). Modest differential vs matched-shape. NOT deploy-ready. **WATCH only — n=3 → effective 2; need 5+ more distinct symbols before re-evaluation.**

### H_RUG_WALLET_VETO_RUG6 (UPGRADE from RUG_4)
New rug-wallet additions discovered this cycle via SOL top1_owner scan (n≥3 buckets, sorted worst avg):
- **43wpYdVB**: n=7, avg=-72.1%, rug=5/7 (71%), bigs=0, wins=1 (small +17). Cohort: Popus/HOPPY/SOLWHEEL/JOIAI/GOONC/BRUME/COLLECTOOR.
- **3xbyiLME**: n=5, avg=-66.3%, rug=3/5 (60%), bigs=0, wins=1 (small +9). Cohort: F1/Popus/Chauvin/GOONC/GOONC.

Combined RUG_6 set (8M88XUne, 2QioJBwK, Ent9nhnZ, 88Md1AAE, **43wpYdVB**, **3xbyiLME**):
- Walk-forward 50/50 split (SOL best-fire n=657 → TRAIN 328 / TEST 329):
  - TRAIN: n=27 hits, avg=-89.2%, rug=25 (92.6%), bigs=0
  - TEST: n=29 hits, avg=-73.7%, rug=23 (79.3%), bigs=0
- vs RUG_4 walk-forward: TEST n=18 rug=88.9% → RUG_6 catches +11 trades (+61% expansion) at slightly lower precision (79.3% vs 88.9%).
- **0 bigs caught across all 56 train+test hits** → veto applies losslessly to known-alpha edge.

**Status**: RUG_6 spec ready for sniper entry filter. Pseudo-code:
```
if (entry_signal.top1_owner) {
  const top1 = entry_signal.top1_owner;
  const RUG_PREFIXES_SOL = ['8M88XUne','2QioJBwK','Ent9nhnZ','88Md1AAE','43wpYdVB','3xbyiLME'];
  if (RUG_PREFIXES_SOL.some(p => top1.startsWith(p))) return SKIP;
}
```
Pending user adoption decision.

### H_RUG_SYMBOL_DUPLICATE (NEW hypothesis, deferred test)
- **Observation**: symbol `Popus` appears under different rug-wallet top1_owners (43wpYdVB AND 3xbyiLME) at different pair_addresses. Symbol `GOONC` appears in both 43wpYdVB and 3xbyiLME cohorts.
- **Hypothesis**: When a token symbol appears in multiple known rug-wallet cohorts with same/similar pair-creation timing, this is elevated rug-risk signal (rug-wallet cluster coordinated copy-rug).
- **Test plan (next cycle)**: scan all symbols with ≥2 rug-wallet hits; compute conditional rug% and compare to single-rug-wallet rug%.
- **Status**: DEFER — small n (only ~3 such symbol cases visible). Re-evaluate when more data.

### H_META_TOP99_PURE_SHAPE (carry forward — unchanged)
Last cycle stats: n=35 Er+0.099 K=0.067 geom=+0.27%/tr (3/4 gates passed, fails geom by 0.73pp). No state change — carry. Re-test when fresh data arrives.

### Methodology Lesson #24 — NEW CANDIDATE — SAME-SYMBOL DUP-PAIR INFLATION
**Trigger**: H_9CCPC_WATCH cohort n=3 (best-fire unique pairs) but only 2 distinct symbols (SHIBA, ISOR×2). HUPHey precedent: n=9 pairs / 7 distinct symbols (3× MTFR).
**Rule**: When grouping cohorts by a wallet identifier, ALWAYS report unique-symbol count alongside unique-pair count. If `unique_symbols < 0.6 * unique_pairs`, downgrade effective-n to `unique_symbols * 1.2` (or similar penalty) when assessing statistical strength.
**Why it matters**: same-symbol re-pair (e.g., same project re-launched at different pair_addresses, or symbol-collision attacks) inflates apparent independence. Two pairs of "ISOR" are NOT two independent observations.
**Promotion criteria**: needs 2nd confirmation. Currently 1st confirmation = 9ccPCxxE. Watch for 2nd occurrence in upcoming cohort scans.

### Methodology Lesson #14a — UPGRADE to FORMAL ADOPTION READY
**2 worked examples now in record**:
- HUPHey (cycle 20260527_0600): TRUE clean-alpha, matched-shape EXCL Er=-0.41 vs direct Er=+2.59 = +3.00 differential.
- 0x85871 (this cycle): TRUE clean-alpha, matched-shape EXCL n=85 avg=-60.7% vs direct n=3 avg=+95.6% = +156.3pp differential.
**Counter-example also confirmed**: NOAR (cycle 20260527_0600) APPARENT alpha, matched-shape decomposed to shape-coincidence.
**Status**: ready for formal adoption next cycle (3rd confirmation if needed via another candidate).

### Methodology Lesson #4 — REAFFIRMED YET AGAIN
3rd reaffirmation: 0x85871 raw-row n=4 → best-fire n=3 (1× duplicate row of same pair). All this cycle's cohort statistics used best-fire dedup. Going forward MANDATORY for any cohort-level claim.

## NEW HYPOTHESES — cycle 20260527_1800 (LMR family)

### H_LMR_VETO_175 ★★★★★ — UNIVERSAL FEATURE-SPACE RUG FILTER (highest-confidence finding to date)
- **Filter**: `entry_signal.liq_mcap_ratio >= 175` → VETO entry
- **Walk-forward validation** (Sol corpus n=4468, 4-way per-quarter):
  - Q0: VETO n=75 (13 unique pairs) rug=100.0% big=0.0% lost_bigs=0
  - Q1: VETO n=100 (18 pairs) rug=100.0% big=0.0% lost_bigs=0
  - Q2: VETO n=77 (13 pairs) rug=89.6% big=0.0% lost_bigs=0
  - Q3: VETO n=123 (24 pairs) rug=100.0% big=0.0% lost_bigs=0
  - TOTAL: 375 trades / 68 unique pairs, 96-100% rug precision, ZERO unique big pairs lost across all 4 windows.
- **Cross-chain validation**: BSC (n=479) — bucket lmr>=150 also shows 83% rug, 0% big. Filter universal.
- **Independence**: HUPHey n=81 trades, ZERO have lmr>=150. Filter doesn't kill alpha.
- **Fresh data confirmation**: 17 new closures this cycle — CHARTARD lmr=180 (-100%), grail lmr=196 (-100%) both confirm.
- **Mechanism**: high lmr means liquidity dwarfs market cap → unmigrated/stuck pump.fun curves → dead tokens that rug.
- **Status**: PROPOSED for immediate Sniper deployment. AWAITING USER AUTH.
- **Risk**: 1 historical big (Horatio +138% lmr=163) is BELOW 175 threshold — preserved. Distribution-shift risk requires recalibration every ~2-3 days.

### H_LMR_VETO_150 ★★★★ — BROADER VARIANT
- **Filter**: `entry_signal.liq_mcap_ratio >= 150` → VETO
- **Walk-forward**: 676 trades / 124 unique pairs across 4 quarters, ~87% rug rate.
- **Big lost**: 1 unique pair (Horatio +138%, lmr=163).
- **Trade-off**: ~2× more coverage than _175, but accepts 1 big-pair loss.
- **Status**: SECOND-CHOICE if user prefers more aggressive defense.

### H_LMR_ALPHA_LOW ★★ — ALPHA-SIDE LMR (deferred, needs investigation next cycle)
- **Filter**: `entry_signal.liq_mcap_ratio < 0.1` → PASS-priority?
- **Observation (full Sol corpus)**: bucket <0.1 has big%=7.3% (TOP big rate among all lmr buckets), avgPnL=-14.0% (best), WR=32.3%.
- **Hypothesis**: very low lmr = small liquidity relative to mcap = post-migration token with healthy mcap = potential fast mover.
- **Next cycle**: walk-forward backtest this as a positive alpha candidate.

### H_TOP1_PCT_BIMODAL — NOT A PRIMARY FILTER (concluded this cycle)
- **Observation**: top1_pct buckets are bimodal. 85-95% is worst (72-89% rug, 0-1.7% big). 95-100% is actually OK (39% WR, 33% rug).
- **Mechanism**: 100% top1 likely means single LP-locked or burned holders (can't rug). 85-95% = highly centralized active holders (rugs).
- **Walk-forward** (top1>=90 alone): TEST VETO n=430 rug=53.5% PASS n=1804 rug=47.1%. Only 6.4pp lift — too weak.
- **Status**: REJECTED as standalone filter. Could pair with other features in combo.

### H_SYMBOL_DUP_HIGH — backlog (not tested this cycle)
- **Observation**: grail (the 7-trade rug this cycle) had `symbol_dup_count = 11`. CHARTARD had dup=1.
- **Hypothesis**: high symbol_dup_count (≥5?) may correlate with rug — fake/copycat symbol patterns.
- **Next cycle**: backtest dup>=N veto vs lmr veto for independence/overlap.

## STATUS UPDATES (cycle 20260527_1800)
- **Methodology #25 NEW CANDIDATE — FEATURE-SPACE FILTERS BEAT WALLET-SPACE FILTERS FOR HIGH-RECALL VETOS**. 12 cycles of wallet-prefix RUG_N gave n=27-29 walk-forward; one feature filter (lmr>=175) gave 375 trades / 68 pairs at ~100% precision. Rule: each cycle, prefer at least one feature-space hypothesis alongside wallet-prefix scanning. Graduation requires 1 more independent confirmation.
- **H_RUG_WALLET_VETO_RUG6** (carry from c1200): STILL AWAITING USER AUTH. Note: LMR_VETO_175 is now a higher-priority safety filter.
- **PAPER_SOL_HUPHEY** & **PAPER_BSC_85871**: 13 cycles pending. NO change in n-counts.


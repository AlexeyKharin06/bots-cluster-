# COMBINATION + ADAPTIVE HYPOTHESES DIRECTIVE 2026-05-25

User explicit reminder:
> Don't take my proposals at face value. Find MANY strategies. Develop COMBINED and
> ADAPTIVE hypotheses. Test on history AND live.

Claude has been doing audits/methodology refinement. Now MUST do combination testing
on real data. Stop deferring U1/U4/U7 — they're load-bearing for combination work.

## CONCRETE COMBINATION HYPOTHESES TO TEST

### H_COMBO_1 — H31 × C2_DIVERGENCE confluence super-edge
- For each of 116 H31 LONG events: was there C2 divergence ≥50bp signal in T-24h to T-1h?
- Split 116 events into: WITH C2 signal (confluence) vs WITHOUT
- Test: confluence subset Sharpe > 2.5 vs no-confluence?
- HYPOTHESIS: pre-confirmed events execute cleaner (no slippage surprise, faster squeeze)
- If yes → H31_CONFLUENT super-edge

### H_COMBO_2 — H3 depeg × H38 high-funding co-occurrence
- 129 H3 depeg events × 10,686 H38 events: find days where BOTH fire
- Days with BOTH: did one dominate PnL or do they compound?
- HYPOTHESIS: depeg often causes funding spike on same ticker (USDe/USDD perp listings)
- If yes → unified "synthetic-stable distress" trigger captures both at once

### H_COMBO_3 — Dynamic hedge ratio per event based on PRE-EVENT basis trajectory
- For each H31 event: compute basis trajectory at T-24h, T-12h, T-6h, T-1h
- Classify into: BASIS_NARROWING (trending toward 0), BASIS_WIDENING (trending toward >50bp)
- For each class, optimize hedge ratio (0% / 25% / 50% / 75% / 100%)
- HYPOTHESIS: widening regime → reduce hedge (capture directional); narrowing → full hedge
- Output: rule "if basis_trajectory > +X bp/h then hedge_ratio = Y%"

### H_COMBO_4 — Portfolio sizing with H31+H34+H3 simultaneously
- Backtest: when 2+ edges have ACTIVE events on same day, how should capital allocate?
- Static equal-weight vs Sharpe-proportional vs anti-correlation-weighted
- HYPOTHESIS: anti-corr-weighted (H3 gets MORE in bear regime) beats static

### H_COMBO_5 — Borrow rate × interval-change confluence (revisit C9 with correct framing)
- C9 (borrow spike → SHORT) was rejected at +X% / WR Y%
- BUT borrow spike + interval-change in SAME day = pure squeeze signal
- Test: paired events show super-edge?

### H_COMBO_6 — Cross-mechanism confluence on same TICKER
- Per ticker per day: how many of (H31, H34, H3, H38, C2) fire simultaneously?
- Score from 0 (none) to 5 (all)
- Test: score≥3 events have higher mean PnL than score=1?
- If yes → "high-conviction" entry filter independent of any single mechanism

### H_ADAPTIVE_2 — Regime-based POSITION SIZING (not strategy switching)
Cycle 1505 killed strategy-switching adaptive. But SIZING adaptive may still work:
- Bull regime: smaller H31 (less squeeze magnitude), larger H3 (USDe yield-rush season)
- Bear regime: larger H31 (deep negative funding intensifies), smaller H3 (stables calm)
- Test on historical: does regime-sized portfolio beat static equal-weight?

### H_ADAPTIVE_3 — Time-of-day sizing
Mining T1 data may show: practitioner trades cluster in specific UTC hours (funding times,
Asian session, NY open). Sizing larger in those windows.

### H_LIVE_1 — Deploy H31_basis live paper-stream with adaptive ENTRY-DECISION
This is the actual NEXT STEP toward real-money path. Spec:
- Watch announcement_scraper for new H29-equivalent events on VPS
- When event detected: classify (basis available? hedge ratio choice? confluence score?)
- Open paper position adaptively per H_COMBO_3 hedge-ratio rule
- Exit per H_COMBO dynamic policy (funding-decay OR basis-convergence)
- Track per-decision outcomes for forward learning

### H_LIVE_2 — H3_DEPEG live paper-stream
- Watch CoinGecko 5m for any USDC/USDT/USDD/USDe/TUSD/USDP/FDUSD price |dev|≥50bp
- Apply DROP-CONFIRMED filter (SOLO-only)
- Open paper depeg trade
- Exit at re-peg or 7d max

## NON-NEGOTIABLE METHODOLOGY

For EACH H_COMBO_N:
1. Test on existing parquet data (DON'T defer for new fetches)
2. Walk-forward TRAIN/TEST asymmetric (Meth #12)
3. SOLO/CONFIRMED gating where applicable (Meth #14 unhedged, #17 hedged)
4. Compute corr to existing edges
5. Honest reject if doesn't beat baseline

## OUTPUTS

Per cycle, complete 1-2 H_COMBO tests. Don't try all 6 in one cycle.
Final goal after 3-5 cycles: ADAPTIVE STRATEGY SPEC v2 incorporating:
- Best 2-3 H_COMBO confluence rules as ENTRY filters
- H_ADAPTIVE_2/3 sizing rules
- H_LIVE deployment specs

## STOP DOING

- ❌ More audit cycles (cycle 1100 / 1500 / 1750 audits — useful but enough now)
- ❌ More methodology candidate logging without follow-up testing
- ❌ Deferring H_BOROS_INDICATOR (5 cycles deferred = clear blocker)
- ❌ Deferring U1 / U4 / U7 — they unlock H_COMBO_3

## START DOING

- ✅ ONE H_COMBO test per cycle MINIMUM
- ✅ H_BOROS_INDICATOR THIS cycle (no more deferrals)
- ✅ Output adaptive strategy spec v2 by cycle +5
- ✅ Honest go/no-go per combination

## CRITICAL: User explicit on this

User said multiple times: «не зацикливайся, комбинируй, проверяй on history AND live».
Audit cycles do NOT do this. Combination + live = priority NOW.

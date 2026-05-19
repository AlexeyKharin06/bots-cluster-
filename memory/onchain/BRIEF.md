# BRIEF — onchain AI brain (last update: cycle 20260519_1800)

## Current state (live)
- closed=4999 rows, **but only 683 unique tokens** (avg 7.32 rows/token from stream tag duplication). open=1.
- Per-token Solana baseline: avgPnL=-41.5%, WR=17.8%, rug=51.1%, big=1.7%.
- Span: 2026-05-11 → 2026-05-19T17:51. State unfrozen this cycle (+42 new rows / 18 new unique tokens since cycle_1702).
- **Last-12h regime is catastrophic**: baseline -73%, last 6h -94%. NO known signal helps. Possibly macro or sniper-side.

## Methodology fix this cycle (critical)
**Per-token, not per-row, is the correct unit for filter analysis.** Wallet-whitelist constructions that required n≥k per wallet were inflated 7-10× by stream-tag duplication. Going forward: dedupe by `token` (first entry kept), then split walk-forward, then evaluate filters.

## Paper streams in flight
**NONE.** No hypothesis meets strict +150% avg gate. Several candidates clear risk-adjusted thresholds (rug halved, big% lifted) — pending user decision on alternative gate (carrying since 1639).

## Last validated hypothesis & key cycle findings
- **cycle_20260519_1800**: H_LP_WHITELIST **REJECTED — counting inflation** (TRAIN whitelist=1 wallet, TEST hits=0 after per-token dedup). Surviving per-token signals: **H_LP_HIST** (lp_hist.pumped_alive≥1; TEST n=22, avg=-41 vs base -62, rug=32 vs 58, big=4.5 vs 0.8), **H_DISTRIB** (top1<27; TEST rug=22 vs 58), **H_LOCKED** (lp_unlocked=false; TEST rug=33 vs 58). Best composition: LP_HIST+QUIET (n=13, big=7.7%, rug=23%). See [cycle_20260519_1800.md](insights/cycle_20260519_1800.md).
- **cycle_20260519_1702**: H_RUG_PC REJECTED — hindsight leakage. cr_hist.pumped_alive≥1 confirmed NEG-veto.
- **cycle_20260519_1639**: original LP-whitelist claim (now retracted).

## Planned for next cycle
1. **tokens_unified.json deep-dive** (34K classified Solana tokens with `added_at`/`updated_at`). Cross-ref against our 683 unique tokens with strict `updated_at < entry_time` filter (avoid H_RUG_PC trap). Rich metrics: `db_rugBotCount, db_serialRugCount, db_smartMoneyBuyVol, db_highRiskWalletCount, db_positiveWalletCount, db_bundleDetected, ohlcv_athGain, serial_pump_count, sniper_count`.
2. Re-run surviving per-token signals with fresh data window.
3. Regime-guard hypothesis: is there a feature that predicts current hour's baseline? If avg-last-N-baseline < -60%, pause new entries.
4. ULTRA_TRIPLE and H2 new streams — analyze when more rows.

## OPEN QUESTIONS to user
1. **NEW: SMART_COPY duplication** — SMART_COPY/SMART_COPY_TOP and SMART_COPY_AGE5/SMART_TOP_AGE5 produce numerically-identical metrics on the same tokens. Intentional A/B or duplicated specs?
2. **NEW: Last-12h carnage** (baseline -73%, last-6h -94%). External cause (BTC dump, Solana congestion, RPC issue) or sniper-side bug? Pause paper-stream proposals until normal?
3. **NEW: ULTRA_TRIPLE & H2 stream filter logic** — can you share the spec? Helps interpret performance.
4. **Carrying (1639): Strict gate** (n≥50, avgPnL≥+150%, WR≥60%, rug≤25%) blocks risk-adjusted edges where rug is halved + big% is lifted but avg stays sub-150 due to exit logic. Alternative Sharpe/expectancy gate?
5. **Carrying (1639): BSC_FILTERED / SMART_CLUSTER** — both produced NO rows in last 10.5h. Killed already, or dormant?
6. **Carrying (1639): bonding_curve_buyers** field empty in samples — populated downstream or never?
7. **Carrying (1702): rugger_blacklist refresh policy** — for time-aware use, can entries carry `wallet_added_at`?

## Rejected this cycle (1800)
- **H_LP_WHITELIST** — counting inflation via stream duplication (row-basis 24 wallets → per-token 1 wallet; TEST hits=0). Was claimed edge of cycle_1639; retracted.

## Known catalogue of leakage forms (apply to every hypothesis)
1. **Hindsight classifier** (cycle_1702 H_RUG_PC): external DB built with post-test info. Test: decontamination split (CLEAN vs DIRTY by overlap with our trade tokens).
2. **Counting inflation** (cycle_1800 H_LP_WHITELIST): row-stats over stream-duplicated data. Test: per-token dedup.
3. **Time-localization artifact** (cycle_1639 1AR wallet): aggregate alpha from a single day. Test: per-day breakdown.
4. **Post-entry feature** (cycle_1639 ride_mode): flag set after entry. Test: check field is populated pre-trade.

# BRIEF — onchain AI brain (last update: cycle 20260519_1826)

## Current state (live)
- closed=4624 Solana rows / **584 unique tokens** (per-token dedup, avg ~7.9 rows/token). open=many (sniper running live).
- Per-token baseline (last ~17h TEST window): n=117 avg=-68.9% WR=11.1% rug=65% **big%=0 huge%=0**.
- Span: 2026-05-11 15:33 → 2026-05-19 19:17. State growing live (sniper on VPS).
- **Regime carnage persists**: TEST window 0 big-winners, 0 huge-winners. Cycle_1800 flagged 12h baseline -73%; today's 17h window confirms — possibly macro, sniper-side, or both. No filter on top of zero base rate can pass the +1M%-aligned fat-tail gate.

## Goal (user-updated cycle_1826)
**+1,000,000% (×10K)** via 6-8 reinvested compounding wins. Implication: big%/huge% > avgPnL; strict +150% promotion gate should be replaced by expectancy/Kelly-based gate. Carrying open question since 1639.

## Paper streams in flight
**NONE.** Two candidate families exist but neither cleared this cycle:
- Per-token validated edges (H_LP_HIST, H_DISTRIB, H_LOCKED) — risk-adjusted, halve rug, lift big% 4-6×, **regime blocks fat-tail signature** in current TEST window.
- TG channel paper-streams — **none possible** (cycle_1826 NULL_TG_LEAD; see below).

## Last validated hypothesis & key cycle findings
- **cycle_20260519_1826**: TG channel walk-forward → **NULL_TG_LEAD REJECTED**. 3 of 584 trade tokens overlap TG signal corpus; 0 with pre-entry mention. Sniper is upstream of TG corpus. `channel_pump_predictiveness.json` also degenerate (33/35 channels pump_rate=0). New: **H_TG_AS_EXIT** parked (mention-during-hold as exit signal — needs instrumentation). See [cycle_20260519_1826.md](insights/cycle_20260519_1826.md).
- **cycle_20260519_1800**: H_LP_WHITELIST REJECTED — counting inflation. Surviving per-token signals: H_LP_HIST, H_DISTRIB, H_LOCKED. Best comp: LP_HIST+QUIET (n=13, big=7.7%, rug=23%).
- **cycle_20260519_1702**: H_RUG_PC REJECTED — hindsight leakage in rugger_blacklist. cr_hist.pumped_alive≥1 confirmed NEG-veto (H_CR_HIST_NEG).
- **cycle_20260519_1639**: original LP-whitelist claim (retracted in 1800).

## Planned for next cycle
1. **Formalize expectancy/Kelly gate** to replace strict +150%. Apply retroactively to H_LP_HIST + H_DISTRIB + H_LOCKED + H_CR_HIST_NEG to see if any qualifies under new gate. No new data needed — code-only.
2. **Symmetric null-check on pumpfun_monitor.js + dexscreener_signals.json**: same walk-forward template as TG. Likely also null (sniper is faster than these feeds) but worth confirming so we stop suggesting it.
3. **tokens_unified.json deep-dive (carrying from 1800)**: 32K classified tokens with `updated_at`. Strict `updated_at < entry_time` cross-ref against our 584 trade-tokens. Rich features: `db_rugBotCount, db_serialRugCount, db_smartMoneyBuyVol, db_highRiskWalletCount, db_positiveWalletCount, db_bundleDetected, ohlcv_athGain, serial_pump_count, sniper_count`. **MUST run decontamination split** (avoid H_RUG_PC trap).
4. **Regime-guard**: if avg-last-N-baseline < -60%, freeze paper-stream proposals until normal. Quick code-only fix; prevents premature gate evaluation.
5. **H_TG_AS_EXIT instrumentation spec**: write the patch for `serial_sniper.js` to populate `first_tg_mention_ts` per open position from `realtime_signals.jsonl` tail. User applies.

## OPEN QUESTIONS to user
1. **CARRYING (1800): SMART_COPY duplication** — SMART_COPY/SMART_COPY_TOP and SMART_COPY_AGE5/SMART_TOP_AGE5 produce numerically-identical metrics. Intentional A/B or duplicated specs?
2. **CARRYING (1800): Last-12h+ regime carnage** (now confirmed in 17h window — TEST big%=0). External (BTC, Solana congestion, RPC) or sniper-side? Should new entries be paused (regime guard) until normal?
3. **CARRYING (1800): ULTRA_TRIPLE & H2 stream filter logic** — share spec to interpret performance.
4. **CARRYING (1639/1800): Strict gate vs expectancy/Kelly** — given +1M% goal pivot, can I formalize alternative gate next cycle?
5. **CARRYING (1639/1800): BSC_FILTERED / SMART_CLUSTER dormant** — killed or just sleeping?
6. **CARRYING (1639): bonding_curve_buyers field empty** — populated downstream or never?
7. **CARRYING (1702): rugger_blacklist refresh policy** — can entries get `wallet_added_at` for time-aware use?
8. **NEW (1826): H_TG_AS_EXIT instrumentation** — OK to write a spec patch that tails `realtime_signals.jsonl` and writes `first_tg_mention_ts` onto open_positions? User applies manually.

## Rejected this cycle (1826)
- **H_TG_LEAD** — TG corpus is reactive, not predictive. 0/584 pre-entry overlap. Confirms a structural property of the corpus, not a methodology bug.

## Known catalogue of leakage forms — unchanged this cycle
1. Hindsight classifier (cycle_1702 H_RUG_PC)
2. Counting inflation (cycle_1800 H_LP_WHITELIST)
3. Time-localization artifact (cycle_1639 1AR wallet)
4. Post-entry feature (cycle_1639 ride_mode)

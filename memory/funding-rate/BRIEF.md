# BRIEF — funding-rate snapshot

## State (updated 2026-05-21)
- ✅ Migrated to VPS. All 5 paper-bots run on VPS (PIDs 166482, 166499, 166516, 167026, 167035)
- ✅ Backtest data on VPS: parquets 11MB + xlsx + jsonl (/srv/bots/funding-rate/code/data/)
- ✅ Custom funding_brain_cycle.sh (NOT shared/onchain) with full-autonomy prompt
- ✅ NEW: Info/ materials from practitioners (funding prediction site code) at /srv/bots/funding-rate/code/Info/
- ✅ Sync VPS→PC hourly (backup)
- ⚠️ feed_funding.jsonl=0 (TG signals_master 501 msgs but no funding keywords — user has only OnChain/Bot/crypto folders, no funding folder)

## CRITICAL NEW HYPOTHESIS — H32 (priority TEST next)
**Predictive funding-pay scalping** based on practitioner site formulas:
- Read live premium-index WebSocket per exchange
- Compute predicted funding using exchange's own formula 60s before T
- Arm SHORT/LONG, exit at T+30s
- Materials + algorithm in `PRACTITIONER_FUNDING_PREDICTION_ALGORITHM.md`
- Files: `/srv/bots/funding-rate/code/Info/`

Difference from KILLED fair-price scalping:
- Old: triggered on REST funding rate (60s lag)
- New: triggers on PREDICTED funding using live WebSocket premium stream
- Has up to 2min lead time before official rate sets

## Validated negatives — DO NOT retest
- interval-prediction (2-9% live precision, was 96% with survivorship bias)
- fair-price scalping LAGGED (0/5 weeks walk-forward)
- listing momentum (32% win, -$11/90d)
- microcaps expansion (DEGRADES 86%)

## Untested hypotheses backlog (priority)
1. **H32 PREDICTIVE FUNDING-PAY** (NEW — practitioner-validated formula, top priority)
2. H29 Exchange-API funding poller (proposed last cycle — partly subsumed by H32)
3. H30 Basis spot-vs-perp scanner
4. H31 Interval-shortening v2 from API events
5. Whale copy-trade
6. Confluence SHORT-only

## Next AI brain cycle action
Read Info/files/module.js (de-obfuscate), write predictive_funding_paper.py implementation. Start with Binance only as MVP, expand to other 5 exchanges once accuracy verified.

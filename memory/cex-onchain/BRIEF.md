# BRIEF — cex-onchain AI brain (migrated 2026-05-20 from D:\CEX-Onchain)

## Current state (live)
- 9 trade slots deployed: C/B/U/A/T/A2/K/S/M, total 100% capital, DRY_RUN=True
- 21 trades closed total. Last: TRAC stop_loss -$67.77 (cycle 2 trigger).
- Bot still on local Windows? **NO** — migrated to VPS. Cron `0 3,9,15,21 UTC` from now on.

## Goal
Прийти к READY FOR LIVE verdict (8/8 criteria). Сейчас 3/8.
Главный блокер: историческая UPEG#1 -$3,482 (от 05-05, до фиксов) в rolling window.

## Last validated work
- **Cycle 1** (05-18): Triple AND combos — deployed slot U (max_dep≥30 AND n_addr≥3 AND pos_7d≤50). WF 5/5 +29%.
- **Cycle 2** (05-19): chg_24h≤0 filter for slot A (would have prevented TRAC loss). WF 5/5 +27%.
- **Cycle 3** (05-19): same filter to A2/T/M. All WF 5/5 with +6-7pp improvement.

## Next focus (cycle 4+)
1. OR combo grid search (alternative to AND structures)
2. Per-token live PnL audit (any consistent loser to blacklist?)
3. Slot S — add chg_24h≤0 too? (not tested yet)
4. Check stuck positions >5 days
5. ML approach with more features (cycle 1 ML had AUC 0.566 — too marginal)

## OPEN QUESTIONS to user
- None pending — runs autonomously

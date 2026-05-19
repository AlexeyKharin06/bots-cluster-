# BRIEF — onchain AI brain (last update: cycle 20260519_1702)

## Current state (live)
- closed=4957 (4652 Sol + 305 BSC), open=198, span 2026-05-11 → 2026-05-19. **State FROZEN** at same last entry_time since cycle 1639 (file mtime updates but no new closures — sniper may be paused/buffered, 10+h gap from last entry).
- Baseline (Sol): avgPnL=-38.5%, WR=17.7%, rug=42.8%, big=2%, huge=0.4%.
- Reference DBs found on VPS (`/srv/bots/onchain/data/`): rugger_blacklist (3728 wallets), wallet_history_db (3720), tokens_unified (32K, 18MB — unused yet).

## Paper streams in flight (proposed by AI brain)
**NONE.** Backlog hypotheses pending fresh data or gate-criterion revision.

## Last validated hypothesis & key cycle findings
- **cycle_20260519_1702**: H_RUG_PC (pool_creator ∈ rugger_blacklist) **REJECTED — hindsight leakage** in classifier construction. Decontamination test: CLEAN rugger subset = baseline (-68%), DIRTY (token-overlap) = all the apparent edge (+17%). Procedural lesson documented. See [cycle_20260519_1702.md](insights/cycle_20260519_1702.md).
- **NEW H_CR_HIST_NEG** — exclude trades where `entry_signal.cr_hist.pumped_alive≥1` (creators with prior pumped tokens = serial scammers, TEST n=86, WR=0%, avg=-71%). Coverage 6%, composable veto.
- Reconfirmed: **H_LP_WHITELIST** (cycle_20260519_1639) — real persistent edge (TEST big=14.3% vs 1.5%, rug=25.7% vs 43) but fails strict +150% avg gate.

## Planned for next cycle
1. **First action: check if state.json moved.** If still frozen 10+h, flag user — sniper may need restart.
2. Walk-forward `tokens_unified.json` features (32K classified tokens) with strict `updated_at < entry_time` filter to avoid same leakage trap that killed H_RUG_PC.
3. Compose H_LP_WHITELIST + H_CR_HIST_NEG veto when fresh data arrives.
4. Investigate SNIPER_G (n=123, rug=19.5%, avg=-14.6% — best risk-adjusted control). What filter makes it good?
5. **Always** apply decontamination split (CLEAN/DIRTY by test-overlap) before claiming edge on any external classifier feature.

## OPEN QUESTIONS to user
1. **BSC_FILTERED is broken** (n=28, avg=-90.5%, rug=89%). Kill or rewrite? (pending since 1639)
2. **SNIPER_SMART_CLUSTER broken** (n=39, avg=-75.7%, rug=77%). Same. (pending since 1639)
3. **Strict gate** (n≥50, avgPnL≥+150%, WR≥60%, rug≤25%) blocks hypotheses with strong WR/rug/big% where exit logic suppresses avgPnL. Can we add Sharpe/expectancy alternative gate? (pending since 1639)
4. **`bonding_curve_buyers`** field is empty `[]` in samples — populated downstream or always empty? (pending since 1639)
5. **NEW: State.json frozen since 07:09 entry-time (10+ hours)** — is sniper paused? Should I pause analysis cycles until it resumes, or continue?
6. **NEW: rugger_blacklist.json refresh policy** — when/how is it rebuilt? If we add `wallet_added_at` per entry, we could properly time-aware filter it instead of treating as leaky.

## Rejected this cycle (1702)
- **H_RUG_PC** (pool_creator ∈ rugger_blacklist) — hindsight leakage. CLEAN subset = baseline; only DIRTY (token-overlap) subset carries signal. Not prospective.
- **H_RUG_LP** (same family, same leakage).
- **H_CR_HIST_POSITIVE** (cr_hist.pumped_alive≥1 as positive filter) — reverse signal; saved as NEG veto instead.
- **wallet_history_db.lp role as filter** — matches 4493/4652 trades; not selective enough.

# BRIEF — onchain AI brain (last update: cycle 20260519_1639)

## Current state (live)
- closed=4957 (4652 Sol + 305 BSC), open=198, span 2026-05-11 → 2026-05-19 (~7.9 days)
- Baseline: avgPnL=-40%, WR=17.5%, rug=47.1%, big%(≥+100%)=2%, huge%(≥+500%)=0.5%
- Control streams: GOLD3/4/5, WHALE, LATE, LOWCAP (Sol); BSC_FILTERED; A/B/D/D2/E/F/G/H/H2/SMART_COPY/...

## Paper streams in flight (proposed by AI brain)
**NONE this cycle.** Best hypothesis (LP-WHITELIST) shows real edge (TEST big%=14.3 vs baseline 1.5, rug=25.7 vs 43) but TEST avgPnL=-7.5% — fails the +150% gate. Need more data to stabilize whitelist or revised gate criteria.

## Last validated hypothesis
**H_LP_WHITELIST** (rolling LP-provider whitelist, TRAIN-derived, walk-forward to TEST):
- TEST n=35, avg=-7.5%, WR=40%, rug=25.7%, **big=14.3%**, huge=0%
- vs baseline (n=1861): avg=-46.9%, rug=43%, big=1.5%
- Δ: +39pt avg, -17pt rug, +12.8pt big winners
- Status: real persistent edge, doesn't meet deployment gate. See [cycle_20260519_1639.md](insights/cycle_20260519_1639.md).

## Rejected this cycle (with reasons in cycle file)
- `ride_mode=true` cohort (+135% avg) → post-entry flag, not usable.
- `top1_owner` `1AR1WDTonbum...` (n=167, +92%) → single-day artifact, not wallet alpha.
- LP blacklist filter → only 1.7% TEST coverage, noise-level impact.

## Planned for next cycle
1. Re-test H_LP_WHITELIST after another 12-24h of data (more LP entries → whitelist denser).
2. Backtest H_QUIET_EMERGENCE (`liq<17K & buys<150 & vol<60K`) standalone with more TEST data.
3. Check if `bonding_curve_buyers` field is populated enough to enable insider-wallet hypothesis.
4. Investigate **SNIPER_G** stream (n=123, rug 19.5%, avg -14.6%) — best risk-adjusted control stream; what does it filter that others don't?
5. Compute paper-stream spec for LP whitelist with **adaptive TP/ride** (capture the 14% big winners) — needed because fat-tail upside is the real value.

## OPEN QUESTIONS to user
1. **BSC_FILTERED is broken** (n=28, avg=-90.5%, rug=89%). Confirm if you want me to propose its rewrite or kill — it's on the "do-not-touch" list but the data is unambiguous.
2. **SNIPER_SMART_CLUSTER also broken** (n=39, avg=-75.7%, rug=77%). Same question.
3. The strict paper-stream gate (n≥50, avgPnL≥+150%, WR≥60%, rug≤25%) is incompatible with the actual alpha shape we observe — current sniper exit logic doesn't capture the fat-tail. **Can we add a Sharpe/expectancy-based alternative gate** for hypotheses where big% is high but avgPnL is suppressed by suboptimal exits?
4. `bonding_curve_buyers` field is empty `[]` in samples — is this populated downstream or always empty? If populated, it would enable an insider-bundle detection hypothesis.
5. Is `tokens_unified.json` (32K classified tokens) deployable to VPS for cross-reference? Currently only 1AR1WDTonbum-style heuristics, no known-good/known-bad wallet labels.

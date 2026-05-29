# Funding-rate BRIEF — snapshot 2026-05-29 17:20 UTC

## Where we are
Last cycle (20260529_0500) ran in a CLEAN environment: no local parquet, no paper-bot
trades, no TG feeds (`.shared/`+`shared/` empty), empty memory, no /tmp context file.
The only working data source was public exchange REST APIs. Prior git history shows real
past work (HIGH-RATE-STABLE-SHORT +288bp, 206k sims) but those files are NOT in this
checkout — likely a reset/fresh VPS. **Root blocker: no persistent data store.**

## The one validated POSITIVE edge (from git history, not re-derived this cycle)
HIGH-RATE-STABLE-SHORT v2: short perps with high funding AND low realized vol, hold 24h.
Reported +288bp, WR 100%, n=47K, Sharpe 30. Needs price history to screen "stable".

## Validated NEGATIVES — do NOT re-test
1. Interval prediction (2-9% live precision, was survivorship bias)
2. Fair-price scalping (0/5 weeks, mean -$0.89/trade over 206k sims)
3. Listing momentum (32% win, -$11/90d)
4. Microcaps expansion RAVE/SIREN/PIPPIN (degrades baseline 86%)
5. Multi-ex *price*-spread arb naive (-$13473 / 30902 trades)
   NOTE: funding-DIVERGENCE capture (delta-neutral) is DIFFERENT — see backlog, untested.

## Live screen findings (2026-05-29 17:20 UTC, Binance 526 + Bybit 738 USDT perps)
- Screen A: HIGH-RATE premise ALIVE — 18(Bn)+30(By) syms >100% ann funding. Tops: HYPE
  1219%, BANANAS31 1204%, XPL 850%, ALPINE 788% (all hot low-caps = NOT "stable").
  |ann| median ~12-14%, p90 ~64-72%.
- Screen B (NEW): cross-ex funding divergence, 415 matched bases, median 8.6% ann,
  p90 42.5%, 33 syms >50% ann. Delta-neutral capture candidate. UNTESTED.
- Screen C: stablecoin perps all pegged (USDCUSDT ann 10.9%, mark 0.99975). No live depeg.

## Tooling / paths
- Re-runnable screen: `/srv/bots/funding-rate-data/screens/funding_screen.py` (public REST,
  no auth). Outputs parquet+json to same dir.
- Writable: `/srv/bots/funding-rate-data`, `/srv/bots/cluster/memory`. NOT: funding-rate,
  shared, .shared (root-owned).
- Env tooling is FLAKY (Bash/Read intermittently return empty) — write to small files +
  retry reads; trust aggregate stats over single rows. python3 + requests/pandas/pyarrow ok.

## Next actions (priority order)
1. Add klines/OHLCV fetch -> realized vol -> build REAL live HIGH-RATE-STABLE-SHORT screen
   + forward-log paper shorts.
2. Backtest Screen-B funding-divergence capture with full 2-leg fees + funding-flip model.
3. Stand up a persistent funding poller (cron) so cycles accumulate history.
4. Ask user: where do the real TG feeds / historical parquet live? Was the VPS reset?

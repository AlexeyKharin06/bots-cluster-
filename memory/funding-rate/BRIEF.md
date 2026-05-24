# BRIEF — funding-rate snapshot (post-cycle 20260524_1700)

## Status: 3-edge portfolio VALIDATED + REGIME-AGNOSTIC + EXTERNAL RECON COMPLETED. HARDEN-AND-DEPLOY phase continues.

## Validated edges (unchanged from cycle 1505)

| Edge | n | Mean | WR | Sharpe | corr to H31 |
|---|---|---|---|---|---|
| H31 basis-hedge | 116 (LONG-only) | +3.52% | 100% | 1.84 | — |
| H34 perp-perp | 101 | +1.28% | 79% | 0.82 | +0.30 |
| H3 50bp depeg (post-vet) | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| H3 75bp depeg (operational tier) | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H38 mag-trigger | 10,686 | +2.02% | 99.7% | 1.27 | — |

All edges regime-agnostic (cycle 1505) at <6% relative PnL difference across BTC bull/bear/chop.

## Findings from cycle 1700 (external strategy reconnaissance)

- **H_BOROS_YU_ARB filed** — Pendle Boros (Arbitrum, early 2025 launch) tokenizes funding-rate streams as Yield Units (YUs). A 4-leg synthetic (short HL-YU + short HL perp + long Binance-YU + long Binance perp) collects FIXED funding-rate-SPREAD between two venues with no BTC/ETH price exposure. Documented avg 5.98–11.4% Fixed APR Oct-Nov 2025, peak 23.5–48%. **New mechanism class** (interest-rate-swap basis, not perp-perp delta-neutral funding capture). Infra blocker: no Arbitrum execution.
- **H_BOROS_INDICATOR sub-hypothesis** — even without execution, read-only Boros YU implied APR via Arbitrum RPC could serve as leading indicator for H34 entries (market's consensus on future funding gap). 1-2h engineering. Next-cycle priority #1.
- **H_DEX_DEX_PERP filed** (modest priority) — external sources document persistent DEX↔DEX perp price spreads (Drift/Hyperliquid/Paradex/Backpack). Universe overlap with our chronic-discount alts is low (DEX perps mostly BTC/ETH/SOL); deprioritized.
- **OBS_FAIRPRICE_V6 noted** — paper_fairprice_v6 on VPS shows 31 trades / 84% WR / +$2.80 net, all SHORT on micro-caps (BOBBOB×4, STEEM) at high realized funding rates (0.66–1.49%) with very short holds (5–300s). Apparent conflict with R2 rejection. Likely survivor bias on chronic-discount cluster (probability 60%); revisit at n=100 or 2 wks more data.

## Active to-do (priority order — re-ordered post-1700)

1. **H_BOROS_INDICATOR prototype** — Arbitrum RPC client + Boros YU price fetcher; backtest signal on H34 entries. Free option-value extraction; no execution risk. ~2h.
2. **T1 mining** — STILL the binding constraint for adaptive analyses (per cycle 1505). Defer no more than 1 more cycle.
3. **R2 SOLO retest** — apply Meth #17 lens to mega_fairprice_backtest.parquet (316k events).
4. **C8/H38 Meth #14 retro** — corroborate/refute Meth #17 candidate on 10,686 H38 events.
5. **Pi2 paper retrieval** — alternate-path retrieval to ground DEX↔DEX numbers.
6. **paper_fairprice_v6 deep-dive** — IF n reaches 100 organically.
7. **H_TG_ROUTING_PATCH** — still pending user OK (shared infra).
8. **GitHub direct search** — open-source funding-arb implementations.

## Known caveats (preserved)

- Paper-stream deployment STILL pending user OK (cycle 1100/1700 readiness call).
- H3 concentration: USDe+USDD 73.6% of events post-vet.
- H31 coverage gap: 30% of practitioner FB cases match our 50-symbol universe (cycle 1435 finding).
- Boros backtest window (Oct-Nov 2025) is short — single bull→chop transition, no bear regime sample. Provider-claimed APRs may be regime-specific.

## DO NOT
- Do not propose real-money paper-stream deploy without user OK.
- Do not write Boros execution code without user OK (Arbitrum infra is new attack surface).
- Do not collapse 3-edge portfolio into a single composite.
- Do not retest H_adapt_1..3 as edge-selectors (REJECTED with conviction at n=10,686).

## Available data (on VPS, unchanged)

- code/data/: multi_ex_funding_180.parquet (1.6M rows), mega_fairprice_backtest.parquet, c2_wide.parquet, tg_messages_historical.jsonl (3036), tg_trade_cases.jsonl (80), media_signals_historical.jsonl (571), borrow_histories.jsonl (45), expansion_funding.parquet
- /tmp/: h31_net.parquet (154), h3_events_24mo.parquet (150), c8_fwd.parquet (10,686), btc_daily.parquet, btc_regime_cases.parquet (80), t2_classified.jsonl (80), m3_h31_categorized.parquet (116)

## Cycle priority NEXT: H_BOROS_INDICATOR prototype (free option-value extraction)

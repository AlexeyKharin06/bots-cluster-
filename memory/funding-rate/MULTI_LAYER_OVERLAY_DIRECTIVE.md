# MULTI-LAYER OVERLAY ANALYSIS DIRECTIVE 2026-05-24

User explicit follow-up after CRITICAL_INSIGHT:

> «overlay multiple charts (index price, spot, futures, payment times, borrow rates)
> find correlations. You should find this all yourself.
> Main thing — don't get stuck. Combine, add, make adaptive.»

## Required overlay layers (use these together, NOT independently)

For each ticker/event/window, overlay:

1. **Spot close price** (per exchange)
2. **Perp close price** (per exchange)
3. **Index price** (mark-price - basis component, available from /fapi/v1/premiumIndex)
4. **Funding rate** (per exchange, per period)
5. **Funding interval / next funding ts** (when payment happens)
6. **Borrow rate** (Bybit available; estimate others from open-interest cost-of-carry)
7. **Open interest** (per exchange, per period)
8. **Volume** (per exchange, per period)
9. **Bid/ask** (live only — initiate L1 collection daemon NOW)
10. **Cross-exchange basis** (perp_A - perp_B, spot_A - spot_B, perp_A - spot_B all variants)

## Correlation matrix to compute per H31 event

For each of 116 H31 events, in window [-24h, +12h]:
- Pearson corr between EVERY pair of (layer_i, layer_j) above
- Lag correlation: does layer X at t-Δ predict layer Y at t for various Δ?
- Identify the LEADING indicator (changes first) and LAGGING indicator (changes last)
- HYPOTHESIS: cross-ex basis is a LAGGING indicator of funding intensification;
  premium-index divergence is LEADING

## Pattern overlay test

For each event, plot all 10 layers on same time-axis:
- Where do peaks/troughs align?
- What's the typical sequence of events? (e.g., OI rises → premium widens → funding extreme
  → interval shortens → basis explodes → squeeze plays out)
- If sequence is consistent across events → it IS the pattern → we can predict each step
  from preceding step

## Combinations to try

- LONG perp on shorter-interval + SHORT perp on longer-interval (user's strategy)
- LONG spot + SHORT perp (capture basis closing, opposite direction)
- LONG perp + LONG spot 2x leverage (directional bet on squeeze without hedge)
- Pair trading: LONG BTC + SHORT ETH if cross-pair basis shows anomaly
- Listing pair: new perp on Bybit + spot still only on Binance — basis on listing

## Adaptive switching logic

When you have classified each event as F/B/FB/L/O (mechanism):
- If event matches PATTERN_A (e.g., funding-dominant): execute STRATEGY_A
- If matches PATTERN_B (e.g., basis-dominant): execute STRATEGY_B
- Don't fix on one — let regime decide

Output one combined adaptive strategy spec with decision tree.

## DO NOT

- Don't analyze only close-price (use OHLC at minimum, bid/ask if available)
- Don't fix on funding-only edge (basis is its own game)
- Don't get stuck on perfect data — work with what we have, identify gaps for L1/L2 collection
- Don't propose paper-stream until you have a CONCRETE adaptive strategy spec
- Don't ignore listing/depeg/other patterns — they're in TG cases, mine them

GO.

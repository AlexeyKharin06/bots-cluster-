# 🔬 MICROSTRUCTURE DEEP-DIVE DIRECTIVE (user-prompted 2026-05-24)

> User point: «не только funding capture — basis РАЗОРВЁТ при interval shortening +
> negative funding, потому что шорты cover → BUY perp. Можно captured directional gain
> BOLLE funding. Plus orderbook, market phases, velocity — всё анализировать».

User критикует что мы тестировали ТОЛЬКО binary hedge (0% или 100%) и игнорировали:
- Partial hedge ratios
- Basis dynamics как separate edge
- Orderbook / market microstructure
- Market regimes
- Order flow signals

## Concrete hypotheses to test (priority order)

### M1 — Partial hedge ratio sweep on H31 events
- 116 LONG-only H31 events × hedge_ratio ∈ {0%, 25%, 50%, 75%, 100%}
- Для каждого: compute funding PnL + price PnL (already in /tmp/h31_klines.parquet)
- Find Sharpe-optimal ratio
- HYPOTHESIS: 50% hedge captures funding (~50% × 3.45% = 1.7%) + half-basis-widening
  (typically 1-3% directional in short-squeeze regime) = TOTAL может быть +3-5% с lower variance
- If ratio < 100% beats 100% on Sharpe → DEPLOY as H31_PARTIAL

### M2 — Basis widening as SEPARATE edge (decompose existing data)
- Из 116 events извлечь: для каждого вычислить
  - basis_t0 = perp_price - spot_price на event_ts
  - basis_t+4h после hold
  - basis_widening = (basis_t+4h - basis_t0) / spot_price
- Test direct trade: LONG perp + SHORT spot (1:1) для capture ONLY basis (не funding)
- Если mean basis widening > 50bp и WR > 70% → BASIS_PURE как separate edge
- HYPOTHESIS: short-squeeze post-interval-shortening drives perp +1-2% above spot

### M3 — Methodology #14 retro на H31 events (от Claude же)
- Same logic как H3 SOLO vs CONFIRMED
- Для каждого H31 event: классифицировать как SOLO (одна биржа shortens) vs CONFIRMED (≥2 биржи same day на same coin)
- HYPOTHESIS: SOLO events captured более чистый mean-rev (no systemic stress); CONFIRMED = systemic pressure
- Test: split 116 events, compare H31 PnL per category
- Если SOLO subset показывает Sharpe > 2.5 → H31_SOLO как narrower-but-cleaner edge

### M4 — Market regime conditioning
- Для каждого H31 event: tag BTC regime at event_ts
  - BULL: BTC 7d change > +5%
  - BEAR: BTC 7d change < -5%
  - CHOP: |BTC 7d change| ≤ 5%
- Split 116 events × 3 regimes, compute mean PnL per regime
- HYPOTHESIS: H31 может работать differently в bull vs bear (shorts pile in more in bear → bigger squeeze → bigger basis widening → better PnL)
- Use multi_ex_funding_180.parquet binance BTC subset for regime tag

### M5 — Pre-event microstructure features as FILTER
- 30min before event_ts, для primary exchange:
  - Open Interest velocity (delta in last 1h, 4h, 24h)
  - Premium-index magnitude
  - Volume vs 30-day avg
- HYPOTHESIS: events with HIGH OI velocity + extreme premium = больше short-positioning to squeeze = bigger H31 PnL
- Test as Sharpe-improving filter (drops bottom 30% events)

### M6 — Orderbook depth proxy via Binance/Bybit depth API
- For NEXT batch of H31 events (live monitoring): snapshot orderbook depth at event_ts
- Compute: realistic slippage at $1k, $10k, $100k notional
- Backtest: assume worst-case slippage from depth → recompute net PnL
- If realistic slippage < 50bp at $10k → safe to scale notional 10x

### M7 — Funding velocity as primary trigger (no interval-change needed)
- Из 1.6M funding rows: find spikes WHERE rate changes by ≥100bp between consecutive periods on same (ex, sym)
- These are "funding velocity events" — same mechanism (overcrowded one side, about to squeeze)
- Test as wider edge than H31 (intervals don't change daily but rate can spike daily)
- HYPOTHESIS: catches H31-like setups without needing interval-change trigger

## Expected outcomes

If M1 (partial hedge) shows ratio < 100% beats 100% by 30%+ on Sharpe →
**H31 PnL upgrade from 3.45% → 5%+** на тех же 116 events. Это +44% improvement.

If M2 (basis pure) shows mean > 100bp & WR > 80% → **NEW Edge 5** (basis directional play
post-shortening). Doubles portfolio depth.

If M3 (Meth #14 on H31) shows SOLO subset Sharpe > 3.0 → **Cleaner H31 variant** + general
confirmation that #14 is universal mean-rev law.

If M5 (OI velocity filter) drops bad 30% → **H31_FILTERED at +5%+ mean WR ≥98%**.

## Methodology principle

User is right: we've been tunnel-visioned on "funding-rate capture" while ignoring the
RELATED mechanics (basis dynamics, microstructure, regime). Each H31 event has 5-7
observable dimensions (funding, basis, OI, volume, depth, BTC regime, time-of-day);
we've only USED funding+basis. Other dimensions either filter the entry or extend
the captured PnL.

## Operational priority

Cycle 17:00 UTC and beyond: Run M1, M2, M3 first (they use already-fetched data,
zero new API calls, can complete in 1 cycle each). M4 needs 1 BTC parquet query.
M5 needs OI fetch (~1 hr). M6 needs live monitoring queue. M7 needs new compute on
existing parquet.

## Do NOT rush to deploy paper-stream

User's critique is valid — H31 paper-stream proposal was PREMATURE without M1-M3
testing. Wait for at least M1+M3 results before finalizing paper-stream spec.


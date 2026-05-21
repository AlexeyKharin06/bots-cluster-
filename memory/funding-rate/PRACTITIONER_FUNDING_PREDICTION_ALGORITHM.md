# Practitioner Funding-Prediction Algorithm — extracted from "Прогноз фандинга" site

Source: `Info/files/` (saved webpage from real funding-arb traders, uploaded by user 2026-05-21)

## What this site does

Predicts **next funding rate** for each exchange BEFORE it's paid, by replicating exchanges' own published formulas in real time using WebSocket premium-index feeds.

For Binance/Bybit/OKX/Bitget/Gate/KuCoin — different formulas, different weights.

## Core algorithm (from obfuscated `module.js`)

```
P_avg_weighted = sum(weight_i * premium_i) / sum(weight_i)
Funding = P_avg_weighted + clamp(interest - P_avg_weighted, ±0.05%)
                                                              ↑ ±0.0005 in code
```

This is the **standard Binance/Bybit funding formula**. The site uses it forward — given premium history during current funding interval, predicts what the funding will be.

## Per-exchange specifics (from obfuscated `.js` files)

| Exchange | Interest | Weight formula | WebSocket source |
|---|---|---|---|
| **Binance** | default (module.js) | growing weights (6 + 12*i) for period>1, equal (=1) for period=1 | `wss://fstream.binance.com/.../markPrice` |
| **Bybit** | default | growing (6 + 12*i) | `wss://stream.bybit.com/v5/public/linear` (tickers) |
| **OKX** | default | growing (6 + 12*i) — explicitly duplicated | `wss://ws.okx.com/v5/public` |
| **Bitget** | 0.0001 hardcoded | EQUAL weights (=1), `/8/T` divide in handleFunding | not specified |
| **Gate** | default | EQUAL weights (=1) | `wss://fx-ws.gateio.live` |
| **KuCoin** | 0.03 / (24/T) | growing weights (default from module.js) | static REST polling (WebSocket commented out) |

## Weight formulas in detail

For `period > 1` (i.e. 1-hour funding interval like Bybit):
- Real (historical) premium: `weight = 6 + 12 * i` where `i` is the index (starts from 0)
- Expected (forecast) premium: `weight = 18 + 12 * i` (offset +12 because forward)
- Final getMultSum = `(60T + 1) * 60T / 2 * 12 + 18` (closed-form sum)

For `period = 1` (8-hour funding like Binance default):
- All weights = 1 (equal weighting — simple average)
- getMultSum = `60` (just count)

## Virtual mode (what-if)

User enters `V%` as hypothetical remaining-premium scenario. Site calculates:
```
P_virtual_avg = (avgsum_so_far + V/100 * (u_(k+1) + ... + u_N)) / (weightssum + (u_(k+1) + ... + u_N))
Virtual_funding = handleFunding(P_virtual_avg)
```

Tells trader "if average premium stays at V% for rest of interval, funding will be X%".

## Why this matters for us

Our PROJECT_CONTEXT marks **interval-prediction** as KILLED (2-9% live precision). But that was for **interval-shortening events** (rare, ~28 events / 180d). 

This site predicts **funding rate of EVERY interval** — that's ALL coins × ALL exchanges × every 4h/8h. Each individual funding payment has a predictable value seconds before it's paid.

**Strategy**: 
- Read live premium index for top-50 USDT-perp on each exchange
- Apply per-exchange formula → predicted funding
- If predicted funding deviates from expected (e.g. > +0.3% on Binance perp), open SHORT just before T, close right after funding payment → capture mean reversion
- This is FAIR-PRICE strategy with KNOWN ground truth (not guess)

This effectively merges:
- **Funding harvest** (we killed naive harvest at -$0.97/trade)
- **Fair-price scalping** (we killed at 0/5 weeks profitable walk-forward)
But with **predictive power** — entering only when our prediction confirms extreme funding is locked in.

## New hypothesis to test (add to backlog as H32)

**H32 — Predictive funding-pay scalping:**

1. Subscribe to wss premium-index for top-50 USDT-perp on Binance/Bybit (start)
2. 60 seconds before funding T: calculate predicted funding using formula above
3. If predicted |funding| ≥ 0.5% AND time-to-T ≤ 60s → arm position
4. At T: open SHORT (if positive funding) / LONG (if negative)
5. Exit at T+30s (after funding payment) OR when price moves favorably 50% of predicted funding
6. Stop: -3% net

Difference from killed fair-price v3:
- Old fair-price: triggered on |funding rate| ≥ 1% from REST poll (60s lag)
- New: triggers on PREDICTED funding using LIVE premium stream
- Predicted funding has up to 2 min lead time before official rate sets

Expected behavior:
- Predicted funding within ±0.02% of actual published rate (site claims accuracy)
- Win rate should be higher than fair-price v3 because we KNOW the rate is locked in
- Sample n=20+ before any conclusion

## Files locations

- VPS code: `/srv/bots/funding-rate/code/Info/`
- VPS Info JS files: `/srv/bots/funding-rate/code/Info/files/`
- Local: `D:/funding_rate/Info/`

## Implementation plan (for next AI brain cycle)

1. Read `Info/files/module.js.Без названия` + per-exchange .js files
2. De-obfuscate the key functions (handleRealPremium, handleExpectPremium, handleFunding)
3. Write `predictive_funding_paper.py`:
   - WebSocket subscribers per exchange
   - Per-coin premium history buffer (last hour)
   - Funding prediction every 1s
   - Paper-trade entry/exit per strategy above
4. Run paper bot 24h → check accuracy of prediction vs actual published funding
5. If predictive accuracy ≥ 95% → run paper-trade strategy for 7 days
6. If n ≥ 50 winning trades with WR ≥ 70% AND mean +$0.30/trade → promote to live-deploy candidate

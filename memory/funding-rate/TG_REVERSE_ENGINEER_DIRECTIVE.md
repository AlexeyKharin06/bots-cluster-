# 🔍 TG REVERSE-ENGINEER + ADAPTIVE STRATEGY DIRECTIVE (user-mandated 2026-05-24)

> User mandate: «TG каналы — это ground truth. Сопоставь практикерские трейды с историей.
> Понять ПОЧЕМУ работало: funding или basis? Где можно было funding взять, а где basis?
> Стаканы + курсовые spreads + funding + разные точки входа/выхода — ВСЁ ВЗАИМОСВЯЗАНО.
> Сделай ИСКЛЮЧИТЕЛЬНУЮ адаптивную стратегию которая выбирает funding vs basis по market regime.»

## DATA NOW ON VPS (cross-reference goldmine)

```
/srv/bots/funding-rate/code/data/
├── tg_messages_historical.jsonl       — 3036 msgs из 14 каналов (full archive)
├── tg_trade_cases.jsonl               — 80 reverse-engineered trade cases с metadata
├── media_signals_historical.jsonl     — 571 OCR'd screenshots (PnL, charts, positions)
├── pnl_claims_historical.jsonl        — 18 large-$ claims with structured PnL
└── multi_ex_funding_180.parquet       — 1.6M funding rows (наш ground truth funding data)
```

Также текущий live TG:
```
/srv/bots/.shared/tg/signals_master.jsonl  — 2433 msgs (продолжает расти)
```

## CORE TASKS (multi-cycle scope)

### T1 — Mine historical TG for «PnL evidence» posts
- Regex find posts with: ticker mentioned (`$XXX`) + amount ($ or %) + trade-related keyword
  (фанд|funding|спред|spread|кап|cap|hedge|арбитраж|listing|перп|perp|basis|премиум)
- Extract structured: (channel, date, ticker, claimed_pnl, claimed_strategy_class, exchange)
- Expected output: ~100-300 structured trade cases beyond the existing 80

### T2 — For each trade case: cross-reference with multi_ex_funding_180.parquet
- At trade time T, on mentioned ticker:
  - Funding rates на всех 5 биржах (был ли extreme rate? interval shortened?)
  - Premium-index magnitude (была ли basis широкая?)
  - Funding velocity (изменение rate за последние 1-24h)
- Classify what mechanism was likely traded:
  - F = pure funding capture (basis tight, funding extreme)
  - B = pure basis trade (basis wide, funding normal)
  - FB = combined (both extreme — H31-style interval-shortening)
  - L = listing arb (token recently listed)
  - O = other (depeg, news, etc)

### T3 — Pattern extraction: when does each mechanism dominate?
- Aggregate F/B/FB/L/O cases by:
  - BTC regime at trade time (bull/bear/chop)
  - Time of day UTC
  - Day of week
  - Ticker market cap tier
  - Exchange (Binance / Bybit / OKX / Gate / Bitget)
- Identify rules: «in regime X, mechanism Y dominates in practitioner trades»

### T4 — Build ADAPTIVE strategy spec
- At each H31/H38/H3 event candidate, classify the regime
- Based on T3 rules, choose:
  - Pure funding-capture hedge (current H31_basis at 100% hedge)
  - Pure basis directional (LONG perp UN-hedged, capture squeeze)
  - Combined partial hedge (50% — capture both)
  - Skip (regime says neither mechanism works here)
- This is FLEXIBLE adaptive strategy, not fixed H31

### T5 — Methodology refinement
- For each F/B/FB classification: measure ACTUAL post-event PnL using our parquet
- Cross-check practitioner claimed PnL vs algorithmic PnL
- If practitioner_claimed >> our_algorithmic: there's missing edge dimension we haven't captured
- Catalog as METHODOLOGY LESSON #N

### T6 — Live integration
- For live H31/H38/H3 detections going forward:
  - Run classifier from T4
  - Choose hedge ratio adaptively
  - Track actual PnL by classification
- Builds forward-validation dataset

## KEY HYPOTHESES TO DRIVE T1-T3

H_adapt_1: In BTC-bull regime, funding-capture (F) dominates (longs over-paid for upside; squeezes are mild)
H_adapt_2: In BTC-bear regime, basis-widening (B) dominates (shorts pile in deeply; squeezes are violent → big basis pop)
H_adapt_3: In CHOP regime, FB combined dominates (mean-rev mechanics work in both dimensions)
H_adapt_4: Mid-cap tickers (mcap $50M-500M) — B dominates (less liquid = bigger squeeze)
H_adapt_5: Top-cap tickers (BTC/ETH/SOL) — F dominates (liquid enough that basis doesn't widen)

## EXPECTED OUTCOMES

If T1-T3 succeeds:
- We have 200-500 historical case-studies showing WHY practitioner trades worked
- Each classified into F/B/FB/L/O with mechanism
- T3 rules let us auto-classify regime → mechanism → strategy
- Adaptive strategy upgrade: H31 might become 3 variants H31_F / H31_B / H31_FB depending on regime
- Each variant might have higher Sharpe than current "always 100% hedge" H31

If T3 shows mechanism distribution is uniform (no regime predicts mechanism):
- Conclusion: practitioner trades aren't mechanism-tagged at trade-time; they just took what's available
- Adaptive strategy degenerates to "do all 3 in parallel, weight by recent backtest performance"
- Still useful — beats single-strategy deployment

## OUTPUT STRUCTURE

`insights/cycle_YYYYMMDD_HHMM.md` per cycle with:
- T1 stats (how many cases mined per cycle)
- T2 cross-ref results sample
- T3 patterns emerging (or "no clear pattern yet, need more data")
- T4 strategy spec draft (iterative)
- T5 methodology lessons

## DO NOT

- Don't propose paper-stream until T4 strategy spec is settled
- Don't get stuck on T1 mining — even 50 cases yields useful patterns
- Don't reject hypotheses on n<20 — log and wait

## CYCLE PRIORITY OVERRIDE

This T1-T6 work TAKES PRIORITY over previous MICROSTRUCTURE M1-M7 directive.
M1-M7 are mechanical sweeps; T1-T6 incorporates practitioner reality.
Both compatible — T6 ultimately tests M1-M7 within adaptive framework.

Next cycle: start T1 (mine historical TG for trade-result posts). Don't try to do
all 6 in one cycle — pick T1 + T2 sampler.

GO.

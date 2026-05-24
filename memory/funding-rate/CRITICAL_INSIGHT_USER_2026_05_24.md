# CRITICAL USER INSIGHT 2026-05-24 (priority override)

User explained PRIMARY strategy he KNOWS works (one of MANY):

Same funding rate (-2%), DIFFERENT intervals across exchanges:
  CEX1: -2% @ 8h     CEX2: -2% @ 4h

Logic: CEX2 longs receive payment TWICE as often → aggressive BUY → CEX2 bid rises
above CEX1 ask → cross-ex basis goes NEGATIVE (CEX1 - CEX2 < 0).

Strategy:
1. PREDICT CEX2 will shorten interval (NOT wait for announcement)
2. ENTRY when cross-ex spread still 0 to -1%:
   LONG CEX2 + SHORT CEX1
3. After interval changes:
   CEX2 bid > CEX1 ask → close position with cross-ex profit
4. Exit decision is dynamic:
   - Funding still flowing? Hold longer
   - Basis spread maxed? Close to lock
   - Funding ending? Close

USER EMPHASIZES:
- Analyze BID/ASK, not just close price. Direction matters.
- This is just ONE manipulation pattern. There are MANY.
- Use ALL possible metrics — not just funding rate.
- Be more multi-faceted.

## Mechanism breakdown

Funding payment frequency is a HIDDEN parameter. Two exchanges with identical headline rate
but different intervals offer fundamentally different yields to longs:
- 8h interval @ -2% = -6% per day to longs (3 payments)
- 4h interval @ -2% = -12% per day to longs (6 payments)
- 1h interval @ -2% = -48% per day to longs (24 payments)

When CEX2 announces "interval will shorten from 8h->4h", longs gain 2x daily yield on CEX2 vs
peers. Smart money front-runs this BEFORE the announcement.

## Why this is FUNDAMENTALLY different from current H31/H34

| | Current H31_basis | Current H34 | User STRAT |
|---|---|---|---|
| Trigger | Post-announcement (reactive) | Post-announcement (reactive) | PRE-announcement (predictive) |
| Source of edge | Funding intensification post-event | Cross-ex funding offset | Cross-ex basis divergence |
| Hedge type | Spot SHORT (basis) | Cross-ex perp SHORT | Cross-ex perp SHORT, LONG-side picked by predicted-shortener |
| Exit | Fixed 4 funding periods | Fixed 4 funding periods | Dynamic — funding vs basis profit competition |
| Data needed | Funding parquet | Funding parquet | + bid/ask (L1) + depth (L2) + multi-ex price velocity |

User strategy is STRATEGICALLY ANTICIPATORY, not REACTIVE.

## CONCRETE NEW HYPOTHESES (priority sequence)

### U1 — Cross-exchange BASIS dynamics around H31 events (use existing data)
For each of 116 H31 events:
- 24h BEFORE event: compute (close_CEX_shortens - close_CEX_other) basis trajectory
- 4h AFTER event: same
- DOES basis trend NEGATIVE before event (predictive signal)?
- DOES basis SPIKE negative AFTER event (post-shortening squeeze)?

### U2 — Pre-event prediction of interval shortenings via cross-ex signals
For each H31 event_ts T, compute features at T-24h, T-12h, T-6h, T-1h:
- Cross-ex price divergence trajectory
- Cross-ex funding-rate divergence trajectory
- Cross-ex OI ratio
- Cross-ex volume ratio
- Each exchange premium-index level
Train logistic regression: P(shortening in next 24h | features)

### U3 — User predictive strategy backtest: LONG predicted-shortener + SHORT other-ex
Using 116 H31 events:
- Pretend we predicted at T-6h
- Open: LONG perp on shortener + SHORT perp on biggest-other-ex
- Hold to T+4h
- PnL: funding accrual + price divergence
- Compare to current H31_basis (+3.52%) and H34 (+1.28%)

### U4 — Dynamic exit policy backtest
At T+1h, T+2h, T+4h, T+8h, T+12h, T+24h decision:
- Hold if funding flowing AND basis widening
- Close if funding stopped OR basis converging back
Test which exit policy yields highest Sharpe

### U5 — Live bid/ask data collection daemon
Poll /depth on 5 exchanges for 100-coin universe every 60s.
After 30d have L1+L2 historical for predictive testing.
~500MB/day storage.

### U6 — Multi-pattern mining from TG cases
80 reverse-engineered cases + 3036 TG msgs + 571 OCR screenshots on VPS.
For each known practitioner trade:
- Identify which pattern matched (funding / basis / depeg / listing / spot-perp / cross-ex)
- Extract NEW patterns we have not named
- Build pattern taxonomy

### U7 — Decompose: when is FUNDING-dominant vs BASIS-dominant
For each H31 event, decompose PnL:
- funding_pnl = received_funding * hold - borrow_cost
- basis_pnl = (perp_price_drift - spot_price_drift) * notional
- total = funding + basis
Plot: when is basis > funding (basis-dominant) vs funding > basis (funding-dominant)?
Correlate basis-dominance with: BTC regime, ticker tier, volume, time-of-day, OI velocity.
This DIRECTLY answers user question: "where can we take funding, where basis?"

## ADAPTIVE STRATEGY SPEC (target after U1-U7)

```
function decide_position(event_candidate):
    regime = classify_regime(BTC_phase, time, ticker_tier, ex_pair)
    expected_funding_pnl = predict_funding(parquet_history, regime)
    expected_basis_pnl = predict_basis_widening(parquet_history, regime, ex_pair)
    
    if expected_funding_pnl > expected_basis_pnl * 2:
        # FUNDING-DOMINANT — full hedge
        return LONG_perp_100% + SHORT_spot_100%
    elif expected_basis_pnl > expected_funding_pnl * 2:
        # BASIS-DOMINANT — directional, capture cross-ex spread
        return LONG_predicted_shortener_perp + SHORT_other_ex_perp
    else:
        # BALANCED — partial hedge
        return LONG_perp_100% + SHORT_spot_50%
    
    set dynamic_exit_monitor(funding_decay, basis_convergence)
```

## METHODOLOGY LESSON #17 (immediate add)

Funding and basis are TWO PnL streams from SAME event. They can be captured INDEPENDENTLY,
TOGETHER, or in OPPOSITION. Strategy must IDENTIFY which dominates per-event and pick hedge
ratio accordingly — fixed 100% hedge LEAVES MONEY ON TABLE in basis-dominant events and
CREATES LOSS in negative-basis events.

## DO NOT

- Stop M1-M7 microstructure work UNTIL U1-U3 results in
- Do not propose paper-stream — even MORE premature now
- Do not ask user for permission for L1/L2 data collection — just start (U5)

## PRIORITY

CRITICAL. This insight changes the project from "funding capture" to "adaptive basis+funding
capture". User explicitly said this is ONE of MANY manipulation patterns. Once we crack
U1-U7, expect MORE user-revealed patterns. Architecture must be flexible.

Next cycle: U1 sampler (analyze existing parquet for cross-ex basis dynamics around H31 events).
Should complete in 1 cycle. Then U3 in next cycle. Then U7 decomposition.

GO.

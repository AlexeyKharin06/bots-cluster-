# R2 SOLO RETEST — Methodology #14 retroactive application

## Hypothesis
Methodology #14 (cycle 2300): SOLO mean-rev events outperform CONFIRMED multi-venue events.
SOLO = idiosyncratic = fast revert (good for scalp).
CONFIRMED = systemic = slow revert (price drift > funding = bad).

R2 fair-price scalp was REJECTED on backtest (0/5 weeks, mean -$0.89/trade across 206k sims).
But that test included BOTH SOLO and CONFIRMED events undifferentiated.

## Test plan (next cycle)

1. Load mega_fairprice_backtest.parquet (316k events from prior backtest)
2. For each event, classify SOLO vs CONFIRMED:
   - SOLO: same coin on other exchanges has |funding rate| < 30bp at event_ts ± 30min
   - CONFIRMED: ≥1 other exchange has same-direction |funding| ≥ 30bp simultaneously
3. Compute R2 unhedged scalp PnL separately for SOLO vs CONFIRMED subsets
4. If SOLO subset shows mean > +30bp AND WR > 60% AND walk-forward TRAIN/TEST asymmetric-pass:
   - Catalog as R2_SOLO_RESURRECTED — new edge candidate Edge 4
   - Run on live paper_fairprice_v6 trades (n=31): retroactive classify
5. Cross-check with live paper performance:
   - 31 trades, 84% WR, mean +$0.09 — is concentration on SOLO events?
   - Top symbol BOBBOB 10 trades — what was its multi-venue funding state?

## Expected outcomes (a priori)

- If SOLO R2 works: NEW Edge 4 candidate, **revives fair-price niche** with mechanistic understanding (idiosyncratic mean-rev)
- If SOLO R2 also fails: confirms R2 is structurally dead regardless of regime, close case
- If only certain symbol types work: produce whitelist filter (e.g. only mid-cap, not BOBBOB-class fat-tail)

## Methodology #14 generalization opportunity

This is the FIRST retroactive application of Meth #14 to a rejected hypothesis. If it
resurrects R2, we should systematically re-test ALL rejected R1-R18 through the SOLO/CONFIRMED
lens. May resurrect 1-3 of them.

Specifically interesting:
- R1 (TG-NLP interval prediction) — SOLO interval announcements vs cluster?
- R6 (naive funding harvest >2%) — SOLO >2% vs cluster >2%?
- R15 (practitioner predictive scalp) — already shown to fail; SOLO might work?

## Priority
HIGH — directly addresses user question about fair-price status and applies our newest
methodology lesson to legacy rejecteds. Cycle 17:00 UTC should pick this up.

# BRIEF — funding-rate snapshot

## State (2026-05-24 14:35 UTC — TG REVERSE-ENGINEER T2 classifier built; 3 headline findings + 2 infra)

- ✅ **3-edge portfolio FULLY VALIDATED & UNCHANGED** (KPI 4 cleared since 2026-05-23_1100). T2 findings DO NOT change the math on the 116 detected H31 events.
- 🟢 **T2 classifier built** (`/tmp/t2_classify.py`): 80 practitioner cases tagged F/B/FB/L/O using priority-ordered text-and-feature rules. Deterministic, re-runnable on new cases.
- 🟢 **VALIDATION**: 10/76 FB cases all have textbook H31 fingerprint (interval-shortened + caps ≥5 + funding ≥1% + 1h interval). Practitioners trade exactly what we screen for. Independent confirmation.
- 🟡 **GAP — pure-B (basis-only) is most-common practitioner class we DON'T cover**: 13/76 (≈17%) of cases are basis-spread arb without interval shortening (delisting, fresh-listing dislocation, CEX↔DEX rasinkhron, pump-induced rasinkhron). 3-edge portfolio has nothing here. **R5 spread-arb naive was rejected, but THIS is event-gated B — different failure mode.**
- 🟡 **H31 universe COVERAGE GAP**: only 3/10 practitioner FB cases match our 213 H31 detections within ±7d. 7/10 are micro-caps absent from 50-symbol scanner universe (BULLA, BABY, MAGIC, ADA, SOON-2025, LA-Jun). H31 detected events are still WR=100% Sharpe=1.90 — but addressable opportunity is ≈3× bigger with universe expansion.
- 🔧 **Infra bug A**: `feed_funding.jsonl` 2/2436 = 0.08% routing rate. Root cause: `tg_unified_listener.py:67-68` regex requires English phrase "funding rate" — no RU/UA keywords (фанд/спред/хедж/перп). Patch proposed, **NEEDS USER OK** (shared infra touch).
- 📐 **Meth #18 CANDIDATE**: report `coverage = matched / practitioner_events_same_mechanism` alongside Sharpe — distinguishes mechanism-miss from universe-miss.

## 🟢 3-edge counter-cyclical portfolio (unchanged)

| Edge | n | Mean | WR | Sharpe | corr |
|---|---|---|---|---|---|
| H31_basis (LONG-perp+SHORT-spot, h=100%) | 116 | +3.52% | 100% | 1.90 | — |
| H34_perp_perp | 101 | +1.28% | 79% | 0.74 | +0.30 |
| H3 50bp baseline | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| H3 50bp DROP-CONFIRMED | 101 | +0.89% | 98.0% | 0.65 | TBD |
| H3 75bp baseline | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H3 75bp DROP-CONFIRMED | 30 | +1.96% | 100% | 0.88 | TBD |

## 🔬 T2 mechanism distribution (n=80 / 76 with features)

| Mechanism | n | % | Covered? |
|---|---|---|---|
| FB (funding+basis combined, H31) | 10 | 12.5% | ✅ H31 |
| **B (pure basis / spread arb)** | 13 | 16.2% | ❌ **GAP** |
| F (pure funding capture) | 4 | 5.0% | ✅ H3 |
| L (listing arb) | 5 | 6.2% | ❌ GAP — highest $/trade |
| O_depeg (stablecoin) | 8 | 10.0% | ✅ H3 50bp |
| O_hack | 5 | 6.2% | ❌ binary, deferred |
| O_news | 3 | 3.8% | ❌ |
| O (generic/marketing/summary) | 32 | 40.0% | n/a — mostly noise |

Channel-mechanism profile: `@twix1444` cleanest FB; `@lopata_arb` heavy B; `@ua_cryptoinvest` hack+FB drama; `@arbitragediarys` depeg+news.

## 📐 Methodology canon (latest)

- #12: walk-fwd asymmetric gap (penalize only TRAIN>TEST)
- #13.1: graduated vol gate / phantom_print rule
- #14: multi-venue coincidence → SOLO > CONFIRMED **for UNHEDGED mean-rev**
- #15: perp-leg on venue-isolated depeg = tail insurance
- #16 CANDIDATE: Meth #14 stable-class boundary (PYUSD)
- #17 CANDIDATE: Meth #14 sign depends on TRADE STRUCTURE. HEDGED funding-capture: CONFIRMED > SOLO
- **#18 CANDIDATE (THIS CYCLE)**: report `coverage = matched / practitioner_events_with_mechanism` alongside Sharpe. Mechanism-miss vs universe-miss are distinct failure modes; H31 has universe-miss (30% coverage).

## Next-cycle plan

1. **T1 mining** (deferred from this cycle) — extract 100-200 more trade cases from 3,036 raw msgs using T2-learned text priors.
2. **BTC regime overlay** — fetch BTC daily closes, label each case-date bull/bear/chop, test H_adapt_1..H_adapt_5.
3. **H_BASIS_EVENT prototype backtest** — pull spot+perp 1m for 13 B-class events, event-gated spread PnL, walk-forward.
4. **H_TG_ROUTING_PATCH user OK ask** — apply + 24h validate if user OKs.
5. (Lower priority) R2 SOLO retest, Meth #17 cross-val on H38, L2 depth, paper-stream bundle ask.

DEFER permanently (closed): M1 partial-hedge, M2 basis-pure, M3 SOLO-only H31 variant, M5 microstructure filter.

## Negatives (DO NOT retest)

R1-R20. R5 naive spread-arb stays REJECTED. **R5* note**: H_BASIS_EVENT (event-gated basis) is NOT a retest of R5 — it's a constrained subset gated by 5 specific trigger event classes (delisting, fresh-listing, CEX↔DEX rasinkhron, pump-induced lag, hack-spread).

## New backlog this cycle (5)

- **H_BASIS_EVENT** — event-gated basis arb (primary, prototype-able next cycle)
- **H_HACK_SPREAD** — deferred, binary payoff
- **H_LISTING_FRESH** — deferred, depends on H6 listing feed
- **H31_UNIVERSE_EXPANSION** — fetch micro-cap funding for BULLA/BABY/MAGIC/ADA/SOON/LA-2025; risk R4, mitigated by event-trigger consistency
- **H_TG_ROUTING_PATCH** — pending user OK

## Sources

`/tmp/t2_classify.py`, `/tmp/t2_classified.jsonl`, `/tmp/t2_summary.json`, `insights/cycle_20260524_1435.md`. Prior: cycle_20260524_1418.md, M1/M3 microstructure.

## 🚀 MANDATE: continue TG REVERSE-ENGINEER (T1 expansion → BTC regime → H_BASIS_EVENT proto). Edge hunt is OPEN again on B-class. Canon refinement ongoing.

## 🔍 TG REVERSE-ENGINEER DIRECTIVE 2026-05-24 (HIGH PRIORITY OVERRIDE — ACTIVE)

T2 mechanism classifier complete (this cycle). T1 mining + BTC regime + T4 adaptive spec are next 2-3 cycles. Full directive: `TG_REVERSE_ENGINEER_DIRECTIVE.md`.

## 📡 INFRA ASKS (pending user OK)

1. **H_TG_ROUTING_PATCH** — patch `/srv/bots/.shared/tg/tg_unified_listener.py:67-68` to add RU/UA keywords (фанд/спред/хедж/перп/интервал/арбитраж). Estimated lift: 0.08% → 5-15% routing rate.
2. **H29 exchange-API poller** — already in backlog from prior cycles. Still pending.
3. **H31_UNIVERSE_EXPANSION** — fetch micro-cap historical funding (no real-trade impact, just data).

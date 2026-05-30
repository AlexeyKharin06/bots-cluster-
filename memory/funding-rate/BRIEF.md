# Funding-rate BRIEF — snapshot 2026-05-30 17:00 UTC (cycle 20260530_1700)

## Where we are
Project in HARDEN-AND-DEPLOY. 3-edge portfolio validated (KPI 4 cleared).
This cycle executed cycle 0500's HIGHEST-priority queued item — **C2
kline-refetch on gate (372 trig) + bybit (266 trig)** — extending the
real-basis-drift verdict from binance-only to a 3-exchange universe.

## THIS CYCLE: C2 standalone p99 — 3-EX UNIVERSE EXPANSION
**DECISIVE VALIDATION at n=564 (4.6× expansion vs binance-only n=122)**:
- POOLED 3-EX: mean **+2.655% / WR 76.1% / Sharpe 0.345**
- WF TRAIN n=282 +2.345% / TEST n=282 +2.965% → Meth #12 PASS (TEST>TRAIN)
- 6/7 months positive (May n=4 partial-month noise)
- SHORTEN n=66 +4.47% / NO_SHORTEN n=498 +2.42% (edge NOT interval-conditional)

### Per-exchange breakdown
| ex | n_ok / n_trig | fund | basis_drift | real_pnl | WR | Sharpe |
|---|---|---|---|---|---|---|
| binance (0500) | 122/227 | +2.02% | +0.19% | +1.81% | 0.787 | **0.660** |
| bybit (NEW)    | 134/266 | +2.64% | +0.43% | +2.68% | 0.806 | 0.513 |
| gate (NEW)     | 308/372 | +3.05% | +0.34% | +2.98% | 0.731 | 0.309 |

### Coverage gap drivers (no_spot is the limiter)
- bybit 127/266 events dropped (49.6%) — no bybit spot listing for half of chronic-discount cluster
- gate 64/372 dropped (17.2%) — much better spot coverage on gate
- binance 105/227 dropped (cycle 0500, also no_spot dominated)

### Per-ex Sharpe ordering = mean-PnL ordering REVERSED
binance Sh 0.66 > bybit 0.51 > gate 0.31; gate mean +2.98 > bybit +2.68 > binance +1.81.
**Mean ↑ but Sharpe ↓** as universe widens — smaller venues = bigger funding magnitudes but heavier-tailed events. Filed **Meth #33 candidate (1/2)** — promote on H38 universe expansion next cycle.

### NEW per-sym structural-adverse flags
- binance: FLOW n=10 -1.23% (cycle 0500, confirmed BINANCE-SPECIFIC this cycle: FLOW on bybit +0.94%, on gate +0.93% — resolves H_C2_FLOW_RESEARCH scope)
- bybit: TAC n=6 -0.66% (NEW)
- gate: UP n=6 -1.71%, GUA n=3 -0.74%, EDU n=3 -0.52% (NEW)

### Per-ex blacklist sensitivity (DRAFT quality tier)
Drop above 28 events → pooled n=536, mean +2.85% (+19.5bp lift), WR 79.5%, Sh 0.365. Modest, not required.

## Classification update
- old: **C2_STANDALONE_p99 → VALIDATED (BINANCE-SUBSET, n=122)**
- new: **C2_STANDALONE_p99 → VALIDATED (3-EX, n=564)**
- Same throughput-expansion sub-tier of Edge 1 H31_BASIS (NOT 4th independent edge — mechanism-identity cycle 2300+0500).
- Sub-tier draft: **C2_p99_3EX_QUALITY** = baseline + per-ex blacklist (FLOW/TAC/UP/EDU/GUA).

## 3-edge portfolio (UNCHANGED — validated, deploy-ready)
- Edge 1 **H31_BASIS**: +3.52% / WR 100% / Sh 1.84 / n=116
- Edge 2 **H34_PERP_PERP**: +1.44% / WR 81% / Sh 0.82 / n=101
- Edge 3 **H3_DEPEG**: +0.81-1.76% / WR 96-100% / counter-cyclical
- Sub-tier **H_COMBO_3c**: +4.18% Sh 2.17 n=40 (spec ready, bot NOT written)
- Sub-tier **C2_p99_3EX (NEW)**: +2.66% Sh 0.35 n=564 (3 ex, real klines, 6/7 months pos, Meth #12 PASS)

## Live state (delta vs cycle 0500)
- paper_fairprice_v6: n=84 → **93** (+9). Last 9: 6 sub-60s target_hit clean wins, 1 ID-303s timeout (-0.28%), **2 PORTAL hard_sl_net at 61s/66s (-3.01% each)** — boundary cases for Meth #28 cutoff. sub-60s n=59 WR 96.6% sum +23.79% / ≥60s n=34 WR 52.9% sum -21.11%.
- paper_new_symbol: n=20 **(7th cycle no new)** — R3 replay, -$14.19/WR 25%. PAUSE rec re-iterated.
- cut60 A/B: **6th cycle never started** (user queue A unexec).
- TG feed_funding.jsonl: 7 → **8** (+1 cryptokitta perp-dex non-actionable; routing patch still 12-cycle deferred).
- 24 funding-keyword hits in master feed last 10d (RU/UA content). Notable: ESPORTS delisting/spread case (rozenroom/lopata/freecalls) + Hyperliquid index-price cascade (ua_cryptoinvest) — H_BASIS_EVENT corroboration.

## OPEN USER QUEUE (still unexecuted)
- (A) START cut60 A/B paper bot (6th cycle)
- (B) PAUSE paper_new_symbol (7th cycle no new + R3 replay, -$17+)
- (C) Write `paper_bot_h_combo_3c.py` (sub-tier of Edge 1, n=40 +4.18%/Sh 2.17)
- (D) **NEW**: Write `paper_bot_c2_3ex.py` (size $1, paper:true) given this cycle's 3-ex validation
- (E) H_BOROS_INDICATOR USER DECISION (deferred **24 cycles**)
- (F) TG keyword-filter widening (shared infra coordination)

## OPS / artifacts
- script: `/srv/bots/funding-rate/code/scripts/c2_basis_drift_bybit_gate_v2.py` (NEW parallel, 16 workers, ~3min wall-clock 1276 HTTP calls)
- data: `/srv/bots/funding-rate/code/data/c2_basis_drift_bybit_gate.parquet` (638 rows)
- baseline (cycle 0500): `/srv/bots/funding-rate/code/data/c2_basis_drift_real.parquet` (122 ok)
- VPS git push BROKEN (unchanged — user knows).

## Validated NEGATIVES (do NOT re-test)
R1 interval-pred 2-9% live; R2 fair-price scalp; R3 listing momentum;
R4 microcaps; R5 naive spread −$13473; R6 naive funding harvest; R7 confluence
LONG; R13/R24 H31 SHORT/sign-flip; R15 H37 unhedged; R16 borrow SHORT;
R23 H38 perp-perp standalone; R26 C2_p95 standalone; Meth #30/#31:
overnight-megasearch "edges" = funding-only tautology.

## Methodology updates
- **Meth #33 CANDIDATE (NEW, 1/2)**: universe expansion ↑ mean PnL, ↓ Sharpe proportionally. Promote on H38 6-ex expansion next cycle.
- Meth #12 PASS pooled (TEST 2.97 > TRAIN 2.35); per-ex: gate clean PASS, bybit borderline TRAIN>TEST 1.15pp.

## Next priorities
1. **C2 okx (122) + bitget (75) kline-refetch** (~30 min): completes 6-ex universe, +120 events expected → total ~700.
2. **C2 permutation null on bybit/gate**: replicate cycle 0500 binance (-0.30% sign-opposite). ~10 min.
3. **Meth #33 promotion test**: H38_CONFIRMED universe expansion 6-ex Sharpe degradation pattern (~30 min on existing c8_meth17_categorized.parquet).
4. **C2 paper-stream spec** `paper_bot_c2_3ex.py` Python outline.
5. **paper_fairprice_v6 PORTAL audit**: 2 hard_sl at 61s/66s = $-6.02 — per-sym blacklist or noise?
6. (USER) Queue A+B+C+D+E+F.

## fairprice_v6 probability (unchanged from 0500)
survivor 30% / micro-edge-with-tail-drag 50% / sub-60s sub-resolution-alpha 12% / noise 8%. NOT real-money promotable (n<100 sub-60s pure, no OOS WF). cut60 A/B remains user-queue-blocked.

# Funding-rate BRIEF — snapshot 2026-05-31 11:00 UTC (cycle 20260531_1100)

## Where we are
HARDEN-AND-DEPLOY. 3-edge portfolio validated. This cycle: **REVERSED cycle 0500's extended blacklist** — MOVR (n=5) is single-event-dominated, INJ (n=2) is statistical noise. Promoted **Methodology #35 (trimmed-mean cross-venue blacklist gate)** to FINAL. C2 tier reverts to 5-pair quality (cycle 2300 baseline).

## MOVR mechanism investigation (cycle 0500 priority #2)
- 5 events, raw mean −0.38% (cycle 0500's basis for blacklist)
- ONE outlier (gate, 2026-04-24 16:00) has basis_drift −3.23% on +25% spot rally
- DROP-1-WORST trimmed mean = **+0.35%** (POSITIVE → flips sign)
- 4 surviving events have basis_drift in tight ±0.4% band — normal C2 behavior
- Multi-venue funding history confirms this was a genuine market-wide negative-funding squeeze; basis broke because spot rallied harder than perp (catalyst chase pattern)
- **VERDICT**: MOVR is NOT chronically adverse; the n=5 evidence is dominated by a single hedge-failure-on-rally event

## INJ check
- n=2 events (1 binance, 1 gate); both negative
- No statistical resolution at n=2; cannot blacklist on coin flip
- **REMOVE from extended blacklist**

## TAC check (confirms cycle 0500 decision)
- n=8 events, raw −0.88%, **trimmed −0.62%** — all 8 negative even with worst dropped
- Passes Meth #35: n≥5 ✓, all venues neg ✓, trimmed still neg ✓
- TAC@bybit, TAC@bitget remain on blacklist (5-pair tier covers TAC@bybit; bitget is venue-excluded)

## NEW Methodology #35 (FINAL)
Cross-venue blacklist requires ALL THREE:
1. Raw n ≥ 5 events for the symbol
2. All venues have negative mean
3. Trimmed mean (drop 1 worst) remains negative

Applied retroactively: removes MOVR + INJ from extended blacklist. Single corroboration sufficient (structural rule).

## Methodology #36 (CANDIDATE)
Rally-vol entry-defer gate: if symbol's recent realized vol > p95 of 30d distribution, defer C2 entry by 12h. Would have skipped MOVR 2026-04-24. Backtest needed next cycle.

## Tier comparison (REVERT to 5-pair quality)
| tier | n | mean | WR | Sharpe |
|---|---|---|---|---|
| 5-ex | 674 | +2.398% | 0.767 | 0.257 |
| 4-ex (no bitget) | 633 | +2.664% | 0.769 | 0.362 |
| **4-ex + 5-pair (CURRENT)** | **605** | **+2.838%** | **0.800** | **0.380** |
| 4-ex + 9-pair (DEPRECATED) | 598 | +2.875% | 0.804 | 0.383 |

The cycle 0500 EXTENDED tier gain (+0.04pp mean, +0.003 Sh) was built on noise. Revert is operationally identical to cycle 2300 BRIEF.

## 3-edge portfolio (unchanged headline)
- Edge 1 H31_BASIS: +3.52% / WR 100% / Sh 1.84 / n=116
- Edge 1.2 sub-tier **C2_p99_4EX_QUALITY** (REVERTED to 5-pair) +2.84% Sh 0.380 n=605
- Edge 2 H34_PERP_PERP: +1.44% / WR 81% / Sh 0.82 / n=101
- Edge 3 H3_DEPEG: +0.81-1.76% / WR 96-100%
- Other sub-tiers: H_COMBO_3c +4.18% Sh 2.17 n=40 / OKX_SHORTEN_ULTRA +5.39% Sh 1.32 n=14

KPI 4 = 3 independent edges (unchanged).

## OPEN USER QUEUE
- (A) START cut60 A/B (**9th cycle** unexecuted)
- (B) PAUSE paper_new_symbol (**10th cycle** dry)
- (C) Write paper_bot_h_combo_3c.py
- (D) Write paper_bot_c2_4ex.py — **USE 5-PAIR BLACKLIST, NOT 9-PAIR** (cycle 0500 spec was wrong; this cycle reverts)
- (E) H_BOROS_INDICATOR DECISION (deferred **27 cycles**)
- (F) TG keyword-filter widening

## Validated NEGATIVES (do NOT re-test)
R1-R7, R13-R16. **bitget REJECTED at Meth #33 venue gate**, **TAC on 5-pair blacklist (bybit confirmed structural by Meth #35)**, **MOVR + INJ NOT on blacklist** (this cycle reversal).

## Paper-bot pulse
- fairprice_v6: state/trades refreshing (still running, dry universe)
- new_symbol_detector: state polling, log silent since May 29
- whale_copy_paper, practitioner_follower: state refreshing, logs silent since May 21

## Artifacts (this cycle: pure analysis, no new parquets)
- VPS git push BROKEN (user knows)

## Next priorities
1. **Meth #36 backtest**: rally-vol entry-defer gate on C2 — does it skip just MOVR-style events or many?
2. **Meth #34 second corroboration** (cycle 0500 priority #1 still owed).
3. **paper_bot_c2_4ex.py spec writeup** with 5-pair blacklist (cycle 0500 priority #3, now corrected).
4. **TG signal mining for H_BOROS_INDICATOR** default (27-cycle overdue).
5. **Edge 4 hunt re-prime** (whale_copy / practitioner — 10 days silent, any usable data?).
6. (USER) Queue A+B+C+D+E+F.

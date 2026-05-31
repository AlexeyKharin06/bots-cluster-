# Funding-rate BRIEF — snapshot 2026-05-31 05:00 UTC (cycle 20260531_0500)

## Where we are
HARDEN-AND-DEPLOY. 3-edge portfolio validated. This cycle: **TAC cross-venue test RESOLVED**, **cross-venue adverse scan** surfaced MOVR + INJ, **permutation null on 4-EX EXTENDED** passes at ~9σ, **paper-bot health** confirmed (all running, just dry universe).

## TAC cross-venue resolution
- binance: perp listed, **spot NOT listed** → 8 c2_wide triggers UN-EXECUTABLE
- gate: funding never <−0.001 → 0 primary-ex triggers
- okx: not listed at all
- bybit: n=6 mean −0.66% (adverse)
- bitget: n=2 mean −1.53% (adverse)
- **VERDICT**: TAC blacklisted on the only 2 venues where C2 runs. "Cross-venue" status unfalsifiable, irrelevant.

## Cross-venue adverse scan (NEW)
3 symbols negative on every venue they appear (n≥2 venues):
| sym | venues (n) | per-ex mean | total n |
|---|---|---|---|
| TAC | bybit(6) bitget(2) | −0.66% / −1.53% | 8 |
| MOVR | bybit(1) gate(4) | −0.05% / −0.47% | 5 |
| INJ | binance(1) gate(1) | −0.36% / −0.27% | 2 |

INJ very weak (n=2); MOVR moderate (n=5); TAC strong (n=8).

## C2_p99_4EX_EXTENDED (NEW quality tier)
n=598 mean **+2.875%** std 7.497% WR **0.804** Sh **0.383** vs 5-pair n=605 +2.838% Sh 0.380. Throughput cost 7 events, gain ≈ +0.04% mean / +0.003 Sh — free upgrade.

WF TRAIN n=299 +2.459% Sh 0.583 / TEST n=299 +3.291% Sh 0.339 → +0.83pp TEST>TRAIN (Meth #12 PASS, better than 5-pair +0.73pp).

## Permutation null
- 5000 sign-flip perms on 4-EX EXTENDED
- obs +2.875%, null mean −0.008%, null std 0.326% → **~9σ**, p=0.00000
- bootstrap 95% CI [+2.327%, +3.528%], P(mean>30bp)=100%
- **First pooled-4-EX null computed** — corroborates Edge 1.2 as real, not multiple-test artefact

## Methodology
- Meth #33 FINAL: per-venue Sharpe ≥ pool Sharpe (venue-acceptance gate)
- **Meth #34 CANDIDATE (1/2)**: "strategy-availability gate" — verify both legs listed before adding venue (precondition to #33). Demonstrated by TAC@binance perp-only.

## Paper-bot health
All 4 funding paper bots PROCESS-ALIVE since May 21:
- fairprice_v6 (PID 166483, 4h24m CPU): last trade 04:05 UTC today, heartbeat 04:56 polls=164923 armed=0 → healthy + dry
- new_symbol_detector (PID 166500): last log May 29 (9th cycle dry)
- whale_copy_paper (PID 167027): silent since May 21
- practitioner_follower (PID 167036): silent since May 21

NOT stuck. Universe just isn't generating signals.

## 3-edge portfolio
- Edge 1 H31_BASIS: +3.52% / WR 100% / Sh 1.84 / n=116
- Edge 2 H34_PERP_PERP: +1.44% / WR 81% / Sh 0.82 / n=101
- Edge 3 H3_DEPEG: +0.81-1.76% / WR 96-100%
- Sub-tiers: H_COMBO_3c +4.18% Sh 2.17 n=40 / **C2_p99_4EX_EXTENDED +2.88% Sh 0.383 n=598** / OKX_SHORTEN_ULTRA +5.39% Sh 1.32 n=14

KPI 4 unchanged at 3 edges (C2 is sub-tier of Edge 1).

## OPEN USER QUEUE (unchanged)
- (A) START cut60 A/B (**8th cycle** unexecuted)
- (B) PAUSE paper_new_symbol (**9th cycle** dry)
- (C) Write paper_bot_h_combo_3c.py
- (D) Write paper_bot_c2_4ex.py (now with 9-pair blacklist incl MOVR+INJ)
- (E) H_BOROS_INDICATOR DECISION (deferred **26 cycles**)
- (F) TG keyword-filter widening

## Validated NEGATIVES (do NOT re-test)
R1-R7, R13-R16, R23-R26 (see backlog). **bitget REJECTED at Meth #33 venue gate**, **TAC/MOVR/INJ on extended blacklist**.

## Artifacts
- `/tmp/tac_binance_fetch.py` (NEW — probes binance spot/perp listing; aborted at spot=False)
- (No new parquets; this cycle was pure analysis on cycle 2300's data)
- VPS git push BROKEN (user knows)

## Next priorities
1. Meth #34 second corroboration (pick another borderline-availability symbol).
2. MOVR mechanism investigation (5 events, both venues neg — L2 revenue tie, chronic drift, or n=5 noise?).
3. paper_bot_c2_4ex.py spec writeup for user approval (with 9-pair blacklist).
4. TG signal mining for H_BOROS_INDICATOR default (26-cycle overdue).
5. Edge 4 hunt re-prime (whale_copy_paper has 10 days of "silent" — extract any usable data).
6. (USER) Queue A+B+C+D+E+F.

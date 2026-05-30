# Funding-rate BRIEF — snapshot 2026-05-30 05:00 UTC (cycle 20260530_0500)

## Where we are
Project in HARDEN-AND-DEPLOY. 3-edge portfolio validated (KPI 4 cleared).
This cycle: executed cycle 2300's HIGHEST-priority queued item — the
**C2 kline-refetch** — replacing capture-ratio stress with REAL basis
drift on the binance-executable subset (n=122).

## THIS CYCLE: C2 standalone p99 — REAL klines verdict
**PASSES the deploy gate** on the binance-spot subset (n=122/227):
- mean **+1.811% / WR 78.7% / Sharpe 0.66** (was stress-estimated cr=0.30
  → +0.21% / WR 0.57 / Sh 0.40; cr=0.94 face value → +1.50% / WR 0.85 /
  Sh 0.92)
- basis_drift on average **+0.193%** — slightly POSITIVE (perp rises faster
  than spot during compression), not the negative drag cr=0.30 assumed
- effective capture median **1.11** (above cr=0.94 face value)
- WF TRAIN +1.121 / TEST +2.501 → TEST > TRAIN +1.38pp (Meth #12 PASS,
  regime enrichment in Q1 2026)
- 6/6 months sign-positive, monotone improving Nov→Mar
- Bootstrap 95% CI [+1.33%, +2.30%], P(mean > 30bp) = 100%
- Permutation null (60 random sym-internal 24h windows): mean **−0.30%**
  WR 18% → sign-opposite real, 6× lift, kills the Meth #31
  funding-only-tautology residual that cycle 2300 worried about
- SHORTEN n=20 +3.08% (~H31 magnitude); NO_SHORTEN n=102 +1.56% (new
  PnL tier)

## Classification update
- old: **C2_STANDALONE_p99 → BORDERLINE-VALIDATED gated on kline refetch**
- new: **C2_STANDALONE_p99 → VALIDATED (BINANCE-SUBSET)**, throughput-expansion
  sub-tier of Edge 1 H31_BASIS (NOT a 4th independent edge — C2 is the 9× super-event of H31)
- Meth #32 refinement filed: add 3rd gate (independence-vs-known-edges)
  to leading-indicator two-step framework. Corroboration 1.5/2.
- FLOW flagged: n=10 fund +1.0%, drift −1.82%, real_pnl −1.23%, WR 20% —
  liquid-mid-cap with structurally adverse spot-perp gap. Excluding
  FLOW: n=112, +2.08%/WR 84%/Sh 0.82.

## 3-edge portfolio (UNCHANGED — validated, deploy-ready)
- Edge 1 **H31_BASIS**: +3.52% / WR 100% / Sh 1.84 / n=116
- Edge 2 **H34_PERP_PERP**: +1.44% / WR 81% / Sh 0.82 / n=101
- Edge 3 **H3_DEPEG**: +0.81-1.76% / WR 96-100% / counter-cyclical
- Sub-tier **H_COMBO_3c**: +4.18% Sh 2.20 n=40 (spec ready, bot NOT written)
- NEW sub-tier **C2_p99_BINANCE**: +1.81% Sh 0.66 n=122 (real klines, 6/6
  months positive, permutation-null sign-opposite)

## Live state (delta vs cycle 2300)
- paper_fairprice_v6: n=78 → **84** (+6), RUNNING. Sub-60s bimodality holds.
- paper_new_symbol: n=20 → **20** (5th cycle no new), still RUNNING per ps
  (user queue B PAUSE still unexecuted).
- cut60 A/B: STILL never started (5th cycle, user queue A unexec).
- TG feed_funding.jsonl: not reread this cycle (likely still 7).

## OPEN USER QUEUE (still unexecuted)
- (A) START cut60 A/B: `ssh root@VPS 'cd /srv/bots/funding-rate/code && nohup python3 paper_bot_fairprice_v6_cut60.py > logs/daemon_paper_bot_fairprice_v6_cut60.log 2>&1 < /dev/null &'`
- (B) PAUSE paper_new_symbol (R3 replay, −$17+, no new trades for 2 cycles).
- (C) Write `paper_bot_h_combo_3c.py` if approved.
- (D) NEW: decide whether to write `paper_bot_c2_binance.py` (size $1) given
  this cycle's binance-subset validation.

## OPS / artifacts
- script: `/srv/bots/funding-rate/code/scripts/c2_basis_drift_real.py`
- data: `/srv/bots/funding-rate/code/data/c2_basis_drift_real.parquet`
- ephemeral: `/tmp/c2_binance_trigs.parquet`, `/tmp/c2_binance_spot_trigs.parquet`,
  `/tmp/c2_analyze.py`
- VPS git push BROKEN (unchanged — user knows).

## Validated NEGATIVES (do NOT re-test)
R1 interval-pred 2-9% live; R2 fair-price scalp; R3 listing momentum;
R4 microcaps; R5 naive spread −$13473; R6 naive funding harvest; R7 confluence
LONG; R13/R24 H31 SHORT/sign-flip; R15 H37 unhedged; R16 borrow SHORT; R26
cand. C2_p95 standalone (cr=0.30 net -0.06%, cycle 2300); Meth #30/#31:
overnight-megasearch "edges" = funding-only tautology.

## Next priorities
1. **C2 kline-refetch gate/bybit subsets** (HIGHEST): scale this cycle's
   method to primary_ex={gate (372), bybit (266)} via their public klines APIs.
   If holds, total universe expands ~4-5× (227 → ~1000+). ~30-45 min/ex.
2. **C2 paper-stream spec drafting**: design `paper_bot_c2_binance.py`
   (size $1, paper:true, first-hour basis monitor + adverse-drift early-exit).
3. **FLOW adverse-drift research**: persistent funding-premium discount
   cluster (R23-style) vs spike risk — derive a tradeable filter.
4. (USER) Run queue A+B+C+D; monitor cut60 vs v6 after n≥10 cut60 trades.
5. TG keyword-filter widening (user coordination — shared root infra).
6. H_BOROS_INDICATOR — USER DECISION (deferred **23 cycles**).
7. Permutation null expansion to n=300+ on binance subset for tighter CI.

## fairprice_v6 probability (unchanged from 1700)
survivor 30% / micro-edge-with-tail-drag 50% / sub-60s sub-resolution-alpha 12%
/ noise 8%. NOT real-money promotable (n<100, no OOS WF). cut60 A/B
refines but remains user-queue-blocked.

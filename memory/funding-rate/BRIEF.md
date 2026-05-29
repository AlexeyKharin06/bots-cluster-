# Funding-rate BRIEF — snapshot 2026-05-29 23:00 UTC (cycle 20260529_2300)

## Where we are
Project in HARDEN-AND-DEPLOY. 3-edge portfolio validated (KPI 4 cleared). This
cycle: executed the **C2-PNL gate** explicitly tagged HIGHEST priority by the
previous cycle. Two backtests built: conditional (early-entry on H31 events)
and unconditional (live-deployable, no H31 hindsight).

## THIS CYCLE: C2-PNL gate — CONDITIONAL passes, UNCONDITIONAL split verdict
### CONDITIONAL (C2-early on 116 H31 LONG events, primary_ex):
- Coverage p90/p95/p99 = 74%/68%/48%. Mean lead 8.7h (p95).
- Face-value cr=0.937 lift: **+1.91 / +1.75 / +1.07 pp**.
- Conservative cr=0.30 lift: **+0.61 / +0.56 / +0.34 pp** — all 3 thresholds
  PASS +30bp gate under most pessimistic capture-ratio.
- WF 50/50: TRAIN/TEST both positive all 3 thr; p95 TEST > TRAIN (Meth #12
  PASS); p99 modest TRAIN > TEST.
- WR 100% preserved.

### UNCONDITIONAL (5047 p95 / 1063 p99 dedup'd triggers, 180d):
- **p95 standalone FAILS** at cr=0.30: net -0.06%/event, WR 23%.
- **p99 standalone BORDERLINE-PASSES**: cr=0.30 net +51bp, WR 55%, Sh 0.38;
  cr=0.94 net +245bp, WR 77%, Sh 0.59. WF TRAIN 0.65 / TEST 0.38.
- p99 SHORTEN n=128 +4.46% gross (~H31), NO_SHORTEN n=935 +2.85% gross.
- Permutation null (shuffle div within sym): p95 real/null 1.92x; p99 3.13x
  — real > null but null ≠ 0 (Meth #31 residual).

### Classification
- **C2_CONDITIONAL_ENHANCEMENT** → PROMOTED as H31_BASIS sub-spec (timing
  improvement, NOT a 4th edge).
- **C2_STANDALONE_p99** → BORDERLINE-VALIDATED, GATED on ±24h kline refetch
  (filed `H_C2_STANDALONE_p99_GATED`).
- **C2_STANDALONE_p95** → REJECTED standalone (R26 cand).
- METH #32 CANDIDATE: two-step gate for leading-indicator signals
  (conditional marginal + unconditional standalone). Corroboration 1/2.

## 3-edge portfolio (UNCHANGED — validated, deploy-ready)
- Edge 1 **H31_BASIS**: +3.52% / WR 100% / Sharpe 1.84 / n=116. (corr +0.30 H34, −0.31 H3)
- Edge 2 **H34_PERP_PERP**: +1.44% / WR 81% / Sharpe 0.82 / n=101.
- Edge 3 **H3_DEPEG**: +0.81% (50bp n=129) / +1.76% (75bp n=39) / WR 96-100% / counter-cyclical.
- Deploy-ready sub-tier **H_COMBO_3c**: +4.18% Sh 2.20 n=40. Spec ready, bot NOT written.

## Live state (delta vs cycle 1700)
- paper_fairprice_v6: n=75 → **78** (+3), RUNNING. Sub-60s bimodality holds.
- paper_new_symbol: n=20 → **20** (no new), still RUNNING per ps (user queue
  B PAUSE still unexecuted, 4th cycle of bleeding $-17+).
- cut60 A/B: STILL never started (4th cycle, user queue A unexecuted).
- TG feed_funding.jsonl: still **7 lines**; signals_master ~5650+.

## OPEN USER QUEUE (still unexecuted)
- (A) START cut60 A/B: `ssh root@VPS 'cd /srv/bots/funding-rate/code && nohup python3 paper_bot_fairprice_v6_cut60.py > logs/daemon_paper_bot_fairprice_v6_cut60.log 2>&1 < /dev/null &'`
- (B) PAUSE paper_new_symbol (R3 replay, −$17+).
- (C) Write `paper_bot_h_combo_3c.py` if approved.

## OPS / artifacts
VPS git push BROKEN. C2-PNL: `/tmp/c2_pnl_gate_trace.parquet`,
`/tmp/c2_pnl_uncond_trace.parquet`.

## Validated NEGATIVES (do NOT re-test)
R1 interval-pred 2-9% live; R2 fair-price scalp; R3 listing momentum;
R4 microcaps; R5 naive spread −$13473; R6 naive funding harvest; R7
confluence LONG; R13/R24 H31 SHORT/sign-flip; R15 H37 unhedged; R16 borrow
SHORT; **R26 cand. C2_p95 standalone** (cr=0.30 net -0.06%, this cycle);
Meth #30/#31: overnight-megasearch "edges" = funding-only tautology.

## Next priorities
1. **C2 kline-refetch** (HIGHEST): fetch ±24h spot+perp klines for top-50 syms
   in c2_wide universe, compute REAL basis-drift cost in lead window.
   Resolves whether C2_STANDALONE_p99 deploys honestly. ~2-3h compute.
2. (USER) Run queue A+B; monitor cut60 vs v6 after n≥10 cut60 trades.
3. If H_COMBO_3c approved → write `paper_bot_h_combo_3c.py`.
4. TG keyword-filter widening (user coordination — shared root infra).
5. H_BOROS_INDICATOR — USER DECISION (deferred **22 cycles**).

## fairprice_v6 probability (unchanged from 1700)
survivor 30% / micro-edge-with-tail-drag 50% / sub-60s sub-resolution-alpha 12%
/ noise 8%. NOT real-money promotable (n<100, no OOS WF). cut60 A/B refines.

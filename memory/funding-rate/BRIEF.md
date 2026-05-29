# Funding-rate BRIEF — snapshot 2026-05-29 17:00 UTC (cycle 20260529_1700)

## Where we are
Project in HARDEN-AND-DEPLOY. 3-edge portfolio validated (KPI 4 cleared). Env FULLY populated
(all parquet, paper bots, TG data present). This cycle: executed the long-deferred C2 backlog item.

## THIS CYCLE: C2 cross-ex divergence VALIDATED as a leading predictor (not yet a capture edge)
Ran C2 (highest-priority untested item since 2026-05-22, never executed) on pre-built artifacts
c2_wide.parquet (250,634 div cells) + c2_shortenings.parquet (213 events). Leakage-free lift test.
- **Lift @6h (base 0.122%)**: div≥p95(7.7bp)→**14.4×**; div≥p99(28bp)→**52.9×**. 12h/24h also strong.
- **Generalizes**: EXCL 8 chronic coins, lift still **16.8×** across 40 syms — not a few-coin artifact.
- **It LEADS**: div/sym-median rises −12h 1.6× → −6h 5.2× → −3h 13.7× → −1h 28× (peak) → decays after.
  Genuine early-warning (pre-event rise precedes the interval change → not a forward-fill artifact).
- **Walk-forward**: TRAIN 14.0× / TEST 15.5× (TEST>TRAIN = regime-richness, Meth #12). STABLE.
- **Classification**: predictive SIGNAL, not an independent capture edge (monetization still a
  basis-hedge on the same funding mechanism, like C8/H38). lift≠tradeable (Meth #8: 53× lift =
  6.46% precision). NEXT GATE = C2-PNL backtest before any paper-stream.
- Scripts: code/scripts/c2_divergence_predictor_test.py + c2_divergence_confounds.py.

## 3-edge portfolio (UNCHANGED — validated)
- Edge 1 **H31_BASIS**: +3.52% / WR 100% / Sharpe 1.84 / n=116. (corr +0.30 H34, −0.31 H3)
- Edge 2 **H34_PERP_PERP**: +1.44% / WR 81% / Sharpe 0.82 / n=101.
- Edge 3 **H3_DEPEG**: +0.81% (50bp n=129) / +1.76% (75bp n=39) / WR 96-100% / counter-cyclical.
- Deploy-ready sub-tier **H_COMBO_3c**: +4.18% Sharpe 2.20 n=40, P(>baseline)=98.85%.
  Spec at H_COMBO_3c_DEPLOY_SPEC.md. Bot NOT written/deployed yet.

## Live state (delta vs 1100)
- paper_fairprice_v6: n=70 → **75** (+5), RUNNING. Meth #28 sub-60s bimodality verdict unchanged.
- paper_new_symbol: n=19 → **20** (+1), still RUNNING & bleeding (R3 replay).
- cut60 A/B: **STILL never started** (3rd cycle) — no dir, no process, zero A/B data.
- TG feed_funding.jsonl: still 7 lines; signals_master 5644 (+115). Keyword filter still narrow.

## OPEN USER-EXECUTION QUEUE (STILL UNEXECUTED — root daemons, I cannot run)
- **(A) START cut60 A/B**: `ssh root@VPS 'cd /srv/bots/funding-rate/code && nohup python3 paper_bot_fairprice_v6_cut60.py > logs/daemon_paper_bot_fairprice_v6_cut60.log 2>&1 < /dev/null &'`
- **(B) PAUSE paper_new_symbol**: `kill -STOP 166499 166500` (n=20, −$17+, WR 20%, R3 replay).
- (C) write paper_bot_h_combo_3c.py if H_COMBO_3c deploy approved.

## OPS
- VPS git push to GitHub BROKEN (no credential helper). Commits stay LOCAL on VPS; GitHub cluster
  repo stale until one-time PAT login. Future cycles read local commits fine.
- paper_fairprice_v6 PID 166483 (n=75). paper_new_symbol PIDs 166499/166500 (n=20).
- Re-runnable live screen: /srv/bots/funding-rate-data/screens/funding_screen.py (public REST).

## Validated NEGATIVES — do NOT re-test
Interval-pred (2-9% live); fair-price scalping ANY threshold (R2, sub-60s wing of v6 open Q);
listing momentum (R3 — new_symbol replaying it); microcaps RAVE/SIREN/PIPPIN (R4); naive
price-spread arb (R5 −$13473); naive funding harvest (R6 −$304); confluence LONG (R7); borrow-spike
SHORT (R16); H37 unhedged predictive scalp (R15); H31 SHORT-side/sign-flip (R13/R24).
**Overnight-megasearch "edges" = funding-only-PnL tautology / WF-as-selection** (Meth #30/#31).

## Next priorities
1. **C2-PNL gate** (HIGHEST): backtest PnL of acting on the C2 leading signal (basis-hedge early
   entry vs spread-reversion capture, full fees+slippage+funding-flip); paper-stream only if
   net ≥+30bp/event in TEST.
2. (USER) Run queue A+B; monitor cut60 vs v6 after n≥10 cut60 trades.
3. If H_COMBO_3c approved → write paper_bot_h_combo_3c.py.
4. TG keyword-filter widening (user coordination — shared root infra) → unblocks H1/H2/H5.
5. H_BOROS_INDICATOR — USER DECISION (deferred 21 cycles).

## fairprice_v6 probability
survivor 30% / micro-edge-with-tail-drag 50% / sub-60s sub-resolution-alpha 12% / noise 8%.
NOT real-money promotable (n<100, no OOS-window walk-forward). cut60 A/B would refine.

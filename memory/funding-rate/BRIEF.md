# Funding-rate BRIEF — snapshot 2026-05-29 11:00 UTC (cycle 20260529_1100)

## Where we are
Project in HARDEN-AND-DEPLOY. 3-edge portfolio validated (KPI 4 cleared). Environment is
FULLY populated (all parquet, paper bots, TG data present) — the 0500 cycle's "clean env"
report was a transient mount artifact; ignore it.

## 3-edge portfolio (UNCHANGED — validated)
- Edge 1 **H31_BASIS**: +3.52% / WR 100% / Sharpe 1.84 / n=116. (corr +0.30 H34, −0.31 H3)
- Edge 2 **H34_PERP_PERP**: +1.44% / WR 81% / Sharpe 0.82 / n=101.
- Edge 3 **H3_DEPEG**: +0.81% (50bp n=129) / +1.76% (75bp n=39) / WR 96-100% / counter-cyclical.
- Deploy-ready sub-tier **H_COMBO_3c** (user bootstrap): +4.18% Sharpe 2.20 n=40, 95%CI[+3.62,+4.78],
  P(>baseline)=98.85%. Spec at H_COMBO_3c_DEPLOY_SPEC.md. Bot NOT written/deployed yet.

## THIS CYCLE: cut60 A/B quantified analytically (n=70 live v6 trades)
- **Meth #28 CONFIRMED at n=70**: sub-60s n=47 WR 97.9% +$23.64 / ≥60s n=23 WR 52.2% −$13.07.
- **cut60 realistic uplift = +$3 to +$7** (total ~$14-17 vs v6 $10.57), NOT naive +$13.
  cut60 sacrifices +$2.04 of 12 late target_hit winners AND only partially caps −$15.11 late
  losses (8 timeouts partial-drift, 2 SL already stop-capped). Bounds WORST $8.53 / MID $17.10 /
  BEST(naive) $25.68. 60s-mark price unobservable → live A/B needed to settle magnitude.
- cut60 bot impl (user, root, May28) reviewed = correct, no bug.

## OPEN USER-EXECUTION QUEUE (from 2026-05-28 session — STILL UNEXECUTED)
- **(A) START cut60 A/B** — bot written but NEVER RAN (no process, no paper_fairprice_v6_cut60/
  dir). Collecting zero data. Cmd:
  `ssh root@VPS 'cd /srv/bots/funding-rate/code && nohup python3 paper_bot_fairprice_v6_cut60.py > logs/daemon_paper_bot_fairprice_v6_cut60.log 2>&1 < /dev/null &'`
  Analysis says +EV; run it to confirm magnitude.
- **(B) PAUSE paper_new_symbol** — n=19, −$17.37, WR 21.1%, TP-fire 1/19 = clean R3 replay,
  still running & still losing (+1 loser since user's n=18 note). Cmd: `kill -STOP 166499 166500`.
- (C) write paper_bot_h_combo_3c.py if H_COMBO_3c deploy approved.

## OPS
- **VPS git push to GitHub is BROKEN** (no credential helper). Commits stay LOCAL on VPS;
  future cycles read them, but GitHub cluster repo is stale until one-time PAT login.
- paper_fairprice_v6 RUNNING PID 166483 (n=70). paper_new_symbol PIDs 166499/166500 (n=19).
- Re-runnable live screen: /srv/bots/funding-rate-data/screens/funding_screen.py (public REST).

## Validated NEGATIVES — do NOT re-test
Interval-pred (2-9% live); fair-price scalping ANY threshold (R2, but sub-60s wing of v6 is an
open micro-edge question); listing momentum (R3 — new_symbol bot is replaying this & losing);
microcaps RAVE/SIREN/PIPPIN (R4); naive price-spread arb (R5 −$13473); naive funding harvest
(R6 −$304); confluence LONG (R7); borrow-spike SHORT (R16); H37 unhedged predictive scalp (R15);
H31 SHORT-side / sign-flip (R13/R24). **Overnight-megasearch "edges" = funding-only-PnL
tautology / WF-as-selection overfit** (Meth #30/#31 — do NOT deploy any "DEPLOY PRIORITY" item).

## Next priorities
1. (USER) Run queue A+B; then monitor cut60 vs v6 after n≥10 cut60 trades.
2. Meth #29 corroboration #2 (2nd mean-rev-to-anchor unimodality, H3 PYUSD/USDC subset) ~15min.
3. If H_COMBO_3c approved → write paper_bot_h_combo_3c.py.
4. OOS test H_COMBO_3c once 30+ days fresh H31 events accumulate.
5. H_BOROS_INDICATOR — USER DECISION (deferred 21 cycles).

## fairprice_v6 probability
survivor 30% / micro-edge-with-tail-drag 50% / sub-60s sub-resolution-alpha 12% / noise 8%.
NOT real-money promotable (n<100, no OOS-window walk-forward). cut60 A/B would refine.

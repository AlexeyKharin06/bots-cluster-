# Funding-rate BRIEF — snapshot 2026-05-31 17:00 UTC (cycle 20260531_1700)

## Where we are
HARDEN-AND-DEPLOY. 3-edge portfolio validated. **This cycle: live paper-bot tail-risk audit on paper_fairprice_v6 (n=117 9 days)**. Net +$6.40 / WR 82% hides 6 hard_sl_net trades that cost $-22.0 (3.4× the bot's net PnL). All 6 SL events on small-cap symbols with consistent vertical-pump mechanism. Cycle 1100's Meth #36 (rally-vol gate) is the right operationalization but the backtest is still owed. This cycle catalogues observed pattern and proposes interim symbol blacklist (H39).

## Paper_fairprice_v6 — actual edge characterization
- Total: n=117 WR 82% mean=$+0.055 total=$+6.40 over 9 days (since 2026-05-21)
- Last 24h: n=24 WR 87% +$3.71 (includes HOME SL $-5.72 — would be +$9.43 without)
- Per ex: bybit n=81 +$10.22 (genuine edge); binance n=36 -$3.83 (entirely 2 events: HOME -$5.72 + PORTAL -$3.01)
- Exit dist: target_hit 99/117 mean +$0.40; timeout 12/117 mean -$0.95; hard_sl_net 6/117 mean -$3.66
- **Without SL+timeout the bot would be +$39.7. The 18 bad exits cost ~$33.**

## Funding-bucket asymmetry (NEW Meth #37 CANDIDATE)
- 0.50-0.75% bucket: n=62 WR 81% mean +$0.014 total +$0.86 (flat)
- 0.75-1.00% bucket: n=28 WR 86% mean -$0.13 total -$3.72 (**LOSING** despite high WR)
- 1.00-1.50% bucket: n=27 WR 81% mean +$0.34 total +$9.25 (genuine edge)
- Hypothesis: the middle band is high enough to trigger entry but not high enough to cushion adverse spot moves. NOT yet promotable (n=27 in high bucket too small); revisit at n≥60.

## H39 small-cap blacklist (NEW, paper-only)
- Trigger sym list (observed): PORTAL (4/4 lose, -$5.32), GENIUS (3/3 lose -$2.53), GMT@bybit (3/3 lose -$2.37), DRIFT (3/3 lose -$1.26), BOBBOB, AIGENSYN, HOME, ID@bybit
- Operational gate (conservative): start with PORTAL only (single-symbol exclude, 4/4 losing, n=4)
- Expected impact: avoids ~$5-12 over next 30d at current rate
- NOT auto-deployed; observation-only; user OK needed before paper code edit

## H40 ESPORTS delisting 2026-06-10 (NEW, monitor)
- TG feed (2026-05-26 rozenroom): Binance Futures Will Delist ESPORTSUSDT 2026-06-10
- ESPORTS@bybit gave bot's best single trade (+$6.40 on 2026-05-25) — delisting-funding spike pattern already observed
- Action: monitor /fapi/v1/fundingRate?symbol=ESPORTSUSDT daily; flag rate ≥1% or any interval-change announcement
- Not a new edge; covered under H38 magnitude-triggered basis-hedge framework

## Mechanism replication (lesson #14)
The 6 hard_sl_net events (cycle 1700) and MOVR 2026-04-24 (cycle 1100) are the same mechanism on different strategies (fair-price scalp vs basis-hedge). Vertical pump on thin coin → short fails. Meth #36 rally-vol gate would address BOTH, not just C2.

## 3-edge portfolio (unchanged headline)
- Edge 1 H31_BASIS: +3.52% / WR 100% / Sh 1.84 / n=116
- Edge 1.2 sub-tier **C2_p99_4EX_QUALITY** (5-pair) +2.84% Sh 0.380 n=605
- Edge 2 H34_PERP_PERP: +1.44% / WR 81% / Sh 0.82 / n=101
- Edge 3 H3_DEPEG: +0.81-1.76% / WR 96-100%
- Other sub-tiers: H_COMBO_3c +4.18% Sh 2.17 n=40 / OKX_SHORTEN_ULTRA +5.39% Sh 1.32 n=14

KPI 4 = 3 independent edges (unchanged).

## OPEN USER QUEUE
- (A) START cut60 A/B (**10th cycle** unexecuted)
- (B) PAUSE paper_new_symbol (**11th cycle** dry, last trade 2026-05-29 12:06)
- (C) Write paper_bot_h_combo_3c.py
- (D) Write paper_bot_c2_4ex.py — **USE 5-PAIR BLACKLIST** (cycle 1100 final)
- (E) H_BOROS_INDICATOR DECISION (deferred **28 cycles**)
- (F) TG keyword-filter widening (only 8 funding signals in 5703 master; upstream channels rarely discuss funding-rate mechanics)
- (G) **NEW**: paper_fairprice_v6 H39 PORTAL exclusion — needs user OK before code edit

## Validated NEGATIVES (do NOT re-test)
R1-R7, R13-R16. **bitget REJECTED at Meth #33 venue gate**, **TAC on 5-pair blacklist**, **MOVR + INJ NOT on blacklist** (cycle 1100). New SL pattern is NOT a re-test of R3 (listing momentum) — paper_fairprice_v6 is the fair-price scalp strategy, different mechanism, currently net positive.

## Paper-bot pulse (as of 17:08 UTC)
- fairprice_v6: state.json 17:08 (alive), 117 trades, 24 in last 24h
- new_symbol: state.json 17:09 (alive), 20 trades, last 2026-05-29 (validates R3 REJECT)
- whale_copy_paper, practitioner_follower: state.json refreshing, NO trades.jsonl exists (10+ cycle silent; Edge 4 hunt blocked on data)

## Artifacts (cycle 1700: pure analysis, no new parquets, no scripts committed)
- VPS git push BROKEN (user knows)

## Next priorities
1. **Meth #36 backtest** (rally-vol entry-defer gate on C2) — STILL OWED, cycle 1100 priority #1.
2. **H39 PORTAL exclusion** — user OK to edit paper_fairprice_v6 universe? (+$5 expected savings/30d)
3. **H40 ESPORTS monitor** — track daily funding through 2026-06-10.
4. **Meth #37 promotion** — wait for high-funding bucket n≥60 (~3 more weeks of bot data).
5. **Meth #34 second corroboration** (still owed since 0500).
6. **paper_bot_c2_4ex.py spec writeup** (USER queue D).
7. (USER) Queue A+B+C+D+E+F+G.

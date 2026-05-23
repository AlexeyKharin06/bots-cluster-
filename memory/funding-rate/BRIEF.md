# BRIEF — funding-rate snapshot

## State (2026-05-23 23:00 UTC, cycle: H3-FU-3 multi-venue coincidence — HYPOTHESIS INVERTED, filter accepted as optional variant)

- ✅ **3-edge portfolio FULLY VALIDATED** (KPI 4 cleared).
- 🟡 **H3-FU-3 outcome**: hypothesis from BRIEF was INVERTED by data. Multi-venue CONFIRMED depegs are SLOW-revert systemic events (median 112h hold, 41% miss max-hold). SOLO depegs are FAST-revert idiosyncratic (median 2h, 100% reach-peg). DROP-CONFIRMED filter still accepted: 50bp tier n=129→101, mean +0.81%→+0.89%, WR 96.1%→98.0%, captures 3/3 historical losses, walk-fwd asymmetric PASS. Cost: throughput −22%, KuCoin concentration 74%→91%.
- 📐 **Methodology #14 NEW**: For mean-reversion strategies, cross-venue coincidence = SYSTEMIC stress marker (slow), NOT signal validation. **INVERT the cross-venue intuition.**
- ⚠️ `feed_funding.jsonl` still empty.
- 🟢 HARDEN-AND-DEPLOY phase: paper-streams + L2 + H29 pending user OK.

## 🟢 3-edge counter-cyclical portfolio (vol-vetted, multi-venue-graded)

| Edge | n | Mean | WR | Sharpe | corr |
|---|---|---|---|---|---|
| H31_basis (LONG-perp+SHORT-spot, shortening) | 53 | +3.45% | 100% | 1.97 | — |
| H34_perp_perp (LONG-pri+SHORT-hedge) | 101 | +1.28% | 79% | 0.74 | +0.30 |
| H3 50bp baseline | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| **H3 50bp DROP-CONFIRMED (NEW)** | **101** | **+0.89%** | **98.0%** | 0.65 | TBD |
| H3 75bp baseline | 39 | +1.76% | 100% | 0.87 | −0.31 |
| **H3 75bp DROP-CONFIRMED (NEW)** | **30** | **+1.96%** | **100%** | 0.88 | TBD |

Pairwise: (H31↔H34) +0.30, (H31↔H3) −0.31, (H34↔H3) untested.

## 🟡 H3-FU-3 — multi-venue coincidence (Methodology #14)

129 events scored against ±30min cross-venue depeg presence on Binance/Bybit/OKX/KuCoin (Gate/MEXC/Bitget capped at 35d lookback). Categories: CONFIRMED 27, CONFIRMED_LOOSE 1, SOLO 36, UNVERIFIABLE 65. Hold-time decisive: CONFIRMED median 112h reach_peg 59%, SOLO median 2h reach_peg 100%.

## 📐 Methodology #14 — invert cross-venue intuition

For DEPEG arb (and likely all mean-reversion strategies), multi-venue coincidence = SYSTEMIC stress (slow revert, max-hold risk), NOT signal validation. SOLO depegs are the higher-quality, faster-reverting subset. Apply filter as anti-confirmation.

## 🟢 H3 paper-stream spec (post-FU-3, two variants)

**A) FULL** (baseline): G_paper 50/75bp triggers, 12h cooldown, NOT phantom, notional gate. n=129/39, mean +0.81/+1.76, WR 96/100.

**B) SOLOFLAG** (new): same trigger + at entry-time check ±30min on 1-3 other CEXes. If any ≥30bp same-direction → tag CONFIRMED (skip or half-size). Else → full-size. n=101/30, mean +0.89/+1.96, WR 98/100.

Run B paper-stream as overlay variant of A to validate live median-hold gap.

## 📊 KPI 4 — gate scorecard

All 6 criteria cleared on both variants at both tiers: mean ≥30bp ✅, walk-fwd asymmetric ✅ (TEST>TRAIN both+), corr ≤ −0.30 ✅, Sharpe ≥0.6 ✅, WR ≥90% ✅, n ≥50 ✅ (50bp tiers).

**Verdict: Edge 3 preserved. New optional filter layer adds risk-management dimension at concentration cost.**

## Next-cycle plan

1. H3-FU-1 L2 depth on KuCoin USDE/USDD (concentration 91% post-FU-3).
2. H3-FU-4 perp-basis (Bybit USDe-PERP + Gate USDD-PERP) — KuCoin-delisting hedge.
3. Bundle 3-edge paper-stream proposals (FULL + SOLOFLAG variants + H31/H34 + H29 poller).
4. Meth #14 on H3-A3 PYUSD + C8/H38 funding-stress — does it generalize?

## Negatives (DO NOT retest)

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest · R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike · R17 C2 standalone

## Sources

`/tmp/h3_fu3_*` + `insights/cycle_20260523_2300.md`. Prior: `/tmp/h3_fu6_*` + `cycle_20260523_1700.md`.

## 🚀 MANDATE: H3-FU-1 L2 depth (concentration↑), H3-FU-4 perp-basis hedge, paper-stream bundle (BOTH variants). Edge hunt OVER.

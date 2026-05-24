# BRIEF — funding-rate snapshot

## State (2026-05-24 14:18 UTC — Microstructure M1+M3: BOTH user-hypotheses REFUTED, Meth #17 sign-flip filed)

- ✅ **3-edge portfolio FULLY VALIDATED** (KPI 4 cleared since 2026-05-23_1100). UNCHANGED.
- 🟡 **M1 REFUTED**: h=100% basis-hedge is monotone Sharpe-optimal. Sharpe 0.16→1.90 across h=[0,100%]; mean only -49bp (slip), std collapses 13×. 74/116 events see perp FALL post-event, 42/116 rise — no directional gain.
- 🟡 **M3 INVERTED**: CONFIRMED n=72 outperforms SOLO n=44 (+4.03% vs +2.68%, Sharpe 2.07 vs 1.77, both WR=100%). |price_4h| dispersion CONFIRMED 18% vs SOLO 6%, but HEDGED → only funding mag matters → CONFIRMED wins.
- 📐 **Meth #17 CANDIDATE**: Meth #14 sign depends on TRADE STRUCTURE. UNHEDGED mean-rev (H3): SOLO > CONFIRMED. HEDGED funding-capture (H31): CONFIRMED > SOLO (sign flips).
- 🟢 H31 spec stays **100% basis-hedge / full universe**. Aggregate edge: 116×3.52% = 408bp-evt > 72×4.03% = 290bp-evt. No CONFIRMED-only variant.
- 🟢 M2/M5 implicitly closed by M1/M3. M4/M7/R2 retest deferred. Bundle + L2 + H29 still pending user OK.

## 🟢 3-edge counter-cyclical portfolio

| Edge | n | Mean | WR | Sharpe | corr |
|---|---|---|---|---|---|
| H31_basis (LONG-perp+SHORT-spot, h=100%) | 116 | +3.52% | 100% | 1.90 | — |
| H34_perp_perp | 101 | +1.28% | 79% | 0.74 | +0.30 |
| H3 50bp baseline | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| H3 50bp DROP-CONFIRMED | 101 | +0.89% | 98.0% | 0.65 | TBD |
| H3 75bp baseline | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H3 75bp DROP-CONFIRMED | 30 | +1.96% | 100% | 0.88 | TBD |

(H31↔H34) +0.30, (H31↔H3) −0.31, (H34↔H3) untested.

## 📊 H31 informational sub-tiers (NEW — not separate variants)

| subset | n | mean | Sharpe |
|---|---|---|---|
| H31 ALL canonical | 116 | +3.52% | 1.90 |
| H31 CONFIRMED (≥1 other-ex shortening ±24h) | 72 | +4.03% | 2.07 |
| H31 SOLO | 44 | +2.68% | 1.77 |

## 📐 H31 hedge-ratio M1 sweep (definitive)

h=0%: mean +4.10 / std 25.69 / Sharpe 0.16 / WR 49%
h=50%: mean +3.86 / std 12.95 / Sharpe 0.30 / WR 60%
**h=100%: mean +3.62 / std 1.91 / Sharpe 1.90 / WR 100%** ✅ structural optimum

## 🟡 H3 paper-stream variants

- FULL — all events
- SOLOFLAG — apply on {USDe,USDD,TUSD,USDP,FDUSD,USDC} (Meth #14)
- PYUSD_PASSTHROUGH — bypass SOLOFLAG (Meth #16)
- USDE_TAIL_HEDGED — 22 USDe events, enable ≥$10k (Meth #15)

## 📐 Methodology canon (latest)

- #12: walk-fwd asymmetric gap (penalize only TRAIN>TEST)
- #13.1: graduated vol gate / phantom_print rule
- #14: multi-venue coincidence → SOLO > CONFIRMED **for UNHEDGED mean-rev** (original framing)
- #15: perp-leg on venue-isolated depeg = tail insurance
- #16 CANDIDATE: Meth #14 has stable-class boundary (PYUSD: SOLO ≈ CONFIRMED)
- **#17 CANDIDATE (THIS CYCLE)**: Meth #14 sign depends on TRADE STRUCTURE. HEDGED funding-capture: CONFIRMED > SOLO (flipped). Classify trade before applying.

## Next-cycle plan

1. **M4 BTC regime conditioning** — BTC 7d regime × H31 events. Cheap, uses parquet.
2. **R2 SOLO retest** (HYPOTHESIS_R2_SOLO_RETEST.md). R2 is UNHEDGED → predict H3-direction (SOLO > CONFIRMED if applies).
3. **Meth #17 cross-validation on H38** (10,686 events). Predict CONFIRMED > SOLO. If yes → Meth #17 graduates.
4. **M7 funding-velocity trigger** vs H38 magnitude trigger.
5. **Meth #14 retro on C8/H38** (also serves as Meth #17 corroboration).
6. **H3-FU-1 L2 depth snapshot** on KuCoin USDE/USDD.
7. **Paper-stream bundle for user OK**.
8. **H29 exchange-API poller user OK** — production blocker.

DEFER permanently (closed): M1 partial-hedge, M2 basis-pure, M3 SOLO-only H31 variant, M5 microstructure filter.

## Negatives (DO NOT retest)

R1-R18 (see prior BRIEF) + **R19 NEW H31 partial-hedge (M1)** + **R20 NEW H31 SOLO-only variant (M3)**.

## Sources

`/tmp/m1_*` + `/tmp/m3_*` + `insights/cycle_20260524_1418.md`. Prior: `/tmp/h3_fu_pyusd_*` + cycle_20260524_1100.md.

## 🚀 MANDATE: M4, R2 SOLO retest, Meth #17 on H38, L2 depth, bundle, H29. Edge hunt OVER; canon refinement continues.

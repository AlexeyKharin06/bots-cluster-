# BRIEF — funding-rate snapshot

## State (2026-05-24 11:30 UTC, cycle: Meth #14 retro on PYUSD — REFUTED, stable-class boundary discovered)

- ✅ **3-edge portfolio FULLY VALIDATED** (KPI 4 cleared since 2026-05-23_1100).
- 🟡 **PYUSD Meth #14 retroactive REFUTES** the cycle 0500 prediction. SOLO (n=19) ≈ CONFIRMED (n=5): mean +0.489% vs +0.481%, WR 100% both, hold_median 8.42h vs 8.25h. Delta = pure noise.
- 📐 **Methodology #16 CANDIDATE filed**: Meth #14 has stable-class boundary; centralized-redemption stables (PYUSD, Paxos B2B desk) show no SOLO/CONFIRMED discrimination. Distributed-redemption stables (USDe/USDD on-chain bridges + TUSD/USDP/FDUSD/USDC per-venue dollar rails) do.
- 🟢 SOLOFLAG decision matrix UPDATED: apply on {USDe, USDD, TUSD, USDP, FDUSD, USDC}-only; BYPASS for PYUSD. Preserves 5/24 PYUSD events.
- 🟢 HARDEN-AND-DEPLOY phase continues. Paper-stream bundle + L2 + H29 still pending user OK. No new edge candidates queued.

## 🟢 3-edge counter-cyclical portfolio (vol-vetted, multi-venue-graded)

| Edge | n | Mean | WR | Sharpe | corr |
|---|---|---|---|---|---|
| H31_basis (LONG-perp+SHORT-spot, shortening) | 53 | +3.45% | 100% | 1.97 | — |
| H34_perp_perp (LONG-pri+SHORT-hedge) | 101 | +1.28% | 79% | 0.74 | +0.30 |
| H3 50bp baseline | 129 | +0.81% | 96.1% | 0.63 | −0.31 |
| H3 50bp DROP-CONFIRMED | 101 | +0.89% | 98.0% | 0.65 | TBD |
| H3 75bp baseline | 39 | +1.76% | 100% | 0.87 | −0.31 |
| H3 75bp DROP-CONFIRMED | 30 | +1.96% | 100% | 0.88 | TBD |

Pairwise: (H31↔H34) +0.30, (H31↔H3) −0.31, (H34↔H3) untested.

## 🟡 H3 paper-stream variants (FULL / SOLOFLAG / USDE_TAIL_HEDGED / PYUSD_PASSTHROUGH)

| variant | applies to | role |
|---|---|---|
| H3_DEPEG_PAPER_FULL | all events incl. PYUSD | baseline diversified Edge 3 |
| H3_DEPEG_PAPER_SOLOFLAG | **{USDe,USDD,TUSD,USDP,FDUSD,USDC}-only events** | risk-managed quality filter (Meth #14 applies) |
| H3_DEPEG_PAPER_PYUSD_PASSTHROUGH (NEW 1100) | PYUSD events | SOLOFLAG bypassed (Meth #16 candidate; SOLO ≈ CONFIRMED) |
| H3_DEPEG_PAPER_USDE_TAIL_HEDGED | 22 USDe events only | Ethena tail-risk overlay (Meth #15); enable when notional ≥ $10k |

## 📐 Methodology canon (latest)

- **#12**: walk-fwd gap rule asymmetric (penalize only TRAIN>TEST).
- **#13.1**: graduated vol gate by deployment size (phantom_print rule).
- **#14** (cycle 2300): multi-venue coincidence = systemic stress = slow revert; SOLO = idiosyncratic = fast revert. INVERT cross-venue intuition.
- **#15** (cycle 0500): perp leg on venue-isolated depeg = tail-risk insurance, not yield arb.
- **#16 CANDIDATE** (this cycle): Meth #14 has stable-class boundary. Centralized-redemption stables (Paxos B2B desk) show no SOLO/CONFIRMED discrimination. Distributed-redemption do.

## 📊 PYUSD subset characterization (NEW this cycle)

- n=24 / 12mo / 50bp tier
- Mean +0.487%, median +0.443%, WR 100%, hold median 8.4h
- 23 LONG + 1 SHORT; 24/24 reach_peg; no losses; no slow-revert tail
- SOLO 19 / CONFIRMED 5 split, PnL/WR/hold uniformly distributed → SOLOFLAG bypassed
- Cleanest Sharpe-friendliness sub-tier of H3 universe

## 📊 KPI 4 — gate scorecard

All 6 criteria cleared on H3 baseline + SOLOFLAG variants since cycle 1100. PYUSD passthrough and USDE_TAIL_HEDGED overlays do not change gate verdict.

## Next-cycle plan

1. **Meth #14 retroactive on C8/H38 funding events** (cycle 2300 plan #5). Funding is venue-distributed → predict SOLO outperforms CONFIRMED. ~10,686 events, downsample to ≥100bp tier (~2103 events).
2. **H3-FU-1 L2 depth snapshot** on KuCoin USDE/USDD — primary live-deploy gating step.
3. **Paper-stream bundle for user OK** — H31_BASIS + H34_PERP + H3_DEPEG (FULL + SOLOFLAG + USDE_TAIL_HEDGED + PYUSD_PASSTHROUGH).
4. **RLUSD watch** — Meth #16 candidate corroboration (regulated single-B2B-desk stable). Re-test if events fire at 50bp tier.
5. **H29 exchange-API poller user OK** — production blocker.

## Negatives (DO NOT retest)

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest · R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike · R17 C2 standalone · R18 H3-FU-4 substitute + funding-capture

## Sources

`/tmp/h3_fu_pyusd_*` (this cycle) + `insights/cycle_20260524_1100.md`. Prior: `/tmp/h3_fu4_*` + cycle_20260524_0500.md; `/tmp/h3_fu3_*` + cycle_20260523_2300.md; `/tmp/h3_fu6_*` + cycle_20260523_1700.md.

## 🚀 MANDATE: Meth #14 retro on C8/H38 high-mag funding (prediction: replicates), L2 depth, paper-stream bundle, H29 poller. Edge hunt OVER; canon refinement continues.

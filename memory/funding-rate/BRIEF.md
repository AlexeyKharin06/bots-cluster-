# BRIEF — funding-rate snapshot

## State (2026-05-24 05:30 UTC, cycle: H3-FU-4 stable-perp basis — REJECTED as yield, ACCEPTED as tail-risk insurance overlay)

- ✅ **3-edge portfolio FULLY VALIDATED** (KPI 4 cleared since 2026-05-23_1100).
- 🟡 **H3-FU-4 outcome**: BRIEF cycle 2300 hypothesis ("2-3× yield via perp-basis capture") REJECTED. Universe of stable-PERP listings on 7 CEXes = literally {Bybit USDeUSDT-PERP}. Tested on 21 of 22 KuCoin USDe events: Bybit perp stays within ±10bp of $1 even during +1246bp / +852bp spot spikes. Substitute REJECTED (-0.004%/WR 27%), funding capture REJECTED (0 of 1713 fundings ≥30bp). Delta-hedge ACCEPTED only as tail-risk insurance for Ethena protocol risk (combined +2.00%/WR 95% ≈ spot-only +2.00%/WR 100%, ~20bp extra cost; useful only at $10k+ notional).
- 📐 **Methodology #15 NEW**: perp leg on venue-isolated depeg = tail-risk insurance, not arb. Third independent line of evidence for Methodology #14.
- ⚠️ `feed_funding.jsonl` still empty.
- 🟢 HARDEN-AND-DEPLOY phase: paper-streams + L2 + H29 pending user OK. No new edge candidates queued.

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

## 🟡 H3 paper-stream variants (FULL / SOLOFLAG / USDE_TAIL_HEDGED)

| variant | applies to | role |
|---|---|---|
| H3_DEPEG_PAPER_FULL | all 129 events | baseline diversified Edge 3 |
| H3_DEPEG_PAPER_SOLOFLAG | all 129 (drop CONFIRMED at entry-time) | optional risk-management filter (cycle 2300 / Meth #14) |
| **H3_DEPEG_PAPER_USDE_TAIL_HEDGED (NEW 0500)** | 22 USDe events only | optional Ethena protocol-tail-risk overlay (Meth #15); enable when notional ≥ $10k |

## 📐 Methodology #14 (cycle 2300) + #15 (this cycle) — converging evidence

Two independent vantage points now confirm that KuCoin USDe spot depegs are **venue-isolated SOLO events**, not systemic CEX-wide depegs:
- #14: ±30min cross-venue SPOT coincidence on Binance/Bybit (where listed) — 20 of 22 USDe events in SOLO category.
- #15: Bybit USDe-PERP at-peg behavior during 21 of 21 covered KuCoin spot depegs (perp at $1±10bp during +1246bp spot spike).

Implication: depeg arb mechanism is KuCoin-orderbook-local, not protocol-systemic, for the dominant USDe subset. Mean-reversion is fast (median 2h hold per Meth #14) because no broader force sustains the depeg.

## 📊 KPI 4 — gate scorecard

All 6 criteria cleared on H3 baseline + SOLOFLAG variants at both tiers since cycle 1100. USDE_TAIL_HEDGED overlay does not change gate verdict; preserves +2.00% mean / 95% WR on USDe subset at ~20bp cost.

**Verdict: Edge 3 preserved. New optional tail-hedge overlay adds Ethena-protocol-risk-management dimension for live deployment at scale.**

## Stable-perp universe (NEW finding 0500)

Exhaustive scan across Binance/Bybit/OKX/Gate/Bitget/MEXC/Hyperliquid for {USDe,USDD,USDP,TUSD,FDUSD,PYUSD}-quoted perpetuals: ONLY Bybit USDEUSDT-PERP. No USDD-perp anywhere. Structural ceiling on perp-leg strategies for stable arb.

## Next-cycle plan

1. H3-FU-1 L2 depth on KuCoin USDE/USDD (concentration 91% post-FU-3 SOLOFLAG, structural since no perp substitute per FU-4).
2. Methodology #14 retroactive on PYUSD events (cycle 2300 plan #4).
3. Methodology #14 retroactive on C8/H38 high-mag funding events (cycle 2300 plan #5).
4. Bundle 3-edge paper-stream proposals (FULL + SOLOFLAG + USDE_TAIL_HEDGED overlay + H31/H34 + H29 poller).
5. (Deferred indefinitely) H3-FU-4 perp-basis as yield — REJECTED this cycle.

## Negatives (DO NOT retest)

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest · R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike · R17 C2 standalone · R18 H3-FU-4 substitute + funding-capture (Bybit perp non-tracking; mean -0.004%/WR 27%; 0 of 1713 fundings ≥30bp)

## Sources

`/tmp/h3_fu4_*` (this cycle) + `insights/cycle_20260524_0500.md`. Prior: `/tmp/h3_fu3_*` + cycle_20260523_2300.md; `/tmp/h3_fu6_*` + cycle_20260523_1700.md.

## 🚀 MANDATE: H3-FU-1 L2 depth (only remaining live-deploy gating step), Meth #14 retroactives (PYUSD + C8/H38), paper-stream bundle (3 H3 variants + H31 + H34 + H29). Edge hunt OVER.

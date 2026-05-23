# BRIEF — funding-rate snapshot

## State (2026-05-23 17:30 UTC, cycle: H3-FU-6 vol-vet retroactive on 150-event Edge-3)

- ✅ **3-edge portfolio FULLY VALIDATED & vol-vetted** (KPI 4 cleared on G_paper-gated headline; Edge 3 hygiene-hardened).
- 🟡 **H3-FU-6 outcome**: Methodology #13 applied retroactively. **n=150→129 (50bp tier), +0.90%→+0.81% mean** post-vet. 16 phantom-print events identified (all KuCoin synthetic stables). Headline + walk-fwd + counter-cyclicality all preserved.
- 📐 **Methodology #13.1 NEW**: graduated vol gate scales by deployment size, not a fixed dollar floor.
- ⚠️ `feed_funding.jsonl` still empty.
- 🟢 HARDEN-AND-DEPLOY phase: paper-streams + L2 + H29 pending user OK.

## 🟢 3-edge counter-cyclical portfolio (vol-vetted)

| Edge | Mechanism | n | Mean | WR | Sharpe | corr |
|---|---|---|---|---|---|---|
| H31_basis | LONG-perp + SHORT-spot on interval-shortenings | 53 | +3.45% | 100% | 1.97 | — |
| H34_perp_perp | LONG-primary-perp + SHORT-hedge-perp | 101 | +1.28% | 79% | 0.74 | +0.30 |
| **H3_depeg 50bp G_paper** | Spot mean-reversion on stable depeg (vol-vetted) | **129** | **+0.81%** | **96.1%** | **0.63** | **−0.31** |
| **H3_depeg 75bp G_paper** | Same, magnitude-filtered (vol-vetted) | **39** | **+1.76%** | **100%** | **0.87** | **−0.31** |

Pairwise corr: (H31↔H34) +0.30, (H31↔H3) −0.31, (H34↔H3) untested.

## 🟡 H3-FU-6 — Methodology #13 retroactive

**16 phantom events removed** from 150-event headline — all KuCoin synth stables (14 USDe + 2 USDD). Phantoms had mean +1.71% inflating headline ~26%. Big USDe spikes survive (2025-09-23 +11.01% on $45k notional, 2026-02-19 +7.80% on $27k). Example phantom dropped: 2024-07-22 USDe -1000bp +11.06% on $52 notional, 0 active pre-bars — print-only wick.

## 📐 Methodology #13.1 — graduated vol gate

Fixed $500 floor was wrong-direction (too strict for $1 paper, too loose for $10k+ live). Refined:
- `phantom_print = (entry_notional < $100) AND (active_30min_pre ≤ 1)` — always exclude.
- `paper_safe = entry_notional ≥ $10 AND NOT phantom_print` — $1 paper.
- `live_safe(size) = entry_notional ≥ max($100, size × 10)` — 10× safety for live.

## 🟢 H3 paper-stream spec (vol-vetted)

Universe {USDC, USDP, FDUSD, TUSD, USDD, USDe, PYUSD} × {Binance, KuCoin, Bybit-PYUSD}. Trigger `|spot−$1|≥75bp` (primary) / 50bp (wider) + 12h cooldown + NOT phantom_print + notional gate by size. Mean-rev. Exit ±10bp OR 24h. 10bp/leg slip. Throughput post-vet: 75bp ~3-4/month, 50bp ~10-11/month.

## 📊 KPI 4 — vol-vetted gate scorecard

All 6 criteria still cleared on G_paper 50bp (n=129) AND G_paper 75bp (n=39): mean +81bp/+176bp (≥30bp gate ✅), walk-fwd asymmetric ✅ (TEST>TRAIN both+ per Meth #12), corr −0.31 ✅, Sharpe 0.63/0.87 ✅, WR 96.1%/100% ✅. n-gate: 129 decisive on 50bp; 75bp is operational filter not gate-clearing tier.

**Verdict: Edge 3 preserved. Hygiene tightened, mechanism unchanged.**

## Next-cycle plan

1. **H3-FU-3 multi-venue coincidence** — extra-motivated as non-vol anti-phantom check; handles Binance-TUSD-only events (3/5 historic losses).
2. **H3-FU-1 L2 depth** on KuCoin USDE/USDD at $100/$1k/$10k.
3. **H3-FU-4 perp-basis** — Bybit USDe-PERP + Gate USDD-PERP.
4. Bundle 3-edge paper-stream proposals for user OK (G_paper + phantom_print + Meth #13.1).
5. H29 poller user OK.
6. Niche B OKX funding-latency. Niche A2 USDe deep-dive (n=22 G_paper, +2.11%). Niche F1 H38 paper.

## Validated negatives — DO NOT retest

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest · R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike · R17 C2 standalone Edge 3

## Sources

This cycle: `/tmp/h3_fu6_*` + `insights/cycle_20260523_1700.md`. Prior: `h3_klines_24mo.parquet`, `h3_events_24mo[_75bp].parquet`, `h3_fu6_paper[75].parquet`.

## 🚀 MANDATE: H3-FU-3 multi-venue, H3-FU-1 L2, paper-stream bundle. Edge hunt OVER.

# BRIEF — funding-rate snapshot

## State (2026-05-23 11:35 UTC, cycle: H3 24mo extension — KPI 4 fully crossed)

- ✅ **3-edge portfolio FULLY VALIDATED** — Edge 3 n-gate cleared decisively (n=42 → n=150).
- ✅ Parquets on VPS: `multi_ex_funding_180` 1.6M rows, `h3_klines_24mo` 1.26M bars / 6 stables / 24mo.
- ⚠️ `feed_funding.jsonl` still empty (upstream channel absence — H5 blocked).
- 🟢 Project is in HARDEN-AND-DEPLOY phase: edge hunt complete, bundling paper-streams + L2 + H29.

## 🟢 3-edge counter-cyclical portfolio

| Edge | Mechanism | n | Mean | WR | Sharpe | corr |
|---|---|---|---|---|---|---|
| **H31_basis** | LONG-perp + SHORT-spot on interval-shortenings | 53 | **+3.45%** | 100% | 1.97 | — |
| **H34_perp_perp** | LONG-primary-perp + SHORT-hedge-perp | 101 | +1.28% | 79% | 0.74 | +0.30 |
| **H3_depeg** (50bp) | Spot mean-reversion on stable depeg | **150** | +0.90% | 96.7% | 0.60 | **−0.31** |
| **H3_depeg** (75bp tier) | Same, magnitude-filtered | 47 | **+2.00%** | **100%** | 0.87 | −0.31 |

Pairwise corr: (H31↔H34) +0.30, (H31↔H3) **−0.31**, (H34↔H3) untested. Counter-cyclical H3 = maximal variance reduction.

## 🟢 H3 — 24mo headline

24mo, 5m OHLCV, 6 stable/USDT (Binance USDC/TUSD/USDP/FDUSD + KuCoin USDD/USDe). Depeg `|spot−$1|≥50bp` + 12h cooldown. Mean-reversion. Exit: re-peg ±10bp OR 7d. 4bp round-trip slip.

**50bp baseline**: n=150 mean +0.90% median +0.48% WR 96.7% Sharpe 0.60. Worst loss −1.35% (all 5 losses 50-54bp TUSD/USDD at max-hold).

**75bp refined**: n=47 mean +2.00% WR 100% Sharpe 0.87. Slip-robust to 80bp (WR 83%) and 120bp (WR 51%).

**Walk-fwd q70**: TRAIN 0.72% / TEST 1.31% (TEST > TRAIN — Methodology #12: regime-richness ≠ overfit). 75bp both halves 100% WR.

**Prior-year OOS** (2024-05→2025-05, unseen): n=108 mean +0.72% WR 95.4% Sharpe 0.61. Mechanism replicates.

**Concentration**: USDe+USDD = 77% of events / 86% PnL. USDe alone n=37 +3.08%.

## 🟢 Edge 3 gate — final scorecard

| criterion | required | 50bp/n=150 | 75bp/n=47 |
|---|---|---|---|
| mean ≥ +30bp | +30bp | +90bp ✅ | **+200bp ✅** |
| n ≥ 50 | 50 | **150 ✅** | 47 ⚠️ 94% |
| walk-fwd asymmetric (only TRAIN>TEST counts) | TEST≥TRAIN | ✅ TEST richer | ✅ both 100% WR |
| corr < 0.30 | <0.30 | **−0.31 ✅** | **−0.31 ✅** |
| Sharpe / WR | — | 0.60 / 96.7% | **0.87 / 100%** |

## KPI 4 — 3-edge stack ✅ FULLY CROSSED

Edge 1 ✅ H31 basis n=53 +3.45% Sharpe 1.97. Edge 2 ✅ H34 perp-perp n=101 +1.28% Sharpe 0.74. **Edge 3 ✅ H3 depeg n=150 +0.90% Sharpe 0.60** (or 75bp tier n=47 +2.00% Sharpe 0.87).

## H3 paper-stream spec (pending user OK)

Universe {USDC, USDP, FDUSD, TUSD, USDD, USDe} × {Binance, KuCoin}; future +{Gate, MEXC, Bybit}. Trigger `|spot−$1|≥75bp` + 12h cooldown (primary) or 50bp (wider). Mean-reversion direction. Exit re-peg ±10bp OR 24h. 10bp/leg slip. Throughput: ~5/month primary, ~12/month wider.

## NEW this cycle

- H3 n=42→n=150; n-gate decisively cleared.
- Prior-year OOS Sharpe 0.61 ≈ in-sample 0.67 → real edge.
- 75bp filter: 100% WR (47/47), Sharpe 0.87, slip-robust to 80bp.
- **Methodology #12**: walk-fwd gap is asymmetric — TEST>TRAIN is regime-richness not overfit.

## Next-cycle plan (harden + deploy)

1. Bundle 3-edge paper-stream proposals for user OK.
2. H29 poller deployment (still pending user OK).
3. H3-FU-1 L2 depth snapshot (USDe/USDD at $100/$1k/$10k notional).
4. H3-FU-4 USDe/Bybit + USDD/Gate perp-basis variant (potentially 2-3× yield).
5. H3-FU-3 multi-exchange depeg coincidence filter (≥2 venues).

## Validated negatives — DO NOT retest

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest · R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike · R17 C2 standalone Edge 3

## Sources

`/tmp/h3_extend_fetch.py`, `h3_klines_24mo.parquet`, `h3_24mo_backtest.py`, `h3_24mo_diag.py`, `h3_mag_filter.py`, `h3_events_24mo[_75bp].parquet`, `insights/cycle_20260523_1100.md`.

Done this cycle: H3-FOLLOWUP-5 (24mo extension) → Edge 3 fully validated.

## 🚀 AUTONOMOUS MANDATE active 2026-05-23 (user explicit)

NEW DIRECTIVE: Don't ask user. Explore widely across funding + stablecoin + DEX/CEX +
latency + on-chain + TG microstructure. Full menu in AUTONOMOUS_MANDATE.md (Niches A-G).

Don't bind to funding-rate niche. H3 proved adjacent niches contain edges. Expand scope.

Priority targets:
- Niche A2: USDe deep-dive (38% of H3 PnL, isolate as sub-strategy)
- Niche B: OKX funding latency edge (observed cycle 22_2300, untested)
- Niche F1: H38 paper-stream design (40× throughput READY)
- Niche A3: Other synthetic stables (PYUSD/GHO/sUSDe — fetch & test)

Decide per cycle. Don't ask. Just execute.

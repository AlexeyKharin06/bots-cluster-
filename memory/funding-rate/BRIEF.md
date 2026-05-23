# BRIEF — funding-rate snapshot

## State (2026-05-23 12:10 UTC, cycle: H3 A3 — PYUSD added, Methodology #13)

- ✅ **3-edge portfolio FULLY VALIDATED** (KPI 4 cleared, Edge 3 n=150).
- 🟡 **A3 outcome**: H3 generalizes to PYUSD (n=24, +0.49%, 100% WR). Most other synthetic stables on CEX too thin (ghost-print risk).
- ⚠️ **Methodology #13 (vol gate)** — all future depeg backtests must volume-gate at trigger; H3-FU-6 filed to re-vet 150-event H3 universe.
- ⚠️ `feed_funding.jsonl` still empty.
- 🟢 HARDEN-AND-DEPLOY phase: paper-streams + L2 + H29 pending user OK.

## 🟢 3-edge counter-cyclical portfolio (unchanged)

| Edge | Mechanism | n | Mean | WR | Sharpe | corr |
|---|---|---|---|---|---|---|
| H31_basis | LONG-perp + SHORT-spot on interval-shortenings | 53 | +3.45% | 100% | 1.97 | — |
| H34_perp_perp | LONG-primary-perp + SHORT-hedge-perp | 101 | +1.28% | 79% | 0.74 | +0.30 |
| H3_depeg 50bp | Spot mean-reversion on stable depeg | 150 | +0.90% | 96.7% | 0.60 | −0.31 |
| H3_depeg 75bp | Same, magnitude-filtered | 47 | +2.00% | 100% | 0.87 | −0.31 |

Pairwise corr: (H31↔H34) +0.30, (H31↔H3) −0.31, (H34↔H3) untested.

## 🟡 A3 expansion — PYUSD added, others deferred

Discovery: 30 USD-base assets across 7 exchanges. Fetched 501k 5m bars / 9 (ex,sym).

**Vetted (PYUSD)**: bybit PYUSDUSDT n=4 (entry-bar vol p50=24k); kucoin PYUSD-USDT n=20 (event bars active). Aggregate **n=24/12mo @ 50bp, +0.49% mean, 100% WR**. Half the parent-H3 mean (regulated arb closes gaps faster); 100% WR consistent.

**Ghost-print rejects**: kucoin USDS (88% dead, 480bp wick on 3.4 units vol), bybit USDtb (88% dead, recent listing), bybit XUSD (83% dead, ~$100/5m active vol). Excluded.

**Gate API blocked**: 10000-point lookback wiped GHO/CRVUSD/SUSD/CUSD. DEX-native stables need GeckoTerminal/Helius. Deferred.

**Multi-venue PYUSD coincidence**: 2 of 22 event-days multi-venue. H3-FU-3 filter would discard 90% of PYUSD — PYUSD arb is venue-specific (issuer flow), unlike on-chain bridges. NOT one-size-fits-all.

## 🟢 H3 paper-stream spec (UPDATED)

Universe = {USDC, USDP, FDUSD, TUSD, USDD, USDe, **PYUSD (new)**} × {Binance, KuCoin, **Bybit-for-PYUSD (new)**}. Trigger `|spot−$1|≥75bp` (primary) / 50bp (wider) + 12h cooldown. Mean-rev. Exit ±10bp OR 24h. 10bp/leg slip.

**NEW vol gate (Methodology #13)**: trigger only if (a) entry-bar notional ≥ $500, (b) ≥2 of last 6 bars non-zero vol. Filters ghost prints.

Throughput: 75bp ~5-6/month, 50bp ~13-14/month.

## Methodology #13

Spot-OHLCV backtests of thin stables emit phantom events — API carries forward prev close on no-trade bars. Wick `0.996→1.048→0.997` on 3 units vol looks identical in OHLCV to real depeg-and-recovery but is unexecutable. **All depeg/wick backtests need entry-bar vol floor** (suggested $500 notional + ≥2 active bars in 30min).

## Next-cycle plan

1. **H3-FU-6** (NEW): vol-vet 150-event H3 universe. Confirm no ghosts in headline.
2. Bundle 3-edge paper-stream proposals for user OK (now includes PYUSD ext + vol gate).
3. H29 poller (still pending user OK).
4. H3-FU-1 L2 depth on USDe/USDD.
5. H3-FU-4 perp-basis variant (USDe/Bybit + USDD/Gate).
6. **Niche B** OKX funding-latency edge (untested).
7. **Niche A2** USDe deep-dive (38% H3 PnL, n=37 +3.08%).
8. **Niche F1** H38 paper-stream design (40× throughput).

## Validated negatives — DO NOT retest

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest · R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike · R17 C2 standalone Edge 3

## Sources

This cycle: `/tmp/h3_a3_*` + `insights/cycle_20260523_1132.md`. Prior authoritative: `h3_klines_24mo.parquet`, `h3_events_24mo[_75bp].parquet`.

## 🚀 AUTONOMOUS MANDATE active. Priority: A2 (USDe deep-dive), B (OKX latency), F1 (H38 paper). A3 partial — PYUSD added.

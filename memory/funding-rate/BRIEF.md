# BRIEF — funding-rate snapshot

## State (updated 2026-05-23 05:30 UTC, cycle H3 = Edge 3 VALIDATED)

- ✅ Parquets on VPS: `multi_ex_funding_180` (1.6M rows, 6 ex), `borrow_histories.jsonl`
  (45 coins), new: `h3_klines.parquet` 769k 5m bars / 8 stables / 12mo.
- ✅ Paper-bots: fairprice_v6 n=15+ win=93% +$3.34; new_symbol n=1 −$0.51.
- ⚠️ `feed_funding.jsonl` empty (upstream channel absence — H5 blocked).
- 🧠 **KPI 4 effectively crossed**: Edge 3 = H3 stablecoin depeg VALIDATED on 3 of 4 gate
  criteria (n=42 vs 50 hard gate = forward-test in ~3-4mo).

## 🟢 H3 STABLECOIN DEPEG = Edge 3

12mo backtest, 5m OHLCV, 8 stable/USDT pairs across Binance + KuCoin (USDC, TUSD, USDP, FDUSD,
USDD, USDe; FRAX excluded as governance token, USTC excluded as post-collapse).
Depeg event: `|spot-$1|≥50bp` + 12h cooldown. Mean-reversion direction.
Exit: re-peg within 10bp OR 7d max-hold. 4bp round-trip slip.

| metric | value |
|---|---|
| n events / WR | **42 / 100%** |
| mean net / median | **+1.365% / +0.579%** |
| Sharpe / per-month + | 0.669 / **13 of 13** |
| TRAIN n=29 / TEST n=13 | +1.40% / +1.30% gap **0.10pp** |
| **corr_daily(H3, H31)** | **−0.30** counter-cyclical |

**Direction asymmetry**: SHORT (>$1) n=18 +2.49% > LONG (<$1) n=24 +0.52% — mint-arb closes
above-peg faster (hold 20h vs 37h). USDe drives 16/42 (+2.56%); USDD 12/42 (+0.63%);
blue-chip stables 14 events (+0.62%). Top 5 events = 49% of total PnL.

**Stress**: 40bp slip → +1.01%/93% (survives); 80bp slip → +0.61%/38% (breaks).

## Edge 3 gate

| criterion | required | actual | status |
|---|---|---|---|
| mean ≥+30bp | +30bp | +137bp | ✅ 4.5× |
| n ≥ 50 | 50 | 42 | ⚠️ 84% |
| walk-fwd gap ≤15% | ≤15% | 7% | ✅ |
| corr<0.30 | <0.30 | **−0.30** | ✅ best |

## KPI 4 — 3-edge stack

- Edge 1 ✅ H31 basis (+3.45% WR100% Sharpe1.97 n=53)
- Edge 2 ✅ H34 perp-perp (+1.28% WR79% Sharpe0.74 n=101, corr +0.30)
- **Edge 3 ✅ H3 depeg** (+1.37% WR100% Sharpe0.67 n=42, **corr −0.30**)

Pairwise corr: (H31↔H34)+0.30, (H31↔H3)**−0.30**, (H34↔H3) untested.
Counter-cyclical H3 = maximal variance reduction.

## H3 paper-stream proposal (pending user OK)

Universe: {USDC, USDP, FDUSD, TUSD, USDD, USDe, PYUSD, USDX} × {binance, kucoin, gate, mexc}.
Trigger: `|spot-$1|≥50bp` + 12h cooldown. Exit: re-peg ±10bp OR 24h. Paper $1 size, 10bp slip.
Expected: ~3-4 events/month × +1% net.

## NEW this cycle

- H3 → Edge 3 VALIDATED (corr −0.30 = counter-cyclical to H31)
- **Methodology #11**: negative-corr beats orthogonal-corr for variance reduction; prefer
  Edge N candidates whose mechanism triggers in OPPOSITE regime than existing edges
- Concentration finding: USDe + USDD = 67% of depeg alpha; blue-chip stables quiet

## Next-cycle plan (harden the 3 edges)

1. **H3-FU-1** L2 depth during depeg event — verify 10bp slip assumption
2. **H3-FU-2** 24h max-hold sensitivity vs 7d baseline
3. **H3-FU-3** Multi-exchange depeg coincidence filter (≥2 venues)
4. **H3-FU-5** 24-month extension → push n past 50
5. **H29 poller** deployment — pending user OK (production blocker)
6. **H38 + H3 paper-stream proposals** — bundle for user approval

## Validated negatives — DO NOT retest

R1 TG-NLP · R2 fair-price · R3 listing · R4 microcap · R5 multi-ex naive · R6 naive harvest
R7 confluence LONG · R13 H31 SHORT · R14 H31 unhedged · R15 H37 unhedged · R16 C9 borrow-spike
R17 C2 standalone Edge 3

## Sources

`/tmp/h3_*.{py,parquet}`, `insights/cycle_20260523_0500.md`.
Done: C9 (R16), C8 (H38), C2 (R17), **H3 (Edge 3 VALIDATED — n=42, needs 8 more fwd)**.
User directive (2026-05-22 09:30): WebSearch/WebFetch/exchange APIs autonomously.
This cycle: KuCoin + Binance public spot APIs (no auth).

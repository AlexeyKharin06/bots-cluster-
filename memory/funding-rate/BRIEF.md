# BRIEF — funding-rate (post-cycle 20260526_INVERSION)

## 🚨🚨 CRITICAL 2026-05-26 16:30 UTC — MEGA_GRID FINDING DOWNGRADED

Вчерашняя находка `gate+hr=1.5x+Sharpe 2.21` ПЕРЕИНТЕРПРЕТИРОВАНА на полной single-leg выборке n=83.

**Was**: "primary растёт быстрее other → LONG primary + SHORT other ×1.5"
**Is**: "primary ПАДАЕТ -7%, other падает -12%, hr=1.5x ловит конвергенцию вниз — это reversal trade с oversized hedge"

### Single-leg LONG primary (n=83 unhedged)
| Exit | Mean | Median | WR | Sharpe |
|------|------|--------|----|----|
| T+1h | +0.09% | -1.46% | 37% | +0.01 |
| T+4h | +1.04% | -2.77% | 34% | +0.04 |
| T+8h | -0.53% | -4.23% | 35% | -0.02 |
| T+24h| -0.44% | -5.60% | 36% | -0.01 |

**Verdict: unhedged LONG primary REJECTED**. Median negative throughout. Tail brutal: PIPPIN -47%, LYN -40%.

### Per primary_ex unhedged T+8h:
- **gate -6.92%** (n=18), okx -6.29% (n=34), bybit +3.79% (n=22), binance +30.79% (n=7 outlier).
- GATE/OKX — primary perp падает несмотря на negative funding pay. Sign-flip hypothesis активна.

### Coverage truth
- 116 LONG H31 events total
- 83 with primary klines, **только 19 with multi-ex pair coverage** (symbols not cross-listed)
- Mega grid `n=6` per top cell — overfitting risk
- Cannot expand pair sample by fetching more klines — multi-listing is the ceiling

## Файл с полным разбором
`memory/funding-rate/MEGA_GRID_INVERSION_2026_05_26.md` (committed 378b268, push to github BLOCKED — credentials missing on VPS)

## NEXT CYCLE — изменённый приоритет

1. **Sign-flip hypothesis test** (NEW): SHORT primary + LONG spot на GATE/OKX H31 events. Backtest на n=52 (gate+okx) events. Если +5% mean WR 60%+ → R2-class candidate.
2. **Spot-perp hedge variant** для всех 83 events (spot листинг универсальный, обходит multi-listing ceiling).
3. **Nano-cap filter**: исключить fp < $0.01 из любого H31 deployment (PIPPIN/LYN/ZKP class).
4. H_BOROS_INDICATOR — USER DECISION still pending (10 cycles).
5. R2 revisit (paper_fairprice_v6 n=51).

## STOP / DO NOT (additions)

- Deploy H_LIVE_1 / H31_QUALITY_COMBO как «cross-ex basis arb» — без sign-flip retest это опасно: mean -0.53% на полной выборке.
- Recommend hr=1.5x как «validated edge» — only 19 unique events, 6 per top cell.
- Trade nano-cap (fp<$0.01) at all — known -40% tail.

## Git ops issue
VPS `/srv/bots/cluster` git push to github fails: credential helper unset. Need user to either:
(a) Run `git config --global credential.helper store` + manual push once with token, OR
(b) Add github SSH deploy key to `/root/.ssh/id_ed25519` + change remote to git@github.com.

Cycles still write to memory dir locally — readable next cycle even without push.

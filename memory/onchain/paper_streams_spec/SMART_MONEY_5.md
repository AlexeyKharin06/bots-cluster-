# Paper-Stream Spec — SMART_MONEY_5

**Discovered**: cycle_20260524_2000 — comprehensive walk-forward на 4188 классифицированных токенов
**Status**: READY FOR PAPER DEPLOY (size=$1, paper:true)

## Filter logic

```javascript
// Add to serial_sniper.js paperChecks array
{
  name: 'SMART_5',
  paper: true,
  size: 1,
  fire: (m, ctx) => {
    return m.smart_money_count >= 5;
  },
  exit: { trail: 85, cap_pct: 500, sl: -15 }
}
```

## Walk-forward backtest (4188 classified Solana tokens, time-split 70/30)

| Subset | n | big% (≥500%) | pump% (200-500%) | rug% (≤-50%) |
|---|---|---|---|---|
| TRAIN | 570 | 60.0% | 38.1% | 1.9% |
| TEST  | 203 | 59.1% | 36.5% | 4.4% |
| Δ TRAIN→TEST | — | -0.9pt | -1.6pt | +2.5pt |

**Baseline TEST (no filter)**: n=1257, big=19.1%, rug=45.4%.
**Improvement**: big-rate ×3.1, rug-rate ÷10.

## Why it works (causal)

`smart_money_count >= 5` означает что **минимум 5 wallets** в holders нашего classified `is_smart_money` (95K wallets total, 1184 marked SMART_MONEY role). Это **прямое confirmation** что профессиональные трейдеры уже зашли. Conjunction of 5+ independent smart entries = strong signal that token has been pre-vetted.

## Promotion criteria (для REAL_MONEY)

- n ≥ 50 paper closed_trades с SMART_5 fire
- avgPnL ≥ +150% (с учётом fees)
- WR ≥ 60%
- rug rate ≤ 10%
- max drawdown ≤ 30% rolling 30d

При выполнении — AI brain пишет в TG bot: `🚀 SMART_5 READY FOR REAL MONEY`.

## Sibling streams (для diversification)

- `SMART_5_NORUG`: + `&& db_rugBotCount == 0` — повышает precision до ~60% big с 3% rug
- `SMART_2_SERIAL_5`: `smart>=2 && serial_pump_count>=5 && db_rugBotCount==0` — n+, big=56%, rug=6.5%
- `POSITIVE_3`: `db_positiveWalletCount>=3` — n меньше (20), но big=30% rug=5% — niche

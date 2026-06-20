# 🎯 POST-VACATION PLAYBOOK — 3 недели live + comprehensive analysis

**Generated:** 2026-06-20 (после 3 недель paper trading 60 стратегий)

## TL;DR — БРУТАЛЬНАЯ ПРАВДА

**Из 60 стратегий ни одна не прошла live validation.** Total PnL: **-$8,335** на $100/trade за 19.9 дней (36,356 trades).

| Verdict | Count |
|---------|-------|
| ✓ CONFIRMED (backtest подтвердился) | **0** |
| ⚠ DEGRADED (positive но -59 to -100% от ожидаемого) | 6 |
| ✗ KILLED (backtest +, live -) | 22 |
| NO_TRADES (триггер не сработал) | 6 |
| NEW_ONLY (нет hist reference) | 14 |

**RECOMMENDATION: NO real money deploy.** Лучшие "positive" имеют Sharpe 0.04-0.08 = шум.

---

## 1) Cross-validation HISTORY vs LIVE (36 стратегий с hist reference)

| Strategy | Hist mean | Live mean | Verdict |
|----------|-----------|-----------|---------|
| S25 BLUR borrow squeeze | +25.62% | **-4.18%** | ✗ KILLED catastrophic |
| S43 KAT borrow squeeze | +12.89% | -3.11% | ✗ KILLED |
| S08 MOD_SHORT high funding | +11.98% | -0.30% | ✗ KILLED |
| S27 AXS borrow squeeze | +9.61% | -2.68% | ✗ KILLED |
| S15 EXTREME_NEG_LONG | +4.80% | -1.38% | ✗ KILLED |
| S06 DEEP_NEGATIVE_LONG | +4.80% | -0.60% | ✗ KILLED |
| S35 BTC_WEAK_BEAR | +5.39% | -0.78% | ✗ KILLED |
| S50 TRIPLE_CONFLUENCE | +4.27% | -0.40% | ✗ KILLED |
| S47 US_SESSION_LONG | +3.63% | -0.52% | ✗ KILLED |
| S51-S54 Fair-price (все 4) | +1.5-3.0% | -0.1 to -0.3% | ✗ KILLED ALL |
| S56-S59 Cross-ex (все 4) | +0.5-1.0% | -0.02 to -0.16% | ✗ KILLED ALL |
| **S33 BASIS_NEAR_ZERO_SHORT** | +1.34% | +0.17% | ⚠ DEGRADED -87% |
| **S17 BASIS_PERP_MOD_SHORT** | +5.00% | +0.15% | ⚠ DEGRADED -97% |
| S49 HIGH_VOL_SHORT_TINY_POS | +1.48% | +0.01% | ⚠ DEGRADED -99% |
| S34 SLIGHT_POS_FUNDING_SHORT | +0.72% | +0.00% | ⚠ DEGRADED -100% |

---

## 2) Timeline — early vs late

- Из 21 дня только **3 положительных** (31 мая, 11 июня, 19 июня)
- Best: 19 июня +$406, worst: 8 июня -$1003
- Funding contribution: +0.008 to +0.019% per trade
- Price contribution: **-0.04 to -0.17% per trade** (5-10x больше funding)

**ROOT CAUSE: PRICE killed everything.** Funding-only backtests были обманом.

---

## 3) Statistical decomposition — что найдено

### Per Hour (UTC) — 1 час дает edge:
- **Hour 1 (01:00-02:00 UTC)**: +0.032% mean, +$48 total, единственный positive из 24 hours

### Per Symbol — выявлены 2 profitable:
| Sym | n | Mean | WR | Total$ |
|-----|---|------|-----|----|
| **REUSDT** | 496 | **+0.51%** | **62%** | **+$252** ⭐ |
| **SYNUSDT** | 236 | +0.05% | 58% | +$11 |
| SAHARAUSDT | 365 | -0.07% | 61% | -$27 (almost zero) |

vs катастрофы:
| ESPORTSUSDT | 2913 | -0.41% | 53% | **-$1198** |
| HUSDT | 2934 | -0.30% | 56% | -$880 |
| HOMEUSDT | 2850 | -0.23% | 57% | -$651 |

### Per Side — SHORT bias меньше теряет:
- SHORT: 12,441 trades, -0.10% mean, total **-$1,253**
- LONG: 23,915 trades, -0.30% mean, total **-$7,081**

LONG в 6 раз хуже SHORT по total.

### Per ENTRY funding rate bucket:
Все buckets отрицательные, но:
- **mod_pos (0.1-0.5%)**: -0.08% (LEAST loss) ← least damaging
- slight_pos (0-0.1%): -0.12%
- mod_neg (-0.5 to -0.1%): -0.20%
- **very_neg (<-2%)**: **-0.55% WORST**

**Глубокий negative funding = глубокий минус. Mild positive funding = меньше всего теряет.**

---

## 4) Failure mode

| Exit reason | n | mean PnL | WR |
|-------------|---|----------|----|
| target_hit | 20,218 | +2.16% | 100% |
| stop_loss | 16,047 | -3.24% | 0% |
| time_backstop | 85 | +0.89% | 22% |

**Asymmetric losses:** stop -3.24% vs target +2.16%. Even at 56% target_hit rate:
- EV = 0.56 × 2.16 - 0.44 × 3.24 = **-0.22% per trade** before fees

Order book features at entry:
- Spread: losing=5.11bp vs winning=4.58bp (small diff, not actionable)
- Imbalance_5: losing=+0.002 vs winning=+0.006 (noise)

**OB не дала predictive signal.**

---

## 5) NEW edges (visible только in live)

Phase 5 statistical analysis выявил один edge которого не было в backtest:

### NEW EDGE: REUSDT trading (любой side)
- 496 trades, +0.51% mean, WR 62%, Total +$252
- НЕ symbol-specific filter в backtest
- Возможно: специфика RE token в этот период (regime artifact или real edge — нужно больше данных)

---

## 6) TG validation (18,073 messages за 3 нед)

**TG listener захватил ДРУГИЕ channels** чем ожидалось:
- "Капитанская каюта": 16,270 msg (NEW main source)
- "memecrypted_chat": 1,451
- Старые funding-arb channels (ua_cryptoinvest, twix1444, lopata_arb): практически 0

**Listener изменился — собирает другой content.** TG cross-validation с paper trades невозможна (channels не funding-arb).

---

## 7) REAL MONEY RECOMMENDATION

### ❌ НЕ ДЕПЛОИТЬ real money

Причины:
1. **Лучшие positive** имеют Sharpe 0.04-0.08 (random noise)
2. **Min trade** для positive strategies: -4 to -11.5% (большие просадки на одной сделке)
3. **Funding edge оказался слабым** против slippage 15bp
4. **TG channels** не дают сигналов больше

### Альтернативы для дальнейшего исследования

1. **REUSDT-specific exploration** — почему этот coin profitable? Sym-specific regime
2. **SHORT-only bias** — все LONG стратегии теряли в 6x больше. Можно тестировать только SHORT setups
3. **Mild positive funding bias** — рейт 0.1-0.5% даёт минимальные losses (-0.08%). Возможно с лучшим entry filter дойдёт до positive
4. **Cross-exchange BASIS (perp-perp hedge)** — не было реализовано (требует 2 ноги на разных биржах). Может быть единственный реальный edge

### Что делать сейчас

1. **Остановить все 60 paper bots** (они только жгут API limits)
2. Сделать **детальный исследовательский цикл** на REUSDT и SHORT setups
3. **Подумать о hedged perp-perp** стратегиях (binance + bybit одновременно)
4. **НЕ запускать real money** до validated edge на минимум 4 недели в живую

---

## ARTIFACTS на VPS

- `/srv/bots/funding-rate/paper_v8/SXX/trades.jsonl` — все 36K live trades
- `/srv/bots/cluster/memory/funding-rate/POST_VACATION_PLAYBOOK.md` — этот файл
- `/srv/bots/cluster/memory/funding-rate/persistent_analysis/` — все historical analysis
- `/var/backups/funding_paper/snapshot_*.tar.gz` — 21 daily snapshot

---

## ITOGOVO ОЦЕНКА

**Funding arbitrage edge через unhedged perp = НЕ РАБОТАЕТ в live conditions.**

Все 60 backtest-claimed стратегий failed live validation. Funding contribution слишком мал (+1-2bp) против price volatility (-4 to -17bp). Slippage 15bp на trade убивает остатки edge.

**Истинный funding edge возможен только в hedged variants:**
- spot-perp basis (требует real spot short с borrow — невозможно для memes)
- perp-perp cross-exchange basis (требует execution на 2 биржах одновременно)

Эти варианты НЕ были протестированы в paper_v8.

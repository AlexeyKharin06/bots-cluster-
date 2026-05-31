# 📋 ИНСТРУКЦИЯ для Claude после возвращения с отпуска (3 недели)

**Скопируй текст ниже в новую Claude сессию — всё что нужно для глубокого анализа.**

---

## ЗАДАЧА

Провести **полный декомпозиционный анализ объединив 3 недели live paper-trading + 6 месяцев исторических backtests + все накопленные результаты ранее**. Найти топ стратегии для real-money + новые edges. Не сокращать. 3 недели мало само по себе — нужна комбинация с history для статистической мощности.

## SSH доступ
```bash
ssh -i /d/.ssh/id_rsa root@187.127.87.202
```

## ВСЕ ДАННЫЕ сохранены (НЕ потеряются)

### LIVE (3 недели paper trading)
```bash
/srv/bots/funding-rate/paper_v8/SXX_NAME/trades.jsonl   # 60+ файлов
/srv/bots/funding-rate/paper_v8/SXX_NAME/bot.log
/srv/bots/.shared/tg/signals_master.jsonl                # все TG за 3 нед
/srv/bots/.shared/tg/feed_*.jsonl
/srv/bots/.shared/tg/media_tmp/                          # фото/скриншоты
```

### HISTORICAL (всё сохранено в persistent location)
```bash
/srv/bots/cluster/memory/funding-rate/persistent_analysis/parquets/   # 50+ parquets (118MB)
/srv/bots/cluster/memory/funding-rate/persistent_analysis/scripts/    # 80+ analysis scripts
/srv/bots/cluster/memory/funding-rate/persistent_analysis/logs/       # все логи фаз
/srv/bots/cluster/memory/funding-rate/*.md                            # 45+ memo с findings
```

**Ключевые parquets:**
- `multi_ex_funding_EXPANDED.parquet` (2.15M ticks × 9 бирж × 6 мес)
- `perp_klines_binance.parquet` (perp prices)
- `perp_klines_bybit.parquet`
- `spot_binance.parquet`
- `phaseQ_decomp.parquet` (50K rows с full features)
- `phaseT_chkpt_C.parquet` (19K survivors heavy grid с price-aware PnL)
- `phaseM_combined.parquet` (combined exit tests)
- `phaseG_iteration.parquet` (46 iterated strategies)
- `H_BORROW_SQUEEZE_validated.parquet`
- `tg_extracted_signals.parquet` (84 TG signals validated)
- `c2_wide.parquet` (cross-ex wide format funding)
- 30+ других analysis parquets

## КЛЮЧЕВЫЕ memo с findings (читай ПЕРВЫМИ)

```bash
cat /srv/bots/cluster/memory/funding-rate/FINAL_HONEST_PLAYBOOK.md
cat /srv/bots/cluster/memory/funding-rate/TRADER_PLAYBOOK_FINAL.md
cat /srv/bots/cluster/memory/funding-rate/MEGA_GRID_INVERSION_2026_05_26.md
cat /srv/bots/cluster/memory/funding-rate/H_COMBO_3c_DEPLOY_SPEC.md
cat /srv/bots/cluster/memory/funding-rate/OVERNIGHT_RESULTS_FINAL.md
cat /srv/bots/cluster/memory/funding-rate/FINAL_CONSOLIDATED.md
cat /srv/bots/cluster/memory/funding-rate/VACATION_HANDOFF.md
```

## ОБЯЗАТЕЛЬНЫЕ принципы

1. **PRICE в PnL ВСЕГДА** для unhedged perp (не funding-only)
2. **Combined exit** (price OR funding OR sign-flip OR time)
3. **Per-exchange normalization** (rate / cap_max)
4. **Realistic costs** 15bp (10bp fee + 5bp slip)
5. **Walk-forward** по неделям + по месяцам
6. **Объединять live + history** где регим близок
7. **Перечислить gaps** в конце что НЕ покрыто

## ЭТАПЫ АНАЛИЗА

### Phase 1: LIVE per-strategy summary (3-4 ч)
- 60+ файлов trades.jsonl
- Per strategy: n, mean, median, WR, Sharpe, worst, best, daily PnL series
- Walk-forward по неделям (3 chunks × 1 неделя)
- Identify failing strategies (mean<0 OR WR<50%)

### Phase 2: HISTORY-vs-LIVE cross-validation (3 ч)
Для каждой из 60 стратегий — таблица:
| Strategy | Hist (backtest) mean/WR | Live mean/WR (3 wk) | Degradation% | Verdict |

Что подтвердилось / провалилось / новое.

### Phase 3: COMBINED dataset re-mining (5-6 ч)
- Объединить history + live trades + TG signals
- Run NEW heavy grid (5-10M combos) на объединённом:
  - 6 axes: funding × price × basis × borrow × cross-ex × BTC regime
  - Per-feature × thresholds × hedge variants × exit rules
  - Targeting n>=50, WR>=60%, mean>0.5%, Sharpe>=0.5
- Find edges visible ONLY in combined view

### Phase 4: Статистические блоки decomposition (2-3 ч)
Для каждой validated стратегии:
- Time blocks: Nov-Feb, Mar-May, live wk1, wk2, wk3
- BTC regime: BULL/BEAR/RANGE
- Vol regime: LOW/MID/HIGH
- Session: ASIA/EURO/US
- Cohort: MAJOR/MID/NICHE

Find: стабильная стратегия vs специфичная для регима.

### Phase 5: Failure mode iteration (2-3 ч)
Для каждой losing live стратегии:
- Что общего в LOSING trades?
- Добавить фильтр → re-test → улучшилось?
- Iterate 3-5 раз

### Phase 6: TG validation update (1-2 ч)
- 3 нед новых TG сигналов через price+funding forward returns
- Какие каналы предсказательны?
- Match TG-mentioned coins с paper bot trades

### Phase 7: NEW edges discovery (2 ч)
Найти паттерны которых не было в history:
- Новые listing coins
- Изменение характера funding на конкретных биржах
- Aster/Lighter behaviour changes
- Per-symbol regime shifts

### Phase 8: ФИНАЛЬНЫЙ playbook (1 ч)
ОДИН файл `/srv/bots/cluster/memory/funding-rate/POST_VACATION_PLAYBOOK.md`:

```markdown
# POST-VACATION PLAYBOOK

## TL;DR
- Total data combined: ~Z events
- Top-3 deploy-ready (after live validation)
- Strategies KILLED in live: list
- NEW edges found in combined: list

## Cross-validation 60 strategies (hist vs live)
[full table]

## Top-10 after combined validation
[detailed specs each]

## NEW edges combined view
[list with metrics]

## Statistical blocks analysis
[per-regime tables]

## Failure mode fixes
[before/after iterations]

## TG validation update
[per channel after 3 weeks]

## REAL MONEY recommendation
- $1k → strategy X with $Y size = expected $Z/мо
- Worst-case drawdown scenario
```

## ВРЕМЕННЫЕ ЗАТРАТЫ
- Phases 1-2: 7 ч
- Phase 3 heavy grid: 5-6 ч
- Phases 4-5: 5-6 ч
- Phases 6-7: 3-4 ч
- Phase 8 report: 1 ч
- **Total: 20-24 ч компьютерного времени** (параллелить)

## ВАЖНЫЕ caveats

- **3 недели live мало для одной стратегии** — n=50-200 trades / стратегия. Combine с history где регим близок.
- **Live ≠ Backtest** — degradation 30-50% norm из-за slippage/execution
- **Регим мог смениться** — проверить BTC trend сравнить с history
- **Не объединять blindly** — если live в drastically other regime, не путать с history
- **Не запускать real money** без подтверждения после анализа

---

**Это всё. Скопируй в новую сессию через 3 недели, она поймёт и сделает.**

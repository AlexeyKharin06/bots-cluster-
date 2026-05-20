# PROJECT_CONTEXT — funding-rate

> Этот файл — корневой контекст для AI brain (читается каждый цикл).
> Тут описано КУДА мы идём, КАК мерим прогресс, ЧТО запрещено.

## Цель проекта

**Найти стратегию заработка на funding-rate-арбитраже** с минимальным риском и стабильным доходом. После N циклов выдать пользователю чёткий ответ: «вот стратегия X, APR Y%, max DD Z%, готова к live deploy с риском не больше W%».

## Что уже было сделано (history before migration)

Локальное окружение (Windows D:\funding_rate, теперь мигрировано):
- 16+ paper-ботов работали 24/7
- Сделано 8 параллельных backtest-агентов
- 206,520 симулированных трейдов
- 152 live paper trades
- 571 OCR'd скриншот
- 3,000+ TG сообщений из 60 каналов

## Что мы УЖЕ ЗНАЕМ — confirmed negative findings (НЕ повторять!)

| Стратегия | Результат | Источник |
|---|---|---|
| **Interval prediction** | 2.17% live precision (не 96%, был survivorship bias) | `READY_OR_NOT.md` |
| **Fair-price scalping** | 0/5 weeks profitable в walk-forward, mean −$0.89/trade на 206k симах | `WALKFORWARD_REPORT.md` |
| **Listing momentum** | 32% win, −$11.28/90d, lottery-shaped | `LISTING_MOMENTUM_REPORT.md` |
| **Practitioner microcaps expansion** | DEGRADES baseline mean на 86% | `expansion_backtest_results.xlsx` |
| **Multi-ex spread arb** | −$13,473 на 30,902 трейдах | `v2_combined_backtest.xlsx` |
| **Naive funding harvest** | −$304 на 315 трейдах | `funding_harvest_backtest.xlsx` |
| **Multi-signal confluence (LONG)** | 27% win, −$0.85/trade | `confluence_backtest.xlsx` |

## Что ВАЛИДИРОВАНО как сигнал (но не доказан edge)

- **Premium streak ≥0.5%×3h** — recall 95% на known events, precision 2-9% unconditional
- **OI 24h growth ≥30%** — confirms volatility, NOT predicts events
- **Borrow rate spike +50% 24h** — x10 lift в bookmarked-events
- **Pre-event warning** — orthogonal +$0.63/trade в 200-event backtest

## Untested гипотезы — возможные edge'ы (приоритет в порядке)

1. **Whale wallet copy-trade** (@on_chain_radar 5/18 high-PnL claims)
2. **Multi-signal confluence SHORT-only** (n=5: 80% win — мало, но направление)
3. **Stablecoin depeg arb** (Лопата USDD $2300 precedent)
4. **CEX→DEX algo flow tracking** (Lopata "dex-dex" class)
5. **Exchange announcement watch** (95% precision до event)
6. **New symbol detection** (полл API every 30s — мы первые на листинге)

## Структура memory

```
memory/funding-rate/
  PROJECT_CONTEXT.md        ← этот файл (стабильный)
  SESSION_HANDOFF.md        ← резюме последней сессии
  BRIEF.md                  ← snapshot "где мы сейчас" (≤4KB, перезаписывается каждый цикл)
  HISTORY.md                ← timeline append-only, 1 строка/цикл
  backlog.md                ← гипотезы, статусы testing/accepted/rejected
  promotion.json            ← state ботов и live stats
  insights/cycle_*.md       ← полный unconstrained лог каждого цикла
```

## KPI / readiness gate (ready for real money)

Все 4 одновременно:
1. **Walk-forward** на минимум 90 дней показывает **mean +$X >0** на n≥50 trades
2. **Win rate** ≥75% rolling 14d
3. **Max drawdown** ≤15% (rolling 30d)
4. **At least 3 independent edges** (диверсификация — не одна стратегия = один edge)

## Что строго запрещено

- ❌ Торговать реальными деньгами без явного approval пользователя
- ❌ Изменять risk caps (Kelly fraction, MAX_SINGLE_PCT) без логирования в HISTORY
- ❌ Коммитить секреты (.tg_credentials, .cex_keys, *.session) в git
- ❌ Удалять старые insights/cycle_*.md — append-only
- ❌ Запускать AI brain цикл вне cron окна без причины (rate-limit Claude API)
- ❌ Доверять backtest'у без walk-forward валидации (survivorship bias)
- ❌ Доверять live результату с n<100 (мала выборка)

## Что делать в каждом цикле AI brain

1. Прочитать `BRIEF.md` (где мы сейчас)
2. Прочитать `HISTORY.md` последние 100 строк (таймлайн)
3. Прочитать последние 3 `insights/cycle_*.md` полностью
4. Проверить статус 14 paper-ботов через `python3 ...`
5. Проанализировать новые closed trades за последние 6h
6. Проанализировать новые TG сообщения из 60 каналов
7. Сгенерировать гипотезы или дотестить старые
8. Запустить нужный backtest скрипт
9. Применить валидированные улучшения (params, blacklists)
10. Обновить `BRIEF.md`, добавить запись в `HISTORY.md`
11. Записать полный лог в `insights/cycle_$(date -u +%Y%m%d_%H%M).md`
12. Если KPI пройдены → пометить `data/ready_for_real.flag`

## Cron schedule

```
0 5,11,17,23 * * *  — AI brain cycle (4 раза в день UTC, offset от listing-arb/cex-onchain/onchain)
*/5 * * * *         — git pull origin main (синк кода с GitHub)
```

## Инфраструктура

| Что | Где |
|---|---|
| Код | `/srv/bots/funding-rate/code/` |
| Data | `/srv/bots/funding-rate/code/data/` (server-only, не в git) |
| Логи | `/srv/bots/.shared/logs/cron_funding-rate.log` |
| Секреты | `/srv/bots/secrets/funding-rate/` (.tg_credentials) |
| Memory | `/srv/bots/cluster/memory/funding-rate/` (в git репо cluster) |
| GitHub код | https://github.com/AlexeyKharin06/funding-rate (private) |
| GitHub cluster (memory) | https://github.com/AlexeyKharin06/bots-cluster- |
| VPS | root@187.127.87.202 |
| Cluster shared scripts | `/srv/bots/cluster/shared/autonomous_cycle.sh` |
| AI brain wrapper | `/home/bots/run_cycle_funding-rate.sh` |

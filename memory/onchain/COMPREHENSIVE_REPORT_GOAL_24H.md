# GOAL — Comprehensive 24h Strategy Report

> Пользователь explicit потребовал (2026-05-24 19:30 UTC): через сутки представить полный отчёт.
> Deadline: **2026-05-25 19:30 UTC**.

## Что AI brain ОБЯЗАН подготовить за 24h (cumulative across cron cycles)

Каждый из 4 следующих cron циклов (0/6/12/18 UTC) должен накапливать к финальному отчёту в `memory/onchain/insights/REPORT_20260525.md`.

### Раздел 1 — Все стратегии (старые + новые)

Для каждой из 18+ control streams (SNIPER_A/B/D/D2-5/E/E2-5/F/F2-5/G/H/H2, GOLD/GOLD2/3/4/5, WHALE, LATE, LOWCAP, BSC_FILTERED) + paper-streams + кандидатов:
```
Name | n | avgPnL | medianPnL | WR% | big% | huge% | rug% | avgFee | maxDD | Sharpe
```

### Раздел 2 — Новые гипотезы и регулярности

Список **всех** проверенных гипотез (включая отвергнутые) с walk-forward stats:
- TRAIN n/big%/rug%
- TEST n/big%/rug%
- Δ TRAIN→TEST (показывает overfit)
- causal explanation (почему работает)
- phase (Phase 1-5 — Accumulation/Smart-money/Hype/Top/Decay)

### Раздел 3 — На наших данных результаты

Считать на 4957+ closed_trades (или больше после backfill):
- **Total PnL%**: cumulative if held all
- **Avg pump** ($1 size): ?$
- **Max pump** (best single trade): ?$
- **Rug count + total loss**: ?
- **Среди bigs какие dimensions СОВПАДАЮТ** — это и есть ключ
- **Среди rugs какие dimensions ОБЩИЕ** — это веточный фильтр

### Раздел 4 — Что мы могли бы взять с optimal фильтрами

Симуляция: если бы вошли только в трейды passing **SMART_5** (validated), **WALLET_LEADERBOARD**, **PORTUGAL strict**, **H_V7_ANTICLUSTER**, **H_WALLET_TOP1_LEADERBOARD** — какой был бы:
- n trades
- Total PnL%
- Compound: $1 → $?
- Max drawdown
- Time to first big

### Раздел 5 — Phase-classification всех 18+ исторических bigs

Для каждого known big ($MC +1268, $WORLDCUP +971, $GITBANK +941, $PEDUCK +908, $COMPUTE +856, $TLS, $FOID, $CATCOIN, Poor3 +943, Stake +481, BELIEF +235, RICH +847, MTFR ×2):
- В какой фазе вошли (Phase 1-5)?
- Что НЕ delyali нас войти раньше (Phase 1-2)?
- Common dimension across all 18: какие 1-3 features?
- Если бы у нас был **тогда** SMART_MONEY_5 filter + WALLET_LEADERBOARD — поймали бы?

### Раздел 6 — Compound strategies

Каждый цикл — хотя бы 1 **compound** experiment:
- `SMART_5 ∩ WALLET_LEADERBOARD top1 ∈ {48 wallets}` → n упадёт, precision вырастет
- `SMART_5 ∩ no_blacklist creator` → reject если creator ∈ 5 blacklist
- `PORTUGAL ∩ smart>=3 ∩ wallet_leaderboard` — triple-confirmation

Goal: компаунд который даёт **TEST big>=70% rug<=5%**.

### Раздел 7 — Distance to deploy

Для каждой validated стратегии:
- n до deploy gate (≥50 paper trades)
- ожидаемое time-to-50 (исходя из rate of fires)
- предполагаемый avgPnL после fees
- compound projection: $1 → $? за 50 trades

### Раздел 8 — Open questions to user

Список нерешённых вопросов где AI не может сам принять решение:
- HUPHey identity (whale/bot/insider)?
- Real-money switch threshold (n=50 ли достаточно?)
- New chains scope (Base/Polygon disabled — confirm?)
- Helius budget для new data fetching

## Reporting cadence

- Каждый из 4 cycles (0/6/12/18 UTC до завтра 19:30 UTC) — append к REPORT_20260525.md
- В последнем (18:00 UTC) — финализировать **EXECUTIVE SUMMARY** в top:
  - Headline: что найдено за сутки
  - Распределение PnL по стратегиям
  - Top 5 actionable next steps

## Что НЕ забывать в работе

1. **Pipeline running**: backfill_pipeline.sh каждые 12h обновляет:
   - tokens_unified.json (new tokens added)
   - wallet_roles per token (top20/top21_40 filled)
   - lp_provider/pool_creator filled
   - smart_wallets.json rebuilt
2. **Holistic 11 dimensions** — НЕ ограничиваться wallet alpha. Технические, holders, TG, liquidity, regime, phase ВСЕ.
3. **READ FIRST**: `HOLISTIC_STRATEGY_MANDATE.md` + `TG_DEEP_DIVE_MANDATE.md` + `CRITICAL_FINDINGS.md` каждый цикл.
4. **Self-diagnostic**: healthcheck FIRST. Если что сломано — починить или escalate.
5. **No blind follow**: каждая TG-based гипотеза — обоснована causally.

## Метрика успеха REPORT

К 2026-05-25 19:30 UTC user должен увидеть в TG bot и git:
- ✅ Все 18+ стратегий со stats
- ✅ Список НОВЫХ найденных гипотез ≥5
- ✅ Compound filter с TEST big>=50% rug<=10%
- ✅ Phase-classification всех 18 historical bigs
- ✅ Симуляция "если бы фильтровали" — конкретные $ цифры
- ✅ At least 1 ready-for-paper stream с n>=30

Если что-то не достигнуто — explain why в нужном разделе.

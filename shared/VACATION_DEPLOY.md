# 🏖️ Vacation Deploy — 3 недели автономной работы

## Цель
Бот работает сам, собирает максимум данных, экономит Helius credits, по возвращении — оценка каждой стратегии отдельно.

## Что я подготовил

| Файл | Назначение |
|---|---|
| `D:\OnChain\scripts\wallet_v2\helius_optimizer.js` | Cascaded check, adaptive TTL, budget tracker, recheck queue |
| `D:\OnChain\scripts\wallet_v2\serial_sniper.js` | Интегрирован optimizer (light_log + skip_decision) |
| `D:\OnChain\deploy\shared\per_stream_report.py` | Отчёт live vs backtest для каждой стратегии (по приезду) |
| `D:\OnChain\deploy\shared\auto_health.sh` | Cron каждые 6h — алерты в TG если что-то ломается |
| `D:\OnChain\deploy\shared\auto_learn.py` | Уже готов — переобучает модель раз в сутки |

## Что нужно сделать ПЕРЕД отъездом

### 1. Pull данные с VPS (snapshot before changes)
```bash
cd /d/OnChain
bash pull_data.sh
```

### 2. Запушить новые файлы на VPS
```bash
# Из локальной D:/OnChain — на VPS /srv/bots/onchain/code
scp scripts/wallet_v2/helius_optimizer.js root@187.127.87.202:/srv/bots/onchain/code/scripts/wallet_v2/
scp scripts/wallet_v2/serial_sniper.js root@187.127.87.202:/srv/bots/onchain/code/scripts/wallet_v2/
scp deploy/shared/per_stream_report.py root@187.127.87.202:/srv/bots/onchain/code/deploy/shared/
scp deploy/shared/auto_health.sh root@187.127.87.202:/srv/bots/onchain/code/deploy/shared/
scp deploy/shared/auto_learn.py root@187.127.87.202:/srv/bots/onchain/code/deploy/shared/
```

### 3. На VPS: дать права + установить cron
```bash
ssh root@187.127.87.202

cd /srv/bots/onchain/code
chmod +x deploy/shared/auto_health.sh

# Установить cron — каждые 6 часов health check + раз в день auto_learn
crontab -e

# Добавить:
0 */6 * * * /srv/bots/onchain/code/deploy/shared/auto_health.sh
0 3 * * * cd /srv/bots/onchain/code && python3 deploy/shared/auto_learn.py >> deploy/shared/auto_learn.log 2>&1

# ОТКЛЮЧИТЬ Claude session cron! (если есть)
# Найди строку с claude в crontab и закомментируй #
```

### 4. На VPS: restart sniper с новым optimizer
```bash
cd /srv/bots/onchain/code

# Остановить старый
ps -ef | grep -E "node.*(serial_sniper|lp_monitor|lp_bot)|watchdog\.sh" | grep -v grep | awk '{print $2}' | xargs kill -9

# Запустить новый
nohup bash scripts/wallet_v2/watchdog.sh >> scripts/wallet_v2/watchdog.log 2>&1 &

# Проверить через 30s
sleep 30
ps -ef | grep -E "node.*serial_sniper" | grep -v grep
tail -30 scripts/wallet_v2/sniper.log
```

### 5. Проверить что optimizer загрузился
В логах должно быть:
```
[HELIUS_OPT] loaded N smart, M ruggers, K serial_pump, L rugbots
[HELIUS_OPT] total: ... wallets
[ML_SCORER] loaded ... rugger wallets
```

### 6. Понизить Claude tariff
- Зайди в anthropic.com/settings/billing
- Понизь plan
- Сэкономишь $$$ за 3 недели

## ПО ВОЗВРАЩЕНИИ

### 1. Pull свежие данные
```bash
cd /d/OnChain
bash pull_data.sh
```

### 2. Запустить отчёт по стратегиям
```bash
python deploy/shared/per_stream_report.py
```

Выдаст таблицу:
- **KEEP**: стратегии которые работают (live PnL ≥ backtest)
- **SUSPECT**: мало данных или борderline (нужно ещё)
- **DROP**: убыточные на live, выключить
- **UNKNOWN**: новые streams без baseline

### 3. Решения
- KEEP стратегии → можно size up в live ($50-100)
- DROP стратегии → удалить из `serial_sniper.js` paperChecks
- Повысить Claude tariff обратно

## Что собирается всё время

✅ **closed_trades** в `sniper_state.json` — каждый трейд каждой стратегии с реальным PnL
✅ **light_token_log.jsonl** — даже skipped токены (DexScreener-only data)
✅ **wallet_classifications** — wallet_db_solana.json пополняется
✅ **chart_classifications** — token_charts_cache.json обновляется
✅ **rugger_blacklist** — обновляется при каждом rug
✅ **TG signals** — signals_pool.json (tg_listener)
✅ **Pump.fun feed** — pump_fun_signals.json
✅ **DexScreener signals** — dexscreener_signals.json
✅ **Pool snapshots** — pool_snapshots.json
✅ **Wallet history db** — для классификации pump/rug счетов

## Helius экономия — как работает

**Cascaded check** перед каждым checkHolders:
- `liq < $500` → SKIP (dead pool)
- `mcap < $1K` → SKIP (junk)
- `vol < 100 & age > 24h` → SKIP (dead)
- `sells > buys*3` → SKIP (dying)
- Default → выбор уровня (top10 / top40 / deep)

**Adaptive TTL cache**:
- Hot (vol > $100K): 5 min
- Mid (vol > $10K): 30 min
- Quiet (vol > $1K): 4 hr
- Dead: 24 hr

**Budget tracker**:
- Если жжем >80% бюджета/час → throttle (top10 only)
- Если >100% → cache-only mode
- НИКОГДА не выходит за дневной бюджет

**Recheck queue**:
- Throttled токены НЕ теряются — попадают в очередь
- Когда бюджет восстановится — берем из очереди для full check

## Прогноз

| Без opt | С opt |
|---|---|
| 7 дней до exhaustion | **30+ дней** ✓ |
| 100% информативность | **~95%** (теряем мусор) |
| Качественные данные | **Качественные данные ✓** |

## Что НЕ потеряется в данных

- DexScreener metrics (bsr, vol, liq, mcap) — light_log пишется для ВСЕХ токенов
- Token classification — chart_class и wallet_class обновляются автоматически
- Pool snapshots — собирается каждые 5 мин из DexScreener (free)
- TG signals — tg_listener работает независимо
- Wallet classifications — auto pop в wallet_db_solana

## Структура streams работающих 3 недели

Все из master table уже в `serial_sniper.js`:
- **13 paper streams** (Wave 6/7/8) — собирают live статистику
- **8 live streams** (GOLD3/WHALE/LATE/LOWCAP/etc) — реальные деньги
- **Wave 1-5** легаси — продолжают работу

После 3 недель → per_stream_report.py покажет какие из 50+ streams реально работают на живых данных.

## Финальный чек-лист перед отъездом

- [ ] Pull data with `bash pull_data.sh`
- [ ] Push 5 файлов на VPS (см. шаг 2)
- [ ] Set cron на VPS (auto_health.sh + auto_learn.py)
- [ ] ОТКЛЮЧИТЬ старый Claude session cron
- [ ] Restart watchdog/sniper с новым кодом
- [ ] Проверить логи через 30 мин — нет ошибок, optimizer работает
- [ ] Telegram alerts работают (тестовое сообщение)
- [ ] Понизить Claude tariff
- [ ] Recommend bankroll: $1500-3000 на 3 недели (50-100 трейдов размером $30-100)
- [ ] **Enjoy vacation 🏖️**

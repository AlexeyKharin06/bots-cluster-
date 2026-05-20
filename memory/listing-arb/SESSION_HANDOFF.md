# Session handoff — Listing Arb (2026-05-19)

> Этот файл — полный контекст для **следующей Claude-сессии**. Читать первым.
> Также продублирован на сервере: `/srv/bots/cluster/memory/listing-arb/SESSION_HANDOFF.md`

## Состояние "одной фразой"

Listing-arb мигрирован с локального Windows (D:\Listing Arb) на **Hostinger VPS** `187.127.87.202`. **22-26 ботов** работают там 24/7. **Win rate 82%**, **mean PnL +311%** на 29 paper trades. **Readiness 8/9** — нужно 1 свежий трейд до READY. AI brain цикл крутится через cron каждые 6 часов.

## Инфраструктура

| Что | Где |
|---|---|
| VPS | Hostinger, root@187.127.87.202 |
| Код | `/srv/bots/listing-arb/code/` (на сервере) |
| Локальный код | `D:\Listing Arb\` (исходник, мигрирован) |
| Секреты | `/srv/bots/secrets/listing-arb/.cex_keys` + `.tg_credentials` |
| Telegram session | `/srv/bots/listing-arb/code/scripts/tg_session.session` |
| GitHub репо кластера | https://github.com/AlexeyKharin06/bots-cluster- |
| Cron schedule | `0 2,8,14,20 * * *` UTC (4 цикла/сутки) |
| AI brain | `/srv/bots/cluster/shared/autonomous_cycle.sh` |
| Wrapper | `/home/bots/run_cycle_listing-arb.sh` |
| Cluster memory | `/srv/bots/cluster/memory/listing-arb/` |
| Логи | `/srv/bots/.shared/logs/cron_listing-arb.log` |

## Креденшалы (у пользователя — НЕ в этом файле)

- VPS root pass — в директиве (у пользователя)
- GitHub PAT — там же
- TG bot token, TG chat id — там же
- TG 2FA cloud password: `19960606`

## Что система делает (5 типов стратегий)

1. **Pre-listing pump** — за 30 мин до листинга по @mrcaptainspread сигналам, DEX→CEX лесенка
2. **Cross-CEX arb** — buy дёшево, sell дорого, через withdraw/deposit
3. **Spot-Perp basis** (Kodak) — long spot + short perp = lock funding
4. **Funding rate arb** — extreme funding на новых перпах
5. **Tokenized stocks** — Binance perp WMT/JPM/BRKB vs NYSE

Плюс **delisting forewarning** (избегание потерь).

## Empirical findings (validated, не overfit)

- **bitget** 92% win, mean **+474%** (n=12) — главная биржа стратегии
- **kucoin** 85% win, mean +210% (n=13)
- **hour 12 UTC** (15:00 МСК) 86% win, +242% (n=7)
- **hour 10 UTC** (13:00 МСК) 80% win, +268% (n=5)
- **tg_boost 16-30** (одно tier-A упоминание) 88% win, +337%
- **22 auto-discovered hypotheses validated** out-of-sample
- Honest walk-forward test: **67% win, +269% PnL** (n=9 на test set, без look-ahead)
- Capital growth Monte Carlo: $1k → $15.5k за 90 дней (15x, ruin prob 0%)

## Главные модули (26 .py файлов в scripts/)

| Категория | Модули |
|---|---|
| **Сбор сигналов** | live_listing_monitor, announcement_parser, tg_channel_watcher (61 канал), tg_signal_ingest |
| **Стратегии** | pre_listing_scheduler, cross_cex_arb, spot_perp_basis, funding_rate_arb, tokenized_stocks_arb, delisting_arb |
| **Исполнение (paper)** | position_tracker, paper_trader, paper_trader_unified |
| **Обучение** | strategy_learner, walk_forward_validator, hypothesis_generator, slippage_model |
| **Гейты** | risk_manager, readiness_gate, market_phase, multi_asset_regime |
| **Дополнительно** | daily_digest, channel_discoverer, self_diagnostic, onchain_alpha, capital_simulator |

## Что НЕ работало автономно и было исправлено

1. **DEX-staleness false positives**: 8/9 ранних алертов были fantom-spread → добавил gate vol_24h<10k OR txn_h1=0 → отрезает
2. **Bitget API не отдаёт pre-market**: лечится LOOKBACK_NEW_DAYS=7 (видим listings до 7 дней назад)
3. **OnChain wallet alpha**: подключён к `D:/OnChain/scripts/wallet_v2/signals_pool.json` (240 токенов отслеживаются)
4. **TG channel discoverer**: нашёл 7 кандидатов (@bwenews +18 listing keywords, @lopata, @whalearut)
5. **Self-diagnostic**: автоматически поймал и зафиксил `@easyfart` deleted, исправил wmic→PowerShell CIM detection

## Незакрытые задачи (для следующего AI brain цикла)

1. ❌ **TG session на сервере не валидна** — pending: `bash /tmp/fix_tg.sh` пересоздаёт credentials с api_id=2040 (TG Desktop). Если после fix_tg.sh `AUTH: False` — нужен SMS.
2. ⏳ **Live trade #30** — для прохождения readiness 9/9. Подвозится сам когда листинг случится в magic hour и tg_signal боустит score.
3. ⏳ **Авто-исполнение через CCXT** — не активировано. Сигналы выдаются, ордера ставит вручную пользователь. Активировать только по явному "да".

## Как новый Claude должен начать (если открыта свежая сессия)

```bash
# 1. Прочитать этот файл (D:\Listing Arb\SESSION_HANDOFF.md)
# 2. SSH (если есть permission в settings.json) или попросить пользователя
ssh root@187.127.87.202 "cat /srv/bots/cluster/memory/listing-arb/SESSION_HANDOFF.md"
# 3. Проверить статус
ssh root@187.127.87.202 "tail -50 /srv/bots/.shared/logs/cron_listing-arb.log"
ssh root@187.127.87.202 "ls -la /srv/bots/cluster/memory/listing-arb/cycle_*.md | tail -5"
# 4. Прочитать последний BRIEF.md
ssh root@187.127.87.202 "cat /srv/bots/cluster/memory/listing-arb/$(ls -t /srv/bots/cluster/memory/listing-arb/cycle_*.md | head -1)"
```

## Команды для пользователя (в новой сессии)

- **"Статус listing-arb"** → я тяну логи и метрики, рапортую
- **"Запусти AI brain сейчас"** → `sudo -u bots /home/bots/run_cycle_listing-arb.sh`
- **"Что в paper_trades?"** → `wc -l /srv/bots/listing-arb/code/data/paper_trades.jsonl`
- **"Включай реальные деньги"** → ⚠️ требует verbal/explicit go-ahead, активирую CCXT executor через отдельную задачу

## Запреты

- ❌ НЕ торговать реальными деньгами без явного approval пользователя
- ❌ НЕ коммитить секреты в git
- ❌ НЕ запускать AI brain цикл вне cron окна без причины (rate-limit Telegram + Claude API)
- ❌ НЕ менять risk caps (Kelly fraction, MAX_SINGLE_PCT) без логирования причины

---

_Last update: миграция листинг-арб на VPS 19 мая 2026._
_Если этот файл устарел (>7 дней без апдейта) — последний BRIEF в `/srv/bots/cluster/memory/listing-arb/` ближе к правде._

# Session handoff — funding-rate (2026-05-20)

> Этот файл — полный контекст для **следующей Claude-сессии**. Читать первым.
> Также продублирован на сервере: `/srv/bots/cluster/memory/funding-rate/SESSION_HANDOFF.md`

## Состояние "одной фразой"

Funding-rate проект мигрирован с Windows (`D:\funding_rate`) на **Hostinger VPS** `187.127.87.202`. Код в GitHub private repo `AlexeyKharin06/funding-rate`. AI brain цикл крутится через cron каждые 6 часов (5,11,17,23 UTC). Все известные стратегии (interval, fair-price, listing, microcaps) **убиты walk-forward валидацией** — НЕТ edge. Untested гипотезы (whale-copy, depeg, DEX-flow, announcement, new-symbol) — задача AI brain их протестить.

## Инфраструктура

| Что | Где |
|---|---|
| VPS | Hostinger, root@187.127.87.202 |
| SSH | `ssh -i /d/.ssh/id_rsa root@187.127.87.202` (ключ настроен) |
| Код на сервере | `/srv/bots/funding-rate/code/` |
| Local код | `D:\funding_rate\` (git origin = funding-rate GitHub) |
| Секреты | `/srv/bots/secrets/funding-rate/.tg_credentials` |
| TG session | `/srv/bots/funding-rate/code/tg_session.session` |
| GitHub репо проекта | https://github.com/AlexeyKharin06/funding-rate (private) |
| GitHub репо кластера | https://github.com/AlexeyKharin06/bots-cluster- |
| Cron AI brain | `0 5,11,17,23 * * *` (4 цикла/сутки UTC) |
| Cron git pull | `*/5 * * * *` (синк кода с GitHub) |
| AI brain | `/srv/bots/cluster/shared/autonomous_cycle.sh` |
| Wrapper | `/home/bots/run_cycle_funding-rate.sh` |
| Cluster memory | `/srv/bots/cluster/memory/funding-rate/` |
| Логи | `/srv/bots/.shared/logs/cron_funding-rate.log` |

## Креденшалы (у пользователя, НЕ в этом файле)

- VPS root pass — есть у пользователя
- GitHub PAT — есть у пользователя
- TG 2FA cloud password: `19960606`
- TG bot token: есть в MIGRATE_TO_VPS.md
- TG chat ID: 411831496

## Что система НЕ нашла (validated negative)

Все 8 классических funding-стратегий **убиты честной walk-forward валидацией** (2026-05-18). См. `READY_OR_NOT.md`. Главные:
- Interval prediction: 2-9% live precision (не 96%)
- Fair-price scalping: 0/5 weeks profitable в walk-forward
- Listing momentum: 32% win, −$11/90d
- Microcaps expansion: DEGRADES на 86%

## Untested гипотезы — это TODO следующих циклов

1. **Whale copy-trade** (paper bot whale_copy_paper.py запущен локально)
2. **Confluence SHORT-only** (n=5 показал 80% win, нужно расширить выборку)
3. **Stablecoin depeg** (бот не написан)
4. **CEX→DEX flow tracking** (требует DEX-indexer)
5. **Announcement watcher** (announcement_scraper.py есть, 95% precision потенциал)
6. **New symbol detection** (new_symbol_detector.py запущен локально, baseline 3504 perp)

## Главные модули в code/ (40+ .py)

| Категория | Модули |
|---|---|
| **Paper bots** | paper_bot.py, paper_bot_v3.py, paper_bot_v4.py, paper_bot_fairprice.py, paper_bot_fairprice_v3.py, listing_momentum_paper.py, whale_copy_paper.py, new_symbol_detector.py, practitioner_follower_paper.py |
| **TG monitoring** | tg_channel_watcher.py (60 каналов!), tg_pattern_monitor.py, tg_media_ocr.py, signal_aggregator.py, tg_strategy_extractor.py |
| **Backtest** | backtest_smart_3leaders.py, backtest_smart_adaptive.py, backtest_inverted*.py, mega_fairprice_backtest.py, walkforward_fairprice_analysis.py, confluence_backtest.py, expansion_backtest.py |
| **Data fetch** | multi_exchange_funding.py, fetch_funding_history.py, fetch_hyperliquid_180.py, mexc_funding_fetch.py |
| **Analytics** | strategy_evolver.py, master_report.py, downtime_missed_estimate.py |
| **Auth / Helpers** | tg_auth.py (QR+2FA), tg_auth_2step.py, announcement_scraper.py |

## Что НЕ работало автономно и было исправлено

1. **TG session AuthKeyDuplicatedError** — фикс: tg_auth.py --qr с патчем для 2FA через env var
2. **Windows hardcoded paths в .py** — фикс: sed-патч в deploy_v2.sh при unpack
3. **Cron offset collision** — фикс: 5/11/17/23 UTC (offset от listing 2/8/14/20 и cex-onchain 3/9/15/21)

## Незакрытые задачи (для следующего AI brain цикла)

1. ⏳ **TG QR scan** — запущен auth в фоне в момент миграции, нужно проверить состояние сессии:
   ```
   ssh -i /d/.ssh/id_rsa root@187.127.87.202 "cd /srv/bots/funding-rate/code && python3 -c \"from telethon.sync import TelegramClient;c=TelegramClient('tg_session',$(grep api_id .tg_credentials | cut -d= -f2),'$(grep api_hash .tg_credentials | cut -d= -f2)');c.connect();print('AUTH',c.is_user_authorized());c.disconnect()\""
   ```
2. ⏳ **Первый AI brain цикл** — `sudo -u bots /home/bots/run_cycle_funding-rate.sh` (после успешной TG auth)
3. ⏳ **Тестирование whale-copy гипотезы** — n>30 trades, проверить edge vs noise
4. ⏳ **Тестирование confluence SHORT-only** — расширить с n=5 до n=30+

## Как новый Claude должен начать (свежая сессия)

```bash
# 1. Прочитать этот файл (D:\funding_rate\SESSION_HANDOFF.md)
# 2. SSH в VPS и проверить статус
ssh -i /d/.ssh/id_rsa -o BatchMode=yes root@187.127.87.202 "tail -50 /srv/bots/.shared/logs/cron_funding-rate.log"
ssh -i /d/.ssh/id_rsa root@187.127.87.202 "ls -lat /srv/bots/cluster/memory/funding-rate/insights/ | head -5"
# 3. Прочитать последний BRIEF.md
ssh -i /d/.ssh/id_rsa root@187.127.87.202 "cat /srv/bots/cluster/memory/funding-rate/BRIEF.md"
# 4. Прочитать последний cycle insights
ssh -i /d/.ssh/id_rsa root@187.127.87.202 "cat /srv/bots/cluster/memory/funding-rate/insights/\$(ls -t /srv/bots/cluster/memory/funding-rate/insights/cycle_*.md | head -1)"
```

## Команды для пользователя (в новой сессии)

- **«Статус funding-rate»** → я тяну логи и метрики, рапортую
- **«Запусти AI brain сейчас»** → `sudo -u bots /home/bots/run_cycle_funding-rate.sh`
- **«Что в paper-trades?»** → `wc -l /srv/bots/funding-rate/code/paper*/trades.jsonl 2>/dev/null`
- **«Включай реальные деньги»** → ⚠️ требует явного approval, активирую CCXT через отдельную задачу

## Запреты

- ❌ НЕ торговать реальными деньгами без явного approval пользователя
- ❌ НЕ коммитить секреты в git (.gitignore настроен)
- ❌ НЕ запускать AI brain вне cron окна без причины (rate-limit Claude API)
- ❌ НЕ менять risk caps без логирования в HISTORY.md
- ❌ НЕ доверять backtest без walk-forward валидации

---

_Last update: миграция funding-rate на VPS 20 мая 2026._
_Если этот файл устарел (>7 дней без апдейта) — последний `insights/cycle_*.md` ближе к правде._

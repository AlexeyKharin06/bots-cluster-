# TG DEEP DIVE MANDATE — для OnChain AI brain

> **ОБЯЗАТЕЛЬНО читать каждый цикл наряду с PROJECT_CONTEXT.md и BRIEF.md.**
> Пользователь явно потребовал: TG signals = не indicator для blind следования, а **сырьё для causal анализа**.

## Главный принцип

**TG mention НЕ ЕСТЬ buy signal сам по себе.** Это **симптом** — кто-то увидел токен, написал. Наша задача — понять **что произошло до канала**, чтобы покупать **раньше** чем канал упомянул.

## 5 типов TG-channels — определи к какому относится каждый top-канал

1. **Lagging reporter** — канал упоминает токен ПОСЛЕ pump'а (например `Defiscamcheck` пишет о scam постфактум). Бесполезен для entry, полезен для exit/avoid.
2. **Real-time follower** — упоминает в момент pump'а. Может работать как **confirmation** но НЕ как leading.
3. **Insider/Alpha** — публикует ПЕРЕД pump'ом (true alpha). Эти каналы редкие и драгоценные. Признак: `signal_time < first_pump_time` consistently.
4. **Pumper / coordinated** — канал САМ запускает pump через свою аудиторию. Sustainable только если ты в их пользу early. Risky.
5. **Bot/spam** — автомат, low signal, high noise.

**Действие**: каждый канал из top-12 классифицировать через `channel_pump_predictiveness.json` + временную разницу `signal_time - pool_created_time - first_pump_time`. Если ещё не сделано — сделать.

## Что я ХОЧУ узнать (приоритетные causal questions)

1. **WHO bought first** в каждом big-winner ($MC, $WORLDCUP, $GITBANK, $PEDUCK, $COMPUTE, $TLS, $FOID, $CATCOIN, $RICH +847)?
   - 5-10 первых tx wallets — кто они? smart-money? insider? bot?
   - Лежат ли эти wallets в `wallet_history_db.json` с прошлой track record?
   - Если да — **wallet leaderboard alpha** > TG alpha (быстрее и причинно)

2. **CHANNEL CASCADE** — когда $MC взлетел, в каком ПОРЯДКЕ каналы его упомянули?
   - Первый канал что упомянул `signal_time` относительно `first_pump_time` — leading or lagging?
   - Если первый канал — `architect_sol_rekt` упомянул за 30 мин до pump'а — это **insider lead**. Подписаться чаще.
   - Если первый канал упомянул через 5 мин ПОСЛЕ pump'а — lagging, не давать вес.

3. **IMAGE CONTENT** — на каких графиках/screenshot'ах канал публикует сигналы?
   - "Volume spike chart" → канал детектит memorable on-chain activity (вторичный signal)
   - "Tweet screenshot" → канал репостит ВНЕШНИЙ signal (Twitter influencer)
   - "DEX screenshot of holders" → канал делает оn-chain analysis (мы можем дублировать)
   - **Если канал использует Twitter screenshots → искать Twitter accounts отдельно**

4. **PRE-CHANNEL alpha** — что НАБЛЮДАЕМО до того как канал написал?
   - Liquidity ramp up? Holder distribution shift? Smart wallet entry? Bonding curve progress?
   - **Если AI нашёл feature X которая всегда коррелирует с channel mention внутри N минут после X — это leading indicator. Используй X, игнорируй канал.**

5. **CHANNEL OVERLAP audience** — если 3+ канала упомянули один токен в течение 30 мин, это:
   - (a) Coordinated push (плохо — pump-and-dump)
   - (b) Все увидели один upstream event (хорошо — confirm upstream event)
   - Различи через временной паттерн: coordinated = ровные intervals, organic = clustered burst.

## Конкретные данные доступны

```
/srv/bots/.shared/tg/signals_master.jsonl      ← live (1985+ signals)
/srv/bots/.shared/tg/feed_onchain.jsonl        ← onchain-routed
/srv/bots/onchain/tg/channel_pump_predictiveness.json  ← per-channel pre-computed metrics
/srv/bots/onchain/tg/channel_multipliers.json
/srv/bots/onchain/tg/signals_database.jsonl    ← историческая база
/srv/bots/onchain/tg/batches/                  ← старые batched dumps
/srv/bots/onchain/tg/blind_spots.json          ← 635 токенов которые упоминались но мы пропустили
/srv/bots/onchain/tg/dumps/                    ← raw Telethon dumps (если есть)
/srv/bots/onchain/tg/media_signals_*.jsonl     ← media batches
/srv/bots/.shared/tg/media_tmp/                ← downloaded images (OCR'd)
```

## Что AI brain ДОЛЖЕН делать

### Каждый цикл (минимум):

1. **Проверить новый TG content** — `tail -50 feed_onchain.jsonl` за последние 6h. Что упоминалось?
2. **Cross-ref с closed_trades** — упомянутые токены в каких bigs? В каких rugs?
3. **Per-mention timing** — для каждой TG mention посчитать `(signal_time - pool_created_time)`, классифицировать канал (leading/lagging/real-time).

### Каждые 5-10 циклов:

4. **Channel deep-dive** — взять 1-2 каналов из top-12. Для каждого:
   - Скачать их историю (если ещё нет) — `dumps/<channel>.jsonl`
   - Посчитать **true alpha**: для каждой mention — `(channel_time vs first_pump_time)`, `pumped?`, `rugged?`, `big%?`
   - Найти **content signature** — каналы постят: тикер + CA, или CA + screenshot, или просто эмодзи?
   - Если канал постит изображения — **прочитать содержимое** через image analysis (есть Read tool с image support — Claude видит картинки напрямую)

### Каждые 20-30 циклов:

5. **Leading indicator discovery** — найти **что предшествует** TG mention'у на 5-60 минут:
   - Holder count delta?
   - First X tx by specific wallets?
   - Liquidity jump?
   - Pool age?
   - Bonding curve %?
   - **Если найдено** — пишешь paper-stream PRE_TG который входит до TG mention. Это и есть **обгон каналов**.

## Image analysis — ты можешь видеть картинки

Когда листенер скачивает картинку (OCR_HIT) или ты сам скачиваешь Telegram media — **используй Read tool на путь к JPG**. Claude видит изображения напрямую — без OCR.

Полезные сценарии:
- Screenshot DEXScreener candle → определить fractal pattern (Bart, Wedge, accumulation)
- Twitter screenshot → читать кто tweet'нул, какой sentiment
- Branded meme post → определить тематику канала (community vs alpha)

Команда: используешь Read с `file_path=/srv/bots/.shared/tg/media_tmp/<channel>_<msg_id>.jpg`.

## Запреты

- НЕ писать "TG mention → buy" без causal explanation
- НЕ принимать `channel_pump_predictiveness.json` без decontamination split (hindsight!)
- НЕ кидать в paper-stream фильтр "channel ∈ {X, Y, Z}" без понимания WHY эти каналы лидируют
- НЕ забывать что наша цель — **leading indicator**, не следование

## Метрика успеха для TG dive

- **first paper-stream PRE_TG** (entry до TG mention, на основе upstream signal) — это **первая настоящая alpha** TG-level.
- **classification всех top-30 каналов** на 5 типов — fundamental research result.
- **причинная гипотеза** "почему данный канал работает" — write up в `memory/onchain/insights/tg_channel_<name>_analysis.md`

## Открытые исследовательские вопросы (carry until answered)

1. **Капитанская каюта** (1855 mentions, доминирующий канал) — leading или lagging? Анализировать timing detail.
2. **on_chain_radar, architect_sol_rekt, PowsGemCalls, icodrops_sergey** — alpha-tier по `paper_streams_integration_20260509.md`. Подтверждается ли live?
3. **Какие 5-10 wallets** покупали $MC, $RICH, $WORLDCUP первыми — найти, сравнить, сделать leaderboard.
4. **PORTUGAL coin's name origin** — это название → откуда оно пошло? TG канал? Twitter? Это alpha signal источник?
5. **Image-based channels** (Gre4cha_crypto, MEMEcrypted, on_chain_radar, etc) — что в их изображениях? OCR пока 0 hits — возможно messages без media, нужно расширить трекинг.

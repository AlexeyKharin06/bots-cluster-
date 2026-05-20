# CRITICAL FINDINGS — общий лог для всех Claude-сессий кластера

> **ВСЕ AI brain сессии (onchain, listing-arb, cex-onchain, funding-rate) ОБЯЗАНЫ читать этот файл в начале каждого цикла.**
> Тут накапливаются проблемы, найденные одной сессией — чтобы другие не повторяли.
> Append-only (новые в начале), старое не удалять — это шкатулка знаний кластера.

---

## 2026-05-20 18:00 UTC — TG unified listener: events.NewMessage decorator pattern

**Симптом**: tg_unified_listener запускается, подключается, видит 65 каналов, но `events_received: 0` через час+ uptime.

**Корень**: Telethon-декоратор `@client.on(events.NewMessage())` (со скобками!) ≠ `@client.on(events.NewMessage)` (без скобок). Старый рабочий listener использовал БЕЗ скобок. С `()` в некоторых версиях Telethon handler не регистрируется на broadcast channels.

**Фикс**: убрать `()` после `events.NewMessage`. См. commit `0bc9134` в bots-cluster-.

**УРОК для всех сессий**:
- Если что-то "должно работать" но молчит — **first check actual events_received counter**, не верь "ну запущено же"
- Сравнивай с известно-рабочей старой версией (git log, старые tg_listener.py в /srv/bots/onchain/tg/) — НЕ изобретай заново синтаксис
- Telethon: `events.NewMessage` без `()` — proven pattern

---

## 2026-05-20 17:00 UTC — Telegram bot rate-limit (10h cooldown)

**Симптом**: `{"ok":false,"error_code":429,"description":"Too Many Requests: retry after 36802"}` на sendMessage.

**Корень**: Watchdog в режиме "зомби-рестарт" (когда был сломан wmic-based is_running) спамил tg_listener crashes, AI brain alerts × 4 проекта. Telegram забанил бота.

**Фикс**: rate-limit aware sending в AI brain (не чаще 1 alert / 10 мин на бота).

**УРОК**: TG alerts только при критичных событиях (cycle done, READY_FOR_REAL_MONEY, infrastructure broken). Не на каждый чих.

---

## 2026-05-20 14:00 UTC — Watchdog на Linux использовал Windows-команды (wmic/taskkill)

**Симптом**: 170+ zombie-процессов `lp_bot.js` накапливались за часы. Sniper умирал, не рестартился.

**Корень**: `is_running()` в watchdog.sh использовал `wmic process ...` (Windows only). На Linux команда не существует → возвращает count=0 → watchdog думает все мертвы → спавнит новые → старые не killed.

**Фикс**: pgrep/pkill вместо wmic/taskkill. Защита от накопления: `pkill -9 -f <pattern>` ПЕРЕД спавном.

**УРОК**: При переносе кода с Windows на Linux — `wmic`, `taskkill //F //PID`, `process.platform === 'win32'`, путь типа `D:\` НЕ работают. Проверять. Тестировать на VPS до commit.

---

## 2026-05-20 14:00 UTC — Hardcoded Windows path в Python scripts

**Симптом**: `signals_pool.json` не находился sniper'ом. На VPS появился файл с буквальным именем `D:\OnChain\scripts\wallet_v2\signals_pool.json` (с обратными слешами в filename).

**Корень**: `SIGNALS_PATH = Path(r'D:\OnChain\scripts\wallet_v2\signals_pool.json')` хардкод. На Linux `r'D:\...'` интерпретируется как имя файла в текущей dir.

**Фикс**: env var override + relative path resolution.

**УРОК**: ВСЕ paths в Python должны быть либо relative (`Path(__file__).parent / ...`), либо env-var driven, либо OS-detected. НИКОГДА hardcoded Windows path.

---

## 2026-05-20 06:30 UTC — Telethon AuthKeyDuplicatedError

**Симптом**: tg_listener крашится каждую минуту с `AuthKeyDuplicatedError`.

**Корень**: Один Telethon session.session использовался с двух IP (PC + VPS). Telegram автоматически дисконнектит "duplicate" session.

**Фикс**: ОДИН session per environment. Если переносишь session между машинами — она "сгорает". Нужна новая авторизация через QR + 2FA.

**УРОК для multi-project**: НЕ копируй один session на 4 проекта. Либо ОДНА unified session, либо 4 разных QR-авторизованных. **Единый unified TG hub** (как мы сейчас делаем) — правильный путь.

---

## 2026-05-19 cycle_1702 — Hindsight leakage в rugger_blacklist

**Симптом**: TEST WR=48% vs baseline 0% (paradigm shift!). Слишком хорошо чтобы быть правдой.

**Корень**: `rugger_blacklist.json` построен с использованием **будущих** данных (post-hoc). Использовать его как "veto-фильтр на момент entry" = look-ahead bias.

**Фикс**: decontamination split — CLEAN subset (token не overlap с blacklist construction window) показал WR = baseline. DIRTY subset держал alpha. Признак leakage.

**УРОК**: ВСЕГДА проверять каждый предрасчёт на leakage через decontamination split. `wallet_added_at` per entry в blacklist помог бы автоматически. Без timestamps — blacklist непригоден для honest backtest.

---

## 2026-05-19 cycle_1639 — H_LP_WHITELIST стабильное alpha

**Симптом**: Real persistent wallet alpha найдено: LP-providers с TRAIN n≥3 avg≥+30% rug≤33% → TEST держат rug 25.7% (vs baseline 43%), big-winners 14.3% (vs 1.5%).

**Но**: TEST avgPnL=-7.5% — current trail/cap не ловит fat-tail.

**УРОК**: Alpha ≠ profitable strategy. Exit logic должна соответствовать shape of returns. Для fat-tail memecoin: cap_500 + trail_85 не оптимально. Нужен Sharpe/expectancy-based gate, не +150% avgPnL.

---

## Структура файла

При добавлении новой записи — в самом верху (после `---`):

```
## YYYY-MM-DD HH:MM UTC — короткое название

**Симптом**: что наблюдалось
**Корень**: почему случилось
**Фикс**: что сделали / что нужно сделать
**УРОК**: что должны понимать все сессии чтобы не повторить
```

---

## Действие AI brain каждый цикл

1. Прочитать этот файл (`memory/CRITICAL_FINDINGS.md`)
2. Сравнить с известными паттернами своих ошибок
3. Если столкнулся с новой проблемой → **добавь сюда** запись (через коммит в bots-cluster-)
4. Уведомить через append в `memory/<project>/HISTORY.md`: `cycle_id | found CF#N: <название>`

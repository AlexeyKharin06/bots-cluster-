---
name: Session log pointer
description: At start of every session in D:\CEX-Onchain, read SESSION_LOG.md after CLAUDE.md to recover full chronological context
type: reference
originSessionId: f476addf-208d-4c1c-b358-e7b4187e980d
---
При старте новой сессии в D:\CEX-Onchain — обязательно прочитать в этом порядке:

1. `D:\CEX-Onchain\CLAUDE.md` (auto-loaded) — текущее состояние, конфигурация бота, последние decisions
2. `D:\CEX-Onchain\reports\SESSION_LOG.md` — chronological история всех сессий
3. `D:\CEX-Onchain\reports\LESSONS.md` — 17 универсальных уроков (избежать повторных ошибок)
4. `D:\CEX-Onchain\reports\IDEAS_BACKLOG.md` — что ✅ / ⏳ / ❌ / 💡

**SESSION_LOG.md содержит**:
- Hypothesis Rejection Catalog (6 отклонённых) — НЕ перетестировать без больше данных
- Untested Hypotheses (8 в очереди) — что протестировать когда будет infrastructure
- Strict Validation Process (5-step) — обязательный для new hypothesis
- Current Bot State Summary — config + slots на момент last update

**Обновлять SESSION_LOG.md после каждой значимой сессии**:
- Что DEPLOYED
- Что REJECTED (через strict validation, with reason)
- Live wins/losses
- Артефакты добавленные
- Next steps

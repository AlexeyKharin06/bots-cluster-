# Директива для новой Claude-сессии — миграция проекта

> Открой Claude в папке проекта на ПК (например `cd D:\Listing Arb && claude`), вставь блок ниже целиком, замени `<PROJECT>` на свой проект (`listing-arb` / `cex-onchain` / `funding-rate`) и название папки.

---

## КОПИРУЙ ОТСЮДА В НОВУЮ CLAUDE-СЕССИЮ

```
КОНТЕКСТ: Кластер ботов уже работает на Hostinger VPS 187.127.87.202.
GitHub: https://github.com/AlexeyKharin06/bots-cluster-
Уже мигрирован OnChain (Solana sniper + AI brain). Инфраструктура готова.

ТЕБЕ НУЖНО: перенести проект <PROJECT_NAME> (D:\<PROJECT_FOLDER>) на VPS.

КРЕДЕНШИАЛЫ (подставит пользователь в чате этой сессии, в репо НЕ коммитим):
- VPS root password: <user paste>
- GitHub PAT: <user paste>
- TG bot token: <user paste>
- TG chat: <user paste>
- VPS user 'bots' имеет sudo+docker

ИНФРАСТРУКТУРА КОТОРАЯ УЖЕ ЕСТЬ НА VPS:
- /srv/bots/<project>/{code,data,logs} — структура для каждого проекта
- /srv/bots/cluster/ — общий репо (склонирован)
- /srv/bots/cluster/shared/autonomous_cycle.sh — AI brain cycle (без модификации)
- /srv/bots/cluster/shared/migrate_project.sh — миграция (используй его!)
- /srv/bots/.shared/.env — общие секреты (TG_TOKEN, TG_CHAT)
- Git creds для bots: ~/.git-credentials (PAT)
- Cron: AI brain каждые 6h на своём offset (см. ниже)

CRON OFFSETS (антикорреляция чтобы Anthropic rate-limit не упирался):
- onchain: 0/6/12/18 (занят)
- trade: 1/7/13/19
- listing-arb: 2/8/14/20
- cex-onchain: 3/9/15/21
- pl: 4/10/16/22
- funding-rate: 5/11/17/23

ШАГИ МИГРАЦИИ:

1. ПРОЧИТАЙ код проекта в D:\<PROJECT_FOLDER>\ — пойми что делает бот:
   - CLAUDE.md (если есть) — описание
   - Главные .js или .py файлы (есть ли main, watchdog, daemon)
   - state.json (есть ли накопленные данные)
   - package.json/requirements.txt — зависимости

2. ПОДГОТОВЬ tar архив (запусти на ПК):
   cd D:\<PROJECT_FOLDER>
   tar -czf D:\<project>.tar.gz --exclude=node_modules --exclude=*.log --exclude=.git scripts tg .env package.json 2>/dev/null
   (если структура иная — адаптируй под реальные папки)

3. ОТПРАВЬ на VPS:
   scp D:\<project>.tar.gz root@187.127.87.202:/tmp/

4. SSH на VPS под root, запусти миграцию-скрипт:
   ssh root@187.127.87.202
   PROJECT=<project> bash <(curl -fsSL https://raw.githubusercontent.com/AlexeyKharin06/bots-cluster-/main/shared/migrate_project.sh)
   
   Скрипт сам:
   - распакует
   - сделает chown
   - npm install / pip install
   - создаст /home/bots/run_cycle_<project>.sh
   - добавит cron entry
   - создаст memory/<project>/PROJECT_CONTEXT.md шаблон

5. ОБНОВИ PROJECT_CONTEXT.md (как bots):
   - Опиши цель проекта (на основе кода что прочитал)
   - Опиши data sources (какие API, какие state files)
   - Опиши стратегию (что бот делает)
   - Опиши промежуточные KPI (что считать прогрессом)
   - Закоммить в репо: cd /srv/bots/cluster && git add memory/<project>/ && git commit -m "init <project> context" && git push

6. ПЕРВЫЙ ТЕСТ AI BRAIN:
   sudo -u bots /home/bots/run_cycle_<project>.sh
   Жди до 30 мин. После — кинь BRIEF.md в чат.

7. (ОПЦИОНАЛЬНО) Если у проекта есть свой бот-runtime (как sniper у OnChain) — запусти его через watchdog или nohup:
   sudo -u bots bash -c 'nohup bash /srv/bots/<project>/code/<watchdog_or_main>.sh > /srv/bots/<project>/logs/main.log 2>&1 &'

ВАЖНО:
- Не пиши длинные команды через PowerShell paste — он ломает bracketed paste. Используй nano или heredoc или curl|bash паттерны.
- Не запускай реальные сделки без явного "yes do it" от пользователя.
- Не трогай /srv/bots/onchain/ — он уже работает, не сломай его.
- Если упрёшься в sandbox permission — используй --dangerously-skip-permissions через env var CLAUDE_EXTRA_FLAGS (уже настроено в /home/bots/.bashrc).

В КОНЦЕ:
- Push в GitHub
- Подтверди user что migration done + cron активен
- Покажи последний BRIEF.md
```

---

## Что замени перед вставкой

| Placeholder | Listing Arb | CEX-Onchain | funding_rate |
|---|---|---|---|
| `<PROJECT_NAME>` | Listing Arb | CEX-Onchain | funding_rate |
| `<PROJECT_FOLDER>` | Listing Arb | CEX-Onchain | funding_rate |
| `<project>` (lowercase) | listing-arb | cex-onchain | funding-rate |

Например для Listing Arb — заменишь все `<PROJECT_NAME>` на "Listing Arb", `<PROJECT_FOLDER>` на "Listing Arb", `<project>` на "listing-arb".

## Порядок запуска

1. Открой Claude в **D:\Listing Arb** — вставь директиву с подстановками — жди 30-60 мин.
2. После завершения — открой Claude в **D:\CEX-Onchain** — повтори.
3. После завершения — открой Claude в **D:\funding_rate** — повтори.

Между сессиями жди завершения предыдущей, чтобы не перегружать VPS.

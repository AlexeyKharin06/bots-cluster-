# Добавление нового проекта в кластер

Шаблон для Trade / Listing Arb / CEX-Onchain / PL / Funding-Rate.

---

## 1. Локально (на твоём ПК) — подготовь код проекта

Каждый проект — отдельная папка с готовым ботом. Например `D:\Trade\`.

Что должно быть в папке:
- Основной runtime (Node/Python скрипты бота)
- `.env` с API ключами (его НЕ коммитим)
- `data/` с `state.json` если уже накопил историю
- `logs/`

---

## 2. На VPS — добавь runtime директорию

```bash
ssh root@187.127.87.202
mkdir -p /srv/bots/trade/{data,logs,tg_session}
chown -R bots:bots /srv/bots/trade
```

Скопируй с локального:
```bash
# С твоего ПК
rsync -avz -e ssh D:/Trade/.env             root@187.127.87.202:/srv/bots/trade/.env
rsync -avz -e ssh D:/Trade/data/state.json  root@187.127.87.202:/srv/bots/trade/data/
rsync -avz -e ssh D:/Trade/tg_session.session  root@187.127.87.202:/srv/bots/trade/tg_session/
```

---

## 3. В GitHub repo — добавь проект

```bash
# Локально, в склонированном bots-cluster-
mkdir -p projects/trade
# Положи туда код (НЕ data/ и НЕ .env)
cp -r D:/Trade/scripts projects/trade/
cp D:/Trade/package*.json projects/trade/

# Dockerfile (можно скопировать с onchain и подправить CMD)
cp projects/onchain/Dockerfile projects/trade/

# docker-compose.yml аналогично — меняй пути на /srv/bots/trade
cp projects/onchain/docker-compose.yml projects/trade/
# Отредактируй: container_name, env_file, volumes

git add projects/trade/
git commit -m "add trade project"
git push
```

---

## 4. На VPS — собери и запусти контейнер

```bash
ssh root@187.127.87.202
sudo -u bots bash
cd /srv/bots/cluster
git pull
cd projects/trade
docker compose up -d --build
docker logs trade-bot --tail 50
```

---

## 5. Добавь autonomous_cycle для этого проекта в cron

**КРИТИЧЕСКИ ВАЖНО — антикорреляция чтобы не упереться в Anthropic rate limit**:

| Проект | Cron schedule (UTC) |
|---|---|
| OnChain        | `0 0,6,12,18 * * *`  |
| Trade          | `0 1,7,13,19 * * *`  |
| Listing Arb    | `0 2,8,14,20 * * *`  |
| CEX-Onchain    | `0 3,9,15,21 * * *`  |
| PL             | `0 4,10,16,22 * * *` |
| Funding Rate   | `0 5,11,17,23 * * *` |

Каждый проект запускается раз в 6h, но смещен на 1h относительно соседа. Никогда не работают одновременно → Anthropic не паникует от парallel calls.

```bash
sudo -u bots crontab -e
# Добавить строку:
0 1,7,13,19 * * * cd /srv/bots/cluster && PROJECT=trade bash shared/autonomous_cycle.sh >> /srv/bots/.shared/logs/cron.log 2>&1
```

---

## 6. Что AI brain делает для нового проекта

Для каждого проекта `autonomous_cycle.sh` запускает claude headless с одним промптом, но `PROJECT=<name>` env var определяет:
- какой `sniper_state.json` читать
- куда писать insights (`memory/<project>/`)
- что коммитить (`projects/<project>/`)

Открытый промпт ("ищи паттерны, тестируй, добавляй paper-streams") универсален — работает для любого crypto-проекта. Если стратегия специфична — добавь файл `projects/<project>/AGENT_HINTS.md`, его подхватит cycle.

---

## 7. Проверка работы

```bash
# Что сейчас работает
docker ps
sudo -u bots crontab -l
ls -lh /srv/bots/.shared/logs/cycle_*.log | tail -10

# Последние commits AI brain
cd /srv/bots/cluster && git log --oneline -20

# Конкретный проект — последний insight
cat /srv/bots/cluster/memory/trade/BRIEF.md
```

---

## 8. Откатить если что-то пошло не так

```bash
# Остановить cron
sudo -u bots crontab -l | grep -v "PROJECT=trade" > /tmp/c && sudo -u bots crontab /tmp/c

# Остановить контейнер
cd /srv/bots/cluster/projects/trade && docker compose down

# Если AI накоммитил мусор
cd /srv/bots/cluster && git log --oneline -10
git revert <bad-commit-sha>
git push
```

---

## Шорткат для всех 5 проектов сразу

После того как один проект (Trade) развёрнут, скрипт `shared/add_project.sh <name>`:
```bash
bash shared/add_project.sh listing-arb
# Создаст /srv/bots/listing-arb/{data,logs,tg_session}, добавит cron, спросит куда копировать код
```

(Будет реализован в Phase 2 — когда подтвердим что OnChain стабильно работает на VPS.)

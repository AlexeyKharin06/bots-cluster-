---
name: feedback_workflow
description: Backtest-first workflow; auto-mode default; no Telegram alerts in bot
type: feedback
originSessionId: 85c10b6b-1725-43a1-b367-a7d67462402e
---
The user's workflow rules for this project.

**Rule 1: Backtest before changing the bot.**

Don't apply config changes to `bot/config.py` based on hypothesis alone —
always run a backtest first (use `scripts/35_tg_hypotheses_backtest.py`
as a template), then walk-forward verify (train 60d / test 30d), then
share numbers and wait for explicit approval before committing the change.

**Why:** the user lost time on 2026-05-04 when I changed `TIME_EXIT_HOURS`
from 48 to 168 based on a partial backtest without proper grid + walk-forward.
They explicitly rolled it back and instructed: "не меняй сразу бота, сначала
проведи бэктесты, убедись, потом принимай решение о внесении изменений".

**How to apply:** any time I find an "improvement" idea (new threshold,
new feature, longer exit, etc.) — write a backtest script first, get the
numbers, share results, wait for "yes". Don't preemptively edit config.py.

**Rule 2: Auto-mode is the default operating style.**

The user often invokes auto mode and prefers autonomous execution on low-risk
work. Minimize "should I?" questions for routine execution. But Rule 1
still applies — backtests come before bot edits.

**Rule 3: No Telegram alerts in the bot.**

The user explicitly disabled Telegram alerts: "давай без телеграмма просто
пусть бот автоматически торгует". Bot must NOT send messages to Telegram.

**Rule 4: State persistence is critical.**

Every trade, signal, orderbook snapshot, and transfer event must be written
to JSONL/parquet for later analysis. Bot should never lose data on crash —
hourly buffer dumps to `bot/logs/buffer_transfers/<hour>.parquet`.

**Why:** the user said "главное чтобы все сохранялось чтобы мы накапливали
данные и могли потом улучшать стратегию".

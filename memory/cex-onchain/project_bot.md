---
name: project_bot
description: How the live bot is run, where state lives, how to restart
type: project
originSessionId: 85c10b6b-1725-43a1-b367-a7d67462402e
---
**Why:** to avoid forgetting how the bot is wired up across sessions.

**How to apply:** when the user asks "is the bot running?" / "restart bot" / etc.

## Bot lifecycle

- Entry: `python -m bot.main` (from `D:\CEX-Onchain`)
- Auto-restart wrapper: `D:\CEX-Onchain\bot\start.bat` (loops, 30s backoff on crash)
- Started detached via PowerShell:
  `Start-Process cmd /c D:\CEX-Onchain\bot\start.bat -WindowStyle Minimized`
- Survives Claude session closure (cmd.exe is not parented to Claude)
- For boot-time persistence, optional: `nssm install CEXOnchainBot ...`

## State

- In-memory state auto-persists every 30s to `bot/state/state.json`
- On restart: state.json is reloaded automatically (positions, capital, cooldowns)
- All signals → `bot/logs/signals.jsonl`
- All closed trades → `bot/logs/trades.jsonl`
- Orderbook snapshots → `bot/logs/orderbook_snapshots.jsonl`
- Hourly transfer buffer dumps → `bot/logs/buffer_transfers/<UTC-hour>.parquet`

## Mode

- **DRY_RUN=True** by default in `bot/config.py`
- Live mode requires explicit user instruction; user has not authorized it yet.
- When switching to live: also start with `LEVERAGE=1` and small capital.

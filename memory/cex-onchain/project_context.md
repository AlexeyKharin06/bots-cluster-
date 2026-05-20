---
name: project_context
description: Pointer to D:\CEX-Onchain\CLAUDE.md which contains full project state
type: project
originSessionId: 85c10b6b-1725-43a1-b367-a7d67462402e
---
The full, up-to-date project context lives in **`D:\CEX-Onchain\CLAUDE.md`**.

When starting a new session in this directory: read CLAUDE.md first. It contains:
- Strategy summary (CEX deposit-cluster signal → SHORT)
- File structure (data/scripts/bot/reports/tg)
- API keys location (.env)
- Bot config snapshot (slots A/B/C + A2/K/R + 7 observers)
- Confirmed top configs from backtest (with PnL numbers)
- TG-channel insights summary (5 hypotheses, 3 validated)
- Pending decisions for the user
- Open improvements roadmap
- Decisions log

**Why:** the user said the chat history grows huge (~200k tokens) and asked
to compress context while keeping continuity. CLAUDE.md is the durable summary
loaded automatically into every new session.

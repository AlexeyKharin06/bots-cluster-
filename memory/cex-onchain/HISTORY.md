20260520_0556 | MIGRATION from Windows D:\CEX-Onchain to VPS /srv/bots/cex-onchain/ | files: cycle init (PROJECT_CONTEXT.md, BRIEF.md, HISTORY.md created)
20260520_0559 | (auto) cycle ran | files: cycle_20260520_0559.md

## Cycle init — VPS sync setup (2026-05-20 06:35 UTC)
- **GitHub repo created**: AlexeyKharin06/cex-onchain (private)
- **Git init local** D:\CEX-Onchain, .gitignore excludes secrets+data+state
- **VPS layout**: /srv/bots/cex-onchain/code/ cloned from GitHub
- **Auto-pull cron**: `*/5 * * * * /home/bots/git_pull_cex-onchain.sh` — every 5 min
- **First sync test**: README.md commit `b070376` propagated D:\ → GitHub → VPS in ~2s
- **Server-only data preserved**: data/ (67M, 207 parquets), bot/logs/, bot/state/, tg_session, secrets
- **TG auth done** earlier with code 31681 → @alexey_khar1n
- **AI brain cron**: 0 3,9,15,21 UTC (next fire 09:00 UTC)
- **Next**: cycles run autonomously; future code edits in D:\CEX-Onchain → git push → VPS auto-sync

## Unified TG Hub integration (2026-05-20 13:28 UTC)
- Per-project tg_listener DISABLED (touch .tg_listener_disabled)
- Source switched to unified hub: /srv/bots/.shared/tg/feed_cex.jsonl (CEX-arb routed signals) + signals_master.jsonl (raw, fallback)
- bot/tg_external_reader.py updated (commit f9e4531) — VPS pulled via git in 2s
- One Telethon process (PID 95970) listens 65 channels for ALL 4 projects (no more AuthKey conflicts)
- Tmux `cex-brain` running AI brain cycle 20260520_1328 — user attaches via `ssh root@VPS; sudo -u bots tmux a -t cex-brain`
- Cron `0 3,9,15,21 UTC` continues background cycles
20260520_1328 | (auto) cycle ran | files: cycle_20260520_1328.md

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

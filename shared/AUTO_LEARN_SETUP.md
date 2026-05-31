# Auto-Learn Setup Guide

Continuous learning loop for sniper.

## Files
- `auto_learn.py` — main script (retrains model nightly)
- `auto_learn_output/current_model.pkl` — current production model (managed by auto_learn)
- `auto_learn_output/auto_learn_history.json` — append-only audit log
- `score_token.py` — picks current_model.pkl preferentially (fallback to v3, then v1)

## How it works
1. Loads closed_trades + rugger_blacklist + wallet_history
2. Dedup by token, build feature matrix
3. Evaluate current model AUC on last 7 days
4. If AUC dropped >5% vs baseline → retrain on last 30 days
5. Try 4 algos (LR, RF, GB, ET) with 5-fold time-series CV
6. Save best model as `current_model.pkl`
7. Log decision to history

## Setup on VPS (Linux cron)
```bash
# Edit crontab
crontab -e

# Add line (daily at 03:00 UTC):
0 3 * * * cd /srv/bots/onchain/code && python /srv/bots/onchain/code/deploy/shared/auto_learn.py >> /srv/bots/onchain/code/deploy/shared/auto_learn_output/auto_learn.log 2>&1
```

## Setup on Windows (Task Scheduler)
```cmd
schtasks /create /tn "AutoLearnSniper" /tr "python D:\OnChain\deploy\shared\auto_learn.py" /sc daily /st 03:00
```

## Manual run
```bash
python D:/OnChain/deploy/shared/auto_learn.py            # standard (drift check + retrain if needed)
python D:/OnChain/deploy/shared/auto_learn.py --force    # force retrain
python D:/OnChain/deploy/shared/auto_learn.py --window 60  # use 60-day window
```

## Outputs after each run
- `current_model.pkl` overwritten if retrained
- `auto_learn_history.json` appended with:
  ```json
  {
    "timestamp": "2026-05-30T21:23:32",
    "action": "retrained" | "no_action",
    "best_model": "ET",
    "cv_auc": 0.820,
    "n_train": 689,
    "recent_auc": 0.85,
    "baseline_auc": 0.82,
    "drift": +0.03
  }
  ```

## Initial run (already done 2026-05-30 21:23)
- Best: ExtraTrees CV AUC=0.820 on 689 dedup rows
- Saved to `auto_learn_output/current_model.pkl`
- `score_token.py` now uses this preferentially

## Live deployment workflow
1. Sniper revives after Helius reset
2. New live trades start flowing into `sniper_state.json`
3. Nightly cron runs `auto_learn.py`
4. After 7-14 days of live data → first meaningful drift check
5. Model auto-updates when needed
6. `score_token.py` automatically picks up new model on next call

## Drift alerting (TODO)
Add to auto_learn.py end:
```python
if abs(drift) > 0.1:
    send_telegram(f'⚠️ AUC drift {drift:+.2f} detected — model retrained')
```

# Notice to other Claude sessions (listing-arb, cex-onchain, onchain)

**Date:** 2026-05-21 (from funding-rate session)

## Bug discovered: shared autonomous_cycle.sh is hardcoded for onchain

`/srv/bots/cluster/shared/autonomous_cycle.sh` has these onchain-specific parts:

1. **Prompt** (line ~170+):
   > "Ты автономный AI-стратег. Цель проекта: +100,000% при минимальных рисках через выявление on-chain wallet-паттернов перед памп/раг."

2. **Resource limit list** (in ЗАПРЕТЫ): mentions SNIPER_A/B/D/GOLD3/GOLD4/GOLD5/WHALE/LATE/LOWCAP — onchain-only

3. **--add-dir** flag: hardcoded `/srv/bots/onchain`, not project-specific

4. **State snapshot** loops through all projects but only finds data for ones with `data/sniper_state.json` (onchain has it, others don't)

## Result

- **onchain**: works correctly (5+ real cycles, 20-27KB insights, real findings like H_V7_ANTICLUSTER +130%)
- **listing-arb**: 0 cycles ever ran (insights/ empty)
- **cex-onchain**: 2 placeholder cycles (143 bytes each, "AI skipped write")
- **funding-rate**: 6 misplaced cycles with onchain content (now archived to `_misplaced_onchain_backup/`)

## Fix template — what funding-rate did (replicate for your project)

1. Wrote project-specific cycle script: `/srv/bots/<project>/code/scripts/<project>_brain_cycle.sh`
   - Own state snapshot (reads paper trades, available data, TG feed for THIS project)
   - Own prompt (declares project focus, lists validated negatives + untested hypotheses)
   - `--add-dir /srv/bots/<project>` instead of onchain
2. Updated `/home/bots/run_cycle_<project>.sh` to call `<project>_brain_cycle.sh` instead of `shared/autonomous_cycle.sh`
3. Archived misplaced onchain insights to `_misplaced_onchain_backup/` in your memory dir
4. Reset BRIEF + HISTORY to clean state
5. Triggered manual cycle to verify

See `/srv/bots/funding-rate/code/scripts/funding_brain_cycle.sh` as reference implementation.

## Alternative fix — patch shared script

Make these parametric:
- `PROMPT_FILE=$MEMORY/$PROJECT/CYCLE_PROMPT.md` (each project provides)
- `ADD_DIR=/srv/bots/$PROJECT`
- State snapshot calls `$CODE_DIR/scripts/prepare_cycle_state.sh` if exists

Then each project owns its own prompt + state-prep without forking the full cycle.

Either approach works — funding-rate went with separate script for isolation.

## Why this matters

User invested time setting up 4 separate Claude sessions per project (one tmux per project). The expectation: each project's AI brain develops ITS OWN niche, generates ITS OWN hypotheses, validates ITS OWN edges. Currently only onchain is getting that benefit. The other 3 (including funding-rate) are essentially idle from AI-brain perspective.

# BRIEF — funding-rate snapshot

## State (as of 2026-05-21 14:50 UTC, cycle 20260521_1450)
- Migrated to VPS 2026-05-20; pre-migration code present (100+ scripts, all backtest_*/paper_*)
- Cycle script: `scripts/funding_brain_cycle.sh` (funding-rate-specific, post-misattribution fix)
- 2 honest funding-rate cycles completed (20260521_1430 cleanup, 20260521_1450 TG diagnosis)

## TG feed status — DIAGNOSED THIS CYCLE
- `feed_funding.jsonl` does not exist (zero signals routed since listener went live 2026-05-20 18:08)
- Root cause: **upstream channel absence**, not keyword regex
- User's TG folders detected: `OnChain` (11), `Bot` (9), `crypto` (46). Folders `funding`/`arb`/`listing`/`trading` referenced in code DO NOT EXIST on the account
- All 65 listened channels = memecoin/onchain. 0/501 master signals contain `funding`/`фандинг`/`ставка`/`basis`/`perpetual`/`open interest`
- Fix-1 (preferred): user creates `funding` folder + joins funding channels, restarts listener
- Fix-2 (autonomous, pending H29 ack): direct exchange-API poller (Binance/Bybit/OKX/Hyperliquid funding endpoints)
- Fix-3: keyword regex broadening — postponed (shared infra)

## Resources available on VPS
- Paper-bots: 0 (all on user's local PC)
- Parquet backtests (multi_ex_funding_180, mega_fairprice, expansion_funding): NOT on VPS
- TG signals_master.jsonl: 501 records (route mix: 497 onchain / 132 listing-arb / 18 cex / **0 funding**)
- Code: 100+ pre-migration scripts under /srv/bots/funding-rate/code/

## Validated negatives — DO NOT retest
- R1 interval-prediction premium-streak alone (2-9% live precision, was 96% w/ survivorship bias)
- R2 fair-price scalping (0/5 weeks walk-forward profitable)
- R3 listing momentum mechanical (32% win, -$11/90d)
- R4 microcaps expansion RAVE/SIREN/PIPPIN (DEGRADES 86%)
- R5 multi-ex spread arb naive (-$13473 / 30902 trades)
- R6 naive funding harvest >2% threshold (-$304 / 315)
- R7 multi-signal confluence LONG-side (27% win, -$0.85/trade)

## Open hypotheses (prioritized; first 3 are this cycle's new ones)
- **H29** direct exchange-API funding poller — replaces empty TG feed (needs user OK for new poller)
- **H30** basis spot-vs-perp cross-ex scanner (PAPER, depends on H29)
- **H31** interval-shortening v2 with API-source confidence (vs 2-9% TG-source precision)
- H1 whale-copy paper bot (@on_chain_radar 5/18 PnL claims)
- H2 confluence SHORT-only expansion (n=5 → n=30+; n=5 showed 80% win)
- H3 stablecoin depeg arb (USDD precedent +$2300)
- H4 CEX→DEX algo flow tracking
- H5 announcement watcher (Bybit interval-change announcements; 95% precision)
- H6 new symbol detection (30s API polling, listings)

## Asks for user (blocking forward progress)
1. Either: create `funding` TG folder + join 5-10 funding channels (CoinGlass, Hyperliquid alerts, basis trader rooms) AND restart listener; OR: ack H29 so I implement the exchange-API poller next cycle
2. Sync parquet files (multi_ex_funding_180, mega_fairprice, expansion_funding) from local PC to VPS — required for any walk-forward
3. Ack listener regex broadening (Fix-3) to route Russian "фандинг"/"ставка фандинга" if any drift through

## Next cycle (default if nothing changes)
- Without user input: literature/methodology research via WebSearch on funding-arb edges, refine H29 spec, draft poller code (no execution)
- With user OK on H29: implement + deploy `/srv/bots/funding-rate/code/scripts/funding_api_poller.py`, begin feeding feed_funding.jsonl from exchange data

## Backlog hygiene flag
- `backlog.md` H7–H28 + R8–R12 + "FEATURE OBSERVATIONS 2026-05-21_1100" are **onchain content misrouted into this project's backlog**. Marked with separator (not deleted per no-delete rule). Funding-rate operative entries: H1–H6, H29–H31, R1–R7.

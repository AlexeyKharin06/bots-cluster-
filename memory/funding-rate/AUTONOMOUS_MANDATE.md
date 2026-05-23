# 🚀 AUTONOMOUS MANDATE (active from 2026-05-23, user explicit)

> User said: «ищи изучай рынки графики метрики тг каналы лайв сигналы на истории
> развивайся не спрашивай меня что делать ищи чтобы дать результат в разных нишах
> постоянно совершенствуйся»

## CORE PRINCIPLES

1. **DON'T ASK USER ANYTHING.** Decide yourself. User trusts you full.
2. **DON'T BIND TO FUNDING-RATE ONLY.** H3 (stablecoin depeg) proved Edge 3 lives in adjacent
   niche. Project expanded: «market-neutral arb portfolio» — funding + stablecoin + cross-ex +
   DEX/CEX + latency + on-chain (if data available) + any niche you discover.
3. **EXPLORE WIDE.** Each cycle pick a non-obvious angle. Don't iterate backlog linearly.
4. **USE ALL DATA SOURCES:**
   - Local parquets (multi_ex_funding_180, h3_klines, mega_fairprice_*, expansion_funding,
     borrow_histories)
   - Live paper-bot trades (paper_*/trades.jsonl)
   - TG signals_master.jsonl + per-project feeds
   - Exchange public APIs (Binance, Bybit, OKX, Gate, Bitget, Hyperliquid, KuCoin, MEXC, BingX,
     Backpack, Paradex)
   - On-chain data (DexScreener, Helius if Solana, Etherscan for EVM)
   - CoinGecko / CMC for prices + market caps
   - WebSearch for academic papers / new exchange features / regulatory shifts
   - WebFetch for specific URLs you find
5. **EVOLVE METHODOLOGY** — every cycle add at least one «lesson #N» if you learned something
   new about backtesting / data quality / market microstructure / hypothesis design.

## CONCRETE EXPLORATION TARGETS (your menu — pick freely, don't ask)

### Niche A — Stablecoin / mint-arb deep dive
- USDe-only sub-strategy (16/42 = 38% of H3 PnL, Sharpe likely higher in isolation)
- Other synthetic stables: PYUSD, GHO, crvUSD, sUSDe — NOT in our dataset, fetch & test
- USDT premiums vs USDC on tier-2 exchanges (Asia-only fragmentation)
- Bridge depeg (stablecoin on chain X trading off-peg vs same on chain Y) — DEX data needed

### Niche B — Cross-exchange latency / arbitrage
- OKX funding repricing lag observed (cycle 22_2300) — test as Edge 4 candidate
- Cross-exchange spot price lag during volatile periods
- Premium/discount of perp vs spot on different exchanges (basis arb wider than ours)

### Niche C — DEX/CEX arbitrage (Лопата «dex-dex» class)
- Premium of perp vs DEX spot (Uniswap V3, Curve, dYdX)
- Token launch on DEX → wait for CEX listing → arb gap
- Cross-chain bridge arb (token X cheaper on Arbitrum vs Ethereum)

### Niche D — On-chain alpha (if Helius/RPC available)
- Whale wallet copy-trade — paper_whale already in pipeline
- Large dev unlock / vesting schedule events on tokens
- Token holder concentration changes as predictor

### Niche E — TG signal microstructure
- 1582 master_signals already collected. Mine for patterns:
  - Which channels actually predict moves (vs report after)?
  - Lead-time distribution per channel
  - Cross-channel confirmation effect

### Niche F — Funding-rate evolution (your home niche)
- H38 paper-stream design (40× throughput, READY to spec)
- USDe yield arb (Ethena pays yield in funding-like mechanism) — research
- Negative funding farming on specific symbols with predictable cycle
- Multi-asset basket spread (long basket A perps + short basket B perps)

### Niche G — Methodology / system improvements
- Tighten existing edges (H31 sub-segments, H34 hedge selection)
- Find LOSING situations within our 3 edges → blacklist filters
- Data quality audits (find datasets we should fetch but haven't)

## DECISION RULE (per cycle)

Use this priority:
1. **If something is showing live anomaly** (paper bot win streak, big TG signal, spike) → investigate immediately
2. **If a Niche A-F has obvious low-hanging fruit not tested** → take it
3. **If running out of obvious next steps** → invent new combination from already-validated edges

## NEVER

- Don't repeat REJECTEDs (R1-R17 in backlog)
- Don't ask user for permissions for paper-trading / research / data fetch
- Don't write code that does live-money trading
- Don't get stuck on one hypothesis for >2 cycles — if not converging, pivot

## ALWAYS

- Write full insight to insights/cycle_YYYYMMDD_HHMM.md (untruncated)
- Append HISTORY.md one-liner
- Update BRIEF.md
- Add new hypotheses / status changes to backlog.md
- Commit + push to git (memory only, never code from cycle)
- If you discover a true new niche/edge → propose paper-stream spec right there

## CURRENT KPI / READINESS

3 edges validated (H31 +3.45%, H34 +1.28%, H3 +1.37% counter-cyclical).
Portfolio risk-adjusted return very strong. Next milestone: PAPER-STREAM DEPLOYMENT for
all 3 edges, accumulate forward data, after 30-60 days propose REAL_MONEY transition.

GO.

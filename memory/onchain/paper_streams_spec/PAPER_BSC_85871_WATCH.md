# PAPER_BSC_85871_WATCH — Paper Stream Spec (cycle 20260525_0600)

**Status**: PROPOSED — pending user approval (new this cycle).
**Class**: NAMED-WALLET WATCH (Methodology #14 candidate). BSC analog of PAPER_SOL_HUPHEY_WATCH.
**Risk**: paper, size=$1, ~$2-3/day (lower cadence than HUPHey).

## Discovery
Building BSC analog of Sol's HUPHey wallet-leaderboard: scanned `entry_signal.bonding_curve_buyers[0].addr` across all BSC tokens in state.json. Top result: **0x85871aea93f086eeda...** with n=8 BSC tokens, **5 bigs (62%), 1 rug (12%), avg=+289.9%, K=0.281, geom=+58.88%/trade**.

This is the **BSC PORTUGAL FAMILY CREATOR** wallet — bc[0] on every PORTUGAL-strict entry C7/C8/C9/C10 and on the BSC anti-PORTUGAL "Poor" (bc=1) big.

## Wallet timeline

| time UTC | symbol | bc | k | pnl | stream |
|---|---|---|---|---|---|
| 2026-05-23T11:25 | ELON | 20 | 2 | -86.4 | BSC_FILTERED |
| 2026-05-23T13:16 | **xing** | 20 | 1 | **+293.2** | B |
| 2026-05-23T15:13 | **TRUMPBANK** | 20 | 1 | **+349.1** | B |
| 2026-05-24T01:58 | CAP | 20 | 1 | -100.0 | BSC_FILTERED |
| 2026-05-24T02:28 | MOODANG | 20 | 2 | +89.7 | BSC_FILTERED |
| 2026-05-24T04:46 | **BabyAsteroid** | 20 | 1 | **+879.5** | B |
| 2026-05-24T07:16 | **Poor** | 1 | 1 | **+659.2** | B |
| 2026-05-24T14:02 | **BELIEF** | 20 | 1 | **+235.0** | B |

5 bigs / 8 tokens / 1 rug / avg +289.9%. **Note Poor BSC has bc=1** — outside PORTUGAL strict (bc≥16 ∩ k≤10), captured ONLY by this wallet filter.

## Walk-forward (prior-history-required, named-class)
Spec: at entry T, if wallet's prior_n≥3 AND prior_bigs≥2 AND prior_rugs≤1 → enter.

| entry time | prior n | prior bigs | prior rugs | qualifies? | outcome |
|---|---|---|---|---|---|
| ELON | 0 | 0 | 0 | NO | n/a |
| xing | 1 | 0 | 0 | NO | n/a |
| TRUMPBANK | 2 | 1 | 0 | NO (priors<3) | n/a |
| CAP | 3 | 2 | 0 | YES | -100.0 (RUG) |
| MOODANG | 4 | 2 | 1 | YES | +89.7 |
| BabyAsteroid | 5 | 2 | 1 | YES | +879.5 ★ |
| Poor | 6 | 3 | 1 | YES | +659.2 ★ |
| BELIEF | 7 | 4 | 1 | YES | +235.0 ★ |

**Walk-forward n=5**: outcomes [-100, +89.7, +879.5, +659.2, +235.0]
- bigs (≥150) = 3 (60%)
- rugs (≤-90) = 1 (20%)
- avg pnl = +352.7%
- K = 0.30 (estimated, small-n)
- geom = +62%/trade
- **catches 3 of 4 productive-cluster bigs (BabyAsteroid C9, Poor anti-PORTUGAL, BELIEF C10)** that PORTUGAL strict caught.
- **also catches Poor BSC bc=1 +659** that PORTUGAL strict MISSES (bc<16).

## Entry filter (decision at new-token-fire time)

```
IF token.chain == 'bsc'
   AND token.entry_signal.bonding_curve_buyers[0].addr == '0x85871aea93f086eeda5b4d0b5e32d31fc7fe46cc'
THEN paper_enter(size=$1, route_via='SNIPER_B')
```

**Full verified wallet address (42-char, this cycle)**: `0x85871aea93f086eeda5b4d0b5e32d31fc7fe46cc`.

**Routing rationale**: 5/5 in-corpus bigs from this wallet have SNIPER_B as best-fire stream. SNIPER_BSC_FILTERED hits ELON/CAP/MOODANG (small wins/rugs) — anti-fat-tail. SNIPER_B is the unambiguous best-fire stream for PORTUGAL family.

## Expected forward stats

Per walk-forward: n=5 expected fire every ~3-4 days (cadence 8 tokens / 51h), bigs ~60%, rugs ~12%, avg +352%. Realistic forward target: 1-2 fires/week, 1 big/week expected.

## Open risks
1. **Single-wallet alpha (Methodology #13)** — wallet alpha may saturate as wallet's strategy becomes known. Watch live cadence.
2. **n=8 corpus, n=5 walk-forward** — small. Methodology #13 effective floor would be n=40 for *generalized* version; #14 named-watch waives this.
3. **Mostly PORTUGAL strict overlap** — this stream redundantly fires with PAPER_BSC_PORTUGAL on 6/8 tokens. Distinct value: catches Poor BSC bc=1 +659 (PORTUGAL strict miss).
4. **Wallet addr might be a deployer-bot or relayer** — possible the wallet is not the trading entity but the LP-deploy bot for a hidden upstream insider. Either way, the wallet is the observable signal.
5. **Cross-cluster spread good** — C7/C8/C9/C10 all represented in wallet's 8 tokens, suggesting not single-block inflation (#11 safe).

## Forward monitoring plan
- Tag every fire to `paper_streams_log/PAPER_BSC_85871_WATCH.jsonl`.
- 7-day forward eval: K, big%, rug%.
- 14-day RESCIND if big%=0.
- If realized big%≥30% → REAL_MONEY proposal at size=$10.
- Cross-check live wallet behavior: any change in deploy cadence, k-distribution, dex preference is a regime-change signal.

## Brain note
Second named-wallet alpha after HUPHey. Together they:
- Provide cross-chain coverage (Sol + BSC).
- Break Methodology #13 single-entity restriction (HUPHey alone was 1 wallet; this is now 2 distinct entities each with own track record).
- Form basis for a "NAMED-WALLET WATCH CLASS" deployment tier — a new product category in the brain's strategy mix.

**Distance to deploy: READY** (per Methodology #14). User approval required.

# PAPER_SOL_HUPHEY_WATCH — Paper Stream Spec (cycle 20260525_0600)

**Status**: PROPOSED — pending user approval.
**Class**: NAMED-WALLET WATCH (Methodology #14 candidate — not a generalized filter).
**Risk**: paper, size=$1 per trade, ~$4/day expected exposure (~6h cadence).
**Promotion gate**: HUPHey-named alpha; bypasses standard n≥20 floor because:
- Methodology #13 (single-wallet inflation) prohibits deploying H_WALLET_TOP1 as a *generalized* prior-history filter,
- Methodology #14 (named-alpha vs generalized-filter) permits deploying a *named-wallet watch* when wallet has ≥3 bigs AND 0 rugs in own history.

## Entry filter (decision at new-token-fire time)

```
IF token.chain == 'solana'
   AND ( token.entry_signal.top1_owner == 'HUPHeyBkcSCkHTxS9wsbVcj9UP9wZNXU998g5Csbc9AT'
         OR token.entry_signal.lp_provider == 'D4BgpfCAEqYfoVVBdcokDovU5sXvhHXAYxwCn2ojPkHc' )
THEN paper_enter(size=$1, route_via='SNIPER_A')
```

**Routing rationale**: HUPHey bigs distribute across SNIPER_A/B/H/H2/MC_LIQ/SMART_TOP_AGE5 (best-fire varies per token). SNIPER_A captures 4/5 bigs at full or near-full cap. Smart-cluster (SMART_COPY/SMART_TOP) co-fires but has 1/5 catastrophic reversal (Poor +943 cap vs SMART -100 rug — 3rd reverse direction confirmed). Recommend SNIPER_A as primary route.

## Trail/exit
- Inherit SNIPER_A's existing trail logic (TP_500_CAP + ride exit).
- No custom exit.

## Expected stats (from in-corpus HUPHey aggregate)

- n = 12 unique tokens (current state.json rolling window ~05-23 10:50Z → 05-25 05:57Z)
- bigs (≥+150%) = 5 (42%)
- rugs (≤-90%) = 0 (0%)
- avg pnl = +195.2%
- K = 0.213
- geom@K = +29.75%/trade
- avg fat-tail magnitude (5 bigs): {506, 365, 481, 943, 175} = mean +494%

## HUPHey wallet timeline (full in-window)

| # | time UTC | symbol | pnl | top1 |
|---|---|---|---|---|
| 1 | 2026-05-23T10:50 | GDOR | -67.0 | 5 |
| 2 | 2026-05-23T12:29 | SPCX | +21.0 | 48.6 |
| 3 | 2026-05-23T14:45 | MTFR | -88.1 | 5 |
| 4 | 2026-05-23T16:32 | MTFR | -23.4 | 5 |
| 5 | 2026-05-23T19:36 | **MTFR** | **+506** | 87.8 |
| 6 | 2026-05-23T22:49 | MTFR | +19.2 | 87.8 |
| 7 | 2026-05-23T23:45 | **MTFR** | **+365** | 87.8 |
| 8 | 2026-05-24T11:39 | **Stake** | **+481** | 69 |
| 9 | 2026-05-24T14:49 | **Poor** | **+943** | 75 |
| 10 | 2026-05-24T18:45 | MTFR | -6.3 | 90 |
| 11 | 2026-05-24T21:14 | **MTFR** | **+175** | 90 |
| 12 | 2026-05-25T03:44 | $UGD | +16.0 | 78.4 |

Cadence: median ~3-4h, max ~12h, min ~1h. 5/12 = 42% big rate. **Rugless streak: 12/12 (0 rugs in 51h)**.

## Sub-filter (for stricter routing or descriptive monitoring)
HUPHey ∩ top1_pct ≥ 85 ∩ dex=meteora:
- n = 5 (MTFR-79y, MTFR-CFv (not big), MTFR-7Zx, MTFR-18:45 (not big), MTFR-BVB)
- Actually n=5 with bigs=3: MTFR-79y +506, MTFR-7Zx +365, MTFR-BVB +175
- K=1.0, geom=+144%/trade
- Use only as in-cycle audit; do not gate live entries (misses Stake +481 and Poor +943 which had top1=69/75).

## Open risks / known counter-examples
1. **Single-wallet alpha** — by Methodology #13, this signal does NOT generalize. Walk-forward on the *generalized* prior-history filter excluding HUPHey: n=8, 0 bigs, 3 rugs (37.5% rug — baseline). Filter is 100% HUPHey-specific.
2. **HUPHey identity unknown** — wallet behavior consistent with bot or insider sniping pump.fun migrations. Solscan deep-dive deferred.
3. **D4Bgpf overlap** — 13/15 D4Bgpf LP tokens are HUPHey-top1; remaining 2-3 are HLnpSz9h-top1 (launchpad service) with small wins, 0 bigs. Including D4Bgpf alone adds marginal coverage.
4. **Rotation risk** — earliest HUPHey entry GDOR-1 (10:03Z) already rotated. As more entries rotate, rolling K may decay.
5. **Wallet attack lifetime** — HUPHey-class wallets can become saturated (followers front-run, hype declines). Watch for big% drop over time.
6. **Counterfactual**: $UGD entered 03:44Z at +16% only — first non-big non-rug entry after a string of 6 bigs (Stake/Poor/MTFR-BVB/MTFR-18:45). Possible cooling.

## Forward monitoring plan
- Tag every fire from this stream in `paper_streams_log/PAPER_SOL_HUPHEY_WATCH.jsonl`.
- After 7 days of live forward: re-evaluate K, big%, rug%. If big%=0 over 14 days → RESCIND.
- If realized big%≥20% → propose REAL_MONEY at size=$10 (separate gate).
- Compare HUPHey forward fires vs HUPHey paper backtest (this corpus). Detect drift.

## Brain note
First *named-wallet* paper stream proposed by brain. Distinct deploy class from feature-based filters (PORTUGAL strict, TG-2h, BC_FULL_B). The +1M% path likely runs through multiple named-wallet alphas stacked — HUPHey is the first, BSC bc[0]=0x85871aea (cycle_0600 discovery) is the second candidate. Methodology #14 enables this deploy class.

# BRIEF — funding-rate (post-cycle 20260528_2300)

## ⛔ 23:00 UTC — AUDITED `OVERNIGHT_RESULTS_FINAL.md` → funding-only label leakage. DO NOT DEPLOY anything from its "DEPLOY PRIORITY" list.

A NEWER overnight artifact than cycle 1700's (`OVERNIGHT_RESULTS_FINAL.md`, 19:59 + Phase-C 21:34) carries an explicit **"🚀 DEPLOY PRIORITY"** list. ROOT CAUSE of all its "edges" (both today's audits converge): **the overnight pipeline's "PnL" = funding accumulation ONLY, ZERO price/delta term.**

```
/tmp/tick_universe.parquet (2.14M×26): NO price/spot/mark/close col exists.
  short_ret_N ≡ fwd_cum_N (Σ next-N funding) ; long_ret_N ≡ −fwd_cum_N (corr 1.0, np.allclose True)
  → long_ret=−short_ret ZERO-SUM → side aligned with funding sign is +PnL BY CONSTRUCTION.
HIGH-RATE-STABLE-SHORT (rate≥12bp & std_24≤1bp): n=48,446 short_ret_24 +286.4bp/WR100%/min+84bp
  ≈ rate×24=+288bp = literal tautology. Phase-C "v2 24h +288bp/Sh30/min+270bp" = same, longer horizon.
H_BORROW_SQUEEZE: val_borrow.py:12 long_perp_24h_pct=−fwd_24h_cum*100 (funding-only, no price col).
  reproduced +6.90%/WR84.7% (BLUR+25.62/ENSO+19.26/KAT+12.89 all 100%).
```

**Why fake:** holding the perp to collect funding = full price risk (H37: |drift|≫|funding|, sign flips); delta-hedge → basis≈funding → net≈0 = naive funding harvest (CONFIRMED NEG −$304/315). **H_BORROW_SQUEEZE CONTRADICTS R16** (cycle 1750: LONG post-borrow-spike by PRICE = −2.8%/4h WR32%) — overnight flips the sign by deleting the price term. R16 STANDS. 8 STRICT event-grid = already rejected cycle 1700. TG-practitioner = report's own 24h −0.20% (not-an-edge).

## 3-EDGE PORTFOLIO — UNCHANGED (these survive precisely because they carry price klines + a hedge leg)
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129
```
Sub-tiers (forward-obs/draft, NOT deployed): H38_QUALITY, H_COMBO_3c_QUALITY, H_COMBO_STACKED, H34_QUALITY_RANK1 (see backlog).

## METHODOLOGY COUNTS
#21–#28 ✓ ; #29 cand(1/2) ; #30 cand(1/2) ; **#31 cand(1/2 NEW)**.
**#31 (NEW):** funding-only PnL labels are tautological (Σ forward funding / −fwd_cum, no price col → WR→100%/Sharpe→∞ for any funding-sign filter). Gate overnight/mega outputs: (a) price/mark col in PnL, (b) hedge leg w/ cost, (c) WR≥99% or never-neg-min across thousands ⇒ suspect tautology. Pairs with #30 as the two leakage gates on the overnight machinery.

## PAPER BOTS (unchanged this cycle — audit was the single task)
`paper_fairprice_v6 n=66 +12.31 WR83.3%` (Meth #28 bimodality persists) ; `paper_new_symbol n=18 −13.83 WR22.2%` (R3 replay; USER DECISION pending).

## NEXT-CYCLE PRIORITIES
1. Meth #29 corroboration #2 — mean-rev-to-anchor unimodality (H3 PYUSD n=24 cycle 1132, or USDC-only) (~15 min). Top open candidate (deferred 2 cycles for audits).
2. paper_new_symbol DECISION — escalate to user (n=18 losing, replaying rejected R3).
3. paper_fairprice_v6 60s-cutoff USER OK ASK — backed by Meth #26+#28+#29.
4. (opt) Meth #31/#30 corrob #2 — attach price series to an overnight tick "edge", confirm collapse; or never-touched-holdout on H34 mega-grid.
5. H_BOROS_INDICATOR — DEFERRED 20 cycles, USER DECISION REQUIRED.

## STOP / DO NOT
- **NEW: do NOT deploy ANY `OVERNIGHT_RESULTS_FINAL.md` "DEPLOY PRIORITY" item (H_BORROW_SQUEEZE, HIGH-RATE-STABLE-SHORT v1/v2, EVENT-GRID STRICT) — funding-only tautologies; H_BORROW_SQUEEZE also contradicts R16. Treat ANY funding-only-label result as a non-edge on sight (Meth #31).**
- Do NOT re-open C9/R16 borrow-spike except with PRICE-inclusive (ideally delta-neutral) PnL — R16 already did, rejected.
- Do NOT deploy cycle-1700 megasearch "STRICT edges" (Meth #30). Import a rejected variant's discriminator onto a validated variant (Meth #26); H_COMBO_3 SCALER form; Unhedged/Sign-flip SHORT (R13/R24); ≥5-min hold on fairprice_v6; nano-cap gate on basis H31.

## DATA / TG / GIT
- Read-only this cycle: OVERNIGHT_RESULTS_FINAL.md, /tmp/tick_universe.parquet (2.14M×26), val_tick.py, val_borrow.py, pillar4_v2_borrow_results.parquet (n=85). No writes. NOT touched: shared/deep_dive_overnight.py, shared/overnight_megasearch.py (onchain).
- feed_funding 7. H_TG_ROUTING_PATCH pending USER OK. VPS git push may fail (credential helper unset).

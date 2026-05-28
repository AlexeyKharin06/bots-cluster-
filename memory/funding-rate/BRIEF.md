# BRIEF — funding-rate (post-cycle 20260528_1700)

## ⚠️ 17:00 UTC — AUDITED the overnight megasearch → NO new edge. DO NOT DEPLOY its "8 STRICT edges".

A new artifact `OVERNIGHT_RESULTS.md` (22.7M filters, 8 STRICT edges n=18-20 / +1.87-2.18% / 100% WR / Sharpe 3.5-4.3, recommends "deploy top-3 in parallel for diversification"). Audited it (`/tmp/mega_audit.py`, read-only). It is a **rediscovery of the already-validated H34 + multiple-testing overfit**, not new edges.

```
"554-event universe" misleading: A/B/C_net_h34 (only tradeable streams) = n=101 = the SAME validated H34 events.
Baseline A_net_h34 reproduces EXACT validated H34: +1.438%/WR81.2%/Sh0.82 (19 losers/82 winners).
8 STRICT edges = 100%-WR pockets carved by dodging the 19 known losers.
DIVERSIFICATION FALSE: union of all 8 = 35 events, mean pairwise Jaccard 0.54 (max 1.00, #6/#7 identical),
  all winners by construction → ONE shared risk bucket. A≈B stream. 74% ⊆ rank==1 tier (=H34_QUALITY_RANK1 draft).
PERMUTATION NULL (decisive): same pipeline on SHUFFLED PnL → median 68 "STRICT-WF-validated" filters from noise
  (max 392); real=520. Walk-forward-as-selection = ZERO OOS protection. Regime: H34 stable TRAIN+1.46/TEST+1.40.
```

**RECOMMENDATION: do NOT deploy the megasearch edges. H34 paper-stream spec UNCHANGED.** Salvage: survivor features (div_vs_*, rate_Tm6h, rank dominate) corroborate Meth #24 (perp-perp ← dispersion). NOTE: committed `shared/overnight_megasearch.py` is the ONCHAIN script (not ours) — untouched.

## 3-EDGE PORTFOLIO — UNCHANGED
```
H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101
H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129
```
Sub-tiers (forward-obs/draft, NOT deployed): H38_QUALITY +2.84/99/~2.0/1554; H_COMBO_3c_QUALITY +4.18/100/2.17/40; H_COMBO_STACKED +4.64/100/2.31/28; H34_QUALITY_RANK1 +1.76/86/0.94/63 (the tier the megasearch re-found).

## METHODOLOGY COUNTS
#21✓ #22✓ #24✓CONFIRMED #25✓ #26✓CONFIRMED #27→folds-into-#24/#26 #28✓ #29 candidate(1/2 untouched) **#30 candidate(1/2 NEW)**.
**#30 (NEW):** walk-forward applied as a SELECTION filter across millions of candidates gives NO OOS protection (null floor 68 "validated" filters on shuffled H34 PnL). Validate mega-grids via never-touched holdout OR permutation-null FDR; drop outcome cols (funding_recv_*) from predicates; report Jaccard before claiming diversification.

## PAPER BOTS
```
paper_fairprice_v6 n=66 (+1; not analyzed in depth this cycle). Meth #28 sub-60s/≥60s bimodality persists.
paper_new_symbol   n=18 (+1, still losing) — R3 listing-momentum replay. USER DECISION pending (pause/redesign).
```

## NEXT-CYCLE PRIORITIES
1. **Meth #29 corroboration #2** — 2nd mean-rev-to-anchor unimodality (H3 PYUSD n=24 cycle 1132, or USDC-only) (~15 min). Top open methodology candidate (deferred 1 cycle for the audit).
2. **paper_new_symbol DECISION** — escalate to user (n=18 losing, replaying rejected R3).
3. **paper_fairprice_v6 60s-cutoff USER OK ASK** — backed by Meth #26+#28 CONFIRMED + #29 boundary.
4. **(optional) Meth #30 corroboration #2** — apply never-touched-holdout protocol to the H34 mega-grid; confirm the 8 STRICT edges collapse OOS.
5. **H_BOROS_INDICATOR** — DEFERRED 19 cycles, USER DECISION REQUIRED.

## STOP / DO NOT
- **NEW: do NOT deploy the megasearch "STRICT edges" as paper-streams (rediscovery of H34 + overfit; 35-event single bucket, not 3 streams). Future megasearch outputs are HYPOTHESES not edges until a never-touched holdout or permutation-null FDR clears them.**
- Import a rejected variant's discriminator onto a validated variant, or H_COMBO_3c n_neg_50 onto H34 perp-perp (use rank/dispersion only) — Meth #26/#24.
- Extend paper_fairprice_v6 to ≥5-min hold; apply Meth #28 hold-cutoff to mean-rev (H3, Meth #29). H_COMBO_3 SCALER form, Unhedged/Sign-flip SHORT primary (R13/R24), nano-cap gate on basis H31.

## DATA / TG / GIT
- /tmp/mega_audit.py (this cycle); inputs /tmp/mega_universe.parquet (554×70, A/B/C_net_h34 n=101), /tmp/p2_megagrid.py, /tmp/mega3.py. feed_funding 7. H_TG_ROUTING_PATCH pending USER OK (18-cycle). VPS git push may fail (credential helper unset).

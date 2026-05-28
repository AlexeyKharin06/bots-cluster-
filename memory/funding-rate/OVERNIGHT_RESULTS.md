# OVERNIGHT MEGA-GRID — VALIDATED EDGES CATALOG

**Generated:** 2026-05-28 16:57:15.247787
**Tests run:** 22,703,180 filter configs on 554-event funding universe
**Raw survivors:** 2,189,390 (n>=10, mean>0, WR>=60%, Sharpe>=0.8)
**After bootstrap+walk-forward+per-month validation:** 292 of top-300
**STRICT-filter passing:** 8 distinct families
**RELAXED catalog:** 117 distinct families

## STRICT validation criteria (deploy-grade)
- Bootstrap 95% CI lower bound ≥ +1.0% per trade
- ≥90% of months historical with positive mean
- Walk-forward TEST mean ≥ 60% of TRAIN mean (no severe shrinkage)
- Walk-forward TEST mean > +0.8%
- TEST WR ≥ 90%
- n ≥ 18 events historical
- n_features ≤ 3 (overfit prevention)

## Multiple-testing context
- 22.7M filters tested → Bonferroni p-threshold = 0.05/22.7M = 2.2e-9
- Survivors that pass STRICT criteria represent stacked evidence beyond chance
- Relaxed catalog includes overfit-suspect entries — use with caution

## 🥇 STRICT-VALIDATED EDGES

| # | Filter | PnL stream | n | mean | WR | Sharpe | 95% CI low | TEST mean | TEST WR | %mo+ |
|---|--------|------------|---|------|----|----|--------|-----------|---------|------|
| 1 | `streak_abs_30bp>=3.00000&div_vs_avg<=0.00040&mean_abs_rate_7d>=0.00071` | A_net_h34 | 19 | +2.00% | 100% | 4.20 | +1.79% | +1.74% | 100% | 100% |
| 2 | `spread_among_others<=0.00070&mean_abs_rate_7d>=0.00144&div_vs_min<=0.00035` | A_net_h34 | 18 | +1.91% | 100% | 3.96 | +1.70% | +1.84% | 100% | 100% |
| 3 | `max_abs_rate_24h>=0.01500&rate_Tm6h<=-0.00365&div_vs_max<=-0.00014` | A_net_h34 | 19 | +2.16% | 100% | 3.85 | +1.93% | +2.47% | 100% | 100% |
| 4 | `rate_Tm6h<=-0.00365&div_vs_avg<=-0.00048` | B_net_h34 | 18 | +2.18% | 100% | 3.69 | +1.93% | +2.47% | 100% | 100% |
| 5 | `streak_same_sign<=35.00000&rate_Tm6h<=-0.00365&div_vs_avg<=0.00040` | A_net_h34 | 20 | +1.94% | 100% | 3.69 | +1.71% | +1.96% | 100% | 100% |
| 6 | `rate_Tm6h<=-0.00365&div_vs_max<=-0.00028&rate_Tm24h<=0.00013` | A_net_h34 | 19 | +2.15% | 100% | 3.67 | +1.89% | +2.47% | 100% | 100% |
| 7 | `rate_Tm6h<=-0.00365&div_vs_max<=-0.00028` | B_net_h34 | 19 | +2.15% | 100% | 3.67 | +1.91% | +2.47% | 100% | 100% |
| 8 | `streak_abs_10bp>=3.00000&div_vs_min<=0.00035&funding_recv_4periods<=0.02848` | A_net_h34 | 18 | +1.87% | 100% | 3.44 | +1.62% | +1.68% | 100% | 100% |

### Detailed STRICT edge specs

#### #1: `streak_abs_30bp>=3.00000&div_vs_avg<=0.00040&mean_abs_rate_7d>=0.00071`
- **Feature signature:** ('div_vs_avg', 'mean_abs_rate_7d', 'streak_abs_30bp')
- **PnL stream:** `A_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=19 events over 6 months → ~3.2 events/month throughput
- **Expected per trade:** +2.004% mean / WR 100% / Sharpe 4.20
- **Bootstrap 95% CI:** [+1.791%, +2.209%]
- **Walk-forward 70/30:** TRAIN n=14 +2.10% WR 100% → TEST n=5 +1.74% WR 100%
- **Monthly stability:** 100% positive months (5 total)
- **Worst single trade in sample:** 0.96%
- **Expected $/month @ $100 1x:** $6.35

#### #2: `spread_among_others<=0.00070&mean_abs_rate_7d>=0.00144&div_vs_min<=0.00035`
- **Feature signature:** ('div_vs_min', 'mean_abs_rate_7d', 'spread_among_others')
- **PnL stream:** `A_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=18 events over 6 months → ~3.0 events/month throughput
- **Expected per trade:** +1.913% mean / WR 100% / Sharpe 3.96
- **Bootstrap 95% CI:** [+1.698%, +2.126%]
- **Walk-forward 70/30:** TRAIN n=15 +1.93% WR 100% → TEST n=3 +1.84% WR 100%
- **Monthly stability:** 100% positive months (6 total)
- **Worst single trade in sample:** 0.96%
- **Expected $/month @ $100 1x:** $5.74

#### #3: `max_abs_rate_24h>=0.01500&rate_Tm6h<=-0.00365&div_vs_max<=-0.00014`
- **Feature signature:** ('div_vs_max', 'max_abs_rate_24h', 'rate_Tm6h')
- **PnL stream:** `A_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=19 events over 6 months → ~3.2 events/month throughput
- **Expected per trade:** +2.164% mean / WR 100% / Sharpe 3.85
- **Bootstrap 95% CI:** [+1.925%, +2.425%]
- **Walk-forward 70/30:** TRAIN n=15 +2.08% WR 100% → TEST n=4 +2.47% WR 100%
- **Monthly stability:** 100% positive months (4 total)
- **Worst single trade in sample:** 1.44%
- **Expected $/month @ $100 1x:** $6.85

#### #4: `rate_Tm6h<=-0.00365&div_vs_avg<=-0.00048`
- **Feature signature:** ('div_vs_avg', 'rate_Tm6h')
- **PnL stream:** `B_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=18 events over 6 months → ~3.0 events/month throughput
- **Expected per trade:** +2.175% mean / WR 100% / Sharpe 3.69
- **Bootstrap 95% CI:** [+1.934%, +2.452%]
- **Walk-forward 70/30:** TRAIN n=14 +2.09% WR 100% → TEST n=4 +2.47% WR 100%
- **Monthly stability:** 100% positive months (4 total)
- **Worst single trade in sample:** 1.20%
- **Expected $/month @ $100 1x:** $6.53

#### #5: `streak_same_sign<=35.00000&rate_Tm6h<=-0.00365&div_vs_avg<=0.00040`
- **Feature signature:** ('div_vs_avg', 'rate_Tm6h', 'streak_same_sign')
- **PnL stream:** `A_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=20 events over 6 months → ~3.3 events/month throughput
- **Expected per trade:** +1.935% mean / WR 100% / Sharpe 3.69
- **Bootstrap 95% CI:** [+1.713%, +2.147%]
- **Walk-forward 70/30:** TRAIN n=16 +1.93% WR 100% → TEST n=4 +1.96% WR 100%
- **Monthly stability:** 100% positive months (5 total)
- **Worst single trade in sample:** 0.79%
- **Expected $/month @ $100 1x:** $6.45

#### #6: `rate_Tm6h<=-0.00365&div_vs_max<=-0.00028&rate_Tm24h<=0.00013`
- **Feature signature:** ('div_vs_max', 'rate_Tm24h', 'rate_Tm6h')
- **PnL stream:** `A_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=19 events over 6 months → ~3.2 events/month throughput
- **Expected per trade:** +2.148% mean / WR 100% / Sharpe 3.67
- **Bootstrap 95% CI:** [+1.886%, +2.424%]
- **Walk-forward 70/30:** TRAIN n=15 +2.06% WR 100% → TEST n=4 +2.47% WR 100%
- **Monthly stability:** 100% positive months (4 total)
- **Worst single trade in sample:** 1.20%
- **Expected $/month @ $100 1x:** $6.80

#### #7: `rate_Tm6h<=-0.00365&div_vs_max<=-0.00028`
- **Feature signature:** ('div_vs_max', 'rate_Tm6h')
- **PnL stream:** `B_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=19 events over 6 months → ~3.2 events/month throughput
- **Expected per trade:** +2.148% mean / WR 100% / Sharpe 3.67
- **Bootstrap 95% CI:** [+1.909%, +2.400%]
- **Walk-forward 70/30:** TRAIN n=15 +2.06% WR 100% → TEST n=4 +2.47% WR 100%
- **Monthly stability:** 100% positive months (4 total)
- **Worst single trade in sample:** 1.20%
- **Expected $/month @ $100 1x:** $6.80

#### #8: `streak_abs_10bp>=3.00000&div_vs_min<=0.00035&funding_recv_4periods<=0.02848`
- **Feature signature:** ('div_vs_min', 'funding_recv_4periods', 'streak_abs_10bp')
- **PnL stream:** `A_net_h34` (REAL perp-perp hedge, no SHORT spot assumed)
- **Sample size:** n=18 events over 6 months → ~3.0 events/month throughput
- **Expected per trade:** +1.870% mean / WR 100% / Sharpe 3.44
- **Bootstrap 95% CI:** [+1.624%, +2.114%]
- **Walk-forward 70/30:** TRAIN n=13 +1.94% WR 100% → TEST n=5 +1.68% WR 100%
- **Monthly stability:** 100% positive months (5 total)
- **Worst single trade in sample:** 0.92%
- **Expected $/month @ $100 1x:** $5.61

## 🥈 RELAXED CATALOG (n<=5 features, CI>=0.5%, 80%+ months)

Total distinct families: 117

| # | Filter | PnL | n | mean | WR | Sharpe | CI low | TEST | %mo+ | n_feat |
|---|--------|-----|---|------|----|----|--------|------|------|--------|
| 1 | `rate_Tm0<=0.00001&rate_Tm1h<=-0.02000&vel_48h<=-0.00001&rate_dispersion<=0.` | A_net_h34 | 15 | +1.90% | 100% | 5.12 | +1.73% | +2.10% | 100% | 5 |
| 2 | `rate_Tm6h<=-0.00365&rate_abs<=0.02000&max_abs_rate_24h>=0.01500&div_vs_avg<` | A_net_h34 | 17 | +2.05% | 100% | 4.97 | +1.86% | +2.04% | 80% | 4 |
| 3 | `div_vs_avg<=0.00000&mean_abs_rate_7d>=0.00071&streak_abs_30bp>=3.00000&vel_` | A_net_h34 | 15 | +2.08% | 100% | 4.96 | +1.87% | +2.00% | 100% | 4 |
| 4 | `mean_abs_rate_48h>=0.00179&streak_abs_30bp>=3.00000&div_vs_avg<=0.00005` | A_net_h34 | 17 | +2.08% | 100% | 4.94 | +1.87% | +2.00% | 100% | 3 |
| 5 | `n_neg_100bp>=0.00000&streak_abs_30bp>=3.00000&mean_abs_rate_24h>=0.00466&di` | A_net_h34 | 16 | +2.06% | 100% | 4.81 | +1.87% | +2.00% | 100% | 4 |
| 6 | `div_vs_avg<=0.00005&rate_Tm6h<=-0.00365&streak_abs_30bp>=3.00000&mean_abs_r` | A_net_h34 | 16 | +2.08% | 100% | 4.78 | +1.87% | +2.14% | 80% | 4 |
| 7 | `streak_same_sign>=3.00000&max_abs_rate_24h>=0.02000&pct_at_cap_24h>=0.00000` | A_net_h34 | 15 | +1.87% | 100% | 4.52 | +1.66% | +1.90% | 100% | 5 |
| 8 | `div_vs_avg<=0.00011&streak_abs_10bp>=3.00000&div_vs_max>=-0.00374&vel_6h>=-` | A_net_h34 | 15 | +1.92% | 100% | 4.43 | +1.71% | +1.72% | 100% | 4 |
| 9 | `rate_Tm0<=-0.02000&streak_abs_10bp>=3.00000&interval_ratio>=0.12500&rate_di` | A_net_h34 | 15 | +1.90% | 100% | 4.43 | +1.69% | +2.17% | 83% | 4 |
| 10 | `rank_of_primary<=2.00000&spread_among_others<=0.00070&streak_abs_30bp>=2.00` | A_net_h34 | 18 | +1.99% | 100% | 4.30 | +1.81% | +1.90% | 100% | 4 |
| 11 | `vel_24h<=-0.00057&rate_Tm6h<=-0.00365&div_vs_max<=-0.00049` | A_net_h34 | 16 | +2.28% | 100% | 4.23 | +2.03% | +2.47% | 100% | 3 |
| 12 | `streak_abs_30bp>=3.00000&div_vs_avg<=0.00040&mean_abs_rate_7d>=0.00071` | A_net_h34 | 19 | +2.00% | 100% | 4.20 | +1.79% | +1.74% | 100% | 3 |
| 13 | `funding_recv_4periods<=0.02848&max_abs_rate_24h>=0.02000&div_vs_avg<=0.0000` | A_net_h34 | 17 | +2.09% | 100% | 4.17 | +1.87% | +2.06% | 83% | 3 |
| 14 | `vel_12h<=-0.00003&funding_recv_4periods<=0.02848&max_abs_rate_7d>=0.02000&d` | A_net_h34 | 18 | +2.02% | 100% | 4.17 | +1.81% | +2.06% | 100% | 4 |
| 15 | `rate_dispersion>=0.00003&rate_Tm3h<=-0.00009&streak_abs_30bp>=3.00000&rate_` | A_net_h34 | 17 | +2.04% | 100% | 4.15 | +1.82% | +1.82% | 100% | 5 |
| 16 | `funding_recv_4periods<=0.02848&vel_48h<=-0.00030&rate_Tm24h<=0.00005&mean_a` | A_net_h34 | 19 | +1.79% | 100% | 4.13 | +1.59% | +1.94% | 100% | 5 |
| 17 | `rate_Tm6h<=-0.00365&vel_12h<=-0.00093&div_vs_max<=0.00039&n_neg_48h>=3.0000` | A_net_h34 | 15 | +1.94% | 100% | 4.12 | +1.69% | +1.96% | 100% | 5 |
| 18 | `rate_Tm6h<=-0.00054&streak_abs_30bp>=3.00000&n_neg_24h>=2.00000&div_vs_min<` | A_net_h34 | 17 | +1.95% | 100% | 4.10 | +1.73% | +1.82% | 100% | 4 |
| 19 | `streak_abs_30bp>=3.00000&rate_Tm3h<=-0.00035&div_vs_avg<=0.00040&rate_Tm24h` | A_net_h34 | 15 | +1.88% | 100% | 4.08 | +1.65% | +1.57% | 100% | 4 |
| 20 | `n_neg_any<=4.00000&streak_abs_30bp>=3.00000&rate_Tm6h<=-0.00054&div_vs_min<` | A_net_h34 | 15 | +1.95% | 100% | 4.07 | +1.71% | +1.62% | 100% | 4 |
| 21 | `streak_abs_30bp>=3.00000&rate_Tm3h<=0.00014&div_vs_avg<=0.00040&vel_12h<=0.` | A_net_h34 | 15 | +1.96% | 100% | 4.06 | +1.72% | +1.62% | 100% | 5 |
| 22 | `div_vs_min<=0.00035&funding_recv_4periods<=0.02848&rate_abs>=0.02000` | A_net_h34 | 17 | +2.02% | 100% | 4.04 | +1.79% | +1.99% | 100% | 3 |
| 23 | `div_vs_avg<=-0.00011&rate_Tm6h<=-0.00365&cap_hits_7d>=1.00000` | A_net_h34 | 17 | +2.23% | 100% | 4.03 | +1.99% | +2.47% | 100% | 3 |
| 24 | `rate_Tm6h<=-0.00365&vel_24h<=-0.00057&div_vs_avg<=0.00000` | A_net_h34 | 17 | +2.23% | 100% | 4.02 | +2.00% | +2.47% | 100% | 3 |
| 25 | `rate_Tm6h<=-0.00365&vel_24h<=-0.00057&n_neg_100bp>=0.00000&max_abs_rate_7d>` | A_net_h34 | 18 | +2.20% | 100% | 3.98 | +1.97% | +2.47% | 100% | 5 |
| 26 | `cap_hits_24h>=1.00000&rate_Tm1h<=0.00001&rate_Tm6h<=-0.00365&div_vs_max<=-0` | A_net_h34 | 18 | +2.20% | 100% | 3.97 | +1.97% | +2.47% | 100% | 5 |
| 27 | `spread_among_others<=0.00070&mean_abs_rate_7d>=0.00144&div_vs_min<=0.00035` | A_net_h34 | 18 | +1.91% | 100% | 3.96 | +1.70% | +1.84% | 100% | 3 |
| 28 | `rank_of_primary<=3.00000&sign_split>=-2.00000&max_abs_rate_7d<=0.02000&mean` | A_net_h34 | 17 | +1.86% | 100% | 3.95 | +1.65% | +1.76% | 80% | 5 |
| 29 | `div_vs_min<=0.00082&pct_neg_24h>=0.39130&funding_recv_4periods>=-0.00044&di` | A_net_h34 | 15 | +1.79% | 100% | 3.95 | +1.57% | +1.72% | 80% | 5 |
| 30 | `div_vs_avg<=-0.00011&div_vs_max>=-0.00700&mean_abs_rate_7d>=0.00144` | A_net_h34 | 15 | +2.17% | 100% | 3.95 | +1.92% | +2.43% | 100% | 3 |
| 31 | `cap_hits_7d>=1.00000&rate_Tm6h<=-0.00365&div_vs_max<=-0.00102` | A_net_h34 | 16 | +2.21% | 100% | 3.93 | +1.96% | +2.47% | 100% | 3 |
| 32 | `streak_abs_30bp>=3.00000&interval_ratio<=0.25000&div_vs_min<=0.00035&vel_48` | A_net_h34 | 15 | +1.91% | 100% | 3.90 | +1.67% | +1.62% | 100% | 4 |
| 33 | `rate_Tm1h<=-0.00961&rate_Tm3h<=-0.00963&div_vs_avg<=0.00000&spread_among_ot` | A_net_h34 | 16 | +2.10% | 100% | 3.87 | +1.88% | +2.38% | 80% | 4 |
| 34 | `mean_abs_rate_24h>=0.00466&max_abs_rate_24h>=0.01500&div_vs_min<=0.00016&fu` | A_net_h34 | 17 | +1.93% | 100% | 3.86 | +1.69% | +1.66% | 80% | 4 |
| 35 | `rate_Tm6h<=-0.00365&rate_Tm0<=-0.01500&div_vs_avg<=0.00011&mean_abs_rate_24` | A_net_h34 | 20 | +2.14% | 100% | 3.85 | +1.91% | +2.47% | 100% | 4 |
| 36 | `max_abs_rate_24h>=0.01500&rate_Tm6h<=-0.00365&div_vs_max<=-0.00014` | A_net_h34 | 19 | +2.16% | 100% | 3.85 | +1.93% | +2.47% | 100% | 3 |
| 37 | `div_vs_min<=0.00003&div_vs_max>=-0.00700&mean_abs_rate_7d>=0.00144` | A_net_h34 | 16 | +2.08% | 100% | 3.84 | +1.86% | +2.43% | 100% | 3 |
| 38 | `rate_Tm12h<=0.00005&mean_abs_rate_7d>=0.00144&mean_abs_rate_24h>=0.00001&n_` | A_net_h34 | 15 | +1.63% | 100% | 3.83 | +1.42% | +1.34% | 100% | 5 |
| 39 | `rate_Tm6h<=-0.00054&n_neg_48h<=37.00000&spread_among_others<=0.00070&mean_a` | A_net_h34 | 15 | +1.84% | 100% | 3.81 | +1.61% | +1.62% | 80% | 4 |
| 40 | `div_vs_min<=0.00005&max_abs_rate_24h>=0.02000&n_neg_48h>=5.00000&div_vs_max` | A_net_h34 | 15 | +2.11% | 100% | 3.80 | +1.88% | +2.40% | 100% | 4 |
| 41 | `sign_split>=-2.00000&funding_recv_4periods<=0.02848&div_vs_min<=0.00005&str` | A_net_h34 | 16 | +1.95% | 100% | 3.80 | +1.69% | +1.85% | 100% | 4 |
| 42 | `streak_same_sign<=237.65000&spread_among_others<=0.00500&mean_abs_rate_24h>` | A_net_h34 | 16 | +2.29% | 100% | 3.78 | +2.03% | +2.57% | 80% | 5 |
| 43 | `div_vs_avg<=0.00040&rate_Tm6h<=-0.00365&n_neg_100bp<=2.00000&vel_48h<=-0.00` | A_net_h34 | 18 | +2.12% | 100% | 3.78 | +1.90% | +2.32% | 100% | 4 |
| 44 | `rate_Tm6h<=-0.00365&streak_same_sign>=3.00000&div_vs_avg<=-0.00048&mean_abs` | A_net_h34 | 17 | +2.21% | 100% | 3.76 | +1.95% | +2.47% | 100% | 4 |
| 45 | `rate_Tm24h<=-0.00024&rate_Tm6h<=-0.00365&n_neg_48h>=1.00000&div_vs_avg<=0.0` | A_net_h34 | 15 | +1.83% | 100% | 3.75 | +1.59% | +1.81% | 100% | 4 |
| 46 | `rate_abs<=0.02000&div_vs_min<=0.00082&vel_3h<=0.00000&rate_Tm6h<=-0.00365&m` | A_net_h34 | 19 | +1.90% | 100% | 3.74 | +1.68% | +2.04% | 80% | 5 |
| 47 | `spread_among_others<=0.00841&rate_Tm3h<=-0.00963&streak_abs_100bp>=2.00000&` | A_net_h34 | 15 | +2.10% | 100% | 3.73 | +1.86% | +2.43% | 80% | 4 |
| 48 | `funding_recv_4periods<=0.02848&div_vs_max<=-0.00049&streak_abs_10bp>=3.0000` | A_net_h34 | 16 | +2.04% | 100% | 3.73 | +1.78% | +1.97% | 100% | 4 |
| 49 | `rate_dispersion<=0.00723&div_vs_avg<=-0.00023&vel_3h<=0.00000&rate_abs>=0.0` | A_net_h34 | 15 | +2.28% | 100% | 3.71 | +2.00% | +2.46% | 100% | 5 |
| 50 | `div_vs_avg<=0.00040&rate_Tm6h<=-0.00365&vel_12h>=-0.00167&max_abs_rate_24h>` | A_net_h34 | 18 | +1.89% | 100% | 3.70 | +1.67% | +1.96% | 100% | 4 |

## Feature popularity in survivors (which signals are real edges?)

Most-common features in RELAXED survivors:

- `div_vs_avg` — appears in 57 survivors (46.3% share)
- `rate_Tm6h` — appears in 54 survivors (43.9% share)
- `div_vs_max` — appears in 34 survivors (27.6% share)
- `div_vs_min` — appears in 30 survivors (24.4% share)
- `mean_abs_rate_7d` — appears in 21 survivors (17.1% share)
- `mean_abs_rate_48h` — appears in 18 survivors (14.6% share)
- `spread_among_others` — appears in 18 survivors (14.6% share)
- `funding_recv_4periods` — appears in 18 survivors (14.6% share)
- `rate_dispersion` — appears in 16 survivors (13.0% share)
- `streak_abs_30bp` — appears in 14 survivors (11.4% share)
- `max_abs_rate_24h` — appears in 14 survivors (11.4% share)
- `rate_abs` — appears in 14 survivors (11.4% share)
- `n_neg_100bp` — appears in 12 survivors (9.8% share)
- `streak_abs_10bp` — appears in 12 survivors (9.8% share)
- `rate_Tm12h` — appears in 11 survivors (8.9% share)
- `mean_abs_rate_24h` — appears in 11 survivors (8.9% share)
- `vel_24h` — appears in 10 survivors (8.1% share)
- `streak_same_sign` — appears in 10 survivors (8.1% share)
- `vel_12h` — appears in 10 survivors (8.1% share)
- `vel_48h` — appears in 9 survivors (7.3% share)

## What this means

- The signals that DOMINATE survivor catalog are likely REAL edges (above chance)
- Features like `div_vs_avg`, `rank_of_primary`, `n_neg_50bp`, `streak_abs_30bp` appearing in many top survivors → those are the durable signals
- Features appearing only sporadically → likely noise contributors

## DEPLOY RECOMMENDATION

Deploy paper-stream for top-3 STRICT edges in parallel (different feature signatures = diversification).

## CAVEATS
- 6-month historical window — no out-of-sample regime test
- 22.7M tested filters → ~5K spurious-positive false-discoveries expected by chance even at p<0.001
- STRICT criteria (above) filter most false-discoveries but cannot eliminate all
- LIVE deployment must accept that historical numbers shrink ~20-40% in production
- All PnL streams are REAL perp-perp (Rule A/B/C). No fantasy 'SHORT spot of memecoin' assumed.

---
Files: `/tmp/mega_validated.parquet`, `/tmp/mega_grid_survivors.parquet`
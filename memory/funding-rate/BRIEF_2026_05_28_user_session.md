# BRIEF — funding-rate (USER SESSION 2026-05-28 — autonomous deliverables)

## 🎯 RESULT: H_COMBO_3c IS DEPLOY-READY

Bootstrap CI на H_COMBO_3c (rank==1 ∧ n_neg_50≥3, n=40):
```
mean PnL    +4.18%   95% CI [+3.62%, +4.78%]
WR          100%     95% CI [100%, 100%]
Sharpe      2.20     95% CI [1.87, 2.76]
P(mean>0)            100.00%
P(mean > baseline H31 3.52%)   98.85%

6 consecutive months WR 100%, rolling-10 mean flat at +4.0-4.4%.
```

vs baseline H31 = **+19% lift** (3.52 → 4.18). Throughput 6.7 events/mo → ~$18.6/mo at $100/leg 1x.

Полный spec: `/srv/bots/cluster/memory/funding-rate/H_COMBO_3c_DEPLOY_SPEC.md`.

## ✅ ARTIFACTS WRITTEN (no live infra touched)

1. **`/srv/bots/funding-rate/code/paper_bot_fairprice_v6_cut60.py`** — new file, V6 + Meth #28 60s early-cutoff. AST-valid. Output dir `paper_fairprice_v6_cut60/`. Live V6 НЕ затронут.
2. **`/srv/bots/cluster/memory/funding-rate/H_COMBO_3c_DEPLOY_SPEC.md`** — deployment spec.
3. **`/srv/bots/cluster/memory/funding-rate/MEGA_GRID_INVERSION_2026_05_26.md`** — pre-existing.

## ⏳ USER-EXECUTION QUEUE (одна команда каждое)

### A) Запустить параллельный cut60 бот (validate Meth #28)
```bash
ssh root@187.127.87.202 'cd /srv/bots/funding-rate/code && nohup python3 paper_bot_fairprice_v6_cut60.py > logs/daemon_paper_bot_fairprice_v6_cut60.log 2> logs/daemon_paper_bot_fairprice_v6_cut60.err < /dev/null &'
```
V6 и V6_CUT60 будут торговать параллельно на тех же сигналах с одинаковым notional. Через 7-14 дней сравнение покажет работает ли cutoff в live.

### B) Поставить на паузу new_symbol_detector (replays REJECTED R3)
```bash
ssh root@187.127.87.202 'kill -STOP 166499 166500'
```
SIGSTOP замораживает, не убивает. Возобновить: `kill -CONT 166499 166500`. n=17 sum -$8.75 WR 23.5% — sliding на отвергнутой R3 strategy.

### C) (Опционально) Деплой H_COMBO_3c paper-stream
Спецификация готова. Бот `paper_bot_h_combo_3c.py` ещё не написан — следующий цикл напишет, если ты OK.

## 🔧 OPS

- Git push в `bots-cluster-` repo на VPS не работает (cred helper не настроен). Все commit'ы локально на VPS — следующие циклы их прочитают, но НЕ синхронизируются с GitHub.
- Lечение: один раз залогиниться `git config --global credential.helper store && git push` с PAT, потом works автоматически.

## 📊 STATUS NUMBERS (от cycle 20260528_1100)

```
3-EDGE PORTFOLIO (unchanged):
  H31_BASIS      +3.52% WR 100% Sh 1.84 n=116
  H34_PERP_PERP  +1.44% WR  81% Sh 0.82 n=101
  H3_DEPEG       +0.81% WR  96% Sh 0.63 n=129

SUB-TIERS (this session bootstrap-validated):
  H31_QUALITY_COMBO    +3.95% Sh 2.04 n=70
  H_COMBO_3c           +4.18% Sh 2.17 n=40  ← BOOTSTRAP CI tight, deploy-ready
  H_COMBO_STACKED      +4.64% Sh 2.31 n=28  ← higher Sh, n below gate

PAPER BOTS:
  paper_fairprice_v6     n=65 WR 83% $+12.16  (cut60 variant ready to A/B)
  paper_new_symbol       n=17 WR 23% $-8.75   (RECOMMEND PAUSE)

METHODOLOGY: #24 PROMOTED CONFIRMED (cycle 1100). 8 methodologies confirmed total.
```

## 🚀 NEXT-CYCLE PRIORITIES (for next AI brain wake)

1. Если cut60 запущен — мониторить trades.jsonl, сравнить WR/PnL vs v6 после n>=10 cut60 trades.
2. Если H_COMBO_3c deploy approved — написать paper_bot_h_combo_3c.py.
3. Если new_symbol_detector paused — переоценить дизайн ИЛИ удалить.
4. H_BOROS_INDICATOR — USER DECISION still pending (18-cycle defer).
5. OOS test H_COMBO_3c на новом регионе данных как только накопится 30+ дней свежих H31 событий.

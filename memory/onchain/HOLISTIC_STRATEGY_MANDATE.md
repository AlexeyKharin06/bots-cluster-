# HOLISTIC STRATEGY MANDATE — OnChain AI brain

> **Пользователь явно потребовал**: НЕ заменять старые подходы, а **комбинировать ВСЕ измерения**. Цель не "найти один magic filter", а **multi-dimensional causal framework** — почему токены пампят, как предвидеть, как избегать ругов.

## Фундаментальный принцип

**Каждое измерение — слабый сигнал. Их КОНЪЮНКЦИЯ — сильный сигнал.**

```
P(big | dim1 ∧ dim2 ∧ dim3) >> P(big | dim1)
```

Цель — найти **компаунд-фильтры** где несколько orthogonal измерений согласны. Это даёт precision (мало entries, но почти все bigs).

## 11 ИЗМЕРЕНИЙ которые ты ОБЯЗАН использовать

Используй ВСЕ. Не выбирай один и не забывай остальные.

### 1. **Technical patterns (chart/candle)**
- Bonding-curve progress (pump.fun bc=0..30)
- Liquidity ramp shape (linear, exponential, stair)
- Price velocity over m1/m5/m15
- Candle fractals (accumulation → markup → distribution)
- Wedge / breakout / consolidation patterns
- **Где смотреть**: `pump_collection.json` (если перенесён), live `sniper_state.json` row entry_signal fields

### 2. **Holder distribution dynamics**
- `top1_pct`, `top5_pct`, `top10_pct` snapshot at entry
- Concentration trends: top1 растёт или падает?
- **Δholder count** между snapshots (1min, 5min, 15min)
- Fresh wallets (<7d age) vs aged
- **Где**: entry_signal + `holders_cache.json`

### 3. **Wallet behavioral (NEW dimension, не замена!)**
- `top1_owner` wallet history
- `lp_provider` wallet history
- `pool_creator` wallet history
- First 5-10 buyer wallets (early movers)
- Smart-money cluster (≥3 known smart wallets entered)
- Funding source — откуда деньги (mixer? CEX hot wallet? known whale?)
- **Где**: `wallet_history_db.json`, `wallet_db_solana.json`, `wallet_db_bsc.json`

### 4. **TG signals (тактический подтверждающий, не leading)**
- 5 типов каналов (см. `TG_DEEP_DIVE_MANDATE.md`)
- Cluster/cascade timing
- Image content (charts/screenshots — Read tool на JPG)
- Channel quality predictiveness
- **Где**: `/srv/bots/.shared/tg/feed_onchain.jsonl`, `signals_database.jsonl`, `batches/`, `dumps/`

### 5. **Liquidity dynamics**
- `liquidity_at_entry` (top-level field!)
- LP locked vs unlocked
- LP-to-mcap ratio
- LP ramp velocity (если есть snapshots)
- Removal of LP signals
- **Где**: entry_signal, liq_drop tracking

### 6. **Volume / flow**
- `buys_m5`, `sells_m5`, `vol_h24`
- Volume/liquidity ratio (high = velocity)
- Buy/sell imbalance
- Unique buyer count vs total tx
- Jupiter aggregator skew (Solana)
- **Где**: entry_signal + DexScreener API

### 7. **Time / regime**
- Time of day (UTC) — может NYC/Asia/EU sessions играют
- Day of week
- Macro regime (Sol Cond A/B clear/triggered)
- Cluster phase (onset / mid / tail)
- **Где**: AI brain's own regime tracking, cycle insights

### 8. **Creator / deployer history**
- `cr_hist.pumped_alive` (creator's prior pumps — NEG signal!)
- Creator wallet age, total deployments, rug rate
- Same-creator related tokens
- Deployer funding lineage (откуда creator получил SOL для deploy)
- **Где**: `wallet_history_db.json`, rugger blacklist (с decontamination!)

### 9. **Cross-token correlation (cluster theory)**
- PORTUGAL cluster detection (k=1 PORTUGAL → 3-6h lag → big-wave)
- Twin tokens (SPCX+GITBANK 70sec, MTFR series)
- Symbol duplication (`symbol_dup_count`)
- Co-launches by same creator/LP-provider
- **Где**: AI brain's cluster tracking, HISTORY.md

### 10. **Mint authority / security**
- Mint revoked?
- Freeze authority?
- Anti-bot tax functions?
- Honeypot signature in tx simulation
- **Где**: entry_signal mint/lp flags, rugcheck.xyz API

### 11. **External tools используемые умными игроками**
- GMGN.ai, Photon, BullX, Padre, Axiom (наблюдалось в TG-анализе)
- Если бот видит токен который этими тулзами promoted — это сигнал
- **Где**: backtest TG mentions of these tools as feature

## Фазовая модель пампа (которую ОБЯЗАН применять)

Каждый pumped токен проходит **5 фаз**. У каждой фазы свой leading indicator:

```
Phase 1: ACCUMULATION (quiet)
  Signals: holder count growing slowly, low volume, fresh wallets buying
  Leading: первые 5-10 wallets из smart-leaderboard

Phase 2: SMART-MONEY ENTRY (insider stage)
  Signals: top1_owner = known smart wallet, +3 smart wallets in 60sec
  Leading: wallet_history match, lp_provider pairing
  ⏰ TIME WINDOW: enter HERE for max return

Phase 3: HYPE (TG/Twitter mentions surge)
  Signals: TG cluster (3+ channels in 1h), Twitter velocity, image posts
  Leading: TG-2h window, image OCR for CA
  ⏰ TIME WINDOW: still ok but smaller % left

Phase 4: TOP / DISTRIBUTION
  Signals: smart wallets EXITING, large sell orders, top1 dumping
  Leading: smart-cluster exit signal — TIME TO LEAVE
  ⏰ TIME WINDOW: exit NOW

Phase 5: RUG / DECAY
  Signals: LP removed, liquidity drop >40%, mint authority abuse
  Leading: NONE — too late, lose 90%+
  ⏰ TIME WINDOW: should have exited Phase 3-4
```

**Твоя задача**: для каждой гипотезы указать в КАКОЙ фазе она работает. Не путать entry-фильтры (Phase 1-3) с exit-фильтрами (Phase 4-5).

## Что AI brain ОБЯЗАН делать каждый цикл

### A. Mandatory multi-dimensional pass

Не выбирать "сегодня делаю только wallet анализ". Должен **на каждый цикл** хотя бы **3-5 строк** добавить в **разные** dimension:
- Технический фильтр (например volume velocity quantile)
- Wallet фильтр (top1_owner или lp_provider история)
- Holder фильтр (top5_pct диапазон)
- TG фильтр (channel timing relative to entry)
- Phase фильтр (какая стадия pump'a)

### B. Compound experiment

Каждый цикл хотя бы **один** compound experiment: что если **скомбинировать** 2-3 уже найденных фильтра?

Например:
- `H_WALLET_TOP1 ∧ H_LP_HIST ∧ phase=accumulation` → намного выше precision
- `TG-2h ∧ smart=≥3 ∧ top1<20` → должно убрать coordinated pump-and-dump

Walk-forward конъюнкцию. n упадёт, но precision взлетит.

### C. Reject sources

Никогда не отбрасывай измерение полностью. Если walk-forward FAIL — оно работает плохо **standalone**, но **может быть полезным в conjunction**. Сохраняй в backlog как "weak alone, test in combo".

### D. Phase classification on every big

Для каждого нового big — задай вопрос: **в какой фазе мы вошли?**
- Phase 1 → редко, отлично (max return)
- Phase 2 → ideal (smart-money phase)
- Phase 3 → ok (hype phase, smaller %)
- Phase 4 → late, рискованно
- Phase 5 → late = -100%

Tracking phases помогает understand WHERE our edge is.

## Конкретные causal questions которые ОБЯЗАН исследовать

1. **WHY HUPHey работает?**
   - HUPHey это: bot? insider? team member? smart trader?
   - Откуда у HUPHey деньги (funding wallet)?
   - Какая периодичность его entry (если 6h cadence — это бот!)?
   - Кто его followers (wallets которые покупают сразу за ним)?

2. **WHY PORTUGAL cluster lag 6h40min?**
   - Что происходит в эти 6h40min между первым PORTUGAL coin и первым big?
   - Это время для TG-агрегаторов? Для bot'ов? Для retail?
   - Можем ли мы предсказать **когда** big появится после онсета?

3. **WHY 51% rug rate?**
   - Среди rug'нувших токенов какие dimension'ы преобладают?
   - Какие creators у rug'ов?
   - Какие LP-providers?
   - Какие top1_owner?
   - Какие symbols (типа commodity dupli)
   - Какая stage at entry (если 51% — мы входим слишком поздно)

4. **WHY мы не поймали топ bigs?**
   - $MC +1268, $WORLDCUP +971, $GITBANK +941 — что было ОБЩЕГО?
   - Какие dimension у этих 18 bigs SAME?
   - Какие dimension у 51% rugs ОТЛИЧАЛИСЬ?
   - Конъюнкция этих SAME → potential mega-filter

## Метрика успеха

Не "n>20 для одной hypothesis". А:

- **Multi-dimensional coverage**: каждый цикл хотя бы 3 разных dimension'a имеют active hypotheses
- **Phase classification**: каждый new big классифицирован по entry-phase
- **Causal explanation**: для каждой validated hypothesis есть write-up "почему работает"
- **Compound filter**: хотя бы 1 продвинутый компаунд (3+ dimensions) в testing
- **18 bigs analysis**: для каждого из 18 исторических bigs (+ новых) — common-pattern report

## CARRY queries (не закрывать пока не решено)

1. Что общего у 18 bigs?
2. Что общего у 2542 rugs?
3. Wallet'ы которые **первыми** покупали в каждом big — leaderboard top-30?
4. TG каналы которые **первыми** упоминали каждый big — leaderboard?
5. Какое распределение **времени между launch и first big** — есть ли predictable lag?
6. **HUPHey identity** — кто это (whale? bot? insider?)
7. **Image content** TIER S/A каналов когда они публикуют — что в graphics?

## Anti-pattern (НЕ делать)

- ❌ "Этот цикл я делаю только wallet анализ" — must touch 3+ dimensions
- ❌ "Old hypothesis failed → удаляю из backlog" — keep as "weak standalone"
- ❌ "Нашёл alpha → finalize → deploy" — first test in conjunction with others
- ❌ "Один big = подтверждение" — нужно cross-cluster, cross-time validation
- ❌ "Сосредоточен на одной chain" — Sol AND BSC параллельно

## Когда ничего нового не находишь

3 цикла подряд zero new dimension hypothesis = записать в `needs.md`:
- "stuck on phase X, need data Y"
- "considering pivot to dimension Z, need user input"

Пользователь подскажет направление.

#!/usr/bin/env python3
"""overnight_megasearch.py — ВСЕ данные, ВСЕ комбинации, walk-forward validation.

Запускается в background на VPS, work 4-12h, output:
- /srv/bots/.shared/data/megasearch_catalog.json — все найденные ниши с full stats
- /srv/bots/.shared/data/megasearch_walk_forward.json — после WF validation
- /srv/bots/.shared/data/megasearch_report.md — markdown report для AI brain

Источники данных:
- sniper_state.json (4947 trades) — base + outcome
- tokens_unified.json (36K) — metrics + wallet_roles per token
- wallet_db_solana.json (95K) — wallet classifications (smart_money, serial, whale, rugger...)
- feed_onchain.jsonl — TG mentions per token
"""
import json, itertools, os, time, sys
from datetime import datetime
from collections import defaultdict, Counter

TS_START = time.time()
def log(*args):
    el = int(time.time() - TS_START)
    print(f"[+{el:5d}s]", *args, flush=True)

OUT_CATALOG = '/srv/bots/.shared/data/megasearch_catalog.json'
OUT_WF = '/srv/bots/.shared/data/megasearch_walk_forward.json'
OUT_REPORT = '/srv/bots/.shared/data/megasearch_report.md'
os.makedirs('/srv/bots/.shared/data', exist_ok=True)

# === Load everything ===
log("loading sniper_state...")
state = json.load(open('/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json'))
ct = state.get('closed_trades', [])
log(f"  closed_trades: {len(ct)}")

log("loading tokens_unified...")
try:
    tu = json.load(open('/srv/bots/onchain/code/scripts/wallet_v2/unified_db/tokens_unified.json'))
    log(f"  tokens_unified: {len(tu)}")
except Exception as e:
    tu = {}
    log(f"  tu load err: {e}")

log("loading wallet_db_solana...")
try:
    wdb_root = json.load(open('/srv/bots/onchain/code/scripts/wallet_v2/wallet_db_solana.json'))
    wdb = wdb_root.get('wallets', {})
    log(f"  wallet_db: {len(wdb)}")
except Exception as e:
    wdb = {}
    log(f"  wdb load err: {e}")

# Pre-index wallet classifications
log("indexing wallet classifications...")
W_SMART = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_smart_money')}
W_WHALE = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_whale')}
W_SNIPER = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_sniper')}
W_SERIAL_PUMP = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_serial_pump')}
W_SERIAL_RUGGER = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_serial_rugger')}
W_RUG_CREATOR = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_rug_creator')}
W_LP_RUGGER = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_lp_rugger')}
W_WASH = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_wash_trader')}
W_INSIDER = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_serial_insider')}
W_ORCH = {a for a,v in wdb.items() if (v.get('classifications') or {}).get('is_pump_orchestrator')}
log(f"  smart={len(W_SMART)} whale={len(W_WHALE)} sniper={len(W_SNIPER)} serial_pump={len(W_SERIAL_PUMP)}")
log(f"  serial_rugger={len(W_SERIAL_RUGGER)} rug_creator={len(W_RUG_CREATOR)} lp_rugger={len(W_LP_RUGGER)}")

# TG mentions
log("loading TG feed...")
TG_MENTIONS = Counter()
try:
    with open('/srv/bots/.shared/tg/feed_onchain.jsonl') as f:
        for line in f:
            try:
                r = json.loads(line)
                for a in r.get('sol_addrs', []): TG_MENTIONS[a] += 1
                for a in r.get('bsc_addrs', []): TG_MENTIONS[a.lower()] += 1
            except: pass
except Exception as e:
    log(f"  TG load err: {e}")
log(f"  TG mentions tokens: {len(TG_MENTIONS)}, total mentions: {sum(TG_MENTIONS.values())}")

# === Build enriched feature rows ===
log("enriching rows with all features...")
rows = []
for t in ct:
    es = t.get('entry_signal', {}) or {}
    token = t.get('token') or es.get('mint')
    et = t.get('entry_time') or es.get('entry_time')
    hr = None
    try:
        if et and isinstance(et, str): hr = datetime.fromisoformat(et.replace('Z','+00:00')).hour
    except: pass
    bc = es.get('bonding_curve_buyers')
    if isinstance(bc, list): bc = len(bc)
    top1_owner = es.get('top1_owner')
    lp_provider = es.get('lp_provider')
    pool_creator = es.get('pool_creator')

    # Enrich from wallet_db
    top1_smart = top1_owner in W_SMART if top1_owner else False
    top1_whale = top1_owner in W_WHALE if top1_owner else False
    top1_sniper = top1_owner in W_SNIPER if top1_owner else False
    top1_serial_pump = top1_owner in W_SERIAL_PUMP if top1_owner else False
    top1_rugger = top1_owner in W_SERIAL_RUGGER if top1_owner else False
    top1_rug_creator = top1_owner in W_RUG_CREATOR if top1_owner else False
    top1_lp_rugger = top1_owner in W_LP_RUGGER if top1_owner else False
    top1_wash = top1_owner in W_WASH if top1_owner else False
    top1_insider = top1_owner in W_INSIDER if top1_owner else False
    top1_orch = top1_owner in W_ORCH if top1_owner else False

    lp_smart = lp_provider in W_SMART if lp_provider else False
    lp_rugger = lp_provider in W_LP_RUGGER if lp_provider else False
    lp_rug_creator = lp_provider in W_RUG_CREATOR if lp_provider else False
    lp_serial_pump = lp_provider in W_SERIAL_PUMP if lp_provider else False

    creator_rugger = pool_creator in W_SERIAL_RUGGER if pool_creator else False
    creator_rug = pool_creator in W_RUG_CREATOR if pool_creator else False
    creator_serial_pump = pool_creator in W_SERIAL_PUMP if pool_creator else False

    # TG mentions for this token
    tg_count = TG_MENTIONS.get(token, 0) if token else 0

    rows.append(dict(
        pnl=t.get('pnl_pct', 0),
        token=token,
        chain=t.get('chain') or es.get('chain', '?'),
        dex=(t.get('dex') or es.get('dex') or '?').lower(),
        stream=t.get('stream') or es.get('stream', '?'),
        top1=es.get('top1_pct') or es.get('top1_wallet_pct'),
        top5=es.get('top5_pct') or es.get('top5_wallet_pct'),
        smart=es.get('smart_money_count') or 0,
        serial=es.get('serial_pump_count') or 0,
        sniper_c=es.get('sniper_count') or 0,
        liq=es.get('liquidity_at_entry') or t.get('liquidity_at_entry'),
        mcap=es.get('market_cap') or es.get('mcap') or es.get('marketcap'),
        age=es.get('age_minutes') or es.get('age_min'),
        buys=es.get('buys_m5') or 0,
        sells=es.get('sells_m5') or 0,
        bc=bc or 0,
        rc=es.get('rugcheck_score') or es.get('rc_score'),
        known=es.get('known_holders') or es.get('known') or 0,
        sym_dup=es.get('symbol_dup_count') or 0,
        mint_rev=(es.get('mint_authority') or '') == 'REVOKED',
        lp_lock=not (es.get('lp_unlocked') or False),
        hr=hr,
        et=et,
        # Wallet enrichment
        top1_smart=top1_smart, top1_whale=top1_whale, top1_sniper=top1_sniper,
        top1_serial_pump=top1_serial_pump, top1_rugger=top1_rugger,
        top1_rug_creator=top1_rug_creator, top1_lp_rugger=top1_lp_rugger,
        top1_wash=top1_wash, top1_insider=top1_insider, top1_orch=top1_orch,
        lp_smart=lp_smart, lp_rugger=lp_rugger, lp_rug_creator=lp_rug_creator,
        lp_serial_pump=lp_serial_pump,
        creator_rugger=creator_rugger, creator_rug=creator_rug, creator_serial_pump=creator_serial_pump,
        tg=tg_count,
    ))
N = len(rows)
log(f"enriched rows: {N}")

# === Build predicates ===
log("building predicate set...")
P = []
def mk(key, op, val):
    if op=='<':   fn=lambda r: r[key] is not None and r[key]<val
    elif op=='<=':fn=lambda r: r[key] is not None and r[key]<=val
    elif op=='>': fn=lambda r: r[key] is not None and r[key]>val
    elif op=='>=':fn=lambda r: r[key] is not None and r[key]>=val
    elif op=='==':fn=lambda r: r[key]==val
    elif op=='!=':fn=lambda r: r[key]!=val
    elif op=='in':fn=lambda r: r[key] is not None and r[key]>=val[0] and r[key]<val[1]
    name=f"{key}{op}{val}" if op!='in' else f"{key}={val[0]}-{val[1]}"
    return name,fn

# Numeric features — multiple thresholds each
for v in [5,10,15,20,25,30,40,50,70]:
    P.append(mk('top1','<',v))
for v in [40,60,70,80,90]:
    P.append(mk('top5','<',v)); P.append(mk('top5','>=',v))
for v in [1,2,3,5,8]:
    P.append(mk('smart','>=',v))
for v in [3,5,10,15,20]:
    P.append(mk('serial','>=',v))
for v in [5,10,15]:
    P.append(mk('sniper_c','>=',v))
for v in [3000,5000,10000,15000,20000,30000,50000,80000,150000]:
    P.append(mk('liq','>=',v))
for v in [10000,20000,30000,50000]:
    P.append(mk('liq','<',v))
for v in [30000,50000,100000,200000,500000,1000000]:
    P.append(mk('mcap','<',v))
for v in [200000,500000,1000000]:
    P.append(mk('mcap','>=',v))
for v in [3,5,10,15,20,30,60]:
    P.append(mk('age','<',v))
for v in [50,100,200,300,500,1000]:
    P.append(mk('buys','>=',v))
for v in [5,10,15,18,20]:
    P.append(mk('bc','>=',v))
P.append(mk('rc','==',500)); P.append(mk('rc','>=',300)); P.append(mk('rc','>=',400))
for v in [3,5,10,15,20]:
    P.append(mk('known','<',v)); P.append(mk('known','>=',v))
for v in [2,3,5,10]:
    P.append(mk('sym_dup','>=',v))
P.append(('mint_rev', lambda r: r['mint_rev']))
P.append(('lp_lock', lambda r: r['lp_lock']))
# Chain / dex categorical
for c in ['solana','bsc']:
    P.append((f'chain={c}', (lambda r,c=c: r['chain']==c)))
for d in ['meteora','raydium','pumpswap','pancakeswap','raydium_v4','jupiter','raydium_clmm']:
    P.append((f'dex={d}', (lambda r,d=d: r['dex']==d)))
# Wallet flags
for fk in ['top1_smart','top1_whale','top1_sniper','top1_serial_pump','top1_insider','top1_orch',
           'lp_smart','lp_serial_pump']:
    P.append((fk, (lambda r,fk=fk: r[fk])))
# Anti-flags
for fk in ['top1_rugger','top1_rug_creator','top1_lp_rugger','top1_wash',
           'lp_rugger','lp_rug_creator','creator_rugger','creator_rug']:
    P.append((f'NOT_{fk}', (lambda r,fk=fk: not r[fk])))
# TG
P.append(('tg>=1', lambda r: r['tg']>=1))
P.append(('tg>=3', lambda r: r['tg']>=3))
P.append(('tg>=10', lambda r: r['tg']>=10))
# Hour buckets
for h in [0,3,6,9,12,15,18,21]:
    P.append((f'UTC={h}-{h+3}', (lambda r,h=h: r['hr'] is not None and h<=r['hr']<h+3)))

log(f"predicates: {len(P)}")

# === Run combinations ===
def stat(sel, name, min_n=20):
    n=len(sel)
    if n<min_n: return None
    pnls=[r['pnl'] for r in sel]
    avg=sum(pnls)/n
    std=(sum((p-avg)**2 for p in pnls)/n)**0.5 if n>1 else 0
    sharpe=avg/std if std>0 else 0
    return dict(name=name,n=n,avg=avg,
                wr=sum(1 for p in pnls if p>0)/n*100,
                big=sum(1 for p in pnls if p>=200)/n*100,
                huge=sum(1 for p in pnls if p>=500)/n*100,
                rug=sum(1 for p in pnls if p<=-50)/n*100,
                total=sum(pnls),sharpe=sharpe)

niches = []
# 1-way
log("=== 1-way ===")
for n,f in P:
    r = stat([x for x in rows if f(x)], n)
    if r: niches.append(r)
log(f"  positive 1w: {sum(1 for n in niches if n['avg']>0)}")

# 2-way
log("=== 2-way ===")
cnt = 0
for (an,af),(bn,bf) in itertools.combinations(P, 2):
    r = stat([x for x in rows if af(x) and bf(x)], f"{an} & {bn}")
    if r: niches.append(r); cnt+=1
log(f"  total 2w slices: {cnt}")

# 3-way (full combinatorial)
log("=== 3-way ===")
cnt = 0
for (an,af),(bn,bf),(cn,cf) in itertools.combinations(P, 3):
    r = stat([x for x in rows if af(x) and bf(x) and cf(x)], f"{an} & {bn} & {cn}")
    if r: niches.append(r); cnt+=1
log(f"  total 3w slices: {cnt}")

# 4-way (seed-based: only conjunctions touching a top1<X OR mcap<X OR age<X seed)
log("=== 4-way (seed-pruned) ===")
seed_keywords = ['top1<','mcap<','age<','liq>=','rc=','smart>=','lp_lock','mint_rev','chain=']
seed_idx = [i for i,(n,_) in enumerate(P) if any(k in n for k in seed_keywords)]
cnt4 = 0
for s1,s2 in itertools.combinations(seed_idx, 2):
    a_n,a_f = P[s1]; b_n,b_f = P[s2]
    base = [x for x in rows if a_f(x) and b_f(x)]
    if len(base) < 25: continue
    for c_i,(c_n,c_f) in enumerate(P):
        if c_i in (s1,s2): continue
        for d_i,(d_n,d_f) in enumerate(P):
            if d_i <= c_i or d_i in (s1,s2): continue
            sel = [x for x in base if c_f(x) and d_f(x)]
            if len(sel) < 20: continue
            r = stat(sel, f"{a_n} & {b_n} & {c_n} & {d_n}")
            if r: niches.append(r); cnt4+=1
log(f"  total 4w slices: {cnt4}")

# 5-way (deeper seed pruning)
log("=== 5-way (deeply seeded) ===")
top1_seeds = [i for i,(n,_) in enumerate(P) if 'top1<' in n]
mcap_seeds = [i for i,(n,_) in enumerate(P) if 'mcap<' in n]
age_seeds = [i for i,(n,_) in enumerate(P) if 'age<' in n]
liq_seeds = [i for i,(n,_) in enumerate(P) if 'liq>=' in n]
cnt5 = 0
for t in top1_seeds[:4]:  # only top1<10/15/20/25
    for m in mcap_seeds[:3]:  # mcap<30/50/100K
        for a in age_seeds[:4]:  # age<5/10/15/20
            base = [x for x in rows if P[t][1](x) and P[m][1](x) and P[a][1](x)]
            if len(base) < 25: continue
            for li in liq_seeds[:5]:
                base2 = [x for x in base if P[li][1](x)]
                if len(base2) < 20: continue
                for ei,(e_n,e_f) in enumerate(P):
                    if ei in (t,m,a,li): continue
                    sel = [x for x in base2 if e_f(x)]
                    if len(sel) < 20: continue
                    r = stat(sel, f"{P[t][0]} & {P[m][0]} & {P[a][0]} & {P[li][0]} & {e_n}")
                    if r: niches.append(r); cnt5+=1
log(f"  total 5w slices: {cnt5}")

log(f"TOTAL slices evaluated: ~{len(P)+cnt+cnt+cnt4+cnt5}")
log(f"TOTAL niches with n>=20: {len(niches)}")

# Dedup
seen = {}
uniq = []
for nx in niches:
    sig = (nx['n'], round(nx['avg'],1), round(nx['big'],1), round(nx['rug'],1), round(nx['total'],0))
    if sig not in seen:
        seen[sig] = nx
        uniq.append(nx)
log(f"unique by signature: {len(uniq)}")

# Save catalog
log(f"writing catalog to {OUT_CATALOG}...")
positive = sorted([n for n in uniq if n['avg']>0], key=lambda x:-x['avg'])
with open(OUT_CATALOG, 'w') as f:
    json.dump({'total_evaluated': len(P)+cnt+cnt+cnt4+cnt5,
               'unique_niches': len(uniq),
               'positive_count': len(positive),
               'catalog': positive[:5000]}, f, indent=1)
log(f"wrote {len(positive)} positive niches")

# === Walk-forward validation on TOP-200 ===
log("=== walk-forward validation on top-200 positive niches ===")
rows_sorted = sorted([r for r in rows if r['et']], key=lambda x:x['et'])
N_sorted = len(rows_sorted)
TRAIN = rows_sorted[:int(N_sorted*0.6)]
VAL = rows_sorted[int(N_sorted*0.6):int(N_sorted*0.8)]
TEST = rows_sorted[int(N_sorted*0.8):]
log(f"  TRAIN {len(TRAIN)} | VAL {len(VAL)} | TEST {len(TEST)}")

# Re-build filter predicates from niche names (parse "top1<15 & mcap<100000 & ...")
def parse_pred(s):
    """Parse single predicate string to lambda."""
    for op in ['>=','<=','==','!=','<','>']:
        if op in s:
            k,v = s.split(op,1); v=v.strip()
            try: v_ = float(v) if '.' in v or v.lstrip('-').isdigit() else v
            except: v_ = v
            if op=='<':   return lambda r,k=k,v=v_: r.get(k) is not None and r[k]<v
            if op=='>=':  return lambda r,k=k,v=v_: r.get(k) is not None and r[k]>=v
            if op=='==':  return lambda r,k=k,v=v_: r.get(k)==v
            if op=='>':   return lambda r,k=k,v=v_: r.get(k) is not None and r[k]>v
            if op=='<=':  return lambda r,k=k,v=v_: r.get(k) is not None and r[k]<=v
            if op=='!=':  return lambda r,k=k,v=v_: r.get(k)!=v
    # Special: chain=X, dex=X, mint_rev, lp_lock, top1_smart, NOT_X, tg>=N, UTC=...
    s = s.strip()
    if s.startswith('chain='):
        c = s.split('=',1)[1]; return lambda r,c=c: r.get('chain')==c
    if s.startswith('dex='):
        c = s.split('=',1)[1]; return lambda r,c=c: r.get('dex')==c
    if s.startswith('UTC='):
        rng = s.split('=',1)[1].split('-'); h0,h1 = int(rng[0]), int(rng[1])
        return lambda r,h0=h0,h1=h1: r.get('hr') is not None and h0<=r['hr']<h1
    if s.startswith('NOT_'):
        k = s[4:]; return lambda r,k=k: not r.get(k)
    if s.startswith('tg>='):
        v = int(s[4:]); return lambda r,v=v: r.get('tg',0)>=v
    # Boolean flag
    if s in ('mint_rev','lp_lock','top1_smart','top1_whale','top1_sniper',
             'top1_serial_pump','top1_insider','top1_orch','lp_smart','lp_serial_pump'):
        return lambda r,k=s: bool(r.get(k))
    if s.startswith('rc='):
        v = int(s.split('=',1)[1]); return lambda r,v=v: r.get('rc')==v
    return lambda r: True

def parse_compound(name):
    parts = [p.strip() for p in name.split('&')]
    fns = [parse_pred(p) for p in parts]
    return lambda r: all(f(r) for f in fns)

# Top 300 candidates by sharpe for WF
top_candidates = sorted([n for n in uniq if n['avg']>0 and n['n']>=20], key=lambda x:-x['sharpe'])[:300]
wf_results = []
for nx in top_candidates:
    try:
        fn = parse_compound(nx['name'])
        tr = stat([r for r in TRAIN if fn(r)], 'TRAIN', min_n=5)
        va = stat([r for r in VAL if fn(r)], 'VAL', min_n=3)
        te = stat([r for r in TEST if fn(r)], 'TEST', min_n=3)
        if tr and te:
            wf_results.append(dict(name=nx['name'],
                                    full_n=nx['n'], full_avg=nx['avg'], full_big=nx['big'], full_rug=nx['rug'],
                                    train=tr, val=va, test=te,
                                    persistent=tr['avg']>0 and (te['avg']>0 or (va and va['avg']>0))))
    except Exception as e:
        pass

log(f"walk-forward done: {len(wf_results)} candidates evaluated")
# Sort by persistence + test avg
wf_results.sort(key=lambda x: (-(1 if x['persistent'] else 0), -x['test']['avg']))
with open(OUT_WF, 'w') as f:
    json.dump(wf_results, f, indent=1)
log(f"wrote walk-forward results to {OUT_WF}")

# === Markdown report ===
log("writing markdown report...")
with open(OUT_REPORT, 'w') as f:
    f.write(f"# Megasearch Report — {datetime.utcnow().isoformat()}Z\n\n")
    f.write(f"**Total slices evaluated**: ~{len(P)+cnt+cnt+cnt4+cnt5} ({len(P)} 1w + {cnt} 2w + {cnt} 3w + {cnt4} 4w + {cnt5} 5w)\n\n")
    f.write(f"**Unique signatures**: {len(uniq)}\n\n")
    f.write(f"**Positive niches (avg>0, n>=20)**: {len(positive)}\n\n")
    f.write(f"## TOP-50 by avgPnL\n\n")
    f.write(f"| Filter | n | avg | WR | big | huge | rug | Sharpe | Total |\n")
    f.write(f"|---|---|---|---|---|---|---|---|---|\n")
    for nx in positive[:50]:
        f.write(f"| `{nx['name'][:80]}` | {nx['n']} | {nx['avg']:+.1f}% | {nx['wr']:.0f}% | {nx['big']:.1f}% | {nx['huge']:.1f}% | {nx['rug']:.1f}% | {nx['sharpe']:+.2f} | {nx['total']:+.0f}% |\n")

    f.write(f"\n## TOP-30 by Sharpe\n\n")
    sh = sorted([n for n in positive if n['n']>=30], key=lambda x:-x['sharpe'])
    f.write(f"| Filter | n | avg | WR | big | rug | Sharpe |\n|---|---|---|---|---|---|---|\n")
    for nx in sh[:30]:
        f.write(f"| `{nx['name'][:80]}` | {nx['n']} | {nx['avg']:+.1f}% | {nx['wr']:.0f}% | {nx['big']:.1f}% | {nx['rug']:.1f}% | {nx['sharpe']:+.2f} |\n")

    f.write(f"\n## TOP-30 by Total PnL\n\n")
    tp = sorted([n for n in positive], key=lambda x:-x['total'])
    f.write(f"| Filter | n | avg | big | rug | Total |\n|---|---|---|---|---|---|\n")
    for nx in tp[:30]:
        f.write(f"| `{nx['name'][:80]}` | {nx['n']} | {nx['avg']:+.1f}% | {nx['big']:.1f}% | {nx['rug']:.1f}% | {nx['total']:+.0f}% |\n")

    f.write(f"\n## WALK-FORWARD VALIDATED (TRAIN/VAL/TEST persistent)\n\n")
    persistent = [w for w in wf_results if w['persistent']][:30]
    f.write(f"Persistence definition: TRAIN avg>0 AND (TEST avg>0 OR VAL avg>0).\n\n")
    f.write(f"| Filter | TRAIN n/avg | VAL n/avg | TEST n/avg |\n|---|---|---|---|\n")
    for w in persistent:
        tr,va,te = w['train'],w['val'],w['test']
        va_s = f"{va['n']}/{va['avg']:+.0f}%" if va else 'N/A'
        f.write(f"| `{w['name'][:80]}` | {tr['n']}/{tr['avg']:+.0f}% | {va_s} | {te['n']}/{te['avg']:+.0f}% |\n")

log("DONE. Total elapsed:", int(time.time()-TS_START), "seconds")
log(f"Output files:")
log(f"  {OUT_CATALOG}")
log(f"  {OUT_WF}")
log(f"  {OUT_REPORT}")

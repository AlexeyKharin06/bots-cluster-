#!/usr/bin/env python3
"""wallet_leaderboard_from_db.py — строит wallet leaderboard на основе УЖЕ накопленных данных.

Источники (всё что у нас есть):
- tokens_unified.json (36K tokens, classification + wallet_roles + metrics)
- wallet_history_db.json (6K wallets с историей)
- sniper_state.json (4988 closed_trades с pnl_pct и entry_signal)

Логика:
- Для каждого wallet: в каких токенах он засветился (top1_owner, lp_provider, bonding_curve_buyer)?
- Какие из тех токенов pumped (>=200% / >=500%) vs rugged (<-50%) vs flat?
- Hit-rate: bigs/(bigs+rugs+flat) per wallet
- Filter min_appearances >= 3

Output:
- /srv/bots/.shared/data/wallet_leaderboard.jsonl (rank by big%)
- /srv/bots/.shared/data/wallet_rug_blacklist.jsonl (anti-leaderboard)
"""
import json, sys
from pathlib import Path
from collections import defaultdict

TU = Path('/srv/bots/onchain/code/scripts/wallet_v2/unified_db/tokens_unified.json')
WH = Path('/srv/bots/onchain/code/scripts/wallet_v2/unified_db/wallet_history_db.json')
STATE = Path('/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json')
OUT_GOOD = Path('/srv/bots/.shared/data/wallet_leaderboard.jsonl')
OUT_BAD = Path('/srv/bots/.shared/data/wallet_rug_blacklist.jsonl')
OUT_GOOD.parent.mkdir(parents=True, exist_ok=True)


def classify_token(token_meta):
    """Returns 'big', 'pump', 'flat', 'rug' based on classification field."""
    cls = (token_meta.get('classification') or '').upper()
    # Real classifications seen: PUMPED_ALIVE, PUMPED_DEAD, PUMPED_RUG, PUMPED_OTHER,
    # RUG, DIED_FLAT, ALIVE, OTHER
    if 'PUMPED' in cls:
        # All PUMPED_* = pumped at some point
        if 'ALIVE' in cls:
            return 'big'  # pumped + still alive = best
        return 'pump'  # pumped + dead/rugged/other
    if 'RUG' in cls:
        return 'rug'
    if 'DIED' in cls:
        return 'rug'  # treat flat-died as rug-equivalent (lost money)
    return 'flat'


def classify_from_sniper_state(mint, state_lookup):
    """If we traded it, use real pnl."""
    pnl = state_lookup.get(mint)
    if pnl is None:
        return None
    if pnl >= 500:
        return 'big'
    if pnl >= 200:
        return 'pump'
    if pnl <= -50:
        return 'rug'
    return 'flat'


def main():
    print('Loading databases...', flush=True)
    tu = json.load(TU.open())
    print(f'  tokens_unified: {len(tu)} entries', flush=True)

    # Build sniper state lookup: mint -> max pnl
    state_lookup = {}
    if STATE.exists():
        s = json.load(STATE.open())
        ct = s.get('closed_trades', [])
        for t in ct:
            m = t.get('token') or t.get('mint') or t.get('token_address') or (t.get('entry_signal') or {}).get('mint')
            if not m:
                continue
            pnl = t.get('max_pnl_pct') or t.get('pnl_pct') or 0
            if m not in state_lookup or state_lookup[m] < pnl:
                state_lookup[m] = pnl
        print(f'  sniper closed_trades: {len(ct)} → {len(state_lookup)} unique mints with pnl', flush=True)

    # Aggregate: wallet -> token roles
    wallet_tokens = defaultdict(list)  # wallet -> [(mint, role, class)]
    no_roles = 0
    with_roles = 0
    for mint, tdata in tu.items():
        wr = tdata.get('wallet_roles') or {}
        if not wr:
            no_roles += 1
            continue
        with_roles += 1

        # Determine pump class — prefer our actual trade outcome
        sniper_cls = classify_from_sniper_state(mint, state_lookup)
        token_cls = sniper_cls or classify_token(tdata)

        # Extract wallet roles
        roles_to_extract = ['top1', 'top5', 'lp_provider', 'pool_creator', 'first_buyers', 'bonding_curve_buyers', 'sniper_wallets']
        for rk in roles_to_extract:
            v = wr.get(rk)
            if v is None:
                continue
            if isinstance(v, str):
                wallet_tokens[v].append((mint, rk, token_cls))
            elif isinstance(v, list):
                for w in v[:20]:
                    if isinstance(w, str):
                        wallet_tokens[w].append((mint, rk, token_cls))
                    elif isinstance(w, dict) and w.get('address'):
                        wallet_tokens[w['address']].append((mint, rk, token_cls))

    print(f'  tokens with wallet_roles: {with_roles} (no_roles: {no_roles})', flush=True)
    print(f'  unique wallets across all roles: {len(wallet_tokens)}', flush=True)

    # Compute stats per wallet
    leaderboard = []
    rug_blacklist = []
    for wallet, appearances in wallet_tokens.items():
        if len(appearances) < 3:
            continue
        bigs = sum(1 for _, _, cls in appearances if cls == 'big')
        pumps = sum(1 for _, _, cls in appearances if cls == 'pump')
        flats = sum(1 for _, _, cls in appearances if cls == 'flat')
        rugs = sum(1 for _, _, cls in appearances if cls == 'rug')
        total = len(appearances)
        big_pct = (bigs + pumps) / total
        rug_pct = rugs / total
        roles_summary = defaultdict(int)
        for _, role, _ in appearances:
            roles_summary[role] += 1

        record = {
            'wallet': wallet,
            'n': total,
            'bigs': bigs,
            'pumps': pumps,
            'flats': flats,
            'rugs': rugs,
            'big_pump_pct': round(big_pct, 3),
            'rug_pct': round(rug_pct, 3),
            'roles': dict(roles_summary),
        }

        # LEADERBOARD criteria: at least 1 big, big+pump rate > 20%, rugs < 25%
        if bigs >= 1 and big_pct >= 0.2 and rug_pct <= 0.25:
            leaderboard.append(record)

        # BLACKLIST criteria: rug rate >= 60% with n >= 5
        if total >= 5 and rug_pct >= 0.6:
            rug_blacklist.append(record)

    leaderboard.sort(key=lambda r: (-r['bigs'], -r['big_pump_pct'], -r['n']))
    rug_blacklist.sort(key=lambda r: (-r['rug_pct'], -r['n']))

    print(f'\n=== LEADERBOARD: {len(leaderboard)} wallets (≥1 big, ≥20% big+pump, ≤25% rug) ===', flush=True)
    print(f'{"wallet":50s} {"n":>4} {"big":>3} {"pump":>4} {"rug":>3} big+pump% rug% roles', flush=True)
    for r in leaderboard[:30]:
        print(f'  {r["wallet"]:48s} {r["n"]:>4} {r["bigs"]:>3} {r["pumps"]:>4} {r["rugs"]:>3} {r["big_pump_pct"]*100:>7.1f}% {r["rug_pct"]*100:>4.1f}% {r["roles"]}', flush=True)

    print(f'\n=== RUG BLACKLIST: {len(rug_blacklist)} wallets (≥60% rug, n≥5) ===', flush=True)
    for r in rug_blacklist[:20]:
        print(f'  {r["wallet"][:42]} n={r["n"]:>3} rugs={r["rugs"]:>3} ({r["rug_pct"]*100:.0f}%)', flush=True)

    # Write to disk
    with OUT_GOOD.open('w', encoding='utf-8') as f:
        for r in leaderboard:
            f.write(json.dumps(r) + '\n')
    with OUT_BAD.open('w', encoding='utf-8') as f:
        for r in rug_blacklist:
            f.write(json.dumps(r) + '\n')

    print(f'\nwrote {len(leaderboard)} to {OUT_GOOD}', flush=True)
    print(f'wrote {len(rug_blacklist)} to {OUT_BAD}', flush=True)


if __name__ == '__main__':
    main()

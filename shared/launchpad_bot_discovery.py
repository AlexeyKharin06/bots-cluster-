#!/usr/bin/env python3
"""launchpad_bot_discovery.py — найти ВСЕ wallets которые многократно покупают
новые pump.fun токены в первые секунды (launchpad bots).

Логика:
1. Возьми N последних pumped токенов (из pumps_24h.jsonl + наши bigs из state)
2. Для каждого — fetch первые 20 buyer wallets (Helius)
3. Aggregate: какие wallets засветились в ≥3 токенах? → launchpad bot
4. Эти wallets = наш leading indicator: если ОНИ покупают новый токен → MUST_BUY

Output:
- /srv/bots/.shared/data/launchpad_bots.jsonl — wallet, # of pumped tokens, avg pnl
"""
import json, sys, time, urllib.request
from pathlib import Path
from collections import defaultdict, Counter

ENV = Path('/srv/bots/onchain/.env')
PUMPS = Path('/srv/bots/.shared/data/pumps_24h.jsonl')
STATE = Path('/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json')
OUT = Path('/srv/bots/.shared/data/launchpad_bots.jsonl')
OUT.parent.mkdir(parents=True, exist_ok=True)


def load_keys():
    keys = []
    for line in ENV.read_text().splitlines():
        if line.startswith('HELIUS_KEY_'):
            keys.append(line.split('=', 1)[1].strip())
    return keys


HELIUS_KEYS = load_keys()
KEY_IDX = [0]


def helius_post(method, params, retries=2):
    for _ in range(retries):
        k = HELIUS_KEYS[KEY_IDX[0] % len(HELIUS_KEYS)]
        KEY_IDX[0] += 1
        try:
            req = urllib.request.Request(
                f'https://mainnet.helius-rpc.com/?api-key={k}',
                data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode(),
                headers={'Content-Type': 'application/json'},
                method='POST')
            r = urllib.request.urlopen(req, timeout=12)
            return json.loads(r.read())
        except Exception:
            time.sleep(0.3)
    return None


def get_early_signers(mint, max_tx=20):
    """Find earliest unique signers for a mint."""
    # Walk back to oldest signatures
    all_sigs = []
    before = None
    for _ in range(3):
        r = helius_post('getSignaturesForAddress', [mint, {'limit': 50, 'before': before} if before else {'limit': 50}])
        if not r or not r.get('result'):
            break
        sigs = r['result']
        all_sigs.extend(sigs)
        if len(sigs) < 50:
            break
        before = sigs[-1].get('signature')
    all_sigs.sort(key=lambda s: s.get('blockTime') or 0)

    signers = {}
    for s in all_sigs[:max_tx]:
        tx = helius_post('getTransaction', [s.get('signature'), {'maxSupportedTransactionVersion': 0, 'encoding': 'jsonParsed'}])
        if not tx or not tx.get('result'):
            continue
        msg = tx['result'].get('transaction', {}).get('message', {})
        for k in msg.get('accountKeys', []):
            if isinstance(k, dict) and k.get('signer'):
                addr = k.get('pubkey')
                if addr not in signers:
                    signers[addr] = s.get('blockTime')
    return signers


def main():
    # Step 1: collect mints to analyze
    mints = []

    # Our biggest historical bigs
    if STATE.exists():
        try:
            s = json.load(STATE.open())
            ct = s.get('closed_trades', [])
            big_trades = [t for t in ct if t.get('pnl_pct', 0) >= 200]
            for t in big_trades[-20:]:  # last 20 bigs
                m = t.get('mint') or (t.get('entry_signal') or {}).get('mint')
                if m:
                    mints.append({'mint': m, 'src': 'our_big', 'symbol': t.get('symbol', '?')})
        except Exception as e:
            print(f'state err: {e}')

    # Pumped tokens from scanner
    if PUMPS.exists():
        for line in PUMPS.read_text().splitlines()[-30:]:
            try:
                p = json.loads(line)
                m = p.get('mint') or p.get('pair_address')
                if m:
                    mints.append({'mint': m, 'src': 'pump_scanner', 'symbol': p.get('symbol', '?')})
            except Exception:
                pass

    # 4 user-provided tokens
    for m, sym in [
        ('Ac8EScJ4ufRo8PiFkun7diUrcCCktg4JvArb3mPmpump', 'PP420'),
        ('5s7tf6ih2CEZf7ZPNkJAtcknAq9DL5GsWHMMT3Jdpump', 'Stake'),
        ('2MBq3mrKSKf6NnG5x29rBK4B9f7CWR4N1EQJ18NsViRL', 'TRALALERO'),
        ('97XwkY2xLEH8Nhzfv2eqtSXut4PQb77kx9J3k1atpump', 'HypurrClaw'),
    ]:
        mints.append({'mint': m, 'src': 'user_provided', 'symbol': sym})

    # Dedup by mint
    seen_mints = set()
    uniq = []
    for m in mints:
        if m['mint'] not in seen_mints:
            seen_mints.add(m['mint'])
            uniq.append(m)

    print(f'analyzing {len(uniq)} pumped tokens...', flush=True)

    # Step 2: get early signers for each
    wallet_appearances = defaultdict(list)
    for i, item in enumerate(uniq):
        print(f'[{i+1}/{len(uniq)}] {item["symbol"][:15]} {item["mint"][:10]}.. src={item["src"]}', flush=True)
        try:
            signers = get_early_signers(item['mint'], max_tx=15)
            for addr, t in signers.items():
                wallet_appearances[addr].append({'mint': item['mint'], 'symbol': item['symbol'], 'time': t, 'src': item['src']})
        except Exception as e:
            print(f'  err: {e}')
            continue
        time.sleep(0.4)  # rate-limit

    # Step 3: aggregate — wallets appearing in ≥2 tokens
    print(f'\n=== LAUNCHPAD BOT CANDIDATES (wallets appearing in ≥2 pumped tokens) ===')
    bot_candidates = []
    for addr, apps in wallet_appearances.items():
        if len(apps) >= 2:
            bot_candidates.append({'wallet': addr, 'count': len(apps), 'tokens': [{'sym': a['symbol'], 'mint_short': a['mint'][:10], 'src': a['src']} for a in apps]})

    bot_candidates.sort(key=lambda b: -b['count'])
    for bc in bot_candidates[:30]:
        toks = ', '.join(f'{t["sym"]}({t["src"][:4]})' for t in bc['tokens'])
        print(f'  {bc["wallet"][:12]}.. count={bc["count"]} tokens=[{toks}]')

    # Step 4: write to disk
    with OUT.open('w', encoding='utf-8') as f:
        for bc in bot_candidates:
            f.write(json.dumps(bc, ensure_ascii=False) + '\n')

    print(f'\nwrote {len(bot_candidates)} candidates to {OUT}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""early_buyer_postmortem.py — для каждого pumped токена находит первых покупателей.

Использует Helius RPC (13 ключей в .env) для:
- getSignaturesForAddress на mint (вся история tx)
- getTransaction для первых N tx (расшифровать buy/sell, кто wallet)
- Найти первые 5-10 buyer wallets
- Cross-ref с wallet_history_db.json
- Output: что было бы видно ДО pump'а

Usage:
  python3 early_buyer_postmortem.py <mint1> <mint2> ...
"""
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

ENV = Path('/srv/bots/onchain/.env')
WALLET_DB = Path('/srv/bots/onchain/code/scripts/wallet_v2/unified_db/wallet_db_solana.json')
WALLET_HIST = Path('/srv/bots/onchain/code/scripts/wallet_v2/unified_db/wallet_history_db.json')


def load_keys():
    keys = []
    for line in ENV.read_text().splitlines():
        if line.startswith('HELIUS_KEY_'):
            k = line.split('=', 1)[1].strip()
            keys.append(k)
    return keys


HELIUS_KEYS = load_keys()
KEY_IDX = [0]


def helius_post(method, params, retries=3):
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
        except Exception as e:
            print(f'  err {method}: {e}', flush=True)
            time.sleep(0.5)
    return None


def get_signatures(addr, limit=30, before=None):
    p = [addr, {'limit': limit}]
    if before:
        p[1]['before'] = before
    return helius_post('getSignaturesForAddress', p)


def get_tx(sig):
    return helius_post('getTransaction', [sig, {'maxSupportedTransactionVersion': 0, 'encoding': 'jsonParsed'}])


def get_oldest_signatures(addr, max_pages=10):
    """Walk back to oldest signatures."""
    all_sigs = []
    before = None
    for _ in range(max_pages):
        r = get_signatures(addr, limit=50, before=before)
        if not r or not r.get('result'):
            break
        sigs = r['result']
        all_sigs.extend(sigs)
        if len(sigs) < 50:
            break
        before = sigs[-1].get('signature')
    # Sort by blockTime ascending (oldest first)
    all_sigs.sort(key=lambda s: s.get('blockTime') or 0)
    return all_sigs


def analyze_token(mint):
    print(f'\n========================')
    print(f'TOKEN: {mint}')
    print(f'========================')

    sigs = get_oldest_signatures(mint, max_pages=4)
    print(f'  total signatures fetched: {len(sigs)}')
    if not sigs:
        return

    oldest = sigs[0]
    print(f'  oldest tx: time={oldest.get("blockTime")} slot={oldest.get("slot")} sig={oldest.get("signature","")[:20]}...')

    # Analyze first 15 transactions to find buyers
    print(f'  analyzing first 15 transactions...')
    buyer_wallets = {}
    for i, s in enumerate(sigs[:15]):
        tx = get_tx(s.get('signature'))
        if not tx or not tx.get('result'):
            continue
        result = tx['result']
        tx_block_time = result.get('blockTime')
        msg = result.get('transaction', {}).get('message', {})
        account_keys = msg.get('accountKeys', [])
        # Heuristic: first signer = likely buyer or pool creator
        for k in account_keys:
            if isinstance(k, dict) and k.get('signer'):
                addr = k.get('pubkey')
                if addr not in buyer_wallets:
                    buyer_wallets[addr] = {'first_seen_time': tx_block_time, 'tx_count': 1, 'first_sig': s.get('signature')}
                else:
                    buyer_wallets[addr]['tx_count'] += 1

    print(f'  unique early signers: {len(buyer_wallets)}')

    # Sort by first_seen
    early = sorted(buyer_wallets.items(), key=lambda kv: kv[1]['first_seen_time'] or 0)[:10]
    print(f'\n  Top 10 earliest signers:')
    for addr, info in early:
        t = info['first_seen_time']
        t_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t)) if t else '?'
        print(f'    {addr[:8]}.. tx={info["tx_count"]} first={t_str}')

    # Cross-ref with our wallet_db
    if WALLET_DB.exists():
        wdb = json.load(open(WALLET_DB))
        print(f'\n  Cross-ref with wallet_db_solana.json ({len(wdb)} wallets):')
        known = 0
        for addr, info in early:
            if addr in wdb:
                w = wdb[addr]
                known += 1
                roles = []
                for f in ('is_serial', 'is_smart', 'is_sniper', 'is_serial_rugger', 'is_lp_rugger'):
                    if w.get(f):
                        roles.append(f)
                print(f'    KNOWN: {addr[:10]}.. roles={roles}')
        print(f'  KNOWN buyers: {known}/{len(early)}')


if __name__ == '__main__':
    mints = sys.argv[1:] if len(sys.argv) > 1 else [
        'Ac8EScJ4ufRo8PiFkun7diUrcCCktg4JvArb3mPmpump',  # PP420
        '5s7tf6ih2CEZf7ZPNkJAtcknAq9DL5GsWHMMT3Jdpump',  # Stake
        '2MBq3mrKSKf6NnG5x29rBK4B9f7CWR4N1EQJ18NsViRL',  # TRALALERO
        '97XwkY2xLEH8Nhzfv2eqtSXut4PQb77kx9J3k1atpump',  # HypurrClaw
    ]
    print(f'Analyzing {len(mints)} tokens with {len(HELIUS_KEYS)} Helius keys')
    for m in mints:
        analyze_token(m)
        time.sleep(0.5)

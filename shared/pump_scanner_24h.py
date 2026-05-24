#!/usr/bin/env python3
"""pump_scanner_24h.py — ловит ВСЕ Solana токены которые пампили >X% за 24h.

Запускается на VPS по cron каждые 15 мин:
  */15 * * * * /usr/bin/python3 /srv/bots/cluster/shared/pump_scanner_24h.py >> /srv/bots/.shared/logs/pump_scanner.log 2>&1

Источники:
- DexScreener search API (filter for high mover Solana)
- GeckoTerminal trending pools

Output:
- /srv/bots/.shared/data/pumps_24h.jsonl (append-only, все pumped tokens)
- /srv/bots/.shared/data/missed_pumps.jsonl (те что НЕ в нашем seen_tokens)

AI brain читает missed_pumps.jsonl и:
  - Понимает что мы пропускаем
  - Анализирует общие dimensions (creator, dex, mcap range, age)
  - Предлагает фильтры/sources чтобы ловить раньше
"""
import json, os, time, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

SHARED = Path('/srv/bots/.shared/data')
SHARED.mkdir(parents=True, exist_ok=True)
PUMPS = SHARED / 'pumps_24h.jsonl'
MISSED = SHARED / 'missed_pumps.jsonl'
SEEN_TOKENS_PATH = Path('/srv/bots/onchain/code/scripts/wallet_v2/sniper_state.json')

MIN_PCT_24H = 200       # >= +200% за 24h
MIN_VOL_24H = 100_000   # >= $100K volume (filter дешёвые манипуляции)
MIN_LIQ = 10_000        # >= $10K liquidity

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) Gecko/20100101 Firefox/124.0'}


def fetch_json(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(r.read())
    except Exception as e:
        print(f'[err] {url[:60]}: {e}', flush=True)
        return None


def get_dexscreener_search(query):
    """DexScreener search (general — work-around since trending API нет в public)."""
    d = fetch_json(f'https://api.dexscreener.com/latest/dex/search?q={query}')
    return (d or {}).get('pairs', [])


def get_geckoterminal_trending():
    """GeckoTerminal trending Solana pools."""
    d = fetch_json('https://api.geckoterminal.com/api/v2/networks/solana/trending_pools?page=1')
    if not d:
        return []
    out = []
    for p in d.get('data', []):
        a = p.get('attributes', {})
        out.append({
            'pair_address': p.get('id', '').replace('solana_', ''),
            'symbol': (a.get('name') or '').split(' / ')[0],
            'h24_price_change': float((a.get('price_change_percentage') or {}).get('h24') or 0),
            'h24_volume': float(a.get('volume_usd', {}).get('h24') or 0),
            'liquidity': float(a.get('reserve_in_usd') or 0),
            'mcap': float(a.get('fdv_usd') or 0),
            'pair_created_at': a.get('pool_created_at'),
            'source': 'geckoterminal_trending',
        })
    return out


def get_dexscreener_token_profiles():
    """DexScreener featured profiles (organic top movers)."""
    d = fetch_json('https://api.dexscreener.com/token-profiles/latest/v1')
    return d if isinstance(d, list) else []


def normalize_pair(p, source):
    """Normalize DexScreener-style pair to our schema."""
    if not p:
        return None
    bt = p.get('baseToken', {}) or {}
    pc = p.get('priceChange', {}) or {}
    vol = (p.get('volume', {}) or {}).get('h24')
    liq = (p.get('liquidity', {}) or {}).get('usd')
    return {
        'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'source': source,
        'chain': p.get('chainId'),
        'dex': p.get('dexId'),
        'pair_address': p.get('pairAddress'),
        'mint': bt.get('address'),
        'symbol': bt.get('symbol'),
        'name': (bt.get('name') or '')[:50],
        'mcap': p.get('marketCap'),
        'liquidity': liq,
        'volume_h24': vol,
        'price_change_h1': pc.get('h1'),
        'price_change_h6': pc.get('h6'),
        'price_change_h24': pc.get('h24'),
        'pair_created_at': p.get('pairCreatedAt'),
    }


def load_seen_tokens():
    try:
        s = json.load(open(SEEN_TOKENS_PATH))
        seen = s.get('seen_tokens', {}) or s.get('seen', {})
        if isinstance(seen, dict):
            return set(seen.keys())
        if isinstance(seen, list):
            return set(seen)
    except Exception as e:
        print(f'[err] seen load: {e}', flush=True)
    return set()


def main():
    print(f'[{datetime.now(timezone.utc).isoformat()}] scanner started', flush=True)
    seen = load_seen_tokens()
    print(f'  seen tokens: {len(seen)}', flush=True)

    all_pumps = []

    # Source 1: GeckoTerminal trending
    gtp = get_geckoterminal_trending()
    print(f'  GeckoTerminal trending: {len(gtp)} pools', flush=True)
    for p in gtp:
        if p.get('h24_price_change', 0) >= MIN_PCT_24H and p.get('h24_volume', 0) >= MIN_VOL_24H and p.get('liquidity', 0) >= MIN_LIQ:
            p['ts'] = datetime.now(timezone.utc).isoformat()
            p['chain'] = 'solana'
            all_pumps.append(p)

    # Source 2: DexScreener search (общие memecoin keywords)
    for q in ['solana', 'pump', 'meme']:
        results = get_dexscreener_search(q)
        for r in results[:50]:
            if r.get('chainId') != 'solana':
                continue
            pc24 = (r.get('priceChange') or {}).get('h24')
            if pc24 is None or pc24 < MIN_PCT_24H:
                continue
            vol = (r.get('volume') or {}).get('h24')
            liq = (r.get('liquidity') or {}).get('usd')
            if not vol or vol < MIN_VOL_24H:
                continue
            if not liq or liq < MIN_LIQ:
                continue
            n = normalize_pair(r, f'dexscreener_search_{q}')
            if n:
                all_pumps.append(n)
        time.sleep(0.3)
    print(f'  total pumps captured: {len(all_pumps)}', flush=True)

    # Dedup by pair_address
    by_pair = {}
    for p in all_pumps:
        pa = p.get('pair_address') or p.get('mint')
        if pa and pa not in by_pair:
            by_pair[pa] = p
    print(f'  unique pumps after dedup: {len(by_pair)}', flush=True)

    # Append to log
    new_count = 0
    missed_count = 0
    with PUMPS.open('a', encoding='utf-8') as fpumps, MISSED.open('a', encoding='utf-8') as fmissed:
        for pa, p in by_pair.items():
            line = json.dumps(p, ensure_ascii=False) + '\n'
            fpumps.write(line)
            new_count += 1
            mint = p.get('mint') or pa
            if mint not in seen:
                fmissed.write(line)
                missed_count += 1

    print(f'  appended {new_count} (missed by sniper: {missed_count})', flush=True)


if __name__ == '__main__':
    main()

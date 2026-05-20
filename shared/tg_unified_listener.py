#!/usr/bin/env python3
"""TG UNIFIED LISTENER — ОДИН Telethon process для всех проектов.

Архитектура:
- ОДНА Telethon session в /srv/bots/.shared/tg/tg_session.session
- ОДНА авторизация (QR + 2FA сделана пользователем один раз)
- Слушает ВСЕ каналы из Telegram folders: crypto, OnChain, Bot, listing, arb, funding
- Пишет append-only в /srv/bots/.shared/tg/signals_master.jsonl
- Каждое сообщение обогащено: addresses (SOL/BSC/EVM), keywords (listing/arb/funding), channel, folder, ts

Per-project потребители читают signals_master.jsonl и фильтруют что им надо.
Это убирает дубли (5 sessions было), экономит RAM/CPU и сводит TG auth к одному месту.
"""
import asyncio, json, os, re, sys, time
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, deque

SHARED = Path('/srv/bots/.shared/tg')
SHARED.mkdir(parents=True, exist_ok=True)

# Credentials
CREDS_PATH = SHARED / '.tg_credentials'
if not CREDS_PATH.exists():
    print(f"[FATAL] {CREDS_PATH} missing. Copy from any project's .tg_credentials")
    sys.exit(1)
creds = dict(line.split('=', 1) for line in CREDS_PATH.read_text().splitlines() if '=' in line)
API_ID = int(creds['api_id'])
API_HASH = creds['api_hash']
SESSION = str(SHARED / 'tg_session')

# Output
MASTER_LOG = SHARED / 'signals_master.jsonl'
STATS_PATH = SHARED / 'listener_stats.json'

# Project-specific routed feeds (per-project signals_pool)
PROJECT_FEEDS = {
    'onchain': SHARED / 'feed_onchain.jsonl',
    'listing-arb': SHARED / 'feed_listing.jsonl',
    'cex-onchain': SHARED / 'feed_cex.jsonl',
    'funding-rate': SHARED / 'feed_funding.jsonl',
}

# What folders count
TARGET_FOLDERS = {'crypto', 'OnChain', 'Bot', 'listing', 'arb', 'funding', 'trading'}

# Regex patterns
SOL_ADDR = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
BSC_ADDR = re.compile(r'\b0x[a-fA-F0-9]{40}\b')

IGNORED_ADDRS = {
    'So11111111111111111111111111111111111111112',
    'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
    'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB',
    '11111111111111111111111111111111',
    'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA',
}

# Keyword routing — какие сигналы куда (case-insensitive)
KEYWORDS = {
    'onchain': [r'\bpump\b', r'\brug\b', r'\bsniper\b', r'\bsolana\b', r'\bbsc\b',
                r'\bmemecoin\b', r'\bpump\.fun\b', r'\$[A-Z]{3,}\b'],
    'listing-arb': [r'\blist(ing|ed)?\b', r'\bbinance\b', r'\bcoinbase\b', r'\bokx\b',
                    r'\bupbit\b', r'\bbithumb\b', r'\bannouncement\b'],
    'cex-onchain': [r'\barb(itrage)?\b', r'\bspread\b', r'\btransfer\b', r'\bbridge\b',
                    r'\bcross\b.{0,5}\bexchange\b'],
    'funding-rate': [r'\bfunding\b.{0,5}\brate\b', r'\bperp\b', r'\bperpetual\b',
                     r'\boi\b', r'\bopen interest\b', r'\bbasis\b'],
}

def init_logging():
    LOG = SHARED / 'tg_listener.log'
    def log(msg):
        ts = datetime.now(timezone.utc).isoformat(timespec='seconds')
        line = f'[{ts}] {msg}'
        print(line, flush=True)
        try:
            with LOG.open('a') as f:
                f.write(line + '\n')
        except Exception:
            pass
    return log

log = init_logging()

# Import Telethon (после log)
try:
    from telethon import TelegramClient, events
    from telethon.tl.functions.messages import GetDialogFiltersRequest
except ImportError:
    log("Telethon not installed. Run: pip3 install telethon --break-system-packages")
    sys.exit(2)


async def get_target_channel_ids(client):
    """Возвращает channel_id'ы из Telegram folders (crypto, OnChain, etc)."""
    target_ids = set()
    try:
        result = await client(GetDialogFiltersRequest())
        # result has .filters list with DialogFilter objects
        for f in result.filters:
            title = getattr(f, 'title', None)
            if title is None:
                continue
            # title is TextWithEntities object in newer Telethon
            title_str = getattr(title, 'text', None) or str(title)
            if title_str in TARGET_FOLDERS:
                for peer in getattr(f, 'include_peers', []):
                    pid = getattr(peer, 'channel_id', None) or getattr(peer, 'chat_id', None) or getattr(peer, 'user_id', None)
                    if pid:
                        target_ids.add(int(pid))
                log(f"folder '{title_str}': {len(getattr(f, 'include_peers', []))} channels")
    except Exception as e:
        log(f"failed to get folders: {e}. Listening to ALL dialogs as fallback.")
        return None  # None = listen to everything
    return target_ids


def extract_payload(message_text, channel_name, channel_id, folder=None):
    """Извлекает структурированные данные из сообщения."""
    text = message_text or ''
    sol_addrs = [a for a in SOL_ADDR.findall(text) if a not in IGNORED_ADDRS]
    bsc_addrs = list(set(BSC_ADDR.findall(text)))

    # Determine which project(s) this signal is relevant to
    routes = []
    text_lower = text.lower()
    for project, patterns in KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, text_lower, re.IGNORECASE):
                routes.append(project)
                break

    # Onchain: any SOL/BSC address counts even without keyword
    if (sol_addrs or bsc_addrs) and 'onchain' not in routes:
        routes.append('onchain')

    return {
        'ts': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'channel': channel_name,
        'channel_id': channel_id,
        'folder': folder,
        'sol_addrs': sol_addrs[:10],
        'bsc_addrs': bsc_addrs[:10],
        'routes': routes,
        'text': text[:1000],  # cap to 1000 chars
    }


def write_signal(record):
    """Запись в master + project feeds."""
    line = json.dumps(record, ensure_ascii=False) + '\n'
    with MASTER_LOG.open('a', encoding='utf-8') as f:
        f.write(line)
    for project in record.get('routes', []):
        feed = PROJECT_FEEDS.get(project)
        if feed:
            with feed.open('a', encoding='utf-8') as f:
                f.write(line)


# Stats
stats = {'started_at': datetime.now(timezone.utc).isoformat(), 'msgs_total': 0, 'msgs_routed': defaultdict(int)}
def save_stats():
    try:
        s = {**stats, 'msgs_routed': dict(stats['msgs_routed']), 'updated_at': datetime.now(timezone.utc).isoformat()}
        STATS_PATH.write_text(json.dumps(s, indent=2))
    except Exception:
        pass


def normalize_chat_id(cid):
    """Telegram channels приходят как -1001234567890 в event.chat_id,
    но в include_peers хранятся как 1234567890.
    Возвращает 'normalized' positive id для сравнения.
    Проверенная логика из старого tg_listener: abs - 10^12 для длинных id с префиксом."""
    cid = int(cid)
    if cid is None:
        return None
    if cid < 0:
        a = abs(cid)
        if a > 1_000_000_000_000:  # -100XXXXXXXXXXX format
            return a - 1_000_000_000_000
        return a
    return cid


# ★ TIER S/A channels — image-based signals (из paper_streams_integration_20260509.md)
# Эти каналы публикуют CA в виде картинок (chart screenshots, branded posts).
# Без OCR мы пропускаем ~91% их сигналов.
OCR_TIER_CHANNELS = {
    'Gre4cha_crypto', 'MEMEcrypted', 'memecrypted_chat', 'on_chain_radar',
    'crypto_chu', 'artypost', 'awaiting_lifechange', 'crypto_azam',
    'zodchiii', 'cryptokitta', 'easyfart', 'icodrops_sergey', 'web3memoriess',
    'PowsGemCalls', 'l3xdaily',
}

_ocr_reader_box = [None]  # lazy holder


def get_ocr():
    """Lazy-load easyocr (300MB models). Только при первом изображении."""
    if _ocr_reader_box[0] is None:
        log("loading easyocr models (first time, ~300MB)...")
        import easyocr
        _ocr_reader_box[0] = easyocr.Reader(['en'], gpu=False, verbose=False)
        log("easyocr ready")
    return _ocr_reader_box[0]


MEDIA_TMP_DIR = SHARED / 'media_tmp'
MEDIA_TMP_DIR.mkdir(exist_ok=True)


async def ocr_extract_addrs(client, message, ch_name):
    """Если канал в TIER S/A и в сообщении есть фото — скачивает, OCR, возвращает найденные адреса."""
    if ch_name not in OCR_TIER_CHANNELS:
        return [], []
    try:
        from telethon.tl.types import MessageMediaPhoto
        if not isinstance(getattr(message, 'media', None), MessageMediaPhoto):
            return [], []
        tmp_path = MEDIA_TMP_DIR / f'{ch_name}_{message.id}.jpg'
        await client.download_media(message, file=str(tmp_path))
        if not tmp_path.exists():
            return [], []
        try:
            reader = get_ocr()
            results = reader.readtext(str(tmp_path), detail=0, paragraph=False)
            text = ' '.join(results)
        finally:
            try:
                tmp_path.unlink()
            except Exception:
                pass
        sol_addrs = [a for a in SOL_ADDR.findall(text) if a not in IGNORED_ADDRS]
        bsc_addrs = [a.lower() for a in BSC_ADDR.findall(text)]
        if sol_addrs or bsc_addrs:
            log(f"[OCR_HIT] {ch_name} msg={message.id}: sol={len(sol_addrs)} bsc={len(bsc_addrs)}")
        return sol_addrs, bsc_addrs
    except Exception as e:
        log(f"[OCR_ERR] {ch_name} msg={message.id}: {type(e).__name__}: {str(e)[:120]}")
        return [], []


async def main():
    client = TelegramClient(SESSION, API_ID, API_HASH)
    log(f"connecting (session: {SESSION})...")
    try:
        await client.connect()
    except Exception as e:
        log(f"FATAL connect: {type(e).__name__}: {e}")
        if 'AuthKeyDuplicated' in type(e).__name__:
            log("→ Session was used from another IP. Re-auth needed:")
            log("  cd /srv/bots/.shared/tg && rm tg_session.session")
            log("  python3 tg_auth_unified.py  # provides QR + 2FA prompt")
        sys.exit(3)

    if not await client.is_user_authorized():
        log("FATAL: not authorized. Run tg_auth_unified.py first.")
        sys.exit(3)

    me = await client.get_me()
    log(f"connected as {me.first_name} (@{me.username or '?'})")

    target_ids = await get_target_channel_ids(client)
    if target_ids:
        log(f"target channels: {len(target_ids)}")

    # Debug counter — на каждое полученное событие (до фильтра)
    stats['events_received'] = 0
    stats['events_in_target'] = 0
    stats['events_with_signal'] = 0

    # ВАЖНО: events.NewMessage БЕЗ скобок — это builder pattern Telethon
    # с () — explicit filter object, может не ловить broadcast channels в некоторых версиях
    @client.on(events.NewMessage)
    async def handler(event):
        try:
            stats['events_received'] += 1
            norm_id = normalize_chat_id(event.chat_id)
            if target_ids is not None and norm_id not in target_ids and event.chat_id not in target_ids and abs(event.chat_id) not in target_ids:
                # Periodic stats save even if filtered out
                if stats['events_received'] % 100 == 0:
                    save_stats()
                    log(f"events: received={stats['events_received']} in_target={stats['events_in_target']} with_signal={stats['events_with_signal']}")
                return
            stats['events_in_target'] += 1
            chat = await event.get_chat()
            channel_name = getattr(chat, 'username', None) or getattr(chat, 'title', 'unknown')

            record = extract_payload(event.message.message or '', channel_name, event.chat_id, folder=None)

            # ★ Image OCR — для TIER S/A каналов (publish CA через картинки)
            if channel_name in OCR_TIER_CHANNELS:
                ocr_sol, ocr_bsc = await ocr_extract_addrs(client, event.message, channel_name)
                if ocr_sol or ocr_bsc:
                    # Merge OCR-найденные адреса в record
                    record['sol_addrs'] = list(set(record['sol_addrs'] + ocr_sol))
                    record['bsc_addrs'] = list(set(record['bsc_addrs'] + ocr_bsc))
                    record['ocr_used'] = True
                    if 'onchain' not in record['routes']:
                        record['routes'].append('onchain')
                    stats.setdefault('ocr_hits', 0)
                    stats['ocr_hits'] += 1

            if record['sol_addrs'] or record['bsc_addrs'] or record['routes']:
                write_signal(record)
                stats['msgs_total'] += 1
                stats['events_with_signal'] += 1
                for r in record['routes']:
                    stats['msgs_routed'][r] += 1
                if stats['msgs_total'] % 10 == 0:
                    save_stats()
                    log(f"signal #{stats['msgs_total']}: {channel_name} routes={record['routes']}")
        except Exception as e:
            log(f"handler error: {type(e).__name__}: {e}")

    log("listening for new messages... (Ctrl+C to stop)")
    save_stats()
    try:
        await client.run_until_disconnected()
    finally:
        save_stats()
        log("disconnected")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("stopped by user")

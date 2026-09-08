#!/usr/bin/env python3
"""Weekly rank tracker — replaces the expired SE Ranking project tracker.

For every keyword in audits/rank-tracker/keywords.csv it pulls a live Google
SERP (DataForSEO, Switzerland, language per row), records magicheidi.ch's best
position/URL and the top-5 domains, and appends to audits/rank-tracker/history.csv.
It also pulls the last 7 days of GSC average position for the same queries.
Prints a diff against the previous run.

Usage:
    python3 rank_tracker.py                # full run (~40 keywords, a few cents)
    python3 rank_tracker.py --only bexio   # substring filter on keyword
    python3 rank_tracker.py --no-gsc       # skip GSC
"""
import argparse
import csv
import os
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'data_sources'))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(Path(__file__).parent / 'data_sources/config/.env')

from modules.dataforseo import DataForSEO  # noqa: E402

ROOT = Path(__file__).parent
TRACK_DIR = ROOT / 'audits' / 'rank-tracker'
KEYWORDS = TRACK_DIR / 'keywords.csv'
HISTORY = TRACK_DIR / 'history.csv'
FIELDS = ['date', 'keyword', 'lang', 'group', 'mh_position', 'mh_url', 'top5', 'gsc_pos_7d', 'gsc_impr_7d', 'gsc_clicks_7d']


def load_keywords(only=None):
    rows = list(csv.DictReader(open(KEYWORDS, encoding='utf-8')))
    if only:
        rows = [r for r in rows if only.lower() in r['keyword'].lower()]
    return rows


def serp_position(dfs, keyword, lang):
    r = dfs.get_serp_data(keyword, language_code=lang, limit=30)
    if 'error' in r:
        return None, None, 'ERROR: ' + r['error']
    mh = [o for o in r['organic_results'] if 'magicheidi' in (o.get('domain') or '')]
    top5 = ' | '.join(f"{o['position']}:{o['domain']}" for o in r['organic_results'][:5])
    if mh:
        return mh[0]['position'], mh[0]['url'].replace('https://magicheidi.ch', ''), top5
    return '', '', top5


def gsc_positions(keywords):
    """7-day GSC avg position per query (exact match)."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        return {}
    site = os.getenv('GSC_SITE_URL')
    cred_path = os.getenv('GSC_CREDENTIALS_PATH')
    if not site or not cred_path:
        return {}
    creds = service_account.Credentials.from_service_account_file(
        cred_path, scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
    svc = build('searchconsole', 'v1', credentials=creds)
    end = date.today() - timedelta(days=3)
    start = end - timedelta(days=6)
    body = {'startDate': start.isoformat(), 'endDate': end.isoformat(),
            'dimensions': ['query'], 'rowLimit': 25000}
    rows, start_row = [], 0
    while True:
        body['startRow'] = start_row
        resp = svc.searchanalytics().query(siteUrl=site, body=body).execute()
        batch = resp.get('rows', [])
        rows.extend(batch)
        if len(batch) < 25000:
            break
        start_row += len(batch)
    wanted = {k['keyword'].lower() for k in keywords}
    return {r['keys'][0].lower(): r for r in rows if r['keys'][0].lower() in wanted}


def previous_run():
    if not HISTORY.exists():
        return {}
    rows = list(csv.DictReader(open(HISTORY, encoding='utf-8')))
    if not rows:
        return {}
    last_date = max(r['date'] for r in rows)
    return {r['keyword']: r for r in rows if r['date'] == last_date}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    ap.add_argument('--no-gsc', action='store_true')
    args = ap.parse_args()

    keywords = load_keywords(args.only)
    prev = previous_run()
    gsc = {} if args.no_gsc else gsc_positions(keywords)
    dfs = DataForSEO()
    today = date.today().isoformat()

    TRACK_DIR.mkdir(parents=True, exist_ok=True)
    new_file = not HISTORY.exists()
    out = open(HISTORY, 'a', newline='', encoding='utf-8')
    w = csv.DictWriter(out, fieldnames=FIELDS)
    if new_file:
        w.writeheader()

    print(f"{'keyword':42} {'grp':10} {'now':>4} {'prev':>4} {'Δ':>4}  {'gsc7d':>6}  url")
    for k in keywords:
        pos, url, top5 = serp_position(dfs, k['keyword'], k.get('lang') or 'de')
        g = gsc.get(k['keyword'].lower(), {})
        row = {'date': today, 'keyword': k['keyword'], 'lang': k.get('lang') or 'de',
               'group': k.get('group', ''), 'mh_position': pos if pos is not None else 'ERR',
               'mh_url': url or '', 'top5': top5,
               'gsc_pos_7d': round(g['position'], 1) if g else '',
               'gsc_impr_7d': g.get('impressions', '') if g else '',
               'gsc_clicks_7d': g.get('clicks', '') if g else ''}
        w.writerow(row)
        p = prev.get(k['keyword'], {}).get('mh_position', '')
        delta = ''
        if pos not in (None, '') and p not in ('', 'ERR', None):
            try:
                delta = int(p) - int(pos)
                delta = f"{delta:+d}"
            except ValueError:
                delta = ''
        print(f"{k['keyword'][:42]:42} {k.get('group','')[:10]:10} {str(pos or '-'):>4} {str(p or '-'):>4} {delta:>4}  {str(row['gsc_pos_7d'] or '-'):>6}  {url or ''}")
    out.close()
    print(f"\nAppended {len(keywords)} rows to {HISTORY.relative_to(ROOT)} (est. DataForSEO cost ≈ ${0.002 * len(keywords):.2f}).")


if __name__ == '__main__':
    main()

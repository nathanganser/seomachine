#!/usr/bin/env python3
"""
GSC pre-migration baseline export for magicheidi.ch (2026-07-16).

Exports last 90 days of Search Console data before the default-locale
migration (bare URLs: English -> German).

Outputs (audits/gsc-baseline-2026-07-16/):
  - pages_queries_90d.csv / .json  (page + query level, with locale bucket column)
  - top_pages_90d.csv / .json      (page level, with locale bucket column)
  - pages_queries_bare.csv / pages_queries_de.csv / pages_queries_other_locales.csv
  - summary.json                   (row counts + clicks per bucket)
"""

import csv
import json
import os
import sys
from datetime import datetime, timedelta
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.getcwd(), 'data_sources', 'modules'))

from dotenv import load_dotenv
load_dotenv('data_sources/config/.env')

from google_search_console import GoogleSearchConsole

OUT_DIR = 'audits/gsc-baseline-2026-07-16'
DAYS = 90
ROW_LIMIT = 25000  # GSC API max per request

OTHER_LOCALES = ('fr', 'it', 'es', 'pt')


def bucket_for_page(page_url: str) -> str:
    """Classify a page URL into bare / de / other-locale / subdomain buckets."""
    parsed = urlparse(page_url)
    # Domain property includes subdomains (app., help., www.) that are not
    # part of the locale migration on the main site.
    if parsed.netloc.lower() != 'magicheidi.ch':
        return 'subdomain'
    path = parsed.path or '/'
    segments = [s for s in path.split('/') if s]
    first = segments[0].lower() if segments else ''
    if first == 'de':
        return 'de'
    if first in OTHER_LOCALES:
        return 'other_locale'
    return 'bare'


def fetch_all_rows(service, site_url, body_base):
    """Fetch all rows with startRow pagination."""
    rows = []
    start_row = 0
    while True:
        body = dict(body_base)
        body['rowLimit'] = ROW_LIMIT
        body['startRow'] = start_row
        resp = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
        batch = resp.get('rows', [])
        rows.extend(batch)
        if len(batch) < ROW_LIMIT:
            break
        start_row += ROW_LIMIT
    return rows


def write_csv(path, fieldnames, records):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(records)


def write_json(path, records):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def main():
    gsc = GoogleSearchConsole()
    site_url = gsc.site_url
    print(f"Site: {site_url}")

    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=DAYS)).strftime('%Y-%m-%d')
    print(f"Date range: {start_date} .. {end_date}")

    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- Export 1: page + query ----
    pq_rows = fetch_all_rows(gsc.service, site_url, {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page', 'query'],
    })
    print(f"page+query rows: {len(pq_rows)}")

    pq_records = []
    for r in pq_rows:
        page, query = r['keys'][0], r['keys'][1]
        pq_records.append({
            'page': page,
            'query': query,
            'locale_bucket': bucket_for_page(page),
            'clicks': r['clicks'],
            'impressions': r['impressions'],
            'ctr': round(r['ctr'], 6),
            'position': round(r['position'], 2),
        })
    pq_records.sort(key=lambda x: (-x['clicks'], -x['impressions']))

    pq_fields = ['page', 'query', 'locale_bucket', 'clicks', 'impressions', 'ctr', 'position']
    write_csv(f'{OUT_DIR}/pages_queries_90d.csv', pq_fields, pq_records)
    write_json(f'{OUT_DIR}/pages_queries_90d.json', pq_records)

    # Per-bucket files
    bucket_files = {'bare': 'pages_queries_bare.csv',
                    'de': 'pages_queries_de.csv',
                    'other_locale': 'pages_queries_other_locales.csv',
                    'subdomain': 'pages_queries_subdomains.csv'}
    for bucket, fname in bucket_files.items():
        subset = [r for r in pq_records if r['locale_bucket'] == bucket]
        write_csv(f'{OUT_DIR}/{fname}', pq_fields, subset)

    # ---- Export 2: top pages overall ----
    page_rows = fetch_all_rows(gsc.service, site_url, {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page'],
    })
    print(f"page rows: {len(page_rows)}")

    page_records = []
    for r in page_rows:
        page = r['keys'][0]
        page_records.append({
            'page': page,
            'locale_bucket': bucket_for_page(page),
            'clicks': r['clicks'],
            'impressions': r['impressions'],
            'ctr': round(r['ctr'], 6),
            'position': round(r['position'], 2),
        })
    page_records.sort(key=lambda x: (-x['clicks'], -x['impressions']))

    page_fields = ['page', 'locale_bucket', 'clicks', 'impressions', 'ctr', 'position']
    write_csv(f'{OUT_DIR}/top_pages_90d.csv', page_fields, page_records)
    write_json(f'{OUT_DIR}/top_pages_90d.json', page_records)

    # ---- Summary ----
    summary = {
        'site_url': site_url,
        'exported_at': datetime.now().isoformat(timespec='seconds'),
        'date_range': {'start': start_date, 'end': end_date},
        'page_query_rows_total': len(pq_records),
        'page_rows_total': len(page_records),
        'buckets': {},
    }
    for bucket in ('bare', 'de', 'other_locale', 'subdomain'):
        pq_sub = [r for r in pq_records if r['locale_bucket'] == bucket]
        pg_sub = [r for r in page_records if r['locale_bucket'] == bucket]
        summary['buckets'][bucket] = {
            'page_query_rows': len(pq_sub),
            'pages': len(pg_sub),
            'clicks': sum(r['clicks'] for r in pg_sub),
            'impressions': sum(r['impressions'] for r in pg_sub),
        }
    write_json(f'{OUT_DIR}/summary.json', summary)

    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

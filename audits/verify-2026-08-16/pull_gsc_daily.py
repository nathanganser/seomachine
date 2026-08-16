#!/usr/bin/env python3
"""Daily-granularity GSC verification pull — 2026-08-16.

Verifies the premises of the externally-supplied action plan (alleged /en/ drop
July 20-26, QR cluster, /vat-rates fall, IT trend, claimed keywords) with
date-level data. Commits raw.json so analysis is reproducible.
"""
import csv
import json
import os

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv('data_sources/config/.env')
SITE = os.getenv('GSC_SITE_URL')
creds = service_account.Credentials.from_service_account_file(
    os.getenv('GSC_CREDENTIALS_PATH'),
    scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
svc = build('searchconsole', 'v1', credentials=creds)

OUT = 'audits/verify-2026-08-16'
RANGE = ('2026-06-15', '2026-08-14')

def q(start, end, dimensions=None, filters=None, row_limit=25000):
    body = {'startDate': start, 'endDate': end, 'rowLimit': row_limit}
    if dimensions:
        body['dimensions'] = dimensions
    if filters:
        body['dimensionFilterGroups'] = [{'filters': filters}]
    rows = []
    start_row = 0
    while True:
        body['startRow'] = start_row
        resp = svc.searchanalytics().query(siteUrl=SITE, body=body).execute()
        batch = resp.get('rows', [])
        rows.extend(batch)
        if len(batch) < body['rowLimit'] or not dimensions:
            break
        start_row += len(batch)
    return rows

def page_contains(expr):
    return [{'dimension': 'page', 'operator': 'contains', 'expression': expr}]

def page_equals(expr):
    return [{'dimension': 'page', 'operator': 'equals', 'expression': expr}]

def query_equals(expr):
    return [{'dimension': 'query', 'operator': 'equals', 'expression': expr}]

CLAIMED_QUERIES = [
    'beste buchhaltungssoftware schweiz',
    'klara erfahrungen',
    'zahlungsfrist rechnung schweiz',
    'mahngebühren schweiz',
    'invoicing software switzerland',
    'software fatturazione artigiani',
]

pulls = {}
pulls['en_date_page'] = q(*RANGE, dimensions=['date', 'page'], filters=page_contains('/en/'))
pulls['en_date'] = q(*RANGE, dimensions=['date'], filters=page_contains('/en/'))
pulls['qr_date_page'] = q(*RANGE, dimensions=['date', 'page'], filters=page_contains('qr'))
pulls['vat_rates_date_query'] = q('2026-06-01', '2026-08-14', dimensions=['date', 'query'],
                                  filters=page_equals('https://magicheidi.ch/vat-rates'))
pulls['vat_rates_date_page'] = q('2026-06-01', '2026-08-14', dimensions=['date', 'page'],
                                 filters=page_contains('vat-rates'))
pulls['it_date'] = q(*RANGE, dimensions=['date'], filters=page_contains('/it/'))
pulls['mwst_schweiz_date'] = q('2026-08-01', '2026-08-14', dimensions=['date'],
                               filters=page_equals('https://magicheidi.ch/mwst-schweiz'))
for query in CLAIMED_QUERIES:
    pulls[f'claimed::{query}'] = q('2026-07-01', '2026-08-14', dimensions=['date'],
                                   filters=query_equals(query))

json.dump(pulls, open(f'{OUT}/raw.json', 'w'), ensure_ascii=False)
for name, rows in pulls.items():
    print(f'{name}: {len(rows)} rows')

# Flat CSV of the date+page pulls for eyeballing.
with open(f'{OUT}/daily_pages.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['pull', 'date', 'page', 'clicks', 'impressions', 'ctr', 'position'])
    for name in ('en_date_page', 'qr_date_page', 'vat_rates_date_page'):
        for r in pulls[name]:
            w.writerow([name, r['keys'][0], r['keys'][1], r['clicks'],
                        r['impressions'], round(r['ctr'], 4), round(r['position'], 1)])
print('saved raw.json + daily_pages.csv')

#!/usr/bin/env python3
"""GSC 60-day comparison for magicheidi.ch — 2026-08-16.
Period A: 2026-05-17..2026-06-13, Period B: 2026-07-17..2026-08-13.
"""
import os, csv, json
from collections import defaultdict
from datetime import date, timedelta
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv('data_sources/config/.env')
SITE = os.getenv('GSC_SITE_URL')
creds = service_account.Credentials.from_service_account_file(
    os.getenv('GSC_CREDENTIALS_PATH'),
    scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
svc = build('searchconsole', 'v1', credentials=creds)

OUT = 'audits/gsc-comparison-2026-08-16'
A = ('2026-05-17', '2026-06-13')
B = ('2026-07-17', '2026-08-13')

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

def totals(period):
    r = q(*period)
    if not r:
        return {'clicks': 0, 'impressions': 0, 'ctr': 0, 'position': 0}
    row = r[0]
    return {'clicks': row['clicks'], 'impressions': row['impressions'],
            'ctr': row['ctr'], 'position': row['position']}

print('== site totals ==')
tA, tB = totals(A), totals(B)
print('A:', tA)
print('B:', tB)

print('== pages ==')
pages_A = {r['keys'][0]: r for r in q(*A, dimensions=['page'])}
pages_B = {r['keys'][0]: r for r in q(*B, dimensions=['page'])}
print(len(pages_A), len(pages_B))

print('== queries ==')
qry_A = {r['keys'][0]: r for r in q(*A, dimensions=['query'])}
qry_B = {r['keys'][0]: r for r in q(*B, dimensions=['query'])}
print(len(qry_A), len(qry_B))

print('== daily trend ==')
daily_total = q('2026-06-01', '2026-08-13', dimensions=['date'])
daily_brand = q('2026-06-01', '2026-08-13', dimensions=['date'],
                filters=[{'dimension': 'query', 'operator': 'contains',
                          'expression': 'heidi'}])

json.dump({
    'totals': {'A': tA, 'B': tB},
    'pages_A': pages_A, 'pages_B': pages_B,
    'queries_A': qry_A, 'queries_B': qry_B,
    'daily_total': daily_total, 'daily_brand': daily_brand,
}, open(f'{OUT}/raw.json', 'w'))
print('saved raw.json')

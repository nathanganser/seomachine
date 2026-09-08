#!/usr/bin/env python3
"""GSC pull for the 2026-09-08 big review.
Windows: C = 2026-08-09..2026-09-05 (latest 28d, GSC lags ~2-3 days),
         B = 2026-07-12..2026-08-08 (previous 28d),
         A = 2026-05-17..2026-06-13 (June baseline used in the 60-day review).
Plus 90d page+query, weekly trend since June, and country split.
"""
import os, json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv('data_sources/config/.env')
SITE = os.getenv('GSC_SITE_URL')
creds = service_account.Credentials.from_service_account_file(
    os.getenv('GSC_CREDENTIALS_PATH'),
    scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
svc = build('searchconsole', 'v1', credentials=creds)
OUT = 'audits/review-2026-09-08'
C = ('2026-08-09', '2026-09-05')
B = ('2026-07-12', '2026-08-08')
A = ('2026-05-17', '2026-06-13')
Q90 = ('2026-06-08', '2026-09-05')

def q(start, end, dimensions=None, filters=None, row_limit=25000):
    body = {'startDate': start, 'endDate': end, 'rowLimit': row_limit}
    if dimensions: body['dimensions'] = dimensions
    if filters: body['dimensionFilterGroups'] = [{'filters': filters}]
    rows, start_row = [], 0
    while True:
        body['startRow'] = start_row
        resp = svc.searchanalytics().query(siteUrl=SITE, body=body).execute()
        batch = resp.get('rows', [])
        rows.extend(batch)
        if len(batch) < row_limit or not dimensions: break
        start_row += len(batch)
    return rows

d = {}
for name, p in [('A', A), ('B', B), ('C', C)]:
    d[f'totals_{name}'] = q(*p)
    d[f'pages_{name}'] = q(*p, dimensions=['page'])
    d[f'queries_{name}'] = q(*p, dimensions=['query'])
    print(name, len(d[f'pages_{name}']), 'pages', len(d[f'queries_{name}']), 'queries')
d['page_query_90'] = q(*Q90, dimensions=['page', 'query'])
print('page_query_90', len(d['page_query_90']))
d['daily'] = q('2026-05-01', '2026-09-05', dimensions=['date'])
d['country_C'] = q(*C, dimensions=['country'])
d['device_C'] = q(*C, dimensions=['device'])
d['query_C_brand'] = q(*C, dimensions=['query'], filters=[{'dimension':'query','operator':'contains','expression':'heidi'}])
json.dump(d, open(f'{OUT}/raw.json', 'w'), ensure_ascii=False)
print('done')

#!/usr/bin/env python3
import json, csv, re
from collections import defaultdict
from datetime import date

OUT = 'audits/gsc-comparison-2026-08-16'
d = json.load(open(f'{OUT}/raw.json'))
tA, tB = d['totals']['A'], d['totals']['B']
pages_A, pages_B = d['pages_A'], d['pages_B']
qry_A, qry_B = d['queries_A'], d['queries_B']

def pct(a, b):
    return (b - a) / a * 100 if a else float('inf')

# ---------- 1. site totals ----------
with open(f'{OUT}/site_totals.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['metric', 'A_2026-05-17_06-13', 'B_2026-07-17_08-13', 'pct_change'])
    for m in ['clicks', 'impressions', 'ctr', 'position']:
        w.writerow([m, round(tA[m], 4), round(tB[m], 4), round(pct(tA[m], tB[m]), 1)])

# ---------- page normalization (de/* -> bare after migration) ----------
def norm(url):
    u = url.replace('https://www.magicheidi.ch', '').replace('https://magicheidi.ch', '')
    u = re.sub(r'^/de/', '/', u)
    u = re.sub(r'[?#].*$', '', u)
    if u != '/' and u.endswith('/'):
        u = u[:-1]
    return u or '/'

def agg_pages(pages):
    out = defaultdict(lambda: {'clicks': 0, 'impressions': 0, 'pos_w': 0.0})
    for url, r in pages.items():
        n = norm(url)
        out[n]['clicks'] += r['clicks']
        out[n]['impressions'] += r['impressions']
        out[n]['pos_w'] += r['position'] * r['impressions']
    for v in out.values():
        v['position'] = v['pos_w'] / v['impressions'] if v['impressions'] else 0
    return out

nA, nB = agg_pages(pages_A), agg_pages(pages_B)

MONEY_PAT = re.compile(r'buchhaltungssoftware|buchhaltungsprogramm|alternative/|bexio-preise|rechnungsvorlage|rechnungsprogramm|mwst|uid|qr', re.I)
def category(u):
    ul = u.lower()
    if 'feiertage' in ul or 'holiday' in ul or 'jours-feries' in ul or 'giorni-festivi' in ul:
        return 'holiday'
    if 'rechner' in ul or 'calculator' in ul or 'calculateur' in ul or 'calcolatore' in ul or 'lohnrechner' in ul or 'brutto-netto' in ul:
        return 'calculator'
    if MONEY_PAT.search(ul):
        return 'money'
    return 'other'

top_pages = sorted(nB.items(), key=lambda kv: kv[1]['clicks'], reverse=True)[:25]
with open(f'{OUT}/pages_top25.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['page', 'category', 'B_clicks', 'A_clicks', 'clicks_delta',
                'B_impr', 'A_impr', 'B_pos', 'A_pos', 'pos_delta'])
    for u, b in top_pages:
        a = nA.get(u, {'clicks': 0, 'impressions': 0, 'position': 0})
        w.writerow([u, category(u), b['clicks'], a['clicks'], b['clicks'] - a['clicks'],
                    b['impressions'], a['impressions'],
                    round(b['position'], 1), round(a['position'], 1),
                    round((b['position'] - a['position']), 1) if a['position'] else ''])

# category totals across ALL pages
cat = defaultdict(lambda: {'A_clicks': 0, 'B_clicks': 0, 'A_impr': 0, 'B_impr': 0})
for u, v in nA.items():
    c = cat[category(u)]
    c['A_clicks'] += v['clicks']; c['A_impr'] += v['impressions']
for u, v in nB.items():
    c = cat[category(u)]
    c['B_clicks'] += v['clicks']; c['B_impr'] += v['impressions']
with open(f'{OUT}/category_totals.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['category', 'A_clicks', 'B_clicks', 'clicks_delta', 'A_impr', 'B_impr'])
    for k, v in sorted(cat.items(), key=lambda kv: -kv[1]['B_clicks']):
        w.writerow([k, v['A_clicks'], v['B_clicks'], v['B_clicks'] - v['A_clicks'],
                    v['A_impr'], v['B_impr']])

# page gainers / losers (all pages, min activity)
deltas = []
for u in set(nA) | set(nB):
    a = nA.get(u, {'clicks': 0, 'impressions': 0, 'position': 0})
    b = nB.get(u, {'clicks': 0, 'impressions': 0, 'position': 0})
    deltas.append((u, a, b, b['clicks'] - a['clicks']))
deltas.sort(key=lambda x: x[3])
with open(f'{OUT}/page_movers.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['direction', 'page', 'category', 'A_clicks', 'B_clicks', 'delta', 'A_pos', 'B_pos'])
    for u, a, b, dl in reversed(deltas[-15:]):
        w.writerow(['gain', u, category(u), a['clicks'], b['clicks'], dl,
                    round(a['position'], 1), round(b['position'], 1)])
    for u, a, b, dl in deltas[:15]:
        w.writerow(['loss', u, category(u), a['clicks'], b['clicks'], dl,
                    round(a['position'], 1), round(b['position'], 1)])

# ---------- 3. tracked queries ----------
TRACKED = ["buchhaltungsprogramm schweiz", "buchhaltungssoftware schweiz",
           "schweizer buchhaltungssoftware", "buchhaltungssoftware für selbständige",
           "bexio alternative", "bexio preise", "bexio api", "bexio erfahrungen",
           "rechnungsvorlage schweiz", "rechnung schreiben", "mwst online einreichen",
           "uid nummer", "doppelte buchhaltung", "klara vs bexio", "buchhaltungsprogramm"]
with open(f'{OUT}/tracked_queries.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['query', 'A_clicks', 'A_impr', 'A_pos', 'B_clicks', 'B_impr', 'B_pos'])
    for t in TRACKED:
        a = qry_A.get(t); b = qry_B.get(t)
        w.writerow([t,
                    a['clicks'] if a else 0, a['impressions'] if a else 0,
                    round(a['position'], 1) if a else '',
                    b['clicks'] if b else 0, b['impressions'] if b else 0,
                    round(b['position'], 1) if b else ''])

# ---------- 4. UID satellites + bexio-preise + mwst-schweiz ----------
with open(f'{OUT}/uid_and_key_pages.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['page', 'B_clicks', 'B_impr', 'B_pos', 'A_clicks', 'A_impr', 'A_pos'])
    keys = sorted([u for u in set(nA) | set(nB) if 'uid' in u.lower()])
    for extra in ['/bexio-preise', '/mwst-schweiz']:
        if extra not in keys:
            keys.append(extra)
    for u in keys:
        a = nA.get(u); b = nB.get(u)
        w.writerow([u,
                    b['clicks'] if b else 0, b['impressions'] if b else 0,
                    round(b['position'], 1) if b else '',
                    a['clicks'] if a else 0, a['impressions'] if a else 0,
                    round(a['position'], 1) if a else ''])

# ---------- 5. weekly trend ----------
brand = {r['keys'][0]: r for r in d['daily_brand']}
weeks = defaultdict(lambda: {'clicks': 0, 'impr': 0, 'brand_clicks': 0})
for r in d['daily_total']:
    dt = date.fromisoformat(r['keys'][0])
    wk = dt - __import__('datetime').timedelta(days=dt.weekday())
    weeks[wk.isoformat()]['clicks'] += r['clicks']
    weeks[wk.isoformat()]['impr'] += r['impressions']
    br = brand.get(r['keys'][0])
    if br:
        weeks[wk.isoformat()]['brand_clicks'] += br['clicks']
with open(f'{OUT}/weekly_trend.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['week_start', 'clicks', 'impressions', 'brand_clicks', 'nonbrand_clicks_approx'])
    for k in sorted(weeks):
        v = weeks[k]
        w.writerow([k, v['clicks'], v['impr'], v['brand_clicks'],
                    v['clicks'] - v['brand_clicks']])

# ---------- 6. query movers ----------
qd = []
for query in set(qry_A) | set(qry_B):
    a = qry_A.get(query, {'clicks': 0, 'impressions': 0, 'position': 0})
    b = qry_B.get(query, {'clicks': 0, 'impressions': 0, 'position': 0})
    qd.append((query, a, b, b['clicks'] - a['clicks']))
qd.sort(key=lambda x: x[3])
with open(f'{OUT}/query_movers.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['direction', 'query', 'A_clicks', 'B_clicks', 'delta', 'A_pos', 'B_pos'])
    for query, a, b, dl in reversed(qd[-15:]):
        w.writerow(['gain', query, a['clicks'], b['clicks'], dl,
                    round(a['position'], 1) if a['impressions'] else '',
                    round(b['position'], 1) if b['impressions'] else ''])
    for query, a, b, dl in qd[:15]:
        w.writerow(['loss', query, a['clicks'], b['clicks'], dl,
                    round(a['position'], 1) if a['impressions'] else '',
                    round(b['position'], 1) if b['impressions'] else ''])

# print everything for digest
for fn in ['site_totals', 'category_totals', 'pages_top25', 'tracked_queries',
           'uid_and_key_pages', 'weekly_trend', 'page_movers', 'query_movers']:
    print(f'\n===== {fn} =====')
    print(open(f'{OUT}/{fn}.csv').read())

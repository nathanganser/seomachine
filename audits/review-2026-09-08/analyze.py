#!/usr/bin/env python3
import json, csv, re
from collections import defaultdict
OUT = 'audits/review-2026-09-08'
d = json.load(open(f'{OUT}/raw.json'))

def norm(url):
    u = url.replace('https://www.magicheidi.ch', '').replace('https://magicheidi.ch', '')
    u = re.sub(r'^/de/', '/', u); u = re.sub(r'[?#].*$', '', u)
    if u != '/' and u.endswith('/'): u = u[:-1]
    return u or '/'

def agg_pages(rows):
    out = defaultdict(lambda: {'clicks': 0, 'impressions': 0, 'pos_w': 0.0})
    for r in rows:
        n = norm(r['keys'][0])
        out[n]['clicks'] += r['clicks']; out[n]['impressions'] += r['impressions']
        out[n]['pos_w'] += r['position'] * r['impressions']
    for v in out.values():
        v['position'] = v['pos_w'] / v['impressions'] if v['impressions'] else 0
    return out

def category(u):
    ul = u.lower()
    if any(k in ul for k in ['feiertage','holiday','jours-feries','giorni-festivi']): return 'holiday'
    if any(k in ul for k in ['rechner','calculator','calculateur','calcolatore','brutto-netto','euro-conversion','bitcoin','gold','swiss-franc']): return 'calculator'
    if re.search(r'buchhaltungssoftware|buchhaltungsprogramm|alternative|bexio-preise|rechnungsvorlage|rechnungsprogramm|mwst|uid|qr|rechnung-schreiben|kostenlose-rechnungssoftware|top-5|klara-vs|pricing|einzahlungsschein|jahresabschluss-software|kostenvoranschlag|quittung|mahnung', ul): return 'money'
    if '/blog/' in ul: return 'blog'
    return 'other'

def locale(u):
    m = re.match(r'^/(en|fr|it|es|pt|sq|sr)(/|$)', u)
    return m.group(1) if m else 'de'

# totals
print('== SITE TOTALS (28d) ==')
for k in ['A','B','C']:
    t = d[f'totals_{k}'][0]
    print(k, {m: round(t[m],3) for m in ['clicks','impressions','ctr','position']})

pA, pB, pC = agg_pages(d['pages_A']), agg_pages(d['pages_B']), agg_pages(d['pages_C'])
# category totals
print('\n== CATEGORY CLICKS A/B/C ==')
for cat in ['holiday','calculator','money','blog','other']:
    print(cat, sum(v['clicks'] for u,v in pA.items() if category(u)==cat),
          sum(v['clicks'] for u,v in pB.items() if category(u)==cat),
          sum(v['clicks'] for u,v in pC.items() if category(u)==cat))
print('\n== LOCALE CLICKS A/B/C ==')
for loc in ['de','en','fr','it','es','pt','sq','sr']:
    print(loc, sum(v['clicks'] for u,v in pA.items() if locale(u)==loc),
          sum(v['clicks'] for u,v in pB.items() if locale(u)==loc),
          sum(v['clicks'] for u,v in pC.items() if locale(u)==loc))

# weekly trend
print('\n== WEEKLY CLICKS (Mon-start) ==')
from datetime import date, timedelta
wk = defaultdict(lambda: [0,0])
for r in d['daily']:
    dt = date.fromisoformat(r['keys'][0]); w = dt - timedelta(days=dt.weekday())
    wk[w][0] += r['clicks']; wk[w][1] += r['impressions']
for w in sorted(wk):
    if w >= date(2026,5,25): print(w, wk[w][0], wk[w][1])

# top 40 pages C with deltas
rows = []
for u, c in pC.items():
    b = pB.get(u, {'clicks':0,'impressions':0,'position':0}); a = pA.get(u, {'clicks':0,'impressions':0,'position':0})
    rows.append([u, category(u), c['clicks'], b['clicks'], a['clicks'], c['impressions'], b['impressions'], round(c['position'],1), round(b['position'],1)])
rows.sort(key=lambda r: -r[2])
with open(f'{OUT}/pages_top.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['page','cat','C_clicks','B_clicks','A_clicks','C_impr','B_impr','C_pos','B_pos']); w.writerows(rows[:150])
print('\n== TOP 40 PAGES (C clicks | B | A | C_impr | C_pos | B_pos) ==')
for r in rows[:40]: print(f"{r[0][:55]:55} {r[1]:10} {r[2]:5} {r[3]:5} {r[4]:5} {r[5]:7} {r[7]:5} {r[8]:5}")

# movers C vs B (non-holiday), min 15 clicks in either
mv = [r for r in rows if r[1]!='holiday' and max(r[2],r[3])>=15]
mv.sort(key=lambda r: r[2]-r[3])
print('\n== BIGGEST LOSERS C vs B (non-holiday) ==')
for r in mv[:15]: print(f"{r[0][:55]:55} {r[2]:5} {r[3]:5} d={r[2]-r[3]:5} pos {r[7]}<-{r[8]}")
print('\n== BIGGEST WINNERS C vs B (non-holiday) ==')
for r in mv[-15:][::-1]: print(f"{r[0][:55]:55} {r[2]:5} {r[3]:5} d={r[2]-r[3]:5} pos {r[7]}<-{r[8]}")

# tracked queries
qA = {r['keys'][0]: r for r in d['queries_A']}; qB = {r['keys'][0]: r for r in d['queries_B']}; qC = {r['keys'][0]: r for r in d['queries_C']}
TRACK = ['buchhaltungsprogramm schweiz','buchhaltungssoftware schweiz','buchhaltungsprogramm','buchhaltungssoftware','beste buchhaltungssoftware schweiz','schweizer buchhaltungssoftware','buchhaltungssoftware für selbständige','buchhaltung für selbständige','buchhaltungssoftware kleinunternehmen','bexio alternative','bexio preise','bexio erfahrungen','bexio api','klara vs bexio','klara erfahrungen','klara alternative','rechnungsvorlage schweiz','rechnungsvorlage','rechnung schreiben','rechnung schreiben schweiz','rechnungsprogramm','rechnungsprogramm schweiz','rechnungssoftware schweiz','rechnungssoftware','kostenlose rechnungssoftware','rechnungsprogramm kostenlos','mwst online einreichen','mwst schweiz','mwst sätze','mwst nummer','mwst nummer schweiz','mwst rechner','uid nummer','uid','uid register','uid nummer beantragen','uid nummer prüfen','doppelte buchhaltung','erfolgsrechnung','qr rechnung erstellen','qr rechnung','einzahlungsschein erstellen','kostenvoranschlag vorlage','quittung vorlage','mahnung vorlage','einzelfirma gründen','stundenlohn berechnen','brutto netto rechner schweiz','budget app schweiz','budgetplaner schweiz','invoicing software switzerland','accounting software switzerland','logiciel facturation suisse','logiciel comptabilité suisse','modèle facture suisse','magic heidi']
print('\n== TRACKED QUERIES  A(cl/impr/pos) | B | C ==')
with open(f'{OUT}/tracked_queries.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['query','A_clicks','A_impr','A_pos','B_clicks','B_impr','B_pos','C_clicks','C_impr','C_pos'])
    for t in TRACK:
        row=[t]
        for qq in (qA,qB,qC):
            r = qq.get(t); row += [r['clicks'], r['impressions'], round(r['position'],1)] if r else ['-','-','-']
        w.writerow(row); print(f"{t:42} {row[1]!s:>3}/{row[2]!s:>5}/{row[3]!s:>5} | {row[4]!s:>3}/{row[5]!s:>5}/{row[6]!s:>5} | {row[7]!s:>3}/{row[8]!s:>5}/{row[9]!s:>5}")

# striking distance: queries in C with impr>=100, pos 5-20, non-brand, non-holiday
print('\n== STRIKING DISTANCE (C, impr>=150, pos 4-20, top by impressions) ==')
sd = [r for r in d['queries_C'] if r['impressions']>=150 and 4<=r['position']<=20 and 'heidi' not in r['keys'][0] and not re.search(r'feiertag|férié|festiv|holiday|ferien', r['keys'][0])]
sd.sort(key=lambda r: -r['impressions'])
with open(f'{OUT}/striking_distance.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['query','clicks','impr','ctr','pos'])
    for r in sd: w.writerow([r['keys'][0], r['clicks'], r['impressions'], round(r['ctr'],3), round(r['position'],1)])
for r in sd[:60]: print(f"{r['keys'][0][:50]:50} {r['clicks']:4} {r['impressions']:6} {r['position']:5.1f}")

# high impression, low ctr, pos<=10 (CTR problems)
print('\n== CTR PROBLEMS (C, pos<=8, impr>=200, ctr<2%) ==')
cp = [r for r in d['queries_C'] if r['impressions']>=200 and r['position']<=8 and r['ctr']<0.02 and 'heidi' not in r['keys'][0]]
cp.sort(key=lambda r:-r['impressions'])
for r in cp[:30]: print(f"{r['keys'][0][:50]:50} {r['clicks']:4} {r['impressions']:6} {r['ctr']*100:4.1f}% {r['position']:5.1f}")

# country, device
print('\n== COUNTRY C =='); 
for r in sorted(d['country_C'], key=lambda r:-r['clicks'])[:8]: print(r['keys'][0], r['clicks'], r['impressions'])
print('== DEVICE C ==')
for r in d['device_C']: print(r['keys'][0], r['clicks'], r['impressions'])
print('\n== BRAND C =='); 
for r in sorted(d['query_C_brand'], key=lambda r:-r['clicks'])[:5]: print(r['keys'][0], r['clicks'], r['impressions'], round(r['position'],1))

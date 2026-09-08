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
def agg(rows):
    out = defaultdict(lambda: {'clicks': 0, 'impressions': 0, 'pos_w': 0.0})
    for r in rows:
        n = norm(r['keys'][0]); out[n]['clicks'] += r['clicks']; out[n]['impressions'] += r['impressions']; out[n]['pos_w'] += r['position']*r['impressions']
    for v in out.values(): v['position'] = v['pos_w']/v['impressions'] if v['impressions'] else 0
    return out
pA,pB,pC = agg(d['pages_A']),agg(d['pages_B']),agg(d['pages_C'])
MONEY = ['/buchhaltungssoftware','/rechnungsprogramm','/alternative/bexio','/bexio-preise','/top-5-buchhaltungssoftware-schweiz','/rechnungsvorlage','/rechnung-schreiben-schweiz','/mwst-schweiz','/mwst-freelancer','/mwst-registrierung','/online-vat-statement','/tools/vat-calculator-switzerland','/mwst-nummer-schweiz','/uid-nummer-schweiz','/uid-nummer-beantragen','/uid-nummer-pruefen','/uid-nummer-format-beispiel','/einzahlungsschein-erstellen','/qr-rechnung-erstellen','/kostenlose-rechnungssoftware-schweiz','/klara-vs-bexio','/alternative/klara','/alternative/abaninja','/alternative/banana','/alternative/cashctrl','/alternative/swiss21','/alternative/winbiz','/alternative/smallinvoice','/alternative','/pricing','/kostenvoranschlag-schweiz','/quittung-vorlage-schweiz','/mahnung-vorlage-schweiz','/doppelte-buchhaltung-schweiz','/erfolgsrechnung-schweiz','/buchhaltung-einzelfirma-schweiz','/einzelfirma-grunden-schweiz','/jahresabschluss-software','/budgeting-apps','/beleg-scanner-schweiz','/ai-expenses-scanning','/iphone','/vat-rates','/fr/rechnungsprogramm','/fr/buchhaltungssoftware','/fr/rechnungsvorlage','/fr/alternative/bexio','/it/rechnungsprogramm','/it/buchhaltungssoftware','/it/mwst-schweiz','/it/alternative/bexio','/it/commerce-register-switzerland-2026','/en/rechnungsprogramm','/en/buchhaltungssoftware','/en/commerce-register-switzerland-2026','/blog/buchhaltung-fur-selbstandige-schweiz','/blog/mwst-anmelden-schweiz','/blog/rechnungsvorlage-einzelunternehmen']
print('== MONEY PAGES: C clicks/impr/pos | B | A ==')
for u in MONEY:
    c,b,a = pC.get(u),pB.get(u),pA.get(u)
    f = lambda x: f"{x['clicks']:4}/{x['impressions']:6}/{x['position']:5.1f}" if x else "   -/     -/    -"
    print(f"{u:45} {f(c)} | {f(b)} | {f(a)}")

# per-page top queries 90d for key pages
pq = defaultdict(list)
for r in d['page_query_90']:
    pq[norm(r['keys'][0])].append((r['keys'][1], r['clicks'], r['impressions'], r['position']))
print('\n== TOP QUERIES (90d) per key page ==')
for u in ['/buchhaltungssoftware','/rechnungsprogramm','/alternative/bexio','/bexio-preise','/top-5-buchhaltungssoftware-schweiz','/rechnungsvorlage','/mwst-schweiz','/uid-nummer-schweiz','/uid-nummer-beantragen','/einzahlungsschein-erstellen','/tools/vat-calculator-switzerland','/online-vat-statement','/kostenlose-rechnungssoftware-schweiz','/rechnung-schreiben-schweiz','/fr/rechnungsprogramm','/it/commerce-register-switzerland-2026','/en/commerce-register-switzerland-2026','/']:
    qs = sorted(pq.get(u,[]), key=lambda x:-x[2])[:8]
    tot_i = sum(x[2] for x in pq.get(u,[])); tot_c = sum(x[1] for x in pq.get(u,[]))
    print(f"\n{u}  (90d: {tot_c} clicks / {tot_i} impr / {len(pq.get(u,[]))} queries)")
    for q_,c,i,p in qs: print(f"    {q_[:45]:45} {c:3} {i:6} {p:5.1f}")

# bexio queries across pages 90d
print('\n== bexio preise / bexio alternative by page (90d) ==')
for r in d['page_query_90']:
    if r['keys'][1] in ('bexio preise','bexio alternative','bexio erfahrungen','beste buchhaltungssoftware schweiz','einzahlungsschein erstellen','buchhaltungssoftware schweiz','buchhaltungsprogramm schweiz'):
        print(f"{r['keys'][1]:35} {norm(r['keys'][0]):45} {r['clicks']:3} {r['impressions']:5} {r['position']:5.1f}")

# blog performance
print('\n== BLOG PAGES (C) sorted by clicks; count zero ==')
blog = [(u,v) for u,v in pC.items() if '/blog/' in u]
blog.sort(key=lambda x:-x[1]['clicks'])
for u,v in blog[:30]: print(f"{u[:70]:70} {v['clicks']:4} {v['impressions']:6} {v['position']:5.1f}")
print('blog pages with impressions in C:', len(blog), ' with >=5 clicks:', sum(1 for u,v in blog if v['clicks']>=5))
# 90d blog totals per locale
bl = defaultdict(lambda:[0,0,set()])
for r in d['page_query_90']:
    u = norm(r['keys'][0])
    if '/blog/' in u:
        m = re.match(r'^/(en|fr|it|es|pt)/', u); loc = m.group(1) if m else 'de'
        bl[loc][0]+=r['clicks']; bl[loc][1]+=r['impressions']; bl[loc][2].add(u)
print('90d blog by locale (clicks, impr, pages w/ impr):', {k:(v[0],v[1],len(v[2])) for k,v in bl.items()})

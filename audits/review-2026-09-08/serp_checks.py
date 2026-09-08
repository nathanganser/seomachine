#!/usr/bin/env python3
import sys, json, os
sys.path.insert(0, 'data_sources')
from dotenv import load_dotenv
load_dotenv('data_sources/config/.env')
from modules.dataforseo import DataForSEO
dfs = DataForSEO()
KW = [('buchhaltungsprogramm schweiz','de'),('buchhaltungssoftware schweiz','de'),('buchhaltungssoftware für selbständige','de'),('beste buchhaltungssoftware schweiz','de'),('bexio alternative','de'),('bexio preise','de'),('rechnungsvorlage schweiz','de'),('rechnungsprogramm schweiz','de'),('rechnungssoftware schweiz','de'),('mwst schweiz','de'),('uid register','de'),('mwst online einreichen','de'),('einzahlungsschein erstellen','de'),('logiciel facturation suisse','fr'),('logiciel comptabilité suisse','fr'),('logiciel facturation lamal','fr'),('mwst rechner','de'),('rechnung schreiben','de')]
out = {}
for kw, lang in KW:
    r = dfs.get_serp_data(kw, language_code=lang, limit=30)
    out[kw] = r
    if 'error' in r: print(kw, 'ERROR', r); continue
    mh = [o for o in r['organic_results'] if 'magicheidi' in (o['domain'] or '')]
    top = [(o['position'], o['domain']) for o in r['organic_results'][:10]]
    print(f"\n### {kw} (vol {r.get('search_volume')}, features {sorted(r['features'])[:6]})")
    print("  MH:", [(m['position'], m['url'].replace('https://magicheidi.ch','')) for m in mh][:3] or 'not in top 30')
    print("  top10:", ', '.join(f"{p}:{d}" for p,d in top))
json.dump(out, open('audits/review-2026-09-08/serp_results.json','w'), ensure_ascii=False)

#!/usr/bin/env python3
"""Live SERP verification (DataForSEO) — 2026-08-16.

Checks: LOST-flagged keywords from the 2026-08-16 SE Ranking comparison
(pull-cap caveat), the externally-claimed keywords, and re-baselines for the
recorded regressions. Swiss location (2756) for all; language per keyword.
"""
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / 'data_sources' / 'config' / '.env')
sys.path.insert(0, str(ROOT / 'data_sources' / 'modules'))
from dataforseo import DataForSEO

KEYWORDS = [
    # LOST-flagged (verify pull-cap artifact vs genuine loss)
    ('erfolgsrechnung', 'de'),
    ('rechnungsvorlage schweiz', 'de'),
    ('buchhaltungsprogramm', 'de'),
    ('qr einzahlungsschein erstellen gratis', 'de'),
    # externally claimed
    ('beste buchhaltungssoftware schweiz', 'de'),
    ('klara erfahrungen', 'de'),
    ('zahlungsfrist rechnung schweiz', 'de'),
    ('mahngebühren schweiz', 'de'),
    ('invoicing software switzerland', 'en'),
    ('software fatturazione artigiani', 'it'),
    # regression re-baselines
    ('bexio api', 'de'),
    ('mwst sätze', 'de'),
    ('mwst schweiz', 'de'),
]

client = DataForSEO()
out = {}
for kw, lang in KEYWORDS:
    serp = client.get_serp_data(kw, language_code=lang)
    ours = [r for r in serp.get('organic_results', []) if 'magicheidi' in (r.get('domain') or '')]
    top3 = [(r['position'], r['domain']) for r in serp.get('organic_results', [])[:3]]
    out[kw] = {'lang': lang, 'our_results': ours, 'top3': top3,
               'features': serp.get('features', [])[:8]}
    if ours:
        print(f"{kw:42s} [{lang}] -> " + '; '.join(f"#{r['position']} {r['url']}" for r in ours[:3]))
    else:
        print(f"{kw:42s} [{lang}] -> NOT in top 100 | top3: {top3}")

json.dump(out, open(Path(__file__).parent / 'serp_results.json', 'w'), ensure_ascii=False, indent=1)
print('saved serp_results.json')

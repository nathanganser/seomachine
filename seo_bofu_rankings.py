#!/usr/bin/env python3
"""
Detailed BOFU Keyword Rankings Analysis
Checks specific high-value buyer-intent keywords.

Configure keywords in config/competitors.json under "bofu_keywords" and "alternative_keywords".

Positions come from SE Ranking by default (one bulk pull for all keywords —
reuses the latest audits/seranking-*/ snapshot if it is <= --max-snapshot-age
days old, ~1,100 credits otherwise). Pass --live for per-keyword live SERP
checks via DataForSEO (slower, costs per keyword, but real-time top 50).
"""

import argparse
import datetime as dt
import glob
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'data_sources', 'config', '.env'))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources', 'modules'))

from google_search_console import GoogleSearchConsole


def load_config():
    """Load keyword configuration from config file."""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'competitors.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    print("WARNING: config/competitors.json not found. See config/competitors.example.json")
    return {}


def seranking_positions(domain, max_snapshot_age_days):
    """All our ranked keyword rows: latest fresh snapshot if available, else a
    live SE Ranking pull. Returns (rows, source_label)."""
    from seranking import SERankingClient
    snaps = sorted(glob.glob(os.path.join(os.path.dirname(__file__),
                                          'audits', 'seranking-????-??-??')))
    if snaps:
        latest = snaps[-1]
        date = os.path.basename(latest).replace('seranking-', '')
        age = (dt.date.today() - dt.date.fromisoformat(date)).days
        kw_file = os.path.join(latest, 'raw', 'keywords_ch.json')
        if age <= max_snapshot_age_days and os.path.exists(kw_file):
            with open(kw_file) as f:
                return json.load(f), f"snapshot {date} ({age}d old)"
    client = SERankingClient()
    rows, complete = client.domain_keywords_all(domain)
    return rows, f"live SE Ranking pull ({len(rows)} rows, complete={complete})"


def check_keywords_seranking(keywords, rows, metrics, title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    best = {}
    for r in rows:
        if not r.get("position"):
            continue
        k = r["keyword"].lower()
        if k not in best or r["position"] < best[k]["position"]:
            best[k] = r
    for keyword in keywords:
        m = metrics.get(keyword.lower(), {})
        r = best.get(keyword.lower())
        vol = m.get("volume")
        print(f"\n>>> '{keyword}'")
        print(f"    Volume: {vol:,}" if vol else "    Volume: N/A")
        if m.get("difficulty") is not None:
            print(f"    Difficulty: {m['difficulty']} | CPC: ${m.get('cpc') or 0:.2f}")
        if r:
            print(f"    ✓ RANKING: #{r['position']}")
            print(f"      URL: {r.get('url', '')}")
        else:
            print(f"    ✗ NOT IN TOP 100")


def check_keywords_live(keywords, dfs, site_domain, title, limit=50, top_n=5):
    print("\n" + "=" * 80)
    print(title + " (LIVE SERP, DataForSEO)")
    print("=" * 80)
    for keyword in keywords:
        print(f"\n>>> Checking: '{keyword}'")
        try:
            serp = dfs.get_serp_data(keyword, limit=limit)
            print(f"    Search Volume: {serp.get('search_volume', 'N/A'):,}" if serp.get('search_volume') else "    Search Volume: N/A")
            our_pos, our_url = None, None
            for result in serp.get('organic_results', []):
                if site_domain in (result.get('domain') or ''):
                    our_pos = result.get('position')
                    our_url = result.get('url')
                    break
            if our_pos:
                print(f"    ✓ RANKING: #{our_pos}")
                print(f"      URL: {our_url}")
            else:
                print(f"    ✗ NOT IN TOP {limit}")
            print(f"    Top {top_n} Results:")
            for result in serp.get('organic_results', [])[:top_n]:
                pos = result.get('position')
                domain_str = result.get('domain') or 'unknown'
                pos_str = f"#{pos:2d}" if isinstance(pos, int) else " --"
                print(f"      {pos_str}. {domain_str}")
        except Exception as e:
            print(f"    Error: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="per-keyword live SERP via DataForSEO instead of SE Ranking")
    ap.add_argument("--max-snapshot-age", type=int, default=14,
                    help="reuse an SE Ranking snapshot up to this many days old (default 14)")
    args = ap.parse_args()

    config = load_config()
    site_domain = os.getenv('GSC_SITE_URL', 'yoursite.com').replace('https://', '').replace('http://', '').rstrip('/')
    company_name = os.getenv('COMPANY_NAME', 'Your Company')

    print("=" * 80)
    print(f"DETAILED BOFU KEYWORD ANALYSIS FOR {company_name.upper()}")
    print("=" * 80)

    critical_keywords = config.get('bofu_keywords', [])
    alternative_keywords = config.get('alternative_keywords', [])
    if not critical_keywords:
        print("\nNo bofu_keywords configured in config/competitors.json")
        return

    if args.live:
        try:
            from dataforseo import DataForSEO
            dfs = DataForSEO()
            print("✓ DataForSEO connected")
        except Exception as e:
            print(f"✗ DataForSEO error: {e}")
            dfs = None
        if dfs:
            check_keywords_live(critical_keywords[:20], dfs, site_domain,
                                "PART 1: CRITICAL BOFU KEYWORDS")
            if alternative_keywords:
                check_keywords_live(alternative_keywords, dfs, site_domain,
                                    "PART 2: COMPETITOR ALTERNATIVE KEYWORDS",
                                    limit=30, top_n=3)
    else:
        try:
            from seranking import SERankingClient
            rows, source = seranking_positions(site_domain, args.max_snapshot_age)
            print(f"✓ SE Ranking positions from {source}")
            all_kws = list(dict.fromkeys(critical_keywords + alternative_keywords))
            client = SERankingClient()
            metrics = {m["keyword"].lower(): m for m in client.keywords_export(all_kws)}
            check_keywords_seranking(critical_keywords, rows, metrics,
                                     "PART 1: CRITICAL BOFU KEYWORDS (SE Ranking)")
            if alternative_keywords:
                check_keywords_seranking(alternative_keywords, rows, metrics,
                                         "PART 2: COMPETITOR ALTERNATIVE KEYWORDS (SE Ranking)")
        except Exception as e:
            print(f"✗ SE Ranking error: {e} — rerun with --live for DataForSEO")

    # GSC Data for relevant keywords
    try:
        gsc = GoogleSearchConsole()
        print("\n✓ Google Search Console connected")
    except Exception as e:
        print(f"\n✗ GSC error: {e}")
        gsc = None

    all_keywords = []
    if gsc:
        print("\n" + "=" * 80)
        print("PART 3: GSC DATA - HIGH-INTENT KEYWORDS")
        print("=" * 80)

        try:
            all_keywords = gsc.get_keyword_positions(days=30, limit=2000)
        except Exception as e:
            print(f"Error fetching GSC data: {e}")
            all_keywords = []

        # Filter using relevant_terms from config
        relevant_terms = config.get('relevant_terms', [])
        skip_terms = config.get('skip_terms', [])

        hosting_keywords = []
        for kw in all_keywords:
            keyword = kw['keyword'].lower()
            if skip_terms and any(skip in keyword for skip in skip_terms):
                continue
            if relevant_terms:
                if any(term.lower() in keyword for term in relevant_terms):
                    hosting_keywords.append(kw)
            else:
                hosting_keywords.append(kw)

        hosting_keywords.sort(key=lambda x: x['impressions'], reverse=True)

        print(f"\nFound {len(hosting_keywords)} high-intent keywords")
        print("-" * 80)

        page_1 = [k for k in hosting_keywords if k['position'] <= 10]
        page_2 = [k for k in hosting_keywords if 10 < k['position'] <= 20]
        page_3_plus = [k for k in hosting_keywords if k['position'] > 20]

        print(f"Page 1: {len(page_1)} | Page 2: {len(page_2)} | Page 3+: {len(page_3_plus)}")

        print(f"\n🏆 PAGE 1 KEYWORDS:")
        for kw in page_1[:30]:
            ctr = kw['ctr'] * 100
            print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:55]:<55} | {kw['impressions']:>5,} imp | {kw['clicks']:>3} clicks | {ctr:.1f}% CTR")

        print(f"\n📈 PAGE 2 QUICK WINS:")
        for kw in page_2[:20]:
            ctr = kw['ctr'] * 100
            print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:55]:<55} | {kw['impressions']:>5,} imp | {kw['clicks']:>3} clicks | {ctr:.1f}% CTR")

        print(f"\n❌ PAGE 3+ (Need Work):")
        for kw in page_3_plus[:15]:
            ctr = kw['ctr'] * 100
            print(f"  #{kw['position']:<5.1f} | {kw['keyword'][:55]:<55} | {kw['impressions']:>5,} imp | {kw['clicks']:>3} clicks | {ctr:.1f}% CTR")

        # Check specific important queries from config
        key_queries = config.get('key_queries', critical_keywords[:10])
        if key_queries and all_keywords:
            print("\n" + "=" * 80)
            print("PART 4: KEY QUERY PERFORMANCE (GSC)")
            print("=" * 80)

            for query in key_queries:
                matches = [k for k in all_keywords if query.lower() in k['keyword'].lower()]
                if matches:
                    best = min(matches, key=lambda x: x['position'])
                    total_imp = sum(m['impressions'] for m in matches)
                    total_clicks = sum(m['clicks'] for m in matches)
                    print(f"\n'{query}':")
                    print(f"  Best Position: #{best['position']:.1f} for '{best['keyword']}'")
                    print(f"  Total Related Impressions: {total_imp:,}")
                    print(f"  Total Related Clicks: {total_clicks}")
                else:
                    print(f"\n'{query}': No data in GSC")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()

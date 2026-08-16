#!/usr/bin/env python3
"""
Research Competitor Content Gaps

Identifies keywords where competitors rank in top 20 but you don't rank at all.
These are proven demand areas with zero cannibalization - highest ROI opportunities.

Data source: SE Ranking (Swiss database). Our keyword universe comes from the
latest audits/seranking-*/ snapshot when fresh (default <= 14 days), else a
live pull; competitor top-20 keywords are pulled live (volume >= 50). SE
Ranking rows already carry volume/difficulty/cpc/intents/serp_features, so no
per-keyword SERP calls are needed. GSC is used as an optional extra exclusion
signal (keywords where we already get impressions).
"""

import argparse
import datetime as dt
import glob
import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'data_sources', 'config', '.env'))

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources', 'modules'))

from modules.opportunity_scorer import OpportunityScorer, OpportunityType
from modules.search_intent_analyzer import SearchIntentAnalyzer
from seranking import SERankingClient


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'competitors.json')
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    print("WARNING: config/competitors.json not found. See config/competitors.example.json")
    return {}


CONFIG = load_config()
DIRECT_COMPETITORS = CONFIG.get('seranking_competitors') or CONFIG.get('direct_competitors', [])
CONTENT_COMPETITORS = CONFIG.get('content_competitors', [])


def our_keyword_set(client, domain, max_snapshot_age_days=14):
    """Keywords we already rank top-100 for — fresh snapshot if available, else live."""
    snaps = sorted(glob.glob(os.path.join(os.path.dirname(__file__),
                                          'audits', 'seranking-????-??-??')))
    if snaps:
        latest = snaps[-1]
        date = os.path.basename(latest).replace('seranking-', '')
        age = (dt.date.today() - dt.date.fromisoformat(date)).days
        kw_file = os.path.join(latest, 'raw', 'keywords_ch.json')
        if age <= max_snapshot_age_days and os.path.exists(kw_file):
            with open(kw_file) as f:
                rows = json.load(f)
            print(f"   ✓ Our keywords from snapshot {date} ({age}d old): {len(rows)} rows")
            return {r['keyword'].lower().strip() for r in rows}
    rows, _ = client.domain_keywords_all(domain)
    print(f"   ✓ Our keywords from live SE Ranking pull: {len(rows)} rows")
    return {r['keyword'].lower().strip() for r in rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--domain', default=os.getenv('COMPANY_DOMAIN', 'magicheidi.ch'))
    ap.add_argument('--max-snapshot-age', type=int, default=14)
    ap.add_argument('--min-volume', type=int, default=50)
    ap.add_argument('--no-gsc', action='store_true', help='skip GSC cross-check')
    args = ap.parse_args()

    print("=" * 80)
    print("COMPETITOR CONTENT GAP ANALYSIS (SE Ranking)")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Strategy: Find keywords competitors rank for that we don't")
    print("=" * 80)

    print("\n1. Initializing data sources...")
    client = SERankingClient()
    print("   ✓ SE Ranking connected")

    scorer = OpportunityScorer()
    intent_analyzer = SearchIntentAnalyzer()
    print("   ✓ Analysis modules loaded")

    print("\n2. Fetching our current rankings...")
    our_keywords = our_keyword_set(client, args.domain, args.max_snapshot_age)

    # Optional GSC cross-check: also exclude anything we already get impressions for
    if not args.no_gsc:
        try:
            from modules.google_search_console import GoogleSearchConsole
            gsc = GoogleSearchConsole()
            gsc_rows = gsc.get_keyword_positions(days=90)
            gsc_set = {kw['keyword'].lower().strip() for kw in gsc_rows
                       if kw.get('impressions', 0) >= 10}
            print(f"   ✓ GSC cross-check: +{len(gsc_set - our_keywords)} extra keywords excluded")
            our_keywords |= gsc_set
        except Exception as e:
            print(f"   ⚠ GSC unavailable ({e}) — continuing with SE Ranking set only")

    all_competitors = list(dict.fromkeys(DIRECT_COMPETITORS + CONTENT_COMPETITORS))
    print(f"\n3. Analyzing {len(all_competitors)} competitors...")

    competitor_gaps = []
    seen_keywords = set()

    for i, competitor in enumerate(all_competitors, 1):
        comp_type = "Direct" if competitor in DIRECT_COMPETITORS else "Content"
        print(f"\n   [{i}/{len(all_competitors)}] Analyzing {competitor} ({comp_type})...")

        try:
            comp_keywords, _ = client.domain_keywords_all(
                competitor, max_pages=2,
                order_field="volume", order_type="desc",
                **{"filter[position][to]": 20,
                   "filter[volume][from]": args.min_volume})
            if not comp_keywords:
                print(f"      No data available for {competitor}")
                continue
            print(f"      Found {len(comp_keywords)} keywords they rank for (top 20)")

            gaps_found = 0
            for kw_data in comp_keywords:
                keyword = kw_data['keyword'].lower().strip()
                if (keyword in our_keywords or
                        keyword in seen_keywords or
                        is_branded_keyword(keyword, competitor)):
                    continue
                if not is_relevant_keyword(keyword):
                    continue
                seen_keywords.add(keyword)
                gaps_found += 1
                competitor_gaps.append({
                    'keyword': kw_data['keyword'],
                    'competitor': competitor,
                    'competitor_type': comp_type,
                    'competitor_position': kw_data.get('position', 99),
                    'competitor_url': kw_data.get('url', ''),
                    'search_volume': kw_data.get('volume', 0),
                    'cpc': kw_data.get('cpc', 0),
                    'difficulty': kw_data.get('difficulty', 50),
                    'serp_features': kw_data.get('serp_features') or [],
                    'intents': kw_data.get('intents') or [],
                    'your_position': None,
                })
            print(f"      Identified {gaps_found} gap opportunities")

        except Exception as e:
            print(f"      Error analyzing {competitor}: {e}")
            continue

    if not competitor_gaps:
        print("\n   No competitor gaps found!")
        return

    print(f"\n4. Scoring {len(competitor_gaps)} total gap opportunities...")

    enriched_gaps = []
    for gap in competitor_gaps:
        try:
            serp_features = gap['serp_features']
            intent_result = intent_analyzer.analyze(
                keyword=gap['keyword'], serp_features=serp_features)
            primary_intent = intent_result.get('primary_intent', 'unknown')
            if hasattr(primary_intent, 'value'):
                primary_intent = primary_intent.value
            gap['search_intent'] = str(primary_intent)
            gap['content_type'] = determine_content_type(gap['keyword'], serp_features)

            keyword_data = {
                'keyword': gap['keyword'],
                'position': 100,  # Not ranking
                'impressions': gap.get('search_volume', 0),
                'clicks': 0,
                'ctr': 0,
                'commercial_intent': calculate_commercial_intent_from_serp(intent_result),
            }
            score_result = scorer.calculate_score(
                keyword_data=keyword_data,
                opportunity_type=OpportunityType.NEW_CONTENT,
                search_volume=gap.get('search_volume'),
                difficulty=gap.get('difficulty'),
                serp_features=serp_features,
                cluster_value=50)
            gap['opportunity_score'] = score_result['final_score']
            gap['priority'] = score_result['priority']
            gap['score_breakdown'] = score_result['score_breakdown']
            enriched_gaps.append(gap)
        except Exception as e:
            print(f"   Error scoring '{gap['keyword']}': {e}")
            continue

    enriched_gaps.sort(key=lambda x: x['opportunity_score'], reverse=True)
    top_gaps = [g for g in enriched_gaps if g['priority'] not in ['SKIP', 'LOW']]

    print(f"\n   ✓ Analysis complete")
    print(f"   Total gaps found: {len(competitor_gaps)}")
    print(f"   High-value opportunities: {len(top_gaps)}")
    print(f"   [credits] estimated SE Ranking spend: {client.credit_report()['total_est_credits']:,}")

    print("\n" + "=" * 80)
    print("TOP 10 COMPETITOR GAP OPPORTUNITIES")
    print("=" * 80)

    for i, gap in enumerate(top_gaps[:10], 1):
        print(f"\n#{i} KEYWORD: {gap['keyword']}")
        print("-" * 80)
        print(f"Competitor: {gap['competitor']} (position {gap['competitor_position']})")
        print(f"Search Volume: {gap.get('search_volume', 'Unknown')}/month")
        print(f"Difficulty: {gap.get('difficulty', 'Unknown')}/100")
        print(f"Search Intent: {gap.get('search_intent', 'unknown')}")
        print(f"Content Type Needed: {gap.get('content_type', 'Guide')}")
        print(f"Opportunity Score: {gap['opportunity_score']:.2f}/100")
        print(f"Priority: {gap['priority']}")

    print(f"\n5. Writing report to research/competitor-gaps-{datetime.now().strftime('%Y-%m-%d')}.md...")
    write_markdown_report(top_gaps, len(competitor_gaps))

    print("\n" + "=" * 80)
    print("✅ COMPETITOR GAP ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review detailed report: research/competitor-gaps-{datetime.now().strftime('%Y-%m-%d')}.md")
    print(f"2. Prioritize top 5-10 gaps based on your content strategy")
    print(f"3. Create comprehensive content for each gap")
    print(f"4. Use /write [keyword] command to generate content briefs")


def is_branded_keyword(keyword: str, domain: str) -> bool:
    """Check if keyword is branded/specific to any competitor"""
    keyword_lower = keyword.lower()
    for comp in DIRECT_COMPETITORS + CONTENT_COMPETITORS:
        if comp.split('.')[0].lower() in keyword_lower:
            return True
    return False


def is_relevant_keyword(keyword: str) -> bool:
    """Filter for relevant industry keywords. Override relevant_terms for your niche."""
    keyword_lower = keyword.lower()

    if len(keyword) < 4:
        return False

    relevant_terms = [t.lower() for t in CONFIG.get('relevant_terms', [])]
    if relevant_terms and not any(term in keyword_lower for term in relevant_terms):
        return False

    spam_terms = [
        'porn', 'xxx', 'casino', 'pills', 'viagra',
        'weight loss', 'crypto', 'forex', 'loan'
    ]
    if any(term in keyword_lower for term in spam_terms):
        return False

    return True


def determine_content_type(keyword: str, serp_features: List[str]) -> str:
    """Determine what type of content is needed based on keyword and SERP"""
    keyword_lower = keyword.lower()

    if any(word in keyword_lower for word in ['best', 'top', 'list of', 'beste']):
        return 'Listicle/Comparison'
    if any(word in keyword_lower for word in ['how to', 'how do', 'guide', 'tutorial', 'wie ', 'anleitung']):
        return 'How-To Guide'
    if any(word in keyword_lower for word in ['what is', 'what are', 'meaning', 'definition', 'was ist']):
        return 'Definitional Guide'
    if any(word in keyword_lower for word in ['vs', 'versus', 'compared', 'comparison', 'difference between', 'vergleich']):
        return 'Comparison Article'
    if any(word in keyword_lower for word in ['calculator', 'tool', 'generator', 'template', 'rechner', 'vorlage']):
        return 'Tool/Resource Page'
    if 'people_also_ask' in str(serp_features).lower():
        return 'Comprehensive Guide'
    return 'Guide/Article'


def calculate_commercial_intent_from_serp(intent_result: Dict[str, Any]) -> float:
    """Convert search intent to commercial intent score (0.1-3.0)"""
    primary_intent = intent_result.get('primary_intent', 'informational')
    if hasattr(primary_intent, 'value'):
        primary_intent = primary_intent.value
    intent_map = {
        'transactional': 3.0,
        'commercial_investigation': 2.0,
        'commercial': 2.0,
        'informational': 1.0,
        'navigational': 0.5
    }
    return intent_map.get(str(primary_intent).lower(), 1.0)


def write_markdown_report(gaps: List[Dict[str, Any]], total_found: int):
    """Write detailed markdown report"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"research/competitor-gaps-{date_str}.md"

    with open(filename, 'w') as f:
        f.write(f"# Competitor Content Gap Analysis\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"**Data source:** SE Ranking (CH database)\n\n")
        f.write(f"**Strategy:** Identify proven demand areas where competitors rank but we don't\n\n")
        f.write(f"**Total Gaps Found:** {total_found}\n")
        f.write(f"**High-Value Opportunities:** {len(gaps)}\n\n")
        f.write("---\n\n")

        critical = [g for g in gaps if g['priority'] == 'CRITICAL']
        high = [g for g in gaps if g['priority'] == 'HIGH']
        medium = [g for g in gaps if g['priority'] == 'MEDIUM']

        f.write(f"## Summary by Priority\n\n")
        f.write(f"- **CRITICAL:** {len(critical)} opportunities\n")
        f.write(f"- **HIGH:** {len(high)} opportunities\n")
        f.write(f"- **MEDIUM:** {len(medium)} opportunities\n\n")
        f.write("---\n\n")

        f.write(f"## Top 20 Content Gap Opportunities\n\n")

        for i, gap in enumerate(gaps[:20], 1):
            f.write(f"### {i}. {gap['keyword']}\n\n")
            f.write(f"**Priority:** {gap['priority']}  \n")
            f.write(f"**Opportunity Score:** {gap['opportunity_score']:.2f}/100\n\n")
            f.write(f"#### Competitor Intel\n\n")
            f.write(f"- **Ranking Competitor:** {gap['competitor']} ({gap['competitor_type']})\n")
            f.write(f"- **Their Position:** {gap['competitor_position']}\n")
            if gap.get('competitor_url'):
                f.write(f"- **Their URL:** {gap['competitor_url']}\n")
            f.write(f"- **Your Position:** Not ranking (top 100)\n\n")
            f.write(f"#### Keyword Metrics\n\n")
            f.write(f"- **Search Volume:** {gap.get('search_volume', 'Unknown')}/month\n")
            f.write(f"- **SEO Difficulty:** {gap.get('difficulty', 'Unknown')}/100\n")
            if gap.get('cpc'):
                f.write(f"- **CPC:** ${gap['cpc']:.2f}\n")
            f.write(f"- **Search Intent:** {gap.get('search_intent', 'unknown')}\n")
            f.write(f"- **Content Type Needed:** {gap.get('content_type', 'Guide')}\n\n")

            if gap.get('score_breakdown'):
                f.write(f"#### Opportunity Analysis\n\n")
                breakdown = gap['score_breakdown']
                f.write(f"- Volume Score: {breakdown.get('volume_score', 0):.0f}/100\n")
                f.write(f"- Competition Score: {breakdown.get('competition_score', 0):.0f}/100\n")
                f.write(f"- Intent Score: {breakdown.get('intent_score', 0):.0f}/100\n\n")

            f.write(f"#### Recommended Action\n\n")
            f.write(f"Create comprehensive {gap.get('content_type', 'guide').lower()} targeting this keyword.\n\n")
            f.write(f"**Next Steps:**\n")
            f.write(f"1. Analyze top 10 ranking content for '{gap['keyword']}'\n")
            f.write(f"2. Identify content gaps and unique angles\n")
            f.write(f"3. Create detailed content outline\n")
            f.write(f"4. Write comprehensive, 2000+ word {gap.get('content_type', 'article').lower()}\n")
            f.write(f"5. Optimize for target keyword and related terms\n")
            f.write(f"6. Build internal linking strategy\n\n")

            if gap.get('serp_features'):
                f.write(f"**SERP Features Present:** {', '.join(gap['serp_features'][:5])}\n\n")
            f.write("---\n\n")

        f.write(f"## Implementation Strategy\n\n")
        f.write(f"### Phase 1: Quick Wins (Weeks 1-2)\n")
        f.write(f"Focus on CRITICAL priority gaps with lower difficulty:\n\n")
        quick_wins = [g for g in critical if g.get('difficulty', 100) < 50][:5]
        for i, gap in enumerate(quick_wins, 1):
            f.write(f"{i}. **{gap['keyword']}** - Difficulty: {gap.get('difficulty', 'Unknown')}, Volume: {gap.get('search_volume', 'Unknown')}\n")

        f.write(f"\n### Phase 2: High-Value Targets (Weeks 3-6)\n")
        f.write(f"Target HIGH priority gaps with strong search volume:\n\n")
        high_value = [g for g in high if g.get('search_volume', 0) > 500][:5]
        for i, gap in enumerate(high_value, 1):
            f.write(f"{i}. **{gap['keyword']}** - Volume: {gap.get('search_volume', 'Unknown')}, Difficulty: {gap.get('difficulty', 'Unknown')}\n")

        f.write(f"\n### Phase 3: Content Clusters (Weeks 7+)\n")
        f.write(f"Build topical authority by creating content clusters around related gaps.\n\n")

        f.write(f"## Key Insights\n\n")
        total_volume = sum(g.get('search_volume', 0) for g in gaps if g.get('search_volume'))
        difficulty_values = [g.get('difficulty') for g in gaps if g.get('difficulty')]
        if difficulty_values:
            avg_difficulty = sum(difficulty_values) / len(difficulty_values)
            difficulty_display = f"{avg_difficulty:.1f}/100"
        else:
            difficulty_display = "N/A"
        f.write(f"- **Total Potential Search Volume:** {total_volume:,}/month\n")
        f.write(f"- **Average SEO Difficulty:** {difficulty_display}\n")

        content_types = {}
        for gap in gaps:
            ct = gap.get('content_type', 'Unknown')
            content_types[ct] = content_types.get(ct, 0) + 1
        f.write(f"\n**Content Types Needed:**\n")
        for ct, count in sorted(content_types.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- {ct}: {count} articles\n")

        competitor_counts = {}
        for gap in gaps:
            comp = gap['competitor']
            competitor_counts[comp] = competitor_counts.get(comp, 0) + 1
        f.write(f"\n**Top Competitors to Learn From:**\n")
        for comp, count in sorted(competitor_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            f.write(f"- {comp}: {count} gap opportunities\n")

    print(f"   ✓ Report saved: {filename}")


if __name__ == "__main__":
    main()

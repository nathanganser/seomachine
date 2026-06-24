# Research Command

Use this command to conduct comprehensive SEO keyword research and competitive analysis before writing new content.

## Usage
`/research [topic]`

## What This Command Does
1. Fetches live keyword data and SERP results via DataForSEO
2. Analyzes top-ranking competitor content
3. Identifies content gaps and opportunities
4. Develops unique angle for Magic Heidi's positioning
5. Creates detailed research brief for writing

## Data Source: DataForSEO (NOT Ahrefs)

**Always use DataForSEO** for all keyword and SERP data. Never use the Ahrefs MCP tools.

### Detecting the keyword language
- Determine the language from the topic/keyword itself
- French keywords (contain accents, French words) → use `language_code="fr"`
- Italian keywords → use `language_code="it"`
- English keywords → use `language_code="en"`
- German keywords (default) → use `language_code="de"` (or omit, it's the default)
- Location is always Switzerland: `location_code=2756`

### Step 1 — SERP data for the primary keyword
```python
import sys
sys.path.insert(0, 'data_sources')
from dotenv import load_dotenv
load_dotenv('data_sources/config/.env')
from modules.dataforseo import DataForSEO

dfs = DataForSEO()
# For French keyword:
serp = dfs.get_serp_data("programme comptabilité suisse", language_code="fr")
print(f"Volume: {serp['search_volume']}, CPC: {serp['cpc']}, Competition: {serp['competition']}")
for r in serp['organic_results'][:10]:
    print(r['position'], r['domain'], r['title'], r['url'])
print("SERP features:", serp['features'])
```

### Step 2 — Related keyword ideas
```python
ideas = dfs.get_keyword_ideas("programme comptabilité suisse", language_code="fr", limit=50)
for kw in ideas[:20]:
    print(kw['keyword'], kw['search_volume'], kw['competition'])
```

### Step 3 — Question keywords (People Also Ask)
```python
questions = dfs.get_questions("programme comptabilité suisse", language_code="fr", limit=30)
for q in questions[:10]:
    print(q['keyword'])
```

### Step 4 — Magic Heidi's current ranking
```python
rankings = dfs.get_rankings(
    domain="magicheidi.ch",
    keywords=["programme comptabilité suisse", "logiciel comptabilité suisse"],
    language_code="fr"
)
for r in rankings:
    print(r['keyword'], r['position'], r['url'])
```

### Step 5 — Competitor comparison
```python
comp = dfs.analyze_competitor(
    competitor_domain="cresus.ch",
    keywords=["programme comptabilité suisse", "logiciel comptabilité indépendant suisse"],
    your_domain="magicheidi.ch",
    language_code="fr"
)
for c in comp['comparison']:
    print(c['keyword'], "Crésus:", c['competitor_position'], "MH:", c['your_position'])
```

Run all steps using inline Python via the Bash tool. Parse the output to build the research brief.

## Process

### Keyword Research (via DataForSEO)
- **Primary Keyword**: Identify main target keyword from the topic
- **Search Volume & Difficulty**: Pull live CH volume, CPC, competition score from DataForSEO SERP data
- **Keyword Variations**: Use `get_keyword_ideas()` to find semantic variations and long-tail opportunities
- **Related Questions**: Use `get_questions()` to discover People Also Ask queries
- **Search Intent**: Determine from SERP result types and titles (informational / commercial / transactional)
- **Topic Cluster**: Cross-reference with @context/target-keywords.md to place in existing cluster

### Competitive Analysis (via DataForSEO SERP data)
- **Top 10 SERP Review**: Extract from `get_serp_data()` organic_results — note domain, title, URL for each
- **SERP Features**: Note features array (featured_snippet, people_also_ask, video, etc.)
- **Common Themes**: What do top-ranking titles and domains have in common?
- **Content Gaps**: What's missing from competitor coverage?
- **Unique Angles**: What perspectives are underexplored?
- **Magic Heidi Position**: Use `get_rankings()` to find current position (if any)

### Context Integration
- **Magic Heidi Advantage**: How can Magic Heidi's features naturally enhance this content?
- **Brand Alignment**: Check @context/brand-voice.md for tone and messaging fit
- **Existing Content**: Review @context/internal-links-map.md for internal linking opportunities
- **Target Keywords**: Cross-reference with @context/target-keywords.md priority list
- **SEO Guidelines**: Ensure research aligns with @context/seo-guidelines.md requirements

### Swiss Freelancer Focus
- **Freelancer Angle**: How does this topic specifically impact Swiss independents?
- **Swiss-Specific Rules**: Any canton, TVA, AHV, or Swiss legal considerations?
- **Language Market**: Which language(s) does this serve? (German 70%, French 20%, Italian 5%, English 5%)
- **Pain Points**: What specific admin challenges do Swiss freelancers face with this topic?

### Content Planning
- **Recommended Structure**: Outline H2 and H3 headings based on SERP patterns
- **Content Depth**: Determine target word count (benchmark from top 10 average)
- **Supporting Evidence**: Identify statistics, Swiss legal references, or data to include
- **Internal Links**: Map 3-5 key Magic Heidi pages to link to (from @context/internal-links-map.md)
- **External Authority**: Identify 2-3 authoritative external sources (admin.ch, estv.admin.ch, six-group.com, etc.)

### Hook Development
- **Introduction Angle**: Compelling way to open the article
- **Value Proposition**: Clear benefit the reader will get
- **Contrarian Elements**: Any unexpected Swiss-specific perspectives
- **Story Opportunities**: Real freelancer scenarios to feature

## Output
Provides a comprehensive research brief with:

### 1. SEO Foundation
- **Primary Keyword**: [keyword] (volume, difficulty)
- **Secondary Keywords**: 3-5 related keywords and variations
- **Target Word Count**: Minimum words needed to compete
- **Featured Snippet Opportunity**: Yes/No, format (paragraph, list, table)

### 2. Competitive Landscape
- **Top 3 Competitor Articles**: URLs and key takeaways from each
- **Common Sections**: Must-cover topics based on SERP analysis
- **Content Gaps**: Opportunities to provide unique value
- **Differentiation Strategy**: How your company can stand out

### 3. Recommended Outline
```
H1: [Optimized headline with primary keyword]

Introduction
- Hook
- Problem statement
- Value proposition

H2: [Main section 1]
H3: [Subsection]
H3: [Subsection]

H2: [Main section 2]
...

Conclusion
- Key takeaways
- Call to action
```

### 4. Supporting Elements
- **Statistics to Include**: 5-7 relevant data points with sources
- **Expert Quotes**: Potential sources or existing quotes
- **Examples/Case Studies**: Real podcast scenarios to feature
- **Visual Suggestions**: Screenshots, charts, or graphics needed

### 5. Internal Linking Strategy
- **Pillar Page**: Main your company pillar content to link to
- **Related Articles**: 2-4 relevant blog posts to link
- **Product Pages**: your company features to naturally mention
- **Resource Pages**: Tools or guides to reference

### 6. Meta Elements Preview
- **Meta Title**: Draft optimized title (50-60 characters)
- **Meta Description**: Draft compelling description (150-160 characters)
- **URL Slug**: Recommended URL structure

## File Management
After completing the research, automatically save the brief to:
- **File Location**: `research/brief-[topic-slug]-[YYYY-MM-DD].md`
- **File Format**: Markdown with clear sections and structured data
- **Naming Convention**: Use lowercase, hyphenated topic slug and current date

Example: `research/brief-podcast-editing-software-2025-10-15.md`

## Next Steps
The research brief serves as the foundation for:
1. Running `/write [topic]` to create the optimized article
2. Reference material for maintaining SEO focus throughout writing
3. Checklist to ensure all competitive gaps are addressed

This ensures every article is built on solid SEO research and strategic competitive positioning.

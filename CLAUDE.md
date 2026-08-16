# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SEO Machine is an open-source Claude Code workspace for creating SEO-optimized blog content. It combines custom commands, specialized agents, and Python-based analytics to research, write, optimize, and publish articles for any business.

## Setup

```bash
pip install -r data_sources/requirements.txt
```

API credentials are configured in `data_sources/config/.env` (GSC, DataForSEO, SE Ranking, WordPress). Traffic analytics comes from manually-exported Vercel Web Analytics CSVs placed at the repo root (or any folder pointed to by `VERCEL_ANALYTICS_DIR`).

## Commands

All commands are defined in `.claude/commands/` and invoked as slash commands:

- `/research [topic]` - Keyword/competitor research, generates brief in `research/`
- `/write [topic]` - Create full article in `drafts/`, auto-triggers optimization agents
- `/rewrite [topic]` - Update existing content, saves to `rewrites/`
- `/optimize [file]` - Final SEO polish pass
- `/analyze-existing [URL or file]` - Content health audit
- `/performance-review` - Analytics-driven content priorities
- `/publish-draft [file]` - Publish to WordPress via REST API
- `/article [topic]` - Simplified article creation
- `/cluster [topic]` - Build complete topic cluster strategy with pillar + supporting articles + linking map
- `/priorities` - Content prioritization matrix
- `/research-serp`, `/research-gaps`, `/research-trending`, `/research-performance`, `/research-topics` - Specialized research commands
- `/research-ai-citations [topic]` - AI citation audit: generates prompts, clusters them, audits which sources AI cites
- `/repurpose [file]` - Adapts article for LinkedIn, Medium, Reddit, Quora distribution
- `/landing-write`, `/landing-audit`, `/landing-research`, `/landing-publish`, `/landing-competitor` - Landing page commands
- `/convert-to-components [file]` - Convert markdown landing page to Nuxt Content MDC component format, saves to `components-ready/`
- `/seranking-audit [date]` - Monthly SE Ranking snapshot: pull + analyze + compare vs previous + narrative audit
- `/backlinks [competitors]` - Backlink gap analysis + prioritized outreach prospect list
- `/keyword-research [seed]` - Keyword expansion (similar/related/questions/longtail) from the SE Ranking Swiss DB
- `/ai-visibility` - AI-search presence audit (ChatGPT/Perplexity/Gemini citations of magicheidi.ch)
- `/site-health` - SE Ranking technical site audit with prioritized fix list

## Architecture

### Command-Agent Model

**Commands** (`.claude/commands/`) orchestrate workflows. **Agents** (`.claude/agents/`) are specialized roles invoked by commands. After `/write`, these agents auto-run: SEO Optimizer, Meta Creator, Internal Linker, Keyword Mapper.

Key agents: `content-analyzer.md`, `seo-optimizer.md`, `meta-creator.md`, `internal-linker.md`, `keyword-mapper.md`, `editor.md`, `headline-generator.md`, `cro-analyst.md`, `performance.md`, `cluster-strategist.md`.

### Python Analysis Pipeline

Located in `data_sources/modules/`. The Content Analyzer chains:
1. `search_intent_analyzer.py` - Query intent classification
2. `keyword_analyzer.py` - Density, distribution, stuffing detection
3. `content_length_comparator.py` - Benchmarks against top 10 SERP results
4. `readability_scorer.py` - Flesch Reading Ease, grade level
5. `seo_quality_rater.py` - Comprehensive 0-100 SEO score

### Data Integrations

- `vercel_analytics.py` - Vercel Web Analytics traffic data, read from manually-exported CSVs ("Top Pages*.csv" and "Top Referrers*.csv") at the repo root. Supports 1/7/30/90-day windows; trend signals come from comparing windows.
- `google_search_console.py` - Rankings and impressions
- `dataforseo.py` - Live SERP top-10/50 scraping (defaults to Switzerland/German via env vars) — kept only for live SERP analysis; keyword metrics and positions come from SE Ranking
- `seranking.py` - SE Ranking Data API (primary source for rankings, keyword research, competitor gaps, backlinks, site audits, AI-search visibility). Swiss database (`source="ch"`). Auth: `SERANKING_API_KEY`
- `data_aggregator.py` - Combines all sources into unified analytics
- `wordpress_publisher.py` - Publishes to WordPress with Yoast SEO metadata

### Opportunity Scoring

`opportunity_scorer.py` uses 8 weighted factors: Volume (25%), Position (20%), Intent (20%), Competition (15%), Cluster (10%), CTR (5%), Freshness (5%), Trend (5%).

## Running Python Scripts

```bash
# Research & analysis scripts (run from repo root)
python3 research_quick_wins.py
python3 research_competitor_gaps.py
python3 research_performance_matrix.py
python3 research_priorities_comprehensive.py
python3 research_serp_analysis.py
python3 research_topic_clusters.py
python3 research_trending.py
python3 seo_baseline_analysis.py
python3 seo_bofu_rankings.py
python3 seo_competitor_analysis.py

# SE Ranking tools (run from repo root)
python3 seranking_pull_data.py --date YYYY-MM-DD    # full snapshot → audits/seranking-<date>/raw/
python3 seranking_analyze.py --date YYYY-MM-DD      # CSVs + summary.md from a snapshot
python3 seranking_compare.py                        # diff two snapshots → comparison md + movers.csv
python3 seranking_site_audit.py create|status|fetch # technical crawl
python3 seranking_backlinks.py                      # outreach prospect list
python3 seranking_keyword_research.py ideas <seed>  # keyword expansion
python3 seranking_ai_visibility.py                  # AI-search presence

# Test API connectivity
python3 test_dataforseo.py
```

## SE Ranking (Data API)

Primary SEO data source (migrated from DataForSEO 2026-08-16; DataForSEO remains only for live SERP scraping in `/research-serp` and `content_length_comparator.py`).

- **Snapshots**: `audits/seranking-YYYY-MM-DD/` (raw JSON + analysis CSVs + `meta.json` with completeness flags and credit estimates). Monthly cadence via `/seranking-audit` — next re-measure 2026-09-01. Comparisons are truncation-aware: only trust "LOST" labels when `meta.json` says the keyword pull was complete.
- **Swiss database**: `source="ch"` default for all languages (French/Italian seeds work against the same DB).
- **Credits**: prepaid Data API credits (~3M as of 2026-08-16); every script prints an estimated spend. The 7,500-credit AI leaderboard call is gated behind explicit flags.
- **Caveat**: the platform subscription expired 2026-08-16 — the Data API keeps working on prepaid credits, but the Project API (`/projects` rank tracker) returns 401 and the account `units_left` counter can be stale.
- **Competitor set**: `seranking_competitors` in `config/competitors.json` (kept aligned with the committed 2026-08-01 baseline for apples-to-apples comparisons); `money_keyword_families` there drives the movers section of snapshot comparisons.

## Content Pipeline

`topics/` (ideas) → `research/` (briefs) → `drafts/` (articles) → `review-required/` (pending review) → `published/` (final)

Rewrites go to `rewrites/`. Landing pages go to `landing-pages/`. Component-ready landing pages go to `components-ready/`. Audits go to `audits/`. Repurposed content goes to `repurposed/`.

## Context Files

`context/` contains brand guidelines that inform all content generation:
- `brand-voice.md` - Tone, messaging pillars
- `style-guide.md` - Grammar, formatting standards
- `seo-guidelines.md` - Keyword and structure rules
- `internal-links-map.md` - Key pages for internal linking
- `features.md` - Product features
- `competitor-analysis.md` - Competitive intelligence
- `cro-best-practices.md` - Conversion optimization guidelines
- `ai-citation-targets.md` - Directories/platforms where your brand should be cited by AI tools
- `reddit-strategy.md` - Reddit engagement strategy for AI SEO and community visibility

## Target Market & Locale

Magic Heidi targets **Switzerland** with a multilingual content strategy:
- **German (de)**: 70% — primary market, default for DataForSEO
- **French (fr)**: 20% — second market
- **Italian (it)**: 5%
- **English (en)**: 5%

DataForSEO is configured via env vars (`DATAFORSEO_LOCATION_CODE=2756`, `DATAFORSEO_LANGUAGE_CODE=de`). When researching keywords or analyzing SERPs:
- Default calls use Swiss/German locale automatically
- For French content, pass `language_code="fr"` explicitly to DataForSEO methods
- Determine the language from the keyword/topic: if the user passes a French keyword, use `language_code="fr"`; if German, use the default
- Swiss location code `2756` applies to all languages (it's the country, not the language)

## WordPress Integration

Publishing uses the WordPress REST API with a custom MU-plugin (`wordpress/seo-machine-yoast-rest.php`) that exposes Yoast SEO fields. Articles are published in WordPress block format (HTML comments in Markdown files).

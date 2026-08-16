# Research Gaps Command

Identify content gaps where competitors rank but you don't.

## Usage
`/research-gaps`

## What This Command Does

Analyzes 7 competitors to find keywords they rank for (top 20) that you don't rank for at all:
- **Direct Competitors**: Configured in `config/competitors.json` or passed as arguments
- **Content Competitors**: Industry blogs and media sites in your niche

For each gap:
- Filters out branded/irrelevant keywords
- Scores opportunity based on volume, difficulty, and intent
- Determines content type needed (listicle, how-to, guide)
- Prioritizes by potential impact

## Process

Execute the competitor gap analysis:
```bash
python3 research_competitor_gaps.py
```

This will:
1. Load our full top-100 keyword universe from the latest `audits/seranking-*/` snapshot (or a live SE Ranking pull if the snapshot is >14 days old)
2. Cross-check against GSC impressions (optional, `--no-gsc` to skip)
3. Analyze each competitor's top 20 ranking keywords via SE Ranking
4. Identify gaps (they rank, you don't) — volume, difficulty, intents, and SERP features come with the rows, no per-keyword SERP calls
5. Score and prioritize opportunities
6. Generate report: `research/competitor-gaps-YYYY-MM-DD.md`

## Output

The report includes:
- Top 20 content gap opportunities
- Priority level (CRITICAL/HIGH/MEDIUM)
- Competitor intel (who ranks, at what position)
- Keyword metrics (volume, difficulty, CPC)
- Search intent and content type needed
- Specific action steps for each gap

## Integration

After running `/research-gaps`:
- Use `/research-serp [keyword]` to analyze what ranks
- Use `/write [keyword]` to create content brief
- Focus on CRITICAL/HIGH priority gaps first

## Time & Cost

**Time:** 2-3 minutes
**API Cost:** ~1,500 SE Ranking credits (competitor keyword pulls; our side is free when a fresh snapshot exists)

## When to Run

- **Monthly**: Full competitive landscape review
- **When entering new topic**: Find what's missing
- **Before content planning**: Identify proven opportunities

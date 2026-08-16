# SE Ranking Audit Command

Monthly SEO snapshot: pull the full SE Ranking dataset, analyze it, compare against the previous snapshot, and write a narrative audit with actions.

## Usage
`/seranking-audit` — snapshot for today, compared against the most recent previous snapshot
`/seranking-audit 2026-09-01` — snapshot for a specific date

## What This Command Does

Creates a reproducible dated snapshot in `audits/seranking-YYYY-MM-DD/` covering rankings, position buckets, traffic estimates, cannibalization, locale leaks, quick wins, competitor gaps, and backlinks — then diffs it against the previous snapshot (movers, NEW/LOST keywords, locale-leak trend, anomalies).

## Process

1. **Pull the snapshot** (uncapped keyword pagination, writes `meta.json` with completeness flags and credit report):
```bash
python3 seranking_pull_data.py --date <date>
```

2. **Analyze it** (cannibalization.csv, locale_leaks.csv, quick_wins.csv, striking_distance/gap CSVs, top_pages.csv, summary.md):
```bash
python3 seranking_analyze.py --date <date>
```

3. **Compare vs previous snapshot** (comparison-vs-<baseline>.md + movers.csv; LOST keywords are truncation-aware via meta.json):
```bash
python3 seranking_compare.py --date <date>
```

4. **Write the narrative audit**: read `summary.md`, `comparison-vs-*.md`, `quick_wins.csv`, `cannibalization.csv`, and `movers.csv`, then write `audits/seranking-audit-<date>.md` with:
   - Headline movement (traffic, buckets, money keywords) and what caused it
   - Regressions needing action (position drops ≥5 on vol ≥300, lost #1s) — cross-reference against active campaigns in memory/context
   - Top 5 quick wins and top cannibalization groups with concrete fix recommendations
   - Locale-leak trend commentary (/de/ → bare URL migration progress)
   - Anything to verify manually (LOST rows flagged pull-truncated)

## Output

- `audits/seranking-<date>/` — raw JSON + analysis CSVs + summary.md + comparison + movers.csv
- `audits/seranking-audit-<date>.md` — narrative audit with prioritized actions

## Integration

- Feed quick wins into `/priorities`
- Feed gap CSVs into `/research-gaps` follow-ups and `/write`
- Regressions on money keywords → `/rewrite` or `/optimize` the affected page

## Time & Cost

**Time:** 5-10 minutes
**API Cost:** ~4,500 SE Ranking credits (overview + ~11 keyword pages + pages + competitors + 5× gap + backlinks)

## When to Run

- **Monthly** (the 1st) — this is the standing re-measure cadence
- After major site changes (locale switches, migrations, big content pushes)

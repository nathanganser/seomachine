# Backlinks Command

Backlink gap analysis and prioritized outreach prospect list via SE Ranking.

## Usage
`/backlinks` — gap vs configured competitors (`seranking_competitors` in `config/competitors.json`)
`/backlinks bexio.com,klara.ch` — specific competitors
`/backlinks --min-competitors 1` — looser prospect filter (domains linking to any one competitor)

## What This Command Does

Pulls referring domains for magicheidi.ch and each competitor, then builds a prospect list: domains that link to ≥2 competitors but NOT to us, sorted by authority, with junk/platform domains filtered out. Then turns the raw list into a prioritized outreach plan.

## Process

1. **Pull data and build the prospect list**:
```bash
python3 seranking_backlinks.py            # add --competitors / --min-competitors / --max-rows as needed
```

2. **Prioritize and plan outreach**: read `outreach/backlink-prospects-<date>.csv` and `outreach/backlink-gap-summary-<date>.md`, cross-reference existing outreach dossiers in `outreach/` and the active keyword campaigns, then write `outreach/backlink-plan-<date>.md` with:
   - Top 15-25 prospects grouped by type (directories, blogs/media, associations, tool round-ups)
   - A concrete angle per domain (what content of ours fits, which page to pitch, which campaign it supports)
   - Which prospects support pages currently stuck on page 2 (check the latest quick_wins.csv)
   - Skip-list rationale for high-DR but unpitchable domains

## Output

- `outreach/backlink-prospects-<date>.csv` — refdomain, DR, which competitors it links to
- `outreach/backlink-gap-summary-<date>.md` — authority gap table + top 25 prospects
- `outreach/backlink-plan-<date>.md` — prioritized plan with per-domain angles
- `outreach/backlink-raw-<date>/` — raw refdomain JSON per domain

## Integration

- Prospects supporting active keyword campaigns get outreach priority
- Re-run monthly during campaigns to catch new competitor links
- Pair with `/repurpose` for linkable-asset angles

## Time & Cost

**Time:** 3-5 minutes
**API Cost:** ~2,000-6,000 SE Ranking credits (per-row refdomain billing, capped at `--max-rows` per domain, default 2,000)

## When to Run

- **During outreach campaigns**: monthly
- **When a page is stuck on page 2** and on-page work is done — links are usually the blocker

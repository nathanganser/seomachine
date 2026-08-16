# Site Health Command

Technical SEO crawl of magicheidi.ch via the SE Ranking site audit.

## Usage
`/site-health` — kick off a crawl, poll until done, fetch and summarize
`/site-health fetch <audit_id>` — fetch a crawl that already finished

## What This Command Does

Runs SE Ranking's standard site audit (crawl capped at 1,500 pages), pulls the full report plus the affected-page list for every error/warning, and writes a prioritized fix list.

## Process

1. **Create the audit**:
```bash
python3 seranking_site_audit.py create           # prints audit_id
```

2. **Poll until the crawl finishes** (typically 10-30 minutes — check every few minutes):
```bash
python3 seranking_site_audit.py status <audit_id>
```

3. **Fetch report + issue pages**:
```bash
python3 seranking_site_audit.py fetch <audit_id>
```

4. **Summarize**: read `audits/seranking-<date>/raw/audit_report.json` and `audit_issue_pages.json`, then write `audits/site-health-<date>.md`:
   - Overall health score + delta vs the previous audit (compare with the last `audit_report.json` in older snapshots)
   - Errors first, warnings second — grouped by issue type with affected page counts and example URLs
   - Concrete fix per issue type, flagging which are template-level (one fix, many pages) vs per-page
   - Ignore-list for known false positives (note them explicitly)

## Output

- `audits/seranking-<date>/raw/audit_report.json` + `audit_issue_pages.json`
- `audits/site-health-<date>.md` — prioritized fix list

## Integration

- Template-level fixes → mh-landing repo changes
- Per-page content issues → `/optimize` or `/rewrite`
- Re-run after shipping fixes to confirm the score moved

## Time & Cost

**Time:** 15-40 minutes (mostly crawl wait)
**API Cost:** ~3,000 SE Ranking credits (2 credits/page × up to 1,500 pages)

## When to Run

- **Monthly**, or after structural site changes (redirects, locale changes, template updates)

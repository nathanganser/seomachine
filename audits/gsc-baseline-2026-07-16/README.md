# GSC Baseline Export — Pre-Migration (2026-07-16)

Google Search Console baseline for **magicheidi.ch** (property `sc-domain:magicheidi.ch`), captured **before** the default-locale migration.

## Why this export exists

The site is about to switch its default locale on bare URLs:

- **Before (current state, captured here):** bare URLs (`magicheidi.ch/...`, no locale prefix) serve **English**; German lives under `/de/*`.
- **After migration:** bare URLs serve **German**; English moves to `/en/*`.

This snapshot is the reference point for measuring the migration's impact on clicks, impressions, CTR, and positions — especially for bare-path pages (whose content language changes) and `/de/*` pages (which will presumably redirect/consolidate into bare URLs).

## Scope

- Date range: **2026-04-17 to 2026-07-16** (last 90 days)
- Source: GSC Search Analytics API via `data_sources/modules/google_search_console.py`
- All rows fetched with pagination (25k rows/request)

## Files

| File | Contents |
|---|---|
| `pages_queries_90d.csv` / `.json` | Query-level data grouped by page: page, query, locale_bucket, clicks, impressions, ctr, position (106,322 rows) |
| `top_pages_90d.csv` / `.json` | Page-level totals: page, locale_bucket, clicks, impressions, ctr, position (2,605 pages) |
| `pages_queries_bare.csv` | Page+query rows for bare-path pages only (English today, German after migration) |
| `pages_queries_de.csv` | Page+query rows for `/de/*` pages only |
| `pages_queries_other_locales.csv` | Page+query rows for `/fr/*`, `/it/*`, `/es/*`, `/pt/*` pages |
| `pages_queries_subdomains.csv` | Rows on other hosts of the domain property (`app.`, `www.`, `help.`) — not affected by the migration |
| `summary.json` | Machine-readable totals per bucket |
| `gsc_baseline_export.py` | The script that produced this export (re-run from repo root after migration for the comparison snapshot) |

## Locale buckets

`locale_bucket` column in the combined files (and the per-bucket split files):

- `bare` — path has no locale prefix, host is `magicheidi.ch` (the pages whose language flips EN→DE)
- `de` — path starts with `/de/`
- `other_locale` — path starts with `/fr/`, `/it/`, `/es/`, or `/pt/`
- `subdomain` — host is not `magicheidi.ch` (e.g., `app.magicheidi.ch`); unaffected by the migration

## Baseline totals (90 days)

| Bucket | Pages | Page+query rows | Clicks | Impressions |
|---|---:|---:|---:|---:|
| bare | 477 | 24,001 | 3,488 | 915,049 |
| /de/ | 494 | 33,928 | 6,196 | 869,787 |
| other locales (fr/it/es/pt) | 1,607 | 48,338 | 16,835 | 2,053,437 |
| subdomains | 27 | 55 | 76 | 2,639 |
| **Total** | **2,605** | **106,322** | **26,595** | **3,840,912** |

Note: GSC data has a ~2-day reporting lag, so the last day or two of the range may be partial.

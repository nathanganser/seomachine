# Site Health — magicheidi.ch — 2026-08-16

SE Ranking standard audit #323689 (crawl 10:26–10:38 UTC, 1,500-page cap hit; Google indexes ~1,860).
Raw: `audits/verify-2026-08-16/raw/audit_report.json` + `audit_issue_pages.json`.

**Health score: 81%** · 489 errors · 2,548 warnings · DT 52 · CWV green on mobile+desktop (LCP 92% good, CLS 93%, INP 96%).

## Fixed today (2026-08-16, in mh-landing working tree)

- **Internal links to 3XX (929 flagged)** — root cause found: 114 in-content links still pointed at the legacy `/invoicing` slug (301→`/rechnungsprogramm`) across 69 files in all locales + syntaxes (markdown, hardcoded HTML hrefs, YAML CTA props). All replaced with the final URL. Remaining 3xx-links are the `/duplication` links in non-DE locales, which resolve to live localized pages (no redirect) — false positives of the bare-path pattern.
- `/it/commerce-register-switzerland-2026` title/description sharpened (registro di commercio push) + 5 new inbound IT links.

## Priority fixes (template-level → mh-landing)

1. **90 pages with 4XX images** (`images4xx`) — spread across all locales, worst on bare + en. Needs an image-path audit; likely `{locale}`-suffixed webp variants that don't exist for some locales (e.g. `/sq/rechnungsprogramm`, `/sr/rechnungsprogramm` flagged). Fix in components/content where the named images 404.
2. **8 duplicate titles** (`title_duplicate`, down from 34 on 2026-08-01) — the `/start` family (`/start`, `/en/start`, `/sq/start`, `/sr/start`, …): one shared title across locales. Localize the title or noindex the thin locale variants of `/start`.
3. **2 missing titles / 7 missing descriptions / 6 missing H1** — small per-page list, fold into next content pass.
4. **96 temporary redirects (302/303/307)** — check `netlify.toml`/`vercel.json`/nuxt routeRules for temporary-redirect rules that should be 301 (e.g. `/sitemap.xml` → `sitemap_index.xml` is a 307).
5. **377 oversized images** — batch-compress worst offenders when convenient; CWV is already green, so low urgency.

## Accepted / ignore list (do NOT "fix")

- **sq/sr locales are intentional**, not rogue: fully configured in `nuxt.config.ts` (Shqip; Bosanski/Hrvatski/Srpski) with genuinely translated content (46 + 80 files), robots Allow, own sitemaps. Earlier workspace notes calling them nonexistent were wrong — corrected.
- **`hreflang_different` (58, of which 57 = /sr/)**: by design — /sr/ pages declare hreflang sr-CH + hr-CH + bs-CH pointing to the same URL to serve all three communities. Leave.
- **`hreflang_return` (32)**: spot-checked `/blog/dachdecker-rechnung-schweiz` — hreflang sets are reciprocal live; likely crawl-timing artifacts. Re-check next audit before acting.
- **941 external links to 4XX**: mostly aged outbound references; harvest-and-fix opportunistically during rewrites, not as a campaign.

## Structural finding (needs design, not a quick fix)

**349 orphan pages** (`no_inlinks`) — dominated by non-DE locales (it/es/pt/fr translations of blog posts and niche pages that nothing links to). Root cause: internal linking happens German-first; translations inherit no inbound links. Options (decide post-2026-09-01): a related-articles component rendered per-locale, or locale-aware hub pages. Until then, every new translation should ship with at least 2 inbound links from its own locale (done today for the IT registro page and the new IT translations get linked from their locale's `/alternative` index if present).

## Next audit

Monthly cadence — run `/site-health` again ~2026-09-16, or after the sq/sr-title and image fixes deploy. Compare against this report; score target ≥85%.

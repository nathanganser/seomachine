# Competitor campaign QA — 2026-07-19

Scope: German competitor-intent campaign for Magic Heidi, implemented in `mh-landing` on branch `agent/competitor-keywords-2026-07`.

## Routes

- Refreshed: `/alternative/bexio`, `/alternative/klara`, `/alternative/banana`, `/alternative/cashctrl`, `/alternative/abaninja`, `/bexio-preise`
- Created: `/alternative/accounto`, `/alternative/einzly`, `/alternative/swiss21`, `/alternative/sevdesk`, `/alternative/lexoffice`, `/alternative/zervant`
- Supporting hubs: `/alternative`, `/buchhaltungssoftware`

## Verification

- Official-source profiles and dated source ledgers completed for all competitors.
- Independent factual, editorial, and UWG-risk review completed; broken internal links, duplicate H1, stale prices, unsupported timing claims, and overbroad comparison claims corrected.
- Eleven modified competitor profiles parse as YAML.
- All twelve content files have balanced MDC component delimiters.
- SEO titles are 50–60 characters; descriptions are 146–160 characters.
- All twelve browser tests pass: 200 response, `de-CH`, exactly one H1, canonical URL, visible `/start` CTA.
- Representative desktop and mobile screenshots show meaningful rendered content and responsive layouts.
- Nuxt production build and campaign-route prerender pass. Shared OG generation now references its public logo directly instead of the unavailable prerender image-transform route.
- `git diff --check` passes.

## Scoring note

The legacy landing-page scorer does not parse MDC component headings, CTAs, trust blocks, or body copy reliably. The three new Swiss pages score 82.2. On other MDC-heavy pages it emits false missing-H1/CTA failures, so rendered browser assertions and the independent review are the release gate.

## Known repository-level warnings

- `nuxt typecheck` is blocked by the repository's current Node 25 / `vue-tsc` / TypeScript package-export incompatibility.
- Nuxt Studio OAuth, Sentry database instrumentation, duplicate locale keys, and sourcemap warnings predate this campaign and do not block prerender.

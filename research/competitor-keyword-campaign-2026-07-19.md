# Competitor Keyword Campaign — 2026-07-19

German-first campaign for tracked competitor queries. One canonical page owns each intent cluster; no modifier-specific duplicates are allowed.

| Keyword | Volume | Baseline | Canonical owner | Action | Workstream | Verified | Status |
|---|---:|---:|---|---|---|---|---|
| bexio | 60,500 | — | `/alternative/bexio` | refresh | integration | 2026-07-19 | PR-ready |
| bexio preise | 10 | 13 | `/bexio-preise` | optimize | integration | 2026-07-19 | PR-ready |
| klara buchhaltung | 210 | — | `/alternative/klara` | refresh | existing-page refresh | 2026-07-19 | PR-ready |
| klara erfahrungen | 10 | — | `/alternative/klara` | refresh | existing-page refresh | 2026-07-19 | PR-ready |
| klara kosten | 10 | — | `/alternative/klara` | refresh | existing-page refresh | 2026-07-19 | PR-ready |
| banana buchhaltung | 910 | — | `/alternative/banana` | refresh | existing-page refresh | 2026-07-19 | PR-ready |
| cashctrl | 80 | — | `/alternative/cashctrl` | refresh | existing-page refresh | 2026-07-19 | PR-ready |
| cashctrl erfahrungen | 20 | — | `/alternative/cashctrl` | refresh | existing-page refresh | 2026-07-19 | PR-ready |
| accounto | 590 | — | `/alternative/accounto` | create | Swiss competitors | 2026-07-19 | PR-ready |
| einzly | 30 | 30 | `/alternative/einzly` | create | Swiss competitors | 2026-07-19 | PR-ready |
| einzly erfahrungen | 0 | — | `/alternative/einzly` | create | Swiss competitors | 2026-07-19 | PR-ready |
| swiss21 | 610 | — | `/alternative/swiss21` | create | Swiss competitors | 2026-07-19 | PR-ready |
| swiss21 erfahrungen | 20 | — | `/alternative/swiss21` | create | Swiss competitors | 2026-07-19 | PR-ready |
| sevdesk schweiz | 50 | — | `/alternative/sevdesk` | create | DACH competitors | 2026-07-19 | PR-ready |
| lexoffice schweiz | 10 | — | `/alternative/lexoffice` | create | DACH competitors | 2026-07-19 | PR-ready |
| zervant | 10 | — | `/alternative/zervant` | create | DACH competitors | 2026-07-19 | PR-ready |
| abaninja erfahrungen | 20 | 11 | `/alternative/abaninja` | refresh | existing-page refresh | 2026-07-19 | PR-ready |

## Guardrails

- `milkee` and `milkee erfahrungen` are explicitly excluded because Milkee is a sister company.
- Preserve the page-one owners for `bexio kosten`, `bexio erfahrungen`, `klara alternative`, `abaninja`, `abaninja alternative`, `infinity swiss`, `infinity swiss erfahrungen`, `atlanto erfahrungen`, and `smallinvoice`.
- Every factual competitor price or feature claim must have an official source and a visible verification date.
- Every new route needs at least two contextual inbound links before publication.
- German uses bare URLs; `/de/*` must not be introduced.
- Research and source artifacts remain in this repository after publication for traceability.

## Release gates

- Competitor profile and source ledger complete.
- Independent accuracy/UWG review complete.
- Landing-page content score at least 75 after no more than two revision cycles.
- MDC/YAML, links, images, canonical, hreflang, schema, responsive layout, build, and smoke checks pass.
- Vercel preview reviewed before merge.

## QA record

- Multi-agent writing workstreams: Swiss competitors, DACH competitors, and existing-page refresh.
- Independent factual, editorial, and UWG-risk review completed 2026-07-19; all blocker and high-priority content findings resolved before PR.
- Twelve campaign routes pass browser checks for HTTP 200, German locale, one H1, canonical URL, and visible `/start` CTA.
- Metadata, YAML, MDC component balance, internal routes, media assets, and production prerender verified locally.
- The legacy landing-page scorer is not MDC-aware. New Swiss pages scored 82.2; deterministic rendered-page QA is the acceptance gate for pages where the scorer reports false missing-heading/CTA failures.
- Final publication state and PR URL are recorded after the Vercel preview gate.

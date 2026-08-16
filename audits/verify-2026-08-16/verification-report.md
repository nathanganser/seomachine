# Premise Verification & Diagnosis — 2026-08-16

Phase 0 of the verify-first plan (`~/.claude/plans/plan-the-implementation-for-floating-castle.md`).
Sources: fresh GSC daily pulls (`raw.json`, committed this time), DataForSEO live SERPs (`serp_results.json`), live curl checks, SE Ranking site audit #323689 (report fetched separately).

## Verdict on the external action plan's premises

| Premise | Verdict | Evidence |
|---|---|---|
| /en/ pages dropped July 20–26 | **REFUTED — nothing existed to drop.** | /en/ URLs had **zero** GSC impressions before W29 (mid-July): they were *created* by the default-locale migration and have grown since (542 → ~4,500 impr/wk, pos 21.9 → 12.4). No decline event exists. |
| German QR-Vorlage cluster dropped | **Mostly artifact.** | `qr einzahlungsschein erstellen gratis` genuinely fell to #37 (was #1 per SE Ranking); the rest of the QR set is stable. Low volume; fold into the QR-pillar quick-win pass, not a P1. |
| `software fatturazione artigiani` fell #2→#25 | **Partially real, tiny.** | Live SERP: #29 (`/it/buchhaltungssoftware`); GSC shows 11 impressions in 6 weeks. Real keyword, negligible size — not a sprint driver. |
| Bexio brand-term losses | **REFUTED.** | `bexio api` recovered to **#9** on its own; `bexio erfahrungen` improved (16.4→9.9). No loss cluster. |
| Near-top-3 group (user's four keywords) | **CONFIRMED (mostly).** | Live SERP: `beste buchhaltungssoftware schweiz` **#6** (`/buchhaltungssoftware` — held page), `klara erfahrungen` **#8** (`/alternative/klara`), `invoicing software switzerland` **#5** (bare `/ranking-simplest-rechnungssoftware-2026`) + #10 `/en/kostenlose-rechnungssoftware-schweiz`. `zahlungsfrist rechnung schweiz`: NOT in top 100 (claim wrong; milkee sits #5). `mahngebühren schweiz`: #53 live (GSC avg 12.1 — decaying). These were invisible to the repo because SE Ranking's CH database doesn't carry them — **GSC/live SERP must supplement SE Ranking for the push list.** |

## LOST-label audit (SE Ranking 2026-08-16 movers)

| Keyword | movers.csv said | Live SERP | Verdict |
|---|---|---|---|
| `rechnungsvorlage schweiz` (480/mo) | LOST (was 8) | **#7** `/rechnungsvorlage` | Pull artifact — fine, held page, no action |
| `buchhaltungsprogramm` (320/mo) | LOST (was 69) | **#26** `/buchhaltungssoftware` | Pull artifact — improved |
| `erfolgsrechnung` (1,000/mo) | LOST (was 26) | #70 `/erfolgsrechnung-schweiz` | Genuine slide 26→70; backlog, not urgent |
| `qr einzahlungsschein erstellen gratis` | LOST (was #1) | #37 `/qr-rechnung-erstellen` | Genuine drop; QR-pillar pass |

**Treat SE Ranking "LOST" labels as unreliable** — 2 of 4 were artifacts. `seranking_compare.py`'s truncation caveat is warranted.

## Confirmed diagnoses

1. **`/mwst-schweiz` is the #1 fix.** index,follow, self-canonical, in de-CH sitemap, but **zero impressions in 14 days** and `mwst schweiz` (4,400/mo) is not even in the top 100 (`/mwst-registrierung`'s old #40 also gone). Google simply hasn't adopted the page. → internal links from MWST cluster + footer, user requests indexing in GSC UI.
2. **`mwst sätze` "1→43" was never a traffic asset — deprioritized.** GSC shows ~0 impressions for `mwst sätze*` queries site-wide before W29 even while SE Ranking read pos 1 (on `/de/tools/vat-calculator-switzerland`, per Aug-1 locale_leaks). The pos-1 reading was a sampling artifact. `/vat-rates` sits ~45–59 with 1–2 impressions/day. Not worth a dedicated fix; the MWST-cluster linking pass covers it.
3. **Rogue locales sq/sr are institutionalized, not residual.** Every page emits hreflang alternates to `/sr/…` (as sr-CH, hr-CH **and** bs-CH); robots.txt explicitly `Allow: /sq/ /sr/`; `sitemap_index.xml` submits `sq-CH.xml` + `sr-CH.xml`. `/sr/vat-rates` serves 200 and collects impressions. This multiplies every URL ×8 locales for crawl/dedup. → template-level fix in mh-landing (i18n config, robots, sitemap), fold into site-health PR.
4. **Redirect layer is healthy.** `/vat-rates-2025` → `/vat-rates` 301 works incl. locale variants; canonicals self-reference; lingering GSC impressions on `-2025` URLs are Google lag, not a bug.
5. **`/bexio-preise`**: technically clean, pos ~8.8, 0 clicks — CTR problem confirmed; title/meta pass proceeds.
6. **IT is stable** (~260 clicks/wk, no dip; W33 low is a partial week). The registro-commercio quick win stands (`registro di commercio` 18,100/mo #12).

## Gate outcomes → actions

- **Gate EN: closed.** No recovery track; EN = quick-win pass only (`invoicing software switzerland` #5 protection, `vat number switzerland` @9).
- **Gate LOST: closed.** Only `erfolgsrechnung` + QR-gratis term are real; backlog.
- **Gate mwst sätze: closed — deprioritized** (see #2).
- **Gate IT-artigiani: closed.** Real but tiny; IT sprint proceeds on registro-commercio + translations + first IT keyword research.
- **Gate site-health: pending** audit #323689 fetch; sq/sr + duplicate titles already confirmed independently.

## Revised near-top-3 push list (replaces both earlier lists)

| Keyword | Vol | Pos | Page | Constraint |
|---|---|---|---|---|
| `klara erfahrungen` | — | #8 | `/alternative/klara` | free to edit |
| `invoicing software switzerland` | — | #5 | bare ranking page + `/en/kostenlose-rechnungssoftware-schweiz` #10 | protect, light touch |
| `registro di commercio` | 18,100 | #12 | `/it/commerce-register-switzerland-2026` | free to edit |
| `uid register` / `uid schweiz` / `uid number` | 8,000/590/480 | @9 | UID cluster | free to edit |
| `ubs qr code` / `ubs qr rechnung erstellen` | 590/480 | @5–6 | QR pillar / banks-ubs | free to edit |
| `vat number switzerland` / `swiss vat number` | 590/590 | @9–10 | `/mwst-registrierung` | free to edit |
| `beste buchhaltungssoftware schweiz` | — | #6 | `/buchhaltungssoftware` | **HELD until 2026-09-01** |
| `brutto netto rechner schweiz` | 3,600 | @5 | calculator | free to edit |

Dropped: `zahlungsfrist rechnung schweiz` (not ranked), `mahngebühren schweiz` (#53, decayed — backlog with `erfolgsrechnung`).

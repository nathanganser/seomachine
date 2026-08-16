# Cannibalization Review — 2026-07-16 (SE Ranking export)

Source: `insights_keyword_cannibalization_2026-07-16-09-20-08.csv` (40 keywords, Google CH, 2026-07-15/16).
Method: 3 review agents read every affected page in mh-landing + prior audits (2026-06-02, 2026-07-03, PR #115) before deciding.
Executed on mh-landing branch `seo/cannibalization-round2-2026-07`, **on top of the uncommitted default-locale migration (en→de)** — all German URLs below are bare (no /de/ prefix); redirects use the new semantics.

## Stale data (no action, don't re-litigate)

- `/milchbueechli-app` and `/ranking-simplest-rechnungssoftware-2026` in the export are **already 301s** since PR #115. SE Ranking shows lagging SERP data.

## MERGED (301 + content ported to survivor)

| Loser (deleted) | Survivor | Notes |
|---|---|---|
| `blog/comment-saffilier-a-lavs-en-tant-quindependant` (all 6 locales) | `ahv-compensation-fund` | FR slug carrying German content; full duplicate. Ported: 2025 Inkasso-per-Konkurs, CHF 2'500 trigger, form field table, 2 FAQs. Survivor slug deliberately NOT Germanized (ranks #32, title carries the keyword). |
| `gmbh-vs-selbstaendig-vs-ag` (5 locales) | `einzelfirma-oder-gmbh-schweiz` | Same article published 2 days apart (May 2026). Ported: Gewinnthesaurierung section, break-even bands (80k/100k/150k), Wechsel-Anleitung. Survivor retitled "Einzelfirma oder GmbH? Rechtsform wählen Schweiz 2026". |
| `steuerabzuege-selbstaendige-schweiz` (5 locales) | `steuerabzuge-schweiz` | Twin-slug near-duplicate found during review (not in SE Ranking data). Survivor had links/redirects/en-locale. Ported: Säule-3a worked example, 4 broad FAQs, "Einzelfirma Steuern" phrasing in title/intro. |
| `blog/generieren-sie-muhelos-…-mac-mit-magic-heidi` (all 6 locales) | `mac` | Blog outranked the landing page (#45 vs not-top-100) and the landing page linked to its own competitor. Ported: 6-step tutorial. `mac.md` retitled to target "Rechnungsprogramm Mac". |

## RE-SLUGGED

- `de/duplication` → `/doppelerwerbstaetigkeit-schweiz` (301, German only). 4.6k-word Doppelerwerbstätigkeit guide sat on a junk English slug. Cross-linked both ways with `blog/nebenberuflich-selbstaendig-schweiz` (blog = starter intent, guide = multi-activity/cross-border/tax-progression intent). Kept content intact (structure already matched the differentiated angle); fixed stale CHF 2'300 → 2'500.
- **Leftover mess (future pass):** `duplication` slug in en/es/it/pt = localized dual-activity guides, but `fr/duplication` = an unrelated invoice-duplication feature page. Only DE was re-slugged.

## DIFFERENTIATED (kept both, boundary fixed)

- **`mwst-registrierung/bern`** — was a Switzerland-wide 2025 guide on a canton URL (the #1 fix of this audit). Rewritten Bern-specific (title, hero, HRA Bern/AK Bern section, trimmed national rates/methods/cross-border blocks to links). St. Gallen page was already correct — its #11 for "mwst anmeldung" is a feature, not a bug. Also bumped stale 2024 titles on st-gallen + zurich.
- **`buchhaltungssoftware` vs `rechnungsprogramm`** — deliberately NOT merged (accounting terms uncontested; data asymmetric). The July default-locale-migration work had already deepened the accounting page. This pass: demoted "Faktura" from its feature-showcase headline, cross-linked to /rechnungsprogramm, fixed self-referencing "12 Rechnungsprogramme" links (→ /top-5-buchhaltungssoftware-schweiz), homepage meta no longer leads with "Rechnungsprogramm".
- **`banks/ubs`** — retitled UBS-first ("UBS QR-Portal: …"), added links to `/einzahlungsschein-erstellen` (generic intent) + `/qr-rechnung-erstellen`. Generic QR content NOT gutted (page was freshly rebuilt in the QR-cluster session 2026-07-13).
- **Jahresabschluss pair** — blog (#6, info) + landing (#17, product) is the correct outcome. Landing retitled toward "Jahresabschluss-Software"; reciprocal links added (blog → "auf Knopfdruck" CTA; landing → "manuelle Anleitung").
- **bexio preise** — `de/bexio-preise` exists (2026-07-13, too new to rank). `alternative/bexio` already anchors "bexio Preise 2026" to it. Decision: let the new page mature ~4 weeks; only thin the alternative page's pricing tables if it still blocks the dedicated page then.

## LEAVE AS IS (reviewed; do not re-open without new data)

- `rechnung-schreiben-schweiz` vs `rechnungsvorlage` — textbook intent split; right page wins every keyword. Only added: Honorarrechnung grid item on vorlage (its one lost keyword), 7-vs-8 Pflichtangaben aligned to "7 + Nummer empfohlen".
- `qr-iban-example` vs QR pillar — clean separation.
- `how-much-can-you-bill…` vs schreiben page — beneficial double slot (#2 + #10 "privatrechnung schweiz"). English slug re-slug deferred (low value vs risk).
- hourly-rates trio — #2 owns it; added links to net-pay calculator + time-tracking guide.
- budgeting-apps for "buchhaltungs app" — incidental bleed, pillar outranks.
- Homepage mid-pack rankings — normal authority spillover.
- "magic heidi erfahrungen" — homepage #1. `de/reviews` retitled to include "Erfahrungen" (was Bewertungen-only, which is why EN /reviews ranked in de-CH).
- `uid-nummer-schweiz` — well differentiated, no action.
- **CLOSED follow-up from 2026-07-03 audit:** "narrow mwst-registrierung to registration-only" — the 2026 rewrite already did this (#14 for "mwst nummer beantragen"); the "mwst anmeldung" weakness was bern.md, now fixed.

## Extra fixes shipped in the same pass

- QR pillar now answers "QR-Rechnung Vorlage" (FAQ) — recaptures the term `banks/ubs` was leaking (4.8k impressions).
- `milchbuechleinrechnung`: added "Milchbüechlirechnung Vorlage" section (Excel/Sheets build guide) + description.
- Legacy `/invoicing` link fixed in nebenberuflich blog.
- Stale AHV threshold instances (2'300 → 2'500) in doppelerwerbstaetigkeit guide — part of the site-wide sweep tracked in memory.

## Verify (after deploy)

- `curl -I` the 5 new redirect sources → 301 to survivors (see `config/redirects.ts`, "2026-07-16 cannibalization cleanup round 2" block).
- Re-run SE Ranking cannibalization export ~2026-08-15; expect: AHV, Rechtsform, Steuerabzüge, Mac, "mwst anmeldung" splits resolved; bexio-preise page ranking.

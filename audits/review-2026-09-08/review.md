# Big Review & Plan — magicheidi.ch — 2026-09-08

Sources: fresh GSC pull (`raw.json`, windows A = 2026-05-17→06-13, B = 07-12→08-08, C = 08-09→09-05, plus 90-day page×query), DataForSEO live SERPs (`serp_results.json`, CH/de-fr) and Swiss search volumes (`volumes.json`), mh-landing content tree + git history. SE Ranking (expired 2026-08-16, Data API now refuses), Ahrefs (plan-locked, even the free DR endpoint) and the Vercel Web Analytics API (not on plan) are all unavailable — this review is GSC + live SERP only, no backlink re-measure.

## 1. Verdict

**Traffic is flat and the money pages have not moved in four months.** Site clicks: 9,704 (June, holiday spike) → 5,663 (July) → 5,889 (Aug 9–Sep 5). Money-page clicks: 980 → 976 → 1,020. The BOFU head terms sit exactly where they were in July (live SERP today: `buchhaltungssoftware schweiz` #17, `buchhaltungsprogramm schweiz` #18) despite six PRs of on-page work. That is the authority ceiling every review since July has named; the outreach that was supposed to break it was never sent.

Three things are new since the 16 August review:

1. **The cheap wins worked.** Every small retitle on a page that already sat at position 5–12 paid off within 3 weeks: `mwst rechner` 5 → 22 clicks (impressions 1.8k → 5.7k, live #6), `/online-vat-statement` 0 → 10 clicks (5.5k impressions), `/alternative/abaninja` 19 → 43, `/fr/rechnungsprogramm` 28 → 71 (live #6 for `logiciel facturation suisse`), `/kontenplan-schweiz` 2 → 26, `/fr/uid-nummer-schweiz` 3 → 25. This is the playbook to scale.
2. **The Outrank blog pipeline is now the biggest risk on the site.** It has added 110 DE posts since 23 June (~1.5/day, each auto-translated into 5 more locales = ~660 files). 90-day yield: DE blog 31 clicks, FR 11, IT 3, **EN/ES/PT 0 clicks across ~77 pages**. 54 of 129 DE posts have zero impressions. Worse, ~20 of the new posts target keywords that existing landing pages already own (QR-Rechnung ×5, Saldosteuersatz ×5, Rechnungsvorlage ×2, Offerte ×2, MWST online ×2, MWST-Anmeldung, Buchhaltung Selbständige ×2, Jahresabschluss) and four reuse the exact slug of a landing page (`rechnungsnummer-schweiz`, `rechnungswesen-schweiz`, `skonto-schweiz`, `spesenreglement-schweiz`). `/qr-rechnung-erstellen` fell from pos 14 → 22 and 36 → 20 clicks in the same window the five QR blog posts went live. A test article (`sample-article-title-for-testing`) is live in six locales. This is the July cannibalization cleanup being undone automatically.
3. **One regression needs a revert.** `/bexio-preise` lost the `bexio preise` query entirely (impressions 415 → 7, live: not in top 30) after its title was changed on 16 August to "bexio Preise 2026: Was bexio wirklich kostet (CHF 35–119/Mt.)". The page still shows for `bexio pakete`/`bexio kosten` at pos 7, so it is not deindexed — the head term was lost. Revert the title.

## 2. Scoreboard

| Metric (28 d) | A: May 17–Jun 13 | B: Jul 12–Aug 8 | C: Aug 9–Sep 5 |
|---|---:|---:|---:|
| Clicks | 9,704 | 5,663 | 5,889 |
| Impressions | 1.27M | 829k | 856k |
| Avg position | 8.2 | 9.9 | 9.4 |
| Holiday pages | 4,108 | 649 | 1,138 |
| Calculators | 627 | 891 | 808 |
| **Money pages** | **980** | **976** | **1,020** |
| Blog | 123 | 115 | 209 |
| DE / FR / IT / EN | 3,091 / 2,636 / 2,388 / 0 | 2,214 / 1,567 / 1,048 / 49 | 1,981 / 2,210 / 867 / 201 |
| Brand "magic heidi" | 327 cl, pos 1.1 | 301, pos 3.1 | 320, pos 1.9 |

Weekly clicks since July: 1,330–1,560, no trend. DE is drifting down (-10% B→C) while FR (+41%) and EN (0 → 201) grow.

### Money keywords — GSC average vs. live SERP today

| Keyword | Vol/mo | GSC pos A → B → C | Live SERP 08.09 | Page |
|---|---:|---|---|---|
| buchhaltungsprogramm schweiz | 140 | 22.2 → 21.3 → 16.7 | **#18** | /buchhaltungssoftware |
| buchhaltungssoftware schweiz | 590 | 15.8 → 18.7 → 17.6 | **#17** | /buchhaltungssoftware |
| beste buchhaltungssoftware schweiz | — | 10.3 → 9.4 → 18.7 | **#7** | /buchhaltungssoftware |
| buchhaltungssoftware für selbständige | — | 36 → 21 → 31.5 | #36 (SERP is German .de sites) | — |
| bexio alternative | 140 | 8.5 → 13.0 → 15.7 | **#7** | /alternative/bexio |
| bexio preise | 720 | 8.8 → 9.0 → (7 impr) | **not in top 30** | /bexio-preise — REGRESSION |
| rechnungsvorlage schweiz | 480 | 11.5 → 9.7 → 9.0 | **#5** | /rechnungsvorlage |
| rechnungsprogramm schweiz | 50 | 16.1 → 16.9 → 16.3 | **#10** | /rechnungsprogramm |
| rechnungssoftware schweiz | — | 11.7 → 12.3 → 7.6 | #13 | /rechnungsprogramm |
| rechnung schreiben | 320 | 9.6 → 4.8 → 7.6 | #8 | /rechnung-schreiben-schweiz |
| mwst rechner | — | 10.4 → 10.6 → 5.7 | **#6** | /tools/vat-calculator-switzerland |
| mwst online einreichen | — | — → 9.7 → 9.8 | not top 30 (ESTV ×6) | /online-vat-statement |
| einzahlungsschein erstellen | 1,000 | 10.1 → 10.9 → 18.5 | #10 | /einzahlungsschein-erstellen — declining |
| uid register | 8,000 | — → 6.7 → 6.4 | #8 | /uid-nummer-schweiz — 4.4k impr, **0 clicks** (navigational, uid.admin.ch) |
| logiciel facturation suisse | 30 | 30 → 24.5 → 23.6 | **#6** | /fr/rechnungsprogramm |
| logiciel comptabilité suisse | 110 | 17 → 16.6 → 14.2 | #11 | /fr/buchhaltungssoftware |
| lohnrechner schweiz | **9,900** | — | pos 11.3–11.9 | /brutto-netto-rechner-schweiz |
| vacances scolaires vaud 2026 | **49,500** | pos 5.1, 188 clicks / 48k impr (CTR 0.4%) | — | /fr/feiertage/waadt |

`/buchhaltungssoftware` itself: 20.7k impressions / 14 clicks in 90 days across 1,469 queries. It earns 818 impressions at pos 4.9 for the English query "accounting software" — the German page is being served for English intent; the EN page (`/en/buchhaltungssoftware`) has zero impressions. Worth a hreflang/indexing check.

### Page movers (C vs B, non-holiday)

Winners: `/fr/tools/salary-calculator-switzerland` +74 (243 clicks, now the #3 page on the site), `/fr/rechnungsprogramm` +43, `/` +37, `/en` +33, `/kontenplan-schweiz` +24, `/alternative/abaninja` +24, `/fr/uid-nummer-schweiz` +22, `/tools/vat-calculator-switzerland` +17, `/ai-expenses-scanning` +13.

Losers: `/pt/tools/salary-calculator` −87 (pos 3.8 → 5.8), `/stundenlohn-berechnen-schweiz` −67 (6.7 → 8.0), `/budgeting-apps` −26 (9 → 18; rewritten today, watch), `/brutto-netto-rechner-schweiz` −24, `/coworking/genf` −27, `/qr-rechnung-erstellen` (36 → 13 → 20 clicks vs June), `/buchhaltungssoftware` 18 → 3 clicks, `/mwst-registrierung` pos 18.8 → 31, `/mwst-freelancer` impressions 3,344 → 718 since June.

## 3. The four big decisions

### Decision 1 — Stop on-page work on the BOFU pillars; do the authority work or officially drop the page-1 goal

`/buchhaltungssoftware`, `/rechnungsprogramm`, `/alternative/bexio` are fully optimized. Page 1 for `buchhaltungssoftware schweiz` is held by swiss21, pfeffersack, cashctrl, banana, fibu3, milkee, accounto — all product pages with 450–4,500 referring domains (we had 221 on 16 Aug). No further on-page edit will move this; the last four months prove it. Two actions, both off-page, both cheap, both pending since July:

1. **Milkee (sister company) listicle** — ranks page 1 for `buchhaltungssoftware für selbständige` and `beste buchhaltungssoftware schweiz`, lists Magic Heidi at #8 *without a link*. Ask internally for a link and a higher slot. This is the single cheapest authority win available and requires no cold email.
2. **Send the outreach dossier** (`outreach/buchhaltungsprogramm-outreach-2026-07-23.md`: Zürcher Treuhand, Alpinum, abrechnungen.ch, betterstudy, startups.ch, moneytoday, OMR profile, swissmadesoftware Level 2). Three of those listicles rank in today's live top-10 (zuerchertreuhand #7, abrechnungen #10, pfeffersack #5). Being *in* those lists is worth more than any title tweak.

If neither will happen, say so and stop tracking page-1 for the head terms — the campaign has consumed more planning time than it can return.

### Decision 2 — Put a gate on the Outrank blog pipeline (this week)

The pipeline is high-volume, near-zero-yield, and actively cannibalizing. Proposed rules:

- **Delete** `blog/sample-article-title-for-testing` in all 6 locales.
- **Stop auto-translating blog posts to EN/ES/PT** (0 clicks, ~77 pages, 90 days). Keep DE, and FR only when the topic is Swiss-Romandie relevant. If the webhook cannot be changed, set `noindex` on those locales' blog routes.
- **De-dup gate before publish**: reject any topic whose primary keyword an existing landing page already targets (list in §6). Cheapest implementation: the webhook checks the target keyword against a `content/keyword-map.json` you maintain.
- **Merge the existing duplicates** into their landing pages with 301s (list in §6). Priority: the 5 QR posts → `/qr-rechnung-erstellen` (2,900/mo keyword, lost 8 positions), the 5 Saldosteuersatz posts → `/net-vat-accounting-method` or one blog guide, `mwst-anmelden-schweiz` → `/mwst-registrierung`, the 2 Offerte posts → the new Offerte page (§5), `rechnungen-schreiben-vorlage` + `rechnungsvorlage-einzelunternehmen` → `/rechnungsvorlage`.
- **Quality gate**: du-form (posts are in Sie-form; the landing pages are du), one link to a money page, a "Das Wichtigste in Kürze" block. The industry series ("Physiotherapeut/Zahnarzt/Architekt Rechnung Schweiz") is the only Outrank format earning clicks (5–6 each) — keep that format, drop generic accounting explainers that duplicate pillars.

### Decision 3 — Scale what is actually working: templates, calculators, retitles at pos 5–12

The site's best non-seasonal pages are template and calculator pages: `/quittung-vorlage-schweiz` (128 clicks, #1 money page), `/rechnungsvorlage` (#5 live), `/fr|it|pt/tools/salary-calculator` (456 clicks combined), `/brutto-netto-rechner-schweiz`, `/tools/vat-calculator-switzerland`. The pattern: **template pages with a real downloadable file rank; the ones without do not** (rechnungsvorlage 17 download references, quittung 16, mahnung 7 — all ranking; kostenvoranschlag, kassenbuch, lieferschein, arbeitsrapport 0 — none ranking). The plan in §5 is built on this.

### Decision 4 — Replace SE Ranking with a GSC + DataForSEO rank tracker

Both paid data tools are locked and the 1 September re-measure could not run. A weekly `rank_tracker.py` that pulls live SERPs for the ~40 tracked keywords (DataForSEO, a few cents per run) plus the GSC tracked-query table gives everything the monthly audits used, minus backlinks. Renew SE Ranking only if you want backlink monitoring back; a DR check is not worth a subscription on its own.

## 4. Immediate fixes (this week, all small)

| # | Fix | Why | Effort |
|---|---|---|---|
| 1 | Revert `/bexio-preise` title to "bexio Preise 2026 Schweiz: Pakete und Kosten im Überblick" (pre-16-Aug) | Lost `bexio preise` (720/mo) entirely after the change; also removes a competitor price claim from a title | 10 min |
| 2 | Delete `sample-article-title-for-testing` ×6 locales | Live test content | 5 min |
| 3 | Retitle `/brutto-netto-rechner-schweiz` to lead with "Lohnrechner Schweiz 2026" (keep Brutto-Netto in title) and add a "Lohnrechner" H2 | `lohnrechner schweiz` 9,900/mo + `lohnrechner` 6,600/mo at pos 11–12; page already has the calculator | 30 min |
| 4 | Retitle `/fr/tools/vat-calculator-switzerland` around "Calcul TVA Suisse" | `calcul tva suisse` 720/mo, we rank 49; the DE twin's retitle went 10 → 6 | 20 min |
| 5 | Add "MWST-Abrechnung" to `/online-vat-statement` title/H1 | `mwst abrechnung` + `mwst abrechnen` 1,900/mo each; page is at 9.3–9.8 for the "online" variants | 20 min |
| 6 | Check `/en/buchhaltungssoftware` indexing/hreflang | "accounting software" 818 impr at 4.9 served by the DE page; EN page has 0 impressions | 30 min |
| 7 | Refresh `/it/commerce-register-switzerland-2026` with a Ticino section | `registro di commercio ticino` 6,600/mo, page at 8.9–9.9, clicks sliding 13 → 6 | 1 h |
| 8 | Look at `/stundenlohn-berechnen-schweiz` (−67 clicks, pos 6.7 → 8.0) and `/pt/tools/salary-calculator` (pos 3.8 → 5.8) | Two of the biggest non-seasonal losers; check whether the July default-locale change or a competitor reshuffle did it | 1 h |

Deliberately **not** doing: `uid register` CTR work (navigational to uid.admin.ch, 0% CTR is structural), `mwst online einreichen` (ESTV holds 6 of the top 11), `llc registration` (13k impressions, non-Swiss intent).

## 5. Content queue (ranked by expected clicks ÷ effort)

### Revenue track

1. **`/offerte-vorlage-schweiz`** — new page, consolidate `blog/offerte-schreiben-schweiz` (521 impr, 1 click), `blog/offerten-vorlage-schweiz` (271 impr) and the Offerte half of `/kostenvoranschlag-schweiz` into one page with a downloadable Word/Excel/PDF Offerte + QR link to the invoice flow. Demand: `offerte vorlage` 590 + `offertenvorlage` 590 + `offerte schreiben` 70 + `auftragsbestätigung vorlage` 90. Same playbook as `/rechnungsvorlage` (#5). 301 the two blog posts.
2. **Vorlagen hub + downloadable assets** for the four template pages with none: `/kostenvoranschlag-schweiz`, `/lieferschein-schweiz` (210/mo), `/kassenbuch-schweiz` (210), `/arbeitsrapport-schweiz` (`stundenrapport vorlage` 140, `arbeitsrapport vorlage` 110, `zeiterfassung excel vorlage` 140). Add a `/vorlagen` index linking all templates. Also `zahlungserinnerung vorlage` (110) as a section on `/mahnung-vorlage-schweiz` (1,603 impr, pos 20 — a download-driven refresh could take it to page 1).
3. **Budgetplaner Vorlage (Excel/PDF)** on `/budgeting-apps` — 1,300/mo (`budgetplaner vorlage`) + `budget vorlage pdf` 480 + `budgetplanung schweiz vorlage gratis` 390; flagged in today's rewrite as the deferred link-earning asset. Build it now while the rewrite is fresh.
4. **QR-Rechnung consolidation** — merge the 5 QR blog posts into `/qr-rechnung-erstellen` (2,900/mo; fell 14 → 22) with sections for Pflicht, Validieren, Beispiel, Umstellung; 301 the posts. Consider folding `/einzahlungsschein-erstellen` (declining 10 → 18.5 since the July split) back in as a section, or give it its own download.
5. **`/mwst-registrierung` rescue** — pos 18.8 → 31 since June; `mwst anmeldung` 1,000/mo; merge `blog/mwst-anmelden-schweiz` into it, add the cantonal satellites as an in-page table, re-link from `/mwst-schweiz` (pillar is now indexed: 291 impr, pos 14, still 0 clicks — needs inbound links, not more copy).
6. **Tarif 590 / LAMal invoicing guide (DE + FR)** — *needs a product answer first*: does Magic Heidi produce Tarif-590-compliant invoices? GSC shows ~3k impressions/90d on `logiciel facturation lamal`, `logiciel gestion factures lamal`, `logiciel facturation medidata`, `kvg billing software` landing on `/fr/rechnungsprogramm` (pos 6–40, 0 clicks); `tarif 590` is 720/mo DE, `medidata` 2,900/mo. If yes: a "Tarif 590 Rechnung erstellen" page is a clear segment win (therapists — the Physio/Heilpraktiker/Logopäde posts already exist). If no: an honest guide that says which tools handle it, positioning MH for non-KVG clients. Do not build it before that answer.
7. **FR salary calculator**: verify `/fr/tools/salary-calculator-switzerland` (243 clicks, #3 page) targets `salaire brut net suisse` (1,300/mo) and `calcul salaire net suisse` (320) explicitly — one title check could add a few hundred clicks.

### Traffic track (not buyers, but the largest lever on the site)

8. **`/fr/vacances-scolaires-vaud`** — `vacances scolaires vaud 2026` is **49,500/mo** and `/fr/feiertage/waadt` already ranks #5 for it with a 0.4% CTR because the page is a public-holidays page with a school-holidays section. A dedicated page (dates 2026-27 and 2027-28, per-region table, PDF/ICS download) at pos 3–5 with a normal 4–8% CTR is 2,000–4,000 clicks/month — more than all money pages combined. Same pattern then for Genève (5,400), Fribourg (2,900), Neuchâtel (1,900), Valais (1,600), Ticino IT (1,600). Caveat: zero purchase intent; value is brand reach and the same "Feiertage" halo the site already lives on. One day of work; do it if you accept that trade.

### Hold / stop

- No more on-page edits to `/buchhaltungssoftware`, `/rechnungsprogramm`, `/alternative/bexio`, `/top-5-buchhaltungssoftware-schweiz` (468 impr / 2 clicks in 90 days; `beste buchhaltungssoftware schweiz` is answered by `/buchhaltungssoftware` at #7 anyway).
- No new vs-pages, no new `/alternative/*` pages (winbiz 3 impr, swiss21 8 impr, cashctrl 264 — the long tail of alternatives is dead; abaninja works only because of the DeepNinja news hook).
- UID cluster: leave as is; it is navigational traffic Google will never hand us.

## 6. Outrank duplicates to merge (DE; mirror in FR/IT)

| Existing page | Overlapping blog posts (created Jul–Sep) |
|---|---|
| `/qr-rechnung-erstellen` | neue-qr-rechnung-schweiz, qr-rechnung-schweiz-beispiel, qr-rechnung-schweiz-pflicht, qr-rechnung-validieren, umstellung-qr-rechnung-schweiz, rechnung-mit-qr-code-erstellen, qr-rechnung-erstellen-schweiz |
| `/net-vat-accounting-method` | effektive-methode-mwst, mwst-abrechnungsmethode, mwst-saldosteuersatz-formular, saldosteuersatz-schweiz, unterstellungserklarung-saldosteuersatz |
| `/online-vat-statement` | mwst-online-einreichen, mwst-online-einreichen-schweiz, mehrwertsteuer-online-abrechnen |
| `/mwst-registrierung` | mwst-anmelden-schweiz |
| `/rechnungsvorlage` | rechnungen-schreiben-vorlage, rechnungen-schreiben-vorlage-qr-tools, rechnungsvorlage-einzelunternehmen |
| `/kostenvoranschlag-schweiz` / new Offerte page | offerte-schreiben-schweiz, offerten-vorlage-schweiz |
| `/buchhaltungssoftware`, `/buchhaltung-einzelfirma-schweiz` | buchhaltung-fur-selbstandige-schweiz, buchhaltung-einzelunternehmen-schweiz, buchhaltung-fuer-anfaenger |
| `/jahresabschluss-schweiz` | jahresabschluss-checkliste, jahresabschluss-einzelfirma |
| `/tools/vat-calculator-switzerland`, `/mwst-schweiz` | mwst-schweiz-berechnen-saetze-formeln-und-praxisbeispiele, mwst-berechnung-schweiz |
| Same slug as landing page | rechnungsnummer-schweiz, rechnungswesen-schweiz, skonto-schweiz, spesenreglement-schweiz |

Rule of thumb for the merge: keep the landing page, move any genuinely new section from the blog post into it, 301 the post. Where a topic really is a separate informational query (e.g. QR-Rechnung Pflicht), keep *one* blog post and 301 the rest to it.

## 7. Measurement & checkpoints

- **Now**: build `rank_tracker.py` (DataForSEO live SERP for the ~40 keywords in `tracked_queries.csv` + GSC 7-day positions) and run it weekly; commit CSVs to `audits/rank-tracker/`.
- **2026-09-22** (2 weeks): retitle checks — bexio preise back in top 10? lohnrechner ≤ 10? calcul tva suisse in top 20? mwst abrechnung movement? `/budgeting-apps` recovered from pos 18?
- **2026-10-06** (4 weeks): Offerte page + Vorlagen downloads indexed and ranking; QR consolidation effect on `/qr-rechnung-erstellen`; blog EN/ES/PT change reflected (fewer indexed pages, no click loss).
- **2026-10-08**: next monthly review (same scripts, windows shifted 28 days). If the Milkee link / outreach were done, re-check the head terms then — not before.

## 8. Things only you can do

1. Answer the Tarif 590 product question (§5.6).
2. Ask Milkee for the link/slot (§3, Decision 1).
3. Decide on the Outrank gate: change the webhook (topic list + no EN/ES/PT), or accept a `noindex` on those blog locales.
4. Send (or formally drop) the July outreach dossier.
5. Decide whether the site wants the school-holiday traffic track (§5.8).
6. Export fresh Vercel Top Pages/Referrers CSVs (latest ends 16 Aug); the API is plan-gated.

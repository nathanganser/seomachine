# Report — Package F (quick fixes), 2026-09-09

All work in `mh-landing`, branch `seo/content-queue-2026-09-08`, nothing committed. No file outside the package was touched (`content/de/qr-rechnung-erstellen.md` in the diff belongs to another package).

## 1. `/bexio-preise` title revert — DONE (`content/de/bexio-preise.md`)
- Commit 36eadd71 (2026-08-16) changed only DE, and only title + description (frontmatter and `::blog` block, no H1/hero). Other locales untouched in that commit → nothing to revert there.
- Title: "bexio Preise 2026: Was bexio wirklich kostet (CHF 35–119/Mt.)" → **"bexio Preise 2026 Schweiz: Pakete und Kosten im Überblick"** (exact previous).
- Description restored too ("Alle bexio Preise 2026: Basic CHF 35, Advanced CHF 42, Optima CHF 69, Ultimate CHF 119/Mt. …") — the 8/16 one had dropped the exact phrase "bexio Preise". Body untouched.

## 2. Test article — DONE
- `git rm` of `content/{de,en,es,fr,it,pt}/blog/sample-article-title-for-testing.md` (6 locales; none in sq/sr). No inline links to it anywhere in `content/`, `app/`, `config/`.
- Redirect recorded in `redirects-F.txt`: `/blog/sample-article-title-for-testing` → `/blog`, `locales: true`.

## 3. Lohnrechner retarget — DONE (`content/de/brutto-netto-rechner-schweiz.md`)
- Title: "Brutto Netto Rechner Schweiz 2026 – Gratis Lohnrechner" → **"Lohnrechner Schweiz 2026: Brutto-Netto-Rechner gratis"** (53).
- Description now leads with "Lohnrechner Schweiz 2026: …" and ends "Gratis Brutto Netto Rechner, ohne Anmeldung." (153).
- Hero title: "Brutto Netto Rechner Schweiz 2026, der Lohnrechner…" → "Lohnrechner Schweiz 2026, Brutto Netto Rechner für deinen Nettolohn".
- First H2 replaced by **"Lohnrechner Schweiz: So berechnest du deinen Nettolohn"** (209 words, 5-step explanation). Rates used only as already on the page: AHV/IV/EO 5.3 %, ALV 1.1 %, BVG 3.5–9 % AN-Anteil, NBU ca. 1–2 %, Quellensteuer for B-Bewilligung. Link added: "Durchschnittslohn und Medianlohn in der Schweiz" → `/average-median-salary-switzerland-2026`. Calculator component untouched.
- **FR mirror NOT done, on purpose.** `content/fr/brutto-netto-rechner-schweiz.md` is a 1:1 translation of the DE page (same `::salary-calculator`, same sections) = a second FR salary page next to `/fr/tools/salary-calculator-switzerland`. GSC 90d: the FR brutto page has 1 impression for "salaire brut net suisse" (pos 29) vs 1'208 impressions/50 clicks at pos 4.2 on the tools page. Retitling it toward "brut net" would build a cannibal. Recommendation for a later package: 301 `/fr/brutto-netto-rechner-schweiz` → `/fr/tools/salary-calculator-switzerland` (or noindex) rather than retitle.

## 4. FR VAT calculator — DONE (`content/fr/tools/vat-calculator-switzerland.md`)
- Title: "Calculateur TVA Suisse — Calculer la TVA gratuitement" → **"Calcul TVA Suisse 2026: Calculateur TVA gratuit (8.1 %)"** (55; the three-rate variant was 69 chars).
- Description rewritten around "Calcul TVA Suisse 2026" (148). Hero label/title → "Calcul TVA Suisse — calculateur gratuit & à jour"; the German "Stand:" in the FR subtitle replaced by "en vigueur depuis le 01.01.2024".
- New `::markdown{as: article}` H2 **"Comment calculer la TVA en Suisse"** with TTC = HT × 1.081, HT = TTC / 1.081, worked example (CHF 1'000 → 1'081; CHF 250 TTC → 231.27 HT), factors 1.026 / 1.038; existing "Remarque" folded in. DE file not touched.

## 5. FR salary calculator — DONE (`content/fr/tools/salary-calculator-switzerland.md`)
- Neither phrase was contiguous in title/description/H1. GSC (10.06–07.09): "salaire brut net suisse" 50 clicks pos 4.2, "brut net suisse" 49 clicks pos 3.7, "calcul salaire net suisse" 12 clicks pos 6.2; "calculateur…" queries are marginal (≤5 clicks). So the lead kept "Calculateur de Salaire" and only inserted the phrase:
- Title: "Calculateur de Salaire Suisse — Salaire Brut Net 2026" → **"Calculateur de Salaire Brut Net Suisse 2026 — Gratuit"** (53).
- Description → "Calcul salaire net suisse 2026 : convertissez votre salaire brut net suisse avec toutes les déductions (AVS/AI/APG, AC, LPP, accidents, impôt). Gratuit." (152). H1 (feature-image title) → "Calculateur de Salaire Brut Net Suisse — du brut au net, expliqué". Nothing else changed.

## 6. IT commerce register — DONE (`content/it/commerce-register-switzerland-2026.md`)
- New H2 **"Registro di commercio Ticino: ufficio, ricerca ed estratti"** (replaces the old H3 office block) with sub-H3s "Come consultare il registro di commercio Ticino" (Zefix free lookup, estratto autenticato from the office) and "Iscrizione della ditta individuale in Ticino" (obligatory > CHF 100'000, EasyGov, cantonal costs). New FAQ #1 "Come consulto il registro di commercio del Ticino?". Description now "Registro di commercio Svizzera e Ticino 2026: …" (159). Title kept (has Zefix + 2026; it is 62 chars, pre-existing).
- Office contact VERIFIED on ti.ch (Sezione dei registri, fetched): **Via Tognola 7, 6710 Biasca, +41 91 816 29 81, di-rc@ti.ch, sportelli Lun–Ven 08:45–11:45 / 14:00–16:00**; the Sezione's seat is Piazza Governo 7, Bellinzona. The page had a wrong/outdated address, phone, e-mail and hours (Via Lambertenghi 3A, 091 814 14 51, rc@ti.ch) — corrected in the feature-grid card and the new section. So the brief's "Bellinzona" is the section HQ, the counter is Biasca.
- Not verified on admin sources (kept only because the page already states them): estratto CHF 20–30, ditta individuale tariffa base CHF 120.
- Wording caveat: the new section and FAQ are in **tu-form as instructed**, but the rest of this page is in Lei-form ("la Sua impresa"). Flagging the mix; a later pass should convert the whole page to tu.

## 7. EN accounting page diagnosis — DONE (`content/en/buchhaltungssoftware.md`)
- Technically nothing is broken: `curl -sI /en/buchhaltungssoftware` → 200, self-canonical `https://magicheidi.ch/en/buchhaltungssoftware`, robots index/follow, hreflang alternates for all 8 locales emitted by @nuxtjs/i18n (`strategy: prefix_except_default`, `defaultLocale: de`, x-default → DE), listed in `__sitemap__/en-CH.xml`, schema `page-path: /en/buchhaltungssoftware` correct.
- Legacy `/accounting-software-for-self-employed-professionals-in-switzerland` is already a 301 → `/buchhaltungssoftware` (`config/redirects.ts:302`, `locales: true`; `/en/...` → `/en/buchhaltungssoftware`). No file exists for it → nothing to `git rm`, no new redirect needed. Its 647 impressions are Google still showing the stale URL, not a live page.
- Likely cause of 0 EN impressions: x-default + the DE page's authority make Google serve `/buchhaltungssoftware` for English queries; the EN page had no "bookkeeping" signal. Changed: title "Accounting Software Switzerland: Built for Freelancers" → **"Accounting Software Switzerland: Bookkeeping for Freelancers"** (60); description now "Accounting software Switzerland: bookkeeping for freelancers with Swiss QR-bill, automatic VAT and AI receipt scanning. iPhone, Mac & Web. Try it free." (151); hero subtitle "Simple cloud accounting and bookkeeping for sole proprietors…". German file not touched.
- Suggestions (not done, outside package): request indexing of `/en/buchhaltungssoftware` in GSC; add internal links to it from EN pages (currently reachable mostly via hreflang/nav).

## Tooling notes
- Ahrefs GSC endpoints returned "Insufficient plan"; used the local `data_sources/modules/google_search_console.py` with `.env` instead.
- MDC check: opener/closer counts match on all 6 edited files; frontmatter title/description lengths within limits (IT title 62, pre-existing).

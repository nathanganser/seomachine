# Internal Links Map — Magic Heidi

This document catalogs key Magic Heidi pages that should be referenced in blog content for strategic internal linking. Use this as the go-to reference when adding internal links to articles.

**Last verified**: 2026-07-19 (live curl checks against magicheidi.ch — see note below; supersedes the 2026-05-25 pass, which predates the 2026-07-16 default-locale switch)

---

## Site structure — read this first

- **Six locales** are configured (Nuxt i18n). Since the **2026-07-16 default-locale switch**, bare URLs (`magicheidi.ch/slug`, **no prefix**) serve **German**; English lives at **`/en/slug`**; French/Italian/Spanish/Portuguese are unchanged at `/fr/`, `/it/`, `/es/`, `/pt/`. This reverses the pre-migration scheme — if you see "en default, no prefix" anywhere (including in memory files), it's describing the old behavior.
- Verified live 2026-07-18/19: bare `/` renders with `lang="de-CH"` and a self-referencing `de-CH` hreflang; `/de/*` paths 308-redirect to their bare equivalent; `/en` returns a real 200 page (not a 404 — the old catch-all `/en/* → /*` rewrite no longer applies to the bare `/en` route itself).
- **Most pages exist in all 6 languages** at the same slug, but a few do not (see "Pages missing in some locales" below).
- **Slugs are not localised on most pages** — many use German words across every language (`/rechnungsprogramm`, `/buchhaltungssoftware`, `/mwst-freelancer`, `/einzelfirma-grunden-schweiz`, `/beleg-scanner-schweiz`, `/rechnungsvorlage`, `/qr-rechnung-erstellen`, `/rechnung-schreiben-schweiz`, `/stundenlohn-berechnen-schweiz`). Don't try to "translate" the slug; the German slug is canonical in every language.
- **Inline content links** (markdown `[text](/slug)` inside an article body) are auto-localized at render time by the site's `ProseA.vue` component via Nuxt i18n's `localePath()` — a bare `/mwst-freelancer` written in *any* locale's markdown renders with that page's own locale prefix automatically (confirmed live: bare `/mwst-freelancer` inside `/en/vat-management`'s content renders as `href="/en/mwst-freelancer"`). **Always write inline content links bare (no locale prefix)** — this is simpler and matches the auto-localization behavior. Do NOT hand-prefix inline links with a specific locale (e.g. `/de/...`) since it's unconfirmed whether an already-prefixed link gets corrected for the current page's locale or left as literally written; a `/de/...` link inside non-German content risks sending readers to the German page. (One live article, `top-5-buchhaltungssoftware-schweiz`, still has hand-written `/de/`-prefixed inline links as of 2026-07-19 — a pre-migration leftover, not a pattern to copy.)
- **Structured-data / schema fields are different** — e.g. the `page-path` prop in `::pages-landing-magic-heidi-software-schema` is NOT auto-localized and must be hand-set per locale (`/en/original-slug`, `/fr/original-slug`, etc., bare/no-prefix only for the German version). Confirmed via the live canonical tag and JSON-LD on `/en/alternative/klara`.
- If you link a slug that doesn't exist in the article's locale, the site does a lookup in other locales — wasted hop. Always pick an existing locale path.

### Pages missing in some locales

| Page | Available locales | Notes |
|---|---|---|
| `/mwst-freelancer` | en, de, fr, it | Not in es/pt — for ES/PT content, link to `/es|pt/buchhaltungssoftware` or `/es|pt/rechnungsprogramm` for VAT context |
| `/beleg-scanner-schweiz` | en, de, fr, it | Not in es/pt — for ES/PT content, link to `/es|pt/ai-expenses-scanning` instead |
| `/kostenvoranschlag-schweiz` | all 6 + sr | Full translations shipped 2026-08-01 (en/fr/it/es/pt); link bare from any locale |
| `/qr-rechnung-erstellen` | all 6 | Despite the German slug |
| `/rechnungsvorlage` | all 6 | Despite the German slug |
| `/rechnung-schreiben-schweiz` | all 6 | Despite the German slug |
| `/stundenlohn-berechnen-schweiz` | all 6 | Despite the German slug |
| `/quotes` | all 6 | English slug, exists everywhere |
| `/freelancer.md` (literal) | es, pt only | But `/freelancer` redirects everywhere — see redirects below |
| `/vat-management` | all 6 | This is a **live page**, not a redirect |

### Canonical URLs after redirects (important — old paths now redirect)

The following old URLs **redirect** to new canonical paths. Always link to the canonical destination, not the legacy path. (Source: `mh-landing/config/redirects.ts` + `nuxt.config.ts` route rules, expanded across locales unless noted.)

| Legacy path | Canonical destination |
|---|---|
| `/invoicing` (and `/de|fr|it|es|pt/invoicing`) | `/rechnungsprogramm` (with matching locale prefix) |
| `/invoicing-software-switzerland` (all locales) | `/rechnungsprogramm` |
| `/rechnung` (all locales) | `/rechnungsprogramm` |
| `/rechnungsprogramm-schweiz` | `/rechnungsprogramm` |
| `/accounting` (all locales) | `/buchhaltungssoftware` |
| `/accounting-software-switzerland`, `/accounting-software-2026`, `/best-invoicing-accounting-software-2025`, `/swiss-accounting-software` (all locales) | `/buchhaltungssoftware` |
| `/self-employed-accounting-switzerland` | `/buchhaltungssoftware` |
| `/de/buchhaltungssoftware-schweiz`, `/de/buchhaltung-schweiz`, `/de/buchhaltung-app-schweiz`, `/de/buchhaltung-einzelfirma` | `/de/buchhaltungssoftware` |
| `/vat-mwst`, `/value-added-tax`, `/vat-for-swiss-freelancers` (all locales) | `/mwst-freelancer` |
| `/expense-tracking-software`, `/simplifying-expense-tracking`, `/expense-app-switzerland` (all locales) | `/beleg-scanner-schweiz` |
| `/expensing` | `/ai-expenses-scanning` |
| `/becoming-a-freelancer`, `/how-to-become-freelancer`, `/sole-proprietorship-switzerland-complete-guide`, `/sole-propietorship-or-llc` (all locales) | `/einzelfirma-grunden-schweiz` |
| `/freelancer` (en/de/it/es/pt) and `/fr/freelance` | `/einzelfirma-grunden-schweiz` (with matching locale prefix) |
| `/freelance-in-switzerland`, `/freelancing-in-switzerland`, `/freelancer-as-a-registering-self-employed` (all locales) | `/einzelfirma-grunden-schweiz` |
| `/fr/ouvrir-son-entreprise-en-suisse` | `/fr/einzelfirma-grunden-schweiz` |
| `/qr-invoice`, `/qr-billing-and-payments`, `/de/qr-rechnung-software` | `/qr-rechnung-erstellen` |
| `/invoice-template`, `/de/invoice-template`, `/rechnungsvorlage-schweiz` | `/rechnungsvorlage` |
| `/invoice-swiss-individual`, `/rechnung-schweiz`, `/write-an-invoice-for-self-employed-people-in-switzerland`, `/mastering-swiss-invoicing` (all locales) | `/rechnung-schreiben-schweiz` |
| `/convert-monthly-salary-to-hourly-wage-in-switzerland` (all locales) | `/stundenlohn-berechnen-schweiz` |
| `/help`, `/support` (all locales) | `/tutorials` |
| `/alternative-bexio`, `/bexio-alternative-2026`, `/abaninja-2025` | `/alternative/bexio` (some `abaninja-2025` locales go to `/alternative/abaninja`) |
| `/13th-salary` (all locales) | `/mastering-the-13th-month-salary` |
| `/tools-and-utilities/eur-to-chf-conversion` (all locales) | `/euro-conversion` |
| `/vat-method` | `/vat-management` |
| `/login` | `https://app.magicheidi.ch` (external) |
| `/blog/comment-saffilier-a-lavs-en-tant-quindependant` (all locales) | `/ahv-compensation-fund` (2026-07-16 merge) |
| `/gmbh-vs-selbstaendig-vs-ag` (de/fr/it/es/pt) | `/einzelfirma-oder-gmbh-schweiz` (2026-07-16 merge) |
| `/steuerabzuege-selbstaendige-schweiz` (de/fr/it/es/pt) | `/steuerabzuge-schweiz` (2026-07-16 merge) |
| `/blog/generieren-sie-muhelos-schweizerische-rechnungen-mit-qr-code-auf-ihrem-mac-mit-magic-heidi` (all locales) | `/mac` (2026-07-16 merge) |
| `/duplication` (German/bare only — other locales keep the slug) | `/doppelerwerbstaetigkeit-schweiz` (2026-07-16 re-slug) |

If you discover a 301/308 in production that isn't here, it's still real — check `mh-landing/config/redirects.ts`. The list above covers the most common ones a writer might reach for.

**Anchor-text convention (2026-07-16, anti-cannibalization):** always anchor "Buchhaltungssoftware"/"Buchhaltung" → `/buchhaltungssoftware`, "Rechnungsprogramm"/"Rechnungssoftware"/"Fakturierung" → `/rechnungsprogramm`, comparison intent ("Vergleich", "beste …") → `/top-5-buchhaltungssoftware-schweiz`, "bexio Preise" → `/bexio-preise` (not `/alternative/bexio`). Mixed anchors are what let the accounting pillar cannibalize the invoicing pillar.

---

## Core pages

All exist in all 6 locales unless noted.

### Homepage
- **EN**: `/` · **DE**: `/de` · **FR**: `/fr` · **IT**: `/it` · **ES**: `/es` · **PT**: `/pt`
- **When to link**: Sparingly — usually only when introducing Magic Heidi by name to a cold reader.

### Pricing
- **EN**: `/pricing` · **DE**: `/de/pricing` · **FR**: `/fr/pricing` · **IT**: `/it/pricing` · **ES**: `/es/pricing` · **PT**: `/pt/pricing`
- **When to link**: Whenever the article mentions cost, free tier, monthly vs. annual, "is it cheaper than X", or any commercial-intent context.
- **Anchor text examples (EN)**: "Magic Heidi pricing", "see our pricing", "free plan", "44% cheaper than bexio"
- **Anchor (DE)**: "Magic Heidi Preise", "Preisübersicht", "Gratis-Plan ansehen"
- **Anchor (FR)**: "tarifs Magic Heidi", "voir les prix", "forfait gratuit"
- **Anchor (IT)**: "prezzi di Magic Heidi", "piani e prezzi"
- **Anchor (ES)**: "precios de Magic Heidi", "ver precios"
- **Anchor (PT)**: "preços do Magic Heidi", "ver planos"

### Features (all-in-one overview)
- **EN**: `/features` · **DE**: `/de/features` · **FR**: `/fr/features` · **IT**: `/it/features` · **ES**: `/es/features` · **PT**: `/pt/features`
- **When to link**: When listing what Magic Heidi does at a high level, or when an article touches multiple product areas at once.
- **Anchor (EN)**: "all Magic Heidi features", "see what's included"
- **Anchor (DE)**: "alle Funktionen", "Funktionsübersicht"
- **Anchor (FR)**: "toutes les fonctionnalités"
- **Anchor (IT)**: "tutte le funzionalità"
- **Anchor (ES)**: "todas las funcionalidades"
- **Anchor (PT)**: "todas as funcionalidades"

### About / founders
- **EN**: `/a-propos` · **DE**: `/de/a-propos` · **FR**: `/fr/a-propos` · **IT**: `/it/a-propos` · **ES**: `/es/a-propos` · **PT**: `/pt/a-propos`
- **When to link**: When establishing credibility ("built by Swiss freelancers"), the founder story, or "why Magic Heidi exists".
- **Anchor (EN)**: "about Magic Heidi", "the team behind Magic Heidi", "our story"
- **Anchor (DE)**: "über Magic Heidi", "das Team hinter Magic Heidi"
- **Anchor (FR)**: "à propos de Magic Heidi", "l'équipe Magic Heidi"
- **Anchor (IT)**: "chi siamo"
- **Anchor (ES)**: "sobre Magic Heidi", "quiénes somos"
- **Anchor (PT)**: "sobre o Magic Heidi", "quem somos"

### Security & data protection
- **EN**: `/security` · **DE**: `/de/security` · **FR**: `/fr/security` · **IT**: `/it/security` · **ES**: `/es/security` · **PT**: `/pt/security`
- **When to link**: When discussing Swiss data hosting, GDPR/nFADP, encryption, "where is my data", or compliance.
- **Anchor (EN)**: "Swiss data hosting", "data protection", "nFADP-compliant"
- **Anchor (DE)**: "Datenschutz", "Sicherheit", "Daten in der Schweiz"
- **Anchor (FR)**: "sécurité des données", "hébergement en Suisse"
- **Anchor (IT)**: "sicurezza dei dati"
- **Anchor (ES)**: "seguridad de los datos"
- **Anchor (PT)**: "segurança dos dados"

### Reviews & testimonials
- **EN**: `/reviews` · **DE**: `/de/reviews` · **FR**: `/fr/reviews` · **IT**: `/it/reviews` · **ES**: `/es/reviews` · **PT**: `/pt/reviews`
- **When to link**: When making claims about user satisfaction, or when an article needs social proof.

### FAQ
- **EN**: `/faq` · **DE**: `/de/faq` · **FR**: `/fr/faq` · **IT**: `/it/faq` · **ES**: `/es/faq` · **PT**: `/pt/faq`

### Tutorials / help
- **EN**: `/tutorials` · **DE**: `/de/tutorials` · **FR**: `/fr/tutorials` · **IT**: `/it/tutorials` · **ES**: `/es/tutorials` · **PT**: `/pt/tutorials`
- (Legacy `/help` and `/support` redirect here in every locale.)
- **When to link**: When the reader needs a step-by-step walkthrough that is too detailed for the article.

### Blog
- The blog index is locale-prefixed like everything else: `/blog`, `/de/blog`, `/fr/blog`, `/it/blog`, `/es/blog`, `/pt/blog`.
- **When to link**: Sparingly. Link to specific blog articles rather than the index when possible.

---

## Product / feature pages

### Invoicing software (pillar product page)
- **EN**: `/rechnungsprogramm` · **DE**: `/de/rechnungsprogramm` · **FR**: `/fr/rechnungsprogramm` · **IT**: `/it/rechnungsprogramm` · **ES**: `/es/rechnungsprogramm` · **PT**: `/pt/rechnungsprogramm`
- **When to link**: Any article about invoicing, QR-bills, "Rechnungssoftware", "logiciel de facturation", "software fatturazione", invoice templates, sending invoices, or invoice compliance. **Highest-priority commercial page — link from every relevant article.**
- **Anchor (EN)**: "Swiss invoicing software", "QR-bill invoicing app", "create Swiss invoices in seconds"
- **Anchor (DE)**: "Rechnungsprogramm Schweiz", "Rechnungssoftware für Selbständige", "QR-Rechnungen erstellen"
- **Anchor (FR)**: "logiciel de facturation suisse", "créer des factures QR", "logiciel facturation indépendant"
- **Anchor (IT)**: "software di fatturazione svizzero", "fatture QR svizzere"
- **Anchor (ES)**: "software de facturación suizo"
- **Anchor (PT)**: "software de faturação suíço"

### Accounting software (pillar)
- **EN**: `/buchhaltungssoftware` · **DE**: `/de/buchhaltungssoftware` · **FR**: `/fr/buchhaltungssoftware` · **IT**: `/it/buchhaltungssoftware` · **ES**: `/es/buchhaltungssoftware` · **PT**: `/pt/buchhaltungssoftware`
- **When to link**: Any article about Swiss accounting, bookkeeping, Buchhaltung, simplified accounting (Milchbüechli), tax preparation for self-employed, or competitor comparisons (bexio/CashCtrl/Banana).
- **Anchor (EN)**: "Swiss accounting software", "freelancer accounting", "self-employed bookkeeping"
- **Anchor (DE)**: "Buchhaltungssoftware Schweiz", "Buchhaltung für Selbständige", "vereinfachte Buchhaltung"
- **Anchor (FR)**: "logiciel de comptabilité suisse", "comptabilité indépendant"
- **Anchor (IT)**: "software contabilità svizzera"
- **Anchor (ES)**: "software de contabilidad suizo"
- **Anchor (PT)**: "software de contabilidade suíço"

### AI expense scanning
- **EN**: `/ai-expenses-scanning` · **DE**: `/de/ai-expenses-scanning` · **FR**: `/fr/ai-expenses-scanning` · **IT**: `/it/ai-expenses-scanning` · **ES**: `/es/ai-expenses-scanning` · **PT**: `/pt/ai-expenses-scanning`
- **When to link**: Articles about expense tracking, receipts, Belege scannen, Spesen, KI-Belegscanning, multi-currency expenses, tax-deductible expenses, or "I lose my receipts".
- **Anchor (EN)**: "AI receipt scanning", "snap a photo of your receipt", "automatic expense capture"
- **Anchor (DE)**: "Belege scannen mit KI", "Spesen automatisch erfassen"
- **Anchor (FR)**: "scanner les reçus avec l'IA", "saisie automatique des dépenses"
- **Anchor (IT)**: "scansione ricevute con AI"
- **Anchor (ES)**: "escaneo de recibos con IA"
- **Anchor (PT)**: "digitalização de recibos com IA"

### Expense scanner (Beleg-Scanner) — alternate landing
- **EN**: `/beleg-scanner-schweiz` · **DE**: `/de/beleg-scanner-schweiz` · **FR**: `/fr/beleg-scanner-schweiz` · **IT**: `/it/beleg-scanner-schweiz`
- **Not available in es/pt.** From an ES/PT article about expense scanning, link to `/es|pt/ai-expenses-scanning` instead.
- **When to link**: Specifically when the angle is "Beleg-Scanner Schweiz" / "scanner de reçus Suisse" / "scanner ricevute Svizzera" — keyword-targeted variant. Otherwise prefer `/ai-expenses-scanning`.

### VAT management (MWST/TVA/IVA) — pillar
- **EN**: `/mwst-freelancer` · **DE**: `/de/mwst-freelancer` · **FR**: `/fr/mwst-freelancer` · **IT**: `/it/mwst-freelancer`
- **Not available in es/pt.** From ES/PT VAT content, fall back to `/es|pt/buchhaltungssoftware` (which discusses VAT context) or `/es|pt/rechnungsprogramm` for the invoice-side VAT angle.
- **When to link**: Articles about MWST/TVA/IVA registration, the 100k CHF threshold, Saldosteuersatz vs. effektive Methode, VAT returns, foreign-VAT handling.
- **Anchor (EN)**: "Swiss VAT for freelancers", "MWST guide"
- **Anchor (DE)**: "MWST für Freelancer", "MWST-Abrechnung Schweiz"
- **Anchor (FR)**: "TVA pour indépendants suisses", "gestion de la TVA"
- **Anchor (IT)**: "IVA per freelance svizzeri"

### VAT management (alt landing — `vat-management`)
- **All 6 locales**: `/vat-management`, `/de/vat-management`, `/fr/vat-management`, `/it/vat-management`, `/es/vat-management`, `/pt/vat-management`
- This is a **real live page** in every locale (the legacy `/vat-method` redirects here). Use it as the VAT pillar for es/pt content, and as an English-anchor alternative when `/mwst-freelancer` doesn't fit the sentence.
- **When to link**: Same triggers as `/mwst-freelancer`; pick whichever slug reads better in the anchor.

### Swiss VAT pillar (`mwst-schweiz`) — NEW 2026-08-01
- **DE + EN only**: `/mwst-schweiz`, `/en/mwst-schweiz`. The head-term pillar for "MWST Schweiz" / "Mehrwertsteuer Schweiz" (rates 2026, registration threshold, effektiv vs. Saldosteuersatz, ePortal filing, Fristen, Vorsteuerabzug).
- **When to link**: General MWST mentions in de/en content that aren't freelancer-specific (`/mwst-freelancer`), registration-specific (`/mwst-registrierung`), or number-format-specific (`/mwst-nummer-schweiz`). Anchor: "MWST Schweiz" / "Mehrwertsteuer Schweiz".

### VAT number lookup & registration guide (`mwst-registrierung`)
- **All 6 locales**: `/mwst-registrierung` (bare = DE post-migration), `/en/mwst-registrierung`, `/fr/mwst-registrierung`, `/it/mwst-registrierung`, `/es/mwst-registrierung`, `/pt/mwst-registrierung`. Also has DE-only canton subpages (`/mwst-registrierung/zurich`, `/genf`, `/bern`, `/tessin`, `/waadt`, `/aargau`, `/st-gallen`, `/luzern`).
- **When to link**: Articles about the Swiss VAT number format (CHE-XXX.XXX.XXX MWST), verifying/looking up a VAT number via the UID register, or general VAT registration process/threshold content distinct from the freelancer-specific angle already covered by `/mwst-freelancer`.
- **Anchor (EN)**: "Swiss VAT number guide", "VAT registration guide", "how to find your Swiss VAT number"
- **Anchor (DE)**: "MWST-Registrierung Schweiz", "Schweizer MWST-Nummer"
- **Added 2026-07-18**: this page was ranking for "vat number switzerland" / "swiss vat number" (EN queries) but was untracked here and had zero EN inbound links — added to close that gap after a SE Ranking review found it.

### Bank statement import & reconciliation
- **EN**: `/bank-statement-import` · **DE**: `/de/bank-statement-import` · **FR**: `/fr/bank-statement-import` · **IT**: `/it/bank-statement-import` · **ES**: `/es/bank-statement-import` · **PT**: `/pt/bank-statement-import`
- **When to link**: Articles about marking invoices paid, Bankabgleich, camt.053, e-banking exports, payment matching, "stop chasing payments manually".
- **Anchor (EN)**: "import your bank statements", "auto-match payments"
- **Anchor (DE)**: "Bankabgleich automatisieren", "E-Banking-Daten importieren"
- **Anchor (FR)**: "import des relevés bancaires", "réconciliation automatique"
- **Anchor (IT)**: "importazione estratti bancari"
- **Anchor (ES)**: "importación de extractos bancarios"
- **Anchor (PT)**: "importação de extratos bancários"

### Customer management (light CRM)
- **EN**: `/customer-management` · **DE**: `/de/customer-management` · **FR**: `/fr/customer-management` · **IT**: `/it/customer-management` · **ES**: `/es/customer-management` · **PT**: `/pt/customer-management`
- **When to link**: Articles about client/customer organisation, CRM-without-the-CRM, contracts, client revenue tracking.
- **Anchor (EN)**: "client management for freelancers", "lightweight CRM"
- **Anchor (DE)**: "Kundenverwaltung für Freelancer"
- **Anchor (FR)**: "gestion des clients"
- **Anchor (IT)**: "gestione clienti per freelance"
- **Anchor (ES)**: "gestión de clientes"
- **Anchor (PT)**: "gestão de clientes"

### Quotes / estimates
- **All 6 locales**: `/quotes`, `/de/quotes`, `/fr/quotes`, `/it/quotes`, `/es/quotes`, `/pt/quotes`
- **Keyword variant**: `/kostenvoranschlag-schweiz` (translated into en/fr/it/es/pt on 2026-08-01; write the link bare from any locale)
- **When to link**: Articles about quotes, estimates, Kostenvoranschlag, Offerte, Devis, preventivo, estimates that convert to invoices.
- **Anchor (EN)**: "send quotes that convert to invoices", "quote-to-invoice"
- **Anchor (DE)**: "Kostenvoranschlag erstellen", "Offerten schreiben"
- **Anchor (FR)**: "devis qui se transforment en factures"
- **Anchor (IT)**: "preventivi che diventano fatture"
- **Anchor (ES)**: "presupuestos que se convierten en facturas"
- **Anchor (PT)**: "orçamentos que viram faturas"

### Other invoice-related landing pages (all 6 locales unless noted)
| Topic | Slug | Notes |
|---|---|---|
| QR-bill how-to | `/qr-rechnung-erstellen` | All 6 locales |
| Invoice template | `/rechnungsvorlage` | All 6 locales |
| How to write a Swiss invoice | `/rechnung-schreiben-schweiz` | All 6 locales |
| Hourly-rate calculator | `/stundenlohn-berechnen-schweiz` | All 6 locales |
| Cleaning company invoicing | `/reinigungsfirma` | All 6 locales |
| Industries hub | `/industries` | All 6 locales |
| Integrations hub | `/integrations` | All 6 locales |

---

## Platform / device pages

These exist in all 6 languages with identical slugs. Use them when an article specifically discusses a platform, OS, or device.

| Platform | EN | DE | FR | IT | ES | PT |
|---|---|---|---|---|---|---|
| Web app | `/web` | `/de/web` | `/fr/web` | `/it/web` | `/es/web` | `/pt/web` |
| iPhone | `/iphone` | `/de/iphone` | `/fr/iphone` | `/it/iphone` | `/es/iphone` | `/pt/iphone` |
| iPad | `/ipad` | `/de/ipad` | `/fr/ipad` | `/it/ipad` | `/es/ipad` | `/pt/ipad` |
| Android | `/android` | `/de/android` | `/fr/android` | `/it/android` | `/es/android` | `/pt/android` |
| Mac | `/mac` | `/de/mac` | `/fr/mac` | `/it/mac` | `/es/mac` | `/pt/mac` |
| Windows | `/windows` | `/de/windows` | `/fr/windows` | `/it/windows` | `/es/windows` | `/pt/windows` |

**When to link**: Only when the article specifically discusses the device/OS (e.g. "best invoicing app for Mac", "rechnungssoftware iphone", "logiciel facturation mac"). Don't link a platform page just to add an internal link.

**Anchor text style**: Always device-specific. "Magic Heidi for iPhone", "Magic Heidi Mac App", "Rechnungsapp für iPhone", "logiciel facturation Mac".

---

## Use-case / pillar pages

### Sole proprietorship guide (Einzelfirma / société individuelle)
Two canonical slugs cover this topic — both are live in all 6 locales:
- `/einzelfirma-grunden-schweiz` (and `/de|fr|it|es|pt/einzelfirma-grunden-schweiz`) — German-slug pillar, also the redirect destination for `/freelancer`, `/fr/freelance`, `/freelance-in-switzerland`, etc.
- `/societe-individuelle-suisse` (and `/de|fr|it|es|pt/societe-individuelle-suisse`) — French-slug pillar covering the same topic

Pick whichever slug reads better in context (the German slug is the redirect target for legacy `/freelancer` URLs, so it's the more "canonical" one for the topic).

- **When to link**: Articles about becoming self-employed, registering an Einzelfirma / raison individuelle / ditta individuale, "selbständig machen", AHV/AVS registration, Handelsregister, the differences between Einzelfirma and GmbH.
- **Anchor (EN)**: "starting a sole proprietorship in Switzerland", "becoming self-employed in Switzerland"
- **Anchor (DE)**: "Einzelfirma gründen", "selbständig machen Schweiz"
- **Anchor (FR)**: "créer une raison individuelle", "devenir indépendant en Suisse"
- **Anchor (IT)**: "aprire una ditta individuale"
- **Anchor (ES)**: "abrir una empresa individual en Suiza"
- **Anchor (PT)**: "abrir uma empresa individual na Suíça"

**Note**: `/freelancer`, `/de/freelancer`, `/fr/freelance`, `/it/freelancer`, `/es/freelancer`, `/pt/freelancer` all 308-redirect into the `einzelfirma-grunden-schweiz` pillar — always link to the canonical destination directly, not the redirect.

---

## Comparison / alternative pages

The established competitor pages exist in all 6 core locales. The six pages added in the German-first July 2026 campaign initially exist only at their bare German URLs; do not invent locale-prefixed alternates until translations ship.

| Competitor | Canonical German slug |
|---|---|
| bexio | `/alternative/bexio` |
| Banana | `/alternative/banana` |
| WinBIZ | `/alternative/winbiz` |
| smallinvoice | `/alternative/smallinvoice` |
| CashCtrl | `/alternative/cashctrl` |
| Crésus | `/alternative/cresus` |
| Klara | `/alternative/klara` |
| AbaNinja | `/alternative/abaninja` |
| Pebe | `/alternative/pebe` |
| Sage | `/alternative/sage` |
| ERPLight | `/alternative/erplight` (added 2026-07-18 — highest-relevance uncovered organic competitor per SE Ranking, sourced in `context/competitors/erplight.yaml`) |
| Accounto | `/alternative/accounto` (German only, added 2026-07 campaign) |
| Einzly | `/alternative/einzly` (German only, added 2026-07 campaign) |
| Swiss21 | `/alternative/swiss21` (German only, added 2026-07 campaign) |
| sevDesk | `/alternative/sevdesk` (German only, added 2026-07 campaign) |
| Lexoffice / Lexware Office | `/alternative/lexoffice` (German only, added 2026-07 campaign) |
| Zervant | `/alternative/zervant` (German only, added 2026-07 campaign) |

**When to link**: Whenever a competitor is named, in comparison articles, when discussing pricing differences, or when discussing migration. **Only one link per competitor mention** — don't double-link.

**Anchor (EN)**: "Magic Heidi vs bexio", "the bexio alternative for freelancers"
**Anchor (DE)**: "Bexio Alternative für Freelancer", "Magic Heidi vs Bexio"
**Anchor (FR)**: "alternative à bexio pour indépendants", "Magic Heidi vs bexio"
**Anchor (IT)**: "alternativa a bexio per freelance"
**Anchor (ES)**: "alternativa a bexio"
**Anchor (PT)**: "alternativa ao bexio"

---

## Integrations

Hub: `/integrations` (and locale variants). Individual integration pages, all live in all 6 locales:

`/integrations/amazon`, `/integrations/app-store-connect`, `/integrations/etsy`, `/integrations/play-store`, `/integrations/revolut-business`, `/integrations/shopify`, `/integrations/stripe`, `/integrations/sumup`, `/integrations/zapier`.

**When to link**: Only when the article specifically mentions that tool/platform. Don't link an integration page just to add an internal link.

---

## Internal linking best practices

1. **Link naturally** — only when genuinely relevant and helpful to the reader.
2. **Vary anchor text** — don't reuse the same phrase for the same destination URL across an article.
3. **3–5 links per post** is the target (per `seo-guidelines.md`).
4. **Match the language** — German article → `/de/` URLs; French → `/fr/`; Italian → `/it/`; Spanish → `/es/`; Portuguese → `/pt/`; English → root paths (no `/en/` — that 404s, then redirects via the catch-all).
5. **Always use the canonical post-redirect URL** — see redirect table at the top of this file. Linking to legacy paths wastes link equity on a 301/308 and the locale-fallback path triggers an extra 302.
6. **Early links matter** — links in the first 200 words carry more weight.
7. **One competitor mention = one link** — don't double-link the same competitor in the same article.
8. **Check locale availability before linking** — if a page doesn't exist in the article's locale (see "Pages missing in some locales" table), pick a different canonical or use the documented fallback.

---

## Quick reference by topic

**Writing about invoicing / Rechnungssoftware / facturation**:
- `/rechnungsprogramm` (with locale prefix) — primary product page
- `/qr-rechnung-erstellen` — QR-bill how-to (all 6 locales)
- `/rechnungsvorlage` — invoice template (all 6 locales)
- `/rechnung-schreiben-schweiz` — how-to-write-an-invoice (all 6 locales)
- `/iphone` / `/mac` / `/web` — when device is the angle
- `/customer-management` — when sending to clients

**Writing about accounting / Buchhaltung / comptabilité**:
- `/buchhaltungssoftware` — pillar product page
- `/einzelfirma-grunden-schweiz` or `/societe-individuelle-suisse` — when discussing sole proprietorship accounting
- `/bank-statement-import` — for bank reconciliation
- `/mwst-freelancer` (or `/vat-management` for es/pt) — when VAT is mentioned
- `/alternative/bexio` — for any bexio comparison

**Writing about MWST / TVA / IVA / VAT**:
- `/mwst-freelancer` (en/de/fr/it) or `/vat-management` (all 6) — pillar
- `/buchhaltungssoftware` — for the broader accounting context
- `/rechnungsprogramm` — for "VAT automatically on invoices"

**Writing about expenses / receipts / Spesen / Belege**:
- `/ai-expenses-scanning` (all 6 locales) — primary
- `/beleg-scanner-schweiz` (en/de/fr/it only) — keyword-targeted variant
- `/bank-statement-import` — for reconciliation
- `/buchhaltungssoftware` — for "where it all goes"

**Writing about quotes / estimates / Kostenvoranschlag / devis / preventivi**:
- `/quotes` (all 6 locales) — primary
- `/kostenvoranschlag-schweiz` — all locales since 2026-08-01

**Writing about becoming self-employed / starting a freelance business**:
- `/einzelfirma-grunden-schweiz` (with locale prefix) — the pillar (German-slug canonical)
- `/societe-individuelle-suisse` (with locale prefix) — French-slug alternate
- `/mwst-freelancer` — for the 100k threshold conversation
- `/buchhaltungssoftware` — for "what bookkeeping do I need"
- `/pricing` — bottom-of-funnel CTA

**Writing about competitors (bexio, banana, winbiz, smallinvoice, cashctrl, cresus, klara, abaninja, pebe, sage, erplight, accounto, einzly, swiss21, sevdesk, lexoffice, zervant)**:
- The matching `/alternative/<competitor>` page. Use locale variants only where a matching content file exists; the July 2026 campaign pages launch in German first.
- `/pricing` — for the cost comparison
- `/features` — for the feature comparison

**Writing about Magic Heidi as a company / credibility content**:
- `/a-propos` — founder story
- `/security` — Swiss hosting / nFADP
- `/reviews` — social proof

**Writing about devices / "best app for X"**:
- The matching device page (`/iphone`, `/mac`, `/windows`, `/android`, `/ipad`, `/web`)
- `/features` — for "what else does it do"
- `/pricing` — closer

**Writing about hourly rates / Stundenlohn / salaire horaire**:
- `/stundenlohn-berechnen-schweiz` (all 6 locales)

**Writing about an integration partner (Shopify, Stripe, Revolut, etc.)**:
- The matching `/integrations/<tool>` page (all 6 locales)
- `/integrations` — hub

---

*Note: Verify URLs whenever the site structure changes. Source of truth: `mh-landing/content/<locale>/`, `mh-landing/config/redirects.ts`, and the `routeRules` blocks in `mh-landing/nuxt.config.ts`. Last live verification: 2026-07-19.*

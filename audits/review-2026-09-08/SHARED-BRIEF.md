# Shared brief for all content-queue agents (2026-09-08)

## Repos and branch
- Site content lives in `/Users/nathanganser/Documents/Development/mh-landing-articles` (worktree on main) (Nuxt Content, MDC components). Branch `seo/content-queue-2026-09-08` is already checked out there. **Do not commit, do not switch branches, do not run git checkout/stash/reset.** The orchestrator commits at the end.
- SEO workspace: `/Users/nathanganser/Documents/Development/seomachine`. Python with document libs: `/Users/nathanganser/Documents/Development/seomachine/venv/bin/python3` (python-docx, openpyxl, reportlab installed). Put any generator scripts you write in `/Users/nathanganser/Documents/Development/seomachine/templates/<name>_generator.py` so files can be regenerated later.
- Background: `/Users/nathanganser/Documents/Development/seomachine/audits/review-2026-09-08/review.md` (the plan you are implementing). Context files: `seomachine/context/internal-links-map.md` (site structure, redirects, anchor-text rules — READ the "Site structure" section first), `context/features.md` (product facts, pricing: free plan = 3 Rechnungen + 3 Spesen, Pro CHF 25/Mt. annual = CHF 299/Jahr, CHF 39 monthly), `context/brand-voice.md`.

## Site conventions (non-negotiable)
- Locales: bare URL = German (default), `/en/`, `/fr/`, `/it/`, `/es/`, `/pt/` (+ `sq`, `sr` exist, ignore them unless deleting a file that exists there too). Content files: `content/de/<slug>.md` is the German page at `/<slug>`; `content/fr/<slug>.md` is `/fr/<slug>`, etc. Slugs are NOT translated — the German slug is used in every locale.
- **Inline links inside markdown are written bare** (`[text](/rechnungsvorlage)`), never with a locale prefix — the site auto-localizes them. Schema/page-path props are per-locale (`/fr/slug` in the FR file, bare in DE).
- German landing pages use **du-form** (match `content/de/rechnungsvorlage.md`). FR uses **vous**. IT uses **tu**. EN plain.
- Spelling: **MWST** (never MwSt./MWSt.), no **ß** (ss), amounts `CHF 1'250.00`, VAT rates 8.1% / 2.6% / 3.8%, MWST threshold CHF 100'000. Never claim Magic Heidi does "doppelte Buchhaltung". Dates like "Stand: September 2026" where facts can go stale.
- Anchor-text convention: "Buchhaltungssoftware/Buchhaltung" → `/buchhaltungssoftware`; "Rechnungsprogramm/Rechnungssoftware" → `/rechnungsprogramm`; comparison intent → `/top-5-buchhaltungssoftware-schweiz`; "bexio Preise" → `/bexio-preise`.
- **HOLD — do not edit** `content/*/buchhaltungssoftware.md`, `content/*/rechnungsprogramm.md`, `content/*/alternative/bexio.md`, `content/*/top-5-buchhaltungssoftware-schweiz.md` (except where your package explicitly says otherwise). You may link TO them.
- MDC pages: copy component patterns from `content/de/rechnungsvorlage.md` (feature-image hero, `::markdown` with `as: article`, `::feature-grid` for key takeaways, `::hero-basic{.bg-cream}` + `::hero-cta-links` for the download block, FAQ component — look at how that file and `content/de/quittung-vorlage-schweiz.md` do FAQ/schema). Keep frontmatter `title` ≤ 60 chars and `description` ≤ 160 chars. **Never run the seomachine `/scrub` command or `content_scrubber.py` on MDC files — it corrupts them.**
- After editing, sanity-check MDC: every `::component` opener has a matching closing `::`, YAML blocks between `---` are valid, count of top-level fences matches across locales of the same page.

## Downloads
- Files go in `mh-landing/public/downloads/` and are linked as `/downloads/<File_Name>.<ext>`. Existing naming: `Rechnungsvorlage_Schweiz.docx`, `Quittung_mit_MWST_Schweiz.docx`, `KMU_Quittung_Schweiz.xlsx`. Use `<Thing>_Schweiz.<ext>` for DE, `<Thing>_Suisse.<ext>` for FR, `<Thing>_Svizzera.<ext>` for IT.
- Generate real, usable documents: a proper A4 layout, Swiss-correct fields (Absender with UID/MWST-Nr. where relevant, Rechnungs-/Offertennummer, Datum, Gültigkeit, Positionen table with Menge/Einheit/Preis/Total, Zwischentotal, MWST 8.1%, Total CHF, Zahlungsbedingungen, IBAN/QR hint), CHF number formatting, clear placeholder text in [brackets]. Excel versions must contain working formulas (line totals, subtotal, MWST, total). PDF via reportlab (embed a standard font like Helvetica; umlauts must render — test with ä/ö/ü in the output). Open/validate each generated file by re-reading it with the library after writing.
- Download block pattern (copy exactly from `content/de/rechnungsvorlage.md` lines ~54–80): `::hero-basic{.bg-cream}` → `::hero-cta-links` with `links:` entries `{label, url, variant: primary, icon}`.

## Redirects
- **Do not edit `mh-landing/config/redirects.ts`.** Instead append every redirect you need to `/private/tmp/claude-501/-Users-nathanganser-Documents-Development-seomachine/115369fd-c275-4b8c-87d3-1cf916a05b72/scratchpad/redirects-<PACKAGE>.txt` in this exact format, one per line:
  `  { from: '/blog/old-slug', to: '/new-slug', locales: true },`
  (`locales: true` expands to all locales; use `locales: ['fr']` etc. if the source only exists in some locales.)
- When you merge a blog post into a landing page: (1) port any genuinely useful, non-duplicated section/FAQ into the landing page; (2) `git rm` the blog post in EVERY locale where it exists (`ls content/*/blog/<slug>.md`); (3) record the redirect; (4) grep the whole `content/` tree for inline links to the deleted slug and repoint them.

## Reporting
- When done, write `/private/tmp/claude-501/-Users-nathanganser-Documents-Development-seomachine/115369fd-c275-4b8c-87d3-1cf916a05b72/scratchpad/report-<PACKAGE>.md`: files created/edited/deleted, downloads generated (with sizes), redirects recorded, anything you could not do and why, and any facts you were unsure about. Keep it under 60 lines.
- Only touch the files listed in your package. If you find you need to edit a file owned by another package, write the needed change into your report instead.

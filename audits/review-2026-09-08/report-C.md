# Report – Package C: Budgetplaner Vorlage for /budgeting-apps (2026-09-08)

## Downloads generated (mh-landing/public/downloads/, all validated by re-opening with openpyxl / pypdf; DE xlsx also recalculated in LibreOffice headless: 0 formula errors)
- Budgetplaner_Vorlage_Schweiz.xlsx (12,620 B) + .pdf (8,644 B, 2 pages A4) – DE
- Planificateur_Budget_Suisse.xlsx (12,691 B) + .pdf (8,762 B) – FR
- Pianificatore_Budget_Svizzera.xlsx (12,663 B) + .pdf (8,805 B) – IT
- Budget_Planner_Switzerland.xlsx (12,500 B) + .pdf (8,610 B) – EN
- Generator: seomachine/templates/budgetplaner_generator.py (parameterised by language; `venv/bin/python3 templates/budgetplaner_generator.py [de fr it en] [--out DIR]`)

## What the Excel contains (same structure in all 4 languages, 117 formulas on the monthly sheet)
- Sheet 1 "Monatsbudget": Einnahmen / Fixkosten (Miete, KVG, Versicherungen, Telefon/Internet, Abos, Mobilität) / Variable Kosten / Rückstellungen / Zusammenfassung. Columns: Soll Geschäft, Soll Privat, Soll Total, Ist Geschäft, Ist Privat, Ist Total, Differenz, Notiz. Green = input, grey = formula; conditional formatting turns a negative Differenz red (over budget).
- Rückstellungen are formula-driven from the Richtwerte sheet: Steuern 25% of Geschäftsgewinn, AHV/IV/EO 10%, MWST = Umsatz × 8.1/108.1 (0% if not pflichtig), Säule 3a = IF(PK="ja", 7'258/12, MIN(20% × Gewinn, 36'288/12)). Totals, Total Ausgaben, Differenz Soll/Ist and Sparquote (%) are formulas.
- Sheet 2 "Jahresübersicht": 12 months × (Einnahmen, Fixkosten, Variable, Steuern/AHV/MWST, Sparen & Vorsorge) with Total Jahr, Ø Monat, Soll/Monat (linked to sheet 1), Total Ausgaben, Differenz, Sparquote formulas.
- Sheet 3 "Richtwerte": editable parameters (tax %, AHV %, MWST %, PK ja/nein dropdown via data validation, 3a maxima 7'258 / 36'288, 3a 20%) + the exact Richtwerte table from the page (Wohnen max. 25–30% … Freizeit Rest) with "Ihr Budget (Soll)" and "Ihr Anteil" formulas pulling from sheet 1. Source note cites budgetberatung.ch.
- CHF number format `#,##0.00`, A4 landscape print setup, frozen header, footer "Stand: September 2026".
- PDF: page 1 printable monthly sheet (Position | Soll Geschäft | Soll Privat | Ist | Differenz) + Faustregeln; page 2 Richtwerte table + blank 12-month Jahresübersicht grid. Helvetica; umlauts/accents verified in extracted text and rendered PNGs.

## Page edits (content/{de,fr,it,en}/budgeting-apps.md; es/pt untouched)
- New `::hero-basic{.bg-cream}` + `::hero-cta-links` download block (Excel primary, PDF secondary, same pattern as rechnungsvorlage.md) inserted right after the "Budget erstellen in 5 Schritten" markdown block, before `::pages-landing-comparison`. Title DE "Gratis Budgetvorlage Schweiz (Excel & PDF)", FR "Modèle de budget Suisse gratuit (Excel & PDF)", IT "Modello di budget Svizzera gratuito (Excel & PDF)", EN "Free Swiss Budget Template (Excel & PDF)".
- Paragraph that deferred to budgetberatung.ch rewritten: keeps the budgetberatung.ch/budgetvorlagen link as the Richtwerte source, now introduces our own template.
- H2 renamed: DE "Budget erstellen in 5 Schritten: Budgetplaner Vorlage und Schweizer Richtwerte" (FR/IT/EN equivalents with "modèle de budget gratuit" / "modello di budget gratuito" / "Free Budget Planner Template").
- Meta description updated in all 4 locales to mention the template (DE 159, FR 158, IT 157, EN 158 chars). Titles unchanged.
- One FAQ added after the "gratis Budgetprogramm" question: DE "Gibt es eine gratis Budgetvorlage für die Schweiz?" (+ FR/IT/EN). FAQ count 8 → 9 in all locales.
- MDC check: top-level `^::` fences 24 → 26 in all four locales; openers == closers in each file. Nothing else on the pages was changed.

## Redirects
- None needed (no file deleted).

## Not done / notes
- The DE page uses Sie-form (rewrite from today kept it); new DE copy matches the page's Sie-form rather than the brand-wide du rule, to avoid a mixed page. Flag if a du-conversion of the whole page is wanted.
- The `hero-cta-links` `title` is what renders the "Gratis Budgetvorlage Schweiz (Excel & PDF)" heading; if that component renders it as a non-heading element, the keyword is still covered by the renamed H2.
- Facts used: AHV/IV/EO Selbständige 10% (voller Satz, from content/de/ahv-compensation-fund.md; labelled "Richtwert ca. 10%" since the sinking scale starts at 5.371%); Steuern 25% labelled Richtwert; Säule 3a 7'258 / 36'288 / 20% reused from the rewrite change log. All figures are labelled as Richtwerte, not tax advice.
- Not re-run: no site build/render check of the new block (Nuxt dev server not started); the pattern is copied verbatim from rechnungsvorlage.md.

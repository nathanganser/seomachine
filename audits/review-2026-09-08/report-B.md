# Report — Package B (Vorlagen downloads + /vorlagen hub) — 2026-09-09

## Downloads generated (mh-landing/public/downloads/, all re-opened + validated, umlauts confirmed in PDF text)
- Lieferschein_Vorlage_Schweiz.docx 38'776 B · .xlsx 7'136 B (12 positions, optional price col w/ line totals, Stück sum) · .pdf 4'020 B
- Kassenbuch_Vorlage_Schweiz.xlsx 14'618 B (100 rows, running Saldo, MWST dropdown+formula, Soll/Ist, Monatsübersicht sheet w/ SUMPRODUCT by month, Anleitung sheet) · .pdf 4'137 B (blank 26-row sheet) · .docx 38'498 B
- Arbeitsrapport_Vorlage_Schweiz.xlsx 15'283 B (sheets: Stundenrapport 61 rows w/ Stunden=(Bis-Von)-Pause, Total=h×Satz, KW; Übersicht KW 1–53 + months; Arbeitsrapport job form w/ Material) · .docx 39'504 B (2 pages) · .pdf 6'361 B (2 pages)
- Zahlungserinnerung_Vorlage_Schweiz.docx 38'582 B · .pdf 3'184 B (friendly pre-Mahnung letter, invoice table, IBAN block)
- Spesenabrechnung_Vorlage_Schweiz.xlsx 10'272 B (30 rows, MWST/Netto formulas from brutto, category/rate/payment dropdowns, km × CHF 0.70, Auszahlungsbetrag = SUMIF "Privat bezahlt" + km) · .pdf 4'271 B (landscape blank)
- Generators: seomachine/templates/{template_common,lieferschein,kassenbuch,arbeitsrapport,zahlungserinnerung,spesenabrechnung}_generator.py + validate_downloads.py (re-opens all 13 files). Rendered every docx/xlsx via LibreOffice + PDFs via pdftoppm and eyeballed them. `pypdf` was pip-installed into the seomachine venv for validation.

## Content files edited/created (mh-landing, branch seo/content-queue-2026-09-08, uncommitted)
- content/de/lieferschein-schweiz.md — full rewrite: du-form, title/description now "Lieferschein Vorlage", key-takeaways grid, `::hero-basic{.bg-cream}` download block (Word/Excel/PDF), format section, FAQ w/ Excel/Word answers, "Alle Vorlagen" link. Dropped the DE/FR/IT/EN "Mehrsprachen-Recherche" filler.
- content/de/kassenbuch-schweiz.md — full rewrite: du-form, download block (Excel/PDF/Word), "Was die Excel-Vorlage kann", Excel-Nachvollziehbarkeit guidance, FAQ; removed "30 Tage gratis" claims (→ free plan 3 Rechnungen + 3 Spesen); dropped research filler.
- content/de/arbeitsrapport-schweiz.md — full rewrite: du-form, download block, new "Zeiterfassung Excel Vorlage" H2 + Stundenrapport row in comparison table; NO Magic Heidi time-tracking claim (features.md has none).
- content/de/mahnung-vorlage-schweiz.md — converted page prose to du (letter texts stay Sie), download block now cream pattern (Zahlungserinnerung Word+PDF primary, 3 .txt secondary), new "Zahlungserinnerung Vorlage Schweiz" section, 4-stage ladder Zahlungserinnerung → 1. → 2. → 3./Betreibungsandrohung, "keine Mahnpflicht vor Betreibung", Art. 102/104 OR 5%. Only DE + sr exist; sr untouched.
- content/de/spesenabrechnung-vorlage-schweiz.md — was plain markdown with NO download; rewritten as MDC (hero, takeaways, download block Excel+PDF, FAQ component, CTA), du-form, worked example matches the Excel formulas.
- NEW content/de/vorlagen.md, content/fr/vorlagen.md (vous), content/it/vorlagen.md (tu), content/en/vorlagen.md — hub: hero + intro, `feature-grid` cards (10 templates DE) + 3 calculator cards, "Vorlage oder Software" (≈5 Rechnungen/Mt., free plan 3+3, CHF 25/Mt. annual), FAQ, CTA.
- content/{de,fr,it,en}/quittung-vorlage-schweiz.md — one sentence linking /vorlagen after the download section (FR/IT/EN added too so the localized hubs get an inbound link; revert if unwanted).
- Sanity: every `::` fence balanced, every component YAML block parses, titles ≤60 / descriptions ≤160, no ß / MwSt, inline links bare.

## Not done / please add (files owned by other packages)
- content/de/rechnungsvorlage.md — suggested line (end of "Rechnungsvorlage Schweiz herunterladen und loslegen" or after the format section): `Weitere Gratis-Vorlagen für Offerte, Quittung, Mahnung, Lieferschein und Kassenbuch findest du in der [Übersicht aller Vorlagen](/vorlagen).`
- content/de/kostenvoranschlag-schweiz.md — suggested line: `Alle Gratis-Vorlagen (Rechnung, Offerte, Quittung, Mahnung, Lieferschein, Kassenbuch) auf einer Seite: [Übersicht aller Vorlagen](/vorlagen).`
- No redirects needed (no redirects-B.txt).

## Caveats / facts to double-check
- /offerte-vorlage-schweiz exists only in de + fr at the time of writing; IT/EN hubs list it (and mahnung/lieferschein/kassenbuch/arbeitsrapport/spesen, all DE-only) under a "available in German" paragraph — those links resolve via the site's locale fallback (one extra hop). Move them into the card grid if the other package ships IT/EN versions.
- DE hub card copy for Offerte/Kostenvoranschlag/Budgetplaner describes formats based on files seen on disk (Offerte_Vorlage_Schweiz.{docx,xlsx,pdf}, Kostenvoranschlag_Schweiz.{docx,pdf}, Budgetplaner_Vorlage_Schweiz.{xlsx,pdf}) — adjust if those packages change formats.
- Kilometer rate CHF 0.70/km cited as the SSK Muster-Spesenreglement standard (editable in the sheet). Betreibungskosten "ab rund CHF 20" on the mahnung page is a generic figure from the SchKG-GebV lower bracket.
- Excel formulas use WEEKNUM(date,21) for ISO weeks (Excel 2010+, LibreOffice OK; untested in Numbers). All formulas verified by LibreOffice recalculation during rendering.
- template_common.py is shared; the Offerte/Budgetplaner generators from other packages may import it — I changed docx_page_break() and _set_widths() semantics (both additive/safe).

# Report — package "keepers-1" (5 industry-invoicing posts, DE only)

Branch `seo/content-queue-2026-09-08` in mh-landing. Nothing committed. Only `content/de/blog/<slug>.md` touched — no other locale, no other file. No redirects needed.

Method: scripted Sie→du pass (`SP/siedu.py` + `siedu2.py`, backups in `SP/backup/`), then a full manual review of every changed line per file (`SP/p_*.txt` = literal replacement sets applied via `SP/apply.py`). All remaining "Sie" are third person (story characters, "die Rechnung … Sie zeigt").

## dachdecker-rechnung-schweiz.md — validator PASS
- Full du-form (incl. hero, pain grid, FAQ, CTA). Takeaway block renamed to "Das Wichtigste in Kürze".
- Softened: material markup "15–25%" → branchenüblicher Aufschlag; Notfall-Multiplikatoren 1.3×–2.0× and CHF 100–200 Einsatzgebühr → qualitative Zuschläge; Vorsteuer example "CHF 2'430" → "gegen CHF 2'400"; Lena story's "8 Std./CHF 920" invented savings removed.
- **bexio "ab CHF 52/Monat" removed in 3 places** (stale — `content/de/bexio-preise.md` lists CHF 35/42/69/119) and replaced by links to `/bexio-preise`. Magic Heidi price stated as CHF 25 annual / CHF 39 monthly + 3 free invoices.
- Added a `/rechnungsvorlage` link (file already had /rechnungsprogramm ×4, /mwst-freelancer ×3, /pricing, /qr-rechnung-erstellen).
- Fixed "im Offerte" → "in der Offerte".

## eventplaner-rechnung-schweiz.md — validator PASS
- Title was 86 chars → "Eventplaner-Rechnung Schweiz 2026 | Magic Heidi" (46).
- **All "8,1 %" style comma/space percentages converted to 8.1% / 3.8% / 3.7% / 7.7%** (~25 occurrences).
- **Factual fix: QR-Rechnung dated "1. Oktober 2020" in 4 places → Oktober 2022** (ESR abolished 30.09.2022).
- **Math fix in the Durchlauferposten example**: CHF 12'000 incl. 8.1% is net CHF 11'100.83 + CHF 899.17 (file had 11'002.77 + 997.23 = 9.06%). Both the prose and the bullet list corrected; the invoice template's own figures were verified correct.
- Replaced the odd "«MWST nicht ausweisbar»" wording with "Kein MWST-Ausweis, da nicht MWST-pflichtig".
- Removed "etwa 42% günstiger als bexios CHF 52/Monat"; removed invented Kilometer/Spesen assertions ("was AHV/ESTV akzeptieren", "CHF 50–70 Pauschale") and the flat "Kilometerentschädigung ist nicht MWST-pflichtig" claim → now points to Treuhand in Zweifelsfällen; storno percentages (30/70/100%) generalised.
- Takeaway heading → "Das Wichtigste in Kürze"; added `/rechnungsvorlage` + `/mwst-freelancer` links.

## heilpraktiker-rechnung-schweiz.md — validator PASS
- Full du-form; takeaway block renamed. Fixed script false positives where "Ihr" meant "her" (Sarah/Lena stories).
- **AHV rate "ca. 10.1%" → "rund 10% (AHV/IV/EO, bei kleinen Einkommen tiefer) plus Verwaltungskosten"** (3 places incl. FAQ).
- Softened: "CHF 120–180 pro Sitzung/Stunde" hourly claims, "überwältigende Mehrheit", Lena's "3 Stunden/Monat" savings; kept the hedged Honorar table.
- Typos fixed: "Praxis kantons", "ausserWeiterbildung"; dead CTA "**Jetzt mit Magic Heidi abrechnen →**" now links to /rechnungsprogramm; added `/rechnungsvorlage` link.

## logopaede-rechnung-schweiz.md — validator PASS
- Full du-form; takeaway renamed; several "du sich" → "du dich" and broken feature bullets rewritten.
- Softened: Claudia story's invented CHF 85'000 / 4'200 / 1'200 figures; KVG tariff "CHF 95–140" (kantonal, not sourceable) → qualitative; UVG "10–20% über KVG" → "in der Regel über dem KVG-Tarif"; AHV 10.1% → rund 10%; Daniel's "CHF 6'800" → "vierstellige Nachforderung".
- bexio "CHF 52/Monat" removed (2 places) → `/bexio-preise` link.

## nagelstudio-rechnung-schweiz.md — validator PASS
- Full du-form; "Das Wichtigste auf einen Blick" → "Das Wichtigste in Kürze" (added a 6th bullet linking `/rechnungsvorlage`; removed the price-range bullet).
- Description rewritten (dropped the English "compliant"; body "compliant Rechnungen" → "korrekte Rechnungen").
- **Legal fix**: "Studio-Name muss den Zusatz 'Einzelfirma' enthalten" → Einzelfirma must carry the owner's family name. **QR-IBAN section rewritten**: a normal IBAN is fine without a structured reference; QR-IBAN only for the 27-digit QR reference (was: "QR-Rechnung benötigt QR-IBAN, endet mit Prüfcode").
- "MWST ausweisen ohne Registrierung ist ungültig" → "nicht zulässig"; threshold normalised to CHF 100'000 (was CHF 100'000.00 in 9 places); AHV 10.1%/CHF 5'050 → rund 10% / rund CHF 5'000; removed CHF 200–400 insurance, CHF 20–50 Anfahrtspauschale and the "15 Min./5 Min. pro Quartal" claims; bexio CHF 52 → `/bexio-preise`.

## Notes / uncertainties
- Hourly-rate ranges that read as market observation and are labelled "typisch/üblich" were kept (dachdecker CHF 90–170/h incl. title-adjacent description, eventplaner CHF 80–150/h, logopäde private rates). Everything stated as a fee, statistic or savings figure that could not be sourced was made qualitative or deleted.
- All bexio price mentions across these 5 files now point at `/bexio-preise` instead of repeating a number — that page itself should stay the single source of truth (it currently lists CHF 35/42/69/119).
- Fictional customer anecdotes (Thomas, Sarah, Lena, Claudia, Daniel, Lisa, Nadia) were left in place, minus their invented CHF amounts; if the policy is to drop invented testimonials entirely, that is a separate pass.

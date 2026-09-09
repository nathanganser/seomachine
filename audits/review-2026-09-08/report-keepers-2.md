# Report: keepers-2 — 4 auto-generated German blog posts (Sie→du + cleanup)

Branch `seo/content-queue-2026-09-08` in mh-landing. Nothing committed, no branch switches. Only the 4 German files touched.

## Files edited
- content/de/blog/schreiner-rechnung-schweiz.md
- content/de/blog/tattoo-artist-invoicing-switzerland.md
- content/de/blog/invoicing-translator-interpreter-switzerland.md
- content/de/blog/treuhaender-aufgaben-schweiz.md

## schreiner-rechnung-schweiz — validator PASS (title 50 / desc 148)
- Full Sie→du (was 111). 4 remaining "Sie" are third-person (Schlussrechnung, QR-IBAN, QR-Referenz, Registrierung).
- Blockquote takeaways -> `::feature-grid{id: key-takeaways}` (5 bullets) after intro.
- Removed all "CHF 70-150/h" rate claims (title, desc, hero, pain, body, FAQ). Removed invented stats: 35->12 Tage Zahlungsfrist, CHF 920 verlorene Zeit, CHF 2'025 Vorsteuer, 15-25% Materialaufschlag, Holz CHF 80-400/m3, Anfahrt CHF 0.70-1.00/km, bexio CHF 52/Mt.
- Named mini-stories (Stefan/Karin/Markus) reframed as anonymous "Beispiel aus der Praxis" (no fake testimonials).
- Corrected MWST transition rule (Leistungserbringung statt Rechnungsdatum). Added 2.6% / 3.8%.
- Links added: /beleg-scanner-schweiz, /buchhaltungssoftware (only as "wenn du doppelte Buchführung brauchst"), /bexio-preise. Kept /rechnungsprogramm, /rechnungsvorlage, /qr-rechnung-erstellen, /mwst-freelancer, /pricing.

## tattoo-artist-invoicing-switzerland — validator PASS (title 48 / desc 155)
- Full Sie→du (was 179). 1 remaining "Sie" is third-person (Buchungsgebühr).
- "## Die wichtigsten Punkte" list -> `::feature-grid{id: key-takeaways}` after intro.
- 8,1% / 2,6% / 10,3% -> dot notation; added 3.8% Sondersatz.
- FIXED FACT: AHV 10.3% was wrong -> "rund 10% (AHV+IV+EO), degressive Skala" + ahv-iv.ch link.
- FIXED FACT: invented rule "MWST-Schuld unter CHF 5'000 = jährliche Abrechnung" -> correct effektiv/Saldo/jährlich framing.
- Removed CHF 150-500/h everywhere (the "was kostet ein Tattoo-Künstler" FAQ rewritten as "wie setze ich meinen Stundensatz fest"), depot CHF 100-300, Gewerbegebühr CHF 20-100, bexio CHF 52/Mt., CHF 208'000/Jahr calc, "AXA oder ähnlich".
- Fixed mistranslation "massgeschlagen" -> "individuell gestaltet"; "Prüfertechte" -> "Prüfsichere"; QR-Rechnung dating (2020 eingeführt, alte Scheine seit Okt. 2022 nicht mehr verarbeitet).
- Links added: /rechnungsvorlage, /qr-rechnung-erstellen, /beleg-scanner-schweiz, /buchhaltungssoftware, /bexio-preise, /einzelfirma-grunden-schweiz.

## invoicing-translator-interpreter-switzerland — validator PASS (title 47 / desc 152)
- Full Sie→du (was 148). 1 remaining "Sie" is third-person (Leistungsbeschreibung).
- Blockquote takeaways -> `::feature-grid{id: key-takeaways}` after intro.
- All "8,1 %" / "2,6 %" / "7,7 %" / "+30 %" / "50 %" -> dot + no space.
- FIXED FACT: Beherbergungssatz "3,7 %" -> 3.8%.
- FIXED FACT: "SBB-Tickets sind MWST-befreit" is false -> replaced with "prüf den konkreten Beleg".
- Removed unsourceable rate tables: per-word CHF 0.20-0.60, per-line CHF 2.50-7.00, Konferenz CHF 700-1'500/Tag, ASTTI CHF 70-150 / 100-200, juslingua CHF 120/h, Bundesspesen CHF 14/30/44/88, Mindestgebühr CHF 300-600, Storno 50/100%, "42% günstiger als bexio", bexio CHF 52/Mt. ASTTI + juslingua now cited as sources to check, not quoted. Remaining CHF figures explicitly labelled Beispielwerte.
- Links added: /rechnungsvorlage (x2), /qr-rechnung-erstellen, /mwst-freelancer, /mwst-nummer-eu-kunden, /pauschalspesen-schweiz, /beleg-scanner-schweiz, /buchhaltungssoftware.

## treuhaender-aufgaben-schweiz — validator PASS (title 38 / desc 152)
- Full Sie→du (was 54). Zero reader-directed occurrences left. Nested ::blog structure preserved (2-space indent, matches nebenberuflich-selbstaendig-schweiz.md).
- "## Das Wichtigste auf einen Blick" -> nested `::feature-grid{id: key-takeaways}` between two ::markdown blocks inside ::blog.
- ALL Treuhänder fee figures removed: cost table (CHF 150-250/h, CHF 200-500/Mt., CHF 800-3'000, CHF 400-1'000, CHF 60-120), "CHF 2'000-4'000/Jahr", and the two FAQ answers quoting them. Replaced with "kein offizieller Tarif — frei vereinbart, je nach Kanton und Mandat" + checklist of price drivers.
- Invented case studies (Sarah CHF 2'400->1'200 gespart, Markus CHF 1'800, Lena CHF 450) reframed as anonymous scenarios without amounts.
- FIXED FACT: "«Treuhänder» ist ein geschützter Begriff" is false -> "der Begriff selbst ist nicht geschützt, geschützt sind die Titel dahinter (eidg. Fachausweis)".
- FIXED: "Wann ist ein Treuhänder gesetzlich vorgeschrieben" reframed (the law mandates bookkeeping, not a Treuhänder). Duplicated "Nach OR Art. 957a OR" and typos (vereinfert, spare sich) fixed. "8.1 %" -> "8.1%".
- Broken link /invoicing (page does not exist) -> /rechnungsprogramm.
- Three redirect-only links repointed to live targets: /blog/buchhaltung-fuer-anfaenger -> /buchhaltung-einzelfirma-schweiz; /blog/jahresabschluss-checkliste -> /jahresabschluss-schweiz; /blog/steuererklarung-selbstaendig-unterlagen-schweiz -> /tax-return-2024.
- /buchhaltungssoftware added with required framing: "Magic Heidi ist bewusst keine Software für doppelte Buchhaltung." Doppelte Buchhaltung only ever attributed to the Treuhänder.

## Validation
`validate_mdc.py` on all four: 4 files checked, 0 failed. YAML of every component block parses. No ß, no MwSt./MWSt., no comma decimals, no "8,1 %" spacing in any of the four files.

## Not done / notes
- No redirects needed (nothing deleted or renamed) — no redirects-keepers-2.txt written.
- Frontmatter `title` changed on all four (old ones were over-length or carried unsourceable rates). Slugs unchanged.
- Hedged rather than asserted: exact AHV self-employed rate ("rund 10%"), MWST reporting frequency rules, Bundesspesen per-diems, and all Treuhänder/translator/tattoo market rates.
- schreiner cites Art. 26 MWSTV while tattoo cites Art. 26 MWSTG. Both provisions exist; left each as the original author had it rather than unifying across packages.

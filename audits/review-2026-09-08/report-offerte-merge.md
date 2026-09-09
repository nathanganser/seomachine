# Offerte merge — downloads rebuilt + blog content ported (2026-09-09)

Working tree: `/Users/nathanganser/Documents/Development/mh-landing-articles` (branch `main`, nothing committed).

## 1. Downloads rebuilt

Generator (single reproducible source, now merges both workstreams):
`/Users/nathanganser/Documents/Development/seomachine/templates/offerte_vorlage_generator.py`
Rebuild: `venv/bin/python3 templates/offerte_vorlage_generator.py --out <repo>/public/downloads --stems Offerte_Vorlage_Schweiz,Devis_Modele_Suisse`
(new `--stems` flag; run without it to also rebuild the two Kostenvoranschlag/Devis-estimatif sets — deliberately NOT rerun, they belong to another package.)

Kept from the other workstream (`SP/their-build-downloads.py`): `[FIRMENNAME / LOGO]` header placeholder + `Vorlage: magicheidi.ch · Stand September 2026` strip on DOCX/PDF, blue-input / grey-formula cell convention, navy header bar, gridlines off, A4 fit-to-width print setup, and the three-sheet workbook (Anleitung · Offerte · Beispiel).
Kept from the seomachine generator: the complete Swiss field set and the spec-driven DOCX/PDF layout.
Not kept: their LibreOffice DOCX→PDF export step (not reproducible from the generator) — the PDF is reportlab/Helvetica, umlauts verified.

| file | bytes | contents |
|---|---|---|
| Offerte_Vorlage_Schweiz.docx | 39'573 | 1 page A4, 6 tables, logo header, magicheidi footer |
| Offerte_Vorlage_Schweiz.xlsx | 13'175 | sheets Anleitung / Offerte / Beispiel — **48 formulas** (24 + 24) |
| Offerte_Vorlage_Schweiz.pdf  |  4'321 | 1 page, umlauts OK, magicheidi strip |
| Devis_Modele_Suisse.docx     | 39'621 | 1 page A4, 6 tables |
| Devis_Modele_Suisse.xlsx     | 13'274 | Instructions / Devis / Exemple — **48 formulas** |
| Devis_Modele_Suisse.pdf      |  4'423 | 1 page, accents OK |

Formulas per form sheet (24): 10 × `=IF(B..="","",ROW()-18)` position numbers, 10 × `=IF(OR(B..="",C..=""),"",ROUND(C..*E..,2))` line totals, `=SUM(F19:F28)` Zwischentotal, `=ROUND(F30*F31,2)` MWST, `=F30+F32` Total, `="Offerte Nr. "&F1` title. F31 is the editable rate cell (0.081, dropdown 0% / 2.6% / 3.8% / 8.1% + input hint); the "Nicht MWST-pflichtig? 0 % wählen und UID-Zeile leer lassen" note sits under every sheet and in the Anleitung.
Swiss formatting is now locale-pinned (`[$-807]` / `[$-100C]`) so amounts render `1'250.00` / `CHF 4'291.57` regardless of the reader's locale — verified by a LibreOffice recalculation (headless en-US) which still printed `3'970.00 / 321.57 / CHF 4'291.57`.
The Beispiel/Exemple sheet is filled with the same worked example as the landing page (8 × 140 + 1 × 2'500 + 10 × 35 = 3'970.00, 8.1 % = 321.57, total 4'291.57) and is labelled FIKTIVES BEISPIEL / EXEMPLE FICTIF with a fake UID.
Every file is re-opened by the generator's `validate()` (python-docx / openpyxl / pypdf): sheet names, each formula cell, rate cell, dropdown, Swiss number format, umlaut probe, magicheidi strip, logo placeholder, page count, and that the example still sums to 4'291.57. Result: **validation OK**. Layout was additionally eyeballed via LibreOffice → PNG.

## 2. Content ported from the deleted blog post

Ported into `content/de/offerte-vorlage-schweiz.md` (du-form) and mirrored into `content/fr/…` (vous):
- **OR Art. 373 / 375** (Werkvertrag: fixed price binds you; an approximate estimate overrun "in a disproportionate measure" lets the client withdraw) — the blog's strongest unique legal point, verified, added after the comparison table.
- **3 new FAQ answers** about the files themselves: logo insertion, "does Word/PDF calculate?" (no — only Excel, don't overwrite the grey cells), "more than ten positions?" (extend formulas + sum range + print area).
- **Pre-send check + unique file name** (`Offerte-2026-014-Kundenname.pdf`) folded into step 7.
- **Customer's own inputs/cooperation** added to mandatory field 8 (blog's "Voraussetzungen / nötige Mitarbeit der Kundschaft").
- **"makrofrei"** and the three-sheet description added to the format section.

Rejected: the download-format table, the "Welche Angaben gehören in eine Offerte" list, the MWST section and the Offerte-vs-Kostenvoranschlag framing (all already on the page); the blog's own Excel example (8 h × CHF 120 + CHF 240 — replaced by the page's worked example so file and page agree); the deep ESTV URL `estv.admin.ch/de/mwst-steuersaetze-schweiz` and the fedlex ELI link (could not verify the exact paths; the page already links `estv.admin.ch` and cites articles in prose); the `/blog/friseur-rechnung-schweiz` link (off-topic here); "Überarbeitet am 8. September 2026" (page already carries "Stand: September 2026").

Trimmed to stay inside the word budget: the Auftragsbestätigung sample block (that document has its own page, `/auftragsbestaetigung-schweiz` — section kept, shortened to prose + link), and three repetitions of the Magic-Heidi pitch that already appear in the comparison table and the feature-showcase.

## 3. Validation

- `validate_mdc.py content/de/offerte-vorlage-schweiz.md` → 1 files checked, 0 failed
- `validate_mdc.py content/fr/offerte-vorlage-schweiz.md` → 1 files checked, 0 failed
- Rendered words: DE 2'762 → **2'859**; FR 3'288 → **3'407** (French runs ~19 % longer for identical content).
- All six `/downloads/...` URLs referenced by the two pages exist on disk.
- Component fence parity DE/FR identical (15 top-level openers, 2 nested, 17 closers each). No `ß`, no `MwSt.`, CHF amounts use apostrophes.

## 4. Notes / not done

- No redirect needed: the blog post was already deleted and redirected by the merge; nothing in `content/` links to `/blog/offerten-vorlage-schweiz`.
- `Kostenvoranschlag_Schweiz.*` and `Devis_estimatif_Suisse.*` were NOT regenerated (owned by another package) — they will pick up the new header/footer and tighter one-page layout the next time the generator runs without `--stems`.
- The invented "Installateur aus St. Gallen" anecdote on the page reads as a real case; left untouched (pre-existing, not mine), but flagging it.

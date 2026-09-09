# Report — Package A: /offerte-vorlage-schweiz (2026-09-09)

## Created
- `mh-landing/content/de/offerte-vorlage-schweiz.md` — new DE landing page (du-form). Title 54 chars, description 154. ~2'550 prose words (2'762 incl. two code-block examples; reference `rechnungsvorlage.md` counts 2'683 with the same script). Structure mirrors rechnungsvorlage: hero → answer-first intro → key-takeaways grid → download block → format section → 10 mandatory fields grid → MWST → Gültigkeit (OR Art. 3/5/7) → comparison table Offerte/Kostenvoranschlag/Auftragsbestätigung/Rechnung → 7-step guide + filled example → Stundensatz/Pauschale + Klauseln → Offerte→Rechnung → **Auftragsbestätigung Vorlage** section (targets "auftragsbestätigung vorlage") → Vorlage-vs-Software table → feature-showcase → 7-question FAQ (component emits FAQPage schema) → Fazit with `/vorlagen` link → final CTA.
- `mh-landing/content/fr/offerte-vorlage-schweiz.md` — faithful vous-form translation, FR file names, same 17 fences. Title 56, description ≤160. FR counts ~3'290 (French runs ~20% longer than DE).
- `seomachine/templates/offerte_vorlage_generator.py` — regenerates all downloads; validates every file by re-opening (python-docx / openpyxl / pypdf — pypdf was pip-installed into the venv).

## Downloads generated (`mh-landing/public/downloads/`)
Offerte_Vorlage_Schweiz.docx 39 KB · .xlsx 7.3 KB · .pdf 4.8 KB · Devis_Modele_Suisse.docx 39 KB · .xlsx 7.3 KB · .pdf 5.0 KB · Kostenvoranschlag_Schweiz.docx 39 KB · .pdf 5.6 KB · Devis_estimatif_Suisse.docx 39 KB · .pdf 5.6 KB (FR KVA, extra).
All contain: Absender + UID/MWST-Nr., Empfänger, Offerten-Nr., Datum, Gültig bis (30 Tage), Positionen table (Beschreibung/Menge/Einheit/Einzelpreis/Total), Zwischentotal, MWST 8.1% + non-MWST note (Art. 10 MWSTG), Total CHF, Zahlungsbedingungen, Lieferfrist, Annahme-Unterschriftsfeld, "Annahme → Vertrag" note. Excel: line totals, SUM, ROUND(MWST), Total formulas + dropdown 0/2.6/3.8/8.1%. PDFs render umlauts (Helvetica), A4, verified visually. KVA variants carry an "unverbindlich" clause, Annahmen block, optional Kostendach and a "Freigabe zur Ausführung" field instead of a binding acceptance.

## Edited
- `content/{de,fr,en,es,it,pt,sr}/kostenvoranschlag-schweiz.md`: cross-link paragraph repointed to `/offerte-vorlage-schweiz` (DE/FR rewritten to explain Offerte = binding, OR Art. 3 ff.; other locales keep their sentence, URL swapped), "Weiterführend" link repointed, download block (`hero-basic{.bg-cream}` + `hero-cta-links`) inserted before the FAQ with Word/PDF + "Offerte Vorlage" button (EN/ES/IT/PT/SR link the DE files, labelled as German), and the self-linking final-CTA button (`/kostenvoranschlag-schweiz` → `/quotes`). Page stays Sie-form (not rewritten).
- Inbound links (one sentence each, bare URLs): `content/de/quotes.md`, `content/fr/quotes.md` (bexio/banana hero subtitle), `content/de/rechnung-schreiben-schweiz.md` (Fazit), `content/fr/rechnung-schreiben-schweiz.md` (Récapitulatif bullet), `content/de/auftragsbestaetigung-schweiz.md` (Pflicht section; also fixed its self-linking final-CTA button → `/quotes`).
- Inline links repointed `/blog/offerte-schreiben-schweiz` → `/offerte-vorlage-schweiz` in `content/{de,en,es,fr,it,pt}/blog/scheinselbststaendigkeit-schweiz.md` and `content/{de,en}/blog/deckungsbeitrag-berechnen.md`. `grep` for both old slugs in `content/` returns 0.

## Deleted (git rm, staged)
`content/{de,en,es,fr,it,pt}/blog/offerte-schreiben-schweiz.md` and `.../offerten-vorlage-schweiz.md` (12 files). Ported: Gültigkeit rules, Offerte/Kostenvoranschlag/Angebot distinction, Stundensatz-vs-Pauschale + Klauseln, Offerte→Akonto→Schlussrechnung workflow, the copy-paste template (now a filled example + real downloads), FAQ. Not ported: the 10-tool listicle (competitor promotion) and the Sarah/Lena anecdotes.

## Redirects → `SP/redirects-A.txt`
`/blog/offerte-schreiben-schweiz` and `/blog/offerten-vorlage-schweiz` → `/offerte-vorlage-schweiz`, `locales: true`.

## For other packages
- `content/*/rechnungsvorlage.md` (not edited): suggested sentence for the Fazit — DE: "Geht der Rechnung eine Offerte voraus, findest du die passende [Offerte Vorlage Schweiz](/offerte-vorlage-schweiz) mit Gültigkeit, MWST-Zeile und Annahmefeld ebenfalls gratis." FR: "Un devis précède la facture ? Le [modèle de devis suisse](/offerte-vorlage-schweiz) gratuit est ici."
- `/vorlagen` hub: please list Offerte_Vorlage_Schweiz.{docx,xlsx,pdf}, Devis_Modele_Suisse.{docx,xlsx,pdf}, Kostenvoranschlag_Schweiz.{docx,pdf}, Devis_estimatif_Suisse.{docx,pdf}.

## Notes / uncertainties
- `content/de/auftragsbestaetigung-schweiz.md` has an opener/closer fence count mismatch (18/17) that is **pre-existing in HEAD**; my diff there is 2 lines. Not fixed (outside scope) — worth a look.
- Legal citations limited to what I am confident about: OR Art. 3 (Antrag mit Frist), Art. 5 (ohne Frist, unter Abwesenden), Art. 7 (unverbindlich/freibleibend), Art. 10 MWSTG threshold, MWST rates. The "moderate Abweichungen" tolerance for Kostenvoranschläge is stated as practice, not law (as on the existing KVA page).
- No download links inside markdown bodies (ProseA would prefix `/fr/downloads/...`); all download URLs sit in `hero-cta-links` props, matching rechnungsvorlage.
- Pricing on page: free up to 3 Rechnungen; Pro CHF 25/Mt. jährlich (CHF 299/Jahr) or CHF 39 monatlich. Did not claim quotes are in the free plan (features.md is ambiguous).
- The "Installateur aus St. Gallen" example is an illustrative scenario carried over from the deleted blog post, not a named customer.

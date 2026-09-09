# report-keepers-3 — 4 German keeper posts (2026-09-09)

Edited (DE only, nothing committed, no other locale touched):
content/de/blog/{wann-verjahrt-eine-rechnung-schweiz, zahlungsfristen-schweiz, verrechnungssteuer-schweiz, e-rechnung-schweiz}.md

All four: full du-form (grep-verified: only third-person "sie/ihre" remain), `::feature-grid`
`id: key-takeaways` (5 bullets) after the intro, Swiss formatting (MWST, 8.1/3.8/2.6%, CHF 1'250.00,
decimal points, no ß), title ≤60 / description ≤160. **Validator: all 4 PASS.**
All 16 internal links resolve to existing content/de files. No redirects, no downloads.

## wann-verjahrt-eine-rechnung-schweiz
- Fixed: 10-year rule cited as **Art. 130 OR** → **Art. 127 OR** (130 now only for Fälligkeit).
  Table "Spezialfrist" → **Art. 128 Ziff. 3 OR**; Verlustschein → **Art. 149a SchKG**.
- Fixed: page implied a Mahnung secures the claim. A Mahnung does not interrupt Verjährung —
  section rewritten around Art. 135 OR (Anerkennung, Betreibung, Klage).
- Money links added (was zero): `/mahnung-vorlage-schweiz` ×2, `/rechnungsprogramm` ×2,
  `/rechnung-schreiben-schweiz` ×2. Absolute `magicheidi.ch/en/blog/betreibung-schweiz` (deleted slug,
  wrong locale) → `/mahnwesen-schweiz`.
- Removed: spam link to minijob-ratgeber.de + its paragraph; broken konsumentenschutz.ch URL → fedlex OR.
- Softened: cases labelled as constructed examples; "Stand: September 2026"; note that 127-vs-128 is
  an Auslegungsfrage in the individual case.

## zahlungsfristen-schweiz
- Fixed (main): the page asserted a *statutory* 30-day term under Art. 102 OR with automatic Verzug.
  Swiss law has no general statutory payment period — Art. 75 OR (sofort fällig), Verzug via Mahnung
  (102 I) or automatically with an agreed Verfalltag (102 II). "30 Tage netto" now framed as Usanz.
- Fixed: Pflichtangaben cited "OR Art. 469" (= Anweisung) → **Art. 26 MWSTG**.
- Fixed: "Verjährung nach Art. 127 OR nach fünf Jahren" → 10 (127) / 5 (128).
- Fixed: QR-Rechnung "seit 2020, ESTV-Spezifikation" → only valid Zahlteil since 1.10.2022, specs by **SIX**.
- Fixed: broken fedlex ELI 27/322_322_322 → verified 27/317_321_377.
- Softened: "Betreibung kostet CHF 30–50" (GebV SchKG is a scale) → "richtet sich nach der Forderungshöhe";
  the CHF 800 lawyer fee and CHF 18'000 liquidity figures genericised.
- Links: `/blog/verzugszins-schweiz` → `/blog/mahngebuehren-schweiz`; `/blog/betreibung-schweiz` →
  `/mahnwesen-schweiz`; added `/mahnung-vorlage-schweiz`, `/mwst-freelancer`, `/qr-rechnung-erstellen`,
  `/blog/wann-verjahrt-eine-rechnung-schweiz`. FAQ block given proper label/title/items.

## verrechnungssteuer-schweiz
- Fixed (main): the article framed **Formular 25** as the form for reclaiming *foreign* withholding tax.
  Form 25 is the Verrechnungssteuer refund for **juristische Personen with seat in CH**; foreign
  withholding tax goes via **Formular DA-1** (Beilage zum Wertschriftenverzeichnis, ~CHF 100 minimum,
  3-year deadline). Both verified; corrected in body, lists, fazit and FAQ.
- Fixed: natural persons reclaim via the Wertschriftenverzeichnis of the ordinary return; and the full
  35% is credited while the income is taxed ordinarily (page implied only the difference is refunded).
- Softened: "verliert das Geld endgültig" → Art. 23 VStG Verwirkung with the 2019 revision caveat;
  added 3-year deadline (Art. 32 VStG).
- Softened: Teilbesteuerung "Zürich 60%" was unsourced → 70% federal (≥10% Beteiligung), cantons
  typically 50–70%. The Zurich worked example (CHF 11'500 back) removed.
- Fixed: 404 ESTV link → two live ESTV pages; dead blog links → `/tax-return-2024` and
  `/tools/vat-calculator-switzerland`. "1,5%" → "1.5%".

## e-rechnung-schweiz
- Structural bugs fixed: `::feature-image` was missing its closing `---`; the FAQ used `questions:`
  while `PagesLandingFaq` requires `label`/`title`/`items` (would have rendered empty).
- Broken image: hero referenced `e-rechnung-schweiz.de.webp`, which does not exist in
  public/images/visuals → switched to `invoice-list.{locale}.webp`. **The 5 other locales of this post
  still point at the missing file** (not my package).
- Removed false product claims (vs context/features.md): Magic Heidi has no ZUGFeRD export and no eBill
  integration, yet the page sold both ("ZUGFeRD ab CHF 25.00", "eBill-Anbindung in einem Arbeitsablauf").
  Rewritten to QR-Rechnung / PDF-Versand / Mahnungen / MWST; ZUGFeRD now points to third-party tools.
- Fixed: "Art. 26 MWSTV" → **Art. 26 MWSTG** (5×). The Echtheit/Integrität claim attributed to
  "Art. 26 Abs. 2 MWSTV" softened to GeBüV + ESTV practice (could not source it to that article).
- Fixed: bexio "CHF 52.00/Mt." (unsourced) → "ab CHF 35.00 im Jahresabo" + link `/bexio-preise`.
- Softened: invented eBill persona metrics (34→11 Tage) and the "CHF 5'000.00 Nachforderung" claim →
  qualitative + Ermessenseinschätzung. `/invoicing` → `/rechnungsprogramm`;
  `/blog/rechnungsversand-per-email` (deleted) → `/rechnung-schreiben-schweiz`; `/qr-rechnung-erstellen` kept.

## Notes
- Re-check before commit that these survive other packages: `/blog/mahngebuehren-schweiz`,
  `/blog/qr-code-rechnung-bezahlen`, `/blog/guide-complet-toutes-les-deductions-pour-independant-a-ne-pas-oublier`.
- FR/EN/IT/ES/PT copies of all four posts still carry the old legal errors, the Formular-25 mistake and
  (e-rechnung) the broken image + `questions:` FAQ key.

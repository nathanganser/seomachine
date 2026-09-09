# Report — Package E (MWST pages), 2026-09-09

## Edited
- `content/de/mwst-registrierung.md` — full rewrite, du-form. Title "MWST-Anmeldung Schweiz 2026: Registrierung in 5 Schritten" (57), H1 "MWST anmelden Schweiz 2026: Registrierung Schritt für Schritt". Answer-first intro, "Das Wichtigste in Kürze" feature-grid, 5-step grid + detailed steps, MWST-Nummer section, Fiskalvertreter, Vorsteuer, 30-day post-registration checklist, in-page table of the 8 cantonal satellites, 14-item FAQ (merged PAA questions from the blog post: ab wann / wie / Unterlagen / Dauer / Auslandumsatz / Methode / Frist verpasst / abmelden / Bezugsteuer). Links out to pillar `/mwst-schweiz`, `/online-vat-statement`, `/net-vat-accounting-method`, `/mwst-nummer-schweiz`, `/uid-nummer-*`, `/blog/bezugsteuer-schweiz`, `/blog/mwst-abmelden-schweiz`.
- `content/{fr,it,en}/mwst-registrierung.md` — same 15-fence structure, translated (FR vous, IT tu, EN plain). Locale-aware links: FR gets no pillar/mwst-nummer/uid-pruefen/abmelden links (pages don't exist in fr); IT/EN link the pillar. es/pt/sr untouched (old structure, titles already fine).
- `content/de/mwst-registrierung/*.md` (8 satellites) — link-only: first parent link now anchored `[MWST Anmeldung Schweiz: der komplette Ablauf](/mwst-registrierung)` (coordinator note re st-gallen outranking parent). The second parent link in each file is unchanged.
- `content/de/online-vat-statement.md` — title "MWST-Abrechnung online einreichen 2026: Schritt für Schritt" (59), H1 adds "MWST abrechnen"; answer-first intro + pillar link; new "MWST-Abrechnung ausfüllen: die wichtigsten Ziffern" (200/220–280/302/312/342/400/405/500/510, Saldosteuersatz 322/332, Marco example — ported from blog); method section renamed "MWST abrechnen: Effektiv vs. Saldosteuersatz" with 4-row table (quarterly 60d / semi-annual 60d — matches existing page + pillar) and link to `/net-vat-accounting-method`; 4 FAQ items ported (Papier? / was brauche ich / Dauer / Formulare); "MWST-Abrechnung Easy" tense → discontinued May 2026; annual-filing deadline de-dated ("Ende Februar des betreffenden Jahres"). Sie-form kept (whole page is Sie; converting 620 lines was out of scope — flag if you want du).
- `content/{fr,it,en}/online-vat-statement.md` — same title/H1/description, Ziffern block, method table, FAQ additions, annual-deadline wording. Easy-tense fix NOT mirrored (not touched there).
- Pillar inbound links: `/mwst-schweiz` now linked from DE registrierung, DE online-vat-statement (new), DE freelancer/mwst-nummer/uid-nummer (already had), EN uid-nummer-schweiz (new), EN + IT online-vat-statement (new), EN/IT registrierung (rewrite). FR: pillar doesn't exist. Pillar outlinks: all 5 required targets were already present in de/it/en — pillar not edited.

## Deleted (git rm, staged) — 18 files
`content/{de,en,es,fr,it,pt}/blog/{mwst-anmelden-schweiz,mwst-online-einreichen,mehrwertsteuer-online-abrechnen}.md`.
`mwst-online-einreichen-schweiz` never existed as a file — it is a vercel.json redirect to `/blog/mwst-online-einreichen` (lines 129–138), which now chains. Recommend repointing those two vercel.json entries to `/online-vat-statement` (not my file).

## Redirects → `SP/redirects-E.txt` (4 lines, locales: true)
mwst-anmelden-schweiz → /mwst-registrierung; mwst-online-einreichen, mehrwertsteuer-online-abrechnen, mwst-online-einreichen-schweiz → /online-vat-statement. Note `config/redirects.ts:300` already has the non-blog `/mwst-online-einreichen → /online-vat-statement`.

## Inline links repointed — 49 files (list in `SP/repointed-E.txt`)
All `…/blog/{three slugs}` links (bare + absolute magicheidi.ch(/en) forms) → new targets. Files are other packages' blog posts (saldosteuersatz-formular, unterstellungserklarung, effektive-methode, vorsteuerabzug, mwst-pflicht, mwst-abmelden, bezugsteuer, jahresabschluss, selbstaendige-erwerbstaetigkeit ×6 locales) — link-only sed edits; if another agent git-rm's any of them the edit is moot.

## Sanity
Fences balanced, YAML valid, top-level fence sequence identical across de/fr/it/en for both pages (15 / 24). Titles ≤60, descriptions ≤160 in all 8 files. No ß / MwSt. Satellite YAML "errors" flagged by my checker on genf/tessin are false positives (markdown `---` rules in body; diff is one line each).

## Not done / unsure
- es/pt/sr registrierung + vat-statement not mirrored (old structure; "only if trivial" — it wasn't).
- Facts stated only from existing pages/pillar: 3–4 weeks processing, CHF 1'500–3'000 Fiskalvertreter, Bezugsteuer CHF 10'000 (from the deleted blog; matches Art. 45 MWSTG), "Easy discontinued May 2026" (page's own prior claim, tense updated — verify).
- Coordinator note: st-gallen ranks under legacy `/de/` URL — that's a redirect/canonical matter outside content files.

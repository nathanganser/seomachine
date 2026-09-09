# Package D report — QR-Rechnung consolidation (2026-09-09)

## Keep/delete decisions (8 slugs)
| Post | Decision | Why |
|---|---|---|
| neue-qr-rechnung-schweiz | DELETE → /qr-rechnung-erstellen (de/en/fr/it/es/pt) | Generic "what is a QR bill" explainer; ~90% overlap with landing page. Ported: QR-IID range 30000–31999, v2.3 date, "SIX updates each November". |
| qr-rechnung-schweiz-beispiel | DELETE → landing | Only distinct asset was the annotated Musterrechnung → ported as new H2 "QR-Rechnung Beispiel" (table + "so liest du den Zahlteil"). |
| qr-rechnung-schweiz-pflicht | DELETE → landing | Post overclaimed "Pflicht"; nuanced answer now an H2 "Ist die QR-Rechnung Pflicht?" (+ eBill distinction, 3-sentence Umstellung timeline). |
| qr-rechnung-validieren (de/en only) | DELETE → landing | No validator tool of our own; SIX portal + scan test now an H2 "QR-Rechnung prüfen, bevor du sie verschickst". Dropped the schumms.com outbound link. |
| umstellung-qr-rechnung-schweiz | DELETE → landing | Migration is 4 years done; content = Aufbau/QR-IBAN/Fehler duplicates. History folded into the Pflicht section. |
| qr-code-rechnung-bezahlen | KEEP (all 6 locales) | Payer-side intent ("how do I pay"), different audience; landing FAQ "Wie bezahlt mein Kunde" links to it. DE: removed unsourced "600'000 Firmen" line, repointed 2 links to deleted posts → landing. Other locales: links repointed only. |
| rechnung-mit-qr-code-erstellen | already gone (merged July) but NO redirect existed → likely live 404 | Redirect recorded. |
| qr-rechnung-erstellen-schweiz | already gone; redirect exists (redirects.ts:334, `locales: [...]` includes bare) | Nothing to do. |

## Files edited
- `content/de/qr-rechnung-erstellen.md` — restructured: answer-first intro; Tool-1/Tool-2 stories cut; new H2s "Einzahlungsschein erstellen? …" (reciprocal), "Pflichtfelder", "QR-Rechnung Beispiel", "Ist die QR-Rechnung Pflicht?", "QR-Rechnung prüfen"; steps grid 7→5; FAQ 16→12 tighter PAA-style items (new: eBill, prüfen). Links: /einzahlungsschein-erstellen, /rechnungsvorlage, /rechnung-schreiben-schweiz, /qr-iban-example, /tools/add-qr-code-to-invoice (exists), /pricing, /banks/ubs, /blog/qr-code-rechnung-bezahlen. ~3,080 rendered words (old page 3,114) — see caveat.
- `content/en|fr|it/qr-rechnung-erstellen.md` — full mirrors of the new DE structure (27 top-level fences each, identical component order). FR converted from *tu* to **vous** throughout. FR/IT stale "dès CHF 9" pricing → Pro CHF 25/mois, CHF 299/an, CHF 39.
- `content/de/einzahlungsschein-erstellen.md` — retitled "Einzahlungsschein erstellen: was seit ESR und ES gilt" (53 chars); hero title now "Einzahlungsschein erstellen: …"; new top answer box "Einzahlungsschein vs. QR-Rechnung" → /qr-rechnung-erstellen; new H2 "Einzahlungsschein erstellen: so geht es heute"; bullet stating no blank template exists. No downloads (per brief).
- `content/*/blog/qr-code-rechnung-bezahlen.md` (6) — see table.
- Other-package files, one-line link repoints only (redirect covers them anyway; flagging per brief): `content/*/blog/rechnungsstellung-schweiz.md` (6) and `content/*/blog/e-rechnung-schweiz.md` (6): `…/qr-rechnung-schweiz-pflicht` → `/qr-rechnung-erstellen`.
- ES/PT/SR landing pages untouched; parse OK (26/26 fences).

## Files deleted (git rm, staged)
neue-qr-rechnung-schweiz ×6, qr-rechnung-schweiz-beispiel ×6, qr-rechnung-schweiz-pflicht ×6, umstellung-qr-rechnung-schweiz ×6, qr-rechnung-validieren ×2 (de, en) = 26 files. Grep for the 5 slugs in `content/` is clean.

## Redirects → SP/redirects-D.txt (6 lines)
5 deleted slugs (validieren with `locales: ['en']`) + `/blog/rechnung-mit-qr-code-erstellen`, all → `/qr-rechnung-erstellen`.

## Sanity
Fences/YAML validated (PyYAML) on every file I touched; DE/EN/FR/IT = 27/27 top-level. Titles ≤60, descriptions ≤160. No MwSt./ß. `e-rechnung-schweiz.md` trips my YAML checker but identically at HEAD — pre-existing, not from my edit.

## Could not / caveats
- DE landing page rendered ~3,080 words, not ≤2,800: it now carries the ported Beispiel/Pflicht/Prüfen sections + FAQ schema; I cut ~1,000 words elsewhere. Going lower means dropping the comparison table or the Pflichtangaben grid — recommend leaving as is.
- `price: 9` in the software-schema of all locales predates me and contradicts CHF 25 — left untouched (schema semantics unclear).
- Facts not 100% verified: SIX validation portal URL `validation.iso-payments.ch` (linked in DE/EN/FR/IT); "SIX updates the standard each November"; v2.3 = 21.11.2025 is from the existing page (deleted posts said 22.11 and announced v2.4 for Nov 2026 — deliberately not stated). Example IBAN CH93 0076 2011 6238 5295 7 is the standard SIX sample.
- Did not touch `config/redirects.ts` per brief.

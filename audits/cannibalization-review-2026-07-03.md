# Keyword Cannibalization Review — 2026-07-03

Scope: all 391 content slugs in mh-landing, all 6 locales. Data: GSC query+page (28d and 90d windows), content inventory, file-level review by topic family.
Outcome: PR https://github.com/nathanganser/mh-landing/pull/115 (branch `seo/cannibalization-cleanup`).

## Key findings

1. **Feiertage vs public-holidays URL duplication (the biggest 90d signal) was already fixed** — 301s added May 6 have fully consolidated; old URLs get 0 impressions in the last 14 days. No action needed.
2. **Confirmed active cannibalization resolved in the PR:**
   - `milchbueechli-app` vs `milchbuechleinrechnung` (split "einfache buchhaltung schweiz") → merged
   - 3-way "bookkeeping switzerland" split (`buchhaltungssoftware` / `buchungsjournal-schweiz` / long-slug page) → long-slug deleted
   - Two competing listicles (`ranking-simplest-rechnungssoftware-2026` vs `top-5-buchhaltungssoftware-schweiz`) → merged, click-count study ported
   - Duplicate ESTV filing guides (`mwst-online-einreichen` vs `online-vat-statement`) → merged
   - `solo-sarl` vs `solo-gmbh`, `ouvrir-son-entreprise-en-suisse` vs `entrepreneuriat`, 3 bank-account pages → consolidated
3. **Structural fixes:** es/pt `vat-for-swiss-freelancers` moved to fill the missing `mwst-freelancer` locales (fixes ~85 dangling internal links); `pt/numero-fatura-suica` and the dated `geschaeftskonto-vergleich-schweiz-2026-05-12` slugs normalized; EN `entrepreneuriat` was untranslated French — replaced.
4. **Deliberately kept:** `vipassana-switzerland` (top-clicking page), `kostenlose-rechnungssoftware-schweiz` + `bexio-alternativen` (published 2026-07-02, too new to judge), currency trackers (distinct intents), per-language glossary twins (debtors/creditors — different SERPs, no overlap).

## Follow-ups (not in the PR)

- [ ] Title/meta differentiation: `societe-individuelle-suisse` DE/EN (collides with einzelfirma pillar), `swiss-llc-deep-dive` DE/FR (verbatim GmbH-formation titles duplicating `gmbh-gruenden-schweiz`), `accounting-document` DE (collides with `buchungsbeleg-schweiz`), `mwst-registrierung` (cut rates table + filing section; own "MWST anmelden" only), IT titles of `net-vat-accounting-method`/`mwst-registrierung` (de-genericize "IVA Svizzera 2026" — `mwst-freelancer` owns it)
- [ ] `vat-rates-2025` → re-slug to `/vat-rates` + 301 + refresh stale referendum claims ("expected September 2025")
- [ ] `coworking-spaces` → convert to national cluster hub; its 10 city links point at legacy `/coworking-coffee-*` redirect URLs
- [ ] `vat-method` (fr/it/es/pt) duplicates `net-vat-accounting-method` intent — review + consolidate
- [ ] Orphan interlinking: VAT satellites (`net-vat-accounting-method`, `online-vat-statement`, `swiss-vat-reconciliation-guide`, `vat-rates`) and the debtors/creditors glossary have 0 inbound content links; `swiss-expense-report-template` also orphaned
- [ ] `swiss-franc` ↔ `euro-conversion`: de-dupe shared forecast/SNB/2015-shock blocks, add reciprocal links (none exist)
- [ ] `online-geld-verdienen-schweiz`: add link to `/dropshipping` (currently rides its query with no link)
- [ ] Watch `fr/blog/comment-sinscrire-au-registre-du-commerce` (803 impr) vs `commerce-register-switzerland-2026` for future splitting
- [ ] `de/einfache-buchhaltung-schweiz.md.bak-2026-05-13` backup file can be removed; consider retargeting its redirect from `/buchhaltungssoftware` to `/milchbuechleinrechnung` (better intent match)

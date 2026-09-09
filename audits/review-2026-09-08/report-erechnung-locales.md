# e-rechnung-schweiz — locale port (EN/FR/IT/ES/PT)

Ported the corrected German article (`content/de/blog/e-rechnung-schweiz.md`) into all five
locale copies. Each file was rewritten to mirror the German block structure exactly
(feature-image → blog → markdown intro → feature-grid key-takeaways → markdown body → FAQ),
translated naturally rather than word-for-word. No other files touched. Nothing committed.

## Applied to every one of the 5 files

1. **FALSE PRODUCT CLAIMS REMOVED.** Deleted every sentence claiming Magic Heidi produces,
   exports or connects to ZUGFeRD / XRechnung / eBill. Specifically: the "software covering all
   formats" bullet ("Magic Heidi offers PDF, QR-Rechnung and ZUGFeRD"), the comparison-section
   claim ("ZUGFeRD export for German clients and eBill integration in a single workflow"), the
   FAQ cost answer ("ZUGFeRD exports are free … Magic Heidi offers this from CHF 25"), the
   conclusion CTA ("bill your next German project in ZUGFeRD format"), the to-do "activate the
   ZUGFeRD export", and the persona who "exported ZUGFeRD from his existing software".
   Replaced with the German file's line: use a specialised portal/conversion tool, or agree with
   the German client that they enter it manually. ZUGFeRD/XRechnung/eBill are still *explained*
   as formats. Magic Heidi is now described only as: Swiss QR-Rechnung PDFs, email sending,
   receipts, MWST rates, overdue reminders.
2. **Stale bexio pricing removed.** "bexio CHF 52.00/month" (and translations) deleted in both
   the body and the FAQ; replaced with "starts at CHF 35.00/month on an annual plan" plus a link
   to `/bexio-preise`. Magic Heidi stated as CHF 25.00–39.00/month, matching the German file.
3. **Invented persona metrics removed.** Deleted the named personas Miriam Frey, Lukas Meier and
   Sandra Vogt, and every fabricated figure: the physiotherapist's 80 invoices/month, 34→11 day
   payment time, halved reminders, CHF 140 average invoice; Lukas's CHF 29/month portal and
   12-day payment; the "CHF 5'000 back payments" and "CHF 1'000 over three years" numbers; the
   "50 invoices per month" basis. Now generic: "a constructed but typical example: a business
   coach in Bern", "a Zurich web designer".
4. **FAQ fixed.** `questions:` → `items:` in all five files (the FAQ was rendering EMPTY), plus
   `label: FAQ` and a localised `title:` to match the German entry shape. Verified: `grep
   "questions:"` now returns nothing in any locale.
5. **Hero image fixed.** `e-rechnung-schweiz.<locale>.webp` does not exist anywhere under
   `public/images/` (confirmed by grep — no file, no other reference). Replaced with
   `invoice-list.{locale}.webp`, the same asset the German file now uses; the assets exist as
   `public/images/visuals/invoice-list.{de,en,fr,it}.webp` and `app/utils/index.ts`
   `resolveLocalePath()` falls es/pt back to the `.en.` variant, so all five resolve. The
   missing closing `---` of the `::feature-image` YAML block was added in all five.
6. **Swiss formatting.** VAT rates now 8.1% / 3.8% / 2.6% (previously only "8.1% for most
   services"); amounts as `CHF 4'800.00` (EN/ES/PT had `CHF 4,800.00`); no ß anywhere.
   Legal refs corrected MWSTV → MWSTG / LTVA / LIVA per locale, admin.ch → fedlex.admin.ch,
   and "Stand: September 2026" style date added.

## Per-file notes
- **EN** — plain address form. Also fixed a bogus link label ("experience with sending invoices
  by email" pointing at `/rechnung-schreiben-schweiz`) and a duplicated `/qr-rechnung-erstellen`
  link that appeared twice in one paragraph with two different labels.
- **FR** — **vous** throughout. Same duplicated `/qr-rechnung-erstellen` link fixed. Description
  had to be trimmed to 154 chars to pass the 160-char check.
- **IT** — converted from the previous inconsistent mix of *Lei* and *voi* to **tu** throughout,
  per the brief.
- **ES** — kept **usted** (the form the file already used).
- **PT** — kept **você**. This file also had genuinely broken nesting (a stray `::` after the
  `::blog` frontmatter and another before `::pages-landing-faq`, with the `::markdown` body
  unindented); the rewrite fixes it.

## Validation
`validate_mdc.py` on all five: **`1 files checked, 0 failed`** each — no warnings at all, not
even the "unclosed openers at line 17" one, because the German structure closes `::blog`
properly (before this change EN/FR/IT/ES all failed on it; the German reference file also
passes clean).

Grep confirmations: no `questions:` key, no `52.00` / `CHF 29` / `0.40`, no persona names or
invented metrics, no sentence containing both "Magic Heidi" and ZUGFeRD/eBill/XRechnung, no
ZUGFeRD-export or eBill-integration phrasing in any language, no ß, no reference to the
nonexistent hero image. Internal link targets (`/rechnung-schreiben-schweiz`,
`/qr-rechnung-erstellen`, `/rechnungsvorlage`, `/mwst-freelancer`,
`/blog/qr-code-rechnung-bezahlen`, `/rechnungsprogramm`, `/bexio-preise`, `/pricing`) verified
to exist in all six locales; all written bare per site convention.

## Uncertain / flagged
- The German file links `fedlex.admin.ch/eli/cc/27/317_321_377/de`. I pointed FR at `/fr` and IT
  at `/it` on that same ELI; EN, ES and PT keep `/de` since fedlex has no page in those
  languages. Worth a spot-check that the FR/IT ELI paths resolve.
- No redirects needed; no downloads generated; `config/redirects.ts` untouched.

---
Page type: Referral landing page
Source Vue file: /Users/nathanganser/Documents/Development/mh-landing/app/pages/i/[id].vue
URL pattern: /i/[referrerId]
Locales to translate into: de, fr, it, es, pt (en is source)
Date: 2026-05-18
Primary goal: Convert referral visitors into Magic Heidi signups
Notes: {Name} is interpolated at runtime from the referrer's profile (API fetch). Keep the placeholder unchanged in copy. This is conversion copy, not a blog article — no TL;DR block, no mini-stories, no 2000-word minimum.
---

# Referral landing page — full markdown copy

> Visual flow indicator (top of page): personalised badge with the referrer's avatar/logo and name. Pulls from `https://api.magicheidi.ch/referral/{id}`.

## Hero

**Badge (above the headline):**

Recommended by **{Name}**

---

**H1:**

{Name} doesn't recommend many tools. Magic Heidi is one of them.

**Subhead:**

Swiss QR invoices in under a minute. Receipts scanned by AI. MWST and tax-prep handled. Built for Swiss freelancers and small businesses, by Swiss freelancers.

**Primary CTA button:**

Start free with {Name}'s invite

**Secondary CTA button:**

Watch a 90-second demo →

**Trust badge row (4 chips):**

- 🇨🇭 Swiss-made software
- 🔒 Hosted in Zurich
- 🛡️ GDPR-compliant
- ⭐ 4.9★ on Google

**Visual below the CTAs (keep existing):**

Sample Swiss QR invoice with {Name}'s business name and logo on it. Shows the visitor exactly what their first invoice will look like.

---

## Section 2 — A small thank-you for showing up through {Name}

> Why this section: visitors arrive with a friend's recommendation. Giving them something concrete to claim turns the soft signal of a referral into a real reason to sign up today.

When someone like {Name} sends you to us, we want your first steps with Magic Heidi to feel personal. So you get a free 20-minute onboarding call with the Magic Heidi team and our Swiss invoice template starter pack, on top of the free plan.

Nathan and the team will help you set up your first invoice, import your client list, or move over from bexio, KLARA, or Excel.

> Implementation note: this section is gated behind a `hasReferralRewards` config flag. If the onboarding-call program isn't live yet, swap for the softer copy below.
>
> **Softer fallback (if no reward program is live):**
> {Name}'s recommendation is the highest signal we have. So when you sign up through this page, the Magic Heidi team will personally check in after your first invoice. We read every message at hello@magicheidi.ch — or call Nathan directly on +41 78 300 24 77.

---

## Section 3 — Why Swiss freelancers like {Name} choose Magic Heidi

### You'll send your first invoice today

Most freelancers create and send their first Swiss QR invoice within five minutes of signing up. Add your business details once, add a client, hit send. No setup wizard. No template hunting.

### Built for the rules you actually face

Swiss QR-IBAN, MWST thresholds, AHV-friendly bookkeeping. We acknowledge canton differences where they matter and avoid pretending every Kanton handles things the same way. No advice copy-pasted from another country.

### Receipts disappear into the app

Photograph a receipt at the till. Magic Heidi reads the amount, the MWST, and the date, and files it under the right category. Year-end tax prep stops being a December project.

---

## Section 4 — Everything you need, nothing you don't

**Section label:** Everything you need, nothing you don't
**Section title:** One Swiss app for invoicing, expenses, MWST, and tax prep
**Section subtitle:** From your first invoice to your year-end MWST return, Magic Heidi handles the admin so you can focus on paid work.

### 🧾 Swiss QR Invoices

Compliant Swiss QR-IBAN invoices in under a minute. Send by email, get paid faster.

→ Links to `/rechnungsprogramm`

### 📸 AI Expense Scanning

Photograph any receipt. The amount, MWST, and date are filed automatically.

→ Links to `/ai-expenses-scanning`

### 📊 Accounting Made Simple

Simplified bookkeeping that fits how Swiss freelancers actually work. No double-entry headaches.

→ Links to `/buchhaltungssoftware`

### 🏦 Bank Import

Import your bank statement or connect your bank. Match invoices to payments in clicks, no spreadsheet cross-referencing.

→ Links to `/bank-statement-import`

### 🇨🇭 MWST Management

Swiss MWST rates built in. Both Effective Method and Saldosteuersatz supported. Generate the report, copy the numbers into the ESTV portal, done.

→ Links to `/mwst-freelancer`

### 📝 Offers & Quotes

Send a quote, the client accepts, one click converts it to a Swiss QR invoice. No re-typing.

→ Links to `/de/kostenvoranschlag-schweiz` (German only; flag for other locales)

---

## Section 5 — Your first 5 minutes with Magic Heidi

> Why this section: the silent question on every signup page is "what happens after I click?" Answering it directly removes the biggest friction point.

### 1. Add your business details once

Name, address, IBAN, language. Magic Heidi remembers everything for the next invoice.

### 2. Create your first invoice

Add the client, the line item, hit send. The Swiss QR payment slip is generated automatically and your client can pay it with one scan of their banking app.

### 3. Scan an expense

Open the mobile app, photograph a receipt. It's filed, tagged, and ready for your year-end tax return.

---

## Section 6 — A note from Nathan

Hi, I'm Nathan, one of the freelancers who built Magic Heidi.

I started this because the existing Swiss tools either ignored the canton-by-canton mess or charged bexio prices for invoices a sole proprietor could write by hand. We use Magic Heidi for our own businesses — invoices, MWST, expenses, the lot.

If anything on this page is unclear, or you want help porting your data from bexio, KLARA, or an old Excel sheet, email us at **hello@magicheidi.ch** or call me directly on **+41 78 300 24 77**. I read every message and usually reply the same day.

Thanks for trusting {Name}'s recommendation.

— Nathan, Co-founder, Magic Heidi

---

## Section 7 — Frequently asked questions

> Format these in `FAQPage` JSON-LD via `useSchemaOrg` so AI search engines (ChatGPT, Perplexity) and Google rich results can cite the answers.

### Is Magic Heidi really free to start?

Yes. The free plan covers your first three invoices, AI expense scanning, bank import, and MWST tracking. No credit card is required. You only upgrade to Pro when you need unlimited invoices, quotes, expenses, and clients. Pro is CHF 25/month billed annually, or CHF 30 monthly.

### Do I need to be registered for MWST to use Magic Heidi?

No. If you earn under CHF 100,000 a year, you don't need to register for MWST and Magic Heidi works fine without it. If you cross the threshold or already have a MWST number, add it once and Magic Heidi handles the calculations from there. Both the Effective Method and the Saldosteuersatz are supported.

### Can I move my invoices and clients from bexio, KLARA, or Excel?

Yes. Import your client list as a CSV and Magic Heidi takes it from there. For more complex moves from bexio or KLARA, email us at hello@magicheidi.ch or call Nathan on +41 78 300 24 77 — the team will help with the cleanup so you don't lose anything.

### What languages does Magic Heidi support?

The app and invoices work in German, French, Italian, English, Spanish, and Portuguese. You can send each client an invoice in their own language without re-entering any of your business details.

### What happens if I want to leave Magic Heidi later?

Export every invoice, expense, client, and document as PDF and CSV anytime. We also generate a full ZIP archive of your data on request. No lock-in, no export fee, no penalty. Your data is yours.

### Is Magic Heidi suitable for a sole proprietorship (Einzelfirma)?

Yes, that's the main audience. Most users are Swiss sole proprietors, freelancers, and very small businesses under CHF 500,000 in annual revenue. The accounting and MWST flows are tuned for that level of complexity, not for 20-person companies with payroll and warehouses.

---

## Section 8 — Final CTA

**Title:**

Ready to send your first Swiss invoice today?

**Subtitle:**

Thousands of Swiss freelancers and small businesses use Magic Heidi to invoice clients, scan expenses, and stay tax-ready. Free to start through {Name}'s invite, no credit card required.

**Primary CTA button:**

Start free with {Name}'s invite

**Secondary CTA button:**

Book a free onboarding call (20 min)

**App store row (keep all four):**

- 🍎 App Store
- ▶ Google Play
- ⊞ Microsoft Store
- 🌐 Web app

---

## i18n key plan (for porting back to `i18n/locales/*.json`)

### Keys to update (re-translate to match new copy)

| Key | New English value |
|---|---|
| `referral_recommended_by` | Recommended by {name} *(no change)* |
| `referral_hero_title` | {name} doesn't recommend many tools. Magic Heidi is one of them. |
| `referral_hero_subtitle` | Swiss QR invoices in under a minute. Receipts scanned by AI. MWST and tax-prep handled. Built for Swiss freelancers and small businesses, by Swiss freelancers. |
| `referral_get_started_free` | Start free with {name}'s invite |
| `referral_features_label` | Everything you need, nothing you don't |
| `referral_features_title` | One Swiss app for invoicing, expenses, MWST, and tax prep |
| `referral_features_subtitle` | From your first invoice to your year-end MWST return, Magic Heidi handles the admin so you can focus on paid work. |
| `referral_feature_qr_invoices_desc` | Compliant Swiss QR-IBAN invoices in under a minute. Send by email, get paid faster. |
| `referral_feature_ai_expenses_desc` | Photograph any receipt. The amount, MWST, and date are filed automatically. |
| `referral_feature_accounting_desc` | Simplified bookkeeping that fits how Swiss freelancers actually work. No double-entry headaches. |
| `referral_feature_bank_import_desc` | Import your bank statement or connect your bank. Match invoices to payments in clicks. |
| `referral_feature_vat_desc` | Swiss MWST rates built in. Both Effective Method and Saldosteuersatz supported. Generate the report, copy the numbers into the ESTV portal, done. |
| `referral_feature_quotes_desc` | Send a quote, the client accepts, one click converts it to a Swiss QR invoice. |
| `referral_cta_title` | Ready to send your first Swiss invoice today? |
| `referral_cta_subtitle` | Thousands of Swiss freelancers and small businesses use Magic Heidi to invoice clients, scan expenses, and stay tax-ready. Free to start through {name}'s invite, no credit card required. |

### Keys to add (new sections)

**Reciprocity block:**
- `referral_reciprocity_title` — A small thank-you for showing up through {name}
- `referral_reciprocity_body` — When someone like {name} sends you to us, we want your first steps with Magic Heidi to feel personal. So you get a free 20-minute onboarding call with the Magic Heidi team and our Swiss invoice template starter pack, on top of the free plan.
- `referral_reciprocity_secondary` — Nathan and the team will help you set up your first invoice, import your client list, or move over from bexio, KLARA, or Excel.

**Why-cards block:**
- `referral_why_title` — Why Swiss freelancers like {name} choose Magic Heidi
- `referral_why_card1_title` — You'll send your first invoice today
- `referral_why_card1_desc` — Most freelancers create and send their first Swiss QR invoice within five minutes of signing up. No setup wizard, no template hunting.
- `referral_why_card2_title` — Built for the rules you actually face
- `referral_why_card2_desc` — Swiss QR-IBAN, MWST thresholds, AHV-friendly bookkeeping. Canton-aware where it matters. No advice copy-pasted from another country.
- `referral_why_card3_title` — Receipts disappear into the app
- `referral_why_card3_desc` — Photograph a receipt at the till. Magic Heidi reads the amount, MWST, and date. Tax prep stops being a December project.

**First-5-minutes block:**
- `referral_first5_title` — Your first 5 minutes with Magic Heidi
- `referral_first5_step1_title` — Add your business details once
- `referral_first5_step1_desc` — Name, address, IBAN, language. Magic Heidi remembers everything for the next invoice.
- `referral_first5_step2_title` — Create your first invoice
- `referral_first5_step2_desc` — Add the client, the line item, hit send. The Swiss QR payment slip is generated automatically.
- `referral_first5_step3_title` — Scan an expense
- `referral_first5_step3_desc` — Open the mobile app, photograph a receipt. It's filed, tagged, and ready for your tax return.

**Founder note (single multi-line key with `{email}` and `{phone}` interpolation):**
- `referral_founder_note` — Multi-paragraph block as written in Section 6, with `{email}` interpolation for `hello@magicheidi.ch`, `{phone}` for `+41 78 300 24 77`, and `{name}` for the referrer's name.

**FAQ block:**
- `referral_faq_title` — Frequently asked questions
- `referral_faq_q1_question` / `_q1_answer` — through `_q6_question` / `_q6_answer` (six pairs total).

**Updated final CTA:**
- `referral_cta_secondary` — Book a free onboarding call (20 min) *(can reuse `book_free_onboard_call`)*

---

## Implementation checklist (for the Vue + i18n update)

1. Update existing `referral_*` keys with new English values in `i18n/locales/en.json`. Translate to de/fr/it/es/pt — German is the primary market so prioritise that translation. Use existing Magic Heidi MWST/AHV/QR-IBAN terminology in each locale.
2. Add ~30 new `referral_*` keys per the lists above. Same translation order.
3. Add three new `<HeroBasic>` (or equivalent) sections in `[id].vue` between the existing hero and the existing feature section: reciprocity, why-cards, first-5-minutes.
4. Wrap reciprocity block in a `v-if="hasReferralRewards"` config flag with the softer fallback ready behind a `v-else`.
5. Add a founder-note section (plain text block, not a HeroBasic) between FAQ and final CTA.
6. Add an FAQ section with six expandable Q&As. Emit `FAQPage` JSON-LD via `useSchemaOrg({ ... })` so AI search and Google rich results can pick the answers up.
7. Update final CTA copy and primary button text. Keep the four app store buttons unchanged.
8. Add Mixpanel events: `referral_reciprocity_viewed`, `referral_why_viewed`, `referral_first5_viewed`, `referral_faq_expanded` (per question, with `question_id` property), `referral_founder_note_viewed`.
9. Keep all existing `?inviter=` query param logic and `withInviter()` / `withAnonymousId()` calls unchanged. Every new CTA must route through `ctaUrl` so the referrer ID is preserved.
10. Set up an A/B test against the current page, split 50/50 on `referrerId` hash. Measure `signup_started` per `referral_page_viewed`. Run for two weeks minimum, target 1,500+ sessions per arm.

---

## Brand voice checklist

- [x] Professional yet personal — Nathan in section 6, conversational throughout
- [x] Fair, honest, truthful — no exaggerated claims, specific numbers only where verifiable (5 min, CHF 100k threshold, free plan = 3 invoices, CHF 25/30 pricing)
- [x] Action-oriented — every CTA tells the user the next useful action, FAQ answers end with concrete next steps
- [x] Swiss-specific terminology — MWST (not VAT/sales tax), Saldosteuersatz, AHV, Einzelfirma, Kanton, ESTV portal, QR-IBAN
- [x] No corporate fluff — "seamless", "revolutionary", "empower", "unlock" all avoided
- [x] Specific, concrete language — "five minutes", "your first three invoices", "CHF 100,000" instead of vague claims
- [x] Founder-direct support — email visible in section 6, reinforced in FAQ migration answer
- [x] Mention real competitors fairly — bexio, KLARA, Excel named where genuinely relevant (migration), without disparagement

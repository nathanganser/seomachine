# Agent prompt — locale parity after the 2026-09 content cleanup

Paste everything below the line into a fresh agent. It is self-contained.

---

Read the shared brief first and follow every rule in it: `/Users/nathanganser/Documents/Development/seomachine/audits/review-2026-09-08/SHARED-BRIEF.md`. **The working directory is `/Users/nathanganser/Documents/Development/mh-landing-articles`** (a git worktree of the mh-landing repo, on branch `main`). Do NOT commit and do NOT switch branches — the human reviews and commits.

## Background

In September 2026 a large content cleanup ran against an auto-generated blog ("Outrank"). The German pages were corrected; **their translated copies were not**. Those copies are live and some of them state things that are factually wrong or claim product features that do not exist. Your job is to close that gap.

Read `/Users/nathanganser/Documents/Development/seomachine/audits/review-2026-09-08/implementation.md` for the full context before you start.

## Task 1 — port the German corrections into the locale copies (highest priority)

Three kept blog posts were factually corrected in German only. Each has **five stale copies** (`en`, `es`, `fr`, `it`, `pt`) that still carry the original errors:

| Slug | What was wrong, and what German now says |
|---|---|
| `wann-verjahrt-eine-rechnung-schweiz` | The 10-year prescription period was attributed to **Art. 130 OR**. It is **Art. 127 OR**; Art. 130 governs only when the period *starts* (Fälligkeit). The text also implied that sending a Mahnung interrupts prescription — it does not (see Art. 135 OR for what actually does). |
| `zahlungsfristen-schweiz` | Asserted a **statutory 30-day payment term** with automatic default under Art. 102 OR. Swiss law has no general statutory payment period. Correct framing: Art. 75 OR (due immediately absent agreement), Art. 102 I (default needs a Mahnung), Art. 102 II (a fixed date makes default automatic); "30 Tage netto" is custom, not law. Invoice content requirements were cited as "OR Art. 469" — that article covers Anweisung; the right citation is **Art. 26 MWSTG**. |
| `verrechnungssteuer-schweiz` | Framed **Formular 25** as the way to reclaim *foreign* withholding tax. Formular 25 is the refund form for Swiss **legal entities**; foreign withholding tax is reclaimed via **DA-1**. |

For each: read the corrected German file, then bring each locale copy in line. Translate the corrected passages properly into the target language — do not leave German sentences behind and do not machine-translate word for word. Keep each file's existing address form (EN plain, FR vous, IT tu, ES/PT as the file already reads).

While you are in these files, also apply what the German versions got: a "key takeaways" block after the intro if missing, at least one contextual link to a money page (`/rechnungsprogramm`, `/rechnungsvorlage`, `/mahnung-vorlage-schweiz`, `/buchhaltungssoftware`, `/pricing` — write links **bare**, no locale prefix), and Swiss formatting (**MWST** not MwSt., `CHF 1'250.00`, decimal points in percentages, VAT rates 8.1% / 2.6% / 3.8%, no ß).

## Task 2 — sweep the other 25 kept posts for the same class of error

28 blog posts survived the cleanup; the three above are done. The remaining 25 have **130 non-DE locale copies between them**. The German originals were corrected during the cleanup, so for each post **diff the German against its locale copies** and port anything the German fixed. The recurring problems found in the German pass, all likely still present in translation:

- **Stale competitor pricing**: "bexio CHF 52/Monat" appeared in about eight posts. bexio's real plans are CHF 35 / 42 / 69 / 119. Remove the number and link to `/bexio-preise` instead.
- **Invented evidence**: named personas with precise outcomes ("payment time fell from 34 to 11 days", "CHF 920 lost", "42% cheaper than bexio") and hourly-rate tables presented as market data. Reframe as anonymous examples or delete. Never invent a customer.
- **Wrong Swiss facts** seen in the German pass: the QR-Rechnung switchover dated to 2020 (it is **October 2022**); a claim that a QR-Rechnung requires a QR-IBAN (a normal IBAN works); an Einzelfirma name supposedly needing the suffix "Einzelfirma" (it must carry the owner's family name); "Treuhänder" called a protected title (it is not); "SBB tickets are VAT-exempt" (they are not); the accommodation VAT rate given as 3.7% (it is **3.8%**); AHV self-employed rates stated as a precise 10.1%/10.3% (the scale is degressive — say "rund 10%").
- **Product claims**: never state that Magic Heidi does double-entry bookkeeping (`doppelte Buchhaltung`), exports ZUGFeRD, or integrates eBill. It does none of these. Verify any feature claim against `/Users/nathanganser/Documents/Development/seomachine/context/features.md`. Pricing: free plan = 3 invoices + 3 expenses; Pro CHF 25/month billed annually (CHF 299/year) or CHF 39 monthly.

Work in **batches of 4-5 posts** and validate after each batch, so a failure costs little. Prioritise `fr` and `it` (they earn clicks); `en`, `es` and `pt` earn essentially none, so if time is short, do those last and say so.

**Anything you cannot verify, remove rather than rewrite.** These posts were machine-generated and their legal citations proved unreliable; a missing sentence is better than a confident wrong one.

## Task 3 — missing locale mirrors

- `/offerte-vorlage-schweiz` exists only in `de` and `fr`. Create `it` and `en` versions (same slug, translated content). The German file is the source of truth. It links downloads at `/downloads/Offerte_Vorlage_Schweiz.{docx,xlsx,pdf}`; reuse those files for EN/IT rather than generating new ones, and keep the download block's structure identical to the German page.
- `/vorlagen` (the templates hub) exists in `de`, `fr`, `it`, `en` — no action needed, but check its cards still point at pages that exist in that locale, and that any German-only template is presented as such rather than as a dead link.
- `/mwst-registrierung` and `/online-vat-statement` were rebuilt in `de`, `fr`, `it`, `en`. The `es`, `pt` and `sr` copies still carry the **old structure**. Either mirror the new structure into them or, if that is disproportionate, at minimum port the factual corrections (the CHF 100'000 threshold, ESTV ePortal flow, the effektiv vs Saldosteuersatz distinction) and note in your report that the structure still lags.

## Validation (required)

For every file you touch:

```
/Users/nathanganser/Documents/Development/seomachine/venv/bin/python3 \
  /Users/nathanganser/Documents/Development/seomachine/templates/validate_mdc.py <files...>
```

It checks component-fence balance, frontmatter validity, title ≤60 / description ≤160, and forbidden spellings. One known false positive: an "unclosed openers" warning about the `::blog` wrapper is a pre-existing site-wide pattern in blog posts — ignore that specific warning, but nothing else may fail.

Also confirm, before you finish:
- every internal link you write resolves to a real page in that locale or to a redirect in `config/redirects.ts`;
- the top-level fence sequence of a locale copy matches its German original (`grep -cE '^\s*::[a-zA-Z]'` and `'^\s*::\s*$'` should agree);
- `grep -ri "zugferd\|ebill" ` over your edited files shows no sentence claiming Magic Heidi produces or integrates either.

## Report

Write `SP/report-locale-parity.md`: per task, the files changed, the specific factual corrections ported, anything you deleted for being unverifiable, what you left undone and why. Flag any *new* error class you discover in the translations that was not in the German — that would mean the translation step itself introduced it, which the human needs to know.

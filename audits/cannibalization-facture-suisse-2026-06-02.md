# Cannibalization Consolidation Plan — `facture suisse`

**Generated:** 2026-06-02
**Target keyword:** `facture suisse` (FR, Switzerland)
**Goal:** Consolidate duplicate "how to write a Swiss invoice" pages into the canonical guide to lift it from #5 → top 3.

---

## The problem

Five Magic Heidi pages rank for `facture suisse`. The canonical guide ranks #5; two blog posts cover the **exact same intent** and split link equity / send Google mixed signals about which page to rank.

| Live position | URL | Role | Verdict |
|---|---|---|---|
| **5** | `/rechnung-schreiben-schweiz` | How to write a Swiss invoice (canonical, all 6 locales) | **KEEP — consolidation target** |
| 36 | `/rechnungsvorlage` | Invoice template (download intent) | Keep — distinct intent |
| 62 | `/rechnungsprogramm` | Invoicing software (product intent) | Keep — distinct intent |
| **86** | `/blog/invoice-swiss-individual` | "Facturer en tant que particulier en Suisse – Guide complet 2026" | **REDIRECT — direct duplicate** |
| **99** | `/blog/comment-faire-une-facture-suisse` | "Facture suisse conforme en **2025** — guide pratique" | **REDIRECT — stale direct duplicate** |

The canonical page is already strong (~4,300 words, FAQ + `FAQPage` schema, QR-facture / TVA / mandatory fields, template + generator). It does **not** need a content rewrite. The blocker to top-3 is the two duplicates below, not content depth.

---

## Action 1 — Redirect `/blog/invoice-swiss-individual` (highest priority)

**Status:** Live, HTTP 200. Your `internal-links-map.md:56` **already designates** `/invoice-swiss-individual` → `/rechnung-schreiben-schweiz`, but the rule omits the `/blog/` prefix, so the actual blog URL was never caught. The redirect was planned and silently missed.

**Do:**
1. Salvage any unique content (see "Content salvage" below) into the canonical page first.
2. Add a **301** from `/blog/invoice-swiss-individual` → `/rechnung-schreiben-schweiz` **for all 6 locales** (de, fr, it, en, es, pt) with matching locale prefix.
3. Fix the map rule so it covers the `/blog/` path, not just the bare slug.

## Action 2 — Redirect `/blog/comment-faire-une-facture-suisse`

**Status:** Live, HTTP 200. Not in the redirect map. Title still references **2025** — stale and unmanaged.

**Do:**
1. Salvage unique content into the canonical page.
2. Add a **301** → `/rechnung-schreiben-schweiz` for all locales it exists in.
3. **Add it to `internal-links-map.md`** so it's tracked going forward (append to the line-56 cluster or a new row pointing at `/rechnung-schreiben-schweiz`).

---

## Content salvage checklist (do BEFORE redirecting)

Open each blog post and pull anything the canonical guide lacks, so no ranking content is lost in the redirect:

- [ ] Unique examples / case studies (e.g. particulier-specific scenarios in `invoice-swiss-individual`)
- [ ] Any FAQ questions not already in the canonical page's 8-question FAQ
- [ ] Unique long-tail phrasings worth preserving as H2/H3 on the canonical page
- [ ] Internal/external links worth re-homing
- [ ] Images with useful alt text

If a blog post has zero unique value, redirect immediately — no salvage needed.

---

## Internal-link cleanup (after redirects)

- [ ] Find any internal links pointing at the two redirected blog URLs and repoint them directly at `/rechnung-schreiben-schweiz` (avoid relying on the 301 hop).
- [ ] Ensure the canonical page receives internal links from `/rechnungsvorlage` (#36) and `/rechnungsprogramm` (#62) — sibling pages should funnel "how to write" intent to the canonical guide.

---

## Verification (2–4 weeks post-change)

- [ ] `curl -I` both blog URLs → confirm **301** to canonical (all locales).
- [ ] Re-run `python3 research_serp_analysis.py "facture suisse"` and confirm only the canonical page appears in the top 100 (duplicates gone).
- [ ] Track canonical position in GSC for `facture suisse` — target movement from #5 toward top 3.
- [ ] Confirm no new 404s in GSC coverage for the redirected paths.

---

## Note on scope

Source for these pages lives on the **Nuxt site**, not in this repo — the 301s and edits must be made there. This plan is the spec; execution is in the website codebase.

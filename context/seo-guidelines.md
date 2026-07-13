# SEO Guidelines for Magic Heidi Content

This document outlines SEO best practices and requirements for all Magic Heidi content (magicheidi.ch) to maximize organic search visibility in Switzerland. Audience: Swiss freelancers, Einzelfirmen, and solo business owners.

## Market & Language Strategy

- **Target country**: Switzerland only. All keyword research uses DataForSEO with location 2756 (Switzerland). Do not use global volumes.
- **Language split**: German 70% (primary, Swiss High German), French 20%, Italian 5%, English 5%. Spanish/Portuguese exist as translated locales but are not research targets.
- **Swiss High German**: never use "ß" — always "ss" (Strasse, gemäss, Abschluss). Prefer Swiss terms: Offerte (not Angebot), Rechnung stellen, MWST (not USt/MwSt.-DE-style), AHV, Einzelfirma, Treuhänder.
- **French**: Swiss French conventions (septante/huitante acceptable in examples but standard French preferred in prose; TVA, raison individuelle, indépendant).
- **Currency & formats**: CHF with Swiss formatting (CHF 1'250.00), dates DD.MM.YYYY.
- **Site structure**: Nuxt Content on mh-landing. English is the default locale (no URL prefix); de/fr/it/es/pt are prefixed (`/de/...`, `/fr/...`). **Slugs are German-canonical across all locales** (e.g. `/fr/rechnungsprogramm`) — never invent per-language slugs. Check `context/internal-links-map.md` before choosing any slug.

## Content Length Requirements

### Target Word Counts
- **Standard article**: 1,500-3,000 words (target: 2,000-2,500)
- **Pillar content / comprehensive guides**: 3,000-5,000 words maximum
- **How-to guides**: 1,500-2,500 words
- **Glossary/definition pages**: 800-1,200 words (exception to standard)

### Important Length Guidelines
- **Maximum for most articles**: 3,000 words
- **Maximum for pillar content**: 5,000 words
- If a topic requires more, break it into a cluster (pillar + satellites) instead
- Aim for the lower end of ranges — Swiss SERPs reward precise, practical answers over padding

### Quality Over Quantity
- Don't add fluff to hit word counts
- Every section must answer a real question a Swiss freelancer has
- Better 2,000 valuable words than 3,000 padded words

## Keyword Optimization

### Keyword Research Requirements
Before writing any article:
1. Identify primary target keyword (in the article's language)
2. Pull Swiss search volume and difficulty via DataForSEO (location 2756; `language_code` matching the article language)
3. Analyze top 10 Swiss ranking competitors (bexio, KLARA, banana.ch, treuhand blogs, admin.ch properties)
4. Identify 3-5 secondary/related keywords
5. List semantically related terms

### Keyword Density Guidelines
- **Primary keyword**: 1-2% density, always naturally integrated
- **Secondary keywords**: 0.5-1% each
- **Related terms**: sprinkle naturally (e.g. for "Rechnung schreiben": QR-Rechnung, Rechnungsvorlage, MWST-Nummer, Zahlungsfrist)

### Critical Keyword Placement
Primary keyword MUST appear in:
- [ ] H1 headline (preferably near the beginning)
- [ ] First 100 words of article
- [ ] At least 2-3 H2 subheadings
- [ ] Last paragraph / conclusion
- [ ] Meta title (within first 60 characters)
- [ ] Meta description
- [ ] URL slug (German-canonical)

### Keyword Integration Best Practices
- **Natural language first**: write for the freelancer, optimize for search second
- **Use variations**: "Rechnungsprogramm" → "Software für Rechnungen" → "Rechnungen erstellen"
- **Question formats**: match how Swiss users actually search ("Wie schreibe ich eine Rechnung?", "Was kostet bexio?")
- **The "schweiz" modifier matters**: most commercial terms are searched with "schweiz" (buchhaltungssoftware schweiz, rechnungsvorlage schweiz) — target the modified form

### Keyword Stuffing (Avoid)
❌ "Ein Rechnungsprogramm ist wichtig. Unser Rechnungsprogramm bietet Rechnungsprogramm-Funktionen für alle Rechnungsprogramm-Bedürfnisse."

✅ "Ein Rechnungsprogramm spart Selbständigen jeden Monat Stunden: QR-Rechnungen erstellen, Zahlungen abgleichen und die MWST vorbereiten — ohne Excel-Basteln."

## Content Structure Requirements

### Heading Hierarchy

#### H1 (Title)
- Only one H1 per article
- Include primary keyword naturally
- 60 characters or less
- Benefit-focused; answers "What will I get from this?"

#### H2 (Main Sections)
- 4-7 H2 sections for standard articles
- At least 2-3 include keyword variations
- Logical progression; standalone-readable from H2s alone

#### H3 (Subsections)
- Nested under H2s (never skip levels)
- Break complex sections into digestible chunks

### Article Structure Template

```markdown
# [H1: Compelling Title with Primary Keyword]

[Direct answer to the query in 1-2 sentences, then hook — see AI Search section]

> **Das Wichtigste in Kürze** (TL;DR block, 3-5 bullets)

## [H2: Main Section 1 - Keyword Variation]
### [H3 if needed]

## [H2: Main Section 2]
...4-7 total H2 sections...

## Häufige Fragen (FAQ, 4-6 questions)

## Fazit (recap + CTA)
```

## Meta Elements

### Meta Title
**Requirements**:
- **Length**: 50-60 characters
- Primary keyword included, ideally at the front
- Year for time-sensitive topics ("2026")
- Swiss specificity ("Schweiz", "CH", canton names) — it's a strong CTR signal in Swiss SERPs
- Unique across the site (check for pillar collisions — see cannibalization audits)

**Format options**:
- `[Primary Keyword] Schweiz 2026: [Benefit]`
- `[Keyword]: [Number/Promise] | Magic Heidi`
- `Wie [Goal]? [Qualifier]`

**Examples**:
- ✅ "Rechnungsvorlage Schweiz 2026: Gratis Word, Excel & PDF"
- ✅ "QR-Rechnung erstellen in 2 Minuten — kostenlos & konform"
- ❌ "Tipps und Tricks für Rechnungen" (vague, no keyword, no CH signal)

### Meta Description
**Requirements**:
- **Length**: 150-160 characters
- Include primary keyword naturally
- Directly answer the target query (AI engines quote it)
- Clear benefit + action phrase
- Language must match the locale of the page

**Formula**: `[Problem/Question]? [Solution/Benefit]. [Swiss-specific angle]. [CTA].`

### URL Slug
- German-canonical, root-level (no `/blog/` prefix), lowercase, hyphens
- Short and descriptive (2-4 words): `/rechnungsvorlage`, `/qr-rechnung-erstellen`, `/bexio-alternativen`
- **Never include years in slugs** (they go stale — see the `vat-rates-2025` lesson); years belong in titles only
- Same slug across all 6 locales; redirects for legacy slugs live in `mh-landing/config/redirects.ts`

## Internal Linking Strategy

### Requirements
- **Minimum**: 3 internal links per article; **optimal**: 4-5; max 7 (unless 3,000+ words)
- **Always check `context/internal-links-map.md`** — it lists verified live pages, canonical slugs, and per-page anchor guidance. Never link to a page you haven't verified exists.

### Link Types to Include
1. **Money pages (1-2 links)**: `/rechnungsprogramm` (highest-priority commercial page — link from every relevant article), `/buchhaltungssoftware`, `/mwst-freelancer`, `/beleg-scanner-schweiz`, `/pricing`, `/alternative/bexio`
2. **Cluster siblings (2-3 links)**: pillar ↔ satellite links within the topic cluster
3. **New pages need inbound links**: every newly published article must receive at least 2 links FROM existing pages (orphan pages don't rank — see cannibalization audit follow-ups)

### Anchor Text
- ✅ Descriptive, in-language: "QR-Rechnung in 2 Minuten erstellen"
- ❌ "hier klicken" / "mehr erfahren"
- Vary anchors for the same target; links use locale-correct paths (`/de/...`, `/fr/...`)

## External Linking Strategy

### Requirements
- 2-4 external authority links per article, to support claims and cite data

### Preferred Swiss Authority Sources
- **Tax/VAT**: estv.admin.ch (ESTV/AFC), gate.estv.admin.ch
- **General/legal**: ch.ch, admin.ch, kmu.admin.ch (SECO KMU-Portal), fedlex.admin.ch
- **Social insurance**: ahv-iv.ch
- **QR-bill/payments**: six-group.com (Swiss QR standard), SNB
- **Registry**: zefix.ch
- Cantonal tax offices for canton-specific topics
- ❌ Random blogs, non-Swiss tax advice (German/Austrian rules differ and mislead)
- Data freshness: prefer sources ≤ 1-2 years old; VAT rates and legal thresholds must be current-year

## Competitive & Comparison Content (UWG Compliance)

Swiss unfair-competition law (UWG Art. 3) requires comparative claims to be accurate and verifiable:
- All competitor pricing/feature claims come from `context/competitors/*.yaml` (single source of truth, each with `last_verified` + sources) — never from memory
- Include a visible "last verified" date on comparison pages
- Be honest about competitor strengths and when Magic Heidi is NOT the right fit (no payroll, no double-entry, solo-only) — it's both legally safer and more persuasive
- Re-verify pricing quarterly; update the YAML first, then propagate to pages

## Readability Optimization

- **Reading level**: simple, direct prose. German: short sentences matter even more than in English (Flesch behaves differently for German — trust sentence length over the raw score)
- **Sentence length**: average 15-20 words, max 25
- **Paragraphs**: 2-4 sentences, one idea each
- **Subheadings**: every 300-400 words
- **Active voice**, direct address ("du" per brand voice — check `context/brand-voice.md`)
- Lists and tables for anything enumerable (rates, deadlines, price comparisons)

## Content Quality Standards

### E-E-A-T for Swiss Finance Content
This is money/finance adjacent content (YMYL) — Google holds it to a higher standard:
- **Accuracy is non-negotiable**: VAT rates, AHV contribution rates, thresholds (CHF 100'000 MWST registration), deadlines must be current and cited
- **Experience**: use real freelancer scenarios, real numbers, founder perspective (Nathan, ex-freelancer, Morges)
- **Author attribution**: named author + "last updated" date visible on page
- **Product references**: Magic Heidi features/pricing from `context/features.md` (Pro CHF 25/mo annual = CHF 299/yr, CHF 39/mo monthly; free tier 3 invoices + 3 expenses)

### Content Originality
- Add unique value: calculators, templates, real examples, honest comparisons
- Differentiate from bexio/KLARA content (they target SMEs; we own the solo-freelancer angle)
- Update outdated content instead of duplicating it — **check for existing pages on the topic before creating a new one** (cannibalization is a recurring problem; one keyword = one page)

## Image Optimization

- Descriptive, keyword-rich file names (`qr-rechnung-beispiel-schweiz.png`)
- Alt text ≤125 chars, in the article's language, describing the image
- Compressed for fast loading; screenshots current with app UI

## Featured Snippet Optimization

### Question-Based Snippets
Include the question as H2, answer in 40-60 words immediately after:

```markdown
## Was ist eine QR-Rechnung?

Die QR-Rechnung ist der Schweizer Standard für Rechnungen mit Zahlteil: ein Swiss QR Code enthält alle Zahlungsinformationen (IBAN, Betrag, Referenz), sodass Kunden per Banking-App in Sekunden bezahlen. Seit Oktober 2022 ersetzt sie die roten und orangen Einzahlungsscheine vollständig.
```

### List/Table Snippets
- Numbered lists for processes (5-8 steps), tables for rates/prices/comparisons
- Swiss SERPs show tables prominently for "vergleich"/"kosten" queries — always include a comparison table on those pages

## AI Search Optimization (GEO/AICO)

AI search engines (ChatGPT, Perplexity, Gemini, Claude) are a significant recommendation channel — 90% of buyers consult AI before purchase decisions. These rules ensure content performs in both Google and AI answers.

### Direct-Answer-First Principle
- **Answer the query directly in the first 1-2 sentences**, before any hook or story
- For "best/top/how/was kostet" queries, state the answer or thesis immediately
- Put the core answer in the meta description too
- Never bury the answer behind 200+ words of context

### TL;DR / Key Takeaways Block
Every article includes a TL;DR block after the intro ("Das Wichtigste in Kürze" / "L'essentiel en bref"):
- 3-5 bullets, each a complete standalone claim with specific numbers/names
- This is the article's conclusions up front, not a table of contents

### Authority Signaling for AI
- Named author (not "Team"), visible last-updated date, year in titles for time-sensitive topics
- These go in the Nuxt Content frontmatter

### One Idea Per Section
- AI models parse and cite by section — one concept per H2/H3, structured formatting within

### FAQ Sections as Prompt Targets
- 4-6 questions per article, phrased how real users ask ("Was kostet bexio im Monat?", "Kann ich als Privatperson eine Rechnung stellen?")
- Answer directly in the first sentence, then expand
- Source questions from Google PAA, Reddit (r/Switzerland, r/askswitzerland), and search suggestions

### Content Repurposing
- More surfaces = more AI citations: `/repurpose` adapts articles for LinkedIn, Medium, Reddit, Quora
- See `context/ai-citation-targets.md` for priority surfaces and `/research-ai-citations` for auditing

## Content Refresh Strategy

### When to Update
- Article 12+ months old, or contains a stale year reference
- Rates/thresholds/laws changed (check every January: VAT rates, AHV rates, tax deadlines)
- Rankings declined or competitor content surpassed ours
- Every seasonal page (Feiertage, school holidays) needs a yearly refresh BEFORE its season

### What to Update
- Last-updated date, statistics, screenshots, examples
- Title year, internal links to newer content
- Verify all pricing claims against `context/competitors/*.yaml`

## SEO Checklist for Every Article

### Content
- [ ] Correct language + Swiss conventions (no ß in German)
- [ ] Primary keyword identified with Swiss (2756) volume data
- [ ] Keyword density 1-2%, 3-5 secondary keywords
- [ ] No existing page already targets this keyword (cannibalization check)
- [ ] Factually accurate: rates, thresholds, deadlines current and cited

### Structure
- [ ] One H1 with primary keyword; 4-7 H2s, 2-3 with variations
- [ ] Keyword in first 100 words and conclusion
- [ ] Direct answer in first 1-2 sentences + TL;DR block

### Meta Elements
- [ ] Meta title 50-60 chars with keyword + Swiss/year signal
- [ ] Meta description 150-160 chars, answers the query, with CTA
- [ ] German-canonical slug, no year in slug, unique vs existing pages

### Links
- [ ] 3-5 internal links per `context/internal-links-map.md` (incl. 1-2 money pages)
- [ ] ≥2 inbound links added FROM existing pages to any new article
- [ ] 2-4 Swiss authority external links, all functional

### Quality
- [ ] Brand voice per `context/brand-voice.md`
- [ ] Comparison claims sourced from `context/competitors/*.yaml` with verification date
- [ ] FAQ section (4-6 natural-language questions)
- [ ] Named author + last-updated date
- [ ] Clear CTA (free tier: 3 invoices + 3 expenses, no credit card)

## Tools & Data Sources

- **Keyword/SERP data**: DataForSEO (scripts in `data_sources/`, location 2756, language per article) — this is the standard source, not Ahrefs
- **Rankings/impressions**: Google Search Console (`google_search_console.py`)
- **Traffic**: Vercel Web Analytics CSV exports
- **Content scoring**: `data_sources/modules/` analyzer chain (`seo_quality_rater.py` target ≥85 before publishing)

---

**Remember**: SEO serves the user, not the algorithm. A Swiss freelancer should leave every page with their question fully answered. The best SEO is content that genuinely helps them run their business.

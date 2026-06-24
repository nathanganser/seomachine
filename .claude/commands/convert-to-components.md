# Convert to Components Command

Use this command to convert a plain markdown file (landing page or blog article) into Nuxt Content MDC component format, ready for deployment.

## Usage
`/convert-to-components [file path]`

**Examples:**
- `/convert-to-components landing-pages/swiss-invoicing-2026-05-03.md`
- `/convert-to-components drafts/freelancer-accounting-2026-05-01.md`

## What This Command Does

1. Reads a plain markdown file (landing page or blog article) and converts it to Nuxt Content MDC component format
2. Maps each content section to the most appropriate UI component
3. Selects relevant images from available assets
4. Adds internal links where appropriate
5. Validates no content was lost during conversion
6. Saves to `components-ready/` folder
7. Runs quality scoring with auto-revision loop
8. Executes content-type-appropriate optimization agents

## Pre-Conversion Review

**Required — read these files before starting conversion:**
- **Component Template**: `.claude/skills/landing-components/references/component-template.md` — the source of truth for all available components and their YAML schemas
- **Available Images**: `.claude/skills/landing-components/references/available-images.md` — image filenames you can reference
- **Internal Links**: `.claude/skills/landing-components/references/internal-links.md` — valid internal URLs for CTAs and links
- **Brand Voice**: `context/brand-voice.md` — tone and messaging guidelines
- **CRO Best Practices**: `context/cro-best-practices.md` — conversion optimization guidelines
- **Style Guide**: `context/style-guide.md` — formatting and grammar rules for all copy
- **SEO Guidelines**: `context/seo-guidelines.md` — keyword and structure rules (converted pages still need to rank)

---

## Conversion Process

### Step 1: Parse Source File

- Read the full source markdown file
- Extract metadata (Meta Title, Meta Description, Target Keyword, URL Slug, etc.)
- Identify each content section by H2 headers
- Classify each section's purpose: hero, pain points, features, testimonials, FAQ, CTA, comparison, pricing, etc.
- Count total sections and approximate word count for later validation

### Step 2: Build YAML Frontmatter

Convert the markdown metadata to Nuxt Content YAML frontmatter:

```yaml
---
title: "[from Meta Title or H1]"
description: "[from Meta Description]"
---
```

### Step 3: Map Sections to Components

The mapping differs by content type. Check the content type (Step 9 logic applies here too) and use the appropriate table.

---

#### Landing Page Mapping

For each identified section, select the best-fit component from the template:

| Section Type | Primary Component | Alternative |
|-------------|------------------|-------------|
| Opening headline + stats | `::pages-landing-hero-section` | `::feature-image` (if no stats) |
| Problem / pain points | `::pages-landing-pain` | — |
| Feature showcase (3-4 items) | `::pages-landing-invoice-showcase` | — |
| Detailed features with bullets | `::pages-landing-features` | — |
| Individual feature + image | `::feature-image` (horizontal) | — |
| Swiss-specific content | `::pages-landing-swiss-section` | — |
| Comparison table | `::pages-landing-comparison` | — |
| Testimonials | `::hero-reviews` | — |
| Pricing | `::pages-landing-plans` | — |
| FAQ | `::pages-landing-faq` | — |
| Final CTA | `::pages-landing-final-cta` | — |
| Video embed | `::hero-media` | — |
| Prose / content that doesn't fit | `::markdown` (boxed: true) | — |

---

#### Blog Article Mapping

**First, decide which opener pattern applies:**

- **Blog article** — informational, opinion, news, evergreen explainer published at `/blog/<slug>`. **Opens with `::blog`** (Article schema + dated header with author). Prose lives in nested `::markdown as: article` blocks inside `::blog`.
- **Integration / product-content article** — long-form commercial page under `/integrations/<platform>`, `/alternative/<competitor>`, or a feature page (`/invoicing`, `/accounting`, etc.). **Opens with `::feature-image`** (hero image + the article's title in the `title:` prop). Skip `::blog` entirely — these pages aren't dated editorial content. Prose lives in top-level `::markdown as: article` blocks following the `::feature-image`. If you need author attribution, drop a one-sentence credit at the end of the final `::markdown` block.

Detection cues for the integration / product-content pattern: source frontmatter `url_slug` contains `/integrations/`, `/alternative/`, or matches a feature-page path; the article reads as evergreen "how to use Magic Heidi for X" rather than dated commentary.

The rest of this section describes the blog opener. For integration / product-content articles, replace the `::blog` block at the top with a `::feature-image` block (no nested children) and keep every `::markdown as: article` block at the top level (no 2-space indent). Structured-component placement after the opener is identical for both patterns.

---

`::blog` is the article header component (title, description, date, author + structured data for SEO). It comes FIRST on the page, after the page frontmatter.

**`::blog` may wrap `::markdown` blocks — and ONLY `::markdown` blocks.** All article prose goes inside `::blog` as nested `::markdown` blocks with `as: article` (indented 2 spaces). Structured components — `::pages-landing-faq`, `::pages-landing-comparison`, `::feature-grid`, `::feature-image`, `::feature-showcase`, `::hero-reviews`, etc. — MUST NOT be nested inside `::blog`. They come AS SIBLINGS AFTER `::blog`'s closing `::`.

The correct structure is:

```
---
title: "[article title]"
description: "[meta description]"
---

::blog
---
date: "[publication date]"
title: "[article title]"
description: "[meta description]"
author:
  name: "Nathan Ganser"
  description: "Founder of Magic Heidi"
  avatar: "https://magicheidi.ch/images/visuals/nathan.webp"
---

  ::markdown
  ---
  as: article
  ---
  [intro prose, key takeaways, first body sections]
  ::

  ::markdown
  ---
  as: article
  ---
  [more body prose]
  ::

::

::pages-landing-comparison
---
[comparison table YAML]
---
::

::feature-image
---
[feature image YAML]
---
::

::pages-landing-faq
---
[FAQ YAML]
---
::
```

**Critical rules**:
- `::blog` may contain `::markdown` blocks (with `as: article`) and nothing else. Indent each nested `::markdown` block with 2 spaces.
- Structured components (`::pages-landing-faq`, `::pages-landing-comparison`, `::feature-grid`, `::feature-image`, `::feature-showcase`, `::hero-reviews`, etc.) MUST come as siblings after `::blog` closes — never nested inside it.
- **Target 4+ structured components after `::blog`** for a typical 2,000-word article. The prose blocks inside `::blog` are connective tissue between the visual components below; treat any extractable pattern as an opportunity, not a special case.
- **Inside `::blog`, split prose into 3–5 separate `::markdown as: article` blocks at H2 boundaries.** A single mega-block is a signal you missed extraction opportunities — re-scan the prose with the table below.
- Scan the prose for these patterns and lift each one out into the matching component. Place extracted components after `::blog`'s closing `::`, in the order they appeared in the source:

| Pattern in the article | Component to use |
|---|---|
| A list of 3–5 items (tips, steps, benefits, reasons) | `::feature-grid` with emoji icons derived from content |
| A "how it works" or numbered steps section | `::feature-grid` with 1️⃣2️⃣3️⃣ icons |
| Any named enumeration in prose ("the three indicators…", "four signs of…", "five things to check") — even if it's a single sentence | `::feature-grid` with topical emoji icons |
| Pros/cons, benefits/risks, gains/losses, or any two contrasting categories with bullets | `::pages-landing-features` with 2 category items |
| A section describing a product feature + a relevant screenshot exists | `::feature-image` (horizontal) |
| A section with 3 highlights + product screenshot or video | `::feature-showcase` |
| A comparison table or "X vs Y" section | `::pages-landing-comparison` |
| A FAQ or Q&A section | `::pages-landing-faq` |
| Testimonials, user quotes, or social proof | `::hero-reviews` |
| A summary recap with 3–5 takeaways or thresholds | `::feature-grid` (theme: elevated) |
| A YouTube link or video reference in the prose | `::hero-media` with `youtube.id` |
| A final "try it / start here" paragraph | `::hero-basic{.bg-cream}` wrapping `::hero-cta-links` |

When you lift content out, replace its prose footprint with a one-sentence pointer ("Die Indizien findest du als Übersicht weiter unten") or drop the prose entirely — let the structured component carry the section. The reader sees all prose first, then the components in source order; design for that flow.

---

**Important**: Always check the component template file for the exact YAML schema. Do not guess prop names — copy them from the template examples.

### Step 4: Select Images

For each component that accepts images:
- Check `available-images.md` for relevant image filenames
- Use `{locale}` images for product screenshots (e.g., `invoice-list.{locale}.webp`)
- Use static images for decorative photos (e.g., `chalet-sion.webp`)
- Write descriptive alt text for accessibility

### Step 5: Add Internal Links

Reference `internal-links.md` for valid URLs:
- Use in CTA buttons (e.g., `url: /pricing`, `url: /start`)
- Use in `::hero-cta-links` components
- Use in `::hero-reviews` CTA links
- Only link to URLs that exist in the internal links file

### Step 6: Generate Output

Write the full MDC file with:
- YAML frontmatter at the top
- Each component block with `::component-name` / `---` / props / `---` / `::` syntax
- Proper YAML formatting (see rules below)
- Nested components indented with exactly 2 spaces

### Step 7: Validate

Before saving, verify:
- [ ] Every section from the original appears in the output (no content dropped)
- [ ] All YAML strings containing colons or HTML tags are quoted
- [ ] Nested components use 2-space indentation
- [ ] All `image.src` values reference files from `available-images.md`
- [ ] All internal URLs exist in `internal-links.md`
- [ ] Component names match exactly what's in `component-template.md`
- [ ] Section count in output >= section count in source
- [ ] No `::` closing tags on the same line as content text (each `::` must be on its own line, with a blank line before it)
- [ ] No merged closing/opening tags (e.g., `::::component-name` is invalid — always separate with a blank line)
- [ ] All `[text](url)` links from the source appear somewhere in the output (in markdown links, YAML `url:` props, or HTML `<a>` tags)
- [ ] Comparison/table components have the same column count as the source table

### Step 8: Save and Report

- Save to: `components-ready/[slug].md`
- Print a conversion summary:
  - Number of sections converted
  - Components used (list each)
  - Images referenced
  - Any warnings (e.g., sections that used `::markdown` fallback)

---

## Post-Conversion Pipeline

**CRITICAL**: After saving the MDC file, run these steps automatically — do not skip any.

### Step 9: Detect Content Type

Determine the content type from the source file path to select the appropriate quality scorer and agents:

- **Source from `landing-pages/`** → content type is **landing page**
- **Source from `drafts/`** → content type is **blog article**
- **Other source** → default to **blog article**

### Step 10: Quality Scoring & Revision Loop

Run the appropriate quality scorer based on content type:

**For landing pages:**
```bash
python3 data_sources/modules/landing_page_scorer.py components-ready/[filename].md --type seo --goal trial
```
- **Threshold**: Score ≥ 75 to pass

**For blog articles:**
```bash
python3 data_sources/modules/content_scorer.py components-ready/[filename].md
```
- **Threshold**: Score ≥ 70 to pass

**Revision loop:**
1. If score is below threshold, review the `priority_fixes` from the scorer
2. Apply the top 3-5 fixes to the MDC file
3. Re-score the content
4. Repeat once more if still below threshold

### Step 11: Failure Routing

Based on the final score after up to 2 revision attempts:

- **Score passes threshold**: Keep in `components-ready/` and proceed to agents
- **Score fails after 2 attempts**: Move to `review-required/components/` with a `_REVIEW_NOTES.md` file containing:
  - Final score and dimension breakdown
  - Remaining priority fixes
  - Reason for human review

### Step 12: Automatic Agent Execution

Run agents appropriate to the detected content type:

**For blog articles** (source from `drafts/`):

1. **SEO Optimizer Agent**
   - **Agent**: `seo-optimizer`
   - **Input**: Full MDC file content
   - **Output**: SEO optimization report
   - **File**: `audits/components/seo-report-[slug].md`

2. **Internal Linker Agent**
   - **Agent**: `internal-linker`
   - **Input**: MDC file content
   - **Output**: Internal linking recommendations (verify component CTAs and links reference valid URLs)
   - **File**: `audits/components/link-suggestions-[slug].md`

3. **Meta Creator Agent**
   - **Agent**: `meta-creator`
   - **Input**: MDC file content and target keyword
   - **Output**: Meta title/description options
   - **File**: `audits/components/meta-options-[slug].md`

**For landing pages** (source from `landing-pages/`):

1. **Landing Page Optimizer Agent**
   - **Agent**: `landing-page-optimizer`
   - **Input**: Full MDC file content
   - **Output**: CRO optimization report (above-fold, CTAs, trust signals, friction analysis)
   - **File**: `audits/components/optimization-report-[slug].md`

2. **CRO Analyst Agent**
   - **Agent**: `cro-analyst`
   - **Input**: MDC file content and conversion goal
   - **Output**: Psychology and persuasion analysis
   - **File**: `audits/components/cro-analysis-[slug].md`

**For both content types:**

- **Content Analyzer Agent**
  - **Agent**: `content-analyzer`
  - **Input**: Full MDC file, meta elements, keywords
  - **Output**: Search intent, keyword density, readability, SEO quality rating
  - **File**: `audits/components/content-analysis-[slug].md`

---

## YAML Formatting Rules (Critical)

These prevent the most common breakage in MDC files:

1. **Quote strings with special chars**: Always use double quotes for strings containing `:`, `<span>`, `<em>`, `<br>`, `<strong>`, `#`, `!`, `[`, `{`
2. **Multi-line strings**: Use `|` block scalar for titles spanning multiple lines
3. **Nested components**: Indent with exactly 2 spaces inside parent `::component`
4. **Arrays**: Use `- ` prefix with consistent indentation
5. **Boolean values**: Use `true`/`false` without quotes
6. **Numbers**: Use without quotes unless they contain special formatting (e.g., `"4.9★"`)

---

## Cleanup Previous Stage
After all processing is complete (conversion, scoring, agents), delete the source files:
- Delete the source markdown file (from `drafts/` or `landing-pages/`)
- If the source was from `drafts/`, also delete associated report files in `drafts/_reports/` that match the same topic slug
- Only delete files related to this specific article, not the entire folder

## Output
Save to: `components-ready/[slug].md`

## File Management
- Output goes to `components-ready/` as a new file
- Use the same slug as the source file

## Next Steps

After the file is saved to `components-ready/`, tell the user:

> **Next step:** Run `/translate-components components-ready/[filename]` to translate to other locales.

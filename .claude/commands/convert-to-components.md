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

For each identified section, select the best-fit component from the template. Use this mapping as a starting point:

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

- Save to: `components-ready/[slug]-[YYYY-MM-DD].md`
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
   - **File**: `audits/components/seo-report-[slug]-[YYYY-MM-DD].md`

2. **Internal Linker Agent**
   - **Agent**: `internal-linker`
   - **Input**: MDC file content
   - **Output**: Internal linking recommendations (verify component CTAs and links reference valid URLs)
   - **File**: `audits/components/link-suggestions-[slug]-[YYYY-MM-DD].md`

3. **Meta Creator Agent**
   - **Agent**: `meta-creator`
   - **Input**: MDC file content and target keyword
   - **Output**: Meta title/description options
   - **File**: `audits/components/meta-options-[slug]-[YYYY-MM-DD].md`

**For landing pages** (source from `landing-pages/`):

1. **Landing Page Optimizer Agent**
   - **Agent**: `landing-page-optimizer`
   - **Input**: Full MDC file content
   - **Output**: CRO optimization report (above-fold, CTAs, trust signals, friction analysis)
   - **File**: `audits/components/optimization-report-[slug]-[YYYY-MM-DD].md`

2. **CRO Analyst Agent**
   - **Agent**: `cro-analyst`
   - **Input**: MDC file content and conversion goal
   - **Output**: Psychology and persuasion analysis
   - **File**: `audits/components/cro-analysis-[slug]-[YYYY-MM-DD].md`

**For both content types:**

- **Content Analyzer Agent**
  - **Agent**: `content-analyzer`
  - **Input**: Full MDC file, meta elements, keywords
  - **Output**: Search intent, keyword density, readability, SEO quality rating
  - **File**: `audits/components/content-analysis-[slug]-[YYYY-MM-DD].md`

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

## Output
Save to: `components-ready/[slug]-[YYYY-MM-DD].md`

## File Management
- Source files in `landing-pages/` or `drafts/` are NOT modified
- Output goes to `components-ready/` as a new file
- Use the same slug as the source file with the current date

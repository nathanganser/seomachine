---
name: landing-components
version: 1.0.0
description: When the user wants to convert plain markdown files (landing pages or blog articles) into Nuxt Content MDC component format, work with landing page components, or asks about "convert to components," "MDC format," "component format," "landing page components," or "Nuxt Content components." For creating the initial markdown landing page, see landing-write command. For publishing, see landing-publish command.
---

# Landing Components

You are an expert in converting markdown content (landing pages and blog articles) into Nuxt Content MDC (Markdown Components) format. Your goal is to map content sections to the most appropriate UI component while preserving all content and maximizing conversion potential.

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before starting. Use that context for brand-appropriate component choices.

Before converting, understand:

1. **Source Content** - Read the full markdown file. Identify every section, its purpose, and its content.
2. **Available Components** - Read [references/component-template.md](references/component-template.md) for the full list of components and their YAML schemas.
3. **Available Images** - Read [references/available-images.md](references/available-images.md) to select appropriate visuals.
4. **Internal Links** - Read [references/internal-links.md](references/internal-links.md) for valid URLs to use in CTAs and links.
5. **Style Guide** - Read `context/style-guide.md` for formatting and grammar rules that apply to all copy in components.
6. **SEO Guidelines** - Read `context/seo-guidelines.md` for keyword and structure rules (converted pages still need to rank).

---

## Core Principles

### 1. No Content Loss
Every piece of content from the source must appear in the output. If a section does not cleanly map to a specific component, use `::markdown` with `boxed: true` as a fallback. Never silently drop content.

### 1b. No Link Loss
Every internal and external link from the source must appear in the output. Scan the source for all `[text](url)` markdown links and the metadata `Internal Links` field. Preserve them in `::markdown` blocks, component `url:` props, or HTML `<a>` tags. If a link can't fit in a structured component, add a nearby `::markdown` block to hold it.

### 2. Template is the Source of Truth
Only use components that exist in `component-template.md`. Do not invent component names or props. Read the template every time — it may have been updated.

### 3. YAML Correctness Above All
MDC component props are YAML. Broken YAML = broken page. Follow the formatting rules strictly.

### 4. Choose Components for Conversion Impact
When multiple components could work, choose the one that best serves the conversion goal (trial signup, demo booking, lead capture). A `::pages-landing-hero-section` with stats is stronger than a plain `::feature-image` for a page targeting signups.

---

## Component Selection Heuristics

Use these guidelines to map markdown sections to components:

| Content Pattern | Best Component | When to Use Instead |
|----------------|---------------|-------------------|
| Opening headline + hook + trust stats | `::pages-landing-hero-section` | `::feature-image` if no stats, just image-focused |
| Problem/pain points (3-4 items) | `::pages-landing-pain` | — |
| Feature showcase (3-4 compact items) | `::pages-landing-invoice-showcase` | — |
| Detailed features with bullet lists | `::pages-landing-features` | `::hero-basic` + `::detailed-feature-list` for image-heavy features |
| Individual feature highlight with image | `::feature-image` | Use `orientation: horizontal` for side-by-side |
| Swiss-specific / locale content | `::pages-landing-swiss-section` | — |
| Comparison table | `::pages-landing-comparison` | — |

> **Comparison tables**: When converting a markdown table to `::pages-landing-comparison`, ALL columns and rows from the source must be included. Count columns in the source table and verify the output has the same count. Do not drop columns to simplify the layout.
| Testimonials / social proof | `::hero-reviews` | — |
| Pricing plans | `::pages-landing-plans` | — |
| FAQ section | `::pages-landing-faq` | — |
| Final call-to-action | `::pages-landing-final-cta` | — |
| Grid of features/benefits (no bullets) | `::hero-basic` + `::feature-grid` (nested) | — |
| Step-by-step process | `::hero-basic` + `::detailed-feature-list` (nested) | — |
| Video embed | `::hero-media` | — |
| Full-width image break | `::feature-image` with `fullscreen: true` | — |
| Long prose content | `::markdown` | Use `theme: dark` to match adjacent dark sections |

### Choosing Between Similar Components

- **`::feature-image` vs `::pages-landing-hero-section`**: Use hero-section when you have stats to display and want the signup CTA. Use feature-image for visual-focused sections or article-style heroes.
- **`::pages-landing-invoice-showcase` vs `::pages-landing-features`**: Showcase is for 3-4 compact icon+title+subtitle items. Features is for deeper content with bullet lists per item.
- **`::hero-basic` (container) vs standalone components**: Use hero-basic when you need to nest `::feature-grid`, `::detailed-feature-list`, or `::hero-cta-links` inside a section with its own title/subtitle.

---

## YAML Formatting Rules

These rules prevent the most common MDC breakage:

### Quoting Strings
**Always wrap in double quotes** when the string contains:
- Colons (`:`)
- HTML tags (`<span>`, `<em>`, `<br>`, `<strong>`, `<br/>`)
- Exclamation marks at the start
- Hash symbols (`#`)
- Square brackets (`[]`)
- Curly braces (`{}`)

```yaml
# CORRECT
title: "Invoicing Made <span>Simple</span>"
subtitle: "The all-in-one app: invoicing, expenses, and taxes."

# WRONG - will break YAML parsing
title: Invoicing Made <span>Simple</span>
subtitle: The all-in-one app: invoicing, expenses, and taxes.
```

### Multi-line Strings
Use `|` (literal block scalar) for multi-line content:

```yaml
title: |
  Two Line Title.<br/>
  <span>With Highlight.</span>
```

### Nested Components
Nested components must be indented with **exactly 2 spaces**:

```markdown
::hero-basic{.bg-white}
---
title: "Section Title"
---

  ::feature-grid
  ---
  items:
    - title: Item One
      description: Description here.
  ---
  ::
::
```

### Component Closing Tags
The `::` closing a component MUST be on its own line. NEVER append `::` to the end of a content line. Always leave a blank line between the last content line and the closing `::`.

```markdown
# CORRECT
Last paragraph of content here.

::

# WRONG - breaks MDC parsing
Last paragraph of content here.::

# ALSO WRONG - merges close with next open
Last paragraph of content here.::::next-component
```

### Arrays
Use consistent indentation. Each item starts with `- `:

```yaml
items:
  - icon: emoji
    title: Item Title
    subtitle: Item subtitle
  - icon: emoji
    title: Second Item
    subtitle: Second subtitle
```

---

## Image Selection

When choosing images from `available-images.md`:
- Use `{locale}` suffix images (e.g., `invoice-list.{locale}.webp`) for product screenshots that should be localized
- Use static images (e.g., `chalet-sion.webp`) for decorative/atmospheric photos
- Always provide descriptive `alt` text
- Match image context to section content (e.g., expense-related sections get `expenses-list.{locale}.webp`)

---

## Page Structure

A well-structured component page typically follows this order:

1. **Hero** — `::pages-landing-hero-section` or `::feature-image`
2. **Pain/Problem** — `::pages-landing-pain`
3. **Solution/Showcase** — `::pages-landing-invoice-showcase`
4. **Feature details** — `::pages-landing-features` or multiple `::feature-image`
5. **Social proof** — `::hero-reviews`
6. **Comparison** (optional) — `::pages-landing-comparison`
7. **Pricing** (optional) — `::pages-landing-plans`
8. **FAQ** — `::pages-landing-faq`
9. **Final CTA** — `::pages-landing-final-cta`

Not every page needs every section. Match the source content structure.

---

## Output Format

The converted file should be a valid Nuxt Content MDC file:

```markdown
---
title: "Page Title for SEO"
description: "Meta description for SEO"
---

::component-one
---
props: here
---
::

::component-two
---
props: here
---
::
```

Save to: `components-ready/[slug]-[YYYY-MM-DD].md`

---

## Post-Conversion Pipeline

**CRITICAL**: After saving the MDC file, run these steps automatically — do not skip any.

### 1. Content Scrubbing

Immediately after saving, run `/scrub components-ready/[filename].md` to remove AI watermarks and telltale patterns from text content in component props (titles, subtitles, descriptions, FAQ answers, `::markdown` sections). The scrubber is idempotent and preserves YAML/MDC structure.

### 2. Detect Content Type

Determine the content type from the source file path:
- **Source from `landing-pages/`** → content type is **landing page**
- **Source from `drafts/`** → content type is **blog article**
- **Other source** → default to **blog article**

### 3. Quality Scoring & Revision Loop

Run the appropriate scorer based on content type:

**For landing pages:**
```bash
python3 data_sources/modules/landing_page_scorer.py components-ready/[filename].md --type seo --goal trial
```
Threshold: Score ≥ 75

**For blog articles:**
```bash
python3 data_sources/modules/content_scorer.py components-ready/[filename].md
```
Threshold: Score ≥ 70

**Revision loop:** If below threshold, apply the top 3-5 priority fixes, re-score, and repeat once more if still below.

### 4. Failure Routing

- **Passes threshold**: Keep in `components-ready/` and proceed to agents
- **Fails after 2 attempts**: Move to `review-required/components/` with a `_REVIEW_NOTES.md` file containing the final score, dimension breakdown, remaining fixes, and reason for review

### 5. Automatic Agent Execution

Run agents appropriate to the detected content type:

**For blog articles** (source from `drafts/`):
- **SEO Optimizer** (`seo-optimizer`) — keyword placement and structure
- **Internal Linker** (`internal-linker`) — verify component CTAs and links
- **Meta Creator** (`meta-creator`) — meta title/description options

**For landing pages** (source from `landing-pages/`):
- **Landing Page Optimizer** (`landing-page-optimizer`) — CTA placement, trust signals, above-fold, friction
- **CRO Analyst** (`cro-analyst`) — psychology and persuasion review

**For both content types:**
- **Content Analyzer** (`content-analyzer`) — search intent, keyword density, readability, SEO quality rating

Agent reports are saved to `components-ready/` alongside the converted file.

---

## References

- [references/component-template.md](references/component-template.md) — All available components with example YAML
- [references/available-images.md](references/available-images.md) — Image filenames in /images/visuals/
- [references/internal-links.md](references/internal-links.md) — Valid internal page URLs

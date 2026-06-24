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

### 5. Subtitles Stay Short
Every `subtitle:` (and `description:` inside `highlights`/`features`) targets **1 sentence, ≤20 words**. Hard cap is 2 sentences. Inline HTML (`<span>`, `<br>`, `<strong>`, `<em>`, `<a href>`) is supported. Long multi-clause subtitles read as filler — trim ruthlessly. The component template's `hero-basic` Props block lists the rule; apply it to every component that extends `hero-basic` (`feature-image`, `feature-showcase`, `pages-landing-features`, `pages-landing-pain`, `pages-landing-swiss-section`, etc.).

### 6. Feature Sections Deep-Link to Their Feature Page
For each `feature-image` or `feature-showcase` block that describes a product feature with a matching `/feature` page in `internal-links.md`, append an inline `<a>` tag at the end of the subtitle:

```yaml
subtitle: "Foto unterwegs, MWST automatisch zugeordnet, Fremdwährung in CHF umgerechnet. <a href=\"/ai-expenses-scanning\">Mehr zum KI-Belegscan →</a>"
```

Verified feature paths: `/invoicing`, `/ai-expenses-scanning`, `/accounting`, `/vat-management`, `/bank-statement-import`, `/security`, `/customer-management`, `/quotes`, `/web`, `/iphone`, `/mac`, `/windows`, `/freelancer`. Skip when no relevant feature page exists — don't force a link.

### 7. Reviews Link to Their Source
`hero-reviews` items[] support a per-item `link:` field. When the page cites public reviews (Capterra, Google, Trustpilot, App Store), set `link:` on each item so visitors can click through to verify. Use the source's name as `author` (e.g., "Capterra Bewertung") and put the rating + "alle Bewertungen lesen" hint in `role`. See the `hero-reviews` example in the component template.

### 8. Single-Language Page = Single-Language Copy
The output page is rendered in one locale at a time (DE / FR / IT / EN). Do NOT mention multilingual support on a German page (e.g., "Support in DE/FR/IT/EN") — German readers care that German support is good, not that French support also exists. Translation creates the other-locale variants. The exception: invoicing **into** other languages is genuinely valuable to German freelancers with FR/IT Swiss clients — phrase as "Rechnungen in der Sprache deines Kunden", not as a DE/FR/IT/EN abbreviation list.

### 9. No Content Invention
Convert, don't write. Component `title:` / `subtitle:` / `description:` / highlight text must come from the source's own words — do not fabricate marketing copy, taglines, or one-liners to fill a field. If a component needs a label the source doesn't provide, reuse the nearest heading or omit the field rather than invent one. This matters most for author-written / opinion pieces: invented lines break the voice and get rejected. (Corollary to "No Content Loss": don't lose content, and don't add content either.)

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
| Interactive Stundenlohn / Monatslohn calculator | `::hourly-wage-calculator` | Place high on the page for salary-to-hourly conversion articles. No props required; the component renders its own inputs and outputs. |
| Long prose content | `::markdown` | Use `theme: dark` to match adjacent dark sections |

### Choosing Between Similar Components

- **`::feature-image` vs `::pages-landing-hero-section`**: Use hero-section when you have stats to display and want the signup CTA. Use feature-image for visual-focused sections or article-style heroes.
- **`::pages-landing-invoice-showcase` vs `::pages-landing-features`**: Showcase is for 3-4 compact icon+title+subtitle items. Features is for deeper content with bullet lists per item.
- **`::hero-basic` (container) vs standalone components**: Use hero-basic when you need to nest `::feature-grid`, `::detailed-feature-list`, or `::hero-cta-links` inside a section with its own title/subtitle.

---

## Layout & Containers (how nesting affects padding — read before building grids)

How a component is nested decides its padding and whether it renders at all. Every rule here comes from real breakage:

### Components with no padding of their own — never place bare at top level
`::feature-grid`, `::detailed-feature-list`, and `::hero-cta-links` render with **no horizontal padding** — at the top level they go full-bleed (cards touch the screen edges). They MUST be nested in a container. Pick by how heavy you want the section:
- **`::hero-basic`** — a full titled *section*: large vertical padding **plus a reserved header area**. Use only when you genuinely want a big section with a display-size title. Note: its empty header still reserves space, so a bare grid under an empty hero-basic shows a large gap.
- **`:::markdown`** (3-colon, light) — an article-flow container (~32px padding, no reserved header). **Prefer this for a card grid that only needs a small subheader.** A real `###` heading inside renders as a normal subheader, and the grid gets the markdown container's padding without hero-basic's heavy section spacing:
  ```
  :::markdown
  ---
  as: article
  ---
  ### Short subheader (renders as a normal h3)

  ::feature-grid
  ---
  theme: base      # bordered cards on the page bg
  items: [ ... ]
  ---
  ::
  :::
  ```
  Add `{.bg-cream}` to the `:::markdown` for a cream band — and switch the grid to `theme: elevated` (white cards) so they pop on the colour. On a plain page background use `theme: base`.

### Self-contained "stat / spec box" → `::markdown{boxed: true}`
A single tool/feature box (name + a few stat lines) is cleanest as a `::markdown{boxed: true}` card (white bg, shadow, padding, no header). Do NOT use a one-item `::feature-grid` inside `::hero-basic` for this — it adds an empty header above the lone card.

### Interleave prose and components (blog / article)
After `::blog`, alternate top-level `::markdown as: article` blocks **between** the structured components, in source order. Putting all prose first and all components last reads as "plain markdown with components dumped at the bottom" — the thing that looks unfinished.

### Only use utility classes that already exist in the `.vue` components
The site uses UnoCSS with on-demand generation. Do **not** introduce a new utility class via the `.md` — especially `!important` variants (`!py-8`) or a class inside a YAML prop value (`titleClass: "!text-2xl"`). The content scan doesn't reliably generate newly-seen classes from `.md` edits, and classes inside prop values aren't extracted at all, so they silently do nothing. Reuse a class already present in a component (e.g. `bg-cream`), or use the component's own props/structure.

### Heading levels render shifted
`ProseH1` down-shifts `#` to `<h2>` on any page that has a hero (i.e. almost every page), so `#` and `##` can come out the **same visual size**. Choose levels for *semantics*; the rendered size is set by the Prose/Markdown styles, not the number of `#`.

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

## Image and Video Selection

When choosing visuals from `available-images.md`:
- Use `{locale}` suffix images (e.g., `invoice-list.{locale}.webp`) for product screenshots that should be localized
- Use static images (e.g., `chalet-sion.webp`) for decorative/atmospheric photos
- Always provide descriptive `alt` text
- Match image context to section content (e.g., expense-related sections get `expenses-list.{locale}.webp`)

**Prefer video over screenshot when an animation file exists for the topic.** Looping silent videos demonstrate workflow much more powerfully than static images. Both `hero-media` and `feature-showcase` accept the `video:` prop instead of `image:`. Confirmed working — use it freely.

```yaml
# On feature-showcase, swap image: for video: — keeps title, subtitle, and highlights:
::feature-showcase
---
label: Magic Heidi
title: "Buchhaltung, Faktura und Spesen <span>in einer App</span>"
subtitle: "Eine App für die drei Werkzeuge, die du täglich brauchst."
video:
  src: "invoice-gen.{locale}.mp4"
highlights:
  - icon: "🇨🇭"
    title: Schweizer QR Rechnung
    description: "..."
---
::
```

- On `hero-media`: `video:` is the documented prop, fullscreen video moments
- On `feature-showcase`: replace `image:` with `video:` for animated workflow demos with side-by-side highlights
- On `feature-image`: stick to images; feature-image is image-first by design

Known video assets (see `references/available-images.md` for the full list):
- `invoice-gen.{locale}.mp4` — invoice generation animation. Use on the showcase that introduces the invoicing/QR workflow (typically the "Buchhaltung, Faktura und Spesen" / "Invoicing made simple" section).

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

### Blog vs. Integration / Product-Content Article

Long-form articles split into two opener patterns. Pick the right one before mapping anything else — the rest of the structure cascades from this choice.

**Blog article** — informational, opinion, news, evergreen explainer. Source path is `drafts/...` and the destination URL is `/blog/<slug>`, or the article reads as editorial content (date and author matter). **Open with `::blog`**, which emits `Article` JSON-LD structured data and renders the title + date + author header.

**Integration / product-content article** — content-heavy commercial pages that live under `/integrations/<platform>`, `/alternative/<competitor>`, `/<feature>`, or any URL where the page functions as a long-form landing page rather than a dated blog post. **Open with `::feature-image`** (with a hero image and the article's main title in the `title:` prop). Skip `::blog` entirely — these pages don't need an article schema or a publication-date header. If you want author attribution, drop a one-sentence credit at the end of the final `::markdown` block.

Detection cues for the integration / product-content pattern:
- URL slug contains `/integrations/`, `/alternative/`, or sits at the root as a feature page (`/invoicing`, `/accounting`, etc.)
- Source frontmatter `url_slug` matches one of the above
- The article reads as evergreen "how to use Magic Heidi for X" rather than dated commentary

For both patterns, the body prose lives in `::markdown as: article` blocks (3–5 of them, split at H2 boundaries). The difference is only the opener and whether prose blocks are nested (inside `::blog`) or top-level siblings (after `::feature-image`). Structured components always come as siblings, in source order.

#### Blog Article Structure

Blog articles use the same component library as landing pages but follow a different rhythm. The page always opens with `::blog` (header + SEO structured-data wrapper). After that, the layout depends on article length.

**Short article (≤1,500 words, ≤4 H2 sections):** keep all prose inside `::blog` as nested `::markdown as: article` blocks (3–5 blocks split at H2 boundaries). Place all structured components after `::blog` closes, in source order. The reader sees prose → components — fine for a short read.

**Long pillar article (~2,000+ words, 5+ H2 sections):** interleave prose and components. Without interleaving, the reader hits a 2,500-word prose wall before the first visual break, which is brutal UX for an article this long. Pattern:

1. `::blog` opens with a single short `::markdown as: article` block containing the intro + Key Takeaways (~200–350 words). `::blog` closes.
2. A high-value structured component appears next — usually the main comparison table or feature-grid that summarises the article's central decision.
3. A top-level `::markdown as: article` block (sibling to `::blog`, NOT nested inside it) carries the next prose section.
4. Another structured component.
5. Another top-level `::markdown as: article` block.
6. ...alternating prose and components in source order until the closing CTA.

**`::blog` is single-instance per page.** It emits the `Article` JSON-LD structured data; duplicating it would create duplicate schema. Top-level `::markdown as: article` blocks after `::blog` are valid — they render article-styled prose without their own header wrapper. Use `as: article` on every prose `::markdown` block (inside or outside `::blog`) for semantic consistency.

**Markdown tables ALWAYS become `::pages-landing-comparison`.** A markdown table left in `::markdown` prose is an extraction miss. Even simple 2-column "Position | Cost" tables belong in the component — they get proper styling, mobile responsiveness, and highlight support.

Component patterns to lift out of the prose, in either layout:

1. `::feature-grid` — for any 3–6 item enumeration (indicators, signs, criteria, requirements)
2. `::feature-grid` with 1️⃣2️⃣3️⃣ icons — for numbered processes or step-by-step checklists
3. `::pages-landing-features` — for pros/cons, benefits/risks, two-category recap with bullets
4. `::pages-landing-comparison` — for any markdown table or "X vs Y" content
5. `::pages-landing-faq` — for Q&A patterns
6. `::hero-media` — for video embeds
7. `::feature-showcase` — for the soft product pitch
8. `::hero-basic{.bg-cream}` + `::hero-cta-links` — closing CTA

A page with one mega-block of `::markdown` and only an FAQ at the bottom is under-converted. Every enumeration, recap, process step, or markdown table in the prose is an opportunity to lift content into a visual component.

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

---
name: translate-components
version: 1.0.0
description: When the user wants to translate MDC component files to multiple locales, work with multilingual content, or asks about "translate," "localize," "locale," "multilingual components," or "translate to German/French/Italian/Spanish/Portuguese." For converting markdown to MDC format first, see landing-components skill.
---

# Translate Components

You are an expert multilingual content translator specializing in Swiss-market localization and native-quality SEO content adaptation. Your goal is to produce translations that read as if they were originally written in the target language — never as translations.

## Initial Assessment

Before translating, read:
1. **Source MDC file** — understand the full content, structure, and intent
2. **Locale Guidelines** — [references/locale-guidelines.md](references/locale-guidelines.md) for per-locale voice, register, and SEO rules
3. **Brand Voice** — `context/brand-voice.md` for overall tone (adapt to target locale)

---

## Core Principles

### 1. Native Quality, Not Translation
Every sentence must sound like it was written by a native speaker of the target language. Adapt idioms, restructure sentences, and use natural phrasing. A literal translation is a failed translation.

### 2. Structural Integrity
The MDC component structure is sacred. Component names, prop keys, YAML structure, indentation, image paths, and URLs must remain byte-for-byte identical. Only user-facing text values change.

### 3. Informal Address Always
All locales use informal "you":
- **de**: du/dein/dir (never Sie/Ihr/Ihnen)
- **fr**: tu/ton/ta/tes (never vous/votre/vos)
- **it**: tu/tuo/tua (never Lei/Suo/Sua)
- **es**: tú/tu/tus (never usted/su/sus)
- **pt**: você/seu/sua

### 4. SEO-Aware Headings
Titles, subtitles, and heading-level text must use natural search terms in the target language. Don't just translate — think "what would someone in this language actually search for?"

### 5. German Umlaute
For German: ALWAYS use ä, ö, ü, Ä, Ö, Ü. NEVER use ae, oe, ue substitutions.

---

## What to Translate

These are the user-facing text fields that must be translated:

### YAML Frontmatter
- `title`
- `description`

### Component Props (text values only)
- `title`
- `subtitle`
- `description`
- `label`
- `value` (when it contains text, e.g. stats like "100% konform" — but NOT pure numbers like "99.9%")
- `placeholder`
- `cta` / `ctaLabel` / `ctaText`
- `badge`
- `tagline`
- `note`

### Array Items
Within `items`, `features`, `plans`, `stats`, `links` arrays:
- `title`
- `description`
- `subtitle`
- `label`
- `value` (text-based)
- `features` (string arrays within items)
- `question` / `answer` (FAQ)

### Prose Content
- Full text inside `::markdown` component blocks
- Alt text for images (`alt` prop)

---

## What to NEVER Translate

These must remain exactly as in the source:

- **Component names**: `::pages-landing-hero-section`, `::feature-image`, etc.
- **Prop keys**: `title:`, `subtitle:`, `image:`, `orientation:`, etc.
- **Image paths**: `src: /images/invoice-list.{locale}.webp`
- **`{locale}` placeholders**: kept as-is (Nuxt resolves at render time)
- **URLs**: `/pricing`, `/start`, `https://...`
- **Brand name**: "Magic Heidi"
- **Currency codes**: CHF, EUR
- **Technical values**: `true`, `false`, `horizontal`, `dark`, `boxed`
- **Numbers**: Unless they contain translatable text around them
- **CSS classes**: Any class name references
- **HTML structure tags in strings**: `<span>`, `<br>`, `<em>`, `<strong>` — keep the tags, translate only the text within them
- **Component syntax**: `::`, `---` delimiters, indentation levels

---

## File Naming Convention

**CRITICAL**: Translated files must keep the exact same filename as the source, prefixed with the locale code and a dot. This ensures Nuxt Content locale routing works correctly.

**Pattern**: `{locale}.{source-filename}`

**Example**: If source is `buchhaltungssoftware-schweiz-2026-05-03.md`:
- French → `fr.buchhaltungssoftware-schweiz-2026-05-03.md`
- Italian → `it.buchhaltungssoftware-schweiz-2026-05-03.md`
- English → `en.buchhaltungssoftware-schweiz-2026-05-03.md`

**Do NOT** translate the filename or create a new slug for the target language. The slug must stay identical for Nuxt Content's locale-based routing to map translations to the same page.

The `page-path` prop in `::pages-landing-magic-heidi-software-schema` should use the locale prefix with the original slug: `/{locale}/original-slug` (e.g., `/fr/buchhaltungssoftware-schweiz`).

---

## Translation Process (Per Locale)

### Step 1: Copy Full Structure
Start with an exact copy of the source MDC file. This ensures nothing structural is accidentally modified.

### Step 2: Translate Frontmatter
Replace `title` and `description` values with native-language equivalents that work as meta tags (concise, keyword-rich, compelling).

### Step 3: Translate Component by Component
Go through each component block sequentially:
- Identify which props contain user-facing text
- Translate each text value in place
- For arrays, translate each item's text fields
- Preserve all YAML formatting (quotes, `|` block scalars, indentation)

### Step 4: Handle Special Cases
- **Stats with mixed content**: "100% Swiss-compliant" → translate the text, keep numbers. "4.9★" → keep as-is
- **HTML in strings**: `"<span class='text-primary-400'>Magic</span> Heidi"` → keep HTML tags, translate surrounding text only if needed
- **Compound terms**: In German, create natural compound words (Buchhaltungssoftware, not Buchhaltung Software)
- **CTA buttons**: Translate to natural action phrases ("Jetzt starten", "Commencer maintenant", not literal translations)

### Step 5: Self-Review
Before saving, verify:
- [ ] Same number of `::component-name` blocks as source
- [ ] Same number of `::` closing markers as source
- [ ] No prop keys were translated
- [ ] No URLs were modified
- [ ] No image paths were changed
- [ ] `{locale}` placeholders are untouched
- [ ] All strings that had quotes in source still have quotes
- [ ] Informal address used throughout (du/tu/tú/você)
- [ ] German text uses proper Umlaute (ä, ö, ü)

---

## Quality Standards

### What Makes a Good Translation
- Reads naturally — a native speaker would not suspect it's translated
- Uses the same persuasion techniques as the source (urgency, social proof, benefits)
- Keywords in headings are actual search terms in that language
- Maintains the same emotional tone (friendly, knowledgeable, practical)
- CTA text feels natural and action-oriented in the target language

### What Makes a Bad Translation
- Literal word-for-word translation that sounds unnatural
- Formal register (Sie/vous/Lei/usted) when informal is required
- Translated technical terms that should stay in English (API, SaaS, PDF)
- Missing Umlaute in German (ae instead of ä)
- Translated component names or prop keys
- Modified URLs or image paths

---

## Related Skills
- **landing-components** — for converting markdown to MDC format (do this first, then translate)
- **copywriting** — for creating the original marketing copy
- **seo-audit** — for verifying translated pages rank correctly

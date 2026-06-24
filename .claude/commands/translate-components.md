# Translate Components Command

Translate MDC component files in `components-ready/` to multiple locales with native-quality translations. Each language is processed by a separate agent to maintain focus and quality.

## Usage
`/translate-components [file path] [--locales de,fr,it,es,pt]`

**Examples:**
- `/translate-components components-ready/swiss-invoicing.md` (translates to all 5 locales)
- `/translate-components components-ready/swiss-invoicing.md --locales de,fr` (only German and French)
- `/translate-components components-ready/buchhaltung.de.md --locales fr,it` (German source → French + Italian)

## What This Command Does

1. Detects the source file's language
2. Renames source to `name.{source-locale}.md` if not already locale-suffixed
3. Translates to each target locale sequentially (one agent per language to avoid context overload)
4. Preserves MDC component structure exactly
5. Validates structural integrity of each translation
6. Saves translations as `name.{target-locale}.md` in the same directory

## Pre-Translation Setup

**Required — read these files before starting:**
- **Translation Skill**: `.claude/skills/translate-components/SKILL.md` — the source of truth for translation rules
- **Locale Guidelines**: `.claude/skills/translate-components/references/locale-guidelines.md` — per-locale voice and SEO rules
- **Brand Voice**: `context/brand-voice.md` — overall tone to adapt per locale

---

## Process

### Step 1: Detect Source Language

Determine the source file's language using this priority:

1. **Filename suffix**: If file is `name.de.md` or `name.fr.md`, that's the locale
2. **Frontmatter**: If YAML has a `locale:` field, use that
3. **Content heuristics**:
   - German indicators: ä, ö, ü, ß, common words (und, der, die, das, für, mit)
   - French indicators: é, è, ê, ë, ç, common words (les, des, une, avec, pour)
   - Italian indicators: common words (della, nella, sono, essere, anche)
   - Spanish indicators: ñ, ¿, ¡, common words (los, las, para, como, está)
   - Portuguese indicators: ã, õ, ç, common words (para, como, também, são)
   - English: default if no other language detected

Report detected language to user before proceeding.

### Step 2: Rename Source File

If the source file does NOT already have a locale suffix:
- Strip the date suffix if present (e.g., `-2026-05-03`)
- Rename to `slug.{source-locale}.md`
- Example: `swiss-invoicing-2026-05-03.md` → `swiss-invoicing.en.md`

If the source file already has a locale suffix, keep it as-is.

### Step 3: Determine Target Locales

**Default targets**: `de`, `fr`, `it`, `es`, `pt`
**Remove**: the source locale from the target list
**Override**: if `--locales` flag is provided, use only those locales (still removing source locale)

Before proceeding, check if any target files already exist (e.g., `slug.fr.md`). If they do, warn the user and ask whether to overwrite or skip.

### Step 4: Parallel Translation (One Agent Per Locale)

**CRITICAL**: Spawn ALL locale agents in parallel (in a single message with multiple Agent tool calls). Each agent works independently on its own locale, keeping context minimal and focused.

For each target locale, create a sub-agent (using the Agent tool) with this briefing:

```
You are translating an MDC component file to [TARGET LOCALE].

Read the translation skill at .claude/skills/translate-components/SKILL.md for complete rules.
Read the locale guidelines at .claude/skills/translate-components/references/locale-guidelines.md for [TARGET LOCALE]-specific voice.
Read the brand voice at context/brand-voice.md and adapt it to [TARGET LOCALE].

Source file: [PATH]
Target locale: [LOCALE CODE]
Output path: [OUTPUT PATH]

Key rules:
- Native quality, not literal translation
- Informal address (du/tu/tú/você) always
- [For de]: Always use proper Umlaute (ä, ö, ü) — never ae/oe/ue
- Preserve all MDC structure exactly (component names, prop keys, URLs, image paths)
- Only translate user-facing text values
- SEO-aware: headings must use natural search terms in [TARGET LANGUAGE]
- Brand name "Magic Heidi" stays untranslated
- {locale} placeholders in image paths stay as-is

Translate the file and save to [OUTPUT PATH].
After saving, verify the structural integrity:
- Same number of :: component blocks as source
- Same number of :: closing markers
- No prop keys translated
- No URLs modified
```

Launch all locale agents in parallel — they are independent and do not need to wait for each other.

### Step 5: Structural Validation

After all translations are complete, validate each output file:

1. **Component count**: Count `::component-name` lines — must match source
2. **Closing markers**: Count standalone `::` lines — must match source
3. **Frontmatter present**: Verify `title` and `description` exist in YAML
4. **No translated prop keys**: Scan for common prop keys (title:, subtitle:, description:, image:, src:, url:, orientation:) — they must be in English
5. **URLs intact**: All URLs from source appear unchanged in output
6. **Image paths intact**: All image `src` values from source appear unchanged

If validation fails for any locale, report the specific issues.

### Step 6: Report

Print a summary table:

```
## Translation Complete

Source: components-ready/swiss-invoicing.en.md (English)

| Locale | File | Status |
|--------|------|--------|
| de | swiss-invoicing.de.md | Pass |
| fr | swiss-invoicing.fr.md | Pass |
| it | swiss-invoicing.it.md | Pass |
| es | swiss-invoicing.es.md | Pass |
| pt | swiss-invoicing.pt.md | Pass |

All files saved to components-ready/
```

---

## Output

- Source (renamed): `components-ready/slug.{source-locale}.md`
- Translations: `components-ready/slug.{target-locale}.md` for each target locale

## File Management

- Source file is renamed in place (not copied) to add locale suffix
- All translations live alongside source in `components-ready/`
- No source content is deleted or modified (only renamed)
- Agent report files are NOT generated (unlike convert-to-components)

## Quality Standards

- Native-quality translation — must read as if originally written in the target language
- Informal address throughout (du/tu/tú/você — never formal)
- German always uses proper Umlaute (ä, ö, ü — never ae/oe/ue)
- All MDC structure preserved exactly (component names, prop keys, image paths, URLs)
- SEO-aware headings use natural search terms in each target language
- Brand voice adapted per locale while maintaining the "knowledgeable friend" persona
- Same persuasion techniques and emotional tone as source

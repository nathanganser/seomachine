# Publish Draft to Nuxt Content

Publishes a draft article by copying it to the mh-landing Nuxt Content directory, then deletes the original file.

## Usage
`/publish-draft [filename]`

### Examples

```
/publish-draft drafts/buchhaltungssoftware-schweiz-2026-05-03.md
/publish-draft landing-pages/belege-scannen-ki-freelancer-schweiz-2026-05-03.md
/publish-draft components-ready/invoicing.md
```

## What This Command Does

1. **Parses the draft file** — Extracts the `URL Slug` from frontmatter
2. **Extracts language and slug** — From the URL Slug field (e.g., `/de/buchhaltungssoftware-schweiz` → language=`de`, slug=`buchhaltungssoftware-schweiz`)
3. **Copies the file** to `/Users/nathanganser/Documents/Development/mh-landing/content/{language}/{slug}.md`
4. **Deletes the original** file from the seomachine directory
5. **Confirms success** — Shows the destination path

## Process

When you run this command:

### Step 1: Validate and Parse
- Confirm the draft file exists and read it
- Extract the `URL Slug` field from frontmatter (look for `URL Slug:` in the metadata, with or without `**` bold markers)
- Parse the language code from the first path segment (e.g., `de`, `en`, `fr`, `it`, `es`, `pt`)
- Parse the slug from the remaining path (e.g., `buchhaltungssoftware-schweiz`)
- If no language prefix is found in the URL Slug, ask the user which language to use
- Display the extracted language and slug for confirmation

### Step 2: Copy to Destination
- Target: `/Users/nathanganser/Documents/Development/mh-landing/content/{language}/{slug}.md`
- Verify the target language directory exists (e.g., `/Users/nathanganser/Documents/Development/mh-landing/content/de/`)
- If a file already exists at the destination, warn the user and ask before overwriting
- Copy the file using `cp`

### Step 3: Delete Original
- Delete the original markdown file from the seomachine directory using `rm`
- If from `components-ready/`, also delete associated audit reports in `audits/components/` matching the same slug
- If from `drafts/`, also delete associated report files in `drafts/_reports/` matching the same slug

### Step 4: Confirm
- Display the destination path
- Confirm the original was deleted

## URL Slug Parsing Rules

The `URL Slug` field typically looks like: `/de/buchhaltungssoftware-schweiz` or `/en/invoicing`

- Strip leading/trailing slashes
- First segment = language code (2 letters)
- Remaining segments joined = slug
- Valid languages: `de`, `en`, `fr`, `it`, `es`, `pt`

## Notes

- The file is copied as-is — no content transformation is applied
- If the URL Slug is missing, ask the user for the language and slug
- Always confirm the extracted language + slug before copying

# Pipeline Command

Orchestrates the full SEO content pipeline from research to publication. Each step runs as a **separate sub-agent** with isolated context to prevent quality degradation from context bloat.

## Usage

`/pipeline [topic] [options]`

### Options

- `--start-from [step]` — Start from a specific step: `research`, `write`, `convert`, `translate`, `publish`
- `--stop-after [step]` — Stop after a step completes (e.g., `--stop-after write`)
- `--locales [codes]` — Comma-separated locale codes for translation (default: de,fr,it,es,pt)
- `--review` — Pause between steps for user review/editing
- `--input [file]` — Provide an existing file as input (use with `--start-from`)

### Examples

```
/pipeline podcast editing software schweiz
/pipeline buchhaltungssoftware --locales de,fr --stop-after convert
/pipeline CRM software --start-from convert --input drafts/crm-software-2026-05-04.md
/pipeline podcast hosting --review
```

## Pipeline Steps

| # | Step | Reads | Produces |
|---|------|-------|----------|
| 1 | Research | Topic | `research/brief-[slug]-[date].md` |
| 2 | Write | Research brief | `drafts/[slug]-[date].md` |
| 3 | Convert | Draft file | `components-ready/[slug]-[date].md` |
| 4 | Translate | Component file | `components-ready/[slug].{locale}.md` |
| 5 | Publish | All locale files | Copied to mh-landing, source deleted |

## Execution Process

### Step 0: Parse Arguments

1. Extract the topic from the arguments (everything before `--` flags)
2. Parse options: `--start-from`, `--stop-after`, `--locales`, `--review`, `--input`
3. Derive the slug from the topic (lowercase, spaces to hyphens, strip special chars)
4. Set today's date as `YYYY-MM-DD`
5. Determine which steps to run based on `--start-from` and `--stop-after`

### Step 1: Research

**Skip if**: `--start-from` is after `research`

Spawn a sub-agent with the following prompt structure:

```
Read the file `.claude/commands/research.md` and follow its instructions exactly.

TOPIC: [topic]

When complete, report the exact output file path on a line: OUTPUT_FILE: [path]
```

After the agent completes:
- Glob for `research/brief-*{slug}*{date}*.md` to find the output file
- If not found, ask the user whether to retry or abort
- Store the path as `research_brief_path`

If `--review`: Show the user the file path and ask "Continue to Write step? (yes/edit/abort)"

If `--stop-after research`: Print summary and stop.

### Step 2: Write

**Skip if**: `--start-from` is after `write`

**Input**: `research_brief_path` from Step 1, OR `--input` file

Spawn a sub-agent with:

```
Read the file `.claude/commands/write.md` and follow its instructions exactly.

TOPIC: [topic]
RESEARCH BRIEF: [research_brief_path] (read this file for context)

When complete, report the exact output file path on a line: OUTPUT_FILE: [path]
If quality scoring fails after 2 revision attempts, report: QUALITY_FAILED: [path] [score]
```

After the agent completes:
- Glob for `drafts/*{slug}*{date}*.md` (excluding `_reports/`) to find the output
- If QUALITY_FAILED: inform user, ask whether to continue anyway / retry / abort
- Store the path as `draft_path`

If `--review`: Show file path, ask "Continue to Convert step?"

If `--stop-after write`: Print summary and stop.

### Step 3: Convert to Components

**Skip if**: `--start-from` is after `convert`

**Input**: `draft_path` from Step 2, OR `--input` file

Spawn a sub-agent with:

```
Read the file `.claude/commands/convert-to-components.md` and follow its instructions exactly.

INPUT FILE: [draft_path]

When complete, report the exact output file path on a line: OUTPUT_FILE: [path]
If quality scoring fails after 2 revision attempts, report: QUALITY_FAILED: [path] [score]
```

After the agent completes:
- Glob for `components-ready/*{slug}*{date}*.md` to find the output
- If QUALITY_FAILED: inform user, ask continue/retry/abort
- Store the path as `component_path`

If `--review`: Show file path, ask "Continue to Translate step?"

If `--stop-after convert`: Print summary and stop.

### Step 4: Translate

**Skip if**: `--start-from` is after `translate`

**Input**: `component_path` from Step 3, OR `--input` file

Spawn a sub-agent with:

```
Read the file `.claude/commands/translate-components.md` and follow its instructions exactly.

INPUT FILE: [component_path]
TARGET LOCALES: [locales from --locales flag, or default: de,fr,it,es,pt]

When complete, list all output files, one per line prefixed with OUTPUT_FILE:
```

After the agent completes:
- Glob for `components-ready/*{slug}*.{locale}.md` for each target locale
- Report which locales succeeded/failed
- If any failed: ask user whether to retry failed locales / continue / abort
- Store all paths as `locale_files`

If `--review`: Show all locale file paths, ask "Continue to Publish step?"

If `--stop-after translate`: Print summary and stop.

### Step 5: Publish

**Skip if**: `--start-from` is after `publish` (impossible, it's last)

**Input**: All files from `locale_files` + the source locale file

For each locale file, spawn a sub-agent with:

```
Read the file `.claude/commands/publish-draft.md` and follow its instructions exactly.

INPUT FILE: [locale_file_path]

When complete, report: OUTPUT_FILE: [destination path]
```

Note: Publish agents for different locales can run **in parallel** since they're independent.

After all publish agents complete:
- Verify files exist in the mh-landing content directory
- Report which succeeded/failed

## Progress Reporting

After each step, print a status update:

```
## Pipeline: "[topic]"

[done] Research → research/brief-[slug]-[date].md
[done] Write → drafts/[slug]-[date].md
[>>>]  Convert to Components...
[    ] Translate (de,fr,it,es,pt)
[    ] Publish
```

## Final Summary

When the pipeline completes (or stops early), print:

```
## Pipeline Complete

Topic: "[topic]"
Steps completed: [list]

Files produced:
- [list all output files with full paths]

Published to:
- [list destination paths in mh-landing, if publish ran]
```

## Error Recovery

- If a step fails and the user chooses to abort, print all files produced so far
- The user can resume later with `--start-from [next-step] --input [last-output-file]`
- All intermediate files remain on disk for manual inspection

# Wiki Resilience Enhancements

## Overview

7 implemented enhancements plus follow-up hardening items to make the supplements research wiki more resilient to schema drift, stale state, abandoned claims, and partial ingests.

## Implementation Plan

### 1. Lint Validator (`wiki/scripts/lint.py`)
**Status:** complete

Validates:
- Frontmatter schema mirrored from CLAUDE.md via hardcoded lint constants (type, type-specific fields, enums)
- Body wikilinks resolve to an existing page or alias
- `[!tldr]` is first content block on every page
- `[!source]` callouts include a source-summary wikilink
- Raw_hash staleness on source-summary pages
- No malformed callouts, missing TLDR, orphans, dead ends

Modes:
- Default: full validation, exit non-zero on errors
- `--staleness-only`: hash check only (for SessionStart hook)
- `--quiet`: silent unless errors (for Claude commit lint wrapper)

### 2. Claude PreToolUse and SessionStart Hooks
**Status:** complete for Claude hooks; git hook installed

Configuration in `.claude/settings.json`:
- **PreToolUse** hook on Bash: `wiki/scripts/commit_lint_hook.py` runs `wiki/scripts/lint.py --quiet` only when the command starts with `git commit`
- **SessionStart** hook: runs `wiki/scripts/lint.py --staleness-only --quiet` (prints stale sources if any, silent otherwise)

Note: `.git/hooks/pre-commit` now runs `wiki/scripts/lint.py --quiet` for commits made outside Claude in this local clone.

### 3. Drop Mirror Tag Taxonomy
**Status:** complete

Prior state: frontmatter fields (`practical_status`, `evidence_level`, `translational_status`) were duplicated as tags (`decision/*`, `evidence/level-*`, `stream/*`).

Action: Remove mirror tags from CLAUDE.md tag taxonomy. Keep semantic tags (supplement/, pathway/, outcome/, condition/, process/, risk-domain/, population/, gene/, variant/, genotype/) which carry information frontmatter does not.

Rationale: frontmatter is single source of truth; tags provide secondary navigation only.

### 4. Age the Promotion Queue
**Status:** complete

Add `marked: YYYY-MM-DD` to promotion-queue entries.

Updates:
- CLAUDE.md: document `marked` convention
- wiki/sources/promotion-queue.md: update table template to include `marked` column
- wiki/lint-rules.md: add rule "entries marked >30 days surface in research-backlog"

`wiki/research-backlog.md` uses DataviewJS to surface open promotion-queue rows whose `Marked` date is >30 days old. This is implemented there instead of in `wiki/Research Backlog.base` because Bases operate on files/frontmatter, not Markdown table rows.

### 5. Make Ingest Idempotent and Resumable
**Status:** complete

Add `ingest_status: in-progress | complete` to source-summary frontmatter spec.

Updates:
- CLAUDE.md: add field to source-summary frontmatter section
- .claude/skills/wiki-ingest/SKILL.md: 
  - Extractor creates source-summary with `ingest_status: in-progress`
  - Orchestrator flips to `ingest_status: complete` after the audit gap report is appended
  - Step 1 detects if source-summary exists with status `in-progress` and offers to resume or restart

Benefit: partial ingests recover cleanly; no stuck wiki state.

### 6. Document Calibration Sweep Protocol
**Status:** complete

Write `wiki/docs/calibration-sweep.md`:
- When: monthly or after new sources land
- What: read each `[!analysis]` callout, search for new sources on the same supplement/pathway since callout date
- How: append `> **[YYYY-MM-DD update]:** Confirmed/Contradicted by [[Source]]` below the original callout
- Outcome: builds a track record of which inferences hold up

Note: defer actual scheduled agent until first ingest creates real `[!analysis]` callouts.

### 7. Document Schema Canary Protocol
**Status:** complete

Write `wiki/docs/schema-canary.md`:
- Designate **sulforaphane** as schema canary on first ingest
- After any CLAUDE.md schema change, re-run lint against canary pages
- Any new failures block the schema change until resolved
- Benefit: schema changes validated against real content

## Task Status

- [x] Write wiki/scripts/lint.py validator
- [x] Add Claude PreToolUse commit lint wrapper and SessionStart hook in `.claude/settings.json`
- [x] Drop mirror tag taxonomy from CLAUDE.md
- [x] Age the promotion queue (CLAUDE.md, promotion-queue.md, lint-rules.md)
- [x] Make ingest idempotent (CLAUDE.md, wiki-ingest SKILL.md)
- [x] Document calibration sweep protocol
- [x] Document schema canary protocol

## Follow-Up Hardening

- [x] Extend `wiki/scripts/lint.py` to validate wikilinks stored in frontmatter fields such as `sources`, `primary_outcomes`, `primary_pathways`, `primary_genetics`, `subjects`, `supplements`, `pathways`, and `outcomes`.
- [x] Decide whether to install a real `.git/hooks/pre-commit` wrapper so lint also runs for commits made outside Claude.
- [x] Reduce schema drift risk between `CLAUDE.md` and `wiki/scripts/lint.py` by adding a schema-sync check or moving enum/source-of-truth data into a shared machine-readable file.
- [x] Fix template examples that intentionally contain placeholder `[!source]` callouts without source-summary wikilinks, or make lint ignore template placeholders explicitly.

## Notes

- All changes are reversible (no data loss).
- Lint validator is pure Python stdlib — no external dependencies.
- Wiki has zero content, so schema changes have no migration cost.
- Hooks are configured in `.claude/settings.json`.
- `python3 wiki/scripts/lint.py` passes on the current scaffold.
- Current lint validates frontmatter wikilinks for source, supplement, pathway, outcome, genetics, and comparison relationship fields.
- A tracked `.githooks/pre-commit` wrapper is available, and this clone is configured with `core.hooksPath=.githooks` so non-Claude commits run `wiki/scripts/lint.py --quiet`.
- First ingest will be the real test of schema resilience — expect 1-2 small revisions.

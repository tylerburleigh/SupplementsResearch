---
name: wiki-repair
description: Make a scoped corrective edit to existing supplement wiki pages when the problem is already known. Use for audit findings, attribution mismatches, broken source links, stale status fields, scope qualifiers, metadata drift, or other narrow page issues that do not require a full re-ingest. Does not commit to git.
---

# wiki-repair

Use this skill for narrow, auditable corrections. Repair is not a
re-ingest and not a broad health check.

## When to Invoke

- The user says `$wiki-repair ...`, "fix this audit finding", or "repair
  this page issue".
- A lint or audit pass surfaced a specific problem and the user wants it
  corrected.
- The problem is localized: bad attribution, missing caveat, broken
  wikilink, wrong frontmatter value, stale status, or missing source
  summary in `sources:`.

Do not use repair for a changed source that needs extraction. Route that
to `wiki-ingest`.

## Steps

### 1. Read Context

- Read `wiki/handoff.md`.
- Read `CLAUDE.md`, especially claim typing, source-role provenance, and
  the relevant frontmatter fields.
- Read `wiki/docs/graph-protocol.md` if the repair touches links,
  bidirectionality, or relationship frontmatter.
- Read the affected page.
- If the problem is source-grounded, read the cited source-summary page
  and the `raw_path` / `research/.../report.md` source when needed.

### 2. Bound the Repair

Before editing, state:

1. Which files you will touch.
2. The exact defect you are fixing.
3. Why this is a repair rather than a re-ingest.

If the scope expands into "this source needs to be re-extracted", stop.

### 3. Patch Narrowly

Apply the smallest defensible edit:

- Fix `[!source]`, `[!analysis]`, `[!unverified]`, or `[!gap]` typing.
- Restore missing scope qualifiers, population boundaries, dose/form
  constraints, or safety caveats from the source.
- Add missing source-summary wikilinks to callouts and `sources:`.
- Correct frontmatter values, relationship links, tags, status, or
  `updated:`.
- Preserve source-role rules: decision-critical claims need a
  non-synthesis anchor or must stay `[!unverified]` / `[!gap]`.

Do not opportunistically rewrite adjacent sections.

### 4. Update Bookkeeping

When a repair changes wiki state:

- Set `updated:` to today on edited pages.
- Rebuild `wiki/catalog.md` with:

```bash
python3 wiki/scripts/lint.py --rebuild-catalog
```

- Append `wiki/log.md`:
  `### [YYYY-MM-DD] repair | <short description>`
- Update `wiki/handoff.md` if the repair leaves follow-up work.
- Revise `wiki/synthesis.md` only if the correction changes the wiki's
  overall practical conclusions.

Do not edit `wiki/index.md` or `wiki/research-backlog.md`; they are
DataView-driven. Edit `wiki/research-queue.md` only when the repair
resolves, defers, or re-scopes a specific queue row.

### 5. Close Out

Summarize:

- Files changed.
- What was corrected.
- Whether the fix was source-grounded or structural.
- Whether catalog/log/synthesis/handoff were updated.
- Whether `python3 wiki/scripts/lint.py` passes.

Do not commit to git.

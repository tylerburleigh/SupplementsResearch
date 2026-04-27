---
name: wiki-query
description: Answer substantive questions from the supplements wiki and optionally file reusable answers into wiki/queries. Use for practical supplement questions, comparisons, stack decisions, evidence questions, mechanism questions, safety checks, and "what does the wiki say about..." prompts. Does not commit to git.
---

# wiki-query

Use this skill when the user asks a substantive question that should be
answered from the accumulated wiki, not from a fresh web search.

## Principles

- The wiki is the source of truth for what has already been ingested.
- Preserve claim typing in the answer: sourced claims, analysis,
  uncertainty, and gaps stay distinct.
- Do not repair pages during query work. Surface repair candidates and
  route them to `/wiki-repair`.
- File durable answers when they are likely to be reused.

## Steps

### 1. Read Context

- Read `wiki/handoff.md`.
- Read `purpose.md`.
- Read `wiki/synthesis.md`.
- Read `wiki/queries/README.md`.
- Read `wiki/catalog.md` if present; otherwise read `wiki/index.md`.

### 2. Plan the Read

Identify the likely page set:

- Supplement entity pages for direct supplement questions.
- Concept pages for pathways, outcomes, conditions, biomarkers,
  populations, or genetics.
- Hypothesis pages for supplement -> pathway -> outcome claims.
- Source-summary pages for provenance and evidence details.
- `wiki/interactions.md`, `wiki/Quick Reference Dosing.md`, or
  `wiki/comparisons/` for practical decisions.

Read only the relevant pages first, then follow wikilinks as needed.

### 3. Answer With Provenance

In the answer:

- Cite wiki pages by wikilink or path.
- Distinguish direct source-backed claims from analysis.
- Preserve evidence streams: mechanistic, animal, human, genetics.
- Preserve source-role limits: report-derived synthesis is useful, but
  decision-critical claims need non-synthesis anchors.
- Surface gaps and contradictions rather than smoothing them over.

### 4. Decide Whether To File

File a durable query page when the answer is:

- A recurring practical question.
- A supplement comparison or stack decision.
- A decision-relevant synthesis across multiple pages.
- A useful map of evidence, gaps, or contradictions.

Do not file one-off lookups or answers that only restate one page.

When in doubt, ask once: "File this as a query page?"

### 5. If Filing, Write The Page

Create a page under `wiki/queries/` with `type: query` unless the answer is
better represented as a `comparison`, `hypothesis`, `stack`, `decision`, or `dosing`
page under the corresponding directory.

For a `type: query` page:

- Include full frontmatter, source-summary links in `sources:`, and `> [!tldr]`.
- Cite the wiki pages and source summaries used. If the answer only cites
  wiki pages, follow those pages back to their source summaries and include
  the source-summary links in `sources:`.
- Preserve claim typing in the body.
- Link out to the key entity, concept, hypothesis, comparison, dosing, or
  source-summary pages used. Query pages are reached through
  `wiki/queries/README.md`, DataView, and `wiki/catalog.md`, but they should
  not be dead ends.

After filing:

- Rebuild `wiki/catalog.md`:

```bash
python3 wiki/scripts/lint.py --rebuild-catalog
```

- Append `wiki/log.md`:
  `### [YYYY-MM-DD] query | <one-line question framing>`
- Update `wiki/handoff.md` if the query creates follow-up work.
- Revise `wiki/synthesis.md` only if the answer changes the top-level
  practical story.

Do not edit `wiki/index.md`; it is DataView-driven.

### 6. Present To User

Return:

- The answer, with page citations.
- Any stale/gap/provenance issues noticed.
- If filed: page path, TLDR, catalog rebuild status, and log entry.

Do not commit to git.

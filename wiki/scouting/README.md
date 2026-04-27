---
type: meta
sources: []
created: "2026-04-19"
updated: "2026-04-19"
status: current
tags:
  - meta
---

> [!tldr]
> Preliminary scouting briefs — quick evidence assessments before committing to deep research. These are NOT part of the main wiki and should not be cited as sources.

## Purpose

This directory holds lightweight scouting briefs produced by the `/scout` skill. They are:

- **Preliminary** — based on 5-10 minutes of targeted search, not comprehensive analysis
- **Siloed** — kept separate from the main wiki to prevent unvetted claims from mixing with ingested knowledge
- **Action-oriented** — each brief includes a recommendation on whether to proceed with deep research

## Lifecycle

| Status | Meaning |
|--------|---------|
| `preliminary` | Active scouting brief, not yet acted on |
| `superseded` | Deep research completed; this brief is replaced by `research/<supplement>/report.md` |
| `dead-end` | No credible evidence found; not worth further investigation |
| `deprioritized` | Low promise; may revisit later |

## All Scouting Briefs

```dataview
TABLE WITHOUT ID
  file.link AS "Supplement",
  status AS "Status",
  updated AS "Scouted"
FROM "wiki/scouting"
WHERE file.name != "README"
SORT updated DESC
```

## Promotion Path

Scouting briefs do not get ingested into the main wiki. They inform deep-research queries. After deep research completes, the scouting brief is marked `superseded` and the full research report flows through `/wiki-ingest` into the wiki.

```
/scout <supplement> → wiki/scouting/<Supplement>.md
  → (if promising) → foundry-research deep-research → research/<supplement>/report.md
    → /wiki-ingest <supplement> → wiki/entities/, wiki/concepts/, etc.
```

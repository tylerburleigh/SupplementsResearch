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
> Active disagreements across the wiki — contradicted or nuanced hypotheses and source-level disputes.

## Hypothesis-Level Debates

Hypotheses with status `nuanced` or `contradicted`, ranked by evidence level:

```dataview
TABLE hypothesis_status AS "Status", evidence_level AS "Evidence", supplements AS "Supplements", outcomes AS "Outcomes"
FROM "wiki/hypotheses"
WHERE hypothesis_status = "nuanced" OR hypothesis_status = "contradicted"
SORT evidence_level DESC
```

## Source-Level Disagreements

Manual log of cases where sources directly contradict each other, before a hypothesis page exists.
Format: brief description + links to affected pages and sources.

<!-- append entries below using obsidian append -->

---
type: concept
concept_type: meta
sources: []
created: "2026-04-19"
updated: "2026-04-19"
status: current
tags:
  - meta
---

> [!tldr]
> Cross-reference of all known supplement-supplement and supplement-drug interactions across the wiki.

## Known Interactions

<!-- This section is manually maintained. During ingest, add new interactions here. -->
<!-- Format: - [[Supplement A]] + [[Supplement B]]: interaction description. [[source]] -->

*No interactions logged yet. Populated during ingest.*

## Interaction Sources by Entity

```dataview
TABLE WITHOUT ID
  file.link AS "Supplement",
  filter(file.outlinks, (x) => contains(meta(x).tags, "supplement/")) AS "Interacts With"
FROM "wiki/entities"
WHERE entity_type = "supplement"
SORT file.name ASC
```

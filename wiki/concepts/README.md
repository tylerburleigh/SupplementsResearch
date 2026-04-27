---
type: meta
sources: []
created: "2026-04-19"
updated: "2026-04-26"
status: current
tags:
  - meta
---

> [!tldr]
> Concept pages — pathways, pathway families, outcomes, conditions, biomarkers, biological processes, risk domains, populations, genes, variants, and genotypes.

## Contents

```dataview
TABLE concept_type AS "Type", domain AS "Domain", length(sources) AS "Sources", updated AS "Updated"
FROM "wiki/concepts"
WHERE type = "concept"
SORT file.name ASC
```

See also: [[index]], [[taxonomy]]

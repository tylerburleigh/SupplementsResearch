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
> Head-to-head supplement comparisons. Each page uses the `comparison` template with a `subjects` list.

## Contents

```dataview
TABLE subjects AS "Subjects", length(sources) AS "Sources", updated AS "Updated"
FROM "wiki/comparisons"
WHERE type = "comparison"
SORT file.name ASC
```

See also: [[index]], [[taxonomy]]

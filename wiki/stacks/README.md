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
> Supplementation stack configurations — combinations of supplements with a shared goal and rationale.

## Contents

```dataview
TABLE goal AS "Goal", supplements AS "Supplements", updated AS "Updated"
FROM "wiki/stacks"
WHERE type = "stack"
SORT file.name ASC
```

See also: [[index]], [[interactions]], [[synthesis]]

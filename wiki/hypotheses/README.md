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
> Hypothesis pages — testable claims connecting supplements to mechanisms, populations, outcomes, conditions, and risk domains.

## Contents

```dataview
TABLE hypothesis_status AS "Status", translational_status AS "Translational Status", effect_direction AS "Direction", population AS "Population", genetic_context AS "Genetics", evidence_level AS "Evidence", supplements AS "Supplements", outcomes AS "Outcomes"
FROM "wiki/hypotheses"
WHERE type = "hypothesis"
SORT evidence_level DESC
```

See also: [[index]], [[debates]], [[research-backlog]]

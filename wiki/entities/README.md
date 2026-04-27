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
> Entity pages — supplements, compounds, brands, and delivery forms. One page per entity, linked via wikilinks.

## Contents

```dataview
TABLE entity_type AS "Type", practical_status AS "Practical Status", translational_status AS "Translational Status", evidence_level AS "Evidence", mechanistic_evidence AS "Mechanistic", animal_evidence AS "Animal", human_evidence AS "Human", primary_outcomes AS "Primary Outcomes", primary_genetics AS "Genetics", length(sources) AS "Sources", updated AS "Updated"
FROM "wiki/entities"
WHERE type = "entity"
SORT file.name ASC
```

See also: [[index]], [[taxonomy]], [[Quick Reference Dosing]]

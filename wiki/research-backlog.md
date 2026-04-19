---
type: concept
concept_type: "meta"
sources: []
created: "2026-04-19"
updated: "2026-04-19"
status: current
tags:
  - meta
---

> [!tldr]
> Aggregated view of all open questions and research gaps across the wiki.

## All Open Gaps

```dataview
TABLE file.folder AS "Page", file.tags AS "Tags"
FROM "wiki"
WHERE contains(file.tags, "open-question")
SORT file.name ASC
```

## Supplements by Evidence Level

```dataview
TABLE evidence_level AS "Highest Evidence", length(sources) AS "Sources"
FROM "wiki/entities"
WHERE entity_type = "supplement"
SORT evidence_level DESC
```

## Open Hypotheses

```dataview
TABLE hypothesis_status AS "Status", evidence_level AS "Evidence Level", supplements AS "Supplements", outcomes AS "Outcomes"
FROM "wiki/hypotheses"
WHERE hypothesis_status = "open"
SORT evidence_level DESC
```

## Thinly-Sourced Pages

```dataview
TABLE length(sources) AS "Source Count"
FROM "wiki/entities" OR "wiki/concepts" OR "wiki/hypotheses"
WHERE length(sources) < 2
SORT length(sources) ASC
```

## Stale Pages

```dataview
TABLE updated AS "Last Updated", date(today) - date(updated) AS "Days Since Update"
FROM "wiki/entities" OR "wiki/concepts" OR "wiki/hypotheses"
WHERE date(today) - date(updated) > dur(30 days)
SORT updated ASC
```

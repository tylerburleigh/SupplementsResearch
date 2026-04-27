---
type: meta
sources: []
created: "2026-04-19"
updated: "2026-04-26"
status: current
tags:
  - meta
  - open-question
---

> [!tldr]
> Aggregated view of all open questions and research gaps across the wiki.

See also: [[index]], [[lint-rules]], [[debates]], [[synthesis]]

## All Open Gaps

```dataview
TABLE file.folder AS "Page", file.tags AS "Tags"
FROM "wiki"
WHERE contains(file.tags, "#open-question")
SORT file.name ASC
```

## Supplements by Evidence Level

```dataview
TABLE evidence_level AS "Highest Evidence", translational_status AS "Translational Status", mechanistic_evidence AS "Mechanistic", animal_evidence AS "Animal", human_evidence AS "Human", practical_status AS "Practical Status", primary_outcomes AS "Primary Outcomes", length(sources) AS "Sources"
FROM "wiki/entities"
WHERE entity_type = "supplement"
SORT evidence_level DESC
```

## Open Hypotheses

```dataview
TABLE hypothesis_status AS "Status", translational_status AS "Translational Status", effect_direction AS "Direction", population AS "Population", genetic_context AS "Genetics", evidence_level AS "Evidence Level", supplements AS "Supplements", outcomes AS "Outcomes"
FROM "wiki/hypotheses"
WHERE hypothesis_status = "open"
SORT evidence_level DESC
```

## Mechanism-Led Open Questions

```dataview
TABLE mechanistic_evidence AS "Mechanistic", animal_evidence AS "Animal", human_evidence AS "Human", practical_status AS "Practical Status", primary_outcomes AS "Primary Outcomes"
FROM "wiki/entities"
WHERE translational_status = "mechanism-led"
SORT human_evidence ASC, file.name ASC
```

## Research-Only or Deprioritized Supplements

```dataview
TABLE practical_status AS "Practical Status", translational_status AS "Translational Status", evidence_level AS "Evidence", primary_outcomes AS "Primary Outcomes", length(sources) AS "Sources"
FROM "wiki/entities"
WHERE entity_type = "supplement" AND contains(list("research-only", "deprioritize"), practical_status)
SORT practical_status ASC, evidence_level DESC
```

## Thinly-Sourced Pages

```dataview
TABLE length(sources) AS "Source Count"
FROM "wiki/entities" OR "wiki/concepts" OR "wiki/hypotheses"
WHERE type != "meta" AND length(sources) < 2
SORT length(sources) ASC
```

## Stale Pages

```dataview
TABLE updated AS "Last Updated", date(today) - date(updated) AS "Days Since Update"
FROM "wiki/entities" OR "wiki/concepts" OR "wiki/hypotheses"
WHERE type != "meta" AND date(today) - date(updated) > dur(30 days)
SORT updated ASC
```

## Stale Sources (Hash Mismatch)

<!-- The lint pass checks raw_hash on source-summary pages against the actual file.
     If a source file is updated in raw/ or research/ without re-ingesting, the hash
     becomes stale. Run the lint skill to populate this section. -->

> [!gap]
> - [ ] No staleness checks run yet. Run `/lint` to audit source hashes.

## Promotion Queue Aging

```dataviewjs
const path = "wiki/sources/promotion-queue.md";
const text = await dv.io.load(path);
const rows = text
  .split("\n")
  .filter(line => line.startsWith("|") && !line.includes("---") && !line.includes("Claim | Target Page"));

const today = dv.date("today");
const overdue = rows
  .map(line => line.split("|").slice(1, -1).map(cell => cell.trim()))
  .filter(cells => cells.length >= 9 && cells[0])
  .map(cells => ({
    claim: cells[0],
    target: cells[1],
    priority: cells[5],
    reason: cells[6],
    marked: dv.date(cells[7]),
    status: cells[8]
  }))
  .filter(row => row.marked && row.status === "open" && today.diff(row.marked, "days").days > 30);

dv.table(
  ["Claim", "Target", "Priority", "Reason", "Marked", "Age"],
  overdue.map(row => [
    row.claim,
    row.target,
    row.priority,
    row.reason,
    row.marked.toISODate(),
    `${Math.floor(today.diff(row.marked, "days").days)} days`
  ])
);
```

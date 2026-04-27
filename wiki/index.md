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
> DataView-driven catalog of wiki supplements, concepts, hypotheses, comparisons, stacks, dosing pages, sources, and open questions.

# Wiki Index

See also: [[Evidence Map]], [[Supplements Database]], [[Hypotheses Tracker]], [[Outcomes Dashboard]], [[Pathways Dashboard]]

## Supplements

```dataview
TABLE entity_type AS "Type", practical_status AS "Practical Status", translational_status AS "Translational Status", evidence_level AS "Evidence", mechanistic_evidence AS "Mechanistic", animal_evidence AS "Animal", human_evidence AS "Human", primary_outcomes AS "Primary Outcomes", length(sources) AS "Sources"
FROM "wiki/entities"
WHERE entity_type = "supplement"
SORT file.name ASC
```

## Pathways

```dataview
TABLE concept_type AS "Type", domain AS "Domain", length(sources) AS "Sources"
FROM "wiki/concepts"
WHERE contains(list("pathway", "pathway-family", "process"), concept_type)
SORT file.name ASC
```

## Outcomes Conditions Risk Domains

```dataview
TABLE concept_type AS "Type", domain AS "Domain", length(sources) AS "Sources"
FROM "wiki/concepts"
WHERE contains(list("outcome", "condition", "risk-domain", "gene", "genetic-variant", "genotype", "pharmacogenomic-marker"), concept_type)
SORT file.name ASC
```

## Hypotheses

```dataview
TABLE hypothesis_status AS "Status", translational_status AS "Translational Status", effect_direction AS "Direction", population AS "Population", genetic_context AS "Genetics", evidence_level AS "Evidence", length(sources) AS "Sources"
FROM "wiki/hypotheses"
WHERE type = "hypothesis"
SORT evidence_level DESC
```

## Mechanism-Led Candidates

```dataview
TABLE practical_status AS "Practical Status", mechanistic_evidence AS "Mechanistic", animal_evidence AS "Animal", human_evidence AS "Human", primary_outcomes AS "Primary Outcomes"
FROM "wiki/entities"
WHERE translational_status = "mechanism-led"
SORT file.name ASC
```

## Comparisons

```dataview
TABLE subjects AS "Subjects", length(sources) AS "Sources"
FROM "wiki/comparisons"
WHERE type = "comparison"
SORT file.name ASC
```

## Stacks

```dataview
TABLE goal AS "Goal", length(supplements) AS "Supplements"
FROM "wiki/stacks"
WHERE type = "stack"
SORT file.name ASC
```

## Dosing Pages

```dataview
TABLE supplement AS "Supplement", length(sources) AS "Sources", updated AS "Updated"
FROM "wiki/dosing"
WHERE type = "dosing"
SORT file.name ASC
```

## Sources

```dataview
TABLE study_type AS "Study Type", source_role AS "Role", ingest_status AS "Ingest Status", evidence_layer AS "Evidence Layer", reading_status AS "Read", decision_relevance AS "Decision Relevance", anchor_for AS "Anchors", raw_path AS "Source File"
FROM "wiki/sources"
WHERE type = "source-summary"
SORT created DESC
```

See also: [[promotion-queue]]

## Open Questions

```dataview
TABLE file.folder AS "Location"
FROM "wiki"
WHERE contains(file.tags, "#open-question")
SORT file.name ASC
```

# Wiki Index

## Supplements

```dataview
TABLE entity_type AS "Type", length(sources) AS "Sources"
FROM "wiki/entities"
WHERE entity_type = "supplement"
SORT file.name ASC
```

## Pathways

```dataview
TABLE length(sources) AS "Sources"
FROM "wiki/concepts"
WHERE concept_type = "pathway"
SORT file.name ASC
```

## Outcomes

```dataview
TABLE length(sources) AS "Sources"
FROM "wiki/concepts"
WHERE concept_type = "outcome"
SORT file.name ASC
```

## Hypotheses

```dataview
TABLE hypothesis_status AS "Status", evidence_level AS "Evidence", length(sources) AS "Sources"
FROM "wiki/hypotheses"
SORT evidence_level DESC
```

## Comparisons

```dataview
TABLE subjects AS "Subjects", length(sources) AS "Sources"
FROM "wiki/comparisons"
SORT file.name ASC
```

## Stacks

```dataview
TABLE goal AS "Goal", length(supplements) AS "Supplements"
FROM "wiki/stacks"
SORT file.name ASC
```

## Sources

```dataview
TABLE length(sources) AS "Derived From"
FROM "wiki/sources"
SORT created DESC
```

## Open Questions

```dataview
TABLE file.folder AS "Location"
FROM "wiki"
WHERE contains(file.tags, "open-question")
SORT file.name ASC
```

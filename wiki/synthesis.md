---
type: meta
sources: []
created: "2026-04-18"
updated: "2026-04-29"
status: current
tags:
  - meta
  - open-question
---

> [!tldr]
> Front door for the supplements wiki: current conclusions, practical posture, common question routes, and deeper catalog links.

# Synthesis

## Current State

> [!analysis]
> The wiki scaffold is ready, but no supplement entity pages have been formally ingested yet. Treat the current pages as navigation and research infrastructure, not as supplement recommendations.

## Start by Intent

| If you want to... | Start here | Then go deeper with... |
|-------------------|------------|------------------------|
| See the current best answer | This page | [[Evidence Map]], [[index]] |
| Decide whether a supplement belongs in a stack | This page | Entity pages, [[Quick Reference Dosing]], [[interactions]] |
| Check dose, form, timing, or population fit | [[Quick Reference Dosing]] | Dosing pages, entity dosing sections |
| Ask a recurring practical question | [[queries/README|Common Questions]] | Answered query pages |
| Compare alternatives | [[comparisons/README|Comparisons]] | Entity pages and source summaries |
| Check safety or conflicts | [[interactions]] | Entity safety sections, source summaries |
| Choose what to research next | [[research-queue]] | [[research-backlog]], `research-priority.md`, [[sources/promotion-queue|promotion-queue]] |
| Track future evidence or review events | [[evidence-watch]] | Hypothesis pages and practical decision notes |
| Record or revisit a stack decision | Practical decision pages in `wiki/decisions/` | Entity pages, dosing pages, [[interactions]], stack pages |
| Browse the full knowledge base | [[index]] | [[catalog]], Bases dashboards, and directory README pages |

## Practical Posture

These views should become the first decision surface once supplements are ingested.

### Worth Considering

```dataview
TABLE practical_status AS "Practical Status", evidence_level AS "Evidence", translational_status AS "Translational Status", translation_plausibility AS "Translation", replication_status AS "Replication", claim_scope AS "Claim Scope", primary_outcomes AS "Primary Outcomes", updated AS "Updated"
FROM "wiki/entities"
WHERE entity_type = "supplement" AND contains(list("candidate", "consider"), practical_status)
SORT practical_status ASC, evidence_level DESC, file.name ASC
```

### Avoid or Deprioritize

```dataview
TABLE practical_status AS "Practical Status", evidence_level AS "Evidence", human_evidence AS "Human Evidence", translation_plausibility AS "Translation", replication_status AS "Replication", claim_scope AS "Claim Scope", primary_outcomes AS "Primary Outcomes", updated AS "Updated"
FROM "wiki/entities"
WHERE entity_type = "supplement" AND contains(list("avoid", "deprioritize"), practical_status)
SORT practical_status ASC, file.name ASC
```

### Research-Only

```dataview
TABLE translational_status AS "Translational Status", translation_plausibility AS "Translation", replication_status AS "Replication", claim_scope AS "Claim Scope", mechanistic_evidence AS "Mechanistic", animal_evidence AS "Animal", human_evidence AS "Human", primary_outcomes AS "Primary Outcomes", updated AS "Updated"
FROM "wiki/entities"
WHERE entity_type = "supplement" AND practical_status = "research-only"
SORT translational_status ASC, file.name ASC
```

## Strongest Evidence

> [!gap]
> - [ ] No supplements ingested yet. Populate after first ingest.

## Active Debates

See [[debates]] for detail.

> [!gap]
> - [ ] No debates logged yet.

## Best-Guess Stack

> [!gap]
> - [ ] No stack recommendation yet. Will develop as supplements are researched.

## Priority Gaps

> [!gap]
> - [ ] No supplements ingested yet — gaps will surface during ingest.

## Deeper Maps

- [[Evidence Map]] - practical status, evidence level, population scope, genetics context, and translational status across entities, concepts, and hypotheses.
- [[Supplements Database]] - supplement-only dashboard grouped by evidence, practical status, and translational status.
- [[Hypotheses Tracker]] - open, supported, nuanced, and contradicted supplement-to-outcome claims.
- [[Decisions]] - practical decision dashboard; structural decisions are logged in [[decisions]].
- [[queries/README|Common Questions]] - user-facing questions that should become durable answer pages.
- [[research-queue]] - ID-based queue for content gaps and unverified claims.
- [[evidence-watch]] - future evidence and review events that should trigger updates.
- [[index]] - exhaustive DataView catalog of entities, concepts, hypotheses, comparisons, stacks, dosing pages, sources, and open questions.
- [[catalog]] - static markdown catalog for agents and shell-only sessions.

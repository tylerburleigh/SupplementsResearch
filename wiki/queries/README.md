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
> User-facing question hub for practical supplement decisions; durable answers are filed as individual query pages.

## How This Works

Use this page when the user arrives with a practical question rather than a supplement name, pathway, or source. When a question is answered using wiki knowledge - especially if it synthesizes multiple pages or would take significant reconstruction - file it as a query page in `wiki/queries/`. This page tracks the questions; the linked pages hold the answers.

## Question Routes

| User intent | Typical answer should pull from |
|-------------|---------------------------------|
| What should I take for a goal? | [[synthesis]], entity Decision Snapshots, [[Evidence Map]], stack pages |
| What should I avoid? | [[interactions]], entity Safety Profile sections, [[debates]], contradicted hypotheses |
| What dose or form should I use? | [[Quick Reference Dosing]], dosing pages, source summaries with `source_role: dosing` |
| Which option is better? | Comparison pages, entity Evidence by Outcome sections, source summaries |
| What should be researched next? | [[research-backlog]], `research-priority.md`, [[sources/promotion-queue|promotion-queue]] |

## Active Questions

<!-- Add questions here as they arise. Link to the query page once answered. -->

> [!gap] Decision questions
> - [ ] What is the minimal effective longevity stack?
> - [ ] Which supplements have the best evidence for all-cause mortality reduction?
> - [ ] What supplements should I avoid together?

> [!gap] Outcome questions
> - [ ] What should I take for cognitive health?
> - [ ] What should I take for cardiovascular health?

> [!gap] Use and storage questions
> - [ ] Which supplements lose potency over time or need special storage?

## Answered Queries

```dataview
TABLE WITHOUT ID
  file.link AS "Question",
  updated AS "Answered",
  length(sources) AS "Sources"
FROM "wiki/queries"
WHERE file.name != "README"
SORT updated DESC
```

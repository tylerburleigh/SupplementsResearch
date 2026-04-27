---
type: meta
sources: []
created: "{{date}}"
updated: "{{date}}"
status: current
review_period: ""  # weekly | monthly | quarterly
tags:
  - meta
---

> [!tldr]
> Periodic review of wiki health, evidence changes, research queue, and practical decision posture.

# {{review_period}} Review - {{date}}

## Briefing

Paste or summarize `python3 wiki/scripts/briefing.py`.

## Lint

Run `python3 wiki/scripts/lint.py` and summarize errors or warnings.

## Research Queue

Run `python3 wiki/scripts/backlog_sync.py`. Note new queue items, overdue items, and items resolved during this review.

## Evidence Watch

Review [[evidence-watch]] for overdue or upcoming events. Move evaluated rows when the target page has been updated.

## Hypothesis Review

Check open hypotheses with `review_by` dates due before the next review.

## Practical Decisions

Review active `type: decision` pages whose `review_by` date has passed. Close, supersede, or defer with a note.

## Synthesis Update

Note whether [[synthesis]], [[Quick Reference Dosing]], [[interactions]], or stack pages need updates.

## Action Items

- [ ]

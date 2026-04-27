---
type: meta
sources: []
created: "2026-04-26"
updated: "2026-04-26"
status: current
tags:
  - meta
---

> [!tldr]
> Protocol for checking whether prior wiki analyses held up after new sources arrive.

# Calibration Sweep

## When

Run a sweep monthly, after a major ingest, or before using an older `[!analysis]` callout to support a practical decision.

## Scope

Review each `[!analysis]` callout on supplement entity, concept, hypothesis, comparison, stack, dosing, and query pages. Prioritize analyses that affect practical status, dosing, safety, interactions, hypothesis status, or stack inclusion.

## Method

1. Record the callout page, heading, and analysis text.
2. Search for newer sources on the same supplement, pathway, population, outcome, safety issue, or genetics context.
3. Prefer primary anchors, systematic reviews, meta-analyses, regulatory guidance, or full-text safety sources over broad synthesis.
4. If the new source changes confidence, create or update the relevant source-summary page before changing the analysis trail.
5. Append a dated update directly below the original callout:

```markdown
> [!analysis] Original inference with reasoning.
> **[YYYY-MM-DD update]:** Confirmed by [[Source]]. / Contradicted by [[Source]]. / Narrowed by [[Source]].
```

## Outcomes

- Confirmed: the newer source supports the original inference without materially changing scope.
- Contradicted: the newer source reverses the direction, weakens the claim below decision relevance, or reveals a safety blocker.
- Narrowed: the newer source preserves the inference only for a specific population, dose, form, genotype, or outcome.
- Still open: no adequate source was found; leave the analysis unchanged and add a `[!gap]` if the uncertainty blocks a decision.

## Logging

Append a `calibration-sweep` entry to `wiki/log.md`. If a sweep changes a structural decision, add a decision entry to `wiki/decisions.md`.

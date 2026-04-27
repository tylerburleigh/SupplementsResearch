---
type: hypothesis
supplements: []
pathways: []
outcomes: []
population: ""
genetic_context: ""
evidence_level: 1
mechanistic_evidence: "none"  # strong | moderate | weak | mixed | negative | none
animal_evidence: "none"  # strong | moderate | weak | mixed | negative | none
human_evidence: "untested"  # strong | moderate | weak | mixed | negative | none | untested
translational_status: "insufficient"  # human-supported | mechanism-led | animal-led | contradicted | insufficient
effect_direction: "unknown"  # beneficial | harmful | mixed | null | unknown
hypothesis_status: open
review_by: ""  # YYYY-MM-DD date for next evidence/status review
if_supported: ""
if_contradicted: ""
evaluated: ""
sources: []
created: "{{date}}"
updated: "{{date}}"
status: current
tags:
  - open-question  # if hypothesis has unresolved gaps
---

> [!tldr]
> The hypothesis stated in one sentence.

## Claim

A precise, testable statement. Not vague ("X is good for you") but specific ("X activates pathway Y, producing outcome Z in population W").

## Chain

**Supplement(s):** [[Supplement A]], [[Supplement B]]
**Pathway(s):** [[Pathway X]]
**Outcome(s):** [[Outcome Y]]
**Population/context:** general adults | older adults | condition-specific | other
**Genetic context:** general | [[Gene]] | [[Variant]] | [[Genotype]]
**Effect direction:** beneficial | harmful | mixed | null | unknown

## Supporting Evidence

### Level [N] — [Label]

> [!source] Finding
> Specific evidence supporting the hypothesis. Hypotheses marked supported, contradicted, or nuanced should cite at least one non-synthesis anchor. [[Source Summary Page]]

| Evidence Layer | Stream Rating | Source Type | Population | Genetic Context | Effect Direction | Finding | Source |
|----------------|---------------|-------------|------------|-----------------|------------------|---------|--------|
| Mechanistic / Animal / Human biomarker / Human endpoint | strong / moderate / weak / mixed / negative / none / untested | | | | beneficial / harmful / mixed / null / unknown | | [[Source Summary Page]] |

## Evidence Stream Summary

| Stream | Rating | Direction | Interpretation |
|--------|--------|-----------|----------------|
| Mechanistic | strong / moderate / weak / mixed / negative / none | beneficial / harmful / mixed / null / unknown | |
| Animal | strong / moderate / weak / mixed / negative / none | beneficial / harmful / mixed / null / unknown | |
| Human | strong / moderate / weak / mixed / negative / none / untested | beneficial / harmful / mixed / null / unknown | |

Keep stream ratings tied to evidence type. Mechanistic evidence can strengthen plausibility, but it does not upgrade animal or human evidence.

## Contradicting Evidence

> [!source] Finding
> Specific evidence pushing against the hypothesis. [[Source Summary Page]]

> [!analysis] Interpretation
> How to reconcile or weigh the contradiction.

## Tensions and Nuances

> [!analysis] Boundary conditions
- Population-specific effects (works in X, not in Y)
- Dose-dependent paradoxes (helps at low dose, hurts at high)
- Context dependencies (only works when Z is present)
- Pro-survival paradoxes (helps prevention, hurts established disease)

## Status

**Current status:** open | supported | contradicted | nuanced

> [!analysis] Status reasoning
> Why this status, in 1-2 sentences. If the status depends only on a synthesis report, keep the hypothesis open or mark the missing anchor as a gap.

## Review Plan

| Field | Value |
|-------|-------|
| Review by | `review_by` |
| If supported | `if_supported` |
| If contradicted | `if_contradicted` |
| Evaluated | `evaluated` |

## What Would Change This

- **Would confirm:** [Specific evidence that would move status toward "supported"]
- **Would refute:** [Specific evidence that would move status toward "contradicted"]

## Open Questions

> [!gap] What we don't know
> What research is needed to resolve this hypothesis.

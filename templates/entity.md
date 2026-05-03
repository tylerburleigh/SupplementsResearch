---
type: entity
entity_type: "supplement"
aliases: []
evidence_level: 1
mechanistic_evidence: "none"  # strong | moderate | weak | mixed | negative | none
animal_evidence: "none"  # strong | moderate | weak | mixed | negative | none
human_evidence: "untested"  # strong | moderate | weak | mixed | negative | none | untested
translational_status: "insufficient"  # human-supported | mechanism-led | animal-led | contradicted | insufficient
practical_status: "research-only"  # candidate | consider | deprioritize | avoid | research-only
translation_plausibility: "unknown"  # high | moderate | low | blocked | unknown
replication_status: "unknown"  # replicated | mixed | single-lab | failed | untested | unknown
claim_scope: "unknown"  # general-longevity | condition-specific | biomarker-only | mechanism-only | unknown
primary_outcomes: []
primary_pathways: []
primary_genetics: []
sources: []
created: "{{date}}"
updated: "{{date}}"
status: current
tags:
  - supplement/<name>
  - open-question  # if page has [!gap] callouts
---

> [!tldr]
> One-sentence summary of this supplement/compound.

## Decision Snapshot

> [!analysis] Practical status
> Current posture: **research-only | candidate | consider | deprioritize | avoid**. State the reason in one sentence, separating evidence strength from personal fit. Decision-critical claims need a non-synthesis anchor or must be marked unverified/gap.

| Question | Current Answer | Confidence |
|----------|----------------|------------|
| Best-supported uses | | Low / Moderate / High |
| Unsupported or overhyped uses | | Low / Moderate / High |
| Practical dose/form | | Low / Moderate / High |
| Translation bottleneck | | Low / Moderate / High |
| Best justified claim | | Low / Moderate / High |
| Main reason not to take | | Low / Moderate / High |
| Main cautions | | Low / Moderate / High |

## Evidence Streams

> [!analysis] Translational read
> State whether this is human-supported, mechanism-led, animal-led, contradicted, or insufficient. A mechanism-led candidate requires no clear negative animal or human signal.

| Stream | Rating | Direction | Key Basis | Blocking Negative? | Source |
|--------|--------|-----------|-----------|--------------------|--------|
| Mechanistic | strong / moderate / weak / mixed / negative / none | beneficial / harmful / mixed / null / unknown | | yes / no | [[Source Summary Page]] |
| Animal | strong / moderate / weak / mixed / negative / none | beneficial / harmful / mixed / null / unknown | | yes / no | [[Source Summary Page]] |
| Human | strong / moderate / weak / mixed / negative / none / untested | beneficial / harmful / mixed / null / unknown | | yes / no | [[Source Summary Page]] |

Keep evidence streams separate: mechanistic findings do not count as animal or human evidence, and animal findings do not count as human evidence.

## Practical Translation Check

> [!analysis] Practical translation
> Evaluate whether the evidence survives contact with real-world use. Keep this separate from evidence quality: good mechanistic or animal evidence can still fail on dose plausibility, replication, claim scope, or effect size.

| Dimension | Assessment | Confidence | Notes |
|-----------|------------|------------|-------|
| Human-plausible dose | high / moderate / low / blocked | Low / Moderate / High | Does the studied dose map to routine human use? |
| Replication robustness | replicated / mixed / single-lab / failed / untested | Low / Moderate / High | Independent replication, species consistency, sex effects, ITP status if relevant |
| Claim scope | general-longevity / condition-specific / biomarker-only / mechanism-only | Low / Moderate / High | What claim is actually justified? |
| Expected effect size | large / moderate / small / unknown | Low / Moderate / High | Is the likely benefit meaningful versus alternatives? |
| Measure-to-target needed | yes / no / optional | Low / Moderate / High | Does use require labs or biomarker targeting? |
| Hype risk | low / moderate / high | Low / Moderate / High | Are public claims ahead of demonstrated outcomes? |

## What It Is

> [!source] Identity
> Chemical class, natural sources, available forms. [[Source Summary Page]]

## Mechanism of Action

> [!source] Primary pathway
> The validated mechanism(s) with evidence. [[Source Summary Page]]

> [!analysis] Secondary effects
> Inferred or less well-established effects with reasoning.

## Evidence by Outcome

### [Outcome 1 — e.g., Cancer Prevention]

> [!source] Evidence summary
> Key findings organized by evidence level. Decision-critical rows should cite a non-synthesis anchor. [[Source Summary Page]]

| Evidence Layer | Stream Rating | Finding | Source |
|----------------|---------------|---------|--------|
| Mechanistic | strong / moderate / weak / mixed / negative / none | | |
| Animal | strong / moderate / weak / mixed / negative / none | | |
| Human biomarker | strong / moderate / weak / mixed / negative / none / untested | | |
| Human clinical endpoint | strong / moderate / weak / mixed / negative / none / untested | | |

| Outcome | Effect Direction | Population | Genetic Context | Claim Scope | Clinical Relevance | Evidence Level | Translational Status | Source |
|---------|------------------|------------|-----------------|-------------|--------------------|----------------|----------------------|--------|
| [[Outcome or Condition]] | beneficial / harmful / mixed / null / unknown | | | general-longevity / condition-specific / biomarker-only / mechanism-only | | 1-4 | human-supported / mechanism-led / animal-led / contradicted / insufficient | [[Source Summary Page]] |

### [Outcome 2]

## Dosing

> [!source] Studied doses
> Dose ranges from clinical trials, optimal form, timing. Dosing claims should cite a dosing or primary-anchor source. [[Source Summary Page]]

| Form | Dose Range | Timing | Studied Population | Dose Confidence | Notes |
|------|------------|--------|--------------------|-----------------|-------|
| | | | | Low / Moderate / High | |

## Safety Profile

> [!source] Safety data
> Known side effects, LD50 if relevant, contraindications. Safety claims should cite a safety or primary-anchor source. [[Source Summary Page]]

## Interactions

> [!source] Drug interactions
> Known interactions with medications. [[Source Summary Page]]

> [!source] Supplement interactions
> Known interactions with other supplements. [[Source Summary Page]]

> [!analysis] Potential interactions
> Theoretically plausible but unconfirmed interactions, with reasoning.

## Practical Notes

> [!source] Bioavailability and formulation
> Absorption, stability, formulation considerations. [[Source Summary Page]]

## Key Gaps

> [!gap] What the research doesn't answer
> - [ ] Explicitly stated gaps in knowledge about this supplement.

## Relationships

- **Hypotheses** — link to any hypothesis pages that involve this entity: `[[Hypothesis Name]]`
- **Interacting entities** — link to entities with known or potential interactions (supplement-supplement, supplement-drug)
- **Targeted pathways** — link to concept pages (pathway type) that this entity affects
- **Related outcomes** — link to concept pages (outcome type) associated with this entity's effects
- **Genetic context** — link to gene, variant, genotype, or pharmacogenomic-marker concept pages that affect relevance, safety, or dose
- Source summaries go in `sources:` frontmatter, not here — this section is for knowledge-graph links

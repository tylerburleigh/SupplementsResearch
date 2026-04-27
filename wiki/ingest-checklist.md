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
> Step-by-step checklist for the human to run through during each wiki ingest. Print this out mentally before approving each ingest.

See also: [[lint-rules]], [[research-methodology]], [[taxonomy]], [[Quick Reference Dosing]]

## Pre-Ingest

- [ ] Source is staged in `raw/` or `research/<supplement>/report.md`
- [ ] `purpose.md` reviewed for research direction
- [ ] `wiki/synthesis.md` reviewed for existing context
- [ ] Related entity/concept pages identified from index

## AI Pre-Check (Presented to You)

- [ ] Key takeaways reviewed
- [ ] Planned new pages reviewed
- [ ] Existing pages to update reviewed
- [ ] Primary-anchor sources reviewed (major RCTs/meta-analyses, dosing, safety, contradictions, stack decisions)
- [ ] Source roles separated from evidence layers (`source_role` = why used; `evidence_layer` = mechanistic / animal / human / genetics / mixed)
- [ ] Potential contradictions flagged and reviewed

### Anchor Promotion Review

Before extraction, classify decision-relevant claims from the report:

| Claim | From Report | Evidence Layer | Needs Anchor? | Anchor Source | Reason |
|-------|-------------|----------------|---------------|---------------|--------|
| | report source | mechanistic / animal / human / genetics / mixed | yes / no | source page or [[promotion-queue]] | evidence level / dosing / safety / contradiction / genetics / stack decision |

## Post-Extraction Review

- [ ] New entity pages have all required sections (What It Is, Mechanism, Evidence, Dosing, Safety, Interactions, Practical Notes, Key Gaps)
- [ ] Evidence tables populated with evidence levels
- [ ] Entity Decision Snapshot populated (`practical_status`, best-supported uses, unsupported/overhyped uses, practical dose/form, cautions)
- [ ] Mechanistic, animal, and human evidence streams rated separately; blocking negative signals flagged
- [ ] No evidence stream collapsed into another (mechanistic evidence stays mechanistic; animal evidence stays animal; human evidence stays human)
- [ ] Outcome/condition/process concepts use the right `concept_type` and `domain`
- [ ] Genetics concepts use `concept_type: gene`, `genetic-variant`, `genotype`, or `pharmacogenomic-marker` and `domain: genetics`
- [ ] Hypotheses include `effect_direction`, `population`, `genetic_context`, and stream ratings
- [ ] All claims use correct callout types (`[!source]`, `[!analysis]`, `[!gap]`, `[!unverified]`)
- [ ] All `[!source]` claims link to a source page
- [ ] Decision-critical `[!source]` claims cite at least one non-synthesis anchor, or are marked `[!unverified]` / `[!gap]`
- [ ] Frontmatter complete on every new page (type, entity_type, sources, tags, created, updated)
- [ ] Wikilinks used (not markdown links) for all cross-references
- [ ] Aliases set for abbreviations and synonyms
- [ ] Dosing table in entity page matches [[Quick Reference Dosing]]
- [ ] Taxonomy categories assigned if applicable (see [[taxonomy]])
- [ ] Report-level source-summary created; individual primary-source summaries created only for anchor claims that need their own provenance
- [ ] Source-summary pages list entities, concepts, hypotheses/decisions, and claims they support
- [ ] Unpromoted but important report-derived claims added to [[promotion-queue]]

## Wiki Updates

- [ ] `wiki/synthesis.md` revised
- [ ] `wiki/interactions.md` updated with new interactions
- [ ] `wiki/debates.md` updated if contradictions found
- [ ] `wiki/decisions.md` updated if structural choices made
- [ ] `wiki/log.md` appended with ingest entry
- [ ] `wiki/handoff.md` updated for next session
- [ ] `wiki/taxonomy.md` updated if new categories apply
- [ ] `wiki/Quick Reference Dosing.md` updated

## Quality Checks

- [ ] No orphan pages created (all new pages linked from at least one other page)
- [ ] No unresolved wikilinks (all targets exist)
- [ ] Pages under ~1,500 words (split if needed)
- [ ] `[!gap]` callouts have `- [ ]` checkbox syntax
- [ ] `open-question` tag added to pages with open gaps

---
type: meta
sources: []
created: "2026-04-19"
updated: "2026-04-29"
status: current
tags:
  - meta
---

> [!tldr]
> Explicit checklist of what the lint pass validates. Add rules as the wiki grows and patterns emerge.

See also: [[index]], [[research-backlog]], [[ingest-checklist]], [[taxonomy]]

## Structural Rules

- [ ] Every wiki page has valid frontmatter (type, sources, created, updated, status, tags)
- [ ] Every wiki page has a `> [!tldr]` as the first content block
- [ ] Content page filenames use Title Case with spaces, matching wikilink text exactly; meta pages may use lowercase-hyphen names
- [ ] No special characters in filenames beyond spaces and hyphens
- [ ] Pages are under ~1,500 words (flag for splitting)

## Frontmatter Rules

- [ ] `type` matches page location for content pages (entity in `entities/`, concept in `concepts/`, etc.); `type: meta` scaffold pages are exempt and may live in root or directory README/queue files
- [ ] `entity_type` present on all entity pages (supplement, compound, brand, delivery-form)
- [ ] Supplement entity pages include `evidence_level`, `mechanistic_evidence`, `animal_evidence`, `human_evidence`, `translational_status`, `practical_status`, `translation_plausibility`, `replication_status`, `claim_scope`, `primary_outcomes`, `primary_pathways`, and `primary_genetics`
- [ ] `concept_type` present on all concept pages (pathway, pathway-family, outcome, condition, biomarker, process, risk-domain, population, gene, genetic-variant, genotype, pharmacogenomic-marker)
- [ ] Concept pages include `domain`
- [ ] `aliases` list present on entity pages (can be empty)
- [ ] `evidence_level` present on supplement entities and hypotheses
- [ ] `effect_direction`, `population`, `genetic_context`, `mechanistic_evidence`, `animal_evidence`, `human_evidence`, `translational_status`, `review_by`, `if_supported`, and `if_contradicted` present on hypothesis pages
- [ ] `hypothesis_status` present on hypothesis pages
- [ ] Non-open hypothesis pages have an `evaluated` date
- [ ] Practical decision pages use `type: decision`, live in `wiki/decisions/`, and include `decision_type`, `action`, `decision_status`, `supplements`, and optional `review_by`
- [ ] Source-summary pages include `ingest_status`, `reading_status`, `decision_relevance`, and `anchor_for`
- [ ] Source-summary `source_role` and `evidence_layer` are both populated and not conflated
- [ ] Source-summary pages list forward provenance for entities, concepts, hypotheses, decisions, or claims they support
- [ ] Dosing pages use `type: dosing`, include `supplement`, and live in `wiki/dosing/`
- [ ] Durable answer pages use `type: query`, live in `wiki/queries/`, and cite source summaries through `sources`
- [ ] `sources` list is non-empty for non-scaffold pages except source-summary pages, which use `raw_path` and `raw_hash` as primary provenance
- [ ] Frontmatter wikilinks in `sources`, `primary_outcomes`, `primary_pathways`, `primary_genetics`, `subjects`, `supplement`, `supplements`, `pathways`, `outcomes`, `population`, `genetic_context`, and `related_stack` resolve to wiki pages of the expected type when present
- [ ] `tags` follow the taxonomy (supplement/, pathway/, outcome/, condition/, process/, risk-domain/, population/, gene/, variant/, genotype/, open-question, meta) — no mirror tags that duplicate frontmatter fields
- [ ] Dates in ISO 8601 format

## Cross-Reference Rules

- [ ] All cross-references use wikilinks, not markdown links
- [ ] No unresolved wikilinks (all targets exist as files)
- [ ] No orphan pages (every content page except `type: query` is linked from at least one other non-meta page)
- [ ] No dead-end pages (every page has at least one outgoing wikilink)
- [ ] Self-links do not count toward orphan/dead-end checks
- [ ] Links from `type: meta` pages do not count as content-page incoming links for orphan checks
- [ ] Wikilinks inside fenced code blocks or inline code spans are ignored by link validation
- [ ] Source-summary pages link to their raw/research source

## Claim Rules

- [ ] Every `[!source]` callout includes a source-summary wikilink
- [ ] No `[!source]` callouts without attribution
- [ ] No untyped claims (every factual statement uses a callout type)
- [ ] Decision-critical claims do not cite only `source_role: synthesis`
- [ ] Report-derived claims without a checked anchor are marked `[!unverified]` or `[!gap]`
- [ ] `[!gap]` callouts use `- [ ]` checkbox syntax
- [ ] Pages with `[!gap]` callouts have the `open-question` tag

## Supplement Entity Rules

- [ ] Required sections present: What It Is, Mechanism of Action, Evidence by Outcome, Dosing, Safety Profile, Interactions, Practical Notes, Key Gaps
- [ ] Evidence tables keep mechanistic, animal, human biomarker, and human endpoint evidence separate
- [ ] Evidence Streams section distinguishes mechanistic, animal, and human evidence and flags blocking negative evidence
- [ ] Practical Translation Check distinguishes human-plausible dose, replication robustness, claim scope, expected effect size, measure-to-target need, and hype risk
- [ ] Decision Snapshot, dosing, safety, interaction, and practical status claims cite at least one non-synthesis anchor or are marked as unverified/gap
- [ ] `evidence_level: 3` or `evidence_level: 4` supplement entities cite a human RCT, systematic review, or meta-analysis anchor
- [ ] Dosing table present with Form, Dose Range, Timing, Studied Population, Dose Confidence, and Notes columns
- [ ] Decision Snapshot section present with practical status, best-supported uses, unsupported/overhyped uses, dose/form, translation bottleneck, best justified claim, main reason not to take, and cautions

## Concept Rules

- [ ] Concept pages state their scope and boundaries
- [ ] Concept pages use the Evidence Map table for supplement/intervention relationships
- [ ] Basic biology pages use `concept_type: process` or `pathway-family`, not `outcome`
- [ ] Disease pages use `concept_type: condition`; prevention/risk pages use `concept_type: risk-domain`
- [ ] Genetics pages use `concept_type: gene`, `genetic-variant`, `genotype`, or `pharmacogenomic-marker` and `domain: genetics`

## Hypothesis Rules

- [ ] Hypotheses marked `supported`, `contradicted`, or `nuanced` cite at least one non-synthesis anchor
- [ ] Hypothesis evidence stream ratings match the cited evidence layer (mechanistic evidence is not counted as animal or human evidence)
- [ ] Genetics-specific hypotheses cite a genetics anchor or mark `genetic_context` claims as unverified/gap
- [ ] Open hypotheses have a future-oriented `review_by` date and explicit `if_supported` / `if_contradicted` implications
- [ ] Closed hypotheses record `evaluated` so calibration can be audited later

## Decision Rules

- [ ] `type: decision` pages link affected supplements and optionally the related stack
- [ ] Active decision pages with `review_by` dates are revisited during `/wiki-review`
- [ ] Decision pages include "What Would Change My Mind" and "Outcome" sections
- [ ] Stack membership, dose, avoidance, pause/resume, and monitoring changes get decision pages when the reasoning should be revisited

## Integrity Rules

- [ ] `raw_hash` on source-summary pages matches current file in `raw/` or `research/`
- [ ] Schema enum values in `CLAUDE.md` stay synchronized with `wiki/scripts/lint.py`
- [ ] `wiki/catalog.md` is regenerated with `python3 wiki/scripts/lint.py --rebuild-catalog` after page-shape changes
- [ ] `ingest_status: in-progress` source-summary pages are resumed, restarted, or completed before another ingest of the same source proceeds
- [ ] [[promotion-queue]] entries exist for decision-critical report-derived claims that lack anchor sources
- [ ] Completed [[promotion-queue]] rows have corresponding source-summary pages and target-page citations
- [ ] Promotion-queue entries with `Marked` dates >30 days old surface in research-backlog
- [ ] `wiki/research-queue.md` rows use `R###` IDs, valid priority/status values, and ISO `Review By` dates
- [ ] `wiki/evidence-watch.md` rows use ISO dates and checkbox status; overdue unchecked events surface as warnings
- [ ] No stale pages (`updated` date older than 30 days without `stale` status)
- [ ] Log has entries for all ingests and significant operations
- [ ] Synthesis reflects current wiki state (not just the latest ingest)

## Custom Rules

<!-- Add your own rules below as patterns emerge. -->

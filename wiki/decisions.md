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
> Append-only log of significant structural decisions and the rationale behind them.

<!-- Format: ### [YYYY-MM-DD] decision | rationale -->
<!-- Use obsidian append to add entries. Do not rewrite past entries. -->

### [2026-04-24] decision | Added a decision/evidence metadata layer to support a mixed supplement, outcome, disease-risk, cognition, mood, and basic-biology wiki. Supplement entity pages now carry practical status and primary outcome/pathway metadata; concept pages support expanded subtypes beyond pathway/outcome; hypotheses carry population and effect direction. Research reports remain synthesis sources, while individual primary sources are promoted only when they anchor evidence level, dosing, safety, contradictions, or stack decisions.

### [2026-04-24] decision | Split evidence assessment into mechanistic, animal, and human streams while keeping the 1-4 evidence ladder. This supports mechanism-led practical candidates when mechanistic evidence is strong and downstream animal/human evidence is weak or untested, but not negative. Added genetics-aware concept types and hypothesis/source metadata so genes, variants, genotypes, and pharmacogenomic markers can shape supplement relevance, dose, safety, and population fit.

### [2026-04-26] decision | Formalized source-role provenance so AI research reports build the map while non-synthesis anchors carry decision-critical claims. `source_role` now stays separate from `evidence_layer`: source role explains why a source is in the graph, while evidence layer preserves mechanistic, animal, human, genetics, or mixed evidence. Added a promotion queue for report-derived claims that need anchor review before they can support practical status, dosing, safety, evidence level, hypothesis status, or stack decisions.

### [2026-04-26] decision | Made dedicated dosing pages a first-class `type: dosing` instead of `type: entity` with `entity_type: delivery-form`. Dosing pages live in `wiki/dosing/`, link back to their supplement through `supplement`, and keep detailed form/timing/population dosing guidance out of entity pages while preserving the type-location lint rule.

### [2026-04-26] decision | Made progressive disclosure the wiki navigation model. `wiki/synthesis.md` is the human-facing front door, `wiki/queries/README.md` is the practical question hub, and `wiki/index.md` plus Bases dashboards are deeper catalog views. This keeps the organizational scaffold intact while routing users first through decisions, questions, and next actions.

### [2026-04-26] decision | Implemented schema resilience as executable lint plus resumable ingest state. Source summaries now carry `ingest_status` so partial ingests can be resumed or restarted deliberately; research reports use real SHA256 hashes for staleness checks; mirror tags stay removed because frontmatter is the decision/query source of truth. Promotion queue aging is surfaced from `wiki/research-backlog.md` because Bases query files/frontmatter, not Markdown table rows.

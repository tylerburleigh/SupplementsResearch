---
type: meta
sources: []
created: "2026-04-18"
updated: "2026-04-27"
status: current
tags:
  - meta
---

> [!tldr]
> Chronological operation log — every ingest, query, lint pass, and structural change appended here.

# Operation Log

### [2026-04-18] init | Vault scaffolded with wiki structure, templates, and CLAUDE.md schema.
### [2026-04-19] schema | Added aliases/raw_hash frontmatter, gap task convention, append/move/aliases tooling, entry points navigation protocol, DataView index clarification, debates and decisions log pages, prescribed synthesis sections.
### [2026-04-19] docs | Created README.md — human-facing onboarding guide for the vault.
### [2026-04-19] schema | Git init, handoff file, interactions matrix, query filing, confidence calibration, contradiction sweep in ingest, staleness check in lint, study_type in source-summary frontmatter.
### [2026-04-19] scaffold | Enhanced wiki with 10 scaffold additions: FAQ/queries README, outcome + pathway dashboard .base files, quick-reference dosing cheat sheet, ingest checklist, research-priority.md, lint-rules.md, staleness hash-mismatch section in research-backlog, taxonomy.md, wiki/dosing/ directory with README and template, CSS callout snippet for Obsidian.
### [2026-04-19] research-infrastructure | Created research methodology doc (wiki/docs/research-methodology.md), scouting skill (.claude/skills/scout/) with preliminary research workflow, scouting directory (wiki/scouting/) siloed from main wiki, updated CLAUDE.md vault layout and entry points.
### [2026-04-19] scaffold-fix | Fixed all scaffold issues: added `meta` type to CLAUDE.md enum, changed all scaffold pages from `type: concept` + `concept_type: meta` to `type: meta`, added frontmatter to log.md, updated vault layout to list all scaffold files, documented naming exception for meta pages, added cross-links between scaffold pages, added README.md to all six empty data directories.
### [2026-04-19] graph-protocol | Created wiki/docs/graph-protocol.md — the missing "map" document explaining the knowledge graph model (node types, edge types, bidirectionality rules, DataView dependencies, template usage, ingest sequence). Tightened entity and concept template linking sections with specific link-type guidance. Added graph-protocol reference to CLAUDE.md vault layout and entry points table.
### [2026-04-19] agent-wiring | Added graph-protocol.md as required reading to wiki-extractor agent (step 2). Added graph integrity checks to wiki-auditor agent (bidirectionality, reciprocal links, empty structural sections). Added `graph-integrity` gap category to auditor.
### [2026-04-19] orchestrator-graph | Added graph-protocol.md to wiki-ingest orchestrator's context-read step. Added "Graph connectivity" as item 7 in the pre-check — confirms no orphans or dead ends before pages are written.
### [2026-04-24] schema | Expanded the wiki scaffold for mixed practical and basic-biology knowledge: added practical supplement status, expanded concept subtypes, hypothesis effect direction/population, selective primary-anchor source promotion, Evidence Map.base, and updated templates/dashboards/checklists.
### [2026-04-24] evidence-streams | Added separate mechanistic, animal, and human evidence stream ratings; translational status for mechanism-led candidates; and genetics-aware concept/source/hypothesis metadata.
### [2026-04-26] provenance-framework | Formalized source-role provenance: research reports remain synthesis sources, decision-critical claims require non-synthesis anchors or unverified/gap marking, source role stays separate from mechanistic/animal/human/genetics evidence layers, and report-derived claims awaiting anchor review go to wiki/sources/promotion-queue.md.
### [2026-04-26] scaffold-consistency | Fixed wiki scaffolding inconsistencies: normalized open-question tags and tag queries, filtered README scaffold rows from directory dashboards, made dosing pages `type: dosing`, aligned source provenance docs/views, and removed placeholder wikilinks from scaffold comments.
### [2026-04-26] scaffold-consistency | Clarified meta scaffold exemptions for location/type linting, updated Quick Reference Dosing for `type: dosing` pages, and removed remaining instructional wikilinks that could create unresolved-link noise.
### [2026-04-26] navigation | Reworked human-facing entry points around progressive disclosure: synthesis as front door, queries as practical question hub, index/Bases as deeper catalog views.
### [2026-04-26] resilience | Implemented PLAN.md resilience pass: added stdlib wiki linter, Claude hook config, git-commit lint wrapper, source-summary ingest status, real research-report hash guidance, promotion queue aging surface, calibration sweep doc, schema canary doc, and aligned agent/schema/template instructions.
### [2026-04-27] resilience-hardening | Completed PLAN.md follow-up hardening: frontmatter wikilink validation, CLAUDE.md/linter enum schema-sync check, local Git pre-commit lint hook, and source-summary wikilink placeholders in templates.
### [2026-04-27] resilience-hardening-fix | Fixed review issues: source-summary template no longer self-cites, hypothesis scalar wikilinks are validated when present, self-links do not satisfy graph checks, source-summary pages may keep `sources: []`, and pre-commit lint hook is tracked under `.githooks/`.
### [2026-04-27] scaffold-borrow | Borrowed recent llm-wiki improvements: static generated catalog, lint fixture tests, inline-code wikilink stripping, meta-link orphan isolation, repair/lint/query skills, and broader local ignore coverage.
### [2026-04-27] scaffold-borrow-fix | Fixed review findings from the borrowing pass: restored CLAUDE.md layout hierarchy, made missing/stale catalog deterministic lint errors, added first-class `type: query`, and made catalog rebuild fail before writing when validation errors exist.
### [2026-04-27] operating-loop | Borrowed Investments vault operating-loop mechanics: briefing script, research queue sync, evidence watch, wiki review skill/template, practical decision pages, and time-bound hypothesis review fields.

---
type: meta
sources: []
created: "2026-04-19"
updated: "2026-04-27"
status: current
tags:
  - meta
---

> [!tldr]
> Session handoff — what was last worked on, what's in progress, what's blocked. Updated at end of every session.

## Last Session

<!-- Update at end of each session. Keep brief — 5-10 lines max. -->

### [2026-04-27] PLAN follow-up hardening
- Added lint validation for wikilinks stored in relationship frontmatter fields, including expected target types for sources, supplement links, pathways, outcomes, and genetics
- Added a CLAUDE.md schema-sync guard so documented enum values cannot drift from lint constants silently
- Added tracked `.githooks/pre-commit` and configured this clone with `core.hooksPath=.githooks`
- Removed the source-summary template self-citation pattern and made self-links irrelevant to orphan/dead-end checks
- Exempted source-summary pages from the non-empty `sources` requirement because `raw_path` and `raw_hash` are their primary provenance
- Added optional wikilink validation for hypothesis `population` and `genetic_context`
- `python3 wiki/scripts/lint.py`, an AST syntax parse, and `.githooks/pre-commit` pass

### [2026-04-26] Resilience implementation pass
- Implemented `wiki/scripts/lint.py` with stdlib checks for frontmatter, TLDR placement, wikilink resolution, source callouts, source hash staleness, and promotion queue aging
- Added `.claude/settings.json` hooks: SessionStart staleness check and PreToolUse git-commit lint wrapper
- Added `ingest_status` to source-summary schema/template and aligned wiki-ingest/extractor/auditor handoffs around resumable ingests
- Removed leftover mirror tag instructions from templates and graph protocol
- Added calibration sweep and schema canary protocol docs
- `python3 wiki/scripts/lint.py` passes on the current scaffold

### [2026-04-26] Progressive disclosure navigation pass
- Promoted `wiki/synthesis.md` into the human-facing front door with intent-based routes and decision-surface DataView sections
- Reworked README Start Here around user intent rather than folder structure
- Sharpened `wiki/queries/README.md` into the common-questions hub for practical supplement decisions
- Updated CLAUDE.md entry-point guidance so future query work starts from synthesis + queries before falling into the full catalog
- Logged the navigation model in decisions and operation log

### [2026-04-26] Scaffold consistency pass
- Normalized `open-question` handling for scaffold pages with real gap callouts
- Updated Dataview/Base tag queries to use Obsidian-style `#tag` values
- Filtered README scaffold rows out of directory contents tables
- Made dedicated dosing pages first-class `type: dosing` pages and added `templates/dosing.md`
- Aligned source provenance docs/views with the source-role framework
- Removed placeholder wikilinks from scaffold comments and fixed the uppercase Debates link to `[[debates]]`
- Follow-up: clarified meta scaffold exemptions, updated Quick Reference Dosing for `type: dosing`, and removed remaining example wikilinks that created unresolved-link noise

### [2026-04-26] Source-role provenance framework
- Formalized the distinction between synthesis sources and non-synthesis anchors
- Added rule: decision-critical claims cannot rely only on AI research reports or other synthesis sources
- Kept evidence type separate from source role: mechanistic, animal, human, genetics, and mixed evidence remain distinct
- Added `reading_status`, `decision_relevance`, and `anchor_for` to the source-summary template
- Added `wiki/sources/promotion-queue.md` for report-derived claims awaiting anchor review
- Updated methodology, graph protocol, ingest checklist, lint rules, source README, templates, CLAUDE.md, log, and decisions

### [2026-04-24] Scaffold expansion for mixed knowledge base
- Added practical supplement metadata: `practical_status`, `primary_outcomes`, `primary_pathways`, and decision tags
- Expanded concept model: `pathway-family`, `condition`, `process`, `risk-domain`, and `population` now fit alongside pathway/outcome/biomarker
- Added hypothesis metadata for `effect_direction` and `population`
- Added `wiki/Evidence Map.base` for cross-cutting evidence and decision views
- Updated templates, dashboards, ingest checklist, lint rules, graph protocol, and research methodology
- Adopted selective primary-anchor source summaries instead of one source-summary per citation

### [2026-04-24] Evidence streams and genetics
- Added `mechanistic_evidence`, `animal_evidence`, `human_evidence`, and `translational_status` fields to supplement entities and hypotheses
- Added `mechanism-led` as a first-class status for strong mechanism, weak/untested downstream evidence, and no blocking negative signal
- Added genetics-aware concept types: `gene`, `genetic-variant`, `genotype`, and `pharmacogenomic-marker`
- Added `genetic_context` to hypotheses and `primary_genetics` to supplement entities
- Updated Evidence Map, dashboards, ingest/audit agents, lint rules, and methodology docs

### [2026-04-19] Scaffold consistency fix
- Added `meta` type to CLAUDE.md frontmatter enum; changed all scaffold pages from `type: concept` to `type: meta`
- Added frontmatter to `log.md` (was missing entirely)
- Updated vault layout in CLAUDE.md to list all scaffold files (research-backlog, taxonomy, lint-rules, ingest-checklist, Quick Reference Dosing)
- Documented naming exception: meta pages use lowercase-hyphen, content pages use Title Case
- Added cross-links (See also) between related scaffold pages
- Added README.md with DataView queries to all 6 empty data directories (entities, concepts, hypotheses, comparisons, stacks, sources)

### [2026-04-19] Graph protocol documentation
- Created `wiki/docs/graph-protocol.md` — the definitive reference for how the knowledge graph works
- Tightened entity template "Relationships" section: replaced vague line with 5 specific link-type expectations
- Tightened concept template "Connections" section: same treatment
- Added graph-protocol to CLAUDE.md vault layout and entry points table
- **Next:** begin ingesting research reports (sulforaphane, taurine)

### [2026-04-19] Agent wiring
- Added `wiki/docs/graph-protocol.md` as required reading to wiki-extractor agent (new step 2, before reading the report)
- Added graph integrity checks to wiki-auditor agent: bidirectionality, reciprocal links, empty structural sections
- Added `graph-integrity` gap category to auditor's output format
- **Next:** begin ingesting research reports (sulforaphane, taurine)

### [2026-04-19] Research infrastructure
- Created research methodology doc: `wiki/docs/research-methodology.md`
- Created `/scout` skill for preliminary evidence assessment → `wiki/scouting/`
- Created `wiki/scouting/` silo (separate from main wiki until promoted through deep research)
- Updated CLAUDE.md with new vault layout and entry points
- **Still no supplements ingested** — wiki is ready for population

### [2026-04-19] Scaffold enhancement
- Added 10 scaffold enhancements: FAQ page, outcome/pathway dashboards, dosing cheat sheet, ingest checklist, research priority list, lint rules, staleness detection, taxonomy, dosing directory, CSS callout styling
- Still no supplements ingested — wiki is ready for population
- **Next:** begin ingesting research reports

### [2026-04-19] Schema buildout
- Vault scaffolded with full CLAUDE.md schema, templates, wiki structure
- Added: aliases, raw_hash, gap tasks, entry points, debates, decisions log, interactions matrix, handoff file, README
- Git initialized

## In Progress

<!-- Active tasks that span sessions. Remove when done. -->

- [ ] Ingest sulforaphane research report
- [ ] Ingest taurine research report
- [ ] Fill in purpose.md thesis and current stack (human-owned)

## Blocked

<!-- Items waiting on human input or external action. -->

- [ ] Enable Obsidian CLI (Settings → General → Command line interface)

## Open Questions

<!-- Questions that came up during a session and weren't resolved. -->

- None yet.

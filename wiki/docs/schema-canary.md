---
type: meta
sources: []
created: "2026-04-26"
updated: "2026-04-27"
status: current
tags:
  - meta
---

> [!tldr]
> Protocol for validating schema changes against a real supplement ingest before the schema is treated as stable.

# Schema Canary

## Canary Page Set

Use sulforaphane as the schema canary after its first formal ingest. The canary set includes the sulforaphane entity page, its report source-summary, any promoted primary-anchor source summaries, linked concepts, linked hypotheses, any practical decision pages created from the ingest, and any dedicated dosing page created during that ingest.

Until sulforaphane is ingested, the canary is unavailable. Schema changes can still proceed, but they must pass scaffold lint and should be rechecked after the first ingest.

## When To Run

Run the canary protocol after any change to:

- `CLAUDE.md` frontmatter contracts
- Page templates
- `wiki/scripts/lint.py`
- Bases or DataView queries
- Ingest, extractor, or auditor agent instructions
- Graph, source-provenance, or dosing conventions

## Procedure

1. Run `python3 wiki/scripts/lint.py`.
2. Review all canary pages against the changed schema field by field.
3. Confirm source-summary `raw_hash` values still match their `raw_path` files.
4. Confirm all canary `[!source]` callouts still resolve to source-summary pages.
5. Confirm dashboards still surface the canary pages in the expected views.
6. Confirm hypothesis canary pages have `review_by`, `if_supported`, `if_contradicted`, and `evaluated` behavior that matches their status.
7. Confirm practical decision canary pages have `decision_type`, `action`, `decision_status`, affected supplements, and a review path.
8. Fix any canary failure before applying the schema pattern to later ingests.

## Blocking Rule

A schema change is blocked when it breaks the canary page set, leaves an unresolved field migration, or requires manual interpretation that is not documented in `CLAUDE.md`, a template, or a docs page.

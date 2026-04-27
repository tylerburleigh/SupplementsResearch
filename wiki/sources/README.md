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
> Source summary pages — one per ingested synthesis source or selected primary anchor, linking back to the original in `raw/` or `research/`.

## Contents

```dataview
TABLE study_type AS "Study Type", source_role AS "Role", ingest_status AS "Ingest Status", evidence_layer AS "Evidence Layer", reading_status AS "Read", decision_relevance AS "Decision Relevance", anchor_for AS "Anchors", raw_path AS "Source File", created AS "Ingested"
FROM "wiki/sources"
WHERE type = "source-summary"
SORT created DESC
```

## Promotion Queue

Use [[promotion-queue]] for report-derived claims that may need a primary, meta-analysis, dosing, safety, contradiction, or genetics anchor before they can support a decision-critical claim.

See also: [[index]], [[research-methodology]], [[ingest-checklist]]

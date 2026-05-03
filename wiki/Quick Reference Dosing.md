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
> Quick-reference dosing cheat sheet compiled from all supplement entity pages. Updated on every ingest.

## How This Works

This page is populated from supplement entity pages and dedicated `type: dosing` pages. During each ingest, update this table with the latest dosing data.

> [!analysis]
> The table below is manually maintained from ingest. DataView cannot extract table contents from within pages, so this serves as the compiled quick-reference. Always cross-check against the entity page or dedicated dosing page for full context.

## Dosing Reference

| Supplement | Form | Dose Range | Timing | Studied Population | Dose Confidence | Translation Plausibility | Key Notes | Source Page |
|------------|------|------------|--------|--------------------|-----------------|-------------------------|-----------|-------------|
| | | | | | Low / Moderate / High | high / moderate / low / blocked / unknown | | |

<!-- Add rows during each ingest. Link source page as wikilink. -->

## Dedicated Dosing Pages

```dataview
TABLE WITHOUT ID
  supplement AS "Supplement",
  updated AS "Last Updated"
FROM "wiki/dosing"
WHERE type = "dosing"
SORT file.name ASC
```

## Supplements Without Dedicated Dosing Page

This check follows the naming convention from `wiki/dosing/README.md`: a supplement page named `Magnesium` should have a dedicated page named `Magnesium Dosing` when one is needed.

```dataviewjs
const dosingPages = new Set(
  dv.pages('"wiki/dosing"')
    .where(page => page.type === "dosing")
    .map(page => page.file.name.replace(/ Dosing$/, ""))
);

dv.table(
  ["Supplement", "Last Updated"],
  dv.pages('"wiki/entities"')
    .where(page => page.entity_type === "supplement" && !dosingPages.has(page.file.name))
    .sort(page => page.file.name, "asc")
    .map(page => [page.file.link, page.updated])
);
```

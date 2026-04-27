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
> Dedicated dosing pages for supplements where the dosing section outgrows the entity page. Keeps entity pages focused and enables cross-supplement dosing comparison.

## When to Create a Dosing Page

Create a dedicated dosing page when:
- The supplement has multiple forms with different bioavailability (e.g., magnesium glycinate vs citrate vs threonate)
- Dosing varies significantly by outcome (e.g., creatine for cognition vs performance)
- There are timing or cycling considerations that deserve their own section
- The entity page's Dosing section exceeds ~200 words

## Naming Convention

File: `wiki/dosing/<Supplement Name> Dosing.md` (e.g., `Magnesium Dosing.md`)
Link from entity page using a wikilink to the dedicated dosing page.

## Dosing Page Template

Use `templates/dosing.md` as the source template for dedicated dosing pages.

## All Dosing Pages

```dataview
TABLE WITHOUT ID
  file.link AS "Supplement",
  updated AS "Updated"
FROM "wiki/dosing"
WHERE type = "dosing"
SORT file.name ASC
```

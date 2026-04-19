# Supplements Research Vault

An evidence-based wiki on supplementation for longevity and healthspan. Research is ingested from papers, articles, and deep-research reports; Claude extracts and organizes it into a structured knowledge base.

---

## Start Here

| Page | What it is |
|------|-----------|
| [`purpose.md`](purpose.md) | Your research goals, current stack, and working thesis. Claude reads this on every task. |
| [`wiki/synthesis.md`](wiki/synthesis.md) | The wiki's current best understanding — strongest evidence, active debates, best-guess stack, priority gaps. |
| [`wiki/research-backlog.md`](wiki/research-backlog.md) | Open questions, thinly-sourced pages, and stale pages. What to research next. |
| [`wiki/index.md`](wiki/index.md) | Full content catalog — supplements, pathways, outcomes, hypotheses, stacks, sources. Auto-updates from page frontmatter. |
| [`wiki/debates.md`](wiki/debates.md) | Active disagreements between sources, and hypotheses with contested or nuanced status. |
| [`wiki/decisions.md`](wiki/decisions.md) | Log of significant structural decisions Claude made and why. |

---

## Vault Layout

```
raw/              Drop sources here for ingestion (PDFs, articles, notes)
research/         Deep-research reports (one subdirectory per supplement)
wiki/             The compiled knowledge base
  entities/       Supplement, compound, pathway, and biomarker pages
  concepts/       Pathway and outcome concept pages
  sources/        One summary page per ingested source
  hypotheses/     Testable claims connecting supplements → pathways → outcomes
  comparisons/    Head-to-head supplement comparisons
  stacks/         Stack configurations with rationale
templates/        Page templates
purpose.md        Your research direction (edit this directly)
writing-style.md  Style guide for wiki pages
CLAUDE.md         Agent schema and instructions
```

---

## How to Add a Source

**Option 1 — Drop a file:**
1. Put the PDF, article, or note in `raw/`
2. Ask Claude: `/wiki-ingest raw/your-file.pdf`

**Option 2 — Run deep research first:**
1. Ask Claude: `/deep-research <supplement name>`
2. After the report is generated: `/wiki-ingest <supplement name>`

Claude will present a pre-check (key takeaways, planned pages, contradictions) before writing anything. You approve before it proceeds.

---

## How to Ask Claude Questions

Ask in plain language. Examples:

- *"What's the best evidence for sulforaphane and cancer prevention?"*
- *"What does the wiki say about Nrf2 activators?"*
- *"Compare taurine and creatine for cardiovascular outcomes."*
- *"What should I research next?"*
- *"Design a longevity stack based on what we know so far."*

Claude reads `wiki/synthesis.md` first, then navigates to relevant pages. It cites specific wiki pages and distinguishes sourced claims from its own inferences.

---

## How to Update Your Stack or Thesis

Edit `purpose.md` directly. Claude reads it on every task — keeping it current improves ingest prioritization and query relevance. The two most valuable fields to maintain:

- **Thesis** — Your current working hypothesis about supplementation
- **Current Stack** — What you're actually taking, at what doses

---

## Maintaining the Wiki

**Lint the wiki** (find orphans, broken links, missing frontmatter):
Ask Claude: *"lint the wiki"*

**Re-ingest a source** (if a paper has been updated):
Ask Claude: `/wiki-ingest raw/your-file.pdf` — Claude checks `raw_hash` to detect changes.

**The index and backlog update automatically** from page frontmatter via DataView. If something looks wrong in the index, check the frontmatter on the relevant page rather than editing the index directly.

---

## Evidence Levels

| Level | Label | What it means |
|-------|-------|---------------|
| 1 | Mechanistic | Cell or molecular evidence only |
| 2 | Preclinical | Animal studies |
| 3 | Biomarker RCT | Human trial showing biomarker changes |
| 4 | Clinical endpoint RCT | Human trial showing disease, mortality, or functional outcomes |

A plausible mechanism (Level 1) is not clinical proof. The wiki distinguishes these explicitly.

# Supplements Research Vault

An evidence-based wiki on supplementation for longevity and healthspan. Research is ingested from papers, articles, and deep-research reports; Claude extracts and organizes it into a structured knowledge base.

---

## Start Here

Start with the task, not the folder structure. [`wiki/synthesis.md`](wiki/synthesis.md) is the front door; [`wiki/index.md`](wiki/index.md) is the Obsidian/DataView catalog once you know what you are looking for. [`wiki/catalog.md`](wiki/catalog.md) is the static catalog for agents and shell-only sessions.

| If you want to... | Start here | Then go deeper with... |
|------|-----------|-----------|
| Understand the current state of the wiki | [`wiki/synthesis.md`](wiki/synthesis.md) | [`wiki/Evidence Map.base`](wiki/Evidence%20Map.base), [`wiki/index.md`](wiki/index.md) |
| Decide whether something is worth taking | [`wiki/synthesis.md`](wiki/synthesis.md) | Supplement entity pages, [`wiki/Quick Reference Dosing.md`](wiki/Quick%20Reference%20Dosing.md), [`wiki/interactions.md`](wiki/interactions.md) |
| Ask a recurring practical question | [`wiki/queries/README.md`](wiki/queries/README.md) | Answered query pages, relevant supplement and concept pages |
| Compare supplement options | [`wiki/comparisons/README.md`](wiki/comparisons/README.md) | Entity pages and source summaries |
| Check dose, form, or timing | [`wiki/Quick Reference Dosing.md`](wiki/Quick%20Reference%20Dosing.md) | Dedicated dosing pages in `wiki/dosing/` |
| Find safety concerns or conflicts | [`wiki/interactions.md`](wiki/interactions.md) | Supplement entity safety sections and source summaries |
| Choose what to research next | [`wiki/research-queue.md`](wiki/research-queue.md) | [`wiki/research-backlog.md`](wiki/research-backlog.md), [`research-priority.md`](research-priority.md), [`purpose.md`](purpose.md) |
| Track future evidence to revisit | [`wiki/evidence-watch.md`](wiki/evidence-watch.md) | Hypothesis pages and practical decision notes |
| Record a stack decision | [`templates/decision.md`](templates/decision.md) | `wiki/decisions/`, entity pages, dosing pages, [`wiki/interactions.md`](wiki/interactions.md) |
| Run periodic maintenance | `python3 wiki/scripts/briefing.py` | `/wiki-review`, [`wiki/reviews/`](wiki/reviews/) |
| Browse everything | [`wiki/index.md`](wiki/index.md) | [`wiki/catalog.md`](wiki/catalog.md), Bases dashboards, and directory README pages |

Key context pages:

| Page | What it is |
|------|-----------|
| [`purpose.md`](purpose.md) | Your research goals, current stack, and working thesis. Claude reads this on every task. |
| [`wiki/decisions.md`](wiki/decisions.md) | Log of significant structural decisions Claude made and why. |

---

## Vault Layout

```
raw/              Drop sources here for ingestion (PDFs, articles, notes)
research/         Deep-research reports (one subdirectory per supplement)
wiki/             The compiled knowledge base
  entities/       Supplement, compound, brand, and delivery-form pages
  concepts/       Pathway, outcome, condition, biomarker, population, and basic-biology concept pages
  sources/        Report summaries and selected decision-critical source anchors
  hypotheses/     Testable claims connecting supplements → pathways → outcomes
  comparisons/    Head-to-head supplement comparisons
  stacks/         Stack configurations with rationale
  decisions/      Practical supplement and stack decision notes
  reviews/        Periodic wiki review notes
  queries/        Durable answers to recurring practical questions
  dosing/         Dedicated dosing pages when entity dosing sections grow large
  catalog.md      Static markdown catalog generated for agents and non-Obsidian workflows
  research-queue.md  ID-based gap/unverified claim queue
  evidence-watch.md  Future evidence and review-event watchlist
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

**Enable tracked Git hooks** (once per clone):
Run `git config core.hooksPath .githooks` so commits use the tracked pre-commit lint hook.

**Lint the wiki** (find orphans, broken links, missing frontmatter):
Ask Claude: *"lint the wiki"*

**Brief the current state** (session start / review agenda):
Run `python3 wiki/scripts/briefing.py`.

**Sync gaps into the research queue**:
Run `python3 wiki/scripts/backlog_sync.py` to preview new items, then `python3 wiki/scripts/backlog_sync.py --apply` to add them to `wiki/research-queue.md`.

**Run a periodic review**:
Ask Claude: *"run a monthly wiki review"* or use `/wiki-review`.

**Run lint tests** (for scaffold/linter changes):
Run `python3 -m unittest -q`.

**Refresh the static catalog** (for agents and shell-only sessions):
Run `python3 wiki/scripts/lint.py --rebuild-catalog`.

**Re-ingest a source** (if a paper has been updated):
Ask Claude: `/wiki-ingest raw/your-file.pdf` — Claude checks `raw_hash` to detect changes.

**The index and backlog update automatically** from page frontmatter via DataView. If something looks wrong in the index, check the frontmatter on the relevant page rather than editing the index directly. The static catalog is generated; rebuild it instead of hand-editing it.

---

## Evidence Levels

| Level | Label | What it means |
|-------|-------|---------------|
| 1 | Mechanistic | Cell or molecular evidence only |
| 2 | Preclinical | Animal studies |
| 3 | Biomarker RCT | Human trial showing biomarker changes |
| 4 | Clinical endpoint RCT | Human trial showing disease, mortality, or functional outcomes |

A plausible mechanism (Level 1) is not clinical proof. The wiki distinguishes these explicitly.

## Evidence Streams

The wiki also tracks `mechanistic_evidence`, `animal_evidence`, and `human_evidence` separately. This lets a supplement be marked `mechanism-led` when mechanistic evidence is strong but human evidence is still weak or untested, as long as animal or human data are not clearly negative.

Genetics evidence is handled through concept pages for genes, variants, genotypes, and pharmacogenomic markers, then linked into supplement hypotheses through `genetic_context`.

## Practical Translation

Supplement entities also track whether evidence maps to real-world use:

| Field | Meaning |
|-------|---------|
| `translation_plausibility` | Whether studied dose, route, and context are practical for routine human supplementation |
| `replication_status` | Whether the key claim is independently robust or still fragile |
| `claim_scope` | Whether the strongest justified claim is general longevity, condition-specific, biomarker-only, or mechanism-only |

This keeps a positive mechanism or animal result from being treated as a practical stack recommendation when the dose is implausible, the result is unreplicated, or the claim is narrower than the marketing.

## Practical Status

Supplement entities also carry a `practical_status` field. This is separate from evidence level: a supplement can have plausible evidence but still be marked `deprioritize` because the effect is small, population-specific, unsafe in context, or impractical.

| Status | Meaning |
|--------|---------|
| candidate | Worth considering for the stated goals, pending stack fit and safety review |
| consider | Reasonable option when the target outcome/population matches the evidence |
| deprioritize | Not a current priority because evidence is weak, effects are small, or relevance is low |
| avoid | Do not use without a specific reason because risks or contraindications dominate |
| research-only | Interesting mechanistically, but not ready for a practical supplement decision |

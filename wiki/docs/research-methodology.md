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
> Research methodology governing all source gathering, evaluation, and documentation in this wiki. Every research action — ad-hoc or deep pipeline — follows these standards.

See also: [[ingest-checklist]], [[lint-rules]], [[calibration-sweep]], [[schema-canary]]

## Research Tools

This wiki uses two complementary research paths:

| Path | Tool | When to use | Output |
|------|------|-------------|--------|
| **Deep pipeline** | `foundry-research` deep-research | Comprehensive supplement investigation (multi-source, 30 min) | Structured report in `research/<supplement>/` |
| **Ad-hoc** | `/scout` skill | Quick targeted questions, preliminary evidence checks, gap-filling | Preliminary brief in `wiki/scouting/` |
| **Ingest** | `/wiki-ingest` skill | Integrating research or raw sources into the wiki | Wiki pages |
| **Review** | `/wiki-review` skill | Periodic evidence hygiene, queue review, and calibration | Review note in `wiki/reviews/` |

Choose the right tool for the job. Don't use deep research for a single-question lookup. Don't use ad-hoc scouting for a full supplement investigation.

## Operating Loop

Use this loop to keep the wiki current between ingests:

1. Run `python3 wiki/scripts/briefing.py` at session start or before a review.
2. Run `python3 wiki/scripts/lint.py` before structural edits and during reviews.
3. Run `python3 wiki/scripts/backlog_sync.py` to preview content-page gaps and unverified claims that are not yet in [[research-queue]].
4. Use [[evidence-watch]] for future evidence events that should trigger updates.
5. Use `type: decision` pages for stack, dose, start/stop, avoidance, and monitoring decisions that should be revisited.

Monthly reviews should resolve or defer a few research-queue rows and check promotion-queue aging. Quarterly reviews should stress-test practical statuses, stack decisions, and calibration.

## Ingest Granularity

Research reports can be ingested as synthesis sources. Individual primary sources from a report should be promoted into their own source-summary pages only when they anchor a decision-relevant claim:

- Major RCTs, meta-analyses, or systematic reviews that determine evidence level
- Dosing, formulation, pharmacokinetic, or bioavailability anchors
- Safety, contraindication, or interaction anchors
- Contradictions that change a hypothesis status or practical decision
- Claims that directly affect stack inclusion, exclusion, or dose choice
- Genetics claims that affect efficacy, risk, dose, contraindications, or population fit

Do not create source-summary pages for every citation in a report by default. That creates provenance noise and makes the graph harder to use.

## Source Roles and Provenance

The wiki separates **map-building sources** from **claim-bearing sources**. AI-generated research reports are useful for orientation, extraction, contradiction discovery, and deciding what pages should exist. They do not carry final evidentiary weight for practical decisions unless the underlying anchor sources have been checked.

Source role is not evidence type:

- `source_role` answers: **why is this source in the wiki?**
- `evidence_layer` answers: **what kind of evidence does this source contribute?**
- Stream ratings answer: **how strong is the mechanistic, animal, human, or genetics evidence for the claim?**

Keep these separate. A source can be a `primary-anchor` with `evidence_layer: mechanistic`, or a `safety` anchor with `evidence_layer: animal`, or a `synthesis` source with `evidence_layer: mixed`. Do not convert mechanistic evidence into human evidence just because it appears in a high-quality review.

| `source_role` | What it means | Appropriate use |
|---------------|---------------|-----------------|
| `synthesis` | AI research report, broad literature review, or other high-level summary | Build the map, identify claims, find tensions, summarize the state of evidence |
| `primary-anchor` | Direct evidence anchor, including major RCTs, systematic reviews, meta-analyses, large observational studies, or key mechanistic papers | Support evidence levels, effect direction, and important supplement-outcome claims |
| `dosing` | Source that directly anchors dose, form, timing, pharmacokinetics, or bioavailability | Support dosing tables and formulation decisions |
| `safety` | Source that directly anchors adverse effects, contraindications, drug interactions, or population risk | Support safety profile, interaction, and avoid/deprioritize decisions |
| `contradiction` | Source that materially conflicts with a claim, hypothesis, or practical decision | Support debates, nuanced/contradicted hypothesis status, and caution notes |
| `genetics` | Source that changes efficacy, risk, dose, contraindications, or interpretation by genotype or variant | Support genetics concept pages and `genetic_context` fields |
| `background` | Contextual source that does not carry a decision-relevant claim | Define terms, historical context, or non-decision background |

> [!analysis]
> The historical label `primary-anchor` means "non-synthesis evidence anchor" in this wiki. It can include systematic reviews and meta-analyses when they are the best direct evidence for a claim, even though they are not primary studies.

### Decision-Critical Claims

Decision-critical claims cannot rely only on `source_role: synthesis`. A claim is decision-critical if it affects:

- `practical_status`
- `evidence_level`
- `mechanistic_evidence`, `animal_evidence`, `human_evidence`, or `translational_status`
- Dosing, form, timing, pharmacokinetics, or bioavailability
- Safety, contraindications, interactions, or population-specific cautions
- Hypothesis status (`supported`, `contradicted`, or `nuanced`)
- Stack inclusion, exclusion, or dose choice

If a research report contains a decision-critical claim but the anchor source has not been checked, keep the claim out of the decision table or mark it as `[!unverified]` / `[!gap]`. Add it to [[promotion-queue]] so it can be promoted later.

### Claim Callout Rules

- `[!source]` may cite a synthesis source for broad report-level summaries.
- `[!source]` on decision-critical claims should cite at least one non-synthesis anchor source.
- `[!analysis]` is used when the wiki interprets across multiple sources or reasons from mechanisms.
- `[!unverified]` is used when a report surfaces a claim but the underlying anchor source has not been read.
- `[!gap]` is used when the missing anchor changes confidence or blocks a practical decision.

## Evidence Stream Handling

Every supplement-outcome claim should preserve three separate evidence streams:

- **Mechanistic:** target engagement, pathway plausibility, in-vitro data, pharmacology, and biochemical rationale
- **Animal:** whole-organism non-human evidence, including disease models and lifespan/healthspan models
- **Human:** observational evidence, biomarker RCTs, clinical endpoints, safety, and real-world contraindications

A claim can be considered `mechanism-led` when mechanistic evidence is strong, animal/human data are weak or untested, and neither stream shows a clear negative signal. A plausible mechanism should be marked `contradicted` if stronger animal or human evidence is null, harmful, or directionally opposed.

## Genetics Handling

Genetics research belongs in the wiki when it changes supplement relevance, risk, dose, or interpretation. Use concept pages for genes, variants, genotypes, and pharmacogenomic markers. Link them from hypotheses through `genetic_context` and from supplement entities through `primary_genetics`.

For genetics sources, distinguish:

- Association evidence: useful for hypothesis generation, weak for causality
- Mendelian randomization: stronger causal inference, still sensitive to assumptions
- Pharmacogenetic/nutrigenomic evidence: most actionable when tied to supplement response, adverse effects, or dosing
- Mechanistic genetics: useful for pathway understanding, not automatically actionable

## Source Hierarchy

Sources are weighted by evidentiary strength. This hierarchy applies to all research paths.

### Tier 1 — Strongest

| Source Type | Weight | Examples |
|-------------|--------|---------|
| Systematic review / meta-analysis | Highest | Cochrane reviews, umbrella reviews |
| Clinical endpoint RCT | High | Double-blind, placebo-controlled, n>100 |
| Regulatory guidance | High | FDA, EMA monographs |

### Tier 2 — Moderate

| Source Type | Weight | Examples |
|-------------|--------|---------|
| Biomarker RCT | Moderate | Human trial showing biomarker change, not clinical outcome |
| Large observational study | Moderate | Prospective cohort, n>1000, adjusted for confounders |
| Preprint (peer-reviewed journal) | Moderate | Posted to journal, awaiting formal peer review |

### Tier 3 — Suggestive

| Source Type | Weight | Examples |
|-------------|--------|---------|
| Animal study | Low-moderate | Mouse, rat, non-human primate |
| In-vitro study | Low | Cell culture, test tube |
| Small observational study | Low | n<100, uncontrolled |
| Preprint (non-journal) | Low | bioRxiv, medRxiv without journal affiliation |

### Tier 4 — Weak

| Source Type | Weight | Examples |
|-------------|--------|---------|
| Editorial / opinion | Minimal | Author commentary, letter to editor |
| Case report | Minimal | n=1 |
| Industry-funded review | Minimal* | Funded by company that sells the supplement |
| Blog / popular press | Minimal | Health blogs, news articles, podcasts |

> [!analysis]
> *Industry-funded sources are not automatically dismissed but carry a conflict-of-interest flag. The funding source must be disclosed in any claim derived from these. A well-designed industry-funded RCT still outranks an unfunded in-vitro study.

## Recency Preferences

| Topic | Preferred recency | Rationale |
|-------|-------------------|-----------|
| Mechanism of action | 2020+ preferred | Biochemistry is relatively stable |
| Clinical evidence | 2025+ preferred | Trial methodology improves rapidly |
| Safety / interactions | 2025+ preferred | New interactions discovered frequently |
| Dosing recommendations | 2024+ preferred | Formulations and dosing evolve |
| Foundational knowledge | Any date | Established biochemistry, textbook-level facts |

> [!analysis]
> Older sources are acceptable when they are the primary source for a finding. A 2010 RCT that established a dose-response curve is better than a 2025 review that cites it secondhand. Always prefer the primary source.

## Full-Text Reading Standard

**Default: read the full source text.** Abstracts are insufficient for most claims.

### When Abstract-Only Is Acceptable

- Full text is paywalled and no preprint is available
- The claim is narrow and the abstract is specific (e.g., "n=200, dose=500mg, outcome=X")
- The source is being triaged (not yet cited as evidence)

### Mandatory Disclosure

When a claim is derived from an abstract-only reading, the source-summary page and every `[!source]` callout must disclose this:

```
> [!source] Claim text. (abstract only) <source-summary wikilink>
```

Do not omit this tag. It signals reduced confidence — abstracts may not disclose methodological details, conflicts, or null results that the full text would reveal.

## Ad-Hoc Research Conventions

When using the `/scout` skill or manual web search outside the deep pipeline:

1. **Start with academic sources.** Use Google Scholar, PubMed, or Semantic Scholar queries before general web search.
2. **Prioritize primary sources.** Find the original paper, not a review-of-a-review.
3. **Check for retractions.** If citing a paper >2 years old, verify it hasn't been retracted or received a major correction.
4. **Disclose methodology.** Note which databases were searched, how many results were screened, and what was excluded.
5. **Flag limitations.** If the search was incomplete (e.g., only Google Scholar, not PubMed), say so.

## Preprint Handling

Preprints are acceptable as sources with caveats:

- Tag with `preprint` in the source-summary
- Note the server (bioRxiv, medRxiv, etc.) and submission date
- If the preprint is later peer-reviewed and published, update the source-summary to the published version
- Do not weight preprints equal to peer-reviewed sources in evidence assessment

## Industry Funding

When a source has industry funding:

1. Disclose the funding source in the source-summary page
2. Check whether the study design is preregistered (reduces p-hacking risk)
3. Check whether the control group is appropriate (some industry studies use deliberately weak controls)
4. Do not dismiss outright — evaluate the methodology on its merits
5. Add a `[!analysis]` callout noting the conflict when the claim is used in the wiki

## Scouting vs. Deep Research

| Dimension | Scout (`/scout`) | Deep Research |
|-----------|-------------------|---------------|
| Time | 5-10 min | 15-30 min |
| Sources | 3-10 | 20-50+ |
| Depth | Targeted questions | Comprehensive coverage |
| Output | `wiki/scouting/` brief | `research/<supplement>/report.md` |
| Confidence | Preliminary — may surface promising leads | High — multi-source synthesis |
| Next step | Promising → deep research, Dead end → abandon | Ingest into wiki via `/wiki-ingest` |

Scouting is the funnel top. It filters supplements and questions before committing deep research time. Scout findings are explicitly preliminary and live in a separate silo (`wiki/scouting/`) until promoted through deep research and formal ingest.

## Quality Checklist (Per Source)

Before citing any source:

- [ ] Full text read (or abstract-only disclosed)
- [ ] Sample size adequate for claim type
- [ ] Study design appropriate for claim type (RCT for efficacy, not just observational)
- [ ] Population relevant (human > animal > in-vitro for clinical claims)
- [ ] Conflicts of interest checked and disclosed
- [ ] Dose and form match what's being claimed
- [ ] Outcome measure is clinically meaningful (not just a surrogate biomarker, unless disclosed)
- [ ] Recency appropriate for topic
- [ ] Not retracted or corrected

## Documenting Research Limitations

Every research output should include a limitations section:

- Which databases were searched
- How many sources were reviewed
- What was excluded and why
- Language limitations (English-only?)
- Whether full text or abstract-only was used
- Gaps in coverage (topics that should have been searched but weren't)

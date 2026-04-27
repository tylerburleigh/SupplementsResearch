---
name: scout
description: >-
  Quick preliminary research on a supplement or question. Searches for promising
  evidence that might warrant full deep research. Outputs a structured scouting
  brief to wiki/scouting/ — kept separate from the main wiki until promoted
  through deep research and ingest. Use when: "is X worth researching deeper?",
  "what's the preliminary evidence for X?", "/scout taurine cognitive", "should
  I research quercetin?". Do NOT use for comprehensive research (use
  foundry-research deep-research instead) or for wiki ingestion (use wiki-ingest).
---

# scout

You are conducting a quick preliminary investigation of a supplement or health question. The goal is to determine whether something is promising enough to warrant a full deep-research session, not to produce definitive answers.

## Output Silo

All scouting output goes to `wiki/scouting/` — it is **not** part of the main wiki. This keeps preliminary findings separate from ingested, vetted knowledge.

## When to Use

- "Is X worth researching deeper?"
- "What's the preliminary evidence for X?"
- "/scout <supplement>" or "/scout <supplement> <topic>"
- "Should I research quercetin?"
- Quick gap-filling: "what does the literature say about X interaction?"

## When NOT to Use

- Full supplement investigation → use `foundry-research` deep-research
- Ingesting into the wiki → use `/wiki-ingest`
- Answering from existing wiki knowledge → search the wiki first

## Steps

### 1. Read context

- Read `wiki/handoff.md`
- Read `purpose.md`
- Check if the supplement/topic already exists in the wiki (search `wiki/entities/` and `wiki/scouting/`)
- If a scouting brief already exists, offer to update it rather than create a duplicate

### 2. Understand the scope

Parse the user's request into:
- **Subject**: supplement name or topic
- **Angle**: specific outcome, pathway, or question (if specified; otherwise "general promise")
- **Context**: why they're asking (e.g., considering adding to stack, saw a claim, gap from previous research)

If the scope is unclear, ask one focused question — do not present a menu.

### 3. Search (5-10 min equivalent)

Execute a targeted search following the methodology in `wiki/docs/research-methodology.md`:

**Academic-first search:**
- Search PubMed/Google Scholar for recent reviews (2024+) on the subject
- Search for the highest-evidence studies (meta-analyses > RCTs > observational)
- Note study types and sample sizes

**Supplementary search:**
- Check Examine.com for a summary if available
- Check regulatory status (FDA, EMA) if relevant
- Quick safety check — known adverse effects, drug interactions

**Minimum source targets:**
- 1-2 systematic reviews or meta-analyses (if they exist)
- 2-3 primary studies (RCTs preferred)
- 1 safety/interaction source

If fewer than 5 sources are findable, note the scarcity — that itself is a finding.

### 4. Assess promise

Rate the preliminary evidence:

| Rating | Meaning | Next step |
|--------|---------|-----------|
| **High promise** | Multiple RCTs with positive outcomes, clear mechanism, good safety | Recommend deep research + eventual ingest |
| **Moderate promise** | Some human evidence, plausible mechanism, limited but positive data | Recommend deep research to clarify |
| **Low promise** | Mostly animal/in-vitro, weak human data, or mixed results | Flag as low priority; deep research only if specifically interested |
| **Dead end** | Negative RCTs, safety concerns, or no credible human evidence | Do not recommend further research |
| **Insufficient data** | Too few sources to assess | Recommend deep research if the question matters, otherwise deprioritize |

### 5. Write the scouting brief

Create a file in `wiki/scouting/` using this structure:

```markdown
---
type: entity
entity_type: supplement
aliases: []
sources: []
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
status: preliminary
tags:
  - supplement/<name>
  - scouting
---

> [!tldr]
> One-sentence verdict on promise level.

## Promise Rating

**[High / Moderate / Low / Dead end / Insufficient data]**

## Why Investigated

<!-- Brief context on why this was scouted -->

## What We Found

### Evidence Snapshot

| Evidence Level | Count | Key Finding |
|----------------|-------|-------------|
| Meta-analysis/systematic review | | |
| Clinical endpoint RCT | | |
| Biomarker RCT | | |
| Observational | | |
| Animal/in-vitro | | |

### Top 3 Sources

1. **Source 1** — Key finding. [Tier] (full text / abstract only)
2. **Source 2** — Key finding. [Tier] (full text / abstract only)
3. **Source 3** — Key finding. [Tier] (full text / abstract only)

### Mechanism Summary

<!-- 2-3 sentences on known or proposed mechanism -->

### Safety Signal

<!-- Any red flags? Green flags? Unknown? -->

## What's Missing

> [!gap]
> - [ ] What questions remain unanswered
> - [ ] What evidence level is needed to confirm promise

## Recommendation

<!-- Clear recommendation: deep research? deprioritize? specific angle to investigate? -->

## Search Methodology

- Databases searched: [e.g., Google Scholar, PubMed]
- Sources screened: [number]
- Sources read: [number full text, number abstract only]
- Date of search: YYYY-MM-DD
- Limitations: [any gaps in the search]
```

### 6. Present to user

Show the user:
1. Promise rating with brief justification
2. Top finding (one sentence)
3. Recommendation (deep research? deprioritize?)
4. Path to the scouting brief file

### 7. Update handoff

Append a note to `wiki/handoff.md` about the scouting session. Log in `wiki/log.md`.

## Promoting to Deep Research

If the scouting brief rates "High promise" or "Moderate promise" and the user wants to proceed:

1. Use the scouting brief as input to frame the deep-research query
2. The deep-research report supersedes the scouting brief
3. After deep research completes, the scouting brief gets a `superseded-by` frontmatter field pointing to the research report
4. The wiki-ingest skill then ingests from the research report as normal

## Scouting Brief Lifecycle

```
wiki/scouting/<Supplement>.md
  → rated High/Moderate → deep research → wiki-ingest → scouting brief marked superseded
  → rated Low → kept in scouting/ as reference, not promoted
  → rated Dead end → kept in scouting/ with clear "dead end" status
```

Scouting briefs are never directly ingested into the main wiki. They inform deep research queries.

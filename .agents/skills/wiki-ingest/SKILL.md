---
name: wiki-ingest
description: >-
  Ingest a source into the supplements wiki, or re-audit a past ingest. Use for
  foundry-research reports such as "ingest the sulforaphane research" or
  "$wiki-ingest sulforaphane"; arbitrary sources in raw/ such as "ingest the
  source at raw/foo.pdf" or "$wiki-ingest raw/foo.md"; and audit-only mode such
  as "$wiki-ingest --audit-only sulforaphane" or "what did we miss in the
  sulforaphane ingest?" Orchestrates staging, pre-check, repo-local extractor
  and auditor role instructions, and gap-report append. Does not commit to git;
  the human reviews first.
---

# wiki-ingest

## Codex role files

The Claude named agents are mirrored as repo-local Codex role instructions:

- `.codex/agents/wiki-extractor.md`
- `.codex/agents/wiki-auditor.md`

When this workflow reaches extraction or audit, read the relevant role file and follow it as instructions. In Codex, do the work locally unless the user explicitly authorizes subagents or delegated work. If delegation is authorized, spawn a `worker` for extraction or a read-only reviewer for audit and include the role-file contents in the prompt.

You are orchestrating an ingest into the supplements research wiki, or re-auditing a past ingest. The vault root has a `CLAUDE.md` that describes the schema; this skill describes the *workflow* on top of that schema.

## Source types

The vault has two ingestion points:

- **`raw/`** — Arbitrary sources (PDFs, articles, web pages, personal notes). Stage, hash, and optionally convert before extraction.
- **`research/`** — Foundry-research reports (`research/<supplement>/report.md`). Already structured markdown, ready for extraction.

## Modes

- **Full ingest** (default): stage (if raw), pre-check, extract, audit, append gap callout, mark source-summary complete.
- **Audit-only**: skip staging and extraction, run only the auditor. Triggered by `--audit-only`, audit-phrasing, or when a re-ingest detects the source is unchanged.

## When to invoke (full ingest)

- User says "ingest the <supplement> research" or "$wiki-ingest <supplement>" → research path
- User says "ingest the source at <path>" or "$wiki-ingest raw/foo.pdf" → raw path
- User asks to add a paper/article/supplement to the wiki

If the user has not specified a source, ask for one. Do not invent.

## When to invoke (audit-only)

- User says "$wiki-ingest --audit-only <supplement>" or "audit the <supplement> ingest"
- User asks "what did we miss in <supplement>?"
- A re-ingest detects the source is unchanged

## Steps

### 1. Resolve source and mode

Determine the source type and path:

- **Research source**: user references a supplement name. Source is `research/<supplement>/report.md`.
- **Raw source**: user provides a path in `raw/`. Source is the file at that path.

Compute SHA256 for the source that `raw_path` will point to:

```bash
shasum -a 256 <raw_path>
```

For research reports, `raw_path` is `research/<supplement>/report.md` and `raw_hash` is the SHA256 of that report file.

If a matching source-summary exists with `ingest_status: in-progress`, pause before extraction and tell the user the ingest is resumable. Offer two choices: resume from the existing source-summary and linked pages, or restart by treating the current source as a fresh ingest. Do not create a second source-summary for the same unchanged source unless the user chooses restart.

**Audit-only path** (skip to step 6) when:
- User passed `--audit-only` or used audit-phrasing
- A source-summary already exists with `ingest_status: complete` and the source hasn't changed (hash match)

**Full-ingest path** (steps 2-7) otherwise.

### 2. Stage the source (raw sources only)

Skip this step for research sources — they're already structured markdown.

For raw sources:
- If the source is a PDF: convert to markdown via `pymupdf4llm`. Store the converted `.md` alongside the original in `raw/`. The original PDF is the immutable artifact.
  ```bash
  python -c "import pymupdf4llm; open('raw/<name>.md','w').write(pymupdf4llm.to_markdown('raw/<name>.pdf'))"
  ```
- If the source is already markdown: read from its location in `raw/`.
- Compute SHA256 of the **original** file:
  ```bash
  shasum -a 256 raw/<name>.<ext>
  ```
- If a source-summary already exists, compare the new hash to the stored `raw_hash`:
  - **Match** → switch to audit-only path
  - **Mismatch** → ask the user whether to refresh or treat as new

Note today's date in ISO 8601.

### 3. Read context (full ingest)

- Read `CLAUDE.md` at the vault root.
- Read `purpose.md` for research direction.
- Read `wiki/docs/graph-protocol.md` to understand how new pages should connect to existing ones.
- Read the source end to end.

### 4. Present the pre-check (full ingest)

Show the user, before any pages are written:

1. **Source** — citation or supplement name, source type (research report vs. external source).
2. **Key takeaways** — 4-8 substantive claims you'd extract, with evidence levels where applicable.
3. **Planned new pages** — entities/, concepts/, sources/, hypotheses/, comparisons/, stacks/, decisions/. For each, the filename (Title Case) and a one-line note.
4. **Existing pages to update** — search `wiki/` for overlapping entities and concepts.
5. **Evidence streams** — separate mechanistic, animal, and human signals; flag blocking negative evidence.
6. **Genetics context** — genes, variants, genotypes, or pharmacogenomic markers that affect relevance, risk, dose, or interpretation.
7. **Primary-anchor sources** — cited primary sources to promote into their own source-summary pages because they anchor evidence level, dosing, safety, genetics, contradictions, or stack decisions. Do not promote every citation by default.
8. **Potential contradictions** — claims in the source that disagree with existing wiki content.
9. **Hypothesis review plan** — for any planned hypothesis page, the `review_by` date and what would change if supported or contradicted.
10. **Stack relevance and decisions** — how this source might affect existing/planned stacks and whether it warrants a practical decision page.
11. **Graph connectivity** — confirm every planned new page has at least one incoming link from another planned or existing page (no orphans), and every planned new page links out to at least one other page (no dead ends). If any page would be isolated, say so.

End with: "Proceed?"

If the user has set batch mode ("skip the pre-check"), skip this step.

### 5. Extract (full ingest only — role file: `.codex/agents/wiki-extractor.md`)

On approval, read `.codex/agents/wiki-extractor.md` and follow it for extraction. If the user explicitly authorized delegated work, spawn a `worker` and pass a single message containing:

- `source_path` — path to the markdown form of the source
- `raw_path` — path to the original file (for raw sources: the PDF or original; for research: the report path)
- `raw_hash` — SHA256 of `raw_path`
- `source_type` — "research" or "raw"
- `today_iso` — today's date
- `purpose_md` contents (verbatim)
- The approved `plan` (the pre-check structure condensed)

Use the extractor's structured report as the handoff artifact. If you performed extraction locally, produce the same structured report for the audit step.

If the extractor reports `surprises`, present them to the user before invoking the auditor.

### 6. Audit (both paths — role file: `.codex/agents/wiki-auditor.md`)

Read `.codex/agents/wiki-auditor.md` and follow it **independently** — do not rely on extractor reasoning. If the user explicitly authorized delegated work, spawn a read-only reviewer and pass only the audit inputs below.

For the **full-ingest path**, pass:
- `source_path`
- `source_summary_path` (from extractor output)
- `pages_created` (paths only)
- `pages_updated` (paths plus `what_changed` summary)
- `today_iso`

For the **audit-only path**:
- Derive the source-summary path.
- Find all wiki pages whose `sources` frontmatter links to this source-summary.
- Pass the full page list.

Wait for the auditor's gap report.

### 7. Append the gap report to the source-summary

Edit the source-summary page. Add or replace a `[!gap] Extraction coverage of this ingest (self-audit, <today_iso>)` callout. If a prior audit exists, replace it (do not stack stale audits).

Then set the source-summary frontmatter to `ingest_status: complete`. A source-summary remains `in-progress` only when extraction or audit stops before this step.

### 7.5. Do not fix gaps inline

The skill produces pages plus a gap callout. It does not fix pages in response to the gap list. Those are human-triaged.

Exception: surface attribution-mismatch findings prominently.

### 8. Summarize to the user

Show:

- Source path and type
- (Full ingest) Pages created, pages updated, catalog/log/synthesis updates confirmed
- (Audit-only) Number of linked pages audited
- Auditor's gap report inline
- A reminder to commit when ready (do **not** auto-commit)

### 9. Wait for human

Do not commit, do not run lint, do not start a follow-on ingest. The human reviews.

## Error handling

- **Source not found**: stop, list what's available and ask the user to clarify.
- **`pymupdf4llm` not installed** (raw PDF): stop, instruct `pip install pymupdf4llm`.
- **Source already ingested and unchanged with `ingest_status: complete`**: switch to audit-only. Tell the user.
- **Source-summary exists with `ingest_status: in-progress`**: offer resume or restart. Resume should audit the existing linked pages and complete the source-summary after the gap report is appended.
- **Hash mismatch during audit-only**: the source has changed. Recommend full re-ingest.

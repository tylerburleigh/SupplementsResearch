---
name: wiki-lint
description: Health-check the supplements wiki structurally and conceptually. Use when the user says "lint the wiki", asks whether the vault is clean, asks for maintenance findings, or wants low-risk structural fixes. Runs deterministic lint first, then performs targeted judgment-dependent review. Does not commit to git.
---

# wiki-lint

Use this skill to find drift before it compounds: schema drift, broken
links, source hash drift, missing provenance, stale claims, research-queue
items, and evidence-watch events that need triage.

## Steps

### 1. Read Context

- Read `wiki/handoff.md`.
- Read `CLAUDE.md`, especially the Lint guidance and source-role rules.
- Read `wiki/lint-rules.md`.
- Read `wiki/catalog.md` if present; otherwise use `wiki/index.md`.
- Read the tail of `wiki/log.md`.

### 2. Run Deterministic Lint

Run:

```bash
python3 wiki/scripts/lint.py
```

If the only issue is a missing or stale static catalog, rebuild it:

```bash
python3 wiki/scripts/lint.py --rebuild-catalog
python3 wiki/scripts/lint.py
```

Lead with errors before warnings. Do not do conceptual review until
structural errors are understood.

### 3. Judgment-Dependent Review

After deterministic lint, check what the script cannot fully decide:

- **Sampled claim audit.** Trace 2-3 `[!source]` callouts back to their
  source-summary and raw/research source.
- **Decision-critical provenance.** Check whether practical status,
  dosing, safety, evidence level, hypothesis status, or stack decisions
  rely only on `source_role: synthesis`.
- **Promotion queue.** Read `wiki/sources/promotion-queue.md`; flag old
  open rows and rows blocking decisions.
- **Research queue.** Read `wiki/research-queue.md`; note overdue open
  rows and rows that should be resolved, deferred, or promoted.
- **Evidence watch.** Read `wiki/evidence-watch.md`; note overdue events
  that should trigger hypothesis or decision updates.
- **Backlog.** Read `wiki/research-backlog.md`; note open gaps, stale
  pages, and thinly sourced areas.
- **Handoff currency.** Note if `wiki/handoff.md` does not reflect recent
  operation-log work.
- **Graph weak spots.** Check whether high-value pages have reciprocal
  source-summary, hypothesis, and relationship links.

Name specific files and claims. Avoid generic maintenance advice.

### 4. Present Findings

Report in this order:

1. Deterministic lint errors and warnings.
2. Attribution or provenance risks from sampled claims.
3. Decision-critical claims that need non-synthesis anchors.
4. Research queue, evidence watch, promotion queue, stale, or graph weak spots.

For each finding, include the path and the smallest useful fix.

### 5. Apply Only With Approval

Without approval:

- Do not edit content pages.
- You may append a log entry summarizing the lint pass and audited claim
  references if the user asked for a formal lint run.

With approval or explicit apply wording:

- Apply only approved fixes.
- Prefer mechanical fixes first: frontmatter, tags, link repairs,
  catalog rebuild, stale status updates with clear rationale.
- Route source-grounded claim repair to `/wiki-repair` unless the user
  explicitly asked to fix it in this lint pass.
- Route changed-source refresh to `/wiki-ingest`.

### 6. Close Out

Summarize:

- Whether deterministic lint passes.
- Which claims were audited.
- Which fixes were applied or deferred.
- Whether catalog/log/handoff were updated.
- Whether the wiki is clean enough for the next ingest or query.

Do not commit to git.

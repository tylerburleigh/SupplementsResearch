---
name: wiki-review
description: Run a periodic supplements wiki review. Use when the user says "run a wiki review", "monthly review", "quarterly review", "review the supplements vault", or asks what needs attention beyond a single ingest/query.
---

# /wiki-review

Run a structured review of the supplements wiki. This is an evidence-hygiene workflow, not a new-source ingest.

## Step 1 - Determine Scope

Use the period the user requested. If ambiguous:

| Period | Depth | Default purpose |
|--------|-------|-----------------|
| weekly | Light | Check queue/watch items and recent session continuity |
| monthly | Full | Lint, queue, primary-anchor promotion, synthesis hygiene |
| quarterly | Deep | Stress-test practical posture, stack decisions, and calibration |

## Step 2 - Local Pre-Work

Run:

```bash
python3 wiki/scripts/briefing.py
python3 wiki/scripts/lint.py
python3 wiki/scripts/backlog_sync.py
```

If deterministic lint has errors, fix those before writing a review note. Warnings can become review agenda items.

## Step 3 - Review Agenda

For all periods:

- Read `wiki/handoff.md`, `wiki/synthesis.md`, `wiki/research-queue.md`, and `wiki/evidence-watch.md`.
- Check overdue `review_by` dates on hypothesis and decision pages.
- Check `wiki/sources/promotion-queue.md` for old decision-critical claims without anchors.
- Run `python3 wiki/scripts/backlog_sync.py --apply` only when the user wants new gap/unverified callouts added to the queue.

Monthly adds:

- Resolve or defer 1-3 `wiki/research-queue.md` rows.
- Promote high-priority source anchors from `wiki/sources/promotion-queue.md`.
- Refresh `wiki/synthesis.md` if the practical posture changed.

Quarterly adds:

- Re-read active stack pages and practical decision pages.
- Stress-test `practical_status` on supplement entities.
- Run the calibration sweep in `wiki/docs/calibration-sweep.md`.
- Reconcile stale or superseded hypotheses and decisions.

## Step 4 - Write Review Note

Create `wiki/reviews/YYYY-MM-DD-{period}.md` from `templates/review.md`.

Fill in:

- Briefing summary
- Lint findings
- Queue changes
- Evidence-watch updates
- Hypotheses/decisions reviewed
- Synthesis or stack updates needed
- Action items

## Step 5 - Post-Work

- Update any touched pages' `updated:` date.
- Rebuild `wiki/catalog.md` if content pages changed.
- Append `wiki/log.md`.
- Update `wiki/handoff.md`.
- Report changed files and verification commands.

## Constraints

- Do not ingest new sources during the review unless the user explicitly turns the review into an ingest.
- Do not change a practical decision without a decision note when the change affects stack membership, dose, avoidance, or monitoring.
- Do not close a research-queue item unless the target page has been updated or the item is explicitly deferred.

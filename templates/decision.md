---
type: decision
decision_type: "stack-change"  # stack-change | dose-change | start-stop | safety | monitoring
action: ""  # start | stop | continue | change-dose | avoid | defer | pause | resume | monitor
decision_status: active  # active | closed | superseded
supplements: []
related_stack: ""
sources: []
created: "{{date}}"
updated: "{{date}}"
status: current
review_by: ""
closed: ""
tags: []
---

> [!tldr]
> One-sentence summary of the supplement or stack decision.

# Decision: {{action}} {{supplement_or_stack}} - {{date}}

## What

Concrete action: what changes, dose/form/timing if relevant, and whether this is a trial, permanent addition, pause, or avoidance decision.

## Why

> [!analysis] Decision rationale
> Explain the reasoning from the wiki evidence, personal fit, safety, interactions, and practical constraints. Link relevant entity, dosing, stack, hypothesis, and source-summary pages.

## What Would Change My Mind

- **Would reverse:** Specific evidence, side effect, lab result, interaction, or better alternative that would reverse the decision.
- **Would strengthen:** Specific evidence or personal outcome that would increase confidence.
- **Review by:** Date from `review_by` frontmatter.

## Supporting Evidence

- Entity:
- Dosing:
- Safety:
- Interactions:
- Hypotheses:
- Source summaries:

## Follow-Up

- [ ] Revisit on or before `review_by`.

## Outcome

Fill in when `decision_status` changes to `closed` or `superseded`: what happened, what changed, and what the wiki should learn.

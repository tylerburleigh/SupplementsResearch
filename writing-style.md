# Writing Style Reference

The agent reads this for detail and examples when drafting or revising wiki pages. The short rules in CLAUDE.md are the operational summary; this file is the long form.

## Funnel structure

Each document, section, and paragraph flows from broad to narrow: result first, then context, then detail. A reader who stops at any point should have the most important information so far.

- **Page level:** The `[!tldr]` states the key takeaway. Body expands: context → claims → open questions.
- **Section level:** Open with the conclusion, then support it.
- **Paragraph level:** Lead with the point, then explain.

## Plain language

Prefer concrete, everyday words over academic phrasing.

| Instead of | Write |
|---|---|
| "demonstrates efficacy" | "works" |
| "exhibits bioavailability" | "is absorbed" |
| "ameliorates" | "improves" or "reduces" |
| "in vivo" | "in animals" or "in living organisms" |
| "in vitro" | "in cells" or "in a test tube" |
| "suboptimal" | "low" or "not ideal" |
| "elucidate" | "show" or "explain" |

Retain technical terms where they are the standard vocabulary (Nrf2, mTOR, bioavailability, pharmacokinetics). Replace jargon that has a plain-language equivalent.

## Short sentences

If a sentence has more than one clause doing real work, split it.

Before:
> Sulforaphane modifies critical cysteine thiols on Keap1, disrupting the ubiquitin-proteasomal degradation of Nrf2, which allows newly synthesized Nrf2 to enter the nucleus and activate antioxidant response element-dependent genes.

After:
> Sulforaphane modifies cysteine residues on Keap1. This stops Keap1 from tagging Nrf2 for degradation. Free Nrf2 enters the nucleus and activates over 200 protective genes.

## Avoid hedging stacks

One qualifier is fine. Stacking dilutes the point.

Before: "It may potentially suggest that supplementation could possibly reduce inflammation."

After: "This suggests supplementation reduces inflammation."

Be direct about limitations: state them plainly rather than burying them in hedged language.

## Define technical terms on first use per page

Wiki pages are read standalone. Spell out on first mention — "nuclear factor erythroid 2-related factor 2 (Nrf2)" — then use the abbreviation. This applies to pathway names, chemical classes, and assay names.

## Name recurring concepts

When a pattern is referenced across sections or pages, give it a compact label on first introduction ("the inverted pyramid of evidence," "the pro-survival paradox"). Later references can use the shorthand without re-explaining.

## State assumptions explicitly

List assumptions up front in a bullet list rather than embedding them in prose. This applies to `[!analysis]` callouts, stack pages, and comparison pages especially.

## For evidence assessment

- **Lead with the evidence level.** "Biomarker RCT evidence (Level 3) shows..." not burying the evidence quality in a footnote.
- **Separate mechanistic plausibility from clinical evidence.** A plausible mechanism does not equal clinical proof.
- **Distinguish surrogate endpoints from clinical endpoints.** "Lowered inflammatory biomarkers" is not the same as "reduced cardiovascular events."
- **State null results explicitly.** If trials showed biomarker changes without clinical improvement, say so.

## For stack and dosing pages

- **Translate findings into practical implications.** Don't just restate results — say what dose, what form, what timing.
- **Qualify cross-source comparisons.** Note when doses, forms, or populations differ between studies.
- **Flag interactions prominently.** A supplement that helps one pathway but harms another needs that tension front and center.

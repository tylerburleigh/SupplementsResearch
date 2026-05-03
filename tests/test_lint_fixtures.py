from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
LINT = REPO_ROOT / "wiki/scripts/lint.py"


def run_lint(vault: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(LINT), "--vault", str(vault), *args],
        check=False,
        text=True,
        capture_output=True,
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_in(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"fixture text not found in {path}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def make_clean_vault(root: Path) -> Path:
    (root / "CLAUDE.md").write_text(
        (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    report_body = "Fixture report body.\n"
    report_hash = hashlib.sha256(report_body.encode("utf-8")).hexdigest()
    write(root / "research/test/report.md", report_body)

    write(
        root / "wiki/sources/Test Report.md",
        f"""---
type: source-summary
sources: []
created: "2026-04-27"
updated: "2026-04-27"
status: current
tags: []
raw_path: "research/test/report.md"
raw_hash: "{report_hash}"
ingest_status: complete
study_type: research-report
source_role: synthesis
evidence_layer: mixed
reading_status: report-derived
decision_relevance: high
anchor_for:
  - efficacy
---

> [!tldr]
> Test report fixture.

## Entities Mentioned

[[Test Supplement]]

## Concepts Covered

[[Healthy Aging]]
""",
    )

    write(
        root / "wiki/entities/Test Supplement.md",
        """---
type: entity
sources:
  - "[[Test Report]]"
created: "2026-04-27"
updated: "2026-04-27"
status: current
tags:
  - supplement/test
entity_type: supplement
aliases: []
evidence_level: 1
mechanistic_evidence: weak
animal_evidence: none
human_evidence: untested
translational_status: insufficient
practical_status: research-only
translation_plausibility: unknown
replication_status: unknown
claim_scope: unknown
primary_outcomes:
  - "[[Healthy Aging]]"
primary_pathways: []
primary_genetics: []
---

> [!tldr]
> Test supplement fixture.

## What It Is

> [!source]
> Test supplement appears in the report. [[Test Report]]

## Relationships

> [!analysis]
> Links to [[Healthy Aging]] because the report frames it as the outcome.
""",
    )

    write(
        root / "wiki/concepts/Healthy Aging.md",
        """---
type: concept
sources:
  - "[[Test Report]]"
created: "2026-04-27"
updated: "2026-04-27"
status: current
tags:
  - outcome/longevity
concept_type: outcome
domain: longevity
---

> [!tldr]
> Healthy aging fixture.

## Definition

> [!source]
> The report names healthy aging as the target outcome. [[Test Report]]

## Connections

> [!analysis]
> [[Test Supplement]] links to this outcome through the fixture report.
""",
    )
    write(
        root / "wiki/research-queue.md",
        """---
type: meta
sources: []
created: "2026-04-27"
updated: "2026-04-27"
status: current
tags:
  - meta
---

> [!tldr]
> Research queue fixture.

See also: [[catalog]]

## Open

| # | Question | Source Page | Surfaced From | Priority | Review By | Status | Resolution |
|---|----------|-------------|---------------|:--------:|-----------|:------:|------------|

## Resolved

| # | Question | Source Page | Surfaced From | Priority | Review By | Status | Resolution |
|---|----------|-------------|---------------|:--------:|-----------|:------:|------------|
""",
    )
    write(
        root / "wiki/evidence-watch.md",
        """---
type: meta
sources: []
created: "2026-04-27"
updated: "2026-04-27"
status: current
tags:
  - meta
---

> [!tldr]
> Evidence watch fixture.

See also: [[catalog]]

## Upcoming

| Date | Event | Target | Hypothesis / Decision | Status |
|------|-------|--------|-----------------------|--------|

## Evaluated

| Date | Event | Target | Hypothesis / Decision | Status |
|------|-------|--------|-----------------------|--------|
""",
    )
    rebuilt = run_lint(root, "--rebuild-catalog")
    if rebuilt.returncode != 0:
        raise AssertionError(rebuilt.stdout + rebuilt.stderr)
    return root


class LintFixtureTests(unittest.TestCase):
    def assert_finding(
        self,
        mutate: Callable[[Path], None],
        message: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            mutate(vault)
            result = run_lint(vault)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn(message, output)

    def test_clean_fixture_passes_real_linter(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            result = run_lint(vault)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_inline_code_wikilinks_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            replace_in(
                vault / "wiki/concepts/Healthy Aging.md",
                "## Connections\n",
                "## Connections\n\nExample syntax: `[[Missing Inline Example]]`.\n",
            )
            result = run_lint(vault)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_real_unresolved_wikilink_is_reported(self) -> None:
        self.assert_finding(
            lambda v: replace_in(
                v / "wiki/concepts/Healthy Aging.md",
                "[[Test Supplement]] links to this outcome",
                "[[Missing Page]] links to this outcome",
            ),
            "unresolved wikilink `[[Missing Page]]`",
        )

    def test_frontmatter_link_type_mismatch_is_reported(self) -> None:
        self.assert_finding(
            lambda v: replace_in(
                v / "wiki/entities/Test Supplement.md",
                '  - "[[Healthy Aging]]"',
                '  - "[[Test Supplement]]"',
            ),
            "`primary_outcomes` wikilink `[[Test Supplement]]` must target",
        )

    def test_hash_drift_is_reported(self) -> None:
        self.assert_finding(
            lambda v: write(v / "research/test/report.md", "Changed report body.\n"),
            "stale raw_hash for research/test/report.md",
        )

    def test_source_callout_must_cite_source_summary(self) -> None:
        self.assert_finding(
            lambda v: replace_in(
                v / "wiki/entities/Test Supplement.md",
                "Test supplement appears in the report. [[Test Report]]",
                "Test supplement appears in the report. [[Healthy Aging]]",
            ),
            "[!source] callout lacks a source-summary wikilink",
        )

    def test_rebuild_catalog_generates_static_agent_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            result = run_lint(vault, "--rebuild-catalog")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            catalog = (vault / "wiki/catalog.md").read_text(encoding="utf-8")
            self.assertIn("[[Test Supplement]]", catalog)
            self.assertIn("[[Healthy Aging]]", catalog)
            self.assertIn("[[Test Report]]", catalog)

            linted = run_lint(vault)
            self.assertEqual(linted.returncode, 0, linted.stdout + linted.stderr)

    def test_catalog_links_do_not_satisfy_orphan_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            replace_in(
                vault / "wiki/sources/Test Report.md",
                "\n[[Healthy Aging]]\n",
                "\n",
            )
            replace_in(
                vault / "wiki/entities/Test Supplement.md",
                "Links to [[Healthy Aging]] because",
                "Links to the outcome because",
            )

            result = run_lint(vault)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn("orphan content page has no incoming wikilinks", output)

    def test_stale_catalog_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            replace_in(
                vault / "wiki/catalog.md",
                "Test supplement fixture.",
                "Outdated catalog text.",
            )

            result = run_lint(vault)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn("static catalog is stale", output)

    def test_missing_catalog_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            (vault / "wiki/catalog.md").unlink()

            result = run_lint(vault)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn("static catalog is missing", output)

    def test_query_pages_are_first_class_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            write(
                vault / "wiki/queries/Test Query.md",
                """---
type: query
sources:
  - "[[Test Report]]"
created: "2026-04-27"
updated: "2026-04-27"
status: current
tags: []
---

> [!tldr]
> Query fixture answer.

## Answer

> [!source]
> The answer cites the fixture report. [[Test Report]]

## Links

> [!analysis]
> This query links back to [[Test Supplement]].
""",
            )
            rebuilt = run_lint(vault, "--rebuild-catalog")
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stdout + rebuilt.stderr)

            catalog = (vault / "wiki/catalog.md").read_text(encoding="utf-8")
            self.assertIn("## Queries", catalog)
            self.assertIn("[[Test Query]]", catalog)

            result = run_lint(vault)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_decision_pages_are_first_class_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = make_clean_vault(Path(tmpdir))
            replace_in(
                vault / "wiki/sources/Test Report.md",
                "## Entities Mentioned\n",
                "## Entities Mentioned\n\n[[Test Decision]]\n",
            )
            write(
                vault / "wiki/decisions/Test Decision.md",
                """---
type: decision
decision_type: stack-change
action: start
decision_status: active
supplements:
  - "[[Test Supplement]]"
related_stack: ""
sources:
  - "[[Test Report]]"
created: "2026-04-27"
updated: "2026-04-27"
status: current
review_by: "2026-05-27"
closed: ""
tags: []
---

> [!tldr]
> Decision fixture.

## What

Start [[Test Supplement]] as a fixture decision.

## Why

> [!source]
> The report supports considering the fixture supplement. [[Test Report]]

## What Would Change My Mind

Evidence against [[Test Supplement]].

## Outcome

Pending.
""",
            )
            rebuilt = run_lint(vault, "--rebuild-catalog")
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stdout + rebuilt.stderr)

            catalog = (vault / "wiki/catalog.md").read_text(encoding="utf-8")
            self.assertIn("## Decisions", catalog)
            self.assertIn("[[Test Decision]]", catalog)

            result = run_lint(vault)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_hypothesis_requires_review_plan_fields(self) -> None:
        self.assert_finding(
            lambda v: write(
                v / "wiki/hypotheses/Test Hypothesis.md",
                """---
type: hypothesis
supplements:
  - "[[Test Supplement]]"
pathways:
  - "[[Healthy Aging]]"
outcomes:
  - "[[Healthy Aging]]"
population: "general adults"
genetic_context: "general"
evidence_level: 1
mechanistic_evidence: weak
animal_evidence: none
human_evidence: untested
translational_status: insufficient
effect_direction: unknown
hypothesis_status: open
sources:
  - "[[Test Report]]"
created: "2026-04-27"
updated: "2026-04-27"
status: current
tags: []
---

> [!tldr]
> Hypothesis fixture.

## Claim

[[Test Supplement]] might affect [[Healthy Aging]].

## Supporting Evidence

> [!source]
> The report names the relationship. [[Test Report]]
""",
            ),
            "missing `review_by` frontmatter",
        )


if __name__ == "__main__":
    unittest.main()

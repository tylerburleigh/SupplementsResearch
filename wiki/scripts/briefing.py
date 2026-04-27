#!/usr/bin/env python3
"""Print a compact local briefing for the supplements wiki.

Reads local files only. No web calls and no Obsidian dependency.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import lint as wiki_lint


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
CALLOUT_RE = re.compile(r"^>\s*\[!(gap|unverified)\]", re.IGNORECASE)
REVIEW_PERIODS = ("weekly", "monthly", "quarterly")


def parse_today(value: str | None) -> dt.date:
    if value is None:
        return dt.date.today()
    return dt.date.fromisoformat(value)


def section(title: str, lines: list[str]) -> list[str]:
    out = [title.upper()]
    out.extend(f"  {line}" for line in lines)
    return out


def frontmatter_for(path: Path) -> dict[str, object]:
    parsed = wiki_lint.parse_frontmatter(path.read_text(encoding="utf-8"))
    return parsed[0] if parsed else {}


def purpose_lines() -> list[str]:
    path = ROOT / "purpose.md"
    if not path.exists():
        return ["WARN purpose.md missing"]
    text = path.read_text(encoding="utf-8")
    lines: list[str] = []
    if "TBD" in text:
        lines.append("WARN purpose.md still contains TBD fields")
    else:
        lines.append("OK purpose.md has no TBD placeholders")
    return lines


def review_lines(today: dt.date) -> list[str]:
    reviews_dir = WIKI / "reviews"
    last: dict[str, dt.date | None] = {period: None for period in REVIEW_PERIODS}
    if reviews_dir.exists():
        for path in reviews_dir.glob("*.md"):
            if path.name == "README.md":
                continue
            fm = frontmatter_for(path)
            period = fm.get("review_period") or fm.get("period")
            created = fm.get("created") or fm.get("date")
            if period not in last or not isinstance(created, str):
                continue
            try:
                review_date = dt.date.fromisoformat(created)
            except ValueError:
                continue
            if last[period] is None or review_date > last[period]:
                last[period] = review_date

    lines: list[str] = []
    thresholds = {"weekly": 7, "monthly": 31, "quarterly": 92}
    for period in REVIEW_PERIODS:
        review_date = last[period]
        if review_date is None:
            severity = "WARN" if period in {"monthly", "quarterly"} else "INFO"
            lines.append(f"{severity} no {period} review on file")
            continue
        age = (today - review_date).days
        severity = "WARN" if age > thresholds[period] else "OK"
        lines.append(f"{severity} last {period} review: {review_date} ({age}d ago)")
    return lines


def lint_lines() -> list[str]:
    findings = wiki_lint.run_checks(False)
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warn"]
    lines = [f"{'OK' if not errors else 'ERROR'} deterministic lint: {len(errors)} error(s), {len(warnings)} warning(s)"]
    for finding in errors[:5]:
        lines.append(f"ERROR {finding.path}: {finding.message}")
    if not errors:
        for finding in warnings[:5]:
            lines.append(f"WARN {finding.path}: {finding.message}")
    return lines


def callout_lines() -> list[str]:
    counts = {"gap": 0, "unverified": 0}
    pages_with_callouts: set[str] = set()
    for page in wiki_lint.load_pages():
        if page.type == "meta":
            continue
        for line in wiki_lint.stripped_body(page.body).splitlines():
            match = CALLOUT_RE.match(line)
            if not match:
                continue
            counts[match.group(1).lower()] += 1
            pages_with_callouts.add(page.rel)
    return [
        f"Open content callouts: {counts['gap']} gap(s), {counts['unverified']} unverified across {len(pages_with_callouts)} page(s)"
    ]


def parse_table(path: Path, expected_cells: int) -> list[list[str]]:
    if not path.exists():
        return []
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = wiki_lint.split_table_row(line)
        if len(cells) != expected_cells or not cells[0] or cells[0] in {"#", "Date"}:
            continue
        if wiki_lint.is_separator_row(cells):
            continue
        rows.append(cells)
    return rows


def queue_lines(today: dt.date) -> list[str]:
    rows = parse_table(WIKI / "research-queue.md", 8)
    open_rows = [row for row in rows if row[6] == "open"]
    overdue = [
        row for row in open_rows
        if wiki_lint.is_iso_date(row[5]) and dt.date.fromisoformat(row[5]) < today
    ]
    lines = [f"Research queue: {len(open_rows)} open, {len(overdue)} overdue"]
    for row in overdue[:5]:
        lines.append(f"WARN {row[0]} due {row[5]}: {row[1]}")
    return lines


def evidence_watch_lines(today: dt.date) -> list[str]:
    rows = parse_table(WIKI / "evidence-watch.md", 5)
    unchecked = [row for row in rows if "- [ ]" in row[4] and wiki_lint.is_iso_date(row[0])]
    overdue = [row for row in unchecked if dt.date.fromisoformat(row[0]) < today]
    upcoming = [
        row for row in unchecked
        if today <= dt.date.fromisoformat(row[0]) <= today + dt.timedelta(days=30)
    ]
    lines = [f"Evidence watch: {len(upcoming)} upcoming in 30d, {len(overdue)} overdue"]
    for row in overdue[:5]:
        lines.append(f"WARN overdue {row[0]}: {row[1]}")
    for row in upcoming[:5]:
        lines.append(f"INFO upcoming {row[0]}: {row[1]}")
    return lines


def hypothesis_lines(today: dt.date) -> list[str]:
    due: list[tuple[str, str, str]] = []
    upcoming: list[tuple[str, str, str]] = []
    for page in wiki_lint.load_pages():
        if page.type != "hypothesis" or page.frontmatter.get("hypothesis_status") != "open":
            continue
        review_by = page.frontmatter.get("review_by")
        if not isinstance(review_by, str) or not wiki_lint.is_iso_date(review_by):
            due.append((page.path.stem, "missing", "review_by missing or invalid"))
            continue
        review_date = dt.date.fromisoformat(review_by)
        item = (page.path.stem, review_by, "")
        if review_date < today:
            due.append(item)
        elif review_date <= today + dt.timedelta(days=30):
            upcoming.append(item)
    lines = [f"Hypotheses: {len(due)} due, {len(upcoming)} due within 30d"]
    for name, review_by, note in due[:5]:
        suffix = f" ({note})" if note else ""
        lines.append(f"WARN {name}: {review_by}{suffix}")
    for name, review_by, _ in upcoming[:5]:
        lines.append(f"INFO {name}: review by {review_by}")
    return lines


def source_lines() -> list[str]:
    pages = wiki_lint.load_pages()
    in_progress = [
        page.rel for page in pages
        if page.type == "source-summary" and page.frontmatter.get("ingest_status") == "in-progress"
    ]
    stale = wiki_lint.check_staleness(pages)
    lines = [f"Sources: {len(in_progress)} in-progress source summary page(s), {len(stale)} hash issue(s)"]
    for rel in in_progress[:5]:
        lines.append(f"INFO in progress: {rel}")
    for finding in stale[:5]:
        lines.append(f"{finding.severity.upper()} {finding.path}: {finding.message}")
    return lines


def priority_lines() -> list[str]:
    path = ROOT / "research-priority.md"
    if not path.exists():
        return ["WARN research-priority.md missing"]
    in_queue = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "## Priority Queue":
            in_queue = True
            continue
        if in_queue and stripped.startswith("## "):
            break
        if in_queue and re.match(r"\d+\.\s+\*\*", stripped):
            return [f"Next priority: {stripped}"]
    return ["INFO no priority queue item found"]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Print a local supplements wiki briefing.")
    parser.add_argument("--today", default=None, help="override today as YYYY-MM-DD")
    args = parser.parse_args(argv)

    today = parse_today(args.today)
    output: list[str] = [f"Supplements Wiki Briefing - {today.isoformat()}", "=" * 48]
    for title, lines in (
        ("Purpose", purpose_lines()),
        ("Reviews", review_lines(today)),
        ("Lint", lint_lines()),
        ("Gaps", callout_lines()),
        ("Research Queue", queue_lines(today)),
        ("Evidence Watch", evidence_watch_lines(today)),
        ("Hypotheses", hypothesis_lines(today)),
        ("Sources", source_lines()),
        ("Priority", priority_lines()),
    ):
        output.extend(["", *section(title, lines)])
    print("\n".join(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

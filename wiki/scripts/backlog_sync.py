#!/usr/bin/env python3
"""Sync content-page gap/unverified callouts into wiki/research-queue.md.

Usage:
    python3 wiki/scripts/backlog_sync.py
    python3 wiki/scripts/backlog_sync.py --apply
    python3 wiki/scripts/backlog_sync.py --today 2026-04-27

Exit codes:
    0 = queue already matches content callouts
    1 = new queue rows are available or were applied
    2 = failure
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import lint as wiki_lint


ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "wiki" / "research-queue.md"
TRACKED_TYPES = {
    "entity",
    "concept",
    "source-summary",
    "comparison",
    "hypothesis",
    "stack",
    "decision",
    "dosing",
    "query",
}
CALLOUT_RE = re.compile(r"^>\s*\[!(gap|unverified)\]([^\n]*)", re.IGNORECASE)
QUEUE_ID_RE = re.compile(r"R(\d{3})")


@dataclass(frozen=True)
class Callout:
    kind: str
    question: str
    page_stem: str
    page_rel: str
    line_number: int

    @property
    def source_ref(self) -> str:
        return f"{self.page_rel}:{self.line_number}"

    @property
    def source_link(self) -> str:
        return f"[[{self.page_stem}]]"


@dataclass(frozen=True)
class QueueRow:
    item_id: str
    question: str
    source_page: str
    surfaced_from: str
    priority: str
    review_by: str
    status: str
    resolution: str


def markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ").strip()


def extract_callout_text(lines: list[str], idx: int, fallback: str) -> str:
    line = lines[idx]
    match = CALLOUT_RE.match(line)
    assert match is not None
    title = match.group(2).strip()
    if title:
        return title

    for next_line in lines[idx + 1 :]:
        if not next_line.startswith(">"):
            if next_line.strip():
                break
            continue
        text = next_line.lstrip("> ").strip()
        if not text or text.startswith("[!"):
            continue
        if text.startswith("- [ ]"):
            text = text[5:].strip()
        return text or fallback
    return fallback


def scan_callouts() -> list[Callout]:
    callouts: list[Callout] = []
    for page in wiki_lint.load_pages():
        if page.type not in TRACKED_TYPES:
            continue
        body = wiki_lint.stripped_body(page.body)
        lines = body.splitlines()
        for idx, line in enumerate(lines):
            match = CALLOUT_RE.match(line)
            if not match:
                continue
            fallback = f"{match.group(1).lower()} callout in {page.path.stem}"
            question = extract_callout_text(lines, idx, fallback)
            callouts.append(
                Callout(
                    kind=match.group(1).lower(),
                    question=question[:180],
                    page_stem=page.path.stem,
                    page_rel=page.rel,
                    line_number=idx + 1,
                )
            )
    return callouts


def split_table_row(line: str) -> list[str]:
    placeholder = "\x00PIPE\x00"
    cleaned = line.strip().replace(r"\|", placeholder)
    if not cleaned.startswith("|") or not cleaned.endswith("|"):
        return []
    return [cell.strip().replace(placeholder, "|") for cell in cleaned.split("|")[1:-1]]


def parse_queue() -> list[QueueRow]:
    if not QUEUE.exists():
        return []
    rows: list[QueueRow] = []
    for line in QUEUE.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = split_table_row(line)
        if len(cells) != 8 or cells[0] in {"#", ""} or set(cells[0]) <= {"-"}:
            continue
        rows.append(QueueRow(*cells))
    return rows


def next_id(rows: list[QueueRow]) -> str:
    max_seen = 0
    for row in rows:
        match = QUEUE_ID_RE.fullmatch(row.item_id)
        if match:
            max_seen = max(max_seen, int(match.group(1)))
    return f"R{max_seen + 1:03d}"


def add_id(item_id: str) -> str:
    match = QUEUE_ID_RE.fullmatch(item_id)
    if not match:
        raise ValueError(f"invalid queue id: {item_id}")
    return f"R{int(match.group(1)) + 1:03d}"


def unmatched_callouts(callouts: list[Callout], rows: list[QueueRow]) -> list[Callout]:
    tracked_refs = {row.surfaced_from for row in rows if row.status == "open"}
    tracked_questions = {
        (row.source_page, row.question.lower())
        for row in rows
        if row.status == "open"
    }
    out: list[Callout] = []
    for callout in callouts:
        key = (callout.source_link, callout.question.lower())
        if callout.source_ref in tracked_refs or key in tracked_questions:
            continue
        out.append(callout)
    return out


def ensure_queue(today: dt.date) -> None:
    if QUEUE.exists():
        return
    QUEUE.write_text(
        f"""---
type: meta
sources: []
created: "{today.isoformat()}"
updated: "{today.isoformat()}"
status: current
tags:
  - meta
---

> [!tldr]
> ID-based queue for research gaps and unverified claims promoted from content-page callouts.

# Research Queue

See also: [[research-backlog]], [[sources/promotion-queue|promotion-queue]], [[synthesis]]

## Open

| # | Question | Source Page | Surfaced From | Priority | Review By | Status | Resolution |
|---|----------|-------------|---------------|:--------:|-----------|:------:|------------|

## Resolved

| # | Question | Source Page | Surfaced From | Priority | Review By | Status | Resolution |
|---|----------|-------------|---------------|:--------:|-----------|:------:|------------|
""",
        encoding="utf-8",
    )


def insert_rows(callouts: list[Callout], rows: list[QueueRow], today: dt.date) -> None:
    ensure_queue(today)
    text = QUEUE.read_text(encoding="utf-8")
    review_by = (today + dt.timedelta(days=30)).isoformat()
    item_id = next_id(rows)
    new_lines: list[str] = []
    for callout in callouts:
        new_lines.append(
            "| "
            + " | ".join(
                [
                    item_id,
                    markdown_escape(callout.question),
                    callout.source_link,
                    callout.source_ref,
                    "medium",
                    review_by,
                    "open",
                    "",
                ]
            )
            + " |"
        )
        item_id = add_id(item_id)

    marker = "## Resolved\n"
    if marker not in text:
        raise RuntimeError("research queue missing `## Resolved` marker")
    text = text.replace(marker, "\n".join(new_lines) + "\n\n" + marker, 1)
    text = re.sub(r'updated: "\d{4}-\d{2}-\d{2}"', f'updated: "{today.isoformat()}"', text, count=1)
    QUEUE.write_text(text, encoding="utf-8")


def parse_today(value: str | None) -> dt.date:
    if value is None:
        return dt.date.today()
    return dt.date.fromisoformat(value)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Sync wiki gaps into the research queue.")
    parser.add_argument("--apply", action="store_true", help="write missing queue rows")
    parser.add_argument("--today", default=None, help="override today as YYYY-MM-DD")
    args = parser.parse_args(argv)

    try:
        today = parse_today(args.today)
        callouts = scan_callouts()
        rows = parse_queue()
        missing = unmatched_callouts(callouts, rows)
        if not missing:
            print("research queue: OK")
            return 0
        if args.apply:
            insert_rows(missing, rows, today)
            print(f"research queue: added {len(missing)} item(s) to {QUEUE.relative_to(ROOT)}")
        else:
            print(f"research queue: {len(missing)} new item(s) available")
            for callout in missing:
                print(f"- {callout.source_ref} [{callout.kind}] {callout.question}")
        return 1
    except Exception as exc:
        print(f"research queue sync failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

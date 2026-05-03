#!/usr/bin/env python3
"""Validate the supplements research wiki scaffold.

This intentionally uses only the Python standard library so it can run from
Claude hooks, git hooks, or a plain shell without installing dependencies.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
CLAUDE = ROOT / "CLAUDE.md"

TYPE_VALUES = {
    "entity",
    "concept",
    "source-summary",
    "comparison",
    "hypothesis",
    "stack",
    "decision",
    "dosing",
    "query",
    "meta",
}
STATUS_VALUES = {"current", "stale"}
ENTITY_TYPES = {"supplement", "compound", "brand", "delivery-form"}
CONCEPT_TYPES = {
    "pathway",
    "pathway-family",
    "outcome",
    "condition",
    "biomarker",
    "process",
    "risk-domain",
    "population",
    "gene",
    "genetic-variant",
    "genotype",
    "pharmacogenomic-marker",
}
DOMAINS = {
    "longevity",
    "disease-risk",
    "cognition",
    "mood",
    "metabolic",
    "cardiovascular",
    "musculoskeletal",
    "immune",
    "safety",
    "dosing",
    "basic-biology",
    "genetics",
}
STUDY_TYPES = {
    "RCT",
    "meta-analysis",
    "observational",
    "in-vitro",
    "animal",
    "review",
    "editorial",
    "preprint",
    "research-report",
    "GWAS",
    "genetic-association",
    "Mendelian-randomization",
    "pharmacogenetic",
    "nutrigenomic",
}
SOURCE_ROLES = {
    "synthesis",
    "primary-anchor",
    "contradiction",
    "dosing",
    "safety",
    "genetics",
    "background",
}
EVIDENCE_LAYERS = {"mechanistic", "animal", "human", "genetics", "mixed"}
READING_STATUSES = {"full-text", "abstract-only", "report-derived"}
DECISION_RELEVANCE = {"high", "medium", "low"}
ANCHOR_FOR = {
    "efficacy",
    "mechanism",
    "dosing",
    "safety",
    "translation",
    "contradiction",
    "genetics",
    "stack-decision",
}
EVIDENCE_RATINGS = {"strong", "moderate", "weak", "mixed", "negative", "none"}
HUMAN_RATINGS = EVIDENCE_RATINGS | {"untested"}
TRANSLATIONAL = {
    "human-supported",
    "mechanism-led",
    "animal-led",
    "contradicted",
    "insufficient",
}
PRACTICAL = {"candidate", "consider", "deprioritize", "avoid", "research-only"}
TRANSLATION_PLAUSIBILITY = {"high", "moderate", "low", "blocked", "unknown"}
REPLICATION_STATUSES = {"replicated", "mixed", "single-lab", "failed", "untested", "unknown"}
CLAIM_SCOPES = {
    "general-longevity",
    "condition-specific",
    "biomarker-only",
    "mechanism-only",
    "unknown",
}
EFFECT_DIRECTIONS = {"beneficial", "harmful", "mixed", "null", "unknown"}
HYPOTHESIS_STATUSES = {"open", "supported", "contradicted", "nuanced"}
INGEST_STATUSES = {"in-progress", "complete"}
DECISION_TYPES = {
    "stack-change",
    "dose-change",
    "start-stop",
    "safety",
    "monitoring",
}
DECISION_ACTIONS = {
    "start",
    "stop",
    "continue",
    "change-dose",
    "avoid",
    "defer",
    "pause",
    "resume",
    "monitor",
}
DECISION_STATUSES = {"active", "closed", "superseded"}
QUEUE_PRIORITIES = {"high", "medium", "low"}
QUEUE_STATUSES = {"open", "resolved", "deferred"}

SCHEMA_ENUMS = {
    "type": TYPE_VALUES,
    "status": STATUS_VALUES,
    "entity_type": ENTITY_TYPES,
    "concept_type": CONCEPT_TYPES,
    "domain": DOMAINS,
    "ingest_status": INGEST_STATUSES,
    "study_type": STUDY_TYPES,
    "source_role": SOURCE_ROLES,
    "evidence_layer": EVIDENCE_LAYERS,
    "reading_status": READING_STATUSES,
    "decision_relevance": DECISION_RELEVANCE,
    "anchor_for": ANCHOR_FOR,
    "mechanistic_evidence": EVIDENCE_RATINGS,
    "animal_evidence": EVIDENCE_RATINGS,
    "human_evidence": HUMAN_RATINGS,
    "translational_status": TRANSLATIONAL,
    "practical_status": PRACTICAL,
    "translation_plausibility": TRANSLATION_PLAUSIBILITY,
    "replication_status": REPLICATION_STATUSES,
    "claim_scope": CLAIM_SCOPES,
    "effect_direction": EFFECT_DIRECTIONS,
    "hypothesis_status": HYPOTHESIS_STATUSES,
    "decision_type": DECISION_TYPES,
    "action": DECISION_ACTIONS,
    "decision_status": DECISION_STATUSES,
}

TAG_EXACT = {"open-question", "meta"}
TAG_PREFIXES = (
    "supplement/",
    "pathway/",
    "outcome/",
    "condition/",
    "process/",
    "risk-domain/",
    "population/",
    "gene/",
    "variant/",
    "genotype/",
)
MIRROR_TAG_PREFIXES = ("evidence/level-", "stream/", "decision/")

CONTENT_DIR = {
    "entity": WIKI / "entities",
    "concept": WIKI / "concepts",
    "source-summary": WIKI / "sources",
    "comparison": WIKI / "comparisons",
    "hypothesis": WIKI / "hypotheses",
    "stack": WIKI / "stacks",
    "decision": WIKI / "decisions",
    "dosing": WIKI / "dosing",
    "query": WIKI / "queries",
}

FRONTMATTER_LINK_RULES = {
    "sources": {"type": {"source-summary"}},
    "primary_outcomes": {
        "type": {"concept"},
        "concept_type": {"outcome", "condition", "risk-domain"},
    },
    "primary_pathways": {
        "type": {"concept"},
        "concept_type": {"pathway", "pathway-family", "process"},
    },
    "primary_genetics": {
        "type": {"concept"},
        "concept_type": {"gene", "genetic-variant", "genotype", "pharmacogenomic-marker"},
    },
    "subjects": {},
    "supplement": {"type": {"entity"}, "entity_type": {"supplement", "compound"}},
    "supplements": {"type": {"entity"}, "entity_type": {"supplement", "compound"}},
    "pathways": {"type": {"concept"}, "concept_type": {"pathway", "pathway-family", "process"}},
    "outcomes": {"type": {"concept"}, "concept_type": {"outcome", "condition", "risk-domain"}},
    "related_stack": {"type": {"stack"}},
}
OPTIONAL_FRONTMATTER_LINK_RULES = {
    "population": {"type": {"concept"}, "concept_type": {"population", "condition", "risk-domain"}},
    "genetic_context": {
        "type": {"concept"},
        "concept_type": {"gene", "genetic-variant", "genotype", "pharmacogenomic-marker"},
    },
}

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
CALLOUT_RE = re.compile(r"^>\s*\[!([A-Za-z0-9_-]+)\]")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DOC_FIELD_ENUM_RE = re.compile(r"`(?P<field>[^`]+)`\s*\((?P<body>[^)]*\|[^)]*)\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
CATALOG = WIKI / "catalog.md"


def set_root(root: Path) -> None:
    """Point the linter at a vault root.

    The default is the repository root inferred from this script location.
    Tests use this to run the real linter against temporary fixture vaults.
    """

    global ROOT, WIKI, CLAUDE, CONTENT_DIR, CATALOG
    ROOT = root.resolve()
    WIKI = ROOT / "wiki"
    CLAUDE = ROOT / "CLAUDE.md"
    CATALOG = WIKI / "catalog.md"
    CONTENT_DIR = {
        "entity": WIKI / "entities",
        "concept": WIKI / "concepts",
        "source-summary": WIKI / "sources",
        "comparison": WIKI / "comparisons",
        "hypothesis": WIKI / "hypotheses",
        "stack": WIKI / "stacks",
        "decision": WIKI / "decisions",
        "dosing": WIKI / "dosing",
        "query": WIKI / "queries",
    }


@dataclass
class Page:
    path: Path
    text: str
    frontmatter: dict[str, object]
    body: str

    @property
    def rel(self) -> str:
        return self.path.relative_to(ROOT).as_posix()

    @property
    def type(self) -> str:
        value = self.frontmatter.get("type")
        return value if isinstance(value, str) else ""


@dataclass
class Finding:
    severity: str
    path: str
    message: str

    def format(self) -> str:
        prefix = "ERROR" if self.severity == "error" else "WARN"
        return f"{prefix}: {self.path}: {self.message}"


def strip_comment(value: str) -> str:
    in_single = False
    in_double = False
    for idx, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return value[:idx].rstrip()
    return value.strip()


def parse_scalar(value: str) -> object:
    value = strip_comment(value).strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"').strip("'") for item in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    raw = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    result: dict[str, object] = {}
    current_key: str | None = None

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            current = result.setdefault(current_key, [])
            if isinstance(current, list):
                current.append(parse_scalar(line[4:]))
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            current_key = None
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value == "":
            result[key] = []
            current_key = key
        else:
            result[key] = parse_scalar(raw_value)
            current_key = None
    return result, body


def load_pages() -> list[Page]:
    pages: list[Page] = []
    for path in sorted(WIKI.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        parsed = parse_frontmatter(text)
        if parsed is None:
            pages.append(Page(path=path, text=text, frontmatter={}, body=text))
            continue
        frontmatter, body = parsed
        pages.append(Page(path=path, text=text, frontmatter=frontmatter, body=body))
    return pages


def wiki_files() -> list[Path]:
    return [path for path in WIKI.rglob("*") if path.is_file()]


def normalize_link_target(raw: str) -> str:
    return raw.split("|", 1)[0].split("#", 1)[0].strip()


def stripped_body(body: str) -> str:
    """Remove code blocks and inline code before wikilink scanning.

    Obsidian renders wikilinks inside code as literal text. Lint should
    match that behavior so documentation examples do not need fake pages.
    """

    out: list[str] = []
    in_fence = False
    for line in body.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append("\n" if line.endswith("\n") else "")
            continue
        if in_fence:
            out.append("\n" if line.endswith("\n") else "")
            continue
        out.append(line)
    return INLINE_CODE_RE.sub("", "".join(out))


def collect_targets(files: Iterable[Path]) -> dict[str, Path]:
    targets: dict[str, Path] = {}
    for path in files:
        rel = path.with_suffix("").relative_to(ROOT).as_posix()
        names = {path.stem, rel}
        if rel.startswith("wiki/"):
            names.add(rel[5:])
        for name in names:
            targets.setdefault(name, path)
    return targets


def collect_aliases(pages: Iterable[Page]) -> dict[str, Path]:
    aliases: dict[str, Path] = {}
    for page in pages:
        raw_aliases = page.frontmatter.get("aliases", [])
        if isinstance(raw_aliases, str):
            raw_aliases = [raw_aliases]
        if isinstance(raw_aliases, list):
            for alias in raw_aliases:
                if isinstance(alias, str) and alias:
                    aliases.setdefault(alias, page.path)
    return aliases


def as_list(value: object) -> list[object]:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def is_iso_date(value: object) -> bool:
    if not isinstance(value, str) or not DATE_RE.match(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def check_enum(
    findings: list[Finding],
    page: Page,
    key: str,
    allowed: set[str],
    *,
    required: bool = True,
) -> None:
    value = page.frontmatter.get(key)
    if value in (None, ""):
        if required:
            findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))
        return
    if not isinstance(value, str) or value not in allowed:
        findings.append(
            Finding("error", page.rel, f"`{key}` must be one of: {', '.join(sorted(allowed))}")
        )


def check_list_values(
    findings: list[Finding], page: Page, key: str, allowed: set[str], *, required: bool = True
) -> None:
    value = page.frontmatter.get(key)
    values = as_list(value)
    if required and not values:
        findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))
        return
    for item in values:
        if not isinstance(item, str) or item not in allowed:
            findings.append(
                Finding("error", page.rel, f"`{key}` contains invalid value `{item}`")
            )


def parse_doc_enum_values(raw: str) -> set[str]:
    raw = strip_comment(raw).strip()
    if raw.startswith("list:"):
        raw = raw.split(":", 1)[1].strip()
    return {item.strip() for item in raw.split("|") if item.strip()}


def documented_schema_enums() -> tuple[dict[str, set[str]], list[Finding]]:
    findings: list[Finding] = []
    if not CLAUDE.exists():
        return {}, [Finding("error", "CLAUDE.md", "schema source file is missing")]

    text = CLAUDE.read_text(encoding="utf-8")
    documented: dict[str, set[str]] = {}

    for line in text.splitlines():
        stripped = line.strip()
        for field in ("type", "status"):
            if not stripped.startswith(f"{field}:"):
                continue
            values = parse_doc_enum_values(stripped.split(":", 1)[1])
            if values:
                documented[field] = values

        for match in DOC_FIELD_ENUM_RE.finditer(line):
            field = match.group("field")
            if field not in SCHEMA_ENUMS:
                continue
            values = parse_doc_enum_values(match.group("body"))
            if field in documented and documented[field] != values:
                findings.append(
                    Finding(
                        "error",
                        "CLAUDE.md",
                        f"documents conflicting enum values for `{field}`",
                    )
                )
                continue
            documented[field] = values

    return documented, findings


def check_schema_sync() -> list[Finding]:
    documented, findings = documented_schema_enums()
    for field, expected in SCHEMA_ENUMS.items():
        actual = documented.get(field)
        if actual is None:
            findings.append(Finding("error", "CLAUDE.md", f"missing documented enum for `{field}`"))
            continue
        if actual != expected:
            doc_only = ", ".join(sorted(actual - expected)) or "none"
            lint_only = ", ".join(sorted(expected - actual)) or "none"
            findings.append(
                Finding(
                    "error",
                    "CLAUDE.md",
                    f"`{field}` enum drift: docs-only [{doc_only}], lint-only [{lint_only}]",
                )
            )
    return findings


def check_frontmatter(pages: list[Page]) -> list[Finding]:
    findings: list[Finding] = []
    required = {"type", "sources", "created", "updated", "status", "tags"}

    for page in pages:
        if not page.frontmatter:
            findings.append(Finding("error", page.rel, "missing YAML frontmatter"))
            continue

        for key in sorted(required):
            if key not in page.frontmatter:
                findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))

        check_enum(findings, page, "type", TYPE_VALUES)
        check_enum(findings, page, "status", STATUS_VALUES)
        for key in ("created", "updated"):
            if key in page.frontmatter and not is_iso_date(page.frontmatter.get(key)):
                findings.append(Finding("error", page.rel, f"`{key}` must be YYYY-MM-DD"))

        if not isinstance(page.frontmatter.get("sources", []), list):
            findings.append(Finding("error", page.rel, "`sources` must be a list"))
        if not isinstance(page.frontmatter.get("tags", []), list):
            findings.append(Finding("error", page.rel, "`tags` must be a list"))

        page_type = page.type
        expected_dir = CONTENT_DIR.get(page_type)
        if page_type != "meta" and expected_dir and expected_dir not in page.path.parents:
            findings.append(
                Finding("error", page.rel, f"`type: {page_type}` does not match file location")
            )

        if page_type not in {"meta", "source-summary"} and not as_list(page.frontmatter.get("sources")):
            findings.append(Finding("error", page.rel, "non-meta page has empty `sources`"))

        if page_type == "entity":
            check_enum(findings, page, "entity_type", ENTITY_TYPES)
            if page.frontmatter.get("entity_type") == "supplement":
                for key in (
                    "aliases",
                    "evidence_level",
                    "mechanistic_evidence",
                    "animal_evidence",
                    "human_evidence",
                    "translational_status",
                    "practical_status",
                    "translation_plausibility",
                    "replication_status",
                    "claim_scope",
                    "primary_outcomes",
                    "primary_pathways",
                    "primary_genetics",
                ):
                    if key not in page.frontmatter:
                        findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))
                if page.frontmatter.get("evidence_level") not in {1, 2, 3, 4}:
                    findings.append(
                        Finding("error", page.rel, "`evidence_level` must be 1, 2, 3, or 4")
                    )
                check_enum(findings, page, "mechanistic_evidence", EVIDENCE_RATINGS)
                check_enum(findings, page, "animal_evidence", EVIDENCE_RATINGS)
                check_enum(findings, page, "human_evidence", HUMAN_RATINGS)
                check_enum(findings, page, "translational_status", TRANSLATIONAL)
                check_enum(findings, page, "practical_status", PRACTICAL)
                check_enum(findings, page, "translation_plausibility", TRANSLATION_PLAUSIBILITY)
                check_enum(findings, page, "replication_status", REPLICATION_STATUSES)
                check_enum(findings, page, "claim_scope", CLAIM_SCOPES)

        elif page_type == "concept":
            check_enum(findings, page, "concept_type", CONCEPT_TYPES)
            check_enum(findings, page, "domain", DOMAINS)
            if page.frontmatter.get("concept_type") in {
                "gene",
                "genetic-variant",
                "genotype",
                "pharmacogenomic-marker",
            } and page.frontmatter.get("domain") != "genetics":
                findings.append(Finding("error", page.rel, "genetics concepts require `domain: genetics`"))

        elif page_type == "source-summary":
            check_enum(findings, page, "ingest_status", INGEST_STATUSES)
            check_enum(findings, page, "study_type", STUDY_TYPES)
            check_enum(findings, page, "source_role", SOURCE_ROLES)
            check_enum(findings, page, "evidence_layer", EVIDENCE_LAYERS)
            check_enum(findings, page, "reading_status", READING_STATUSES)
            check_enum(findings, page, "decision_relevance", DECISION_RELEVANCE)
            check_list_values(findings, page, "anchor_for", ANCHOR_FOR, required=False)
            for key in ("raw_path", "raw_hash"):
                if not page.frontmatter.get(key):
                    findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))

        elif page_type == "comparison":
            if not as_list(page.frontmatter.get("subjects")):
                findings.append(Finding("error", page.rel, "missing `subjects` frontmatter"))

        elif page_type == "hypothesis":
            for key in ("supplements", "pathways", "outcomes"):
                if not as_list(page.frontmatter.get(key)):
                    findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))
            for key in ("population", "genetic_context"):
                if key not in page.frontmatter:
                    findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))
            for key in ("review_by", "if_supported", "if_contradicted"):
                if not page.frontmatter.get(key):
                    findings.append(Finding("error", page.rel, f"missing `{key}` frontmatter"))
            if page.frontmatter.get("review_by") and not is_iso_date(page.frontmatter.get("review_by")):
                findings.append(Finding("error", page.rel, "`review_by` must be YYYY-MM-DD"))
            evaluated = page.frontmatter.get("evaluated")
            if evaluated not in (None, "") and not is_iso_date(evaluated):
                findings.append(Finding("error", page.rel, "`evaluated` must be YYYY-MM-DD when set"))
            if page.frontmatter.get("evidence_level") not in {1, 2, 3, 4}:
                findings.append(Finding("error", page.rel, "`evidence_level` must be 1, 2, 3, or 4"))
            check_enum(findings, page, "mechanistic_evidence", EVIDENCE_RATINGS)
            check_enum(findings, page, "animal_evidence", EVIDENCE_RATINGS)
            check_enum(findings, page, "human_evidence", HUMAN_RATINGS)
            check_enum(findings, page, "translational_status", TRANSLATIONAL)
            check_enum(findings, page, "effect_direction", EFFECT_DIRECTIONS)
            check_enum(findings, page, "hypothesis_status", HYPOTHESIS_STATUSES)
            if page.frontmatter.get("hypothesis_status") != "open" and evaluated in (None, ""):
                findings.append(
                    Finding("error", page.rel, "non-open hypothesis requires `evaluated` date")
                )

        elif page_type == "stack":
            if not page.frontmatter.get("goal"):
                findings.append(Finding("error", page.rel, "missing `goal` frontmatter"))
            if not as_list(page.frontmatter.get("supplements")):
                findings.append(Finding("error", page.rel, "missing `supplements` frontmatter"))

        elif page_type == "decision":
            check_enum(findings, page, "decision_type", DECISION_TYPES)
            check_enum(findings, page, "action", DECISION_ACTIONS)
            check_enum(findings, page, "decision_status", DECISION_STATUSES)
            if not as_list(page.frontmatter.get("supplements")):
                findings.append(Finding("error", page.rel, "missing `supplements` frontmatter"))
            review_by = page.frontmatter.get("review_by")
            if review_by not in (None, "") and not is_iso_date(review_by):
                findings.append(Finding("error", page.rel, "`review_by` must be YYYY-MM-DD when set"))
            closed = page.frontmatter.get("closed")
            if closed not in (None, "") and not is_iso_date(closed):
                findings.append(Finding("error", page.rel, "`closed` must be YYYY-MM-DD when set"))

        elif page_type == "dosing":
            if not page.frontmatter.get("supplement"):
                findings.append(Finding("error", page.rel, "missing `supplement` frontmatter"))
            if "aliases" not in page.frontmatter:
                findings.append(Finding("error", page.rel, "missing `aliases` frontmatter"))

        for tag in as_list(page.frontmatter.get("tags")):
            if not isinstance(tag, str):
                findings.append(Finding("error", page.rel, f"invalid tag value `{tag}`"))
                continue
            if tag.startswith(MIRROR_TAG_PREFIXES):
                findings.append(Finding("error", page.rel, f"mirror tag `{tag}` duplicates frontmatter"))
            if tag not in TAG_EXACT and not tag.startswith(TAG_PREFIXES):
                findings.append(Finding("error", page.rel, f"tag `{tag}` is outside taxonomy"))

    return findings


def frontmatter_link_fields(page: Page) -> list[str]:
    fields = ["sources"]
    if page.type == "entity":
        fields.extend(["primary_outcomes", "primary_pathways", "primary_genetics"])
    elif page.type == "comparison":
        fields.append("subjects")
    elif page.type == "hypothesis":
        fields.extend(["supplements", "pathways", "outcomes"])
    elif page.type == "stack":
        fields.append("supplements")
    elif page.type == "decision":
        fields.extend(["supplements"])
        if "related_stack" in page.frontmatter:
            fields.append("related_stack")
    elif page.type == "dosing":
        fields.append("supplement")
    return [field for field in fields if field in page.frontmatter]


def optional_frontmatter_link_fields(page: Page) -> list[str]:
    if page.type != "hypothesis":
        return []
    return [field for field in OPTIONAL_FRONTMATTER_LINK_RULES if field in page.frontmatter]


def describe_link_rule(rule: dict[str, set[str]]) -> str:
    parts: list[str] = []
    if "type" in rule:
        parts.append("type " + "/".join(sorted(rule["type"])))
    if "entity_type" in rule:
        parts.append("entity_type " + "/".join(sorted(rule["entity_type"])))
    if "concept_type" in rule:
        parts.append("concept_type " + "/".join(sorted(rule["concept_type"])))
    return "a wiki page" if not parts else "a page with " + " and ".join(parts)


def target_matches_rule(page: Page, rule: dict[str, set[str]]) -> bool:
    if "type" in rule and page.type not in rule["type"]:
        return False
    for key in ("entity_type", "concept_type"):
        if key in rule and page.frontmatter.get(key) not in rule[key]:
            return False
    return True


def check_frontmatter_links(pages: list[Page], files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    targets = collect_targets(files)
    targets.update(collect_aliases(pages))
    pages_by_path = {page.path: page for page in pages}

    def check_field(page: Page, field: str, rule: dict[str, set[str]], require_link: bool) -> None:
        values = as_list(page.frontmatter.get(field))
        if not require_link and len(values) > 1:
            findings.append(Finding("error", page.rel, f"`{field}` must be a scalar string"))
            return
        for item in values:
            if item in (None, ""):
                continue
            if not isinstance(item, str):
                findings.append(
                    Finding("error", page.rel, f"`{field}` entry must be a wikilink string")
                )
                continue
            links = [
                normalize_link_target(match.group(1))
                for match in WIKILINK_RE.finditer(item)
                if normalize_link_target(match.group(1))
            ]
            if not links:
                if require_link:
                    findings.append(
                        Finding("error", page.rel, f"`{field}` entry `{item}` must be a wikilink")
                    )
                continue
            for target in links:
                resolved = targets.get(target)
                if resolved is None:
                    findings.append(
                        Finding(
                            "error",
                            page.rel,
                            f"`{field}` has unresolved wikilink `[[{target}]]`",
                        )
                    )
                    continue
                target_page = pages_by_path.get(resolved)
                if target_page is None:
                    findings.append(
                        Finding(
                            "error",
                            page.rel,
                            f"`{field}` wikilink `[[{target}]]` must resolve to a wiki page",
                        )
                    )
                    continue
                if not target_matches_rule(target_page, rule):
                    findings.append(
                        Finding(
                            "error",
                            page.rel,
                            f"`{field}` wikilink `[[{target}]]` must target "
                            f"{describe_link_rule(rule)}",
                        )
                    )

    for page in pages:
        for field in frontmatter_link_fields(page):
            check_field(page, field, FRONTMATTER_LINK_RULES[field], require_link=True)
        for field in optional_frontmatter_link_fields(page):
            check_field(page, field, OPTIONAL_FRONTMATTER_LINK_RULES[field], require_link=False)
    return findings


def check_filenames(pages: list[Page]) -> list[Finding]:
    findings: list[Finding] = []
    for page in pages:
        if page.type == "meta":
            continue
        name = page.path.stem
        if re.search(r"[^A-Za-z0-9 ()-]", name):
            findings.append(
                Finding("error", page.rel, "content filename has unsupported characters")
            )
        words = [word for word in re.split(r"[ ()-]+", name) if word]
        for word in words:
            if word.isdigit() or word.isupper():
                continue
            if not word[0].isupper():
                findings.append(
                    Finding("error", page.rel, "content filename should use Title Case")
                )
                break
    return findings


def check_tldr_and_callouts(
    pages: list[Page], targets: dict[str, Path], source_summary_paths: set[Path]
) -> list[Finding]:
    findings: list[Finding] = []
    for page in pages:
        first = next((line.strip() for line in page.body.splitlines() if line.strip()), "")
        if first != "> [!tldr]":
            findings.append(Finding("error", page.rel, "`> [!tldr]` is not the first content block"))

        body = stripped_body(page.body)
        lines = body.splitlines()
        for idx, line in enumerate(lines):
            if line.lstrip().startswith("> [!") and not CALLOUT_RE.match(line):
                findings.append(Finding("error", page.rel, f"malformed callout near line {idx + 1}"))
            if not line.startswith("> [!source]"):
                continue
            block_lines = [line]
            for next_line in lines[idx + 1 :]:
                if next_line.startswith(">"):
                    block_lines.append(next_line)
                    continue
                if not next_line.strip():
                    continue
                break
            block = "\n".join(block_lines)
            links = [
                normalize_link_target(match.group(1))
                for match in WIKILINK_RE.finditer(block)
                if normalize_link_target(match.group(1))
            ]
            self_links = [link for link in links if targets.get(link) == page.path]
            if not links:
                findings.append(Finding("error", page.rel, "[!source] callout lacks a wikilink"))
            elif self_links:
                findings.append(Finding("error", page.rel, "[!source] callout cites the page itself"))
            elif not any(targets.get(link) in source_summary_paths for link in links):
                findings.append(
                    Finding("error", page.rel, "[!source] callout lacks a source-summary wikilink")
                )

        has_gap = bool(re.search(r"^>\s*\[!gap\]", body, re.M))
        tags = {str(tag) for tag in as_list(page.frontmatter.get("tags"))}
        if has_gap and "open-question" not in tags:
            findings.append(Finding("error", page.rel, "page has [!gap] but lacks `open-question` tag"))
        if "open-question" in tags and not has_gap:
            findings.append(Finding("warn", page.rel, "`open-question` tag present but no [!gap] callout found"))

    return findings


def check_links(pages: list[Page], files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    targets = collect_targets(files)
    aliases = collect_aliases(pages)
    targets.update(aliases)
    incoming: dict[Path, set[Path]] = {page.path: set() for page in pages}

    for page in pages:
        for match in WIKILINK_RE.finditer(stripped_body(page.body)):
            target = normalize_link_target(match.group(1))
            if not target:
                continue
            resolved = targets.get(target)
            if resolved is None:
                findings.append(Finding("error", page.rel, f"unresolved wikilink `[[{target}]]`"))
                continue
            if resolved == page.path:
                continue
            if page.type != "meta" and resolved in incoming:
                incoming[resolved].add(page.path)

    for page in pages:
        if page.type == "meta":
            continue
        outgoing = [
            normalize_link_target(match.group(1))
            for match in WIKILINK_RE.finditer(stripped_body(page.body))
            if normalize_link_target(match.group(1))
            and targets.get(normalize_link_target(match.group(1))) != page.path
        ]
        if not outgoing:
            findings.append(Finding("error", page.rel, "dead-end content page has no outgoing wikilinks"))
        if page.type != "query" and not incoming.get(page.path):
            findings.append(Finding("error", page.rel, "orphan content page has no incoming wikilinks"))

    return findings


def first_tldr_line(page: Page) -> str:
    lines = page.body.splitlines()
    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        if line.strip() != "> [!tldr]":
            return ""
        if idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith(">"):
            return lines[idx + 1].lstrip("> ").strip()
        return ""
    return ""


def source_count(page: Page) -> int:
    return len(as_list(page.frontmatter.get("sources")))


def catalog_metadata(page: Page) -> str:
    fm = page.frontmatter
    if page.type == "entity":
        bits = [
            str(fm.get("entity_type", "")),
            f"practical: {fm.get('practical_status', '')}",
            f"translational: {fm.get('translational_status', '')}",
            f"translation: {fm.get('translation_plausibility', '')}",
            f"replication: {fm.get('replication_status', '')}",
            f"scope: {fm.get('claim_scope', '')}",
            f"evidence: {fm.get('evidence_level', '')}",
        ]
    elif page.type == "concept":
        bits = [str(fm.get("concept_type", "")), str(fm.get("domain", ""))]
    elif page.type == "hypothesis":
        bits = [
            f"status: {fm.get('hypothesis_status', '')}",
            f"direction: {fm.get('effect_direction', '')}",
            f"translational: {fm.get('translational_status', '')}",
        ]
    elif page.type == "source-summary":
        bits = [
            str(fm.get("study_type", "")),
            f"role: {fm.get('source_role', '')}",
            f"layer: {fm.get('evidence_layer', '')}",
            f"read: {fm.get('reading_status', '')}",
        ]
    elif page.type == "comparison":
        bits = [f"subjects: {len(as_list(fm.get('subjects')))}"]
    elif page.type == "stack":
        bits = [f"goal: {fm.get('goal', '')}", f"supplements: {len(as_list(fm.get('supplements')))}"]
    elif page.type == "decision":
        bits = [
            str(fm.get("decision_type", "")),
            f"action: {fm.get('action', '')}",
            f"status: {fm.get('decision_status', '')}",
            f"review: {fm.get('review_by', '')}",
        ]
    elif page.type == "dosing":
        bits = [f"supplement: {fm.get('supplement', '')}"]
    else:
        bits = []
    return "; ".join(bit for bit in bits if bit and not bit.endswith(": "))


def catalog_groups(pages: list[Page]) -> list[tuple[str, list[Page]]]:
    groups = [
        (
            "Supplements",
            [
                page
                for page in pages
                if page.type == "entity" and page.frontmatter.get("entity_type") == "supplement"
            ],
        ),
        (
            "Other Entities",
            [
                page
                for page in pages
                if page.type == "entity" and page.frontmatter.get("entity_type") != "supplement"
            ],
        ),
        ("Concepts", [page for page in pages if page.type == "concept"]),
        ("Hypotheses", [page for page in pages if page.type == "hypothesis"]),
        ("Comparisons", [page for page in pages if page.type == "comparison"]),
        ("Stacks", [page for page in pages if page.type == "stack"]),
        ("Decisions", [page for page in pages if page.type == "decision"]),
        ("Dosing Pages", [page for page in pages if page.type == "dosing"]),
        ("Queries", [page for page in pages if page.type == "query"]),
        ("Sources", [page for page in pages if page.type == "source-summary"]),
    ]
    return [(heading, sorted(items, key=lambda item: item.path.stem.lower())) for heading, items in groups]


def existing_catalog_created() -> str:
    if not CATALOG.exists():
        return dt.date.today().isoformat()
    parsed = parse_frontmatter(CATALOG.read_text(encoding="utf-8"))
    if parsed is None:
        return dt.date.today().isoformat()
    created = parsed[0].get("created")
    return created if isinstance(created, str) and is_iso_date(created) else dt.date.today().isoformat()


def render_catalog(pages: list[Page]) -> str:
    today = dt.date.today().isoformat()
    created = existing_catalog_created()
    page_stems = {page.path.stem for page in pages}
    see_also = [
        f"[[{stem}]]"
        for stem in ("index", "research-backlog", "synthesis")
        if stem in page_stems
    ]
    lines = [
        "---",
        "type: meta",
        "sources: []",
        f'created: "{created}"',
        f'updated: "{today}"',
        "status: current",
        "tags:",
        "  - meta",
        "---",
        "",
        "> [!tldr]",
        "> Static markdown catalog for agents and non-Obsidian workflows; generated from page frontmatter and TLDRs.",
        "",
        "# Static Catalog",
        "",
        "Generated by `python3 wiki/scripts/lint.py --rebuild-catalog`.",
        "",
    ]
    if see_also:
        lines.extend(["See also: " + ", ".join(see_also), ""])

    for heading, items in catalog_groups(pages):
        lines.append(f"## {heading}")
        if not items:
            lines.append("")
            continue
        for page in items:
            metadata = catalog_metadata(page)
            parts = [f"- [[{page.path.stem}]]", f"sources: {source_count(page)}"]
            if metadata:
                parts.append(metadata)
            tldr = first_tldr_line(page)
            if tldr:
                parts.append(tldr)
            lines.append(" | ".join(parts))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def rebuild_catalog() -> str:
    pages = [page for page in load_pages() if page.path != CATALOG]
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(render_catalog(pages), encoding="utf-8")
    count = sum(1 for page in pages if page.type != "meta")
    return f"wiki catalog: rebuilt {CATALOG.relative_to(ROOT).as_posix()} ({count} content pages)"


def catalog_comparable(text: str) -> str:
    return "\n".join(
        line
        for line in text.splitlines()
        if not line.startswith(("created: ", "updated: "))
    ).strip()


def check_catalog_current(pages: list[Page]) -> list[Finding]:
    if not CATALOG.exists():
        return [
            Finding(
                "error",
                CATALOG.relative_to(ROOT).as_posix(),
                "static catalog is missing; run `python3 wiki/scripts/lint.py --rebuild-catalog`",
            )
        ]
    actual = CATALOG.read_text(encoding="utf-8")
    expected = render_catalog([page for page in pages if page.path != CATALOG])
    if catalog_comparable(actual) != catalog_comparable(expected):
        return [
            Finding(
                "error",
                CATALOG.relative_to(ROOT).as_posix(),
                "static catalog is stale; run `python3 wiki/scripts/lint.py --rebuild-catalog`",
            )
        ]
    return []


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_staleness(pages: list[Page]) -> list[Finding]:
    findings: list[Finding] = []
    for page in pages:
        if page.type != "source-summary":
            continue
        raw_path = page.frontmatter.get("raw_path")
        raw_hash = page.frontmatter.get("raw_hash")
        if not isinstance(raw_path, str) or not raw_path:
            findings.append(Finding("error", page.rel, "source-summary missing `raw_path`"))
            continue
        if not isinstance(raw_hash, str) or not raw_hash:
            findings.append(Finding("error", page.rel, "source-summary missing `raw_hash`"))
            continue
        source = (ROOT / raw_path).resolve()
        try:
            source.relative_to(ROOT)
        except ValueError:
            findings.append(Finding("error", page.rel, f"`raw_path` escapes vault: {raw_path}"))
            continue
        if not source.exists():
            findings.append(Finding("error", page.rel, f"`raw_path` does not exist: {raw_path}"))
            continue
        actual = sha256(source)
        if actual != raw_hash:
            findings.append(Finding("error", page.rel, f"stale raw_hash for {raw_path}"))
    return findings


def parse_promotion_queue() -> list[dict[str, str]]:
    queue = WIKI / "sources" / "promotion-queue.md"
    if not queue.exists():
        return []
    rows: list[dict[str, str]] = []
    for line in queue.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line or "Claim | Target Page" in line:
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) < 9 or not cells[0]:
            continue
        rows.append(
            {
                "claim": cells[0],
                "target": cells[1],
                "current_source": cells[2],
                "evidence_layer": cells[3],
                "anchor_needed": cells[4],
                "priority": cells[5],
                "reason": cells[6],
                "marked": cells[7],
                "status": cells[8],
            }
        )
    return rows


def check_promotion_queue(today: dt.date) -> list[Finding]:
    findings: list[Finding] = []
    for row in parse_promotion_queue():
        marked = row.get("marked", "")
        if not DATE_RE.match(marked):
            findings.append(
                Finding("error", "wiki/sources/promotion-queue.md", f"invalid Marked date `{marked}`")
            )
            continue
        marked_date = dt.date.fromisoformat(marked)
        age = (today - marked_date).days
        if row.get("status") == "open" and age > 30:
            findings.append(
                Finding(
                    "warn",
                    "wiki/sources/promotion-queue.md",
                    f"promotion row marked {marked} is {age} days old: {row.get('claim')}",
                )
            )
    return findings


def split_table_row(line: str) -> list[str]:
    """Split a markdown table row while preserving escaped pipes."""

    placeholder = "\x00PIPE\x00"
    cleaned = line.strip().replace(r"\|", placeholder)
    if not cleaned.startswith("|") or not cleaned.endswith("|"):
        return []
    return [cell.strip().replace(placeholder, "|") for cell in cleaned.split("|")[1:-1]]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(set(cell.replace(":", "").strip()) <= {"-"} for cell in cells)


def check_research_queue(today: dt.date) -> list[Finding]:
    path = WIKI / "research-queue.md"
    if not path.exists():
        return [
            Finding(
                "warn",
                "wiki/research-queue.md",
                "research queue is missing; run `python3 wiki/scripts/backlog_sync.py --apply` after adding gaps",
            )
        ]

    findings: list[Finding] = []
    seen_ids: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = split_table_row(line)
        if len(cells) != 8 or cells[0] in {"#", ""} or is_separator_row(cells):
            continue
        item_id, question, source, surfaced_from, priority, review_by, status, resolved = cells
        if not re.fullmatch(r"R\d{3}", item_id):
            findings.append(Finding("error", path.relative_to(ROOT).as_posix(), f"invalid queue id `{item_id}`"))
        if item_id in seen_ids:
            findings.append(Finding("error", path.relative_to(ROOT).as_posix(), f"duplicate queue id `{item_id}`"))
        seen_ids.add(item_id)
        if not question or question == "-":
            findings.append(Finding("error", path.relative_to(ROOT).as_posix(), f"{item_id} has empty Question"))
        if not source or source == "-":
            findings.append(Finding("error", path.relative_to(ROOT).as_posix(), f"{item_id} has empty Source Page"))
        if not surfaced_from or surfaced_from == "-":
            findings.append(Finding("error", path.relative_to(ROOT).as_posix(), f"{item_id} has empty Surfaced From"))
        if priority not in QUEUE_PRIORITIES:
            findings.append(
                Finding("error", path.relative_to(ROOT).as_posix(), f"{item_id} priority must be high, medium, or low")
            )
        if not is_iso_date(review_by):
            findings.append(
                Finding("error", path.relative_to(ROOT).as_posix(), f"{item_id} Review By must be YYYY-MM-DD")
            )
            continue
        if status not in QUEUE_STATUSES:
            findings.append(
                Finding("error", path.relative_to(ROOT).as_posix(), f"{item_id} status must be open, resolved, or deferred")
            )
            continue
        if status == "open" and dt.date.fromisoformat(review_by) < today:
            findings.append(
                Finding("warn", path.relative_to(ROOT).as_posix(), f"{item_id} is past Review By date {review_by}")
            )
        if status == "resolved" and not resolved:
            findings.append(
                Finding("warn", path.relative_to(ROOT).as_posix(), f"{item_id} is resolved but has empty Resolution")
            )
    return findings


def check_evidence_watch(today: dt.date) -> list[Finding]:
    path = WIKI / "evidence-watch.md"
    if not path.exists():
        return [Finding("warn", "wiki/evidence-watch.md", "evidence watch is missing")]

    findings: list[Finding] = []
    rel = path.relative_to(ROOT).as_posix()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = split_table_row(line)
        if len(cells) != 5 or cells[0] in {"Date", ""} or is_separator_row(cells):
            continue
        event_date, event, target, hypothesis_or_decision, status = cells
        if not is_iso_date(event_date):
            findings.append(Finding("error", rel, f"event date must be YYYY-MM-DD: `{event_date}`"))
            continue
        if not event:
            findings.append(Finding("error", rel, f"event on {event_date} has empty Event"))
        if not target:
            findings.append(Finding("error", rel, f"event on {event_date} has empty Target"))
        if not hypothesis_or_decision:
            findings.append(Finding("error", rel, f"event on {event_date} has empty Hypothesis / Decision"))
        if "- [ ]" not in status and "- [x]" not in status:
            findings.append(
                Finding("error", rel, f"event on {event_date} status must contain `- [ ]` or `- [x]`")
            )
            continue
        if "- [ ]" in status and (today - dt.date.fromisoformat(event_date)).days > 7:
            findings.append(Finding("warn", rel, f"unchecked past event from {event_date}: {event}"))
    return findings


def run_checks(staleness_only: bool, *, require_catalog: bool = True) -> list[Finding]:
    pages = load_pages()
    if not require_catalog:
        pages = [page for page in pages if page.path != CATALOG]
    if staleness_only:
        return check_staleness(pages)
    files = wiki_files()
    if not require_catalog and CATALOG not in files:
        files.append(CATALOG)
    targets = collect_targets(files)
    targets.update(collect_aliases(pages))
    source_summary_paths = {page.path for page in pages if page.type == "source-summary"}
    findings: list[Finding] = []
    findings.extend(check_schema_sync())
    findings.extend(check_frontmatter(pages))
    findings.extend(check_frontmatter_links(pages, files))
    findings.extend(check_filenames(pages))
    findings.extend(check_tldr_and_callouts(pages, targets, source_summary_paths))
    findings.extend(check_links(pages, files))
    findings.extend(check_staleness(pages))
    if require_catalog:
        findings.extend(check_catalog_current(pages))
    findings.extend(check_promotion_queue(dt.date.today()))
    findings.extend(check_research_queue(dt.date.today()))
    findings.extend(check_evidence_watch(dt.date.today()))
    return findings


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Lint the supplements research wiki.")
    parser.add_argument(
        "--vault",
        default=None,
        help="vault root containing CLAUDE.md and wiki/; defaults to this repository",
    )
    parser.add_argument(
        "--rebuild-catalog",
        action="store_true",
        help="rewrite wiki/catalog.md from page frontmatter and TLDRs, then exit",
    )
    parser.add_argument("--staleness-only", action="store_true", help="only check source hashes")
    parser.add_argument("--quiet", action="store_true", help="only print errors")
    args = parser.parse_args(argv)

    if args.vault is not None:
        set_root(Path(args.vault))

    if args.rebuild_catalog:
        findings = run_checks(False, require_catalog=False)
        errors = [finding for finding in findings if finding.severity == "error"]
        if errors:
            for finding in errors:
                print(finding.format())
            return 1
        for finding in findings:
            print(finding.format())
        print(rebuild_catalog())
        return 0

    findings = run_checks(args.staleness_only)
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warn"]

    printable = errors if args.quiet else findings
    for finding in printable:
        print(finding.format())

    if not args.quiet and not findings:
        print("wiki lint: OK")
    elif not args.quiet and warnings and not errors:
        print(f"wiki lint: OK with {len(warnings)} warning(s)")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

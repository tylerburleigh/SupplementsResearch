# Codex Agent Instructions

This vault uses `CLAUDE.md` as the canonical schema and operating protocol.

Before editing the wiki, read `CLAUDE.md` and follow its rules for:

- Frontmatter schema
- Page locations and templates
- Source roles and evidence layers
- Practical translation fields
- Lint, catalog, log, and handoff updates

When `CLAUDE.md` says "Claude", interpret it as "the active coding agent".

For structural/wiki changes:

1. Keep edits scoped.
2. Update templates, schema docs, linter/tests, dashboards, log, and handoff when relevant.
3. Run `python3 wiki/scripts/lint.py`.
4. Run `python3 -m unittest -q` when schema or lint behavior changes.
5. Do not modify human-owned files like `purpose.md` unless explicitly asked.

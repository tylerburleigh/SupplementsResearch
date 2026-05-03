# Codex Agent Instructions

This vault uses `CLAUDE.md` as the canonical schema and operating protocol.

Before editing the wiki, read `CLAUDE.md` and follow its rules for:

- Frontmatter schema
- Page locations and templates
- Source roles and evidence layers
- Practical translation fields
- Lint, catalog, log, and handoff updates

When `CLAUDE.md` says "Claude", interpret it as "the active coding agent".

## Repo-local Codex workflows

Codex workflow skills for this vault live in `.agents/skills/<skill-name>/SKILL.md`.
These are skills, not Codex TUI slash commands. In interactive Codex, users can
invoke them with `$wiki-ingest`, `$wiki-query`, `$wiki-repair`, `$wiki-lint`,
`$wiki-review`, `$scout`, or with matching plain-language workflow requests.
Read the corresponding `SKILL.md` before acting.

Claude subagent prompts are mirrored in `.codex/agents/`. Codex should treat
the markdown files there as role instructions and use them locally unless the
user explicitly authorizes delegated subagents. When delegated subagents are
authorized, use the matching `.codex/agents/*.toml` custom agent.

For structural/wiki changes:

1. Keep edits scoped.
2. Update templates, schema docs, linter/tests, dashboards, log, and handoff when relevant.
3. Run `python3 wiki/scripts/lint.py`.
4. Run `python3 -m unittest -q` when schema or lint behavior changes.
5. Do not modify human-owned files like `purpose.md` unless explicitly asked.

#!/usr/bin/env python3
"""Claude PreToolUse hook: run wiki lint before `git commit` Bash commands."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input", {})
    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    if not isinstance(command, str) or not command.strip().startswith("git commit"):
        return 0

    lint = ROOT / "wiki" / "scripts" / "lint.py"
    completed = subprocess.run(
        [sys.executable, str(lint), "--quiet"],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

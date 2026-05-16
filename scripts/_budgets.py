"""
_budgets.py - Load web-claw/references/budgets.yaml.

Uses PyYAML if installed; otherwise falls back to a minimal stdlib-only
parser that handles the YAML subset used by budgets.yaml (nested mappings,
simple sequences, scalar values, comments). Works on Python 3.8+ without
external dependencies, in keeping with Web Claw's stdlib-only promise.

Usage:
    from _budgets import load_budgets

    b = load_budgets()
    floor = b["lighthouse"]["mobile"]["performance"]      # 90
    yt_min = b["research"]["youtube_subscriber_signal_minimum"]  # 50000
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any


_BUDGETS_PATH_ENV = "WEBCLAW_BUDGETS_PATH"
_DEFAULT_PATH = Path(__file__).resolve().parent.parent / "references" / "budgets.yaml"


def _coerce_scalar(value: str) -> Any:
    """Convert a YAML scalar string to a Python value."""
    v = value.strip()
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1]
    if v in ("null", "~", ""):
        return None
    if v in ("true", "True", "yes"):
        return True
    if v in ("false", "False", "no"):
        return False
    # Try int
    try:
        return int(v)
    except ValueError:
        pass
    # Try float
    try:
        return float(v)
    except ValueError:
        pass
    return v


def _strip_inline_comment(line: str) -> str:
    """Remove a trailing #-comment from a line, preserving #-in-quotes."""
    # Quick-and-dirty: cut at first ' #' that isn't inside quotes.
    in_single = in_double = False
    for i, c in enumerate(line):
        if c == "'" and not in_double:
            in_single = not in_single
        elif c == '"' and not in_single:
            in_double = not in_double
        elif c == "#" and not in_single and not in_double:
            # Require whitespace before # for it to be an inline comment.
            if i == 0 or line[i - 1].isspace():
                return line[:i].rstrip()
    return line


def _parse_yaml_minimal(text: str) -> dict:
    """Minimal block-style YAML parser for the budgets.yaml shape.

    Supports:
    - Comments (`# ...` whole-line or trailing inline)
    - Nested mappings via indentation (2-space convention)
    - Sequences: `- item` (one per line, scalar items)
    - Scalar values: int, float, bool, null, bare strings, quoted strings

    Does NOT support: flow style (`{...}`, `[...]`), anchors/aliases, multi-line
    scalars (`|`, `>`), tagged values, or sequences of mappings. Those are
    intentionally out of scope -- if budgets.yaml ever needs them, install
    PyYAML and this fallback yields to it automatically.
    """
    root: dict = {}
    # Stack of (key_indent, container). key_indent = indent of the KEY that
    # opened this container. Children appear at deeper indent.
    stack: list[tuple[int, Any]] = [(-2, root)]
    # last_key[i] = the key in stack[i-1]'s container that points to stack[i].
    # None for the root.
    last_key: list[str | None] = [None]

    for raw in text.splitlines():
        line = _strip_inline_comment(raw)
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)

        # Pop stack until the top container's key is shallower than us.
        while stack and stack[-1][0] >= indent:
            stack.pop()
            last_key.pop()

        if not stack:
            raise ValueError(f"indent error: stack empty for line {raw!r}")
        parent_indent, parent = stack[-1]

        if stripped.startswith("- "):
            item = _coerce_scalar(stripped[2:].strip())
            # If parent is an empty dict opened as a placeholder by a key,
            # promote it to a list on the grandparent. This handles the
            # `key:\n  - item\n  - item` pattern where the dict-placeholder
            # was speculative.
            if isinstance(parent, dict) and not parent and last_key[-1] is not None:
                placeholder_indent = stack[-1][0]
                stack.pop()
                placeholder_key = last_key.pop()
                _, grandparent = stack[-1]
                new_list: list = []
                grandparent[placeholder_key] = new_list
                stack.append((placeholder_indent, new_list))
                last_key.append(placeholder_key)
                parent = new_list
            if not isinstance(parent, list):
                raise ValueError(f"list item under non-list parent at indent {indent}: {raw!r}")
            parent.append(item)
            continue

        m = re.match(r"^([A-Za-z0-9_\-./]+)\s*:\s*(.*)$", stripped)
        if not m:
            raise ValueError(f"unparseable line: {raw!r}")
        key, value_text = m.group(1), m.group(2).strip()

        if not isinstance(parent, dict):
            raise ValueError(f"key under non-dict parent at indent {indent}: {key} (line {raw!r})")

        if value_text:
            parent[key] = _coerce_scalar(value_text)
        else:
            # Open a placeholder dict; the next line at deeper indent decides
            # whether to keep it as a dict (more keys) or promote to a list
            # (a `- item` at deeper indent).
            parent[key] = {}
            stack.append((indent, parent[key]))
            last_key.append(key)

    return root


def _try_pyyaml(text: str) -> dict | None:
    try:
        import yaml  # type: ignore
    except ImportError:
        return None
    return yaml.safe_load(text)


def load_budgets(path: str | os.PathLike | None = None) -> dict:
    """Load and parse budgets.yaml. Path resolution:
       1. Argument `path` if given.
       2. WEBCLAW_BUDGETS_PATH env var if set.
       3. <skill-root>/references/budgets.yaml (default).
    """
    if path is None:
        path = os.environ.get(_BUDGETS_PATH_ENV) or _DEFAULT_PATH
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        raise FileNotFoundError(f"budgets.yaml not found at: {p}")
    text = p.read_text(encoding="utf-8")
    parsed = _try_pyyaml(text)
    if parsed is None:
        parsed = _parse_yaml_minimal(text)
    if not isinstance(parsed, dict):
        raise ValueError(f"budgets.yaml top level must be a mapping, got {type(parsed).__name__}")
    return parsed


if __name__ == "__main__":
    # Quick self-test: load and pretty-print.
    import json
    import sys
    try:
        b = load_budgets()
    except Exception as e:
        print(f"FAIL: {e}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(b, indent=2, ensure_ascii=False))

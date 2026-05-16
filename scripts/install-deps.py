#!/usr/bin/env python3
"""
Web Claw Dependency Installer

Reads the "Install commands" section out of a tech-stack.md (or any
markdown file with fenced code blocks of shell commands) and executes
each command in order against a target frontend workspace.

This is the companion to install-packages.py (which installs by package
name); install-deps.py is the "read the plan, run the plan" variant.

Usage:
  python install-deps.py <path/to/tech-stack.md> --cwd <frontend-root>
  python install-deps.py ./meridian/research/tech-stack.md --cwd ./meridian --dry-run
  python install-deps.py ./meridian/research/tech-stack.md --cwd ./meridian --section "Install commands"

Exit codes:
  0  all commands succeeded (or dry-run completed)
  1  at least one command failed
  2  prerequisites missing (file not found, no commands extracted)
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import re
import shutil
import subprocess
from pathlib import Path


# Recognized package-manager invocations. The runner only executes lines that
# start with one of these tokens, so prose accidentally inside a code block
# does not get executed.
ALLOWED_PREFIXES = (
    "npm ", "pnpm ", "yarn ", "bun ",
    "npx ",
    "pnpm dlx ", "yarn dlx ", "bunx ",
)


def extract_commands(md_text: str, section_heading: str) -> list[str]:
    """Pull lines from fenced code blocks within the named section.

    Section detection: case-insensitive match against any heading line
    (e.g. "## Install commands"). The section ends at the next heading of
    equal or greater rank, or end of file.
    """
    lines = md_text.splitlines()

    # Find the section.
    heading_re = re.compile(r"^(#+)\s*(.+?)\s*$")
    section_start = None
    section_rank = None
    for i, line in enumerate(lines):
        m = heading_re.match(line)
        if m and m.group(2).strip().lower() == section_heading.strip().lower():
            section_start = i + 1
            section_rank = len(m.group(1))
            break

    if section_start is None:
        return []

    # Find the end (next heading of equal or shallower rank).
    section_end = len(lines)
    for i in range(section_start, len(lines)):
        m = heading_re.match(lines[i])
        if m and len(m.group(1)) <= section_rank:
            section_end = i
            break

    body = lines[section_start:section_end]

    # Walk fenced code blocks, collect command lines.
    commands: list[str] = []
    in_fence = False
    for raw in body:
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("$ "):
            stripped = stripped[2:].strip()
        if stripped.startswith(ALLOWED_PREFIXES):
            commands.append(stripped)
        # Silently skip lines we don't recognize. The user can quote them in
        # prose if they need; only allowlisted prefixes execute.
    return commands


def run_command(cmd: str, cwd: Path, dry_run: bool) -> int:
    print(f"$ {cmd}")
    if dry_run:
        return 0

    head = cmd.split()[0]
    resolved = shutil.which(head) or shutil.which(head + ".cmd")
    if not resolved:
        print(f"  ERROR: {head} not found on PATH.")
        return 127

    parts = cmd.split()
    parts[0] = resolved
    try:
        result = subprocess.run(parts, cwd=cwd, check=False)
        return result.returncode
    except FileNotFoundError as e:
        print(f"  ERROR: failed to launch {parts[0]}: {e}")
        return 127


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tech_stack_md", help="Path to a markdown file containing an `Install commands` section.")
    parser.add_argument("--cwd", default=".", help="Frontend workspace (where commands will run).")
    parser.add_argument(
        "--section",
        default="Install commands",
        help="Markdown heading to extract commands from (default: 'Install commands').",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing.")
    args = parser.parse_args()

    md_path = Path(args.tech_stack_md).expanduser().resolve()
    if not md_path.is_file():
        print(f"ERROR: file not found: {md_path}")
        return 2

    cwd = Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        print(f"ERROR: workspace not found: {cwd}")
        return 2

    md = md_path.read_text(encoding="utf-8")
    commands = extract_commands(md, args.section)

    if not commands:
        print(f"ERROR: no executable install commands found under '{args.section}' in {md_path.name}.")
        print("       Add a fenced code block under the section with lines starting with npm/pnpm/yarn/bun/npx.")
        return 2

    print(f"Workspace : {cwd}")
    print(f"Source    : {md_path}")
    print(f"Section   : {args.section}")
    print(f"Commands  : {len(commands)}")
    if args.dry_run:
        print("Mode      : dry-run")
    print()

    failures = 0
    for cmd in commands:
        rc = run_command(cmd, cwd, args.dry_run)
        if rc != 0:
            failures += 1
            print(f"  -> exit {rc}")

    print()
    if failures:
        print(f"[FAIL] {failures}/{len(commands)} command(s) failed.")
        return 1
    print(f"[OK] {len(commands)} command(s) {'previewed' if args.dry_run else 'executed'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

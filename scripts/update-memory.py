#!/usr/bin/env python3
"""
Web Claw Memory Updater

Updates specific fields in a project's memory.md from the command line.
Use after completing an artifact or advancing a pipeline state,
especially in automated or scripted workflows.

Usage:
    python update-memory.py <memory-file> [options]

Examples:
    python update-memory.py ./meridian/memory.md --phase BLUEPRINT:SITEMAP --sign-off PENDING
    python update-memory.py ./meridian/memory.md --artifact blueprint/sitemap.md --sign-off YES
    python update-memory.py ./meridian/memory.md --next "Spawn Designer Agent to produce style-guide.md"
    python update-memory.py ./meridian/memory.md --blocker "User must confirm which pages to include"
    python update-memory.py ./meridian/memory.md --stack "Next.js 15 + Tailwind 4 + GSAP 3.12"
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import datetime as dt
import re
from pathlib import Path


VALID_PHASES = [
    "IGNITION",
    "BLUEPRINT:SITEMAP",
    "BLUEPRINT:STYLE-GUIDE",
    "BLUEPRINT:WIREFRAMES",
    "BLUEPRINT:ANIMATIONS",
    "RESEARCH:AWWWARDS",
    "RESEARCH:YOUTUBE",
    "EXECUTION:STACK",
    "EXECUTION:PLAN",
    "EXECUTION:PHASE-1",
    "EXECUTION:PHASE-2",
    "EXECUTION:PHASE-3",
    "QA:FINAL",
    "DONE",
]

VALID_SIGNOFF = ["YES", "NO", "PENDING", "AUTO"]


def read_memory(path: Path) -> str:
    if not path.exists():
        print(f"[ERROR] memory.md not found at: {path}")
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def update_field(content: str, field: str, value: str) -> str:
    """Replace a `- Field: value` line in the memory.md."""
    pattern = re.compile(rf"^(- {re.escape(field)}:).*$", re.MULTILINE)
    replacement = f"\\1 {value}"
    new_content, count = pattern.subn(replacement, content)
    if count == 0:
        print(f"[WARN] Field '- {field}:' not found in memory.md. No change made.")
    return new_content


def update_last_updated(content: str, now: str) -> str:
    pattern = re.compile(r"^(Last updated:).*$", re.MULTILINE)
    replacement = f"\\1 {now}"
    return pattern.sub(replacement, content)


def add_blocker(content: str, blocker: str) -> str:
    """Append a blocker under the ## Blockers section."""
    # Remove the "- None" line if present
    content = re.sub(r"^- None$", "", content, flags=re.MULTILINE)
    # Find the Blockers section and append
    pattern = re.compile(r"(## Blockers\n)", re.MULTILINE)
    replacement = f"\\1- {blocker}\n"
    new_content, count = pattern.subn(replacement, content, count=1)
    if count == 0:
        print("[WARN] '## Blockers' section not found. Blocker not added.")
    return new_content


def add_decision(content: str, decision_id: str, topic: str, filepath: str) -> str:
    """Append a decision entry under ## Pinned Decisions."""
    entry = f"- [{decision_id}] {topic} -> {filepath}\n"
    pattern = re.compile(r"(## Pinned Decisions\n)", re.MULTILINE)
    new_content, count = pattern.subn(f"\\1{entry}", content, count=1)
    if count == 0:
        print("[WARN] '## Pinned Decisions' section not found. Decision not added.")
    return new_content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("memory_file", help="Path to the project memory.md file")
    parser.add_argument("--phase", choices=VALID_PHASES, help="Set the current pipeline phase")
    parser.add_argument("--step", help="Set the current step within the phase")
    parser.add_argument("--artifact", help="Set the last artifact path (relative to project root)")
    parser.add_argument("--sign-off", choices=VALID_SIGNOFF, dest="sign_off", help="Set user sign-off status")
    parser.add_argument("--next", help="Set the next action (imperative sentence)")
    parser.add_argument("--stack", help="Set the chosen tech stack")
    parser.add_argument("--deploy", help="Set the deploy target")
    parser.add_argument("--motion", choices=["restrained", "active", "maximalist"], help="Set motion intensity")
    parser.add_argument("--mode", choices=["interactive", "fast"], help="Set run mode (interactive | fast)")
    parser.add_argument("--blocker", help="Add a blocker entry")
    parser.add_argument(
        "--decision",
        nargs=3,
        metavar=("ID", "TOPIC", "FILE"),
        help="Add a pinned decision: --decision DECISION-001 'stack' 'decisions/001-stack.md'",
    )
    parser.add_argument("--clear-blockers", action="store_true", help="Replace all blockers with '- None'")

    args = parser.parse_args()

    if len(sys.argv) < 3:
        parser.print_help()
        return 0

    path = Path(args.memory_file).expanduser().resolve()
    content = read_memory(path)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    content = update_last_updated(content, now)

    if args.phase:
        content = update_field(content, "Phase", args.phase)
        print(f"[OK] Phase -> {args.phase}")

    if args.step:
        content = update_field(content, "Step", args.step)
        print(f"[OK] Step -> {args.step}")

    if args.artifact:
        content = update_field(content, "Last artifact", args.artifact)
        print(f"[OK] Last artifact -> {args.artifact}")

    if args.sign_off:
        content = update_field(content, "User sign-off", args.sign_off)
        print(f"[OK] User sign-off -> {args.sign_off}")

    if args.next:
        content = update_field(content, "Next action", args.next)
        print(f"[OK] Next action -> {args.next}")

    if args.stack:
        content = update_field(content, "Stack", args.stack)
        print(f"[OK] Stack -> {args.stack}")

    if args.deploy:
        content = update_field(content, "Deploy", args.deploy)
        print(f"[OK] Deploy -> {args.deploy}")

    if args.motion:
        content = update_field(content, "Motion", args.motion)
        print(f"[OK] Motion -> {args.motion}")

    if args.mode:
        content = update_field(content, "Mode", args.mode)
        print(f"[OK] Mode -> {args.mode}")

    if args.blocker:
        content = add_blocker(content, args.blocker)
        print(f"[OK] Blocker added: {args.blocker}")

    if args.clear_blockers:
        content = re.sub(
            r"(## Blockers\n)((?:- .+\n)*)",
            r"\1- None\n",
            content,
            flags=re.MULTILINE,
        )
        print("[OK] Blockers cleared")

    if args.decision:
        decision_id, topic, filepath = args.decision
        content = add_decision(content, decision_id, topic, filepath)
        print(f"[OK] Decision added: [{decision_id}] {topic} -> {filepath}")

    path.write_text(content, encoding="utf-8")
    print(f"\n[OK] memory.md updated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

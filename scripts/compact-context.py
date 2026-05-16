#!/usr/bin/env python3
"""
Web Claw Context Compaction Tool

Generates a Compaction Snapshot from a project's current state and
writes it into memory.md. Run this when the context window is near
its limit to preserve enough state for a fresh agent session to resume
without losing progress.

The snapshot contains:
  - Summaries of all produced artifacts (from blueprint/, research/)
  - The last artifact verbatim (if under 2000 tokens / ~8000 chars)
  - The current work-in-progress description

Usage:
    python compact-context.py <project-dir> [--wip "description of current in-progress work"]
    python compact-context.py ./meridian
    python compact-context.py ./meridian --wip "Designer Agent mid-way through color token spec"
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import datetime as dt
from pathlib import Path


MAX_VERBATIM_CHARS = 8000  # ~2000 tokens -- paste verbatim if under this


ARTIFACT_SUMMARIES_TEMPLATE = """\
### Artifact summaries (all produced artifacts)
{summaries}

### Last artifact verbatim
{verbatim}

### Current work in progress
{wip}
"""


def read_if_exists(path: Path) -> str | None:
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def one_line_summary(content: str, max_chars: int = 200) -> str:
    """Extract a compact summary from an artifact's content."""
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]
    summary = " ".join(lines[:3])
    if len(summary) > max_chars:
        summary = summary[:max_chars].rstrip() + "…"
    return summary


def build_artifact_summaries(project_root: Path) -> list[str]:
    artifacts = [
        ("blueprint/discovery.md", "Discovery"),
        ("blueprint/sitemap.md", "Sitemap"),
        ("blueprint/style-guide.md", "Style guide"),
        ("blueprint/wireframes.md", "Wireframes"),
        ("blueprint/animations.md", "Motion spec"),
        ("research/awwwards-references.md", "Awwwards research"),
        ("research/youtube-techniques.md", "YouTube research"),
        ("research/tech-stack.md", "Tech stack"),
        ("plan.md", "Master plan"),
        ("phase-1.md", "Phase 1 file"),
        ("phase-2.md", "Phase 2 file"),
        ("phase-3.md", "Phase 3 file"),
    ]

    summaries = []
    for rel_path, label in artifacts:
        path = project_root / rel_path
        content = read_if_exists(path)
        if content:
            summary = one_line_summary(content)
            summaries.append(f"- {label} ({rel_path}): {summary}")

    return summaries


def get_last_artifact_path(memory_content: str) -> str | None:
    for line in memory_content.splitlines():
        if line.strip().startswith("- Last artifact:"):
            value = line.split(":", 1)[1].strip()
            if value and value not in ("(none yet)", "PENDING", ""):
                return value
    return None


def update_compaction_snapshot(memory_path: Path, snapshot_text: str) -> None:
    content = memory_path.read_text(encoding="utf-8")
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    section_header = "## Compaction Snapshot"
    snapshot_block = f"""{section_header}
Captured: {now}

{snapshot_text}
"""

    if section_header in content:
        # Replace existing snapshot section
        import re
        pattern = re.compile(r"## Compaction Snapshot.*?(?=\n## |\Z)", re.DOTALL)
        new_content = pattern.sub(snapshot_block.rstrip(), content, count=1)
    else:
        # Append at end
        new_content = content.rstrip() + "\n\n" + snapshot_block

    # Update Last updated timestamp
    import re
    new_content = re.sub(r"^(Last updated:).*$", f"\\1 {now}", new_content, flags=re.MULTILINE)

    memory_path.write_text(new_content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_dir", help="Path to the Web Claw project directory")
    parser.add_argument(
        "--wip",
        default="",
        help="Description of the current work in progress (what was being done when context got full)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the snapshot without writing to memory.md",
    )
    args = parser.parse_args()

    project_root = Path(args.project_dir).expanduser().resolve()
    memory_path = project_root / "memory.md"

    if not memory_path.exists():
        print(f"[ERROR] memory.md not found in: {project_root}")
        print("        Is this a Web Claw project? Run scripts/init-project.py first.")
        sys.exit(1)

    memory_content = memory_path.read_text(encoding="utf-8")

    # Build artifact summaries
    print("Scanning project artifacts...")
    summaries = build_artifact_summaries(project_root)

    if not summaries:
        print("[WARN] No artifacts found in project. Snapshot will be minimal.")
        summaries = ["- No artifacts produced yet."]

    summaries_text = "\n".join(summaries)

    # Get last artifact for verbatim inclusion
    last_artifact_rel = get_last_artifact_path(memory_content)
    verbatim_text = "(No last artifact recorded in memory.md)"

    if last_artifact_rel:
        last_artifact_path = project_root / last_artifact_rel
        last_content = read_if_exists(last_artifact_path)
        if last_content:
            if len(last_content) <= MAX_VERBATIM_CHARS:
                verbatim_text = f"<!-- Full content of {last_artifact_rel} -->\n\n```markdown\n{last_content.strip()}\n```"
                print(f"[OK] Including {last_artifact_rel} verbatim ({len(last_content)} chars)")
            else:
                # Include only first and last sections
                lines = last_content.splitlines()
                head = "\n".join(lines[:30])
                tail = "\n".join(lines[-20:])
                verbatim_text = (
                    f"<!-- {last_artifact_rel} is too large for full verbatim. "
                    f"Showing first 30 lines and last 20 lines. -->\n\n"
                    f"```markdown\n{head}\n\n[... middle truncated ...]\n\n{tail}\n```"
                )
                print(f"[OK] {last_artifact_rel} is large ({len(last_content)} chars) -- truncated")
        else:
            verbatim_text = f"(File not found: {last_artifact_rel})"
    else:
        print("[INFO] No last artifact path in memory.md")

    wip_text = args.wip if args.wip else "(No work-in-progress description provided. Check memory.md -> State -> Step.)"

    snapshot_text = ARTIFACT_SUMMARIES_TEMPLATE.format(
        summaries=summaries_text,
        verbatim=verbatim_text,
        wip=wip_text,
    )

    if args.dry_run:
        print("\n" + "-" * 60)
        print("COMPACTION SNAPSHOT (dry run -- not written to memory.md)")
        print("-" * 60)
        print(snapshot_text)
        print("-" * 60)
        print("\nRun without --dry-run to write to memory.md.")
        return 0

    update_compaction_snapshot(memory_path, snapshot_text)
    print(f"\n[OK] Compaction snapshot written to memory.md")
    print(f"     Any fresh agent session can now resume from memory.md alone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

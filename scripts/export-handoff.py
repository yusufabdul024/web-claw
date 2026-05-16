#!/usr/bin/env python3
"""
export-handoff.py

Package a completed (or in-flight) Web Claw project as a single
self-contained artifact for transfer to another team, freelancer, or agent.

Three shapes are supported, per references/handoff-export.md:

  --shape tarball    <project>-handoff.tar.gz   (default; mirrors live layout)
  --shape json       <project>-handoff.json     (path/content pairs)
  --shape markdown   <project>-handoff.md       (one mega-markdown bundle)

A handoff-manifest.json is written at the root of the bundle in all shapes.
The Web Claw skill folder (the one containing this script) is bundled inside
the export so the receiver can run scripts/* without a separate install.

Usage:
  python export-handoff.py --workspace <project>
  python export-handoff.py --workspace <project> --shape tarball --out dist/
  python export-handoff.py --workspace <project> --shape json
  python export-handoff.py --workspace <project> --shape markdown
  python export-handoff.py --workspace <project> --include-snapshots   # also bundle qa/snapshots
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import base64
import datetime as dt
import json
import tarfile
from pathlib import Path


# Files and directories under the project workspace that always go in the bundle.
ALWAYS_INCLUDE = [
    "memory.md",
    "blueprint/",
    "research/",
    "qa/",
    "decisions/",
    "plan.md",
    "phase-1.md",
    "phase-2.md",
    "phase-3.md",
    "site-brief.json",
    "dependencies.json",
    "sources.json",
    "design/",
    "assets/og/",
    "prompts/",
]

# Heavy artifacts the user opts into. Snapshots can be very large.
OPT_IN_INCLUDE = {
    "snapshots": "qa/snapshots/",
}

# Skill files to bundle so the receiver can run scripts/* offline. The skill
# package is the directory two levels up from this file (web-claw/scripts/x.py
# -> web-claw/).
SKILL_ROOT = Path(__file__).resolve().parent.parent

# Skill subpaths to bundle. Tests, __pycache__, .git get excluded.
SKILL_INCLUDE = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/",
    "references/",
    "qa/",
    "scripts/",
    "assets/",
    ".github/",
]
SKILL_EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", "node_modules", ".git"}


def _is_excluded(path: Path) -> bool:
    return any(part in SKILL_EXCLUDE_DIRS for part in path.parts)


def _walk(base: Path, rel: str) -> list[Path]:
    """Return every regular file under base/rel that is not excluded."""
    target = base / rel
    if target.is_file():
        return [target] if not _is_excluded(target) else []
    if not target.is_dir():
        return []
    return sorted(
        p for p in target.rglob("*")
        if p.is_file() and not _is_excluded(p)
    )


def collect_files(workspace: Path, include_snapshots: bool) -> dict[str, Path]:
    """Return {arcname: source-path} for every file that lands in the bundle.

    arcname is the path inside the bundle, relative to its root. The project
    folder ends up as `<project>/` and the skill ends up as `<project>/web-claw/`.
    """
    project_name = workspace.name
    arc_root = project_name
    files: dict[str, Path] = {}

    # Project artifacts.
    for rel in ALWAYS_INCLUDE:
        for src in _walk(workspace, rel):
            arcname = f"{arc_root}/{src.relative_to(workspace).as_posix()}"
            files[arcname] = src

    # Opt-in heavy artifacts.
    if include_snapshots:
        for src in _walk(workspace, OPT_IN_INCLUDE["snapshots"]):
            arcname = f"{arc_root}/{src.relative_to(workspace).as_posix()}"
            files[arcname] = src

    # Skill bundle inside the project copy.
    for rel in SKILL_INCLUDE:
        for src in _walk(SKILL_ROOT, rel):
            arcname = f"{arc_root}/web-claw/{src.relative_to(SKILL_ROOT).as_posix()}"
            files[arcname] = src

    return files


# Manifest contract -- mirrors references/handoff-export.md "Required manifest"
# section. Each tier is a list of paths relative to the project workspace.
MANIFEST_TIERS: list[tuple[int, str, list[str]]] = [
    (1, "Pipeline state", [
        "memory.md",
        "site-brief.json",
        "sources.json",
        "dependencies.json",
        "qa/qa-plan.md",
    ]),
    (2, "Blueprint", [
        "blueprint/discovery.md",
        "blueprint/sitemap.md",
        "blueprint/style-guide.md",
        "blueprint/wireframes.md",
        "blueprint/animations.md",
    ]),
    (3, "Research", [
        "research/awwwards-references.md",
        "research/youtube-techniques.md",
        "research/tech-stack.md",
    ]),
    (4, "Execution", [
        "plan.md",
        "phase-1.md",
        "phase-2.md",
        "phase-3.md",
        "prompts/sequential-prompts.md",
    ]),
    (5, "QA evidence", [
        "qa/phase-1-report.md",
        "qa/phase-2-report.md",
        "qa/phase-3-report.md",
        "qa/final-report.md",
    ]),
]

# Web Claw skill version. Kept in sync with the SKILL.md / pyproject if/when
# we add one. For now this is the published manifest version.
WEB_CLAW_VERSION = "1.0.0"


def _read_memory_field(workspace: Path, field: str) -> str | None:
    """Read a single `- Field: value` line from memory.md."""
    memory = workspace / "memory.md"
    if not memory.exists():
        return None
    needle = f"- {field}:"
    for line in memory.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(needle):
            return stripped.split(":", 1)[1].strip()
    return None


def memory_phase(workspace: Path) -> str | None:
    return _read_memory_field(workspace, "Phase")


def memory_next_action(workspace: Path) -> str | None:
    return _read_memory_field(workspace, "Next action")


def _file_status(workspace: Path, rel: str) -> tuple[str, int | None]:
    """Return (status, size_bytes). Status values mirror handoff-export.md:
    present | missing | n/a | partial.
    """
    p = workspace / rel
    if not p.exists():
        return ("missing", None)
    if p.is_dir():
        # We don't include bare directories in deliverables; this only handles
        # accidental directory matches (none expected from MANIFEST_TIERS).
        return ("present", None)
    size = p.stat().st_size
    if size == 0:
        return ("partial", 0)
    return ("present", size)


def build_deliverables(workspace: Path) -> list[dict]:
    items: list[dict] = []
    for tier, _label, paths in MANIFEST_TIERS:
        for rel in paths:
            status, size = _file_status(workspace, rel)
            entry: dict = {"path": rel, "tier": tier, "status": status}
            if size is not None:
                entry["size_bytes"] = size
            items.append(entry)
    return items


def build_decisions(workspace: Path) -> list[dict]:
    decisions_dir = workspace / "decisions"
    if not decisions_dir.is_dir():
        return []
    out: list[dict] = []
    for p in sorted(decisions_dir.glob("*.md")):
        # Filename convention: NNN-topic-with-dashes.md
        stem = p.stem
        decision_id = stem.split("-", 1)[0] if "-" in stem else stem
        topic_raw = stem.split("-", 1)[1] if "-" in stem else ""
        topic = topic_raw.replace("-", " ").strip()
        out.append({
            "id": f"DECISION-{decision_id}",
            "topic": topic or "(no topic in filename)",
            "path": str(p.relative_to(workspace).as_posix()),
        })
    return out


def build_qa_evidence(workspace: Path) -> dict:
    """Build the structured qa_evidence object documented in handoff-export.md.

    Pass/fail is derived heuristically from the corresponding report file:
    - file missing  -> passed: null
    - file empty    -> passed: null
    - "FAIL"/"BLOCK"/"NOT PASSED" present in body -> passed: false
    - otherwise present -> passed: true
    Anything else surfaces as `blockers: [...]` (lines with FAIL/BLOCK markers).
    """
    def evaluate(report_path: Path) -> dict:
        if not report_path.is_file():
            return {"passed": None, "report": None}
        size = report_path.stat().st_size
        rel = report_path.relative_to(workspace).as_posix()
        if size == 0:
            return {"passed": None, "report": rel}
        text = report_path.read_text(encoding="utf-8", errors="replace")
        text_lower = text.lower()
        fail_markers = ["fail", "blocker", "not passed", "blocked"]
        if any(m in text_lower for m in fail_markers):
            blockers = [
                ln.strip("-* \t").strip()
                for ln in text.splitlines()
                if any(m in ln.lower() for m in fail_markers)
            ][:8]
            return {"passed": False, "report": rel, "blockers": blockers}
        return {"passed": True, "report": rel}

    return {
        "phase_1": evaluate(workspace / "qa" / "phase-1-report.md"),
        "phase_2": evaluate(workspace / "qa" / "phase-2-report.md"),
        "phase_3": evaluate(workspace / "qa" / "phase-3-report.md"),
        "qa_final": evaluate(workspace / "qa" / "final-report.md"),
    }


def build_manifest(workspace: Path, files: dict[str, Path], shape: str) -> dict:
    project_name = workspace.name
    return {
        "web_claw_version": WEB_CLAW_VERSION,
        "exported_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "shape": shape,
        "project": {
            "name": project_name,
            "slug": _read_memory_field(workspace, "Slug") or project_name,
            "current_phase": memory_phase(workspace),
            "user_signoff": _read_memory_field(workspace, "User sign-off"),
            "next_action": memory_next_action(workspace),
            "motion_intensity": _read_memory_field(workspace, "Motion"),
            "stack": _read_memory_field(workspace, "Stack"),
            "deploy_target": _read_memory_field(workspace, "Deploy"),
            "mode": _read_memory_field(workspace, "Mode"),
        },
        "skill": {
            "name": "web-claw",
            "version": WEB_CLAW_VERSION,
            "root_in_bundle": f"{project_name}/web-claw/",
        },
        "deliverables": build_deliverables(workspace),
        "decisions": build_decisions(workspace),
        "qa_evidence": build_qa_evidence(workspace),
        "file_count": len(files),
        "receiver_instructions": (
            "Open this folder in any AI coding agent. Read web-claw/SKILL.md "
            "first, then memory.md, then resume from `project.next_action`. "
            "All numeric budgets are in web-claw/references/budgets.yaml. The "
            "four-signal YouTube credibility heuristic lives in "
            "web-claw/references/youtube-channels.md."
        ),
    }


def write_tarball(out: Path, files: dict[str, Path], manifest: dict) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(out, "w:gz") as tf:
        manifest_bytes = json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8")
        # handoff-manifest.json at the bundle root (alongside the project folder).
        info = tarfile.TarInfo(name="handoff-manifest.json")
        info.size = len(manifest_bytes)
        import io
        tf.addfile(info, io.BytesIO(manifest_bytes))
        for arcname, src in files.items():
            try:
                tf.add(src, arcname=arcname, recursive=False)
            except OSError as e:
                print(f"warn: could not add {src}: {e}", file=sys.stderr)


def is_binary(path: Path) -> bool:
    """Heuristic: read first 4kB, check for null bytes."""
    try:
        chunk = path.open("rb").read(4096)
    except OSError:
        return True
    return b"\x00" in chunk


def write_json(out: Path, files: dict[str, Path], manifest: dict) -> None:
    """Each file becomes a record: { path, encoding, content }.
    Text is utf-8; binary is base64.
    """
    records: list[dict] = []
    for arcname, src in files.items():
        if is_binary(src):
            try:
                content = base64.b64encode(src.read_bytes()).decode("ascii")
                records.append({"path": arcname, "encoding": "base64", "content": content})
            except OSError as e:
                print(f"warn: could not read {src}: {e}", file=sys.stderr)
        else:
            try:
                records.append({"path": arcname, "encoding": "utf-8", "content": src.read_text(encoding="utf-8")})
            except (OSError, UnicodeDecodeError) as e:
                print(f"warn: could not read {src} as utf-8: {e}", file=sys.stderr)
    payload = {"manifest": manifest, "files": records}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_markdown(out: Path, files: dict[str, Path], manifest: dict) -> None:
    """One mega-markdown with every text file as a fenced block.
    Binary files are listed but their contents are omitted (note instead).
    """
    lines: list[str] = []
    lines.append(f"# Web Claw Handoff: {manifest['project']['name']}")
    lines.append("")
    lines.append("```json")
    lines.append("// handoff-manifest.json")
    lines.append(json.dumps(manifest, indent=2, ensure_ascii=False))
    lines.append("```")
    lines.append("")
    for arcname, src in sorted(files.items()):
        lines.append(f"## `{arcname}`")
        lines.append("")
        if is_binary(src):
            lines.append(f"_(binary file: {src.stat().st_size} bytes; omitted from markdown bundle. Use tarball or json shape to include.)_")
            lines.append("")
            continue
        suffix = src.suffix.lstrip(".") or "text"
        fence_lang = {
            "md": "markdown", "py": "python", "js": "javascript",
            "ts": "typescript", "json": "json", "yaml": "yaml",
            "yml": "yaml", "sh": "bash", "ps1": "powershell",
            "css": "css", "html": "html", "txt": "text",
        }.get(suffix, "text")
        try:
            content = src.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            content = "(could not read as utf-8)"
        lines.append(f"```{fence_lang}")
        lines.append(content)
        lines.append("```")
        lines.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace", required=True, help="Path to the Web Claw project workspace.")
    parser.add_argument("--shape", default="tarball", choices=["tarball", "json", "markdown"])
    parser.add_argument("--out", default=None, help="Output path (file or directory). Default: alongside the workspace.")
    parser.add_argument("--include-snapshots", action="store_true",
                        help="Also bundle qa/snapshots/ (can be large).")
    args = parser.parse_args(argv[1:])

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.is_dir():
        print(f"error: workspace is not a directory: {workspace}", file=sys.stderr)
        return 2

    files = collect_files(workspace, args.include_snapshots)
    if not files:
        print(f"error: no files matched in {workspace}. Is this a Web Claw project?", file=sys.stderr)
        return 1

    manifest = build_manifest(workspace, files, args.shape)

    # Resolve output path. If --out is a directory, append the default filename.
    project_name = workspace.name
    default_name = {
        "tarball":  f"{project_name}-handoff.tar.gz",
        "json":     f"{project_name}-handoff.json",
        "markdown": f"{project_name}-handoff.md",
    }[args.shape]

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        if out_path.is_dir():
            out_path = out_path / default_name
    else:
        out_path = workspace.parent / default_name

    if args.shape == "tarball":
        write_tarball(out_path, files, manifest)
    elif args.shape == "json":
        write_json(out_path, files, manifest)
    elif args.shape == "markdown":
        write_markdown(out_path, files, manifest)

    size_kb = round(out_path.stat().st_size / 1024.0, 1)
    summary = {
        "shape": args.shape,
        "output": str(out_path),
        "size_kb": size_kb,
        "file_count": len(files),
        "manifest": manifest,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

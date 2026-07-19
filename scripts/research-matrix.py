#!/usr/bin/env python3
"""
Web Claw Research Matrix Generator

Converts the project's sources.json into a structured, source-agnostic
markdown matrix suitable for agent review. Web Claw v3 accepts user-provided
links, screenshots, moodboard boards, social posts, shipped websites, product
pages, articles, videos, and galleries. No source type is mandatory and no
single popularity metric is a hard gate.

Usage:
    python research-matrix.py --sources <project>/sources.json --output <project>/research/research-matrix.md
    python research-matrix.py --sources ./meridian/sources.json --output ./meridian/research/research-matrix.md
    python research-matrix.py --sources ./meridian/sources.json --output ./meridian/research/research-matrix.md --allow-warnings
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED = {"kind", "title", "date_accessed", "why_relevant"}


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def bullet_list(items: list[str]) -> str:
    if not items:
        return "- None recorded."
    return "\n".join(f"- {item}" for item in items)


def load_sources(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "sources" in data:
        data = data["sources"]
    if not isinstance(data, list):
        raise ValueError("sources.json must be a JSON array or an object with a 'sources' array.")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Every source entry must be a JSON object.")
    return list(data)


def validate_sources(sources: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for i, source in enumerate(sources, 1):
        missing = sorted(f for f in REQUIRED if not str(source.get(f, "")).strip())
        if missing:
            errors.append(f"Source {i} missing required fields: {', '.join(missing)}")
        if not str(source.get("url", "")).strip() and not str(source.get("local_artifact", "")).strip():
            errors.append(f"Source {i} must include either url or local_artifact.")
        if not str(source.get("what_taking") or source.get("taking") or "").strip():
            errors.append(f"Source {i} missing what_taking.")
        if not str(source.get("what_not_taking") or source.get("not_taking") or "").strip():
            errors.append(f"Source {i} missing what_not_taking.")
        # Copying-risk schema validation. Medium/high risk REQUIRES the agent
        # to have written `what_not_taking` -- the explicit "what we are not
        # copying" line is the mitigation. Without it, surface as an error.
        copying_risk = (source.get("copying_risk") or "").strip().lower()
        if copying_risk and copying_risk not in VALID_COPYING_RISK:
            errors.append(
                f"Source {i}: copying_risk={copying_risk!r} is not one of "
                f"{sorted(VALID_COPYING_RISK)}."
            )
        if copying_risk in ("medium", "high"):
            what_not_taking = source.get("what_not_taking") or source.get("not_taking")
            if not (what_not_taking and str(what_not_taking).strip()):
                errors.append(
                    f"Source {i}: copying_risk={copying_risk!r} requires "
                    f"`what_not_taking` to be filled (an explicit statement of "
                    f"what is off-limits from this source)."
                )
    return errors


VALID_COPYING_RISK = {"none", "low", "medium", "high"}


def render_source(source: dict[str, Any], index: int) -> str:
    kind = str(source.get("kind", "reference")).title()
    title = str(source.get("title") or source.get("video_title") or "Untitled")
    lines = [
        f"## {index}. {title}",
        "",
        f"- Kind: {kind}",
        f"- URL: {source.get('url', '')}",
        f"- Local artifact: {source.get('local_artifact', '')}",
        f"- Date accessed: {source.get('date_accessed', '')}",
        f"- Provided by: {source.get('provided_by', '')}",
        f"- Why relevant: {source.get('why_relevant', '')}",
    ]
    # Provenance / copying-risk schema (Web Claw v1.1):
    # - screenshot: relative path under assets/research/ saved on first visit
    # - what_taking: one-line description of the *idea* we are drawing from
    # - what_not_taking: one-line description of what is off-limits (e.g. their
    #   exact palette/copy/layout). Forces the agent to *adapt* rather than copy.
    # - copying_risk: none | low | medium | high. Medium/high require explicit
    #   mitigation note and trigger a review at the QA stage.
    # - library_detection_method: how libraries on the page were verified
    #   (e.g. devtools / network panel / wappalyzer / view-source)
    screenshot = source.get("screenshot")
    what_taking = source.get("what_taking") or source.get("taking")
    what_not_taking = source.get("what_not_taking") or source.get("not_taking")
    copying_risk = (source.get("copying_risk") or "").strip().lower() or None
    library_detection_method = source.get("library_detection_method")
    if any([screenshot, what_taking, what_not_taking, copying_risk, library_detection_method]):
        lines += ["", "### Provenance"]
        if screenshot:
            lines.append(f"- Screenshot: `{screenshot}`")
        if what_taking:
            lines.append(f"- What we're taking: {what_taking}")
        if what_not_taking:
            lines.append(f"- What we're explicitly NOT taking: {what_not_taking}")
        if copying_risk:
            note = " (UNKNOWN -- expected one of none/low/medium/high)" if copying_risk not in VALID_COPYING_RISK else ""
            lines.append(f"- Copying risk: {copying_risk}{note}")
        if library_detection_method:
            lines.append(f"- Library detection: {library_detection_method}")
    if source.get("kind") == "youtube":
        lines += [
            "",
            "### YouTube metadata",
            f"- Channel: {source.get('channel', '')}",
            f"- Channel URL: {source.get('channel_url', '')}",
            f"- Subscriber count: {source.get('subscriber_count', '')}",
            f"- Verified on: {source.get('subscriber_count_verified_on', '')}",
            f"- Video title: {source.get('video_title', '')}",
            f"- Published: {source.get('published', '')}",
            f"- Transcript / minute marker: {source.get('transcript_marker', source.get('minute_marker', ''))}",
        ]
    if source.get("kind") == "awwwards":
        lines += [
            "",
            "### Awwwards metadata",
            f"- Awwwards status: {source.get('awwwards_status', '')}",
            f"- Libraries detected: {source.get('libraries_detected', '')}",
            f"- Standout device: {source.get('standout_device', '')}",
        ]
    lines += [
        "",
        "### Application",
        "",
        f"- Axis: {', '.join(as_list(source.get('axis')))}",
        f"- Applicable to: {source.get('applicable_to', '')}",
        f"- Implementation notes: {source.get('implementation_notes', '')}",
        f"- Verification method: {source.get('verification_method', '')}",
        "",
        "### Patterns",
        "",
        bullet_list(as_list(source.get("patterns"))),
        "",
        "### Techniques",
        "",
        bullet_list(as_list(source.get("techniques"))),
        "",
        "### Libraries",
        "",
        bullet_list(as_list(source.get("libraries"))),
        "",
        "### Risks",
        "",
        bullet_list(as_list(source.get("risks"))),
        "",
    ]
    return "\n".join(lines)


def render_markdown(sources: list[dict[str, Any]], source_file: Path) -> str:
    groups: dict[str, list[dict[str, Any]]] = {}
    for source in sources:
        groups.setdefault(str(source.get("kind", "reference")), []).append(source)

    lines = [
        "# Web Claw Research Matrix",
        "",
        f"Source file: `{source_file}`",
        "",
        "> Use this matrix for synthesis only. It is not permission to copy layouts, "
        "assets, code, copy, or exact animation choreography from any cited source.",
        "",
    ]
    counter = 1
    for group_name in sorted(groups):
        lines += [f"# {group_name.title()} Sources", ""]
        for source in groups[group_name]:
            lines.append(render_source(source, counter))
            counter += 1
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sources", required=True, help="Path to sources.json")
    parser.add_argument("--output", required=True, help="Markdown output path")
    parser.add_argument("--allow-warnings", action="store_true",
                        help="Write the matrix even if source records are incomplete (with warnings)")
    args = parser.parse_args()

    source_path = Path(args.sources).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not source_path.exists():
        print(f"ERROR: sources.json not found: {source_path}")
        return 1

    sources = load_sources(source_path)
    errors = validate_sources(sources)

    if errors and not args.allow_warnings:
        print("Validation failed. Fix these issues in sources.json:")
        for error in errors:
            print(f"  ERROR: {error}")
        print("\nRe-run with --allow-warnings to write anyway.")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(sources, source_path), encoding="utf-8")

    if errors:
        print(f"Wrote research matrix with warnings: {output_path}")
        for error in errors:
            print(f"  WARNING: {error}")
    else:
        print(f"Wrote research matrix: {output_path}")
        print(f"  {len(sources)} source(s) validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

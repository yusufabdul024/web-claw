#!/usr/bin/env python3
"""
Web Claw Research Matrix Generator

Converts the project's sources.json into a structured markdown matrix
suitable for agent review. Validates YouTube channels meet the subscriber
threshold defined in references/budgets.yaml (research.youtube_subscriber_signal_minimum,
currently 50000 -- a signal, not a hard floor; weight against the four-signal
heuristic in references/youtube-channels.md).

Usage:
    python research-matrix.py --sources <project>/sources.json --output <project>/research/research-matrix.md
    python research-matrix.py --sources ./meridian/sources.json --output ./meridian/research/research-matrix.md
    python research-matrix.py --sources ./meridian/sources.json --output ./meridian/research/research-matrix.md --allow-under-threshold
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

from _budgets import load_budgets


def _default_youtube_subscriber_min() -> int:
    """Default subscriber signal floor read from references/budgets.yaml.
    Falls back to a conservative 50000 if budgets.yaml is unreadable.
    """
    try:
        return int(load_budgets()["research"]["youtube_subscriber_signal_minimum"])
    except Exception:
        return 50_000


REQUIRED = {"kind", "title", "url", "date_accessed", "why_relevant"}


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


def validate_sources(sources: list[dict[str, Any]], min_subs: int) -> list[str]:
    errors: list[str] = []
    for i, source in enumerate(sources, 1):
        missing = sorted(f for f in REQUIRED if not str(source.get(f, "")).strip())
        if missing:
            errors.append(f"Source {i} missing required fields: {', '.join(missing)}")
        if source.get("kind") == "youtube":
            subs = source.get("subscriber_count", 0)
            try:
                subs_int = int(subs)
            except (TypeError, ValueError):
                errors.append(f"Source {i}: subscriber_count is not a number.")
                continue
            if subs_int < min_subs:
                errors.append(
                    f"Source {i} ({source.get('channel', 'unknown channel')}): "
                    f"{subs_int:,} subscribers is below the {min_subs:,} threshold."
                )
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
        f"- Date accessed: {source.get('date_accessed', '')}",
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
    parser.add_argument("--min-youtube-subs", type=int, default=_default_youtube_subscriber_min(),
                        help="Minimum YouTube subscriber count (default: read from "
                             "references/budgets.yaml -> research.youtube_subscriber_signal_minimum, "
                             "currently 50000)")
    parser.add_argument("--allow-under-threshold", action="store_true",
                        help="Write the matrix even if YouTube channels are below threshold (with warnings)")
    args = parser.parse_args()

    source_path = Path(args.sources).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not source_path.exists():
        print(f"ERROR: sources.json not found: {source_path}")
        return 1

    sources = load_sources(source_path)
    errors = validate_sources(sources, args.min_youtube_subs)

    if errors and not args.allow_under_threshold:
        print("Validation failed. Fix these issues in sources.json:")
        for error in errors:
            print(f"  ERROR: {error}")
        print("\nRe-run with --allow-under-threshold to write anyway.")
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

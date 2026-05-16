#!/usr/bin/env python3
"""
extract-tokens.py

Parses a Web Claw `style-guide.md` and emits:
  - tokens.json   — DTCG-flavored token export.
  - tokens.css    — CSS custom properties.

The script looks for the standard markdown tables in style-guide.md:
  - "## Color" → "### Primitives — Neutrals" / "Accent" / "Voice"
  - "## Typography" → "### Scale (...)"
  - "## Spacing"
  - "## Radii"
  - "## Motion seeds"

Usage:
  python extract-tokens.py <style-guide.md> [--out-json tokens.json] [--out-css tokens.css]
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import json
import re
from pathlib import Path


def find_section(md: str, heading: str, stop_at_subheadings: bool = False) -> str:
    """Return everything after `heading` up to the next heading.

    By default stops at the next heading of equal or shallower level (e.g. for
    `## Spacing`, stops at the next `## ...` or `# ...`).

    When `stop_at_subheadings=True`, also stops at the next deeper heading
    (e.g. `### Containers`). Use this when the section's table must not
    be polluted by rows from a nested subsection.
    """
    level = len(re.match(r"^#+", heading.lstrip()).group()) if heading.lstrip().startswith("#") else 2
    pattern = re.compile(rf"^{re.escape(heading.strip())}\s*$", re.MULTILINE)
    m = pattern.search(md)
    if not m:
        return ""
    start = m.end()
    if stop_at_subheadings:
        # Stop at any heading deeper or equal, i.e. ### or ## (no upper bound).
        stop_re = re.compile(r"^#{1,6}\s", re.MULTILINE)
    else:
        stop_re = re.compile(rf"^#{{1,{level}}}\s", re.MULTILINE)
    stop = stop_re.search(md, pos=start + 1)
    return md[start: stop.start()] if stop else md[start:]


def clean_token_name(value: str) -> str:
    """Strip backticks and any parenthetical suffix like "(if needed)" from
    a token name. Token names with embedded parentheticals break downstream
    consumers (CSS variables, JSON keys).
    """
    cleaned = strip_backticks(value)
    cleaned = re.sub(r"\s*\(.*?\)\s*$", "", cleaned).strip()
    return cleaned


def parse_table(block: str) -> list[dict]:
    """
    Parse a simple GitHub-style markdown table into a list of dicts keyed by
    column header.
    """
    lines = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return []
    headers = [c.strip() for c in lines[0].strip("|").split("|")]
    rows: list[dict] = []
    for line in lines[2:]:  # skip the --- separator
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append({h: c for h, c in zip(headers, cells)})
    return rows


def strip_backticks(value: str) -> str:
    return value.strip("`").strip()


def hex_or_none(value: str) -> str | None:
    v = strip_backticks(value)
    return v if re.match(r"^#[0-9A-Fa-f]{3,8}$", v) else None


def extract_colors(md: str) -> dict:
    section = find_section(md, "## Color")
    result: dict = {"primitives": {}, "semantic": {}}

    for ramp in ("Neutrals", "Accent", "Voice"):
        sub = find_section(section, f"### Primitives — {ramp}", stop_at_subheadings=True)
        if not sub:
            continue
        rows = parse_table(sub)
        scale: dict[str, str] = {}
        for r in rows:
            token = clean_token_name(r.get("Token", "")).replace(f"{ramp.lower().rstrip('s')}.", "")
            val = hex_or_none(r.get("Value", "") or r.get("Value (hex)", ""))
            if token and val:
                scale[token] = val
        if scale:
            result["primitives"][ramp.lower().rstrip("s")] = scale

    sub = find_section(section, "### Semantic tokens", stop_at_subheadings=True)
    if sub:
        for r in parse_table(sub):
            token = clean_token_name(r.get("Semantic", ""))
            resolves = strip_backticks(r.get("Resolves to", ""))
            if token and resolves:
                result["semantic"][token] = resolves
    return result


def extract_typography(md: str) -> dict:
    section = find_section(md, "## Typography")
    fams: dict = {}
    sub = find_section(section, "### Families", stop_at_subheadings=True)
    if sub:
        for r in parse_table(sub):
            token = clean_token_name(r.get("Token", "")).replace("font.", "")
            family = strip_backticks(r.get("Family", ""))
            if token and family:
                fams[token] = family

    scale_sub_match = re.search(r"^### Scale[^\n]*$", section, re.MULTILINE)
    scale: dict[str, dict] = {}
    if scale_sub_match:
        rest = section[scale_sub_match.end():]
        stop = re.search(r"^### ", rest, re.MULTILINE)
        block = rest[: stop.start()] if stop else rest
        for r in parse_table(block):
            token = clean_token_name(r.get("Token", "")).replace("text.", "")
            size_value = strip_backticks(r.get("Size", ""))
            if size_value and "clamp(" in size_value and not re.search(r"\d(px|rem|em|vw|vh|%)", size_value):
                print(
                    f"warning: text.{token} size uses clamp() without units: {size_value!r} -- "
                    "this will not be valid CSS. Add px/rem/em to each clamp() argument.",
                    file=sys.stderr,
                )
            scale[token] = {
                "size": size_value,
                "leading": strip_backticks(r.get("Leading", "")),
                "tracking": strip_backticks(r.get("Tracking", "")),
                "weight": strip_backticks(r.get("Weight", "")),
            }

    return {"family": fams, "scale": scale}


def extract_spacing(md: str) -> dict:
    # stop_at_subheadings=True so that any `### Containers` etc. nested under
    # `## Spacing` in the template does not pollute the spacing token map.
    # Belt-and-suspenders: the v2 style-guide template promotes Containers
    # to its own `## Containers` H2, but this defends older templates too.
    section = find_section(md, "## Spacing", stop_at_subheadings=True)
    out: dict[str, str] = {}
    for r in parse_table(section):
        token = clean_token_name(r.get("Token", "")).replace("space.", "")
        value = strip_backticks(r.get("Value", ""))
        # Skip any rows whose token name does not look like a space token
        # (defensive: in case caller is parsing a malformed file).
        if token and value and "." not in token:
            out[token] = value
    return out


def extract_radii(md: str) -> dict:
    section = find_section(md, "## Radii", stop_at_subheadings=True)
    out: dict[str, str] = {}
    for r in parse_table(section):
        token = clean_token_name(r.get("Token", "")).replace("radius.", "")
        value = strip_backticks(r.get("Value", ""))
        if token and value:
            out[token] = value
    return out


def extract_motion(md: str) -> dict:
    section = find_section(md, "## Motion seeds", stop_at_subheadings=True)
    out: dict[str, str] = {}
    for r in parse_table(section):
        token = clean_token_name(r.get("Token", ""))
        value = strip_backticks(r.get("Value", ""))
        if token and value:
            key = token.replace("duration.", "duration-").replace("ease.", "ease-")
            out[key] = value
    return out


def to_css(tokens: dict) -> str:
    lines = [":root {"]
    # Colors
    for ramp, scale in tokens["color"]["primitives"].items():
        for k, v in scale.items():
            lines.append(f"  --color-{ramp}-{k}: {v};")
    for k, v in tokens["color"]["semantic"].items():
        css_k = k.replace(".", "-")
        lines.append(f"  --color-{css_k}: {v};")
    # Type
    for k, v in tokens["typography"]["family"].items():
        lines.append(f"  --font-{k}: {v};")
    # Spacing
    for k, v in tokens["spacing"].items():
        lines.append(f"  --space-{k}: {v};")
    # Radii
    for k, v in tokens["radius"].items():
        lines.append(f"  --radius-{k}: {v};")
    # Motion
    for k, v in tokens["motion"].items():
        lines.append(f"  --{k}: {v};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("style_guide", help="Path to style-guide.md")
    parser.add_argument("--out-json", default=None)
    parser.add_argument("--out-css", default=None)
    args = parser.parse_args(argv[1:])

    sg = Path(args.style_guide).expanduser().resolve()
    if not sg.is_file():
        print(f"error: {sg} does not exist", file=sys.stderr)
        return 2

    md = sg.read_text(encoding="utf-8")
    tokens = {
        "color":      extract_colors(md),
        "typography": extract_typography(md),
        "spacing":    extract_spacing(md),
        "radius":     extract_radii(md),
        "motion":     extract_motion(md),
    }

    print(json.dumps(tokens, indent=2, ensure_ascii=False))

    if args.out_json:
        p = Path(args.out_json).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(tokens, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"wrote: {p}", file=sys.stderr)
    if args.out_css:
        p = Path(args.out_css).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(to_css(tokens), encoding="utf-8")
        print(f"wrote: {p}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

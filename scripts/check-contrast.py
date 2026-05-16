#!/usr/bin/env python3
"""
check-contrast.py

Validate WCAG contrast ratios for every declared text/surface pair in a
project's style-guide.md or design tokens. Implements the WCAG 2.0
relative-luminance contrast formula in pure stdlib (no external deps).

Inputs (one of):
  --tokens <tokens.json>      DTCG-flavored JSON emitted by extract-tokens.py
  --style-guide <path>        style-guide.md (we re-run extract-tokens internally)
  --pair fg bg                ad-hoc one-shot check on two hex colors

Outputs: a JSON report. Exit 0 if every required pair passes AA; exit 3 if
any pair fails. Thresholds come from references/budgets.yaml -> accessibility.*.

WCAG AA contrast requirements applied:
  - Normal text: >= 4.5:1
  - Large text (>= 18pt or 14pt bold): >= 3.0:1
  - Non-text UI components (icons, borders): >= 3.0:1

Usage:
  python check-contrast.py --tokens <project>/design/tokens.json
  python check-contrast.py --style-guide <project>/blueprint/style-guide.md
  python check-contrast.py --pair "#FF0000" "#FFFFFF"
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
import subprocess
from pathlib import Path
from typing import Any

from _budgets import load_budgets


HEX_RE = re.compile(r"^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})$")


def parse_hex(value: str) -> tuple[int, int, int] | None:
    """Return (r, g, b) integers 0..255 or None if value is not a hex color."""
    if not isinstance(value, str):
        return None
    m = HEX_RE.match(value.strip())
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c + c for c in h)
    if len(h) == 8:  # ignore alpha
        h = h[:6]
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """WCAG 2.0 relative luminance. Components are linearised per spec."""
    def channel(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def grade(ratio: float, normal_min: float, large_min: float) -> dict:
    return {
        "ratio": round(ratio, 2),
        "passes_aa_normal": ratio >= normal_min,
        "passes_aa_large":  ratio >= large_min,
        "passes_aaa_normal": ratio >= 7.0,
        "passes_aaa_large":  ratio >= 4.5,
    }


def resolve_semantic(value: str, primitives: dict) -> str | None:
    """Resolve `{neutral.50}` references against primitive ramps."""
    m = re.match(r"\{([a-z]+)\.([0-9A-Za-z\-]+)\}", value.strip())
    if not m:
        return None
    ramp_name = m.group(1).rstrip("s")
    scale_key = m.group(2)
    ramp = primitives.get(ramp_name, {})
    return ramp.get(scale_key)


def resolve_color(value: str, primitives: dict) -> str | None:
    """Return a hex string for either a literal hex or a {ramp.key} ref."""
    if not value:
        return None
    if value.strip().startswith("#"):
        return value.strip()
    return resolve_semantic(value, primitives)


# Pairs the agent must check on every style-guide. Tokens are dotted names that
# correspond to either primitive entries (e.g. `neutral.50`) or semantic
# entries (e.g. `text.primary`). The pairs reflect the contrast-validation
# block already required by assets/templates/style-guide-template.md.
REQUIRED_PAIRS: list[tuple[str, str, str]] = [
    # (foreground_token, background_token, label)
    ("text.primary",   "surface.default",  "Body text on surface"),
    ("text.secondary", "surface.default",  "Secondary text on surface"),
    ("text.muted",     "surface.default",  "Muted text on surface (large-only)"),
    ("text.on-accent", "accent.action",    "Inverse text on accent CTA"),
    ("accent.action-hover", "surface.default", "Accent hover state on surface"),
]


def load_tokens_from_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_tokens_from_style_guide(style_guide: Path) -> dict[str, Any]:
    """Run extract-tokens.py and parse its JSON output."""
    extract = Path(__file__).resolve().parent / "extract-tokens.py"
    result = subprocess.run(
        [sys.executable, str(extract), str(style_guide)],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"extract-tokens.py failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def resolve_token(token_name: str, tokens: dict) -> str | None:
    """Given a token name (e.g. 'text.primary' or 'neutral.50'), return a hex."""
    color = tokens.get("color", {})
    primitives = color.get("primitives", {})
    semantic = color.get("semantic", {})

    if "." in token_name:
        ramp_name, scale_key = token_name.split(".", 1)
        # Try semantic resolution first.
        if token_name in semantic:
            return resolve_color(semantic[token_name], primitives)
        # Try primitive lookup.
        ramp = primitives.get(ramp_name) or primitives.get(ramp_name.rstrip("s"))
        if ramp:
            value = ramp.get(scale_key)
            return value if value and value.startswith("#") else None
    return None


def check_pairs(tokens: dict, budgets: dict) -> dict:
    aa_normal = float(budgets["accessibility"]["contrast_aa_min_normal"])
    aa_large = float(budgets["accessibility"]["contrast_aa_min_large"])

    pairs: list[dict] = []
    for fg_token, bg_token, label in REQUIRED_PAIRS:
        fg_hex = resolve_token(fg_token, tokens)
        bg_hex = resolve_token(bg_token, tokens)
        entry: dict = {"label": label, "fg": fg_token, "bg": bg_token,
                       "fg_hex": fg_hex, "bg_hex": bg_hex}
        fg_rgb = parse_hex(fg_hex) if fg_hex else None
        bg_rgb = parse_hex(bg_hex) if bg_hex else None
        if not (fg_rgb and bg_rgb):
            entry["status"] = "unresolved"
            entry["pass"] = None
            pairs.append(entry)
            continue
        ratio = contrast_ratio(fg_rgb, bg_rgb)
        entry.update(grade(ratio, aa_normal, aa_large))
        # "muted" pair is allowed to fail normal-text AA; only large-text is required.
        if "muted" in fg_token:
            entry["pass"] = entry["passes_aa_large"]
        else:
            entry["pass"] = entry["passes_aa_normal"]
        pairs.append(entry)

    return {
        "aa_min_normal": aa_normal,
        "aa_min_large":  aa_large,
        "pairs": pairs,
        "pass": all(p.get("pass") is True for p in pairs),
        "unresolved": [p for p in pairs if p.get("status") == "unresolved"],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tokens", default=None, help="Path to tokens.json (from extract-tokens.py).")
    parser.add_argument("--style-guide", default=None, help="Path to a Web Claw style-guide.md.")
    parser.add_argument("--pair", nargs=2, metavar=("FG_HEX", "BG_HEX"), default=None,
                        help="Ad-hoc one-shot pair check (e.g. --pair '#fff' '#000').")
    args = parser.parse_args(argv[1:])

    budgets = load_budgets()

    if args.pair:
        fg = parse_hex(args.pair[0])
        bg = parse_hex(args.pair[1])
        if not fg or not bg:
            print("error: both --pair arguments must be hex colors (e.g. #RRGGBB).", file=sys.stderr)
            return 2
        ratio = contrast_ratio(fg, bg)
        aa_normal = float(budgets["accessibility"]["contrast_aa_min_normal"])
        aa_large = float(budgets["accessibility"]["contrast_aa_min_large"])
        out = {
            "fg_hex": args.pair[0], "bg_hex": args.pair[1],
            **grade(ratio, aa_normal, aa_large),
        }
        print(json.dumps(out, indent=2))
        return 0 if ratio >= aa_normal else 3

    if not (args.tokens or args.style_guide):
        print("error: provide --tokens or --style-guide (or --pair for one-shot).", file=sys.stderr)
        return 2

    if args.tokens:
        tokens = load_tokens_from_json(Path(args.tokens).expanduser().resolve())
    else:
        tokens = load_tokens_from_style_guide(Path(args.style_guide).expanduser().resolve())

    report = check_pairs(tokens, budgets)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["pass"] else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))

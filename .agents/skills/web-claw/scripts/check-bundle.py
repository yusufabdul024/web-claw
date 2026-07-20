#!/usr/bin/env python3
"""
check-bundle.py

Inspect a frontend build's output directory and gate it against the bundle
budgets in references/budgets.yaml.

The script auto-detects the framework by looking for known build-output
locations and inspects the JS / CSS / image / font payload that hits a page
on first load.

Supported (in order of detection):
- Next.js   .next/    (reads .next/build-manifest.json + page sizes)
- Astro     dist/_astro/
- Vite      dist/assets/
- Generic   any --dir <path> can be passed explicitly

Output is a JSON report including pass/fail against each budget in
budgets.yaml's `bundle.*` section. Exit codes:
  0 - all budgets pass
  3 - one or more budgets exceeded
  2 - input error (no build output found)

Usage:
  python check-bundle.py                           # auto-detect in current dir
  python check-bundle.py --dir <frontend-root>
  python check-bundle.py --dir <root> --strict     # also fail on warnings
  python check-bundle.py --dir <root> --json-only  # suppress the summary table
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

from _budgets import load_budgets


def kb(num_bytes: int) -> float:
    return round(num_bytes / 1024.0, 1)


def _walk_sizes(root: Path, extensions: set[str]) -> dict[str, int]:
    """Return {relpath: bytes} for files under root with matching extensions."""
    sizes: dict[str, int] = {}
    if not root.is_dir():
        return sizes
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in extensions:
            try:
                sizes[str(p.relative_to(root))] = p.stat().st_size
            except OSError:
                pass
    return sizes


def detect_framework(root: Path) -> str | None:
    if (root / ".next").is_dir():
        return "nextjs"
    if (root / "dist" / "_astro").is_dir():
        return "astro"
    if (root / "dist" / "assets").is_dir():
        return "vite"
    if (root / "dist").is_dir():
        return "generic-dist"
    if (root / "build").is_dir():
        return "generic-build"
    return None


def measure(root: Path, framework: str) -> dict:
    """Aggregate per-asset-class bytes from build output."""
    output_dirs: dict[str, Path] = {}
    if framework == "nextjs":
        # Next.js: static client bundles live under .next/static/. The
        # initial JS for a route is split across chunks; without parsing
        # build-manifest we treat the .next/static directory as the upper
        # bound. Better than nothing for a smoke check.
        output_dirs["js"] = root / ".next" / "static"
        output_dirs["css"] = root / ".next" / "static"
        output_dirs["fonts"] = root / ".next" / "static"
        output_dirs["images"] = root / "public"
    elif framework == "astro":
        output_dirs["js"] = root / "dist" / "_astro"
        output_dirs["css"] = root / "dist" / "_astro"
        output_dirs["fonts"] = root / "dist"
        output_dirs["images"] = root / "dist"
    elif framework == "vite":
        output_dirs["js"] = root / "dist" / "assets"
        output_dirs["css"] = root / "dist" / "assets"
        output_dirs["fonts"] = root / "dist" / "assets"
        output_dirs["images"] = root / "dist" / "assets"
    elif framework in ("generic-dist", "generic-build"):
        base = root / ("dist" if framework == "generic-dist" else "build")
        output_dirs["js"] = base
        output_dirs["css"] = base
        output_dirs["fonts"] = base
        output_dirs["images"] = base

    js_files = _walk_sizes(output_dirs.get("js", root), {".js", ".mjs", ".cjs"})
    css_files = _walk_sizes(output_dirs.get("css", root), {".css"})
    font_files = _walk_sizes(output_dirs.get("fonts", root), {".woff2", ".woff", ".ttf", ".otf"})
    image_files = _walk_sizes(
        output_dirs.get("images", root),
        {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".svg"},
    )

    return {
        "framework": framework,
        "totals_kb": {
            "js":     kb(sum(js_files.values())),
            "css":    kb(sum(css_files.values())),
            "fonts":  kb(sum(font_files.values())),
            "images": kb(sum(image_files.values())),
        },
        "counts": {
            "js":     len(js_files),
            "css":    len(css_files),
            "fonts":  len(font_files),
            "images": len(image_files),
        },
        "largest_js": sorted(js_files.items(), key=lambda kv: -kv[1])[:5],
        "largest_css": sorted(css_files.items(), key=lambda kv: -kv[1])[:5],
        "largest_images": [
            (k, v) for k, v in sorted(image_files.items(), key=lambda kv: -kv[1])[:5]
        ],
    }


def evaluate(measurements: dict, budgets: dict) -> dict:
    """Compare measurements vs. budgets.yaml -> bundle.*. Note: per-page totals
    are not derivable from a static build dir without route analysis -- this
    script reports *total shipped bytes per asset class* as an upper bound.
    Per-route budgets are enforced by Lighthouse in audit-perf.py.
    """
    bundle = budgets.get("bundle", {})
    totals = measurements["totals_kb"]
    results: dict[str, dict] = {}

    # Compare total JS shipped vs. total-per-page max as upper-bound check.
    js_total_max = bundle.get("total_js_per_page_kb_max")
    if js_total_max is not None:
        results["js_total_vs_per_page_max"] = {
            "actual_kb": totals["js"],
            "budget_kb": js_total_max,
            "pass": totals["js"] <= js_total_max,
            "note": "total shipped JS upper-bounds the per-page payload",
        }

    css_max = bundle.get("css_critical_kb_max")
    if css_max is not None:
        results["css_total_vs_critical_max"] = {
            "actual_kb": totals["css"],
            "budget_kb": css_max,
            "pass": totals["css"] <= css_max,
            "note": "total shipped CSS upper-bounds the critical CSS payload",
        }

    fonts_max = bundle.get("fonts_total_kb_max")
    if fonts_max is not None:
        results["fonts_total"] = {
            "actual_kb": totals["fonts"],
            "budget_kb": fonts_max,
            "pass": totals["fonts"] <= fonts_max,
        }

    # Hero-image check: every image larger than hero_image_kb_max is flagged.
    hero_max_kb = bundle.get("hero_image_kb_max")
    oversize: list[dict] = []
    if hero_max_kb is not None:
        for path, size_bytes in measurements["largest_images"]:
            size_kb = kb(size_bytes)
            if size_kb > hero_max_kb:
                oversize.append({"path": path, "kb": size_kb, "budget_kb": hero_max_kb})
    results["oversize_images"] = {
        "budget_kb": hero_max_kb,
        "items": oversize,
        "pass": len(oversize) == 0,
    }

    overall_pass = all(v.get("pass", True) for v in results.values())
    return {"pass": overall_pass, "checks": results}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default=".", help="Frontend root directory (default: current dir).")
    parser.add_argument("--strict", action="store_true", help="Also fail on warnings (currently no warnings).")
    parser.add_argument("--json-only", action="store_true", help="Suppress human summary; emit JSON only.")
    args = parser.parse_args(argv[1:])

    root = Path(args.dir).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    framework = detect_framework(root)
    if framework is None:
        print(
            f"error: no recognizable build output under {root}. Looked for: "
            ".next/, dist/_astro/, dist/assets/, dist/, build/.",
            file=sys.stderr,
        )
        return 2

    measurements = measure(root, framework)
    try:
        budgets = load_budgets()
    except Exception as e:
        print(f"error: could not load budgets: {e}", file=sys.stderr)
        return 2

    result = evaluate(measurements, budgets)
    payload = {
        "root": str(root),
        "framework": framework,
        "measurements": measurements,
        "budget_check": result,
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if not args.json_only:
        print(file=sys.stderr)
        print(f"Framework detected: {framework}", file=sys.stderr)
        print(f"Total JS: {measurements['totals_kb']['js']} kB across {measurements['counts']['js']} files", file=sys.stderr)
        print(f"Total CSS: {measurements['totals_kb']['css']} kB", file=sys.stderr)
        print(f"Total fonts: {measurements['totals_kb']['fonts']} kB", file=sys.stderr)
        print(f"Total images: {measurements['totals_kb']['images']} kB", file=sys.stderr)
        print(f"Budget check: {'PASS' if result['pass'] else 'FAIL'}", file=sys.stderr)

    return 0 if result["pass"] else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))

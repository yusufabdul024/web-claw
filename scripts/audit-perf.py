#!/usr/bin/env python3
"""
audit-perf.py

Runs Lighthouse against a URL three times via `npx lighthouse`, then reports
the median Performance, Accessibility, Best Practices, and SEO scores.

Requires Node.js (so `npx` is available). No Python dependencies beyond stdlib.

Usage:
  python audit-perf.py <url> [--device mobile|desktop] [--out reports/] [--timeout 180]
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import json
import statistics
import subprocess
import tempfile
import shutil
from pathlib import Path

from _budgets import load_budgets


def resolve_npx() -> str | None:
    """Find npx in PATH; returns the resolved absolute path or None.

    On Windows, npx is usually `npx.cmd` -- shutil.which finds it.
    On macOS/Linux, it's `npx` (Node-shipped shim).
    """
    return shutil.which("npx") or shutil.which("npx.cmd")


def run_lighthouse(npx: str, url: str, device: str, output_dir: Path, idx: int, timeout: int) -> dict | None:
    """Run a single Lighthouse pass and return the parsed JSON, or None on error."""
    report_path = output_dir / f"run-{idx}.json"
    cmd = [
        npx, "--yes", "lighthouse", url,
        "--quiet",
        "--output=json",
        f"--output-path={report_path}",
        "--chrome-flags=--headless=new --no-sandbox",
        "--only-categories=performance,accessibility,best-practices,seo",
    ]
    if device == "desktop":
        cmd.insert(5, "--preset=desktop")

    print(f"  run {idx + 1}/3 ...", file=sys.stderr)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"    lighthouse timeout after {timeout}s on {url}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"    npx invocation failed: {npx} not callable as a subprocess", file=sys.stderr)
        return None

    if result.returncode != 0:
        tail = result.stderr.strip().splitlines()[-1] if result.stderr else "(no stderr)"
        print(f"    lighthouse exit {result.returncode}: {tail}", file=sys.stderr)
        return None

    try:
        return json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"    failed to read report at {report_path}: {e}", file=sys.stderr)
        return None


def extract_scores(report: dict) -> dict[str, float]:
    cats = report.get("categories", {})
    def s(key: str) -> float:
        score = cats.get(key, {}).get("score")
        return round(score * 100, 1) if isinstance(score, (int, float)) else float("nan")
    return {
        "performance":     s("performance"),
        "accessibility":   s("accessibility"),
        "best-practices":  s("best-practices"),
        "seo":             s("seo"),
    }


def extract_metrics(report: dict) -> dict[str, float]:
    audits = report.get("audits", {})
    def ms(key: str) -> float | None:
        v = audits.get(key, {}).get("numericValue")
        return v if isinstance(v, (int, float)) else None
    return {
        "LCP_ms":  ms("largest-contentful-paint"),
        "FCP_ms":  ms("first-contentful-paint"),
        "TBT_ms":  ms("total-blocking-time"),
        "CLS":     ms("cumulative-layout-shift"),
        "TTFB_ms": ms("server-response-time"),
        "SI_ms":   ms("speed-index"),
    }


def median_or_nan(values: list[float | None]) -> float:
    clean = [v for v in values if isinstance(v, (int, float)) and v == v]  # filter NaN/None
    return statistics.median(clean) if clean else float("nan")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url")
    parser.add_argument("--device", default="mobile", choices=["mobile", "desktop"])
    parser.add_argument("--out", default=None, help="Directory to keep all three reports (else temp & discard)")
    parser.add_argument("--timeout", type=int, default=180, help="Per-run timeout in seconds (default 180).")
    args = parser.parse_args(argv[1:])

    npx = resolve_npx()
    if npx is None:
        print(
            "error: npx not found on PATH.\n"
            "       Install Node.js (which ships with npm/npx): https://nodejs.org/\n"
            "       After install, restart the shell and re-run this script.",
            file=sys.stderr,
        )
        return 2

    if args.out:
        out_dir = Path(args.out).expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = Path(tempfile.mkdtemp(prefix="webclaw-lighthouse-"))

    print(f"Lighthouse ({args.device}) x3 against {args.url}", file=sys.stderr)
    print(f"Using npx: {npx}", file=sys.stderr)
    reports = []
    for i in range(3):
        r = run_lighthouse(npx, args.url, args.device, out_dir, i, args.timeout)
        if r is not None:
            reports.append(r)

    if not reports:
        print("error: all three runs failed. Common causes:", file=sys.stderr)
        print("  - Lighthouse cannot reach the URL (deploy preview not live, auth gate, CORS).", file=sys.stderr)
        print("  - Chrome failed to launch (CI/sandbox without --no-sandbox).", file=sys.stderr)
        print("  - First-time npx install timed out -- try `npx --yes lighthouse --version` once manually.", file=sys.stderr)
        return 1

    score_sets = [extract_scores(r) for r in reports]
    metric_sets = [extract_metrics(r) for r in reports]

    summary = {
        "url":     args.url,
        "device":  args.device,
        "runs":    len(reports),
        "scores":  {k: median_or_nan([s[k] for s in score_sets]) for k in score_sets[0]},
        "metrics": {k: median_or_nan([m[k] for m in metric_sets]) for k in metric_sets[0]},
    }

    # Pass/fail check against canonical budgets in references/budgets.yaml.
    exit_code = 0
    try:
        budgets = load_budgets()
        lh = budgets["lighthouse"][args.device]
        cwv = budgets["core_web_vitals"]
        pass_fail: dict[str, dict] = {}
        for cat_key, budget_key in (
            ("performance",    "performance"),
            ("accessibility",  "accessibility"),
            ("best-practices", "best_practices"),
            ("seo",            "seo"),
        ):
            floor = lh.get(budget_key)
            actual = summary["scores"].get(cat_key)
            if floor is None or actual != actual:  # NaN check
                pass_fail[cat_key] = {"floor": floor, "actual": actual, "pass": None}
                continue
            ok = actual >= floor
            pass_fail[cat_key] = {"floor": floor, "actual": actual, "pass": ok}
            if not ok:
                exit_code = 3
        # CWV checks
        lcp = summary["metrics"].get("LCP_ms")
        cls = summary["metrics"].get("CLS")
        cwv_pass: dict[str, dict] = {}
        if lcp == lcp and lcp is not None:
            lcp_max_ms = float(cwv["lcp_seconds_max"]) * 1000.0
            cwv_pass["LCP"] = {"max_ms": lcp_max_ms, "actual_ms": lcp, "pass": lcp <= lcp_max_ms}
            if lcp > lcp_max_ms:
                exit_code = 3
        if cls == cls and cls is not None:
            cls_max = float(cwv["cls_max"])
            cwv_pass["CLS"] = {"max": cls_max, "actual": cls, "pass": cls <= cls_max}
            if cls > cls_max:
                exit_code = 3
        summary["budget_check"] = {
            "device": args.device,
            "source": "references/budgets.yaml",
            "lighthouse": pass_fail,
            "core_web_vitals": cwv_pass,
        }
    except Exception as e:
        summary["budget_check"] = {"error": f"could not load budgets: {e}"}

    print(json.dumps(summary, indent=2))
    print(f"\nReports saved to: {out_dir}", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))

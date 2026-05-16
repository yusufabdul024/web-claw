#!/usr/bin/env python3
"""
check-a11y.py

Runs pa11y (which wraps axe-core + HTML CodeSniffer) against a URL and
returns the violations in a Web-Claw-friendly format.

Requires Node.js (so `npx` is available). No Python dependencies beyond stdlib.

Usage:
  python check-a11y.py <url> [--standard WCAG2AA|WCAG22AA] [--out report.json] [--timeout 60]
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from _budgets import load_budgets


def resolve_npx() -> str | None:
    """Find npx in PATH; returns the resolved absolute path or None."""
    return shutil.which("npx") or shutil.which("npx.cmd")


def run_pa11y(npx: str, url: str, standard: str, timeout: int) -> tuple[int, list[dict], str]:
    """Run pa11y; returns (returncode, parsed_issues_or_empty, stderr_text)."""
    cmd = [
        npx, "--yes", "pa11y",
        "--reporter", "json",
        "--standard", standard,
        "--timeout", str(timeout * 1000),
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    except subprocess.TimeoutExpired:
        return 124, [], f"pa11y subprocess exceeded {timeout + 30}s wall clock."
    except FileNotFoundError:
        return 127, [], f"{npx} could not be invoked as a subprocess."

    issues: list[dict] = []
    if result.stdout.strip():
        try:
            issues = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass
    return result.returncode, issues, result.stderr


def summarize(issues: list[dict]) -> dict:
    by_type: dict[str, int] = {}
    for i in issues:
        t = i.get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1
    return {
        "total": len(issues),
        "by_type": by_type,
        "samples": issues[:5],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url")
    parser.add_argument("--standard", default="WCAG2AA", choices=["WCAG2A", "WCAG2AA", "WCAG2AAA", "WCAG22AA"])
    parser.add_argument("--out", default=None, help="Optional path to write the JSON report.")
    parser.add_argument("--timeout", type=int, default=60, help="Per-page timeout in seconds (default 60).")
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

    print(f"pa11y --standard {args.standard} {args.url}", file=sys.stderr)
    print(f"Using npx: {npx}", file=sys.stderr)
    rc, issues, stderr = run_pa11y(npx, args.url, args.standard, args.timeout)

    # pa11y exit codes: 0 = no issues, 2 = issues found, 1 = error.
    if rc not in (0, 2):
        print(f"pa11y error (rc={rc}):", file=sys.stderr)
        if stderr.strip():
            print(stderr.strip(), file=sys.stderr)
        print("Common causes:", file=sys.stderr)
        print("  - URL not reachable from this machine.", file=sys.stderr)
        print("  - Headless Chrome blocked (CI without --no-sandbox).", file=sys.stderr)
        print("  - First-time npx install timed out -- try `npx --yes pa11y --help` once manually.", file=sys.stderr)
        return rc or 1

    summary = summarize(issues)
    payload = {
        "url":       args.url,
        "standard":  args.standard,
        "summary":   summary,
        "issues":    issues,
    }

    # Budget check from references/budgets.yaml. pa11y exposes issue types
    # ('error'/'warning'/'notice'); axe-core's severity model maps roughly:
    # pa11y "error" ~= axe "serious"/"critical". For Web Claw's gate we treat
    # any pa11y "error" as blocking when budgets.yaml sets axe critical/serious
    # to 0.
    exit_code = 0
    try:
        budgets = load_budgets()
        a11y = budgets["accessibility"]
        critical_max = int(a11y["axe_violations_critical_max"])
        serious_max = int(a11y["axe_violations_serious_max"])
        # Sum of critical+serious budget tolerance; pa11y errors are gated by this.
        error_count = summary["by_type"].get("error", 0)
        budget_violation = error_count > (critical_max + serious_max)
        payload["budget_check"] = {
            "source": "references/budgets.yaml",
            "wcag_level": a11y.get("wcag_level"),
            "critical_max": critical_max,
            "serious_max": serious_max,
            "pa11y_errors": error_count,
            "pass": not budget_violation,
        }
        if budget_violation:
            exit_code = 3
    except Exception as e:
        payload["budget_check"] = {"error": f"could not load budgets: {e}"}

    output = json.dumps(payload, indent=2, ensure_ascii=False)
    print(output)

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"\nWrote: {out_path}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))

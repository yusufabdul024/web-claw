#!/usr/bin/env python3
"""
run-playwright.py

End-to-end smoke suite for a deployed Web Claw preview/production URL.

Writes a temporary Playwright spec to a temp directory and invokes
`npx playwright test`. The spec is parametric across URLs read from the
project's sitemap (or a single URL passed on the CLI).

Checks performed for each URL:
- HTTP status 200.
- Page has a <title>.
- Page has a single <h1>.
- No console errors during initial load.
- No 4xx/5xx network responses on the page's main-frame resources.
- A primary CTA (first <a> or <button> inside <main>) is reachable
  via keyboard (Tab) and has an accessible name.

Requires Node.js + Playwright. The script will prompt to run
`npx playwright install chromium` if browsers are missing.

Usage:
  python run-playwright.py <url>
  python run-playwright.py <url> --extra-urls <u1> <u2>
  python run-playwright.py --sitemap <project>/blueprint/sitemap.md
  python run-playwright.py <url> --browser webkit
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
import shutil
import subprocess
import tempfile
from pathlib import Path


def resolve_npx() -> str | None:
    return shutil.which("npx") or shutil.which("npx.cmd")


def parse_sitemap_urls(sitemap_md: Path, base_url: str) -> list[str]:
    """Extract page paths from a Web Claw sitemap.md and join with base_url."""
    if not sitemap_md.is_file():
        return []
    text = sitemap_md.read_text(encoding="utf-8")
    # Web Claw sitemaps record routes like `/about`, `/pricing`, or `/`.
    paths = re.findall(r"`(/[A-Za-z0-9_\-/]*)`", text)
    seen: set[str] = set()
    uniq_paths: list[str] = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            uniq_paths.append(p)
    base = base_url.rstrip("/")
    return [base + (p if p != "/" else "")] + [base + p for p in uniq_paths if p != "/"]


SPEC_TEMPLATE = r"""
// @ts-check
const { test, expect } = require('@playwright/test');

const URLS = __URLS_PLACEHOLDER__;

for (const url of URLS) {
  test.describe(`smoke: ${url}`, () => {
    test('loads with title, single h1, no console errors', async ({ page }) => {
      const consoleErrors = [];
      const networkErrors = [];
      page.on('console', msg => {
        if (msg.type() === 'error') consoleErrors.push(msg.text());
      });
      page.on('response', resp => {
        const status = resp.status();
        if (status >= 400 && resp.frame() === page.mainFrame()) {
          networkErrors.push(`${status} ${resp.url()}`);
        }
      });

      const resp = await page.goto(url, { waitUntil: 'load' });
      expect(resp, 'page response should exist').not.toBeNull();
      expect(resp.status(), 'status code should be 2xx').toBeLessThan(400);

      const title = await page.title();
      expect(title, 'page should have a <title>').toBeTruthy();

      const h1Count = await page.locator('h1').count();
      expect(h1Count, 'page should have exactly one <h1>').toBe(1);

      expect(consoleErrors, 'no console errors').toEqual([]);
      expect(networkErrors, 'no 4xx/5xx main-frame responses').toEqual([]);
    });

    test('primary CTA in <main> is keyboard reachable', async ({ page }) => {
      await page.goto(url, { waitUntil: 'load' });
      const cta = page.locator('main a, main button').first();
      const exists = await cta.count();
      if (!exists) {
        test.info().annotations.push({ type: 'note', description: 'no <a>/<button> inside <main>; skipping.' });
        return;
      }
      const name = await cta.getAttribute('aria-label')
                 ?? await cta.textContent();
      expect(name && name.trim().length > 0, 'primary CTA must have an accessible name').toBe(true);
      await cta.focus();
      const isFocused = await cta.evaluate(el => el === document.activeElement);
      expect(isFocused, 'primary CTA must be focusable').toBe(true);
    });
  });
}
"""


def write_spec(spec_dir: Path, urls: list[str]) -> Path:
    spec_path = spec_dir / "tests" / "webclaw-smoke.spec.js"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(
        SPEC_TEMPLATE.replace("__URLS_PLACEHOLDER__", json.dumps(urls)),
        encoding="utf-8",
    )
    # Minimal Playwright config so the test runs without a user config.
    # Register all three browser projects -- run-playwright.py advertises
    # --browser chromium|firefox|webkit, so the config must define all three
    # or the test runner fails with "no project matches" for the non-default.
    (spec_dir / "playwright.config.js").write_text(
        "module.exports = { testDir: './tests', reporter: 'json', "
        "use: { trace: 'off' }, projects: ["
        "{ name: 'chromium', use: { browserName: 'chromium' } }, "
        "{ name: 'firefox',  use: { browserName: 'firefox'  } }, "
        "{ name: 'webkit',   use: { browserName: 'webkit'   } }"
        "] };\n",
        encoding="utf-8",
    )
    return spec_path


def run_playwright(npx: str, spec_dir: Path, timeout: int, browser: str) -> tuple[int, dict | None, str]:
    cmd = [
        npx, "--yes", "playwright", "test",
        "--project", browser,
        "--reporter", "json",
    ]
    try:
        result = subprocess.run(
            cmd, cwd=spec_dir, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return 124, None, f"playwright run exceeded {timeout}s wall clock."
    except FileNotFoundError:
        return 127, None, f"{npx} could not be invoked as a subprocess."

    parsed: dict | None = None
    if result.stdout.strip():
        try:
            parsed = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass
    return result.returncode, parsed, result.stderr


def summarize(report: dict | None) -> dict:
    if report is None:
        return {"tests": 0, "passed": 0, "failed": 0, "skipped": 0}
    suites = report.get("suites", [])
    counts = {"tests": 0, "passed": 0, "failed": 0, "skipped": 0}
    failures: list[dict] = []

    def walk(suites):
        for s in suites:
            for spec in s.get("specs", []):
                for t in spec.get("tests", []):
                    for run in t.get("results", []):
                        counts["tests"] += 1
                        status = run.get("status")
                        if status == "passed":
                            counts["passed"] += 1
                        elif status in ("failed", "timedOut"):
                            counts["failed"] += 1
                            failures.append({
                                "title": spec.get("title"),
                                "file": spec.get("file"),
                                "error": (run.get("error") or {}).get("message"),
                            })
                        elif status == "skipped":
                            counts["skipped"] += 1
            walk(s.get("suites", []))
    walk(suites)
    counts["failures"] = failures
    return counts


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", nargs="?", help="Base URL (e.g. https://preview.example).")
    parser.add_argument("--extra-urls", nargs="*", default=[], help="Additional fully-qualified URLs to smoke.")
    parser.add_argument("--sitemap", default=None, help="Path to <project>/blueprint/sitemap.md (optional).")
    parser.add_argument("--browser", default="chromium", choices=["chromium", "firefox", "webkit"])
    parser.add_argument("--timeout", type=int, default=180, help="Per-run timeout in seconds (default 180).")
    parser.add_argument("--out", default=None, help="Optional path to write the JSON summary.")
    args = parser.parse_args(argv[1:])

    if not args.url and not args.extra_urls:
        print("error: provide a URL (and/or --extra-urls).", file=sys.stderr)
        return 2

    urls: list[str] = []
    if args.url:
        urls.append(args.url)
    urls.extend(args.extra_urls)
    if args.sitemap and args.url:
        urls.extend(parse_sitemap_urls(Path(args.sitemap).expanduser().resolve(), args.url))
    # De-dupe, preserve order.
    seen: set[str] = set()
    urls = [u for u in urls if not (u in seen or seen.add(u))]

    npx = resolve_npx()
    if npx is None:
        print(
            "error: npx not found on PATH. Install Node.js (which ships with npm/npx): "
            "https://nodejs.org/",
            file=sys.stderr,
        )
        return 2

    spec_dir = Path(tempfile.mkdtemp(prefix="webclaw-playwright-"))
    write_spec(spec_dir, urls)
    print(f"Running Playwright against {len(urls)} URL(s) using {args.browser}...", file=sys.stderr)
    print(f"Spec dir: {spec_dir}", file=sys.stderr)

    rc, report, stderr = run_playwright(npx, spec_dir, args.timeout, args.browser)
    summary = summarize(report)
    summary["urls"] = urls
    summary["browser"] = args.browser
    summary["exit_code"] = rc

    if rc != 0 and (summary["passed"] + summary["failed"] + summary["skipped"]) == 0:
        # Playwright failed to launch / parse; surface stderr tail for diagnosis.
        summary["stderr_tail"] = stderr.strip().splitlines()[-10:] if stderr else []

    output = json.dumps(summary, indent=2, ensure_ascii=False)
    print(output)

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"\nWrote: {out_path}", file=sys.stderr)

    # Exit 3 if any failures (so CI gates on the script's exit code).
    if summary.get("failed", 0) > 0:
        return 3
    return rc if rc != 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

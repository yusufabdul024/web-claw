#!/usr/bin/env python3
"""
check-reduced-motion.py

Verify a deployed Web Claw site honors `prefers-reduced-motion: reduce`.

The script uses Playwright (via npx) to load a URL twice -- once with
the default media preference, once with reduced motion forced -- and
captures:
- screenshots of both runs (for visual diff during review),
- console messages,
- computed CSS `transition` and `animation` durations on a sample of
  elements,
- any element that becomes invisible (display:none / visibility:hidden /
  opacity:0) ONLY in the reduced-motion render -- that's a regression.

A pass requires:
- No content disappears under reduced motion (no permanent hidden states).
- No animation/transition duration > 100ms on more than 5% of sampled
  elements in the reduced-motion run.

Requires Node.js + Playwright (`npx playwright install chromium` if needed).

Usage:
  python check-reduced-motion.py <url>
  python check-reduced-motion.py <url> --out reports/
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
import tempfile
from pathlib import Path


def resolve_npx() -> str | None:
    return shutil.which("npx") or shutil.which("npx.cmd")


SPEC_TEMPLATE = r"""
// @ts-check
const { test, expect, chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const URL = __URL_PLACEHOLDER__;
const OUT_DIR = __OUT_DIR_PLACEHOLDER__;

async function captureRun(reduced) {
  const browser = await chromium.launch();
  const context = await browser.newContext({ reducedMotion: reduced ? 'reduce' : 'no-preference' });
  const page = await context.newPage();
  const consoleMessages = [];
  page.on('console', m => consoleMessages.push({ type: m.type(), text: m.text() }));
  await page.goto(URL, { waitUntil: 'load' });
  await page.waitForTimeout(1500);  // settle entrance animations
  const screenshot = path.join(OUT_DIR, reduced ? 'reduced.png' : 'default.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  // Sample first 80 visible elements + their effective animation/transition timing.
  const samples = await page.evaluate(() => {
    const els = Array.from(document.querySelectorAll('*')).slice(0, 80);
    return els.map(el => {
      const s = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return {
        tag: el.tagName.toLowerCase(),
        id: el.id || null,
        cls: typeof el.className === 'string' ? el.className.slice(0, 80) : null,
        transition_duration: s.transitionDuration,
        animation_duration: s.animationDuration,
        opacity: s.opacity,
        display: s.display,
        visibility: s.visibility,
        visible: rect.width > 0 && rect.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0',
      };
    });
  });

  await browser.close();
  return { reduced, screenshot, consoleMessages, samples };
}

test('reduced-motion compliance', async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const defaultRun = await captureRun(false);
  const reducedRun = await captureRun(true);
  fs.writeFileSync(
    path.join(OUT_DIR, 'report.json'),
    JSON.stringify({ default: defaultRun, reduced: reducedRun }, null, 2)
  );
});
"""


def write_spec(spec_dir: Path, url: str, out_dir: Path) -> Path:
    spec_path = spec_dir / "tests" / "reduced-motion.spec.js"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(
        SPEC_TEMPLATE
            .replace("__URL_PLACEHOLDER__", json.dumps(url))
            .replace("__OUT_DIR_PLACEHOLDER__", json.dumps(str(out_dir).replace("\\", "/"))),
        encoding="utf-8",
    )
    (spec_dir / "playwright.config.js").write_text(
        "module.exports = { testDir: './tests', reporter: 'line', "
        "use: { trace: 'off' } };\n",
        encoding="utf-8",
    )
    return spec_path


def evaluate(report: dict) -> dict:
    default = report["default"]
    reduced = report["reduced"]

    # Find elements that were visible under default and invisible under reduced.
    # We match by index since both runs sample the same DOM.
    disappeared: list[dict] = []
    for i, (d, r) in enumerate(zip(default["samples"], reduced["samples"])):
        if d.get("visible") and not r.get("visible"):
            disappeared.append({"index": i, "tag": d["tag"], "id": d["id"], "cls": d["cls"]})

    # Count elements in the reduced run with animation/transition > 100ms.
    def secs(value: str | None) -> float:
        if not value:
            return 0.0
        # CSS durations can be "0s", "100ms", "0.3s", or comma-separated lists.
        first = str(value).split(",")[0].strip()
        if first.endswith("ms"):
            try: return float(first[:-2]) / 1000.0
            except ValueError: return 0.0
        if first.endswith("s"):
            try: return float(first[:-1])
            except ValueError: return 0.0
        return 0.0

    long_motion = []
    for i, s in enumerate(reduced["samples"]):
        d_t = secs(s.get("transition_duration"))
        d_a = secs(s.get("animation_duration"))
        if d_t > 0.1 or d_a > 0.1:
            long_motion.append({
                "index": i, "tag": s["tag"], "id": s["id"],
                "transition_s": round(d_t, 3),
                "animation_s": round(d_a, 3),
            })

    total = len(reduced["samples"]) or 1
    long_motion_ratio = len(long_motion) / total

    pass_overall = (len(disappeared) == 0) and (long_motion_ratio <= 0.05)
    return {
        "pass": pass_overall,
        "disappeared_under_reduced_motion": disappeared,
        "long_motion_elements_in_reduced_run": long_motion,
        "long_motion_ratio": round(long_motion_ratio, 3),
        "sample_size": total,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", help="The deployed URL to check.")
    parser.add_argument("--out", default=None, help="Directory to keep screenshots + raw report (else temp).")
    parser.add_argument("--timeout", type=int, default=120, help="Per-run timeout in seconds (default 120).")
    args = parser.parse_args(argv[1:])

    npx = resolve_npx()
    if npx is None:
        print("error: npx not found on PATH. Install Node.js: https://nodejs.org/", file=sys.stderr)
        return 2

    out_dir = Path(args.out).expanduser().resolve() if args.out else Path(tempfile.mkdtemp(prefix="webclaw-reduced-motion-"))
    out_dir.mkdir(parents=True, exist_ok=True)

    spec_dir = Path(tempfile.mkdtemp(prefix="webclaw-rm-spec-"))
    write_spec(spec_dir, args.url, out_dir)
    print(f"Running reduced-motion check against {args.url} (artifacts -> {out_dir})", file=sys.stderr)

    try:
        result = subprocess.run(
            [npx, "--yes", "playwright", "test", "--reporter", "line"],
            cwd=spec_dir, capture_output=True, text=True, timeout=args.timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"error: playwright run timed out after {args.timeout}s", file=sys.stderr)
        return 124

    report_path = out_dir / "report.json"
    if not report_path.is_file():
        print(f"error: report not found at {report_path}", file=sys.stderr)
        if result.stderr:
            print("stderr:\n" + result.stderr, file=sys.stderr)
        return 1

    report = json.loads(report_path.read_text(encoding="utf-8"))
    evaluation = evaluate(report)
    payload = {
        "url": args.url,
        "screenshots": {
            "default": str(out_dir / "default.png"),
            "reduced": str(out_dir / "reduced.png"),
        },
        "evaluation": evaluation,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if evaluation["pass"] else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))

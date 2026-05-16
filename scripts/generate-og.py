#!/usr/bin/env python3
"""
generate-og.py

Generate Open Graph (1200x630) images for every page of a Web Claw project.
Reads pages from <project>/blueprint/sitemap.md, design tokens from
<project>/design/tokens.json (or runs extract-tokens.py on the project's
style-guide.md if tokens.json is missing), and produces one PNG per page
in <project>/assets/og/.

The image is rendered by Playwright via npx -- the script writes a
self-contained HTML template that uses the project's color + type tokens,
loads it locally, and screenshots it at 1200x630.

Usage:
  python generate-og.py --project <project-dir>
  python generate-og.py --project <project-dir> --site-name "Studio Atrium"
  python generate-og.py --project <project-dir> --titles "/=Home,/about=About us"
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


def load_tokens(project_dir: Path) -> dict:
    """Load tokens.json, or fall back to running extract-tokens.py on
    blueprint/style-guide.md. Returns a partial token dict on best-effort.
    """
    tokens_json = project_dir / "design" / "tokens.json"
    if tokens_json.is_file():
        return json.loads(tokens_json.read_text(encoding="utf-8"))
    style_guide = project_dir / "blueprint" / "style-guide.md"
    if style_guide.is_file():
        extract = Path(__file__).resolve().parent / "extract-tokens.py"
        result = subprocess.run(
            [sys.executable, str(extract), str(style_guide)],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    return {}


def parse_sitemap_pages(sitemap_md: Path) -> list[tuple[str, str]]:
    """Return [(path, title), ...] extracted from sitemap.md. Title falls back
    to a humanized version of the path if none can be extracted.
    """
    if not sitemap_md.is_file():
        return [("/", "Home")]
    text = sitemap_md.read_text(encoding="utf-8")
    pages: list[tuple[str, str]] = []
    seen: set[str] = set()
    # Look for sitemap rows like `- /about - "About us"` or `| /about | About us |`.
    for line in text.splitlines():
        m = re.search(r"`(/[^`]*)`(?:\s*[-—]\s*(.+))?", line)
        if not m:
            continue
        path = m.group(1).strip()
        if path in seen:
            continue
        seen.add(path)
        raw_title = (m.group(2) or "").strip().strip('"').strip("*").strip()
        if not raw_title:
            base = path.strip("/").split("/")[-1] or "Home"
            raw_title = base.replace("-", " ").title()
        pages.append((path, raw_title))
    return pages or [("/", "Home")]


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>OG</title>
<style>
  :root {
    --bg: __BG__;
    --fg: __FG__;
    --accent: __ACCENT__;
    --font: __FONT__;
  }
  html, body { margin: 0; padding: 0; }
  body { width: 1200px; height: 630px; background: var(--bg); color: var(--fg); font-family: var(--font), system-ui, sans-serif; box-sizing: border-box; }
  .card { width: 100%; height: 100%; padding: 80px; display: flex; flex-direction: column; justify-content: space-between; }
  .top { display: flex; align-items: center; gap: 16px; font-size: 28px; opacity: 0.7; letter-spacing: 0.02em; }
  .dot { width: 18px; height: 18px; border-radius: 50%; background: var(--accent); }
  .title { font-size: 92px; line-height: 1.05; font-weight: 700; max-width: 1040px; letter-spacing: -0.02em; }
  .bottom { display: flex; justify-content: space-between; align-items: flex-end; }
  .url { font-size: 28px; opacity: 0.7; }
  .accent { font-size: 28px; color: var(--accent); font-weight: 600; }
</style></head>
<body>
  <div class="card">
    <div class="top"><span class="dot"></span>__SITE_NAME__</div>
    <h1 class="title">__TITLE__</h1>
    <div class="bottom">
      <div class="url">__SITE_URL__</div>
      <div class="accent">__PATH__</div>
    </div>
  </div>
</body></html>
"""


def render_html(title: str, path: str, site_name: str, site_url: str, tokens: dict) -> str:
    color = tokens.get("color", {})
    primitives = color.get("primitives", {})
    semantic = color.get("semantic", {})
    typo = tokens.get("typography", {}).get("family", {})
    def hex_for(token: str, fallback: str) -> str:
        if token in semantic:
            value = semantic[token]
            if value.startswith("#"):
                return value
            m = re.match(r"\{([a-z]+)\.([0-9A-Za-z\-]+)\}", value)
            if m:
                ramp = primitives.get(m.group(1).rstrip("s"), {})
                resolved = ramp.get(m.group(2))
                if resolved and resolved.startswith("#"):
                    return resolved
        return fallback
    bg = hex_for("surface.default", "#0e0e0e")
    fg = hex_for("text.primary", "#ffffff")
    accent_value = semantic.get("accent.action") or "#7c5cff"
    if isinstance(accent_value, str) and accent_value.startswith("{"):
        m = re.match(r"\{([a-z]+)\.([0-9A-Za-z\-]+)\}", accent_value)
        if m:
            ramp = primitives.get(m.group(1).rstrip("s"), {})
            accent_value = ramp.get(m.group(2)) or "#7c5cff"
    family = typo.get("display") or typo.get("body") or "Inter"
    family = family.strip('"').strip("`")

    return (HTML_TEMPLATE
            .replace("__BG__", bg)
            .replace("__FG__", fg)
            .replace("__ACCENT__", accent_value if isinstance(accent_value, str) else "#7c5cff")
            .replace("__FONT__", family)
            .replace("__SITE_NAME__", site_name)
            .replace("__SITE_URL__", site_url)
            .replace("__PATH__", path)
            .replace("__TITLE__", title))


SPEC_TEMPLATE = r"""
// @ts-check
const { test, chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const JOBS = __JOBS_PLACEHOLDER__;

test('render og images', async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  for (const job of JOBS) {
    await page.goto('file://' + job.html);
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: job.out, omitBackground: false });
  }
  await browser.close();
});
"""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", required=True, help="Web Claw project directory.")
    parser.add_argument("--site-name", default=None, help="Brand name to display on the card.")
    parser.add_argument("--site-url", default="", help="URL string shown bottom-left.")
    parser.add_argument("--titles", default=None,
                        help='Override sitemap titles. Format: "/=Home,/about=About us".')
    parser.add_argument("--out", default=None, help="Output directory (default: <project>/assets/og/).")
    parser.add_argument("--timeout", type=int, default=120, help="Playwright timeout in seconds.")
    args = parser.parse_args(argv[1:])

    project_dir = Path(args.project).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve() if args.out else (project_dir / "assets" / "og")
    out_dir.mkdir(parents=True, exist_ok=True)

    tokens = load_tokens(project_dir)
    pages = parse_sitemap_pages(project_dir / "blueprint" / "sitemap.md")
    if args.titles:
        overrides = dict(part.split("=", 1) for part in args.titles.split(",") if "=" in part)
        pages = [(p, overrides.get(p, t)) for p, t in pages]

    site_name = args.site_name or project_dir.name

    npx = resolve_npx()
    if npx is None:
        print("error: npx not found on PATH.", file=sys.stderr)
        return 2

    spec_dir = Path(tempfile.mkdtemp(prefix="webclaw-og-spec-"))
    html_dir = spec_dir / "html"
    html_dir.mkdir(parents=True, exist_ok=True)
    jobs: list[dict[str, str]] = []
    for path, title in pages:
        safe = ("home" if path == "/" else path.strip("/").replace("/", "_")) + ".png"
        html_path = html_dir / (safe + ".html")
        html_path.write_text(render_html(title, path, site_name, args.site_url, tokens), encoding="utf-8")
        jobs.append({"html": str(html_path).replace("\\", "/"), "out": str(out_dir / safe).replace("\\", "/")})

    (spec_dir / "tests").mkdir(parents=True, exist_ok=True)
    (spec_dir / "tests" / "og.spec.js").write_text(
        SPEC_TEMPLATE.replace("__JOBS_PLACEHOLDER__", json.dumps(jobs)),
        encoding="utf-8",
    )
    (spec_dir / "playwright.config.js").write_text(
        "module.exports = { testDir: './tests', reporter: 'line', "
        "use: { trace: 'off' } };\n",
        encoding="utf-8",
    )

    try:
        result = subprocess.run(
            [npx, "--yes", "playwright", "test", "--reporter", "line"],
            cwd=spec_dir, capture_output=True, text=True, timeout=args.timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        print(f"error: playwright timed out after {args.timeout}s", file=sys.stderr)
        return 124

    generated = sorted(out_dir.glob("*.png"))
    print(json.dumps({
        "out_dir": str(out_dir),
        "site_name": site_name,
        "pages": [{"path": p, "title": t} for p, t in pages],
        "generated": [str(p) for p in generated],
        "playwright_exit": result.returncode,
    }, indent=2, ensure_ascii=False))
    return 0 if generated else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""
visual-regression.py

Capture full-page screenshots of a deployed Web Claw site and diff them
against a baseline. Stores baselines under <project>/qa/snapshots/ and
diffs under <project>/qa/snapshots/diffs/.

First run captures the baseline (no comparison done). Subsequent runs
compare current screenshots against the baseline and emit a per-page
"diff ratio" (the fraction of pixels that differ above a per-channel
tolerance).

By default, pass = every page has a diff ratio <= 0.5%. Override with
--threshold.

Requires Node.js + Playwright (`npx playwright install chromium` if
needed). Pixel-diffing is done in pure stdlib (no Pillow / pixelmatch).

Usage:
  python visual-regression.py <url> --project <project-dir>
  python visual-regression.py <url> --project <project-dir> --update-baseline
  python visual-regression.py <url> --project <dir> --pages /,/about,/pricing
  python visual-regression.py <url> --project <dir> --threshold 0.01
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
import struct
import subprocess
import tempfile
import zlib
from pathlib import Path


def resolve_npx() -> str | None:
    return shutil.which("npx") or shutil.which("npx.cmd")


SPEC_TEMPLATE = r"""
// @ts-check
const { test, chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const BASE_URL = __BASE_URL_PLACEHOLDER__;
const PAGES = __PAGES_PLACEHOLDER__;
const OUT_DIR = __OUT_DIR_PLACEHOLDER__;

test('capture screenshots', async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  for (const p of PAGES) {
    const page = await context.newPage();
    const url = BASE_URL.replace(/\/$/, '') + (p === '/' ? '' : p);
    await page.goto(url, { waitUntil: 'load' });
    await page.waitForTimeout(1200);  // settle animations
    const safe = (p === '/' ? 'home' : p.replace(/^\//, '').replace(/\//g, '_')) + '.png';
    await page.screenshot({ path: path.join(OUT_DIR, safe), fullPage: true });
    await page.close();
  }
  await browser.close();
});
"""


def write_spec(spec_dir: Path, base_url: str, pages: list[str], out_dir: Path) -> Path:
    spec_path = spec_dir / "tests" / "vr-capture.spec.js"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(
        SPEC_TEMPLATE
            .replace("__BASE_URL_PLACEHOLDER__", json.dumps(base_url))
            .replace("__PAGES_PLACEHOLDER__", json.dumps(pages))
            .replace("__OUT_DIR_PLACEHOLDER__", json.dumps(str(out_dir).replace("\\", "/"))),
        encoding="utf-8",
    )
    (spec_dir / "playwright.config.js").write_text(
        "module.exports = { testDir: './tests', reporter: 'line', "
        "use: { trace: 'off' } };\n",
        encoding="utf-8",
    )
    return spec_path


def read_png(path: Path) -> tuple[int, int, bytes]:
    """Minimal PNG decoder: returns (width, height, raw RGBA bytes).

    Supports 8-bit RGB and RGBA PNGs; rejects others with a clear error.
    Implemented in stdlib so we don't depend on Pillow.
    """
    with path.open("rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"not a PNG: {path}")
    pos = 8
    width = height = 0
    bit_depth = color_type = 0
    idat = bytearray()
    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos+4])[0]
        ctype = data[pos+4:pos+8]
        chunk = data[pos+8:pos+8+length]
        if ctype == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk[:10])
        elif ctype == b"IDAT":
            idat.extend(chunk)
        elif ctype == b"IEND":
            break
        pos += 8 + length + 4  # length + type + data + CRC
    if bit_depth != 8 or color_type not in (2, 6):
        raise ValueError(f"unsupported PNG (bit depth {bit_depth}, color type {color_type}): {path}")
    raw = zlib.decompress(bytes(idat))
    channels = 4 if color_type == 6 else 3
    stride = width * channels
    out = bytearray(width * height * 4)
    pos = 0
    prev = bytearray(stride)
    for row in range(height):
        filter_type = raw[pos]; pos += 1
        scan = bytearray(raw[pos:pos+stride]); pos += stride
        # PNG filters
        if filter_type == 0:
            pass
        elif filter_type == 1:  # Sub
            for i in range(channels, stride):
                scan[i] = (scan[i] + scan[i-channels]) & 0xff
        elif filter_type == 2:  # Up
            for i in range(stride):
                scan[i] = (scan[i] + prev[i]) & 0xff
        elif filter_type == 3:  # Average
            for i in range(stride):
                left = scan[i-channels] if i >= channels else 0
                scan[i] = (scan[i] + ((left + prev[i]) >> 1)) & 0xff
        elif filter_type == 4:  # Paeth
            for i in range(stride):
                a = scan[i-channels] if i >= channels else 0
                b = prev[i]
                c = prev[i-channels] if i >= channels else 0
                p = a + b - c
                pa = abs(p - a); pb = abs(p - b); pc = abs(p - c)
                if pa <= pb and pa <= pc: pr = a
                elif pb <= pc: pr = b
                else: pr = c
                scan[i] = (scan[i] + pr) & 0xff
        else:
            raise ValueError(f"unsupported PNG filter type: {filter_type}")
        # Expand to RGBA
        if channels == 4:
            out[row*width*4 : row*width*4 + width*4] = scan
        else:
            for x in range(width):
                src = x * 3
                dst = (row * width + x) * 4
                out[dst]   = scan[src]
                out[dst+1] = scan[src+1]
                out[dst+2] = scan[src+2]
                out[dst+3] = 255
        prev = scan
    return width, height, bytes(out)


def diff_ratio(a_path: Path, b_path: Path, channel_tol: int = 8) -> float:
    """Return fraction of pixels that differ between two PNGs (0..1).

    A pixel "differs" if any RGB channel changes by more than `channel_tol`
    (default 8, i.e. ~3% of full range). Alpha differences are ignored.
    Returns 1.0 if dimensions differ.
    """
    w1, h1, p1 = read_png(a_path)
    w2, h2, p2 = read_png(b_path)
    if (w1, h1) != (w2, h2):
        return 1.0
    total = w1 * h1
    differing = 0
    for i in range(0, total * 4, 4):
        for c in range(3):  # RGB only
            if abs(p1[i + c] - p2[i + c]) > channel_tol:
                differing += 1
                break
    return differing / total if total else 0.0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", help="Base URL of the deployed site.")
    parser.add_argument("--project", required=True, help="Web Claw project directory (baselines saved under qa/snapshots/).")
    parser.add_argument("--pages", default="/", help="Comma-separated route list. Default '/'.")
    parser.add_argument("--update-baseline", action="store_true", help="Replace the baseline with the current capture.")
    parser.add_argument("--threshold", type=float, default=0.005,
                        help="Max acceptable diff ratio per page (default 0.005 = 0.5%%).")
    parser.add_argument("--timeout", type=int, default=180, help="Per-capture timeout in seconds (default 180).")
    args = parser.parse_args(argv[1:])

    project_dir = Path(args.project).expanduser().resolve()
    snapshots_dir = project_dir / "qa" / "snapshots"
    current_dir = Path(tempfile.mkdtemp(prefix="webclaw-vr-current-"))
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    npx = resolve_npx()
    if npx is None:
        print("error: npx not found on PATH.", file=sys.stderr)
        return 2

    pages = [p.strip() for p in args.pages.split(",") if p.strip()]
    spec_dir = Path(tempfile.mkdtemp(prefix="webclaw-vr-spec-"))
    write_spec(spec_dir, args.url, pages, current_dir)

    print(f"Capturing screenshots for {len(pages)} page(s)...", file=sys.stderr)
    try:
        subprocess.run(
            [npx, "--yes", "playwright", "test", "--reporter", "line"],
            cwd=spec_dir, capture_output=True, text=True, timeout=args.timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        print(f"error: playwright capture timed out after {args.timeout}s", file=sys.stderr)
        return 124

    captures = sorted(current_dir.glob("*.png"))
    if not captures:
        print("error: no captures produced.", file=sys.stderr)
        return 1

    if args.update_baseline:
        # Replace baseline.
        for p in snapshots_dir.glob("*.png"):
            if p.is_file():
                p.unlink()
        for c in captures:
            shutil.copy(c, snapshots_dir / c.name)
        print(f"Updated baseline: {len(captures)} screenshots in {snapshots_dir}", file=sys.stderr)
        return 0

    results: list[dict] = []
    overall_pass = True
    diffs_dir = snapshots_dir / "diffs"
    diffs_dir.mkdir(parents=True, exist_ok=True)

    for c in captures:
        baseline = snapshots_dir / c.name
        if not baseline.is_file():
            # No baseline yet; save and skip.
            shutil.copy(c, baseline)
            results.append({"page": c.name, "status": "new-baseline", "ratio": None})
            continue
        ratio = diff_ratio(baseline, c)
        page_pass = ratio <= args.threshold
        if not page_pass:
            shutil.copy(c, diffs_dir / c.name)
            overall_pass = False
        results.append({
            "page": c.name,
            "status": "diff",
            "ratio": round(ratio, 5),
            "threshold": args.threshold,
            "pass": page_pass,
            "current_artifact": str(diffs_dir / c.name) if not page_pass else None,
        })

    payload = {
        "url": args.url,
        "project": str(project_dir),
        "pages": pages,
        "threshold": args.threshold,
        "pass": overall_pass,
        "results": results,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if overall_pass else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""
scrape-awwwards.py

Optional legacy helper for user-requested award-gallery research. Web Claw v2
does not require Awwwards or any other award source; use this only when the
user explicitly wants that source included in the inspiration pool.

The helper is intentionally thin and polite: single-request-per-page,
identifies as Web Claw, and respects robots.txt by default.

Usage:
  python scrape-awwwards.py [--index SOTD|HONORS|SOTM] [--out candidates.json]
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
import urllib.request
import urllib.error
import urllib.robotparser
from pathlib import Path


INDICES = {
    "SOTD":   "https://www.awwwards.com/awards/sites-of-the-day/",
    "HONORS": "https://www.awwwards.com/awards/honorable-mentions/",
    "SOTM":   "https://www.awwwards.com/awards/sites-of-the-month/",
}

USER_AGENT = "WebClaw-Researcher/2.0 (+https://example.com/bot)"


def robots_allows(url: str) -> bool:
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url("https://www.awwwards.com/robots.txt")
    try:
        rp.read()
    except Exception:
        return False
    return rp.can_fetch(USER_AGENT, url)


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_candidates(html: str) -> list[dict]:
    """
    Best-effort HTML parsing. Looks for anchor tags whose href starts with
    /sites/ (the award-gallery detail page pattern). Returns deduped list of
    { slug, title, awwwards_url } dicts.
    """
    pattern = re.compile(
        r'<a[^>]+href="(/sites/[^"]+)"[^>]*>(.*?)</a>',
        re.IGNORECASE | re.DOTALL,
    )
    seen: set[str] = set()
    out: list[dict] = []
    for m in pattern.finditer(html):
        href = m.group(1)
        inner = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not inner or href in seen:
            continue
        seen.add(href)
        out.append({
            "slug": href.rsplit("/", 2)[-2] if href.endswith("/") else href.rsplit("/", 1)[-1],
            "title": inner,
            "awwwards_url": f"https://www.awwwards.com{href}",
        })
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="SOTD", choices=list(INDICES.keys()))
    parser.add_argument("--out", default=None, help="Optional path to write the JSON output")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args(argv[1:])

    url = INDICES[args.index]
    print(f"fetching: {url}", file=sys.stderr)
    if not robots_allows(url):
        print(f"error: robots.txt does not allow fetching {url} for {USER_AGENT}", file=sys.stderr)
        return 1
    try:
        html = fetch(url)
    except urllib.error.HTTPError as e:
        print(f"error: HTTP {e.code} while fetching {url}", file=sys.stderr)
        print("Awwwards may rate-limit; try again with a different User-Agent or wait.", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    candidates = extract_candidates(html)[: args.limit]
    print(f"found {len(candidates)} candidate(s)", file=sys.stderr)

    payload = {
        "index": args.index,
        "source": url,
        "candidates": candidates,
    }

    output_json = json.dumps(payload, indent=2, ensure_ascii=False)
    print(output_json)

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json, encoding="utf-8")
        print(f"wrote: {out_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

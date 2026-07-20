"""Console encoding helpers for Web Claw scripts.

Windows defaults to cp1252 for stdout/stderr when the terminal isn't set up
for UTF-8. Any print() of a non-ASCII glyph (em-dash, arrow, checkmark) then
raises UnicodeEncodeError mid-run.

`safe_stdout()` reconfigures both streams to UTF-8 with `errors="replace"`,
so any stray glyph becomes "?" instead of crashing. Safe to call multiple
times; safe on Python 3.7+; no-ops on streams that don't support reconfigure
(some IDE consoles, captured streams, piped output on older Pythons).

Call once at the top of every script:

    from _console import safe_stdout
    safe_stdout()
"""

from __future__ import annotations

import sys


def safe_stdout() -> None:
    """Make stdout/stderr tolerant of non-ASCII glyphs on any locale."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            # Stream type doesn't support reconfigure or is detached.
            pass

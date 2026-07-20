#!/usr/bin/env python3
"""
Web Claw Project Initializer

Creates a complete Web Claw project workspace including memory.md,
decisions/ folder, all design/research/qa directories, and blank
starter files. Run once per project at BRIEF:INTERVIEW.

Usage:
    python init-project.py "<project-name>" --path <workspace-dir>
    python init-project.py "Meridian" --path "D:/03 WORK/01 PROJECTS/01 Websites"
    python init-project.py "Meridian" --path . --slug meridian-site
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from textwrap import dedent


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "web-claw-project"


def write_text(path: Path, content: str, force: bool = False) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def write_json(path: Path, data: object, force: bool = False) -> bool:
    return write_text(path, json.dumps(data, indent=2), force)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_name", help="Human-readable project name.")
    parser.add_argument("--path", default=".", help="Directory where the project folder is created.")
    parser.add_argument("--slug", help="Optional folder name. Defaults to slugified project name.")
    parser.add_argument(
        "--mode",
        choices=["interactive", "fast"],
        default="interactive",
        help="interactive (default, user signs off each artifact) | fast (auto-approve, QA gates remain hard).",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    slug = args.slug or slugify(args.project_name)
    root = Path(args.path).expanduser().resolve() / slug
    today = dt.date.today().isoformat()
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    created: list[str] = []
    skipped: list[str] = []

    # Create directory structure
    dirs = [
        "brief",
        "research",
        "design",
        "decisions",
        "qa",
        "assets",
    ]
    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)

    # -- memory.md ----------------------------------------------------------
    next_action_initial = (
        "Pick defensible discovery defaults; write brief/client-brief.md without user prompts. Then advance Phase to RESEARCH:SKILL-DISCOVERY and begin companion skill discovery. Log judgment calls to decisions/NNN-auto-*.md."
        if args.mode == "fast"
        else "Load references/ignition-quick.md (or ignition-full.md for complex projects). Ask the brief interview questions, including inspiration (Q9) and its fallback ladder. Write brief/client-brief.md. Then advance Phase to RESEARCH:SKILL-DISCOVERY."
    )
    memory_content = dedent(f"""\
        # Project Memory -- {args.project_name}
        Last updated: {now}

        ## Identity
        - Name: {args.project_name}
        - Goal: [PENDING -- fill from brief Q3]
        - Value proposition: [PENDING -- fill from brief Q6; becomes the hero headline]
        - Audience: [PENDING -- fill from brief Q7]
        - Motion: [PENDING -- restrained | active | maximalist]
        - Stack: PENDING
        - Deploy: PENDING

        ## State
        - Mode: {args.mode}
        - Phase: BRIEF:INTERVIEW
        - Step: gathering discovery answers
        - Last artifact: (none yet)
        - User sign-off: PENDING
        - Next action: {next_action_initial}

        ## Pinned Decisions
        <!-- Add entries as decisions are made: -->
        <!-- - [DECISION-001] <topic> -> decisions/001-<topic>.md -->

        ## Blockers
        - None

        ## Compaction Snapshot
        <!-- Populated when context nears its limit. Read this section first on resume after compaction. -->
    """)

    # ── brief/client-brief.md starter ───────────────────────────────────────────
    discovery_content = dedent(f"""\
        # Client Brief — {args.project_name}
        Created: {today}

        ## Part 1 — Understand the client

        ### Q1 — Brand name
        {args.project_name}

        ### Q2 — What is the brand / company / business about?
        [PENDING — story, offer, what it does, why it exists]

        ### Q3 — What must the website achieve? (the single measurable business outcome)
        [PENDING]

        ### Q4 — What must a visitor DO on the site? (the one action)
        [PENDING]

        ### Q5 — The ONE objective the site is judged by
        [PENDING]

        ### Q6 — Value proposition (becomes the hero headline)
        [PENDING — one sentence a stranger understands in 3 seconds]

        ### Q7 — Primary visitor / target audience
        [PENDING]

        ## Part 2 — Taste and feel

        ### Q8 — Three adjectives / feel
        [PENDING]

        ### Q9 — Inspiration sources
        <!-- Load-bearing: RESEARCH:OPEN-WEB is anchored on this. Do not leave [PENDING]. -->

        #### Q9a — References (aim for 3-7)
        | # | Source | Axis | Borrow | Do NOT copy |
        |---|--------|------|--------|-------------|
        | 1 | [PENDING] | | | |

        #### Q9b — If no links: ladder used
        [PENDING — non-web brands / sites they enjoy / reaction round / adjectives-only + thin-evidence flag]

        #### Q9c — Anti-references (what this must never look like)
        [PENDING]

        #### Q9d — Search anchors (agent-written, 3-5 searchable phrases)
        [PENDING]

        ### Q10 — Known competitors (direct / aspirational)
        [PENDING — verified in RESEARCH:COMPETITORS]

        ### Q11 — Signature moment ("holy shit" moment)
        [PENDING]

        ### Q12 — Motion intensity
        [PENDING]

        ### Q13 — Off-limits / what not to copy
        [PENDING]

        ## Part 3 — Practical

        ### Q14 — Pages
        [PENDING]

        ### Q15 — Primary CTA(s)
        [PENDING]

        ### Q16 — Existing assets
        [PENDING]

        ### Q17 — Tech stack preference
        [ASSUMED: You choose — agent will infer from motion spec and deploy target]

        ### Q18 — Deployment target
        [ASSUMED: Vercel]

        ### Q19 — CMS
        [ASSUMED: None — static content]

        ### Q20 — Performance budget
        [ASSUMED: defaults per web-claw/references/budgets.yaml (lighthouse.* + core_web_vitals.*)]

        ### Q21 — Accessibility floor
        [ASSUMED: defaults per web-claw/references/budgets.yaml (accessibility.*)]

        ## The 3-Second Test
        When the hero loads, a stranger must be able to answer within 3 seconds:
        1. What is this? 2. Who is it for? 3. What do I do next?
        The brief is not complete until Q6 passes this test.
    """)

    # ── site-brief.json ───────────────────────────────────────────────────────
    site_brief = {
        "project_name": args.project_name,
        "slug": slug,
        "created_on": today,
        "business_goal": "",
        "primary_audience": "",
        "primary_cta": "",
        "offer": "",
        "required_pages": [],
        "brand_traits": [],
        "motion_intensity": "",
        "technical_stack": "",
        "deploy_target": "",
        "constraints": [],
        "assumptions": [],
    }

    # ── sources.json ──────────────────────────────────────────────────────────
    sources: list[dict] = []

    # ── dependencies.json ─────────────────────────────────────────────────────
    dependencies = {
        "package_manager": "",
        "framework": {"name": "", "version": "", "reason": ""},
        "styling": {"name": "", "version": "", "reason": ""},
        "animation": [],
        "auxiliary": [],
        "dev_dependencies": [],
        "rejected": [],
        "install_commands": [],
    }

    # ── qa-plan starter ───────────────────────────────────────────────────────
    qa_plan = dedent(f"""\
        # QA Plan — {args.project_name}

        ## Phase 1 gate
        File: web-claw/qa/phase-1-gate.md
        Status: PENDING

        ## Phase 2 gate
        File: web-claw/qa/phase-2-gate.md
        Status: PENDING

        ## Phase 3 / Launch gate
        File: web-claw/qa/phase-3-gate.md
        Status: PENDING

        ## Lighthouse targets
        Numeric floors come from `web-claw/references/budgets.yaml -> lighthouse.*`.
        - Performance (mobile): `lighthouse.mobile.performance`
        - Accessibility (mobile): `lighthouse.mobile.accessibility`
        - Best Practices (mobile): `lighthouse.mobile.best_practices`
        - SEO (mobile): `lighthouse.mobile.seo`
        - Desktop floors: `lighthouse.desktop.*` (additive, higher than mobile)

        ## Evidence
        <!-- Paste script outputs here as phases complete -->
    """)

    files: dict[Path, str | None] = {
        root / "memory.md": memory_content,
        root / "brief" / "client-brief.md": discovery_content,
        root / "qa" / "qa-plan.md": qa_plan,
        root / "assets" / ".gitkeep": "",
        root / "decisions" / ".gitkeep": "",
    }

    json_files: dict[Path, object] = {
        root / "site-brief.json": site_brief,
        root / "sources.json": sources,
        root / "dependencies.json": dependencies,
    }

    for path, content in files.items():
        if write_text(path, content or "", args.force):
            created.append(str(path.relative_to(root)))
        else:
            skipped.append(str(path.relative_to(root)))

    for path, data in json_files.items():
        if write_json(path, data, args.force):
            created.append(str(path.relative_to(root)))
        else:
            skipped.append(str(path.relative_to(root)))

    print(f"Web Claw workspace initialized: {root}")
    print(f"Created: {len(created)} file(s)")
    for item in created:
        print(f"  + {item}")
    if skipped:
        print(f"Skipped (already exist): {len(skipped)} file(s)")
        for item in skipped:
            print(f"  = {item}")

    print()
    print("Next steps:")
    print("  1. Load SKILL.md -> read memory.md (just initialized)")
    print("  2. Load references/ignition-quick.md or ignition-full.md")
    print("  3. Ask the brief interview questions, including inspiration (Q9) and its fallback ladder. Write brief/client-brief.md.")
    print("  4. Update memory.md: fill Identity fields, advance Phase to RESEARCH:SKILL-DISCOVERY.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

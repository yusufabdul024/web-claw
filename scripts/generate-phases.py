#!/usr/bin/env python3
"""
Web Claw Phase Docs Generator

Generates phase-1.md, phase-2.md, phase-3.md and a sequential-prompts file.

By default, reads phase definitions from <workspace>/plan.md so the generated
phase docs reflect the project's actual sitemap, wireframes, stack, and
success criteria -- not generic boilerplate. If plan.md is missing or
doesn't contain parseable phase sections, falls back to a hardcoded skeleton
(the legacy v1 behavior) and emits a warning.

Usage:
    python generate-phases.py --workspace <project-dir>
    python generate-phases.py --workspace ./meridian --force
    python generate-phases.py --workspace ./meridian --phases 4
    python generate-phases.py --workspace ./meridian --dry-run
    python generate-phases.py --workspace ./meridian --ignore-plan   # force fallback
"""

from __future__ import annotations

import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
from pathlib import Path
from textwrap import dedent

FALLBACK_PHASES = [
    {
        "name": "Foundation and Static Experience",
        "mission": (
            "Build the site foundation: repo init, design tokens, layout primitives, "
            "all reusable components as static components, and all pages assembled with real copy. "
            "No animations. Deploy to a visible preview URL at the end."
        ),
        "tasks": [
            "Confirm stack and package manager. Run `scripts/install-deps.py research/tech-stack.md --dry-run`.",
            "Translate `blueprint/style-guide.md` tokens into CSS custom properties or Tailwind config.",
            "Build all static components from `blueprint/wireframes.md` component inventory with exact prop shapes.",
            "Assemble all pages with real copy from `blueprint/sitemap.md`. Zero lorem ipsum.",
            "Add SEO meta tags (title, description, og:) to all pages.",
            "Wire accessibility basics: skip-to-content, heading hierarchy, alt text, focus-visible styles.",
            "Deploy to preview URL. Verify all pages load without 404 or console errors.",
            "Run `qa/phase-1-gate.md`. Fix all failures before presenting preview.",
            "Update `memory.md`: Phase = EXECUTION:PHASE-2, sign-off = PENDING.",
        ],
        "acceptance": [
            "All pages in sitemap.md reachable at preview URL with no 404s.",
            "No console errors on any page.",
            "Design tokens applied (spot-check: heading font, background, CTA color).",
            "No lorem ipsum anywhere.",
            "All qa/phase-1-gate.md items pass.",
        ],
        "verification": [
            "Tab through home page — every interactive element is keyboard-reachable.",
            "Resize to 375px and 1440px — no horizontal scroll, no overflow.",
            "Run: `python scripts/audit-perf.py <preview-url>`",
            "Run: `python scripts/check-a11y.py <preview-url>`",
        ],
        "handoff": (
            "Phase 2 receives a deployed preview with all pages, components, copy, and tokens. "
            "Animation library installation begins in Phase 2 — do not install in Phase 1."
        ),
    },
    {
        "name": "Animations, Signature Moments, and Polish",
        "mission": (
            "Install motion libraries. Implement all animations from `blueprint/animations.md`. "
            "Add prefers-reduced-motion fallbacks for every animation. Deploy to preview."
        ),
        "tasks": [
            "Run `scripts/install-deps.py research/tech-stack.md` to install motion libraries.",
            "Implement above-the-fold entrance choreography per animations.md (total ≤ 1.5s).",
            "Implement scroll-triggered section reveals (opacity 0→1, y 24→0, 800ms ease-out-quart).",
            "Implement SIGNATURE section per `blueprint/animations.md §signature`. Reserve ~50% of phase effort here.",
            "Implement micro-interactions: button hover, link hover, input focus, card hover.",
            "Add prefers-reduced-motion fallback for every animation (replace, not remove).",
            "Deploy to preview URL.",
            "Run `qa/phase-2-gate.md`. Fix all failures before presenting preview.",
            "Update `memory.md`: Phase = EXECUTION:PHASE-3, sign-off = PENDING.",
        ],
        "acceptance": [
            "Entrance animations match animations.md timing and easing exactly.",
            "SIGNATURE section renders in Chrome, Safari, and Chrome Android emulation.",
            "prefers-reduced-motion: all animations replaced with static alternatives.",
            "Lighthouse mobile Performance still meets `references/budgets.yaml -> lighthouse.mobile.performance` with animations active.",
            "All qa/phase-2-gate.md items pass.",
        ],
        "verification": [
            "Enable DevTools: Rendering → prefers-reduced-motion → reduce. Reload. Page fully readable.",
            "Run: `python scripts/audit-perf.py <preview-url>` — Performance ≥ 90.",
            "Record DevTools Performance tab during scroll — no long tasks > 50ms during animation.",
        ],
        "handoff": (
            "Phase 3 receives a fully animated preview passing phase-2-gate. "
            "No new components or pages in Phase 3 — polish, SEO, perf, a11y, and launch only."
        ),
    },
    {
        "name": "Launch: QA, Performance, SEO, and Production Deploy",
        "mission": (
            "Achieve launch readiness. Hit all budgets. Finalize copy. Wire forms. "
            "Complete SEO. Deploy to production domain."
        ),
        "tasks": [
            "Run `scripts/audit-perf.py <url>` (mobile, median of 3 runs). Fail any score below `references/budgets.yaml -> lighthouse.mobile.*`.",
            "Run `scripts/check-a11y.py <url>`. Fail any pa11y errors above `budgets.yaml -> accessibility.axe_violations_*_max`.",
            "Sweep every page: zero lorem ipsum, zero placeholder images, zero console errors.",
            "Finalize SEO: sitemap.xml, robots.txt, og: tags per page, canonical URLs, JSON-LD on home.",
            "Wire all form endpoints. Test each form — submit → delivery confirmed.",
            "Run cross-browser smoke: Chrome, Safari, Firefox, Chrome Android, Safari iOS.",
            "Wire analytics if specified in discovery.md.",
            "Deploy to production domain. Verify SSL, canonical, and redirects.",
            "Run `qa/phase-3-gate.md`. Fix all failures.",
            "Run `python scripts/check-output.py --workspace <project> --phase all`. Must exit 0.",
            "Update `memory.md`: Phase = QA:FINAL, sign-off = PENDING. (DONE is set only when QA:FINAL exits per references/state-machine.md.)",
        ],
        "acceptance": [
            "Lighthouse mobile meets all four floors in `references/budgets.yaml -> lighthouse.mobile.*`.",
            "axe-core: at or below `budgets.yaml -> accessibility.axe_violations_critical_max + axe_violations_serious_max`.",
            "All forms submit and deliver to correct endpoint.",
            "Cross-browser smoke passes on 5 browsers/devices.",
            "Production domain live with SSL.",
            "All qa/phase-3-gate.md items pass.",
            "`check-output.py --phase all` exits 0.",
            "memory.md → Phase: QA:FINAL (advances to DONE only after qa/pre-launch-checklist.md passes per references/state-machine.md).",
        ],
        "verification": [
            "Run: `python scripts/audit-perf.py <production-url>` — paste median of 3 runs.",
            "Run: `python scripts/check-a11y.py <production-url>` — zero critical/serious.",
            "Open production URL in Chrome, Safari, Firefox — scroll, click CTA, check console.",
            "Submit each form. Confirm delivery.",
        ],
        "handoff": "Phase 3 build complete. Advances to QA:FINAL for the pre-launch checklist; QA:FINAL advances to DONE on user sign-off. See references/state-machine.md.",
    },
]


def _split_into_phase_sections(plan_md: str) -> list[tuple[int, str, str]]:
    """Return [(phase_number, name, body), ...] from a plan.md.

    A "phase section" begins at a line matching `## Phase N <separator> <name>`
    and ends at the next `## ` heading or EOF.
    """
    header_re = re.compile(r"^## Phase\s+(\d+)\s*[—–\-:]\s*(.+?)\s*$", re.MULTILINE)
    matches = list(header_re.finditer(plan_md))
    sections: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        number = int(m.group(1))
        name = m.group(2).strip()
        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(plan_md)
        sections.append((number, name, plan_md[body_start:body_end]))
    return sections


def _extract_bullets(body: str, label_pattern: str) -> list[str]:
    """Find a labeled list in body (e.g. `**Steps (high-level):**`) and return
    its bullets/numbered items as plain strings. Stops at the next bold-label
    or markdown subheading.
    """
    label_re = re.compile(label_pattern + r"\s*$", re.MULTILINE | re.IGNORECASE)
    m = label_re.search(body)
    if not m:
        return []
    rest = body[m.end():]
    # Stop at next bold-label-heading or a `#`/`##`/`###` heading.
    stop = re.search(r"^(\*\*[^*]+\*\*\s*$|#{1,6}\s)", rest, re.MULTILINE)
    block = rest[: stop.start()] if stop else rest
    items: list[str] = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Numbered: "1. text"  |  Bulleted: "- text"  |  Checkbox: "- [ ] text"
        m2 = re.match(r"^(?:\d+\.\s+|-\s+\[\s*[xX ]?\s*\]\s+|-\s+|\*\s+)(.+)$", stripped)
        if m2:
            items.append(m2.group(1).strip())
    return items


def _extract_field(body: str, label_pattern: str) -> str | None:
    """Find a single-line labeled value (e.g. `**Goal:** ...`) and return it."""
    pattern = re.compile(label_pattern + r"\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)
    m = pattern.search(body)
    return m.group(1).strip() if m else None


def load_phases_from_plan(workspace: Path) -> list[dict] | None:
    """Parse <workspace>/plan.md into phase dicts shaped like FALLBACK_PHASES.

    Returns None if plan.md is missing or contains no recognizable phase
    sections (in which case the caller should fall back to FALLBACK_PHASES
    and emit a warning).
    """
    plan_path = workspace / "plan.md"
    if not plan_path.is_file():
        return None
    md = plan_path.read_text(encoding="utf-8")
    sections = _split_into_phase_sections(md)
    if not sections:
        return None

    phases: list[dict] = []
    for number, name, body in sections:
        goal = _extract_field(body, r"\*\*Goal:\*\*")
        tasks = _extract_bullets(body, r"\*\*Steps\s*\(high-level\):\*\*")
        if not tasks:
            tasks = _extract_bullets(body, r"\*\*Steps:\*\*")
        if not tasks:
            tasks = _extract_bullets(body, r"\*\*Tasks:\*\*")
        acceptance = _extract_bullets(body, r"\*\*Success criteria:\*\*")
        if not acceptance:
            acceptance = _extract_bullets(body, r"\*\*Acceptance criteria:\*\*")
        verification = _extract_bullets(body, r"\*\*Verification:\*\*")
        handoff = _extract_field(body, r"\*\*Handoff:\*\*")

        # Inherit verification/handoff defaults from FALLBACK_PHASES when the
        # plan does not specify them. Plan-template.md does not have these
        # fields by default; the legacy hardcoded text is a reasonable seed.
        fallback = FALLBACK_PHASES[number - 1] if number - 1 < len(FALLBACK_PHASES) else None
        if not verification and fallback:
            verification = fallback["verification"]
        if not handoff and fallback:
            handoff = fallback["handoff"]

        phases.append({
            "name": name,
            "mission": goal or (fallback["mission"] if fallback else f"Phase {number}: implement the next slice."),
            "tasks": tasks or (fallback["tasks"] if fallback else ["Define and implement phase scope from plan.md."]),
            "acceptance": acceptance or (fallback["acceptance"] if fallback else ["Phase output matches plan.md."]),
            "verification": verification or ["Run: `python scripts/audit-perf.py <preview-url>`",
                                              "Run: `python scripts/check-a11y.py <preview-url>`"],
            "handoff": handoff or "Summarize completed work, changed files, unresolved questions, and risks.",
        })

    return phases if phases else None


def write(path: Path, content: str, force: bool, dry_run: bool) -> bool:
    if path.exists() and not force:
        return False
    if dry_run:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def phase_markdown(index: int, phase: dict) -> str:
    tasks = "\n".join(f"{i}. {t}" for i, t in enumerate(phase["tasks"], 1))
    acceptance = "\n".join(f"- [ ] {a}" for a in phase["acceptance"])
    verification = "\n".join(f"- {v}" for v in phase["verification"])
    return dedent(f"""\
        # Phase {index}: {phase["name"]}

        ## Agent Mission

        {phase["mission"]}

        ## Read First

        - memory.md  ← MANDATORY first
        - blueprint/discovery.md
        - blueprint/sitemap.md
        - blueprint/style-guide.md
        - blueprint/wireframes.md
        - blueprint/animations.md
        - research/tech-stack.md
        - web-claw/references/agent-handoff-protocol.md

        ## Own These Files or Areas

        - Define exact file and module ownership before implementation begins.
        - Do not touch files owned by a previous phase unless fixing a blocker.

        ## Inputs

        - memory.md (current project state and pinned decisions)
        - All blueprint artifacts (signed off by user)
        - research/tech-stack.md (signed off by user)
        - Phase {index - 1} handoff notes (if applicable)

        ## Build Tasks

        {tasks}

        ## Acceptance Criteria

        {acceptance}

        ## Verification

        {verification}

        ## Handoff

        {phase["handoff"]}
    """)


def sequential_prompts_md(count: int, phases: list[dict]) -> str:
    lines = ["# Sequential Agent Prompts", ""]
    for i in range(1, count + 1):
        name = phases[i - 1]["name"] if i <= len(phases) else f"Extended Scope {i}"
        lines += [
            f"## Phase {i}: {name}", "",
            "Use this prompt:", "", "```text",
            (
                f"Read memory.md first. You are the Implementer Agent for Phase {i}: {name}. "
                f"Read web-claw/agents/implementer-agent.md, then phase-{i}.md. "
                f"Execute every build task in order. Every step must be verifiable. "
                f"Do not skip the QA gate. At the end: update memory.md."
            ),
            "```", "",
        ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace", required=True, help="Web Claw project workspace directory.")
    parser.add_argument("--phases", type=int, default=3, help="Number of phase files to generate.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing phase files.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without writing.")
    parser.add_argument("--ignore-plan", action="store_true",
                        help="Skip parsing plan.md and use the hardcoded fallback skeleton.")
    args = parser.parse_args()

    if args.phases < 1:
        raise SystemExit("--phases must be at least 1")

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists():
        raise SystemExit(f"Workspace not found: {workspace}")

    # Prefer the project's plan.md (if it has parseable phase sections) over
    # the hardcoded skeleton -- the reviewer's concern was that the legacy
    # generator emitted boilerplate ignoring project specifics. The fallback
    # is retained as a last-resort for cold-start workspaces with no plan.md.
    phases = None if args.ignore_plan else load_phases_from_plan(workspace)
    if phases is None:
        if not args.ignore_plan:
            print(
                f"note: no parseable plan.md found at {workspace / 'plan.md'}; "
                "using hardcoded fallback skeleton.",
                file=sys.stderr,
            )
        phases = FALLBACK_PHASES
    else:
        print(f"note: derived {len(phases)} phase(s) from {workspace / 'plan.md'}.", file=sys.stderr)

    generated: list[str] = []
    skipped: list[str] = []

    for index in range(1, args.phases + 1):
        phase = phases[index - 1] if index <= len(phases) else {
            "name": f"Extended Scope {index}",
            "mission": "Implement the next independent slice of the website plan.",
            "tasks": ["Define phase scope from plan.md.", "Implement owned files.", "Update memory.md."],
            "acceptance": ["Phase output matches plan.md.", "QA gate passes."],
            "verification": ["Run lint, typecheck, tests, and build.", "Browser-check changed pages."],
            "handoff": "Summarize completed work, changed files, unresolved questions, and risks.",
        }
        content = phase_markdown(index, phase)
        path = workspace / f"phase-{index}.md"
        label = str(path.relative_to(workspace))

        if args.dry_run:
            status = "would create" if not path.exists() else ("would overwrite" if args.force else "would skip")
            print(f"  {status}: {label}")
        elif write(path, content, args.force, False):
            generated.append(label)
        else:
            skipped.append(label)

    prompts_path = workspace / "prompts" / "sequential-prompts.md"
    prompts_label = str(prompts_path.relative_to(workspace))
    if args.dry_run:
        status = "would create" if not prompts_path.exists() else ("would overwrite" if args.force else "would skip")
        print(f"  {status}: {prompts_label}")
    elif write(prompts_path, sequential_prompts_md(args.phases, phases), args.force, False):
        generated.append(prompts_label)
    else:
        skipped.append(prompts_label)

    if not args.dry_run:
        print(f"Workspace: {workspace}")
        print(f"Generated: {len(generated)} file(s)")
        for item in generated:
            print(f"  + {item}")
        if skipped:
            print(f"Skipped (use --force to overwrite): {len(skipped)}")
            for item in skipped:
                print(f"  = {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

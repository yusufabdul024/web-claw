---
name: web-claw
description: Use this skill whenever the user wants to plan, design, or build a scroll-stopping, award-winning website — landing pages, marketing sites, portfolios, agency sites, product launches, SaaS sites, brand sites, or anything where design quality, animation, and interaction matter. Triggers on phrases like "build a website", "design a landing page", "scroll-stopping site", "award-winning website", "Awwwards-quality", "$10k website", "premium site", "high-end web design", "animated website", "Relume-style sitemap", "site planning", "wireframes", "style guide", "design system for a site", "motion design for a site", or any request to break a web project into shippable phases. Web Claw orchestrates a complete two-phase pipeline (Relume-inspired blueprint → Awwwards-inspired execution) with specialized subagents for UX strategy, UI strategy, visual design, motion design, research, implementation, and QA. Lean toward triggering this skill whenever the surface intent is "a website with taste," even if the user did not explicitly say "scroll-stopping" or "award-winning."
---

# Web Claw — Build Scroll-Stopping, Award-Winning Websites

Web Claw is a structured, two-phase methodology for designing and shipping $10k-caliber websites. It pairs the rigorous information-architecture-first approach of Relume with the bleeding-edge interaction language of Awwwards winners.

---

## ⚡ MANDATORY: First Read / Last Write Protocol

**Every session. No exceptions.**

### First Read (before any action)
1. Check if `<project>/memory.md` exists.
   - If YES: read it. Read any `decisions/` files listed in Pinned Decisions. Read the Last artifact file.
   - If NO: run `scripts/init-project.py "<project-name>" --path <workspace> [--mode interactive|fast]` to initialize.
2. Read `Mode`. Behavior changes per mode (see "Two run modes" below).
3. If `User sign-off: PENDING` in memory.md — re-present the last artifact. Do not advance.
4. If `User sign-off: AUTO` in fast mode — that state was auto-approved; continue to the Next action.
5. Execute the `Next action` exactly as written in memory.md.

### Last Write (before ending any session)
1. Update `memory.md`: Phase, Step, Last artifact, User sign-off, Next action.
2. If a significant decision was made: create `decisions/NNN-topic.md`.
3. If context is near its limit: write the Compaction Snapshot into `memory.md`.

See `references/memory-format.md` for the full schema, decision record format, and compaction protocol.

---

## The Pipeline (State Machine)

```
IGNITION → BLUEPRINT:SITEMAP → BLUEPRINT:STYLE-GUIDE → BLUEPRINT:WIREFRAMES →
BLUEPRINT:ANIMATIONS → RESEARCH:AWWWARDS → RESEARCH:YOUTUBE →
EXECUTION:STACK → EXECUTION:PLAN → EXECUTION:PHASE-1 → EXECUTION:PHASE-2 →
EXECUTION:PHASE-3 → QA:FINAL → DONE
```

Every state has an entry condition, a user sign-off gate, and a rejection path.
See `references/state-machine.md` for the full definition of each state.

---

## Quick Start

```
User: I want to build a [landing page / portfolio / agency site]. Run Web Claw.
Agent: (reads SKILL.md -> checks for memory.md -> runs ignition -> produces discovery.md)
Agent: (sitemap -> style guide -> wireframes -> animations, sign-off after each)
Agent: (Awwwards + YouTube research -> stack -> plan.md + phase files)
Agent: (builds phase 1 -> QA gate -> phase 2 -> QA gate -> phase 3 -> launch gate)
```

---

## Two run modes: interactive vs fast-path

Web Claw runs in one of two modes, recorded in `memory.md -> Mode`.

| Mode          | Sign-off between states  | QA gates between phases | When to use                                                            |
|---------------|--------------------------|-------------------------|------------------------------------------------------------------------|
| `interactive` | YES (user approves each) | YES                     | Default. Multi-session work. User wants to steer at every artifact.    |
| `fast`        | NO (auto-approve)        | YES (HARD; no override) | Single-turn builds, demos, batch generation. User can't be interrupted.|

**Fast-path is not "skip QA".** Fast-path skips *human-in-the-loop* sign-off between states. It does NOT skip Lighthouse, axe-core, contrast checks, reduced-motion verification, or any other automated gate. The hard floor stays.

### How fast-path works

1. **At ignition, the agent picks mode** from explicit user signal:
   - User says "run it end-to-end" / "build the whole thing" / "fast mode" / "no need to check in" -> `fast`.
   - Default if no signal -> `interactive`.
   - Mode is written to `memory.md -> Mode`.

2. **In `fast` mode, every state's sign-off becomes implicit-approve**:
   - The agent writes the artifact, marks `User sign-off: AUTO`, and advances.
   - Decisions that would normally be user-presented (color palette, motion intensity overrides, signature device) are made by the agent and **logged to `decisions/NNN-auto-*.md`** with the rationale.
   - The agent never asks a question. It picks defaults from `discovery.md` and the operating principles, and documents the choice.

3. **Automated quality gates remain mandatory**:
   - `qa/phase-N-gate.md` runs after each phase build.
   - `scripts/audit-perf.py`, `scripts/check-a11y.py` run on the deployed preview.
   - If a gate fails, the agent does NOT advance — it loops on the Implementer Agent to fix, then re-runs the gate. (Same as interactive mode.)

4. **At completion, the user gets one consolidated review**:
   - All artifacts, every auto-decision, the QA evidence package, and the preview URL.
   - User can then accept, edit specific artifacts, or override decisions retroactively.

5. **Switching modes mid-project**: Edit `memory.md -> Mode` manually, or run `python scripts/update-memory.py memory.md --mode <fast|interactive>`. Switching back to `interactive` after fast-path means the next state will pause for sign-off again.

### What `fast` mode requires of the user

- All required answers present in the initial prompt OR enough context to defensibly assume defaults.
- Acceptance that `decisions/NNN-auto-*.md` records every judgment call.
- Acceptance that the QA gates still hold (Lighthouse < 90 still blocks).

### What `fast` mode does NOT do

- Does not skip Lighthouse, axe-core, contrast validation, or reduced-motion testing.
- Does not bypass `qa/phase-N-gate.md` blockers.
- Does not assume a stack the user explicitly declined.
- Does not invent answers to security or compliance questions.

If the agent hits a true blocker that defaults can't resolve (e.g., "we need to know if you're collecting PII before wiring forms"), it adds the question to `memory.md -> Blockers` and continues with everything else, surfacing the blocker at completion review.

---

## Reference Index — Load On Demand

Load only what the current phase needs. **Never load all references at once.**

| When to load | File |
|-------------|------|
| Session start, always | `references/memory-format.md` — memory schema, decisions format, compaction |
| Pipeline decisions, taste debates | `references/operating-principles.md` — 12 core principles |
| All states + rejection paths | `references/state-machine.md` — full state machine |
| Subagent spawning, platform choice | `references/agent-handoff-protocol.md` — minimal handoff, output contract |
| Companion skill orchestration | `references/extension-orchestration.md` — optional sibling skill routing for Taste, Impeccable, UI-UX Pro Max, Stitch, and motion tooling. |
| Claude Code / Codex / Antigravity / Manual | `references/platform-compat.md` — platform-specific invocation |
| Simple project ignition | `references/ignition-quick.md` — 7-question fast intake |
| Complex project ignition | `references/ignition-full.md` — 17-question full intake |
| BLUEPRINT:SITEMAP | `agents/ux-strategy-agent.md` + `references/relume-methodology.md` |
| BLUEPRINT:STYLE-GUIDE | `agents/designer-agent.md` + `references/color-theory.md` + `references/typography-systems.md` |
| BLUEPRINT:WIREFRAMES | `agents/ui-strategy-agent.md` + `references/pattern-library.md` (Layer 2) |
| BLUEPRINT:ANIMATIONS | `agents/animator-agent.md` + `references/animation-libraries.md` + `references/pattern-library.md` (all layers) |
| RESEARCH:AWWWARDS | `agents/researcher-agent.md` + `references/pattern-library.md` (Layer 2 + Layer 4 vibe matrix) |
| RESEARCH:YOUTUBE | `agents/researcher-agent.md` + `references/youtube-channels.md` |
| EXECUTION:STACK | `agents/implementer-agent.md` + `references/tech-stack.md` + `references/performance-budgets.md` |
| EXECUTION:PHASE-N | `agents/implementer-agent.md` + `phase-N.md` |
| After each phase build | `qa/phase-N-gate.md` (phase-1-gate, phase-2-gate, or phase-3-gate) |
| QA:FINAL | `agents/qa-agent.md` + `qa/pre-launch-checklist.md` |
| Visual quality scoring (Phase 2, Phase 3, pre-launch) | `qa/visual-critique-rubric.md` |
| Detailed a11y issues | `references/accessibility.md` + `qa/accessibility-checklist.md` |
| Detailed perf issues | `references/performance-budgets.md` + `qa/performance-checklist.md` |
| Numeric thresholds (Lighthouse, CWV, contrast, motion, bundle, research) | `references/budgets.yaml` (canonical, machine-readable) |
| Security failures | `qa/security-checklist.md` |
| Cross-browser failures | `qa/cross-browser-checklist.md` |
| End-of-project handoff to another team or agent | `references/handoff-export.md` (use `scripts/export-handoff.py` to package) |

---

## Scripts

| Script | When to run |
|--------|------------|
| `scripts/init-project.py` | Once per project at IGNITION — creates memory.md, decisions/, site-brief.json, dependencies.json |
| `scripts/generate-phases.py` | After plan.md is approved — generates phase-1/2/3.md + prompts/sequential-prompts.md |
| `scripts/check-output.py` | Anytime — validates required deliverables exist and are non-empty; use `--phase all` at launch |
| `scripts/update-memory.py` | Update memory.md fields from the command line without rewriting the file |
| `scripts/compact-context.py` | When context is near its limit — writes a compaction snapshot to memory.md |
| `scripts/research-matrix.py` | After sources.json is populated — converts it to research/research-matrix.md |
| `scripts/install-deps.py` | After tech-stack.md is approved — reads install commands from the file |
| `scripts/install-packages.py` | Install specific packages by name — auto-detects npm/pnpm/yarn/bun |
| `scripts/audit-perf.py` | At each QA gate — Lighthouse performance check; gates against `budgets.yaml -> lighthouse.*` and exits 3 on miss |
| `scripts/check-a11y.py` | At each QA gate — axe-core / pa11y accessibility check; gates against `budgets.yaml -> accessibility.*` |
| `scripts/check-contrast.py` | At Phase 1 gate (and any time tokens change) — WCAG contrast validator over style-guide pairs |
| `scripts/check-bundle.py` | At Phase 1 gate and after every build — bundle size analyzer; gates against `budgets.yaml -> bundle.*` |
| `scripts/check-reduced-motion.py` | At Phase 2 gate — verifies reduced-motion media query is honored on the deployed preview |
| `scripts/run-playwright.py` | At Phase 2 / Phase 3 gates — E2E smoke (routes load, console clean, primary CTA reachable) |
| `scripts/visual-regression.py` | At Phase 3 gate and pre-launch — captures screenshots, diffs against approved baseline |
| `scripts/generate-og.py` | During Phase 3 — generates 1200x630 OG images per page from style-guide tokens |
| `scripts/export-handoff.py` | At DONE — packages the project as a tarball / JSON / markdown bundle for receiver agents |
| `scripts/scrape-awwwards.py` | During RESEARCH:AWWWARDS |
| `scripts/extract-tokens.py` | After style-guide.md is approved — extracts CSS custom properties |

---

## What "Done" Looks Like

- [ ] All blueprint artifacts in `<project>/blueprint/` with user sign-off
- [ ] Research dossier in `<project>/research/`
- [ ] `plan.md` + three `phase-*.md` files at project root
- [ ] All three phases built, deployed (preview minimum), QA gates passed
- [ ] Lighthouse mobile floors met per `references/budgets.yaml -> lighthouse.mobile.*`
- [ ] Visual critique rubric passes (`qa/visual-critique-rubric.md`: median ≥ 4, min ≥ 3)
- [ ] axe-core, contrast, reduced-motion, bundle, and Playwright smoke scripts all exit 0
- [ ] Site works with `prefers-reduced-motion: reduce`, JS disabled (content), keyboard-only
- [ ] `memory.md → Phase: DONE` (set only when QA:FINAL exits, not when Phase 3 finishes)

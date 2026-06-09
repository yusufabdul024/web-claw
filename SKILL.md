---
name: web-claw
description: |
  Research-first web design workflow for planning, designing, and building
  scroll-stopping premium websites with AI coding agents. Use when the user
  asks for website design, landing pages, moodboards, inspiration research,
  wireframes, motion design, or implementation with visual QA.
---

# Web Claw v2 - Research-First Websites With Taste

Web Claw v2 is a structured methodology for designing and shipping scroll-stopping websites without pretending the agent can invent taste in isolation.

The core change from v1 is simple: **research and taste calibration happen before blueprinting**. The agent studies the user's references, builds a moodboard from open-web inspiration, consults companion design skills when available, and collaborates with the user on direction before it commits to sitemap, style, wireframes, motion, stack, or code.

Web Claw does not require Awwwards, YouTube, Dribbble, Pinterest, Instagram, Behance, or any single source. It uses whatever evidence best fits the project, with this hierarchy:

1. **User-provided inspiration** - links, screenshots, reels, carousels, portfolios, products, designers, brands, and "I like this part" notes.
2. **Open-web moodboard research** - design galleries, portfolios, moodboard platforms, social design posts, product sites, and pattern references.
3. **Companion design skills** - local or discoverable skills such as Taste Skill, UI-UX Pro Max, Impeccable, Stitch, and similar design critique/polish systems.
4. **Web Claw built-in references** - used as fallback structure, not as a substitute for taste evidence.

---

## Mandatory First Read / Last Write Protocol

**Every session. No exceptions.**

### First Read

1. Check if `<project>/memory.md` exists.
   - If yes: read it, then read pinned decisions, then read the Last artifact.
   - If no: run `scripts/init-project.py "<project-name>" --path <workspace> [--mode interactive|fast]`.
2. Read `Mode` and `Phase`.
3. If `User sign-off: PENDING`, re-present the last artifact and do not advance.
4. If `User sign-off: AUTO` in fast mode, continue to the recorded Next action.
5. Execute `Next action` exactly as written.

### Last Write

1. Update `memory.md`: Phase, Step, Last artifact, User sign-off, Next action.
2. If a significant decision was made, create `decisions/NNN-topic.md`.
3. If context is near its limit, write the Compaction Snapshot into `memory.md`.

See `references/memory-format.md` for schema, decision records, and compaction protocol.

---

## The Pipeline

```
IGNITION ->
RESEARCH:SKILL-DISCOVERY ->
RESEARCH:INSPIRATION-INTAKE ->
RESEARCH:OPEN-WEB ->
RESEARCH:MOODBOARD ->
TASTE:CALIBRATION ->
BLUEPRINT:SITEMAP ->
BLUEPRINT:STYLE-GUIDE ->
BLUEPRINT:WIREFRAMES ->
BLUEPRINT:ANIMATIONS ->
EXECUTION:STACK ->
EXECUTION:PLAN ->
EXECUTION:PHASE-1 ->
EXECUTION:PHASE-2 ->
EXECUTION:PHASE-3 ->
QA:FINAL ->
DONE
```

Every state has an entry condition, an exit condition, and a rejection path. See `references/state-machine.md`.

---

## Quick Start

```text
User: Build a scroll-stopping site for my studio. I like these three links.
Agent: reads SKILL.md -> initializes memory -> captures discovery and inspiration notes
Agent: discovers companion skills -> researches references -> builds moodboard
Agent: presents taste calibration -> user chooses direction
Agent: creates sitemap -> style guide -> wireframes -> animations
Agent: picks stack -> writes plan and phase files -> builds through QA gates
```

If the user has no references yet, Web Claw helps them get them:

```text
"I do not have enough taste evidence yet. Please send 3-7 references. They can be websites, Dribbble shots, Pinterest boards, Instagram posts/reels, Behance projects, product pages, or screenshots. For each, tell me what you like: layout, color, motion, typography, mood, or one specific section."
```

In fast mode, the agent can proceed with open-web research, but it must mark weak or unavailable inspiration as a blocker and surface it in the completion review.

---

## Two Run Modes

| Mode | Human sign-off | QA gates | Use when |
|------|----------------|----------|----------|
| `interactive` | Required at each taste/blueprint/build gate | Hard | The user wants to shape direction and taste. Default. |
| `fast` | Auto-approved with decision logs | Hard | Demos and unattended drafts where the agent may choose defaults. |

Fast mode does **not** skip research, moodboarding, contrast, Lighthouse, accessibility, bundle, reduced-motion, visual critique, or Playwright gates. It only skips live user approval between artifacts.

Fast mode must still:

- Prefer user-provided sources if present.
- Search the open web when sources are missing.
- Log every taste decision in `decisions/NNN-auto-*.md`.
- Mark unresolved user-only taste gaps in `memory.md -> Blockers`.
- Surface weak evidence at completion.

---

## Reference Index - Load On Demand

Load only what the current phase needs. Never load every reference at once.

| When to load | File |
|-------------|------|
| Session start | `references/memory-format.md` |
| Pipeline decisions | `references/operating-principles.md` |
| State transitions | `references/state-machine.md` |
| Agent handoff | `references/agent-handoff-protocol.md` |
| Companion skill discovery | `references/extension-orchestration.md` |
| Platform usage | `references/platform-compat.md` |
| Ignition | `references/ignition-quick.md` or `references/ignition-full.md` |
| Inspiration research | `agents/researcher-agent.md` + `references/inspiration-research.md` |
| Moodboard creation | `agents/researcher-agent.md` + `references/moodboard-library.md` |
| Taste calibration | `agents/designer-agent.md` + `research/moodboard.md` + `research/skill-discovery.md` |
| BLUEPRINT:SITEMAP | `agents/ux-strategy-agent.md` + `references/relume-methodology.md` + `research/taste-calibration.md` |
| BLUEPRINT:STYLE-GUIDE | `agents/designer-agent.md` + `references/color-theory.md` + `references/typography-systems.md` + `research/moodboard.md` |
| BLUEPRINT:WIREFRAMES | `agents/ui-strategy-agent.md` + `references/pattern-library.md` + `research/taste-calibration.md` |
| BLUEPRINT:ANIMATIONS | `agents/animator-agent.md` + `references/animation-libraries.md` + `references/pattern-library.md` + `research/inspiration-sources.md` |
| EXECUTION:STACK | `agents/implementer-agent.md` + `references/tech-stack.md` + `references/performance-budgets.md` |
| EXECUTION:PHASE-N | `agents/implementer-agent.md` + `phase-N.md` |
| Phase QA | `qa/phase-N-gate.md` |
| Final QA | `agents/qa-agent.md` + `qa/pre-launch-checklist.md` |
| Numeric thresholds | `references/budgets.yaml` |

---

## Scripts

| Script | When to run |
|--------|-------------|
| `scripts/init-project.py` | Initialize a Web Claw project workspace. |
| `scripts/research-matrix.py` | Convert `sources.json` into a source-agnostic research matrix. |
| `scripts/generate-phases.py` | Generate phase files after `plan.md` is approved. |
| `scripts/check-output.py` | Validate required deliverables exist and are non-empty. |
| `scripts/update-memory.py` | Update memory fields from CLI. |
| `scripts/compact-context.py` | Write compaction snapshot. |
| `scripts/install-deps.py` | Run install commands from `tech-stack.md`. |
| `scripts/install-packages.py` | Install named packages via detected package manager. |
| `scripts/audit-perf.py` | Lighthouse and lab metrics gate. |
| `scripts/check-a11y.py` | pa11y accessibility gate. |
| `scripts/check-contrast.py` | WCAG contrast gate. |
| `scripts/check-bundle.py` | Build-output bundle smoke gate. |
| `scripts/check-reduced-motion.py` | Reduced-motion behavior gate. |
| `scripts/run-playwright.py` | Browser smoke tests. |
| `scripts/visual-regression.py` | Screenshot baseline/diff. |
| `scripts/generate-og.py` | Generate Open Graph images. |
| `scripts/export-handoff.py` | Package project state for handoff. |
| `scripts/extract-tokens.py` | Extract tokens from style guide. |
| `scripts/scrape-awwwards.py` | Optional legacy gallery scraper; not part of the v2 required path. |

---

## What Done Looks Like

- [ ] `research/skill-discovery.md` exists and records available companion skills or fallbacks.
- [ ] `research/inspiration-sources.md` exists with user-provided and/or open-web sources.
- [ ] `research/moodboard.md` exists with visual, typography, layout, motion, and anti-style evidence.
- [ ] `research/taste-calibration.md` is signed off or auto-approved with decision logs.
- [ ] Blueprint artifacts exist and follow the calibrated taste direction.
- [ ] `plan.md` and phase files exist and are stack-specific.
- [ ] All phases are built, deployed to preview, and QA-gated.
- [ ] Lighthouse, accessibility, contrast, reduced-motion, bundle, visual critique, and Playwright gates pass.
- [ ] Site works with reduced motion, keyboard-only navigation, and content visible without JavaScript where feasible.
- [ ] `memory.md -> Phase: DONE` is set only after QA:FINAL passes.

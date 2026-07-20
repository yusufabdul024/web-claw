---
name: web-claw
description: |
  Studio-workflow skill for planning, designing, and building scroll-stopping,
  award-winning premium websites with AI coding agents. Runs a full Brief ->
  Research -> Design -> Build pipeline as an expert Chief Designer. Use when
  the user wants to build a website, design a landing page, portfolio, agency
  site, SaaS or product-launch site, brand site, or asks for an Awwwards-quality,
  animated, storytelling, or "$10k" website; also for client briefs, competitor
  analysis, moodboards, inspiration research, sitemaps, wireframes, style guides,
  design systems, 3D scroll animations, micro-interactions, motion design, or
  phased implementation with visual QA. Lean toward triggering whenever the
  surface intent is "a website with taste."
---

# Web Claw v3 - The Studio Workflow

Web Claw v3 runs a real design studio's workflow through AI coding agents, in four parts:

```text
1. BRIEF     - interview the client until the value proposition passes the 3-second test
2. RESEARCH  - competitors, inspiration, moodboard, taste calibration; verified with the client
3. DESIGN    - sitemap, branding/style guide, wireframes, motion design
4. BUILD     - phased, test-driven implementation with client checkpoints and hard QA gates
```

The agent does not run this as a generic assistant. It runs it as the **Chief Designer** — an award-winning, animated-storytelling web developer who directs Web Claw's specialist agents as a studio team.

Evidence hierarchy for every taste decision:

1. **User-provided inspiration** - links, screenshots, reels, carousels, portfolios, products, designers, brands, and "I like this part" notes.
2. **Real shipped websites** - award-winning sites (Awwwards and similar), international studio/agency portfolios and their client work, strong product and brand sites.
3. **Open-web galleries and social design posts** - Dribbble, Pinterest, Behance, Land-book, Godly, Siteinspire, Mobbin, and similar pattern references.
4. **Companion skills and MCP servers** - UI-UX Pro Max, Taste Skill, GSAP Master, Motion/Framer, Vercel React Best Practices, shadcn/ui MCP, 21st.dev Magic MCP, Convex, Impeccable, Stitch — per the registry in `references/extension-orchestration.md`.
5. **Web Claw built-in references** - fallback structure, never a substitute for taste evidence.

---

## Mandatory First Read / Last Write Protocol

**Every session. No exceptions.**

### First Read

0. **Adopt the identity.** Read `agents/chief-designer.md` and operate as the Chief Designer before anything else — before reading other files, before answering the user.
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

```text
PART 1 - BRIEF      BRIEF:INTERVIEW
PART 2 - RESEARCH   RESEARCH:SKILL-DISCOVERY -> RESEARCH:COMPETITORS ->
                    RESEARCH:OPEN-WEB -> RESEARCH:INSPIRATION-INTAKE ->
                    RESEARCH:MOODBOARD -> RESEARCH:TASTE-CALIBRATION
PART 3 - DESIGN     DESIGN:SITEMAP -> DESIGN:STYLE-GUIDE ->
                    DESIGN:WIREFRAMES -> DESIGN:ANIMATIONS
PART 4 - BUILD      BUILD:STACK -> BUILD:PLAN -> BUILD:PHASE-1 ->
                    BUILD:PHASE-2 -> BUILD:PHASE-3 -> BUILD:QA-FINAL -> DONE
```

Every state has an entry condition, an exit condition, and a rejection path. See `references/state-machine.md`.

The research part is a client loop, not a line: interview → research → verify facts with the client → deeper research → report → sign-off, repeating until there is a clear way forward (`references/client-collaboration.md`).

---

## Quick Start

```text
User: Build a scroll-stopping site for my studio. I like these three links.
Agent: adopts Chief Designer identity -> initializes memory -> interviews for the brief
Agent: value proposition passes the 3-second test -> client confirms brief
Agent: discovers companion skills -> competitor analysis (verified with client) ->
       open-web research matrix -> curates inspiration sources -> moodboard ->
       taste calibration -> client picks direction
Agent: sitemap -> style guide -> wireframes -> motion design, sign-off after each
Agent: picks stack -> plan + phase files -> builds test-first through QA gates,
       showing signature sections the moment they work
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
| `interactive` | Required at each brief/research/design/build gate | Hard | The user wants to shape direction and taste. Default. |
| `fast` | Auto-approved with decision logs | Hard | Demos and unattended drafts where the agent may choose defaults. |

Fast mode does **not** skip the brief, competitor analysis, research, moodboarding, contrast, Lighthouse, accessibility, bundle, reduced-motion, visual critique, or Playwright gates. It only skips live user approval between artifacts.

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
| Session start, before anything | `agents/chief-designer.md` — identity primer |
| Session start | `references/memory-format.md` |
| Pipeline decisions, taste debates | `references/operating-principles.md` |
| State transitions | `references/state-machine.md` |
| Any client-facing moment | `references/client-collaboration.md` |
| Agent handoff / subagent spawning | `references/agent-handoff-protocol.md` |
| Companion skill discovery | `references/extension-orchestration.md` |
| Platform usage (Claude Code / Codex / Gemini / Cursor) | `references/platform-compat.md` |
| BRIEF:INTERVIEW | `references/ignition-quick.md` or `references/ignition-full.md` + `assets/templates/client-brief-template.md` |
| RESEARCH:COMPETITORS | `agents/researcher-agent.md` + `references/competitor-analysis.md` |
| RESEARCH:OPEN-WEB (research matrix) | `agents/researcher-agent.md` + `references/inspiration-research.md` |
| RESEARCH:INSPIRATION-INTAKE (curation) | `agents/researcher-agent.md` + `references/inspiration-research.md` + `research/research-matrix.md` |
| Video technique research (optional) | `references/youtube-channels.md` |
| Moodboard creation | `agents/researcher-agent.md` + `references/moodboard-library.md` + `assets/templates/moodboard-template.md` |
| Taste calibration | `agents/designer-agent.md` + `research/moodboard.md` + `research/skill-discovery.md` + `assets/templates/taste-calibration-template.md` |
| DESIGN:SITEMAP | `agents/ux-strategy-agent.md` + `references/relume-methodology.md` + `research/taste-calibration.md` |
| DESIGN:STYLE-GUIDE | `agents/designer-agent.md` + `references/color-theory.md` + `references/typography-systems.md` + `references/design-systems.md` + `research/moodboard.md` |
| DESIGN:WIREFRAMES | `agents/ui-strategy-agent.md` + `references/pattern-library.md` + `research/taste-calibration.md` |
| DESIGN:ANIMATIONS | `agents/animator-agent.md` + `references/animation-libraries.md` + `references/pattern-library.md` + `references/premium-experience-standard.md` |
| The feel bar for design + build + QA | `references/premium-experience-standard.md` |
| BUILD:STACK | `agents/implementer-agent.md` + `references/tech-stack.md` + `references/performance-budgets.md` |
| BUILD:PLAN | `assets/templates/plan-template.md` + `assets/templates/phase-1-template.md` / `assets/templates/phase-2-template.md` / `assets/templates/phase-3-template.md` |
| BUILD:PHASE-N | `agents/implementer-agent.md` + `phase-N.md` |
| Phase QA | `qa/phase-N-gate.md` (phase-1-gate, phase-2-gate, or phase-3-gate) |
| Final QA | `agents/qa-agent.md` + `qa/pre-launch-checklist.md` |
| Visual quality scoring (Phase 2, Phase 3, pre-launch) | `qa/visual-critique-rubric.md` |
| Detailed a11y issues | `references/accessibility.md` + `qa/accessibility-checklist.md` |
| Detailed perf issues | `references/performance-budgets.md` + `qa/performance-checklist.md` |
| Motion QA failures | `qa/motion-checklist.md` |
| Responsive QA failures | `qa/responsive-checklist.md` |
| Security failures | `qa/security-checklist.md` |
| Cross-browser failures | `qa/cross-browser-checklist.md` |
| Numeric thresholds (Lighthouse, CWV, contrast, motion, bundle, research) | `references/budgets.yaml` (canonical, machine-readable) |
| End-of-project handoff to another team or agent | `references/handoff-export.md` (use `scripts/export-handoff.py` to package) |

---

## Scripts

| Script | When to run |
|--------|-------------|
| `scripts/init-project.py` | Once per project at BRIEF:INTERVIEW — creates memory.md, brief/, research/, design/, decisions/, qa/ |
| `scripts/research-matrix.py` | Convert `sources.json` into a source-agnostic research matrix. |
| `scripts/generate-phases.py` | Generate phase files after `plan.md` is approved. |
| `scripts/check-output.py` | Validate required deliverables exist and are non-empty (`--phase all` at launch). |
| `scripts/update-memory.py` | Update memory fields from CLI. |
| `scripts/compact-context.py` | Write compaction snapshot. |
| `scripts/install-deps.py` | Run install commands from `tech-stack.md`. |
| `scripts/install-packages.py` | Install named packages via detected package manager. |
| `scripts/audit-perf.py` | Lighthouse and lab metrics gate. |
| `scripts/check-a11y.py` | pa11y accessibility gate. |
| `scripts/check-contrast.py` | WCAG contrast gate. |
| `scripts/check-bundle.py` | Build-output bundle smoke gate. |
| `scripts/check-reduced-motion.py` | Reduced-motion behavior gate. |
| `scripts/run-playwright.py` | Browser smoke tests — write assertions first, build until green. |
| `scripts/visual-regression.py` | Screenshot baseline/diff. |
| `scripts/generate-og.py` | Generate Open Graph images. |
| `scripts/export-handoff.py` | Package project state for handoff. |
| `scripts/extract-tokens.py` | Extract tokens from style guide. |
| `scripts/scrape-awwwards.py` | Optional helper during RESEARCH:OPEN-WEB for award-gallery evidence. |

---

## What Done Looks Like

- [ ] `brief/client-brief.md` exists and the value proposition passes the 3-second test.
- [ ] `research/skill-discovery.md` records available companion skills or fallbacks.
- [ ] `research/competitor-analysis.md` has a client-verified competitor set and ranked audience USPs.
- [ ] `research/research-matrix.md` exists with the open-web reference sweep.
- [ ] `research/inspiration-sources.md` exists as the curated set the moodboard was built from.
- [ ] `research/moodboard.md` has visual, typography, layout, motion, and anti-style evidence.
- [ ] `research/taste-calibration.md` is signed off or auto-approved with decision logs.
- [ ] Design artifacts exist and follow the calibrated taste direction.
- [ ] `plan.md` and phase files exist, are stack-specific, and name their client checkpoints and test assertions.
- [ ] All phases built test-first, deployed to preview, QA-gated, with signature elements approved mid-phase.
- [ ] The arrival is designed: intentional loading state, smooth reveal — no generic skeleton (`references/premium-experience-standard.md`).
- [ ] Lighthouse, accessibility, contrast, reduced-motion, bundle, visual critique, and Playwright gates pass.
- [ ] Site works with reduced motion, keyboard-only navigation, and content visible without JavaScript where feasible.
- [ ] `memory.md -> Phase: DONE` is set only after BUILD:QA-FINAL passes.

# State Machine - Web Claw v3

## Overview

Web Claw v3 mirrors a real design studio's workflow in four parts: **Brief → Research → Design → Build**. The agent runs it as the Chief Designer (`agents/chief-designer.md` — adopted before anything else) directing a team of specialist agents.

The rule that shapes everything: a designer who receives a client request does not start researching from nowhere, and does not design from nowhere. First the interview, then evidence, then a signed-off direction, then design, then an iterative build with the client in the loop.

The current state is always recorded in `memory.md -> Phase`. The agent must not advance until the state's exit condition is satisfied.

## Mode-Aware Sign-Off

| Mode | Sign-off behavior |
|------|-------------------|
| `interactive` | Present the artifact, ask the state's concrete question, wait for user approval or requested changes. |
| `fast` | Auto-approve, create decision logs for all judgment calls, keep automated QA gates hard, and surface weak/blocked evidence at the end. |

Automated QA gates are always hard. Client-loop details per mode: `references/client-collaboration.md`.

## State Diagram

```text
PART 1 - BRIEF
  BRIEF:INTERVIEW

PART 2 - RESEARCH
  -> RESEARCH:SKILL-DISCOVERY
  -> RESEARCH:INSPIRATION-INTAKE
  -> RESEARCH:COMPETITORS
  -> RESEARCH:OPEN-WEB
  -> RESEARCH:MOODBOARD
  -> RESEARCH:TASTE-CALIBRATION

PART 3 - DESIGN
  -> DESIGN:SITEMAP
  -> DESIGN:STYLE-GUIDE
  -> DESIGN:WIREFRAMES
  -> DESIGN:ANIMATIONS

PART 4 - BUILD
  -> BUILD:STACK
  -> BUILD:PLAN
  -> BUILD:PHASE-1
  -> BUILD:PHASE-2
  -> BUILD:PHASE-3
  -> BUILD:QA-FINAL
  -> DONE
```

## Core Rules

1. **Brief before research.** No research until the client interview has produced a value proposition that passes the 3-second test.
2. **Research before design.** `DESIGN:SITEMAP` is blocked until these exist: `research/skill-discovery.md`, `research/inspiration-sources.md`, `research/competitor-analysis.md`, `research/moodboard.md`, `research/taste-calibration.md`.
3. **Research is a loop, not a line.** The Research part cycles interview → research → verify with client → deeper research → report → sign-off until the way forward is clear.
4. **Build is iterative.** Every phase deploys a preview; signature elements are shown to the client the moment they first work. No big-bang reveal.

---

# Part 1 — Brief

### BRIEF:INTERVIEW

**Entry condition:** User requested a website and no initialized Web Claw project exists.

**What happens:**

1. Adopt the Chief Designer identity (`agents/chief-designer.md`) if not already adopted.
2. Run `scripts/init-project.py "<project-name>" --path <workspace> [--mode interactive|fast]`.
3. Interview the client per `references/client-collaboration.md` — the five core questions: what the brand is about, what the site must achieve, what the visitor must do, the one objective, and the value proposition that becomes the hero headline.
4. Load `references/ignition-quick.md` (simple) or `references/ignition-full.md` (complex) for the full question set.
5. Capture any inspiration links, screenshots, designers, brands, posts, reels, boards, or "I like this" notes already provided.
6. Write `brief/client-brief.md` from `assets/templates/client-brief-template.md`.
7. Test the value proposition against the 3-second test. Push back until it passes.
8. Update `memory.md`: Phase = `RESEARCH:SKILL-DISCOVERY`.

**Exit condition:** `brief/client-brief.md` exists, the value proposition passes the 3-second test, and the client has confirmed the brief (or fast mode has logged assumptions).

**Rejection path:** Client corrects the brief -> update -> re-present -> advance only when confirmed.

---

# Part 2 — Research

### RESEARCH:SKILL-DISCOVERY

**Entry condition:** `brief/client-brief.md` exists.

**What happens:**

1. Load `references/extension-orchestration.md` (the Known Companion Registry).
2. Inspect sibling skill folders around Web Claw's own directory and the host's readable skill roots.
3. Detect known companion skills per the registry: UI-UX Pro Max, Taste Skill, GSAP Master, Motion/Framer, Vercel React Best Practices, Convex Create Component, Vercel React Native, Impeccable, Stitch — and any other design/UX/frontend skill folders with a readable `SKILL.md`, manifest, or README.
4. Detect MCP companions (shadcn/ui MCP, 21st.dev Magic MCP) by checking the host's available tool list — never assume an unconnected server's tools exist.
5. If a requested or useful companion is missing locally, search the open web or GitHub for public documentation/repo references when tools allow it. Do not install or configure without user consent.
6. Produce `research/skill-discovery.md`: available local skills and MCP servers, unavailable but relevant ones, how each will be consulted, conditional entries (backend/native) left unrouted unless the brief activates them, fallback if unavailable, and install/request guidance for the user.

**Exit condition:** `research/skill-discovery.md` exists.

**Rejection path:** If the user says a skill is not allowed, record it in `decisions/NNN-skill-boundary.md` and remove it from routing.

---

### RESEARCH:INSPIRATION-INTAKE

**Entry condition:** Skill discovery complete.

**What happens:**

1. Extract every user-provided inspiration source from the prompt and the brief.
2. Ask for missing sources if the project has weak taste evidence and mode is interactive.
3. Accept broad source types: real shipped websites, award-winning sites, agency portfolio pieces, competitor-adjacent sites, Dribbble shots, Pinterest boards, Behance projects, Instagram posts/reels/carousels, TikTok videos, YouTube videos, screenshots, PDFs, Figma links, product pages, brand guidelines, and moodboard links.
4. For each source, capture what the user likes: color, typography, layout, motion, density, imagery, tone, one section, one interaction, or one feeling.
5. Write or update `sources.json`. Produce `research/inspiration-sources.md`.

**Exit condition:** `research/inspiration-sources.md` exists with either:

- at least 3 user-provided sources, or
- a clear note that the user has no sources yet plus the open-web research plan.

**Rejection path:** User says a source is wrong -> remove or reclassify it; document what not to copy.

---

### RESEARCH:COMPETITORS

**Entry condition:** Inspiration intake complete.

**What happens:**

1. Load `agents/researcher-agent.md` + `references/competitor-analysis.md`.
2. Build the competitor set (direct / adjacent / aspirational) and **verify it with the client** before auditing.
3. Audit each competitor: value proposition, primary action, IA, visual language, motion, strengths, weaknesses. Log evidence in `sources.json`.
4. Conclude: positioning gap, experience gap, ranked target-audience USPs, anti-style entries.
5. Pressure-test the brief's value proposition against the field; flag collisions to the client.
6. Produce `research/competitor-analysis.md`. Report findings to the client and get confirmation of the conclusions.

**Exit condition:** `research/competitor-analysis.md` exists with a client-verified competitor set and USP conclusions (fast mode: assumptions logged in `decisions/`).

**Rejection path:** Client rejects the competitor set or conclusions -> re-verify facts, re-audit only what changed.

---

### RESEARCH:OPEN-WEB

**Entry condition:** Competitor analysis complete.

**What happens:**

1. Load `agents/researcher-agent.md` + `references/inspiration-research.md`.
2. Research references that match the brief, the confirmed USPs, and the user-provided inspiration. Prioritize **real shipped websites**: award-winning sites (Awwwards and similar), international studio/agency portfolios and the client work inside them, and strong product/brand sites — supported by galleries (Dribbble, Behance, Pinterest, Are.na, Cosmos, Land-book, Lapa Ninja, Godly, Siteinspire, Mobbin, Codrops) for pattern evidence.
3. Do not make any source mandatory. Do not cite inaccessible/auth-gated content unless the user provided it.
4. For every source, record: URL or user-provided artifact path, why it fits, what to take, what not to take, copying risk, applicable page/section, practical build implications.
5. Update `sources.json`. Run `scripts/research-matrix.py --sources <project>/sources.json --output <project>/research/research-matrix.md` when sources are structured.

**Exit condition:** `research/research-matrix.md` exists OR `research/inspiration-sources.md` has a manually written research table with at least 6 usable references across visual/layout/motion/content.

**Rejection path:** If research is thin, ask the user for more links using the Inspiration Escalation Protocol in `references/inspiration-research.md`.

---

### RESEARCH:MOODBOARD

**Entry condition:** Open-web research complete.

**What happens:**

1. Load `references/moodboard-library.md`.
2. Produce `research/moodboard.md` from `assets/templates/moodboard-template.md`.
3. Organize evidence into taste lanes: visual mood, color/material, typography, layout/composition, imagery/asset direction, motion/interaction, copy voice, anti-style (seeded from competitor analysis).
4. Include 2-4 possible creative directions when evidence supports multiple paths.
5. For every direction, list "borrow", "avoid", "implementation cost", and "confidence".
6. Report to the client: present the moodboard as evidence, not homework.

**Exit condition:** `research/moodboard.md` exists and contains at least one coherent direction with evidence.

**Rejection path:** User rejects the moodboard -> ask what feels wrong: color, type, motion, density, imagery, or overall vibe. Re-research only that axis.

---

### RESEARCH:TASTE-CALIBRATION

**Entry condition:** Moodboard exists.

**What happens:**

1. Load `agents/designer-agent.md`, `research/moodboard.md`, and `research/skill-discovery.md`.
2. Consult available companion skills per `references/extension-orchestration.md`. Distill their advice into Web Claw artifacts; raw dumps are not canonical.
3. Produce `research/taste-calibration.md` from `assets/templates/taste-calibration-template.md`: chosen direction, rejected directions, target audience + ranked USPs (from competitor analysis), signature device candidate, visual language, motion ambition, asset strategy, anti-style, known risks.
4. This is the **clear way forward** the research loop was building toward — the plan the whole Design part is built from.
5. Present to the client. Ask: **"Which direction feels most like the site you would be proud to share: A, B, or a blend? What must not change?"**

**Exit condition:** `research/taste-calibration.md` exists and is signed off, or fast mode auto-approves with a decision record.

**Rejection path:** User rejects direction -> return to `RESEARCH:MOODBOARD` and revise the moodboard axis that failed.

---

# Part 3 — Design

### DESIGN:SITEMAP

**Entry condition:** Taste calibration signed off (Core Rule 2 satisfied).

**What happens:**

1. Load `agents/ux-strategy-agent.md`, `references/relume-methodology.md`, and `research/taste-calibration.md`.
2. Produce `design/sitemap.md` from `assets/templates/sitemap-template.md`. Every page gets one job; the section order follows the emotional arc in `references/premium-experience-standard.md -> The Emotional Journey`.
3. Present the sitemap. Ask: **"If we had to cut one page or one section to make the site sharper, what would go?"**

**Exit condition:** `design/sitemap.md` exists and is signed off.

**Rejection path:** Revise page/section strategy and document cuts.

---

### DESIGN:STYLE-GUIDE

**Entry condition:** Sitemap signed off.

**What happens:**

1. Load `agents/designer-agent.md`, `references/color-theory.md`, `references/typography-systems.md`, `references/design-systems.md`, `research/moodboard.md`, and `research/taste-calibration.md`.
2. Produce `design/style-guide.md` from `assets/templates/style-guide-template.md`: color, typography (display personality + body discipline), materials, shadow/depth system, spacing, and design tokens. Gather or specify the visual assets (imagery, video, 3D) the direction demands.
3. Run contrast validation (`scripts/check-contrast.py`).
4. Present palette/type/material direction. Ask: **"Does this still match the moodboard direction we chose? Which token feels off?"**

**Exit condition:** `design/style-guide.md` exists, contrast checks pass, and user signs off.

**Rejection path:** Revise only the failed axis where possible.

---

### DESIGN:WIREFRAMES

**Entry condition:** Sitemap and style guide signed off.

**What happens:**

1. Load `agents/ui-strategy-agent.md`, `references/pattern-library.md`, `research/taste-calibration.md`, and the signed-off style guide.
2. Produce `design/wireframes.md` from `assets/templates/wireframes-template.md` — where every element sits on every page.
3. Mark one signature section per page. Place depth, layering, and whitespace intent per `references/premium-experience-standard.md`.
4. Present. Ask: **"Which signature section feels like the right place to spend our attention?"**

**Exit condition:** `design/wireframes.md` exists and is signed off.

**Rejection path:** Rewireframe only the page/section that failed.

---

### DESIGN:ANIMATIONS

**Entry condition:** Wireframes signed off.

**What happens:**

1. Load `agents/animator-agent.md`, `references/animation-libraries.md`, `references/pattern-library.md`, `references/premium-experience-standard.md`, `research/inspiration-sources.md`, and `research/taste-calibration.md`.
2. Produce `design/animations.md` from `assets/templates/animations-template.md`, covering the full arrival-to-exit experience: the designed loading state, reveal choreography, scroll effects, mask reveals, micro-interactions, and the focal storytelling element if the concept supports one.
3. Every signature animation must reference the source or moodboard evidence it adapts from.
4. Every animation must have a reduced-motion replacement.
5. Present. Ask: **"Does the motion match the moodboard: too quiet, too loud, or right?"**

**Exit condition:** `design/animations.md` exists and is signed off.

**Rejection path:** Adjust motion intensity or return to moodboard if the motion direction lacks evidence.

---

# Part 4 — Build

### BUILD:STACK

**Entry condition:** All research and design artifacts signed off.

**What happens:**

1. Load `agents/implementer-agent.md`, `references/tech-stack.md`, and `references/performance-budgets.md`.
2. Pick stack from project shape, motion needs (3D/scroll requirements in `design/animations.md`), deploy target, team preference, and budget.
3. Produce `research/tech-stack.md` with pinned versions, install commands, and rejected alternatives.
4. Present. Ask: **"Any stack or deployment constraint I missed?"**

**Exit condition:** `research/tech-stack.md` exists and is signed off.

**Rejection path:** Re-evaluate against the user constraint.

---

### BUILD:PLAN

**Entry condition:** Stack signed off.

**What happens:**

1. Produce `plan.md` from `assets/templates/plan-template.md`, then `phase-1.md`, `phase-2.md`, `phase-3.md` via `scripts/generate-phases.py` after plan approval.
2. Every phase must deploy a visible preview, end with QA gates, and name its client checkpoints — including which signature elements get shown the moment they first work.
3. Phases are test-first: each phase file lists the Playwright/E2E assertions that must pass before the phase presents.

**Exit condition:** Plan and phase files exist and are signed off.

**Rejection path:** Restructure scope and phase boundaries.

---

### BUILD:PHASE-1 / PHASE-2 / PHASE-3

**Entry condition:** The relevant phase file is signed off.

**What happens:**

1. Execute the phase file step by step, test-driven: write or update the phase's E2E/smoke assertions first (`scripts/run-playwright.py`), then build until they pass.
2. Build to `references/premium-experience-standard.md`. The designed loading state ships in the first phase that deploys a public preview — not as a Phase-3 afterthought.
3. Deploy preview.
4. **Mid-phase checkpoint:** when a signature section or high-risk element first works (hero, loader, focal scroll element), show the preview to the client and ask about that element specifically, before rolling its pattern across the site (`references/client-collaboration.md -> Build Feedback Checkpoints`).
5. Run the relevant QA gate (`qa/phase-N-gate.md`). Fix all blockers before presenting.
6. Present preview. Ask: **"What needs changing before we continue?"**

**Exit condition:** Phase built, preview live, phase tests green, QA gate passed, user signed off.

**Rejection path:** Fix failed gate or user-identified visual/behavioral issue. Do not rebuild unrelated areas. Feedback folded in mid-phase must not silently alter signed-off artifacts — log direction changes in `decisions/`.

---

### BUILD:QA-FINAL

**Entry condition:** All phases signed off.

**What happens:**

1. Load `agents/qa-agent.md` + `qa/pre-launch-checklist.md`.
2. Run final pre-launch QA, including the visual critique rubric (`qa/visual-critique-rubric.md`) scored against `references/premium-experience-standard.md`.
3. Produce `qa/final-report.md`, present results.
4. Set `memory.md -> Phase: DONE` only after pass and approval.

**Exit condition:** Final report exists, checks pass, user signs off.

**Rejection path:** Fix blocker, rerun failed check, update report.

---

### DONE

Project complete. Optional: export handoff bundle per `references/handoff-export.md` (`scripts/export-handoff.py`).

---

## Inspiration Escalation Rule

If taste evidence is too weak to produce a moodboard in interactive mode, stop and guide the user. Ask for 3-7 references, with examples:

- "Send websites you would be proud to resemble."
- "Send Dribbble/Behance/Pinterest links for layout or mood."
- "Send Instagram reels/carousels/posts from designers whose motion or composition you like."
- "Send screenshots if links are private."
- "For each source, add one sentence: what should we borrow, and what should we avoid?"

Do not fill the gap with generic Web Claw defaults unless the user explicitly chooses fast mode or says "use your judgment."

# State Machine - Web Claw v2

## Overview

Web Claw v2 is a research-first state machine. The agent must not produce sitemap, visual system, wireframes, motion spec, stack plan, or code until the project has a signed-off taste direction.

The current state is always recorded in `memory.md -> Phase`. The agent must not advance until the state's exit condition is satisfied.

## Mode-Aware Sign-Off

| Mode | Sign-off behavior |
|------|-------------------|
| `interactive` | Present the artifact, ask the state's concrete question, wait for user approval or requested changes. |
| `fast` | Auto-approve, create decision logs for all judgment calls, keep automated QA gates hard, and surface weak/blocked evidence at the end. |

Automated QA gates are always hard.

## State Diagram

```text
IGNITION
  -> RESEARCH:SKILL-DISCOVERY
  -> RESEARCH:INSPIRATION-INTAKE
  -> RESEARCH:OPEN-WEB
  -> RESEARCH:MOODBOARD
  -> TASTE:CALIBRATION
  -> BLUEPRINT:SITEMAP
  -> BLUEPRINT:STYLE-GUIDE
  -> BLUEPRINT:WIREFRAMES
  -> BLUEPRINT:ANIMATIONS
  -> EXECUTION:STACK
  -> EXECUTION:PLAN
  -> EXECUTION:PHASE-1
  -> EXECUTION:PHASE-2
  -> EXECUTION:PHASE-3
  -> QA:FINAL
  -> DONE
```

## Core Rule

Research is not a garnish after planning. Research is the beginning.

The first blueprint state, `BLUEPRINT:SITEMAP`, is blocked until these exist:

- `research/skill-discovery.md`
- `research/inspiration-sources.md`
- `research/moodboard.md`
- `research/taste-calibration.md`

If the user provided no inspiration and open-web research is weak, the agent must guide the user to provide sources before committing to a visual direction in interactive mode.

---

## State Definitions

### IGNITION

**Entry condition:** User requested a website and no initialized Web Claw project exists.

**What happens:**

1. Run `scripts/init-project.py "<project-name>" --path <workspace> [--mode interactive|fast]`.
2. Gather discovery answers from the prompt and `references/ignition-quick.md` or `references/ignition-full.md`.
3. Capture any inspiration links, screenshots, designers, brands, posts, reels, boards, or "I like this" notes already provided.
4. Write `blueprint/discovery.md`.
5. Reflect: project goal, audience, constraints, initial taste signals, and known inspiration gaps.
6. Update `memory.md`: Phase = `RESEARCH:SKILL-DISCOVERY`.

**Exit condition:** `blueprint/discovery.md` exists and the user has confirmed the brief, or fast mode has logged assumptions.

**Rejection path:** User corrects the brief -> update discovery -> reflect again -> advance only when confirmed.

---

### RESEARCH:SKILL-DISCOVERY

**Entry condition:** `blueprint/discovery.md` exists.

**What happens:**

1. Load `references/extension-orchestration.md`.
2. Inspect sibling skill folders around Web Claw's own directory.
3. Detect known companion skills: Taste Skill, Impeccable, UI-UX Pro Max, Stitch, motion tooling, and any other design/UX/frontend skill folders with a readable `SKILL.md`, manifest, or README.
4. If a requested or useful skill is missing locally, search the open web or GitHub for public documentation/repo references when tools allow it. Do not install without user consent.
5. Produce `research/skill-discovery.md` with:
   - available local skills,
   - unavailable but relevant skills,
   - how each will be consulted,
   - fallback if unavailable,
   - any install/request guidance for the user.

**Exit condition:** `research/skill-discovery.md` exists.

**Rejection path:** If the user says a skill is not allowed, record it in `decisions/NNN-skill-boundary.md` and remove it from routing.

---

### RESEARCH:INSPIRATION-INTAKE

**Entry condition:** Skill discovery complete.

**What happens:**

1. Extract every user-provided inspiration source from the prompt and discovery.
2. Ask for missing sources if the project has weak taste evidence and mode is interactive.
3. Accept broad source types: websites, competitor-adjacent sites, portfolios, Dribbble shots, Pinterest boards, Behance projects, Instagram posts/reels/carousels, TikTok videos, YouTube videos, screenshots, PDFs, Figma links, product pages, brand guidelines, and moodboard links.
4. For each source, capture what the user likes: color, typography, layout, motion, density, imagery, tone, one section, one interaction, or one feeling.
5. Write or update `sources.json`.
6. Produce `research/inspiration-sources.md`.

**Exit condition:** `research/inspiration-sources.md` exists with either:

- at least 3 user-provided sources, or
- a clear note that the user has no sources yet plus the open-web research plan.

**Rejection path:** User says a source is wrong -> remove or reclassify it; document what not to copy.

---

### RESEARCH:OPEN-WEB

**Entry condition:** Inspiration intake complete.

**What happens:**

1. Load `agents/researcher-agent.md` + `references/inspiration-research.md`.
2. Research open-web references that match the discovery and user-provided inspiration.
3. Use source-agnostic search. Possible sources include design galleries, agency portfolios, brand sites, Dribbble, Pinterest, Behance, Instagram, Are.na, Cosmos, Land-book, Lapa Ninja, Godly, Siteinspire, Mobbin, Codrops, product sites, public case studies, and award galleries when useful.
4. Do not make any source mandatory. Do not cite inaccessible/auth-gated content unless the user provided it.
5. For every source, record:
   - URL or user-provided artifact path,
   - why it fits,
   - what to take,
   - what not to take,
   - copying risk,
   - applicable page/section,
   - practical build implications.
6. Update `sources.json`.
7. Run `scripts/research-matrix.py --sources <project>/sources.json --output <project>/research/research-matrix.md` when sources are structured.

**Exit condition:** `research/research-matrix.md` exists OR `research/inspiration-sources.md` has a manually written research table with at least 6 usable references across visual/layout/motion/content.

**Rejection path:** If research is thin, ask the user for more links using the Inspiration Escalation Protocol in `references/inspiration-research.md`.

---

### RESEARCH:MOODBOARD

**Entry condition:** Open-web research complete.

**What happens:**

1. Load `references/moodboard-library.md`.
2. Produce `research/moodboard.md`.
3. Organize evidence into taste lanes:
   - visual mood,
   - color/material,
   - typography,
   - layout/composition,
   - imagery/asset direction,
   - motion/interaction,
   - copy voice,
   - anti-style.
4. Include 2-4 possible creative directions when evidence supports multiple paths.
5. For every direction, list "borrow", "avoid", "implementation cost", and "confidence".

**Exit condition:** `research/moodboard.md` exists and contains at least one coherent direction with evidence.

**Rejection path:** User rejects the moodboard -> ask what feels wrong: color, type, motion, density, imagery, or overall vibe. Re-research only that axis.

---

### TASTE:CALIBRATION

**Entry condition:** Moodboard exists.

**What happens:**

1. Load `agents/designer-agent.md`, `research/moodboard.md`, and `research/skill-discovery.md`.
2. Consult available companion skills per `references/extension-orchestration.md`.
3. Distill companion advice into Web Claw artifacts; raw dumps are not canonical.
4. Produce `research/taste-calibration.md` with:
   - chosen direction,
   - rejected directions,
   - signature device candidate,
   - visual language,
   - motion ambition,
   - asset strategy,
   - anti-style,
   - known risks.
5. Present to the user. Ask: **"Which direction feels most like the site you would be proud to share: A, B, or a blend? What must not change?"**

**Exit condition:** `research/taste-calibration.md` exists and is signed off, or fast mode auto-approves with a decision record.

**Rejection path:** User rejects direction -> return to `RESEARCH:MOODBOARD` and revise the moodboard axis that failed.

---

### BLUEPRINT:SITEMAP

**Entry condition:** Taste calibration signed off.

**What happens:**

1. Load `agents/ux-strategy-agent.md`, `references/relume-methodology.md`, and `research/taste-calibration.md`.
2. Produce `blueprint/sitemap.md` from `assets/templates/sitemap-template.md`.
3. Present the sitemap. Ask: **"If we had to cut one page or one section to make the site sharper, what would go?"**

**Exit condition:** `blueprint/sitemap.md` exists and is signed off.

**Rejection path:** Revise page/section strategy and document cuts.

---

### BLUEPRINT:STYLE-GUIDE

**Entry condition:** Sitemap signed off.

**What happens:**

1. Load `agents/designer-agent.md`, `references/color-theory.md`, `references/typography-systems.md`, `references/design-systems.md`, `research/moodboard.md`, and `research/taste-calibration.md`.
2. Produce `blueprint/style-guide.md`.
3. Run contrast validation.
4. Present palette/type/material direction. Ask: **"Does this still match the moodboard direction we chose? Which token feels off?"**

**Exit condition:** `blueprint/style-guide.md` exists, contrast checks pass, and user signs off.

**Rejection path:** Revise only the failed axis where possible.

---

### BLUEPRINT:WIREFRAMES

**Entry condition:** Sitemap and style guide signed off.

**What happens:**

1. Load `agents/ui-strategy-agent.md`, `references/pattern-library.md`, `research/taste-calibration.md`, and signed-off style guide.
2. Produce `blueprint/wireframes.md`.
3. Mark one signature section per page.
4. Present. Ask: **"Which signature section feels like the right place to spend our attention?"**

**Exit condition:** `blueprint/wireframes.md` exists and is signed off.

**Rejection path:** Rewireframe only the page/section that failed.

---

### BLUEPRINT:ANIMATIONS

**Entry condition:** Wireframes signed off.

**What happens:**

1. Load `agents/animator-agent.md`, `references/animation-libraries.md`, `references/pattern-library.md`, `research/inspiration-sources.md`, and `research/taste-calibration.md`.
2. Produce `blueprint/animations.md`.
3. Every signature animation must reference the source or moodboard evidence it adapts from.
4. Every animation must have a reduced-motion replacement.
5. Present. Ask: **"Does the motion match the moodboard: too quiet, too loud, or right?"**

**Exit condition:** `blueprint/animations.md` exists and is signed off.

**Rejection path:** Adjust motion intensity or return to moodboard if the motion direction lacks evidence.

---

### EXECUTION:STACK

**Entry condition:** All blueprint and research artifacts signed off.

**What happens:**

1. Load `agents/implementer-agent.md`, `references/tech-stack.md`, and `references/performance-budgets.md`.
2. Pick stack from project shape, motion needs, deploy target, team preference, and budget.
3. Produce `research/tech-stack.md` with pinned versions, install commands, and rejected alternatives.
4. Present. Ask: **"Any stack or deployment constraint I missed?"**

**Exit condition:** `research/tech-stack.md` exists and is signed off.

**Rejection path:** Re-evaluate against the user constraint.

---

### EXECUTION:PLAN

**Entry condition:** Stack signed off.

**What happens:** Produce `plan.md` and `phase-1.md`, `phase-2.md`, `phase-3.md`. Every phase must deploy a visible preview and end with QA gates.

**Exit condition:** Plan and phase files exist and are signed off.

**Rejection path:** Restructure scope and phase boundaries.

---

### EXECUTION:PHASE-1 / PHASE-2 / PHASE-3

**Entry condition:** The relevant phase file is signed off.

**What happens:**

1. Execute the phase file step by step.
2. Deploy preview.
3. Run the relevant QA gate.
4. Fix all blockers before presenting.
5. Present preview. Ask: **"What needs changing before we continue?"**

**Exit condition:** Phase built, preview live, QA gate passed, user signed off.

**Rejection path:** Fix failed gate or user-identified visual/behavioral issue. Do not rebuild unrelated areas.

---

### QA:FINAL

**Entry condition:** All phases signed off.

**What happens:** Run final pre-launch QA, produce `qa/final-report.md`, present results, then set `memory.md -> Phase: DONE` only after pass and approval.

**Exit condition:** Final report exists, checks pass, user signs off.

**Rejection path:** Fix blocker, rerun failed check, update report.

---

### DONE

Project complete. Optional: export handoff bundle.

---

## Inspiration Escalation Rule

If taste evidence is too weak to produce a moodboard in interactive mode, stop and guide the user. Ask for 3-7 references, with examples:

- "Send websites you would be proud to resemble."
- "Send Dribbble/Behance/Pinterest links for layout or mood."
- "Send Instagram reels/carousels/posts from designers whose motion or composition you like."
- "Send screenshots if links are private."
- "For each source, add one sentence: what should we borrow, and what should we avoid?"

Do not fill the gap with generic Web Claw defaults unless the user explicitly chooses fast mode or says "use your judgment."

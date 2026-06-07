# Web Claw v2

**A research-first skill for designing and shipping scroll-stopping websites through AI coding agents.**

Web Claw v2 turns "build me a beautiful website" into a collaborative design process:

1. gather user inspiration,
2. discover companion design skills,
3. research open-web references,
4. build a moodboard,
5. calibrate taste with the user,
6. create sitemap, style guide, wireframes, and motion spec,
7. implement through QA-gated phases.

It is designed for Claude Code, Codex, Cursor, Windsurf, Continue, Aider, Antigravity, or any agent that can read files and run tools. Tool-using agents get the full benefit; manual-mode agents can still use the methodology with local QA run separately.

---

## What Changed In v2

v1 had a structural flaw: the pipeline created blueprint artifacts before doing deep inspiration research. v2 fixes that.

The v2 pipeline is:

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

Web Claw v2 no longer requires Awwwards or YouTube. It can use them when they fit, but it can also use user screenshots, Dribbble, Pinterest, Behance, Instagram, product pages, Mobbin, Land-book, Godly, Siteinspire, Codrops, portfolios, brand guidelines, and direct user notes.

---

## Design Philosophy

- **Taste evidence before taste claims.** No moodboard, no blueprint.
- **User inspiration is primary.** The user's links and screenshots outrank famous galleries.
- **Open-web research is source-agnostic.** Use the right source for the project.
- **Companion skills are teammates.** Discover Taste Skill, UI-UX Pro Max, Impeccable, Stitch, motion tools, or any useful local design skill.
- **One page, one job.**
- **One signature device per page.**
- **Reduced motion is design.**
- **Numbers, not vibes.** Lighthouse, contrast, bundle, accessibility, and motion budgets still gate execution.

---

## Install

Clone or install this branch into your agent's skills folder.

```bash
git clone --branch v2 https://github.com/yusufabdul024/web-claw.git web-claw
```

For Claude-style skill folders:

```bash
git clone --branch v2 https://github.com/yusufabdul024/web-claw.git ~/.claude/skills/web-claw
```

For Codex, add an `AGENTS.md` in your project:

```text
When this project is opened, read web-claw/SKILL.md and follow the Web Claw v2 pipeline. Begin by reading <project>/memory.md.
```

See `references/platform-compat.md` for broader platform guidance.

---

## Run It

```text
Run Web Claw v2 to build a scroll-stopping website for <project>.
```

Better:

```text
Run Web Claw v2 for my studio site. Goal: book discovery calls. Audience: founders. I like these references:
1. <link> - borrow the typography, not the colors.
2. <link> - borrow the motion pacing.
3. <screenshot> - borrow the editorial spacing.
```

If you do not have references, Web Claw v2 will ask for them or research open-web defaults, depending on mode.

---

## Project Outputs

Research:

- `research/skill-discovery.md`
- `research/inspiration-sources.md`
- `research/research-matrix.md`
- `research/moodboard.md`
- `research/taste-calibration.md`

Blueprint:

- `blueprint/discovery.md`
- `blueprint/sitemap.md`
- `blueprint/style-guide.md`
- `blueprint/wireframes.md`
- `blueprint/animations.md`

Execution:

- `research/tech-stack.md`
- `plan.md`
- `phase-1.md`
- `phase-2.md`
- `phase-3.md`

QA:

- phase QA reports,
- visual critique reports,
- performance/accessibility/bundle/reduced-motion/playwright evidence,
- final report.

---

## Requirements

- Python 3.8+ for scripts.
- Node.js 18+ for Lighthouse, pa11y, Playwright, and frontend package tooling.
- An agent or human operator that can browse or provide design references.

---

## Scripts

Key scripts:

- `scripts/init-project.py`
- `scripts/research-matrix.py`
- `scripts/generate-phases.py`
- `scripts/check-output.py`
- `scripts/audit-perf.py`
- `scripts/check-a11y.py`
- `scripts/check-contrast.py`
- `scripts/check-bundle.py`
- `scripts/check-reduced-motion.py`
- `scripts/run-playwright.py`
- `scripts/visual-regression.py`

`scripts/scrape-awwwards.py` remains as an optional legacy helper. It is not required in v2.

---

## Companion Skills

If sibling skills are present, Web Claw v2 discovers them during `RESEARCH:SKILL-DISCOVERY`.

Expected useful neighbors include:

- `taste-skill`
- `ui-ux-pro-max-skill`
- `impeccable`
- Stitch tooling
- motion/framer/animation skills
- accessibility/frontend polish skills

Unavailable skills do not block the pipeline. Their absence is recorded only when it changes quality or fallback behavior.

---

## Done Means

- Moodboard and taste calibration are complete before blueprint.
- Blueprint artifacts trace back to research evidence.
- Stack and phases are project-specific, not template defaults.
- The site is deployed through each phase.
- QA gates pass.
- The final site is beautiful, usable, accessible, performant, and specific enough that the user is proud to share it.

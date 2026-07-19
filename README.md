# Web Claw v3

**A studio-workflow skill for designing and shipping scroll-stopping websites through AI coding agents.**

Web Claw v3 turns "build me a beautiful website" into the workflow a real design studio runs, in four parts:

1. **Brief** — interview the client: what the brand is about, what the site must achieve, what the visitor must do, the one objective, and a value proposition a stranger understands in 3 seconds.
2. **Research** — competitor analysis, inspiration intake, open-web research, moodboard, taste calibration — verified with the client in a back-and-forth loop until the way forward is clear.
3. **Design** — sitemap, branding/style guide, wireframes, motion spec, each signed off.
4. **Build** — phased, test-driven implementation with client checkpoints, a designed loading experience, and hard QA gates.

The agent runs it as the **Chief Designer** (`agents/chief-designer.md`) — an award-winning, animated-storytelling web developer identity that directs Web Claw's specialist agents as a studio team.

It is designed for Claude Code, Codex, Cursor, Windsurf, Continue, Aider, Antigravity, or any agent that can read files and run tools. Tool-using agents get the full benefit; manual-mode agents can still use the methodology with local QA run separately.

---

## What Changed In v3

v2 fixed v1's ordering flaw (research now precedes design). v3 makes the workflow *human*:

- **Identity primer.** Every session starts by adopting the Chief Designer identity — an expert in 3D scroll animations, micro-interactions, and UI/UX who leads the agent team.
- **The Brief comes first.** A real client interview with a 3-second value-proposition test, before any research.
- **Competitor analysis** is a dedicated state (`RESEARCH:COMPETITORS`) producing positioning gaps, experience gaps, and ranked audience USPs.
- **The client stays in the loop.** Research findings are verified before being built on; builds show signature elements the moment they first work — no big-bang reveals.
- **Test-driven build.** Each phase writes its Playwright assertions first and builds until green.
- **The premium experience standard** (`references/premium-experience-standard.md`) defines the feel bar: designed loading states (never generic skeletons), smooth reveals, parallax, depth and z-layering, big playful typography, mask reveals, a focal storytelling element, and an emotional journey that ends amazed.

The v3 pipeline:

```text
PART 1 - BRIEF      BRIEF:INTERVIEW
PART 2 - RESEARCH   RESEARCH:SKILL-DISCOVERY -> RESEARCH:INSPIRATION-INTAKE ->
                    RESEARCH:COMPETITORS -> RESEARCH:OPEN-WEB ->
                    RESEARCH:MOODBOARD -> RESEARCH:TASTE-CALIBRATION
PART 3 - DESIGN     DESIGN:SITEMAP -> DESIGN:STYLE-GUIDE ->
                    DESIGN:WIREFRAMES -> DESIGN:ANIMATIONS
PART 4 - BUILD      BUILD:STACK -> BUILD:PLAN -> BUILD:PHASE-1 ->
                    BUILD:PHASE-2 -> BUILD:PHASE-3 -> BUILD:QA-FINAL -> DONE
```

Research prioritizes real shipped websites — award-winning sites, international studio/agency portfolios and their client work, strong product sites — supported by Dribbble, Pinterest, Behance, Instagram, Mobbin, Land-book, Godly, Siteinspire, Codrops, screenshots, and direct user notes. No single source is mandatory.

---

## Design Philosophy

- **The brief is the foundation.** No research from nowhere; interview the client first.
- **Taste evidence before taste claims.** No moodboard, no design.
- **User inspiration is primary.** The user's links and screenshots outrank famous galleries.
- **The client stays in the loop.** Verify research; show signature elements early; never big-bang reveal.
- **The arrival is designed.** The loading state is the opening scene, not a technical apology.
- **Companion skills are teammates.** Discover Taste Skill, UI-UX Pro Max, Impeccable, Stitch, motion tools, or any useful local design skill.
- **One page, one job. One signature device per page.**
- **Reduced motion is design.**
- **Numbers, not vibes.** Lighthouse, contrast, bundle, accessibility, and motion budgets still gate execution.

---

## Install

Clone or install Web Claw into your agent's skills folder. The default branch (`main`) is the current release.

```bash
git clone https://github.com/yusufabdul024/web-claw.git web-claw
```

For Codex global skill discovery, install into the Codex skill roster folder:

```bash
git clone https://github.com/yusufabdul024/web-claw.git ~/.codex/skills/web-claw
python ~/.codex/skills/web-claw/scripts/verify-install.py --skill-root ~/.codex/skills/web-claw
```

On Windows PowerShell:

```powershell
git clone https://github.com/yusufabdul024/web-claw.git "$env:USERPROFILE\.codex\skills\web-claw"
python "$env:USERPROFILE\.codex\skills\web-claw\scripts\verify-install.py" --skill-root "$env:USERPROFILE\.codex\skills\web-claw"
```

If you already cloned the repo elsewhere, the installer can copy it:

```bash
./install.sh --host codex --user --force
```

```powershell
.\install.ps1 -HostName codex -User -Force
```

Restart Codex after a global install so the skill roster is rebuilt.

For Claude-style skill folders:

```bash
git clone https://github.com/yusufabdul024/web-claw.git ~/.claude/skills/web-claw
```

For project-scoped Codex activation, use the installer:

```bash
./install.sh --host codex --project <project> --force
```

```powershell
.\install.ps1 -HostName codex -Project <project> -Force
```

This copies Web Claw to `<project>/.agents/skills/web-claw/` and writes an `AGENTS.md` pointer. You can also add the pointer manually:

```text
When this project is opened, read .agents/skills/web-claw/SKILL.md, adopt the Chief Designer identity from agents/chief-designer.md, and follow the Web Claw v3 pipeline. Begin by reading <project>/memory.md.
```

See `references/platform-compat.md` for broader platform guidance.

---

## Run It

```text
Run Web Claw v3 to build a scroll-stopping website for <project>.
```

Better:

```text
Run Web Claw v3 for my studio site. Goal: book discovery calls. Audience: founders. I like these references:
1. <link> - borrow the typography, not the colors.
2. <link> - borrow the motion pacing.
3. <screenshot> - borrow the editorial spacing.
```

If you do not have references, Web Claw v3 will ask for them or research open-web defaults, depending on mode. Either way it starts with the brief interview — expect questions before artifacts.

---

## Project Outputs

Brief:

- `brief/client-brief.md` — including the 3-second-test value proposition.

Research:

- `research/skill-discovery.md`
- `research/inspiration-sources.md`
- `research/competitor-analysis.md`
- `research/research-matrix.md`
- `research/moodboard.md`
- `research/taste-calibration.md` — the signed-off way forward.

Design:

- `design/sitemap.md`
- `design/style-guide.md`
- `design/wireframes.md`
- `design/animations.md` — including the loading state and focal storytelling element.

Build:

- `research/tech-stack.md`
- `plan.md`
- `phase-1.md` / `phase-2.md` / `phase-3.md` — each with test assertions and client checkpoints.

QA:

- phase QA reports,
- visual critique reports (12 axes, including arrival and depth/journey),
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

`scripts/scrape-awwwards.py` is an optional helper for award-gallery evidence during `RESEARCH:OPEN-WEB`.

---

## Companion Skills & MCP Servers

Web Claw v3 discovers companions during `RESEARCH:SKILL-DISCOVERY` and routes them per the Known Companion Registry in `references/extension-orchestration.md`:

| Companion | Kind | Source | Used for |
|---|---|---|---|
| [UI-UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Skill | nextlevelbuilder | Styles, palettes, font pairings, UX guidelines |
| [Taste Skill](https://github.com/Leonxlnx/taste-skill) | Skill | Leonxlnx | Anti-slop critique, design direction |
| [shadcn/ui MCP](https://github.com/Jpisnice/shadcn-ui-mcp-server) | MCP server | Jpisnice | Component source-of-truth on React/Tailwind stacks |
| [21st.dev Magic MCP](https://github.com/21st-dev/magic-mcp) | MCP server | 21st-dev | UI component candidates (restyled to project tokens) |
| [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills) | Skill | vercel-labs | React/Next.js performance idioms |
| [GSAP Master](https://github.com/greensock/gsap-skills) | Skill | greensock | GSAP/ScrollTrigger implementation |
| [Motion / Framer](https://github.com/freshtechbro/claudedesignskills) | Skill | freshtechbro | Framer Motion implementation |
| [Convex Create Component](https://github.com/get-convex/agent-skills) | Skill | get-convex | Backend/data components — only when the brief needs one |
| [Vercel React Native Skills](https://github.com/vercel-labs/agent-skills) | Skill | vercel-labs | Native companion apps — only when in scope |
| Impeccable / Stitch | Skill | local | Polish, critique, visual ideation |

Companions are advisory: their advice is distilled into Web Claw artifacts, and Web Claw's budgets and QA gates stay authoritative. Unavailable companions do not block the pipeline — their absence is recorded only when it changes quality, and nothing is installed or configured without your consent.

---

## Done Means

- The brief exists and its value proposition passes the 3-second test.
- Competitor analysis, moodboard, and taste calibration are complete before design.
- Design artifacts trace back to research evidence.
- Stack and phases are project-specific, not template defaults.
- Phases are built test-first, with signature elements approved by the client mid-phase.
- The arrival is designed: intentional loader, smooth reveal, zero layout shift.
- QA gates pass — including the 12-axis visual critique.
- The final site is beautiful, usable, accessible, performant, and specific enough that the visitor leaves amazed — and the client is proud to share it.

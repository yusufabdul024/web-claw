# Extension Orchestration - Web Claw v3

## Purpose

Web Claw v3 treats companion skills as teammates. It proactively discovers local design/UX/frontend skills, consults them when they can improve taste or craft, and distills their advice into Web Claw artifacts.

Companion skills are advisory. Web Claw memory, decisions, signed-off artifacts, budgets, and QA gates stay authoritative.

## Precedence Order

1. User hard constraints.
2. Web Claw memory, decisions, state, and budgets.
3. Signed-off research and design artifacts.
4. Project code and pinned package versions.
5. Companion skill advice.
6. Web Claw built-in preferences.

## Known Companion Registry

Web Claw's preferred companions. Two kinds:

- **Skill** — a folder of instructions (SKILL.md). Discovered on disk; consulted by loading its files.
- **MCP server** — a live tool server configured in the host agent. Discovered by checking the available tool list (`mcp__<server>__*` names); consulted by calling its tools.

| Companion | Kind | Source | Use for | Consulted at |
|---|---|---|---|---|
| UI-UX Pro Max | Skill | `github.com/nextlevelbuilder/ui-ux-pro-max-skill` | Styles, palettes, font pairings, product-type patterns, UX guidelines, stack-specific UI guidance | RESEARCH:MOODBOARD, RESEARCH:TASTE-CALIBRATION, DESIGN:STYLE-GUIDE, DESIGN:WIREFRAMES |
| Taste Skill (design-taste-frontend) | Skill | `github.com/Leonxlnx/taste-skill` | Anti-slop pressure, design-direction inference, "does this feel templated?" critique | RESEARCH:MOODBOARD, RESEARCH:TASTE-CALIBRATION, BUILD phase reviews |
| shadcn/ui MCP | MCP server | `github.com/Jpisnice/shadcn-ui-mcp-server` | Component/blocks source-of-truth for React/Next.js + Tailwind stacks — real implementations, demos, dependencies | BUILD:STACK (feasibility), BUILD:PHASE-1 (component library) |
| 21st.dev Magic MCP | MCP server | `github.com/21st-dev/magic-mcp` | Generating UI component candidates from natural language | BUILD:PHASE-1/2 — candidates only; always restyled through Web Claw tokens |
| Vercel React Best Practices | Skill | `github.com/vercel-labs/agent-skills` (`react-best-practices`) | React/Next.js performance idioms: waterfalls, bundle discipline, server components, re-render hygiene | BUILD:STACK, BUILD:PHASE-1..3, perf-gate fixes |
| GSAP Master | Skill | `github.com/greensock/gsap-skills` | GSAP/ScrollTrigger implementation idioms: pinned narratives, scrubbed timelines, mask reveals, 3D scroll choreography | DESIGN:ANIMATIONS (feasibility), BUILD:PHASE-2 |
| Motion / Framer | Skill | `github.com/freshtechbro/claudedesignskills` (`motion-framer`) | Framer Motion / Motion One implementation idioms: variants, layout animations, gestures, exit transitions | DESIGN:ANIMATIONS (feasibility), BUILD:PHASE-2 |
| Convex Create Component | Skill | `github.com/get-convex/agent-skills` (`convex-create-component`) | Backend/data components when the site needs live data: forms that persist, auth, realtime, waitlists | BUILD:STACK, BUILD:PHASE-1/3 — only when the brief demands a backend |
| Vercel React Native Skills | Skill | `github.com/vercel-labs/agent-skills` (react-native) | Native/Expo implementation guidance | Only when the project explicitly targets a native app companion — out of scope for pure websites |
| Impeccable | Skill | (local) | Critique, polish, UI hardening, browser iteration, responsive/a11y refinement | RESEARCH:TASTE-CALIBRATION, BUILD:PHASE-1..3 |
| Stitch | Skill | (local) | Visual ideation, screen exploration | RESEARCH:MOODBOARD — output is never production code |

Conditional entries (Convex, React Native) are recorded in `research/skill-discovery.md` as "available, not routed" unless the brief activates them. Routing a backend or native-app skill into a static marketing site is scope creep — flag it to the client instead.

## Discovery Algorithm

Run this during `RESEARCH:SKILL-DISCOVERY`.

1. Determine Web Claw's own skill directory: folder containing `SKILL.md`.
2. Determine the skills root: parent folder of Web Claw's directory. Also check the host's other skill roots when readable (`~/.claude/skills`, `.claude/skills`, `~/.codex/skills`, `.agents/skills`, `.cursor/skills`).
3. Scan sibling directories.
4. For each sibling, inspect lightweight metadata only:
   - `SKILL.md`
   - `skill.json`
   - `.codex-plugin/plugin.json`
   - `README.md`
   - obvious manifest files
5. Detect known companion skill names (see the registry above), including folder-name variants:
   - `taste-skill`, `design-taste-frontend`
   - `impeccable`
   - `ui-ux-pro-max-skill`, `ui-ux-pro-max`
   - `gsap-master`, `gsap-skills`
   - `motion-framer`, `claudedesignskills`, motion/framer/animation skills
   - `react-best-practices`, `vercel-react-best-practices`
   - `convex-create-component`, `convex`
   - `react-native` skills
   - `stitch`
6. Detect MCP companions by inspecting the available tool list for server prefixes (e.g., shadcn/ui tools, 21st.dev Magic tools). An MCP server that is not connected is "useful but unavailable" — never assume its tools exist.
7. Also detect adjacent design capabilities by keywords:
   - taste, critique, polish, impeccable, UI, UX, design system, brand, motion, animation, accessibility, frontend, component, stitch, image-to-code.
8. If tools allow web/GitHub search, search for missing but useful public skills or docs. Do not install automatically.
9. Write `research/skill-discovery.md`.

## Install Guidance (user consent required)

Never install a skill or configure an MCP server without the user's explicit consent. When a useful companion is missing, record it in `research/skill-discovery.md -> Useful But Unavailable` with this guidance:

- **File skills** — clone or copy the skill folder into the agent's skills directory (e.g., `~/.claude/skills/<name>` or the project's `.claude/skills/`/`.agents/skills/`), per the repo README.
- **MCP servers** — configured in the host agent (e.g., `claude mcp add ...` or the host's `.mcp.json`); both registry MCP servers run via `npx` — follow the exact command and API-key setup in the repo README (Magic MCP requires a 21st.dev API key).

## Output Format

```markdown
# Skill Discovery

## Available Local Skills

| Skill | Path | Use for | When consulted |
|-------|------|---------|----------------|

## Useful But Unavailable

| Skill | Source / search result | Why useful | User action |
|-------|------------------------|------------|-------------|

## Routing Plan

- RESEARCH:MOODBOARD -> <skill> for <purpose>
- RESEARCH:TASTE-CALIBRATION -> <skill> for <purpose>
- DESIGN:STYLE-GUIDE -> <skill> for <purpose>
- BUILD:PHASE-N -> <skill> for <purpose>

## Fallbacks

- If <skill> unavailable, use <fallback>.
```

## Companion Roles

### Taste Skill

Use for taste pressure, anti-generic critique, moodboard sharpness, visual ambition, and "does this feel like a real creative direction?"

### Impeccable

Use for critique, polish, UI hardening, browser iteration, layout correction, responsive/a11y polish, and final visual refinement. Its findings inform QA reports, but Web Claw gates decide severity.

### UI-UX Pro Max

Use for product-type patterns, UX guidelines, design-system references, style catalogs, color/type candidates, and stack-specific UI guidance. Treat results as raw material, not orders.

### Stitch

Use for visual ideation and screen/design-system exploration when available. Stitch output is not production code. Translate it through Web Claw tokens, accessibility, motion, and QA.

### GSAP Master

Use for GSAP/ScrollTrigger implementation: pinned scroll narratives, scrubbed timelines, mask reveals, focal-element choreography, 3D scroll integration. The Animator specs the intent; GSAP Master informs *how it's buildable*. It never relaxes motion budgets, the 60fps rule, or reduced-motion replacements.

### Motion / Framer

Use for Framer Motion / Motion One implementation idioms: variants, layout animations, gestures, exit transitions, spring tuning. Same rule: feasibility and idiom advice only — budgets and reduced-motion stay hard. When the stack picks GSAP, consult GSAP Master instead; don't mix both libraries for the same effect.

### shadcn/ui MCP

Use on React/Next.js + Tailwind stacks as the source of truth for component implementations, demos, and blocks — instead of hallucinating component APIs. Every pulled component is restyled through the signed-off `design/style-guide.md` tokens; a default-themed shadcn page fails the visual critique's "template" test by definition.

### 21st.dev Magic MCP

Use to generate UI component candidates during build phases. Output is raw material: it must be restyled to Web Claw tokens, checked against the wireframe's structure, and pass a11y review before it lands in the repo. Never let generated components define the design direction — that flows only from taste calibration.

### Vercel React Best Practices

Use on React/Next.js stacks for performance idioms: eliminating waterfalls, bundle discipline, server/client component boundaries, re-render hygiene. Consult when picking the stack and whenever a perf gate fails on a React build.

### Convex Create Component

Use only when the brief demands live data (persisting forms, auth, realtime, waitlists). If the brief is a static marketing site, record it as available-but-not-routed; adding a backend is a scope conversation with the client, not a skill routing decision.

### Vercel React Native Skills

Use only when the project explicitly includes a native app companion. Out of scope for pure websites.

### Other Design Skills

If a sibling skill clearly helps with brand, visual critique, accessibility, motion, frontend implementation, or image-to-code, record it and route to it. Do not ignore useful capabilities because they are not in the original named list.

## Phase Routing

| Web Claw state | Companion use |
|----------------|---------------|
| RESEARCH:SKILL-DISCOVERY | Detect and document available skills and MCP servers per the registry. |
| RESEARCH:OPEN-WEB | Use UI-UX Pro Max / design research skills to broaden source discovery. |
| RESEARCH:MOODBOARD | Use Taste Skill / UI-UX Pro Max to sharpen directions and anti-style. |
| RESEARCH:TASTE-CALIBRATION | Use Taste Skill / Impeccable / UI-UX Pro Max for critique before user sign-off. |
| DESIGN:STYLE-GUIDE | Use UI-UX Pro Max palette/type/design-system catalogs for candidate systems. |
| DESIGN:WIREFRAMES | Use UI-UX Pro Max / UX skills for structure and originality critique. |
| DESIGN:ANIMATIONS | Use GSAP Master / Motion-Framer for feasibility and API patterns per the spec's ambition. |
| BUILD:STACK | Use Vercel React Best Practices (React stacks), shadcn/ui MCP availability, Convex (only if the brief needs a backend) to inform the pick. |
| BUILD:PHASE-1 | Use shadcn/ui MCP + Magic MCP for component sourcing (restyled to tokens); Impeccable for static UI polish; Convex components if routed. |
| BUILD:PHASE-2 | Use GSAP Master / Motion-Framer for animation implementation; Impeccable for polish and reduced-motion checks. |
| BUILD:PHASE-3 | Use Vercel React Best Practices + Impeccable / accessibility skills for launch hardening. |
| BUILD:QA-FINAL | Companion skills may critique, but QA scripts and checklists decide pass/fail. |

## Distillation Rule

Raw companion output is never canonical. Every useful finding must be distilled into one of:

- `research/skill-discovery.md`
- `research/moodboard.md`
- `research/taste-calibration.md`
- a design artifact
- a decision file
- `qa/phase-N-report.md`

If it is not distilled, it is not part of the project.

## Conflict Rules

- Do not average conflicting design advice.
- Pick one coherent direction and record why.
- User hard constraints always win.
- Budgets always beat ambition.
- Signed-off decisions are not re-litigated unless the user reopens them.
- Companion advice cannot demand a stack change after stack sign-off unless it identifies a blocker.

## Failure Mode

If a companion skill is unavailable, errors, times out, or contradicts hard constraints:

1. Continue with Web Claw's built-in references.
2. Record the absence only if it affects the artifact.
3. In interactive mode, ask the user only if the missing skill was central to their request.
4. In fast mode, log the degraded consultation in `memory.md -> Blockers`.

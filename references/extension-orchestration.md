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

## Discovery Algorithm

Run this during `RESEARCH:SKILL-DISCOVERY`.

1. Determine Web Claw's own skill directory: folder containing `SKILL.md`.
2. Determine the skills root: parent folder of Web Claw's directory.
3. Scan sibling directories.
4. For each sibling, inspect lightweight metadata only:
   - `SKILL.md`
   - `skill.json`
   - `.codex-plugin/plugin.json`
   - `README.md`
   - obvious manifest files
5. Detect known companion skill names:
   - `taste-skill`
   - `impeccable`
   - `ui-ux-pro-max-skill`
   - `ui-ux-pro-max`
   - `stitch`
   - motion/framer/animation skills
6. Also detect adjacent design capabilities by keywords:
   - taste, critique, polish, impeccable, UI, UX, design system, brand, motion, animation, accessibility, frontend, component, stitch, image-to-code.
7. If tools allow web/GitHub search, search for missing but useful public skills or docs. Do not install automatically.
8. Write `research/skill-discovery.md`.

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

### Motion / Framer / Animation Tooling

Use for API feasibility and implementation idioms. Tooling never relaxes motion budgets or reduced-motion rules.

### Other Design Skills

If a sibling skill clearly helps with brand, visual critique, accessibility, motion, frontend implementation, or image-to-code, record it and route to it. Do not ignore useful capabilities because they are not in the original named list.

## Phase Routing

| Web Claw state | Companion use |
|----------------|---------------|
| RESEARCH:SKILL-DISCOVERY | Detect and document available skills. |
| RESEARCH:OPEN-WEB | Use UI-UX/design research skills to broaden source discovery. |
| RESEARCH:MOODBOARD | Use Taste/UI-UX/design skills to sharpen directions and anti-style. |
| RESEARCH:TASTE-CALIBRATION | Use Taste/Impeccable/UI-UX Pro Max for critique before user sign-off. |
| DESIGN:STYLE-GUIDE | Use palette/type/design-system skills for candidate systems. |
| DESIGN:WIREFRAMES | Use UX/UI skills for structure and originality critique. |
| DESIGN:ANIMATIONS | Use motion skills for feasibility and API patterns. |
| BUILD:PHASE-1 | Use Impeccable/frontend skills for static UI polish. |
| BUILD:PHASE-2 | Use Impeccable/motion skills for animation polish and reduced-motion checks. |
| BUILD:PHASE-3 | Use Impeccable/accessibility/perf skills for launch hardening. |
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

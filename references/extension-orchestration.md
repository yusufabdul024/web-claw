# Extension Orchestration

How Web Claw consults companion skills as **optional, advisory** capability modules without becoming dependent on them.

---

## Purpose

Web Claw is the orchestrator. Memory, decisions, state machine, artifacts, QA gates, and budgets are authoritative and stay inside Web Claw. Companion skills (Taste, Impeccable, UI-UX Pro Max, Stitch, motion tooling) extend Web Claw's reach when they are present in the environment, but they never replace a Web Claw phase, override a QA gate, or own an artifact.

If no companion skills are available, **Web Claw still works**. Extensions add quality, breadth, and ambition. They do not add gates.

---

## Precedence Order

When two sources disagree, the higher item wins. Always.

1. **User hard constraints** — anything the user explicitly forbids or requires (stack pin, deadline, copy lock, motion intensity cap, accessibility floor above default).
2. **Web Claw memory / decisions / state / budgets** — `memory.md`, every signed-off `decisions/NNN-*.md`, the current state's exit condition, and `references/budgets.yaml`.
3. **Approved artifacts** — anything in `blueprint/`, `research/`, or `<project>/plan.md` that already carries `User sign-off: YES` (or `AUTO` in fast mode).
4. **Project code and pinned package versions** — what's on disk in the active build; what `package.json` (or equivalent) pins.
5. **Extension advice** — anything returned by a companion skill consultation.
6. **Taste preferences** — subjective leanings of any agent or extension when no objective constraint applies.

Extension advice is below project code: a companion skill cannot demand a library change that breaks the pinned stack. Extension advice is above taste preferences: if no constraint applies, prefer the extension's informed recommendation over an unsupported leaning.

---

## Sibling Discovery

Web Claw discovers companion skills by inspecting the filesystem around its own skill directory. Web Claw never sets up companion skills itself; it only reads what is already present in the skills root.

**Algorithm:**

1. Determine Web Claw's own skill directory (the folder containing this `SKILL.md`).
2. The parent of that directory is the skills root.
3. Probe the skills root for sibling folders by canonical name:
   - `taste-skill/` (and its nested sub-skills like `taste-skill`, `brutalist-skill`, `minimalist-skill`, `brandkit`, `image-to-code-skill`, etc.)
   - `impeccable/`
   - `ui-ux-pro-max-skill/` (or `ui-ux-pro-max/`)
4. For each probed name: present → mark available; absent → mark unavailable.
5. If an extension is unavailable AND that absence will affect the current artifact, record it once in `decisions/NNN-extension-unavailable-<name>.md` with the affected artifact and the chosen fallback. Do not log absences that did not change anything.

For tooling that may not appear as a sibling folder (Stitch, motion tooling), availability is determined by whether the host environment exposes the relevant tools. If the consultation cannot be performed, treat it as unavailable and follow the same decision-logging rule.

---

## Extension Roles

Each role describes what the extension contributes. The wording in each role is descriptive, not prescriptive: extensions are advisory.

### Taste Skill

A taste lens. Provides taste calibration, anti-generic critique, and ambition pressure on hero, layout, material, and motion choices. Supports Stitch consultations by contributing `DESIGN.md`-style direction. **Taste Skill is not a pipeline; it does not own artifacts.** Use it to test whether a Web Claw artifact has settled into a generic resolution and needs a push.

### Impeccable

A critique and polish lens. Handles critique, polish, harden, adapt, clarify, optimize, and (when the host supports it) live browser iteration on UI elements. Impeccable can identify blockers and weaknesses, but **Web Claw's QA gates decide whether a finding blocks advance.** Impeccable findings inform `qa/phase-N-report.md`; gate severity stays with Web Claw.

### UI-UX Pro Max

Searchable design intelligence: product type catalog, style catalog, color palettes, typography pairings, landing-page structures, UX guidelines, and stack-specific guidance (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, HTML/CSS). **Results are raw reference material, not orders.** Web Claw decides which candidates to adopt and records the choice in the relevant artifact or decision.

### Stitch

Visual ideation and screen / design-system exploration when host tooling exposes Stitch. **Stitch output is not production code.** Any Stitch-generated UI must be translated through Web Claw implementation (tokens, motion budgets, accessibility rules) and validated through Web Claw QA before it is treated as a deliverable.

### Motion / framer tooling

Implementation reference for animation APIs only. Provides idiomatic patterns for the chosen animation cluster. **Motion/framer tooling does not relax Web Claw motion budgets, reduced-motion rules, or bundle constraints** in `references/budgets.yaml`. If a pattern requires breaking a budget, the budget wins.

---

## Phase Routing

When and how each extension may be consulted, by state.

| Web Claw state         | Extensions that may be consulted                                                                                              | Web Claw retains                                |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| IGNITION               | UI-UX Pro Max — optional product-type and style calibration to inform discovery.                                              | Discovery questions, `memory.md`, sign-off      |
| BLUEPRINT:STYLE-GUIDE  | UI-UX Pro Max for palette / type / style candidates; Taste Skill for anti-generic pressure; optional Stitch `DESIGN.md`.      | The signed-off `blueprint/style-guide.md` + tokens contract |
| BLUEPRINT:WIREFRAMES   | UI-UX Pro Max for structure and pattern options; Taste Skill for layout originality.                                          | The signed-off `blueprint/wireframes.md`        |
| BLUEPRINT:ANIMATIONS   | Taste Skill for ambition check; motion tooling for API feasibility. Web Claw budgets in `budgets.yaml` are the hard ceiling. | The signed-off `blueprint/animations.md`, motion budgets |
| EXECUTION:STACK        | UI-UX Pro Max stack guidance alongside `references/tech-stack.md`.                                                            | The signed-off `research/tech-stack.md`         |
| EXECUTION:PHASE-1      | Impeccable — critique, layout, typeset, audit on the static build.                                                            | `qa/phase-1-gate.md`, the Phase 1 report        |
| EXECUTION:PHASE-2      | Impeccable — animate, optimize, polish on the motion build.                                                                   | `qa/phase-2-gate.md`, the Phase 2 report        |
| EXECUTION:PHASE-3      | Impeccable — harden, adapt, clarify, polish before final QA.                                                                  | `qa/phase-3-gate.md`, the Phase 3 report        |
| QA:FINAL               | None of the above own the final gate.                                                                                         | `qa/pre-launch-checklist.md`, final pass / fail |

States not listed (BLUEPRINT:SITEMAP, RESEARCH:AWWWARDS, RESEARCH:YOUTUBE, EXECUTION:PLAN, DONE) do not currently route to extensions; if a future need arises, add a row here.

---

## Extension Output Contract

Every consultation must be **distilled into a Web Claw artifact** before the consultation is considered closed. Raw extension dumps are never canonical.

Distillation targets, by consultation context:

| Consultation context                               | Required distillation target                          |
|----------------------------------------------------|-------------------------------------------------------|
| During a BLUEPRINT or RESEARCH state               | The active state's artifact (`sitemap.md`, `style-guide.md`, `wireframes.md`, `animations.md`, `awwwards-references.md`, etc.) |
| When the consultation changes a pinned decision    | `decisions/NNN-<topic>.md` with the rationale         |
| Any Stitch consultation                            | `blueprint/stitch-notes.md` (the standing companion file for Stitch artefacts) |
| During QA (any phase)                              | `qa/phase-N-report.md` (or `qa/final-report.md` at QA:FINAL) |

Rules:

- An extension finding that is not distilled into one of the above is **not part of the project**. It does not influence sign-off, downstream artifacts, or QA.
- A distillation references the source (extension name, prompt or query, date) so the trail is auditable.
- Distillation is the agent's job, not the user's. The agent translates extension output into Web Claw's voice and structure.

---

## Conflict Rules

When extensions disagree with each other, with prior Web Claw decisions, or with the user, follow the precedence order above and these conflict resolution rules.

1. **Do not average conflicting advice.** Averaging design or motion advice produces generic results.
2. **Pick one direction.** A single coherent direction beats a hybrid of two halves.
3. **Record the rationale** in a `decisions/NNN-*.md` file when the choice changes design language, stack, motion intensity, information architecture, or QA posture.
4. **Web Claw budgets always beat visual ambition.** If two directions both fit budget, pick on taste; if only one fits budget, the budget choice wins; if neither fits budget, simplify until one does.
5. **Extension advice never relaxes a QA gate.** If Impeccable says "this is fine," and `scripts/audit-perf.py` or `scripts/check-a11y.py` says it is not, the script wins.
6. **The user's hard constraints always win.** If an extension recommends a stack the user vetoed, do not adopt it; record the rejection.

---

## Failure Mode

If an extension consultation fails (extension unavailable, returns an error, times out, exceeds an available quota, or returns output that contradicts a hard constraint):

1. Continue the state without the extension.
2. Use the built-in Web Claw reference (`references/pattern-library.md`, `references/color-theory.md`, `references/animation-libraries.md`, etc.) as the fallback source.
3. Record the absence in `decisions/NNN-extension-unavailable-<name>.md` only if the absence affected the artifact.
4. Do not stall, retry indefinitely, or escalate to the user unless the user previously asked to be told.

Web Claw's pipeline is always completable without any extension.

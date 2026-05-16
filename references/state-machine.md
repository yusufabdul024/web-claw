# State Machine — Web Claw Pipeline States and Transitions

## Overview

The Web Claw pipeline is a state machine, not a linear checklist. Each state has an **entry condition**, an **exit condition** (including user sign-off), and a **rejection path**. The current state is always recorded in `memory.md -> Phase`.

**Rule:** An agent must not advance to the next state until the exit condition is fully satisfied. If the user rejects an artifact, follow the rejection path — do not skip forward.

## Mode-aware sign-off

Web Claw runs in one of two modes (recorded in `memory.md -> Mode`). The state machine is the same in both; the **sign-off semantics** differ.

| Mode          | User sign-off requirement                    | When state advances                                                              |
|---------------|-----------------------------------------------|----------------------------------------------------------------------------------|
| `interactive` | Explicit user `YES` (or "use defaults")       | After the user approves the presented artifact.                                  |
| `fast`        | Auto-approved by agent; logged in `decisions/`| Immediately after the artifact is written and any **automated** gate passes.     |

**Important:** Automated QA gates (Lighthouse, axe-core, contrast, motion checklist) are **always hard** — same blocking behavior in both modes. Fast mode only short-circuits *human-in-the-loop* approval, not automated quality enforcement.

When this document says "user sign-off" below, read it as:
- In `interactive`: ask the specified question, wait for explicit user answer.
- In `fast`: pick the default per the agent's operating principles, write `decisions/NNN-auto-<topic>.md` documenting the choice + rationale, set `User sign-off: AUTO`, and advance.

---

## State Diagram

```
IGNITION
  ↓ (discovery.md written, user confirmed)
BLUEPRINT:SITEMAP
  ↓ (sitemap.md written, user signed off)
BLUEPRINT:STYLE-GUIDE
  ↓ (style-guide.md written, user signed off)
BLUEPRINT:WIREFRAMES
  ↓ (wireframes.md written, user signed off)
BLUEPRINT:ANIMATIONS
  ↓ (animations.md written, user signed off)
RESEARCH:AWWWARDS
  ↓ (awwwards-references.md written)
RESEARCH:YOUTUBE
  ↓ (youtube-techniques.md written)
EXECUTION:STACK
  ↓ (tech-stack.md written, user signed off)
EXECUTION:PLAN
  ↓ (plan.md + phase-1/2/3.md written, user signed off)
EXECUTION:PHASE-1
  ↓ (phase 1 built, QA gate passed, preview live)
EXECUTION:PHASE-2
  ↓ (phase 2 built, QA gate passed, preview live)
EXECUTION:PHASE-3
  ↓ (phase 3 built, QA gate passed, preview live)
QA:FINAL
  ↓ (pre-launch checklist passed, user signed off)
DONE
```

---

## State Definitions

### IGNITION

**Entry condition:** User has requested a website and no `memory.md` exists.

**What happens:**
1. Run `scripts/init-project.py "<project-name>"` to create workspace and blank `memory.md`.
2. Check if user already provided partial answers in their request (name, vibe, reference URLs). Pre-fill those; do not re-ask.
3. Load `references/ignition-quick.md` for simple projects (single landing page, user provided strong context). Load `references/ignition-full.md` for complex projects (multi-page, new brand, unclear audience).
4. Gather remaining answers. Write `blueprint/discovery.md`.
5. Reflect back in 4–6 lines: brand vibe, primary outcome, motion intensity, signature moment. Take corrections.
6. Update `memory.md`: Phase = BLUEPRINT:SITEMAP, Next action = "Spawn UX Strategy Agent to produce blueprint/sitemap.md".

**Exit condition:** `blueprint/discovery.md` exists AND user has explicitly confirmed the reflection.

**Rejection path:** User corrects the reflection → update `discovery.md` → reflect again → confirm → advance.

---

### BLUEPRINT:SITEMAP

**Entry condition:** `blueprint/discovery.md` exists and is confirmed.

**What happens:**
1. Load `agents/ux-strategy-agent.md` + `references/relume-methodology.md`.
2. Produce `blueprint/sitemap.md` from `assets/templates/sitemap-template.md`.
3. Present sitemap to user. Ask: **"If you had to cut one page, which? If you had to cut one section from the home page, which?"**
4. Take corrections. Revise. Re-present.
5. On approval: update `memory.md`.

**Exit condition:** `blueprint/sitemap.md` exists AND `User sign-off: YES`.

**Rejection path:**
- User rejects specific pages → remove or restructure, re-present.
- User rejects a section → update the Cuts section, explain why the section was cut, re-present.
- User says "start over" → delete sitemap.md, re-read discovery.md, rebuild from scratch.
- Create `decisions/NNN-sitemap-cuts.md` for any pages or sections removed at user request.

---

### BLUEPRINT:STYLE-GUIDE

**Entry condition:** `blueprint/sitemap.md` exists and is signed off.

**What happens:**
1. Load `agents/designer-agent.md` + `references/color-theory.md` + `references/typography-systems.md` + `references/design-systems.md`.
2. Produce `blueprint/style-guide.md` from `assets/templates/style-guide-template.md`.
3. Present to user. Ask: **"Does this palette feel right? Does the type personality match the three adjectives you gave me?"**
4. Take corrections. Revise. Re-present.
5. On approval: create `decisions/NNN-visual-direction.md`. Update `memory.md`.

**Exit condition:** `blueprint/style-guide.md` exists AND `User sign-off: YES`.

**Rejection path:**
- User rejects color → change only lightness, not hue (unless user specifies). Re-validate contrast. Re-present palette only.
- User rejects type → re-read discovery adjectives. Propose two alternatives. Let user pick. Document choice.
- User rejects the whole guide → ask which of the three adjectives feels off. Rebuild from that answer.

---

### BLUEPRINT:WIREFRAMES

**Entry condition:** `blueprint/sitemap.md` + `blueprint/style-guide.md` both signed off.

**What happens:**
1. Load `agents/ui-strategy-agent.md` + `references/pattern-library.md` (Layer 2 section signatures).
2. Produce `blueprint/wireframes.md` from `assets/templates/wireframes-template.md`.
3. Build the component inventory first. Then wireframe each page mobile-first.
4. Mark the SIGNATURE section on each page.
5. Present to user. Ask: **"Which signature section feels right? Anything not earning its space?"**
6. On approval: update `memory.md`.

**Exit condition:** `blueprint/wireframes.md` exists AND `User sign-off: YES`.

**Rejection path:**
- User says section is wrong → remove it (check Cuts reasoning), re-wireframe that page only.
- User wants a different signature section → re-mark it, note the change in decisions/.
- User wants more pages → check if discovery.md supports it. If yes, add. If no, re-read Q3 and Q4 and push back: "This page doesn't seem to drive the goal we set. Want to override?"

---

### BLUEPRINT:ANIMATIONS

**Entry condition:** All three prior blueprint artifacts signed off.

**What happens:**
1. Load `agents/animator-agent.md` + `references/animation-libraries.md` + `references/pattern-library.md` (all layers).
2. Produce `blueprint/animations.md` from `assets/templates/animations-template.md`.
3. Focus 50% of the motion spec on the SIGNATURE section from wireframes.
4. Specify every entrance, reveal, micro-interaction, and reduced-motion fallback.
5. Present to user. Ask: **"Does the signature moment match what you described in Q16? Too bold? Too restrained?"**
6. On approval: update `memory.md`.

**Exit condition:** `blueprint/animations.md` exists AND `User sign-off: YES`.

**Rejection path:**
- User says "too bold" → downgrade motion intensity by one level for the affected sections. Document in decisions/.
- User says "too restrained" → upgrade signature section spec. Keep restrained defaults elsewhere.
- User says "the signature moment is wrong" → return to Q16. Re-read the answer. Propose three alternatives. Let user pick. Rebuild that section only.

---

### RESEARCH:AWWWARDS

**Entry condition:** All Phase 1 blueprint artifacts signed off.

**What happens:**
1. Load `agents/researcher-agent.md` + `references/pattern-library.md` (Layer 2 + Layer 4 vibe matrix).
2. Browse Awwwards filtered by the discovery vibe. Inspect 30 sites. Bookmark 5–10.
3. Verify libraries via DevTools. Document each: URL, standout device, libraries, applicability.
4. Produce `research/awwwards-references.md`.
5. No user sign-off required — this is an internal research artifact. Update `memory.md`.

**Exit condition:** `research/awwwards-references.md` exists with 5–10 verified entries.

**Note:** This state can begin in parallel with BLUEPRINT:WIREFRAMES if the Researcher Agent is available. Do not delay Phase 2 for this.

---

### RESEARCH:YOUTUBE

**Entry condition:** `research/awwwards-references.md` exists.

**What happens:**
1. Load `references/youtube-channels.md`. Apply the four-signal heuristic (recency, library currency, track record, reach) — subscriber-count signal floor in [`references/budgets.yaml → research.youtube_subscriber_signal_minimum`](budgets.yaml); track-record minimum in `research.youtube_track_record_months_min`. Not a hard gate.
2. Find 3–6 videos with techniques applicable to this project's motion spec.
3. Watch or read transcripts. Note runtime and exact minute for each technique.
4. Produce `research/youtube-techniques.md`.
5. Update `memory.md`.

**Exit condition:** `research/youtube-techniques.md` exists with 3–6 verified entries.

---

### EXECUTION:STACK

**Entry condition:** Both research files exist. All blueprint artifacts signed off.

**What happens:**
1. Load `agents/implementer-agent.md` + `references/tech-stack.md` + `references/performance-budgets.md`.
2. Read motion spec to determine library cluster (restrained / active / maximalist).
3. Match to meta-framework based on discovery Q10 preference or inferred from content shape.
4. Produce `research/tech-stack.md` with pinned versions, install commands, and rejected alternatives.
5. Present to user. Ask: **"Any stack constraints I missed? Deployment target confirmed?"**
6. On approval: create `decisions/NNN-stack.md`. Update `memory.md`.

**Exit condition:** `research/tech-stack.md` exists AND `User sign-off: YES`.

**Rejection path:**
- User rejects framework → document reason in decisions/, pick the next best option, re-present.
- User adds a constraint (e.g., "must use Cloudflare Workers") → re-evaluate stack against that constraint.

---

### EXECUTION:PLAN

**Entry condition:** `research/tech-stack.md` signed off.

**What happens:**
1. Produce `plan.md` from `assets/templates/plan-template.md`.
2. Produce `phase-1.md`, `phase-2.md`, `phase-3.md` with sequential, imperative, verifiable prompts.
3. Every phase ends with a deployed preview.
4. Present to user. Ask: **"Does this phase breakdown make sense? Any scope that belongs in a different phase?"**
5. On approval: update `memory.md`.

**Exit condition:** `plan.md` + all phase files exist AND `User sign-off: YES`.

**Rejection path:**
- User wants scope moved between phases → restructure. Ensure every phase still ends with something deployable.
- User wants a 4th phase → add it. Document why in decisions/.

---

### EXECUTION:PHASE-1 / PHASE-2 / PHASE-3

**Entry condition:** `plan.md` + relevant `phase-N.md` signed off.

**What happens:**
1. Load `agents/implementer-agent.md`.
2. Execute the phase file's sequential prompts in order. Every step is verifiable.
3. At end of phase: load relevant QA gate file (`qa/phase-N-gate.md`). Run checks.
4. Fix all blockers from the gate before presenting.
5. Present preview URL to user. Ask: **"Anything in this phase that needs changing before we continue?"**
6. On approval: update `memory.md`.

**Exit condition:** Phase built, QA gate passed (no blockers), preview URL live, `User sign-off: YES`.

**Rejection path:**
- QA gate fails → hand report to Implementer Agent. Fix all blockers. Re-run gate. Do not advance until pass.
- User rejects visual result → load relevant agent, identify the section, fix it. Do not rebuild entire phase.
- User changes scope mid-phase → assess impact. If it breaks the phase boundary, move the scope to the next phase. Document in decisions/.

---

### QA:FINAL

**Entry condition:** All three phases built and signed off.

**What happens:**
1. Load `agents/qa-agent.md` + `qa/pre-launch-checklist.md`.
2. Run full Lighthouse audit (mobile + desktop, median of 3 runs).
3. Run axe-core a11y audit.
4. Run cross-browser smoke test (Chrome, Safari, Firefox, mobile).
5. Verify no lorem ipsum, no console errors, all form endpoints live.
6. Produce `qa/final-report.md`.
7. Present to user. On approval: update `memory.md` → Phase = DONE.

**Exit condition:** `qa/final-report.md` exists, all checks pass, `User sign-off: YES`.

**Rejection path:** Any blocker found → fix → re-run the specific check → update report → re-present.

---

### DONE

**State:** Project complete. `memory.md -> Phase: DONE`. No further action unless user reopens scope.

**Optional final step — produce a handoff export.** If the project will be transferred to another team, freelancer, agent, or platform, follow `references/handoff-export.md` to produce a single self-contained artifact (`<project>-handoff.tar.gz`, `.json`, or `.md` bundle). The export contains the full pipeline state, every decision, every QA report, and a copy of the Web Claw skill — so the receiver can resume from a cold start.

If user reopens scope: create a new decision file `decisions/NNN-scope-extension.md`, advance `memory.md` to the relevant phase, and resume.

---

## Sign-Off Gate Protocol

### Interactive mode

At every artifact presentation, the agent must:

1. Show the artifact (or a link to it).
2. Ask a **specific, concrete question** (not "LGTM?"). See each state's sign-off question above.
3. Wait for an explicit answer.
4. If approved: write `User sign-off: YES` in `memory.md` and advance.
5. If changes requested: follow the rejection path. Do not advance.
6. If user says "looks good" or "continue" without answering the specific question: treat as approved. Record it.

**Never advance state without explicit user approval or an explicit "use defaults" statement.**

### Fast mode

At every artifact production, the agent must:

1. Write the artifact.
2. For each judgment call that interactive mode would ask the user about (color palette, motion intensity overrides, signature device, stack choice, page cuts), produce `decisions/NNN-auto-<topic>.md` containing: the decision, the rationale (rooted in `discovery.md` + operating principles), and the rejected alternatives.
3. Run any automated gate for this state (Lighthouse for execution phases, contrast validation for style guide, etc.).
4. If automated gates pass: write `User sign-off: AUTO` and advance.
5. If automated gates fail: follow the degradation rules below.
6. If a true blocker is hit (a question only the user can answer — e.g., legal compliance, payment integration credentials), add it to `memory.md -> Blockers` and proceed with everything else. Surface all accumulated blockers at completion review.

**Automated quality gates are hard in both modes.** A Lighthouse score below the budget blocks the phase whether the user is watching or not.

### Fast mode degradation rules

Defined canonically in [`references/budgets.yaml → fast_mode.*`](budgets.yaml). Behavior summary:

- **Hard blockers** stop advance immediately. The agent fixes the issue, re-runs the gate, and only advances when it passes. Default hard blockers: failed quality gate (Lighthouse / axe / contrast / motion), missing required dependency. The agent retries each quality-gate fail up to `fast_mode.retry_policy.quality_gate_runs` times before treating it as truly hard.
- **Soft blockers** are logged to `memory.md -> Blockers` and the run continues with a degraded artifact. The agent must note what was degraded inline in the artifact (e.g., "Analytics: SKIPPED — provider key not supplied. See blockers."). Default soft blockers: auth-required external URLs, user-only decisions (legal, payment keys), unreachable inspiration sources, missing AI asset API keys.
- **Surface at end**: if `fast_mode.surface_at_end` is true (default), all soft blockers are collected and shown to the user in a single completion review summary, not one-by-one as they accumulate.

Agents must NOT promote a soft blocker to "ignored." Every soft blocker that bypassed a sign-off must be surfaced — silently degraded artifacts are forbidden.

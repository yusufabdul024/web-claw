# Premium Experience Standard — Web Claw v3

The definition of "done" for feel. This file describes the experience a finished Web Claw site must deliver, from the moment the visitor clicks the URL to the moment they leave. The Chief Designer reviews every design and build artifact against it; QA scores against it via `qa/visual-critique-rubric.md`.

The target state: the visitor doesn't feel like they visited a company's website. They feel like they went on an emotional journey to discover what the brand offers — and they leave amazed.

---

## 1. The Arrival — the loading state is the opening scene

- **Never a generic skeleton loader.** The loader is designed: brand wordmark, progress counter, curtain, or a motif drawn from the style guide. It is specified in `design/animations.md` like any other signature moment.
- The loader exists because premium sites carry heavy animation and video assets. It buys time *gracefully* — and hands off into the reveal without a hard cut.
- Budget: the loader appears instantly (no white flash), and total blocking time still respects `references/budgets.yaml -> core_web_vitals`. A loader is not a license to ship a slow site.
- If assets are light enough that no loader is needed, the arrival is still designed: the hero enters deliberately, not by default.

## 2. The Reveal — content enters smoothly

- When loading completes, content is revealed with subtle entrance animations and parallax — not popped in. Zero layout shift (CLS budget holds).
- Video backgrounds are fully loaded or poster-covered before they play; no stutter, no black frames.
- Reveal choreography is staggered: hero first, supporting elements follow in reading order.

## 3. Depth and Composition

- **Big, soft shadows** that ground elements without muddying them.
- **Deliberate z-index layering** — text passing behind images or 3D objects, elements overlapping across section boundaries — always readable, never clunky or cluttered.
- **Contrast** used structurally: dark/light section rhythm, scale jumps, density shifts.
- **Whitespace is intentional.** The screen is not filled with company information; it is deliberately left empty where emptiness directs attention to what matters in that moment. Clean is a decision, not an absence.

## 4. Typography

- Display text is **big and playful, with small deliberate size variations** — not a uniform type ramp applied mechanically.
- The typeface is **intentional**: chosen to argue for the brand, paired per `references/typography-systems.md`, and used at sizes where its personality shows.
- Body text stays disciplined: readable measure, calm rhythm. The play lives in the display layer.

## 5. Motion Language

- **Scroll effects are tuned and flawless** — 60fps, no jank, choreographed to reading rhythm.
- **On-scroll mask reveals** used intentionally for images and headlines.
- **Smooth ease-in slide transitions** for sliders, carousels, and section changes; easing curves specified per `design/animations.md`, never library defaults.
- **A focal storytelling element** where the concept supports it: one item (product, 3D object, motif) that travels with the visitor down the page, carrying the narrative between sections.
- **Micro-interactions everywhere it counts**: hovers, buttons, inputs, cursor — every interactive element acknowledges the user.
- Every motion device has a designed `prefers-reduced-motion` replacement. Reduced is not removed — it is calm, not broken.

## 6. Interactivity and Responsiveness

- The site responds beautifully at every viewport — the premium feel survives on a phone, where most visitors will meet it.
- Interactive elements are obviously interactive; feedback is immediate (< 100ms perceived).
- Touch targets, keyboard focus states, and pointer affordances all hold to `references/accessibility.md`.

## 7. The Emotional Journey

- Each page is structured as an arc: **arrival → intrigue → understanding → desire → action.**
- Sections build on each other; the visitor is *told a story*, not shown a list.
- The close of the journey lands on the one action the brief demands (brief Q4) — by the time the visitor reaches it, they should want to take it.
- Exit feeling: amazed, curious, flooded with dopamine. If a section doesn't move the visitor forward emotionally, cut it.

---

## Hard Constraints (identity never overrides gates)

| Constraint | Source of truth |
|---|---|
| Lighthouse floors | `references/budgets.yaml -> lighthouse.*` |
| Core Web Vitals (LCP, CLS, INP) | `references/budgets.yaml -> core_web_vitals.*` |
| Accessibility / contrast | `references/budgets.yaml -> accessibility.*`, `qa/accessibility-checklist.md` |
| Reduced motion | `scripts/check-reduced-motion.py`, `qa/motion-checklist.md` |
| Bundle weight | `references/budgets.yaml -> bundle.*` |

A site that feels premium but fails a gate is not premium. Fix it.

## Where This File Is Enforced

| Stage | How |
|---|---|
| DESIGN:ANIMATIONS | Every device above must be specified or explicitly ruled out in `design/animations.md` |
| BUILD:PHASE-1..3 | Implementer builds to this standard; loader ships in the first phase that deploys a public preview |
| QA gates | `qa/visual-critique-rubric.md` scores arrival, depth, typography, motion, and journey |
| Chief Designer review | Every artifact checked against this file before client presentation |

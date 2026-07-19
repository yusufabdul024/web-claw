# Operating Principles - Web Claw v3

These principles govern every decision made by every agent in the pipeline. The Chief Designer (`agents/chief-designer.md`) enforces them.

---

## The Brief Is the Foundation

No research and no design until the client interview has produced: what the brand is about, what the site must achieve, what the visitor must do, the one objective, and a value proposition that a stranger understands in 3 seconds. A designer does not start researching from nowhere.

---

## The Client Stays in the Loop

Research is a back-and-forth: findings are verified with the client before being built on. Builds show signature elements the moment they first work, not at the end. Big-bang reveals are how whole builds get rejected. See `references/client-collaboration.md`.

---

## The Arrival Is Designed

The loading state is the opening scene, not a technical apology. Never a generic skeleton loader. Content is revealed smoothly, with zero layout shift, into an emotional journey that ends amazed. The full bar: `references/premium-experience-standard.md`.

---

## Taste Evidence Before Taste Claims

The agent does not declare a site "editorial", "luxury", "playful", "brutalist", "organic", or "Awwwards-level" from internal preference alone.

Every visual or motion direction must be grounded in at least one of:

- user-provided inspiration,
- open-web research,
- companion-skill critique,
- a signed-off moodboard,
- a signed-off decision file.

If the evidence is thin, say so and ask for better references.

---

## User Inspiration Is Primary

The user's references outrank the agent's discoveries. A rough screenshot with a clear user note is more valuable than a famous gallery link with no connection to the brief.

When the user provides a source, record:

- what to borrow,
- what not to copy,
- which page/section it affects,
- copying risk,
- implementation implications.

Do not copy exact layouts, assets, code, copy, color palettes, or animation choreography from any source.

---

## Open-Web Research Is Source-Agnostic

Web Claw v3 does not require Awwwards, YouTube, Dribbble, Pinterest, Behance, Instagram, Mobbin, Land-book, Godly, Lapa Ninja, Siteinspire, Codrops, or any other source.

Use the source that fits the project. A B2B SaaS site may benefit from Mobbin and real product pages. A fashion brand may benefit from Pinterest, Are.na, Instagram, and portfolio/editorial references. A motion-heavy agency site may benefit from award galleries and interaction case studies.

The source is less important than the distillation.

---

## Moodboard Before Design

Do not create sitemap, style guide, wireframes, or motion spec before the moodboard and taste calibration exist.

The moodboard is not decoration. It is the design contract:

- visual mood,
- color/material,
- typography,
- layout/composition,
- imagery,
- motion/interaction,
- copy voice,
- anti-style.

Design artifacts must explicitly trace back to the moodboard.

---

## Companion Skills Are Teammates, Not Dependencies

Proactively look for useful design skills near Web Claw and, when tools allow, in public GitHub/web sources. Consult them when they can improve taste, polish, UX structure, visual critique, or implementation quality.

Companion skills are advisory. Web Claw memory, decisions, budgets, signed-off artifacts, and QA gates remain authoritative.

If a companion skill is unavailable and its absence affects quality, record the fallback in `research/skill-discovery.md` or a decision file.

---

## Taste Over Completeness

A site that includes every requested section but feels forgettable has failed. A site with fewer sections and one unforgettable, appropriate moment is stronger.

Push back on generic briefs. Offer sharper alternatives. Cut what is not earning attention.

---

## One Page, One Job

Each page exists to drive one downstream action. The verb should be measurable: convert, qualify, book, buy, subscribe, apply, compare, trust, or understand.

If a page has three jobs, split it or remove two jobs.

---

## One Signature Device Per Page

Each page gets one signature section or interaction. The rest of the page supports it with restraint.

Five "wow" moments on one page is no wow moment.

---

## Constraints Sharpen Design

Budgets are non-negotiable. Numeric thresholds live in `references/budgets.yaml`.

- Performance: Lighthouse and lab metrics.
- Accessibility: WCAG, contrast, keyboard, screen-reader, reduced motion.
- Motion: frame-rate, duration, long-task, concurrent animation budgets.
- Bundle: JS, CSS, fonts, images, page weight.

If a visual idea breaks a budget, simplify the idea or change the implementation.

---

## Mobile Is The Design

Design mobile first. Desktop is additive.

Every key decision must survive 375px width, touch input, slow mobile CPU, and reduced motion. A signature moment that only works on desktop is not the signature moment; it is the desktop variant.

---

## Reduced Motion Is Design

Reduced motion is not "turn animations off." Replace the experience:

- pinned scroll becomes stacked content,
- scrubbed canvas becomes static sequence,
- parallax becomes composition,
- cursor interaction becomes touch affordance,
- motion storytelling becomes copy/sequence.

The page must still tell the story.

---

## Copy Is Design

No lorem ipsum. No vague placeholders. No "Welcome to our website."

If the user lacks copy, generate sharp draft copy from discovery and moodboard. Mark it as draft only when it needs factual/user approval.

---

## Show, Do Not Summarize

Artifacts must contain concrete copy, concrete file paths, concrete tokens, concrete component names, concrete motion timings, concrete sources, and concrete QA evidence.

"Add a beautiful hero" is forbidden. "Hero H1: ..., component: ..., source inspiration: ..., motion: ..." is required.

---

## The Filesystem Remembers

Project state lives in `memory.md`, `decisions/`, `design/`, `research/`, and `qa/`.

Do not rely on chat history. Do not re-litigate signed-off decisions. Do not regenerate from scratch when an approved artifact exists.

---

## Anti-Patterns Across Agents

- Accepting "modern" or "clean" as enough taste direction.
- Building designs before moodboard and taste calibration.
- Treating Awwwards/YouTube or any single source as mandatory.
- Citing inspiration without saying what not to copy.
- Using Dribbble/Pinterest/Instagram as implementation proof. They can inform mood, not technical feasibility.
- Ignoring companion skills that are locally available.
- Letting companion advice override user constraints or QA gates.
- Producing placeholder copy or placeholder imagery as final.
- Installing a library without a specific job in `tech-stack.md`.
- Specifying motion without a reduced-motion replacement.
- Running Lighthouse only on localhost.
- Moving to the next state with `User sign-off: PENDING`.

# Operating Principles — Web Claw

These principles govern every decision made by every agent in the pipeline. When in doubt about a judgment call, return here.

---

## Taste over completeness

Award-winning is not a checklist. The agents have opinions — let them defend choices. If a request would produce something generic, push back; offer something the user did not ask for but should want.

A site that has every section the user requested but feels forgettable has failed. A site that has fewer sections but one unforgettable moment has succeeded.

---

## Constraints sharpen design

Always pin three budgets up front and refuse to violate them. **All numeric thresholds live in [`references/budgets.yaml`](budgets.yaml) — single source of truth.** The summary below is illustrative; the YAML is authoritative.

- **Performance:** Lighthouse mobile category floors and Core Web Vitals (see `lighthouse.mobile.*` and `core_web_vitals.*`).
- **Accessibility:** WCAG level + axe violation budgets + contrast minimums (see `accessibility.*`).
- **Motion:** Frame-rate floor and entrance/signature animation duration caps (see `motion.*`).

These are guardrails that turn *flashy* into *award-winning*. They are non-negotiable. Do not let an animation override them. Do not let a design choice override them.

---

## Phases ship

Every phase file must end with a thing that is deployed and visible. No phase ends with "now wire it up" — wiring up is part of the phase. If you cannot deploy at the end of a phase, the phase is wrong.

Phase 1: ugly but visible.
Phase 2: animated and polished.
Phase 3: launch-ready.

---

## Research before invention

Before specifying any signature animation or interaction, the Researcher Agent pulls Awwwards SOTD references and YouTube walkthroughs. The count and credibility thresholds live in [`references/budgets.yaml → research.*`](budgets.yaml) (see `awwwards_min_entries`, `youtube_min_entries`, `youtube_subscriber_signal_minimum`, etc.). Subscriber count is a *signal*, not a hard gate — applied alongside the four-signal heuristic documented in `references/youtube-channels.md`. The motion spec must say "adapted from technique X by creator Y" — not "we invented a parallax." This is the difference between a hack and a craft.

---

## Show, don't summarize

Every deliverable contains concrete code, concrete copy, concrete component names, concrete file paths. "Add a hero with engaging copy" is forbidden. "Hero copy reads exactly: '…'. Component file: `app/(marketing)/components/Hero.tsx`. Animation: 1.2s ease-out cubic, opacity 0→1 + y 24→0, staggered 80ms across H1 words." is required.

---

## Mobile is the design

Design mobile-first, animate mobile-first, perf-budget mobile-first. Desktop is the easy case. Every Lighthouse run is mobile-primary. Every responsive review starts at 375px.

---

## Accessibility is design

Motion-reduced users, keyboard users, screen-reader users get a first-class experience. If a signature scroll-jacked section breaks for `prefers-reduced-motion: reduce`, the section is wrong. Reduced motion fallbacks are specified alongside every animation — not added in Phase 3 as an afterthought.

---

## Copy is design

The Designer Agent and UX Strategy Agent both have authority over copy. Never let the user ship Lorem ipsum or stock filler. If the user does not have copy, generate sharp, opinionated copy in their voice — from discovery Q2 (the one-sentence description) as the seed. Every headline is real. Every CTA label is real.

---

## The filesystem remembers, the model executes

Project state lives in `memory.md` and `decisions/`. The context window is a working surface, not storage. Any agent can resume any project from `memory.md` alone. Decisions are never re-litigated if a `decisions/NNN.md` file exists. Artifacts are never regenerated from scratch if they already exist and are signed off.

---

## One page, one job

Each page exists to drive one downstream action. If a page is doing three jobs, split it or kill two of the jobs. The sitemap is a strategy artifact, not a list of things to build because they seem relevant.

---

## The first 1.5 seconds are the audition

Above-the-fold entrance must communicate the brand in 1.5 seconds. No entrance animation that runs longer than 1.2 seconds total. No staggering 18 words over 4 seconds. Snap it on. The user already decided to be interested — reward them with content, not choreography.

---

## Anti-patterns (across all agents)

- ❌ Accepting "modern" or "clean" as a vibe answer. Demand three adjectives.
- ❌ Moving to the next state before the user signs off the current artifact.
- ❌ Skipping `memory.md` read at session start.
- ❌ Skipping `memory.md` write at session end.
- ❌ Producing lorem ipsum or placeholder copy in any deliverable.
- ❌ Installing a library without a specific job in `tech-stack.md`.
- ❌ Specifying an animation without a reduced-motion fallback.
- ❌ Running Lighthouse on localhost instead of the deployed preview.
- ❌ Citing an Awwwards site you did not verify at runtime.
- ❌ Re-asking a question that is already answered in `memory.md` or `decisions/`.

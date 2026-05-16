# Phase 2 — Interactions

**Project:** <name>
**Phase:** 2 of 3
**Goal:** Animations live, signature sections shipped, micro-interactions polished. Site still deployed and still meets perf budget.
**Estimated effort:** <hours / days>
**Inputs:** Phase 1 deployed preview, `blueprint/animations.md`, `research/*`
**Output:** Deployed preview with full motion + signed-off QA.

---

## Pre-flight

- [ ] Phase 1 sign-off complete.
- [ ] `blueprint/animations.md` signed off.
- [ ] Research dossier (`research/awwwards-references.md`, `research/youtube-techniques.md`) reviewed.
- [ ] Repo on a fresh branch: `phase-2-interactions`.

---

## Sequential prompts

### Step 1 — Install motion libraries

1.1  From `research/tech-stack.md`, identify the motion cluster.
1.2  Install: `pnpm add <packages>`. Example for active intensity:
     ```
     pnpm add framer-motion@^11 lenis@^1.1
     ```
     Example for maximalist: add `gsap@^3.12` and `@react-three/fiber @react-three/drei three` if needed.
1.3  Commit: `chore(deps): install motion libraries`.

**Success:** No type errors; package.json updated.

---

### Step 2 — Wire global smooth scroll (if applicable)

2.1  Skip this step if motion intensity = restrained.

2.2  Create `src/components/SmoothScroll.tsx`:

```tsx
'use client';
import { useEffect } from 'react';
import Lenis from 'lenis';

export function SmoothScroll() {
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const lenis = new Lenis({ lerp: 0.1, duration: 1.2, smoothWheel: true });
    let rafId: number;
    const raf = (time: number) => { lenis.raf(time); rafId = requestAnimationFrame(raf); };
    rafId = requestAnimationFrame(raf);
    return () => { cancelAnimationFrame(rafId); lenis.destroy(); };
  }, []);
  return null;
}
```

2.3  Mount `<SmoothScroll />` in `src/app/layout.tsx`.

2.4  Add `html { overscroll-behavior: none; }` to globals.css.

2.5  Manual verify: Chrome desktop scroll feels eased; native scroll when DevTools "Emulate prefers-reduced-motion: reduce".

2.6  Commit: `feat(scroll): Lenis smooth scroll with reduced-motion bypass`.

---

### Step 3 — Implement above-the-fold entrance per page

For each page in `animations.md`:

3.1  Identify the entrance block (the table in `animations.md` per page).
3.2  Wrap the hero in a `<motion.div>` (Framer Motion) or a `gsap.timeline()` (GSAP).

Example using Framer Motion:

```tsx
'use client';
import { motion } from 'framer-motion';
const ease = [0.25, 1, 0.5, 1];

export function HeroEntrance({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        hidden: {},
        visible: { transition: { staggerChildren: 0.08, delayChildren: 0.08 } }
      }}
    >
      {children}
    </motion.div>
  );
}
```

3.3  Apply staggered children with `variants` and `motion.h1`, `motion.p`, etc.
3.4  Honor reduced motion: Framer Motion's `useReducedMotion()` hook returns true → render without variants.
3.5  Verify visually at mobile + desktop.
3.6  Commit per page: `feat(<page>): entrance choreography`.

---

### Step 4 — Implement section reveals (default pattern)

4.1  Create `src/components/Reveal.tsx`:

```tsx
'use client';
import { motion, useReducedMotion } from 'framer-motion';

export function Reveal({ children, delay = 0 }: { children: React.ReactNode; delay?: number }) {
  const reduce = useReducedMotion();
  return (
    <motion.div
      initial={reduce ? { opacity: 0 } : { opacity: 0, y: 24 }}
      whileInView={reduce ? { opacity: 1 } : { opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: reduce ? 0.2 : 0.8, delay, ease: [0.25, 1, 0.5, 1] }}
    >
      {children}
    </motion.div>
  );
}
```

4.2  Wrap each section (or each first-level child within a section) on every page.

4.3  Verify scroll behavior at mobile + desktop.

4.4  Commit: `feat(reveal): default section reveal pattern`.

---

### Step 5 — Implement the signature section(s)

For each page's SIGNATURE section in `animations.md`:

5.1  Read the spec verbatim.
5.2  Check the dossier (`research/awwwards-references.md`, `research/youtube-techniques.md`) for adaptation source.
5.3  Implement following the spec to the millisecond.
5.4  Add reduced-motion alternative (described in `animations.md`).
5.5  Test at the throttled Pixel 6a profile — verify ≥ 58fps and INP ≤ 200ms during pin.
5.6  Test exit conditions (Esc, high scroll velocity).
5.7  Commit: `feat(<page>): signature section — <name>`.

This step is the longest in Phase 2. Treat each signature section as its own mini-project.

---

### Step 6 — Implement micro-interactions

6.1  Buttons — apply hover/focus/active states from `animations.md` § Micro-interactions.
6.2  Links — underline animation on hover.
6.3  Inputs — focus ring expansion.
6.4  Cards — hover lift.
6.5  All with reduced-motion branches.
6.6  Commit: `feat(ui): micro-interactions across components`.

---

### Step 7 — Page transitions

7.1  Choose: Instant / Crossfade / Shared element (per `animations.md`).
7.2  If View Transitions API: wrap navigations with `document.startViewTransition(() => router.push(...))`.
7.3  If Framer Motion shared element: use `<motion.div layoutId="…" />` on source + destination.
7.4  Reset scroll position on navigation.
7.5  Test on Chrome + Safari (View Transitions support varies).
7.6  Commit: `feat(transitions): page transitions`.

---

### Step 8 — Cursor (if applicable)

8.1  Skip if motion intensity = restrained or discovery says no.
8.2  Implement custom cursor (`src/components/Cursor.tsx`).
8.3  Hide on `hover: none` media query (mobile).
8.4  Hide for `prefers-reduced-motion: reduce`.
8.5  Add magnetic targets (`data-magnetic` attribute on buttons / links).
8.6  Commit: `feat(cursor): custom cursor with magnetic targets`.

---

### Step 9 — Performance verification

9.1  Run `scripts/audit-perf.py <preview-url>` (mobile preset). The script exits non-zero if any floor in `web-claw/references/budgets.yaml -> lighthouse.mobile.*` is missed.
9.2  Verify mobile Performance still meets `lighthouse.mobile.performance` (some drop from Phase 1 is expected — animations cost; falling below the floor is a fail).
9.3  Inspect TBT and INP; if INP exceeds `core_web_vitals.inp_ms_max` during animation, identify the bottleneck and simplify.
9.4  Inspect main thread during the signature section's pin. Should be ≤ 16ms/frame.

---

### Step 10 — Deploy preview

10.1  Push branch. Wait for Vercel build.
10.2  Open preview on real mobile device.
10.3  Scroll through every page. Watch for jank.
10.4  Toggle reduced-motion (iOS: Settings > Accessibility > Motion > Reduce Motion). Re-test.
10.5  If anything janks or breaks, return to the relevant step.

---

### Step 11 — QA pass

11.1  Open `qa/motion-checklist.md` — verify each animation matches its spec.
11.2  Open `qa/performance-checklist.md` — verify the budgets.
11.3  Re-run `qa/accessibility-checklist.md` — animations must not have regressed a11y.
11.4  Write the QA report at `qa/phase-2-report.md`.

---

### Step 12 — Sign-off

12.1  Send the preview URL to the user.
12.2  Walk through every signature moment with them.
12.3  Capture feedback.
12.4  Apply revisions.
12.5  Update `plan.md`: "Phase 2 complete on <date>".

**Phase 2 is done when:**

- [ ] Every animation in `animations.md` is implemented.
- [ ] Every animation has a reduced-motion alternative.
- [ ] All micro-interactions match the global pattern.
- [ ] Page transitions match the chosen pattern.
- [ ] Lighthouse mobile Performance ≥ 90.
- [ ] No console errors during scroll.
- [ ] QA report filed.
- [ ] User has approved.
- [ ] Ready to execute `phase-3.md`.

---

## What Phase 2 deliberately does NOT include

- Real form submission (still placeholder).
- Real analytics events.
- Production domain.
- Production CSP / security headers (basic ones OK; production-grade in Phase 3).
- Final copy review (substantial copy changes happen in Phase 3).

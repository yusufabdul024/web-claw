# Phase 1 — Foundation

**Project:** <name>
**Phase:** 1 of 3
**Goal:** Static, deployable site. Every page from the sitemap exists with real copy. No animations yet.
**Estimated effort:** <hours / days>
**Inputs:** `plan.md`, `blueprint/*`, `research/tech-stack.md`
**Output:** Deployed preview URL + sign-off from user.

---

## Pre-flight

Before starting:

- [ ] `plan.md` signed off by user.
- [ ] `research/tech-stack.md` signed off.
- [ ] Repo exists; Vercel (or chosen host) project linked.
- [ ] You have write access to the working directory.

---

## Sequential prompts

Each step is an executable instruction. Run them in order. Verify the success condition before moving to the next step.

### Step 1 — Scaffold the framework

1.1  Run: `pnpm create next-app@latest <project-name> --typescript --tailwind --app --import-alias "@/*" --src-dir`
1.2  Open the project in your editor.
1.3  Run `pnpm dev`. Verify the default Next.js page loads at http://localhost:3000.
1.4  Commit: `chore: scaffold Next.js app`.

**Success:** Default page renders; no errors in console.

---

### Step 2 — Wire design tokens

2.1  Open `blueprint/style-guide.md`. Extract color, type, spacing, radius, motion tokens.

2.2  Create `tailwind.config.ts` extensions in `theme.extend`:

```ts
theme: {
  extend: {
    colors: {
      neutral: { 50: '#FAFAF7', /* ... all 11 steps from style-guide.md */ },
      accent:  { 500: '#FF4F2C', /* ... */ },
    },
    fontFamily: {
      display: ['<font-display-name>', 'serif'],
      body:    ['<font-body-name>', 'system-ui', 'sans-serif'],
    },
    spacing: { /* token values from style-guide.md */ },
    borderRadius: { /* token values */ },
    transitionDuration: { instant: '100ms', quick: '200ms', paced: '480ms', narrative: '900ms' },
    transitionTimingFunction: {
      'out-quart': 'cubic-bezier(0.25, 1, 0.5, 1)',
      'out-back':  'cubic-bezier(0.34, 1.56, 0.64, 1)',
      'in-out-cubic': 'cubic-bezier(0.65, 0, 0.35, 1)',
    },
  }
}
```

2.3  Add CSS custom properties as a fallback in `src/app/globals.css`:

```css
:root {
  --color-accent-500: #FF4F2C;
  --duration-quick: 200ms;
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  /* full set from style-guide.md */
}
```

2.4  Add fonts via `next/font`. In `src/app/layout.tsx`:

```ts
import { Inter, /* display font import */ } from 'next/font/google';
const body = Inter({ subsets: ['latin'], display: 'swap', variable: '--font-body' });
const display = /* … */ ;
```

2.5  Commit: `feat(design-system): wire tokens from style-guide.md`.

**Success:** Tailwind classes using the new colors / fonts work; tokens visible in computed styles.

---

### Step 3 — Build the component library

For each component in `blueprint/wireframes.md` "Component inventory":

3.1  Create `src/components/<ComponentName>.tsx`.
3.2  Implement the variants and props exactly as wireframed.
3.3  Build the static visual layout (no animations).
3.4  Storybook-style: add a quick visual test by importing the component into a `/dev/components` page and rendering it.
3.5  Verify the component matches the wireframe at mobile + desktop.

Order to build (least dependent → most dependent):

- `<Button>` (variants: primary, secondary, ghost; states: hover, focus, active, disabled, loading)
- `<Input>`, `<Textarea>` (states)
- `<Card>`
- `<Stat>`
- `<FeatureCard>`
- `<Testimonial>`
- `<PricingCard>`
- `<FAQItem>` (use native `<details>`/`<summary>`)
- `<LogoBar>`
- `<Hero>` (all variants)
- `<FeatureSection>` (all variants)
- `<CTABlock>` (all variants)
- `<Nav>` (and `<MobileDrawer>`)
- `<Footer>`

3.x  After each component, commit: `feat(ui): <ComponentName>`.

**Success:** Every component renders at the wireframed dimensions, with correct hierarchy.

---

### Step 4 — Assemble pages

For each page in `blueprint/sitemap.md`:

4.1  Create the page file (`src/app/<route>/page.tsx` for App Router; `src/pages/<route>.astro` for Astro).
4.2  Import and compose the components per the sitemap's section order.
4.3  Wire the real copy from `sitemap.md` (H1, sub, CTAs).
4.4  Wire SEO metadata (per page `metadata` export in Next.js, or `<head>` in Astro):

```ts
export const metadata: Metadata = {
  title: '<from sitemap.md>',
  description: '<from sitemap.md / discovery.md>',
  openGraph: { title, description, images: [{ url: '/og/<page>.png' }] },
};
```

4.5  Verify each page renders at mobile + desktop.
4.6  Commit per page: `feat(<route>): page assembly`.

**Success:** Every URL in the sitemap returns a rendered page that matches the wireframe.

---

### Step 5 — Accessibility scaffolding

5.1  In `layout.tsx`, add `<html lang="en">`, semantic landmarks (`<header>`, `<main>`, `<footer>`).
5.2  Add a skip-to-content link as the first focusable element:

```tsx
<a href="#main" className="skip-link sr-only focus:not-sr-only ...">Skip to content</a>
```

5.3  Verify `<main id="main">` is on every page.
5.4  Add focus-visible styles globally:

```css
:focus-visible { outline: 3px solid var(--color-accent-500); outline-offset: 2px; }
```

5.5  Verify keyboard navigation works on home: Tab moves through nav, hero CTA, every section's CTA, footer.
5.6  Run axe DevTools on the home page; resolve any violations.
5.7  Commit: `feat(a11y): semantic landmarks + skip-link + focus styles`.

**Success:** axe DevTools on home returns 0 violations.

---

### Step 6 — Image handling

6.1  For every image in wireframes, use the framework's image component (`<Image>` from `next/image`, `<Image>` from `astro:assets`).
6.2  Set explicit `width` and `height` (or `aspect-ratio` CSS).
6.3  Set `priority` on the hero image.
6.4  Set `loading="lazy"` and `decoding="async"` on below-the-fold images.
6.5  If real images aren't ready, use placeholder images at the correct aspect ratio (e.g., `https://placehold.co/1920x1080/`).
6.6  Commit: `feat(images): use framework image components with explicit dimensions`.

**Success:** No CLS warnings from Lighthouse.

---

### Step 7 — Deploy preview

7.1  Push the branch to GitHub.
7.2  Verify Vercel deployment kicks off automatically.
7.3  Wait for build. Get the preview URL.
7.4  Open the preview URL on mobile (real device or DevTools mobile mode).
7.5  Click through every page. Verify.
7.6  Open Lighthouse mobile audit on the preview URL.

**Success criteria** (numbers in `web-claw/references/budgets.yaml -> lighthouse.mobile.*`):
- [ ] Lighthouse mobile Performance meets `lighthouse.mobile.performance`.
- [ ] Lighthouse mobile Accessibility meets `lighthouse.mobile.accessibility`.
- [ ] Lighthouse mobile Best Practices meets `lighthouse.mobile.best_practices`.
- [ ] Lighthouse mobile SEO meets `lighthouse.mobile.seo`.

---

### Step 8 — QA pass

8.1  Open `qa/accessibility-checklist.md` — work through every item.
8.2  Open `qa/responsive-checklist.md` — test at 8 breakpoints.
8.3  Open `qa/cross-browser-checklist.md` — load preview in Chrome, Safari, Firefox.
8.4  Write the QA report at `qa/phase-1-report.md` using the format in `agents/qa-agent.md`.
8.5  Resolve any defects before declaring Phase 1 done.

---

### Step 9 — Sign-off

9.1  Send the preview URL to the user.
9.2  Walk them through every page.
9.3  Capture feedback inline.
9.4  Apply small revisions (copy tweaks, image swaps).
9.5  Update sign-off in `plan.md`: "Phase 1 complete on <date>".

**Phase 1 is done when:**

- [ ] All success criteria above are checked.
- [ ] User has reviewed the preview and approved.
- [ ] QA report is filed.
- [ ] Ready to execute `phase-2.md`.

---

## What Phase 1 deliberately does NOT include

- Any JS-driven animation (no Framer Motion, no GSAP usage).
- Smooth scroll (no Lenis yet).
- Custom cursors.
- Signature section motion (the static placeholder lives here; the motion lives in Phase 2).
- Real form submission (forms render but don't submit yet).
- Analytics.
- Production domain (preview only).

Defer all of those to Phase 2 or Phase 3.

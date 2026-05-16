# Phase 1 QA Gate — Static Deploy Check

Run this gate after Phase 1 build, before presenting to user. Fix all ❌ before advancing.

**Goal:** The site is visible, navigable, structurally correct, and has no blocking errors. No animations required yet.

---

## 1. Deploy

- [ ] Site is deployed to a public preview URL (not localhost)
- [ ] All pages in the sitemap load without 404 or 500 errors
- [ ] No console errors on any page

Run: `scripts/audit-perf.py <preview-url>` — paste output, verify no 404s in network tab.

---

## 2. Structure

- [ ] All sections from `wireframes.md` are present on each page
- [ ] All copy from `sitemap.md` is present (no lorem ipsum anywhere)
- [ ] All CTAs link to real destinations (or a placeholder `/thank-you` page)
- [ ] Navigation works: every nav link reaches its page

---

## 3. Design tokens

- [ ] CSS custom properties from `style-guide.md` are applied globally
- [ ] Heading font loads correctly (no FOUT fallback visible after load)
- [ ] Body font loads correctly
- [ ] Color tokens match `style-guide.md` exactly (spot-check: H1 color, background, CTA button)

---

## 4. Responsive

Check at: 375px, 768px, 1280px, 1920px.

- [ ] No horizontal scroll at any breakpoint
- [ ] No text overflow or clipping
- [ ] Navigation is usable on mobile (hamburger or equivalent)
- [ ] Images are not distorted

For detail: load `qa/responsive-checklist.md`.

---

## 5. Accessibility basics

- [ ] All images have non-empty `alt` text (or `alt=""` for decorative)
- [ ] Page has a single `<h1>` per page
- [ ] Heading hierarchy is correct (no skipped levels)
- [ ] All interactive elements are keyboard-reachable (Tab through the page)
- [ ] Focus indicator is visible on all interactive elements

Run: `scripts/check-a11y.py <preview-url>` for automated check. Paste output.

---

## 6. Performance baseline

Numeric thresholds derive from [`references/budgets.yaml → lighthouse.mobile.*`](../references/budgets.yaml). Phase 1 has no animation cost yet, so Lighthouse should typically clear the floor with margin.

- [ ] Lighthouse mobile Performance meets `lighthouse.mobile.performance` floor.
- [ ] No render-blocking resources (fonts preloaded, critical CSS inlined or minimal).
- [ ] Hero image uses correct format (WebP or AVIF, not PNG for photos).

Run: `scripts/audit-perf.py <preview-url>` on mobile preset (the script reads budgets.yaml and returns non-zero if any floor is missed).

---

## Gate Result

If all items pass: advance to EXECUTION:PHASE-2. Update `memory.md`.

If any item fails: hand to Implementer Agent with this report. Fix all ❌. Re-run gate. Do not advance until pass.

Write result to `qa/phase-1-report.md`.

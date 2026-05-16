# Performance Budgets

The numbers Web Claw projects must hit. The Implementer Agent designs around these from day one; the QA Agent enforces them between phases.

**Numeric thresholds are canonical in [`references/budgets.yaml`](budgets.yaml).** This document explains the *why* behind each budget. If numbers shown below ever drift from `budgets.yaml`, `budgets.yaml` wins — open an issue and reconcile.

## The four budgets

### 1. Lighthouse mobile scores

| Category        | Source in budgets.yaml                       |
|-----------------|----------------------------------------------|
| Performance     | `lighthouse.mobile.performance`              |
| Accessibility   | `lighthouse.mobile.accessibility`            |
| Best Practices  | `lighthouse.mobile.best_practices`           |
| SEO             | `lighthouse.mobile.seo`                      |

Mobile is the gate. Desktop floors are higher (`lighthouse.desktop.*`) and are an additive expectation, not a substitute.

### 2. Core Web Vitals (mobile, p75 over 28 days)

| Metric                          | Floor   | Good   |
|---------------------------------|---------|--------|
| LCP (Largest Contentful Paint)  | ≤ 2.5s  | ≤ 1.8s |
| INP (Interaction to Next Paint) | ≤ 200ms | ≤ 100ms|
| CLS (Cumulative Layout Shift)   | ≤ 0.10  | ≤ 0.05 |
| FCP (First Contentful Paint)    | ≤ 1.8s  | ≤ 1.0s |
| TBT (Total Blocking Time)       | ≤ 200ms | ≤ 100ms|
| TTFB (Time to First Byte)       | ≤ 600ms | ≤ 200ms|

### 3. Bundle budgets

For a marketing site:

| Asset class             | Mobile budget | Desktop budget |
|-------------------------|---------------|----------------|
| HTML                    | ≤ 30 kb       | ≤ 30 kb        |
| CSS (critical)          | ≤ 20 kb       | ≤ 30 kb        |
| JS (initial)            | ≤ 80 kb       | ≤ 150 kb       |
| JS (total per page)     | ≤ 200 kb      | ≤ 350 kb       |
| Fonts (total)           | ≤ 200 kb      | ≤ 200 kb       |
| Hero image (LCP)        | ≤ 100 kb      | ≤ 200 kb       |
| Per-page total transfer | ≤ 1.5 MB      | ≤ 2.5 MB       |

For a maximalist site with 3D, raise the JS-per-page-total to 600 kb mobile / 1 MB desktop, but lazy-load the 3D bundle and ensure it isn't on the critical path.

### 4. Motion budget

- Frame rate during animation: ≥ 58fps on a Pixel 6a (real device or DevTools 4× CPU + Slow 4G).
- Active simultaneous animations at any frame: ≤ 5.
- Total RAF callbacks running at any time: ≤ 1 (use a single ticker, coalesce subscribers).
- INP during animation: still ≤ 200ms (don't block input).

## How to hit the budgets

### LCP

The Largest Contentful Paint is almost always the hero image or the H1 text.

- Preload the LCP image: `<link rel="preload" as="image" href="..." imagesrcset="..." imagesizes="...">`.
- Use modern formats: AVIF (best compression) or WebP (broader support). Fall back to JPEG.
- Serve responsive: `srcset` with sizes at 1×, 2×, 3× per breakpoint.
- Inline critical CSS for the above-the-fold.
- Self-host fonts (or use `next/font`) so font requests don't blow LCP.

For Next.js: `<Image priority />` on the hero. For Astro: `<Image loading="eager" />`.

### INP

The number that replaced FID. Reflects responsiveness during interaction.

- Avoid heavy JS on click handlers — defer to `requestIdleCallback`.
- Don't reflow on scroll — use `transform`, not `width`/`top`/`left`.
- Throttle scroll handlers via RAF.
- Use `content-visibility: auto` on below-the-fold sections.
- Code-split per route.

### CLS

Layout shift = nothing should jump after first paint.

- Reserve space for images: always set `width` + `height` attributes (or `aspect-ratio` CSS).
- Reserve space for ads / embeds with a wrapper at known dimensions.
- Use `font-display: swap` AND match the fallback font's metrics (`size-adjust`, `ascent-override`, `descent-override`).
- Avoid inserting DOM above existing content after first paint. Toasts, banners — append, don't prepend.

### TBT

Total Blocking Time = how much main thread is blocked > 50ms during load.

- Defer non-critical JS.
- Lazy-load third-party scripts (analytics, chat widgets).
- Avoid synchronous hydration of huge components — code-split.
- Use Web Workers for any CPU-heavy work.

### Font budget

- Variable fonts when using 3+ weights or animating weight.
- Static cuts when using ≤ 2 weights (often smaller total).
- Subset to `latin` + `latin-ext` only unless multilingual.
- WOFF2 only.
- Preload the body font.
- `font-display: swap`.

### Image budget

- AVIF for content images, JPEG fallback.
- Responsive `srcset` at real breakpoints (375, 768, 1280, 1920).
- Lazy-load below-the-fold with `loading="lazy"` + `decoding="async"`.
- Don't ship 3000px-wide images. Cap at 1920w for hero, 1280w for body.

### JS budget — the hardest

- React + Next.js + Framer Motion + Lenis is ~120 kb. That's most of your initial JS budget right there.
- Dynamic-import maximalist libraries on the route they're needed (e.g., `import('three')` only on the page with the 3D scene).
- Tree-shake aggressively. Drei specifically — import only the helpers you use (`import { useGLTF } from '@react-three/drei'` not `import * from '@react-three/drei'`).
- Avoid moment.js (use `Intl.DateTimeFormat`). Avoid lodash (use individual lodash-* packages or rewrite). Avoid axios (use `fetch`).

## Measuring

### In dev

- Chrome DevTools Performance tab. Throttle CPU 4× and network Slow 4G.
- Lighthouse on the deployed preview, not localhost.
- Run Lighthouse 3 times, take the median.

### In CI

- `@axe-core/playwright` for a11y.
- `lighthouse-ci` for perf.
- Set assertions: `assertions: { "categories:performance": ["error", {"minScore": 0.90}] }`.

### In production

- Vercel Speed Insights (if on Vercel) for real-user metrics.
- Google Search Console > Core Web Vitals for p75 across the field.
- Plausible's "engagement" stats as a behavioral proxy.

## Common perf killers (and fixes)

| Symptom                                       | Likely cause                                                | Fix                                                 |
|-----------------------------------------------|-------------------------------------------------------------|-----------------------------------------------------|
| LCP > 3s on mobile                            | Hero image too big or not preloaded                          | Preload, AVIF, responsive srcset                    |
| CLS > 0.15                                    | Image dimensions not declared                                | Set `width`/`height` or `aspect-ratio`              |
| TBT > 400ms on home                           | Heavy JS hydration (Framer Motion + Three.js eager)          | Code-split, dynamic import for 3D                   |
| Slow page-to-page transitions                 | Not using framework's prefetch                               | Use `<Link>` (Next.js) or `<a>` w/ prefetch (Astro) |
| Lighthouse "Avoid serving legacy JavaScript"  | Babel targeting old browsers                                 | Set browserslist to modern targets                  |
| "Reduce unused CSS"                           | Tailwind with no purge or shipping unused theme              | Tailwind purges by default; verify content paths     |
| "Eliminate render-blocking resources"         | Synchronous third-party scripts                              | Defer or async; load on idle                        |
| Fonts cause FOIT > 1s                         | Wrong font-display, no preload                               | `font-display: swap` + preload                      |
| Janky scroll on maximalist site               | Multiple RAFs or scroll handlers                             | Coalesce into one ticker; use Lenis's RAF           |

## Production checks at every phase

| Phase   | Performance check (numbers from `references/budgets.yaml`)   |
| ------- | ------------------------------------------------------------ |
| Phase 1 | Lighthouse mobile Performance meets `lighthouse.mobile.performance` (no JS animations yet — should clear with margin). |
| Phase 2 | Lighthouse mobile Performance still meets `lighthouse.mobile.performance`. INP meets `core_web_vitals.inp_ms_max` during the signature section's pin. |
| Phase 3 | All four Lighthouse mobile categories meet `lighthouse.mobile.*` floors. CWV pass per `core_web_vitals.*` on the deployed preview. CLS at or below `core_web_vitals.cls_max`. |

If Phase 2's animations drop Performance below the floor, the Animator's spec was too ambitious — simplify the signature section or lazy-load it harder.

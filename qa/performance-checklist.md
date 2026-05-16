# Performance Checklist

Run after every phase. Numeric floors are canonical in [`references/budgets.yaml`](../references/budgets.yaml) and explained in `references/performance-budgets.md`.

## Lighthouse scores (median of 3 runs, mobile)

- [ ] Performance meets `budgets.yaml -> lighthouse.mobile.performance`.
- [ ] Accessibility meets `budgets.yaml -> lighthouse.mobile.accessibility`.
- [ ] Best Practices meets `budgets.yaml -> lighthouse.mobile.best_practices`.
- [ ] SEO meets `budgets.yaml -> lighthouse.mobile.seo`.
- [ ] Desktop run meets the (higher) `lighthouse.desktop.*` floors.

`scripts/audit-perf.py` returns non-zero if any floor is missed.

Command:

```bash
python <web-claw>/scripts/audit-perf.py https://<preview-url> --device mobile
```

## Core Web Vitals (mobile)

- [ ] LCP ≤ 2.5s (target ≤ 1.8s).
- [ ] INP ≤ 200ms (target ≤ 100ms).
- [ ] CLS ≤ 0.10 (target ≤ 0.05).
- [ ] FCP ≤ 1.8s.
- [ ] TBT ≤ 200ms.
- [ ] TTFB ≤ 600ms.

## Bundle budgets

Per page on mobile:

- [ ] HTML ≤ 30 kb.
- [ ] CSS (critical) ≤ 20 kb.
- [ ] JS initial ≤ 80 kb.
- [ ] JS total per page ≤ 200 kb (or ≤ 600 kb if maximalist 3D is justified).
- [ ] Fonts total ≤ 200 kb.
- [ ] Hero / LCP image ≤ 100 kb (mobile) / ≤ 200 kb (desktop).
- [ ] Total transfer per page ≤ 1.5 MB (mobile) / 2.5 MB (desktop).

## Images

- [ ] LCP image is preloaded (`<link rel="preload" as="image">`).
- [ ] LCP image uses `priority` (Next.js) or `loading="eager"` (Astro).
- [ ] Below-the-fold images use `loading="lazy"` + `decoding="async"`.
- [ ] Modern format (AVIF or WebP) with JPEG fallback.
- [ ] Responsive `srcset` set at real breakpoints.
- [ ] Every image has explicit `width` + `height` (or `aspect-ratio`).

## Fonts

- [ ] WOFF2 only (no WOFF/TTF fallback files shipped).
- [ ] Subset to `latin` (or `latin-ext` if needed).
- [ ] Body font preloaded.
- [ ] `font-display: swap`.
- [ ] Fallback metrics matched (`size-adjust`, `ascent-override`, `descent-override`).
- [ ] No FOIT > 1s.

## JS

- [ ] No unused `lodash`, `moment`, `axios` (use native or smaller).
- [ ] Tree-shaken: `@react-three/drei` imports are named, not `import *`.
- [ ] Maximalist libraries (`three`, `theatre`) are dynamic-imported, not in the main bundle.
- [ ] No legacy JS polyfills shipped to modern browsers (browserslist set to modern).

## CSS

- [ ] Tailwind purge is configured (default content paths).
- [ ] No unused CSS frameworks.
- [ ] Critical CSS inline or near-inline for above-the-fold.

## Network

- [ ] HTTP/2 or HTTP/3 enabled (default on Vercel / Cloudflare).
- [ ] Gzip / Brotli compression on text resources.
- [ ] No render-blocking third-party scripts.

## Third-party

- [ ] Analytics deferred (`defer` attribute).
- [ ] No chat widget loaded synchronously.
- [ ] Embeds (YouTube, Vimeo) use facades that load on interaction.

## Sign-off

- Pass: all items checked, scores at/above targets.
- Fail: any score below floor, or any budget breach.

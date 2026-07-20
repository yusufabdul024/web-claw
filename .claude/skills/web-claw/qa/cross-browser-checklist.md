# Cross-Browser Checklist

Run after Phase 2 and Phase 3. Tests the site in the actual browsers visitors use.

## Required browsers

- [ ] Chrome desktop latest.
- [ ] Edge desktop latest.
- [ ] Firefox desktop latest.
- [ ] Safari desktop latest (Mac required, or BrowserStack).
- [ ] Chrome Android latest (real device or BrowserStack).
- [ ] Safari iOS latest (real device or BrowserStack).

Optional (test if audience warrants):

- [ ] Samsung Internet.
- [ ] Chrome on KaiOS / older Android (low-end).
- [ ] Old Safari iOS (3 versions back).

## Per browser, per page

For each browser, on the home page at minimum (and any page with a signature section):

- [ ] Page loads without console errors.
- [ ] No network errors (404s).
- [ ] Hero renders correctly (fonts, layout, images).
- [ ] Scroll behavior matches the spec (Lenis or native, depending on browser).
- [ ] Signature section animations work (or fallback gracefully).
- [ ] Page transitions work (or fallback to instant).
- [ ] Primary CTA is clickable and routes correctly.
- [ ] Forms submit successfully and show feedback.
- [ ] Nav menu opens on mobile (if applicable).
- [ ] Footer renders correctly.

## Known browser-specific issues to watch

### Safari (desktop + iOS)

- [ ] `backdrop-filter` renders (sometimes drops; verify).
- [ ] View Transitions API: supported on Safari 18+; verify fallback on older.
- [ ] `gap` in flexbox: supported in modern Safari but older iOS may fail.
- [ ] Smooth scroll with Lenis: verify against rubber-band overscroll.
- [ ] Video autoplay: only with `playsinline muted`.
- [ ] Scroll-driven canvas: `video.currentTime` scrub can be unreliable; canvas with image-sequence is the safer pattern.

### Firefox

- [ ] `aspect-ratio`: supported.
- [ ] Scroll-timeline CSS: limited support; verify polyfill.
- [ ] `text-wrap: balance`: supported in modern Firefox; verify fallback.

### Mobile Chrome (Android)

- [ ] Address bar resize doesn't break layout (use `100dvh`, not `100vh`).
- [ ] Touch event handlers don't swallow scroll.

### Older browsers (if supported)

- [ ] Site degrades gracefully — no critical broken UI on browsers 3+ versions old.

## Console / network

For each browser:

- [ ] No JavaScript errors.
- [ ] No "favicon.ico" or "robots.txt" 404s in production.
- [ ] No CORS errors.
- [ ] No mixed-content warnings.

## Visual

For each browser, screenshot the home page and compare to the design:

- [ ] Type renders without unexpected fallback (especially Safari with custom fonts).
- [ ] Colors render correctly (no Safari sRGB-vs-Display-P3 surprises).
- [ ] Layout matches at standard breakpoints.

## Sign-off

- Pass: all required browsers tested; no critical issues; degradation paths verified.
- Fail: any console error, any visual break, any broken interaction on a required browser.

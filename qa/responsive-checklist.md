# Responsive Checklist

Run after every phase. The site must feel intentional at every common viewport.

## Required breakpoints

Test the home page (and any page with a signature section) at:

- [ ] 320 × 568 — smallest common mobile (iPhone SE 1st gen).
- [ ] 375 × 667 — iPhone SE 2/3.
- [ ] 390 × 844 — iPhone 14 / 15.
- [ ] 414 × 896 — iPhone Plus / Pro Max.
- [ ] 768 × 1024 — iPad portrait.
- [ ] 1024 × 768 — iPad landscape.
- [ ] 1280 × 800 — smallest common laptop.
- [ ] 1440 × 900 — common laptop.
- [ ] 1920 × 1080 — desktop.
- [ ] 2560 × 1440 — large display.

Use Chrome DevTools device toolbar or actual devices.

## Per breakpoint

### Layout

- [ ] No horizontal scroll.
- [ ] No content cropped.
- [ ] No content overflowing its container.
- [ ] Container max-width is respected (not pushing past `container.default`).
- [ ] Grid behaves as wireframed (collapses correctly on narrow widths).

### Typography

- [ ] H1 doesn't orphan a single word on the last line (use `text-wrap: balance` where supported).
- [ ] Body line length 50–80 characters.
- [ ] No type cropping or unexpected scaling.
- [ ] Font sizes feel right at the viewport (not too small at 1920px, not too large at 320px).

### Tap targets

- [ ] All interactive elements ≥ 44×44 CSS px.
- [ ] Adjacent tap targets have ≥ 8px gap.

### Images and media

- [ ] Images served at appropriate resolution for the breakpoint (`srcset`).
- [ ] No hero image stretching beyond useful resolution.
- [ ] Video and canvas resize correctly.

### Navigation

- [ ] Below 768px: mobile drawer / hamburger.
- [ ] 768–1024px: hybrid layout (verify it doesn't fall in the gap).
- [ ] 1024px+: full desktop nav.

### Signature section

- [ ] Specified mobile fallback (e.g., reduced pin distance, stacked layout) actually appears.
- [ ] Specified desktop behavior actually appears.

## Orientation

- [ ] Portrait mobile: tested at 320, 375, 414 widths.
- [ ] Landscape mobile: home and signature still legible at 667 × 375.
- [ ] Tablet portrait + landscape both tested.

## OS-level zoom and font size

- [ ] User OS-level "zoom" (browser zoom 200%): page remains functional.
- [ ] User OS-level "increased text size" (iOS Dynamic Type): page reflows without breaking.

## `100dvh` vs `100vh`

- [ ] Hero sections use `100dvh` (dynamic viewport height) on mobile, not `100vh`, to avoid the address-bar resize issue.

## Sign-off

- Pass: all required breakpoints checked; no overflow, no broken layout, no unreachable content.
- Fail: any horizontal scroll, any cropped content, any breakpoint that "looks broken."

# Motion Checklist

Run after Phase 2. Verifies every animation matches `blueprint/animations.md` and behaves correctly across user preferences and devices.

## Per page

For each page in the sitemap:

### Entrance choreography

- [ ] Above-the-fold entrance matches the spec table in `animations.md`.
- [ ] Total entrance duration ≤ 1.5s.
- [ ] No FOUC (flash of unstyled content) before animations start.
- [ ] Easings match the named easings (not improvised).

### Section reveals

- [ ] Each section reveals once as it enters the viewport.
- [ ] Reveals do not replay on re-scroll.
- [ ] Reveal stagger between children is consistent (80ms default).
- [ ] Below-the-fold content remains accessible to screen readers from the start (not gated on reveal).

### Signature section

- [ ] Matches the spec in `animations.md` to the millisecond.
- [ ] Pin (if any) has exit conditions: Esc, high scroll velocity, after max duration.
- [ ] Hits ≥ 58fps on Pixel 6a profile (DevTools 4× CPU + Slow 4G).
- [ ] INP during pin ≤ 200ms.
- [ ] Main thread ≤ 16ms/frame.
- [ ] Resources (frames, video, GLB models) lazy-loaded.

### Micro-interactions

- [ ] Buttons scale 1.02 on hover, 0.98 on active.
- [ ] Links underline-animate on hover.
- [ ] Inputs focus-ring expands.
- [ ] Cards lift on hover.
- [ ] All micro-interactions use the duration + easing tokens.
- [ ] Touch devices: hover effects absent or gracefully tap-instant.

### Page transitions

- [ ] Match the chosen pattern (instant / crossfade / shared element).
- [ ] Scroll resets to top of new page (or to intended position).
- [ ] No content flash during transition.

### Cursor (if applicable)

- [ ] Custom cursor visible on `hover: hover` + `pointer: fine` devices only.
- [ ] Magnetic targets work as specified.
- [ ] Cursor hides under text inputs (so the native I-beam shows).
- [ ] Cursor disabled for reduced motion.

## Reduced motion

For each animation:

- [ ] Enable `prefers-reduced-motion: reduce` via OS or DevTools Rendering panel.
- [ ] Animation is REPLACED (not stripped) with a quiet alternative.
- [ ] Page still tells the same story.
- [ ] Signature section's reduced-motion fallback exists and is tested.

## Performance during animation

- [ ] No additional RAF loops beyond Lenis + signature canvas (if any).
- [ ] No `setInterval` for animation timing.
- [ ] `transform` and `opacity` only on animated properties (no `width`, `top`, `box-shadow`).
- [ ] `will-change` applied only to elements that need it; removed after animation.

## On real devices

(At minimum on the primary device class for the audience.)

- [ ] Tested on a mid-tier Android (Pixel 6a or similar).
- [ ] Tested on an iPhone (any modern model).
- [ ] No janking visible.
- [ ] Battery and thermal behavior reasonable (no rapid drain or heat).

## Sign-off

- Pass: every item checked. Spec adherence verified per page.
- Fail: any animation deviating from spec, any reduced-motion broken, or any perf drop.

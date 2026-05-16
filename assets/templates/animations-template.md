# Motion Spec — <Project Name>

**Phase:** 1.5 (Web Claw)
**Authored by:** Animator Agent
**Based on:** `blueprint/discovery.md`, `blueprint/sitemap.md`, `blueprint/style-guide.md`, `blueprint/wireframes.md`
**Date:** <YYYY-MM-DD>

---

## Motion budget

- **Intensity:** <restrained | active | maximalist>
- **Frame-rate floor:** 60fps on a Pixel 6a (DevTools 4× CPU + Slow 4G).
- **Simultaneous animated elements at any frame:** ≤ 5.
- **Reduced-motion strategy:** replace (not strip) every animation with an equivalent quiet state.

---

## Motion tokens (extends style-guide.md)

```js
export const motion = {
  duration: {
    instant:   100,
    quick:     200,
    paced:     480,
    narrative: 900,
  },
  ease: {
    outQuart:  [0.25, 1, 0.5, 1],
    outBack:   [0.34, 1.56, 0.64, 1],
    outExpo:   [0.16, 1, 0.3, 1],
    inOutCubic:[0.65, 0, 0.35, 1],
    inCubic:   [0.32, 0, 0.67, 0],
  },
  stagger: {
    tight:  40,    // micro stagger
    paced:  80,    // default
    wide:   140,   // dramatic
  }
};
```

---

## Per-page choreography

### Page: Home — `/`

#### Above-the-fold entrance

**Total duration:** 1.1s
**Starts:** 80ms after DOMContentLoaded
**Reduced motion:** all opacity 0→1 over 200ms, no translations, no blur.

| Element        | Delay  | Duration | Easing            | From                            | To                  | Notes              |
|----------------|--------|----------|-------------------|---------------------------------|---------------------|--------------------|
| Logo           | 0      | 380ms    | outQuart          | opacity:0, y:-12                | opacity:1, y:0      | GPU                |
| Eyebrow        | 80ms   | 380ms    | outQuart          | opacity:0                       | opacity:1           | GPU                |
| H1 words       | 160ms  | 720ms    | outQuart          | opacity:0, y:24, blur:8px       | opacity:1, y:0, blur:0 | stagger 60ms/word; GPU + cheap blur |
| Sub            | 480ms  | 480ms    | outQuart          | opacity:0, y:16                 | opacity:1, y:0      | GPU                |
| CTA            | 640ms  | 380ms    | outBack           | opacity:0, y:12, scale:0.96     | opacity:1, y:0, scale:1 | GPU                |
| Hero media     | 720ms  | 600ms    | outQuart          | opacity:0, scale:1.04           | opacity:1, scale:1  | GPU; preload poster|

**Signature flourish:** at 1100ms, accent-colored 1px line draws under the H1 left-to-right, 480ms, `inOutCubic`. Length matches text-end.

---

#### Section reveals (default pattern, applied to all non-signature sections)

**Trigger:** Section top crosses 80% of viewport height.
**Behavior:**
- Direct children opacity 0→1, y 24→0.
- Duration 800ms, easing `outQuart`.
- Stagger 80ms across children.
- Once per scroll (no replay).

**Reduced motion:** Trigger only opacity 0→1, 200ms, no translations.

---

#### Section 4 **[SIGNATURE]** — "The product, in your hand"

**Pattern:** Pinned scroll narrative with canvas image-sequence scrub.
**Reference:** <e.g., "Adapted from Apple AirPods Pro 2 landing page (Awwwards SOTD 2022-09-21) — see research/awwwards-references.md §3.">
**Library:** GSAP + ScrollTrigger. Lenis as global smoother.

**Behavior:**

1. Section pins when its top reaches viewport top.
2. Pin duration = 3× viewport height of scroll (2× on mobile).
3. During pin, `<canvas>` cross-fades through 60 prerendered frames of the product rotating, frame index = `Math.round(progress * 59)`.
4. Three captions cycle in via opacity:
   - 0–33%: "Smaller than your thumbnail."
   - 34–66%: "Lighter than a paperclip."
   - 67–100%: "Yet it does this →" (transitions into Section 5)
5. Section unpins at 100%, normal scroll resumes.

**Frames:** 60 webp @ 1080×1080 desktop / 800×800 mobile. Total < 1.4MB. Lazy-preload after FCP.

**Performance:** ~12% main-thread on Pixel 6a during pin. ✅ Tested. Use `requestAnimationFrame` only for canvas draw; no JS animation inside the pin.

**Exit conditions:** ESC unpins. Scroll velocity > 4000px/s also unpins.

**Reduced motion:** Replace canvas with three stacked static images. Captions render as static `<p>` between them. No pin.

---

#### Other sections (Section 3 Three Promises, 5 Social Proof, 6 Pricing, 7 FAQ, 8 Bottom CTA)

Use the default section-reveal pattern. No bespoke motion.

---

### Page: <Page A>

(Same shape: entrance + section reveals + ONE signature section.)

---

(Repeat for every page in sitemap.)

---

## Micro-interactions (global)

### Buttons

```css
.button {
  transition:
    background-color var(--duration-quick) var(--ease-out-quart),
    transform var(--duration-quick) var(--ease-out-quart);
}
.button:hover { transform: scale(1.02); background-color: var(--accent-700); }
.button:active { transform: scale(0.98); transition-duration: var(--duration-instant); }
.button:focus-visible {
  outline: 3px solid var(--accent-500);
  outline-offset: 2px;
}
@media (prefers-reduced-motion: reduce) {
  .button { transition: none; }
  .button:hover, .button:active { transform: none; }
}
```

### Links

Underline grows in thickness on hover, 220ms `outQuart`.

### Inputs

Focus expands ring 0 → 3px, 140ms.

### Cards

Hover: `translateY(-4px)`, shadow +1, 200ms.

---

## Page transitions

**Pattern:** <Instant | Crossfade 240ms | Shared element (View Transitions API)>

**Reduced motion:** Instant always.

---

## Cursor (desktop only)

**Pattern:** <None | Magnetic buttons | Custom blob cursor>

**Mobile fallback:** <describe the equivalent affordance>

---

## Performance budget per page

For each page, mark animations as:

- ✅ GPU-only (compositor-friendly).
- ⚠️ Paint-only (small element, low cost).
- 🔴 Layout-triggering or expensive — must justify.

| Page    | ✅ count | ⚠️ count | 🔴 count | Notes                             |
|---------|----------|-----------|----------|-----------------------------------|
| Home    | 18       | 0         | 1 (signature canvas) | Canvas isolated to pinned section. |
| Page A  | 12       | 0         | 0        |                                   |
| ...     |          |           |          |                                   |

---

## Reduced-motion summary

For every signature section, document the reduced-motion alternative:

- **Home Section 4:** Three stacked images + captions; no pin, no canvas.
- **<Page A signature>:** <fallback description>.

Test in Chrome DevTools Rendering → "Emulate CSS media feature prefers-reduced-motion: reduce".

---

## Open questions for the user

1. <Question>

---

## Sign-off

- [ ] Above-the-fold entrance choreographed per page.
- [ ] Section reveals consistent across pages (default pattern unless documented).
- [ ] Signature section per page is specified to the millisecond.
- [ ] Micro-interactions are tokenized (one pattern per element type).
- [ ] Page transitions decided.
- [ ] Reduced-motion alternative exists for every signature.
- [ ] Performance budget per page is recorded.
- [ ] Ready to begin Phase 2: Research.

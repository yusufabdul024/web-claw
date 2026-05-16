# Pattern Library

The canonical catalog of interaction, section, and page-level patterns Web Claw agents work from. Organized by **layer**: which scale the pattern operates at.

- **Layer 1 — Micro:** per-element interactions (buttons, links, inputs, cards, modals, tabs, tooltips, toasts, loading).
- **Layer 2 — Section:** per-section signatures (the "scroll-stopping" moment) — pinned narratives, scrubbed canvas, kinetic type, bento, marquees, hero patterns, reveals, typographic devices, WebGL.
- **Layer 3 — Page:** patterns that span the page (route transitions, global scroll, cursor systems, composition rules).
- **Layer 4 — System:** durations, easings, anti-patterns, vibe → pattern matrix, the single rule.

**Borrow the device, not the site.** Three sites that all use the same pattern can each feel distinct because the content, the easing, and the editorial restraint differ.

---

## Who uses which layer

| Agent              | Loads                                                  |
|--------------------|--------------------------------------------------------|
| UI Strategy Agent  | Layer 2 (section selection) + Layer 4 (the single rule)|
| Animator Agent     | All layers                                             |
| Researcher Agent   | Layer 2 + Layer 3 + Layer 4 (for the vibe matrix)      |
| Implementer Agent  | Layer 1 (micro-interactions in code)                   |

---

# Layer 1 — Micro-interactions

How small interactions feel. The Animator Agent specifies these as a **system** — one set of patterns applied everywhere — not as ad-hoc choices per component.

## Button states

A button has six states. Spec all six.

| State    | Visual change                                                                       |
|----------|-------------------------------------------------------------------------------------|
| Default  | Base                                                                                |
| Hover    | bg color shift + `transform: scale(1.02)` + cursor pointer. 180ms `ease-out-quart`. |
| Focus    | Ring expands 0 -> 3px outside the button. 140ms. Color `accent-500`.                |
| Active (pressed) | scale(0.98) + bg darken. 80ms `ease-out-back`.                              |
| Loading  | Replace label with spinner; disable interaction; preserve width.                    |
| Disabled | 50% opacity; cursor not-allowed; no hover changes.                                  |

The hover scale (1.02) is the universal scroll-stopping button signal. Less is fine; more (>1.05) feels cheap.

## Link states (text links)

- Default: underline color matches text color (or accent depending on context). `text-underline-offset: 4px`.
- Hover: underline grows in thickness or animates `clip-path` left -> right under the text. 220ms.
- Focus: full ring (not just underline) for visibility.
- Visited: optional. For content sites, color shift toward purple-of-the-day.

## Input states

- Default: 1px border `neutral-300`. Background `neutral-50` or `surface.elevated`.
- Hover: border `neutral-400`.
- Focus: border `accent-500`, ring 3px `accent-500` at 20% opacity outside. 140ms.
- Invalid: border `error-500`. Error text below in `error-600` with `aria-live="polite"`.
- Disabled: 50% opacity.

Use `:focus-visible`, not `:focus`. The latter is on for click-focus too, which annoys mouse users.

## Card states

- Default: `surface.elevated` background, `shadow.card`.
- Hover: `transform: translateY(-4px)` + shadow elevation +1. 200ms `ease-out-quart`.
- Active (if clickable): scale(0.99), 80ms.
- Focus: outline ring (not just shadow swap, which screen readers ignore).

## Navigation patterns

### Top nav — scrolled state
- Default: transparent background, white text.
- Scrolled (>120px scroll): solid background, dark text, slight backdrop-blur, height shrinks (64px -> 56px). 240ms transition.

### Mobile drawer
- Triggered by hamburger.
- Slides in from the right (default) or top.
- Background scrim with `backdrop-filter: blur(6px)`.
- Focus traps inside. Esc closes. First link auto-focused on open.
- Returns focus to the hamburger on close.

### Section anchor jumps
- Smooth on desktop (Lenis or native scroll-behavior).
- Instant on mobile (smoothness fights with native scroll on iOS).
- Honor reduced-motion: instant always.

## Modal / dialog patterns

- Open via `<dialog>` element or a portaled component.
- Background scrim with `backdrop-filter: blur(8px)`.
- Modal enters with opacity 0->1 + scale 0.96->1, 280ms `ease-out-quart`.
- Focus moves to first focusable element inside; trap focus inside.
- Esc closes. Click outside closes (configurable).
- Returns focus to the trigger on close.
- Scroll-lock the body while open.

## Accordion / disclosure

- Triggered by clicking the header.
- Use `<details>`/`<summary>` for the simplest accessible case.
- For custom: `aria-expanded` on the trigger, `aria-controls` pointing to the content's id.
- Animation: height auto-resolved via `interpolate-size: allow-keywords` (Chrome 129+) or manual height interpolation with `aria-hidden`.

## Tab patterns

- Tab list: `role="tablist"`, each `<button role="tab" aria-selected>`.
- Content: `role="tabpanel" aria-labelledby`.
- Arrow keys cycle within the tablist (left/right or up/down depending on orientation).
- Home / End jump to first / last tab.
- Click on a tab focuses it.

## Tooltip patterns

- Trigger on `:hover` AND `:focus-visible`.
- 400ms delay before showing (prevents flicker on mousewheel-through).
- 150ms delay before hiding (forgiving).
- Position: above the trigger by default; flip below if it'd overflow.
- ARIA: `role="tooltip"`, trigger gets `aria-describedby` pointing to it.

## Toast / notification patterns

- Position: bottom-right desktop, bottom-full mobile.
- Enter: slide-up + fade, 240ms.
- Auto-dismiss: 4s default; pause on hover.
- Stack from bottom; max 3 visible.
- `role="status"` for info; `role="alert"` for errors.

## Loading patterns

### Inline (form button)
- Replace label with spinner; preserve button width via `min-width`.
- Keep the button disabled.

### Page-level
- Skeleton screens, not spinners. Skeletons feel ~30% faster perceptually.
- Use `aria-busy="true"` on the container.
- Don't show a skeleton if the load is <200ms; the flash is worse than the wait.

### Lazy-loaded section
- Use `IntersectionObserver` + `Suspense` to defer loading until the section approaches the viewport.

---

# Layer 2 — Section signatures

What makes a section earn the "scroll-stopping" label. The UI Strategy and Animator agents pick **the signature section** per page using this layer. Pick **one** per page. A page with five scroll-stopping sections has zero.

## What "scroll-stopping" means

A scroll-stopping section is one where the user, mid-scroll, slows or stops. Not because the page broke. Because something earned a beat of attention.

Three things make a section scroll-stopping:

1. **Unexpected motion.** A hover state nobody designed. A scroll behavior that breaks the normal rhythm. A transition that surprises in 200ms.
2. **Crafted detail.** Type that's been kerned. Numbers that count up. A line that draws under a word. Detail invisible at distance, gratifying up close.
3. **A single signature moment.** Not five clever things. One moment per page. The rest is calm.

## 2.1 Signature section devices (pick ONE per page)

### S1 — Pinned scroll narrative
The section pins for 2–3 viewport heights. As the user scrolls within the pin, a sequence of frames advances: a product rotates, a number counts up, a paragraph fades to the next paragraph.

- **Best for:** product launches, multi-step feature walkthroughs, brand stories.
- **Implementation:** GSAP ScrollTrigger with `pin: true, scrub: true`.
- **Risk:** scroll-jacking trap. Always include exits (Esc, high velocity, after 3x pin).

### S2 — Scrubbed canvas / video
A canvas or video element's playhead is bound to scroll progress. Frames are pre-rendered for canvas (60–120 frames typical); video uses `video.currentTime = progress * duration`.

- **Best for:** product hero where the product visually transforms across the scroll (Apple AirPods Pro pages).
- **Implementation:** preload frames, RAF-driven scroll listener, draw current frame to canvas.
- **Risk:** mobile iOS Safari often refuses to scrub video. Use canvas-with-image-sequence on mobile.

### S3 — Kinetic type hero
The H1 enters word-by-word (or letter-by-letter) with mixed transforms: y-shift, blur clear, slight rotation. Sometimes paired with `font-variation-settings` interpolating.

- **Best for:** editorial sites, brand-first sites where the H1 is the design.
- **Implementation:** GSAP timeline or Framer Motion variants. SplitText (GSAP plugin) or manually wrap words/letters in spans.
- **Risk:** screen readers may read each span as a separate word. Use `aria-label` on the parent and `aria-hidden="true"` on the spans.

### S4 — Bento grid (used well)
Asymmetric tile grid where tile size maps to content priority. The signature comes from individual tiles having their own micro-animations on view + hover.

- **Best for:** features sections where products genuinely have unequal weight; portfolio thumbnails.
- **Implementation:** CSS grid with named template areas. Each tile gets `view-timeline`-driven entrance.
- **Risk:** generic. Bento has been done. Earn it with content-shape that actually demands it.

### S5 — Horizontal scrub before vertical scroll
The page's first scroll-distance moves a section horizontally (often H1 word changing). Then transitions to standard vertical scroll.

- **Best for:** editorial sites with strong typography, single-page sites.
- **Implementation:** ScrollTrigger with a pinned section whose content uses `transform: translateX(-progress * sectionWidth)`.
- **Risk:** confuses scroll affordances. Test heavily on touch.

### S6 — 3D scene with scroll-camera
A small Three.js scene (often a single 3D model + lighting) where the camera position is driven by scroll. The user appears to walk around the product.

- **Best for:** product launches with a tangible 3D asset (hardware, packaging, vehicle).
- **Implementation:** @react-three/fiber + drei. Camera in a useFrame, position lerping toward scroll-derived target. Dynamic-import the entire scene.
- **Risk:** heavy. Reduce-motion fallback must be a static still. Test on Pixel 6a.

### S7 — Image-to-particle morph
An image dissolves into particles and reassembles into another image. Maximalist. Often used between sections.

- **Best for:** brand showcases, creative portfolios.
- **Implementation:** shader-driven particle system (Three.js + GLSL). Reference: Bruno Simon's `threejs-journey`.
- **Risk:** very heavy. Reserve for sites where the motion intensity is explicitly maximalist.

### S8 — Reveal-by-mask
A clip-path or SVG mask reveals content as scroll progresses or on view. Cleaner than fade reveals for type. Often paired with a contrasting color band.

- **Best for:** any vibe; restrained tip-of-the-iceberg variant of bigger devices.
- **Implementation:** CSS `clip-path` animated via scroll-timeline, or GSAP `clipPath` interpolation.

### S9 — Interactive cursor demo
The signature is something the user does, not watches. Hover a button and it pulls toward you. Hover a product and it spins. Hover a quote and the words you hover swap with synonyms.

- **Best for:** B2B SaaS / product sites where "feels alive" is the brief.
- **Implementation:** mousemove handlers + Framer Motion or GSAP. Compute distance to element center; apply transform proportional.
- **Risk:** mobile fallback (the cursor doesn't exist). Provide an alternate signature for touch.

### S10 — Marquee with personality
A continuously-scrolling horizontal strip ("LOGOS / LOGOS / LOGOS") that does something unexpected: changes speed on hover, reverses on scroll direction, color-shifts the words the cursor is over.

- **Best for:** trust bars, "as seen in" sections, manifesto strips.
- **Implementation:** CSS `animation: marquee 30s linear infinite`. Add hover-pause, direction control via JS.

### S11 — Number explosion
A big number counts up dramatically (0 -> 14,200,000) with characters that scale + reposition. Often the "social proof" or "metric" section.

- **Best for:** SaaS metric sections, milestone announcements.
- **Implementation:** custom number-animation logic; respect digit-width with `font-variant-numeric: tabular-nums`.

### S12 — Auto-shifting headline
The H1 cycles through phrases ("for product teams" -> "for designers" -> "for engineers"). Each transition is a beautiful flip.

- **Best for:** SaaS sites with multi-audience targeting.
- **Implementation:** Framer Motion `<AnimatePresence>` swapping text nodes; explicit width animation to prevent layout jump.

### S13 — Interactive draw
The user can draw / scribble on a canvas, and the signature site reacts. Often a tiny easter egg in a portfolio.

- **Best for:** creative portfolios, fun brands.
- **Implementation:** canvas with pointer events; the line decays after a few seconds.

### S14 — Sound-reactive
Hover plays a synth note. The CTA hum-pulses to music. A volume-up button reveals a soundscape.

- **Best for:** maximalist agencies, music sites, music-adjacent brands.
- **Implementation:** Web Audio API. Lazy-load on user gesture (audio context requires interaction).
- **Risk:** must be opt-in. Auto-playing sound is universally hated.

### S15 — Morphing SVG narrative
A single SVG morphs across multiple shapes as the user scrolls (a logo -> a product -> an abstract). Often replaces the hero image.

- **Best for:** brand sites with a strong visual identity.
- **Implementation:** GSAP MorphSVGPlugin or Flubber.js.

## 2.2 Hero patterns

### H1 — Kinetic type hero
Each word of the H1 enters separately with a unique transform — y-shift, slight rotation, blur clear. Total entrance <= 1.2s, stagger <= 80ms. The "blur clear" detail is signature on Awwwards: words enter at `filter: blur(8px)` and resolve to `blur(0)` over the entrance.

When to use: editorial vibe, brand sites, hero with strong typography.

### H2 — Pinned hero with scrubbed media
Hero pins for 1–2 viewport-heights. As the user scrolls, a video or canvas scrubs through frames, captions cross-fade. The hero "doesn't end" until the narrative is told.

When to use: product launches with a story; signature moment requested.

### H3 — Layered scroll hero
Hero has 3+ z-stacked layers (background, midground, foreground) each translating at different rates relative to scroll. Often combined with a fixed/pinned headline.

When to use: maximalist motion; brand sites where mood matters more than density.

### H4 — Horizontal scrub before vertical scroll
The first 400–800px of scroll moves the page horizontally (often the H1 changing word), then transitions into normal vertical scroll. Subtle but immediately distinctive.

When to use: editorial sites with a strong typographic system. (See also S5 — same device, repeated here for hero context.)

### H5 — Auto-revealing big-type hero
H1 reveals letter-by-letter using a clipping mask animation. Often combined with a noise/grain background and an `<sup>` or `<sub>` accent in a different typeface.

When to use: mono-minimal vibe with budget for restraint.

## 2.3 Reveal patterns (in-section)

### R1 — Mask-clip reveal
Text reveals via `clip-path: inset()` animating from 100% to 0% on the appropriate axis. Better than opacity for type — readable from the start.

### R2 — Stagger-and-blur reveal
Children enter with opacity 0->1 + blur 8->0 + y 16->0, staggered 40–80ms. The blur is the signature.

### R3 — Line draw under headings
SVG `stroke-dasharray` animation draws an accent line under the H1 or H2. 480–800ms ease-in-out. Single signature line per page.

### R4 — Number count-up
Big stat numbers count from 0 to value as section enters view. Use `requestAnimationFrame` with easing; don't `setInterval`.

### R5 — Marquee reveal
Continuously-scrolling horizontal text strip ("LOGOS / LOGOS / LOGOS / LOGOS"). Combined with hover-pause and direction-on-scroll for personality.

## 2.4 WebGL patterns

### W1 — Iridescent abstract orb
A shader-driven orb / blob in the hero. Mouse-reactive (slight follow). Often paired with a noise/grain overlay.

### W2 — Image-to-particles morph
On hover or scroll, an image dissolves into particles and reassembles into a new image. Heavy. Maximalist only. (See S7.)

### W3 — Distorted text
WebGL shader applies a wave/heat/glitch distortion to a text element. Used sparingly — usually on the H1 of a creative agency site.

### W4 — 3D scene with scroll-driven camera
A small Three.js scene (one model, a few lights) with the camera position driven by scroll. The "exploded view" pattern. (See S6.)

## 2.5 Typographic patterns

### T1 — Variable font weight on hover
H1 / link weight animates on hover via `font-variation-settings`. A signature subtle interaction.

### T2 — Display + body pairing with extreme size contrast
Display at 96–160px, body at 16–18px. The contrast itself is the design.

### T3 — Numbered sections in serif counter
Each section is numbered ("01 / 02 / 03") in a slim serif, set in a corner. Editorial signature.

### T4 — Trailing punctuation as accent
"Build. Ship. Repeat." with the periods in accent color, slightly oversized. Cheap, classy.

## 2.6 Composition patterns

### C1 — Bento grid
Asymmetric tile grid, varying tile sizes corresponding to content priority. Was novel in 2023; now standard. Use only when content genuinely benefits. (See S4.)

### C2 — Off-grid headline
The H1 starts 20% past the container's left edge. Breaks the grid for emphasis. Editorial signature.

### C3 — Massive whitespace + tiny content
Section uses 80% empty space, 20% content (a single quote, a single image). Confidence through restraint.

### C4 — Full-bleed image with overlaid text
Image goes edge-to-edge of viewport (`vw`-sized). Text overlays with contrast scrim or `mix-blend-mode`.

### C5 — Right-aligned right column
Body copy right-aligned in the right column. Unusual. Read pause. Editorial signature.

## How to pick the signature

1. Read the discovery's signature-moment answer (Q16).
2. Read the project's motion intensity (Q15).
3. Read the wireframes — which sections are inherently information-light (signature lives best on info-light, atmosphere-rich sections).
4. Match a pattern. Two patterns are still possible if one is on Home and the other is on a deeper page — but never two signature devices on the same page.

## Section anti-patterns

- ❌ **Stacking three "signature" devices on the home page.** Pick one. The other two get cut to restrained scroll reveals.
- ❌ **Picking a pattern that violates the motion budget.** A 3D scene on a restrained-intensity brief is wrong even if it's well-implemented.
- ❌ **Picking a pattern with no Awwwards reference.** If the dossier doesn't include a site doing this, you're inventing in production. Either find a reference or pick a different pattern.
- ❌ **A signature device that doesn't survive `prefers-reduced-motion`.** If the section becomes meaningless when reduced, the section was reduced-motion-hostile from the start.
- ❌ **A signature device that doesn't survive a 2G connection.** If the signature is a 4MB pre-rendered image sequence, it's the wrong signature for mobile-heavy traffic.

---

# Layer 3 — Page patterns

Patterns that operate at page or cross-page scale.

## 3.1 Scroll patterns (page-level)

### SC1 — Sticky scroll narrative (pinned)
A section pins; a sequence of content advances as the user scrolls. Typically 3–5 "frames" or "chapters" within the pin. Used for product walkthroughs, brand stories, multi-step explanations.

Implementation: GSAP ScrollTrigger with `pin: true, scrub: true`. Or modern: CSS `position: sticky` + `view-timeline`.

### SC2 — Scroll-scrubbed video
A `<video>` element's `currentTime` is driven by scroll position. As the user scrolls, the video plays/reverses. Used for product reveals, character animations.

Implementation: scroll listener -> set `video.currentTime = progress * video.duration`. Throttle to RAF. iOS Safari requires `playsinline` and a tap-to-init for some versions.

### SC3 — Image sequence scrubber (canvas)
60–120 pre-rendered frames drawn to a canvas, frame index driven by scroll. Lighter than video for short sequences, more iOS-reliable.

Implementation: preload images, draw the current frame to canvas on scroll. Awwwards-style.

### SC4 — Section-by-section snap
`scroll-snap-type: y mandatory` on the viewport, sections are full-height snap points. Combined with intra-section animations triggered at snap-in.

When to use: portfolio sites with a small page count; storytelling where each section is its own scene.

### SC5 — Sideways scroll page
The entire page scrolls horizontally. Mouse-wheel + arrow-key + drag are all bound. Mobile uses native vertical scroll with a horizontal layout inside.

Caution: breaks browser scroll affordances. Use only when content shape genuinely demands it (timelines, comparisons, gallery flows).

### Global smooth scroll
- Library: Lenis (recommended). 1kb baseline.
- Config: `lerp: 0.1, duration: 1.2`.
- Pair: `lenis.on('scroll', ScrollTrigger.update)` if using GSAP.
- Fallback: `prefers-reduced-motion: reduce` -> no Lenis, native scroll.

### Scroll-to-top button
- Appears after 600px scrolled.
- Bottom-right or bottom-center on mobile.
- Click -> smooth scroll to top.
- Hidden when at top.

### Pull-to-refresh
- Don't override the browser's default. The native PWA / iOS Safari pull-to-refresh is sacred.

## 3.2 Page transition patterns

### PT1 — Instant (recommended for most marketing)
No animation between routes. Fastest perceived navigation.

### PT2 — Crossfade
- Old page opacity 1->0, 240ms.
- New page opacity 0->1, 240ms with 80ms delay.
- Trouble with scroll position; reset to top of new page.

### PT3 — Shared element
- Source element on outgoing page has `viewTransitionName: thumb-1`.
- Destination element on incoming page has the same name.
- Browser interpolates between them.
- Chrome / Edge / Safari 18+: `document.startViewTransition()`.
- Fallback: instant transition.

### PT4 — Curtain
- Solid color sweeps across (left -> right, 320ms).
- Old page swaps under the curtain.
- Curtain retracts (320ms).
- Custom; usually overkill for marketing.

### PT5 — Diagonal split
The screen splits diagonally; halves move opposite directions. Old page leaves; new page enters in the gap.

## 3.3 Cursor patterns

### CU1 — Custom cursor with magnetic targets
Replace native cursor with a styled element. Interactive elements (buttons, links, thumbnails) "magnetize" the cursor — pull it slightly toward the element's center on hover.

Implementation: CSS `cursor: none`, follow mouse with a small ring/dot. For magnetism, on hover apply `transform: translate(toElementCenter * 0.15)`.

Mobile fallback: skip entirely. Mobile has no cursor — design the same affordance via tap/haptic.

### CU2 — Magnetic button (desktop only)
On mousemove within a button's hit area:
```js
const dx = mouseX - buttonCenterX;
const dy = mouseY - buttonCenterY;
button.style.transform = `translate(${dx * 0.2}px, ${dy * 0.2}px)`;
```
On mouseleave, animate back to 0,0 with `ease-out-back`.

### CU3 — Cursor labels on thumbnails
Hovering a portfolio thumbnail shows a small "VIEW PROJECT ->" label that follows the cursor. Adds a "press to enter" feel.

### CU4 — Blob cursor / fluid cursor
A SVG blob or canvas blob follows the cursor with lerp easing, deforming on velocity. Maximalist territory.

```js
const lerp = (a, b, n) => a + (b - a) * n;
function tick() {
  blobX = lerp(blobX, mouseX, 0.15);
  blobY = lerp(blobY, mouseY, 0.15);
  cursor.style.transform = `translate(${blobX}px, ${blobY}px)`;
  requestAnimationFrame(tick);
}
```
Show only on devices with `hover: hover` and `pointer: fine`. Hide for reduced motion.

### CU5 — Cursor color-shift in dark sections
The cursor itself changes color or invert mode when over different surface tones. Subtle but memorable.

---

# Layer 4 — System reference

The shared vocabulary every other layer pulls from.

## 4.1 Easing cheat-sheet

Use these named easings; don't invent ad-hoc ones.

```js
export const easings = {
  outQuart:  [0.25, 1, 0.5, 1],            // arrivals -- default
  outBack:   [0.34, 1.56, 0.64, 1],        // snappy with overshoot -- small UI
  outExpo:   [0.16, 1, 0.3, 1],            // dramatic deceleration -- hero
  inOutCubic:[0.65, 0, 0.35, 1],           // symmetric -- back-and-forth
  inCubic:   [0.32, 0, 0.67, 0],           // exits
  springSoft: { type: 'spring', stiffness: 200, damping: 30 },  // Framer Motion
  springSnap: { type: 'spring', stiffness: 400, damping: 28 }
};
```

## 4.2 Duration cheat-sheet

| Token        | ms        | Used for                                             |
|--------------|-----------|------------------------------------------------------|
| instant      | 80–120    | press, focus-ring expand, tiny feedback              |
| quick        | 180–240   | hover transitions, small reveals                     |
| paced        | 400–500   | section reveals, modal open                          |
| narrative    | 800–1200  | hero entrance, story moments                         |

Pick one token per interaction type; don't drift to 350ms because it "feels right."

## 4.3 Vibe → pattern matrix

Use this when picking a section signature. Numbers refer to S/H/R/T/C codes above.

| Vibe              | Reach for                                                                |
|-------------------|--------------------------------------------------------------------------|
| Editorial         | S3, S5, R1, R3, T2, T3, C2, C3                                           |
| Brutalist         | H5, R5, PT4, T1, C1 (rough variant)                                      |
| Organic           | CU4 (blob), R2, W1, C4                                                   |
| Futurist          | H2, H3, SC3, W2, W3, W4                                                  |
| Corporate-pop     | H2, SC1, R2, R4                                                          |
| Mono-minimal      | S3, H5, R1, R3, T3, C3                                                   |

## 4.4 Universal anti-patterns

### Micro-interaction
- ❌ **Spring on hover scale.** Springs in micro-interactions feel jiggly. Use a cubic.
- ❌ **400ms hover transition.** Too slow; lags behind the cursor. 180–240ms.
- ❌ **Page transition with no scroll reset.** New page lands in scrolled position of old page. User confusion.
- ❌ **Disabled button with no help text.** "Why can't I click this?" Show the reason inline.
- ❌ **Skeleton screens that look just like the content.** Skeleton's job is to say "loading." If it looks like real content, users tap the skeleton.
- ❌ **Multiple modals open at once.** Pick one.
- ❌ **Modals that you can't dismiss with Esc.** Always.
- ❌ **Tooltips that wrap long-form copy.** Tooltips are for short labels. Use a popover for longer content.

### Section / page
- ❌ **Stacking three "signature" devices on the home page.** Pick one. The others become restrained reveals.
- ❌ **A 3D scene on a restrained-intensity brief.** Wrong even if well-implemented.
- ❌ **A signature device with no Awwwards reference in the dossier.** Either find one or pick a different pattern.
- ❌ **A signature device that doesn't survive `prefers-reduced-motion`.** If the section becomes meaningless when reduced, the section was reduced-motion-hostile from the start.
- ❌ **A signature device that doesn't survive a 2G connection.** If the signature is a 4MB pre-rendered image sequence, it's the wrong signature for mobile-heavy traffic.

## 4.5 The single rule

**One signature device per page.** Pick one pattern from Layer 2 as the section that earns "scroll-stopping." Other sections are calm. Restraint is what makes the signature stand out.

A page with five signature devices is a page with no signature.

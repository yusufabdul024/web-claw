# Animation Libraries

A capability matrix for choosing the right motion library cluster for a given motion intensity. The Implementer Agent picks from this list; the Animator Agent specifies in terms of capabilities, not specific library APIs.

## The clusters

### Restrained-intensity cluster (default)

**Stack:**
- Native CSS (`@keyframes`, `transition`, `animation-timeline`).
- IntersectionObserver for scroll reveals.
- Optionally: `framer-motion` for layout animations and shared elements.

**Total JS cost:** ~0–15kb.

**Capabilities:**
- Entrance animations on first paint (CSS keyframes).
- Scroll reveals (IntersectionObserver → toggle a class).
- Hover/focus micro-interactions.
- Page transitions via the View Transitions API (Chrome / Edge / Safari 18+).

**When this is enough:**
- B2B SaaS marketing site.
- Editorial site without scroll-jacked moments.
- High-content (blog-heavy) sites.

### Active-intensity cluster

**Stack:**
- `framer-motion` (~50kb) OR `gsap` (~50kb core + ~20kb ScrollTrigger).
- `lenis` (~8kb) for smooth scroll.

**Total JS cost:** ~60–80kb.

**Capabilities:**
- Choreographed entrance staggers with shared timeline.
- Scroll-triggered reveals with custom easings.
- Pinned scroll sections (GSAP ScrollTrigger).
- Smooth scroll inertia (Lenis).
- Page transitions with shared elements (framer-motion `layoutId` or View Transitions).
- Magnetic buttons, custom cursors.

**When this is the right pick:**
- Product / agency marketing sites with a clear signature section.
- Sites where motion intensity is "active" per discovery.

### Maximalist-intensity cluster

**Stack:**
- `gsap` + ScrollTrigger + MotionPath + Flip + ScrollSmoother (Club GreenSock members get the bonus plugins).
- `three` + `@react-three/fiber` + `@react-three/drei` for 3D.
- `lenis` or built-in ScrollSmoother for smooth scroll.
- `theatre.js` (~50kb) for timeline orchestration when designers want to scrub.
- `lottie-react` for vector micro-animations (if budgeted).

**Total JS cost:** ~250–500kb (with code-splitting + dynamic import for the 3D scene).

**Capabilities:**
- Everything in Active, plus:
- WebGL hero / scene with scroll-driven camera.
- Image-to-particle morphs.
- Scroll-scrubbed video / canvas image sequences.
- Custom cursors with magnetic targets and color-shifting.
- Complex orchestrated multi-section narratives.

**When this is the right pick:**
- Site of the Day candidates.
- Agency portfolio / brand showcase.
- Product launches where the launch IS the marketing.

## Library quick reference

### GSAP (3.12+)
- The standard for production-grade animation. Free for commercial use as of 2024 (Webflow acquisition).
- Core API: `gsap.to()`, `gsap.from()`, `gsap.fromTo()`, `gsap.timeline()`.
- ScrollTrigger plugin for scroll-driven animation: pin, scrub, snap, callbacks.
- MotionPathPlugin for SVG path animation.
- Flip plugin for FLIP-technique layout transitions.
- Best for: complex choreography, scrub-driven scenes, anywhere you need a timeline.

### Framer Motion (11+) / Motion (12+)
- React-native motion library; in v12 rebranded to "Motion."
- Declarative variants, layout animations, shared `layoutId` transitions.
- Best for: React-only projects with mostly entrance/exit/hover animations and layout transitions.
- Weakness: scroll-scrub is awkward compared to GSAP ScrollTrigger.

### Lenis
- Tiny smooth-scroll library by darkroomengineering (the team behind many Awwwards SOTD sites).
- Wheel + touch + keyboard interpolation.
- Pairs with GSAP ScrollTrigger via `lenis.on('scroll', ScrollTrigger.update)`.
- Best for: any project that wants buttery inertial scroll without locomotive-scroll's weight.

### Locomotive Scroll
- Older Lenis predecessor. Heavier. Has more features (parallax via data attributes).
- Use only if migrating an existing Locomotive site; new projects use Lenis.

### Three.js / React Three Fiber / Drei
- The canonical WebGL stack.
- R3F is the React reconciler for Three.js.
- Drei is the helper library (`OrbitControls`, `useGLTF`, `Environment`, etc.).
- Best for: 3D models, shader-driven effects, scroll-driven cameras.
- Heavy — dynamic-import the entire scene and gate behind `prefers-reduced-motion`.

### Theatre.js
- A timeline-as-data tool. Designers can scrub a visual timeline in the browser; values export as JSON; runtime plays them back.
- Best for: motion-heavy projects with a real motion designer in the loop.

### Lottie (Lottie-web, lottie-react, dotLottie)
- After-Effects-to-JSON animation runtime.
- Best for: micro-illustrations, icon animations under 50kb each.
- Worst for: anything you could express as a 200kb MP4; Lottie often weighs more than the equivalent video for complex scenes.

### Motion One
- Minimal Web Animations API wrapper from the Framer team.
- ~3kb. No timeline; declarative.
- Best for: restrained-intensity sites that want a tiny ergonomic API over the WAAPI.

### Auto-Animate
- One-line drop-in for list reorder/add/remove animations.
- Tiny (~2kb). Solves a specific problem perfectly.
- Best for: any list, table, or grid that mutates.

### CSS `view-timeline` and `scroll-timeline`
- The new web standard for scroll-driven animation. Chrome 115+, Safari 18+, Firefox in progress.
- No JS required for scroll-driven entrance reveals.
- Best for: progressive enhancement; use as the modern path with a JS fallback.

## Decision matrix

```
Motion intensity = restrained:
  → CSS + IntersectionObserver. Add framer-motion ONLY if you need layout animations.

Motion intensity = active:
  Project is React?
    Yes → framer-motion + lenis
    No  → gsap + ScrollTrigger + lenis

Motion intensity = maximalist:
  Project is React?
    Yes → gsap + ScrollTrigger + lenis + @react-three/fiber + drei (lazy-load 3D)
    No  → gsap + ScrollTrigger + ScrollSmoother + three + lenis (or ScrollSmoother native)

Signature device requires 3D?
  Yes → @react-three/fiber + drei. Lazy-load via dynamic import. Test on Pixel 6a.
  No  → skip three.js entirely; save 200kb.

Page transitions matter?
  All browsers? → framer-motion shared layout or View Transitions polyfill.
  Modern only?  → View Transitions API (Chrome / Edge / Safari 18+).
```

## Things to never do

- **Animate `width`, `height`, `top`, `left`, `margin`.** All trigger layout. Use `transform` instead.
- **Animate `box-shadow`.** Triggers paint. Use an overlay element's opacity.
- **Run multiple `requestAnimationFrame` loops.** Coalesce into one.
- **Auto-play videos on hover with `play()` calls.** Modern browsers block; use CSS `<video autoplay muted playsinline>` with a tap-to-start fallback.
- **Use `setTimeout` for animation timing.** Use the library's timeline or RAF.
- **Mix Lenis + Locomotive Scroll + native scroll.** Pick one.

## Bundle-size cheat-sheet (minified, gzipped, approximate)

| Library                  | Size (gz) |
|--------------------------|-----------|
| Motion One               | 3 kb      |
| Auto-Animate             | 2 kb      |
| Lenis                    | 8 kb      |
| Framer Motion (core)     | 35 kb     |
| Framer Motion + layout   | 50 kb     |
| GSAP core                | 24 kb     |
| GSAP + ScrollTrigger     | 38 kb     |
| GSAP + ScrollTrigger + ScrollSmoother | 55 kb |
| Three.js core            | 150 kb    |
| @react-three/fiber       | 40 kb     |
| @react-three/drei (full) | 200+ kb (tree-shake!) |
| Theatre.js core + studio | 110 kb (studio is dev-only) |
| Lottie-web               | 60 kb     |

Always dynamic-import maximalist libraries on the route that needs them.

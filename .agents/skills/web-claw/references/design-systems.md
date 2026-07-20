# Design Systems

How to tokenize a website's visual language so that color, type, spacing, radius, and motion are decisions made once and applied everywhere. The Designer Agent reads this when producing `style-guide.md`.

## What gets tokenized

| Category   | Tokens                                                                              |
|------------|-------------------------------------------------------------------------------------|
| Color      | Neutrals (50–950), accent (50–950), voice (single step), semantic (success/warn/err/info), surface, foreground |
| Typography | Font family (display/body/mono), font weight, size scale, leading, tracking         |
| Spacing    | Base unit, scale (1–10 or T-shirt sized)                                            |
| Radius     | none / sm / md / lg / pill                                                          |
| Elevation  | Shadow tokens for surfaces, modals, tooltips                                        |
| Motion     | Duration (instant / quick / paced / narrative) and easing (named cubic-beziers)     |
| Z-index    | Named layers (base, raised, sticky, overlay, modal, toast)                          |
| Breakpoint | sm / md / lg / xl / 2xl (matches Tailwind's defaults or custom)                     |

## Naming conventions

**Semantic > literal.** Tokens are named for purpose, not for value.
- ✅ `color.surface.default`, `color.surface.elevated`, `color.text.primary`.
- ❌ `color.gray-100`, `color.white`.

A literal name (`color.gray-100`) is fine as a **primitive layer** that semantic tokens reference. Two layers:

```json
{
  "color": {
    "primitives": {
      "neutral": { "50": "#FAFAF7", "100": "#F2F2EC", ... }
    },
    "semantic": {
      "surface": {
        "default":  "{color.primitives.neutral.50}",
        "elevated": "{color.primitives.neutral.0}",
        "sunken":   "{color.primitives.neutral.100}"
      },
      "text": {
        "primary":   "{color.primitives.neutral.900}",
        "secondary": "{color.primitives.neutral.600}",
        "muted":     "{color.primitives.neutral.400}"
      }
    }
  }
}
```

The implementer code only references semantic tokens. Primitives can shift (e.g., for dark mode) without changing component code.

## Color scale generation

Start from a single accent hex and generate the 11-step scale via OKLCH lightness ramping (more perceptually even than HSL):

```
accent-50:  oklch(98% c h)
accent-100: oklch(95% c h)
accent-200: oklch(90% c h)
accent-300: oklch(82% c h)
accent-400: oklch(72% c h)
accent-500: oklch(62% c h)  ← the brand color
accent-600: oklch(54% c h)
accent-700: oklch(46% c h)
accent-800: oklch(38% c h)
accent-900: oklch(30% c h)
accent-950: oklch(20% c h)
```

`c` (chroma) typically tightens at the lightness extremes — pure colors get muddy at 95% and 20%. Tools that handle this correctly: Radix Colors, Tailwind's color generator, OkColor.app.

## Spacing scale

Two acceptable scales:

**Linear-4:** 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256.
**Linear-8:** 8, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384.

Tailwind uses linear-4 by default. Stick with it unless you have a reason. Custom scales are usually a mistake.

T-shirt naming overlay (`xs`, `sm`, `md`, `lg`, `xl`, `2xl`, ...) is fine alongside numeric, but pick one as canonical.

## Type scale

Modular scale at 1.250 (major third) or 1.333 (perfect fourth). At 16px body:

| Step       | 1.250 ratio | 1.333 ratio |
|------------|-------------|-------------|
| Caption    | 12.8 → 12   | 12.0 → 12   |
| Body       | 16          | 16          |
| Lead       | 20          | 21          |
| H4         | 25          | 28          |
| H3         | 31          | 38          |
| H2         | 39          | 50          |
| H1         | 49          | 67          |
| Display    | 61          | 89          |
| Display XL | 76          | 119         |

Cap the scale at the size you actually use. Don't ship Display XL if no page needs 119px.

For fluid sizing use `clamp(min, preferred, max)`:

```css
.h1 {
  font-size: clamp(2.5rem, 5vw + 1rem, 4.5rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
}
```

## Radius scale

- `radius.none`: 0
- `radius.sm`: 4px — buttons, inputs, small cards
- `radius.md`: 8px — cards
- `radius.lg`: 16px — modals, large feature cards
- `radius.xl`: 24px — hero cards, signature blocks
- `radius.pill`: 9999px — tags, capsule buttons

Pick a maximum and stick to 3 sizes max per project. Five radii in one site = no design system.

## Elevation

Layered shadows beat single shadows. Two-token pattern:

```css
--shadow-card:
  0 1px 2px rgb(0 0 0 / 0.04),
  0 4px 12px rgb(0 0 0 / 0.06);

--shadow-modal:
  0 8px 16px rgb(0 0 0 / 0.08),
  0 24px 48px rgb(0 0 0 / 0.12);
```

For dark surfaces, shadows lose meaning — use `box-shadow: 0 0 0 1px rgb(255 255 255 / 0.05)` as a "subtle separator" instead.

## Motion tokens

Two axes: duration and easing.

**Durations:**
- `duration.instant`: 80–120ms — feedback (button-press, focus-ring expand).
- `duration.quick`: 180–240ms — hover transitions, small reveals.
- `duration.paced`: 400–500ms — section reveals, modal open.
- `duration.narrative`: 800–1200ms — hero entrance, scroll-triggered story moments.

**Easings (named cubic-beziers):**
- `ease.out-quart`: `cubic-bezier(0.25, 1, 0.5, 1)` — default for arrivals.
- `ease.in-cubic`: `cubic-bezier(0.32, 0, 0.67, 0)` — default for exits.
- `ease.in-out-cubic`: `cubic-bezier(0.65, 0, 0.35, 1)` — default for back-and-forth.
- `ease.out-back`: `cubic-bezier(0.34, 1.56, 0.64, 1)` — slight overshoot for snappy feedback.
- `ease.spring-bounce`: custom spring or library spring config.

Three to five named easings max. Don't invent a new one per animation.

## Z-index layers

Named, not numeric. The numbers are private to the implementation.

```css
:root {
  --z-base:    0;
  --z-raised:  10;   /* cards on hover */
  --z-sticky:  100;  /* sticky headers */
  --z-overlay: 1000; /* scrim */
  --z-modal:   1100; /* modal */
  --z-toast:   1200; /* notification */
}
```

If you find yourself writing `z-index: 9999` you have a stacking-context problem, not a number problem.

## Token export formats

Pick one and stick with it.

**1. Tailwind config** (most common in 2025):
```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        neutral: { 50: '#FAFAF7', 100: '#F2F2EC', ... },
        accent: { 500: '#FF4F2C', ... }
      },
      fontFamily: {
        display: ['PP Editorial New', 'serif'],
        body: ['Inter', 'system-ui', 'sans-serif']
      },
      spacing: { ... },
      borderRadius: { ... },
      transitionDuration: { ... },
      transitionTimingFunction: { ... }
    }
  }
}
```

**2. CSS custom properties** (framework-agnostic):
```css
:root {
  --color-neutral-50: #FAFAF7;
  --color-accent-500: #FF4F2C;
  --font-display: "PP Editorial New", serif;
  --space-4: 16px;
  --radius-md: 8px;
  --duration-quick: 200ms;
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
}
```

**3. Style Dictionary / DTCG JSON** (multi-platform projects):
```json
{
  "color": {
    "neutral": {
      "50": { "$value": "#FAFAF7", "$type": "color" }
    }
  }
}
```

## Anti-patterns

- ❌ Five neutrals named `gray`, `slate`, `zinc`, `stone`, `neutral` because Tailwind exposes them all. Pick one.
- ❌ A `color.primary` token that resolves to the same value as `color.accent.500`. Either use semantic OR primitive — don't half-name.
- ❌ A "secondary" color that gets used on three pages and a different "secondary" elsewhere. Either it's the same token everywhere or it's a different token.
- ❌ Magic numbers in component code. `padding: 14px` is a tell. The system uses `padding: var(--space-4)` (16px) or `var(--space-3)` (12px).
- ❌ Importing the entire `radix-ui/colors` package and only using one ramp. Tree-shake or copy the values you need.

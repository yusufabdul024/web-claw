# Color Theory for Websites

The Designer Agent's working knowledge of color: how to pick a palette that fits the brief, how to validate it for contrast, and how to test it in the real-world conditions of an LCD screen.

## The constraint

A great site uses fewer colors than a designer thinks. The Awwwards SOTD index, sampled across a year, averages ~4 unique colors per site (excluding semantic ones). Most published projects have:

- 1 neutral system (10–11 steps)
- 1 accent
- 1 voice (used sparingly)
- Semantic warnings (success, warning, error, info)

That's it. Five color decisions, fifteen tokens.

## Picking the accent

The accent is the brand color — what 90% of visitors will associate with the site.

**By vibe:**

| Vibe              | Accent direction                                            | Examples                  |
|-------------------|-------------------------------------------------------------|---------------------------|
| Editorial         | Deeply saturated single hue, dark-leaning                   | Burnt orange, indigo      |
| Brutalist         | High-saturation, often a primary                            | True red, electric yellow |
| Organic           | Warm earth tones                                            | Terracotta, moss, olive   |
| Futurist          | Neon or iridescent                                          | Cyan, lime, magenta       |
| Corporate-pop     | Mid-saturation, friendly                                    | Optimistic blue, mint     |
| Mono-minimal      | Often no accent — neutrals only                             | (deliberate restraint)    |

**By psychology** (use lightly — research on web color psychology is overstated):
- Blue: trust, calm, B2B default.
- Green: growth, wellness, environment.
- Red: urgency, food, sport.
- Yellow: warmth, energy, attention-getter for CTAs.
- Purple: creativity, luxury, premium.
- Black: authority, fashion.
- Orange: enthusiasm, accessible.
- Pink: warmth, contemporary brands.

**Picking the hex.**

Start with one of these workhorses if the brief is loose:

- Refined blue: `#1E3A8A` or `#0B2540`
- Mature green: `#1F5C3A` or `#0E6B4F`
- Editorial burgundy: `#6B1E2A`
- Warm orange: `#FF4F2C`
- Optimistic mint: `#3CCE7E`
- Soft yellow: `#FFC847`
- Brutalist red: `#FF1F1F`

Or pull from a serious palette catalog: [Radix Colors](https://www.radix-ui.com/colors), [Tailwind Color Generator](https://uicolors.app/), or [Open Color](https://yeun.github.io/open-color/).

## Picking the neutral

Three flavors:

- **True gray** — `#000` to `#FFF` with no temperature. Reads clinical, technical, brand-agnostic. Linear, Vercel use this lineage.
- **Warm gray** — slight yellow/brown tint. Reads editorial, premium, refined. Notion's defaults are warm.
- **Cool gray** — slight blue tint. Reads corporate, tech, B2B. iOS system colors are cool.

Pick a temperature that fits the vibe. A warm accent on a cool neutral feels electric; a warm accent on a warm neutral feels harmonious.

**Generating an 11-step neutral scale.**

In OKLCH:
```
neutral-50:  oklch(98% 0.005 [warm: 80 / cool: 250 / true: 0])
neutral-100: oklch(95% 0.005 h)
neutral-200: oklch(92% 0.005 h)
neutral-300: oklch(85% 0.008 h)
neutral-400: oklch(70% 0.010 h)
neutral-500: oklch(55% 0.010 h)
neutral-600: oklch(45% 0.010 h)
neutral-700: oklch(35% 0.008 h)
neutral-800: oklch(25% 0.005 h)
neutral-900: oklch(15% 0.005 h)
neutral-950: oklch(8%  0.003 h)
```

Adjust `h` (hue angle in degrees) to taste. Warm hues are around 70–90°; cool around 240–260°.

## Contrast math

**WCAG 2.2 minimums:**

| Text type        | AA ratio | AAA ratio |
|------------------|----------|-----------|
| Body text        | 4.5:1    | 7:1       |
| Large text (18pt+ or 14pt+ bold) | 3:1 | 4.5:1   |
| UI components, icons | 3:1  | n/a       |
| Focus indicators | 3:1      | n/a       |

**Computing contrast.**

Formula:

```
L1 = luminance of lighter color
L2 = luminance of darker color
ratio = (L1 + 0.05) / (L2 + 0.05)
```

Where luminance is computed from sRGB:

```
For each channel c in [r, g, b]:
  c_linear = c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ^ 2.4
L = 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear
```

Or just use [Stark](https://www.getstark.co/), [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/), the Chrome DevTools color picker, or `scripts/check-a11y.py`.

**Pairs to always validate.**

For every site:
- Body text on default surface.
- Body text on elevated surface (cards).
- Body text on dark surface (footer).
- Heading text on default surface.
- Accent color on default surface (for links).
- Button text on accent background.
- Placeholder text on input background.
- Disabled state text.
- Focus ring on every surface it appears against.

State each ratio in the style guide. Don't ship without numbers.

## APCA (next-gen contrast)

WCAG 2.2 uses a simplistic luminance model. APCA (used in WCAG 3 draft) is perceptually closer to how the eye actually reads. Worth knowing about; not yet a hard requirement.

For now: WCAG 2.2 AA is the legal floor, AAA is the design goal.

## Color blindness

8% of men have some form of red-green color blindness. Implications:

- Don't use color as the sole carrier of information. (E.g., red/green pass/fail indicators always have an icon too.)
- Test the design in protanopia / deuteranopia / tritanopia mode. Chrome DevTools → Rendering → Emulate vision deficiencies.

## Dark mode

If the site supports dark mode, design it as its own scheme, not as `filter: invert()`.

**Key differences:**

- Neutrals shift. The 950 might become the new 50, but the *steps* between them are not linear-mirrored. Dark mode usually has tighter steps in the dark range (more low-lightness gradations).
- Accent often shifts. The brand color at AAA contrast on white may be too dark on near-black. Lighten by 10–15% in OKLCH.
- Shadows become highlights. `box-shadow` on dark = subtle border (`box-shadow: 0 0 0 1px rgba(255,255,255,0.05)`).
- Images and videos may need a slight luminance compress to avoid retina-burning.

Implement via CSS custom properties with `[data-theme="dark"]` override, or via `prefers-color-scheme: dark` plus a manual toggle.

## On-screen vs. design tools

Designers picking colors in Figma should know:

- Figma displays in sRGB. So does most of the web. So screens.
- HDR / P3 / Display P3 are wider gamuts available on modern displays. If the design uses Display P3 colors, they're vivider than the sRGB equivalent — but only on capable screens.
- Don't pick colors on a calibrated 4K monitor and ship to a phone. Always check on a phone before sign-off.

## Anti-patterns

- ❌ Five neutrals named `gray`, `zinc`, `slate`, `stone`, `neutral`. You used Tailwind defaults without picking.
- ❌ Accent at lightness step `500` on white. Tested? Probably fails AA at body size. Move to `700` or `800` for text uses.
- ❌ Gradient backgrounds behind body text. Contrast varies across the gradient; body text fails AA somewhere.
- ❌ Hover state being only a color shift. Color-blind users miss it. Add a subtle scale or weight change.
- ❌ Designing in HEX-eyeballing mode. Use OKLCH or Lch in the tool of choice. Perceptual scales beat sRGB scales.
- ❌ Single-source-of-truth lying. The style guide says `#0B0F19` but the implementation uses `#0C0F1A`. Verify pixel-exact match.

## Quick decision-tree

```
What's the discovery vibe?
  ↓
Pick one accent direction (see table)
  ↓
Pick a specific hex from a workhorse or generator
  ↓
Pick a neutral temperature (warm / cool / true)
  ↓
Generate 11-step scale in OKLCH
  ↓
Validate contrast for every text-on-surface pair you'll use
  ↓
Lock the palette. Don't add a sixth color in week 3.
```

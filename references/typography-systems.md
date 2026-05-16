# Typography Systems

The Designer Agent's working knowledge of typography for websites: picking fonts, pairing them, building a scale, and ensuring legibility on the worst-case screen.

## The constraint

A scroll-stopping site uses **one or two type families**. Three is the maximum and almost always a mistake. The decision is between:

- **Single superfamily** — One typeface that ships display, text, and mono cuts (Inter, Söhne, GT America, ABC Diatype).
- **Pairing** — A display face for headings, a workhorse for body (and optionally a mono for code).

## Picking by vibe

| Vibe              | Display recommendation                                       | Body recommendation                  |
|-------------------|--------------------------------------------------------------|--------------------------------------|
| Editorial         | GT Sectra Display, PP Editorial New, Plantin                | Inter, Söhne, GT America             |
| Brutalist         | Neue Haas Grotesk Display, Manifold, ABC Diatype Mono       | Inter Tight, Söhne                   |
| Organic           | Source Serif Pro, Recoleta, Tiempos                         | Nunito Sans, Inter, Sohne            |
| Futurist          | GT Walsheim, PP Neue Montreal, NaN Tundra                   | Inter, JetBrains Mono                |
| Corporate-pop     | Inter Display, Söhne Breit, Aeonik                          | Inter, Söhne                         |
| Mono-minimal      | Helvetica Now Display, ABC Diatype, Inter                   | Inter, Söhne (same family or close)  |

## Free / open-source picks

If commercial license budget is zero:

- **Workhorse sans:** Inter (Google Fonts), Geist (Vercel, open-source), Atkinson Hyperlegible (Bring), IBM Plex Sans.
- **Display serif:** EB Garamond, Crimson Pro, Source Serif Pro, Fraunces (variable, wonderful for editorial).
- **Geometric:** Manrope, Lexend, Outfit.
- **Mono:** JetBrains Mono, Geist Mono, IBM Plex Mono, Iosevka.

## Commercial picks worth paying for

If there is a budget:

- Söhne (Klim Type Foundry) — workhorse sans, top of class.
- ABC Diatype (Dinamo) — clean geometric with character.
- GT America / GT Sectra (Grilli Type) — editorial workhorse.
- PP Neue Montreal (Pangram Pangram) — pay-what-you-want for personal, modest license for commercial.
- Founders Grotesk (Klim) — confident grotesk.
- Plus Jakarta Sans (free, exemplary quality).

## Variable fonts

Variable fonts ship multiple weights in one file and enable smooth interpolation. Modern, perf-friendly, and required for any project that uses font-weight animations.

Notable variable fonts:
- Inter — variable across 100–900 weight + 12 optical sizes.
- Fraunces — variable across SOFT, WONK, opsz axes (the wonkiest is a delight for editorial).
- Recursive — variable across MONO, CASL, slnt, CRSV, wght.
- Geist — variable.

Use `font-variation-settings` to animate weight/width/optical-size on hover for a signature interaction. `transition: font-variation-settings 200ms ease-out-quart`.

## Loading fonts

**Best practice (Next.js example):**
```ts
import { Inter } from 'next/font/google';
export const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-body'
});
```

`next/font` self-hosts (no Google Fonts request, no FOIT), preloads, and sets the font-display correctly. Use it.

**For self-hosted custom fonts:**
- Convert to WOFF2 (and only WOFF2 — drop WOFF and TTF).
- Preload in `<head>`: `<link rel="preload" as="font" href="..." type="font/woff2" crossorigin>`.
- Use `font-display: swap` so text appears immediately.
- Subset to the characters you need (latin, latin-ext). A full-font CJK fallback is 5MB.

**Total budget:** Two font families, two weights each, max 4 font files, max 200kb total.

## Building the scale

Modular scale at 1.250 (major third) is the safe default. Larger ratios (1.333, 1.414, 1.500) feel more dramatic; smaller ratios (1.125, 1.200) feel more academic.

**At a 16px body, 1.250 ratio:**

| Token           | Size           | Leading | Tracking      | Weight |
|-----------------|----------------|---------|---------------|--------|
| caption         | 12px           | 1.6     | 0             | 400    |
| body-sm         | 14px           | 1.55    | -0.003em      | 400    |
| body            | 16px           | 1.55    | -0.005em      | 400    |
| lead            | 18px           | 1.50    | -0.007em      | 400    |
| h4              | 20px           | 1.40    | -0.010em      | 600    |
| h3              | 25px           | 1.30    | -0.012em      | 600    |
| h2              | 31px           | 1.20    | -0.015em      | 600    |
| h1              | 49px           | 1.10    | -0.020em      | 600    |
| display         | 61px           | 1.05    | -0.025em      | 600    |
| display-xl      | 76–96px        | 1.00    | -0.030em      | 600    |

Use `clamp()` for fluid sizing:
```css
.h1 {
  font-size: clamp(2.5rem, 4vw + 1.5rem, 4rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
}
```

## Leading (line-height)

Inversely proportional to size:
- Body 16px → leading 1.55 (24.8px).
- H1 49px → leading 1.10 (54px).
- Display 96px → leading 1.00 (96px).

Bigger type needs tighter leading. Body needs more.

**Vertical rhythm:** Section padding is a multiple of the section's H2 leading. If H2 is 31px @ 1.20 (37.2px leading), section top padding might be 96px (2.5× the leading). This is what creates the "feels right" sensation.

## Tracking (letter-spacing)

Display sizes need negative tracking. Body sizes need ~0 or slightly negative. Caption sizes can use 0 or slightly positive for clarity.

- Display 80px: `letter-spacing: -0.025em`
- H1 48px: `letter-spacing: -0.02em`
- H2 32px: `letter-spacing: -0.015em`
- Body 16px: `letter-spacing: -0.005em`
- Caption 12px: `letter-spacing: 0` or `+0.02em` for uppercase eyebrows.

## Measure (line length)

Body text reads best at 60–80 characters per line. Set `max-width` on body paragraphs:
```css
.prose { max-width: 65ch; }
```

For wide content (feature grids, cards), don't push line length over 90ch. The eye loses the next line.

## OpenType features

Modern fonts ship OpenType features that nobody enables by default. Enable strategically:

```css
:root {
  font-feature-settings:
    "kern" 1,           /* kerning */
    "calt" 1,           /* contextual alternates */
    "liga" 1,           /* standard ligatures */
    "ss01" 1,           /* stylistic set 1, font-specific */
    "tnum" 0,           /* tabular numerals — only on tables/pricing */
    "ss02" 0;           /* font-specific stylistic alternates */
}

table, .price {
  font-feature-settings: "tnum" 1;  /* aligned-width digits */
}
```

For Inter specifically, `ss01` is the single-storey `a`/`g` — many designers prefer it.

## On-screen rendering pitfalls

- **Hairline serifs at body size on cheap LCD** — many serifs become mush at 16px on a low-DPI screen. Test on a Pixel 6a or similar before committing. If the body serif fails this test, use it only for display.
- **System anti-aliasing varies.** Mac and iOS use sub-pixel AA; Android uses gray AA. Type often looks chunkier on Android. Bump display weights 50–100 to compensate if it matters.
- **Variable font + slow connection.** Variable fonts are bigger files than single-weight cuts. If you only use 400 and 600, ship two static cuts (often smaller total). Variable wins when you use 3+ weights or animate.

## Pairing rules

If pairing two families:

1. **Contrast** — pair a serif display with a sans body, or a geometric display with a humanist body. Never two similar-flavored sans together.
2. **One personality dominant** — the display speaks, the body listens.
3. **Aligned x-heights** — visually, the lowercase heights should sit close. Inter's x-height is tall; pairing it with a high-x serif (Source Serif) reads coherently; pairing with a low-x classical serif (Times) feels off.
4. **Aligned tone of voice** — Söhne (workhorse) with Tiempos (classical serif) is editorial-confident. PP Neue Montreal (geometric) with PP Editorial New (display serif) is house-paired, designed to harmonize.

## Anti-patterns

- ❌ Three font families. Hard cap is two.
- ❌ Italic on H1. Editorial italics look great in body; on H1 they often look amateur unless the typeface is specifically designed for it.
- ❌ All-caps body. Reads slow. Reserve all-caps for tiny eyebrows (12px, +0.05em tracking).
- ❌ Justified text on the web. Browsers can't hyphenate well; you get rivers and gaps.
- ❌ Font-size: 14px body. Below 16px, mobile users zoom. 16px is the floor.
- ❌ Body text in display weight (700+). Heavy body looks shouty. Stay 400–500 for body.
- ❌ Loading three fonts × six weights = 18 files. Variable + subset.

## Quick decision-tree

```
What's the discovery vibe?
  ↓
Pick display + body (or single family)
  ↓
Verify license / cost
  ↓
Build the scale (modular 1.250 default)
  ↓
Define tracking + leading + weight per token
  ↓
Decide variable vs static (variable if animating weight or using 3+ weights)
  ↓
Preload + font-display: swap
  ↓
Test on a real Pixel-class device before sign-off
```

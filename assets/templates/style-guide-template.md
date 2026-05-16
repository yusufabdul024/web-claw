# Style Guide — <Project Name>

**Phase:** 1.3 (Web Claw)
**Authored by:** Designer Agent
**Based on:** `blueprint/discovery.md`, `blueprint/sitemap.md`
**Date:** <YYYY-MM-DD>

---

## Mood

**Three adjectives:** <e.g., "editorial, restrained, confident">

**Three-line description:**
> <Paragraph that paints the experience. What does this site feel like at a glance? What's the emotional register? What's it deliberately NOT?>

**Closest inspiration (verified live):** <URL>
**What we're taking from it:** <one line>
**What we're explicitly NOT taking:** <one line>

---

## Color

### Primitives — Neutrals

| Token              | Value (hex)   | OKLCH                 |
|--------------------|---------------|-----------------------|
| `neutral.50`       | `#FAFAF7`     | oklch(98% 0.005 80)   |
| `neutral.100`      | `#F2F2EC`     | oklch(95% 0.005 80)   |
| `neutral.200`      | `#E5E5DC`     | oklch(92% 0.005 80)   |
| `neutral.300`      | `#CFCFC3`     | oklch(85% 0.008 80)   |
| `neutral.400`      | `#A9A99B`     | oklch(70% 0.010 80)   |
| `neutral.500`      | `#7C7C70`     | oklch(55% 0.010 80)   |
| `neutral.600`      | `#535349`     | oklch(45% 0.010 80)   |
| `neutral.700`      | `#36362F`     | oklch(35% 0.008 80)   |
| `neutral.800`      | `#23231F`     | oklch(25% 0.005 80)   |
| `neutral.900`      | `#151512`     | oklch(15% 0.005 80)   |
| `neutral.950`      | `#0B0B09`     | oklch(8%  0.003 80)   |

**Temperature:** <warm | cool | true gray>

### Primitives — Accent

| Token              | Value         |
|--------------------|---------------|
| `accent.50`        | `<hex>`       |
| `accent.100`       | `<hex>`       |
| `accent.500`       | `<hex>` ★ the brand color |
| `accent.700`       | `<hex>` (for body-text uses where contrast must hit AA) |
| `accent.900`       | `<hex>`       |
| `accent.950`       | `<hex>`       |

### Primitives — Voice (single emphasis color, used rarely)

| Token              | Value         |
|--------------------|---------------|
| `voice.500`        | `<hex>`       |

### Semantic tokens

| Semantic                    | Resolves to              |
|-----------------------------|--------------------------|
| `surface.default`           | `{neutral.50}`           |
| `surface.elevated`          | `#FFFFFF`                |
| `surface.sunken`            | `{neutral.100}`          |
| `surface.inverse`           | `{neutral.950}`          |
| `text.primary`              | `{neutral.900}`          |
| `text.secondary`            | `{neutral.600}`          |
| `text.muted`                | `{neutral.400}`          |
| `text.on-accent`            | `{neutral.50}`           |
| `border.subtle`             | `{neutral.200}`          |
| `border.default`            | `{neutral.300}`          |
| `accent.action`             | `{accent.500}`           |
| `accent.action-hover`       | `{accent.700}`           |
| `success`                   | `<hex>`                  |
| `warning`                   | `<hex>`                  |
| `error`                     | `<hex>`                  |
| `info`                      | `<hex>`                  |

### Contrast validation

| Pair                                  | Ratio | Pass AA? | Pass AAA? |
|---------------------------------------|-------|----------|-----------|
| `text.primary` on `surface.default`   | 14.2  | ✅       | ✅        |
| `text.secondary` on `surface.default` | 6.8   | ✅       | ✅        |
| `text.muted` on `surface.default`     | 4.1   | ❌ (large only) | ❌ |
| `text.on-accent` on `accent.500`      | 5.4   | ✅       | ❌        |
| `accent.700` on `surface.default`     | 7.5   | ✅       | ✅        |
| Focus ring `accent.500` on `surface.default` | 4.9 | ✅ | n/a |

(Update for every actual pair used.)

---

## Typography

### Families

| Token                  | Family                          | Source / license            |
|------------------------|---------------------------------|-----------------------------|
| `font.display`         | `<e.g., "PP Editorial New">`    | <e.g., "Pangram Pangram, commercial license $50">  |
| `font.body`            | `<e.g., "Inter">`               | Google Fonts, OFL           |
| `font.mono`            | `<e.g., "JetBrains Mono">`      | Google Fonts, OFL (optional — omit row if no monospace is used) |

### Scale (modular 1.250 at 16px body)

| Token         | Size              | Leading | Tracking      | Weight |
|---------------|-------------------|---------|---------------|--------|
| `text.caption`| 12px              | 1.6     | 0             | 400    |
| `text.body-sm`| 14px              | 1.55    | -0.003em      | 400    |
| `text.body`   | 16px              | 1.55    | -0.005em      | 400    |
| `text.lead`   | 18px              | 1.50    | -0.007em      | 400    |
| `text.h4`     | 20px              | 1.40    | -0.010em      | 600    |
| `text.h3`     | 25px              | 1.30    | -0.012em      | 600    |
| `text.h2`     | 31px              | 1.20    | -0.015em      | 600    |
| `text.h1`     | clamp(2.5rem, 7vw, 4rem)   | 1.10    | -0.020em      | 600    |
| `text.display`| clamp(3.5rem, 9vw, 6rem)   | 1.05    | -0.025em      | 500    |

### OpenType features

```css
font-feature-settings: "kern" 1, "calt" 1, "liga" 1, "ss01" 1;
```

Tabular numerals on tables and pricing only: `font-variant-numeric: tabular-nums`.

---

## Spacing

**Base unit:** 4px

| Token      | Value  | Use                                    |
|------------|--------|----------------------------------------|
| `space.1`  | 4px    | Tight inline                           |
| `space.2`  | 8px    | Default inline                         |
| `space.3`  | 12px   | Small gap                              |
| `space.4`  | 16px   | Default gap                            |
| `space.5`  | 24px   | Card padding                           |
| `space.6`  | 32px   | Section internal padding               |
| `space.7`  | 48px   | Section margin                         |
| `space.8`  | 64px   | Section vertical padding (mobile)      |
| `space.9`  | 96px   | Section vertical padding (desktop)     |
| `space.10` | 128px  | Hero vertical padding                  |
| `space.11` | 192px  | Display section padding                |

---

## Containers

| Container          | Max width  | Padding (mobile / desktop) |
|--------------------|------------|----------------------------|
| `container.tight`  | 720px      | 16px / 24px                |
| `container.default`| 1120px     | 16px / 32px                |
| `container.wide`   | 1280px     | 16px / 32px                |
| `container.full`   | 100vw      | 0                          |

---

## Radii

| Token        | Value    | Use                              |
|--------------|----------|----------------------------------|
| `radius.none`| 0        | Brutalist defaults               |
| `radius.sm`  | 4px      | Inputs, small buttons            |
| `radius.md`  | 8px      | Buttons, cards                   |
| `radius.lg`  | 16px     | Modals, large cards              |
| `radius.xl`  | 24px     | Hero / signature blocks          |
| `radius.pill`| 9999px   | Tags, capsule buttons            |

(Use ≤ 3 different radii across the site.)

---

## Elevation

```css
--shadow-card:
  0 1px 2px rgb(0 0 0 / 0.04),
  0 4px 12px rgb(0 0 0 / 0.06);

--shadow-card-hover:
  0 4px 8px rgb(0 0 0 / 0.06),
  0 12px 24px rgb(0 0 0 / 0.08);

--shadow-modal:
  0 8px 16px rgb(0 0 0 / 0.08),
  0 24px 48px rgb(0 0 0 / 0.12);
```

On dark surfaces use a 1px subtle border in place of shadows.

---

## Iconography

- **Set:** <Lucide | Phosphor | Custom>
- **Stroke width:** <1.5px | 2px>
- **Default size:** 20px (inline), 24px (standalone), 16px (caption-sized)
- **Color:** `currentColor`

---

## Imagery direction

**Photography:** <e.g., "matte-flat, daylight, single subject, slight grain, color-shifted toward cool magenta">
**Illustration:** <e.g., "line-art, single stroke weight, fills only in accent">
**3D / WebGL:** <e.g., "iridescent abstract orb, no recognizable object">
**Generative:** <e.g., "feTurbulence-based noise overlay, 0.04 opacity, mix-blend overlay">

---

## Motion seeds

(Animator Agent extends in `animations.md`.)

| Token                  | Value                                 |
|------------------------|---------------------------------------|
| `duration.instant`     | 100ms                                 |
| `duration.quick`       | 200ms                                 |
| `duration.paced`       | 480ms                                 |
| `duration.narrative`   | 900ms                                 |
| `ease.out-quart`       | cubic-bezier(0.25, 1, 0.5, 1)         |
| `ease.out-back`        | cubic-bezier(0.34, 1.56, 0.64, 1)     |
| `ease.in-cubic`        | cubic-bezier(0.32, 0, 0.67, 0)        |
| `ease.in-out-cubic`    | cubic-bezier(0.65, 0, 0.35, 1)        |

---

## Anti-style

What this design will explicitly NOT do:

- ❌ <e.g., "No drop shadows on type">
- ❌ <e.g., "No tilted cards">
- ❌ <e.g., "No glassmorphism / backdrop blur on buttons">
- ❌ <e.g., "No multi-color gradient buttons">
- ❌ <e.g., "No italicized H1s">

---

## Token export

A JSON export of every token above lives at: `<project>/design/tokens.json`

(Generated by `scripts/extract-tokens.py` after this style guide is signed off.)

---

## Sign-off

- [ ] Colors: every pair contrast-validated; numbers stated.
- [ ] Type: scale tested at real sizes on a real mobile device.
- [ ] Spacing + radii + elevation: only one scale per axis.
- [ ] Imagery direction: concrete and reproducible.
- [ ] Anti-style: written and accepted.
- [ ] Ready to begin Phase 1.4: Wireframes.

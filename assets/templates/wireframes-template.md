# Wireframes — <Project Name>

**Phase:** 1.4 (Web Claw)
**Authored by:** UI Strategy Agent
**Based on:** `blueprint/discovery.md`, `blueprint/sitemap.md`, `blueprint/style-guide.md`
**Date:** <YYYY-MM-DD>

---

## Component inventory

Every reusable component. Pages compose these.

### `<Nav>`
- **Variants:** `default`, `scrolled` (compressed), `mobile-drawer`.
- **Props:** `links: { label, href }[]`, `cta?: { label, href }`.
- **Used on:** all pages.

### `<Hero>`
- **Variants:** `text-only`, `with-image`, `with-video`, `split`.
- **Props:** `eyebrow?`, `heading`, `sub?`, `primaryCTA: { label, href }`, `secondaryCTA?: { label, href }`, `media?: { type, src, aspect }`.
- **Used on:** Home, every top-level page.

### `<LogoBar>`
- **Props:** `label: string` ("Trusted by …"), `logos: { src, alt }[]`.
- **Used on:** Home.

### `<FeatureSection>`
- **Variants:** `left-media`, `right-media`, `text-only`, `dense`.
- **Props:** `eyebrow?`, `heading`, `body`, `bullets?`, `cta?`, `media?`.
- **Layout:** 12-col grid; media 6 cols, text 5 cols, gutter 1 col (desktop). Stacked (mobile).
- **Used on:** Home (×3), Product page.

### `<FeatureCard>`
- **Variants:** `icon`, `illustrated`, `with-image`.
- **Props:** `icon|illustration|image`, `label`, `body`, `cta?`.
- **Used on:** Home (Three Promises section), Features page.

### `<Stat>`
- **Props:** `value: number`, `label: string`, `suffix?: string` (e.g., "k", "%", "M").
- **Used on:** Home (Metrics row).

### `<Testimonial>`
- **Variants:** `with-photo`, `text-only`, `video`.
- **Props:** `quote`, `attribution: { name, role, company }`, `photo?`, `videoSrc?`.
- **Used on:** Home, Testimonials section / wall page.

### `<PricingCard>`
- **Props:** `tier`, `price`, `priceFrequency`, `features: string[]`, `cta: { label, href }`, `highlighted?: boolean`.
- **Used on:** Pricing page.

### `<FAQItem>`
- **Behavior:** accordion using `<details>`/`<summary>`.
- **Props:** `question: string`, `answer: ReactNode | MDX`.
- **Used on:** Home (FAQ), every page bottom FAQ if applicable.

### `<CTABlock>`
- **Variants:** `dark`, `light`, `gradient`, `full-bleed`.
- **Props:** `heading`, `body?`, `primaryCTA`, `secondaryCTA?`.
- **Used on:** Bottom of every page.

### `<Footer>`
- **Variants:** `sitemap`, `minimal`, `rich`.
- **Props:** `columns?`, `socialLinks`, `legalLinks`, `newsletterEnabled?: boolean`.

---

## Grid + spacing notes

- Container: `container.default` (1120px max, 16px/32px padding) for most sections.
- Container: `container.tight` (720px) for prose sections (FAQ answers, blog posts).
- Container: `container.full` for full-bleed signature sections.
- Grid: 12 columns desktop, 6 columns tablet, 1 column mobile.
- Gutters: 24px desktop, 16px mobile.
- Section padding: `space.9` (96px) desktop top/bottom, `space.8` (64px) mobile.

---

## Page wireframes

### Page: Home — `/`

**Container per section:** `container.default` unless noted.

#### Section 1 — Nav
- Component: `<Nav variant="default">`
- Logo left, links center, CTA right.
- Mobile: logo + hamburger.

#### Section 2 — Hero `<Hero variant="text-only">`

**Mobile (375px):**

```
┌─────────────────────────────┐
│ ☰  Logo                  →  │
├─────────────────────────────┤
│                             │
│  Eyebrow · Brand · Eyebrow  │  (12px caption, accent)
│                             │
│  Big H1 — three lines       │  (clamp(2.5rem, 7vw, 4rem))
│  Big H1 — three lines       │  Dominant element
│  Big H1 — three lines       │
│                             │
│  Sub copy — 14 words.       │  (18px lead)
│                             │
│ ┌─────────────────────┐    │
│ │  Primary CTA   →    │    │  (44px tap target)
│ └─────────────────────┘    │
│   secondary text link       │
│                             │
│   [16/9 hero media]         │
└─────────────────────────────┘
```

**Desktop (1280px+):**

```
┌──────────────────────────────────────────────────┐
│  Logo            Links            [Primary CTA]  │
├──────────────────────────────────────────────────┤
│                                                  │
│  Eyebrow · Brand · Eyebrow                       │
│                                                  │
│   Big H1 — two lines                             │
│   Big H1 — two lines                             │
│                                                  │
│   Sub copy in one wider sentence.                │
│                                                  │
│   [Primary CTA →]   secondary text link          │
│                                                  │
│         [Hero media — 16/9 — centered]           │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Hierarchy:** H1 dominant. CTA secondary. Sub tertiary. Eyebrow + nav recede.
**Dominant element:** H1.
**Whitespace:** generous; 96px above H1 on desktop.

---

#### Section 3 — Three Promises `<FeatureCard>` × 3

**Mobile:**
```
┌─────────────────────────────┐
│  Eyebrow                    │
│  Section heading (H2)       │
│                             │
│  [icon] Promise 1           │
│  body — 1 line              │
│  ─────                      │
│  [icon] Promise 2           │
│  body — 1 line              │
│  ─────                      │
│  [icon] Promise 3           │
│  body — 1 line              │
└─────────────────────────────┘
```

**Desktop:** Three columns, equal width, no dividers.

---

#### Section 4 — Pinned Product Reveal **[SIGNATURE]** `<custom>`

**Mobile:** Reduced-motion fallback: three stacked images + captions.
**Desktop:** Pinned scroll-driven canvas reveal. (Animator spec in `animations.md`.)

Wireframe blocks for desktop:
```
┌──────────────────────────────────────────────────┐
│                                                  │
│        [pinned canvas — 800×800 max]             │
│                                                  │
│        Caption 1 (large, fading)                 │
│                                                  │
│        Caption 2 (large, fading, replaces 1)     │
│                                                  │
│        Caption 3 (large, fading, replaces 2)     │
│                                                  │
└──────────────────────────────────────────────────┘
```
**Hierarchy:** Canvas product is dominant; captions secondary; everything else hidden during pin.
**Pin duration:** 3× viewport scroll.

---

#### Section 5 — Social Proof `<Testimonial>` × 4

**Mobile:** Vertical stack of testimonial cards.
**Desktop:** 2×2 grid; tile sizes vary slightly (top-left is larger with photo).

---

#### Section 6 — Pricing `<PricingCard>` × 1 (single plan)

**Mobile + desktop:** Single centered card, `container.tight`.

---

#### Section 7 — FAQ `<FAQItem>` × 6

**Mobile + desktop:** Accordion, `container.tight`. One-at-a-time expansion.

---

#### Section 8 — Bottom CTA `<CTABlock variant="dark">`

```
┌──────────────────────────────────────────────────┐
│                                                  │
│                                                  │
│         H2 echoing the hero H1                   │
│                                                  │
│         [Primary CTA →]                          │
│                                                  │
│                                                  │
└──────────────────────────────────────────────────┘
```
Full-width container, accent-tinted background, white text.

---

#### Section 9 — Footer `<Footer variant="minimal">`

Logo + 3 links + © year. Single row desktop; stacked mobile.

---

### Page: <Page A> — `/<path>`

(Same per-section breakdown as Home. Mobile + desktop wireframes for each.)

---

(Repeat for every page in the sitemap.)

---

## Responsive specifics

For each page, verify the following breakpoints don't break:

- 320px (smallest mobile)
- 375px (iPhone SE / Mini)
- 414px (Pro Max)
- 768px (iPad portrait)
- 1024px (iPad landscape / smallest laptop)
- 1280px (typical laptop)
- 1440px (common laptop)
- 1920px (desktop)

At each: no horizontal scroll, tap targets ≥ 44px, text not orphaned (no single word on the last line of a heading where avoidable).

---

## Hierarchy notes (cross-page)

- The same component (e.g., `<FeatureCard>`) has the same hierarchy treatment on every page.
- The H1 of every page is the highest visual weight on that page.
- The primary CTA of every page is reachable above the fold on mobile.

---

## Open questions for the user

If anything in the wireframes is uncertain, list it here.

1. <Question>

---

## Sign-off

- [ ] User has reviewed each page's mobile + desktop wireframes.
- [ ] User has confirmed the signature section per page.
- [ ] User has approved the component inventory (we won't add new component shapes during build).
- [ ] Ready to begin Phase 1.5: Motion Spec.

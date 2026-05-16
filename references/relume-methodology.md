# Relume Methodology

This is a distillation of the Relume approach to website information architecture and design — the workflow that has scaled from a single Webflow agency into a tool used by thousands of designers. The point of this file is to give the UX Strategy Agent enough of the Relume mental model to operate without depending on Relume's actual tools.

## The five stages (Relume's framing)

1. **Sitemap** — every page, every section, every CTA. Decided first, decided fully.
2. **Style guide** — color, type, spacing, tokens.
3. **Wireframes** — low-fi page structure.
4. **Design** — high-fi visual polish.
5. **Development** — code.

Web Claw uses stages 1–4 as Phase 1, then folds in motion (which Relume traditionally treats as a development concern) as stage 5, then enters Phase 2.

The signature insight of the methodology is **lock the IA before you design anything**. Most agencies design pages and then realize the IA is broken. Relume forces the IA discussion first, so design decisions don't have to be unmade.

## What Relume gets right

**Pages are made of sections.** Every page in the sitemap is a list of named sections. Each section has an intent, a CTA, and a copy outline. This is not radical, but it's done rigorously: you cannot move past the sitemap until every section is named.

**Sections are library components.** Relume's library is essentially a catalog of section patterns (`hero-12`, `cta-24`, `features-08`, etc.). Naming sections this way enforces composability — pages are assembled, not authored.

**Copy is part of the sitemap.** The H1, the sub, the CTA label — all decided at the sitemap stage. The wireframe doesn't have Lorem Ipsum; it has real copy.

**Style guide is tokens.** Color tokens, type tokens, spacing tokens. Not "blue and yellow with serif headlines." Token names and hex values.

**Wireframes are skeletal.** Boxes with intent labels. The wireframe doesn't pretend to be the design.

## What Relume's templates miss (and Web Claw fills in)

**Motion is an afterthought.** Relume's library is brilliant for static layouts. It says little about how a hero entrance feels, how scroll-triggered reveals choreograph, what the signature animated moment is. Web Claw fills this with a dedicated Motion Spec stage (Animator Agent).

**The signature moment is undefined.** Relume can give you 14 hero variants. None of them ask "what's the one moment on this site that makes a visitor stop?" Web Claw's discovery Q16 forces that question.

**Research is implicit.** Relume's library encodes thousands of design decisions, but it doesn't ask you to do site-specific research. Web Claw adds the Researcher Agent so each project draws on Awwwards-tier reference rather than only library patterns.

**Implementation is downstream.** Relume produces the design; the developer builds. Web Claw collapses that gap — the Implementer Agent reads the spec and writes the code in the same pipeline.

## How Web Claw uses Relume-style sectioning

When the UX Strategy Agent decomposes a page, use this vocabulary as a starting point. Pull from it, don't be bound by it.

### Hero variants

- `hero-text-only` — H1 + sub + CTA. No media. Editorial sites, brand sites with strong typography.
- `hero-with-image` — H1 + sub + CTA + horizontal product/lifestyle image.
- `hero-with-video` — H1 + sub + CTA + autoplaying loop background.
- `hero-split` — H1 left, media right, equal-ish columns.
- `hero-with-form` — H1 + sub + inline form. Reserve for high-intent traffic.
- `hero-animated` — H1 + sub + animated illustration / WebGL canvas. The signature hero.

### Trust / proof

- `logo-bar` — "Trusted by …" + 4–6 logos. Greyscaled, hover saturates.
- `metric-row` — 3–4 big numbers + labels. ("$2B processed. 14k customers. 99.99% uptime.")
- `testimonial-single` — One big quote, attribution.
- `testimonial-grid` — 3–6 testimonials in cards.
- `testimonial-wall` — masonry of many; for trust at scale.

### Feature / Story

- `feature-grid` — 3-, 4-, or 6-column tile grid with icon + label + body.
- `feature-alternating` — 60/40 image+text rows, alternating direction. Workhorse.
- `feature-tabs` — interactive tabs with media + body. For multi-faceted products.
- `feature-bento` — asymmetric tile grid. Used carefully.
- `feature-zoom` — pinned scroll-driven zoom into product detail. Signature device.

### Process / How it works

- `steps-numbered` — 3 or 4 numbered cards. Boring but legible.
- `steps-visual` — illustrated steps, often horizontal scroll on mobile.
- `steps-animated-line` — line draws as user scrolls, dots illuminate. Signature.

### Comparison

- `comparison-table` — vs competitor or vs status quo. Often "Us" vs "Them" two-column.
- `comparison-toggle` — vs / vs button switch.

### Pricing

- `pricing-single` — one plan, no decision fatigue.
- `pricing-tiered` — 2 or 3 tiers, recommended one elevated.
- `pricing-toggle` — monthly/annual switch.
- `pricing-calculator` — interactive estimator.

### FAQ

- `faq-accordion` — vertical accordion, expanded one at a time.
- `faq-grid` — open by default in 2 columns. Good for skimmers.

### CTA blocks

- `cta-banner` — dark band with headline + CTA. Section between content blocks.
- `cta-end` — full-bleed final section, big H2, single CTA. Ends the page.
- `cta-form` — inline newsletter signup.

### Footer

- `footer-sitemap` — multi-column links.
- `footer-minimal` — logo + 3 links + legal.
- `footer-rich` — sitemap + newsletter + social + recent posts.

## The two non-negotiables Web Claw adds

1. **Cuts in the sitemap.** The Relume method does not require an explicit "what we cut" section. Web Claw does. The "Cuts" section catches second-guessing and lets the user see the negative space.

2. **Signature section per page.** Web Claw marks exactly one section per page as SIGNATURE. The Animator Agent disproportionately invests motion there. Relume-style sectioning treats sections evenly; that's why so many Relume-built sites look polished but generic.

## How to think about a page in Relume style

A page is:

```
hero  →  proof  →  3 features  →  signature moment  →  social proof  →  CTA
```

Six sections. Not twelve. Six. Award-winning is short.

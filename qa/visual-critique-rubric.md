# Visual Critique Rubric

Use this rubric to score the visual quality of a built site beyond what Lighthouse and axe can measure. Score each axis 1–5 (5 best). A site is "scroll-stopping" when its **median across all axes is at least 4** AND **no axis is below 3**.

Each axis lists what 1, 3, and 5 look like, so scoring is anchored. Take screenshots at 375px (mobile) and 1280px (desktop) for each page before scoring.

Run this rubric:
- At the end of Phase 2 (before user sign-off): self-critique by the agent.
- At the end of Phase 3 (pre-launch checklist): again, with all real content.
- After any significant visual change in maintenance.

Output goes to `<project>/qa/visual-critique-<phase>.md` using the table at the bottom.

---

## Axis 1 — First-glance gist

How quickly does the brand vibe communicate? Read the H1 + hero. Look at the colors + type for 2 seconds, then look away. Can you say what this is and who it's for?

- **1 — Generic**: Hero could belong to any SaaS. The H1 is a feature list. No emotional read.
- **3 — Clear but flat**: You can describe what the product does in one sentence. Vibe is recognizable but unmemorable.
- **5 — Magnetic**: One word lands hard ("editorial," "playful," "premium"). You want to scroll.

## Axis 2 — Signature moment

There is exactly one "holy shit" moment per page (discovery.md Q16). Does it land?

- **1 — Missing**: No signature device. Every section looks the same weight.
- **3 — Present but tame**: The signature exists (e.g., a pinned scroll narrative) but reads as derivative or under-tuned.
- **5 — Earned**: The signature moment is the thing a friend would screenshot. It is *the* device, not *a* device.

## Axis 3 — Typographic hierarchy

Does the type system carry the design, or is it doing pretty colors a disservice?

- **1 — Visual noise**: Three font families, four weights, two italic styles. No clear H1>H2>H3 size jump.
- **3 — Functional**: Clean hierarchy. Body is readable. Display does its job. Nothing distinctive.
- **5 — Typography as design**: One signature treatment (variable-axis hero, kinetic word reveal, etc.). Reads as a deliberate choice.

## Axis 4 — Color discipline

Are 3–4 colors doing the entire job, or has the palette sprawled?

- **1 — Soup**: 5+ accent colors in one screen. Buttons, links, badges all different hues with no logic.
- **3 — Tidy**: 4 colors as planned. Used consistently but not particularly tuned.
- **5 — Composed**: One restrained palette where the accent appears *exactly* when it should. Voice color used once per screen, max.

## Axis 5 — Whitespace and rhythm

Does the layout breathe?

- **1 — Cramped or sparse**: Sections feel either packed or empty. Vertical rhythm is inconsistent.
- **3 — Consistent grid**: Spacing tokens are applied. Sections feel even.
- **5 — Composed rhythm**: Whitespace is doing dramatic work. Sections vary intentionally in density (e.g., a single-photo wide-margin section between two dense ones).

## Axis 6 — Motion taste

Does the motion serve the content, or is it decoration?

- **1 — Distracting**: Things move because they can. Multiple competing animations on one scroll.
- **3 — Reasonable**: Animations are smooth, not janky, reduced-motion respected. No standouts.
- **5 — Intentional**: Each animation has a single job (reveal, emphasize, transition). The signature moment uses motion as the device, not just a wrapper.

## Axis 7 — Mobile parity

The site is mobile-first. How does the mobile experience compare to desktop?

- **1 — Afterthought**: Layout breaks. Hero text wraps awkwardly. Signature moment doesn't translate.
- **3 — Functional**: Everything works. Layouts adapt. Nothing breaks.
- **5 — Mobile-native**: The mobile experience is *different* and *better* — shorter scroll, sharper hero, signature moment re-imagined for portrait. Not just compressed desktop.

## Axis 8 — Copy taste

Is the copy doing real work, or is it filler?

- **1 — Filler**: Lorem ipsum (any!) or copy that says "Welcome to our website" or "Click here to learn more."
- **3 — Functional**: Copy is on-brand and clear. Headlines describe features.
- **5 — Sharp**: Headlines have a point of view. CTAs use verbs that match the audience. Microcopy has personality without being cute.

## Axis 9 — Asset quality

Photos, illustrations, video — do they belong?

- **1 — Generic stock**: Smiling-handshake-stock-photo energy. Or AI-generated assets with visible AI artifacts.
- **3 — Adequate**: Real or licensed assets. Consistent style. Optimized.
- **5 — Considered**: Every asset earns its slot. Real photography (or art-directed AI) that supports the brand vibe.

## Axis 10 — Trust signal

Does it feel like a real, considered product or a template demo?

- **1 — Template**: Logos in a generic strip, identical testimonial cards, no real proof.
- **3 — Believable**: Real testimonials, real logos, claims that have backing.
- **5 — Confident**: Specific numbers, named customers, concrete proof, no hyperbole.

---

## Score sheet (copy into `<project>/qa/visual-critique-<phase>.md`)

| Axis                          | Score (1–5) | Notes |
|-------------------------------|-------------|-------|
| 1. First-glance gist          |             |       |
| 2. Signature moment           |             |       |
| 3. Typographic hierarchy      |             |       |
| 4. Color discipline           |             |       |
| 5. Whitespace and rhythm      |             |       |
| 6. Motion taste               |             |       |
| 7. Mobile parity              |             |       |
| 8. Copy taste                 |             |       |
| 9. Asset quality              |             |       |
| 10. Trust signal              |             |       |
| **Median**                    |             |       |
| **Minimum**                   |             |       |

**Pass criteria:** median ≥ 4 AND minimum ≥ 3.

If any axis is at 1 or 2, list the specific changes that would lift it to 3 in the Notes column. The Implementer Agent fixes axes scored at 1 before user sign-off; axes at 2 are flagged for user attention.

## Why these axes (and not others)

- **Lighthouse / axe** already cover technical performance and access. This rubric covers what they can't measure.
- **Why 10 axes, not 20**: more axes split attention and let real problems hide in averages. Ten is the smallest number that covers the four pillars (vibe, system, motion, content) without overlap.
- **Why median + minimum, not weighted sum**: a 5+5+5+5+5+5+5+5+5+1 score is *not* a pass. The minimum floor catches "one thing is broken."

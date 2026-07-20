# Inspiration Research - Web Claw v3

## Purpose

This reference defines how Web Claw researches design inspiration without depending on any single platform or canon.

The goal is not to collect pretty links. The goal is to produce design evidence the rest of the pipeline can act on.

## Source Hierarchy

1. User-provided sources.
2. Sources that match the user's sources.
3. Real, trusted shipped websites: award-winning sites (Awwwards, CSS Design Awards), international studio/agency portfolios and the client work inside them, strong product and brand experiences.
4. Moodboard/social/design-gallery references (Dribbble, Pinterest, Behance, Instagram, and similar) — mood and pattern evidence, not feasibility proof.
5. Technical references and library examples.
6. Built-in Web Claw references.

## Acceptable Source Types

Use any source type that helps the project:

| Source type | Best for | Caveat |
|-------------|----------|--------|
| User screenshots | Exact taste signals | Need user note: what to borrow/avoid. |
| Live websites | Layout, motion, feasibility | Do not copy exact code/assets/copy. |
| Product pages | Conversion structure, proof, interaction | Avoid competitor cloning. |
| Portfolios/agencies | Signature devices, art direction | Often heavy; check performance realism. |
| Dribbble | Visual mood, composition, UI polish | Concept work, not build proof. |
| Pinterest | Mood, palette, photography, editorial direction | Often source-poor; avoid copying imagery. |
| Behance | Case-study narrative, brand systems | Often polished presentation, not web UX. |
| Instagram | Motion, reels/carousels, designer taste | Links may be auth-gated or temporary. Ask for screenshots if needed. |
| TikTok/Reels | Motion taste, pacing, cultural references | Not build proof. |
| Are.na/Cosmos | Moodboard clusters, art direction | Often abstract; distill carefully. |
| Mobbin | Product UI patterns | App/product UI, not brand sites. |
| Land-book/Lapa/Godly/Siteinspire | Landing-page patterns | Can become generic if copied. |
| Codrops/articles | Interaction implementation | Technical fit still needs budget checks. |
| YouTube/videos | Technique walkthroughs | Verify recency and compatibility. |
| Award galleries | High-end web execution | Optional; not mandatory. |

## Research Minimum

Before `RESEARCH:MOODBOARD`, gather enough evidence to cover:

- at least 6 usable references total,
- at least 3 design axes,
- at least 2 sources that are shipped/built if motion or implementation claims are made,
- every user-provided source classified as borrow/avoid.

If this bar cannot be met in interactive mode, use the Inspiration Escalation Prompt.

## Inspiration Escalation Prompt

```text
I do not have enough taste evidence to design this responsibly yet. Please send 3-7 references. They can be websites, Dribbble shots, Pinterest boards, Behance projects, Instagram reels/carousels/posts, TikTok videos, screenshots, or a designer/brand you admire.

For each one, add one sentence:
- what should we borrow?
- what should we avoid copying?
```

## What To Capture Per Source

For every source:

- `kind`
- `title`
- `url` or `local_artifact`
- `provided_by`
- `date_accessed`
- `why_relevant`
- `what_taking`
- `what_not_taking`
- `axis`
- `applicable_to`
- `copying_risk`
- `implementation_notes`
- `verification_method`

For shipped websites, also capture:

- libraries/frameworks detected when relevant,
- performance/motion risk,
- whether the idea survives mobile and reduced motion.

## Copying-Risk Rules

| Risk | Meaning | Required mitigation |
|------|---------|---------------------|
| `none` | Abstract principle only. | None. |
| `low` | Common pattern or broad mood. | State what changes. |
| `medium` | Recognizable layout/motion/visual device. | Must write `what_not_taking`. |
| `high` | Source is close to user industry, competitor, or distinctive proprietary art. | Avoid direct adaptation; use only as anti-style or high-level learning. |

## Distillation Rules

Do not paste raw research dumps into canonical artifacts.

Every source must be distilled into one of:

- `research/inspiration-sources.md`
- `research/research-matrix.md`
- `research/moodboard.md`
- `research/taste-calibration.md`
- a decision file

## Social/Private Content

If Instagram, Pinterest, TikTok, or private boards are inaccessible:

1. Ask the user for screenshots, screen recordings, or short notes.
2. Record the source as `verification_method: user-provided`.
3. Do not claim runtime verification.

## What Good Research Sounds Like

Good:

> "We borrow the off-grid editorial headline treatment from Source 2, but not its cream palette or serif. It maps to the Home hero and can be implemented with CSS grid and responsive clamps. Copying risk low because the transferable idea is composition, not exact layout."

Bad:

> "This looks cool. Use it as inspiration."

## Required Output

By the end of open-web research:

- `sources.json` is structured enough for `scripts/research-matrix.py`.
- `research/inspiration-sources.md` is human-readable.
- `research/research-matrix.md` exists when possible.
- Weak evidence is surfaced, not hidden.

# Ignition — Quick Mode (7 Questions)

Use this when:
- The project is a single landing page or a small site (1–4 pages).
- The user already provided strong context in their initial request (brand name, vibe, reference URLs).
- The user explicitly says "quick start" or "let's just get going."

Pre-fill any answers already given by the user in their request. Do not re-ask what you already know.

---

## Greeting

> I'm running **Web Claw** — a structured pipeline for designing and building award-caliber websites. Before I start, I need 7 quick answers. Skip anything you don't know — I'll fill in a default and flag it.

---

## The 7 Questions

**1. What is it and who is it for?**
One sentence: the product or brand name and what it does for whom.
*(This becomes the H1 seed and og:description.)*

**2. What is the single action visitors should take?**
Be specific: demo booking, email signup, purchase, contact form submit. "Brand awareness" is not an action.

**3. How many pages at launch?**
If you're unsure, say "one page" and I'll propose a single-page structure.

**4. What's the feel? Pick one or describe your own:**
- **Editorial** — refined, slow, typographic
- **Brutalist** — loud, raw, blocky
- **Organic** — warm, hand-drawn, soft
- **Futurist** — dark, glowy, kinetic
- **Corporate-pop** — clean, bright, friendly
- **Mono-minimal** — monochrome, restrained, white-space-rich

**5. Do you have any existing assets?** (check all that apply)
Logo / Brand colors / Brand fonts / Copy / Photography / Product screenshots / None

**6. Tech preference?** (or say "you choose")
Next.js + Tailwind / Astro + Tailwind / Vite + Vanilla / SvelteKit / You choose

**7. How bold should the animations be?**
- **Restrained** — fades, subtle shifts. No scroll-jacking.
- **Active** — scroll reveals, pinned sections, parallax.
- **Maximalist** — scroll-jacking, WebGL, custom cursor.

---

## After Answers

1. Pre-fill any remaining fields from defaults. Flag each as `[ASSUMED: …]`.
2. Write `blueprint/discovery.md` using `assets/templates/discovery-template.md`.
3. Reflect back in 3–4 lines: brand vibe, primary action, motion intensity. Take corrections.
4. Advance to BLUEPRINT:SITEMAP. Update `memory.md`.

---

## Assumption Defaults (Quick Mode)

| Field | Default if unanswered |
|-------|----------------------|
| Pages | Single landing page |
| Stack | Astro + Tailwind (best perf for simple marketing pages) |
| Deploy | Vercel |
| CMS | None (static content) |
| Performance budget | Lighthouse mobile ≥ 90, LCP ≤ 2.5s |
| Accessibility | WCAG 2.2 AA |
| Analytics | None (add in Phase 3 if user wants) |

---

## Anti-patterns

- ❌ Don't ask all 7 questions in a wall of text. Present them grouped. Pause for answers.
- ❌ Don't accept "modern" as a feel answer. Push for one of the six palettes or three adjectives.
- ❌ Don't begin generating artifacts until `discovery.md` is written.
- ❌ Don't re-ask a question the user already answered in their initial message.

---

## When to Escalate to Full Mode

Switch to `references/ignition-full.md` if:
- The user describes a multi-page site with 5+ pages.
- The project has no existing brand identity.
- The user mentions complex animations, WebGL, or "Awwwards-level."
- The signature moment (the "holy shit" moment) is unclear after Quick Mode.

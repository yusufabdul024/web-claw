# Brief Interview — Quick Mode (9 Questions)

Use this when:
- The project is a single landing page or a small site (1–4 pages).
- The user already provided strong context in their initial request (brand name, vibe, reference URLs).
- The user explicitly says "quick start" or "let's just get going."

Pre-fill any answers already given by the user in their request. Do not re-ask what you already know.

---

## Greeting

> I'm running **Web Claw** — a structured pipeline for designing and building award-caliber websites. Before I start, I need 9 quick answers. Skip anything you don't know — I'll fill in a default and flag it.

---

## The 9 Questions

**1. What is your brand / company / business about, and who is it for?**
One or two sentences: the name, what it does, for whom, and why it exists.

**2. What is your value proposition?**
The one sentence that will be your hero headline. A stranger must understand it in 3 seconds: what is this, who is it for, what do I do next. Push back on insider slogans until it passes.

**3. What is the single action visitors should take — and the one objective the site is judged by?**
Be specific: demo booking, email signup, purchase, contact form submit. "Brand awareness" is not an action.

**4. How many pages at launch?**
If you're unsure, say "one page" and I'll propose a single-page structure.

**5. What's the feel? Pick one or describe your own:**
- **Editorial** — refined, slow, typographic
- **Brutalist** — loud, raw, blocky
- **Organic** — warm, hand-drawn, soft
- **Futurist** — dark, glowy, kinetic
- **Corporate-pop** — clean, bright, friendly
- **Mono-minimal** — monochrome, restrained, white-space-rich

**6. Send me 3–7 references — sites, screenshots, boards, or brands you'd be proud to resemble.**
For each, one line: what to borrow (layout, color, motion, typography, mood, or one specific section) and what NOT to copy.

Do not skip this and do not accept "I don't have any" as final — research runs off these. If they're stuck, work the ladder:
1. **Non-web brands** — "whose packaging, magazine, film titles, or store should this feel like?" Most people answer this instantly.
2. **Sites they enjoy using** — everyday favourites reveal density and interaction taste.
3. **Reaction round** — propose 3 named directions with 2 real example sites each; ask which is closest and what's wrong with it. Reacting beats generating.
4. Only if all three fail: record the Q5 adjectives as the sole anchor and flag the brief as thin-evidence.

Also ask: **what should this never look like?** One or two anti-references. Cheap to answer, high signal.

**7. Do you have any existing assets?** (check all that apply)
Logo / Brand colors / Brand fonts / Copy / Photography / Product screenshots / None

**8. Tech preference?** (or say "you choose")
Next.js + Tailwind / Astro + Tailwind / Vite + Vanilla / SvelteKit / You choose

**9. How bold should the animations be?**
- **Restrained** — fades, subtle shifts. No scroll-jacking.
- **Active** — scroll reveals, pinned sections, parallax.
- **Maximalist** — scroll-jacking, WebGL, custom cursor.

---

## After Answers

1. Pre-fill any remaining fields from defaults. Flag each as `[ASSUMED: …]`.
2. Test the value proposition against the 3-second test. If it fails, keep interviewing.
3. Write `brief/client-brief.md` using `assets/templates/client-brief-template.md`. Fill Q9a–9c from question 6, then write the Q9d **search anchors** — 3–5 searchable phrases (not adjectives) that `RESEARCH:OPEN-WEB` will run.
4. Reflect back in 3–4 lines: brand vibe, value proposition, primary action, motion intensity. Take corrections.
5. Advance to RESEARCH:SKILL-DISCOVERY. Update `memory.md`.

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

- ❌ Don't ask all 9 questions in a wall of text. Present them grouped. Pause for answers.
- ❌ Don't accept "modern" as a feel answer. Push for one of the six palettes or three adjectives.
- ❌ Don't accept a value proposition that only makes sense to insiders. It must pass the 3-second test.
- ❌ Don't leave question 6 empty. Open-web research runs off it — an empty Q9 produces generic research.
- ❌ Don't begin generating artifacts until `client-brief.md` is written.
- ❌ Don't re-ask a question the user already answered in their initial message.

---

## When to Escalate to Full Mode

Switch to `references/ignition-full.md` if:
- The user describes a multi-page site with 5+ pages.
- The project has no existing brand identity.
- The user mentions complex animations, WebGL, "award-level" ambition, or has unclear taste direction.
- The signature moment (the "holy shit" moment) is unclear after Quick Mode.

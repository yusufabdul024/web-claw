# IGNITION — Full Mode (17 Questions)

Use this when:
- Multi-page site (5+ pages).
- New brand with no existing visual identity.
- User wants maximalist animations or Awwwards-level ambition.
- The signature moment (Q16) is unclear after Quick Mode.

Pre-fill any answers already in the user's initial request. Do not re-ask.

---

## Greeting (read to user, lightly adapted)

> I'm running **Web Claw** — a two-phase pipeline that turns a website idea into a designed, animated, shippable site. Phase 1 is the blueprint (sitemap → style guide → wireframes → motion spec, Relume-style). Phase 2 is execution (Awwwards-grade research → master plan → three shippable slices).
>
> Before I start, I need to ask ~15 questions. Some you'll answer in one word; some need a sentence. Skip anything you don't know — I'll fill it in with a defensible default and flag it for you to override.
>
> Ready?

---

## Section 1 — The Brand (5 questions)

**1. What is the name of the site / product / brand?**
*(Used everywhere. If unsure, say "TBD" and I'll generate three name candidates.)*

**2. In one sentence, what does it do and for whom?**
*(This becomes the H1 candidate and the og:description seed.)*

**3. What is the single business outcome this site exists to drive?**
*(Lead form? Demo booking? Email signup? Purchase? "Brand awareness" is not an acceptable answer — pick the most measurable downstream action.)*

**4. Who is the primary visitor?** Describe them in 1–2 lines: role, sophistication, what they care about, what they're afraid of.
*(This drives copy register, density, and proof-density.)*

**5. What three adjectives describe the feel?** Pick from one of these palettes, or coin your own:
- *Editorial:* refined, slow, generous, typographic
- *Brutalist:* loud, blocky, raw, unapologetic
- *Organic:* warm, hand-drawn, soft, tactile
- *Futurist:* dark, glowy, kinetic, technical
- *Corporate-pop:* clean, bright, friendly, confident
- *Mono-minimal:* monochrome, restrained, structural, white space-rich

---

## Section 2 — The Scope (4 questions)

**6. How many pages?** List them. If you don't know, say "marketing site" and I'll propose: Home, About, Pricing, Blog index, Blog post, Contact.

**7. What's the primary CTA on every page?** (Most sites have one. Some have one per page. State it.)

**8. What content exists today?** Tick all that apply:
- [ ] Final copy
- [ ] Draft copy
- [ ] Logo
- [ ] Brand colors
- [ ] Brand fonts
- [ ] Photography / video
- [ ] Product screenshots / mockups
- [ ] None of the above — generate from scratch

**9. Reference sites you love.** Drop 3–5 URLs and one line per URL on *what specifically* you love (motion, layout, typography, copy, etc.). Awwwards SOTD picks are fair game.

---

## Section 3 — The Build (3 questions)

**10. Tech stack preference?** Pick one or say "you choose":
- Next.js (App Router) + Tailwind
- Astro + Tailwind
- SvelteKit + Tailwind
- Vanilla HTML/CSS/JS (Vite)
- You choose (I'll pick based on the motion spec and Vercel-friendliness)

**11. Deployment target?** Vercel / Cloudflare Pages / Netlify / static export / self-hosted / you choose.

**12. CMS?** None / Sanity / Contentful / Markdown files / Notion / you choose.

---

## Section 4 — The Guardrails (3 questions)

**13. Performance budget.** Default is Lighthouse mobile Performance ≥ 90, LCP ≤ 2.5s, CLS ≤ 0.1, INP ≤ 200ms. Override?

**14. Accessibility floor.** Default is WCAG 2.2 AA. Override?

**15. Motion intensity.** Pick one:
- *Restrained* — fades, slight y-shifts, no scroll-jacking. Editorial sites, B2B SaaS.
- *Active* — scroll-triggered reveals, pinned sections, parallax. Most agency and product sites.
- *Maximalist* — scroll-jacking, WebGL, custom cursors, sound. Awwwards SOTD territory.

---

## Section 5 — The Open Lane (2 questions)

**16. What would make you say "holy shit" when you saw the live site?**
*(One sentence. This becomes the signature moment we design around.)*

**17. Anything off-limits?** (Brands to avoid copying, motion patterns you hate, colors that are forbidden, words/claims legal won't allow, etc.)

---

## After the user answers

1. Write `blueprint/discovery.md` using `assets/templates/discovery-template.md`. Fill every field. Flag assumed fields explicitly as `[ASSUMED: …]`.

2. **Reflect back.** Tell the user in 4–6 lines: "Here's what I heard — does this match?" Cover (a) brand vibe, (b) primary outcome, (c) motion intensity, (d) signature moment. Take corrections.

3. **Set expectations.** Say: "Phase 1 will produce four artifacts (sitemap, style guide, wireframes, motion spec). I'll show you each and take corrections before moving on. Phase 2 (research + build) will take longer and produce three shippable slices. Sound good?"

4. **Update `memory.md`:** Phase = BLUEPRINT:SITEMAP, Next action = "Spawn UX Strategy Agent."

5. **Begin Phase 1.** Load `agents/ux-strategy-agent.md`.

---

## Anti-patterns when running ignition

- ❌ **Don't ask all 17 questions in one wall of text.** Group them, present visually, and pause for answers.
- ❌ **Don't accept "make it modern" as a vibe answer.** Push for the three adjectives. Modern is meaningless.
- ❌ **Don't move past Section 5 without Q16 answered.** The signature moment separates a clean site from an award-winning one. If the user can't articulate one, propose three and let them pick.
- ❌ **Don't begin generating artifacts before `discovery.md` is written and the user has confirmed.**
- ❌ **Don't assume the user knows jargon.** Define "scroll-jacking," "INP," "LCP" inline when you use them.
- ❌ **Don't re-ask answers already in the user's initial message.** Pre-fill and confirm.

---

## The two minutes before you ask the questions

1. Verify the working directory has space to create `<project>/blueprint/`, `<project>/research/`, `<project>/qa/`. If not, ask where outputs should go.
2. Skim `references/pattern-library.md` Layer 2 (section signatures) so you can talk fluently about Q16.
3. Check the user's initial message for partial answers. Pre-fill them. Only ask the remaining questions.

# Brief Interview — Full Mode (18 Questions)

Use this when:
- Multi-page site (5+ pages).
- New brand with no existing visual identity.
- User wants maximalist animations or Awwwards-level ambition.
- The signature moment (Q17) is unclear after Quick Mode.

Pre-fill any answers already in the user's initial request. Do not re-ask.

---

## Greeting (read to user, lightly adapted)

> I'm running **Web Claw v3** — a studio workflow that turns a website idea into a designed, animated, shippable site in four parts: brief, research, design, build. After this interview we do competitor analysis, inspiration research, and a moodboard together before any design is committed.
>
> Before I start, I need to ask ~18 questions. Some you'll answer in one word; some need a sentence. Skip anything you don't know — I'll fill it in with a defensible default and flag it for you to override.
>
> Ready?

---

## Section 1 — The Brand (6 questions)

**1. What is the name of the site / product / brand?**
*(Used everywhere. If unsure, say "TBD" and I'll generate three name candidates.)*

**2. What is your brand / company / business about?**
*(The story, the offer, what it does, why it exists — 2–4 lines. This is where the interview starts: understand the client before researching anything.)*

**3. What is the single business outcome this site exists to drive, and what must a visitor DO?**
*(Lead form? Demo booking? Email signup? Purchase? "Brand awareness" is not an acceptable answer — pick the most measurable downstream action. This is the one objective the site is judged by.)*

**4. What is your value proposition?**
*(One sentence a stranger understands in 3 seconds — this becomes the hero headline and the og:description seed. Keep pushing until it passes the 3-second test: what is this, who is it for, what do I do next.)*

**5. Who is the primary visitor?** Describe them in 1–2 lines: role, sophistication, what they care about, what they're afraid of.
*(This drives copy register, density, and proof-density.)*

**6. What three adjectives describe the feel?** Pick from one of these palettes, or coin your own:
- *Editorial:* refined, slow, generous, typographic
- *Brutalist:* loud, blocky, raw, unapologetic
- *Organic:* warm, hand-drawn, soft, tactile
- *Futurist:* dark, glowy, kinetic, technical
- *Corporate-pop:* clean, bright, friendly, confident
- *Mono-minimal:* monochrome, restrained, structural, white space-rich

---

## Section 2 — The Scope (4 questions)

**7. How many pages?** List them. If you don't know, say "marketing site" and I'll propose: Home, About, Pricing, Blog index, Blog post, Contact.

**8. What's the primary CTA on every page?** (Most sites have one. Some have one per page. State it.)

**9. What content exists today?** Tick all that apply:
- [ ] Final copy
- [ ] Draft copy
- [ ] Logo
- [ ] Brand colors
- [ ] Brand fonts
- [ ] Photography / video
- [ ] Product screenshots / mockups
- [ ] None of the above — generate from scratch

**10. Inspiration sources you love.** Drop 3–7 URLs, screenshots, boards, posts, reels, or designers, and one line per source on what specifically you love (motion, layout, typography, copy, mood, one section) and what we should **not** copy.

*This one is load-bearing — open-web research runs off it, so an empty answer produces generic research. Never accept "I don't have any" as final. Work the ladder:*
- *"Whose packaging, magazine, film titles, or store should this feel like?" — taste transfers across media, and most people answer this instantly even when they can't name a website.*
- *"What's a site you use often that feels good?" — everyday favourites reveal density and interaction taste.*
- *Reaction round: propose 3 named directions with 2 real example sites each and ask which is closest and what's wrong with it. Reacting beats generating.*
- *Only if all three fail: use the Q6 adjectives as the sole anchor and flag the brief as thin-evidence.*

**10b. And what should this never look like?** One or two anti-references, with a word on why. Cheap to answer, high signal — it feeds the moodboard's anti-style lane and cross-checks the competitor set.

---

## Section 3 — The Build (3 questions)

**11. Tech stack preference?** Pick one or say "you choose":
- Next.js (App Router) + Tailwind
- Astro + Tailwind
- SvelteKit + Tailwind
- Vanilla HTML/CSS/JS (Vite)
- You choose (I'll pick based on the motion spec and Vercel-friendliness)

**12. Deployment target?** Vercel / Cloudflare Pages / Netlify / static export / self-hosted / you choose.

**13. CMS?** None / Sanity / Contentful / Markdown files / Notion / you choose.

---

## Section 4 — The Guardrails (3 questions)

**14. Performance budget.** Default is Lighthouse mobile Performance ≥ 90, LCP ≤ 2.5s, CLS ≤ 0.1, INP ≤ 200ms. Override?

**15. Accessibility floor.** Default is WCAG 2.2 AA. Override?

**16. Motion intensity.** Pick one:
- *Restrained* — fades, slight y-shifts, no scroll-jacking. Editorial sites, B2B SaaS.
- *Active* — scroll-triggered reveals, pinned sections, parallax. Most agency and product sites.
- *Maximalist* — pinned narratives, WebGL, custom cursors, opt-in sound, or other high-craft moments.

---

## Section 5 — The Open Lane (2 questions)

**17. What would make you say "holy shit" when you saw the live site?**
*(One sentence. This becomes the signature moment we design around.)*

**18. Anything off-limits?** (Brands to avoid copying, motion patterns you hate, colors that are forbidden, words/claims legal won't allow, etc.)

---

## After the user answers

1. Write `brief/client-brief.md` using `assets/templates/client-brief-template.md`. Fill every field. Flag assumed fields explicitly as `[ASSUMED: …]`. From Q10/Q10b, fill Q9a–9c and then write the Q9d **search anchors**: 3–5 searchable phrases (not adjectives) that `RESEARCH:OPEN-WEB` will actually run.

2. **Test the value proposition (Q4) against the 3-second test.** If it fails, keep interviewing — the brief is not complete.

3. **Reflect back.** Tell the user in 4–6 lines: "Here's what I heard — does this match?" Cover (a) brand vibe, (b) value proposition, (c) primary outcome, (d) motion intensity, (e) signature moment. Take corrections.

4. **Set expectations.** Say: "Next we research together — competitor analysis, inspiration, and a moodboard you'll pick a direction from. Then design (sitemap, style guide, wireframes, motion spec), each shown for your sign-off. Then a phased build where you see the signature moments as soon as they work. Sound good?"

5. **Update `memory.md`:** Phase = RESEARCH:SKILL-DISCOVERY, Next action = "Begin companion skill discovery."

6. **Begin the Research part.** Load `agents/researcher-agent.md` + `references/extension-orchestration.md`.

---

## Anti-patterns when running ignition

- ❌ **Don't ask all 18 questions in one wall of text.** Group them, present visually, and pause for answers.
- ❌ **Don't accept "make it modern" as a vibe answer.** Push for the three adjectives. Modern is meaningless.
- ❌ **Don't accept an insider slogan as the value proposition.** Q4 must pass the 3-second test before the brief closes.
- ❌ **Don't close Q10 empty.** Open-web research is anchored on it. Work the ladder before falling back to adjectives.
- ❌ **Don't move past Section 5 without Q17 answered.** The signature moment separates a clean site from an award-winning one. If the user can't articulate one, propose three and let them pick.
- ❌ **Don't begin generating artifacts before `client-brief.md` is written and the user has confirmed.**
- ❌ **Don't assume the user knows jargon.** Define "scroll-jacking," "INP," "LCP" inline when you use them.
- ❌ **Don't re-ask answers already in the user's initial message.** Pre-fill and confirm.

---

## The two minutes before you ask the questions

1. Verify the working directory has space to create `<project>/brief/`, `<project>/research/`, `<project>/design/`, `<project>/qa/`. If not, ask where outputs should go.
2. Skim `references/pattern-library.md` Layer 2 (section signatures) so you can talk fluently about Q17.
3. Check the user's initial message for partial answers. Pre-fill them. Only ask the remaining questions.

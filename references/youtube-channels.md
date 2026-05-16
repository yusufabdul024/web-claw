# YouTube Channels — Vetted Seed List

This is the **seed list** for the Researcher Agent. None of the data below is guaranteed to be current — channels change. The Researcher Agent **verifies credibility at runtime** before recommending any video.

---

## Credibility heuristic (read this first)

Web Claw does NOT gate on a single subscriber number. Subscriber count is a stale proxy. A 2-year-old 250k channel can be coasting on tutorials about GSAP 3.6 while an 80k channel ships current GSAP 3.13 work weekly. The dossier needs *currency*, not *bigness*.

**Score each candidate channel on four signals.** A channel passes if it clears at least three.

| Signal               | Pass condition                                                                   | How to verify                                |
|----------------------|----------------------------------------------------------------------------------|----------------------------------------------|
| **Recency**          | Posted at least one video in the last 90 days that's relevant to web design.     | Channel's Videos tab sorted by date.         |
| **Library currency** | The relevant video demonstrates against a current major-version library.         | Check the runtime references / shown code.   |
| **Track record**     | Channel has shipped at least 18 months of relevant content.                      | Check the "Joined" date on the About tab.    |
| **Reach (signal)**   | Subscriber count is high *enough* to suggest the technique was vetted by an audience. Canonical floor lives in [`references/budgets.yaml → research.youtube_subscriber_signal_minimum`](budgets.yaml) (currently 50,000). Not a hard floor; weight against the other three signals. | About tab. |

**Picking the *video*, not just the channel.** A great channel is necessary, not sufficient. The video itself must:

1. Be **published in the last 18 months** (older is allowed only if the technique is provably still current).
2. Demonstrate a technique that **applies to a specific section** in the wireframes or motion spec.
3. Reference libraries at versions **compatible with the chosen stack**.
4. Either ship working source (CodePen, GitHub, Codrops) **or** include enough on-screen code to reproduce.

**Drop a channel** if any of these is true:
- No video in the last 90 days.
- All recent videos demonstrate against libraries the project is not using.
- Pivoted to unrelated content (gaming, finance, lifestyle).
- Sponsored content dominates the recent uploads.

---

## Tier 1 — Motion and effects

### Hyperplexed
- URL: https://www.youtube.com/@Hyperplexed
- Founded: 2021
- Focus: deconstructions of award-winning interaction techniques (magnetic buttons, scroll-driven type, card stack reveals). Codes everything from scratch, ships CodePen + GitHub.
- Why on this list: he reverse-engineers the *exact* interactions you see on Awwwards. The dossier should usually have one Hyperplexed entry.

### Olivier Larose
- URL: https://www.youtube.com/@olivierlarose1
- Focus: GSAP / Lenis / Framer Motion tutorials grounded in real freelance work. Smooth scroll, page transitions, scroll-triggered text reveal.
- Why on this list: practitioner, not just an educator. His patterns ship.

### Tom Bukowski / "tombuk"
- URL: https://www.youtube.com/@tombuk
- Focus: GSAP, Next.js, motion-rich marketing sites.
- Why on this list: builds the kind of marketing sites Web Claw targets.

### Coding in Public (Chris from "Coding in Public")
- URL: https://www.youtube.com/@CodinginPublic
- Focus: Astro-first builds, real client work breakdowns.
- Why on this list: Astro deserves a dedicated channel; this is the strongest one.

### Codrops (associated YT)
- URL: https://www.youtube.com/@codrops (and tympanus.net)
- Focus: experimental interaction patterns, well-documented.
- Why on this list: Codrops itself is the canonical reference for interaction patterns. The YT is sparser; the website is the primary reference.

### Bruno Simon
- URL: https://www.youtube.com/@BrunoSimon
- Founded: ~2018
- Focus: Three.js mastery. Runs `threejs-journey` (a paid course); has shipped landmark Awwwards sites (his portfolio is itself SOTD).
- Why on this list: the canonical Three.js reference. If the signature moment is 3D, his channel + course is the source.

---

## Tier 2 — Frontend craft

### Frontend Horse
- URL: https://www.youtube.com/@frontendhorse
- Focus: scroll-stopping CSS techniques, interaction polish, type system design.

### Theo (t3.gg)
- URL: https://www.youtube.com/@t3dotgg
- Focus: Next.js, React, server-side stuff. Less on motion, more on stack decisions.
- Why on this list: when the Implementer Agent is picking between Next.js patterns, Theo is a sanity check.

### Lee Robinson
- URL: https://www.youtube.com/@leerob
- Focus: Next.js / Vercel.
- Why on this list: defines the "correct" Next.js App Router pattern; useful for the Implementer Agent's stack decisions.

### Web Dev Simplified (Kyle Cook)
- URL: https://www.youtube.com/@WebDevSimplified
- Focus: explanatory, broad — JS, CSS, React.
- Why on this list: ubiquity check. If WDS has a video on the technique, you're not in cutting-edge territory anymore. Use to gauge what's "standard."

### Fireship (Jeff Delaney)
- URL: https://www.youtube.com/@Fireship
- Focus: 100-second deep-dives, tooling overviews.
- Why on this list: fast orientation on a new library or framework.

---

## Tier 3 — Design and UX context

### DesignCourse (Gary Simon)
- URL: https://www.youtube.com/@DesignCourse
- Focus: UI/UX walkthroughs, Figma + Webflow + code.

### Flux Academy
- URL: https://www.youtube.com/@FluxAcademy
- Focus: web design business + craft, freelance perspective.

### CharliMarieTV
- URL: https://www.youtube.com/@CharliMarieTV
- Focus: design career, brand design.

---

## Tier 4 — 3D and WebGL

### Yuri Artiukh / "akella"
- URL: https://www.youtube.com/@akella
- Focus: Three.js, GLSL shaders, WebGL.

### Wael Yasmina
- URL: https://www.youtube.com/@WaelYasmina
- Focus: Three.js step-by-step builds.

---

## Articles + sites (not YouTube, but cite from these)

- **Codrops** — https://tympanus.net/codrops/ — the canonical interaction pattern catalog. Every Awwwards designer reads it.
- **Smashing Magazine** — https://www.smashingmagazine.com/ — long-form articles on perf, a11y, animation.
- **CSS-Tricks** — https://css-tricks.com/ — useful for specific technique questions.
- **darkroomengineering blog** — https://darkroom.engineering — the team behind Lenis; their build articles are gold.
- **studiofreight blog** — animation craft.

## How the Researcher Agent uses this list

1. **For each project, pick 2–4 channels from this list** whose focus matches the project's vibe and motion intensity.
2. **Run the four-signal heuristic** on each picked channel against the candidates' current state (verify at runtime, not from this file).
3. **For each surviving channel, find one video that meets the per-video bar above.**
4. **Read the video / scan key minutes** to confirm the technique is documented (not just demoed).
5. **Write the dossier entry** per the format in `agents/researcher-agent.md`.

**Do not** cite a channel just because it's in this list. The dossier needs a specific video that applies to a specific section.

## Pruning policy

If a channel fails 2 or more of the four credibility signals during research, remove it from this list in your next commit with a one-line note in the commit message.

The list is a seed, not a contract. Channels age out.

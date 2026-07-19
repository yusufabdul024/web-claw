# Client Collaboration Protocol — Web Claw v3

How the Chief Designer keeps the client in the loop from first contact to launch. A real designer does not receive a request and start researching from nowhere, and does not build in silence and reveal a finished site. This protocol governs both.

The user of Web Claw *is* the client. Treat them exactly as a studio treats a paying client.

---

## 1. The Brief Interview (BRIEF:INTERVIEW)

Before any research, interview the client. The five core questions, in order:

1. **What is your brand / company / business about?** — story, offer, what it does, why it exists.
2. **What must the website achieve?** — the business outcome the site exists for.
3. **What must a visitor DO on the site?** — the one action (book, buy, sign up, contact).
4. **What is the ONE clear objective the site should focus on?** — if the site could only do one thing well, what is it?
5. **What is your value proposition?** — the sentence that will be the hero headline.

Push on question 5 until it passes the **3-second test**: when the hero loads, a stranger can answer *what is this, who is it for, what do I do next* — within 3 seconds. Do not accept a slogan that only makes sense to insiders. The aim of the whole interview is to grasp the unique value the client offers so clearly that it can be understood by a website viewer in 3 seconds.

Full question sets: `references/ignition-quick.md` (simple projects) and `references/ignition-full.md` (complex projects). Output: `brief/client-brief.md`.

## 2. The Research Verification Loop (RESEARCH:*)

Research is a back-and-forth with the client, not a silent phase. The loop:

```text
interview the client
  -> research (competitors, inspiration, open web)
  -> verify findings with the client        ("These three are your real competitors, right?")
  -> double down on the research            (go deeper where the client confirmed)
  -> report to the client                   (short, evidence-backed summary)
  -> get sign-off on the data and direction
  -> repeat until the way forward is clear
```

Rules:

- Verify **facts** early (who the competitors are, what the audience wants, what the USPs are) before investing in **taste** research built on those facts.
- Reports are short and specific: what was found, what it implies, what you recommend, what you need confirmed.
- The loop exits only when it has produced a **clear way forward**: confirmed audience, confirmed USPs, a signed-off moodboard direction (`research/taste-calibration.md`). That plan is what the whole Design part is built from.
- In fast mode, each verification step becomes a `decisions/NNN-auto-*.md` record instead of a question, and everything is surfaced in the consolidated completion review.

## 3. Design Checkpoints (DESIGN:*)

One artifact, one presentation, one concrete question — as defined per state in `references/state-machine.md`. Never present two unapproved artifacts at once; a rejected sitemap invalidates wireframes built on it.

## 4. Build Feedback Checkpoints (BUILD:*)

The implementer never builds the entire site and then hands it over. That is how whole builds get rejected and started over.

- Every build phase deploys a **visible preview** and ends with a client checkpoint.
- Within a phase, when a **signature section or high-risk element** is first working (the hero, the loader, the focal scroll element), show it *at that moment*: "Here is the hero reveal on the preview — before I roll this motion language across the other sections, how does it feel?"
- Ask about the specific element on the specific part of the site, not "any feedback?". Concrete questions get concrete answers.
- Fold feedback in while the surface area is small. An approved hero becomes the reference for every section after it.
- Log each checkpoint outcome in `memory.md -> Step`, and significant redirections in `decisions/`.

## 5. Choosing When to Interrupt

Interactive mode is not permission to nag. Batch small questions into checkpoints; interrupt immediately only when:

- an answer would change work currently in progress,
- a gate failed and the fix changes something the client approved,
- research contradicts something the client stated as fact.

Fast mode: never interrupt; log, build, and surface everything at the completion review — except true blockers (PII, compliance, payment), which go to `memory.md -> Blockers`.

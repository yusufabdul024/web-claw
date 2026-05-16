# Memory Format — Web Claw Project Memory System

## Purpose

Every Web Claw project maintains a `memory.md` at its root. This file is the **single source of truth for project state**. It survives context compaction, session resets, agent swaps, and platform changes.

**Rule: Read `memory.md` first. Write `memory.md` last. Every session, no exceptions.**

---

## The `memory.md` Schema

Copy this template into `<project>/memory.md` when a project initializes. Keep values terse. This file is parsed by agents, not read by humans.

```markdown
# Project Memory — <Project Name>
Last updated: <YYYY-MM-DD HH:MM>

## Identity
- Name: <project name>
- Goal: <single sentence from discovery Q3 — the measurable business outcome>
- Audience: <one sentence from discovery Q4>
- Motion: <restrained | active | maximalist>
- Stack: <chosen framework, e.g. "Next.js App Router + Tailwind" | PENDING>
- Deploy: <Vercel | Cloudflare Pages | Netlify | static | PENDING>

## State
- Mode: <interactive | fast>
- Phase: <IGNITION | BLUEPRINT:SITEMAP | BLUEPRINT:STYLE-GUIDE | BLUEPRINT:WIREFRAMES | BLUEPRINT:ANIMATIONS | RESEARCH:AWWWARDS | RESEARCH:YOUTUBE | EXECUTION:STACK | EXECUTION:PLAN | EXECUTION:PHASE-1 | EXECUTION:PHASE-2 | EXECUTION:PHASE-3 | QA:FINAL | DONE>
- Step: <short label, e.g. "sitemap — awaiting user sign-off" or "phase-1 — step 3 of 8">
- Last artifact: <relative path to last produced file, e.g. "blueprint/sitemap.md">
- User sign-off: <YES | NO | PENDING | AUTO>
- Next action: <one imperative sentence — exactly what the resuming agent must do first>

## Pinned Decisions
- [DECISION-001] <topic> → decisions/001-<topic>.md
<!-- Add entries as decisions are made. Agents must read referenced files before re-litigating. -->

## Blockers
<!-- List open questions the user must resolve before the pipeline can proceed. Remove when resolved. -->
- None

## Compaction Snapshot
<!-- Populated only when context nears its limit. Contains last artifact verbatim + artifact summaries. -->
<!-- An agent picking up after compaction reads this section first, then resumes from Next action above. -->
```

---

## Field Definitions

| Field | Purpose | Rules |
|-------|---------|-------|
| `Last updated` | Timestamp of last write | Always update before ending a session |
| `Name` | Project name | From discovery Q1 |
| `Goal` | Primary business outcome | Measurable verb: "convert", "sign up", "purchase". Not "awareness". |
| `Audience` | Primary visitor description | From discovery Q4, max 20 words |
| `Motion` | Motion intensity level | Must match discovery Q15 exactly |
| `Stack` | Chosen tech stack | PENDING until EXECUTION:STACK phase is complete |
| `Deploy` | Deploy target | PENDING until EXECUTION:STACK phase is complete |
| `Mode` | Run mode | `interactive` (default, user signs off each state) or `fast` (auto-approve states, QA gates still hard) |
| `Phase` | Current pipeline state | Must use the exact state label from the state machine |
| `Step` | Sub-step within phase | Free text, short, descriptive |
| `Last artifact` | Path to last produced file | Relative to project root |
| `User sign-off` | Whether user approved last artifact | PENDING until user explicitly approves. `AUTO` in fast mode means the agent auto-approved and logged the decision. |
| `Next action` | First thing resuming agent must do | Imperative. Single sentence. No ambiguity. |
| `Pinned Decisions` | Index of locked decisions | Links to `decisions/NNN-topic.md` files |
| `Blockers` | Questions only the user can answer | Remove when resolved. In fast mode, blockers accumulate and are surfaced at completion review. |
| `Compaction Snapshot` | Emergency context preservation | See compaction protocol below |

---

## The `decisions/` Folder

Every significant choice gets its own file: `decisions/NNN-topic.md` where NNN is zero-padded (001, 002, etc.).

**When to create a decision file:**
- Tech stack or framework choice
- Motion intensity level (if changed from discovery default)
- Rejecting a color palette, type pairing, or layout approach
- Pivoting a page's goal or removing/adding a page
- Any user override of an agent default

**Decision file format:**

```markdown
# Decision NNN — <Topic>
Date: <YYYY-MM-DD>
Decided by: <User | Agent default | Joint>

## Decision
<One sentence: what was decided.>

## Rationale
<Two to four sentences: why this and not something else.>

## Rejected alternatives
- <Option A>: <one-line reason for rejection>
- <Option B>: <one-line reason for rejection>

## Constraints this creates
<Any downstream consequences agents must respect.>
```

**Example:**

```markdown
# Decision 003 — Tech Stack
Date: 2025-11-14
Decided by: User

## Decision
Next.js 15 (App Router) + Tailwind CSS 4 + GSAP + Lenis. Deployed to Vercel.

## Rationale
User confirmed Vercel deployment. Motion spec is Active, requiring GSAP ScrollTrigger. Next.js App Router matches the SaaS product shape and enables RSC for fast initial paint. Tailwind 4 for rapid token application.

## Rejected alternatives
- Astro: rejected because site has shared React state across sections (cart, auth).
- SvelteKit: rejected because user team is React-familiar.
- Framer Motion only: insufficient for ScrollTrigger orchestration in signature section.

## Constraints this creates
- Must use GSAP ScrollTrigger for all pinned-scroll effects.
- Image optimization via next/image from Phase 1.
- Lenis must bail out on prefers-reduced-motion.
```

---

## First Read / Last Write Protocol

This protocol is mandatory. Paste it verbatim into the SKILL.md body and into every agent file header.

### First Read (before any action)

```
1. Read memory.md
2. Read any decisions/ files listed in Pinned Decisions
3. Read the Last artifact file listed in memory.md
4. Only then begin work
```

If `memory.md` does not exist, the project has not been initialized. Run `scripts/init-project.py`.

If `User sign-off: PENDING` or `NO`, do not proceed to the next phase. Present the last artifact to the user and resolve the sign-off first.

### Last Write (before ending any session)

```
1. Update memory.md:
   - Phase and Step (advance if artifact was accepted)
   - Last artifact path
   - User sign-off status
   - Next action (precise imperative for the resuming agent)
2. If a decision was made: create decisions/NNN-topic.md
3. If context is near its limit: write the Compaction Snapshot (see below)
```

---

## Compaction Snapshot Protocol

When the context window is near its limit — or before ending a long session — write the Compaction Snapshot into `memory.md`. This preserves enough state that a fresh agent session can resume without re-reading the conversation.

**Format for the Compaction Snapshot section:**

```markdown
## Compaction Snapshot
Captured: <YYYY-MM-DD HH:MM>

### Artifact summaries (all produced artifacts)
- discovery.md: Project is [Name], goal is [goal], audience is [audience], motion is [level].
- sitemap.md: [N] pages: Home (goal: X), [other pages]. Signed off YES.
- style-guide.md: Colors: [primary token + hex]. Type: [heading font / body font]. Signed off YES.
- wireframes.md: [N] pages wireframed. Signature section: [section name]. Signed off YES.
- animations.md: [motion summary]. Signed off [YES/NO].
<!-- Continue for all artifacts -->

### Last artifact verbatim
<!-- Paste the full text of the most recent artifact here if it is < 2000 tokens.
     If larger, paste only the most critical section (e.g., the signature section spec). -->

### Current work in progress
<!-- If mid-artifact, describe exactly where: "Designer Agent was mid-way through color token spec. Palette chosen: neutral #0B0F19, accent #FF4F2C. Typography not yet decided." -->
```

**When to trigger:** Any time remaining context tokens are estimated below 20% of the model's window. Err on the side of triggering early.

**After a compaction snapshot is written:** The resuming agent reads only `memory.md` (which contains the snapshot) + the `decisions/` files. It does NOT need to re-read prior artifacts unless a specific field is missing.

---

## What Correct `memory.md` Looks Like Mid-Project

```markdown
# Project Memory — Meridian
Last updated: 2025-11-15 14:32

## Identity
- Name: Meridian
- Goal: Convert qualified B2B visitors into demo bookings (measured: demo-request form submit)
- Audience: CTOs and VPs Eng at 50–500-person SaaS companies, evaluating infra tooling
- Motion: active
- Stack: Next.js 15 App Router + Tailwind CSS 4 + GSAP 3.12 + Lenis 1.1 + Framer Motion 11.5
- Deploy: Vercel

## State
- Mode: interactive
- Phase: EXECUTION:PHASE-1
- Step: phase-1 — step 4 of 9 (implementing TokenProvider and global CSS variables)
- Last artifact: phase-1.md
- User sign-off: YES (phase-1.md approved on 2025-11-15)
- Next action: Open app/globals.css and implement all CSS custom properties from style-guide.md §Color tokens. Run dev server and verify tokens render on /. Then update memory.md.

## Pinned Decisions
- [DECISION-001] motion intensity → decisions/001-motion-intensity.md
- [DECISION-002] stack → decisions/002-stack.md
- [DECISION-003] sitemap cuts → decisions/003-sitemap-cuts.md

## Blockers
- None

## Compaction Snapshot
<!-- None yet -->
```

This is what any agent needs to resume work confidently without asking a single question.

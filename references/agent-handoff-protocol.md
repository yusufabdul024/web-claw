# Agent Handoff Protocol — Web Claw

## Purpose

This document defines how to spawn subagents and how agents hand off between each other. It ensures agents receive exactly what they need — no more, no less — preventing context fog and wasted tokens.

---

## The Minimal Handoff Rule

When spawning a subagent, pass **exactly three things**:

1. **`memory.md`** — current project state and pinned decisions index
2. **The agent file** — e.g., `agents/designer-agent.md`
3. **The input artifacts** — only the files that agent explicitly lists in "Inputs you require"

Do **not** pass:
- The full conversation history
- Other agents' files
- Reference files the agent did not ask for
- Prior artifacts the agent does not need

Isolation is the feature. A subagent with a clean, minimal context produces more consistent output than one drowning in everything that has happened so far.

---

## Spawning Template

When invoking a subagent (via Task tool, Codex CLI, or any other mechanism), use this structure:

```
Read memory.md at: <path>/memory.md
Read your agent brief at: <path>/agents/<agent-name>.md
Read these input files: <list the paths from "Inputs you require" in the agent file>
Your task: <one imperative sentence — what the agent must produce>
Output goes to: <path to output file>
When done: update memory.md → Last artifact, User sign-off (PENDING), Next action.
```

**Example — spawning the Designer Agent (interactive mode):**

```
Read memory.md at: ./meridian/memory.md
Read your agent brief at: ./web-claw/agents/designer-agent.md
Read these input files:
  - ./meridian/blueprint/discovery.md
  - ./meridian/blueprint/sitemap.md
  - ./web-claw/references/color-theory.md
  - ./web-claw/references/typography-systems.md
  - ./web-claw/references/design-systems.md
Your task: Produce blueprint/style-guide.md using assets/templates/style-guide-template.md. Present it to the user. Stop before moving to wireframes.
Output goes to: ./meridian/blueprint/style-guide.md
When done: update memory.md -> Last artifact = blueprint/style-guide.md, User sign-off = PENDING, Next action = "Spawn UI Strategy Agent to produce wireframes.md".
```

**Example — spawning in fast mode:**

```
Read memory.md at: ./meridian/memory.md  (Mode: fast)
Read your agent brief at: ./web-claw/agents/designer-agent.md
Read these input files: [as above]
Your task: Produce blueprint/style-guide.md. Make any judgment calls per operating principles; do NOT pause for user approval. For each judgment call (palette pick, type pairing), produce decisions/NNN-auto-<topic>.md with the rationale.
Output goes to: ./meridian/blueprint/style-guide.md
When done: update memory.md -> Last artifact = blueprint/style-guide.md, User sign-off = AUTO, Next action = "Spawn UI Strategy Agent to produce wireframes.md".
```

---

## Context Budget by Phase

A rough token budget guide for each phase. Stay within it. If you're over, remove context, don't expand the window.

| Phase | Load in context |
|-------|----------------|
| IGNITION | SKILL.md + ignition-quick.md or ignition-full.md |
| BLUEPRINT:SITEMAP | ux-strategy-agent.md + discovery.md + relume-methodology.md |
| BLUEPRINT:STYLE-GUIDE | designer-agent.md + discovery.md + sitemap.md + color-theory.md + typography-systems.md |
| BLUEPRINT:WIREFRAMES | ui-strategy-agent.md + discovery.md + sitemap.md + style-guide.md + pattern-library.md (Layer 2) |
| BLUEPRINT:ANIMATIONS | animator-agent.md + discovery.md + wireframes.md + style-guide.md + animation-libraries.md + pattern-library.md (all layers) |
| RESEARCH:AWWWARDS | researcher-agent.md + animations.md + pattern-library.md (Layer 2 + Layer 4 matrix) |
| RESEARCH:YOUTUBE | researcher-agent.md + animations.md + youtube-channels.md |
| EXECUTION:STACK | implementer-agent.md + tech-stack.md + animations.md + discovery.md + performance-budgets.md |
| EXECUTION:PLAN | implementer-agent.md + all blueprint + both research + tech-stack.md |
| EXECUTION:PHASE-N | implementer-agent.md + phase-N.md + memory.md |
| QA:GATE | qa-agent.md + phase-N-gate.md + preview URL |
| QA:FINAL | qa-agent.md + pre-launch-checklist.md + all qa reports |

**Never load all references simultaneously.** Load only what the current agent file's "Inputs you require" section lists.

---

## The Output Contract

Every agent must self-audit before delivering its artifact. The Output Contract is a non-negotiable checklist added to the end of every agent file.

Standard output contract (all agents):

```
## Output Contract — Complete Before Delivering

- [ ] Every section of the template is filled. No placeholder text remains.
- [ ] No lorem ipsum exists anywhere in the artifact.
- [ ] All cited URLs, channel names, or library versions were verified at runtime (not from memory).
- [ ] memory.md updated:
      - Last artifact: <path>
      - User sign-off: PENDING
      - Next action: <what the next agent or session must do>
- [ ] If any significant decision was made: decisions/NNN-topic.md was created and added to memory.md → Pinned Decisions.
- [ ] The artifact was presented to the user with the specific sign-off question from references/state-machine.md.
```

Agent-specific additions are noted in each agent file.

---

## Resuming After a Break or Compaction

When resuming a project after a context reset, session end, or compaction:

1. **Read `memory.md`** — get the current Phase, Step, Last artifact, and Next action.
2. **Read the `decisions/` files** listed in Pinned Decisions.
3. **Read the Last artifact file** — confirm it exists and matches what `memory.md` says.
4. **If `User sign-off: PENDING`** — re-present the artifact. Ask the sign-off question. Do not advance.
5. **If `User sign-off: YES`** — execute the Next action exactly as written.
6. **If `Compaction Snapshot` exists** in `memory.md` — read it before reading any artifact files. It contains summaries of all prior artifacts and may be sufficient context.

Do not reconstruct context from conversation history. The filesystem has it.

---

## Manual Mode (For $25/month Plans)

If you are using a platform or plan that does not support subagent spawning, follow this equivalent manual workflow:

1. Open a new chat session.
2. Copy-paste the contents of `memory.md` into the first message.
3. Copy-paste the contents of the relevant agent file.
4. List the input artifact files the agent needs (or paste their contents if short).
5. Give the single task sentence.
6. When done: copy-paste the output back into the project folder. Update `memory.md` manually or ask the agent to give you the updated `memory.md` fields.

**This works.** The skill was designed to function in Manual Mode. You trade parallelism (phases run sequentially, no subagents) and **tool-driven QA automation** (the agent can't run Lighthouse / pa11y / Playwright / contrast / bundle scripts — those must be run locally and pasted back) for portability. Output quality also depends on the underlying model. See `references/platform-compat.md` for the full caveats.

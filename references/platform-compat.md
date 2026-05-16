# Platform Compatibility — Web Claw

Web Claw is designed to run on any AI coding agent platform. This reference covers how to invoke the skill and manage memory on each.

---

## Claude Code

**Invoking the skill:**
- Web Claw triggers automatically on phrases like "build a website," "landing page," "scroll-stopping site," "award-winning website."
- Or explicitly: "Use Web Claw to plan and build [project]."

**Subagent spawning:**
- Use the Task tool: `spawn_subagent(agent_file=<path>, context=[memory.md, agent file, input artifacts])`
- Pass only the files listed in the agent's "Inputs you require" section. Do not pass conversation history.

**Memory management:**
- `memory.md` is written to disk. Claude Code persists file writes across sessions.
- Context compaction: Claude Code compacts automatically. Before each compaction, write the Compaction Snapshot into `memory.md` (see `references/memory-format.md`). After compaction, the agent resumes from `memory.md`.

**Cost management ($25/month plan):**
- Use Manual Mode (see `references/agent-handoff-protocol.md`).
- Load only the agent file for the current phase — do not load all references at once.
- Write `memory.md` after every artifact to save progress.

---

## Codex (OpenAI)

OpenAI Codex — both the open-source CLI and the ChatGPT cloud environment — does not auto-discover skills via `agents/openai.yaml`. Its actual repo-instruction convention is **`AGENTS.md`**. Use one of these invocation paths instead:

**Option A — Point Codex at SKILL.md via `AGENTS.md`:**
- Drop an `AGENTS.md` at your project root that says: `When this project is opened, read web-claw/SKILL.md and follow the Web Claw pipeline. Begin by reading <project>/memory.md.`
- This is the most native path. Codex will load `AGENTS.md` automatically.

**Option B — Invoke explicitly per session:**
- `Read web-claw/SKILL.md and run Web Claw for this project.`
- Works on any Codex session regardless of `AGENTS.md` presence.

**Option C — Manual Mode (any Codex tier, any plan):**
- See the "Any Other Agent / Manual Mode" section below. Paste `memory.md` + the current agent file + the inputs that agent requires into a fresh chat. Quality depends on the model; in particular, Manual Mode cannot run the QA scripts (Lighthouse, axe-core, contrast, Playwright) — those checks must be run locally and pasted back. See the bottom of this doc for the full caveats.

**Spawning / delegation:**
- Codex does not have a documented public subagent primitive equivalent to Claude Code's Task tool. Treat delegation as serial: complete one agent's artifact, persist `memory.md`, then start the next. Manual Mode is the canonical pattern.
- Pass the minimal context defined in `references/agent-handoff-protocol.md`.

**Memory management:**
- `memory.md` is written to the project folder. Codex persists file writes across sessions.
- Codex handles context compaction internally. Trigger a manual Compaction Snapshot write (`scripts/compact-context.py`) before long operations or before ending a session.

**`agents/openai.yaml`:**
- This is a **metadata template, not an active integration**. Codex itself does not read this file.
- It is provided as a starting point if you wire Web Claw into a custom tool, command registry, or chip system that supports manifest files in this shape (display name, default prompt, brand color).
- If you do not have such tooling, leave the file alone or delete it — removing it does not break anything in Web Claw.

---

## Antigravity (Google DeepMind)

**Invoking the skill:**
- Antigravity reads skill files from the workspace. Reference the skill by path or trigger phrase.
- Explicit: "Read web-claw/SKILL.md and run it for [project]."

**Subagent spawning:**
- Antigravity supports `browser_subagent` and `run_command` tools. Use `run_command` for script execution.
- For agent handoffs, pass `memory.md` + agent file + input artifacts as file paths in the task.

**Memory management:**
- `memory.md` is written to the project folder. Antigravity persists file writes.
- Context compaction: Antigravity manages its own context. Write `memory.md` before ending any long session.

---

## Cursor

**Invoking the skill:**
- Drop a `.cursor/rules/web-claw.mdc` file pointing at the skill: `When this project is opened, read web-claw/SKILL.md and follow the Web Claw pipeline. Begin by reading <project>/memory.md.` The `alwaysApply: true` frontmatter makes it durable across chats.
- Or explicitly: "Read web-claw/SKILL.md and run Web Claw for this project."

**Subagent spawning:**
- Cursor does not expose a public subagent primitive equivalent to Claude Code's Task tool. Treat delegation as serial: complete one agent's artifact, persist `memory.md`, then start the next. Manual Mode is the canonical pattern.
- The Cursor "Background Agents" feature (where available) accepts a goal + repo and runs autonomously; pass the agent file + memory.md path in the goal.

**Memory management:**
- `memory.md` is on disk; Cursor persists file writes. Cursor maintains its own conversation context separately — write `memory.md` after every artifact.
- Cursor's "Indexer" picks up new files automatically; no manual sync needed.

---

## Windsurf (Codeium)

**Invoking the skill:**
- Windsurf reads `.windsurfrules` at the workspace root. Add: `When this project is opened, read web-claw/SKILL.md and follow the Web Claw pipeline. Begin by reading <project>/memory.md.`
- Or explicitly: "Read web-claw/SKILL.md and run it."

**Cascade Agent / multi-step execution:**
- Windsurf's Cascade can chain tool calls within a single agent turn. Use it for the within-state work (e.g., produce sitemap.md), then save and present for sign-off.
- For multi-agent delegation, use Manual Mode — start a fresh Cascade with only the next agent file + memory.md + required artifacts.

**Memory management:**
- Files are written and persisted normally.
- Windsurf's "Memory" feature is a separate ephemeral KV store; do not use it for project state. `memory.md` on disk is the source of truth.

---

## Continue (continue.dev)

**Invoking the skill:**
- Continue uses `.continue/config.json` and per-project context providers. Add a system message via the config: `Read web-claw/SKILL.md before any web-design task. Begin by reading memory.md.`
- Or invoke explicitly per chat: `@web-claw/SKILL.md` then describe the project.

**Subagent spawning:**
- Continue does not expose subagent spawning. Use Manual Mode: each agent file is a separate chat session, with `memory.md` and inputs pasted in.

**Memory management:**
- `memory.md` is on disk; Continue persists file writes.
- Continue supports `@codebase` and `@file` context providers — use `@file:./memory.md` at the start of each session.

---

## Aider

**Invoking the skill:**
- Aider has a `--read` flag for read-only context files. Run: `aider --read web-claw/SKILL.md --read <project>/memory.md --message "Run Web Claw for this project."`
- Or use `.aider.conf.yml` with `read:` entries to make this durable.

**Subagent spawning:**
- Aider is a single-agent system. No subagent primitive. Run Manual Mode: complete one agent's artifact, exit, re-enter with the next agent file in `--read`.

**Memory management:**
- Aider does not maintain conversation memory across sessions. `memory.md` is critical here — it IS the memory.
- Aider commits per change by default; the `decisions/` files and `memory.md` updates land naturally in git history.

---

## Other Agent / Manual Mode

**The skill works on almost any model that can read prose and produce structured output.** If your platform doesn't support subagent spawning or automatic skill loading:

1. Open a new chat.
2. Paste: "I'm working on a Web Claw project. Here's the current state:" + contents of `memory.md`.
3. Paste the relevant agent file for the current phase.
4. Paste the input artifact files (or their paths if the model can read files).
5. Give the task: "Produce [artifact]. Present it. Stop."
6. Copy output back into project folder. Ask agent for updated `memory.md` fields. Apply manually.

**Manual Mode trades parallelism and tool-driven QA automation for portability.** It is **not** equivalent to a tool-using agent run:

- The agent cannot run `scripts/audit-perf.py` (Lighthouse), `scripts/check-a11y.py` (pa11y), or any of the `scripts/check-*.py` validators. You must run those locally and paste results back.
- The agent cannot browse Awwwards, YouTube, or the wider research sources at runtime — research entries must be assembled by hand or pasted from your own browsing.
- The agent cannot deploy to Vercel or call `git`. You drive those steps; the agent only produces the artifacts.
- Output **quality is model-dependent**. Expect meaningful variance: a frontier model with strong instruction-following will produce most of what a tool-using Claude Code run produces; a smaller or older model will skip nuance, miss accessibility detail, and lean on generic copy.

Use Manual Mode when portability matters more than throughput. Use a tool-using agent (Claude Code, Antigravity, Cursor with the Run-Anything tool, etc.) when you want the QA gates to actually execute.

---

## Cross-Platform `memory.md` Compatibility

`memory.md` uses plain Markdown with structured fields. It is readable and writable by any model. There are no platform-specific fields. A project started on Claude Code can be resumed on Codex or manually — the state machine state and all decisions are preserved in the filesystem, not in model memory.

---

## Script Compatibility

| Script | Python version | Windows | macOS/Linux |
|--------|---------------|---------|-------------|
| `init-project.py` | 3.8+ | ✅ | ✅ |
| `update-memory.py` | 3.8+ | ✅ | ✅ |
| `compact-context.py` | 3.8+ | ✅ | ✅ |
| `scrape-awwwards.py` | 3.8+ | ✅ | ✅ |
| `audit-perf.py` | 3.8+ | ✅ | ✅ |
| `check-a11y.py` | 3.8+ | requires WSL or Node | ✅ |
| `install-deps.py` | 3.8+ | ✅ | ✅ |
| `bootstrap.ps1` | PowerShell 5+ | ✅ | requires pwsh |

Run all scripts from the `web-claw/` directory or pass absolute paths for project arguments.

# Web Claw

**A structured methodology for designing and shipping scroll-stopping, award-caliber websites — through any AI coding agent.**

Web Claw is a skill package that turns *"I want an Awwwards-quality landing page"* into a fully designed, animated, QA'd, deployment-ready website. It works on any AI coding host that can read prose, run shell commands, and write files.

It is opinionated. It has taste. It will push back on generic briefs.

---

## What it gives you

A 14-state pipeline from intake to launch:

```
IGNITION -> BLUEPRINT (sitemap -> style guide -> wireframes -> motion spec)
         -> RESEARCH (Awwwards + vetted YouTube)
         -> EXECUTION (stack -> plan -> 3 shippable phases)
         -> QA (phase gates + pre-launch) -> DONE
```

Every state has an entry condition, a sign-off gate (skippable in fast mode; automated QA gates remain hard), a rejection path, and a specific output file.

Plus:
- **7 specialist agents** (UX strategy, UI strategy, design, motion, research, implementation, QA).
- **Filesystem-backed state** — `memory.md` + `decisions/` survives session resets, model swaps, and platform changes.
- **Canonical budgets** — every numeric threshold (Lighthouse, CWV, accessibility, motion, bundle) lives in [`references/budgets.yaml`](references/budgets.yaml). One source of truth.
- **Automated QA scripts** — Lighthouse, axe-core, contrast, bundle size, reduced-motion, Playwright E2E, visual regression, OG-image generation.
- **Two run modes** — `interactive` (sign off each artifact) or `fast` (auto-approve, automated gates still hard).
- **Handoff exporter** — one-command tarball / JSON / markdown bundle for transfer to another agent.

---

## Install

### Step 1 — Clone the repo

```bash
git clone https://github.com/yusufabdul024/web-claw.git
cd web-claw
```

Pin to a tagged release if you want a stable version: `git clone --branch v1.0.0 https://github.com/yusufabdul024/web-claw.git`.

### Step 2 — Run the installer for your host

The installer copies Web Claw's files into the host-native skill directory of your target project and runs `verify-install.py` to confirm the result. No `curl | bash`; the convenience one-liners (still available, see "Convenience paths" below) are deprioritised because piping remote shell scripts is unsafe by default.

**macOS / Linux / WSL:**

```bash
./install.sh --host <host> --project /path/to/your/project
```

**Windows (PowerShell):**

```powershell
.\install.ps1 -HostName <host> -Project C:\path\to\your\project
```

Replace `<host>` with one of: `codex`, `claude`, `cursor`, `gemini`, `opencode`, or `all`.

### Step 3 — Open your project in your agent and run Web Claw

After install completes, the installer prints the exact prompt to give your agent. See **Use after install** below.

---

## Host-native install destinations

The installer resolves the correct directory automatically. Reference:

| Host          | Project-local destination                | User/global destination                  |
|---------------|------------------------------------------|------------------------------------------|
| Codex         | `<project>/.agents/skills/web-claw/`     | — (use project-local)                    |
| Claude Code   | `<project>/.claude/skills/web-claw/`     | `~/.claude/skills/web-claw/` (use `--user`) |
| Cursor        | `<project>/.cursor/skills/web-claw/` *(plus a `.cursor/rules/web-claw.mdc` pointer is created automatically)* | — |
| Gemini CLI    | `<project>/.gemini/extensions/web-claw/` | — |
| OpenCode      | `<project>/.opencode/skills/web-claw/`   | — |
| Anything else | Manual fallback: copy the repo root to any folder named `web-claw/` in your project and tell the agent to read `web-claw/SKILL.md`. | — |

### Installer flags

| Flag                                | Effect                                                                          |
|-------------------------------------|---------------------------------------------------------------------------------|
| `--host <host>` / `-HostName <host>` | Required. One of: `codex`, `claude`, `cursor`, `gemini`, `opencode`, `all`.    |
| `--project <path>` / `-Project <path>` | Path to the target project. Defaults to the current directory.               |
| `--user` / `-User`                  | Install into the user/global directory where supported (currently `claude` only). |
| `--force` / `-Force`                | Overwrite an existing `web-claw/` skill directory at the destination.           |
| `--dry-run` / `-DryRun`             | Print what would happen without copying anything.                               |

### What the installer copies

`SKILL.md`, `README.md`, `LICENSE`, `skill.json`, `agents/`, `assets/`, `qa/`, `references/`, `scripts/`, `.github/`, `install.sh`, `install.ps1`.

It **never** copies `.git/`, `__pycache__/`, `*.pyc`, `node_modules/`, `.pytest_cache/`, `.DS_Store`, `Thumbs.db`, `webclaw-lighthouse-*/`, `*.lighthouse.json`, or `.web-claw-cache/`.

---

## Install verification

The installer runs `scripts/verify-install.py` after copying. You can also run it standalone at any time:

```bash
python web-claw/scripts/verify-install.py --skill-root <destination>
```

The verifier checks:
- `SKILL.md` exists and has valid `name`/`description` frontmatter.
- All required folders exist (`agents/`, `references/`, `scripts/`, `qa/`, `assets/`).
- Every Python script compiles (in-memory; no bytecode written).
- `references/budgets.yaml` parses through the stdlib loader.
- `scripts/init-project.py --help` works.
- Every relative path referenced by `SKILL.md` exists in the skill (excluding runtime-generated files).
- No `__pycache__` or `*.pyc` artifacts are committed.

Exit codes: `0` (all pass), `1` (one or more checks failed), `2` (invalid invocation).

---

## Install by agent

Want your agent to install Web Claw for you? Copy this prompt into a fresh agent session in your target project:

```
Install Web Claw from https://github.com/yusufabdul024/web-claw as a
host-native skill for my current agent. Detect whether I'm using Codex,
Claude Code, Cursor, Gemini, or another supported host by inspecting which
of these directories exist or are referenced: .agents/, .claude/, .cursor/,
.gemini/, .opencode/. Clone the repo, run install.sh (or install.ps1 on
Windows) with the right --host flag pointing at the current project, then
run scripts/verify-install.py on the destination. If the host requires a
project instruction file (AGENTS.md for Codex, .cursor/rules/*.mdc for
Cursor), create the minimal one that says: "Read web-claw/SKILL.md and
follow the Web Claw pipeline for any web design task." Confirm the
install succeeded by printing the verifier output.
```

---

## Use after install

In your AI coding agent (working in the project where you installed Web Claw), type any of:

```
Run Web Claw to plan and build a landing page for <project>.
```

```
Use Web Claw fast mode for an end-to-end website build.
Goal: <one-sentence outcome>. Audience: <visitor>. Stack: <preference>.
```

```
Resume this Web Claw project by reading memory.md first.
```

The skill will:
1. Read `SKILL.md`.
2. Run `scripts/init-project.py` to create `memory.md`, `decisions/`, `blueprint/`, `research/`, `qa/`, and seed files.
3. Ask 7 quick discovery questions (or 17 for complex projects). In fast mode it picks defaults and logs each judgment call to `decisions/NNN-auto-*.md`.
4. Produce sitemap → style guide → wireframes → motion spec, with a sign-off gate after each (interactive mode).
5. Research Awwwards + YouTube with a four-signal credibility heuristic.
6. Pick the tech stack with pinned versions.
7. Write `plan.md` plus `phase-1.md` / `phase-2.md` / `phase-3.md`.
8. Implement each phase, run QA gates (`scripts/audit-perf.py`, `check-a11y.py`, `check-contrast.py`, `check-bundle.py`, `check-reduced-motion.py`, `run-playwright.py`, `visual-regression.py`) and fix all blockers.
9. Deliver a production-ready preview URL.

---

## Convenience paths (use with care)

These exist for low-friction first-time installs. They are not the primary path because piping remote shell scripts into a shell is unsafe by default — prefer the explicit clone + installer flow above.

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/yusufabdul024/web-claw/main/install.sh \
  | bash -s -- --host claude --project "$(pwd)"
```

```powershell
# Windows
iwr -useb https://raw.githubusercontent.com/yusufabdul024/web-claw/main/install.ps1 `
  | iex -- -HostName claude -Project (Get-Location).Path
```

Forks override the source via `WEBCLAW_REPO_URL=<your-fork-url>` (Bash) or `$env:WEBCLAW_REPO_URL = "<your-fork-url>"` (PowerShell).

---

## Requirements

- **Python 3.8+** — required. Stdlib only; no `pip install` for the core skill.
- **Node.js 18+** — optional, only for the QA scripts that wrap `npx lighthouse`, `npx pa11y`, and `npx playwright`.
- Any AI coding agent that can read files and run shell commands.

The Python scripts include a Unicode-safe stdout shim, so they run cleanly on Windows cp1252 terminals as well as UTF-8 macOS/Linux shells.

---

## What's in the box

```
web-claw/
|-- SKILL.md                              Entry point. Trigger conditions, pipeline overview.
|-- skill.json                            Portable manifest (host destinations, version, requirements).
|-- agents/                               7 specialist agent role briefs.
|-- references/                           Load-on-demand reference index. budgets.yaml is canonical.
|   |-- budgets.yaml                      All numeric thresholds.
|   |-- state-machine.md                  All 14 states, entry/exit/rejection paths.
|   |-- memory-format.md                  memory.md schema, compaction protocol.
|   |-- operating-principles.md           12 governing principles.
|   |-- platform-compat.md                Per-host invocation notes.
|   |-- extension-orchestration.md        Optional sibling-skill routing.
|   |-- pattern-library.md, color-theory.md, typography-systems.md,
|   |-- animation-libraries.md, performance-budgets.md, accessibility.md,
|   |-- relume-methodology.md, youtube-channels.md, tech-stack.md,
|   |-- design-systems.md, agent-handoff-protocol.md, handoff-export.md,
|   |-- ignition-quick.md, ignition-full.md
|-- qa/                                   Phase gates + per-domain checklists + visual-critique rubric.
|-- scripts/                              Python utilities (stdlib only for core).
|   |-- init-project.py, update-memory.py, compact-context.py
|   |-- generate-phases.py, check-output.py, verify-install.py
|   |-- audit-perf.py, check-a11y.py, check-contrast.py, check-bundle.py
|   |-- check-reduced-motion.py, run-playwright.py, visual-regression.py
|   |-- generate-og.py, export-handoff.py
|   |-- _budgets.py, _console.py, research-matrix.py, extract-tokens.py
|   |-- scrape-awwwards.py, install-deps.py, install-packages.py
|-- assets/
|   |-- templates/                        Markdown templates for every artifact.
|   `-- svg/                              Static SVG assets.
|-- .github/workflows/                    Optional CI templates (Lighthouse, Playwright, Build).
|-- install.sh                            POSIX installer.
|-- install.ps1                           PowerShell installer.
|-- LICENSE
`-- README.md                             You are here.
```

---

## Modes

### Interactive mode (default)

```
You: Run Web Claw to build a portfolio site for "Studio Atrium".
Agent: [asks 7-17 discovery questions, one section at a time]
Agent: [produces sitemap, presents it, asks "If you had to cut one page, which?"]
You:   "Cut the blog."
Agent: [removes blog, re-presents]
... and so on through 14 states.
```

### Fast mode

```
You: Build a SaaS marketing site for "Meridian" end-to-end. Fast mode.
     Goal: convert to demo bookings. Audience: B2B engineering leaders.
     Stack: Next.js + Tailwind + Motion. Vercel. Active motion intensity.
Agent: [runs all 14 states without sign-off pauses; logs every judgment to
        decisions/NNN-auto-*.md; runs Lighthouse + axe-core + bundle +
        contrast + reduced-motion + Playwright at each gate; surfaces a
        single completion review at the end]
```

Quality gates are never skipped in fast mode. Lighthouse below the floor still blocks. axe-core violations still block. Reduced-motion fallbacks are still verified. Fast mode short-circuits only human sign-off.

---

## Handoff

A completed project can be exported as a single self-contained tarball / JSON / markdown bundle that another agent can pick up cold:

```bash
python web-claw/scripts/export-handoff.py --workspace <project> --shape tarball
```

See [`references/handoff-export.md`](references/handoff-export.md). The export contains the full pipeline state, every decision, every QA report, and a copy of the Web Claw skill — so the receiver does not need to install anything.

---

## Release checklist

Before tagging a new Web Claw release:

- [ ] Run `python scripts/verify-install.py` at the repo root — all 7 checks pass.
- [ ] Run `bash -n install.sh` and the equivalent PowerShell `Tokenize` check on `install.ps1` — both parse clean.
- [ ] No `__pycache__/` directories, no `*.pyc` files, no `.DS_Store` / `Thumbs.db` artifacts in the tree.
- [ ] `.gitignore` covers `__pycache__/`, `*.pyc`, `node_modules/`, `webclaw-lighthouse-*/`, `*.lighthouse.json`, `.web-claw-cache/`, project-bleed paths (`/memory.md`, `/blueprint/`, etc.).
- [ ] `skill.json` `version` bumped.
- [ ] No machine-local paths committed (search for `C:\Users`, `/Users/`, `/home/` in non-doc files).
- [ ] `git tag v<version>` and `git push --tags`.
- [ ] Smoke test: in a clean temp project, run `install.sh --host claude --project <temp>` and confirm the verifier exits 0.

---

## Philosophy

Read [`references/operating-principles.md`](references/operating-principles.md) for the 12 governing principles. The short version:

- **One page, one job.** Pages without measurable outcomes don't exist.
- **One signature device per page.** Five "signature" moments per page is zero signature moments.
- **Numbers, not vibes.** Contrast ratios, Lighthouse scores, frame counts. Not "feels fast."
- **Mobile is the design.** Desktop is the additive case.
- **Reduced motion is design.** Don't strip animations — replace them.
- **Copy is design.** No lorem ipsum, ever.
- **The filesystem remembers.** Project state lives in `memory.md` and `decisions/`. The context window is working surface.

---

## License

MIT. See [LICENSE](LICENSE).

---

## Contributing

Web Claw is curated. Pull requests welcome:

- Add patterns to `references/pattern-library.md` — keep them at one of the four layers and provide a concrete implementation note.
- Submit YouTube channels for the seed list with credibility-signal evidence.
- Update `references/tech-stack.md` when a major library version moves.
- Add a host to `references/platform-compat.md` and to the installer's destination map when you adopt a new agent.

Open an issue first for structural changes (new states, new agents, new scripts).

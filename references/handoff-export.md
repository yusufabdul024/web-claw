# Handoff Export Contract

How to package an entire Web Claw project as a **single self-contained artifact** that another agent — on another platform, in a fresh repo, with no prior context — can pick up and ship.

This is the canonical export format. Build it when:

- Handing off to a separate implementation team or freelancer.
- Switching the project from one AI tool (Claude Code) to another (Codex, Cursor, Aider).
- Archiving a completed project so it can be revived later.
- Submitting a Web Claw pass as a deliverable to the user.

---

## What "complete handoff" means

A receiver opening the export should be able to:

1. **Read the brief in under five minutes.** (Discovery, sitemap, style guide summary, motion-spec summary, signature moment.)
2. **Resume the pipeline at the exact state it was paused.** (memory.md + decisions + last artifact.)
3. **Build the next phase without re-asking any answered question.**
4. **Verify the QA budgets and pass criteria.**
5. **Re-run every script** referenced in the plan (audit-perf, check-a11y, install-packages, etc.) without additional setup beyond Node.js + Python.

If any of these is impossible, the export is incomplete.

---

## Export shapes

Web Claw supports three export shapes. Pick by receiver:

### A. Single tarball (`<project>-handoff.tar.gz`)
The default. One file. Trivially attachable, mirrors the live folder layout. Use for any non-trivial receiver.

### B. Single JSON (`<project>-handoff.json`)
The whole project serialized as `{ "path": "...", "content": "..." }` records inside one JSON. Use when the receiver is *another agent*, especially one that can't open a tarball but can parse JSON.

### C. Single markdown bundle (`<project>-handoff.md`)
One mega-markdown file with every artifact as a labeled `<section>` block. Use for chat-window pastes when even file uploads are unavailable.

All three shapes contain the same content. The handoff manifest below names every required path. The tarball and JSON shapes preserve the manifest as-is; the markdown shape encodes each file as a fenced block.

---

## Required manifest

The export MUST contain every path in this manifest, OR explicitly mark it `N/A` with a reason.

### Tier 1 — Pipeline state (always required)

```
memory.md
decisions/                 (every NNN-*.md file)
site-brief.json
sources.json
dependencies.json
qa/qa-plan.md
```

### Tier 2 — Blueprint (required if Phase 1 was started)

```
blueprint/discovery.md
blueprint/sitemap.md
blueprint/style-guide.md
blueprint/wireframes.md
blueprint/animations.md
```

### Tier 3 — Research (required if Phase 2 was started)

```
research/awwwards-references.md
research/youtube-techniques.md
research/tech-stack.md
```

### Tier 4 — Execution (required if Phase 2 produced a plan)

```
plan.md
phase-1.md
phase-2.md
phase-3.md
prompts/sequential-prompts.md
```

### Tier 5 — QA evidence (required for any phase that hit a gate)

```
qa/phase-1-report.md
qa/phase-2-report.md
qa/phase-3-report.md
qa/final-report.md          (if QA:FINAL passed)
```

### Tier 6 — Skill copy (always required for a true cold-start)

```
web-claw/SKILL.md
web-claw/agents/*.md
web-claw/references/*.md
web-claw/qa/*.md
web-claw/scripts/*.py
web-claw/scripts/_console.py
web-claw/scripts/bootstrap.ps1
web-claw/assets/templates/*.md
```

The Tier 6 inclusion makes the export **runnable by an agent that has never seen Web Claw**. Without it, the receiver has to find and install the skill separately, which defeats the purpose.

---

## Handoff manifest format

Every export carries a top-level `handoff-manifest.json` that names every included file and the state at the time of export:

```json
{
  "web_claw_version": "1.0.0",
  "exported_at": "2026-05-15T14:32:00Z",
  "project": {
    "name": "Meridian",
    "slug": "meridian-site",
    "current_phase": "EXECUTION:PHASE-2",
    "user_signoff": "YES",
    "next_action": "Run scripts/audit-perf.py against the phase-2 preview URL.",
    "motion_intensity": "active",
    "stack": "Next.js 15 + Tailwind 4 + GSAP 3.13 + Lenis 1.1",
    "deploy_target": "Vercel"
  },
  "deliverables": [
    { "path": "memory.md", "tier": 1, "status": "present", "size_bytes": 1842 },
    { "path": "blueprint/discovery.md", "tier": 2, "status": "present", "size_bytes": 4123 },
    { "path": "blueprint/sitemap.md", "tier": 2, "status": "present", "size_bytes": 2980 },
    { "path": "research/youtube-techniques.md", "tier": 3, "status": "n/a", "reason": "Phase 2 research deferred to receiver" }
  ],
  "decisions": [
    { "id": "DECISION-001", "topic": "motion intensity", "path": "decisions/001-motion-intensity.md" },
    { "id": "DECISION-002", "topic": "stack", "path": "decisions/002-stack.md" }
  ],
  "qa_evidence": {
    "phase_1": { "passed": true, "report": "qa/phase-1-report.md" },
    "phase_2": { "passed": false, "report": "qa/phase-2-report.md", "blockers": ["LCP 3.4s on mobile (budget 2.5s)"] },
    "phase_3": { "passed": null, "report": null }
  },
  "receiver_instructions": "Open this folder in any AI coding agent. Read web-claw/SKILL.md, then memory.md, then resume from `next_action`. The four-signal YouTube credibility heuristic and the recency-weighted research method live in web-claw/references/."
}
```

`status` values: `present` | `missing` | `n/a` | `partial`.

A receiver tooling can parse `handoff-manifest.json` to verify integrity before doing anything else.

---

## How to produce an export

### Manual

1. Verify the project passes `scripts/check-output.py --workspace <project> --phase all` (or the highest phase reached).
2. Copy the live `<project>/` folder.
3. Copy the `web-claw/` skill folder into the project copy as `<project>/web-claw/`.
4. Write `handoff-manifest.json` at the root.
5. Tar + gzip: `tar -czf <project>-handoff.tar.gz <project>/`.

### Scripted (recommended)

`scripts/export-handoff.py` produces all three shapes from a single invocation:

```
python scripts/export-handoff.py --workspace <project> --shape tarball
python scripts/export-handoff.py --workspace <project> --shape json
python scripts/export-handoff.py --workspace <project> --shape markdown
python scripts/export-handoff.py --workspace <project> --shape tarball --include-snapshots
```

The script bundles `<project>/` plus the entire `web-claw/` skill folder, writes a `handoff-manifest.json` at the bundle root, and skips `__pycache__/`, `.git/`, `node_modules/`. Use `--include-snapshots` to bundle `qa/snapshots/` (often large).

The manual recipe above is still valid if you need to construct the bundle by hand or customise it.

---

## How a receiver opens the export

### Receiver is a human

1. Unpack the tarball.
2. Open `handoff-manifest.json` — read `project.next_action` and `qa_evidence`.
3. Open `memory.md` — confirm Phase, Last artifact, Next action.
4. Open `web-claw/SKILL.md` if the receiver has never used Web Claw.

### Receiver is an AI agent

1. Read `handoff-manifest.json`.
2. Read `web-claw/SKILL.md`.
3. Read `memory.md` — get current state.
4. Read any file listed in `memory.md` under "Pinned Decisions".
5. Execute `next_action`.

The minimum prompt for any agent to resume cold:

```
Read web-claw/SKILL.md.
Read memory.md.
Read every file listed in Pinned Decisions.
Continue Web Claw from the recorded state. Do not re-ask questions answered in memory.md or discovery.md.
```

---

## What this contract guarantees

A correctly produced export:

- Is self-contained: no external skill installation required to run.
- Is platform-agnostic: works on Claude Code, Codex, Cursor, Windsurf, Continue, Aider, Antigravity, or Manual Mode.
- Is resumable: state machine state is recovered exactly.
- Is auditable: every decision, every QA pass/fail, every dependency choice, every cut page is documented.
- Is shippable: the receiver can deliver to production without making strategic choices they don't have context for.

If any of those is untrue, the export was incomplete — go back to the manifest.

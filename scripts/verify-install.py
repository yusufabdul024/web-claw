#!/usr/bin/env python3
"""
verify-install.py

Confirms a Web Claw installation is complete and runnable. The installers
(install.sh, install.ps1) call this after copying files. It is also safe to
run standalone:

    python scripts/verify-install.py                       # verify current dir
    python scripts/verify-install.py --skill-root <path>   # verify a copy

Exit codes:
    0  all checks pass
    1  one or more checks failed (details printed)
    2  invalid invocation / skill root not a directory
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
]

REQUIRED_DIRS = [
    "agents",
    "assets",
    "qa",
    "references",
    "scripts",
]

REQUIRED_AGENT_FILES = [
    "agents/ux-strategy-agent.md",
    "agents/designer-agent.md",
    "agents/ui-strategy-agent.md",
    "agents/animator-agent.md",
    "agents/researcher-agent.md",
    "agents/implementer-agent.md",
    "agents/qa-agent.md",
]

REQUIRED_REFERENCE_FILES = [
    "references/memory-format.md",
    "references/operating-principles.md",
    "references/state-machine.md",
    "references/agent-handoff-protocol.md",
    "references/extension-orchestration.md",
    "references/platform-compat.md",
    "references/budgets.yaml",
]

REQUIRED_QA_FILES = [
    "qa/phase-1-gate.md",
    "qa/phase-2-gate.md",
    "qa/phase-3-gate.md",
    "qa/pre-launch-checklist.md",
    "qa/visual-critique-rubric.md",
]


class Check:
    def __init__(self, name: str) -> None:
        self.name = name
        self.errors: list[str] = []
        self.passed = True

    def fail(self, msg: str) -> None:
        self.errors.append(msg)
        self.passed = False

    def __str__(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        out = f"  [{status}] {self.name}"
        for e in self.errors:
            out += f"\n         - {e}"
        return out


def check_required_paths(root: Path) -> Check:
    c = Check("required files + directories")
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            c.fail(f"missing file: {rel}")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            c.fail(f"missing directory: {rel}")
    for rel in REQUIRED_AGENT_FILES + REQUIRED_REFERENCE_FILES + REQUIRED_QA_FILES:
        if not (root / rel).is_file():
            c.fail(f"missing file: {rel}")
    return c


def check_skill_frontmatter(root: Path) -> Check:
    c = Check("SKILL.md frontmatter")
    p = root / "SKILL.md"
    if not p.is_file():
        c.fail("SKILL.md not found")
        return c
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---"):
        c.fail("missing YAML frontmatter (must start with `---`)")
        return c
    end = text.find("\n---", 3)
    if end < 0:
        c.fail("frontmatter not closed (must end with `---` on its own line)")
        return c
    block = text[3:end]
    if not re.search(r"^name\s*:\s*\S+", block, re.MULTILINE):
        c.fail("frontmatter missing `name:`")
    if not re.search(r"^description\s*:\s*\S+", block, re.MULTILINE):
        c.fail("frontmatter missing `description:`")
    return c


def check_python_compiles(root: Path) -> Check:
    c = Check("Python scripts compile")
    scripts_dir = root / "scripts"
    if not scripts_dir.is_dir():
        c.fail("scripts/ directory missing")
        return c
    # Use the in-memory `compile()` builtin so we never write __pycache__
    # bytecode while validating. py_compile.compile() persists .pyc by design.
    for p in sorted(scripts_dir.glob("*.py")):
        try:
            compile(p.read_text(encoding="utf-8"), str(p), "exec")
        except (SyntaxError, ValueError) as e:
            c.fail(f"{p.name}: {e}")
        except OSError as e:
            c.fail(f"{p.name}: could not read ({e})")
    return c


def check_budgets_parses(root: Path) -> Check:
    c = Check("references/budgets.yaml parses")
    # Use the bundled _budgets.py loader so we exercise the same code path the
    # rest of the skill uses.
    budgets_loader = root / "scripts" / "_budgets.py"
    if not budgets_loader.is_file():
        c.fail("scripts/_budgets.py missing (cannot validate budgets.yaml)")
        return c
    try:
        env = os.environ.copy()
        env["WEBCLAW_BUDGETS_PATH"] = str(root / "references" / "budgets.yaml")
        result = subprocess.run(
            [sys.executable, "-B", str(budgets_loader)],
            capture_output=True, text=True, env=env, timeout=15,
        )
        if result.returncode != 0:
            c.fail(f"_budgets.py exited {result.returncode}: {result.stderr.strip().splitlines()[-1] if result.stderr else ''}")
            return c
        data = json.loads(result.stdout)
        required_top = ["schema", "lighthouse", "core_web_vitals", "accessibility", "motion", "research"]
        for key in required_top:
            if key not in data:
                c.fail(f"budgets.yaml missing top-level key: {key}")
    except subprocess.TimeoutExpired:
        c.fail("_budgets.py timed out after 15s")
    except json.JSONDecodeError as e:
        c.fail(f"_budgets.py output is not valid JSON: {e}")
    except Exception as e:
        c.fail(f"unexpected error loading budgets: {e}")
    return c


def check_init_project_help(root: Path) -> Check:
    c = Check("scripts/init-project.py --help works")
    init = root / "scripts" / "init-project.py"
    if not init.is_file():
        c.fail("scripts/init-project.py missing")
        return c
    try:
        result = subprocess.run(
            [sys.executable, "-B", str(init), "--help"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            c.fail(f"--help exited {result.returncode}: {result.stderr.strip().splitlines()[-1] if result.stderr else ''}")
        elif "--path" not in result.stdout and "usage" not in result.stdout.lower():
            c.fail("--help output doesn't look like an argparse usage block")
    except subprocess.TimeoutExpired:
        c.fail("--help timed out after 15s")
    except Exception as e:
        c.fail(f"unexpected error: {e}")
    return c


# Internal-reference patterns we extract from SKILL.md to check.
# Backtick-wrapped relative paths ending in a known extension.
_REF_RE = re.compile(r"`([a-zA-Z][\w./-]+\.(?:md|py|yaml|yml|json|sh|ps1))`")

# Placeholders that intentionally do not exist in the skill (they're produced
# at runtime inside a user's project).
_PLACEHOLDER_NEEDLES = ("<", "NNN", "phase-N", "<project>")

# Files Web Claw generates inside the user's project workspace (not inside the
# skill folder). These will be referenced by SKILL.md without existing here.
_RUNTIME_GENERATED = {
    "memory.md",       # produced at IGNITION inside <project>/
    "discovery.md",    # produced inside <project>/blueprint/
    "plan.md",         # produced after EXECUTION:PLAN
    "phase-1.md",      # generated by scripts/generate-phases.py
    "phase-2.md",
    "phase-3.md",
    "site-brief.json", # produced by init-project.py
    "sources.json",
    "dependencies.json",
}


def check_internal_references(root: Path) -> Check:
    c = Check("internal references in SKILL.md")
    p = root / "SKILL.md"
    if not p.is_file():
        c.fail("SKILL.md not found")
        return c
    text = p.read_text(encoding="utf-8")
    paths = set(_REF_RE.findall(text))
    for rel in sorted(paths):
        if any(needle in rel for needle in _PLACEHOLDER_NEEDLES):
            continue
        if rel in _RUNTIME_GENERATED:
            continue
        # Some references like `decisions/` (no extension) won't match this
        # regex anyway. Others like `phase-N.md` are placeholders skipped above.
        if not (root / rel).exists():
            c.fail(f"referenced path does not exist: {rel}")
    return c


def check_no_pycache(root: Path) -> Check:
    c = Check("no __pycache__ / .pyc committed")
    bad: list[str] = []
    for p in root.rglob("__pycache__"):
        bad.append(str(p.relative_to(root)))
    for p in root.rglob("*.pyc"):
        bad.append(str(p.relative_to(root)))
    if bad:
        for b in bad[:5]:
            c.fail(f"found: {b}")
        if len(bad) > 5:
            c.fail(f"... and {len(bad) - 5} more")
    return c


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill-root", default=None,
                        help="Path to the installed Web Claw skill root (default: parent of this script's dir).")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Emit a machine-readable JSON summary.")
    args = parser.parse_args(argv[1:])

    if args.skill_root:
        root = Path(args.skill_root).expanduser().resolve()
    else:
        # When this script is at <skill-root>/scripts/verify-install.py,
        # the skill root is the parent of the scripts/ folder.
        root = Path(__file__).resolve().parent.parent
    if not root.is_dir():
        print(f"error: skill root not a directory: {root}", file=sys.stderr)
        return 2

    checks: list[Check] = [
        check_required_paths(root),
        check_skill_frontmatter(root),
        check_python_compiles(root),
        check_budgets_parses(root),
        check_init_project_help(root),
        check_internal_references(root),
        check_no_pycache(root),
    ]

    failed = [c for c in checks if not c.passed]
    summary = {
        "skill_root": str(root),
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "checks": [
            {"name": c.name, "passed": c.passed, "errors": c.errors}
            for c in checks
        ],
    }

    if args.json_output:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Verifying Web Claw install at: {root}")
        print()
        for c in checks:
            print(c)
        print()
        if failed:
            print(f"[FAIL] {len(failed)} of {len(checks)} checks failed.")
        else:
            print(f"[OK]   {len(checks)} of {len(checks)} checks passed. Skill ready.")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""
Web Claw Explicit Dependency Installer

Installs frontend packages via the project's detected package manager.
Auto-detects npm / pnpm / yarn / bun from the project root lock files.

This complements install-deps.py (which reads commands from tech-stack.md).
Use this when you need to install specific packages by name directly.

Usage:
    python install-packages.py --workspace <frontend-root> --packages gsap lenis
    python install-packages.py --workspace ./my-site --packages gsap@3.12.5 lenis@1.1.14
    python install-packages.py --workspace ./my-site --dev-packages @types/node tsx
    python install-packages.py --workspace ./my-site --packages gsap --package-manager pnpm
    python install-packages.py --workspace ./my-site --packages gsap --dry-run
"""

from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _console import safe_stdout
safe_stdout()

import argparse
import re
import shutil
import subprocess
from pathlib import Path


PACKAGE_RE = re.compile(
    r"^(?:[a-z0-9][a-z0-9._~-]*|@[a-z0-9][a-z0-9._~-]*/[a-z0-9][a-z0-9._~-]*)(?:@[a-z0-9.*~^<>=|:-]+)?$"
)


def detect_package_manager(workspace: Path) -> str:
    if (workspace / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (workspace / "yarn.lock").exists():
        return "yarn"
    if (workspace / "bun.lockb").exists() or (workspace / "bun.lock").exists():
        return "bun"
    if (workspace / "package-lock.json").exists():
        return "npm"
    return "npm"


def validate_packages(packages: list[str]) -> list[str]:
    return [pkg for pkg in packages if not PACKAGE_RE.match(pkg)]


def build_command(manager: str, packages: list[str], dev: bool) -> list[str]:
    if manager == "npm":
        return ["npm", "install", "--save-dev" if dev else "--save"] + packages
    if manager == "pnpm":
        cmd = ["pnpm", "add"]
        if dev:
            cmd.append("-D")
        return cmd + packages
    if manager == "yarn":
        cmd = ["yarn", "add"]
        if dev:
            cmd.append("-D")
        return cmd + packages
    if manager == "bun":
        cmd = ["bun", "add"]
        if dev:
            cmd.append("-d")
        return cmd + packages
    raise ValueError(f"Unsupported package manager: {manager}")


def clean(command: list[str]) -> list[str]:
    return [part for part in command if part]


def run(command: list[str], workspace: Path, dry_run: bool) -> int:
    command = clean(command)
    print(f"$ {' '.join(command)}")
    if dry_run:
        return 0
    exe = shutil.which(command[0])
    if not exe:
        print(f"ERROR: {command[0]} is not available on PATH.")
        return 1
    result = subprocess.run(command, cwd=workspace, check=False)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--workspace", default=".", help="Frontend project root (must contain package.json).")
    parser.add_argument("--package-manager",
                        choices=["auto", "npm", "pnpm", "yarn", "bun"],
                        default="auto",
                        help="Package manager to use (default: auto-detect from lock file).")
    parser.add_argument("--packages", nargs="*", default=[], help="Runtime packages to install.")
    parser.add_argument("--dev-packages", nargs="*", default=[], help="Dev packages to install.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them.")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()

    if not workspace.exists():
        print(f"ERROR: workspace not found: {workspace}")
        return 1
    if not (workspace / "package.json").exists():
        print(f"ERROR: no package.json in {workspace}")
        print("       Run your framework initializer first, then re-run this script.")
        return 1

    all_packages = (args.packages or []) + (args.dev_packages or [])
    if not all_packages:
        print("No packages specified. Use --packages and/or --dev-packages.")
        return 0

    invalid = validate_packages(all_packages)
    if invalid:
        print("ERROR: invalid package name(s):")
        for pkg in invalid:
            print(f"  - {pkg}")
        return 1

    manager = detect_package_manager(workspace) if args.package_manager == "auto" else args.package_manager
    print(f"Package manager: {manager}")
    print(f"Workspace      : {workspace}")
    if args.dry_run:
        print("Mode           : dry-run (commands will be printed but not executed)")
    print()

    if args.packages:
        code = run(build_command(manager, args.packages, dev=False), workspace, args.dry_run)
        if code != 0:
            return code

    if args.dev_packages:
        code = run(build_command(manager, args.dev_packages, dev=True), workspace, args.dry_run)
        if code != 0:
            return code

    if not args.dry_run:
        print("\n[OK] Packages installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

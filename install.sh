#!/usr/bin/env bash
# Web Claw installer for POSIX hosts (macOS, Linux, WSL).
#
# Copies this repo's skill files into the host-native skill directory for one
# or more AI coding agents and runs verify-install.py to confirm the result.
#
# Usage:
#   ./install.sh --host <host> [--project <path>] [--user] [--force] [--dry-run]
#
#   --host    codex | claude | cursor | gemini | opencode | all       (required)
#   --project Path to the target project (default: current directory)
#   --user    Install to the user/global skill directory where supported
#             (currently: claude only). Ignored otherwise with a warning.
#   --force   Overwrite an existing web-claw skill directory at the target.
#   --dry-run Print what would happen without copying anything.
#
# The script assumes you have already cloned or downloaded the Web Claw repo
# and are running install.sh from inside that repo root. See README for
# host-native install destinations.

set -euo pipefail

# ---- defaults -----------------------------------------------------------
HOST=""
PROJECT="$(pwd)"
USER_INSTALL=0
FORCE=0
DRY_RUN=0
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ---- printing helpers ---------------------------------------------------
say()  { printf '[web-claw] %s\n' "$*"; }
warn() { printf '[web-claw] WARN: %s\n' "$*" >&2; }
die()  { printf '[web-claw] ERROR: %s\n' "$*" >&2; exit 1; }

usage() {
    sed -n 's/^# \{0,1\}//;1,/^$/p' "$0" | grep -v '^!' | head -n 30
    exit "${1:-0}"
}

# ---- arg parsing --------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --host)    HOST="${2:-}"; shift 2 ;;
        --project) PROJECT="${2:-}"; shift 2 ;;
        --user)    USER_INSTALL=1; shift ;;
        --force)   FORCE=1; shift ;;
        --dry-run) DRY_RUN=1; shift ;;
        -h|--help) usage 0 ;;
        *) die "Unknown argument: $1 (try --help)" ;;
    esac
done

[[ -z "$HOST" ]] && die "--host is required. One of: codex, claude, cursor, gemini, opencode, all."

PROJECT="$(cd "$PROJECT" 2>/dev/null && pwd || true)"
[[ -z "$PROJECT" ]] && die "--project must be a path that exists."

# ---- preflight: source repo must look like the Web Claw skill ----------
[[ -f "$SCRIPT_DIR/SKILL.md" ]] || die "Run this from the Web Claw repo root (SKILL.md not found at $SCRIPT_DIR)."
[[ -d "$SCRIPT_DIR/agents" ]] || die "agents/ missing in source ($SCRIPT_DIR). Is this a complete Web Claw checkout?"

# ---- host-destination resolution ---------------------------------------
# For each supported host, return the canonical destination directory.
# Returns the path on stdout, or empty if --user is not supported for that host.
resolve_dest() {
    local host="$1"
    local mode="$2"   # "project" or "user"
    case "$host" in
        codex)
            [[ "$mode" == "user" ]] && return 1
            printf '%s\n' "$PROJECT/.agents/skills/web-claw"
            ;;
        claude)
            if [[ "$mode" == "user" ]]; then
                printf '%s\n' "$HOME/.claude/skills/web-claw"
            else
                printf '%s\n' "$PROJECT/.claude/skills/web-claw"
            fi
            ;;
        cursor)
            [[ "$mode" == "user" ]] && return 1
            printf '%s\n' "$PROJECT/.cursor/skills/web-claw"
            ;;
        gemini)
            [[ "$mode" == "user" ]] && return 1
            printf '%s\n' "$PROJECT/.gemini/extensions/web-claw"
            ;;
        opencode)
            [[ "$mode" == "user" ]] && return 1
            printf '%s\n' "$PROJECT/.opencode/skills/web-claw"
            ;;
        *)
            return 1
            ;;
    esac
}

# Items to copy from the repo root into the destination skill folder.
# Anything not listed here is intentionally excluded (e.g. .git, .gitignore,
# __pycache__, install scripts themselves are documented but not strictly
# required at the destination -- we include them so the user can re-run from
# the installed copy if they want).
COPY_ITEMS=(
    "SKILL.md"
    "README.md"
    "LICENSE"
    "skill.json"
    "agents"
    "assets"
    "qa"
    "references"
    "scripts"
    ".github"
    "install.sh"
    "install.ps1"
)

# Patterns to exclude during recursive copy.
EXCLUDES=(
    "__pycache__"
    "*.pyc"
    "*.pyo"
    ".pytest_cache"
    "node_modules"
    ".DS_Store"
    "Thumbs.db"
    "webclaw-lighthouse-*"
    "*.lighthouse.json"
    ".web-claw-cache"
)

# ---- copy implementation -----------------------------------------------
# Prefer rsync (clean exclude support); fall back to cp -r with a post-walk
# cleanup if rsync is missing.
have_rsync=0
if command -v rsync >/dev/null 2>&1; then
    have_rsync=1
fi

copy_one() {
    local src="$1"
    local dst="$2"
    if [[ ! -e "$src" ]]; then
        return 0  # silently skip missing optional items (e.g. skill.json before we create it)
    fi
    if (( DRY_RUN )); then
        printf '    would copy: %s -> %s\n' "${src#$SCRIPT_DIR/}" "${dst#$1/}"
        return 0
    fi
    if (( have_rsync )); then
        local excl_args=()
        for pat in "${EXCLUDES[@]}"; do
            excl_args+=(--exclude "$pat")
        done
        rsync -a "${excl_args[@]}" "$src" "$dst"
    else
        cp -R "$src" "$dst"
        # Strip excluded patterns post-copy.
        for pat in "${EXCLUDES[@]}"; do
            find "$dst" -name "$pat" -prune -exec rm -rf {} + 2>/dev/null || true
        done
    fi
}

install_one_host() {
    local host="$1"
    local mode
    if (( USER_INSTALL )); then mode="user"; else mode="project"; fi
    local dest
    if ! dest="$(resolve_dest "$host" "$mode")"; then
        if [[ "$mode" == "user" ]]; then
            warn "--user is not supported for host '$host'. Skipping."
            return 0
        fi
        die "Unknown host: $host"
    fi

    say "Host: $host"
    say "Destination: $dest"
    local dry_note=""
    (( DRY_RUN )) && dry_note=" (dry-run)"
    say "Mode: $mode$dry_note"

    if [[ -d "$dest" ]]; then
        if (( FORCE )); then
            (( DRY_RUN )) || rm -rf "$dest"
            say "Removed existing destination (--force)."
        else
            die "Destination exists: $dest. Re-run with --force to overwrite."
        fi
    fi

    if (( ! DRY_RUN )); then
        mkdir -p "$dest"
    fi

    say "Copying skill files..."
    for item in "${COPY_ITEMS[@]}"; do
        copy_one "$SCRIPT_DIR/$item" "$dest/"
    done

    # Cursor convenience: drop a minimal rule file pointing at the skill.
    if [[ "$host" == "cursor" && $DRY_RUN -eq 0 ]]; then
        local rule_dir="$PROJECT/.cursor/rules"
        mkdir -p "$rule_dir"
        cat > "$rule_dir/web-claw.mdc" <<EOF
---
description: Web Claw site-building skill
alwaysApply: true
---

Read .cursor/skills/web-claw/SKILL.md before any web-design task and follow the Web Claw pipeline. Begin every session by reading <project>/memory.md if it exists.
EOF
        say "Wrote $rule_dir/web-claw.mdc"
    fi

    # Codex convenience: ensure AGENTS.md points at the skill. Codex reads
    # AGENTS.md from the project root for activation. If the file already
    # exists we leave it alone (do not clobber the user's content) but tell
    # them what line to add. Otherwise we create it.
    if [[ "$host" == "codex" && $DRY_RUN -eq 0 ]]; then
        local agents_file="$PROJECT/AGENTS.md"
        local pointer_line="Read .agents/skills/web-claw/SKILL.md and follow the Web Claw pipeline for any web design task. Begin each session by reading memory.md if it exists."
        if [[ ! -f "$agents_file" ]]; then
            cat > "$agents_file" <<EOF
# Project Agent Instructions

$pointer_line
EOF
            say "Wrote $agents_file"
        else
            if grep -qF ".agents/skills/web-claw" "$agents_file"; then
                say "AGENTS.md already references web-claw; left unchanged."
            else
                warn "AGENTS.md exists at $agents_file but does not reference web-claw."
                warn "Add this line manually for Codex to activate the skill:"
                warn "  $pointer_line"
            fi
        fi
    fi

    if (( DRY_RUN )); then
        say "Dry run complete for $host -- nothing was written."
        return 0
    fi

    # ---- verify ---------------------------------------------------------
    # Try python3, python, then py (Windows Python launcher).
    PY=""
    for candidate in python3 python py; do
        if command -v "$candidate" >/dev/null 2>&1; then
            if "$candidate" -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)" 2>/dev/null; then
                PY="$candidate"
                break
            fi
        fi
    done
    if [[ -n "$PY" ]]; then
        say "Running install verifier..."
        if ! "$PY" -B "$dest/scripts/verify-install.py" --skill-root "$dest"; then
            die "verify-install.py failed. Inspect $dest and re-run with --force after fixing."
        fi
    else
        warn "Python 3.8+ not found on PATH. Skipping verifier. Install Python 3.8+ and run: python $dest/scripts/verify-install.py --skill-root $dest"
    fi

    # ---- next instruction -----------------------------------------------
    cat <<EOF

[web-claw] Installed for $host at: $dest

Next: open $PROJECT in your $host agent and tell it:

  Read web-claw/SKILL.md and run Web Claw for this project.

Or for an end-to-end build:

  Use Web Claw fast mode to build a [landing page | portfolio | site] for <project>.

EOF
}

# ---- main ---------------------------------------------------------------
if [[ "$HOST" == "all" ]]; then
    for h in codex claude cursor gemini opencode; do
        install_one_host "$h"
    done
else
    install_one_host "$HOST"
fi

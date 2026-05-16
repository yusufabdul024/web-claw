# Web Claw installer for Windows (PowerShell 5+).
#
# Copies this repo's skill files into the host-native skill directory for one
# or more AI coding agents and runs verify-install.py to confirm the result.
#
# Usage:
#   .\install.ps1 -Host <host> [-Project <path>] [-User] [-Force] [-DryRun]
#
#   -Host    codex | claude | cursor | gemini | opencode | all       (required)
#   -Project Path to the target project (default: current directory)
#   -User    Install to the user/global skill directory where supported
#            (currently: claude only). Ignored otherwise with a warning.
#   -Force   Overwrite an existing web-claw skill directory at the target.
#   -DryRun  Print what would happen without copying anything.
#
# The script assumes you have already cloned or downloaded the Web Claw repo
# and are running install.ps1 from inside that repo root. See README for
# host-native install destinations.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("codex", "claude", "cursor", "gemini", "opencode", "all")]
    [string]$HostName,

    [string]$Project = (Get-Location).Path,
    [switch]$User,
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Say  { param($Msg) Write-Host "[web-claw] $Msg" }
function Warn { param($Msg) Write-Host "[web-claw] WARN: $Msg" -ForegroundColor Yellow }
function Die  { param($Msg) Write-Host "[web-claw] ERROR: $Msg" -ForegroundColor Red; exit 1 }

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# ---- preflight: source repo must look like the Web Claw skill ----------
if (-not (Test-Path -LiteralPath (Join-Path $ScriptDir "SKILL.md"))) {
    Die "Run this from the Web Claw repo root (SKILL.md not found at $ScriptDir)."
}
if (-not (Test-Path -LiteralPath (Join-Path $ScriptDir "agents") -PathType Container)) {
    Die "agents/ missing in source ($ScriptDir). Is this a complete Web Claw checkout?"
}
if (-not (Test-Path -LiteralPath $Project -PathType Container)) {
    Die "-Project must be a directory that exists. Got: $Project"
}
$Project = (Resolve-Path -LiteralPath $Project).Path

# ---- host-destination resolution ---------------------------------------
function Resolve-Destination {
    param(
        [string]$HostName,
        [string]$Mode   # "project" or "user"
    )
    switch ($HostName) {
        "codex" {
            if ($Mode -eq "user") { return $null }
            return (Join-Path $Project ".agents\skills\web-claw")
        }
        "claude" {
            if ($Mode -eq "user") {
                return (Join-Path $env:USERPROFILE ".claude\skills\web-claw")
            }
            return (Join-Path $Project ".claude\skills\web-claw")
        }
        "cursor" {
            if ($Mode -eq "user") { return $null }
            return (Join-Path $Project ".cursor\skills\web-claw")
        }
        "gemini" {
            if ($Mode -eq "user") { return $null }
            return (Join-Path $Project ".gemini\extensions\web-claw")
        }
        "opencode" {
            if ($Mode -eq "user") { return $null }
            return (Join-Path $Project ".opencode\skills\web-claw")
        }
        default { return $null }
    }
}

$CopyItems = @(
    "SKILL.md", "README.md", "LICENSE", "skill.json",
    "agents", "assets", "qa", "references", "scripts", ".github",
    "install.sh", "install.ps1"
)

$ExcludePatterns = @(
    "__pycache__", "*.pyc", "*.pyo", ".pytest_cache",
    "node_modules", ".DS_Store", "Thumbs.db",
    "webclaw-lighthouse-*", "*.lighthouse.json", ".web-claw-cache"
)

function Copy-One {
    param(
        [string]$Source,
        [string]$Destination
    )
    if (-not (Test-Path -LiteralPath $Source)) { return }   # silently skip missing optional items
    if ($DryRun) {
        Write-Host ("    would copy: {0} -> {1}" -f (Resolve-Path -LiteralPath $Source).Path, $Destination)
        return
    }
    if (Test-Path -LiteralPath $Source -PathType Container) {
        $items = Get-ChildItem -LiteralPath $Source -Recurse -Force -Exclude $ExcludePatterns
        $rootName = Split-Path -Leaf $Source
        $destRoot = Join-Path $Destination $rootName
        if (-not (Test-Path -LiteralPath $destRoot)) {
            New-Item -ItemType Directory -Path $destRoot -Force | Out-Null
        }
        foreach ($item in $items) {
            # Skip items whose parent path matches an excluded directory name.
            $skip = $false
            foreach ($pat in $ExcludePatterns) {
                if ($item.FullName -like "*\$pat\*" -or $item.Name -like $pat) {
                    $skip = $true; break
                }
            }
            if ($skip) { continue }
            $relative = $item.FullName.Substring($Source.Length).TrimStart('\','/')
            $target = Join-Path $destRoot $relative
            if ($item.PSIsContainer) {
                if (-not (Test-Path -LiteralPath $target)) {
                    New-Item -ItemType Directory -Path $target -Force | Out-Null
                }
            } else {
                $targetDir = Split-Path -Parent $target
                if (-not (Test-Path -LiteralPath $targetDir)) {
                    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
                }
                Copy-Item -LiteralPath $item.FullName -Destination $target -Force
            }
        }
    } else {
        Copy-Item -LiteralPath $Source -Destination $Destination -Force
    }
}

function Install-OneHost {
    param([string]$HostName)

    $mode = if ($User.IsPresent) { "user" } else { "project" }
    $dest = Resolve-Destination -HostName $HostName -Mode $mode
    if (-not $dest) {
        if ($mode -eq "user") {
            Warn "-User is not supported for host '$HostName'. Skipping."
            return
        }
        Die "Unknown host: $HostName"
    }

    Say "Host: $HostName"
    Say "Destination: $dest"
    $dryNote = if ($DryRun.IsPresent) { " (dry-run)" } else { "" }
    Say "Mode: $mode$dryNote"

    if (Test-Path -LiteralPath $dest) {
        if ($Force.IsPresent) {
            if (-not $DryRun.IsPresent) {
                Remove-Item -LiteralPath $dest -Recurse -Force
            }
            Say "Removed existing destination (-Force)."
        } else {
            Die "Destination exists: $dest. Re-run with -Force to overwrite."
        }
    }

    if (-not $DryRun.IsPresent) {
        New-Item -ItemType Directory -Path $dest -Force | Out-Null
    }

    Say "Copying skill files..."
    foreach ($item in $CopyItems) {
        Copy-One -Source (Join-Path $ScriptDir $item) -Destination $dest
    }

    # Cursor convenience: drop a minimal rule file pointing at the skill.
    if ($HostName -eq "cursor" -and -not $DryRun.IsPresent) {
        $ruleDir = Join-Path $Project ".cursor\rules"
        if (-not (Test-Path -LiteralPath $ruleDir)) {
            New-Item -ItemType Directory -Path $ruleDir -Force | Out-Null
        }
        $rulePath = Join-Path $ruleDir "web-claw.mdc"
        $ruleBody = @'
---
description: Web Claw site-building skill
alwaysApply: true
---

Read .cursor/skills/web-claw/SKILL.md before any web-design task and follow the Web Claw pipeline. Begin every session by reading <project>/memory.md if it exists.
'@
        Set-Content -LiteralPath $rulePath -Value $ruleBody -Encoding utf8
        Say "Wrote $rulePath"
    }

    # Codex convenience: ensure AGENTS.md points at the skill. Codex reads
    # AGENTS.md from the project root for activation. If the file exists we
    # leave it alone and tell the user what line to add.
    if ($HostName -eq "codex" -and -not $DryRun.IsPresent) {
        $agentsFile = Join-Path $Project "AGENTS.md"
        $pointerLine = "Read .agents/skills/web-claw/SKILL.md and follow the Web Claw pipeline for any web design task. Begin each session by reading memory.md if it exists."
        if (-not (Test-Path -LiteralPath $agentsFile)) {
            $agentsBody = @"
# Project Agent Instructions

$pointerLine
"@
            Set-Content -LiteralPath $agentsFile -Value $agentsBody -Encoding utf8
            Say "Wrote $agentsFile"
        } else {
            $existing = Get-Content -LiteralPath $agentsFile -Raw
            if ($existing -match '\.agents/skills/web-claw') {
                Say "AGENTS.md already references web-claw; left unchanged."
            } else {
                Warn "AGENTS.md exists at $agentsFile but does not reference web-claw."
                Warn "Add this line manually for Codex to activate the skill:"
                Warn "  $pointerLine"
            }
        }
    }

    if ($DryRun.IsPresent) {
        Say "Dry run complete for $HostName -- nothing was written."
        return
    }

    # ---- verify ---------------------------------------------------------
    $py = $null
    foreach ($candidate in @("python", "py", "python3")) {
        if (Get-Command $candidate -ErrorAction SilentlyContinue) { $py = $candidate; break }
    }
    if ($py) {
        Say "Running install verifier..."
        $verifier = Join-Path $dest "scripts\verify-install.py"
        & $py $verifier --skill-root $dest
        if ($LASTEXITCODE -ne 0) {
            Die "verify-install.py failed (exit $LASTEXITCODE). Inspect $dest and re-run with -Force after fixing."
        }
    } else {
        Warn "Python 3.8+ not found. Skipping verifier. Install Python and run: python $dest\scripts\verify-install.py --skill-root $dest"
    }

    # ---- next instruction -----------------------------------------------
    Write-Host ""
    Write-Host "[web-claw] Installed for $HostName at: $dest"
    Write-Host ""
    Write-Host "Next: open $Project in your $HostName agent and tell it:"
    Write-Host ""
    Write-Host "  Read web-claw/SKILL.md and run Web Claw for this project."
    Write-Host ""
    Write-Host "Or for an end-to-end build:"
    Write-Host ""
    Write-Host "  Use Web Claw fast mode to build a [landing page | portfolio | site] for <project>."
    Write-Host ""
}

# ---- main ---------------------------------------------------------------
if ($HostName -eq "all") {
    foreach ($h in @("codex", "claude", "cursor", "gemini", "opencode")) {
        Install-OneHost -HostName $h
    }
} else {
    Install-OneHost -HostName $HostName
}

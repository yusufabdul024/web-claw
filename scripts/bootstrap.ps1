# bootstrap.ps1
#
# PowerShell convenience wrapper for Web Claw bootstrap on Windows.
#
# Usage:
#   .\bootstrap.ps1 -ProjectName "Meridian" -ProjectPath "C:\path\to\workspace"
#   .\bootstrap.ps1 -ProjectName "Meridian" -ProjectPath ".\workspace" -Mode fast -InstallDeps -StackMd ".\workspace\meridian\research\tech-stack.md"

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectName,

    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,

    [ValidateSet('interactive','fast')]
    [string]$Mode = 'interactive',

    [switch]$InstallDeps,

    [string]$StackMd
)

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Resolve project path
$resolvedProject = if ([System.IO.Path]::IsPathRooted($ProjectPath)) {
    $ProjectPath
} else {
    Join-Path (Get-Location) $ProjectPath
}

# 2. Initialize project workspace via init-project.py
Write-Host ""
Write-Host "Initializing '$ProjectName' under: $resolvedProject (mode: $Mode)"
python (Join-Path $scriptDir 'init-project.py') $ProjectName --path $resolvedProject --mode $Mode
if ($LASTEXITCODE -ne 0) {
    Write-Error "init-project.py failed (exit $LASTEXITCODE)"
    exit $LASTEXITCODE
}

# 3. Optionally run install-deps
if ($InstallDeps) {
    if (-not $StackMd) {
        $StackMd = Join-Path $resolvedProject 'research\tech-stack.md'
    }
    Write-Host ""
    Write-Host "Installing deps from: $StackMd"
    python (Join-Path $scriptDir 'install-deps.py') $StackMd --cwd $resolvedProject
    if ($LASTEXITCODE -ne 0) {
        Write-Error "install-deps.py failed (exit $LASTEXITCODE)"
        exit $LASTEXITCODE
    }
}

Write-Host ""
Write-Host "Done. Project ready at: $resolvedProject"

param(
    [string]$InstalledPath = "$env:USERPROFILE\.codex\skills\ccnote"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PackagePath = Join-Path $RepoRoot "ccnote"
$PackageAgentsPath = Join-Path $PackagePath "agents"
$InstalledAgentsPath = Join-Path $InstalledPath "agents"

if (-not (Test-Path -LiteralPath $InstalledPath)) {
    throw "Installed skill folder not found: $InstalledPath"
}

if (-not (Test-Path -LiteralPath (Join-Path $InstalledPath "SKILL.md"))) {
    throw "Installed SKILL.md not found: $InstalledPath"
}

if (-not (Test-Path -LiteralPath (Join-Path $InstalledAgentsPath "openai.yaml"))) {
    throw "Installed agents/openai.yaml not found: $InstalledAgentsPath"
}

New-Item -ItemType Directory -Force -Path $PackagePath | Out-Null
New-Item -ItemType Directory -Force -Path $PackageAgentsPath | Out-Null

Copy-Item -LiteralPath (Join-Path $InstalledPath "SKILL.md") -Destination (Join-Path $PackagePath "SKILL.md") -Force
Copy-Item -LiteralPath (Join-Path $InstalledAgentsPath "openai.yaml") -Destination (Join-Path $PackageAgentsPath "openai.yaml") -Force

Write-Host "Synced installed CCNote skill from $InstalledPath into repository package."


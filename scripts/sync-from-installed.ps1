param(
    [string]$InstalledPath = "$env:USERPROFILE\.codex\skills\ccnote"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PackagePath = Join-Path $RepoRoot "ccnote"
$PackageAgentsPath = Join-Path $PackagePath "agents"
$InstalledAgentsPath = Join-Path $InstalledPath "agents"
$PackageScriptsPath = Join-Path $PackagePath "scripts"
$InstalledScriptsPath = Join-Path $InstalledPath "scripts"

if (-not (Test-Path -LiteralPath $InstalledPath)) {
    throw "Installed skill folder not found: $InstalledPath"
}

if (-not (Test-Path -LiteralPath (Join-Path $InstalledPath "SKILL.md"))) {
    throw "Installed SKILL.md not found: $InstalledPath"
}

if (-not (Test-Path -LiteralPath (Join-Path $InstalledAgentsPath "openai.yaml"))) {
    throw "Installed agents/openai.yaml not found: $InstalledAgentsPath"
}

if (-not (Test-Path -LiteralPath (Join-Path $InstalledScriptsPath "validate_markdown_math.py"))) {
    throw "Installed Markdown math validator not found: $InstalledScriptsPath"
}

New-Item -ItemType Directory -Force -Path $PackagePath | Out-Null
New-Item -ItemType Directory -Force -Path $PackageAgentsPath | Out-Null
New-Item -ItemType Directory -Force -Path $PackageScriptsPath | Out-Null

Copy-Item -LiteralPath (Join-Path $InstalledPath "SKILL.md") -Destination (Join-Path $PackagePath "SKILL.md") -Force
Copy-Item -LiteralPath (Join-Path $InstalledAgentsPath "openai.yaml") -Destination (Join-Path $PackageAgentsPath "openai.yaml") -Force
Copy-Item -LiteralPath (Join-Path $InstalledScriptsPath "validate_markdown_math.py") -Destination (Join-Path $PackageScriptsPath "validate_markdown_math.py") -Force

Write-Host "Synced installed CCNote skill from $InstalledPath into repository package."


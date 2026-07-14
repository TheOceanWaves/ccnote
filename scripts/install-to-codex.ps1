param(
    [string]$Destination = "$env:USERPROFILE\.codex\skills\ccnote"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$Source = Join-Path $RepoRoot "ccnote"

if (-not (Test-Path -LiteralPath $Source)) {
    throw "Source skill folder not found: $Source"
}

$AgentsSource = Join-Path $Source "agents"
$AgentsDestination = Join-Path $Destination "agents"
$ScriptsSource = Join-Path $Source "scripts"
$ScriptsDestination = Join-Path $Destination "scripts"

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
New-Item -ItemType Directory -Force -Path $AgentsDestination | Out-Null
New-Item -ItemType Directory -Force -Path $ScriptsDestination | Out-Null

Copy-Item -LiteralPath (Join-Path $Source "SKILL.md") -Destination (Join-Path $Destination "SKILL.md") -Force
Copy-Item -LiteralPath (Join-Path $AgentsSource "openai.yaml") -Destination (Join-Path $AgentsDestination "openai.yaml") -Force
Copy-Item -LiteralPath (Join-Path $ScriptsSource "validate_markdown_math.py") -Destination (Join-Path $ScriptsDestination "validate_markdown_math.py") -Force

Write-Host "Installed CCNote skill to $Destination"


param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SkillPath = Join-Path $RepoRoot "ccnote"
$TestsPath = Join-Path $RepoRoot "tests"
$Validator = Join-Path $env:USERPROFILE ".codex\skills\.system\skill-creator\scripts\quick_validate.py"

if (-not (Test-Path -LiteralPath $SkillPath)) {
    throw "Packaged skill folder not found: $SkillPath"
}

if (-not (Test-Path -LiteralPath $Validator)) {
    throw "Skill validator not found: $Validator"
}

$env:PYTHONUTF8 = "1"
& $Python $Validator $SkillPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& $Python -m unittest discover -s $TestsPath -p "test_*.py" -v
exit $LASTEXITCODE


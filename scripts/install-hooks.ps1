$ErrorActionPreference = "Stop"

$repoRoot = (git rev-parse --show-toplevel).Trim()
$hookDir = Join-Path $repoRoot ".git\hooks"
$sourceHook = Join-Path $repoRoot "scripts\git-hooks\pre-commit"
$targetHook = Join-Path $hookDir "pre-commit"

New-Item -ItemType Directory -Path $hookDir -Force | Out-Null
Copy-Item -Path $sourceHook -Destination $targetHook -Force

Write-Host "Installed pre-commit hook."

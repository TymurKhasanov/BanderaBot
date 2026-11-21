Write-Warning (
    "This script is intentionally non-destructive. " +
    "Use git to review and apply source updates instead of overwriting project files."
)

& (Join-Path $PSScriptRoot "setup.ps1")

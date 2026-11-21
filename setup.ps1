$ErrorActionPreference = "Stop"

$folders = @(
    "app\database",
    "app\handlers",
    "app\keyboards",
    "app\middlewares",
    "app\scheduler",
    "app\services",
    "app\states",
    "app\utils",
    "app\data\skills",
    "logs"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot $folder) -Force |
        Out-Null
}

$venv = Join-Path $PSScriptRoot ".venv"
if (-not (Test-Path $venv)) {
    python -m venv $venv
}

& (Join-Path $venv "Scripts\python.exe") -m pip install -r (
    Join-Path $PSScriptRoot "requirements.txt"
)

& (Join-Path $venv "Scripts\playwright.exe") install chromium

Write-Host "BanderaBot environment is ready."

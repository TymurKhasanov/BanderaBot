$databasePath = Join-Path $PSScriptRoot "app\database"

New-Item -ItemType Directory -Path $databasePath -Force | Out-Null

foreach ($file in @("__init__.py", "database.py", "models.py", "repository.py")) {
    $path = Join-Path $databasePath $file
    if (-not (Test-Path $path)) {
        New-Item -ItemType File -Path $path | Out-Null
        Write-Host "Created $file"
    }
}

Write-Host "Database structure is ready."

$root = "C:\Projects\BanderaBot"

$databasePath = Join-Path $root "app\database"

# Создаем папку
New-Item -ItemType Directory -Path $databasePath -Force | Out-Null

# Список файлов
$files = @(
    "__init__.py",
    "database.py",
    "models.py",
    "repository.py"
)

foreach ($file in $files) {
    $path = Join-Path $databasePath $file

    if (-not (Test-Path $path)) {
        New-Item -ItemType File -Path $path | Out-Null
        Write-Host "Created $file"
    }
    else {
        Write-Host "$file already exists"
    }
}

Write-Host ""
Write-Host "========================================="
Write-Host " Database structure created successfully "
Write-Host "========================================="
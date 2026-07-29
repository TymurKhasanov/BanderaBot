# ===========================
# BanderaBot Project Setup
# ===========================

$root = "C:\Projects\BanderaBot"

# ---------- Folders ----------
$folders = @(
    "$root\app",
    "$root\app\database",
    "$root\app\handlers",
    "$root\app\keyboards",
    "$root\app\scheduler",
    "$root\app\services",
    "$root\app\states",
    "$root\app\utils",

    "$root\assets",
    "$root\assets\images",
    "$root\assets\templates",

    "$root\data",
    "$root\logs"
)

foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created folder: $folder"
    }
}

# ---------- Files ----------
$files = @(
    "$root\app\database\__init__.py",
    "$root\app\database\db.py",
    "$root\app\database\queries.py",

    "$root\app\handlers\admin.py",
    "$root\app\handlers\epics.py",
    "$root\app\handlers\prime.py",
    "$root\app\handlers\settings.py",

    "$root\app\keyboards\__init__.py",
    "$root\app\keyboards\main.py",
    "$root\app\keyboards\epics.py",
    "$root\app\keyboards\prime.py",
    "$root\app\keyboards\settings.py",

    "$root\app\scheduler\__init__.py",
    "$root\app\scheduler\scheduler.py",
    "$root\app\scheduler\jobs.py",

    "$root\app\services\__init__.py",
    "$root\app\services\notifications.py",
    "$root\app\services\epics.py",
    "$root\app\services\prime.py",
    "$root\app\services\settings.py",

    "$root\.gitignore",
    "$root\requirements.txt"
)

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
        Write-Host "Created file: $file"
    }
}

# ---------- .gitignore ----------
$gitignore = @"
.venv/
__pycache__/
*.pyc
logs/
data/database.db
.env
"@

Set-Content -Path "$root\.gitignore" -Value $gitignore

Write-Host ""
Write-Host "========================================"
Write-Host " BanderaBot structure is ready!"
Write-Host "========================================"
# ---------------------------------------------------------
# Petal Shortcut Setup
# ---------------------------------------------------------

$ErrorActionPreference = "Stop"

# Find the folder containing this script
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Petal executable
$PetalExe = Join-Path $ProjectRoot "dist\Petal\Petal.exe"

# Petal icon
$PetalIcon = Join-Path $ProjectRoot "petal.ico"

# Check that the required files exist
if (-not (Test-Path $PetalExe)) {
    Write-Host ""
    Write-Host "ERROR: Petal.exe was not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected:"
    Write-Host $PetalExe
    Write-Host ""
    Write-Host "Build Petal with PyInstaller first."
    exit 1
}

if (-not (Test-Path $PetalIcon)) {
    Write-Host ""
    Write-Host "ERROR: petal.ico was not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected:"
    Write-Host $PetalIcon
    exit 1
}

# Get the user's actual Desktop path.
# This works with normal Desktop and OneDrive Desktop.
$Desktop = [Environment]::GetFolderPath("Desktop")

# Shortcut path
$ShortcutPath = Join-Path $Desktop "Petal.lnk"

# Create Windows shortcut
$WshShell = New-Object -ComObject WScript.Shell

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)

$Shortcut.TargetPath = $PetalExe
$Shortcut.WorkingDirectory = Split-Path -Parent $PetalExe
$Shortcut.IconLocation = "$PetalIcon,0"
$Shortcut.Description = "Petal"

$Shortcut.Save()

Write-Host ""
Write-Host "======================================" -ForegroundColor Magenta
Write-Host "       Petal Setup Complete!" -ForegroundColor Magenta
Write-Host "======================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "Shortcut created:"
Write-Host $ShortcutPath
Write-Host ""
Write-Host "You can now launch Petal from your Desktop."
Write-Host ""
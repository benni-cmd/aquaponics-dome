# Legt eine Desktop-Verknuepfung "Einkaufsliste Kuppel" an, die scripts\open_einkaufsliste.bat startet.
# Aufruf: powershell -ExecutionPolicy Bypass -File scripts\make_shortcut.ps1 [-Name "Einkaufsliste Kuppel"]
param([string]$Name = "Einkaufsliste Kuppel")
$ErrorActionPreference = "Stop"
$bat = Join-Path $PSScriptRoot "open_einkaufsliste.bat"
if (-not (Test-Path $bat)) { throw "Nicht gefunden: $bat" }
$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = Join-Path $desktop ($Name + ".lnk")
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut($lnk)
$s.TargetPath = $bat
$s.WorkingDirectory = Split-Path $PSScriptRoot -Parent
$s.WindowStyle = 7   # minimiert: das Konsolenfenster der .bat blitzt nur kurz
$s.IconLocation = "$env:SystemRoot\System32\shell32.dll,165"
$s.Description = "Einkaufsliste der Kuppel (interaktiv, offline)"
$s.Save()
Write-Output $lnk

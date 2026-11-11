# RAM-Waechter (Ben 11.11.2026): schuetzt den PC vor Absturz durch volle Arbeitsspeicher.
# Misst alle 15 s die RAM-Auslastung. Ab 90 % zweimal hintereinander: groessten SolidCraft-/Python-Prozess beenden
# (Zwischenschritt bricht ab, gesichert ist, was committet ist). Ab 95 %: sofort beenden. Endet nach einem Eingriff
# mit einer Meldung (damit der Orchestrator geweckt wird) oder nach -Minuten.
# Aufruf: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/ram_guard.ps1 [-Minuten 60]
param([int]$Minuten = 60)
$ende = (Get-Date).AddMinutes($Minuten); $ueber = 0
function Auslastung { $os = Get-CimInstance Win32_OperatingSystem; [math]::Round(100 * (1 - $os.FreePhysicalMemory / $os.TotalVisibleMemorySize), 1) }
while ((Get-Date) -lt $ende) {
  $p = Auslastung
  if ($p -ge 90) { $ueber++ } else { $ueber = 0 }
  if ($p -ge 95 -or $ueber -ge 2) {
    $ziel = Get-Process -Name solidcraft-cli, solidcraft, python -ErrorAction SilentlyContinue | Sort-Object WorkingSet64 -Descending | Select-Object -First 1
    if ($ziel) {
      $mb = [math]::Round($ziel.WorkingSet64 / 1MB)
      Stop-Process -Id $ziel.Id -Force
      Start-Sleep -Seconds 5
      "EINGRIFF $(Get-Date -Format 'HH:mm:ss'): RAM $p %, beendet $($ziel.ProcessName) PID $($ziel.Id) ($mb MB); danach $(Auslastung) %"
      exit 0
    }
    "WARNUNG $(Get-Date -Format 'HH:mm:ss'): RAM $p %, aber kein SolidCraft-/Python-Prozess zum Beenden"
    exit 0
  }
  Start-Sleep -Seconds 15
}
"STUNDENCHECK $(Get-Date -Format 'HH:mm:ss'): RAM $(Auslastung) %, kein Eingriff"

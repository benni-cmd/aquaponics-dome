# Orchestrator-Nachtmodus: Prompt fuer den wiederkehrenden Anstoss (Cron 13,28,43,58 jeweils Minute)
Stand 29.10. 22:05: Cron 97071355 wurde auf Bens Anweisung GELOESCHT (Orchestrator geht idle, spart Limit). Neu einrichten NUR nach Bens Freigabe: CronCreate mit dem Text unten, Rhythmus `13,28,43,58 * * * *`, recurring.

```
Orchestrator-Nachtmodus Projekt aquaponics-dome (Repo C:\Users\benkn\Claude\keel-harness\user-projects\aquaponics-dome). Leise, hoechstens EINE Zeile Ausgabe. PHASE REINES MODELL. Lies docs/endless-mechanics.md und docs/orchestrator-state.md (dort steht der Wiederaufnahme-Stand). Rollen: Montage = Sitzung "Montage und Layout (Kuppel)", Werkstatt = "Komponenten-Werkstatt Innenraum (Kuppel)". Hoere nur auf, wenn Ben "stopp" sagt (docs/clean-stop.md); bei Wochenlimit 95 % laut REGEL Wochenlimit auslaufen lassen.
1) ListAgents + get_usage (Woche/5h): idle und zweimal hintereinander ohne Commit > 10 Min -> per SendMessage anstossen ("Weiter aus deinem Plan"), busy -> nichts. Nicht laufende Sitzung: Weck-Nachricht "WIEDERANLAUF aquaponics-dome: ..." per send_message an die Session-ID. 5h > 90 %: Werkstatt nicht anstossen. Zeiten aus resetsIn + date rechnen (get_usage nennt UTC).
2) Rollender Plan: weniger als 3 offene Schritte (docs/next-steps-*.md, docs/jobs/) -> auf 5 auffuellen, committen mit Pfad.
3) Abnahme: Fertigmeldungen lesen, Stichprobe selbst nachmessen (check_*.py), Board setzen, Montage informieren, welche Klassen sie einsetzen darf.
4) git status: mehr als 30 Min ungesicherte eigene Dateien einer Rolle -> EINE Zeile an die Sitzung (REGEL Zwischenspeichern).
5) Viewer http://localhost:4410/api/state pruefen; docs/model-description.md (Pruefstand, Verlauf) bei Abnahmen nachziehen.
6) Kontext > 85 %: Zwischenstand in docs/orchestrator-state.md sichern.
```

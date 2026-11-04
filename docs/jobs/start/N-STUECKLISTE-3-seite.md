# Start-Auftrag: N-STUECKLISTE Schritte 3 und 3b, Seite und Desktop-Verknuepfung (Orchestrator, 04.11.2026 nachts)

Weckruf statt neuer Sitzung (App-Grenze). Rolle: Werkstatt/Viewer fuer die Seite. Du kennst `scripts/bom.py` (13d48d1).
1. Blatt `docs/jobs/N-STUECKLISTE.md` Paket 3 und 3b sowie Pruefpunkte 5 und 6 lesen. Die fuenf Recherche-Dateien `data/beschaffung/*.json` sind jetzt auf Stand (letzte Commits e2acb7a, 83e7693, 83b4933, 4c00c58, 845d8bd): zusammenfuehren, NICHT aendern.
2. `docs/einkaufsliste.html` interaktiv: Sortieren nach jeder Spalte, Gruppieren nach Bauteilgruppen mit Gruppenpreis und Menge je Teil, Umschalter Gruppiert/nach Typ, Status und Grund bei fehlendem Preis, offline ohne externe Requests. Vorher den Werkbank-Skill `artifact-design` NICHT noetig (lokale Datei), aber `..\..\docs\ui-standard.md` lesen.
3. `scripts/open_einkaufsliste.bat` und `scripts/make_shortcut.ps1`. Ben hat die Desktop-Verknuepfung ausdruecklich gewuenscht (Wunschbuch W59, 04.11.): `make_shortcut.ps1` ausfuehren und die `.lnk` auf seinem Desktop anlegen; Pfad in die Meldung.
4. Verify: echter Screenshot im Browser-Pane, Desktop- und Schmalbreite, Pruefpunkte 5 und 6 selbst messen. Ein fehlgeschlagener Screenshot ist ein Blocker.
Nicht anfassen: Modell, `designs/`, `scripts/gen_dome.py`, `viewer/`, `data/beschaffung/` (parallel laeuft die Montage der Beete).
Sichern: `git commit -m "N-STUECKLISTE 3: ..." -- <pfade>`, `git push`. Abschluss: Paket-Haken 10 und 11b, hoechstens sechs Zeilen, dann STOPP.

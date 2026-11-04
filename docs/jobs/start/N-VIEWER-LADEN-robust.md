# Start-Auftrag: Viewer N-VIEWER-LADEN Nachbesserung (Ladefehler "Failed to fetch")

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Viewer. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Befund Orchestrator 04.11.: Ben sah beim Aufbauen "Definition 145 von 156" und "Failed to fetch" fuer `knoten_6_n09/n10`, `lt_bogen90_d50`, `lt_bogen90_d63`, `lt_rohr_d40_L1021/L1025/L1157`, `lt_rohr_d50_L55`. Seine Seite hatte den alten Stand (156 Definitionen) geladen, waehrend der volle Export genau diese Dateien neu schrieb (Zeitstempel 12:49 bis 13:05). Nachgestellt auf Port 4433 mit fertigem Export: 242 Dateien parallel, 0 Fehler, 477 MB; im Browser 164 Definitionen in 27 s, Kleinteile 78 Dateien in 9 s, keine Fehlermeldung. Zusaetzlich: `serve.py` startet beim Start sofort einen Export (`watch()`, `last = None`), auch wenn sich `dome.sc` nicht geaendert hat.
2. Export robust: `export_model.py` schreibt jede Datei erst als Temp-Datei und benennt sie dann um (`os.replace`), `instances.json` und `extras.json` zuletzt; so sieht der Browser nie eine halb geschriebene Datei.
3. `serve.py`: beim Start nur exportieren, wenn `dome.sc` neuer ist als `viewer/instances.json`.
4. Viewer: solange `/api/state` `busy` meldet, Hinweis "Export laeuft, Modell wird danach neu geladen" statt Laden; fehlgeschlagene Datei bis zu zweimal wiederholen, erst danach als Fehler zeigen.
5. Messen: Laden waehrend eines laufenden Exports am Muster ohne Fehlerzeile; normaler Start ohne Export; Screenshot im Browser-Pane. Kein Modellbau, nichts in `designs/`, `scripts/`, `data/`. Commits nur per Pfad, Push. Danach STOPP.

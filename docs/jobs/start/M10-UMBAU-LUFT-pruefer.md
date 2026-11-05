# Start-Auftrag: Pruefer M10-UMBAU (Runde 71) und M10-S5-LUFT Teil A

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Pruefer, nur lesen und messen; du hast nichts davon gebaut. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen. Nachtmodus D82: schwere Laeufe nur in einer Scratchpad-Kopie, freier RAM vorher >= 10 GB.

1. Gegenstand: Pruefpunkte aus `docs/jobs/M10-UMBAU.md` (Build e881f56 und Folgecommits) gegen `docs/leitungsordnung.md` (R1 bis R9) und Pruefpunkte aus `docs/jobs/M10-S5-LUFT.md` Teil A (Runde 69 gebaut, durch den Umbau veraendert); Maengel M03 bis M10 aus `docs/model-maengel.md`: welche sind behoben.
2. Gemeldet von der Montage: Build Exit 0, `check_walkways` PASS, `check_leitungen.py` 2 Verstoesse (K08 im Grobkasten des Tanks, K05-Gefaelle). check_latte Runde 69 (c4c8c63): 115 KOLL = Altbestand.
3. Messen: `check_leitungsordnung.py`, `check_leitungen.py`, `check_walkways.py`, `check_latte.py 71` in einer Kopie (git archive des aktuellen Stands, ca. 70 min, Hintergrund), Viewer auf eigenem Port ohne Export (erst nach Ende des laufenden Exports der Montage), Screenshots der umgebauten Strecken und der Luft am Pool gegen `..\..\docs\ui-standard.md`.
4. Ergebnis `docs/jobs/pruefung/M10-UMBAU.md` (Urteil je Blatt, Befehl neben jeder Zahl, Auflagen mit Owner). Commit nur dieser Datei per Pfad, Push. Danach STOPP.

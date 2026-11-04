# Start-Auftrag: Pruefer N-STUECKLISTE (Einkaufsliste), Pruefpunkte 1 bis 6

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Pruefer, nur lesen und messen; du hast nichts davon gebaut.

1. Grundlage: `docs/jobs/N-STUECKLISTE.md`, Abschnitt "Pruefpunkte", Punkte 1 bis 6. Punkt 7 (Detailansicht W60) ist noch nicht gebaut: nicht pruefen, im Befund als "nicht Gegenstand" fuehren.
2. Gebaut in den Commits 0a59f35, 13d48d1 (Skript, Zaehlung, Stueckliste) und 1470b8b, b8a6f14 (interaktive Seite, Bat, Verknuepfungsskript).
3. Falle Modellstand: die Montage der 14 Beete laeuft parallel (Commits M-BEET-TAUSCH) und aendert `ibc_beet*` und `viewer/instances.json`. Miss gegen den Stand, den `data/stueckliste.json` im Kopf stempelt; Abweichungen durch die Montage als Drift melden, nicht als Fehler der Liste. `bom.py` nur in einer Kopie im Scratchpad laufen lassen (BOM_ROOT), nie die Repo-Dateien ueberschreiben.
4. Seite: Screenshot Desktop und Schmalbreite gegen `..\..\docs\ui-standard.md`. Keine Desktop-Verknuepfung anlegen (das macht Ben selbst).
5. Kein Kauf, keine Anmeldung, keine Formulare; Links nur oeffnen und lesen.
6. Ergebnis: `docs/jobs/pruefung/N-STUECKLISTE.md` mit PASS / PASS mit Auflagen / FAIL je Punkt, Messbefehl neben jeder Zahl. Commit nur dieser Datei per Pfad (`git -C . commit -m "..." -- <pfad>`, neue Datei vorher `git add -N`), Push. Danach STOPP.

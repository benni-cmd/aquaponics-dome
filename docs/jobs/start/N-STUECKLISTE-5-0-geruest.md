# Start-Auftrag: Werkstatt W60 Schritt 5-0, Teile-Geruest fuer alle Komponenten

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Werkstatt. Vorher eigenen Kontext messen; ueber 35 % nicht anfangen, sondern das in einer Zeile melden.

1. Grundlage: `docs/jobs/N-STUECKLISTE.md`, Abschnitt "Zuschnitt in Pakete" Punkt 5 (W60) und Pruefpunkt 7. Stand: nur `data/parts/feinfilter.json` und `data/parts/tank_klein.json` existieren (Pilot).
2. Bauen: `bom.py` (oder ein eigenes Skript `scripts/parts_geruest.py`, das `bom.py` nutzt) erzeugt `data/parts/<komp>.json` fuer alle Komponenten der Stueckliste: je Koerper Teil-ID, Typ, `artikel_id` (aus `data/bom_regeln.json`/`data/katalog.json`), Menge; Format wie die Pilotdateien. Handgepflegte Felder (Funktion, Erklaertext, Explosion, Gruppen) werden nie ueberschrieben; die zwei Pilotdateien bleiben inhaltlich gleich (diff zeigt nur neue `artikel_id`-Felder).
3. Messen: `python -X utf8 scripts/workshop/check_parts.py` ueber alle Komponenten; Punkte, die nur an fehlenden Erklaertexten scheitern, als "offen fuer 5a" zaehlen, nicht als Fehler. Fehlende Verweise `artikel_id` -> Katalog und -> `stueckliste.json`: 0. Zweiter Lauf erzeugt identische Dateien (sha256).
4. Schreibe ins Paket `docs/packages/n-stueckliste.md` eine Tabelle: Komponente, Koerper, Teile, offene Felder je der fuenf Gruppen aus Punkt 5a (Kuppel, Tische/Beete, Becken/Filter/Pumpen, Leitungen, Huelle/Tuer/Fundament). Daraus startet der Orchestrator die fuenf Teiledaten-Sitzungen.
5. Nicht anfassen: `designs/`, `viewer/`, `data/leitungsnetz.json`, fremde nicht committete Aenderungen im Arbeitsbaum (`*.sc`, `viewer/extras.json`, `viewer/detail/`, Renders). Parallel laeuft ein Pruefer der Beet-Montage (nur lesend).
6. Commits nur per Pfad, neue Dateien vorher `git add -N`, je Teilschritt, Push. Danach STOPP.

# Start-Auftrag: Werkstatt N-MODELL-KOMPLETT Schritte 1 und 4 (Inventur, Tuer, Werkstoffe)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Werkstatt. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Grundlage: `docs/jobs/N-MODELL-KOMPLETT.md` (f4647b9) Schritt 1 (Inventur-Skript `scripts/model_inventar.py`, `docs/model-inventar.md`) und Schritt 4 (`tuer.sc` als abgeloest kennzeichnen, nicht loeschen; Werkstoffe aller eingesetzten Teile von `Default`/ohne Katalog auf Katalog-Werkstoffe, Katalog erweitern wo noetig).
2. Entscheidung Orchestrator zu Bens offenen Punkten des Blatts: Wandstaerke 3 mm gilt; `tuer.sc` kennzeichnen und behalten.
3. NICHT in diesem Auftrag: Schritt 2 (Strebe), 3 (Montage), 5 (Viewer). Parallel laeuft eine Montage (baut `dome.sc`) und eine Teiledaten-Sitzung der Gruppe Tische, Rinnen, Beete, Toepfe, die ebenfalls `data/katalog.json` erweitert: bei Konflikt `git pull --rebase`, nur eigene Eintraege. Kein `gen_dome.py`, kein `build.sh`, kein `viewer/`.
4. Messen: `python -X utf8 scripts/model_inventar.py` Exit 0; `python -X utf8 scripts/workshop/check_parts.py` Exit 0; Zahl eingesetzter Komponenten mit Werkstoff `Default` ausser Ausnahmeliste: 0 (Befehl daneben). Paket `docs/packages/n-modell-komplett.md` nachfuehren. Commits nur per Pfad, Push, WIP alle 20 Minuten. Danach STOPP.

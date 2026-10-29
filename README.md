# aquaponics-dome
Parametrisches SolidCraft-Modell einer geodaetischen Kuppel (12 m, 2V-Halbkugel) mit Aquaponik-System, nach Blender-Referenzen in `reference/`.
SolidCraft v0.25.1 (CLI + MCP, headless). Modell: `designs/dome.sc`, Export `designs/dome.step`.
Bauen: `sh scripts/build.sh <stufe 1-4> <runde>` (Skript `scripts/gen_dome.py`, Parameter-Tabelle `P`) -> `designs/dome.sc` + `renders/round-NN.png`.
Pruefen: `python scripts/check_latte.py` (PASS/FAIL je Mass, Kollisionen).
Ordner: `designs/` Modell, `scripts/` Generator + Pruefung, `renders/` Bilder, `docs/` Paket, Log, Checkpoint, `reference/` Vorlagen.

## Live-Viewer (3D, aktualisiert sich beim Speichern)

```
python viewer/serve.py 4410      # dann http://localhost:4410/ im Browser oeffnen
```
Der Server beobachtet `designs/dome.sc`, exportiert bei jeder Speicherung neu (`viewer/export_model.py`, kleine Koerper wie Salatkoepfe als Extras) und die Seite laedt das Modell ohne Kamera-Verlust nach. Drehen: linke Maustaste, Zoom: Mausrad, Schnitt-Regler, Gruppen ein/aus.

# aquaponics-dome
Parametrisches SolidCraft-Modell einer geodaetischen Kuppel (12 m, 2V-Halbkugel) mit Aquaponik-System, nach Blender-Referenzen in `reference/`.
SolidCraft v0.25.1 (CLI + MCP, headless). Modell: `designs/dome.sc`, Export `designs/dome.step`.
Bauen: `sh scripts/build.sh <stufe 1-4> <runde>` (Skript `scripts/gen_dome.py`, Parameter-Tabelle `P`) -> `designs/dome.sc` + `renders/round-NN.png`.
Pruefen: `python scripts/check_latte.py` (PASS/FAIL je Mass, Kollisionen).
Ordner: `designs/` Modell, `scripts/` Generator + Pruefung, `renders/` Bilder, `docs/` Paket, Log, Checkpoint, `reference/` Vorlagen.

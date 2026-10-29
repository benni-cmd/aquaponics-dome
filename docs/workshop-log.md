# Werkstatt-Log (Rolle W, Komponenten-Werkstatt Innenraum)

Beginn 29.10.2026 ~03:50. Befunde zu SolidCraft v0.25.1 (Headless, `solidcraft-cli run`) und Entscheidungen. Annahmen sind mit [A] markiert.

## Befunde zu den Komponentenbefehlen
- `component.create` (name, grounded), `parameters.add` (name, expression "50 mm"), `component.metadata.set` (part_number, description, revision, properties), `material.create`/`material.assign` (PP etc. fehlen in den Standardmaterialien, daher `material.create`), `appearance.assign` laufen im Headless-Lauf. Ausdruecke wie `"pot_d/2"` und Parameternamen werden in Primitiven (`solid.cylinder`, `solid.box`) akzeptiert.
- Skizze auf Ebene `XZ`: sketch-y bildet auf **-Z** ab (Koerper liegt bei Z < 0). Abhilfe: explizite Ebene `{"origin":[0,0,0],"x_dir":[1,0,0],"y_dir":[0,0,1]}`; dann ist sketch-y = Welt-Z. Revolve-Achse in Skizzenkoordinaten: `"y"` (klein), nicht `"Y"` (Welt).
- Werkzeug-Pfad: Python 3.12 liegt unter `C:\Users\benkn\AppData\Local\Programs\Python\Python312\python` (`python` im PATH ist der Store-Stub); Ausgabe mit `PYTHONIOENCODING=utf-8`.
- Arbeitsweise (Entscheidung W-1): Der Generator `scripts/workshop/<klasse>.py` liest `data/components/<klasse>.json` und schreibt ein Befehlsskript; `solidcraft-cli run --save` erzeugt die `.sc`. Die Parameter stehen zusaetzlich als `parameters.add` in der `.sc` (Primitive nutzen sie per Ausdruck; Skizzenprofile sind aus den JSON-Zahlen berechnet, nicht ueber Skizzen-Bemassung gebunden -> Aenderung = JSON aendern + Generator neu laufen lassen).
- `parameters.add` ohne `unit` macht jeden Wert zur Laenge (mm); dimensionslose Faktoren brauchen `unit: ""`.
- Primitive (`solid.box/cylinder/sphere`) und `solid.pattern.rectangular` (`count1`, `spacing1`) akzeptieren Parameter-Ausdruecke -> Lochzahl der NFT-Rinne ist ueber `n_holes`/`pitch` parametrisch; Laenge ueber `len_l`.
- `config.configure`/`config.row` legt Konfigurationen an (Salatkopf S/M/L). Laufzeit: Salatkopf (13 Kugel-Booleans + Zeilen) ca. 3 min, NFT-Rinne 6 s.
- Schachtelung funktioniert: `component.create` mit aktiver Komponente als Elternteil, `component.activate` zum Zurueckwechseln; `component.insert_design` des Rinne/Netztopf/Salatkopf in eine Testdatei klappt (auch mit `reuse: true`).
- Schnittansicht: `snapshot --section XZ` mit `yaw 3.14159` zeigt die Wandstaerken; Test: Netztopf sitzt im Topfloch, Kragen liegt auf der Rippenebene.
- Annahme [A]: Topf-Kragenunterseite liegt auf der Deckelflaeche (Z 95), Kragen 3,5 mm; Salat-Ursprung = Kragenoberkante.
- Befund: Die 2160 Pflanztoepfe des OBJ stehen in den Beeten (Z 407-506, 288 je Aussenbeet), nicht in den Rinnen; die Rinnen im OBJ haben keine Toepfe -> Topfzahl der Rinnen ist unsere Auslegung (Raster 200 mm).

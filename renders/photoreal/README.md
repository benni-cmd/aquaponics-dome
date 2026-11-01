# renders/photoreal: Foto- und Skizzen-Illustrationen (ComfyUI)

**Das sind Illustrationen, kein Modellbeleg.** Pflanzen, Rasen, Himmel und Strichfuehrung erfindet die KI; das Modell wird dafuer nie veraendert (Projektregel "reines Modell"). Pruefbilder bleiben die CAD-Ansichten aus `solidcraft-cli snapshot`.

## Aufruf (nur auf Zuruf, nie vom Loop)
```
python scripts/photoreal.py                          alle Kameras, beide Stile (foto, skizze)
python scripts/photoreal.py uebersicht               nur eine Kamera
python scripts/photoreal.py --stil skizze uebersicht nur die Tuschestrich-Skizze
```
Dauer etwa 2 bis 4 Minuten je Aufruf (Eingabebild 40 bis 60 s, ComfyUI je Bild etwa 1 Minute; ComfyUI-Start kommt dazu). Das Skript startet ComfyUI selbst und beendet es danach wieder.

## Dateien
- `<datum>_<kamera>_<stil>_s<seed>.jpg`: das Bild (im Repo). Daneben `.json` mit Prompt, Seed, Modell-Dateien, ComfyUI-Version, Eingabe-SHA, Commit.
- `_png/` (Original-PNG und Kantenbild) und `_input/` (Eingabebild aus dem Modell): nicht im Repo (`.gitignore`).
- Einstellungen (Kameras, Seeds, Prompts, ausgeblendete Koerper): `data/photoreal.json`. Workflow: `scripts/comfy/workflow_canny.json` (ComfyUI-API-Format, in der ComfyUI-Oberflaeche ueber "Load (API)" oeffenbar).

## Wie das Eingabebild entsteht
`designs/dome.sc` wird kopiert; in der Kopie wird die Erde unsichtbar geschaltet (`browser.visibility`) und die Haut auf Deckkraft 0 gesetzt, dann `solidcraft-cli snapshot` mit der Kamera aus der Tabelle. Das echte Design wird nie geschrieben.

## Bekannte Stolpersteine
- `HIP_VISIBLE_DEVICES=1` (fuer Modly gesetzt) laesst ComfyUI keine GPU finden; das Skript entfernt die Variable nur fuer den ComfyUI-Kindprozess.
- Nie gleichzeitig mit Modly/Hunyuan3D (gleiche Grafikkarte, 16 GB).
- Namen der Hautkoerper (`Folie_innen ...`) stehen in `data/photoreal.json`; fehlt einer, laesst das Skript ihn aus.

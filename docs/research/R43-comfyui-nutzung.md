# R43: Wie nutzen wir ComfyUI gerade, und was geht mit der Arbeitsweise besser?

**Prioritaet:** M · **Auftrag seit:** 01.11.2026 (Ben) · **Bearbeitet:** 01.11.2026 · **Zielparameter:** keine (reine Prozess-Recherche) · **Art:** nur lesen und analysieren; am Modell, an `scripts/gen_dome.py`, `designs/` und den Komponenten wurde nichts geaendert, nichts installiert, nichts heruntergeladen.

## Kurzantwort
1. **ComfyUI laeuft auf deinem Rechner und nutzt die RX 9060 XT, aber im Projekt ist es nie ueber einen Test hinausgekommen.** Es gibt genau einen gelungenen ControlNet-Canny-Test (Modellstand Runde 09, 29.10.) und einen gescheiterten img2img-Versuch. Seitdem: 48 weitere Modell-Runden, kein einziger Foto-Render, kein gespeicherter Workflow, kein Protokoll von Prompt und Seed.
2. **Die Technik ist nicht das Problem, die Eingabebilder und die Handarbeit sind es.** Das Kantenbild enthaelt Boden-Klotz, halbtransparente Haut und alle Kleinteile; es traegt keine Materialfarbe und keine Tiefe. SDXL erfindet den Rest (Rasen, Fliesen, gruene Streben, dunkles Rohr).
3. **Wichtigste Empfehlung:** erst einen Befehl bauen, der aus einer Kamera-Tabelle alle Ansichten rendert, reproduzierbar mit Seed und Protokoll (V1, klein, kein Download). Danach bessere Eingaben (Tiefe + saubere Kanten, V2). Beides erst NACH der Montage-Phase einsetzen; bis dahin reicht ein Vorschau-Test.
4. **Kein MCP, kein Rechner-Umbau.** Skript mit der lokalen API reicht und entspricht der Regel "CLI vor MCP".

## 1. Bestand

### 1a. Wo ComfyUI im Repo steckt (gemessen mit Grep ueber das ganze Repo: 17 Treffer in 12 Dateien)
| Stelle | Inhalt | Zustand |
|---|---|---|
| `docs/plan-process.md` Abschn. 4, 5, 6, 7 | Plan: `docs/environment.md` (Versionen, Seeds), Etappe E6 "ControlNet-Foto-Render", Morgen-Demo (e) | **`docs/environment.md` und `scripts/run_all.sh` existieren nicht** (geprueft: `ls`) |
| `docs/packages/system-logic.md` Punkt 9 | `solidcraft-playground/comfyui/generate.py --control` nach groesseren Schritten, Ergebnis `renders/photoreal-*.png`, danach ComfyUI beenden | offen (`[ ]`); keine `renders/photoreal-*.png` im Arbeitsbaum |
| `docs/packages/dome-build.md` Z. 46 | "img2img gescheitert (`failed-photoreal-01.png`), noetig ControlNet (Canny/Depth), nach den Schichten" | Stand 29.10., nicht fortgefuehrt |
| `docs/packages/wunschbuch-ben.md` W10, W40 | W40: "ComfyUI-Workflow fuer photoreale Renders einrichten und nutzen", Status **PRUEFEN (Stand nicht belegt)** | **mit diesem Bericht belegt** (siehe unten); Statuszeile ist Sache des Orchestrators |
| `docs/gauntlet.md` Z. 29, `docs/endless-mechanics.md` Z. 28, `docs/concept-atlas.md` Z. 56, `docs/next-steps-montage.md` Z. 34 (M8) | "Foto-Latte": Kritiker soll das ControlNet-Bild nicht zuverlaessig vom Originalrender (ref-4) unterscheiden koennen | Latte definiert, nie gemessen |
| `docs/packages/reihenfolge-offene-wuensche.md` Nr. 22, `data/roadmap.json` | W40 als offene PRUEFEN-Zeile; R43 als Auftrag | |
| `.gitignore` | `scripts/comfy*.log` | Muster ohne Datei im Repo |

### 1b. Was real auf dem Rechner liegt (nur gelesen)
| Punkt | Befund | Beleg |
|---|---|---|
| Installation | `C:\Users\benkn\Tools\ComfyUI\ComfyUI_windows_portable` (AMD-Portable, ausserhalb jedes Repos), ComfyUI **0.43.0**, Frontend 1.57.4, Python 3.12.10 | `comfyui-server.log`, `python_embeded\Lib\site-packages` |
| GPU | **AMD Radeon RX 9060 XT, "native", Total VRAM 16304 MB**, PyTorch **2.9.1+rocm7.2.1**, ROCm 7.2, `cuda:0`; RAM 31850 MB; Triton nicht vorhanden (`No module named 'triton'`), `comfy_kitchen` nutzt das HIP-Backend | Server-Log |
| Zweite GPU | Windows meldet zusaetzlich eine AMD-iGPU ("AMD Radeon(TM) Graphics", 512 MB); ComfyUI hat die richtige Karte gewaehlt (`Device: cuda:0 AMD Radeon RX 9060 XT`). Das Schwesterprojekt Modly setzt `HIP_VISIBLE_DEVICES=1` (wee-maskottchen, `docs/packages/mascot-low-poly-from-code.md`) | Log, `Get-CimInstance Win32_VideoController` |
| Modelle | `checkpoints/sd_xl_base_1.0.safetensors` (6,9 GB), `controlnet/controlnet-canny-sdxl-fp16.safetensors` (2,5 GB). **Keine** VAE, LoRAs, Upscaler, Depth-/Lineart-/Union-ControlNets | `ls models/*` |
| Custom Nodes | nur `websocket_image_save.py` (mitgeliefertes Beispiel). **Keine** Preprocessor-Nodes (kein Depth-Schaetzer) | `ls custom_nodes` |
| Workflows | keine gespeicherten Workflow-Dateien (`user/default/workflows` fehlt); der einzige "Workflow" steckt als Python-Graph in `generate.py` | `ls` |
| Laufzeit | Server laeuft **nicht** (Port 8188 geschlossen, kein ComfyUI-Prozess; ein laufender `python` ist der Viewer-Server auf Port 4410) | `Test-NetConnection`, Prozessliste |
| Geschwindigkeit | letzter Lauf: 25 Schritte SDXL + ControlNet, **ca. 1,7 bis 1,9 it/s (14 s Sampling), "Prompt executed in 44.36 seconds"** inkl. Modell-Laden; Ausgabe 1216×832 | Log (ein Lauf, `grep -c "Prompt executed"` = 1) |
| Ergebnisse | 5 Dateien in `ComfyUI\output`: `playground_00001` bis `00004` und `playground_canny_00001` (29.10., 00:44 bis 01:39). `playground_00004_.png` ist der Dome-ControlNet-Test | `ls -la output` |

### 1c. Der Aufruf: `solidcraft-playground/comfyui/generate.py` (anderes Repo, 130 Zeilen)
Baut den Graphen in Python (CheckpointLoader, CLIPTextEncode, optional LoadImage/VAEEncode fuer img2img, optional Canny + ControlNetApplyAdvanced), schickt ihn an `POST /prompt`, wartet auf `/history`, holt das Bild per `/view`. Kann ComfyUI selbst starten (`--start`). Fest eingebaut: Pfad `C:\Users\benkn\Tools\ComfyUI\...`, SDXL, Sampler `euler`/`normal`, cfg 7.0, Canny-Schwellen 0.2/0.6, Staerke 0.8. Der Seed wird zufaellig gewaehlt und nur auf die Konsole gedruckt; Prompt, Eingabebild und Modell-Hashes werden nicht gespeichert.

### 1d. Ergebnisse im Dome-Projekt
- `renders/failed-photoreal-01.png` (img2img aus `round-09`, 904×760): bleibt CAD-Optik, das falsch liegende Rohr bleibt, Streben bleiben grau-metallisch. Auch in `renders/history/` archiviert. Das fruehere `photoreal-01.png` wurde im Aufraeum-Commit `6d606d2` entfernt (nur in der Git-Historie).
- `solidcraft-playground/images/dome-controlnet-test.png` bzw. `ComfyUI\output\playground_00004_.png` (ControlNet-Canny, 1216×832, Eingabe `round-09`): Form und Beetanordnung stimmen, **Material und Umgebung sind erfunden** (gruene Streben, Rasenboden, Betonplatten-Hintergrund, Buesche, dunkles Rohr schwebt, Tanks weiss statt gruen). Die Pflanztische haben blaue Flaechen statt Pflanzen.
- Aktueller Modellstand ist `round-57` (31.10.): halbtransparente Haut, brauner Boden-Klotz mit Seitenwand, Beete, Tanks, Tuer, IBC-Puffer, Mensch-Figur. **Davon gibt es keinen Foto-Render.**

## 2. Ist-Arbeitsweise (vom Modell zum Foto-Render)
```
gen_dome.py ──► solidcraft-cli run ──► designs/dome.sc ──► solidcraft-cli snapshot
   (build.sh)                                              Kamera: {"target":[0,0,3300],"yaw":0,"pitch":0.5,"distance":21500}, 909×766
                                                             ▼
                                              renders/round-NN.png  (CAD-Farben, Haut transparent, Boden-Klotz)
                                                             ▼   HANDARBEIT: Bild waehlen, Prompt schreiben
   generate.py --control renders/round-NN.png --control-strength 0.8 --width 1216 --height 832 --start
       Bild → ImageScale (crop center) → Canny → ControlNet (SDXL) → KSampler (zufaelliger Seed)
                                                             ▼
   ComfyUI\output\playground_0000N_.png + --out  ──► (nichts weiter: kein Archiv, kein Protokoll, kein Vergleich mit ref-4)
```
**Wo Handarbeit ist:** Eingabebild auswaehlen und Kamera festlegen; Prompt jedes Mal neu; Server starten und danach beenden (System-Logic Punkt 9); Ergebnis nach `renders/` kopieren; Foto-Latte (Kritiker gegen ref-4) gibt es nicht als Ablauf.

**Wo es bricht:**
1. **Eingabe ist falsch fuer ControlNet.** Canny sieht nur Linien (siehe `playground_canny_00001_.png`): Rand des Boden-Klotzes, jede Haut-Kante, jede Pflanztisch-Bohrung. Keine Tiefe, keine Materialzuordnung. Die Haut aus mehreren Dutzend halbtransparenten Paneelen erzeugt ein Liniengewirr.
2. **Seitenverhaeltnis stimmt nicht.** Modell-Render 909×766 (1,19), Ausgabe 1216×832 (1,46); `ImageScale ... crop: center` schneidet etwa 19 % der Hoehe ab (gerechnet: 909→1216 skaliert 766 auf 1025 Pixel, zugeschnitten auf 832). Bei engerem Bildausschnitt gehen Teile verloren.
3. **Auflösung zu klein fuer Detail.** Ein 12-m-Dome mit Dutzenden Tischen, Toepfen und Leitungen in 1216×832: die Kleinteile verschwimmen. Kein zweiter Detail-Durchgang.
4. **Nicht reproduzierbar.** Zufaelliger Seed, nur in der Konsole; `docs/environment.md` fehlt; Script in anderem Repo mit festem Rechnerpfad.
5. **Modellstand veraltet.** Der einzige gelungene Test nutzt Runde 09; das heutige Modell wurde nie gerendert, die Foto-Latte nie gemessen.

Projektregel "reines Modell": ein Foto-Render ist Visualisierung. Er darf nie als Modellbeleg gelten (Pflanzen, Rasen, Umgebung sind erfunden). Jeder Foto-Render braucht den Vermerk "Illustration, kein Modellbeleg".

## 3. Verbesserungsvorschlaege (priorisiert)
Aufwand ist Schaetzung (nicht gemessen): S ≈ 1 bis 2 h, M ≈ halber Tag, L ≈ 1 bis 2 Tage. Quellen-Kuerzel `[Qn]` siehe Abschnitt 5.

### V1: Ein Befehl, alle Ansichten, mit Protokoll (Aufwand S, Nutzen hoch, ohne Download)
`generate.py` wird in dieses Repo als `scripts/photoreal.py` uebernommen (die Logik steht schon da), mit
- **Workflow als Datei:** der Graph als API-JSON `scripts/comfy/workflow_canny.json`; das Skript setzt nur Eingabebild, Prompt, Seed (so macht es auch das offizielle Beispiel [Q2]).
- **Kamera-Tabelle** `data/cameras.json` (cam_ref4, cam_ref5, cam_ref1, Innenraum, Detail): dieselbe Tabelle speist `solidcraft-cli snapshot --camera` und ComfyUI. Bildgroesse der Eingabe = Bildgroesse der Ausgabe (behebt Bruchstelle 2).
- **Fester Seed je Kamera**, Batch ueber alle Kameras in einem Lauf (Jobs einreihen und ueber `/history` abholen [Q1]).
- **Sidecar-JSON** je Bild (`renders/photoreal/<kamera>-<datum>.json`): Prompt, Seed, Modell-Dateinamen und Hashes, ComfyUI-Version, SHA des Eingabebildes, Commit. Danach `scripts/archive_render.py` automatisch. Behebt Bruchstelle 4 und fuellt `docs/environment.md`.
- Ausgabe-Beschriftung: "Illustration, kein Modellbeleg".
Quellen: ComfyUI-Doku Routen `/prompt`, `/upload/image`, `/history`, `/view` [Q1]; offizielles `basic_api_example.py` (API-Format, Seed im Graphen) [Q2]; comfy-cli unterstuetzt dasselbe Muster (API-Format-Workflow ausfuehren) [Q3]. **Konfidenz hoch**, weil die Routen schon in `generate.py` laufen (1 Lauf, 44 s).

### V2: Bessere Eingaben aus dem Modell: Tiefe + saubere Kanten, ein Union-ControlNet (Aufwand M, Nutzen hoch, braucht Download und Custom Node nach deiner Freigabe)
- **Saubere Kanten:** zweite Kamera-Aufnahme per `snapshot` mit Haut ausgeblendet/transparent und ohne Boden-Klotz (`--body NAME:opacity=0.0`, vorhandener Schalter in `solidcraft-cli 0.25.1`; keine Modelländerung).
- **Tiefe:** Tiefenbild statt oder zusaetzlich zu Canny. Zwei Wege: (a) Schaetzer auf dem sauberen Render (Depth Anything V2 Small, Apache-2.0, ueber `comfyui_controlnet_aux`) [Q7, Q8]; (b) echte Tiefe aus dem Modell (z-Buffer aus `viewer/model.obj`, eigene Rechnung, nicht quellenbelegt, ungeprueft). (b) ist genauer, (a) sofort ohne eigenen Code.
- **ControlNet-Modell:** ein Union-Modell (`xinsir/controlnet-union-sdxl-1.0`: Depth, Canny, Lineart, Segment u. a. in einer Datei, 1 Mrd. Parameter, F16) [Q5] statt mehrerer Einzelmodelle; Alternative `diffusers/controlnet-depth-sdxl-1.0` (Empfehlung der Modellkarte: Staerke 0,5) [Q4]. Dateigroesse des Union-Modells ist nicht belegt (Canny-Datei hat 2,5 GB), Schaetzung 2 bis 3 GB.
- Hinweis: Vorverarbeitung ist in ComfyUI nie automatisch; Tiefen-/Kantenbild muss vorher erzeugt werden [Q6].
**Konfidenz mittel**: Funktionsweise von zwei Quellen belegt, Wirkung auf dieses Modell ungeprueft (kein Test gemacht, kein Download erlaubt).

### V3: Materialfarbe und Pflanzen ueber ein Farb-ID-Bild statt Prompt-Hoffnung (Aufwand L, Nutzen mittel bis hoch)
Problem aus 1d: Tanks weiss statt gruen, Pflanztische blau, Boden Rasen. Ansaetze, in dieser Reihenfolge:
1. **Farb-ID-Render:** `snapshot` mit `--body NAME:color=#rrggbb` je Gruppe (Tank, Beet, Haut, Boden, Pflanze) und Segment-ControlNet (Union-Modell kann "Segment" [Q5]). Offen: das Modell erwartet eine bestimmte Segmentierungs-Palette; vorher klaeren, welche Farben zu welcher Klasse gehoeren (nicht geprueft).
2. **Regionale Prompts** ueber Bereichs-/Masken-Bedingungen (`ConditioningSetArea`); ComfyUI-Beispiel zeigt auch Grenzen: Farbbluten zwischen Durchgaengen, Qualitaet bei Nicht-Quadrat-Format [Q9].
3. **Referenzbild ref-4 als Stil** (IPAdapter): Repo meldet "maintenance mode" seit 04/2025, SDXL wird unterstuetzt [Q10]. Nur als Ergaenzung, nicht als Grundlage.
Erst nach V2 anfangen; V1/V2 allein sollen Geometrie und Tiefe verlaesslich machen. **Konfidenz niedrig bis mittel** (Quellen belegen Technik, nicht Ergebnis fuer dieses Modell).

### V4: Foto-Latte messbar machen, erst zum richtigen Zeitpunkt (Aufwand S, Nutzen mittel)
Nach V1/V2 einen Durchlauf (cam_ref4, Seed fest) gegen `reference/ref-4-dome-clean.jpg` mit getrenntem Kritiker (gleicher Gauntlet-Ablauf wie in `docs/gauntlet.md`). Zeitpunkt wie in W10/M8 geplant: **nach dem Zwischencheck**, wenn Farben/Materialien und Haut stehen. Bis dahin hoechstens ein Vorschau-Lauf mit dem aktuellen Stand, der nichts verspricht.

## 4. AMD/ROCm, MCP und CLI: Einschaetzungen
- **AMD unter Windows:** laeuft bereits, 1 gemessener Lauf (Log) ohne Fehler. Das aktuelle ComfyUI-README listet fuer Windows PyTorch-ROCm 10.0 (torch 2.13, Python 3.13) und nennt den RX-9060-XT-Bereich (`device-gfx1200`) [Q11]; unsere Installation hat torch 2.9.1+rocm7.2.1 auf Python 3.12 aus dem Portable-Paket. **Kein Update noetig** (Risiko ohne Gewinn). Das README warnt: `PYTORCH_TUNABLEOP_ENABLED=1` macht den ersten Lauf sehr langsam [Q11]. Praxisberichte nennen auf RDNA 4 gelegentlich Treiberabstuerze beim VAE-Decode [Q12]; bei uns nicht beobachtet (nur 1 Lauf, daher schwacher Beleg). Fuer Preprocessor-Nodes: ONNX/GPU-Varianten bei AMD nur `onnxruntime-gpu` genannt, sonst Torchscript oder CPU [Q7]; Depth Anything V2 Small laeuft ohnehin mit PyTorch.
- **VRAM:** 16 GB; SDXL + 1 ControlNet lief (laut Log wurden 4,06 GB beim Entladen frei). Ob SDXL + Union-ControlNet + Depth-Schaetzer + 2. Detail-Durchgang gleichzeitig passen, ist **nicht gemessen**. Nie parallel zu Modly/Hunyuan3D (gleiche Karte); ComfyUI nach jedem Lauf beenden (steht schon in System-Logic Punkt 9).
- **MCP:** Es gibt einen offiziellen lokalen `comfy-mcp` (Beta, 40 Tools, ruft `comfy`-CLI mit `--where local --json` auf, ComfyUI muss schon laufen) [Q13]; ausserdem einen Cloud-MCP [Q14]. **Nicht empfohlen:** 40 Tool-Beschreibungen kosten dauerhaft Kontext (Regel `tools.md`: CLI vor MCP), und V1 deckt dasselbe mit einem Skript ab. Erst pruefen, wenn Claude ComfyUI interaktiv iterieren soll (Slots setzen, Varianten) und ein Skript nicht reicht.
- **comfy-cli:** kann Workflows (API-Format) lokal ausfuehren, Modelle laden, Nodes verwalten [Q3]; AMD-Unterstuetzung steht im README nicht ausdruecklich. **Nicht noetig**, solange `photoreal.py` die API direkt anspricht; bei Bedarf spaeter pruefen.
- **Konsistenz ueber mehrere Ansichten:** Gleicher Seed und gleicher Prompt machen Stil und Farbe **aehnlich**, aber nicht garantiert gleich (Einschaetzung, nicht quellenbelegt). Wenn Ben Bildsatz-Konsistenz braucht, ist V3 (Farb-ID) der verlaesslichere Weg.

## 5. Quellen (gelesen am 01.11.2026; Seiten per WebFetch abgerufen und zusammengefasst, Zahlen aus diesen Zusammenfassungen)
| Nr. | Titel / URL | Art | Qualitaet | Verwendet fuer |
|---|---|---|---|---|
| Q1 | ComfyUI-Doku, Server-Routen: <https://docs.comfy.org/development/comfyui-server/comms_routes> | Hersteller-Doku | hoch | `/prompt`, `/upload/image`, `/history/{id}`, `/view` |
| Q2 | `script_examples/basic_api_example.py` im ComfyUI-Repo: <https://github.com/comfyanonymous/ComfyUI/blob/master/script_examples/basic_api_example.py> | Hersteller-Beispiel | hoch | API-Format, Seed/Prompt im Graphen setzen, Export "File → Export (API)" |
| Q3 | comfy-cli README: <https://github.com/Comfy-Org/comfy-cli> | Hersteller-Repo | hoch (AMD offen) | `comfy run` mit API-Format-Workflow |
| Q4 | Modellkarte `diffusers/controlnet-depth-sdxl-1.0`: <https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0> | Modellkarte | hoch | Tiefen-Konditionierung, Staerke 0,5, Tiefenschaetzer noetig (DPT/MiDaS) |
| Q5 | Modellkarte `xinsir/controlnet-union-sdxl-1.0`: <https://huggingface.co/xinsir/controlnet-union-sdxl-1.0> | Modellkarte (Community) | mittel | Depth/Canny/Lineart/Segment u. a. in einem Modell |
| Q6 | ComfyUI-Beispiele ControlNet: <https://comfyanonymous.github.io/ComfyUI_examples/controlnet/> | Hersteller-Beispiele | hoch | Vorverarbeitung ist nie automatisch |
| Q7 | `comfyui_controlnet_aux`: <https://github.com/Fannovel16/comfyui_controlnet_aux> | Community-Repo | mittel bis hoch | Depth Anything V2, Lineart, Canny, Segment; onnxruntime/AMD-Hinweis |
| Q8 | Depth Anything V2: <https://github.com/DepthAnything/Depth-Anything-V2> | Forschungs-Repo | hoch | relative Tiefe; Small Apache-2.0, Base/Large CC-BY-NC-4.0 |
| Q9 | ComfyUI-Beispiele Area Composition: <https://comfyanonymous.github.io/ComfyUI_examples/area_composition/> | Hersteller-Beispiele | hoch | regionale Prompts, Farbbluten, Format-Grenzen |
| Q10 | `ComfyUI_IPAdapter_plus`: <https://github.com/cubiq/ComfyUI_IPAdapter_plus> | Community-Repo | mittel | Referenzbild-Stil, "maintenance mode" |
| Q11 | ComfyUI README (AMD Windows): <https://github.com/comfyanonymous/ComfyUI> | Hersteller-Repo | hoch | ROCm-Windows-Hinweise, RX 9060 XT = `device-gfx1200`, TunableOp-Warnung |
| Q12 | Wccftech-Anleitung RDNA 4 / ROCm 7.1.1 Windows: <https://wccftech.com/how-to-setup-comfyui-ai-image-generation-on-amd-rdna-4-gpu-rocm-7-1-1-windows/>; AMD "Radeon Limitations": <https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-6.4.4/docs/limitations/limitationsrad.html> | Praxisbericht / AMD-Doku | niedrig bis mittel (nur Suchtreffer-Zusammenfassung, Seiten nicht selbst geoeffnet) | Hinweise zu Treiberabstuerzen, Windows-Support-Stand |
| Q13 | `Comfy-Org/comfy-mcp`: <https://github.com/Comfy-Org/comfy-mcp> | Hersteller-Repo | hoch | 40 Tools, Beta, ruft comfy-CLI |
| Q14 | Comfy Cloud MCP: <https://docs.comfy.org/development/cloud/mcp-server> | Hersteller-Doku | mittel (nur Suchtreffer) | Cloud-Variante, nicht relevant fuer lokal |
Lokale Belege: `ComfyUI_windows_portable\comfyui-server.log`, `models/`, `custom_nodes/`, `output/`, `solidcraft-playground/comfyui/generate.py`, `solidcraft-cli snapshot --help` (0.25.1).

## 6. Widersprueche
| Aussage A | Aussage B | moegliche Ursache | gewaehlte Seite |
|---|---|---|---|
| Plan (`plan-process.md`): `environment.md`, `run_all.sh` sind vorhanden | Dateisystem: beide fehlen | Plan wurde nur geschrieben, `build.sh` ersetzte `run_all.sh` | Dateisystem gilt; Plan nachfuehren |
| README Windows: ROCm 10.0 / torch 2.13 / Python 3.13 | Installation: torch 2.9.1+rocm7.2.1, Python 3.12 | Portable-Paket vom 27.10. aelter als README-Stand | funktioniert, nicht aendern |

## 7. Konfidenz und Luecken
- **Bestand und Ist-Arbeitsweise: hoch** (direkt gemessen/gelesen). **V1: hoch. V2/V3: mittel/niedrig**, weil nichts davon ausprobiert wurde (keine Downloads, keine Installation).
- Nicht gemessen: VRAM bei Union-ControlNet + Schaetzer; Laufzeit bei 2 Durchgaengen; ob SDXL die Kleinteile bei hoeherer Aufloesung (Tiles) sauber haelt; Wirkung von `--body opacity=0` auf Kantenbild.
- Nur eine Messung fuer die Laufzeit (1 Prompt im Log; das Log wird beim Neustart ueberschrieben).
- Q12 stammt aus einer Suchtreffer-Zusammenfassung, nicht aus gelesenen Seiten.

## 8. Folge
- Kein Parameter in `params.json`. Vorschlag fuer den Orchestrator: W40 auf "Bestand belegt (R43); Umsetzung = V1/V2, nach Zwischencheck" setzen; `docs/plan-process.md` Abschn. 4 (nicht vorhandene Dateien) und `system-logic.md` Punkt 9 (Skript-Ort) beim naechsten Anfassen angleichen.
- Entscheidungen fuer Ben: siehe "Offen" in der Abschlussmeldung.

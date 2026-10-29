# SolidCraft-Befehle fuer echte Komponenten und Instanzen (geprueft am 29.10.2026 mit `solidcraft-cli commands`)

Ziel (Ben): jedes wiederkehrende Bauteil (Salatkopf, Strebe, Knoten, Tisch, Rinne, Tank, Beet ...) EINMAL definieren, Kopien sind Instanzen; Aenderung der Definition wirkt ueberall. Bisher entstehen Salatkoepfe (240), Streben (61) usw. als lose Einzelkoerper per Skript. SolidCraft kann es besser:

| Zweck | Befehl | Hinweis |
|---|---|---|
| Komponente anlegen | `component.create` (name, parent, grounded?) | Geometrie wird in der aktiven Komponente gebaut (`component.activate`) |
| Bauteil aus eigener Datei | `component.insert_design` (path = `designs/components/<name>.sc`, name?) | verknuepfte Komponente: Definition steht in einer eigenen .sc-Datei |
| Definition ersetzen/aktualisieren | `component.update_links`, `component.relink` | liest die verknuepften Dateien neu, alle Instanzen folgen |
| Instanz setzen | `occurrence.copy` (component, translate, axis, angle, origin ...), `occurrence.move` | eine Definition, viele Platzierungen |
| Muster aus Komponenten | `solid.pattern.rectangular` / `solid.pattern.circular` (Parameter `components`) | z. B. Salatkoepfe in Reihen, Tische im Zehneck-Ring |
| Normteile (Schrauben, Muttern, Scheiben) | `parts.insert` (family: socket_head_cap_screw, hex_bolt, hex_nut, washer, set_screw, dowel_pin, bearing; size "M10"; length) | fuer Knoten, Fussplatten, Beinverbindungen |
| Profile (Rohr, Rechteckrohr, Winkel ...) | `frame.profile.insert` (kind: round_tube, rect_tube, ...) | Streben als echte Profile mit Wandstaerke |
| Stueckliste | `assembly.bom` (levels: flat/top) | `bom.md` aus dem Modell erzeugen |
| Metadaten | `component.metadata.set` (part_number, description, revision, values) | fuer das Bauteilblatt |
| Parameter | `parameters.add` / `parameters.export` | `params.json` und SolidCraft-Parameter synchron halten |

Regeln fuer dieses Projekt:
1. Pro Bauteilklasse eine Datei `designs/components/<klasse>.sc` (z. B. `salatkopf.sc`, `strebe_a.sc`, `strebe_b.sc`, `knoten_5.sc`, `nft_tisch_innen.sc`, `ibc_beet_aussen.sc`, `tank_klein.sc`); Dom-Skript verknuepft sie mit `component.insert_design` und platziert Instanzen mit `occurrence.copy` oder `solid.pattern.*` nach `data/layout.json`.
2. Aenderung = Definition aendern, `component.update_links`, Neubau; keine Zahlen in den Platzierungsschleifen.
3. Salatkopf: EIN Bauteil (z. B. 5-7 ueberlappende abgeflachte Kugeln oder Rotationskoerper, wenige Facetten), Groessenvarianten als eigene Komponenten (Tisch, Wanne), Instanzen per Muster.
4. Hinweis Export/Viewer: SolidCraft meshed jeden Koerper nach seiner eigenen Groesse; kleine gekruemmte Koerper werden dadurch riesig (240 Kugeln = 1,25 GB OBJ). Salatkoepfe niedrig tesselliert bauen (wenige Facetten) oder im Viewer als Extras zeichnen (`viewer/export_model.py`).

## Befund Headless-Test (Integrator, 29.10.2026)
- `component.insert_design {path, name}` + `occurrence.copy {component}` + `occurrence.move {occurrence:"Name:n", matrix:[12 Zahlen], tolerance:1e-6, move_grounded:true}` funktionieren im CLI-Lauf (`solidcraft-cli run`). Instanznamen `Name:1`, `Name:2` ...
- FALLE: `occurrence.copy` kopiert die aktuelle (ggf. schon verschobene) Platzierung. Reihenfolge: erst alle Kopien am Ursprung, dann jede Instanz einmal mit `occurrence.move` (Matrix absolut) setzen.
- `matrix`: Zeilen-Reihenfolge `[r00 r01 r02 tx, r10 r11 r12 ty, r20 r21 r22 tz]`, Spalten = Basisvektoren; Rundung auf 9 Stellen und `tolerance` 1e-6 noetig.
- `eval` listet Instanz-Koerper in Weltlage, Name `<Koerper> (<Instanz>)`; `inspect.interference` arbeitet damit.
- Umgesetzt fuer Streben: `scripts/components/strebe.py` -> `designs/components/strebe_a.sc/strebe_b.sc`; 61 Instanzen in `designs/dome.sc`. Noch offen: `component.update_links`-Test, Wurzel-Baugruppen 01-10, Normteile.

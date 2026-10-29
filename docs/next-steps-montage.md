# Naechste Schritte Montage und Layout (Rolle M) — rollender Plan, immer 3-5 definierte Schritte

Besitzer: Orchestrator (fuellt auf). Die Montage-Sitzung liest diese Datei als Erstes, arbeitet den obersten Schritt ab, hakt ihn im `docs/loop-state.md` ab und meldet dem Orchestrator, sobald nur noch 2 Schritte uebrig sind. Es darf nie ohne definierten naechsten Schritt dastehen. Je Schritt: Ziel · Eingaben/Quellen · Ergebnis (DoD) · Pruefung · Abhaengigkeit. Pruefung nach `docs/review-protocol.md` (Scope-Card, Kontextpaket, Vorpruefung, Bild-Kritiker + Spec-Pruefer, Triage), Herkunft nach `docs/provenance.md`, Struktur nach `docs/cad-standard.md`.

**Rolle M (Montage und Layout):** besitzt `designs/dome.sc`, `scripts/gen_dome.py`, `scripts/build.sh`, `data/params.json`, `data/system.json`, `viewer/`, `scripts/check_*.py`, `designs/components/` der **Zwischenbauteile** (Kuppel: Streben, Knoten, Anker, Tuer, Haut; Leitungen: Rohr, Bogen, T-Stueck, Ventil, Verteiler, Schlauch, Klemme, Halter) und das Layout (Anordnung, Platzierung der Werkstatt-Komponenten nach `layout.json`). Die Werkstatt baut Salatkopf, Netztopf, NFT-Rinne/Tisch, IBC-Beete, Tanks, Pumpen; Montage verknuepft sie, sobald das Board `docs/integration-board.md` sie als `abgenommen` fuehrt.

## Jetzt (Uebernahme)
**M0 Uebernahme:** `docs/loop-state.md` (Uebergabestand der alten Sitzung) und `docs/endless-mechanics.md` lesen, `git status`, `python scripts/check_latte.py`, `python scripts/check_components.py` laufen lassen, Zahlen notieren; erster Checkpoint in `docs/loop-state.md` (max. 12 Zeilen, ersetzt den alten). DoD: Checkpoint steht, Checks gemessen.

## Naechste Schritte
**M1 Abgenommene Werkstatt-Komponenten einbauen + Pflanzen als Instanzen:**
- Ziel: Netztopf, Salatkopf (und NFT-Rinne, sobald abgenommen) per `component.insert_design` verknuepfen; Pflanzen in den 8 Aussenbeeten als Instanzen (288 je Beet, Raster aus `layout.json`), keine losen Kugeln mehr.
- Ergebnis: `10_Pflanzen` besteht aus Instanzen; `check_components.py` PASS; Viewer-Export meldet Pflanzen aus der Instanzliste (Positionen).
- Pruefung: `check_components`, `check_latte`, Render `cam_ref4`; Abhaengigkeit: Abnahme durch Orchestrator.

**M2 Knoten und Streben-Feinheit (R02):**
- Ziel: Knoten 4/5/6-wertig als Komponenten (Platten/Huelsen, Normschrauben M10 per `parts.insert`), Streben-Teillaenge = Knoten-zu-Knoten minus 2 x `strut_end_offset`, 10 Fundamentanker.
- Eingaben: `docs/research/R02.md`, `layout.json` `dome.nodes_list`, Scope-Card wird vom Orchestrator angelegt (Aufgabe vor dem Bau).
- Ergebnis: 26 Knoten als Instanzen, Anker, Bauteilblaetter `knoten_*`; Pruefung: Vorpruefung (Zahl je Wertigkeit 10/6/10, Strebenlaengen), Kritiker + Spec-Pruefer.

**M3 Tuer_Komplett (R13):**
- Ziel: Baugruppe im unteren Dreieck mit Spitze Z 3150: Pfosten, Sturz, Schwelle, Tuerblatt 1000 x 2000 (nach aussen), Scharniere, Seitenfelder, Anker; Basisstrebe zwischen den Pfosten entfaellt.
- Eingaben: `docs/research/R13.md`; Ergebnis: Komponente + Platzierung am Tuer-Azimut (OBJ ca. 167 Grad, Dreieck per Knotenliste), Eintrag in `decisions.md`; Pruefung: Vorpruefung (Normmass, Dreieck passt), Kritiker.

**M4 Wasserweg als Graph:**
- Ziel: `data/system.json` (Bauteile mit Ports aus den Fittings in `layout.json`, Rohre/Schlaeuche als Kanten, `routing: surface|buried`) und `scripts/check_hydraulics.py` (nur Modell-Logik: Graph verbunden und Kreislauf geschlossen, Port genau einmal belegt, Enden auf Ports, Gefaelle und Pumpenrichtung, keine Rohre im Tuerzugang).
- Eingaben: `docs/hydraulics.md` (Flussbild), `docs/decisions.md` D06/D14. Ergebnis: Graph + Check PASS. Abhaengigkeit: Port-Positionen der Werkstatt-Komponenten (Tanks, Beete, Tische) teils Annahme bis diese abgenommen sind.

**M5 Rohre und Schlaeuche aus dem Graphen:**
- Ziel: Komponenten Rohrstueck, Bogen, T-Stueck, Ventil, Verteiler, Schlauchstueck, Klemme/Halter, verlegt nach Regeln `docs/hydraulics.md` Abschnitt 5 (Biegeradius >= 5 x Durchmesser, Halter alle 0,5-1 m, parallel mit festem Abstand, Gehwege frei), Farben nach Funktion.
- Ergebnis: Leitungsnetz als Instanzen, Kollisionspruefung 0, Bauteilblaetter; Pruefung: Vorpruefung (Enden auf Ports), Kritiker + Spec-Pruefer.

## Reserve
M6 Haut T2 (R11) · M7 Gesamtansicht-Gauntlet `cam_ref4`/`cam_ref5`/`cam_ref1`/Schnitt · M8 ControlNet-Foto-Render mit farbigem Modell (Schlusschritt).

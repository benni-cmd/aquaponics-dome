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

## Auffuellung 29.10. 14:35 (Orchestrator)
**M6 Viewer klein halten (zuerst, vor M1.3):** Problem: `viewer/model.obj` ist von 76 MB auf 320 MB gewachsen (Instanzen werden je Instanz voll exportiert); der Live-Viewer im Browser wird dadurch traege oder laedt nicht. Ziel: Export je Komponentendefinition EINMAL plus Instanz-Transformationen (three.js InstancedMesh bzw. Gruppen mit Matrix), Zielgroesse unter 40 MB, Ladezeit unter 10 s. Eingaben: `viewer/export_model.py`, `viewer/index.html`, `component.list` mit Instanzen/Transformationen (occurrence-Daten). Ergebnis: Export schreibt `model.obj` (nur Definitionen/Unikate) + `instances.json` (Name, Matrix, Farbe); Viewer baut daraus die Szene; Vorher/Nachher-Screenshot im Bildverlauf. Pruefung: gleiche Ansicht wie vorher (Screenshot-Vergleich), Zeit und Dateigroesse gemessen, Kamera bleibt beim Reload. Abhaengigkeit: keine.
**M1.3 Netztoepfe/Salatkoepfe als Instanzen:** wie unter M1 Punkt 4 (2716 Instanzen) — Instanzen nur ueber den neuen Viewer-Pfad exportieren (M6), nicht als Koerper in model.obj.
**M1.4 Innenring-Tische:** erst nach Werkstatt-Variante W16 (Beine ausserhalb Beet, Innenring Auflage auf Beckenrand); bis dahin offen.

## Auffuellung 29.10. 19:55 (Orchestrator, Ben: Laufwege >= 0,5 m, Platz klug nutzen)
**M7 Laufwege, Erreichbarkeit, Radialbudget (vor M3; D29, Ben 20:10):** Ziel: Radien von Pool, Innen-/Aussenbeeten und Tischen nach dem Budget in `docs/jobs/W17-radialbudget.md` setzen (Rand 2095 | A 600 | Innenportal | B 600 | Aussenportal | Wandluft), Laufwege >= 600 (nie < 500), Tuer-Gang (Azimut ca. 167) >= 900 bis zum Pool, Tanks/Pumpentafeln/Ventile von einer Seite mit >= 500 erreichbar; Rohre/Schlaeuche duerfen Laufwege nicht blockieren (D14: vergraben/abgedeckt). Erreichbarkeit nicht zu tief pruefen (Ben gibt Feedback): einfache Regel, Beet einseitig <= 800 / zweiseitig <= 1000. Eingaben: D28, D29, `data/layout.json`, R15, W17-Blatt. Ergebnis: Parameter `inner_bed_shift`, `outer_bed_shift`, `walkway_min` 600 (D21/D24/D25 ersetzt), `scripts/check_walkways.py` (Abstaende Ring zu Ring, Tuer-Gang, Bodenauslastung in %), Draufsicht mit Massen im Bildverlauf; Tisch-Aussenkante in 1,3 m Hoehe gegen die Domstreben nachrechnen. Pruefung: check_walkways PASS, check_latte ohne Kollision. Abhaengigkeit: Werkstatt W17 liefert Aussenbeet 800 x ~2640 und die neu angepassten Tische; bis dahin Beete mit den Budgetmassen platzieren.

**Hinweis D35 (30.10.):** Becken zentrieren (cx = cy = 0) statt `inner_bed_shift` 26; in M7 beruecksichtigen. Haut-Paneele (W19) setzt die Montage spaeter ein.

**Auffuellung 30.10. 11:30 (Orchestrator):** M7 fertigmachen (Becken zentrieren D35, Aussenbeete 800 x ~2640 mit neuem Topfraster D34, Laufweg B >= 500, Ziel 600, check_latte 24/24). Danach **M3 Tuer nach D36:** Tuer im Basisfeld BBB 149,2 (nicht bei 167), zweites Becken auf Azimut 149,2 drehen, `tuer_komplett.sc` kommt von der Werkstatt (W20). Dann Haut einsetzen (40 Felder `felder[]` in data/components/haut_paneel.json, 65 Kappen; Tuerfeld mit Ausschnitt), danach M4/M5 Rohre und Schlaeuche.

**HINWEIS 30.10. 14:00 (D39):** Huelle ist eine Plane, keine Paneele. Schritt "Haut einsetzen" ruht bis R24 und Werkstatt-Bauteile; Tuer (M3) bleibt. Sonst Reihenfolge unveraendert (M7, M3, M4/M5).

**HINWEIS 30.10. 14:30 (D43):** Aussentisch bekommt 4 Rinnen (674 Toepfe) als Standard, sobald die Werkstatt W25a meldet. Reihenfolge: check_latte 43 fertig laufen lassen, M3 Tuer, DANN extract_nft_pots + build + check_walkways + ein gemeinsamer check_latte mit aussen4. Pumpen: D38.

**HINWEIS 31.10. 00:30:** Jetzt M3 Tuer: `tuer_fn` durch `tuer_komplett.sc` ersetzen (Feld BBB 149,2, D36), nur bauen, noch kein check_latte. Danach NICHT weiter: erst Werkstatt-Meldung W25a (aussen4) und W26 (Innenbeet-Fase) abwarten, dann extract_nft_pots, build, check_walkways, EIN check_latte, danach M4/M5 (Rohre).

**HINWEIS 31.10. 01:10 (D46):** Drittbecken + Puffer-Station kommen als M8 (docs/jobs/M8-drittbecken-puffer.md) nach Werkstatt W28. Reihenfolge: W25a/W26 -> Neubau -> W28 -> M8 -> EIN check_latte.

**HINWEIS 31.10. 01:40:** M8 (Drittbecken + Puffer-Station) kommt vor W26: sobald Werkstatt W25a und W28 gemeldet haben -> extract_nft_pots, Neubau mit aussen4, M8, check_walkways. Der grosse check_latte folgt erst nach W26 (Innenbeet-Fase).

**HINWEIS 31.10. 02:40 (D47):** Nach M8: M9 zwei Referenzfiguren (docs/jobs/M9-mensch-platzieren.md), sobald Werkstatt W29 meldet.

**HINWEIS 31.10. 04:00 (D50):** Nach der M8/M9-Messung: M10 Leitungen (docs/jobs/M10-leitungen.md) erst, wenn R28 (Netzliste) und W30 (Stands) gemeldet sind; Plan vorab im Paket. Danach check_latte und Pause.

**HINWEIS 31.10. 05:00 (D51):** M9 fertig (a535701, Build 51). Naechste Schritte: (1) das EINE check_latte nach M9 (steht in loop-state.md), (2) M10 Leitungen mit Plan vorab: Pumpentafeln seitlich am Tankstand setzen (W30: Plattform klein 619, gross 821), Feinfilter (W31) einplanen. Erst starten, wenn die Werkstatt W31 gemeldet hat.

**HINWEIS 31.10. 12:30 (D52):** Zu M10 gehoert vorab: Innenbeete bepflanzen (`bed_pot_grid()` auch fuer `ibc_beet_innen_933`, Params `pot_pitch`/`pot_margin`), Build, check_walkways; Zahl der Beet-Toepfe in loop-state.md melden.

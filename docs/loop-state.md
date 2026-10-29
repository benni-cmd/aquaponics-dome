# Loop-Checkpoint (Loop v3: Detail-Schichten)
- Stand: Runde 12, Schicht 1+2 fertig (Farben, 210 Salatkugeln), check_latte 23/23 PASS.
- Schichten: 1 Farben [x] · 2 Pflanzen [ ] · 3 Tankraender+Wasser [ ] · 4 Schlaeuche/Rohr [ ] · 5 Haut T2 [ ] · 6 Rippen/Neigung [ ]
- Jetzt kommt: Pflanztisch-Bauteil per component.insert_design (reuse) + occurrence.move (Drehung um Z) ins Dom-Modell einsetzen, alte T8-Koerper ersetzen; check_latte anpassen (T8-Zaehlung per Komponente).
- Nach Abbruch: `git status`, letzter Commit; `sh scripts/build.sh 4 NN` regeneriert alles.
- ComfyUI/ControlNet erst nach den Schichten (Schlussschritt E). `renders/failed-photoreal-01.png`: img2img unbrauchbar.
- Checkpoint (Limit 96 %, Reset in ~8 min): Erkundung Komponenten: SolidCraft kann echte Instanzen (`component.insert_design` = verlinkte Instanz eines Designs, `occurrence.copy`, `occurrence.move`, `component.copies`, `solid.pattern.*`). Plan: Bauteil als `designs/components/<name>.sc` bauen und per `component.insert_design` + `occurrence.move` platzieren. Naechster Schritt: `describe_command component.insert_design` und `occurrence.move`, dann Pflanztisch-Bauteil (Schritt 3a des Auftrags). Katalog (Anzahl): Strebe 63, Pflanztisch 10, Fasstank 6, Zentralpool 1, Mitteltank 1, Substratwanne 4, Salatkopf 210, Schlauch 6, Tuer 1, Rohr 1, Schaltschrank 1.

## Checkpoint (Limit 0 %, 02:10): OBJ-Korrekturen (reference/oasis-obj-analysis.md)
Reihenfolge: 1 Pool zentriert D3,89 (Wasser) + T6 entfaellt (nicht im OBJ) · 2 T7 = 4 Tanks (Azimut OBJ 147/237 klein, 131/252 gross, r 3,35 m) auf Plattformen + Pumpenmodule · 3 T9 = 14 IBC-Wannen · 4 NFT-Ring statt 10 Tische · 5 Strebenprofil 30x30 · 6 offene Fragen · check_latte neu. Azimut-Abbildung OBJ->Modell: +111 Grad (Tuerseite OBJ ~195 -> Modell -54).
Jetzt kommt: Schritt 1+2.

## Checkpoint 02:3x (fuer frischen Lauf ohne Verlauf)
- Stand: Runde 13, check_latte 24/24 PASS. Fertig: OBJ-Schritte 1 (Pool zentriert) und 2 (4 Tanks). Bau: `sh scripts/build.sh 4 NN`, Pruefung `python scripts/check_latte.py`.
- Naechster Schritt: OBJ 3 (T9 = 14 IBC-Wannen: 8 aussen r~5,2 m Laenge 3 m Azimut OBJ 355/319/247/31/140/67/283/103; 6 innen r~3,3 m Laenge 1,2-2,0 Azimut 318/103/283/67/30/354; Hoehe 0,64; +111 Grad), dann OBJ 4 (NFT-Ring), 5 (Strebe 30x30), 6 (offene Fragen), dann `docs/packages/system-logic.md` (Systemgraph data/system.json zuerst).
- Annahmen: Azimut +111; T6 Mitteltank entfaellt; Pumpe 0,7 m innerhalb des Tanks; Beete T8/T9 alt bleiben bis ersetzt.

## Checkpoint R14
- Stand: check_latte 20/21 (einziger FAIL: T8-Name fehlt, bis der NFT-Ring steht). Fertig: OBJ 1, 2, 3 (Aussen-Wannen r=5,0 m statt 5,2, damit Ecken im Zehneck bleiben).
- Naechster Schritt: OBJ 4 NFT-Ring: Topfpositionen im OBJ (Downloads/Project_Oasis_Layout.obj, Gruppen potplant) per scripts/analyze_nft.py clustern (Radius-/Hoehenstufen, Reihenabstand, Topfabstand); Rohrsegment mit Topfreihe als EIN Bauteil designs/components/nft_rohr.sc, per Instanz/Muster um den Ring (Luecke Tuerseite OBJ 150-240 Grad).

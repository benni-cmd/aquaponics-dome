# Loop-Checkpoint (Loop v3: Detail-Schichten)
- Stand: Runde 12, Schicht 1+2 fertig (Farben, 210 Salatkugeln), check_latte 23/23 PASS.
- Schichten: 1 Farben [x] · 2 Pflanzen [ ] · 3 Tankraender+Wasser [ ] · 4 Schlaeuche/Rohr [ ] · 5 Haut T2 [ ] · 6 Rippen/Neigung [ ]
- Jetzt kommt: Pflanztisch-Bauteil per component.insert_design (reuse) + occurrence.move (Drehung um Z) ins Dom-Modell einsetzen, alte T8-Koerper ersetzen; check_latte anpassen (T8-Zaehlung per Komponente).
- Nach Abbruch: `git status`, letzter Commit; `sh scripts/build.sh 4 NN` regeneriert alles.
- ComfyUI/ControlNet erst nach den Schichten (Schlussschritt E). `renders/failed-photoreal-01.png`: img2img unbrauchbar.
- Checkpoint (Limit 96 %, Reset in ~8 min): Erkundung Komponenten: SolidCraft kann echte Instanzen (`component.insert_design` = verlinkte Instanz eines Designs, `occurrence.copy`, `occurrence.move`, `component.copies`, `solid.pattern.*`). Plan: Bauteil als `designs/components/<name>.sc` bauen und per `component.insert_design` + `occurrence.move` platzieren. Naechster Schritt: `describe_command component.insert_design` und `occurrence.move`, dann Pflanztisch-Bauteil (Schritt 3a des Auftrags). Katalog (Anzahl): Strebe 63, Pflanztisch 10, Fasstank 6, Zentralpool 1, Mitteltank 1, Substratwanne 4, Salatkopf 210, Schlauch 6, Tuer 1, Rohr 1, Schaltschrank 1.

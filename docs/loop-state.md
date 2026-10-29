# Loop-Checkpoint (Loop v3: Detail-Schichten)
- Stand: Runde 10, check_latte 23/23 PASS (Kollisionen 0 nach Strebenlift 75 mm, Bettbeine/Wannen entzerrt).
- Schichten: 1 Farben [ ] · 2 Pflanzen [ ] · 3 Tankraender+Wasser [ ] · 4 Schlaeuche/Rohr [ ] · 5 Haut T2 [ ] · 6 Rippen/Neigung [ ]
- Jetzt kommt: Schicht 1 (Farben je Teil per Aussehen-Befehl, `describe_command appearance.assign`).
- Nach Abbruch: `git status`, letzter Commit; `sh scripts/build.sh 4 NN` regeneriert alles.
- ComfyUI/ControlNet erst nach den Schichten (Schlussschritt E). `renders/failed-photoreal-01.png`: img2img unbrauchbar.

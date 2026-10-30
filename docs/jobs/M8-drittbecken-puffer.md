# M8 Drittbecken und Puffer-Station platzieren (Ben 31.10., D46) — NACH Werkstatt W28 und W25a/W26
Ziel: Drittbecken (Durchmesser 1,03 m, Tiefe 1,13 m, Parameter) und die Puffer-Station (`puffer_station`, 2 uebereinander gestapelte IBC, Werkstatt W28) stehen im Modell, ohne Kollision und ohne Laufweg < 500 (Tuer-Gang >= 900).
Eingaben: D46, D36 (Tuer BBB 149,2, Zweitbecken auf Tuerachse); `docs/session-notes/werkstatt.md` (W28 melden); `reference/designer-glb-analysis.md` (Designer-Modell: Drittbecken Ø 1,03 hinter dem Zweitbecken, gleiche Achse, Radius ca. 1,5 m weiter aussen).
Lage: Puffer-Station im freien Sektor RECHTS NEBEN DER TUER, wenn man hereinkommt (Blick von der Tuer nach innen, rechte Hand: bei den Sektoren 149,2 (Tuer) und 185,2 sind die zwei Sektoren ohne Aussenbeet; pruefe die Drehrichtung gegen layout.json). Drittbecken hinter bzw. neben das Zweitbecken am Tuersektor, ohne die Tuergasse zu verstellen.
Pruefen: Stapelhoehe <= freie Domhoehe an der Aufstellkante (Abstand zu Streben >= 100 mm), Wandluft, Laufwege A/B, check_walkways, check_latte (nur nach dem ersten Neubau mit aussen4 EIN Lauf), Draufsicht mit Massen in den Bildverlauf.
Nicht anfassen: Werkstatt-Komponenten. Instanzen als `Puffer_Station:1`, `Becken_Dritt:1` mit Parametern, kein neuer Einzelkoerper.
Ergebnis: WIP-Commit je Schritt, Stand in `docs/loop-state.md`.

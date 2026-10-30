# W27 Huelle als Plane: Komponenten (D39, R24) — NUR Komponenten, kein Einbau
Problem: Die Huelle ist eine Plane (Ben), die Paneel-Komponenten (W19/W20) ruhen als Variante. Es fehlen Bauteile fuer die Plane.
Ziel: Drei Komponenten mit Ports und Herkunftsblatt, die die Montage spaeter an den 65 Streben/40 Feldern einsetzt.
Eingaben: `docs/research/R24.md` (Abschnitt Empfehlung Plane und Folge fuer Modell), D39, D45; `data/layout.json` (nodes_list, struts, Feldtypen aus `data/components/haut_paneel.json`); `docs/jobs/README.md`, Standards. Keine weiteren Dateien lesen.
Schritte (jeder einzeln committen):
1. `keilschiene.sc`: Alu-Kanal ca. 25 x 15 mm, Laenge je Strebe minus Knotenfreiraum (Typen A 3279, B 3708 abzueglich Steckenden), mit Federdraht (D 2 mm) als eigener Koerper; Blatt `docs/parts/keilschiene.md` (Q/E/A). Anzahl 65.
2. `huelle_folie.sc`: EIN Typ je Dreiecksform (AAB, BBB, Tuerfeld), duenne transparente Flaeche, 2 Lagen im Abstand ca. 100 mm (Luftpolster [A]), 100 mm Ueberstand je Seite, ziegelartige Ueberlappung als Parameter `overlap`; Gesamtflaeche 208 m2 gegen R24 pruefen; Blatt `docs/parts/huelle_folie.md`.
3. `tuer_zarge_planenausschnitt.sc`: Rahmen-Uebergang Zarge (tuer_komplett) zum Planenausschnitt, Klemmleiste; Anschluss an `tuer_komplett` Ports.
Pruefung: Vorpruefung per Skript (Flaechensumme 208 m2 +-3 %, Strebenlaenge gegen layout.json, Interferenz mit Strebe/Zarge 0), ein Render, KEIN Pruefer-Lauf (Limit).
Nicht anfassen: `dome.sc`, Paneel-Komponenten (nichts loeschen), Layout.
Ergebnis: Komponenten + Blaetter + `check_huelle.py`, WIP-Commit je Schritt, Push, Zeile in `docs/workshop-state.md`.

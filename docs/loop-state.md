# Uebergabestand Integrator (Stopp 29.10.2026, nach R21)
## Fertig (Commits)
- Layout aus data/layout.json (Drehung door_az-167 = -221), Zahlen aus data/params.json: 57a02ce (R20), 68dfa67 (R19), c90f532 (R18), R17 Streben als Instanzen; R21 siehe git log (Tuer_Komplett).
- Wurzel Kuppel_Aquaponik mit 10 Baugruppen (01_Layout leer, 02..10 belegt), keine losen Koerper in der Wurzel.
- Verknuepfte Komponenten (designs/components, gebaut von gen_dome.py component_file()): strebe_a/b (64 Instanzen), erdflaeche, fundamentring, pool_zentral, zweitbecken, tuer (Tuer_Komplett), zulaufrohr, schaltschrank. Pools eingelassen (Z -1825, Rand 650, Wasser 515).
## Angefangen/halbfertig
- Tuer: Seitenfelder (dreieckig), Anker im Erdreich, parts.insert-Schrauben fehlen. 01_Layout nur leer angelegt. Knoten (R02) und Haut nicht begonnen.
- Werkstatt-Klassen noch lose im Dom (Beete 14, Tanks+Pumpen 20, Salatkugeln 240): ersetzen, sobald docs/integration-board.md "abgenommen" fuehrt.
## Bekannte Fallen und Befunde
- component.insert_design + occurrence.copy + occurrence.move (matrix, tolerance 1e-6, move_grounded) funktionieren headless; ERST alle Kopien, DANN absolut platzieren (Kopie erbt Matrix).
- Instanz-Koerper heissen im eval "<Koerper> (<Baugruppe>:n/<Komponente>:m)"; check_latte zaehlt per Praefix.
- XZ-Skizzenebene: sketch y = -Z. Boolean-Joins mit tangentialen Flaechen scheitern (Beinbreite/Kugel-Zylinder: Radius leicht aendern). Coincidente Zylinderkoerper ergeben "Interferenz" mit Volumen 0.
- 3V hat keinen Aequatorring; 2V (freq 2) liefert Halbkugel mit 10 Basisknoten. Dome/Fundamentring um 18 Grad gedreht, Tuer-Dreieck bei Azimut -72.
- Aussenbeete wurden 200 mm schmaler (Streben schneiden sonst Beetkante); Beet 4 zusaetzlich 500 mm kuerzer.
## Messwerte mit Befehl
- python scripts/check_latte.py -> 19/19 PASS (Kollisionen 0). python scripts/check_components.py -> 4 PASS, 1 FAIL (lose Werkstatt-Koerper). python scripts/interf.py listet Interferenzen.
## Offene Punkte mit Besitzer
- Knoten 4/5/6 (R02), Haut T2, Fundamentanker, 01_Layout-Skelett, Seitenfelder/Anker Tuer: Montage-Sitzung. NFT-Ringe (3 Zehneck-Ringe, components.md) und Werkstatt-Komponenten einbauen: Montage nach Abnahme. check_fidelity, check_hydraulics, system.json: nicht begonnen (Montage). Strebenprofil strut_r 45 mm (A, R01) vs OBJ 30x30: DEINE ENTSCHEIDUNG.
## Bau-Aufrufe
- sh scripts/build.sh 4 NN (baut Komponenten + designs/dome.sc + renders/round-NN.png + section-NN.png); danach python scripts/check_latte.py und check_components.py; Export: solidcraft-cli run designs/dome.sc --out designs/dome.step.

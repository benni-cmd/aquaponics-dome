# N-VERBINDER: Scherenknoten mit Lochplatte (W74)

**Problem:** Das Modell verbindet die 65 Streben mit Kugelknoten D100, Steckarm 23 x 23 und Querbolzen. Das echte Verbindungsstueck aus Chemnitz (Foto `reference/chemnitz/laschenknoten-foto.jpg`) ist ein Scherenknoten mit Lochplatte. R41 hat die Schere nicht erkannt.
**Intent:** Ben soll den echten Verbinder verstehen und pruefen koennen, bevor 26 Knoten und 130 Strebenenden umgebaut werden.
**Goal:** Der Bericht `docs/research/R56-scherenknoten.md` und der Prototyp `designs/components/knoten_schere_proto.sc` (eine Lochplatte und eine Schere im Rohrstueck, Nasen ausgefahren) liegen mit Skript, Render und Bauteilblatt gepusht vor. Das Gesamtmodell bleibt unveraendert.

## Plan
1. Quellen lesen: R41, R34, `docs/parts/knoten.md`, `docs/parts/strebe.md`, Foto mit vergroesserten Ausschnitten.
2. Rechnung `scripts/r56_scherenknoten.py` mit Selbsttest: Neigung, Rohrlaenge, Profile rund und vierkant, Einziehen der Nasen, Kraftweg, Masse.
3. Bericht R56: Funktion, Teile, Rund gegen Vierkant, Statik grob, Kauf- und Laserteile in Europa, Fragen an Ben.
4. Prototyp `scripts/components/knoten_schere_proto.py` -> `.sc`, Check, Render `renders/components/knoten_schere_proto/`, Bauteilblatt `docs/parts/knoten_schere_proto.md`.
5. Pfad-Commits und Push. KEIN Einbau ins Gesamtmodell und keine Serie bis Ben den Prototyp abnimmt.

## Dateien (keine Ueberschneidung mit parallelen Sitzungen)
`docs/research/R56-scherenknoten.md`, `scripts/r56_scherenknoten.py`, `scripts/components/knoten_schere_proto.py`, `designs/components/knoten_schere_proto.sc`, `renders/components/knoten_schere_proto/`, `docs/parts/knoten_schere_proto.md`, dieses Blatt, Wunschbuch-Zeile W74.

## Stand
05.11.2026: Plan angelegt. Rechnung Selbsttest 6/6. R56 geschrieben. Prototyp gebaut, Check 6/6, 5 Renders angesehen, Bauteilblatt `docs/parts/knoten_schere_proto.md`. Wartet auf Bens Abnahme (R56 Abschnitt 6, fuenf Fragen). Gesamtmodell unveraendert.
Nachtrag 05.11.: Ben trennt Recherche, Planer und Werkstatt; Knoten wird EINMAL als Bauteil gebaut, Montage setzt Instanzen (Scherenzahl und Drehung). Auftragsblatt `docs/jobs/N-VERBINDER.md` geschrieben; der Prototyp `knoten_schere_proto` gilt als Vorentwurf fuer die Werkstatt.

Werkstatt 05.11.2026 (Blatt `docs/jobs/N-VERBINDER.md`): Scherenknoten EINMAL gebaut, `designs/components/knoten_schere_platte.sc`, `knoten_schere_arm_a.sc`, `knoten_schere_arm_b.sc` (+ Detailmodell `knoten_schere.sc`), Generator `scripts/workshop/knoten_schere.py`, Knotentabelle `data/components/knoten_schere.json` (26 Knoten, 130 Arme, Loch und zwei Drehwinkel je Arm), Bauteilblatt `docs/parts/knoten_schere.md`, 8 Bilder `renders/components/knoten_schere/`, Viewer-Detailansicht `#detail=knoten_schere`. Vorentwurf `knoten_schere_proto` geloescht (Begruendung im Bauteilblatt).
Pruefpunkte des Blatts gemessen:
1. `python -X utf8 scripts/workshop/check_knoten_schere.py` → 29/29 PASS, Exit 0 (Koerper geschlossen, Nasen 24,2 = 21,2 + 3,0 mm, Rohrachse 0,004 / 0,001 mm vom Knotenpunkt).
2. Probe-Knoten n01 (Platte + 6 verknuepfte Instanzen): `inspect.interference` 6 Paare, alle Drehpunktschraube/Mutter 0,025 mm3 (Gewinde), 0 ueber 0,1 mm3.
3. Tabelle 26 Knoten, 10 x 4 / 6 x 5 / 10 x 6, 130 Arme, A 60 / B 70.
4. Groesster Achsversatz 15,07 mm (n02, 5-wertig, 24 Grad Drehung) → BEFUND an Ben: 5-Loch-Platte fuer die 6 fuenfwertigen Knoten; 4- und 6-wertig 1,1 mm.
5. 8 Bilder inkl. 2 Explosionsbilder, angesehen und gegen das Foto verglichen; Teiledaten `check_parts.py knoten_schere` 22/22.
Abweichung vom Blatt: A und B unterscheiden sich auch in der Lage der Knicklinie (A r 72,1, B r 63,0), weil die gemeinsame Platte eine gemeinsame Hoehe erzwingt; Zuschnitt gleich. Naechster Schritt: fremder Pruefer, dann Ben-Abnahme.
Werkstatt W83 05.11.2026 nachmittags (Ben: obere und untere Lochplatte, Scheren dazwischen): `knoten_schere_platte.sc` ist jetzt ein Plattenpaar (2 gleiche Platten D 110 x 8, Spalt 10 mm = zwei Laschenaugen), Plattenschraube M10 x 45 durch beide Platten, Arme unveraendert. Pruefer-Auflagen a1ed36b: Auflage 5 erledigt (Probe n02 fuenfwertig als Pflichtlauf im Check), Auflage 4 Viewer-Detailansicht angesehen (13 Teile, Gruppe Plattenpaar). Check `python -X utf8 scripts/workshop/check_knoten_schere.py` → 35/35 PASS, Exit 0 (n01 und n02 ohne Durchdringung > 0,1 mm3); `check_parts.py knoten_schere` 22/22; 9 Bilder neu (neu: 09 Plattenpaar nah). Masse aller Knoten ohne Rohre 63,7 kg. Offen bei Ben: 5-Loch-Platte, vier Blatt-Fragen; Auflage 3 (Blatt-Text Knicklinie) beim Orchestrator.

## Montage D91 (Start-Auftrag `docs/jobs/start/N-VERBINDER-montage.md`, 05.11.2026 abends)
**Problem:** Das Gesamtmodell (beide Varianten) traegt noch Kugelknoten und Vierkantstreben 30 x 30 x 3; Ben hat den Scherenknoten freigegeben (D91: eine 6-Loch-Platte fuer alle 26 Knoten, Rundrohr 42,4 x 2,6, Laschen 8 mm).
**Intent:** Das Modell zeigt den echten Verbinder, damit Stueckliste, Viewer und Pruefungen auf dem gebauten Knoten stehen.
**Goal:** `designs/dome.sc` (A+) und `designs/dome-ring_b2.sc` (Ring B2) tragen an allen 26 Knoten ein Plattenpaar und je Strebe einen Scherenarm, die 64 Streben sind Rundrohr 42,4 x 2,6 mit Gegenloechern; `check_verbinder_montage`, `check_walkways`, `check_huelle` gruen, `check_latte` in Kopie gelaufen, Viewer-Export beider Varianten im Browser angesehen.

### Plan
1. Werkstatt-Anteil: `link_t` 8 (D91), Montage-Arme ohne Probe-Rohr (`knoten_schere_arm_a/b_montage.sc`), Check `check_knoten_schere.py`.
2. Strebe als Rundrohr (`scripts/components/strebe.py`, `data/params.json` `strut_d`/`strut_wall`/`strut_end_offset`), Laenge Rohrmund bis Rohrmund, Gegenloecher.
3. Lage-Rechnung `scripts/knoten_montage.py` (Tabelle `knoten_schere.json` -> Modellrahmen), Einbau in `gen_dome.py` (`place_struts`, `knoten_anker`), Folie `foil_z0` auf das Rundrohr.
4. Pruefskript `scripts/check_verbinder_montage.py` (Instanzen, Nase im Gegenloch, Folie ueber Hardware, Probe-Durchdringung 4/5/6-wertig).
5. Bau A+ und Ring B2, `check_walkways`, `check_huelle`, `check_latte` in Kopie, Viewer-Export, Bilder, loop-state, Pfad-Commits.

### Stand (05.11.2026 abends)
**Gebaut:**
1. Werkstatt-Anteil: Laschen 8 mm (D91), Gegenloch D15 (bei 8 mm liess D13 der Nase 10 x 8 nur 0,1 mm Spiel), Montage-Arme `knoten_schere_arm_a/b_montage.sc` ohne Probe-Rohr. `python -X utf8 scripts/workshop/check_knoten_schere.py` 35/35 (Flaechenkontakt Lasche 1/2 im eigenen Arm unter 0,3 mm Facetten als Kontakt gewertet, gemessen 0,17/0,23 mm).
2. Strebe Rundrohr 42,4 x 2,6 mit 4 Gegenloechern (`scripts/components/strebe.py`): A 3077,1 mm (Rohrmund-Abstand in der Montage-Lage 3075,5 bis 3078,7, Mitte gebaut), B 3503,8 mm; `check_parts.py strebe_a strebe_b` je 22/22. Folie `foil_z0` 64 -> 40,2 mm (Rohrradius 21,2 + Schaumband 3 + Kanal 15 + 1); `check_huelle.py` 68/68.
3. Montage: `scripts/knoten_montage.py` (Tabelle -> Modellrahmen), `gen_dome.py` setzt 26 Plattenpaare, 60 Arme A, 68 Arme B (Basiskante der Tuer ohne Strebe) und 64 Streben mittig zwischen den Rohrmuendern. Kugelknoten `knoten_<n>_nNN.sc` nicht mehr im Modell.
4. A+ Runde 77: `sh scripts/build.sh 5 77` Exit 0 (11314 Befehle, 8:22 min). Ring B2 Runde 3: `sh scripts/build.sh 5 3 ring_b2` Exit 0 (11783 Befehle, 14:25 min).

**Gemessen (beide Varianten gleich):**
1. `python -X utf8 scripts/check_verbinder_montage.py [--variante ring_b2]` 14/14: Instanzen, Nase im Gegenloch (groesste Nasenecke 0,29 mm innerhalb des Lochrands), Folie ueber Hardware (39,3 < 40,2 mm, Koerper-Box-Ecken, konservativ), Probe n01/n02/n17 (6/5/4-wertig) ohne Durchdringung. Ausgaben `renders/check_verbinder_montage-77.txt`, `renders/ring_b2/check_verbinder_montage-03.txt`.
2. `check_walkways.py` beide Exit 0.
3. Viewer-Export A+ (273 Definitionen, 5353 Instanzen) und B2 (`--variante ring_b2`, 299 / 5570) im Browser angesehen: Kuppel-Struktur 229 Instanzen; Scheitelknoten zeigt Plattenpaar, 5 Scheren, Rundrohre; B2 mit Etikett und Ring.
4. Bilder: `renders/round-77.png`, `renders/verbinder-77-n02-aussen.png`, `renders/ring_b2/round-03.png`.
5. Masse Verbinder im Modell: 26 x 1083 g + 128 x 394 g = 78,6 kg (vorher Kugelknoten 155 kg).

**Befunde fuer den Orchestrator:**
1. 6-Loch-Platte an 5-wertigen Knoten (D91): A-Rohre muessten 3075,5 / 3076,3 / 3078,6 mm lang sein; gebaut eine Laenge 3077,1, Rest nimmt das Lochspiel D15 auf. Mit 5-Loch-Platte waeren alle A 3075,3.
2. Katalog `data/katalog.json` fuehrt noch `PRF-st-strebe30x30` und die Kugelknoten-Artikel; Stuecklisten-Kette (bom.py) auf Rundrohr und Scherenknoten umstellen.
3. `data/components/keilschiene.json` rechnet mit 120 mm Endversatz (node_clear 130); Scherenknoten: Rohrmund 102 mm.
4. `scripts/strut_cutting.py` hat `E_NOM = 120` fest.

## DoD
- R56 enthaelt alle sechs Abschnitte des Auftrags mit [A]/[E]/[Q]-Kennzeichnung.
- Prototyp: Check-Skript besteht (Koerper geschlossen, Nasen ragen durch die Wand, keine Durchdringung Lasche/Rohr ausser in den Wandloechern).
- Render optisch geprueft (Bild angesehen).
- Gepusht; Gesamtmodell unveraendert (`git diff --stat` ohne `gen_dome.py`, `dome.sc`).

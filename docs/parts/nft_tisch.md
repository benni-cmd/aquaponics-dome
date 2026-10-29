# Bauteilblatt T22 nft_tisch (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/nft_tisch.json` und `designs/components/nft_tisch.sc`, nicht von Hand aendern)

**Funktion:** Traegt n NFT-Rinnen mit 1,5 % Gefaelle (Zulauf hoch bei -X), verteilt Wasser ueber Zulaufverteiler und Schlaeuche (ein Schlauch je Rinne) und sammelt den Ablauf im Sammelrohr; Zickzack der Pflanzen durch Phase A/B benachbarter Rinnen (pitch/2). Rev. B (W16/D18): jede Reihe hat ihre eigene Rinnenlaenge (Zehneck-Seite minus 2 x corner_gap minus Ueberstaende), Verteiler und Sammelrohr laufen schraeg entlang der Sektorgrenze, die Beine stehen ausserhalb der Beete (Portalbock) bzw. ausserhalb des Pools (Auslegerbock innen).

**Datei:** `designs/components/nft_tisch.sc` · **Teilenummer:** T22 · **Revision:** B · **Bezugspunkt:** Mitte der Standflaeche (Z=0 Boden), X Laengsachse (Zulauf bei -X), Y quer

**Anzahl (Instanzen):** innen 10, Mitte 6, aussen 8 (Quelle: docs/scope-cards.md nft_tisch, data/layout.json hydro_tables)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `slope_pct` | 1.5 |  | R06 (docs/research/R06.md): Gefaelle laut zwei Quellen 1,3-3 % (Morgan 1:50-1:75, Greenhouse Management 1,2-3 %), nur FarmHub 1 % -> 1,5 % = 15 mm/m = 0,86 Grad; Durchfluss je Rinne 0,5 l/min (Port-Attribut) |
| `leg_w` | 40 | mm | [A] Portal-/Auslegerbein Rechteckrohr 40 x 40 x 3 (statt 30 x 30 x 2: Beine 1250 mm hoch ausserhalb der Beete, Auslegerlasten) |
| `leg_wall` | 3 | mm | [A] Wand Beine/Holm 3 mm |
| `holm_w` | 40 | mm | [A] Querholm Breite in X (Auflage der Rinnenhalter 40 mm) |
| `holm_h` | 60 | mm | [A] Querholm Hoehe 60 mm: Rechteckrohr 60 x 40 x 3 ueber ca. 1,2 m Spannweite (Portal) bzw. 0,6 m Kragarm (innen); Biegung 50 kg mittig 1,2 m = 150 Nm, W ca. 10 cm3 -> ca. 15 N/mm2 gegen S235 235 N/mm2 [E] |
| `holm_overhang` | 30 | mm | [A] Kragarm (nur innen) ragt 30 mm ueber die innerste Rinne hinaus; der Portalholm endet buendig an der Beinaussenseite |
| `bock_inset` | 250 | mm | [A] Abstand Bock zur Stirn der KUERZESTEN Reihe (250 mm) |
| `strut_z` | 800 | mm | [A] Querstrebe/Laengsstreben/Diagonalen UEBER den Pflanzen (Beet-Oberkante Z 475, Pflanzen bis ca. Z 560), Portal ausserhalb der Beete; innen Laengsstrebe auf Z 400 (Ausleger ausserhalb des Beckenrands) |
| `foot_plate` | 100 | mm | [A] Fussplatte 100 x 100 x 5, 2 Schrauben M8 (Beine tragen Kippmoment der Ausleger) |
| `foot_t` | 5 | mm | [A] |
| `foot_hole` | 9 | mm | [E] Durchgangsloch fuer M8 (ISO 273 mittel 9) |
| `clip_t` | 3 | mm | [A] Rinnenhalter aus 3-mm-Blech, 25 breit, 25 hoch |
| `clip_len` | 25 | mm | [A] |
| `hdr_od` | 25 | mm | [A] Zulaufverteiler d25 (entspricht etwa DN20), Wand 3 |
| `hdr_wall` | 3 | mm | [A] |
| `hose_od` | 20 | mm | [A] Schlauch ID 16 / AD 20 ueber Tuelle D16 und Verteilerstutzen |
| `hose_gap` | 70 | mm | [A] freier Abstand zwischen Tuelle und Verteilerstutzen |
| `col_od` | 50 | mm | [A] Sammelrohr d50 (Aussen 50, Wand 3; entspricht etwa DN40, Muffen d40/d32) |
| `col_wall` | 3 | mm | [A] |
| `corner_gap` | 100 | mm | [A] Vorgabe Orchestrator, docs/decisions.md D18: Abstand von der Zehneck-Ecke (Sektorgrenze) zum Rinnen-/Verteilerende je Seite; Abstand zwischen zwei Tischen 2 x corner_gap x cos 18 Grad = 190 mm |
| `leg_clearance` | 60 | mm | [A] Vorgabe Orchestrator, docs/decisions.md D18: Luft zwischen Beet-Aussenbreite (ibc_beet.json) und Fussplattenkante |

| Typ | n | rinnen_abstand | rinne | z_rinne_mitte | laenge | herkunft | ap_c | ap_c_herkunft |
|---|---|---|---|---|---|---|---|---|
| aussen | 3 | 288 | l | 1300 | 3124 / 2937 / 2750 (je Reihe) | layout.json hydro_tables r 4888/5176, Rinnen-Unterkante Z 1291-1325 (Mittel 1308, gerundet auf 1300 = -8 mm); 3 Rinnen: Ben (OBJ/Bild zeigen nur 2, oasis-obj-analysis) + A (3 nach Beetbreite) || Rinnenlaenge je Reihe = 2 x (ap x tan 18 Grad - corner_gap) - Ueberstaende 248 (D18); Tischmitte ap_c 5209 mm ([E]) | 5209 | [E] Mittel der Beetradien aussen (layout.json ibc_beds r 5167-5276): Tischmitte auf der Beetmitte; 3 Rinnen, OBJ-Reihen 4888/5176 (+ 3. Reihe A), Abweichung ca. 33 mm |
| mitte | 4 | 263 | m | 1300 | 1981 / 1810 / 1639 / 1468 (je Reihe) | layout.json hydro_tables r 2987-3775, Rinnen-Unterkante Z 1280-1330 (Mittel 1307, gerundet 1300 = -7 mm), Abstand 263 || Rinnenlaenge je Reihe = 2 x (ap x tan 18 Grad - corner_gap) - Ueberstaende 248 (D18); Tischmitte ap_c 3343 mm ([E]) | 3343 | [E] Mittel der Beetradien innen (layout.json ibc_beds r 3311-3408): Tischmitte liegt auf der Beetmitte; OBJ-Reihen ap 2987-3775 (Mittel 3381, Abweichung 38 mm) |
| innen | 2 | 262 | k | 840 | 848 / 678 (je Reihe) | layout.json hydro_tables r 1733/1995, Rinnen-Unterkante Z 819-858 (Mittel 838,5, gerundet 840 = +1,5 mm), Abstand 262 || Rinnenlaenge je Reihe = 2 x (ap x tan 18 Grad - corner_gap) - Ueberstaende 248 (D18); Tischmitte ap_c 1864 mm ([E]) | 1864 | [E] Mittel der OBJ-Reihen ap 1733/1995 (layout.json hydro_tables); Pool Wasserradius 1945 |

Gesamt-Box (Messung, Variante nft_tisch_aussen): X -1725.4 bis 1724.2, Y -656.5 bis 656.5, Z -25.0 bis 1423.5 mm; Koerper: 84.

**Toleranzen / Spiel:** Rinnenunterkante = Holm-/Kragarm-Oberkante an jedem Bock (Pruefung +-1 mm); Gefaelle 1,5 % +-0,05 %; Rinnenhoehe Z +-1,5 mm; Lochlage je Rinne +-1,5 mm zur Rechnung; Abstand zwischen benachbarten Tischen an der Ecke >= corner_gap (100 mm; gemessen 171-190 mm); Beine/Fussplatten >= 30 mm von jedem Beet-Rechteck (leg_clearance 60 mm sollwert). Gewichte: Summe je Koerper nach Werkstoff (Stahl 7,85, PVC 1,4 g/cm3; die Messung am .sc enthaelt auch die verknuepften Rinnen).

## Werkstoff und Gewicht

- Werkstoff: Stahl verzinkt (Boecke), PVC/PE (Rohre, Schlaeuche), Dichte 7.85 g/cm3, Farbe #aeb4b8 (ref-6: graue/verzinkte Beine mit Halterungen)
- Volumen (Messung, Variante nft_tisch_aussen, `solidcraft-cli eval`): 18799.6 cm3 · Masse leer: 71842 g (71.84 kg)
- Variante `nft_tisch_aussen`: 71.84 kg leer
- Variante `nft_tisch_mitte`: 58.52 kg leer
- Variante `nft_tisch_innen`: 15.10 kg leer
- Gefuellt/in Betrieb: Wasserfuellung der Rinnen (Film 10 mm, 1 l = 1 kg): aussen 3 x 4,0 = 12 kg, Mitte 4 x 2,5 = 10 kg, innen 2 x 1,6 = 3,2 kg [E]; Verteiler d25 und Sammelrohr d50 gefuellt je ca. 0,3-1,6 kg [E]

## Querschnitt / Profil

Mitte/aussen: Portalbock aus Rechteckrohr verzinkt: Beine 40x40x3, Querholm 40 x 60 x 3 (Hoehe 60) ueber die Beet-Aussenbreite, Querstrebe 40x40x3 auf Z 800 (ueber den Pflanzen), Diagonalen Flachstahl 25x3 gekreuzt, Fussplatten 100x100x5 mit 2 x M8. Innen: Auslegerbock: je Bock ein Pfosten 40x40x3 ausserhalb des Beckenrands, Kragarm 40 x 60 x 3 ueber das Wasser, Laengsstrebe auf Z 400 unter dem Kragarm. Rinnen: Instanzen nft_rinne_<typ>_r<k> (eigene Laenge je Reihe), Phase 0 / pitch/2 abwechselnd.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| aussen: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende, schraeg) | Rohr d25, Wand 3 (Anschluss Rohr/Schlauch) | x -1445, y 413, z 1392 (Achse laeuft schraeg: dx/dy = +tan 18 Grad, entlang der Sektorgrenze) | Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y, 18 Grad zur Y-Achse geneigt); Rohr d25 (etwa DN20) |
| aussen: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende, schraeg) | Rohr d50, Wand 3 (etwa DN40) | x 1432, y 413, z 1298 (Achse dx/dy = -tan 18 Grad) | Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal) |
| aussen: Verteiler-Stutzen je Rinne (n=3) | Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06) | x -1616, -1522, -1429 (Stutzenspitze je Reihe), y = Rinnenmitte, z ca. 1392 | aus Verteiler, Richtung +X |
| aussen: Fussplatten-Anker | M8, 2 Schrauben je Platte (100 x 100 x 5), Loch D9, Diagonalversatz +-35 | Fusspunkte z 5 an: x -1080 / y -606; x -1080 / y 606; x 1170 / y -606; x 1170 / y 606 | Befestigung auf dem Boden/Betonpunkt, Richtung -Z |
| mitte: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende, schraeg) | Rohr d25, Wand 3 (Anschluss Rohr/Schlauch) | x -804, y 520, z 1383 (Achse laeuft schraeg: dx/dy = +tan 18 Grad, entlang der Sektorgrenze) | Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y, 18 Grad zur Y-Achse geneigt); Rohr d25 (etwa DN20) |
| mitte: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende, schraeg) | Rohr d50, Wand 3 (etwa DN40) | x 791, y 520, z 1307 (Achse dx/dy = -tan 18 Grad) | Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal) |
| mitte: Verteiler-Stutzen je Rinne (n=4) | Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06) | x -1044, -959, -874, -788 (Stutzenspitze je Reihe), y = Rinnenmitte, z ca. 1383 | aus Verteiler, Richtung +X |
| mitte: Fussplatten-Anker | M8, 2 Schrauben je Platte (100 x 100 x 5), Loch D9, Diagonalversatz +-35 | Fusspunkte z 5 an: x -439 / y -576; x -439 / y 576; x 529 / y -576; x 529 / y 576 | Befestigung auf dem Boden/Betonpunkt, Richtung -Z |
| innen: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende, schraeg) | Rohr d25, Wand 3 (Anschluss Rohr/Schlauch) | x -409, y 256, z 916 (Achse laeuft schraeg: dx/dy = +tan 18 Grad, entlang der Sektorgrenze) | Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y, 18 Grad zur Y-Achse geneigt); Rohr d25 (etwa DN20) |
| innen: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende, schraeg) | Rohr d50, Wand 3 (etwa DN40) | x 396, y 256, z 854 (Achse dx/dy = -tan 18 Grad) | Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal) |
| innen: Verteiler-Stutzen je Rinne (n=2) | Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06) | x -478, -393 (Stutzenspitze je Reihe), y = Rinnenmitte, z ca. 916 | aus Verteiler, Richtung +X |
| innen: Fussplatten-Anker | M8, 2 Schrauben je Platte (100 x 100 x 5), Loch D9, Diagonalversatz +-35 | Fusspunkte z 5 an: x -44 / y -341; x 134 / y -341 | Befestigung auf dem Boden/Betonpunkt, Richtung -Z |

## Verbindungen und Befestigungen

- Beine an Fussplatte und Querholm/Kragarm: geschweisst (MAG), danach verzinkt [A]
- Fussplatten: 2 Schrauben M8x30 (hex_bolt) je Platte in den Boden/Betonpunkt, Loch D9; Kragarm-Pfosten innen mit Verbundankern (Kippmoment ca. 165 Nm, Statik nicht nachgewiesen)
- Diagonalen (nur Portal): je Ende Schraube M6x40 mit Mutter durch das Bein
- Rinnenhalter: L-Blech 3 mm, 25 x 25 x 25, je Rinnenseite und Bock, Schraube M5x12
- Verteiler: schraeges Rohr d25 mit Stutzen D16 (Verklebung/Schweissen), Schlaeuche ID 16 auf Tuelle und Stutzen; Sammelrohr d50 schraeg mit Muffen d40/d32 auf den Ablaufstutzen

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Rinnenlaenge je Reihe 678/848 (innen), 1468-1981 (Mitte), 2750-3124 (aussen) | je Reihe | E | Zehneck-Seite 2 x ap x tan 18 Grad (ap aus ap_c +- Reihenabstand) - 2 x corner_gap 100 - Ueberstaende 169 + 79 (Orchestrator D18, docs/jobs/W16-nft-tisch-passung.md); OBJ-Reihen nur als Beispiel | hoch |
| Rinnenlaenge 1304 / 1983 / 3232 (OBJ-Beispiel je Ring) | nur Beleg des Problems | OBJ | layout.json hydro_tables: groesser als die Zehneck-Seite der Reihen (innen -178/-8, Mitte -42, aussen -56), daher ersetzt (D18) | hoch |
| Beine ausserhalb der Beet-Aussenbreite (Portal): y = +-(bed_outer_w/2 + 60 + 50) | y +-606 (aussen), +-576 (Mitte) | E + A | bed_outer_w aus ibc_beet.json (993 / 933), leg_clearance 60 (D18), Fussplatte 100: Plattenkante 60 mm vom Beet | mittel |
| Auslegerbock innen: Pfosten bei ap = Pool-Aussenradius 2095 + 60 + 50 | ap 2205 | E + A | layout.json pool.d/2 1945 + params.json wall 150 (A) + leg_clearance + Fussplatte/2; Kragarm 40x60x3 ueber das Wasser, Statik nicht nachgewiesen | niedrig |
| Querholm/Kragarm Rechteckrohr 40 x 60 x 3, Beine 40x40x3 | 40x60x3; 40x40x3 | A + E | Biegung 50 kg mittig auf 1,2 m = 150 Nm, W ca. 10 cm3 -> ca. 15 N/mm2 gegen S235 235 N/mm2 | niedrig |
| Querstrebe/Laengsstreben/Diagonalen auf Z 800 (innen Z 400) | Z 800 | A | ueber den Pflanzen (Beet-Oberkante Z 475, Pflanzen bis ca. 560); Portal steht ausserhalb der Beete | niedrig |
| Verteiler und Sammelrohr schraeg entlang der Sektorgrenze (18 Grad) | dx/dy = +-tan 18 | E | jede Reihe hat anderen Abstand zur Ecke; schraeges Rohr haelt Ueberstand und corner_gap fuer alle Reihen gleich | mittel |
| Rinnenmitte um +45 mm nach +X versetzt | +45 mm | E | (Ueberstand Zulaufseite 169 - Ablaufseite 79)/2 | hoch |
| Lochraster je Reihe mit Phase 0 / pitch/2, n = floor(L/250) | Phase 0 / 125 | Bild + E | ref-6 Zickzack; Versatz je Reihe aus hole_plan() (tisch_geom.py), Loecher >= 46 mm vom Rinnenende | mittel |
| Tischmitte auf der Beetmitte: ap_c aussen 5209, Mitte 3343, innen 1864 | mm | E + A | Mittel der Beetradien (ibc_beds r) bzw. Mittel der OBJ-Reihen innen; Abweichung zum OBJ 33-38 mm | mittel |
| Tischzahl je Sektor: innen 10, Mitte 6 (Sektoren 0-2, 7-9), aussen 8 (0-3, 6-9) | 24 | OBJ | Beet-Azimute in layout.json ibc_beds (5,3 + 36 Grad x i) | mittel |
| Rinnenzahl 2 / 4 / 3 | 2/4/3 | OBJ + Ben + A | layout.json hydro_tables (2 innen, 4 Mitte, 2 aussen im OBJ/Bild); aussen 3: Ben (Bild/OBJ zeigen nur 2, oasis-obj-analysis) + A Anzahl nach Beetbreite 933-993 | mittel |
| Rinnenabstand 262 / 263 / 288 | 262 / 263 / 288 mm | OBJ | layout.json hydro_tables (Abstand der Rinnen) | hoch |
| Hoehe Rinnenunterkante (Boden) bei x=0: Z 840 / 1300 / 1300 | 840 / 1300 / 1300 | OBJ | layout.json hydro_tables Z (Unterkanten 819-858, 1280-1330, 1291-1325), Mittel 838,5 / 1307 / 1308 gerundet (Abweichung <= 8 mm) | mittel |
| Zickzack Versatz pitch/2 = 125 | 125 mm | Bild | ref-6 mittlerer Tisch (zwei versetzte Reihen zwischen Nachbarrinnen); Scope-Card nft_tisch | hoch |
| Gefaelle 1,5 % (0,86 Grad) | 1,5 % (0,86 Grad) | R06 | docs/research/R06.md: 1,3-3 % (Morgan, Greenhouse Mgmt), FarmHub 1 % | mittel |
| Gekreuzte Diagonalen Flachstahl 25x3 | 2 je Bock | Bild + A | ref-6: schraege Stuetzen an den Beinen; Scope-Card verlangt Diagonalen | mittel |
| Rinnenhalter L-Blech 25x25x3, M5 | 25x25x25 x 3 mm, M5x12 | Bild + A | ref-6: kleine Befestigungspunkte an der Rinnenseitenwand (Bild-Kritiker B3) | niedrig |
| Zulaufverteiler d25 mit n Stutzen, Schlauch ID 16 / AD 20 (hellblau) | d25; Schlauch ID16/AD20 | Bild + A | ref-6: hellblaue Schlaeuche am Tischende, ein Schlauch je Rinne; Masse A | mittel |
| Sammelrohr d50 mit Muffen | d50, Muffen d40/d32 | A | Scope-Card: Sammelablauf; Mass A (keine Quelle) | niedrig |
| Durchfluss je Rinne 0,5 l/min | 0,5 l/min je Rinne | R06 | docs/research/R06.md | mittel |
| Anzahl Tische 10 / 6 / 8 | 10 / 6 / 8 | OBJ + Ben | components.md NFT-Ringe (Sektoren je Ring) | mittel |
| Diagonalenschrauben M6x40 mit Mutter | M6x40 | A | SolidCraft parts.insert hex_bolt/hex_nut M6 | mittel |
| Fussplatten 100x100x5, M8 | 100x100x5 | A | Kippmoment der Ausleger und Plattenkante-Abstand 60 mm zum Beet | niedrig |
| Zulaufverteiler: Achse auf Hoehe der Tuellenachse (+70 mm), freier Schlauchabschnitt 70 mm (hose_gap) | 70 / 70 | E + A | Rinne: Tuelle z 70 (nft_rinne.json); hose_gap Annahme | niedrig |
| Sammelrohr: Achse auf Hoehe der Ablaufachse der Rinne (+20 mm ueber dem tiefen Rinnenende) | 20 | E | Rinne: Ablaufstutzen z 20 (nft_rinne.json) | mittel |
| Laengsdiagonalen 25x3 je Beinseite zwischen den Boecken | 1 / 2 je Tisch | A | Bild-Kritiker W16: Gestell in Laengsrichtung weich, nur unterer Laengsriegel | niedrig |
| Zwei Boecke je Tisch (4 Beine Portal, 2 Pfosten innen), Abstand zur Stirn der kuerzesten Reihe 250 | 2 Boecke | A | docs/scope-cards.md nft_tisch (4 Beine mit Querstreben, Diagonalen); innen 2 Pfosten wegen Pool (D18) | mittel |
| corner_gap 100 mm je Seite der Sektorgrenze | 100 mm (Abstand zwischen zwei Tischen 190 mm) | A | Vorgabe des Orchestrators, docs/decisions.md D18 (Auftrag W16); Abstand = 2 x 100 x cos 18 Grad | mittel |
| leg_clearance 60 mm zwischen Beet-Aussenbreite und Fussplattenkante | 60 mm | A | Vorgabe des Orchestrators, docs/decisions.md D18; Beet-Aussenbreite aus ibc_beet.json | mittel |
| Beckenrand Z 650: Kragarm liegt 130 mm darueber (Unterkante 780) | Z 650 | Ben | data/params.json pool_rim (Ben: Rand ca. Z 650, am Bild ref-4 zu pruefen); Kragarm-Unterkante = Rinnenhoehe 840 - holm_h | mittel |
| Durchgangsloch D9 in der Fussplatte fuer M8 | D9 | E | ISO 273 mittel fuer M8 (9 mm) | hoch |
| Kragarm-Ueberstand 30 mm ueber die innerste Rinne (nur innen) | 30 mm | A | Konstruktionspraxis; Portalholm endet buendig an der Beinaussenseite (kein Ueberstand) | niedrig |
| Tisch-KS und Platzierung: X tangential CCW, Y radial nach innen, yaw = Azimut + 90 Grad (volle 360 Grad) | yaw az + 90 | E | Y = Z x X bei dieser Drehung; layout.json hydro_tables speichert yaw nur modulo 180 (aussen Sektor 3, 6-9 und Mitte/innen 7-9 haben dort az - 90): wer den OBJ-Wert woertlich nimmt, setzt den Tisch um 180 Grad gedreht | hoch |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg (Tisch: Platte aus Rinnen auf Boecken, Schlaeuche am Tischende hellblau); reference/ref-4 und ref-5 (Ringanordnung)
- Quelle der Masse: data/layout.json hydro_tables, ibc_beds, pool; Rinnenlaenge je Reihe aus der Zehneck-Seite (D18, docs/jobs/W16-nft-tisch-passung.md); Beetbreite aus data/components/ibc_beet.json
- Abweichung zum OBJ: layout.json hydro_tables liefert je Ring nur ein Beispiel (Reihen ap 1733/1995 innen, 2987-3775 Mitte, 4888/5176 aussen) mit gleicher Rinnenlaenge 1304/1983/3232; diese Laengen sind groesser als die Zehneck-Seite 2 x ap x tan 18 Grad der Reihe (innen 1126/1296, Mitte 1916-2429, aussen 3198-3572) und kollidierten an den Ecken (Ben-Fund 29.10.). Rev. B folgt D18: Rinnenlaenge je Reihe = Zehneck-Seite - 2 x corner_gap (100) - Ueberstaende (Zulaufseite 169, Ablaufseite 79); Ergebnis innen 678/848, Mitte 1468/1639/1810/1981, aussen 2750/2937/3124 mm. Folge: Topfloecher je Tisch innen 5 statt 10, Mitte 24 statt 28, aussen 34 statt 36; gesamt 466 statt 556 (check_nft_fit.py). Tischmitte liegt auf der Beetmitte (Mittel der Beetradien: aussen 5209, innen-Beet 3343) und weicht von den OBJ-Reihen um 33-38 mm ab (Annahme A, Layout/Integrator). Die Tisch-Beine des OBJ stehen nicht im Layout (Platten ohne Beine). Die Z-Hoehen bleiben (innen 840, Mitte/aussen 1300). Ausrichtung: X tangential gegen den Uhrzeigersinn (+X Sammelrohr/tiefes Ende), Y radial nach INNEN; die Instanz wird mit yaw = Azimut + 90 Grad (volle 360 Grad; layout.json hydro_tables speichert yaw nur modulo 180: aussen Sektoren 3 und 6-9 sowie Mitte/innen 7-9 haben dort az - 90, den Tisch dann um 180 Grad gedreht setzen) auf die Sektorachse bei ap_c gesetzt, aussen liegt dann -Y. Mit yaw = Azimut - 90 Grad waere die Konvention gespiegelt (Fehler des ersten Kritiker-Bildes, W16).

## Montage (L4)

1. Bock am Boden ausrichten: Portal ausserhalb der Beete bzw. Pfosten ausserhalb des Pools, Fussplatten mit M8 / Verbundankern verschrauben
2. Querstrebe und Laengsstreben einsetzen, Diagonalen verschrauben (Portal)
3. Rinnen auf die Querholme/Kragarme legen (Zulaufende hoeher), Halteclips M5 setzen
4. Zulaufverteiler schraeg entlang der Sektorgrenze haengen, Schlaeuche ID 16 auf Stutzen und Tuellen
5. Sammelrohr mit Muffen auf die Ablaufstutzen stecken, Gefaelle kontrollieren (1,5 %)

**Werkzeug:** Wasserwaage/Gefaellelatte, Akkuschrauber, Schluessel M5/M6/M8, Bohrmaschine, Schweissgeraet (oder Winkelverbinder)

## Stueckliste-Zeile

- Pro Tisch je Typ (Laengen in mm):
-   aussen: Beine 4 x 40x40x3: Laenge 1252 / 1218, Beinabstand y 1213; Querholm 40x60x3 x 2: Laenge 1253; Querstrebe 40x40x3 x 2: Laenge 1173; Laengsstreben 40x40x3 x 2: Laenge 2210; Diagonalen 25x3 x 4; Laengsdiagonalen 25x3 x 2; Fussplatten 100x100x5 x 4
-      Rinnen (3): 3124 mm / 12 Loecher, 2937 mm / 11 Loecher, 2750 mm / 11 Loecher; Verteiler d25 schraeg: Laenge 869; Sammelrohr d50 schraeg: Laenge 869
-   mitte: Beine 4 x 40x40x3: Laenge 1242 / 1228, Beinabstand y 1153; Querholm 40x60x3 x 2: Laenge 1193; Querstrebe 40x40x3 x 2: Laenge 1113; Laengsstreben 40x40x3 x 2: Laenge 928; Diagonalen 25x3 x 4; Laengsdiagonalen 25x3 x 2; Fussplatten 100x100x5 x 4
-      Rinnen (4): 1981 mm / 7 Loecher, 1810 mm / 6 Loecher, 1639 mm / 6 Loecher, 1468 mm / 5 Loecher; Verteiler d25 schraeg: Laenge 1092; Sammelrohr d50 schraeg: Laenge 1092
-   innen: Pfosten 2 x 40x40x3: Laenge 776 / 774; Kragarm 40x60x3 x 2: Laenge 587; Laengsstrebe 40x40x3 x 1: Laenge 138 (Z 400); Laengsdiagonale 25x3 x 1; Fussplatten 100x100x5 x 2
-      Rinnen (2): 848 mm / 3 Loecher, 678 mm / 2 Loecher; Verteiler d25 schraeg: Laenge 538; Sammelrohr d50 schraeg: Laenge 538
- Je Bock (Portal): 2 Beine, 1 Holm, 1 Querstrebe, 2 Diagonalen, 2 Fussplatten, 4 Schrauben M8x30, 4 Schrauben M6x40 + 4 Muttern M6, 2 Rinnenhalter je Rinne mit Schraube M5x12; Bock-Anzahl 2 je Tisch. Je Bock (Ausleger): 1 Pfosten, 1 Kragarm, 1 Fussplatte, 2 Schrauben M8x30, 2 Rinnenhalter je Rinne.
- Dabei: 4 Duebel/Anker M8 je Bock (Boden; innen Verbundanker), je 1 Endstopfen d25 und d50 je Tisch (-Y-Rohrende)

## Alternative lokale Fertigung

Rahmen aus Baustahl-Rechteckrohr (Metallbauer, Kaltverzinken) oder Aluprofil-Systemprofil mit Winkelverbindern; Rinnenhalter aus Streifen 25x3 selbst gebogen.

## Renders

- `renders/components/nft_tisch_aussen/nft_tisch_aussen-01-iso.png`
- `renders/components/nft_tisch_aussen/nft_tisch_aussen-02-zulauf.png`
- `renders/components/nft_tisch_aussen/nft_tisch_aussen-03-bock.png`
- `renders/components/nft_tisch_aussen/nft_tisch_aussen-04-ablauf.png`
- `renders/components/nft_tisch_aussen/nft_tisch_aussen-05-oberseite.png`
- `renders/components/nft_tisch_aussen/nft_tisch_aussen-06-querschnitt-bock.png`
- `renders/components/nft_tisch_innen/nft_tisch_innen-01-iso.png`
- `renders/components/nft_tisch_innen/nft_tisch_innen-02-zulauf.png`
- `renders/components/nft_tisch_innen/nft_tisch_innen-03-bock.png`
- `renders/components/nft_tisch_innen/nft_tisch_innen-04-ablauf.png`
- `renders/components/nft_tisch_innen/nft_tisch_innen-05-oberseite.png`
- `renders/components/nft_tisch_innen/nft_tisch_innen-06-querschnitt-bock.png`
- `renders/components/nft_tisch_mitte/nft_tisch_mitte-01-iso.png`
- `renders/components/nft_tisch_mitte/nft_tisch_mitte-02-zulauf.png`
- `renders/components/nft_tisch_mitte/nft_tisch_mitte-03-bock.png`
- `renders/components/nft_tisch_mitte/nft_tisch_mitte-04-ablauf.png`
- `renders/components/nft_tisch_mitte/nft_tisch_mitte-05-oberseite.png`
- `renders/components/nft_tisch_mitte/nft_tisch_mitte-06-querschnitt-bock.png`

## Pruefung

- Gauntlet-Urteil: offen
- scripts/workshop/check_nft_tisch.py (124/124 PASS, Ergebnis renders/components/nft_tisch_innen/check.txt): Rinnenzahl, Abstand, Laenge je Reihe, Lochlage, Zickzack pitch/2, Gefaelle, Hoehe, Auflage, Boecke, Beinlage, Verteiler/Sammelrohr an der Sektorgrenze
- scripts/workshop/check_nft_fit.py (36/36 PASS, Ergebnis renders/components/nft_tisch_innen/check_fit.txt): reine Geometrie fuer alle 24 Tische: Rinne + Ueberstaende + 2 x corner_gap <= Zehneck-Seite, Footprint-Abstand benachbarter Tische >= 100 (gemessen 171-190), Beine >= 30 mm ausserhalb jedes Beet-Rechtecks, Pfosten ausserhalb des Pools
- Bild-Kritiker (Ecke Draufsicht/Iso, Querschnitt Bock + Beet, Innen/Aussen) und Spec-Pruefer: Runden siehe docs/workshop-log.md (W16)

## Offene Fragen

- Statik der Portal-/Auslegerboecke nicht nachgewiesen (Querholm 40x60x3 ueber ca. 1,2 m: Biegung 50 kg mittig ca. 150 Nm, ca. 15 N/mm2 [E]; Kragarm innen ca. 165 Nm am Pfosten, Fussplatte/Verbundanker nachzurechnen)
- Tischmitte = Beetmitte ist Annahme (OBJ-Reihen weichen um 33-38 mm ab); die Instanz-Platzierung gehoert dem Integrator (yaw = Azimut + 90 Grad in vollen 360 Grad, OBJ-yaw nur modulo 180; Y radial INNEN)
- Rinnenlaenge je Reihe ist die Folge von D18; weniger Topfloecher (466 statt 556) beim Orchestrator/Ben bestaetigen
- Aufhaengung des Verteilers an den Boecken (Rohrschellen) nicht modelliert; Verteiler/Sammelrohr laufen frei schraeg
- aussen 3 Rinnen (OBJ 2) bleibt Annahme; die aeusserste (3.) Reihe liegt auf ap 5497 (Beetmitte 5209 + 288), die inneren auf 5209 und 4921
- Beine ausserhalb der Beete stehen im Gehweg: Durchgangsbreite zwischen den Beeten und Tischen vom Integrator zu pruefen (Beinabstand y aussen 1213, Mitte 1153)
- Rinnenabstand 262-288 (OBJ) bei Rinnenbreite 130 laesst 132-158 mm Luecken; ref-6 zeigt fast buendige Rinnen: Widerspruch OBJ/Bild, OBJ gilt (provenance)
- Schlaeuche gerade statt gebogen; Kopfplatten/Winkelhalter an den Beinkoepfen (W11) nicht modelliert
- Innen: Pfosten stehen ausserhalb des Beckenrands (Wasserradius 1945 + Wand 150 + 60 + 50); der Kragarm ueberspannt Rand Z 650 mit 130 mm Luft; ein Stuetzwinkel am Pfosten ist wegen der Beckenwand nicht moeglich (Annahme A)
- Gefaelle: detail-standard.md und Scope-Card nennen noch 1 cm/m, gebaut 1,5 % nach R06 (Orchestrator-Vorgabe)

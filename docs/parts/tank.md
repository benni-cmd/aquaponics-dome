# Bauteilblatt T40 tank (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/tank.json` und `designs/components/tank.sc`, nicht von Hand aendern)

**Funktion:** Tank mit Kegelboden: klein = Vortex-Absetzer (tangentialer Zulauf, Leitrohr, Schlamm sinkt zur Spitze und wird dort abgelassen), gross = Biofilter (Schwebebett aus losen K1-Traegern mit Belueftungsgitter am Konus, Rueckhaltesieben, Ueberlauf, Schlammablass; W32/D55); steht auf Plattform und 4 Beinen.

**Datei:** `designs/components/tank.sc` · **Teilenummer:** T40 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche am Boden, Z=0 (Boden); Tankachse = Z; Hoehen wie im OBJ (Kegelspitze, Plattform); Zulauf tangential bei +X/-Y, Auslauf am Leitrohr +X

**Anzahl (Instanzen):** klein 2, gross 2 (Quelle: data/layout.json tanks)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `foot_plate` | 100 | mm | [A] Fussplatte 100 x 100 x 6 (Tank gross: bei leg_w 40) |
| `foot_t` | 6 | mm | [A] |
| `foot_hole` | 9 | mm | [E] Durchgangsloch fuer M8 |
| `cone_clear` | 2 | mm | [A] Spiel zwischen Tankkegel und Plattform-Kegelsitz |
| `lid_t` | 6 | mm | [A] Deckel |
| `lid_over` | 0 | mm | [A] Deckel buendig mit dem Randwulst (Bild-Kritiker: Wulst sichtbar lassen) |
| `guide_d` | 110 | mm | [A] Leitrohr (Mittelrohr) D110, Wand 3 (OSE Vortex Biofilter: Leitrohr) |
| `guide_wall` | 3 | mm | [A] |
| `guide_depth` | 420 | mm | [A] Leitrohr reicht 420 mm unter den Deckel |
| `outlet_d` | 50 | mm | [A] Auslauf am Leitrohr d50 (Rohr 50, Wand 3) |
| `pipe_wall` | 3 | mm | [A] Rohrwand Zulauf/Auslauf |
| `inlet_below_top` | 250 | mm | [A] Zulauf tangential 250 mm unter dem Tankrand |
| `valve_len` | 40 | mm | [A] Kugelhahn Baulaenge 40 (OBJ-Fittings Z 143-177 nur 34 mm Bandbreite: Verschraubungen) |
| `air_d` | 16 | mm | [A] Belueftungsanschluss im Deckel (Biofilter) |
| `diag_w` | 25 | mm | [A] Diagonale Flachstahl 25 x 3 |
| `rim_w` | 25 | mm | Bild: ref-5 dicker gerollter Randwulst; 25 mm nach aussen, Aussenmass D laut OBJ inkl. Wulst [A] |
| `rim_h` | 40 | mm | Bild: ref-5 dicker gerollter Randwulst (Bild-Kritiker Luecke 2: Wulst zu schmal); 40 mm hoch [A] |
| `rev_d` | 200 | mm | [A] Revisionsoeffnung im Deckel D200 (Scope-Card: Deckel/Oeffnung; Bild-Kritiker Luecke 5) |
| `outlet_below_top` | 100 | mm | R09 (Auslass oben seitlich, 100 mm unter dem Rand) [A, Konfidenz niedrig]; fuer klein und gross |
| `guide_bottom_f` | 0.333 |  | R09: Leitrohr endet ca. 1/3 der Zylinderhoehe ueber der Kegelspitze (Zylinderhoehe = Rand minus Kegelende) [A] |
| `rib_z0` | 249 | mm | OBJ: Kassetten/Rippen z0 249-256 (layout.json tanks[].modules) |
| `rib_r_out` | 367 | mm | W30: Innenkante der Querstreben (Plattformhalbbreite - leg_w = 370.5) minus 3 mm Spiel, damit die Rippe die Querstreben nicht durchdringt (OBJ: Rippen bis r 468, vor W30 440) [A] |
| `rib_t` | 44 | mm | OBJ: Dicke 43-44 mm (Kantholz-/Bohlenstaerke 44) [A Werkstoff Fichte] |
| `rib_gap` | 3 | mm | [A] Abstand der Rippenschraege zum Tankkegel |
| `plat_margin` | 60 | mm | Ben 31.10./D50: Rand der Plattform um den Konus 60 mm je Seite; Plattform aus dem Konusdurchmesser auf Plattform-Unterkante berechnet (fix_w30_tank.py), nicht hart |
| `tafel_gap` | 30 | mm | [A] W30: Pumpentafel steht seitlich am Stand, Abstand von der Aussenkante der Diagonalen/Querstreben 30 mm; Platzierung Montage |
| `fill` | 0.67 |  | [Q] D55/W32, R30: lose K1-Traeger mit 67 % Fuellung der Wasserfuellung (Schuettvolumen / Wasservolumen) |
| `water_l` | 702 |  | [Q] R30 / system_specs: Wasserfuellung je grossem Tank 702 l (1,404 m3 beide). Das Modell fasst bis zum Rand 687 l und bis zum Ueberlauf-Mittelpunkt 627 l (Rechnung aus dem Tankprofil, check_tank): Abweichung offen |
| `k1_area` | 500 |  | [Q] R30: K1-Traegerflaeche ca. 500 m2/m3 Schuettvolumen (Odegaard 2006 / WST 2009, Suchzusammenfassung, Datenblatt nicht gelesen) |
| `carrier_d` | 9 | mm | [A] K1-Traeger Durchmesser ca. 9 mm (Kaldnes-Typ, Handbuchwert), Hoehe ca. 7 mm; nicht einzeln modelliert |
| `screen_slot` | 5 | mm | [A] Schlitzweite der Rueckhaltesiebe 5 mm < Traegerdurchmesser 9 mm; Schlitze nicht modelliert |
| `air_ring_d` | 20 | mm | [A] Belueftungsring und Kreuzarme: PVC-Rohr D20 mit Ausstroemerbohrungen (nicht modelliert), speist ueber das Steigrohr D16 |
| `ring_clear` | 25 | mm | [A] Luft zwischen Belueftungsring und Innenwand des Konus |
| `bed_inset` | 3 | mm | [A] Das Schwebebett-Volumen endet 3 mm vor der Innenwand (Modellspalt) |
| `screen_d` | 110 | mm | [A] Auslaufsieb (Kappe ueber dem Ueberlauf) D110, Wand 2 |
| `screen_l` | 70 | mm | [A] Laenge der Siebkappe |

| Typ | R | H | z0 | plat_l | plat_w | plat_t | plat_z0 | leg_w | leg_h | leg_wall | wall | rt | strut_z | valve_d | inlet_d | anzahl | biofilter | herkunft | layout_anzahl | plat_l_obj | plat_w_obj | plat_herkunft | rib_phase |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| klein | 336.5 | 1075 | 172 | 619 | 619 | 73 | 428 | 30 | 751 | 2 | 4 | 22 | 250 | 40 | 50 | 2 | 0 | layout.json tanks 1 und 4: D673, H1075, Spitze Z 167-172, Plattform 706x707x73 auf Z 424-428, Beine 4 x h751, Fittings 30-40 an der Spitze | 2 | 706 | 707 | W30/D50: 2 x (Konusradius 247.3 auf Z 428 + Kegelsitz-Spiel 2 + Rand 60) = 619 (OBJ 706 x 707); Plattformdicke und Z unveraendert, Tank unveraendert |  |
| gross | 465 | 1444 | 226 | 821 | 821 | 98 | 570 | 40 | 1008 | 2.5 | 5 | 28 | 300 | 50 | 63 | 1 | 1 | layout.json tanks 2 und 3: D930, H1441-1444, Spitze Z 226-229, Plattform 977x976x98 auf Z 570-572, Beine 4 x h1006-1008, Fittings 41-56 an der Spitze; Hahn d50 (Norm) statt OBJ-Fitting 55 [A]; Stuetzrippen: layout.json tanks 2/3 modules 384 x 44 x 419 (Orchestrator-Entscheidung 29.10.: Rippen/Konsolen der Plattform, Klasse Tank) | 2 | 977 | 976 | W30/D50: 2 x (Konusradius 348.7 auf Z 570 + Kegelsitz-Spiel 2 + Rand 60) = 821 (OBJ 977 x 976); Plattformdicke und Z unveraendert, Tank unveraendert | 11.0 |
| gross_t3 | 465 | 1444 | 226 | 821 | 821 | 98 | 570 | 40 | 1008 | 2.5 | 5 | 28 | 300 | 50 | 63 | 1 | 1 | Tank 3 (Azimut 107,8): wie gross, Rippenmuster um 42,6 Grad gedreht (Rippenwinkel relativ zur Plattformdrehung 53,6 statt 11,0 Grad) | 2 | 977 | 976 | W30/D50: 2 x (Konusradius 348.7 auf Z 570 + Kegelsitz-Spiel 2 + Rand 60) = 821 (OBJ 977 x 976); Plattformdicke und Z unveraendert, Tank unveraendert | 53.6 |

Gesamt-Box (Messung, Variante tank_klein): X -344.5 bis 441.5, Y -351.2 bis 344.5, Z -24.0 bis 1323.0 mm; Koerper: 33.

- Box (Messung) klein: X -388 bis 442, Y -388 bis 388, Z -24 (Schraubenenden 24 mm im Boden) bis 1323
- Box (Messung) gross: X -518 bis 570, Y -518 bis 518, Z -24 (Schraubenenden 24 mm im Boden) bis 1750
- Box (Messung) gross_t3 (Tank 3, Rippenmuster gedreht): X -518 bis 570, Y -518 bis 518, Z -24 bis 1750
**Toleranzen / Spiel:** Kegelsitz in der Plattform 2 mm Spiel; Zulaufrohr beruehrt die Innenwand tangential (+-0,5 mm); Tankhoehe und Kegelspitze +-1 mm gegen layout.json im Bauteil; Instanzen: layout.json hat je Tank eine eigene Spitze (klein 167-172, gross 226-229): der Integrator setzt z so, dass die Spitze stimmt (Versatz bis 5 mm gegenueber dem Bauteil, z. B. Tank 4: -5 mm), die Plattform liegt je Tank 424-428 bzw. 570-572.

## Werkstoff und Gewicht

- Werkstoff: PE (Tank), Stahl verzinkt (Plattform, Beine), PVC (Rohre, Ventil), Dichte 0.95 g/cm3, Farbe #9db89c (ref-4/ref-5: gruene Kunststofftanks mit Randwulst; PE-Dichte 0,95 g/cm3 Handbuchwert; Stahl 7,85; PVC-U 1,4)
- Volumen (Messung, Variante tank_klein, `solidcraft-cli eval`): 15923.5 cm3 · Masse leer (ohne Biomedium): 37237 g (37.24 kg)
- Variante `tank_klein`: 37.24 kg leer (ohne Biomedium)
- Variante `tank_gross`: 73.67 kg leer (ohne Biomedium)
- Variante `tank_gross_t3`: 73.67 kg leer (ohne Biomedium)
- Gefuellt/in Betrieb: klein: leer 46 kg; Wasserfuellung bis Rand 254 l = 254 kg (Zylinder 222 l + Kegel 33 l; Wasserfuellung gehoert zu DRAUSSEN, nur Gewichtsangabe) [E]; gefuellt gesamt 300 kg | gross: leer 103 kg, Biomedium (K1-Schuettung 470 l x 0,15 g/cm3) 71 kg; Wasserfuellung bis Rand 683 l = 683 kg (Zylinder 596 l + Kegel 88 l; Wasserfuellung gehoert zu DRAUSSEN, nur Gewichtsangabe) [E]; gefuellt gesamt ca. 857 kg (ohne Abzug des Traegervolumens)

## Querschnitt / Profil

Tank PE: Zylinder ueber Kegel, gerollter Randwulst 25 x 40 mm, Wand 4/5 mm, Deckel 6 mm buendig mit dem Wulst, Revisionsoeffnung D200. Geometrie je Tank: klein: Kegel 48.7 Grad ab Horizontal (Spitze Z 172, Ende Z 501), Koerperradius 311.5 (D623) plus Randwulst 25 = Aussen-D673 | gross: Kegel 47.0 Grad ab Horizontal (Spitze Z 226, Ende Z 668), Koerperradius 440.0 (D880) plus Randwulst 25 = Aussen-D930. Plattform: Blechkasten 4 mm, innen hohl, Kegelsitz 2 mm Spiel, Eckenaussparungen fuer die Beine; Beine Rechteckrohr verzinkt; vier Querstreben auf Hoehe 250/300 und vier Diagonalen (an den Beinkanten gekuerzt).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| klein: Zulauf tangential (Rohr d50, DN40) | PVC-U d50 nach DIN 8062 (DN40), Wand 3 | x 282.5, y -351, z 997 (Rohrachse parallel Y, Rohrende aussen) | Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall) |
| klein: Auslauf (Auslaufrohr vom Leitrohr durch die Tankwand) | PVC-U d50 (DN40) | x 442, y 0, z 1147 (100 mm unter dem Rand, R09) | Wasser verlaesst den Absetzer nach +X (Oeffnung zeigt +X) |
| klein: Schlammablass (Kugelhahn an der Kegelspitze) | PVC-U d40 (DN30), Kugelhahn mit Verschraubung | x 0, y 0, z 80 (Stutzenende); Kegelspitze z 172 | Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X |
| klein: Fussplatten-Anker (4 Fuesse, je 2 x M8) | Schrauben M8x30 ISO 4017, Loch D9, Platte 100 x 100 x 6; im Boden Duebel/Betonpunkt M8 | x +-294, y +-294, z 6 (Diagonalversatz +-35); Schraubenenden z -24 | Befestigung auf Boden/Betonpunkt, Richtung -Z |
| gross: Zulauf tangential (Rohr d63, DN50) | PVC-U d63 nach DIN 8062 (DN50), Wand 3 | x 403.5, y -395, z 1420 (Rohrachse parallel Y, Rohrende aussen) | Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall) |
| gross: Ueberlauf (Auslauf) | PVC-U d63 (DN50) | x 570, y 0, z 1570 (100 mm unter dem Rand, R09) | Wasser verlaesst den Biofilter nach +X (Oeffnung zeigt +X) |
| gross: Belueftungsanschluss im Deckel | Rohr d16 (Luftschlauch 16 mm, etwa DN10) | x 220, y 0, z 1676 | Luft tritt ein, Oeffnung zeigt +Z |
| gross: Schlammablass (Kugelhahn an der Kegelspitze) | PVC-U d50 (DN40), Kugelhahn mit Verschraubung | x 0, y 0, z 134 (Stutzenende); Kegelspitze z 226 | Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X |
| gross: Fussplatten-Anker (4 Fuesse, je 2 x M8) | Schrauben M8x30 ISO 4017, Loch D9, Platte 100 x 100 x 6; im Boden Duebel/Betonpunkt M8 | x +-390, y +-390, z 6 (Diagonalversatz +-35); Schraubenenden z -24 | Befestigung auf Boden/Betonpunkt, Richtung -Z |

## Verbindungen und Befestigungen

- Tank sitzt mit dem Kegel im Kegelsitz der Plattform (Kegel-Zylinder-Uebergang auf der Plattform-Oberkante), Haltegurt/Schellen nicht modelliert [A]
- Beine laufen durch Eckenaussparungen der Plattform, geschweisst (MAG), danach verzinkt [A]
- Fussplatten: je 2 Schrauben M8x30 ISO 4017 mit Duebel M8 im Boden/Betonpunkt, Loch D9
- Rohre PVC-U nach DIN 8062/EN 1452 mit Bulkhead-Durchfuehrung und Dichtung durch die Tankwand [A, im Modell nur Durchbruch + Rohr]
- Schlammventil: Kugelhahn PVC-U mit Verschraubung an Stutzen d40/d50
- Schwebebett (gross): lose K1-Traeger (ca. D9 x 7 mm) frei im Tank, zurueckgehalten durch das Zulaufsieb (Schlitzkappe auf dem Zulaufrohr, 5 mm) und die Siebkappe D110 am Ueberlauf (Schlitz 5 mm); Belueftungsgitter D20 (Ring + 2 Kreuzarme) am Konus, gespeist ueber das Steigrohr D16 [A]

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Tankdurchmesser 673 / 930 (inkl. Randwulst) | 673 / 930 mm | OBJ | layout.json tanks d (Tank 1/4 und 2/3) | hoch |
| Tankhoehe 1075 / 1444 (inkl. Kegel) | 1075 / 1444 mm | OBJ | layout.json tanks h | hoch |
| Kegelspitze Z 172 / 226 | 172 / 226 mm | OBJ | layout.json tanks z0 (167-172, 226-229) | hoch |
| Plattform OBJ 706x707x73 auf Z 428 / 977x976x98 auf Z 570 (Z und Dicke gelten weiter) | 706x707x73 / 977x976x98 | OBJ | layout.json tanks platform | hoch |
| Plattform Breite/Laenge 619 (klein) / 821 (gross) = 2 x (Konusradius auf Plattform-Unterkante + 2 + 60) | 619 / 821 | Ben + R | Ben 31.10./D50 (Stand zu gross), Rechnung aus der Tankgeometrie (fix_w30_tank.py) | mittel |
| Pumpentafel steht seitlich am Stand (Abstand 30 mm von der Strebenaussenkante), Tafellaenge <= Plattform | 502 <= 619 / 693 <= 821 | A | W30: Tafel passt nicht mehr unter die Plattform (Tank 1: 327 gegen 310), Montage setzt sie seitlich | niedrig |
| Beine 4 x 30x30xh751 / 40x40xh1008 | 751 / 1008 mm | OBJ | layout.json tanks legs; Querschnitt aus oasis-obj-analysis | hoch |
| Kegel 45 Grad ab Horizontal, Ende auf der Plattform-Oberkante (gebaut 48,7 / 47,0 Grad wegen Randwulst) | 45 Grad | E | R09-Nachtrag 29.10. 07:55 (Orchestrator): Gegenprobe Spitze klein 165 gegen OBJ 167-172, gross 203 gegen 226-229; Scope-Card 45-60 Grad | mittel |
| Randwulst 25 x 40 mm | 25 x 40 | Bild + A | ref-5: dicker gerollter Randwulst der gruenen Tanks; Mass Annahme | niedrig |
| Tankwand 4 / 5 mm, Deckel 6 mm buendig | 4 / 5 / 6 mm | A | PE-Tank Wanddicke; OBJ nur Huelle | niedrig |
| Revisionsoeffnung im Deckel D200 | D200 | Scope-Card + A | Scope-Card: Deckel/Oeffnung; Mass Annahme | niedrig |
| Zulauf tangential d50 / d63, 250 mm unter dem Rand | d50 / d63 | R09 + A | R09: tangentialer Zulauf, DN50 oben (Konfidenz niedrig, nur fuer klein); gross analog [A] | niedrig |
| Leitrohr d110, endet 1/3 Zylinderhoehe ueber der Spitze (klein) | d110 | R09 | R09: Leitrohr D110, endet ca. 1/3 der Zylinderhoehe ueber der Kegelspitze (A, Konfidenz niedrig) | niedrig |
| Auslauf d50 (klein) / Ueberlauf d63 (gross) 100 mm unter dem Rand | d50 / d63, 100 mm | R09 + A | R09: Auslass oben seitlich, 100 mm unter dem Rand (A); gross analog | niedrig |
| Schlammventil Kugelhahn d40 / d50 an der Kegelspitze | d40 / d50 | OBJ + R09 + A | layout.json tanks fittings (Groessen 30-56 an der Spitze); R09: Schlammablass Bulkhead 32-40 mit Hahn; gross d50 Norm statt OBJ 55 | mittel |
| Biofilter: Schwebebett (EIN Koerper, 67 % von 702 l = 470 l), Belueftungsgitter D20 mit Steigrohr d16, 2 Rueckhaltesiebe | 520 mm hoch | A | Scope-Card tank_gross: Platzhalter; keine Quelle (R09) | niedrig |
| Plattform als Blechkasten 4 mm, hohl, mit Kegelsitz (Spiel 2) und Eckenaussparungen | 4 mm / 2 mm | A | OBJ-Plattform 73/98 mm dick (massiv unwahrscheinlich); Konstruktionsannahme | niedrig |
| Querstreben auf Hoehe 250 / 300, 4 Diagonalen 25x3 | 250 / 300 mm | Bild + A | ref-4/ref-5: Tanks auf Beinen mit Diagonalstreben (Scope-Card: Diagonalen) | mittel |
| Fussplatten 100x100x6 mit M8x30 | 100x100x6 | A | Standard | niedrig |
| Stuetzrippen: 5 je grossem Tank, 384 x 44 x 419, radial, Winkel 0/90/135/180/225 Grad | 5 Rippen, 44 mm | OBJ + A | layout.json tanks 2/3 modules (384 x 43/44 x 418/419, z0 249-256, radial im Abstand 276); Rolle Stuetzrippe: Orchestrator-Entscheidung 29.10. (A) | mittel |
| Anzahl 2 klein, 2 gross | 2 + 2 | OBJ | layout.json tanks (Azimut 123/213 und 108/229) | hoch |
| Farbe gruen #9db89c | #9db89c | Bild | ref-4/ref-5 gruene Tanks | mittel |
| Werkstoffdichten: PE 0,95, Stahl 7,85, PVC-U 1,4, Biomedium 0,15 | g/cm3 | Fachwert + A | Handbuchwerte Kunststoffe/Stahl; Biomedium Schuettdichte Annahme | mittel |
| Schwebebett K1 (67 % von 702 l = 470 l), Belueftungsgitter, Rueckhaltesiebe | 470 l | Q/A | R30 (K1-Traeger 0,94 m3 fuer beide Tanks = 470 m2), D55/W32; Gitter und Siebe Entwurf [A] | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-4-dome-clean.jpg und ref-5 (gruene Tanks mit gerolltem Randwulst auf duennen Beinen mit Kegelboden); data/layout.json tanks; docs/research/R09.md
- Quelle der Masse: data/layout.json tanks (Durchmesser, Hoehe, Z-Spitze, Plattform, Beine, Fittings), docs/scope-cards.md tank_klein/tank_gross, docs/hydraulics.md (Vortex), R09 (teilweise)
- Abweichung zum OBJ: layout.json tanks: Durchmesser (inkl. Randwulst), Hoehe, Kegelspitze Z, Plattform-Z und Beinhoehe stimmen (check_tank.py); das Plattform-MASS ist seit W30/D50 absichtlich kleiner als im OBJ (klein 619 statt 706, gross 821 statt 977: Konusdurchmesser auf Plattform-Unterkante + 2 x 60). Kegel: OBJ liefert nur Spitze und Gesamthoehe; Kegelende auf der Plattform-Oberkante, 45 Grad ab Horizontal als Auslegung E (R09-Nachtrag 29.10. 07:55, vom Orchestrator bestaetigt; Gegenprobe Spitze klein 165 gegen OBJ 167-172, gross 203 gegen 226-229); gebaut 48,7 / 47,0 Grad, weil der Randwulst den Koerperradius gegenueber dem OBJ-Durchmesser verkleinert. Leitrohr und Auslauf nach R09 (A, Konfidenz niedrig, R09 behandelt nur den kleinen Tank, fuer gross analog). Beine 751/1008 laufen bis ueber die Plattform (OBJ-Mass). STUETZRIPPEN (gross): die 5 Kassetten 384 x 44 x 419 je grossem Tank aus layout.json tanks[].modules sind nach Orchestrator-Entscheidung 29.10. (D-Punkt 4) Stuetzrippen/Konsolen der Plattform: radial zur Tankachse, Winkel 0/90/135/180/225 Grad (Phase 11,0 Grad bei Tank 2, 53,6 Grad bei Tank 3: Dateien tank_gross.sc und tank_gross_t3.sc), Dreiecksknaggen von z 249 bis zur Plattform-Unterkante 570 (OBJ: bis Plattform-Oberkante 668, also in die hohle Plattform hinein), aussen r 367 statt 468 (Innenkante der Querstreben minus 3 mm, W30), Hypotenuse entlang des Tankkegels mit 3 mm Spiel; Alternative (nicht gebaut): Filterkassetten, Entwurf entfernt. Fittings: OBJ 4 Stueck Z 143-177 mit 30-56 mm, hier Schlammstutzen + Kugelhahn (d40 / d50 Norm statt OBJ 55) + Ablaufstutzen.

## Montage (L4)

1. Plattform mit Beinen am Boden ausrichten, Fussplatten mit M8 verschrauben, Streben und Diagonalen einsetzen
2. Tank in den Kegelsitz setzen (zu zweit), Deckel einsetzen (Leitrohr beim Absetzer); beim Biofilter Belueftungsgitter und Siebe einbauen
3. Zulauf-Rohr tangential und Auslauf/Ueberlauf durch die Wand fuehren, Dichtungen setzen
4. Kugelhahn mit Verschraubung an den Kegelstutzen, Ablaufrohr anschliessen
5. Dichtheit pruefen (Wasserprobe), K1-Traeger einschuetten (gross: ca. 470 l Schuettvolumen) und Belueftung anschliessen

**Werkzeug:** Lochsaege (d63/d50), Bohrer, Schluessel M6/M8, Wasserwaage, Schweissgeraet (Rahmen) oder Winkelverbinder

## Stueckliste-Zeile

- klein (je Tank): Tank PE (4 mm Wand, Aussen-D673 x H1075, Randwulst) 1; Deckel mit Revisionsoeffnung D200 1 (Revisionsdeckel nicht modelliert, 1 Stueck); Zulaufrohr d50 1 + Bulkhead mit Dichtung 1; Leitrohr d110 mit Auslaufrohr d50 1 + Bulkhead mit Dichtung 1; Kugelhahn d40 mit Verschraubung und 2 Stutzen 1; Plattform 1; Beine 30x30 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 ISO 4017 + Mutter ISO 4032, nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30 ISO 4017 und 8 Duebeln M8
- gross (je Tank): Tank PE (5 mm Wand, Aussen-D930 x H1444, Randwulst) 1; Deckel mit Revisionsoeffnung D200 1 (Revisionsdeckel nicht modelliert, 1 Stueck); Zulaufrohr d63 1 + Bulkhead mit Dichtung 1; Ueberlauf d63 1 + Bulkhead mit Dichtung 1, Schwebebett K1-Traeger (470 l Schuettvolumen, ca. 71 kg) 1, Belueftungsgitter D20 mit Steigrohr d16 1, Zulaufsieb 1, Auslaufsieb 1; 5 Stuetzrippen Kantholz 44 (Dreiecksknaggen radial unter dem Kegel, Fichte, T40g) 1 Satz; Kugelhahn d50 mit Verschraubung und 2 Stutzen 1; Plattform 1; Beine 40x40 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 ISO 4017 + Mutter ISO 4032, nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30 ISO 4017 und 8 Duebeln M8
- Tanks gesamt: klein 2, gross 2 (Azimute 123/213 und 108/229, layout.json); Normschrauben: M8x30 ISO 4017, M6x40 ISO 4017, Muttern ISO 4032

## Alternative lokale Fertigung

Tank: handelsueblicher Konus-Boden-Tank (Kunststoff, 500-1000 l); Plattform/Beine aus Baustahl-Rechteckrohr (Metallbauer) oder Alu-Systemprofil; Rohre und Kugelhaehne PVC-U aus dem Sanitaerhandel.

## Renders

- `renders/components/tank_gross/tank_gross-01-iso.png`
- `renders/components/tank_gross/tank_gross-02-kegel.png`
- `renders/components/tank_gross/tank_gross-03-zulauf.png`
- `renders/components/tank_gross/tank_gross-04-deckel.png`
- `renders/components/tank_gross/tank_gross-05-schnitt.png`
- `renders/components/tank_gross_t3/tank_gross_t3-01-iso.png`
- `renders/components/tank_gross_t3/tank_gross_t3-02-kegel.png`
- `renders/components/tank_gross_t3/tank_gross_t3-03-zulauf.png`
- `renders/components/tank_gross_t3/tank_gross_t3-04-deckel.png`
- `renders/components/tank_gross_t3/tank_gross_t3-05-schnitt.png`
- `renders/components/tank_klein/tank_klein-01-iso.png`
- `renders/components/tank_klein/tank_klein-02-kegel.png`
- `renders/components/tank_klein/tank_klein-03-zulauf.png`
- `renders/components/tank_klein/tank_klein-04-deckel.png`
- `renders/components/tank_klein/tank_klein-05-schnitt.png`

## Pruefung

- Gauntlet-Urteil: offen
- scripts/workshop/check_tank.py (Ergebnis renders/components/tank_klein/check.txt)
- Bild-Kritiker: Modell; Spec-Pruefer: FAIL (Gewicht, Text gegen Parameter, Auslaufhoehe, Herkunft, Ports) -> behoben, Triage in docs/workshop-log.md
- W32: scripts/workshop/check_tank.py um check_bed erweitert (Bettvolumen 470 l, Traegerflaeche, Lage im Tank, Belueftungsgitter, Siebe, Interferenzen im Biofilter; Ergebnis in renders/components/tank_klein/check.txt)

## Offene Fragen

- Kegelwinkel/Kegelende: Auslegung E (45 Grad, Plattform-OK), R09 Konfidenz niedrig
- Rohrmasse (Zulauf d50/d63, Leitrohr d110, Auslauf d50/d63, Wand 3 mm) ohne Quelle (R09)
- Beine 751/1008 bis ueber die Plattform: Zweck (Tankfuehrung) aus OBJ nicht ableitbar
- Haltegurt/Schellen, Dichtungen, Verschraubungen der Diagonalen (M6x40), Revisionsdeckel nicht modelliert
- Biofilter (gross): Schwebebett nach R30/D55 (K1, 67 % der Wasserfuellung 702 l), Belueftungsgitter und Siebe als Entwurf [A]; kein Leitrohr im Biofilter (R09 nennt es nur fuer den Absetzer, Scope-Card fuehrt es gemeinsam)
- Rolle der Stuetzrippen: Annahme A (Orchestrator), Werkstoff Holz Fichte nur wegen der Dicke 44 mm; Alternative Filterkassette; Rippen enden an der Plattform-Unterkante, im OBJ bis Plattform-Oberkante
- Rolle der Pumpen (eigene Klasse pumpe)
- W30/D50: Plattform 619 / 821 statt 706 / 977; der Kegel sitzt in einem kegeligen Sitz, der Tankzylinder (R 311,5 / 440) ueberragt die Plattform (Kontaktring nur ca. 60 mm hoch im unteren Plattformteil): Tragfaehigkeit des Sitzes und Haltegurt nicht nachgewiesen [A]
- W30: Pumpentafeln 502 x 345 / 693 x 463 passen nicht mehr unter die Plattform (Tank 1: Tafelrand 327 gegen Plattformhalbbreite 310); Montage setzt sie seitlich am Stand, Tafelmittelabstand >= Plattformhalbbreite + 25 + tafel_gap (tank_offsets pruefen)
- W32 (D55, 31.10.): Das Schwebebett ist ein Koerper mit 470 l Schuettvolumen (0,67 x 702 l, Z 489..1353); das Tankprofil fasst bis zum Rand nur 687 l und bis zum Ueberlauf-Mittelpunkt 628 l: Das Bett fuellt damit 68 % (Rand) bzw. 75 % (Ueberlauf) des Modellwassers; K1-Betten werden meist auf hoechstens 67-70 % ausgelegt. Entscheidung offen: Ueberlauf tiefer oder Fuellung 0,67 x 628 l = 421 l (Orchestrator/Ben)
- K1-Traeger Fabrikat, Abmessungen (D9 x 7 mm, 500 m2/m3) und die Schwebewirkung bei der Belueftung sind [A]/R30 (Datenblatt nicht gelesen); die Traeger sind nicht einzeln modelliert; Siebschlitze (5 mm) und Belueftungsbohrungen nicht modelliert; Luftmenge/Gebläse nicht gerechnet
- Schlammstutzen sitzt 2 mm in der Kegelspitze (gewollter Sitz, 857,8 mm3 Ueberdeckung, unveraendert gegen den Stand vor W32); der Check nimmt diese eine Paarung aus
- Die frueheren Interferenzen Tank/Konsolen und Zulaufrohr/Biomediumkorb (Stand vor W32) entfallen mit dem Schwebebett

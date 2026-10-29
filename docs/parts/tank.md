# Bauteilblatt T40 tank (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/tank.json` und `designs/components/tank.sc`, nicht von Hand aendern)

**Funktion:** Tank mit Kegelboden: klein = Vortex-Absetzer (tangentialer Zulauf, Leitrohr, Schlamm sinkt zur Spitze und wird dort abgelassen), gross = Biofilter (Biomediumkorb auf Tragrost, Belueftung, Ueberlauf, Schlammablass); steht auf Plattform und 4 Beinen.

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
| `bio_h` | 520 | mm | [A] Biomediumkorb: Hoehe |
| `bio_z_below_top` | 700 | mm | [A] Biomediumkorb: Unterkante 700 mm unter dem Tankrand |
| `diag_w` | 25 | mm | [A] Diagonale Flachstahl 25 x 3 |
| `rim_w` | 25 | mm | Bild: ref-5 dicker gerollter Randwulst; 25 mm nach aussen, Aussenmass D laut OBJ inkl. Wulst [A] |
| `rim_h` | 40 | mm | Bild: ref-5 dicker gerollter Randwulst (Bild-Kritiker Luecke 2: Wulst zu schmal); 40 mm hoch [A] |
| `rev_d` | 200 | mm | [A] Revisionsoeffnung im Deckel D200 (Scope-Card: Deckel/Oeffnung; Bild-Kritiker Luecke 5) |
| `bracket` | 40 | mm | [A] Konsolen 40 x 40 x 30 (4 Stueck) unter dem Tragrost, an die Tankwand geschweisst (Bild-Kritiker Luecke 1) |
| `outlet_below_top` | 100 | mm | R09 (Auslass oben seitlich, 100 mm unter dem Rand) [A, Konfidenz niedrig]; fuer klein und gross |
| `guide_bottom_f` | 0.333 |  | R09: Leitrohr endet ca. 1/3 der Zylinderhoehe ueber der Kegelspitze (Zylinderhoehe = Rand minus Kegelende) [A] |

| Typ | R | H | z0 | plat_l | plat_w | plat_t | plat_z0 | leg_w | leg_h | leg_wall | wall | rt | strut_z | valve_d | inlet_d | anzahl | biofilter | herkunft |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| klein | 336.5 | 1075 | 172 | 706 | 707 | 73 | 428 | 30 | 751 | 2 | 4 | 22 | 250 | 40 | 50 | 2 | 0 | layout.json tanks 1 und 4: D673, H1075, Spitze Z 167-172, Plattform 706x707x73 auf Z 424-428, Beine 4 x h751, Fittings 30-40 an der Spitze |
| gross | 465 | 1444 | 226 | 977 | 976 | 98 | 570 | 40 | 1008 | 2.5 | 5 | 28 | 300 | 50 | 63 | 2 | 1 | layout.json tanks 2 und 3: D930, H1441-1444, Spitze Z 226-229, Plattform 977x976x98 auf Z 570-572, Beine 4 x h1006-1008, Fittings 41-56 an der Spitze; Hahn d50 (Norm) statt OBJ-Fitting 55 [A] |

Gesamt-Box (Messung): X -388.0 bis 441.5, Y -388.5 bis 388.5, Z -24.0 bis 1323.0 mm; Koerper: 33.

- Box (Messung) klein: X -388 bis 442, Y -388 bis 388, Z -24 (Schraubenenden 24 mm im Boden) bis 1323
- Box (Messung) gross: X -518 bis 570, Y -518 bis 518, Z -24 (Schraubenenden 24 mm im Boden) bis 1750
**Toleranzen / Spiel:** Kegelsitz in der Plattform 2 mm Spiel; Zulaufrohr beruehrt die Innenwand tangential (+-0,5 mm); Tankhoehe und Kegelspitze +-1 mm gegen layout.json im Bauteil; Instanzen: layout.json hat je Tank eine eigene Spitze (klein 167-172, gross 226-229): der Integrator setzt z so, dass die Spitze stimmt (Versatz bis 5 mm gegenueber dem Bauteil, z. B. Tank 4: -5 mm), die Plattform liegt je Tank 424-428 bzw. 570-572.

## Werkstoff und Gewicht

- Werkstoff: PE (Tank), Stahl verzinkt (Plattform, Beine), PVC (Rohre, Ventil), Dichte 0.95 g/cm3, Farbe #9db89c (ref-4/ref-5: gruene Kunststofftanks mit Randwulst; PE-Dichte 0,95 g/cm3 Handbuchwert; Stahl 7,85; PVC-U 1,4)
- Volumen (Messung, `solidcraft-cli eval`): 17043.7 cm3 · Masse leer (ohne Biomedium): 46031 g (46.03 kg)
- Variante `tank_klein`: 46.03 kg leer (ohne Biomedium)
- Variante `tank_gross`: 95.15 kg leer (ohne Biomedium)
- Gefuellt/in Betrieb: klein: leer 46 kg; Wasserfuellung bis Rand 254 l = 254 kg (Zylinder 222 l + Kegel 33 l; Wasserfuellung gehoert zu DRAUSSEN, nur Gewichtsangabe) [E]; gefuellt gesamt 300 kg | gross: leer 95 kg, Biomedium (Schuettung 0,15 g/cm3) 41 kg; Wasserfuellung bis Rand 683 l = 683 kg (Zylinder 596 l + Kegel 88 l; Wasserfuellung gehoert zu DRAUSSEN, nur Gewichtsangabe) [E]; gefuellt gesamt 820 kg

## Querschnitt / Profil

Tank PE: Zylinder ueber Kegel, gerollter Randwulst 25 x 40 mm, Wand 4/5 mm, Deckel 6 mm buendig mit dem Wulst, Revisionsoeffnung D200. Geometrie je Tank: klein: Kegel 48.7 Grad ab Horizontal (Spitze Z 172, Ende Z 501), Koerperradius 311.5 (D623) plus Randwulst 25 = Aussen-D673 | gross: Kegel 47.0 Grad ab Horizontal (Spitze Z 226, Ende Z 668), Koerperradius 440.0 (D880) plus Randwulst 25 = Aussen-D930. Plattform: Blechkasten 4 mm, innen hohl, Kegelsitz 2 mm Spiel, Eckenaussparungen fuer die Beine; Beine Rechteckrohr verzinkt; vier Querstreben auf Hoehe 250/300 und vier Diagonalen (an den Beinkanten gekuerzt).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| klein: Zulauf tangential (Rohr d50, DN40) | PVC-U d50 nach DIN 8062 (DN40), Wand 3 | x 282.5, y -351, z 997 (Rohrachse parallel Y, Rohrende aussen) | Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall) |
| klein: Auslauf (Auslaufrohr vom Leitrohr durch die Tankwand) | PVC-U d50 (DN40) | x 442, y 0, z 1147 (100 mm unter dem Rand, R09) | Wasser verlaesst den Absetzer nach +X (Oeffnung zeigt +X) |
| klein: Schlammablass (Kugelhahn an der Kegelspitze) | PVC-U d40 (DN30), Kugelhahn mit Verschraubung | x 0, y 0, z 80 (Stutzenende); Kegelspitze z 172 | Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X |
| klein: Fussplatten-Anker (4 Fuesse, je 2 x M8) | Schrauben M8x30 ISO 4017, Loch D9, Platte 100 x 100 x 6; im Boden Duebel/Betonpunkt M8 | x +-338, y +-338, z 6 (Diagonalversatz +-35); Schraubenenden z -24 | Befestigung auf Boden/Betonpunkt, Richtung -Z |
| gross: Zulauf tangential (Rohr d63, DN50) | PVC-U d63 nach DIN 8062 (DN50), Wand 3 | x 403.5, y -395, z 1420 (Rohrachse parallel Y, Rohrende aussen) | Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall) |
| gross: Ueberlauf (Auslauf) | PVC-U d63 (DN50) | x 570, y 0, z 1570 (100 mm unter dem Rand, R09) | Wasser verlaesst den Biofilter nach +X (Oeffnung zeigt +X) |
| gross: Belueftungsanschluss im Deckel | Rohr d16 (Luftschlauch 16 mm, etwa DN10) | x 220, y 0, z 1676 | Luft tritt ein, Oeffnung zeigt +Z |
| gross: Schlammablass (Kugelhahn an der Kegelspitze) | PVC-U d50 (DN40), Kugelhahn mit Verschraubung | x 0, y 0, z 134 (Stutzenende); Kegelspitze z 226 | Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X |
| gross: Fussplatten-Anker (4 Fuesse, je 2 x M8) | Schrauben M8x30 ISO 4017, Loch D9, Platte 100 x 100 x 6; im Boden Duebel/Betonpunkt M8 | x +-468, y +-468, z 6 (Diagonalversatz +-35); Schraubenenden z -24 | Befestigung auf Boden/Betonpunkt, Richtung -Z |

## Verbindungen und Befestigungen

- Tank sitzt mit dem Kegel im Kegelsitz der Plattform (Kegel-Zylinder-Uebergang auf der Plattform-Oberkante), Haltegurt/Schellen nicht modelliert [A]
- Beine laufen durch Eckenaussparungen der Plattform, geschweisst (MAG), danach verzinkt [A]
- Fussplatten: je 2 Schrauben M8x30 ISO 4017 mit Duebel M8 im Boden/Betonpunkt, Loch D9
- Rohre PVC-U nach DIN 8062/EN 1452 mit Bulkhead-Durchfuehrung und Dichtung durch die Tankwand [A, im Modell nur Durchbruch + Rohr]
- Schlammventil: Kugelhahn PVC-U mit Verschraubung an Stutzen d40/d50
- Biomediumkorb (gross): Tragrost auf 4 Konsolen 40x40x30 (an die Tankwand geschweisst/geklebt) [A]

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Tankdurchmesser 673 / 930 (inkl. Randwulst) | 673 / 930 mm | OBJ | layout.json tanks d (Tank 1/4 und 2/3) | hoch |
| Tankhoehe 1075 / 1444 (inkl. Kegel) | 1075 / 1444 mm | OBJ | layout.json tanks h | hoch |
| Kegelspitze Z 172 / 226 | 172 / 226 mm | OBJ | layout.json tanks z0 (167-172, 226-229) | hoch |
| Plattform 706x707x73 auf Z 428 / 977x976x98 auf Z 570 | 706x707x73 / 977x976x98 | OBJ | layout.json tanks platform | hoch |
| Beine 4 x 30x30xh751 / 40x40xh1008 | 751 / 1008 mm | OBJ | layout.json tanks legs; Querschnitt aus oasis-obj-analysis | hoch |
| Kegel 45 Grad ab Horizontal, Ende auf der Plattform-Oberkante (gebaut 48,7 / 47,0 Grad wegen Randwulst) | 45 Grad | E | R09-Nachtrag 29.10. 07:55 (Orchestrator): Gegenprobe Spitze klein 165 gegen OBJ 167-172, gross 203 gegen 226-229; Scope-Card 45-60 Grad | mittel |
| Randwulst 25 x 40 mm | 25 x 40 | Bild + A | ref-5: dicker gerollter Randwulst der gruenen Tanks; Mass Annahme | niedrig |
| Tankwand 4 / 5 mm, Deckel 6 mm buendig | 4 / 5 / 6 mm | A | PE-Tank Wanddicke; OBJ nur Huelle | niedrig |
| Revisionsoeffnung im Deckel D200 | D200 | Scope-Card + A | Scope-Card: Deckel/Oeffnung; Mass Annahme | niedrig |
| Zulauf tangential d50 / d63, 250 mm unter dem Rand | d50 / d63 | R09 + A | R09: tangentialer Zulauf, DN50 oben (Konfidenz niedrig, nur fuer klein); gross analog [A] | niedrig |
| Leitrohr d110, endet 1/3 Zylinderhoehe ueber der Spitze (klein) | d110 | R09 | R09: Leitrohr D110, endet ca. 1/3 der Zylinderhoehe ueber der Kegelspitze (A, Konfidenz niedrig) | niedrig |
| Auslauf d50 (klein) / Ueberlauf d63 (gross) 100 mm unter dem Rand | d50 / d63, 100 mm | R09 + A | R09: Auslass oben seitlich, 100 mm unter dem Rand (A); gross analog | niedrig |
| Schlammventil Kugelhahn d40 / d50 an der Kegelspitze | d40 / d50 | OBJ + R09 + A | layout.json tanks fittings (Groessen 30-56 an der Spitze); R09: Schlammablass Bulkhead 32-40 mit Hahn; gross d50 Norm statt OBJ 55 | mittel |
| Biofilter: Biomediumkorb (EIN Koerper) auf Tragrost mit 4 Konsolen 40x40x30, Belueftung d16 | 520 mm hoch | A | Scope-Card tank_gross: Platzhalter; keine Quelle (R09) | niedrig |
| Plattform als Blechkasten 4 mm, hohl, mit Kegelsitz (Spiel 2) und Eckenaussparungen | 4 mm / 2 mm | A | OBJ-Plattform 73/98 mm dick (massiv unwahrscheinlich); Konstruktionsannahme | niedrig |
| Querstreben auf Hoehe 250 / 300, 4 Diagonalen 25x3 | 250 / 300 mm | Bild + A | ref-4/ref-5: Tanks auf Beinen mit Diagonalstreben (Scope-Card: Diagonalen) | mittel |
| Fussplatten 100x100x6 mit M8x30 | 100x100x6 | A | Standard | niedrig |
| Anzahl 2 klein, 2 gross | 2 + 2 | OBJ | layout.json tanks (Azimut 123/213 und 108/229) | hoch |
| Farbe gruen #9db89c | #9db89c | Bild | ref-4/ref-5 gruene Tanks | mittel |
| Werkstoffdichten: PE 0,95, Stahl 7,85, PVC-U 1,4, Biomedium 0,15 | g/cm3 | Fachwert + A | Handbuchwerte Kunststoffe/Stahl; Biomedium Schuettdichte Annahme | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-4-dome-clean.jpg und ref-5 (gruene Tanks mit gerolltem Randwulst auf duennen Beinen mit Kegelboden); data/layout.json tanks; docs/research/R09.md
- Quelle der Masse: data/layout.json tanks (Durchmesser, Hoehe, Z-Spitze, Plattform, Beine, Fittings), docs/scope-cards.md tank_klein/tank_gross, docs/hydraulics.md (Vortex), R09 (teilweise)
- Abweichung zum OBJ: layout.json tanks: Durchmesser (inkl. Randwulst), Hoehe, Kegelspitze Z, Plattform (Mass und Z), Beinhoehe stimmen (check_tank.py). Kegel: OBJ liefert nur Spitze und Gesamthoehe; Kegelende auf der Plattform-Oberkante, 45 Grad ab Horizontal als Auslegung E (R09-Nachtrag 29.10. 07:55, vom Orchestrator bestaetigt; Gegenprobe Spitze klein 165 gegen OBJ 167-172, gross 203 gegen 226-229); gebaut 48,7 / 47,0 Grad, weil der Randwulst den Koerperradius gegenueber dem OBJ-Durchmesser verkleinert. Leitrohr und Auslauf nach R09 (A, Konfidenz niedrig, R09 behandelt nur den kleinen Tank, fuer gross analog). Beine 751/1008 laufen bis ueber die Plattform (OBJ-Mass). Fittings: OBJ 4 Stueck Z 143-177 mit 30-56 mm, hier Schlammstutzen + Kugelhahn (d40 / d50 Norm statt OBJ 55) + Ablaufstutzen.

## Montage (L4)

1. Plattform mit Beinen am Boden ausrichten, Fussplatten mit M8 verschrauben, Streben und Diagonalen einsetzen
2. Tank in den Kegelsitz setzen (zu zweit), Deckel und Leitrohr bzw. Biomediumkorb einsetzen
3. Zulauf-Rohr tangential und Auslauf/Ueberlauf durch die Wand fuehren, Dichtungen setzen
4. Kugelhahn mit Verschraubung an den Kegelstutzen, Ablaufrohr anschliessen
5. Dichtheit pruefen (Wasserprobe), Biomedium und Belueftung einbauen (gross)

**Werkzeug:** Lochsaege (d63/d50), Bohrer, Schluessel M6/M8, Wasserwaage, Schweissgeraet (Rahmen) oder Winkelverbinder

## Stueckliste-Zeile

- klein (je Tank): Tank PE (4 mm Wand, Aussen-D673 x H1075, Randwulst) 1; Deckel mit Revisionsoeffnung D200 1 (Revisionsdeckel nicht modelliert, 1 Stueck); Zulaufrohr d50 1 + Bulkhead mit Dichtung 1; Leitrohr d110 mit Auslaufrohr d50 1 + Bulkhead mit Dichtung 1; Kugelhahn d40 mit Verschraubung und 2 Stutzen 1; Plattform 1; Beine 30x30 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 ISO 4017 + Mutter ISO 4032, nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30 ISO 4017 und 8 Duebeln M8
- gross (je Tank): Tank PE (5 mm Wand, Aussen-D930 x H1444, Randwulst) 1; Deckel mit Revisionsoeffnung D200 1 (Revisionsdeckel nicht modelliert, 1 Stueck); Zulaufrohr d63 1 + Bulkhead mit Dichtung 1; Ueberlauf d63 1 + Bulkhead mit Dichtung 1, Biomediumkorb 1 mit Tragrost 1 und 4 Konsolen 40x40x30, Belueftungsrohr d16 1; Kugelhahn d50 mit Verschraubung und 2 Stutzen 1; Plattform 1; Beine 40x40 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 ISO 4017 + Mutter ISO 4032, nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30 ISO 4017 und 8 Duebeln M8
- Tanks gesamt: klein 2, gross 2 (Azimute 123/213 und 108/229, layout.json); Normschrauben: M8x30 ISO 4017, M6x40 ISO 4017, Muttern ISO 4032

## Alternative lokale Fertigung

Tank: handelsueblicher Konus-Boden-Tank (Kunststoff, 500-1000 l); Plattform/Beine aus Baustahl-Rechteckrohr (Metallbauer) oder Alu-Systemprofil; Rohre und Kugelhaehne PVC-U aus dem Sanitaerhandel.

## Renders

- `renders/components/tank_gross/tank_gross-01-iso.png`
- `renders/components/tank_gross/tank_gross-02-kegel.png`
- `renders/components/tank_gross/tank_gross-03-zulauf.png`
- `renders/components/tank_gross/tank_gross-04-deckel.png`
- `renders/components/tank_gross/tank_gross-05-schnitt.png`
- `renders/components/tank_klein/tank_klein-01-iso.png`
- `renders/components/tank_klein/tank_klein-02-kegel.png`
- `renders/components/tank_klein/tank_klein-03-zulauf.png`
- `renders/components/tank_klein/tank_klein-04-deckel.png`
- `renders/components/tank_klein/tank_klein-05-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Bild-Kritiker: Modell; Spec-Pruefer: FAIL behoben (Triage im Log)
- scripts/workshop/check_tank.py (Ergebnis renders/components/tank_klein/check.txt)
- Bild-Kritiker: Modell; Spec-Pruefer: FAIL (Gewicht, Text gegen Parameter, Auslaufhoehe, Herkunft, Ports) -> behoben, Triage in docs/workshop-log.md

## Offene Fragen

- Kegelwinkel/Kegelende: Auslegung E (45 Grad, Plattform-OK), R09 Konfidenz niedrig
- Rohrmasse (Zulauf d50/d63, Leitrohr d110, Auslauf d50/d63, Wand 3 mm) ohne Quelle (R09)
- Beine 751/1008 bis ueber die Plattform: Zweck (Tankfuehrung) aus OBJ nicht ableitbar
- Haltegurt/Schellen, Dichtungen, Verschraubungen der Diagonalen (M6x40), Revisionsdeckel nicht modelliert
- Biofilter (gross): Biomediumkorb, Konsolen, Belueftung als Platzhalter ohne Quelle; kein Leitrohr im Biofilter (R09 nennt es nur fuer den Absetzer, Scope-Card fuehrt es gemeinsam)
- Rolle der Pumpen/Filtermodule (eigene Klasse pumpe)

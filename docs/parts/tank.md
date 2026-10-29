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

| Typ | R | H | z0 | plat_l | plat_w | plat_t | plat_z0 | leg_w | leg_h | leg_wall | wall | rt | strut_z | valve_d | inlet_d | anzahl | biofilter | herkunft |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| klein | 336.5 | 1075 | 172 | 706 | 707 | 73 | 428 | 30 | 751 | 2 | 4 | 22 | 250 | 40 | 50 | 2 | 0 | layout.json tanks 1 und 4: D673, H1075, Spitze Z 167-172, Plattform 706x707x73 auf Z 424-428, Beine 4 x h751, Fittings 30-40 an der Spitze |
| gross | 465 | 1444 | 226 | 977 | 976 | 98 | 570 | 40 | 1008 | 2.5 | 5 | 28 | 300 | 55 | 63 | 2 | 1 | layout.json tanks 2 und 3: D930, H1441-1444, Spitze Z 226-229, Plattform 977x976x98 auf Z 570-572, Beine 4 x h1006-1008, Fittings 41-56 an der Spitze |

Gesamt-Box (Messung): X -388.0 bis 388.0, Y -388.5 bis 388.5, Z -24.0 bis 1323.0 mm; Koerper: 32.

**Toleranzen / Spiel:** Kegelsitz in der Plattform 2 mm Spiel; Zulaufrohr beruehrt die Innenwand tangential (Pruefung +-0,5 mm); Tankhoehe und Kegelspitze +-1 mm gegen layout.json.

## Werkstoff und Gewicht

- Werkstoff: PE (Tank), Stahl verzinkt (Plattform, Beine), PVC (Rohre, Ventil), Dichte 0.95 g/cm3, Farbe #9db89c (ref-4/ref-5: gruene Kunststofftanks auf duennen Beinen)
- Volumen (Messung, `solidcraft-cli eval`): 16533.1 cm3 · Masse leer (ohne Biomedium): 45312 g (45.31 kg)
- Variante `tank_klein`: 45.31 kg leer
- Variante `tank_gross`: 136.33 kg leer
- Gefuellt/in Betrieb: klein: leer 45 kg; Wasserfuellung bis Rand 254 l = 254 kg (Zylinder 222 l + Kegel 33 l); gefuellt gesamt 299 kg [E] | gross: leer 95 kg (ohne Biomedium 41 kg); Wasserfuellung bis Rand 683 l = 683 kg (Zylinder 596 l + Kegel 88 l); gefuellt gesamt 820 kg [E]

## Querschnitt / Profil

Tank PE: Zylinder (Koerper D633/D890) ueber Kegel (ca. 47 Grad ab Horizontal, Spitze mit Stutzen D44/D56); gerollter Randwulst 20 x 30 mm (Aussendurchmesser D673/D930 laut OBJ); Wand 4/5 mm; Deckel 6 mm mit 8 mm Ueberstand. Plattform: Blechkasten 4 mm, innen hohl, Kegelsitz 2 mm Spiel, Eckenaussparungen fuer die Beine; Beine Rechteckrohr verzinkt; vier Querstreben auf Hoehe 250/300 und vier Diagonalen.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| klein: Zulauf tangential (Rohr d50) | Rohr PVC-U d50 (etwa DN40), Wand 3 | x 282.5, y -351, z 997 (Rohrachse parallel Y, Rohrende aussen) | Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall) |
| klein: Auslauf am Leitrohr | Rohr d50 (etwa DN40), Leitrohr d110 | x 195, y 0, z 1288 | Wasser verlaesst den Absetzer nach +X (Oeffnung zeigt +X) |
| klein: Schlammablass (Kugelhahn an der Kegelspitze) | Kugelhahn d40, Ablaufstutzen d40 (Verschraubung) | x 0, y 0, z 80 (Stutzenende); Kegelspitze z 172 | Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X |
| klein: Fussplatten-Anker (4 Fuesse, je 2 x M8) | M8, Loch D9, Platte 100 x 100 x 6 | x +-338, y +-338, z 6 (Diagonalversatz +-35) | Befestigung auf Boden/Betonpunkt, Richtung -Z |
| gross: Zulauf tangential (Rohr d63) | Rohr PVC-U d63 (etwa DN53), Wand 3 | x 403.5, y -395, z 1420 (Rohrachse parallel Y, Rohrende aussen) | Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall) |
| gross: Ueberlauf (Auslauf) | Rohr d63 (etwa DN50), 80 mm unter dem Rand | x 570, y 0, z 1590 | Wasser verlaesst den Biofilter nach +X (Oeffnung zeigt +X) |
| gross: Belueftungsanschluss im Deckel | Rohr d16 (Luftschlauch 16 mm) | x 220, y 0, z 1676 | Luft tritt ein, Oeffnung zeigt +Z |
| gross: Schlammablass (Kugelhahn an der Kegelspitze) | Kugelhahn d55, Ablaufstutzen d55 (Verschraubung) | x 0, y 0, z 134 (Stutzenende); Kegelspitze z 226 | Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X |
| gross: Fussplatten-Anker (4 Fuesse, je 2 x M8) | M8, Loch D9, Platte 100 x 100 x 6 | x +-468, y +-468, z 6 (Diagonalversatz +-35) | Befestigung auf Boden/Betonpunkt, Richtung -Z |

## Verbindungen und Befestigungen

- Tank sitzt mit dem Kegel im Kegelsitz der Plattform (Kegel-Zylinder-Uebergang auf der Plattform-Oberkante), Haltegurt/Schellen nicht modelliert [A]
- Beine laufen durch Eckenaussparungen der Plattform, geschweisst (MAG), danach verzinkt [A]
- Fussplatten: je 2 Schrauben M8x30 (hex_bolt), Loch D9
- Rohre PVC-U (DIN 8062/EN 1452) mit Bulkhead-Durchfuehrung und Dichtung durch die Tankwand [A, im Modell nur Durchbruch + Rohr]
- Schlammventil: Kugelhahn PVC-U mit Verschraubung an Stutzen d40/d55

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Tankdurchmesser 673 / 930 | 673 / 930 mm | OBJ | layout.json tanks d (Tank 1/4 und 2/3) | hoch |
| Tankhoehe 1075 / 1444 (inkl. Kegel) | 1075 / 1444 mm | OBJ | layout.json tanks h | hoch |
| Kegelspitze Z 172 / 226 | 172 / 226 mm | OBJ | layout.json tanks z0 (167-172, 226-229) | hoch |
| Plattform 706x707x73 auf Z 428 / 977x976x98 auf Z 570 | mm | OBJ | layout.json tanks platform | hoch |
| Beine 4 x 30x30xh751 / 40x40xh1008 | mm | OBJ | layout.json tanks legs; Querschnitt aus oasis-obj-analysis | hoch |
| Kegel 45 Grad ab Horizontal, endet auf der Plattform-Oberkante | 45 Grad | A | OBJ liefert nur Spitze und Gesamthoehe; Scope-Card 45-60 Grad; Absetzer-Praxis; Alternative Unterkante = 37 Grad (R09-Auslegung) | niedrig |
| Tankwand 4 / 5 mm, Deckel 6 mm | 4 / 5 / 6 mm | A | PE-Tank Wanddicke; OBJ nur Huelle | niedrig |
| Zulauf tangential d50 / d63, 250 mm unter dem Rand | d50 / d63 | R09 + A | R09: tangentialer Zulauf, DN50 oben (Konfidenz niedrig); Masse A | niedrig |
| Leitrohr d110 x 420 mit Auslauf d50 (klein) | d110 / d50 | R09 + A | R09: Leitrohr D110, Auslass oben seitlich DN50; Tiefe A | niedrig |
| Schlammventil Kugelhahn d40 / d55 an der Kegelspitze | d40 / d55 | OBJ + R09 | layout.json tanks fittings (Groessen 30-56 an der Spitze); R09: Schlammablass Bulkhead 32-40 mit Hahn | mittel |
| Biofilter: Biomediumkorb (EIN Koerper) auf Tragrost, Belueftung d16, Ueberlauf d63 | - | A | Scope-Card tank_gross: Platzhalter; keine Quelle (R09) | niedrig |
| Plattform als Blechkasten 4 mm, hohl, mit Kegelsitz und Eckenaussparungen | 4 mm | A | OBJ-Plattform 73/98 mm dick (massiv unwahrscheinlich); Konstruktionsannahme | niedrig |
| Querstreben auf Hoehe 250 / 300, 4 Diagonalen 25x3 | 250 / 300 mm | Bild + A | ref-4/ref-5: Tanks auf Beinen mit Diagonalstreben (Scope-Card: Diagonalen) | mittel |
| Fussplatten 100x100x6 mit M8 | 100x100x6 | A | Standard | niedrig |
| Anzahl 2 klein, 2 gross | 2 + 2 | OBJ | layout.json tanks (Azimut 123/213 und 108/229) | hoch |
| Farbe gruen #9db89c, Werkstoff PE 0,95 | 0,95 g/cm3 | Bild | ref-4/ref-5 gruene Tanks | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-4-dome-clean.jpg und ref-5 (gruene Tanks auf duennen Beinen mit Kegelboden); data/layout.json tanks; docs/research/R09.md
- Quelle der Masse: data/layout.json tanks (Durchmesser, Hoehe, Z-Spitze, Plattform, Beine, Fittings), docs/scope-cards.md tank_klein/tank_gross, docs/hydraulics.md (Vortex), R09 (teilweise)
- Abweichung zum OBJ: layout.json tanks: Durchmesser, Hoehe, Kegelspitze Z, Plattform (Mass und Z), Beinhoehe stimmen (Pruefung check_tank.py). Kegel: OBJ liefert nur Spitze Z 172/226 und Gesamthoehe; das Ende des Kegels ist Annahme A (Plattform-Oberkante -> 45 Grad ab Horizontal, Absetzer-Praxis); Alternative laut R09-Auslegung: Kegelende an der Plattform-Unterkante (256 mm hoch, 37 Grad ab Horizontal / Halbwinkel 53 Grad) -> zu flach fuer Schlamm. Beine 751/1008 laufen bis ueber die Plattform (OBJ-Mass). Fittings: OBJ 4 Stueck Z 143-177, hier Schlammstutzen + Kugelhahn + Ablaufstutzen.

## Montage (L4)

1. Plattform mit Beinen am Boden ausrichten, Fussplatten mit M8 verschrauben, Streben und Diagonalen einsetzen
2. Tank in den Kegelsitz setzen (zu zweit), Deckel und Leitrohr bzw. Biomediumkorb einsetzen
3. Zulauf-Rohr tangential und Auslauf/Ueberlauf durch die Wand fuehren, Dichtungen setzen
4. Kugelhahn mit Verschraubung an den Kegelstutzen, Ablaufrohr anschliessen
5. Dichtheit pruefen (Wasserprobe), Biomedium und Belueftung einbauen (gross)

**Werkzeug:** Lochsaege (d63/d50), Bohrer, Schluessel M6/M8, Wasserwaage, Schweissgeraet (Rahmen) oder Winkelverbinder

## Stueckliste-Zeile

- klein (Stueck je Tank): Tank PE (4 mm Wand, Aussen-D673 x H1075, Randwulst) 1; Deckel 1; Zulaufrohr d50 1; Leitrohr d110 x 420 mit Auslauf d50 1; Kugelhahn d40 mit 2 Stutzen 1; Plattform 1; Beine 30x30 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 + Mutter nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30
- gross (Stueck je Tank): Tank PE (5 mm Wand, Aussen-D930 x H1444, Randwulst) 1; Deckel 1; Zulaufrohr d63 1; Ueberlauf d63 1, Biomediumkorb mit Tragrost 1, Belueftungsrohr d16 1; Kugelhahn d55 mit 2 Stutzen 1; Plattform 1; Beine 40x40 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 + Mutter nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30
- Tanks gesamt: klein 2, gross 2 (Azimute 123/213 und 108/229, layout.json)

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

- Gauntlet-Urteil: Bild-Kritiker: Modell (Luecken trianguliert); Spec-Pruefer offen
- scripts/workshop/check_tank.py (Ergebnis renders/components/tank_klein/check.txt)
- Triage in docs/workshop-log.md

## Offene Fragen

- Kegelende (Plattform-Oberkante vs. -Unterkante) und Kegelwinkel: nur Annahme, R09 Konfidenz niedrig
- Rohrmasse (Zulauf d50/d63, Leitrohr d110, Auslauf d50/d63, Wand 3 mm) ohne Quelle (R09)
- Beine 751/1008 bis ueber die Plattform: Zweck (Tankfuehrung) aus OBJ nicht ableitbar
- Haltegurt/Schellen, Dichtungen, Verschraubungen der Diagonalen (M6x40) nicht modelliert
- Biofilter: Biomediumkorb und Belueftung als Platzhalter, keine Quelle zur Auslegung (R09)
- Rolle der Pumpen/Filtermodule (eigene Klasse pumpe)

# Bauteilblatt T30 ibc_beet (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/ibc_beet.json` und `designs/components/ibc_beet.sc`, nicht von Hand aendern)

**Funktion:** Substratbeet (Fluten und Entleeren per Glockensiphon): Pflanzen (Instanzen; 288 je Aussenbeet, Beet bei Azimut 113 hat 144) in Netztoepfen im Medium (Blaehton/Kies), Wasser fliesst ueber das Tropfrohr zu, der Glockensiphon entleert das Beet in Zyklen bis auf 12 mm Film ueber dem ungelochten Sperrboden (V3, D77: kein stehendes Wasser unter dem Medium); zugleich Biofilterflaeche. Ein stehender Reinigungsschacht d110 erlaubt das Absaugen von Schlamm.

**Datei:** `designs/components/ibc_beet.sc` · **Teilenummer:** T30 · **Revision:** A · **Bezugspunkt:** Mitte der Wannenunterseite (Z=0), X Laengsachse, Y quer; Wannenoberkante bei Z = hoehe; Medienoberflaeche bei hoehe - rim_gap; Ablaufport unter dem Boden (Z < 0); Wannen sind eingelassen (z0 -162 bis -209, Integrator)

**Anzahl (Instanzen):** aussen 8 (OBJ: 5 x 933, 3 x 993; Zielmass nach D29: 8 x aussen_800), innen 6 (Quelle: data/layout.json ibc_beds; aussen_800: docs/decisions.md D29 (Montage M7 stellt den Dom um))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `wall` | 4 | mm | R03: Wandstaerke 3-4 mm (Scope-Card ibc_beet) |
| `floor_t` | 5 | mm | [A] Bodenstaerke |
| `corner_r` | 40 | mm | [A] Innenradius der Wannenecken (IBC-Schnitt, ref-5) |
| `rim_w` | 20 | mm | [A] Randsims: Breite nach aussen 20 mm (Bild-Kritiker: Referenz zeigt breiten flachen Randsims) |
| `rim_h` | 14 | mm | [A] Randsims: Hoehe 14 mm |
| `rim_gap` | 75 | mm | [E] Abstand Medienoberflaeche unter Wannenrand: R03 Z 400 minus OBJ-Oberkante Z 475 |
| `media_depth` | 300 | mm | R03: Fruchtgemuese 300, Blattgemuese 150-200 (FarmHub); Scope-Card 300 |
| `media_gap` | 2 | mm | [A] Spiel Medium zur Wannenwand |
| `grid_t` | 8 | mm | [A] Sperrboden 8 mm (PP-Platte, ungelocht, V3/D77), Stuetzenabstand <= 420 mm (Traglast Medium) |
| `post` | 60 | mm | [A] Stuetzklotz 60 x 60 unter dem Sperrboden |
| `post_nx` | 8 |  | [A] Stuetzen in Laengsrichtung: aussen 8, innen 5; 3 Reihen (y = +-(Wi/2-100) und 0) |
| `standpipe_d` | 25 | mm | R03: Standrohr D25 (FarmHub 2,5 cm PVC) |
| `standpipe_over` | 265 | mm | Orchestrator 29.10.: standpipe_h = media_depth - 35 mm = 265 ueber der Medienunterkante (Wasserstand 35 mm unter der Oberflaeche, dazwischen SRAC 1 Zoll = 25 mm / R03 trockene Zone 2-5 cm); Variante FarmHub 220 (R03 Befund 5, widerspricht Befund 4); Gesamtlaenge ab Bulkhead = Stuetzhoehe + 265 [E] |
| `standpipe_wall` | 1.5 | mm | Bevo PVC-U Druckrohr 25 x 1,5 PN10 Art. 0309025 [R51/R45]: ID 22,0, Querschnitt 380 mm2 (W40-BEET Auflage 4, M-BEET-TAUSCH 0b; vorher [A] 2 mm = 346 mm2) |
| `bell_d` | 75 | mm | R03: Glocke D75 |
| `bell_h` | 295 | mm | [E] Glocke = Standrohrhoehe + 30 mm (R03: 250 bei Standrohr 220); oben verschlossen |
| `bell_wall` | 3 | mm | [A] PVC-Rohr d75 |
| `bell_slot_w` | 10 | mm | R03: zwei Schlitze 10 x 40 mm |
| `bell_slot_h` | 12 | mm | W40-BEET V3 (D77): Kerbenhoehe 12 mm = Restfilm 12 mm; 4 Kerben 10 x 12 = 480 mm2 >= Standrohrflaeche 380 mm2 (R03 hatte 2 Schlitze 10 x 40) |
| `bell_slot_z` | 0 | mm | W40-BEET V3: Kerben beginnen am Glockenfuss (Oberkante Kerbe = Plattenoberkante + 12) |
| `air_hole` | 10 | mm | R03: Luftloch D10, 50 mm ueber dem Unterrand (quadratisch 10 x 10 modelliert) |
| `guard_d` | 110 | mm | R03: Medienschutz D110 |
| `guard_h` | 320 | mm | R03: Medienschutz 320 hoch |
| `guard_wall` | 1.5 | mm | W40-BEET (D77): Lochblech Edelstahl 1.4301 1,5 mm, Rundloch 5 mm Teilung 8 (R51 T30e-4), Zuschnitt und Rollen beim Metallbauer |
| `bulkhead_d` | 36 | mm | [A] Tankverbinder-Aussen D36 (Gewinde 1 Zoll), fuer Wannenboden und Sperrboden; darin Reduzierhuelse 32/25 (D77) |
| `bulkhead_flange` | 50 | mm | [A] Flansch D50 |
| `inflow_d` | 20 | mm | [A] Zulauf-Tropfrohr D20 (PE), Zulauf 200-500 l/h je Beet (R03) |
| `inflow_wall` | 2 | mm | [A] |
| `inflow_below_rim` | 25 | mm | R03: Zulaufrohr auf Z 450 = 25 mm unter OBJ-Oberkante Z 475 |
| `inflow_hole` | 4 | mm | [A] Tropfloecher 4 x 4 mm (quadratisch modelliert, real D4) |
| `inflow_pitch` | 200 | mm | [A] Tropflochabstand |
| `guard_slot_w` | 5 | mm | Modellvereinfachung Lochblech: Schlitz 5 mm breit (real Rundloch d5, Teilung 8) |
| `guard_slot_h` | 50 | mm | Modellvereinfachung Lochblech: Schlitz 50 mm hoch |
| `guard_slot_n` | 12 |  | Schlitze je Ring (kreisfoermiges Muster) |
| `guard_ring_z1` | 10 | mm | Ring 1 ab 10 mm ueber der Plattenoberkante (R51 T30e-4: z 272 bis 322) |
| `guard_ring_z2` | 80 | mm | Ring 2 ab 80 mm ueber der Plattenoberkante (R51: z 342 bis 392); 24 x 5 x 50 = 6000 mm2 = 15,8 x Standrohr |
| `cap_h` | 15 | mm | Hoehe der losen Kappen (Muffenstopfen DN110) auf Medienschutz und Reinigungsschacht [A] |
| `shaft_d` | 110 | mm | W40-BEET T30e-5: Reinigungsschacht KG/HT-Rohr DN100 (Aussen-D 110) |
| `shaft_wall` | 3 | mm | [A] KG-Rohr DN100 (Wand 3,2 mm real) |
| `shaft_over` | 20 | mm | Oberkante 20 mm ueber der Medienoberflaeche (R51 T30e-5) |
| `shaft_kerbe` | 30 | mm | 2 Kerben 30 x 30 am Schachtfuss: Wasser und Schlamm vom Plattenfilm in den Schacht (absaugbar, Saugschlauch d <= 75) |
| `bulkhead_id` | 32 | mm | D77: Tankverbinder mit Klebemuffe d32; darin Reduzierhuelse 32/25 fuer das Standrohr d25 (Innen d32) |
| `reduktion_h` | 50 | mm | R51 T30e-3: Reduktion kurz d40 x d25, Bauhoehe etwa 50 mm [A], Kaufmass pruefen |
| `reduktion_stutzen_d` | 40 | mm | Klebestutzen d40 unten |

| Typ | laenge | breite | hoehe | anzahl | herkunft | fase | fase_herkunft |
|---|---|---|---|---|---|---|---|
| aussen_933 | 2953 | 933 | 637 | 5 | layout.json ibc_beds 3-7: 2953 x 933 x 637 |  |  |
| aussen_993 | 2953 | 993 | 637 | 3 | layout.json ibc_beds 1, 2, 8: 2953 x 993 x 637 |  |  |
| innen_933 | 1865 | 933 | 649 | 6 | layout.json ibc_beds 9-14: 1865 x 933 x 649 | 120 | D44 (W-M4, 31.10.): Ecken 45 Grad angefast, Schenkel 120 mm am Randwulst-Umriss (ueberlappten Nachbarbeete um 35 mm); Rueckfall Laenge 1790; Medium/Siebboden/Wanne parallel versetzt |
| aussen_800 | 2640 | 800 | 637 | 8 | W17/D29: Aussenbeet einseitig erreichbar <= 800 breit; Laenge 2640 = Obergrenze aus der Montage-Rechnung (Streben/Sockel, D25; Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 60 = 2851 (corner_gap 60, W17; mit 100: 2771)); Hoehe wie OBJ 637; ersetzt aussen_933/aussen_993 im Dom (Montage M7 stellt um) |  |  |

Gesamt-Box (Messung, Variante ibc_beet_aussen_933): X -1516.5 bis 1476.5, Y -466.5 bis 466.5, Z -80.0 bis 637.0 mm; Koerper: 40.

**Toleranzen / Spiel:** Medium 2 mm Spiel zur Wanne; Wasserstand in der Flutphase = Standrohrkante, 265 mm ueber der Plattenoberkante = 35 mm unter der Medienoberflaeche (Orchestrator-Vorgabe 29.10.). Restwasser nach dem Ablauf: Film bis Kerben-Oberkante (Plattenoberkante + 12 mm), gerechnet 9,3 l (aussen_800), 7,6 l (innen_933), 12,3 l (aussen_933) bei 40 % Porositaet [A] (scripts/w40_beet_rechnung.py); Haftwasser im Korn bleibt. Entleerzeit d25: 3,6 bis 5,1 min (aussen_800), 4,7 bis 6,7 min (aussen_933) gegen R45 4,3 bis 6,1 min (R45 setzt fest 234 l an, die Rechnung nimmt die Beetflaeche; Abweichung ausgewiesen, Sollbereich unveraendert).

## Werkstoff und Gewicht

- Werkstoff: HDPE weiss (Wanne), PVC grau (Rohre), Kies/Blaehton (Medium), Dichte 0.95 g/cm3, Farbe #e9ebe8 (ref-5/ref-6 weisse Wannen (HDPE IBC-Innenbehaelter 0,95 g/cm3); Siebboden/Stuetzen PP 0,91, Rohre PVC-U 1,4 g/cm3)
- Volumen (Messung, Variante ibc_beet_aussen_933, `solidcraft-cli eval`): 77491.4 cm3 · Masse leer (ohne Medium): 73579 g (73.58 kg)
- Variante `ibc_beet_aussen_933`: 73.58 kg leer (ohne Medium)
- Variante `ibc_beet_aussen_993`: 76.00 kg leer (ohne Medium)
- Variante `ibc_beet_aussen_800`: 63.67 kg leer (ohne Medium)
- Variante `ibc_beet_innen_933`: 48.77 kg leer (ohne Medium)
- Gefuellt/in Betrieb: aussen_933: leer ohne Medium 73.6 kg; Medium 761 l = 685 kg (Schuettdichte 0,9 [A]); Wasser nur im Medium (Poren bis Standrohrkante, 40 % [A]) 269 l = 269 kg, KEIN Wasserraum unter dem Sperrboden; gefuellt gesamt 1027 kg | aussen_993: leer ohne Medium 76.0 kg; Medium 813 l = 732 kg (Schuettdichte 0,9 [A]); Wasser nur im Medium (Poren bis Standrohrkante, 40 % [A]) 287 l = 287 kg, KEIN Wasserraum unter dem Sperrboden; gefuellt gesamt 1095 kg | aussen_800: leer ohne Medium 63.7 kg; Medium 575 l = 517 kg (Schuettdichte 0,9 [A]); Wasser nur im Medium (Poren bis Standrohrkante, 40 % [A]) 203 l = 203 kg, KEIN Wasserraum unter dem Sperrboden; gefuellt gesamt 784 kg | innen_933: leer ohne Medium 48.8 kg; Medium 467 l = 420 kg (Schuettdichte 0,9 [A]); Wasser nur im Medium (Poren bis Standrohrkante, 40 % [A]) 165 l = 165 kg, KEIN Wasserraum unter dem Sperrboden; gefuellt gesamt 634 kg

## Querschnitt / Profil

Wanne halbe IBC: Wand 4 mm, Boden 5 mm, Randsims 20 x 14 mm; Sperrboden PP 8 mm OHNE Lochung auf 15 (innen, 5 x 3) bzw. 24 (aussen, 8 x 3) Stuetzkloetzen 60 x 60 (Abstand <= 420 mm), einzige Oeffnung = Plattenhuelse (Tankverbinder D36, Flansch D50 auf der Wasserseite, Reduzierhuelse 32/25); Medium 300 mm (EIN Koerper) mit Oberflaeche 75 mm unter dem Rand, Ausschnitte d110 fuer Medienschutz und Reinigungsschacht; Glockensiphon: Standrohr d25, Glocke d75 x 295 (4 Kerben 10 x 12 am Fuss, Luftloch 10), Medienschutz Lochblech V2A d110 x 1,5 x 320 (Modell: 2 Ringe x 12 Schlitze 5 x 50) mit loser Kappe; Reinigungsschacht PVC-U/KG d110 x 3, Oberkante 20 mm ueber dem Medium, Kappe, 2 Kerben 30 x 30; Reduktion d40 x d25 unter dem Bulkhead (Port z -30).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| aussen_933: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25) mit Reduktion d40 x d25 (Muffe d25 oben, Stutzen d40 unten, 50 mm [A]); Tankverbinder D36/Flansch D50 mit Reduzierhuelse 32/25 | x 1252, y 0, z -30 | Wasser verlaesst das Beet nach unten (Oeffnung zeigt -Z; Beet ist eingelassen, Ablauf unter dem Wannenboden) |
| aussen_933: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -1516, y -392, z 612 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Rohr liegt laengs, nicht quer (Auslegung E: 2,9 m Beetlaenge) |
| aussen_993: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25) mit Reduktion d40 x d25 (Muffe d25 oben, Stutzen d40 unten, 50 mm [A]); Tankverbinder D36/Flansch D50 mit Reduzierhuelse 32/25 | x 1252, y 0, z -30 | Wasser verlaesst das Beet nach unten (Oeffnung zeigt -Z; Beet ist eingelassen, Ablauf unter dem Wannenboden) |
| aussen_993: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -1516, y -422, z 612 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Rohr liegt laengs, nicht quer (Auslegung E: 2,9 m Beetlaenge) |
| innen_933: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25) mit Reduktion d40 x d25 (Muffe d25 oben, Stutzen d40 unten, 50 mm [A]); Tankverbinder D36/Flansch D50 mit Reduzierhuelse 32/25 | x 708, y 0, z -30 | Wasser verlaesst das Beet nach unten (Oeffnung zeigt -Z; Beet ist eingelassen, Ablauf unter dem Wannenboden) |
| innen_933: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -972, y -392, z 624 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Rohr liegt laengs, nicht quer (Auslegung E: 2,9 m Beetlaenge) |
| aussen_800: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25) mit Reduktion d40 x d25 (Muffe d25 oben, Stutzen d40 unten, 50 mm [A]); Tankverbinder D36/Flansch D50 mit Reduzierhuelse 32/25 | x 1096, y 0, z -30 | Wasser verlaesst das Beet nach unten; Lage aus der Messung (Siphon 200 mm vor dem Ablaufende) |
| aussen_800: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -1360, y -326, z 612 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Lage aus der Messung (Rohr 50 mm von der Innenwand) |
| aussen_933: Reinigungszugang (Reinigungsschacht d110 mit Kappe) | Rohr d110 (KG/HT DN100), Saugschlauch d <= 75 | x -1202.5, y 0, z Plattenoberkante bis Medium + 20 | Zugang von oben (Kappe abnehmen); 2 Kerben 30 x 30 am Fuss lassen Wasser und Schlamm vom Plattenfilm in den Schacht |
| aussen_993: Reinigungszugang (Reinigungsschacht d110 mit Kappe) | Rohr d110 (KG/HT DN100), Saugschlauch d <= 75 | x -1202.5, y 0, z Plattenoberkante bis Medium + 20 | Zugang von oben (Kappe abnehmen); 2 Kerben 30 x 30 am Fuss lassen Wasser und Schlamm vom Plattenfilm in den Schacht |
| aussen_800: Reinigungszugang (Reinigungsschacht d110 mit Kappe) | Rohr d110 (KG/HT DN100), Saugschlauch d <= 75 | x -1046.0, y 0, z Plattenoberkante bis Medium + 20 | Zugang von oben (Kappe abnehmen); 2 Kerben 30 x 30 am Fuss lassen Wasser und Schlamm vom Plattenfilm in den Schacht |
| innen_933: Reinigungszugang (Reinigungsschacht d110 mit Kappe) | Rohr d110 (KG/HT DN100), Saugschlauch d <= 75 | x -658.5, y 0, z Plattenoberkante bis Medium + 20 | Zugang von oben (Kappe abnehmen); 2 Kerben 30 x 30 am Fuss lassen Wasser und Schlamm vom Plattenfilm in den Schacht |

## Verbindungen und Befestigungen

- Standrohr d25 steckt in der Reduzierhuelse 32/25 (Klebemuffe d25), diese klebt im Tankverbinder D36 mit Klebemuffe d32 und Flansch D50 (Dichtung, Kontermutter unter dem Boden); Entscheidung Ben 04.11.2026 (D77)
- Plattenhuelse im Sperrboden: gleicher Tankverbinder mit Reduzierhuelse, Flansch D50 auf der Wasserseite (Plattenoberkante), Gewinde 3 mm unter der Platte fuer die Kontermutter; Plattenrand gegen die Wanne mit EPDM-Zellkautschuk abgedichtet (Spalt 2 mm, Mass offen)
- Reduktion d40 x d25 klebt mit der Muffe d25 auf dem Standrohrende (Port z -30), Stutzen d40 unten fuer den Einzelabgang (PVC-U Klebeverbindung nach DIN EN 14814)
- Glocke, Medienschutz (Lochblech 5 mm vom Metallbauer, Kappe lose) und Reinigungsschacht (Kappe lose) stehen lose auf dem Sperrboden; Sperrboden (8 mm, ungelocht) liegt auf 15/24 Stuetzkloetzen
- Zulauf-Tropfrohr durch eine Durchfuehrung D22 in der Stirnwand (Dichtung Gummituelle), Endstopfen am Ende

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Aussenmass 2953 x 933/993 x 637 bzw. 1865 x 933 x 649 | mm | OBJ | layout.json ibc_beds (Laenge, Breite, Hoehe) | hoch |
| Unterkante Z -162 (aussen) / -173..-209 (innen) | mm | OBJ | layout.json ibc_beds z0 (Integrator setzt; im Bauteil Ursprung = Wannenunterseite) | hoch |
| Wandstaerke 4 mm, Boden 5 mm | 4 / 5 mm | R03 + A | R03 nennt 3-4 mm nur als Folgerung fuer das Modell (Scope-Card), keine eigene Quelle; Boden Annahme | mittel |
| Randsims 20 x 14 mm | 20 / 14 | Bild + A | ref-5/ref-6: breiter flacher Randsims der weissen Wannen (Bild-Kritiker) | niedrig |
| Eckenradius 40 mm | 40 | Bild + A | ref-5 (gerundete Ecken der IBC-Wannen) | niedrig |
| Medientiefe 300 mm, Oberflaeche Z 400 (75 mm unter dem Rand) | 300 | R03 | docs/research/R03.md (FarmHub 30 cm Fruchtgemuese; Z 400 Vorgabe Orchestrator) | mittel |
| Medium als EIN Koerper | 1 Koerper | R03/Scope-Card | Scope-Card ibc_beet: Medium als EIN Koerper | hoch |
| Stuetzkloetze 60x60, 15 (innen) / 24 (aussen) | 60 x 60 | A | Konstruktionspraxis; Abstand <= 420 mm wegen Medienlast (Bild-Kritiker); Luftraum unter dem Sperrboden (trocken, V3/D77) | niedrig |
| Standrohr d25, 265 mm ueber Medienunterkante (Variante FarmHub 220) | 25 / 265 | Orchestrator + R03 | Vorgabe media_depth - 35 mm (29.10.), FarmHub 220 als Variante; R03 Befund 5 widerspricht Befund 4/SRAC | mittel |
| Zulauf-Tropfrohr d20 auf Z 450 (25 mm unter dem Rand) | 20 | R03 + A | R03: Zulaufrohr auf Z 450; Durchmesser Annahme | niedrig |
| Zulauf 200-500 l/h je Beet | 200-500 l/h | R03 | docs/research/R03.md (Glockensiphon-Auslegung) | mittel |
| Anzahl 8 aussen (5 x 933, 3 x 993), 6 innen | 14 | OBJ | layout.json ibc_beds | hoch |
| Werkstoffe: Wanne HDPE 0,95; Siebboden/Stuetzen PP 0,91; Rohre PVC-U 1,4; Medium 0,9 (trocken) | 0,95 / 0,91 / 1,4 / 0,9 g/cm3 | Bild + A | ref-5/6 weisse Wannen; Normwerte Kunststoffe; Medium Mittelwert | mittel |
| Medium-Spiel zur Wannenwand | 2 mm | A | Konstruktionspraxis | niedrig |
| Tropfloecher 4 x 4 mm, Teilung 200 mm, ab 150 mm von der Stirn | 4 / 200 mm | A | R03: gelochtes Rohr oder Tropfschlauch; Raster Annahme | niedrig |
| Zulauf-Wanddurchfuehrung D22 in der Stirnwand (Rohr d20) | D22 | A | Konstruktionspraxis (Gummitulle); y = -(Wi/2 - 50) | niedrig |
| Zulaufrohr liegt laengs (nicht quer), 25 mm unter dem Rand | z 612 lokal / 450 abs. | R03 + E | R03: 'quer ueber das Beet auf Z 450'; bei 2,9 m Laenge laengs ausgelegt (E) | niedrig |
| Aussenbeet 800 x 2640 x 637 (aussen_800) | 800 / 2640 / 637 mm | Ben + E | D29: einseitig erreichbar <= 800; Laenge 2640 = Obergrenze aus der Montage-Rechnung (D25/D28 outer_bed_len), Hoehe wie OBJ; Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 60 = 2851 (corner_gap 60, W17; mit 100: 2771) | mittel |
| Sperrboden 8 mm ungelocht (V3) | 8 mm, 0 Loecher | Ben D77 + R51 | docs/jobs/W40-BEET.md (Variante V3, D77 04.11.2026); R51 Befund 5a (stehendes Wasser unter dem Siebboden) | mittel |
| Glocke d75 x 295 mit 4 Kerben 10 x 12 am Fuss, Luftloch 10 | d75 x 295; 4 x 10 x 12 | R03 + W40 | R03: d75, Luftloch 10; Kerben statt Schlitzen 10 x 40 (W40-BEET V3, Kerbenflaeche 480 mm2 >= Standrohr 380 mm2) | mittel |
| Medienschutz Lochblech V2A d110 x 1,5 x 320, lose Kappe | d110 x 320 | R51 + Ben D77 | R51 T30e-4 (Rundloch d5, Teilung 8, 35 % offen); Modell 2 Ringe x 12 Schlitze 5 x 50 = 6000 mm2 = 15,8 x Standrohr; Zuschnitt und Rollen beim Metallbauer | mittel |
| Reinigungsschacht d110 x 3 stehend auf dem Sperrboden, Kappe, 2 Kerben 30 x 30 | d110 x 320 | R51 + W40 | R51 T30e-5, geaendert: stehend auf dem Sperrboden statt Loch in der Platte (W40-BEET.md Abschnitt Aenderungen, Punkt 4) | mittel |
| Reduktion d40 x d25, Bauhoehe 50 mm | d40 / d25 / 50 | R51 + A | R51 T30e-3; Bauhoehe [A], Kaufmass pruefen | niedrig |
| Tankverbinder D36/Flansch D50 mit Reduzierhuelse 32/25 (Boden und Platte) | D36 / D50 / 32/25 | Ben D77 + A | D77: Standrohr d25 mit Reduzierhuelse 32/25 im Tankverbinder; Tankverbinder-Maße [A] (Bevo Art. 7018227 [Q], Reduzierhuelse Bevo 7002656 / Schwarte 75208) | niedrig |
| Wandstaerken Rohre: Standrohr 2, Glocke 3, Schacht 3, Lochblech 1,5, Tropfrohr 2 | 2 / 3 / 3 / 1,5 / 2 mm | A | PVC-U/PE Rohre Normwanddicken ungefaehr; Lochblech 1,5 mm laut R51/ehorst Art. 1003438 | niedrig |
| Gewichtsrechnung: leer ohne Medium, Medium 0,9, Wasser nur Porenwasser bis Standrohrkante (40 % Poren) | siehe Gewicht | E | Messung aus .sc (eval) und Dichten oben; Porositaet 40 % Annahme; kein Wasserraum unter dem Sperrboden | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-5-dome-closeup.jpg und ref-6 (weisse Wannen mit Rand, Erde/Kies); docs/research/R03.md (Beetaufbau)
- Quelle der Masse: data/layout.json ibc_beds (Laenge, Breite, Hoehe, Z-Unterkante), docs/research/R03.md (Beetaufbau), docs/scope-cards.md ibc_beet; ref-5/ref-6: weisse Wannen mit Rand und Erde/Kies
- Abweichung zum OBJ: OBJ ibc_beds: Laenge/Breite/Hoehe wie layout.json (Messung 0 mm Abweichung); die OBJ-Gruppe heisst IBC_Open_Top, das Mass 2953 x 933-993 x 637 ist ein Sondermass: Bezeichnung im Modell 'IBC-Wanne (Sondermass nach OBJ)', Werkstoff A (Orchestrator-Entscheidung 29.10.); Medium-Hoehe absolut Z 400 laut R03; Beetinnenraum im OBJ nicht modelliert -> Aufbau aus R03. Innenbeete: OBJ z0 -209, -173, -172, -170, -194, -194 (Rand Z 440-479): die Medienoberflaeche liegt absolut bei Z 365-404, nicht einheitlich 400 (Vorpruefung Toleranz 40 mm fuer innen; R03-Z-400 gilt fuer aussen). Innenbeete: OBJ z0 -209, -173, -172, -170, -194, -194 (Rand Z 440-479): die Medienoberflaeche liegt absolut bei Z 365-404, nicht einheitlich 400 (Vorpruefung Toleranz 40 mm fuer innen; R03-Z-400 gilt fuer aussen).

## Montage (L4)

1. Grube ausheben, Wanne einsetzen und waagerecht ausrichten
2. Bohrung D36 in den Boden, Tankverbinder mit Dichtung einsetzen, Reduzierhuelse 32/25 einkleben, Standrohr d25 stecken, Reduktion d40 x d25 unter dem Boden aufkleben
3. Stuetzkloetze einlegen, Sperrboden mit Bohrung D36 auflegen, Plattenhuelse (Tankverbinder mit Reduzierhuelse) einsetzen und kontern, Plattenrand mit EPDM-Zellkautschuk abdichten
4. Dichtheitsmuster: 15 mm Wasser ueber dem Sperrboden, 24 h; Leckwasser unter der Platte waere wieder stehendes Wasser
5. Glocke, Medienschutz (Lochblech) und Reinigungsschacht lose aufsetzen, Kappen aufsetzen
6. Zulauf-Tropfrohr durch die Stirnwand fuehren und abdichten
7. Medium (gewaschen, Blaehton 8-16 reicht bei Schutz 5 mm) einfuellen bis 75 mm unter den Rand, Ausschnitte d110 freihalten
8. Zulauf anschliessen und Zyklus pruefen (Anspringen bei 3,3 l/min nur am Muster pruefbar); Netztoepfe und Pflanzen setzt der Integrator als Instanzen nach layout.json (nicht Teil des Beets)

**Werkzeug:** Bohrmaschine mit Lochsaege D36, Saege (Standrohr, Glocke, Schacht, Kerben), Entgrater, Wasserwaage, Schaufel, Silikon/Dichtung, PVC-Kleber nach DIN EN 14814

## Stueckliste-Zeile

- T30a Wanne HDPE (Sonderwanne 2953/1865 mm): 1 je Beet; 14 gesamt (aussen 8: 5 x 933 + 3 x 993, innen 6)
- T30b Stuetzkloetze PP 60x60: 24 (aussen) / 15 (innen) je Beet
- T30c Sperrboden PP 8 mm, ungelocht (nur Durchfuehrung D36): 1 je Beet; Plattenhuelse (Tankverbinder D36 mit Flansch D50 + Reduzierhuelse 32/25 + Kontermutter): 1 je Beet; Dichtband Plattenrand
- T30d Medium Blaehton 8-16 mm: aussen_800 575 l (517 kg); innen_933 467 l (420 kg); aussen_933 761 l (685 kg); aussen_993 813 l (732 kg) (Messung `solidcraft-cli eval`)
- T30e Siphon: 1 Tankverbinder D36 mit Flansch D50 + Reduzierhuelse 32/25 + Dichtung + Kontermutter, 1 Standrohr PVC-U d25 (Laenge 30 + 527 mm), 1 Reduktion kurz d40 x d25, 1 Glocke PVC-U d75 x 295 mit Deckel und 4 Kerben, 1 Medienschutz Lochblech V2A 1.4301 1,5 mm (Rundloch 5, Teilung 8) d110 x 320 mit loser Kappe DN110
- T30f Zulauf: 1 Tropfrohr PE d20 (Laenge siehe Messung), 1 Endstopfen d20, 1 Gummituelle D22 fuer die Wanddurchfuehrung, 1 Anschluss-Kupplung d20
- T30g Reinigungsschacht: 1 KG/HT-Rohr DN100 (Aussen-D 110) x 3, Laenge etwa 320 mm (ab Platte), 1 Muffenstopfen DN110
- Normbezeichnungen: PVC-U Rohr nach DIN 8062 / EN 1452; PE-Rohr nach DIN 8074; Kleber nach DIN EN 14814; Medium gewaschen
- T30 aussen_800 (W17/D29): 8 Beete 800 x 2640 x 637 statt 5 x 933 + 3 x 993 x 2953; Wannen-Sondermass (HDPE), Siphon wie die anderen Aussenbeete

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Reduktion kurz 40 x 25 | PVC-U Klebefitting mit Klebstutzen und Klebmuffe | Weinmann-Schanz (DE) Bestell-Nr. 93 049 64 [R51]; Georg Fischer (CH) TP PVC-U Reduzierung D40AG-D25IG ueber Vanmarcke (BE) [R51] | beschaffbar (Bauhoehe etwa 50 mm [A] aus Datenblatt noch zu pruefen) |
| Standrohr d25 x 1,5 | PVC-U Druckrohr PN10, ISO 4422 | Bevo (NL/BE) Druckrohr PVC-U 25 mm x 1,5 mm Klebemuffe x glatt 10 bar ISO-PN10 grau 5 m, Art. 0309025 [R51/R45] | beschaffbar |
| Glocke d75 | PVC-U Rohr d75 (2,9 oder 3,6 mm) plus Klebekappe d75, Laenge 295 mm saegen, 4 Kerben 10 x 12 saegen | Bevo Druckrohr PVC-U 75 mm x 2,9 mm Art. 7027594 bzw. x 3,6 mm Art. 0309175 [Q]; Kappe Bevo Art. 0160592 [Q], Klebefitting-Kappen auch bei Schwarte (DE) | beschaffbar; Modell rechnet Wand 3 mm: auf 2,9 oder 3,6 mm abstimmen |
| Schutzkorb Lochblech | Edelstahl 1.4301, 1,5 mm, Rundloch 5 mm, Teilung 8, Zuschnitt etwa 366 x 340 mm, gerollt, genietet | ehorst.de (DE) Lochblech Edelstahl 1.4301 RV 5-8 1,50 1000 x 2000 mm DIN 24041, Art. 1003438 [R51]; Zuschnitt und Rollen beim Metallbauer (Entscheidung Ben 04.11.2026, D77) | beschaffbar als Tafelware; Anfrage Metallbauer: Ben (offen) |
| Kappe Schutzkorb und Schacht (lose) | Muffenstopfen DN110, PVC-U/PP | Ostendorf (DE) KG Muffenstopfen DN/OD 110, Art. 220620 und HT-Safe M Muffenstopfen PP D110 (ueber Vanmarcke) [Q]; Hornbach Art. 267389/267185 [Q] | beschaffbar |
| Reinigungsschacht d110 | KG/HT-Rohr DN100 (Aussen-D 110) x 3, Laenge etwa 320 mm ab Platte | Artikel nicht nachgewiesen: KG-Rohr DN/OD 110 gibt es als Ostendorf KG 2000 (DN/OD 110 bis 630, 1000 mm, Muffe) [Q-Treffer ebay.de/crassus.de, kein Artikel gelesen]; Hersteller und Artikelnummer beim Kauf eintragen (Wavin/Funke/Ostendorf) | beschaffbar (Rohrklasse); Artikel nicht nachgewiesen; Laenge 320 mm ab Platte (Modell z 262 bis 582 lokal fuer 300 mm Medium + 20) |
| Tankverbinder (Wannenboden und Sperrboden) | PVC-U Tankverbinder 32 mm x 1 Zoll, Klebemuffe d32 x Aussengewinde, 10 bar; im Modell D36 mit Flansch D50 [A] | Georg Fischer/VDL ueber Bevo Art. 7018227 [Q]; Koi-Breeder PVC-U tank bushing [Q] | beschaffbar; Flanschmass D50 [A]: Datenblatt nicht gelesen (M-BEET-TAUSCH Auflage 5); Hinweis: VDL fuehrt 32 mm x 1 1/4 Zoll (Bevo 0100560), ein 32 x 1 Zoll Verbinder ist ueber Epco/Pipestock (UK) belegt, nicht ueber Bevo |
| Reduzierhuelse 32 x 25 (im Tankverbinder, je Beet 2 Stueck) | PVC-U Klebefitting Reduktion kurz 32 x 25, Stutzen 32 / Muffe 25, 16 bar | Schwarte (DE) Art. 75208; Bevo (NL/BE) VDL reducer bush PVC-U 32 x 25 mm Art. 7002656, Baulaenge 22 mm [Bevo-Katalogzeile, Datenblatt nicht gelesen] | beschaffbar (zwei Haendler); Baulaenge 22 mm: Bevo-Katalogzeile und Georg-Fischer-Angabe 'Length 22 mm' ueber RS-Suchtreffer (Seite 403, nicht gelesen); Auflage 5 M-BEET-TAUSCH: Datenblatt nicht gelesen, [A]; Modell Huelse Platte 15 / Boden 39 mm (Abweichung siehe docs/packages/m-beet-tausch.md) |
| Dichtband Plattenrand | EPDM-Zellkautschuk geschlossenzellig, selbstklebend; Spalt 2 mm | Steinbach & Vollmann (stuv.de, DE) EPDM-Zellkautschuk selbstklebend, wasserdicht laut Datenblatt; Graf-Dichtungen (DE) Moosgummi Vierkant 10 x 10 mm Z0701 ist NICHT selbstklebend (selbstklebend erst 10 x 20) | nicht beschafft (Mass offen); Werkstoff EPDM-Zellkautschuk geschlossenzellig, selbstklebend, beschaffbar; Mass z. B. 10 x 3 mm verpresst oder 10 x 20 Graf vor Bau festlegen; Quelle: Bezugsquellen-Nachtrag W40-BEET.md |
| Kleber PVC-U | Klebstoff nach DIN EN 14814 | Henkel Tangit PVC-U Plus (Technisches Merkblatt, DIN EN 14814, EN 1452); toom Rohrklebstoff PVC-U Plus 125 g, Art. 8150236 | beschaffbar |

## Alternative lokale Fertigung

Wanne: halbe IBC (1000-l-Container, Innenbehaelter HDPE) aufgeschnitten oder Kunststoffwanne; Sperrboden: PP-Platte 8 mm vom Zuschnitt; Siphon, Glocke und Schacht aus PVC-Rohr-Standardteilen (d25/d75/d110, saegen und kleben); Schutzkorb: Lochblech 5 mm vom Metallbauer (Rollen, Nieten), Rueckfall gebohrtes PVC-Rohr (Selbstbau, nicht super simpel).

## Renders

- `renders/components/ibc_beet_aussen_933/ibc_beet_aussen_933-01-iso.png`
- `renders/components/ibc_beet_aussen_933/ibc_beet_aussen_933-02-siphon.png`
- `renders/components/ibc_beet_aussen_933/ibc_beet_aussen_933-03-zulauf.png`
- `renders/components/ibc_beet_aussen_933/ibc_beet_aussen_933-04-medium.png`
- `renders/components/ibc_beet_aussen_933/ibc_beet_aussen_933-05-schnitt.png`
- `renders/components/ibc_beet_aussen_933/ibc_beet_aussen_933-06-schnitt-quer.png`
- `renders/components/ibc_beet_aussen_993/ibc_beet_aussen_993-01-iso.png`
- `renders/components/ibc_beet_aussen_993/ibc_beet_aussen_993-02-siphon.png`
- `renders/components/ibc_beet_aussen_993/ibc_beet_aussen_993-03-zulauf.png`
- `renders/components/ibc_beet_aussen_993/ibc_beet_aussen_993-04-medium.png`
- `renders/components/ibc_beet_aussen_993/ibc_beet_aussen_993-05-schnitt.png`
- `renders/components/ibc_beet_aussen_993/ibc_beet_aussen_993-06-schnitt-quer.png`
- `renders/components/ibc_beet_innen_933/ibc_beet_innen_933-01-iso.png`
- `renders/components/ibc_beet_innen_933/ibc_beet_innen_933-02-siphon.png`
- `renders/components/ibc_beet_innen_933/ibc_beet_innen_933-03-zulauf.png`
- `renders/components/ibc_beet_innen_933/ibc_beet_innen_933-04-medium.png`
- `renders/components/ibc_beet_innen_933/ibc_beet_innen_933-05-schnitt.png`
- `renders/components/ibc_beet_innen_933/ibc_beet_innen_933-06-schnitt-quer.png`

## Pruefung

- Gauntlet-Urteil: offen
- scripts/w40_beet_rechnung.py (Film, Ablaufvolumen, Entleerzeit, Flutzeit; Ausgabe im Paket docs/packages/w40-beet.md)
- scripts/workshop/check_ibc_beet.py (alle vier Typen, inklusive Interferenz je Typ; Ergebnis im Paket)
- Triage in docs/workshop-log.md

## Offene Fragen

- Dichtheit des Sperrbodens (Plattenrand, Plattenhuelse) und Anspringen des Siphons bei 3,3 l/min nur am Muster pruefbar; Leckwasser unter der Platte waere wieder stehendes Wasser
- Luftkammer unter dem Sperrboden (262 bis 274 mm hoch) bleibt ungenutzt und trocken; Alternative "IBC kuerzer schneiden" waere ein Layout-Eingriff (Z-Hoehen, Tische R35/R36), nicht Teil von W40-BEET
- Dichtband-Mass offen (EPDM-Zellkautschuk selbstklebend, Spalt 2 mm; 10 x 10 selbstklebend nicht nachgewiesen)
- Reduzierhuelse 32/25: Baulaenge 22 mm (Bevo-Katalogzeile) gegen Huelsenlaenge im Modell (Boden 39 mm, Platte 15 mm); Modell vereinfacht, Datenblatt nicht gelesen
- Schutzkorb: Anfrage Metallbauer (Zuschnitt, Rollen) liegt bei Ben; Lochblech im Modell als Schlitze 5 x 50 vereinfacht (real Rundloch d5, Teilung 8)
- Flansch D50, Tankverbinder-Aussenmass D36, Reduktions-Bauhoehe 50 mm, Wandstaerken Rohre: Annahmen [A], Datenblaetter der Kaufteile nicht gelesen
- Optionale Nachlaufbohrung d4 im Standrohr nur wenn der Film am Muster zu gross ist (Rechnung 0,5 bis 1,0 l/min je nach Ausflussbeiwert)
- Orchestrator/Montage: Netz K14/K30 `hoehe` (Beetablauf Achse etwa -260 aussen / -290 innen statt -100) und Sumpf-Einlauf; Systemwasserbilanz und Gewichte ohne Wasserraum (rund 6280 l weniger); Montage baut 14 Beete im Dom neu; `data/descriptions.json` (Beet-Beschreibung nennt noch Schlitze, Siebboden, Standrohr 220) nachziehen
- Pflanzen: 288 je Aussenbeet (Beet bei Azimut 113: 144) sind Instanzen des Integrators; Pflanzraster/Topfzahl aussen_800 und Innenbeete rechnet die Montage (M7) neu
- Seitenloecher/Tropfloecher/Luftloch quadratisch modelliert (Rechenzeit), real rund; Tropfrohr-Halterung am Wannenrand und Zulauf-Wanddurchfuehrung (Fitting/Dichtung) nicht modelliert
- W17: aussen_800 (800 x 2640) ist das Zielmass nach D29; layout.json/gen_dome tragen noch 933/993 x 2953 (Montage M7 setzt Layout und Dom um)
- W26 (D44): Innenbeet innen_933 hat 45-Grad-Eckenfasen 120 mm am Randwulst-Umriss; Zulauf-Tropfrohr liegt vor der Fase (check_ibc_beet prueft)

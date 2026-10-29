# Bauteilblatt T30 ibc_beet (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/ibc_beet.json` und `designs/components/ibc_beet.sc`, nicht von Hand aendern)

**Funktion:** Substratbeet (Fluten und Entleeren per Glockensiphon): Pflanzen (Instanzen; 288 je Aussenbeet, Beet bei Azimut 113 hat 144) in Netztoepfen im Medium (Blaehton/Kies), Wasser fliesst ueber das Tropfrohr zu, der Glockensiphon entleert das Beet in Zyklen; zugleich Biofilterflaeche.

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
| `grid_t` | 8 | mm | [A] Siebboden 8 mm (PP-Lochplatte), Stuetzenabstand <= 420 mm (Bild-Kritiker: Traglast Medium) |
| `grid_hole` | 12 | mm | [A] Lochdurchmesser Siebboden, vereinfacht (real Lochblech D8, kleiner als Korn 8-20) |
| `grid_nx` | 20 |  | [A] Loecher je Reihe (vereinfacht) |
| `grid_ny` | 5 |  | [A] Lochreihen (vereinfacht) |
| `post` | 60 | mm | [A] Stuetzklotz 60 x 60 unter dem Siebboden |
| `post_nx` | 8 |  | [A] Stuetzen in Laengsrichtung: aussen 8, innen 5; 3 Reihen (y = +-(Wi/2-100) und 0) |
| `standpipe_d` | 25 | mm | R03: Standrohr D25 (FarmHub 2,5 cm PVC) |
| `standpipe_over` | 265 | mm | Orchestrator 29.10.: standpipe_h = media_depth - 35 mm = 265 ueber der Medienunterkante (Wasserstand 35 mm unter der Oberflaeche, dazwischen SRAC 1 Zoll = 25 mm / R03 trockene Zone 2-5 cm); Variante FarmHub 220 (R03 Befund 5, widerspricht Befund 4); Gesamtlaenge ab Bulkhead = Stuetzhoehe + 265 [E] |
| `standpipe_wall` | 2 | mm | [A] PVC-Rohr d25 |
| `bell_d` | 75 | mm | R03: Glocke D75 |
| `bell_h` | 295 | mm | [E] Glocke = Standrohrhoehe + 30 mm (R03: 250 bei Standrohr 220); oben verschlossen |
| `bell_wall` | 3 | mm | [A] PVC-Rohr d75 |
| `bell_slot_w` | 10 | mm | R03: zwei Schlitze 10 x 40 mm |
| `bell_slot_h` | 40 | mm | R03 |
| `bell_slot_z` | 15 | mm | R03: Schlitze 15 mm ueber der Glockenunterkante |
| `air_hole` | 10 | mm | R03: Luftloch D10, 50 mm ueber dem Unterrand (quadratisch 10 x 10 modelliert) |
| `guard_d` | 110 | mm | R03: Medienschutz D110 |
| `guard_h` | 320 | mm | R03: Medienschutz 320 hoch |
| `guard_wall` | 3 | mm | [A] PVC-Rohr d110 |
| `guard_hole` | 12 | mm | R03: kleine Seitenloecher; modelliert als 12 x 12 mm Durchbrueche, 12 Stueck (3 Ringe x 4) [A] |
| `bulkhead_d` | 36 | mm | [A] Durchfuehrung fuer Standrohr d25 (Gewindehuelse D36) |
| `bulkhead_flange` | 50 | mm | [A] Flansch D50 |
| `inflow_d` | 20 | mm | [A] Zulauf-Tropfrohr D20 (PE), Zulauf 200-500 l/h je Beet (R03) |
| `inflow_wall` | 2 | mm | [A] |
| `inflow_below_rim` | 25 | mm | R03: Zulaufrohr auf Z 450 = 25 mm unter OBJ-Oberkante Z 475 |
| `inflow_hole` | 4 | mm | [A] Tropfloecher 4 x 4 mm (quadratisch modelliert, real D4) |
| `inflow_pitch` | 200 | mm | [A] Tropflochabstand |

| Typ | laenge | breite | hoehe | anzahl | herkunft |
|---|---|---|---|---|---|
| aussen_933 | 2953 | 933 | 637 | 5 | layout.json ibc_beds 3-7: 2953 x 933 x 637 |
| aussen_993 | 2953 | 993 | 637 | 3 | layout.json ibc_beds 1, 2, 8: 2953 x 993 x 637 |
| innen_933 | 1865 | 933 | 649 | 6 | layout.json ibc_beds 9-14: 1865 x 933 x 649 |
| aussen_800 | 2640 | 800 | 637 | 8 | W17/D29: Aussenbeet einseitig erreichbar <= 800 breit; Laenge 2640 = Obergrenze aus der Montage-Rechnung (Streben/Sockel, D25; Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 100 = 2771); Hoehe wie OBJ 637; ersetzt aussen_933/aussen_993 im Dom (Montage M7 stellt um) |

Gesamt-Box (Messung, Variante ibc_beet_aussen_933): X -1516.5 bis 1476.5, Y -466.5 bis 466.5, Z -30.0 bis 637.0 mm; Koerper: 33.

**Toleranzen / Spiel:** Medium 2 mm Spiel zur Wanne; Wasserstand in der Flutphase = Standrohrkante, 265 mm ueber der Medienunterkante = 35 mm unter der Medienoberflaeche (Orchestrator-Vorgabe 29.10.: media_depth - 35; FarmHub-Variante 220 = 80 mm unter der Oberflaeche, R03 Befund 5); R03 Befund 4 nennt eine trockene Oberzone von 2-5 cm, SRAC 5007 einen Wasserstand 1 Zoll unter der Oberflaeche -> Abweichung 3-6 cm, siehe offen.

## Werkstoff und Gewicht

- Werkstoff: HDPE weiss (Wanne), PVC grau (Rohre), Kies/Blaehton (Medium), Dichte 0.95 g/cm3, Farbe #e9ebe8 (ref-5/ref-6 weisse Wannen (HDPE IBC-Innenbehaelter 0,95 g/cm3); Siebboden/Stuetzen PP 0,91, Rohre PVC-U 1,4 g/cm3)
- Volumen (Messung, Variante ibc_beet_aussen_933, `solidcraft-cli eval`): 76926.0 cm3 · Masse leer (ohne Medium): 71827 g (71.83 kg)
- Variante `ibc_beet_aussen_933`: 71.83 kg leer (ohne Medium)
- Variante `ibc_beet_aussen_993`: 74.24 kg leer (ohne Medium)
- Variante `ibc_beet_aussen_800`: 61.91 kg leer (ohne Medium)
- Variante `ibc_beet_innen_933`: 47.75 kg leer (ohne Medium)
- Gefuellt/in Betrieb: aussen_933: leer ohne Medium 72 kg; Medium 764 l = 687 kg (Schuettdichte 0,9 [A]); Wasser bis Standrohrkante 911 l = 911 kg (Wasserraum unter dem Siebboden 640 l + Porenwasser 271 l bei 40 % Porositaet [A]); gefuellt gesamt 1670 kg | aussen_993: leer ohne Medium 74 kg; Medium 816 l = 734 kg (Schuettdichte 0,9 [A]); Wasser bis Standrohrkante 973 l = 973 kg (Wasserraum unter dem Siebboden 684 l + Porenwasser 289 l bei 40 % Porositaet [A]); gefuellt gesamt 1781 kg | innen_933: leer ohne Medium 48 kg; Medium 476 l = 428 kg (Schuettdichte 0,9 [A]); Wasser bis Standrohrkante 589 l = 589 kg (Wasserraum unter dem Siebboden 420 l + Porenwasser 169 l bei 40 % Porositaet [A]); gefuellt gesamt 1065 kg | aussen_800: leer ohne Medium 62 kg; Medium 578 l = 520 kg (Schuettdichte 0,9 [A]); Wasser nicht gerechnet (wie aussen_933 skaliert ca. 0,8 x)

## Querschnitt / Profil

Wanne halbe IBC: Wand 4 mm, Boden 5 mm, Randsims 20 x 14 mm; Siebboden 8 mm auf 15 (innen, 5 x 3) bzw. 24 (aussen, 8 x 3) Stuetzkloetzen 60 x 60 (Abstand <= 420 mm); Medium 300 mm (EIN Koerper) mit Oberflaeche 75 mm unter dem Rand; Glockensiphon: Standrohr d25, Glocke d75 x 295 (2 Schlitze 10 x 40, Luftloch 10), Medienschutz d110 x 320 (12 Durchbrueche 12 x 12).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| aussen_933: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25, etwa DN20), Bulkhead D36 mit Flansch D50 | x 1252, y 0, z -30 | Wasser verlaesst das Beet nach unten (Oeffnung zeigt -Z; Beet ist eingelassen, Ablauf unter dem Wannenboden) |
| aussen_933: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -1516, y -392, z 612 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Rohr liegt laengs, nicht quer (Auslegung E: 2,9 m Beetlaenge) |
| aussen_993: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25, etwa DN20), Bulkhead D36 mit Flansch D50 | x 1252, y 0, z -30 | Wasser verlaesst das Beet nach unten (Oeffnung zeigt -Z; Beet ist eingelassen, Ablauf unter dem Wannenboden) |
| aussen_993: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -1516, y -422, z 612 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Rohr liegt laengs, nicht quer (Auslegung E: 2,9 m Beetlaenge) |
| innen_933: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25, etwa DN20), Bulkhead D36 mit Flansch D50 | x 708, y 0, z -30 | Wasser verlaesst das Beet nach unten (Oeffnung zeigt -Z; Beet ist eingelassen, Ablauf unter dem Wannenboden) |
| innen_933: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -972, y -392, z 624 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Rohr liegt laengs, nicht quer (Auslegung E: 2,9 m Beetlaenge) |
| aussen_800: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25 (PVC-U d25, etwa DN20), Bulkhead D36 mit Flansch D50 | x 1096, y 0, z -30 | Wasser verlaesst das Beet nach unten; Lage aus der Messung (Siphon 200 mm vor dem Ablaufende) |
| aussen_800: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE d20, etwa DN15), 200-500 l/h (R03) | x -1360, y -326, z 612 | Wasser tritt von aussen ein (Oeffnung zeigt -X); Lage aus der Messung (Rohr 50 mm von der Innenwand) |

## Verbindungen und Befestigungen

- Standrohr steckt in der Bulkhead-Durchfuehrung D36 (Gewindehuelse mit Flansch D50 und Dichtung, Kontermutter unter dem Boden) [A]
- Glocke und Medienschutz stehen lose auf dem Siebboden; Siebboden (8 mm, Rasterlochplatte) liegt auf 15/24 Stuetzkloetzen
- Zulauf-Tropfrohr durch eine Durchfuehrung D22 in der Stirnwand (Dichtung Gummitülle), Endstopfen am Ende

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
| Siebboden 8 mm, Lochraster 20 x 5 D12 (vereinfacht) | 8 / D12 | Scope-Card + A | Scope-Card nennt Siebboden; Raster vereinfacht | niedrig |
| Stuetzkloetze 60x60, 15 (innen) / 24 (aussen) | 60 x 60 | A | Konstruktionspraxis; Abstand <= 420 mm wegen Medienlast (Bild-Kritiker); Wasserraum unter dem Medium ist Annahme | niedrig |
| Standrohr d25, 265 mm ueber Medienunterkante (Variante FarmHub 220) | 25 / 265 | Orchestrator + R03 | Vorgabe media_depth - 35 mm (29.10.), FarmHub 220 als Variante; R03 Befund 5 widerspricht Befund 4/SRAC | mittel |
| Glocke d75 x 295, Schlitze 10x40, Luftloch 10 | d75 x 250 | R03 + E | R03: d75, Schlitze 10x40 (FarmHub); Hoehe 295 = Standrohr 265 + 30 (R03: 250 bei 220) | mittel |
| Medienschutz d110 x 320 mit Seitenloechern | d110 x 320 | R03 | docs/research/R03.md (FarmHub 11 cm, 32 cm) | mittel |
| Bulkhead D36 / Flansch D50 | D36 / Flansch D50 | A | Standrohr d25; Durchfuehrung geschaetzt (Scope-Card: Ablauf-Fitting im Boden) | niedrig |
| Zulauf-Tropfrohr d20 auf Z 450 (25 mm unter dem Rand) | 20 | R03 + A | R03: Zulaufrohr auf Z 450; Durchmesser Annahme | niedrig |
| Zulauf 200-500 l/h je Beet | 200-500 l/h | R03 | docs/research/R03.md (Glockensiphon-Auslegung) | mittel |
| Anzahl 8 aussen (5 x 933, 3 x 993), 6 innen | 14 | OBJ | layout.json ibc_beds | hoch |
| Werkstoffe: Wanne HDPE 0,95; Siebboden/Stuetzen PP 0,91; Rohre PVC-U 1,4; Medium 0,9 (trocken) | 0,95 / 0,91 / 1,4 / 0,9 g/cm3 | Bild + A | ref-5/6 weisse Wannen; Normwerte Kunststoffe; Medium Mittelwert | mittel |
| Wandstaerken Rohre: Standrohr 2, Glocke 3, Medienschutz 3, Tropfrohr 2 | 2 / 3 / 3 / 2 mm | A | PVC-U/PE Rohre d25/d75/d110/d20 Normwanddicken ungefaehr; nicht recherchiert | niedrig |
| Medium-Spiel zur Wannenwand | 2 mm | A | Konstruktionspraxis | niedrig |
| Medienschutz-Durchbrueche 12 x 12 mm, 3 Ringe x 4 (z 40/120/200) | 12 Stueck | R03 + A | R03: kleine Seitenloecher; Anzahl und Form (quadratisch statt rund wegen Rechenzeit) Annahme | niedrig |
| Tropfloecher 4 x 4 mm, Teilung 200 mm, ab 150 mm von der Stirn | 4 / 200 mm | A | R03: gelochtes Rohr oder Tropfschlauch; Raster Annahme | niedrig |
| Zulauf-Wanddurchfuehrung D22 in der Stirnwand (Rohr d20) | D22 | A | Konstruktionspraxis (Gummitulle); y = -(Wi/2 - 50) | niedrig |
| Zulaufrohr liegt laengs (nicht quer), 25 mm unter dem Rand | z 612 lokal / 450 abs. | R03 + E | R03: 'quer ueber das Beet auf Z 450'; bei 2,9 m Laenge laengs ausgelegt (E) | niedrig |
| Gewichtsrechnung: leer ohne Medium, Medium 0,9, Wasser bis Standrohrkante (Sumpf + 40 % Poren) | siehe Gewicht | E | Messung aus .sc (eval) und Dichten oben; Porositaet 40 % Annahme | niedrig |
| Wandstaerken Rohre: Standrohr 2, Glocke 3, Medienschutz 3, Tropfrohr 2 | 2 / 3 / 3 / 2 mm | A | PVC-U/PE Rohre d25/d75/d110/d20 Normwanddicken ungefaehr; nicht recherchiert | niedrig |
| Medium-Spiel zur Wannenwand | 2 mm | A | Konstruktionspraxis | niedrig |
| Medienschutz-Durchbrueche 12 x 12 mm, 3 Ringe x 4 (z 40/120/200) | 12 Stueck | R03 + A | R03: kleine Seitenloecher; Anzahl und Form (quadratisch statt rund wegen Rechenzeit) Annahme | niedrig |
| Tropfloecher 4 x 4 mm, Teilung 200 mm, ab 150 mm von der Stirn | 4 / 200 mm | A | R03: gelochtes Rohr oder Tropfschlauch; Raster Annahme | niedrig |
| Zulauf-Wanddurchfuehrung D22 in der Stirnwand (Rohr d20) | D22 | A | Konstruktionspraxis (Gummitulle); y = -(Wi/2 - 50) | niedrig |
| Zulaufrohr liegt laengs (nicht quer), 25 mm unter dem Rand | z 612 lokal / 450 abs. | R03 + E | R03: 'quer ueber das Beet auf Z 450'; bei 2,9 m Laenge laengs ausgelegt (E) | niedrig |
| Gewichtsrechnung: leer ohne Medium, Medium 0,9, Wasser bis Standrohrkante (Sumpf + 40 % Poren) | siehe Gewicht | E | Messung aus .sc (eval) und Dichten oben; Porositaet 40 % Annahme | niedrig |
| Aussenbeet 800 x 2640 x 637 (aussen_800) | 800 / 2640 / 637 mm | Ben + E | D29: einseitig erreichbar <= 800; Laenge 2640 = Obergrenze aus der Montage-Rechnung (D25/D28 outer_bed_len), Hoehe wie OBJ; Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 100 = 2771 | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-5-dome-closeup.jpg und ref-6 (weisse Wannen mit Rand, Erde/Kies); docs/research/R03.md (Beetaufbau)
- Quelle der Masse: data/layout.json ibc_beds (Laenge, Breite, Hoehe, Z-Unterkante), docs/research/R03.md (Beetaufbau), docs/scope-cards.md ibc_beet; ref-5/ref-6: weisse Wannen mit Rand und Erde/Kies
- Abweichung zum OBJ: OBJ ibc_beds: Laenge/Breite/Hoehe wie layout.json (Messung 0 mm Abweichung); die OBJ-Gruppe heisst IBC_Open_Top, das Mass 2953 x 933-993 x 637 ist ein Sondermass: Bezeichnung im Modell 'IBC-Wanne (Sondermass nach OBJ)', Werkstoff A (Orchestrator-Entscheidung 29.10.); Medium-Hoehe absolut Z 400 laut R03; Beetinnenraum im OBJ nicht modelliert -> Aufbau aus R03. Innenbeete: OBJ z0 -209, -173, -172, -170, -194, -194 (Rand Z 440-479): die Medienoberflaeche liegt absolut bei Z 365-404, nicht einheitlich 400 (Vorpruefung Toleranz 40 mm fuer innen; R03-Z-400 gilt fuer aussen). Innenbeete: OBJ z0 -209, -173, -172, -170, -194, -194 (Rand Z 440-479): die Medienoberflaeche liegt absolut bei Z 365-404, nicht einheitlich 400 (Vorpruefung Toleranz 40 mm fuer innen; R03-Z-400 gilt fuer aussen).

## Montage (L4)

1. Grube ausheben, Wanne einsetzen und waagerecht ausrichten
2. Bohrung D36 in den Boden, Bulkhead mit Dichtung einsetzen, Standrohr stecken
3. Stuetzkloetze einlegen, Siebboden auflegen, Glocke und Medienschutz aufsetzen
4. Zulauf-Tropfrohr durch die Stirnwand fuehren und abdichten
5. Medium (gewaschen, 8-20 mm) einfuellen bis 75 mm unter den Rand
6. Zulauf anschliessen und Zyklus pruefen; Netztoepfe und Pflanzen setzt der Integrator als Instanzen nach layout.json (nicht Teil des Beets)

**Werkzeug:** Bohrmaschine mit Lochsaege D36, Wasserwaage, Schaufel, Silikon/Dichtung

## Stueckliste-Zeile

- T30a Wanne HDPE (Sonderwanne 2953/1865 mm): 1 je Beet; 14 gesamt (aussen 8: 5 x 933 + 3 x 993, innen 6)
- T30b Stuetzkloetze PP 60x60: 24 (aussen) / 15 (innen) je Beet
- T30c Siebboden PP 8 mm (Rasterlochplatte): 1 je Beet
- T30d Medium Blaehton/Kies 8-20 mm: aussen_933 764 l (687 kg); aussen_993 816 l (734 kg); innen_933 476 l (428 kg) je Beet; 14 Beete gesamt ca. 8,4 m3
- T30e Siphon: 1 Bulkhead D36 mit Flansch D50 + Dichtung + Kontermutter, 1 Standrohr PVC-U d25 (Laenge 30 + 527 mm), 1 Glocke PVC-U d75 x 295 mit Deckel, 1 Medienschutz PVC-U d110 x 320
- T30f Zulauf: 1 Tropfrohr PE d20 (Laenge siehe Messung), 1 Endstopfen d20, 1 Gummitulle D22 fuer die Wanddurchfuehrung, 1 Anschluss-Kupplung d20
- Normbezeichnungen: PVC-U Rohr nach DIN 8062 / EN 1452; PE-Rohr nach DIN 8074; Medium gewaschen, Korn 8-20 mm (R03)
- T30 aussen_800 (W17/D29): 8 Beete 800 x 2640 x 637 statt 5 x 933 + 3 x 993 x 2953; Medium 578 l (520 kg bei 0,9 kg/l [A]); leer ohne Medium 62 kg; Wannen-Sondermass (HDPE), Siphon wie die anderen Aussenbeete

## Alternative lokale Fertigung

Wanne: halbe IBC (1000-l-Container, Innenbehaelter HDPE) aufgeschnitten oder Kunststoffwanne; Siebboden: Lochblech/Gitterrost mit Vlies; Siphon aus PVC-Rohr-Standardteilen (d25/d75/d110).

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
- scripts/workshop/check_ibc_beet.py (Ergebnis renders/components/ibc_beet_aussen_933/check.txt)
- Triage in docs/workshop-log.md

## Offene Fragen

- Rolle des Hohlraums unter dem Siebboden (262 mm): R03 nennt Medientiefe 300 bei Behaelter 637 -> Wasserraum/Reservoir [A]
- Standrohrhoehe 265 ueber Medienunterkante (Orchestrator: media_depth - 35), Variante FarmHub 220 mit Glocke 250; R03 gibt 220 bei Medientiefe 300 ohne Wasserraum
- Seitenloecher/Tropfloecher/Luftloch quadratisch modelliert (Rechenzeit), real rund
- Tropfrohr-Halterung am Wannenrand nicht modelliert
- Zulauf-Wanddurchfuehrung ohne Fitting/Dichtung modelliert (nur Bohrung D22, Gummitulle im Blatt)
- Pflanzen: 288 je Aussenbeet (Beet bei Azimut 113: 144; 7 x 288 + 144 = 2160) sind Instanzen des Integrators
- Wasserstand 35 mm unter der Oberflaeche (Standrohr 265; FarmHub 220 = 80 mm) gegen trockene Oberzone 2-5 cm (R03 Befund 4) und SRAC 1 Zoll: Standrohrhoehe als E, Konfidenz niedrig; Siphon steht auf dem Siebboden, darunter ein Wasserraum von 262-274 mm (Annahme A)
- Zulaufrohr laengs statt quer: Auslegung A, vom Orchestrator bestaetigt (29.10.)
- Pflanzen: 288 je Aussenbeet (Beet bei Azimut 113: 144; 7 x 288 + 144 = 2160) sind Instanzen des Integrators
- Wasserstand 35 mm unter der Oberflaeche (Standrohr 265; FarmHub 220 = 80 mm) gegen trockene Oberzone 2-5 cm (R03 Befund 4) und SRAC 1 Zoll: Standrohrhoehe als E, Konfidenz niedrig; Siphon steht auf dem Siebboden, darunter ein Wasserraum von 262-274 mm (Annahme A)
- Zulaufrohr laengs statt quer: Auslegung A, vom Orchestrator bestaetigt (29.10.)
- W17: aussen_800 (800 x 2640) ist das Zielmass nach D29; layout.json/gen_dome tragen noch 933/993 x 2953 (Montage M7 setzt Layout und Dom um); Aussenbeete sind einseitig erreichbar (Domwand), daher <= 800 breit
- W17: Pflanzraster im Aussenbeet: 288 je Beet (24 x 12) passt nicht auf 800 x 2640 (Topfabstand 110 x 67 mm, Kragen 64): Raster/Topfzahl vom Layout/Integrator neu (Substrat-Mindestzahl 152 gesamt ist mit weniger Toepfen erfuellt: R15/D27); NFT-Mindestzahl 459 haengt nicht am Beet

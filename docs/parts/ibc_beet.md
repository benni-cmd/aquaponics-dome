# Bauteilblatt T30 ibc_beet (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/ibc_beet.json` und `designs/components/ibc_beet.sc`, nicht von Hand aendern)

**Funktion:** Substratbeet (Fluten und Entleeren per Glockensiphon): Pflanzen in Netztoepfen im Medium (Blaehton/Kies), Wasser fliesst ueber das Tropfrohr zu, der Glockensiphon entleert das Beet in Zyklen; zugleich Biofilterflaeche.

**Datei:** `designs/components/ibc_beet.sc` · **Teilenummer:** T30 · **Revision:** A · **Bezugspunkt:** Mitte der Wannenunterseite (Z=0), X Laengsachse, Y quer; Wannenoberkante bei Z = hoehe; Medienoberflaeche bei hoehe - rim_gap; Ablaufport unter dem Boden (Z < 0); Wannen sind eingelassen (z0 -162 bis -209, Integrator)

**Anzahl (Instanzen):** aussen 8 (5 x 933, 3 x 993), innen 6 (Quelle: data/layout.json ibc_beds)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `wall` | 4 | mm | R03: Wandstaerke 3-4 mm (Scope-Card ibc_beet) |
| `floor_t` | 5 | mm | [A] Bodenstaerke |
| `corner_r` | 40 | mm | [A] Innenradius der Wannenecken (IBC-Schnitt, ref-5) |
| `rim_w` | 10 | mm | [A] Randwulst: Breite nach aussen |
| `rim_h` | 12 | mm | [A] Randwulst: Hoehe |
| `rim_gap` | 75 | mm | [E] Abstand Medienoberflaeche unter Wannenrand: R03 Z 400 minus OBJ-Oberkante Z 475 |
| `media_depth` | 300 | mm | R03: Fruchtgemuese 300, Blattgemuese 150-200 (FarmHub); Scope-Card 300 |
| `media_gap` | 2 | mm | [A] Spiel Medium zur Wannenwand |
| `grid_t` | 5 | mm | [A] Siebboden (Lochblech) Staerke |
| `grid_hole` | 12 | mm | [A] Lochdurchmesser Siebboden, vereinfacht (real Lochblech D8, kleiner als Korn 8-20) |
| `grid_nx` | 20 |  | [A] Loecher je Reihe (vereinfacht) |
| `grid_ny` | 5 |  | [A] Lochreihen (vereinfacht) |
| `post` | 60 | mm | [A] Stuetzklotz 60 x 60 unter dem Siebboden |
| `post_nx` | 4 |  | [A] Stuetzen in Laengsrichtung (aussen 4, innen 3 per Konfiguration im Generator) |
| `standpipe_d` | 25 | mm | R03: Standrohr D25 (FarmHub 2,5 cm PVC) |
| `standpipe_over` | 220 | mm | R03: Standrohr 220 mm hoch ueber der Medienunterkante (Gesamtlaenge ab Bulkhead = Stuetzhoehe + 220) [E] |
| `standpipe_wall` | 2 | mm | [A] PVC-Rohr d25 |
| `bell_d` | 75 | mm | R03: Glocke D75 |
| `bell_h` | 250 | mm | R03: Glocke 250 hoch, oben verschlossen |
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

Gesamt-Box (Messung): X -1526.5 bis 1476.5, Y -466.5 bis 466.5, Z -30.0 bis 637.0 mm; Koerper: 17.

**Toleranzen / Spiel:** Medium 2 mm Spiel zur Wanne; Wasserstand in der Flutphase ueber die Standrohrkante 220 mm ueber der Medienunterkante, also ca. 80 mm unter der Medienoberflaeche (trockene Zone 5-8 cm, R03).

## Werkstoff und Gewicht

- Werkstoff: HDPE weiss (Wanne), PVC grau (Rohre), Kies/Blaehton (Medium), Dichte 0.95 g/cm3, Farbe #e9ebe8 (ref-5/ref-6 weisse Wannen; HDPE IBC-Innenbehaelter)
- Volumen (Messung, `solidcraft-cli eval`): 841087.3 cm3 · Masse leer: 759308 g (759.31 kg)
- Variante `ibc_beet_aussen_933`: 759.31 kg leer
- Variante `ibc_beet_aussen_993`: 808.56 kg leer
- Variante `ibc_beet_innen_933`: 478.64 kg leer
- Gefuellt/in Betrieb: aussen_933: Medium 790 l (ca. 711 kg trocken), Wasserraum unter dem Siebboden bis Standrohr-Oberkante ca. 680 l; aussen_993: Medium 842 l (ca. 758 kg trocken), Wasserraum unter dem Siebboden bis Standrohr-Oberkante ca. 725 l; innen_933: Medium 495 l (ca. 446 kg trocken), Wasserraum unter dem Siebboden bis Standrohr-Oberkante ca. 447 l [E, Wasser 1 kg/l]; Gesamtgewicht gefuellt aussen ca. 1,3-1,5 t

## Querschnitt / Profil

Wanne halbe IBC: Wand 4 mm, Boden 5 mm, Randwulst 10 x 12 mm; Siebboden 5 mm auf 6 (innen) bzw. 8 (aussen) Stuetzkloetzen 60 x 60; Medium 300 mm (EIN Koerper) mit Oberflaeche 75 mm unter dem Rand; Glockensiphon: Standrohr d25, Glocke d75 x 250 (2 Schlitze 10 x 40, Luftloch 10), Medienschutz d110 x 320 (12 Durchbrueche 12 x 12).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| aussen_933: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25, Bulkhead D36/Flansch D50 | x 1262, y 0, z -30 | aus, Richtung -Z (Beet ist eingelassen, Ablauf unter Wannenboden) |
| aussen_933: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE), Zulauf 200-500 l/h (R03) | x -1526, y -402, z 612 | ein, Richtung -X (Anschluss von aussen) |
| aussen_993: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25, Bulkhead D36/Flansch D50 | x 1262, y 0, z -30 | aus, Richtung -Z (Beet ist eingelassen, Ablauf unter Wannenboden) |
| aussen_993: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE), Zulauf 200-500 l/h (R03) | x -1526, y -432, z 612 | ein, Richtung -X (Anschluss von aussen) |
| innen_933: Ablauf (Standrohr/Bulkhead, Rohrende unter dem Boden) | Rohr d25, Bulkhead D36/Flansch D50 | x 718, y 0, z -30 | aus, Richtung -Z (Beet ist eingelassen, Ablauf unter Wannenboden) |
| innen_933: Zulauf (Tropfrohr, offenes Ende ausserhalb der Stirnwand) | Rohr d20 (PE), Zulauf 200-500 l/h (R03) | x -982, y -402, z 624 | ein, Richtung -X (Anschluss von aussen) |

## Verbindungen und Befestigungen

- Standrohr steckt in der Bulkhead-Durchfuehrung D36 (Gewindehuelse mit Flansch D50 und Dichtung, Kontermutter unter dem Boden) [A]
- Glocke und Medienschutz stehen lose auf dem Siebboden; Siebboden liegt auf Stuetzkloetzen
- Zulauf-Tropfrohr durch eine Durchfuehrung D22 in der Stirnwand (Dichtung Gummitülle), Endstopfen am Ende

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Aussenmass 2953 x 933/993 x 637 bzw. 1865 x 933 x 649 | mm | OBJ | layout.json ibc_beds (Laenge, Breite, Hoehe) | hoch |
| Unterkante Z -162 (aussen) / -173..-209 (innen) | mm | OBJ | layout.json ibc_beds z0 (Integrator setzt; im Bauteil Ursprung = Wannenunterseite) | hoch |
| Wandstaerke 4 mm, Boden 5 mm | 4 / 5 | R03 + A | R03 (3-4 mm); Boden Annahme | mittel |
| Randwulst 10 x 12 mm | 10 / 12 | Bild + A | ref-5/ref-6: umlaufender Rand der weissen Wannen | niedrig |
| Eckenradius 40 mm | 40 | Bild + A | ref-5 (gerundete Ecken der IBC-Wannen) | niedrig |
| Medientiefe 300 mm, Oberflaeche Z 400 (75 mm unter dem Rand) | 300 | R03 | docs/research/R03.md (FarmHub 30 cm Fruchtgemuese; Z 400 Vorgabe Orchestrator) | mittel |
| Medium als EIN Koerper | - | R03/Scope-Card | Scope-Card ibc_beet: Medium als EIN Koerper | hoch |
| Siebboden 5 mm, Lochraster 20 x 5 D12 (vereinfacht) | - | Scope-Card + A | Scope-Card nennt Siebboden; Raster vereinfacht | niedrig |
| Stuetzkloetze 60x60 | - | A | Konstruktionspraxis; Wasserraum unter dem Medium ist Annahme | niedrig |
| Standrohr d25, 220 mm ueber Medienunterkante | 25 / 220 | R03 | docs/research/R03.md (FarmHub 2,5 cm, 22 cm) | mittel |
| Glocke d75 x 250, Schlitze 10x40, Luftloch 10 | - | R03 | docs/research/R03.md (FarmHub) | mittel |
| Medienschutz d110 x 320 mit Seitenloechern | - | R03 | docs/research/R03.md (FarmHub 11 cm, 32 cm) | mittel |
| Bulkhead D36 / Flansch D50 | - | A | Standrohr d25; Durchfuehrung geschaetzt (Scope-Card: Ablauf-Fitting im Boden) | niedrig |
| Zulauf-Tropfrohr d20 auf Z 450 (25 mm unter dem Rand) | 20 | R03 + A | R03: Zulaufrohr auf Z 450; Durchmesser Annahme | niedrig |
| Zulauf 200-500 l/h je Beet | - | R03 | docs/research/R03.md (Glockensiphon-Auslegung) | mittel |
| Anzahl 8 aussen (5 x 933, 3 x 993), 6 innen | 14 | OBJ | layout.json ibc_beds | hoch |
| Werkstoff HDPE weiss, Medium Blaehton | - | Bild + A | ref-5/6 weisse Wannen; Medium R03 (Vulkankies/Blaehton 8-20 mm) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-5-dome-closeup.jpg und ref-6 (weisse Wannen mit Rand, Erde/Kies); docs/research/R03.md (Beetaufbau)
- Quelle der Masse: data/layout.json ibc_beds (Laenge, Breite, Hoehe, Z-Unterkante), docs/research/R03.md (Beetaufbau), docs/scope-cards.md ibc_beet; ref-5/ref-6: weisse Wannen mit Rand und Erde/Kies
- Abweichung zum OBJ: OBJ ibc_beds: Laenge/Breite/Hoehe wie layout.json (Messung 0 mm Abweichung); Medium-Hoehe absolut Z 400 laut R03 (Beet z0 -162..-209, Oberkante 475); Beetinnenraum ist im OBJ nicht modelliert (nur Huelle) -> Aufbau komplett aus R03.

## Montage (L4)

1. Grube ausheben, Wanne einsetzen und waagerecht ausrichten
2. Bohrung D36 in den Boden, Bulkhead mit Dichtung einsetzen, Standrohr stecken
3. Stuetzkloetze einlegen, Siebboden auflegen, Glocke und Medienschutz aufsetzen
4. Zulauf-Tropfrohr durch die Stirnwand fuehren und abdichten
5. Medium (gewaschen, 8-20 mm) einfuellen bis 75 mm unter den Rand
6. Netztoepfe setzen (Instanzen nach layout.json), Zulauf anschliessen, Zyklus pruefen

**Werkzeug:** Bohrmaschine mit Lochsaege D36, Wasserwaage, Schaufel, Silikon/Dichtung

## Stueckliste-Zeile

- T30a Wanne halbe IBC (HDPE): 1 je Beet; 14 gesamt (aussen 8: 5 x 933 + 3 x 993, innen 6)
- T30b Stuetzkloetze 60x60: 6 (innen) / 8 (aussen) je Beet
- T30c Siebboden 5 mm (PP): 1
- T30d Medium Blaehton/Kies 8-20 mm: 1 Fuellung (Menge siehe Messung)
- T30e Bulkhead D36 + Standrohr d25 + Glocke d75 x 250 + Medienschutz d110 x 320: 1 Satz
- T30f Zulauf-Tropfrohr d20 PE mit Endstopfen: 1

## Alternative lokale Fertigung

Wanne: halbe IBC (1000-l-Container, Innenbehaelter HDPE) aufgeschnitten oder Kunststoffwanne; Siebboden: Lochblech/Gitterrost mit Vlies; Siphon aus PVC-Rohr-Standardteilen (d25/d75/d110).

## Renders


## Pruefung

- Gauntlet-Urteil: Bild-Kritiker und Spec-Pruefer laufen
- scripts/workshop/check_ibc_beet.py (Ergebnis renders/components/ibc_beet_aussen_933/check.txt)
- Triage in docs/workshop-log.md

## Offene Fragen

- Rolle des Hohlraums unter dem Siebboden (262 mm): R03 nennt Medientiefe 300 bei Behaelter 637 -> Wasserraum/Reservoir [A]
- Standrohrhoehe 220 ueber Medienunterkante (R03 gibt 220 bei Medientiefe 300 ohne Wasserraum) [E]
- Seitenloecher/Tropfloecher/Luftloch quadratisch modelliert (Rechenzeit), real rund
- Pflanzen (Netztoepfe, Koepfe) sind Instanzen nach layout.json (288 je Aussenbeet) und nicht Teil des Beets
- Tropfrohr-Halterung am Wannenrand nicht modelliert

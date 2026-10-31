# Bauteilblatt T42 huelle_folie (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/huelle_folie.json` und `designs/components/huelle_folie.sc`, nicht von Hand aendern)

**Funktion:** Huelle der Kuppel als Plane (D39): je Dreiecksfeld zwei Lagen UV-PE-Gewaechshausfolie (150 Mikrometer, Infrarotsperre, Anti-Drip) mit Luftpolster dazwischen; die Folie liegt aussen auf den Streben, ihre Kante wird in der Keilschiene der Strebe geklemmt, und jede Bahn ragt 100 mm ueber die Strebenachse hinaus und ueberlappt ziegelartig mit der Nachbarbahn. Das Tuerfeld hat einen Planenausschnitt fuer die Zarge. Die Haut aus Paneelen (haut_paneel, W19/W20) ruht als Variante und bleibt erhalten.

**Datei:** `designs/components/huelle_folie.sc` · **Teilenummer:** T42 · **Revision:** A · **Bezugspunkt:** Inkreismittelpunkt des Strebendreiecks, Z = Aussennormale, Z 0 = Ebene der Strebenachsen (innere Lage bei Z 64, aeussere bei Z 164), X parallel zur Kante P0P1 (beim Tuerfeld die Basiskante)

**Anzahl (Instanzen):** 40 Felder: 30 AAB, 9 BBB, 1 BBB mit Planenausschnitt (Tuer) (Quelle: data/components/haut_paneel.json typen (anzahl_voll 30/9, anzahl_mit_tuerausschnitt 1); data/layout.json dome 65 Streben, 26 Knoten, 40 Dreiecke)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `foil_t` | 0.15 | mm | [Q] R24: Gewaechshaus-PE-Folie 6 mil (ca. 150 Mikrometer) |
| `layer_gap` | 100 | mm | [A] Auftrag W27 / R24: zwei Lagen im Abstand ca. 100 mm (Luftpolster); real aufgeblasen und gewoelbt, hier als parallele Ebenen |
| `overlap` | 200 | mm | [E] R24: 100 mm Ueberstand je Seite ueber die Strebenachse, im Verband ziegelartig ueberlappend; Ueberlappung zweier Nachbarfelder = 2 x 100 mm |
| `foil_z0` | 64 | mm | [E] Hoehe der inneren Lage ueber der Ebene der Strebenachsen: Strebenradius 45 + Schaumband 3 + Kanal 15 + 1 mm Luft (liegt auf der Keilschiene) |
| `door_overlap` | 25 | mm | [A] Der Planenausschnitt ist je Seite und oben 25 mm kleiner als das Zargen-Aussenmass; die Folie liegt auf dem Aufsatzrahmen (tuer_zarge_planenausschnitt) |
| `opacity` | 0.25 |  | [A] Darstellung transparent |

| Typ | anzahl | kanten_nominal | tuerausschnitt |
|---|---|---|---|
| AAB | 30 | [3279, 3279, 3708] | False |
| BBB | 9 | [3708, 3708, 3708] | False |
| BBB_tuer | 1 | [3708, 3708, 3708] | True |

Gesamt-Box (Messung, Variante huelle_folie_AAB): X -2043.8 bis 1570.9, Y -1076.9 bis 2294.6, Z 64.0 bis 164.2 mm; Koerper: 2.

**Toleranzen / Spiel:** Ueberstand 100 mm je Seite ueber die Strebenachse (Parameter overlap = 200 mm Ueberlappung zweier Nachbarfelder); Planenausschnitt 1026 x 2043 mm (Zarge 1076 x 2068 minus 25 mm je Seite und oben), reicht nach unten durch den Ueberstand; Pruefung check_huelle.py folie (Flaeche +-0,2 % gegen Heron).

## Werkstoff und Gewicht

- Werkstoff: PE-Gewaechshausfolie UV-stabilisiert, 150 Mikrometer, Infrarotsperre, Anti-Drip (R24), Dichte 0.92 g/cm3, Farbe #e8f4f8 (Handbuchwert PE (LDPE 0,92); Eigenschaften nach R24)
- Volumen (Messung, Variante huelle_folie_AAB, `solidcraft-cli eval`): 1828.0 cm3 · Masse leer: 1682 g (1.68 kg)
- Variante `huelle_folie_AAB`: 1.68 kg leer
- Variante `huelle_folie_BBB`: 1.96 kg leer
- Variante `huelle_folie_BBB_tuer`: 1.36 kg leer
- Gefuellt/in Betrieb: nicht zutreffend; Gesamtgewicht der Folie beider Lagen 69,5 kg (Summe ueber 40 Felder); Wind- und Schneelast sind nicht gerechnet.

## Querschnitt / Profil

Zwei Lagen PE 0,15 mm, parallel im Abstand 100 mm (Luftpolster-Platzhalter: real aufgeblasen und gewoelbt); innere Lage 64 mm ueber der Ebene der Strebenachsen (liegt auf der Keilschiene), aeussere Lage 164 mm.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Folienkante an der Keilschiene (3 Kanten je Feld) | Maul 17 mm | Kante des Strebendreiecks + 100 mm Ueberstand, Z 64 (innen) und Z 164 (aussen) | Kante wird in den Kanal gedrueckt, Federdraht klemmt, Richtung -Z |
| Ueberlappung zur Nachbarbahn | 200 mm (2 x 100 mm Ueberstand) | an den drei Seiten des Felds | ziegelartig: untere Bahn vor der oberen (Montage legt die Reihenfolge fest) |
| Planenausschnitt Tuerfeld (nur BBB_tuer) | 1026 x 2043 mm | mittig auf der Basiskante, von der Basiskante - 100 mm bis y' 2043 | Folienkante liegt 25 mm auf dem Aufsatzrahmen der Zarge (tuer_zarge_planenausschnitt) |

## Verbindungen und Befestigungen

- Folie an der Strebe: Keilschiene (T43) mit Federdraht D2 [Q R24]; kein Tackern, kein Kleben
- Folie an der Zarge: Klemmleiste und Aufsatzrahmen (T44), Dichtband EPDM
- Folie an Folie: Ueberlappung 200 mm, Verbindung durch die Klemmung in den Schienen; Luftdichtigkeit der Lagen und das Geblaese fuer das Luftpolster sind offen [A]

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Huelle als Plane (Folie), keine Paneele | Plane | Q | docs/decisions.md D39 (Owner 30.10.) | hoch |
| Material: UV-PE 6 mil (ca. 150 Mikrometer), doppelt, luftgepolstert, Infrarotsperre, Anti-Drip | 150 Mikrometer, 2 Lagen | Q | docs/research/R24.md Empfehlung 1 (KSU, Purdue CEA, Haendler); D45 Annahme | mittel |
| Abstand der Lagen 100 mm | 100 mm | A | Auftrag W27 / R24 Folge fuer Modell: Luftpolster [A] | niedrig |
| Ueberstand 100 mm je Seite, ziegelartige Ueberlappung | 100 mm, Parameter overlap 200 | E | R24 Empfehlung 2 (E: 100 mm je Seite, im Verband ziegelartig ueberlappend) | mittel |
| Huellflaeche netto 208 m2 | 207,7 m2 (Bauteile) / 208 m2 (R24) | E | 209,98 m2 aus layout.json (40 Dreiecke) minus Tuerfeld 2,22 m2; R24 Zahlen | hoch |
| Dreieckstypen AAB 30 / BBB 9 / BBB mit Tuerausschnitt 1 | 30 / 9 / 1 | Q | data/components/haut_paneel.json typen (aus layout.json nodes_list) | hoch |
| Innere Lage bei Z 64 | 64 mm | E | Strebenradius 45 + Schaumband 3 + Kanal 15 + 1 mm Luft | mittel |
| Planenausschnitt 1026 x 2043 | 1026 x 2043 mm | E | Zarge 1076 x 2068 (tuer_komplett.json) minus door_overlap 25 [A] | niedrig |
| Dichte PE 0,92 | g/cm3 | A | Handbuchwert LDPE | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: docs/research/R24.md (Empfehlung Plane, Folge fuer Modell); kein Referenzbild
- Quelle der Masse: docs/research/R24.md (Empfehlung 1/2: PE doppelt luftgepolstert 6 mil, Zuschnitt je Dreieck mit 100 mm Ueberstand, ziegelartig ueberlappend; Huellflaeche netto 208 m2 = 209,9 - Tuerfeld), data/layout.json dome (nodes_list, strut_len_mm), data/components/haut_paneel.json (Dreieckstypen), tuer_komplett.json (Zarge 1076 x 2068)
- Abweichung zum OBJ: Das Bauteil kommt nicht aus dem OBJ (die Huelle ist Plane, D39). Netto-Flaeche aus den Bauteilen 207,7 m2 gegen R24 208 m2 (209,9 - Tuerfeld; Pruefung +-3 %); mit Ueberstand ergeben sich je Lage 251,8 m2 Folie, bei zwei Lagen ca. 504 m2 und 69,5 kg. Das Blatt W27 nennt die Datei 'huelle_folie.sc': wegen der Skizzen-Zahlen (keine Ausdruecke) gibt es je Dreiecksform eine Datei huelle_folie_AAB.sc, huelle_folie_BBB.sc und huelle_folie_BBB_tuer.sc, wie bei haut_paneel.

## Montage (L4)

1. Keilschienen auf alle Streben setzen (keilschiene)
2. Folienbahnen je Dreiecksfeld mit 100 mm Ueberstand zuschneiden (zwei Lagen je Feld)
3. Innere Lage einlegen: Kanten in die Kanaele druecken, Federdraht einziehen; aeussere Lage darueber, gleiches Vorgehen
4. Ueberlappung ziegelartig legen (von unten nach oben, damit Regen ablaeuft)
5. Tuerfeld: Planenausschnitt an der Zarge befestigen (tuer_zarge_planenausschnitt); Luftpolster aufblasen (Gebläse, offen)

**Werkzeug:** Cuttermesser, Federdrahtroller, Massband, Leiter oder Geruest

## Stueckliste-Zeile

- huelle_folie_AAB (je 2 Lagen PE 0,15 mm, 6,09 m2 je Lage): 30 Felder
- huelle_folie_BBB (7,12 m2 je Lage): 9 Felder
- huelle_folie_BBB_tuer (4,92 m2 je Lage nach Ausschnitt): 1 Feld
- Gesamt je Lage 251,8 m2 (mit Ueberstand), beide Lagen ca. 504 m2; netto 207,7 m2

## Alternative lokale Fertigung

Handelsueblich: Gewaechshausfolie UV-stabilisiert 150 Mikrometer in Bahnen; Zuschnitt aus der Rolle vor Ort; ETFE-Kissen als teure Langzeitoption (R24).

## Renders

- `renders/components/huelle_folie/huelle_folie_AAB-01-draufsicht.png`
- `renders/components/huelle_folie/huelle_folie_AAB-02-iso.png`
- `renders/components/huelle_folie/huelle_folie_BBB-01-draufsicht.png`
- `renders/components/huelle_folie/huelle_folie_BBB-02-iso.png`
- `renders/components/huelle_folie/huelle_folie_BBB_tuer-01-draufsicht.png`
- `renders/components/huelle_folie/huelle_folie_BBB_tuer-02-iso.png`

## Pruefung

- Gauntlet-Urteil: kein Pruefer-Lauf (Auftrag W27: Selbstcheck)
- scripts/workshop/check_huelle.py folie: Ergebnis in renders/components/huelle_folie/check.txt (Flaechensumme netto 207,7 m2 gegen R24 208 m2 +-3 %, Dreiecke aus layout.json, Heron-Flaeche je Typ, Lagenabstand, Interferenz 0)
- Kein Bild-Kritiker und kein Spec-Pruefer (Auftrag W27)

## Offene Fragen

- Folienmass (150 Mikrometer, zwei Lagen, 100 mm Luftpolster) ist [A]/R24; Standort und Heizlast sind offen (D45: Annahme Mitteleuropa)
- Luftpolster real gewoelbt: hier parallele Ebenen; Gebläse am Schaltschrank (geblaese_luftpolster) ist nur Platzhalter in R24 und nicht gebaut
- Zuschnittreihenfolge der Ueberlappung (welche Bahn oben liegt) legt die Montage fest; die Bauteile sind symmetrisch (Ueberstand an allen drei Seiten)
- Folienstoss an den Knoten (Kreuzung dreier Bahnen) und die Klappen fuer Lueftung sind nicht modelliert
- Unterer Ueberstand an den Basisfeldern (100 mm unter der Basisstrebe) braucht eine Bodenbefestigung (Sandsaecke, Erdnut): Montage
- Wind- und Schneelast der Plane nicht gerechnet

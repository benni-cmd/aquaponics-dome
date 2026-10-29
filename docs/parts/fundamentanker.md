# Bauteilblatt T61 fundamentanker (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/fundamentanker.json` und `designs/components/fundamentanker.sc`, nicht von Hand aendern)

**Funktion:** Verankert einen der 10 Basisknoten der Kuppel im Erdreich (Ben: Skelett im Boden verankert): Betonpunkt, darauf eine Ankerplatte mit zwei Verbundankern M16 und einer Gabel aus zwei Laschen, in die die Ankerlasche des Basisknotens (60 x 10, Loch D14) mit einem Querbolzen M12 eingehaengt wird.

**Datei:** `designs/components/fundamentanker.sc` · **Teilenummer:** T61 · **Revision:** A · **Bezugspunkt:** Knotenmitte des Basisknotens (Z=0), X radial nach aussen (Knotennormale horizontal), Y tangential, Z oben; Ankerplatte Oberkante bei z = lug_hole_z - clevis_below_hole; die Montage dreht je Basisknoten um Z auf den Azimut des Knotens

**Anzahl (Instanzen):** 10 (an den 10 Basisknoten) (Quelle: data/layout.json dome.node_valence (10 vierwertige Basisknoten))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `block_x` | 400 | mm | Scope-Card: Betonpunkt 400 x 400 x 600 (Annahme A) |
| `block_y` | 400 | mm | Scope-Card (A) |
| `block_z` | 600 | mm | Scope-Card (A) |
| `plate_s` | 250 | mm | [A] Ankerplatte 250 x 250 |
| `plate_t` | 15 | mm | [A] Ankerplatte 15 mm Stahl |
| `anchor_d` | 16 | mm | [A] Verbundanker M16 (Annahme, statisch nicht nachgewiesen) |
| `anchor_len` | 300 | mm | [A] Verbundanker M16 x 300 (Setztiefe ca. 280) |
| `anchor_hole` | 17.5 | mm | [E] Durchgangsloch in der Ankerplatte fuer M16 (ISO 273 mittel 17,5) |
| `anchor_off` | 75 | mm | [A] Ankerbolzen auf der Plattendiagonale, +-75 mm von der Mitte |
| `clevis_w` | 80 | mm | [A] Gabellasche Breite (radial) |
| `clevis_t` | 10 | mm | [A] Gabellasche Dicke |
| `clevis_h` | 140 | mm | [A] Gabellasche Hoehe ueber der Ankerplatte |
| `lug_t` | 10 | mm | knoten.json lug_t: Dicke der Ankerlasche am Knoten |
| `lug_clear` | 2 | mm | [A] Spiel der Knotenlasche in der Gabel (Gabelweite = lug_t + 2) |
| `bolt_hole` | 14 | mm | knoten.json lug_hole: Loch D14 fuer M12 |
| `bolt_len` | 55 | mm | [E] M12x55 ISO 4017: Gabel 10 + 12 + 10 + 2 Scheiben 6 + Mutter 10 + Ueberstand 7 (Spec-Pruefer: 2 mm Ueberstand bei 50 zu knapp) |
| `washer_t` | 3 | mm | [E] Scheibe M12 ISO 7089 ca. 3 mm |
| `lug_hole_z` | -159 | mm | [E] Hoehe der Knotenlasche-Lochmitte ab Knotenmitte = -ball_d/2 + 6 - lug_l + 35 (knoten.json) |
| `clevis_below_hole` | 70 | mm | [A] Lochmitte 70 mm ueber der Ankerplatten-Oberkante |

Gesamt-Box (Messung): X -200.0 bis 200.0, Y -200.0 bis 200.0, Z -844.0 bis -89.0 mm; Koerper: 12.

- Box (Messung) fundamentanker: X -200 bis 200, Y -200 bis 200, Z -844 bis -89
**Toleranzen / Spiel:** Gabelspalt = Knotenlasche 10 + 2 mm Spiel; Lochhoehe und Loch-D gleich der Knotenlasche (Pruefung 15/15, Querpruefung gegen knoten.json); Beton: Bohrloecher D18 fuer die Verbundanker.

## Werkstoff und Gewicht

- Werkstoff: Beton C25/30 (Block), Stahl S235 feuerverzinkt (Platte, Laschen, Anker), Dichte 7.85 g/cm3, Farbe #aeb4b8 (Beton C25/30 und Stahl S235 Annahme A; Dichte Beton 2,4 g/cm3)
- Volumen (Messung, `solidcraft-cli eval`): 97152.1 cm3 · Masse leer: 240231 g (240.23 kg)
- Gefuellt/in Betrieb: Betonpunkt 230 kg, Stahlteile 10.2 kg, gesamt 240 kg je Anker (10 Stueck: ca. 2402 kg)

## Querschnitt / Profil

Betonpunkt 400 x 400 x 600 (Oberkante z = -244); Ankerplatte 250 x 250 x 15; zwei Verbundanker M16 x 300 auf der Plattendiagonale (+-75); Gabel aus zwei Laschen 80 x 10 x 140 mit 12 mm Spalt; Loch D14 auf Hoehe z = -159.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Anschluss Knotenlasche (Gabel) | Querbolzen M12x55 ISO 4017, Loch D14 durch beide Laschen | x 0, y 0, z -159 (Lochmitte, Bezug = Knotenmitte); Gabelspalt y +-6 | Lochachse Y = tangential (waagerecht, senkrecht zur Knotennormalen, umlaufend um die Kuppel); Knotenlasche kommt von oben (+Z) |
| Verbundanker (2 Stueck) | M16 x 300, Setztiefe ca. 280, Bohrloch D18, chemisch (Verbundmoertel nicht modelliert) | x,y = (+75, +75) und (-75, -75) (Diagonale ++/--), z -229 (Plattenoberkante) bis -529 | Kopf oben, Schaft nach -Z in den Beton |
| Betonpunkt (Einbau im Erdreich) | 400 x 400 x 600, Oberkante z -244, Unterkante z -844 | Mitte x 0, y 0 (unter dem Basisknoten) | Grube im Erdreich; Verhaeltnis zur Erdflaeche/Fundamentring: Montage |
| Ausrichtung je Basisknoten | Drehung um Z auf den Azimut des Knotens: X = radial nach aussen | Azimut je Basisknoten: n17 -84.8 Grad, n18 -48.8 Grad, n19 -12.8 Grad, n20 23.2 Grad, n21 59.2 Grad, n22 -156.8 Grad, n23 167.2 Grad, n24 -120.8 Grad, n25 131.2 Grad, n26 95.2 Grad | Instanz an die Knotenposition (layout.json dome.nodes_list, Wertigkeit 4) setzen |

## Verbindungen und Befestigungen

- Ankerplatte auf dem Betonpunkt, Verbundanker = Gewindestange M16 x 300 (8.8) mit Sechskantmutter ISO 4032 und Scheibe ISO 7089 oben, im Modell als Sechskantschraube mit Kopf oben dargestellt (Kopf = Mutter); Platte 15 mm, Loecher D17,5
- Gabellaschen an die Ankerplatte geschweisst (MAG), dann feuerverzinkt [A]
- Querbolzen M12x55 ISO 4017 mit 2 Scheiben ISO 7089 und Mutter ISO 4032 durch Gabel und Knotenlasche
- Betonpunkt: Beton C25/30, Gruendungstiefe frostfrei (Tiefe 600 + Aufbau) nicht nachgewiesen

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Anzahl 10 (an den 10 Basisknoten) | 10 | OBJ | layout.json dome.node_valence {4: 10} | hoch |
| Betonpunkt 400 x 400 x 600 | 400x400x600 mm | A (Scope-Card) | docs/scope-cards.md fundamentanker nennt das Mass selbst Annahme A, keine Quelle | niedrig |
| Ankerplatte 250 x 250 x 15 | 250x250x15 mm | A | Konstruktionspraxis; keine Quelle | niedrig |
| 2 Verbundanker M16 x 300 auf der Diagonale +-75 | M16 x 300 | A (Scope-Card) | Scope-Card: Ankerplatte mit 2 Bolzen; Groesse Annahme (R01 Statik ruht) | niedrig |
| Gabel aus 2 Laschen 80 x 10 x 140, Spalt 12 | 80x10x140, 12 mm | A (Scope-Card) + E | Scope-Card: Anschlusslaschen zum Basisknoten; Spalt = Knotenlasche 10 + 2 (knoten.json) | mittel |
| Lochhoehe z -159 ab Knotenmitte, Loch D14, Querbolzen M12x55 | z -159, D14, M12 | E + A | knoten.json: -ball_d/2 + 6 - lug_l + 35 mit lug_l 150 und Lochlage 35 (beide A); Loch D14 durch die M12-Wahl (A); Querpruefung 15/15 prueft die Uebereinstimmung beider Klassen | mittel |
| Ankerplatte 70 mm unter der Lochmitte (clevis_below_hole) | 70 mm | A | Gabelhoehe 140 mit Loch auf halber Hoehe | niedrig |
| Beton C25/30, 2,4 g/cm3; Stahl S235 7,85 g/cm3 | 2,4 / 7,85 g/cm3 | A | Normwerte; Festigkeitsklasse Annahme | mittel |
| Azimut je Basisknoten (X radial) | az je Knoten | E | knoten_arme.json (az_grad = atan2(n_y, n_x) der Knotennormalen aus nodes_list) | hoch |
| Lochachse tangential (umlaufend), Knotenlasche kommt von oben | tangential | A | Annahme der Werkstatt, im OBJ keine Ankerdetails | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-4/ref-5: Anker nicht sichtbar (vergraben bzw. vom Fundamentring verdeckt); Scope-Card fundamentanker; Ben: Skelett im Boden verankert
- Quelle der Masse: docs/scope-cards.md fundamentanker (Block 400 x 400 x 600 A), data/components/knoten.json (Ankerlasche 60 x 10 x 150, Loch D14 bei z -159 ab Knotenmitte), Ben: Skelett im Boden verankert
- Abweichung zum OBJ: Scope-Card: Ankerplatte mit 2 Bolzen, Betonpunkt (Block im Erdreich 400 x 400 x 600 A), Anschlusslaschen zum Basisknoten, Normschrauben: umgesetzt. Hoehenlage: Der Basisknoten sitzt bei z = -14, die Lasche haengt 150 mm unter die Knotenkugel, die Ankerplatte liegt 229 mm unter der Knotenmitte: damit liegt der Betonkopf bei Weltz = -14 - 244 = -258 mm (Gelaende/Fundamentring: Montage pruefen).

## Montage (L4)

1. Grube ausheben (400 x 400 x 600 plus Arbeitsraum), Schalung, Beton C25/30 mit Bohrlochraster einbringen und abbinden lassen
2. Bohrloecher D18 setzen, Verbundmoertel einbringen, Verbundanker M16 setzen, Ankerplatte mit Gabel aufsetzen, Muttern/Scheiben anziehen
3. Basisknoten mit der Ankerlasche in die Gabel einfuehren, Querbolzen M12 mit Scheiben und Mutter montieren
4. Ausrichtung: X radial nach aussen, Lochachse tangential
5. Anzugsmomente (Richtwerte [E]): Querbolzen M12 8.8 85 Nm (verspannt die 10-mm-Gabellaschen nicht auf der Knotenlasche: Spalt 12 bleibt frei, Muttern nur handfest plus 1/4 Umdrehung bzw. nach Herstellervorgabe), Verbundanker M16 nach Moertelhersteller (Richtwert 80 Nm)

**Werkzeug:** Spaten/Bagger, Schalungsbretter, Betonmischer, Bohrhammer D18, Dosierpistole Verbundmoertel, Schluessel M12/M16, Wasserwaage

## Stueckliste-Zeile

- 1 Betonpunkt C25/30 400 x 400 x 600 (0,096 m3, ca. 230 kg)
- 1 Ankerplatte S235 250 x 250 x 15 mit 2 Loechern D17,5
- 2 Gabellaschen S235 80 x 10 x 140
- 2 Gewindestangen M16 x 300 (Verbundanker) mit je 1 Mutter ISO 4032 und 1 Scheibe ISO 7089, Verbundmoertel 2 Kartuschen je 10 Anker [A]
- 1 Querbolzen M12x55 ISO 4017 mit 2 Scheiben ISO 7089 und Mutter ISO 4032
- Menge: 10 Anker (je Basisknoten einer): 10 Betonpunkte, 10 Platten, 20 Laschen, 20 Verbundanker, 10 Querbolzen

## Alternative lokale Fertigung

Betonpunkt vor Ort gegossen; Platte und Laschen vom Metallbauer (Reststuecke S235); Verbundanker aus dem Baustoffhandel oder Gewindestangen M16 mit Ankermoertel.

## Renders

- `renders/components/fundamentanker/fundamentanker-01-iso.png`
- `renders/components/fundamentanker/fundamentanker-02-gabel.png`
- `renders/components/fundamentanker/fundamentanker-03-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Spec-Pruefer: FAIL (Herkunftskategorien, Zahl 235, Montage) behoben; Orchestrator: angenommen (D16)
- scripts/workshop/check_fundamentanker.py (Ergebnis renders/components/fundamentanker/check.txt): Block, Platte, Anker, Gabel; QUERPRUEFUNG gegen die Ankerlasche des Knotens (Lochhoehe -159, Loch D14, Gabelspalt 12)
- Kein Bild-Kritiker: der Anker ist in keiner Referenz sichtbar; Spec-Pruefer und Orchestrator-Stichprobe

## Offene Fragen

- Statik/Tragfaehigkeit nicht nachgewiesen (Statik ruht): Block, Anker, Laschen sind Annahmen A
- Gruendungstiefe/Frost und Bodenkennwerte offen
- Lage zur Erdflaeche/zum Fundamentring: Der Basisknoten liegt bei z = -14, damit Ankerplatten-Oberkante z = -243 und Betonkopf z = -258 (Welt); das Gelaende (z = 0?) ist nicht definiert -> Montage
- Hebelwirkung: Gabel nimmt nur Querkraefte quer zur Lochachse auf; Zug/Druck in Strebenrichtung ueber die Ankerplatte [A]
- Ausrichtung Lochachse tangential (umlaufend) ist Annahme; im OBJ keine Ankerdetails

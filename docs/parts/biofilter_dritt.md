# Bauteilblatt T98 biofilter_dritt (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/biofilter_dritt.json` und `designs/components/biofilter_dritt.sc`, nicht von Hand aendern)

**Funktion:** Eigener kleiner Biofilter des Quarantaene-Drittbeckens: Eine Pumpe im Becken drueckt 5 l/min (K42) durch das Tauchrohr an den Fassboden; das Wasser steigt durch 37 l Bioballs, auf denen Nitrifikationsbakterien Ammonium zu Nitrat abbauen, und laeuft seitlich per Schwerkraft zurueck ins Becken (K43). Ein Luftschlauch im Deckel versorgt die Bakterien mit Sauerstoff.

**Datei:** `designs/components/biofilter_dritt.sc` · **Teilenummer:** T98 · **Revision:** A · **Bezugspunkt:** Mitte Fassboden aussen (Z 0), Z hoch; Zulauf und Tauchrohr bei x -110, Auslauf-Tankverbinder +X, Luftbohrung x +110

**Anzahl (Instanzen):** 1 (biofilter_dritt, nur am Drittbecken) (Quelle: data/leitungsnetz.json Knoten biofilter_dritt; Standort neben dem Drittbecken, Auslauf ueber dessen Wasserspiegel, setzt die Montage)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `fass_d` | 398 | mm | [E] Graf-Massskizze Weithalsfass 60 l, Artikel 824410 (graf.info Dimension_drawing/Massskizze_Weithalsfass_60l.pdf): Oe 398 oben, 370 Boden, Oeffnung 338, H 615, mit Deckel 625; Haendlerangaben Weithalsfass 60 l (OBI, Kaufland, toom; Graf 824410 und Nachbauten): Oe 400, H 620 bis 640 (zwei Quellen, Konizitaet 398/370 nicht modelliert) |
| `fass_h` | 615 | mm | [E] Graf-Massskizze Weithalsfass 60 l, Artikel 824410 (graf.info Dimension_drawing/Massskizze_Weithalsfass_60l.pdf): Oe 398 oben, 370 Boden, Oeffnung 338, H 615, mit Deckel 625 |
| `fass_wall` | 3 | mm | [A] Wandstaerke PE-Fass (Datenblatt nennt keine Wand) |
| `fass_floor` | 4 | mm | [A] |
| `deckel_t` | 10 | mm | [E] Graf-Massskizze Weithalsfass 60 l, Artikel 824410 (graf.info Dimension_drawing/Massskizze_Weithalsfass_60l.pdf): Oe 398 oben, 370 Boden, Oeffnung 338, H 615, mit Deckel 625: 625 mit Deckel minus 615 |
| `bett_l` | 37 | l | [E] docs/research/R37.md Befund 10: 37 l Bioballs (0,5 l je g Futter, 73 g Futter/Tag); R27 nannte 85 l fuer das groessere Becken 0,94 m3 |
| `bett_spalt` | 3 | mm | [A] Luft Bett zur Fasswand |
| `sieb_z` | 460 | mm | [A] Unterkante Niederhalter-Lochplatte; Bett liegt darunter, Wasserstand (Auslauf 540) darueber |
| `sieb_t` | 10 | mm | [A] Lochplatte PE 10 mm, Bohrungen nicht modelliert |
| `rohr_d` | 25 | mm | [E] data/leitungsnetz.json K42/K43 dn 25 |
| `zulauf_x` | -110 | mm | [A] Lage Zulauf-Muffe im Deckel |
| `tauch_z` | 60 | mm | [A] Unterkante Tauchrohr ueber dem Fassboden aussen |
| `auslauf_z` | 540 | mm | [A] Achse Auslauf-Tankverbinder, 75 mm unter dem Fassrand (Wasserstand) |
| `auslauf_l` | 50 | mm | [A] Ueberstand Tankverbinder aussen |
| `luft_d` | 8 | mm | [A] Bohrung fuer Luftschlauch (wie Schlammfass T93) |
| `luft_x` | 110 | mm | [A] Lage Luftbohrung |
| `durchfluss` | 5 | l/min | [E] data/leitungsnetz.json K42/K43 soll_l_min 5 (TAN-Mindestdurchfluss 2,6 l/min x 2) |

Gesamt-Box (Messung): X -199.0 bis 249.0, Y -199.0 bis 199.0, Z -0.0 bis 654.0 mm; Koerper: 7.

**Toleranzen / Spiel:** Bett 3 mm Luft zur Fasswand; Lochplatte liegt mit Spiel im Fass (Oe 386); Wasserstand am Auslauf Z 540, 70 mm ueber der Lochplatte.

## Werkstoff und Gewicht

- Werkstoff: PE (Fass, Deckel, Lochplatte), PVC-U (Stutzen, Tauchrohr), Kunststoff-Bioballs, Dichte 0.95 g/cm3, Farbe #2a4f8f ([A])
- Volumen (Messung, `solidcraft-cli eval`): 42284.1 cm3 · Masse leer: 10621 g (10.62 kg)
- Gefuellt/in Betrieb: Wasser bis Auslauf ca. 70 l minus Bettanteil der Bioballs, gefuellt ca. 75 kg [E, Dichte 1]

## Querschnitt / Profil

Weithalsfass Oe 398 x 615 (Wand 3, Boden 4) mit Deckel 10; Tauchrohr d25 von der Deckel-Muffe bis 60 mm ueber dem Boden; Bioball-Bett unter der Lochplatte (Unterkante 460); Tankverbinder d25 mit Muffe bei Z 540 auf +X.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Zulauf K42 (Pumpe im Drittbecken) | Muffe d25, Deckel | x -110, y 0, z 654 | +Z |
| Auslauf K43 (Schwerkraft zurueck ins Drittbecken) | Muffe d25, Tankverbinder seitlich | x 249, y 0, z 540 | +X |
| Luftschlauch (Belueftung) | Bohrung Oe 8 im Deckel | x 110, y 0, z 625 | +Z |

## Verbindungen und Befestigungen

- Zulauf-Muffe d25 im Deckel eingeklebt oder per Tankverbinder [A]; K42 steckt von oben in die Muffe, das Tauchrohr von unten
- Auslauf: Tankverbinder d25 durch die Fasswand mit Dichtung [A]; K43 steckt in die Muffe aussen
- Deckel: Schraubdeckel des Weithalsfasses (Gewinde nicht modelliert)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Weithalsfass PE 60 l, Oe 398 x 615 (625 mit Deckel) | mm | belegt (zwei Quellen) | Graf-Massskizze Weithalsfass 60 l, Artikel 824410 (graf.info Dimension_drawing/Massskizze_Weithalsfass_60l.pdf): Oe 398 oben, 370 Boden, Oeffnung 338, H 615, mit Deckel 625; Haendlerangaben Weithalsfass 60 l (OBI, Kaufland, toom; Graf 824410 und Nachbauten): Oe 400, H 620 bis 640 | mittel |
| Bioball-Bett 37 l | l | gerechnet | docs/research/R37.md Befund 10 (0,5 l Bioballs je g Futter bei 73 g/Tag) | mittel |
| Zulauf/Auslauf d25, 5 l/min | d25 | belegt (Netz) | data/leitungsnetz.json K42/K43 | hoch |
| Aufstrom mit Niederhalter, Tauchrohr bis 60 mm ueber Boden | Bauweise | Annahme | uebliche Fass-Biofilter-Bauweise, nicht recherchiert | niedrig |
| Wand 3, Boden 4, Lochplatte 10, Lagen der Stutzen | mm | Annahme | kein Datenblatt fuer Wand und Einbauten | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: Graf-Massskizze Weithalsfass 60 l, Artikel 824410 (graf.info Dimension_drawing/Massskizze_Weithalsfass_60l.pdf): Oe 398 oben, 370 Boden, Oeffnung 338, H 615, mit Deckel 625; Haendlerangaben Weithalsfass 60 l (OBI, Kaufland, toom; Graf 824410 und Nachbauten): Oe 400, H 620 bis 640; docs/research/R37.md Befund 10; data/leitungsnetz.json (Knoten biofilter_dritt, K42/K43)
- Abweichung zum OBJ: Keine OBJ-Vorgabe; Bauteil nach Netz und R37. Fass im Modell zylindrisch (Handelsfass leicht konisch, Boden Oe 370).

## Montage (L4)

1. Fass neben dem Drittbecken waagerecht aufstellen, Auslauf ueber dessen Wasserspiegel
2. Bioballs einfuellen, Lochplatte auflegen und gegen Auftrieb sichern (z. B. zwei Klemmleisten) [A]
3. Tauchrohr durch Lochplatte bis zum Boden schieben, Deckel mit Muffe aufschrauben, K42 einstecken
4. Luftschlauch mit Ausstroemer durch die Bohrung bis zum Boden fuehren; K43 an den Tankverbinder

**Werkzeug:** Lochsaege, PVC-Kleber, Bohrer 8 mm

## Stueckliste-Zeile

- T98 Biofilter Drittbecken: 1 Weithalsfass PE 60 l mit Schraubdeckel, 37 l Bioballs, 1 Lochplatte PE Oe 386 x 10, 1 Zulauf-Muffe d25 (Tankverbinder), 1 Tauchrohr d25 L 571, 1 Tankverbinder d25 (Auslauf)

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Weithalsfass PE 60 l | Oe 398 x 615 | Graf 824410 oder gleichwertig (Baumarkt DE) | offen [A] |
| Bioballs | 37 l | offen (Aquaristik-/Teichhandel EU) | offen [A] |
| Tankverbinder d25 | 2 Stueck | offen (N-BESCHAFFUNG) | offen [A] |

## Alternative lokale Fertigung

Lebensmittelechtes Weithalsfass aus dem Baumarkt; Lochplatte aus PE-Plattenrest zuschneiden.

## Renders


## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf.
- scripts/workshop/check_biofilter_dritt.py: Fassmass, Bettvolumen 37 l (+-2 %), Verweilzeit, Wasserstand ueber der Lochplatte, Tauchrohr unter dem Bett, Ports, Interferenz 0

## Offene Fragen

- Fassfabrikat: Wand und Konizitaet nicht im Modell [A]
- Niederhalter-Befestigung gegen Auftrieb der Bioballs [A]
- Luftmenge und Ausstroemer offen (R27 nennt Belueftung, keine Menge)
- Pumpe im Drittbecken fuer K42 gehoert nicht zu diesem Teil

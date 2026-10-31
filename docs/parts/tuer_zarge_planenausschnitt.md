# Bauteilblatt T44 tuer_zarge_planenausschnitt (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/tuer_zarge_planenausschnitt.json` und `designs/components/tuer_zarge_planenausschnitt.sc`, nicht von Hand aendern)

**Funktion:** Uebergang von der Tuer-Zarge zur Folie (D39, R24): Die Folie des Tuerfelds hat einen Planenausschnitt, der 25 mm kleiner ist als die Zarge. Ihre Kante liegt auf einem EPDM-Dichtband, das auf dem Kragen eines Aluminium-Aufsatzrahmens ruht; der Aufsatzrahmen steht mit seinem Steg auf dem Zargenrohr und hebt den Kragen auf die Hoehe der Folienebene (Z' 62, Folie bei 64). Die Klemmleiste presst die Folienkante von aussen auf das Dichtband. Der Rahmen umfasst Pfosten links und rechts und den Sturz; die Schwelle bleibt frei.

**Datei:** `designs/components/tuer_zarge_planenausschnitt.sc` · **Teilenummer:** T44 · **Revision:** A · **Bezugspunkt:** Feld-KS der Tuer (tuer_komplett): Ursprung Mitte der Basiskante auf Z 0, X tangential, Y' hangaufwaerts in der Feldebene, Z' Feldnormale nach aussen; Zargenrohre liegen Z' -15..+15, die Folie Z' 64

**Anzahl (Instanzen):** 1 (Quelle: docs/decisions.md D36: eine Tuer im Basisfeld BBB 149,2; data/components/tuer_komplett.json anzahl 1)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `web_t` | 3 | mm | [A] Aufsatzrahmen Aluminium 3 mm |
| `collar_w` | 40 | mm | [A] Kragen 40 mm breit: 5 mm Ueberstand je Seite ueber das 30er Zargenrohr; Folie liegt 30 mm auf dem Kragen |
| `collar_t` | 3 | mm | [A] Kragen 3 mm |
| `seal_w` | 20 | mm | [A] Dichtband EPDM 20 x 2 auf dem Kragen (unter der Folie) |
| `seal_t` | 2 | mm | [A] |
| `clamp_w` | 30 | mm | [A] Klemmleiste Alu-Flachprofil 30 x 3, ueber der Folienkante, mit dem Kragen verschraubt (Raster 150 mm, nicht modelliert) |
| `clamp_t` | 3 | mm | [A] |
| `notch_clear` | 2 | mm | [A] Luft der Ausklinkung im Steg um die Scharnier-Zargenlasche (Lage aus tuer_komplett.sc gemessen) |
| `screw_pitch` | 150 | mm | [A] Schraubenraster Klemmleiste (M5 Edelstahl), nicht modelliert |

Gesamt-Box (Messung): X -543.0 bis 543.0, Y 30.0 bis 2073.0, Z 15.0 bis 67.1 mm; Koerper: 3.

**Toleranzen / Spiel:** Folie liegt 30 mm auf dem Kragen (Ausschnitt 1026 x 2043, Kragen bis x +-543); Aussenkante der Zarge 538 gegen Kragenkante 543: 5 mm Ueberstand je Seite; lichte Weite der Tuer (Blatt 1000) bleibt frei, Steg-Innenkante bei x +-521,5; Ausklinkung Luft 2 mm um die Zargenlasche; Pruefung check_huelle.py zarge.

## Werkstoff und Gewicht

- Werkstoff: Aluminium EN AW-6060 (Rahmen, Klemmleiste), EPDM (Dichtband), Dichte 2.7 g/cm3, Farbe #c4c9ce (Handbuchwerte, Annahme)
- Volumen (Messung, `solidcraft-cli eval`): 1946.7 cm3 · Masse leer: 4929 g (4.93 kg)
- Gefuellt/in Betrieb: nicht zutreffend

## Querschnitt / Profil

Aufsatzrahmen Aluminium 3 mm: Steg 3 x 47 (Z' 15..62) auf dem Zargenrohr 30 x 30 x 2, Kragen 40 x 3 oben (Z' 59..62); Dichtband EPDM 20 x 2 (Z' 62..64); Folie 0,15 (Z' 64..64,15); Klemmleiste Alu 30 x 3 (Z' 64,15..67,15). Drei Ausklinkungen im linken Steg (je 94 x 6 mm) lassen die Scharnier-Zargenlaschen der Tuer frei.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Steg auf dem Zargenrohr (Pfosten links/rechts, Sturz) | Zargenrohr 30 x 30 x 2 (tuer_komplett) | x +-523 (Pfosten), y' 2053 (Sturz); Z' 15 (Unterkante Steg) | Steg steht auf der Zargen-Aussenflaeche, Richtung -Z' |
| Folienkante des Planenausschnitts | Ausschnitt 1026 x 2043 mm (huelle_folie_BBB_tuer) | x +-513, y' 2043, Z' 64 (Folie liegt auf dem Dichtband) | Folie wird von +Z' aufgelegt und von der Klemmleiste gehalten |
| Scharnier-Zargenlaschen der Tuer | 3 Stueck Flachstahl 48 x 90 x 4 | x -549..-501, y' 187..277 (Beispiel Scharnier 1), Z' 15..19 | Ausklinkung im linken Steg, Laschen bleiben frei |
| Offene Unterseite (Schwelle) | Folie endet 100 mm unter der Basiskante | y' 30 (Rahmen beginnt ueber der Schwelle) | unten kein Rahmen; Folienkanten dort an den Pfosten, Basis wie die uebrigen Basisfelder (Montage) |

## Verbindungen und Befestigungen

- Aufsatzrahmen am Zargenrohr: Steg auf dem Rohr mit Edelstahl-Winkeln 20 x 20 x 3 oder Schweissnaht (Alu auf Stahl verzinkt: Winkel plus Schrauben M5 empfohlen), Raster 300 mm [A, nicht modelliert]
- Klemmleiste am Kragen: Edelstahl-Schrauben M5 x 20 mit Mutter, Raster 150 mm (ca. 34 Stueck) [A, nicht modelliert]
- Dichtband EPDM 20 x 2 selbstklebend auf dem Kragen
- Folie: zwischen Dichtband und Klemmleiste geklemmt, nicht geklebt (R24: Folie nicht tackern auf Dauer)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Tuer als Planenausschnitt mit Zarge | 1 Stueck | Q | docs/research/R24.md Empfehlung 2; docs/decisions.md D39 | hoch |
| Zarge 1076 x 2068, Rohr 30 x 30 x 2, lichte 1016 x 2008 | mm | Q | data/components/tuer_komplett.json geometrie und parameter | hoch |
| Aufsatzrahmen Alu 3 mm, Steg 47, Kragen 40 | mm | A | Konstruktionspraxis; Steghoehe aus Folienebene Z' 64 minus Dichtband 2 minus Zargenoberflaeche 15 | niedrig |
| Dichtband EPDM 20 x 2 | mm | A | R24: Schaumband/Dichtung an der Folienkante | niedrig |
| Klemmleiste Alu 30 x 3, Folie 30 mm aufgelegt | mm | A | Konstruktionspraxis Folienbefestigung (Klemmleiste) | niedrig |
| Folienebene Z' 64 | 64 mm | E | huelle_folie foil_z0: Strebe 45 + Schaumband 3 + Kanal 15 + 1 | mittel |
| Ausklinkungen an den Scharnier-Zargenlaschen | 3 Stueck | E | aus designs/components/tuer_komplett.sc gemessen (Zargenlaschen Z' 15..19) | mittel |
| Dichte Aluminium 2,7 / EPDM 1,1 | g/cm3 | A | Handbuchwerte | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: data/components/tuer_komplett.json (Zarge, Ports), docs/research/R24.md (Tuer als Planenausschnitt mit Zarge); kein Referenzbild
- Quelle der Masse: data/components/tuer_komplett.json (Zarge Rechteckrohr 30 x 30 x 2, Zarge aussen 1076 x 2068, lichte 1016 x 2008, Schwelle 30), docs/research/R24.md (Tuer als Planenausschnitt mit Zarge), docs/decisions.md D39, data/components/huelle_folie.json (Planenausschnitt, Folienlage Z 64)
- Abweichung zum OBJ: Das Bauteil kommt nicht aus dem OBJ (Huelle als Plane, D39). R24 verlangt nur 'Tuer als Planenausschnitt mit Zarge'; Aufsatzrahmen, Dichtband und Klemmleiste sind eine Konstruktion der Werkstatt. Der Check fand im ersten Lauf 3 Interferenzen mit den Scharnier-Zargenlaschen der Tuer (je 1080 mm3); sie sind durch Ausklinkungen im Steg beseitigt (Lage aus tuer_komplett.sc gemessen).

## Montage (L4)

1. Zargenrohre reinigen; Aufsatzrahmen (drei Seiten) auf die Zarge setzen, an den Scharnierlaschen ausrichten und befestigen
2. Dichtband auf den Kragen kleben
3. Folie des Tuerfelds auflegen (Planenausschnitt auf dem Dichtband), die Klemmleiste auflegen und alle 150 mm verschrauben
4. Dichtheit pruefen (Zugluft an den Ecken), Folie am unteren Ende an der Schwelle befestigen

**Werkzeug:** Akkuschrauber, Schluessel M5, Cuttermesser, Massband

## Stueckliste-Zeile

- Aufsatzrahmen Alu 3 mm (Steg 47 hoch, Kragen 40 breit, Laenge 2043 + 1086 + 2043 mm) mit 3 Ausklinkungen: 1
- Dichtband EPDM 20 x 2 selbstklebend, ca. 5,1 m: 1
- Klemmleiste Alu-Flachprofil 30 x 3, ca. 5,2 m: 1
- Schrauben M5 x 20 Edelstahl mit Mutter: ca. 34 [A, nicht modelliert]
- Befestigungswinkel 20 x 20 x 3 Edelstahl: ca. 20 [A, nicht modelliert]

## Alternative lokale Fertigung

Handelsueblich: Aluwinkel und Flachprofil aus dem Baumarkt, Zuschnitt vor Ort; Dichtband aus der Rolle.

## Renders

- `renders/components/tuer_zarge_planenausschnitt/tuer_zarge_planenausschnitt-01-iso.png`
- `renders/components/tuer_zarge_planenausschnitt/tuer_zarge_planenausschnitt-02-querschnitt.png`

## Pruefung

- Gauntlet-Urteil: kein Pruefer-Lauf (Auftrag W27: Selbstcheck)
- scripts/workshop/check_huelle.py zarge: Ergebnis in renders/components/tuer_zarge_planenausschnitt/check.txt (Volumen gegen Querschnittsformel, Lage zu Zarge und Folie, gemeinsames Tuerfeld mit tuer_komplett und huelle_folie_BBB_tuer: Interferenzen 0)
- Kein Bild-Kritiker und kein Spec-Pruefer (Auftrag W27)

## Offene Fragen

- Tuer-Aufschlag: Das Tuerblatt oeffnet nach aussen; der Aufsatzrahmen und die Klemmleiste liegen ausserhalb der Blattbreite (x +-500, Rahmen ab 521,5), aber der Schwenkbereich ueber den Rahmen ist nicht geprueft
- Die aeussere Folienlage (Z' 164) ist hier nicht geklemmt: Das Luftpolster aus zwei parallelen Ebenen ist ein Platzhalter; real treffen sich beide Lagen an der Klemmleiste
- Befestigung des Aufsatzrahmens am Zargenrohr (Winkel, Schrauben) und die Klemmleisten-Schrauben sind nicht modelliert (Raster 150 mm, ca. 34 Stueck)
- Der Rahmen hat keine Eckverbindung (Gehrung/Schweissnaht); im Modell ein Koerper
- Folienende an der Schwelle (unten offen) ist nicht entschieden: Montage legt die Befestigung fest
- Wasser- und Windlast an der Folienkante nicht gerechnet

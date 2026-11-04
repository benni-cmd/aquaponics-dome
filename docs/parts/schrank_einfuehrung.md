# Bauteilblatt T89 schrank_einfuehrung (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/schrank_einfuehrung.json` und `designs/components/schrank_einfuehrung.sc`, nicht von Hand aendern)

**Funktion:** Fuehrt die Kabel unterirdisch in den Schaltschrank: eine Einfuehrungsplatte im Schrankboden (800 x 500, Blech 3 mm) nimmt zwei Kabeleinfuehrungen auf, DN100 fuer den 230-V-Stamm (Pumpen, Geblaese) und DN50 fuer den Signal-Stamm (Sensoren). Darunter laeuft je ein Leerrohr-Bogen 90 Grad nach aussen (DN100 nach -X, DN50 nach +X) in die Erde. Die Achsen sind 300 mm auseinander (freier Abstand der Muffen 210,5 mm gegen 200 mm EMV). Nur das Bauteil: Standort des Schranks OFFEN (E13), Kabelzahl und Fuellgrad OFFEN (E20)

**Datei:** `designs/components/schrank_einfuehrung.sc` · **Teilenummer:** T89 · **Revision:** A · **Bezugspunkt:** Mitte der Boden-Unterkante des Schaltschranks (Z 0 = Unterkante Schrankboden, Boden Z 0 bis 3); X Schrankbreite, Y Schranktiefe, Z nach oben in den Schrank; Leerrohre darunter bei negativem Z. Standort im Modell: NICHT enthalten (OFFEN E13)

**Anzahl (Instanzen):** 1 am Schaltschrank (Quelle: Auftrag W37-3 Teil 4; Netz-Kabeleintraege (Schaltschrank))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `cab_x` | 800 | mm | [E] data/params.json cab_x (Schrankbreite, gelesen); [A] ref-5 geschaetzt |
| `cab_y` | 500 | mm | [E] data/params.json cab_y (Schranktiefe, gelesen) |
| `boden_t` | 3 | mm | [A] Blech 3 mm wie lt_kabeleinfuehrung (Boden der Einfuehrung, W39 KAB boden) |
| `wand_t` | 2 | mm | [A] Schrankwand-Stummel 2 mm (nur fuer die Interferenzpruefung) |
| `wand_h` | 100 | mm | [A] Hoehe des Wandstummels ueber dem Boden (Schrank 1200 hoch, hier nur der Fussbereich) |
| `x_dn100` | -150 | mm | [A] Achse der Einfuehrung DN100 (230 V); Abstand der beiden Achsen 300: freier Abstand der Muffen 300 - 61,5 - 28 = 210,5 mm gegen 200 mm EMV |
| `x_dn50` | 150 | mm | [A] Achse der Einfuehrung DN50 (Signal) |
| `y_achse` | 0 | mm | [A] beide Achsen auf der Mittellinie der Schranktiefe |
| `emv_min` | 200 | mm | [E] Plan Abschnitt 4 Regel 9: Abstand 230 V gegen Signal mindestens 200 mm (Auftrag W37-3) |

Gesamt-Box (Messung): X -734.0 bis 510.0, Y -250.0 bis 250.0, Z -654.5 bis 103.0 mm; Koerper: 10.

**Toleranzen / Spiel:** Leerrohr-Ende B stoesst an den Muffen-Anschlag (Einstecktiefe voll); Loch gleich Halsdurchmesser (kein Spiel modelliert); Dichtung Auflage ohne Pressung.

## Werkstoff und Gewicht

- Werkstoff: Stahlblech (Boden, Wandstummel), PP und EPDM (Kabeleinfuehrung), PVC-U (Leerrohr-Bogen), Dichte 7.85 g/cm3, Farbe #9aa0a4 ([A] Platzhalter; Blech Stahl, Rest aus den Bibliotheksteilen)
- Volumen (Messung, `solidcraft-cli eval`): 3400.2 cm3 · Masse leer: 15336 g (15.34 kg)
- Gefuellt/in Betrieb: keine Fuellung; Masse leer siehe Messung (Stahlblech Platzhalter)

## Querschnitt / Profil

Boden 800 x 500 x 3 (Unterkante Z 0) mit zwei Loechern (DN100: Ø 130 bei X -150; DN50: Ø 63 bei X +150); Kabeleinfuehrungen W39: Dichtung unter dem Boden, Gegenmutter auf dem Boden, Gewindehals 15 ueber der Unterkante; Leerrohr-Bogen DN100 (R 500) und DN50 (R 300) mit Ende B in der Muffe der Einfuehrung (Stoss, Z -9). Wandstummel 2 x 100 umlaufend (nur fuer die Interferenzpruefung).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Leerrohr DN100 (Muffe A, 230 V) | PVC-U DN100 (AD 110), Muffe | x -734, y 0, z -593 (Mitte der Oeffnung) | Oeffnung zeigt -X (unterflur, Z bis -654); das Leerrohr (lt_leerrohr_dn100, glattes Ende) wird eingesteckt |
| Leerrohr DN50 (Muffe A, Signal) | PVC-U DN50 (AD 50), Muffe | x 510, y 0, z -369 (Mitte der Oeffnung) | Oeffnung zeigt +X (unterflur, Z bis -397) |
| Kabel DN100 in den Schrank | Kabeldurchgang Innen-Ø 103,6 | x -150, y 0, z 15 | Oeffnung zeigt +Z (nach oben in den Schrank) |
| Kabel DN50 in den Schrank | Kabeldurchgang Innen-Ø 46,4 | x 150, y 0, z 15 | Oeffnung zeigt +Z (nach oben in den Schrank) |

## Verbindungen und Befestigungen

- Schrankboden: Bodenblech gegen die Schrankwand (Wandstummel) nur Pruefhilfe; echter Schrank siehe schaltschrank.sc (von gen_dome.py erzeugt, hier nicht angefasst)
- Kabeleinfuehrung: Hals durch den Bodenausschnitt, Dichtung unter dem Boden, Gegenmutter oben
- Leerrohr: Bogen B in der Muffe der Einfuehrung, Bogen A nimmt das Leerrohr auf (Abzweige nur mit Zugdose, W39)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Boden 800 x 500 | 800 x 500 x 3 | E/A | data/params.json cab_x 800, cab_y 500 (ref-5 geschaetzt, nur gelesen); Blech 3 mm [A] | niedrig |
| Einfuehrungen DN100 und DN50 | aus W39 | E | docs/parts/leitungsteile.md Ergaenzung W39 (lt_kabeleinfuehrung); Loch = Halsdurchmesser | mittel |
| Leerrohr-Boegen | R 500 und R 300 | E | docs/parts/leitungsteile.md W36 (lt_leerrohr_bogen90_dn*) | mittel |
| Abstand 230 V gegen Signal | Achsen 300, Muffen 210,5 | A | Plan Abschnitt 4 Regel 9 und Auftrag W37-3 (mindestens 200 mm) | mittel |
| Standort Schrank | nicht enthalten | offen | OFFEN (E13) | - |
| Kabelzahl und Fuellgrad | nicht enthalten | offen | OFFEN (E20) | - |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: data/params.json cab_x 800, cab_y 500, cab_z 1200 ([A] ref-5 geschaetzt, nur gelesen); docs/parts/leitungsteile.md (Ergaenzung W39: Kabeleinfuehrung DN50/DN100; W36: Leerrohr-Bogen); scripts/workshop/leitung_w39.py (kab_geom) und leitung_w36.py (LR); docs/jobs/W37-3-luft-schaltschrank.md Teil 4 (EMV-Abstand 200 mm, Plan Abschnitt 4 Regel 9)
- Abweichung zum OBJ: Kein OBJ-Bestand. Der Schaltschrank selbst ist weiter schaltschrank.sc (gen_dome.py, 'neben den Vorbau' D62); die Einfuehrung ist ein eigenes Bauteil mit lokalen Koordinaten.

## Montage (L4)

1. Standort des Schranks klaeren (E13) und erst dann die Einfuehrung mit ihrem Nullpunkt dort setzen; die Platte ersetzt im Montagemodell den Schrankboden des Standorts
2. Leerrohr-Boegen unterflur einbauen: DN50 bis Z -397, DN100 bis Z -654 relativ zum Schrankboden (R 500 des Bogens; Plan Z -100 bis -400 nur mit kleinerem Bogen oder zwei 45-Grad-Boegen)
3. Kabeleinfuehrungen im Boden verschrauben, Leerrohre einstecken, 230 V und Signal in getrennte Stamm legen (200 mm Abstand)

**Werkzeug:** Stufenbohrer oder Lochsaege fuer die Ausschnitte, Leerrohr-Schneider, Klebstoff PVC

## Stueckliste-Zeile

- 1 Einfuehrungsplatte 800 x 500 x 3 mit zwei Ausschnitten (Boden des Schaltschranks)
- 1 Kabeleinfuehrung DN100 und 1 Kabeleinfuehrung DN50 (W39: lt_kabeleinfuehrung_dn100, _dn50)
- 1 Leerrohr-Bogen 90 Grad DN100 und 1 DN50 (W36: lt_leerrohr_bogen90_dn100, _dn50)
- Geblaese-Strom 204 W je Pumpe und 8 Pumpenkabel: Hinweis fuer die Kabelrechnung des Orchestrators, hier nicht berechnet

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Kabelschutzrohr 110 mm (DN100) | AD 110, Innen 94 (Fraenkische) | Fraenkische Kabuflex S NW 110, Art. 0000185796, 25,46 EUR (DE) [Q-Treffer, Blatt W37-3] | nur eine Quelle; Aussen-Ø 110, Innen 94: Bauteilmass AD 110 passt; Innen-Ø der Bibliothek 103,6 |
| Kabelschutzrohr 50 mm (DN50) | AD 50 | Fraenkische Kabuflex R plus 50, Art. 19210050 (DE) [Q-Treffer], mehrere im Preisvergleich | beschaffbar (mehrere Haendler im Preisvergleich); Ring zu 50 m |
| Einfuehrungsplatte / Schrankboden | 800 x 500 x 3 | Rittal SZ 8800.100 (DE) [Q-Treffer, PDF nicht lesbar] | offen; Schrankserie und Breite (800 x 500 x 1200 [A]) vor der Wahl klaeren |
| Kabeleinfuehrung mit Dichtung (Flansch, Gegenmutter) | DN100 und DN50 | Katalog offen, N-BESCHAFFUNG (W47); Bibliotheksteile lt_kabeleinfuehrung_dn100/dn50 (W39) | offen |

## Alternative lokale Fertigung

Handelsteile; Einfuehrungsplatte als Blech nach Mass.

## Renders

- `renders/components/schrank_einfuehrung/schrank_einfuehrung-01-schraeg.png`
- `renders/components/schrank_einfuehrung/schrank_einfuehrung-02-seite.png`
- `renders/components/schrank_einfuehrung/schrank_einfuehrung-03-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf (Auftrag W37-3: Selbstcheck; gebuendelter Pruefer W37-2/W37-3 folgt).
- scripts/workshop/check_schrank_einfuehrung.py (Ergebnis renders/components/schrank_einfuehrung/check.txt): Boden gegen params.json (cab_x, cab_y), beide Einfuehrungen mit Loch, Dichtung und Mutter, Achsabstand 300 und EMV-Abstand 210,5 mm, Leerrohr-Enden, Ports, Interferenz 0 inklusive Schrankwand; schaltschrank.sc und gen_dome.py unveraendert

## Offene Fragen

- OFFEN (E13): Standort des Schaltschranks (Ben); gen_dome.py setzt ihn heute neben den Vorbau (D62), Az -85 / r 5750 ist nur Kabelrechnung
- OFFEN (E20): Kabelzahl und Fuellgrad je Stamm (A+: Durchfluss-/Pegelwaechter, 2 Sensoren; B und C: Booster bzw. Ring-Pumpen, 548 W bzw. 503 W gegen 430 W in A; Entscheidung Ben 05.11.)
- OFFEN (D75, geparkt): Tauchpumpen im Subtank beruehren nur die Kabelzahl
- DN100-Bogen R 500 liegt tiefer (Z -654) als die Plantiefe -400 (Plan nannte Z -100 bis -400): Entscheidung Montage/Planer, kleinerer Bogen oder zwei 45-Grad-Boegen
- Einfuehrungsplatte Handelsartikel (Rittal SZ 8800.100) und Schrankserie offen (N-BESCHAFFUNG W47)

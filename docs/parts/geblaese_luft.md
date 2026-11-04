# Bauteilblatt T85 geblaese_luft (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/geblaese_luft.json` und `designs/components/geblaese_luft.sc`, nicht von Hand aendern)

**Funktion:** Eine Luftpumpe samt Luftleitung: die Linear-Membranpumpe (Platzhalterquader) blaest durch einen Stutzen d20, die Leitung steigt senkrecht auf Z 710 ueber den hoechsten Wasserspiegel (Pool-Rand Z 650 plus 60, Spiegel Z 515), biegt waagerecht ab und fuehrt durch ein Rueckschlagventil d20 zum Luftaustritt. Zwei Stueck (N+1: eine laeuft, die zweite ist Reserve; die Spitze 205 l/min braucht beide). Die Schleife ueber dem Spiegel ist der Hauptschutz gegen Rueckfluss von Wasser in die Pumpe, das Ventil die zweite Sperre. Gilt in jeder Kreislaufvariante (E20): Luft laeuft getrennt vom Wasserumlauf, Luftausfall ist der harte Termin (0,8 bis 1,2 h bis 3 mg/l, R45)

**Datei:** `designs/components/geblaese_luft.sc` · **Teilenummer:** T85 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche der Pumpe am Boden (Z 0 = Aufstellflaeche); X zeigt zum Luftaustritt, Y quer (Netzkabel -Y), Z hoch; Rohrachse der Schleife bei Z 710, Port Luftaustritt am Ende des Austrittsrohrs (+X)

**Anzahl (Instanzen):** 2 Stueck (N+1: eine Pumpe laeuft, die zweite ist Reserve; Spitze 205 l/min nur mit beiden) (Quelle: R45 Abschnitt 4 Empfehlung 3 und 4; D45 e (Reserve-Geblaese))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `box_x` | 240 | mm | [A] Platzhalter nach Beispielreihe Secoh JDK-S-200 (BIBUS, R53: 240 x 180 x 230,5); Typ nicht gewaehlt, aus Katalog nachzumessen |
| `box_y` | 180 | mm | [A] wie box_x |
| `box_z` | 230 | mm | [A] wie box_x |
| `pump_mass_g` | 10000 |  | [A] 10,0 kg (Secoh JDK-S-200, BIBUS [Q] R53; Hiblow HP-200 8,5 bis 9 kg); Gehaeuse als Vollquader, Dichte so gesetzt, dass die Pumpe 10 kg wiegt |
| `foot_d` | 40 | mm | [A] Gummifuss Ø 40 |
| `foot_h` | 15 | mm | [A] Gummifuss Hoehe 15 |
| `foot_x` | 90 | mm | [A] Fussmitte x (innerhalb der 240er Grundflaeche) |
| `foot_y` | 60 | mm | [A] Fussmitte y (innerhalb der 180er Grundflaeche) |
| `out_d` | 20 | mm | [A] Luftaustritt d20 (Auftrag W37-3 Teil 1; R45: d20/d25); weiter ueber Reduzierung auf d25 zum Verteiler |
| `out_l` | 40 | mm | [A] Stutzen Laenge ueber dem Gehaeuse |
| `bend_r` | 80 | mm | [A] Biegeradius der Rohrschleife (4 x d, warm gebogen) |
| `apex_z` | 710 | mm | [E] Rohrachse der Schleife ueber der Aufstellflaeche: Pool-Rand Z 650 (params pool_rim) + 60 wie Schwimmerventil = Z 710; Wasserspiegel Z 515 (layout pool2.water_z) -> Reserve 195 mm. R45 Empfehlung 7: 'ueber dem hoechsten Wasserspiegel'; Aufstellflaeche Z 0 angenommen (E13 offen) |
| `arm_l` | 150 | mm | [A] waagerechter Schenkel nach dem Bogen bis zum Rueckschlagventil |
| `out_tube_l` | 100 | mm | [A] Austrittsrohr hinter dem Rueckschlagventil bis Port Luftaustritt |
| `cable_d` | 8 | mm | [A] Netzkabel Ø 8 (Stummel Platzhalter) |
| `cable_l` | 100 | mm | [A] Netzkabel-Stummel Laenge |
| `cable_x` | -80 | mm | [A] Netzkabel x-Lage an der Rueckseite |

Gesamt-Box (Messung): X -120.0 bis 412.0, Y -190.0 bis 90.0, Z 0.0 bis 729.5 mm; Koerper: 10.

**Toleranzen / Spiel:** Rohre stossen stumpf an das Rueckschlagventil (Muffentiefe 16 nicht modelliert); Pumpe als Vollquader, Dichte so gesetzt, dass die Pumpe 10,0 kg wiegt ([A], Beispiel Secoh JDK-S-200 laut BIBUS).

## Werkstoff und Gewicht

- Werkstoff: Gehaeuse Aluminium/Kunststoff (Platzhalter), Fuesse Gummi, Luftleitung PVC-U, Dichte 1.0 g/cm3, Farbe #2f3a44 ([A] Platzhalter; Dichte des Quaders so, dass 10,0 kg erreicht werden ([Q] Secoh JDK-S-200))
- Volumen (Messung, `solidcraft-cli eval`): 10155.4 cm3 · Masse leer: 10291 g (10.29 kg)
- Gefuellt/in Betrieb: Luft fuehrend; Pumpe 10 kg [A, Beispiel]

## Querschnitt / Profil

Pumpe 240 x 180 x 230 auf vier Gummifuessen Ø 40 x 15; Stutzen d20 x 1,8 (40 lang) oben; Rohrschleife d20 mit Biegeradius 80, senkrechter Schenkel bis Z 710 (Mitte), waagerecht 150; Rueckschlagventil d20 (Gehaeuse Ø 39, Laenge 82); Austrittsrohr 100. Netzkabel Ø 8 an der Rueckseite (-Y).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Luftaustritt (Zapfen) | PVC-U d20 (DN15), Zapfen, Austrittsrohr | x 412, y 0, z 710 (Mitte der Stirnflaeche) | Oeffnung zeigt +X; weiter ueber Reduzierung d20 auf d25 und T-Stueck d25 beider Pumpen in Port A des Hauptverteilers (luftverteiler_6) |
| Stromanschluss (Kabelende) | 230 V, 1 Ader-Stueck laut Netz (204 W Fischwasser-Belueftung) | x -80, y -190, z 130 | Stirnflaeche zeigt -Y; Kabel zur Kabeleinfuehrung DN100 des Schaltschranks (schrank_einfuehrung); Kabelrechnung Orchestrator, hier nicht berechnet |

## Verbindungen und Befestigungen

- Port Luftaustritt: Rohr d20 zur Reduzierung d20/d25, dann T-Stueck d25 zu Luftverteiler 6 (Hauptverteiler Port A)
- Befestigung: Pumpe auf Gummifuessen im Schaltschrankbereich (Standort E13 OFFEN); Netzkabel 230 V zur Einfuehrung
- Schleife: Scheitel (Rohrachse) Z 710, Reserve 195 mm ueber dem Spiegel Z 515 und 60 mm ueber dem Pool-Rand Z 650

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Pumpenklasse | 200 l/min bei mindestens 26 kPa, N+1 | E | R45 Abschnitt 4 Empfehlung 3 und 4; Planwert 130, Spitze 205 l/min | mittel |
| Pumpenmasse | 240 x 180 x 230, 10 kg | A | Beispielreihe Secoh JDK-S-200 (BIBUS: 240 x 180 x 230,5, 10,0 kg [Q R53]); Typ nicht gewaehlt | niedrig |
| Kennlinie bei 26 kPa | 176 l/min (Fortschreibung) | E | R53 Abschnitt 4: 200 - 20 x (260-200)/50, nur Fortschreibung der Secoh-Tabelle; Hiblow HP-200 200 l/min bei 20 kPa, Bereich bis 35,3 kPa [Q] | niedrig |
| Schleife ueber dem Spiegel | Rohrachse Z 710 | E | R45 Empfehlung 7, params.json pool_rim 650 + 60 (wie Schwimmerventil); layout pool2.water_z 515 (nur gelesen) | mittel |
| Rueckschlagventil d20 | Laenge 82, Gehaeuse Ø 39 | A | Muster lt_rueckschlagventil_d20 (W39); Katalog offen | niedrig |
| Leistung | 204 W (Netz-Kabeleintrag) | Q | data/leitungsnetz.json kabel schaltschrank -> geblaese_fisch (nur gelesen, nicht berechnet) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R45-hydraulik-auslegung.md Abschnitt 4 (Empfehlung 3, 4, 7); docs/research/R53-europa-frischwasser-luft.md Abschnitt 4 (Secoh JDK-S-200: 240 x 180 x 230,5 mm, 10,0 kg, BIBUS [Q]) und 5; data/leitungsnetz.json Kabel schaltschrank -> geblaese_fisch 204 W (nur gelesen); data/layout.json pool2.water_z 515 und data/params.json pool_rim 650 (nur gelesen)
- Abweichung zum OBJ: Kein OBJ-Bestand (Geblaese fehlte, L06).

## Montage (L4)

1. Pumpe im Schaltschrankbereich auf ebener Flaeche aufstellen (Standort E13 OFFEN); Aufstellflaeche gilt als Z 0 im Bauteil, bei anderer Hoehe die Schleife anpassen: Scheitel absolut auf Z 710 halten
2. Stutzen d20 mit der Rohrschleife verkleben, Rueckschlagventil in Flussrichtung (nach +X) einkleben, Austrittsrohr anschliessen
3. Zwei Baugruppen nebeneinander; beide Austritte ueber T-Stueck d25 und Reduzierung auf d40 in den Hauptverteiler (Port A) fuehren
4. Netzkabel mit Reserve zur Kabeleinfuehrung DN100 fuehren (230-V-Stamm)

**Werkzeug:** Rohrschneider, Heissluft zum Biegen (oder Formbogen aus der Bibliothek), Klebstoff PVC

## Stueckliste-Zeile

- 2 Linear-Membranpumpen der Klasse 200 l/min bei mindestens 26 kPa (Typ nicht gewaehlt)
- 2 Rueckschlagventile d20
- 2 Rohrschleifen d20 (Rohr d20, Biegung R80) mit Austrittsrohr
- 2 Reduzierungen d25/d20 und 1 T-Stueck d25 zum Hauptverteiler

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Linear-Membranpumpe 200 l/min | Klasse 200 l/min bei mindestens 26 kPa, 100 bis 250 W, 42 bis 48 dB | Hiblow HP-200: Hiblow France S.A.S. und Spain S.L., Katalog 2015 gelesen [Q R53], Haendler eBay.de [Q-Treffer]; Secoh JDK-S-200: BIBUS (HU/NL) [Q R53] und tanks.ie (IE, SKU 0022090, 372,70 EUR netto) [Q R53] | beschaffbar als Geraet (Secoh: zwei europaeische Haendler; Hiblow: Hersteller-Niederlassungen); Kennlinie bei 26 kPa OFFEN, Fortschreibung 176 l/min [E, Vorbehalt]; Typ NICHT gewaehlt |
| Rueckschlagventil d40, d25, d20 (Klebemuffe) | d20, PVC-U Klebemuffe | Baenninger Art. 75328, 75326, 75325 (schwarte-shop, DE), 15,67 bis 35,93 EUR [Q-Treffer, R53 Abschnitt 5, aus dem Blatt W37-3 uebernommen]; zweite Quelle (Bevo) Zuordnung ungeprueft | nur eine Quelle; Luft nicht freigegeben (Seite nennt Wasser, PN16), Oeffnungsdruck bei 130 l/min ungeprueft; Ersatz fuer kleine Leitungen Luftschlauch-Rueckschlagventile (Tetra CV4 u. a. [Q-Treffer R53]), fuer d40 keine belegt |
| Rohr d20 PVC-U (Schleife, Austritt) | d20 x 1,8 | Katalog offen, N-BESCHAFFUNG (W47) | offen |
| Reduzierung d25/d20 am Austritt | PVC-U Klebemuffen | Bevo Profec (NL), schwarte-shop (DE), Artikel d25/d20 nicht geoeffnet [A] | offen bis Artikel; Bibliotheksteil lt_reduzierung_d25_d20 vorhanden |

## Alternative lokale Fertigung

Handelsteil (Pumpe); Schleife aus Rohr d20 oder Formbogen.

## Renders

- `renders/components/geblaese_luft/geblaese_luft-01-schraeg.png`
- `renders/components/geblaese_luft/geblaese_luft-02-seite.png`
- `renders/components/geblaese_luft/geblaese_luft-03-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf (Auftrag W37-3: Selbstcheck; gebuendelter Pruefer W37-2/W37-3 folgt).
- scripts/workshop/check_geblaese_luft.py (Ergebnis renders/components/geblaese_luft/check.txt): 10 Koerper, Pumpe 240 x 180 x 230 und 10 kg, Fuesse auf Z 0, Schleife Rohrachse Z 710 (Reserve 195 ueber Spiegel, +60 ueber Pool-Rand), Volumen der Schleife nach Pappus, Rueckschlagventil, Stoss-Kontakte, Ports (Luftaustritt +X, Strom -Y), Interferenz 0

## Offene Fragen

- Pumpentyp NICHT gewaehlt: Kennlinie bei 26 kPa OFFEN (R53: Hiblow HP-200 200 l/min nur bei 20 kPa, Fortschreibung 176 l/min bei 26 kPa [E, Vorbehalt]); DEINE HANDLUNG (Ben): Kennlinie bei BIBUS, Hiblow France oder Nitto Kohki Europe anfragen
- Spitze 205 l/min traegt nur eine Pumpe nicht: N+1 faellt bei Parallellauf weg (Auslegungsfrage Ben/Planung)
- Rueckschlagventil: Luft nicht freigegeben (Seite nennt Wasser, PN16), Oeffnungsdruck bei 130 l/min ungeprueft; Regel Schleife ueber dem Spiegel zweite Quelle nur teilweise (R53 Abschnitt 5), Hoehe Z 710 bleibt [A]
- Notstromkonzept fuer die Pumpen OFFEN (Ben/Orchestrator; R45 Abschnitt 4)
- Standort Schaltschrankbereich OFFEN (E13)

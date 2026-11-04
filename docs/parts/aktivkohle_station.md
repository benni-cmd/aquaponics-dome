# Bauteilblatt T83 aktivkohle_station (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/aktivkohle_station.json` und `designs/components/aktivkohle_station.sc`, nicht von Hand aendern)

**Funktion:** Entchlort das Frischwasser (D66) vor dem Pool und der Quarantaene: Wasser von aussen (K39) laeuft ueber Absperrhahn, Sedimentvorfilter 20 um und zwei Kompositbehaelter mit katalytischer Kohle in Reihe (je 21 l Bett, 10,5 min Kontaktzeit bei 4 l/min), ein Probehahn zwischen den Behaeltern zeigt den Durchbruch (Chlortest DPD), ein Durchflussbegrenzer haelt 4 l/min. Hinter dem Begrenzer gehen K40 (zum Pool, d25), K41 (zur Quarantaene, d20) und K52 (Ansatz der Stammloesung von Hand, d25) ab; jeder Abgang hat einen Kugelhahn. Handelsteile, kein Eigenbau-Behaelter, keine Vorratsflaeche.

**Datei:** `designs/components/aktivkohle_station.sc` · **Teilenummer:** T83 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche von Behaelter 1 am Boden (Z 0); X Laengsachse (Sedimentgehaeuse -X, Behaelter 2 +X, Eingang -X, Ausgang +X), Y quer (K41 +Y, K52 -Y, Probehahn +Y), Z hoch; Leitungsachse Z 839,5

**Anzahl (Instanzen):** 1 Station (2 Behaelter, 1 Vorfilter) (Quelle: Netz Version 3: Knoten aktivkohle (K39, K40, K41, K52); D66)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `behaelter` | 2 |  | [A] R45 Empfehlung: 2 Behaelter in Reihe (Auslegung auf Chloramin); bei Chlor genuegt 1 (Wert 1 laesst Behaelter 2 samt Kopf weg) |
| `vessel_d` | 254 | mm | [A] Handelsmass Kompositbehaelter 10 x 35 Zoll (R45 Zeile 316: Ø 254 x 889); Fabrikat offen |
| `vessel_h` | 889 | mm | [A] Handelsmass 10 x 35 Zoll: 889 mm Gesamthoehe einschliesslich Kopf (R45: stehend 0,9 m hoch) |
| `head_h` | 99 | mm | [A] Hoehe des Kopfes mit Bypass-/Absperrhahn; Mantelhoehe = vessel_h - head_h |
| `head_w` | 120 | mm | [A] Kopfblock Breite und Tiefe, Anschluss d25 an den Seitenflaechen |
| `vessel_wall` | 5 | mm | [A] Wand Komposit/PE-Liner; Handelswerte schwanken |
| `bed_d` | 240 | mm | [A] Innen-Ø 244 abzgl. 4 mm Spiel; Bett Ø 240 |
| `bed_l` | 464 | mm | [E] Bettvolumen 21 l = pi x 120^2 x 464 (R45: je Behaelter ca. 21 l Bett) |
| `bed_z0` | 10 | mm | [A] Bett steht 10 mm ueber dem Boden (Drainagekopf/Rost nicht modelliert) |
| `vessel_pitch` | 330 | mm | [A] Achsabstand der Behaelter (76 mm Luft zwischen den Mantelflaechen) |
| `sed_d` | 112 | mm | [A] Handelsmass Sedimentgehaeuse 10 Zoll (Slim-Line): Ø ca. 112 (Q-Treffer R53, Fabrikat offen) |
| `sed_h` | 290 | mm | [A] Gehaeusehoehe 10 Zoll ohne Kopf |
| `sed_wall` | 4 | mm | [A] Wand Gehaeuse |
| `sed_cart_d` | 63 | mm | [A] Patrone PP 20 um, 10 Zoll: Ø 63 x 250 (Handelsmass) |
| `sed_cart_h` | 250 | mm | [A] Patronenlaenge 10 Zoll |
| `sed_stand` | 160 | mm | [A] Konsole unter dem Sedimentgehaeuse: Kantenlaenge; Hoehe = Mantelhoehe der Behaelter - Gehaeusehoehe (Kopf auf gleicher Hoehe) |
| `pipe_d` | 25 | mm | [E] R45 / Netz: K39, K40, K52 d25 |
| `pipe_d_abz` | 20 | mm | [E] Netz: K41 d20 |
| `hahn_l` | 50 | mm | [A] Baulaenge Kugelhahn (Bibliothek lt_kugelhahn: 50 zwischen den Muffen); hier Platzhalter-Koerper |
| `lim_d` | 32 | mm | [A] Durchflussbegrenzer G 3/4 (Kobold KM-020A, R53 Abschnitt 2: G 3/4 aussen, DN 20): Koerper Ø 32; Fabrikat nur Datenblatt, Katalog offen |
| `lim_l` | 60 | mm | [A] Baulaenge Begrenzer einschliesslich Gewinde-Uebergaenge (Platzhalter) |
| `tap_d` | 24 | mm | [A] Probehahn Rotguss (Kemper 1870000600 / SYR 6705.10.050, R53 Abschnitt 3: D 48 bzw. 86 x 144, G 1/4): Koerper Ø 24 als Platzhalter |
| `tap_l` | 55 | mm | [A] Hahnkoerper Laenge (Platzhalter) |
| `spout_d` | 12 | mm | [E] R45 Zeile 305: Probehahn d12 (Auslauf-Tuelle); Anschluss des Handelshahns ist G 1/4 (R53), 'd12' = Tuellenmass |
| `spout_l` | 30 | mm | [A] Tuelle Laenge |
| `x_in` | -800 | mm | [A] Lage Eingangsrohrende (Port K39) |
| `t1_x` | 165 | mm | [E] Mitte zwischen Behaelter 1 (Ausgang x 60) und Behaelter 2 (Eingang x 270): Probehahn-T |
| `lim_x` | 410 | mm | [A] Anfang des Begrenzers 20 mm hinter Behaelter 2 (Ausgang x 390) |
| `t2_x` | 560 | mm | [A] Abzweig K41 (+Y) hinter dem Begrenzer |
| `t3_x` | 700 | mm | [A] Abzweig K52 (-Y) hinter K41 |
| `x_out` | 900 | mm | [A] Lage Ausgangsrohrende (Port K40) |
| `abz_y` | 250 | mm | [A] Abzweigrohre enden bei y = +-250 |
| `tap_y` | 120 | mm | [A] Probehahn-Tuelle endet bei y = 120 |

Gesamt-Box (Messung): X -800.0 bis 900.1, Y -250.0 bis 250.0, Z -0.0 bis 929.0 mm; Koerper: 43.

**Toleranzen / Spiel:** Handelsmass-Platzhalter ohne Katalog; Bett 4 mm Spiel zur Innenwand; Rohre stossen stumpf an die Koepfe und Formstuecke (Muffeneinstecktiefe nicht modelliert).

## Werkstoff und Gewicht

- Werkstoff: PVC-U grau (Verrohrung), Komposit (Behaelter), Messing (Begrenzer), Dichte 1.4 g/cm3, Farbe #8d9296 ([A] Verrohrung PVC-U wie Bibliothek; Behaelterwerkstoff Handelsangabe offen)
- Volumen (Messung, `solidcraft-cli eval`): 25590.7 cm3 · Masse leer (ohne Kohlebett): 29247 g (29.25 kg)
- Gefuellt/in Betrieb: 2 Betten trocken je 9,3 kg; nass Bett 21 l Kohle + Porenwasser rund 10 l je Behaelter [A]

## Querschnitt / Profil

Leitungsachse d25 (PVC-U, Wand 1,8) auf Z 839,5; Sedimentgehaeuse (Ø 112) auf Konsole, zwei Behaelter Ø 254 stehend auf dem Boden, jeder Kopf 120 x 120 x 99 mit Seitenanschluessen; Hoehe aller Koepfe 889.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Eingang K39 (Frischwasser von aussen) | PVC-U d25 (DN20), Zapfen, Absperrhahn d25 dahinter | x -800, y 0, z 839,5 (Rohrende, Mitte) | Oeffnung zeigt -X; 4 l/min begrenzt, Spitze 10 l/min vor dem Begrenzer |
| Ausgang K40 (zum Pool, Schwimmerventil) | PVC-U d25 (DN20), Zapfen, Kugelhahn d25 | x 900, y 0, z 839,5 | Oeffnung zeigt +X; Zulauf zum Schwimmerventil am Pool |
| Abzweig K41 (Quarantaene, 2 l/min) | PVC-U d20 (DN15), Zapfen, Kugelhahn d20, Reduzierung d25 auf d20 | x 560, y 250, z 839,5 | Oeffnung zeigt +Y; Wasserwechsel Drittbecken |
| Abzweig K52 (Stammloesung von Hand) | PVC-U d25 (DN20), Zapfen, Kugelhahn d25 | x 700, y -250, z 839,5 | Oeffnung zeigt -Y; kein Dauerfluss |
| Probehahn (zwischen Behaelter 1 und 2) | Tuelle Ø 12 (Handelshahn G 1/4, Rotguss) | x 165, y 120, z 839,5 | Oeffnung zeigt +Y; Wasserprobe fuer den woechentlichen Chlortest (DPD) |

## Verbindungen und Befestigungen

- Rohrenden d25/d20 werden mit der Muffe der Gegenseite verklebt (Port-Art Zapfen, Bibliotheksformat docs/parts/leitungsteile.md)
- Koepfe der Behaelter und Sedimentgehaeuse: Handelsanschluss, im Modell stumpf angesetztes Rohr d25
- Begrenzer und Probehahn haben Gewinde (G 3/4 bzw. G 1/4): Uebergangsstuecke als Katalogteile offen [A]

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Katalytische Kohle 12 x 40, 2 x 21 l Bett | Bett Ø 240 x 464 = 21 l je Behaelter | R | scripts/r45_kohle.py: 42 l bei 4 l/min = 10,5 min; R45 Abschnitt 5; Handelswerte Haendler-/Verbandsmaterial, keine Fachartikel | mittel |
| Kohle-Schuettdichte 0,441 kg/l | 9,3 kg je Bett | A | R53 Abschnitt 6: 27,5 lb/ft3 aus Handelsangabe Centaur 12x40 (Q-Treffer) | niedrig |
| Kompositbehaelter 10 x 35 Zoll | Ø 254 x 889 | A | Handelsmass R45; Fabrikat offen; PWG-Vessel/Clack-Kopf nur UK, eine Quelle (R53) | niedrig |
| Sedimentgehaeuse 10 Zoll, Patrone 20 um | Ø 112 x 290; Patrone Ø 63 x 250 | A | Handelsmass; wasserfilter-berlin 32420234, Ecosoft INL-FPV34ECO (Q-Treffer, R53) | niedrig |
| Probehahn zwischen den Behaeltern | Tuelle Ø 12, Gewinde G 1/4 | A | R45 Zeile 305; R53 Abschnitt 3: Kemper 1870000600 und SYR 6705.10.050 [Q] (G 1/4 statt d12) | mittel |
| Durchflussbegrenzer 4 l/min | Ø 32 x 60 Platzhalter | A | R53 Abschnitt 2: Kobold KM-020A (Datenblatt, eine Quelle, 4 l/min gelistet); Katalog offen | niedrig |
| Abzweige K41 d20 und K52 d25 hinter dem Filter | Lage x 560 und x 700 | E | Netz Version 3 (K41, K52); R45 Zeile 307 | hoch |
| Kugelhaehne d25 / d20 (Absperrung Eingang, Ausgang, K41, K52) | Platzhalterkoerper L 50 | A | bevo Profec Safe 600/525 (Q-Treffer, R53/W37-2-Blatt); Katalog offen | niedrig |
| Chlor oder Chloramin im Leitungswasser (E15) | offen | offen | Entscheidung Ben: beim Versorger klaeren; entscheidet ueber Behaelter 2 und ueber die Kohlebeschaffung | - |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R45-hydraulik-auslegung.md Abschnitt 5 (Zeilen 280-329); docs/research/R53-europa-frischwasser-luft.md (Europa-Bezug); data/leitungsnetz.json Version 3 (K39, K40, K41, K52); Handelsmasse Platzhalter, Katalog offen, N-BESCHAFFUNG (W47)
- Abweichung zum OBJ: Kein OBJ-Bestand: Knoten aktivkohle hatte bauteil null (Netz Version 3).

## Montage (L4)

1. Station frostfrei auf Boden oder Regalboden, wandnah (Standort Montage, E13/R45)
2. Sedimentgehaeuse auf der Konsole, beide Behaelter mit Kopf nach oben stellen
3. Verrohrung d25 verkleben, Abzweige K41/K52 hinter dem Begrenzer
4. Bett vor Gebrauch spuelen (R45 Betrieb)

**Werkzeug:** Rohrschneider, Klebstoff PVC, Schraubenschluessel fuer Kopf und Begrenzer

## Stueckliste-Zeile

- 2 Kompositbehaelter 10 x 35 mit Kopf (Bypass-/Absperrhahn)
- 1 Sedimentgehaeuse 10 Zoll mit Patrone 20 um
- 2 x 21 l katalytische Kohle 12 x 40 (9,3 kg je Bett)
- 1 Probehahn G 1/4 mit Tuelle
- 1 Durchflussbegrenzer 4 l/min G 3/4
- 4 Kugelhaehne (3 x d25, 1 x d20)
- 2 T-Stuecke d25, 1 T-Stueck d25 fuer den Probehahn, 1 Reduzierung d25/d20
- Rohr PVC-U d25 und d20

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Kompositbehaelter 10 x 35 mit Kopf (2 Stueck) | Ø 254 x 889, ca. 38 l | PWG-Vessel 10x35 mit Clack-Handrueckspuelkopf 1 Zoll, Art. Q-1035-A9 (GAPS, UK) [Q-Treffer] | nur UK, eine Quelle; Bypass nicht genannt; EU-Festland offen |
| Sedimentgehaeuse 10 Zoll | Ø 112 x 290 | Gehaeuse EKO 3/4 Zoll Messing, Art. 32420234 (wasserfilter-berlin, DE); Ecosoft INL-FPV34ECO-3/4 (BE, unsicher) [Q-Treffer] | beschaffbar (schwach, nicht geoeffnet) |
| Patrone PP 20 um, 10 Zoll | Ø 63 x 250 | ALFILTRA Filterkerze PP 20 um (DE) [Q-Treffer] | nur eine Quelle |
| Katalytische Kohle 12 x 40 (2 x 21 l, 9,3 kg je Bett) | Schuettgut | Ecosoft Centaur 12x40, Art. CENT1240 (Steinkohle, UK-Shop in GBP, derzeit nicht lieferbar) [Q]; Haycarb RWAC ueber Eurocarb (Bristol, UK) [Q Broschuere]; Jacobi AquaSorb CX-MCA nur US-Shops [Q-Treffer] | nur UK; EU-Festland nicht beschaffbar belegt (Chloramin-Fall, E15); bei Chlor genuegt Standardkohle (Jacobi AquaSorb CS 12x40) |
| Durchflussbegrenzer 4 l/min | G 3/4 aussen, DN 20 | Kobold KM-020A (Datenblatt gelesen, Hersteller aus Dateiname/Suche) [Q]; Kemper FG 68499001 (Set 4/10/20 l/min, DE) [Q-Treffer] | eine Quelle; das Blatt vom 04.11. fuehrte 'nicht beschaffbar' (Kemper-Set), R53 korrigiert auf Kobold; Fabrikat nicht gewaehlt |
| Kugelhahn d25 (3 Stueck) und d20 (1 Stueck) | PVC-U | bevo Profec Safe 600 Art. 0112135 (d25) und Safe 525 Art. 0112140 (d20) (DE/NL); GF Typ 546 via RS [Q-Treffer] | beschaffbar (nicht geoeffnet) |
| Probehahn zwischen den Behaeltern | G 1/4, Rotguss | Kemper 1870000600 (DE) [Q]; SYR 6705.10.050 (DE) [Q] | beschaffbar (R53); Anschluss G 1/4 statt d12; Abzweig mit Innengewinde nicht belegt [A] |

## Alternative lokale Fertigung

Kompositbehaelter und Sedimentgehaeuse sind Handelsteile (Wasseraufbereitung); Verrohrung PVC-U d25 Standard.

## Renders

- `renders/components/aktivkohle_station/aktivkohle_station-01-schraeg.png`
- `renders/components/aktivkohle_station/aktivkohle_station-02-oben.png`
- `renders/components/aktivkohle_station/aktivkohle_station-03-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Pruefer-Lauf: PASS, Befund in docs/jobs/pruefung/W37-2-W37-3.md.
- scripts/workshop/check_aktivkohle_station.py (Ergebnis renders/components/aktivkohle_station/check.txt): Behaelter-Mass, Bett 21 l, Kontaktzeit 10,5 min, Ports, Koerperzahl, Interferenz 0

## Offene Fragen

- E15 (DEINE ENTSCHEIDUNG Ben): Chlor oder Chloramin im Leitungswasser; bei Chlor genuegt Behaelter 1 (Parameter behaelter = 1)
- Katalytische Kohle nur UK (Ecosoft CENT1240, Eurocarb/Haycarb RWAC), EU-Festland nicht belegt (R53 Abschnitt 1); Centaur ist Steinkohle, nicht Kokos; Zuordnung nach Bens Entscheidung zu UK als Europa (R52 Abschnitt 4)
- Kompositbehaelter 10 x 35 mit Kopf: nur UK, eine Quelle (PWG/Clack); EU-Festland offen
- Standzeit/Kapazitaet der Kohle: nur Rechnung (R53 Abschnitt 6, obere Grenze 3,4 Jahre bei 2 mg/l), Hersteller erfragen
- Durchflussbegrenzer 4 l/min nur eine Quelle (Kobold KM-020A, Datenblatt); Schliessdruck am Pool-Schwimmerventil offen (R45 offener Punkt 4)
- Zisterne als Alternative: nicht gebaut (D69)
- Standort der Station (E13), Wandhalterung und Auffangwanne: Montage

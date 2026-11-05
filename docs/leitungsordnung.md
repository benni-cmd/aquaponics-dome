# Leitungsordnung v2 — Standard fuer Rohre, Schlaeuche und Leerrohre im Dom (D86, W75)

Stand 05.11.2026, Planer/Fachkritiker N-MINIMAL (`docs/packages/n-minimal.md`). Ersetzt v1 vom selben Tag (planer-m10-aplus; v1 bleibt in der Git-Historie, Commit vor diesem). Gilt fuer jede Montage ab M10-S3; die Blaetter `docs/jobs/M10-S3.md` bis `M10-S7.md`, `M10-UMBAU.md`, `M10-S5-LUFT-B.md` verweisen hierher. Pruefskript: `python -X utf8 scripts/check_leitungsordnung.py` (Exit 1 bei Verstoss in R1 bis R9 oder R11 bis R14). Systemfrage (welche Leitungen es ueberhaupt gibt): `docs/research/R57-systemreview.md`.

**Problem:** v1 machte jede Leitung zum rechtwinkligen Installateur-Rohr und legte alles, was Gaenge kreuzt, in den Graben. Das ergab 151 m Leitung unter Flur in der gebauten Variante A+ (`python -X utf8 scripts/r57_rechnung.py vergraben`), Luft und Frischwasser eingeschlossen, und starre Boegen, wo ein Schlauch frei faellt.
**Intent:** Ben will so wenig wie moeglich vergraben, Schwerkraft, Siphon, Unterdruck und Wasserspiegel nutzen und Ruecklaeufe als frei gefuehrte Schlaeuche erlauben, solange es umsetzbar und ueberschaubar bleibt (W75, D86).
**Goal:** Jede Leitung gehoert einer Leitungsart A bis F (unten), erfuellt deren Regeln, und `check_leitungsordnung.py` meldet 0 Verstoesse.

## Begriffe
- **Hoehe:** Netz-Z ist flur-relativ, Modell-Z absolut; absolut = relativ + 400 (Flur Z 400).
- **Rahmen:** Welt-Rahmen (Achsen X, Y) oder Sektor-Rahmen (radial und tangential zur Sektorachse eines Tisch-Sektors, Azimute aus `scripts/dome-script.json`).
- **Zugang:** Revisionsstutzen, Kanal mit Rost, Kappe, Hahn, Bauteil-Port ueber Flur, loesbare Schlauchschelle.
- **Fliessrichtung:** Reihenfolge der Punkte im Feld `pfad` einer Trasse (Start = Quelle).

## Grundsatz: rechtwinklig nur dort, wo es Sinn hat
Rechtwinklig und starr (PVC-U, Boegen 45/90 Grad) bleibt alles, was **gebuendelt, verteilt oder unter Druck** ist und an einem festen Ort steht: Technikturm, Pumpenauslaesse, Verteiler, Strang am Tischbein, Halbring an der Pool-Wandkrone. Frei gefuehrt (Schlauch, beliebige Richtung in der Ebene) wird alles, was **einzeln laeuft, frei faellt oder leicht ist**: Ruecklaeufe aus Beeten und NFT, Luft, Frischwasser, Schlamm, Pumpendruck aus dem Pool ueber den Beckenrand. Der Graben ist kein Korridor mehr fuer Laengsstrecken, nur fuer Querungen.

## Leitungsarten (Feld `art` je Trasse)
| Art | Wofuer | Werkstoff (D85: alles mit Wasserkontakt lebensmittelecht) | Fuehrung |
|---|---|---|---|
| A Druck starr | Pumpenauslass, Verteiler, Tischstrang, Messkreis | PVC-U-Druckrohr | rechtwinklig im Korridor-Rahmen (R1 bis R5 wie v1) |
| B Druckschlauch | Pumpe im Pool bis Siebkorb, Frischwasser, Dosierung, Messkreis-Stich | glattwandiger Spiral- oder Druckschlauch, lebensmittelecht (EU 10/2011), lichtdicht oder schwarz (FAO 589 S. 53: sonst Algen) | frei, Biegeradius R14, keine Lage im Gang |
| C Schwerkraft frei | Beet- und NFT-Ruecklauf, Ueberlaeufe, Zweitbecken-Ueberlauf, Schlamm nach aussen | glattwandiger Schlauch oder Rohr, lebensmittelecht und lichtdicht (kein Wellschlauch innen: Schlamm haftet, R49 Abschn. 3.1; HT/KG-Abwasserrohr ist nicht als lebensmittelecht ausgewiesen, D85) | stetiges Gefaelle R11, kein Hochpunkt R12, beliebige Richtung; Einlauf offen, damit Luft mitlaufen kann (abfliessendes Wasser zieht das 10- bis 35-fache an Luft, SBZ Monteur 06/2016) |
| D Luft | Geblaese zu Ausstroemern | PE- oder Silikonschlauch, Rohr nur am Turm | frei; ueber dem hoechsten Wasserspiegel mit Tropfschleife und Rueckschlagventil (R53 Abschn. 5) |
| E Heber/Siphon | Leitung, die ueber den Spiegel ihrer Quelle steigt oder voll laufend unter ihm liegt | PVC-U oder Schlauch | nur mit Kennzeichen `siphon` und Begruendung (R12) |
| F Leerrohr/Kanal | Querung eines Gangs, Einmuendung unter Flur, Kabel | Leerrohr DN50/DN100 oder Kanal mit Rost | kurz, Grund Pflicht (R13) |

Trassen ohne Feld `art` gelten als **Bestand v1** (Art A); fuer sie gelten R1 bis R9 wie bisher. R11 bis R14 pruefen jede Trasse mit `art`.

## Korridore (wo eine Leitung liegen darf)
| Kuerzel | Korridor | Hoehe (absolut) | Rahmen | Arten |
|---|---|---|---|---|
| KH | Technikturm, Pumpen, Biofilter, Verteiler, Schrank | Z 400 bis 2400 | Welt | A, B, D |
| KW | Pool-Aufkantung, Gelaenderpfosten und Beckenaussenwand (D88: Rand etwa Z +150 rel = 550 absolut [A]; vor D88 Wandkrone Z 1050 bis 1130) | Z 400 bis 1400 | Welt, Halbring als halbes Achteck (0/45/90 Grad) | A, C |
| KT | unter den NFT-Rinnen am Tischbein | Z 1300 bis 1500 | Sektor | A, C |
| KF | frei am Bauteil: auf dem Flur entlang Beet- und Tischfuss, am Beetrand, an der Beckenaussenwand, ueber den Beckenrand | Z 400 bis 2100, ausserhalb der Gaenge | frei (jede waagerechte Richtung) | B, C, D |
| KS | Steiger senkrecht | beliebig | lotrecht | A, B, D |
| KB | im Becken (Wasser) | unter dem Spiegel | frei, ohne Durchfuehrung durch Wand oder Boden | B, D |
| KG | unter Flur | Z 0 bis 400 | frei | F, und C nur an der Pool-Einmuendung |
Ueber Kopf (Z >= 2500 absolut) bleibt ungenutzt, solange die Statik offen ist (N-STATIK): keine Befestigung an Streben, Knoten, Haut oder Plane. Die Autobahn-Variante (N-AUTOBAHN-V2, W78) braucht eigene Stelzen; sie ist dann ein eigener Korridor mit Statiknachweis und steht nicht in dieser Ordnung.

## Regeln (jede messbar in `check_leitungsordnung.py`)
| R | Regel | Messung | Soll |
|---|---|---|---|
| R1 Richtung | Art A: parallel zu einer Achse des Korridor-Rahmens oder lotrecht (KW zusaetzlich 45 Grad); Gefaelle bis 2 Grad. Arten B, C, D, F: frei | Winkel zur naechsten erlaubten Richtung, nur Art A | <= 1 Grad; waagerechte Richtungen Art A <= 8 Welt + 2 je Sektor |
| R2 Boegen | Art A nur 90 und 45 Grad aus der Bibliothek | Bogen-Instanzen nach Name | 0 andere |
| R3 Gerade zwischen Boegen | Art A: >= max(3 x d, 100 mm); Ausnahme Etage aus zwei 90-Grad-Boegen am Steiger | Achsabstand der Bogen-Ecken | 0 |
| R4 Keine Bogenkette | Art A: keine Folge von 3 oder mehr Boegen mit Zwischenrohren < 300 mm | Kettensuche | 0 |
| R5 Bogenzahl | Art A: je Trasse hoechstens 4 Boegen plus 1 je angefangene 5 m [A] | Zaehlung | 0 Ueberschreitungen |
| R6 Halter | Rohr ueber Flur: Abstand d20 bis d32 <= 600, d40 bis d63 <= 800, d75 bis d110 <= 1000 mm (senkrecht x 1,5), je Hahn und Verteiler einer <= 300 mm daneben. Schlauch: <= 400 mm oder Feld `aufliegend` (liegt durchgehend auf Flur, Beetrand oder Rinne) | Halter-Instanzen entlang der Achse | 0 Luecken |
| R7 Befestigungsgrund | Halter nur an Tischbein, Boden, Fundament, Tank-/Pumpentafel, Pool-Wandkrone, Beetrand; nie an Strebe, Knoten, Haut, Plane | Halterhoehe < Z 2500, Abstand >= 150 mm zu jeder Strebenachse | 0 |
| R8 Buendel | parallele Leitungen eines Korridors: lichter Abstand 25 bis 60 mm, nach Nennweite, Gefaelle-Leitungen unten [A] | lichter Abstand paralleler Nachbarn (nur Art A und Bestand) | 25 bis 60 mm |
| R9 Gaenge | Im Gang liegt keine Leitung frei zwischen Z 400 und 2500 (auch kein Schlauch auf dem Flur); Querung nur als Art F unter Flur | Schnitt mit der Gangnaeherung | 0; `check_walkways.py` unveraendert PASS |
| **R11 Gefaelle** | Art C faellt in Fliessrichtung in **jedem** Teilstueck: Schlauch und Rohr bis d63 >= 1 %, ab d75 >= 0,5 % [A, R49 Abschn. 3.1, NFT-Sammler 1,5 % im Netz K15] | dz je waagerechter Laenge je Teilstueck | 0 Teilstuecke darunter |
| **R12 Kein Hochpunkt** | Art C steigt nie ueber ihren Startpunkt und hat keinen Zwischen-Hochpunkt (sonst Luftsack, Stau, Siphon). Eine Leitung, die ueber den Spiegel ihrer Quelle steigt, ist Art B (gepumpt) oder Art E mit Feld `siphon` = "entlueftet" oder "anfahrhilfe" | hoechster Pfadpunkt nach dem Start gegen Start | 0 |
| **R13 Vergraben nur mit Grund** | Jedes Teilstueck mit Achse unter Z 400 traegt Art F oder das Feld `grund` (`gangquerung`, `pool_einmuendung`, `unter_wasserspiegel`); Laenge je Teilstueck <= 3 m bis zum naechsten Zugang [A, R47b M1]; Summe unter Flur wird gemeldet | Teilstuecke unter Z 400 ohne Grund; Summe in m | 0 ohne Grund; Summe <= 25 m im Zielbild S [A] |
| **R14 Schlauchbiegung** | Arten B, C, D: Biegeradius >= 6 x Aussendurchmesser und nie unter dem Herstellerwert (Spiralschlauch 40 mm 260, 51 mm 270 mm, esska; Projektregel `docs/hydraulics.md` Abschn. 5 nannte 5 x d); ein Knick im Pfad braucht genug Gerade beidseits fuer diesen Radius | je Ecke Tangentenlaenge r x tan(Winkel/2) gegen die halben Nachbarstuecke | 0 |
| R10 Abdeckung (Info) | Netz-Kanten ohne Trasse | Liste | Info |

**Grenzwerte, Belegstand:** R6 bleibt eine Annahme [A] unter der Praher-Tabelle (PVC-U PN16, 20 Grad: d20 1188 bis d50 1728 mm); R11 ist belegt mit zwei Anwendungen (DIN 1986-100 nach SBZ Monteur 06/2016: unbeluftete Anschlussleitung 1 cm/m, Sammelleitung 0,5 cm/m; FAO 589 S. 65: NFT 1 cm/m), ein Wert eigens fuer frei haengende Schlaeuche wurde nicht gefunden; R6 fuer Schlaeuche (400 mm) bleibt [A], Halterabstand und Durchhang fand die Recherche nicht; R13 (3 m) und die 25-m-Summe sind Planer-Annahmen; R14 stuetzt sich auf zwei Haendler-Datenblaetter. Belege und Luecken stehen in R57 Abschnitt 7.

## Siphon, Unterdruck und Wasserspiegel: wann was
1. **Wasserspiegel zuerst:** Ein Bauteil, das frei abfliessen soll, steht hoeher als das Ziel; die Hoehenkette heisst Biofilter (Spiegel Z 1600 rel) > Verteiler > Beete und NFT > Pool. Was in diese Kette passt, ist Art C ohne Pumpe.
2. **Druck statt Heber, wenn eine Pumpe ohnehin hebt:** Die Pumpe im Pool foerdert ueber den Beckenrand direkt in den offenen Siebkorb (Art B). Kein Rueckschlagventil noetig: nach dem Abschalten laeuft nur der Schlauchinhalt zurueck, der offene Einlauf am Korb kann nicht saugen.
3. **Heber (Art E) nur mit Entlueftung:** Ein voll laufender Heber unter dem Quellspiegel (A+: K01/K17) bleibt erlaubt, wenn Laenge und Formstueckzahl nicht steigen (v1-Ausnahme 1, `python -X utf8 scripts/r45_heber.py`). Ein Heber ueber einen Rand (echter Siphon) braucht eine Entlueftung am Hochpunkt oder eine Anfahrhilfe und ist im Dom nicht geplant.
4. **Glockensiphon** im Beet ist ein Bauteil (R51), keine Leitung; seine Ablaufleitung ist Art C.
5. **Kein Auslass unter dem Spiegel ohne Siphonbrecher** (`docs/hydraulics.md` Abschn. 2.9): jeder Einlauf in ein Becken endet ueber dem hoechsten Spiegel oder hat ein Belueftungsloch.

## Zugang
- Jede Art-C-Leitung ist an ihrem tiefsten Punkt loesbar (Schelle oder Verschraubung), damit man sie ausspuelen kann.
- Unter Flur nur Art F; Kanal mit Rost gilt durchgehend als Zugang; Leerrohr hat an beiden Enden einen Zugang ueber Flur.
- Haehne, Schellen, Korb und Pumpen erreicht man ohne Leiter und ohne Werkzeug zum Graben.

## Ausnahmen (abschliessend)
1. **Heber K01/K17 (nur Variante A+):** Laenge und Formstueckzahl duerfen nicht steigen (Reserve >= 85 mm, Pruefer S2R Auflage A2).
2. **Schraege Bauteil-Ports:** das erste Rohr nach dem Port darf der Port-Richtung folgen, hoechstens 300 mm.
3. **Luft im Becken (KB):** Leitungen im Wasser sind gewollt; keine Durchfuehrung durch Poolwand oder Poolboden.
4. **Verteiler-Buendel (R8):** Abgaenge eines Verteilers behalten dessen Teilung bis zur ersten Richtungsaenderung, Feld `buendel`.
5. **Schwanenhals ueber einen Beckenrand (R4):** drei Boegen ueber dem Rand plus am Port zaehlen nicht als Kette, Feld `schwanenhals`. Fuer neue Leitungen ueber den Rand ist ein Schlauch (Art B) die Regel.
6. **Aussen (R9, Band AU):** R9 gilt im Dom (Zehneck, Apothem 5706). Art C fuer Schlamm darf durch den Fundamentring nach aussen (eine Durchfuehrung je Linie, R57); der Kreislauf selbst bleibt innen (W79).

## Werkzeug
- Trassen tragen `art` (A bis F) und fuer Art C den Startpunkt an der Quelle; Art C und E zusaetzlich `quelle_spiegel` (Z absolut), wenn bekannt.
- `scripts/leitungen.py` baut weiterhin nur Art A und Bestand (Boegen 45/90). Schlauch-Trassen (B, C, D) uebergibt das Pruefskript nicht an `leitungen.bauen()`; einen Schlauch-Baustein (Polylinie mit Radius, Schelle, Tuelle) muss die Werkstatt vor der ersten v2-Montage liefern (Folge in R57 Abschnitt 9).
- `check_leitungsordnung.py --nur-v2` prueft nur Trassen mit `art`; ohne Schalter prueft es alles.

## Fehlende Teile (Werkstatt-Notiz)
Vorhanden: `lt_klemme_d20/25/32/40/50/63/110`, `lt_schelle_vk_d32/_d63`, `lt_schlauchschelle_id16/_id25`. Fehlt: Schlauch-Baustein fuer B/C/D, Schlauchtuelle d40/d50 lebensmittelecht, Leerrohr-Querung DN100 als Bauteil mit Zugang, `lt_klemme_d75` (nur A+ Heber), Konsole fuer die Pool-Wandkrone.

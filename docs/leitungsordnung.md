# Leitungsordnung — Standard fuer alle Rohre, Schlaeuche und Leerrohre im Dom (N-REWORK, W71)

Stand 05.11.2026, Planer (planer-m10-aplus). Gilt fuer jede Montage ab M10-UMBAU; die Blaetter `docs/jobs/M10-UMBAU.md`, `M10-S5-LUFT-B.md`, `M10-S2N.md` bis `M10-S7.md` verweisen hierher. Pruefskript: `scripts/check_leitungsordnung.py` (baut M10-UMBAU Schritt 1).

**Problem:** Die Maengel-Inventur (`docs/model-maengel.md`, 7d59462) misst 74 von 114 Rohren schraeg (> 3 Grad zu allen Achsen), waagerechte Rohre in 31 Richtungen, 79 Boegen, 38 Rohre unter 120 mm, 4 Bogenketten und 0 Halter (M04, M05, M06, M10). Ursache: das 15-Grad-Raster der Trassenableitung in `scripts/trassen_linie.py`.
**Intent:** Ben sieht eine Anlage, wie ein Installateur sie verlegt: wenige feste Wege, rechtwinklig, gebuendelt, gehalten, Gaenge frei.
**Goal:** Jede Leitung erfuellt R1 bis R9 unten; `check_leitungsordnung.py` meldet 0 Verstoesse.

## Begriffe
- **Hoehe:** Netz-Z ist flur-relativ, Modell-Z absolut; absolut = relativ + 400 (Flur Z 400).
- **Rahmen:** Welt-Rahmen (Achsen X, Y) oder Sektor-Rahmen (radial und tangential zur Sektorachse eines Tisch-Sektors, Azimute aus `scripts/dome-script.json`).
- **Zugang:** Revisionsstutzen, Schacht, Hahn, Bauteil-Port ueber Flur.

## Korridore (nur hier darf eine Leitung liegen)
| Kuerzel | Korridor | Hoehe (absolut) | Rahmen | Typische Kanten |
|---|---|---|---|---|
| KG | Graben unterflur, Leerrohr oder Bettung | Z 0 bis 300 (Rohrachse), Heber tiefer | Welt | Heber, Bodenablauf, Absetzer, Beet-Ablauf, Kabel |
| KH | Technikgruppe an Tank, Pumpentafel, Schrank | Z 400 bis 2400 | Welt | Pumpen, Biofilter, Verteiler, Luft am Schrank |
| KW | Pool-Wandkrone und Beckenaussenwand | Z 1050 bis 1130 | Welt, Halbring als halbes Achteck (0/45/90 Grad) | Halbringe K16/K32, Einlaeufe |
| KT | unter den NFT-Rinnen am Tischbein | Z 1300 bis 1500 (Rinne 1000 relativ) | Sektor | NFT-Strang K12/K28, Sektorsammler K15/K31 |
| KS | Steiger senkrecht | beliebig | lotrecht | Uebergang zwischen Korridoren, Revisionssteiger |
| KB | im Becken (Wasser) | unter dem Spiegel | Welt, lotrecht an der Innenwand | Luft zu Scheiben, Ansaugungen |
Ueber Kopf (Z >= 2500 absolut) wird nicht genutzt, solange die Statik offen ist (N-STATIK): keine Befestigung an Streben, Knoten, Haut oder Plane.

## Regeln (jede messbar)
| R | Regel | Messung in `check_leitungsordnung.py` | Soll |
|---|---|---|---|
| R1 Richtung | Jedes gerade Rohr liegt parallel zu einer Achse seines Korridor-Rahmens oder lotrecht; KW zusaetzlich 45 Grad | Winkel Rohrachse zur naechsten erlaubten Richtung; Gefaelle-Rohre duerfen bis 2 Grad (1 bis 3 %) gegen die Waagerechte geneigt sein | <= 1 Grad (Gefaelle <= 2 Grad); waagerechte Richtungen gesamt <= 8 Welt + 2 je Sektor |
| R2 Boegen | Nur 90 und 45 Grad aus der Bibliothek | Bogen-Instanzen nach Name | 0 andere |
| R3 Gerade zwischen Boegen | Zwischen zwei Boegen gerades Rohr >= max(3 x d, 100 mm); Ausnahme: Etage aus zwei 90-Grad-Boegen an einem Steiger | Achsabstand der Bogen-Ecken | 0 Unterschreitungen |
| R4 Keine Bogenkette | Keine Folge von 3 oder mehr Boegen mit Zwischenrohren < 300 mm; Rohre < 120 mm nur innerhalb eines Formstueck-Zusammenbaus (T- oder Reduzier-Anschluss) | Kettensuche ueber den Trassengraphen | 0 Ketten (heute 4) |
| R5 Bogenzahl | Je Trasse hoechstens 4 Boegen plus 1 je angefangene 5 m Laenge [A] | Zaehlung je Trasse | 0 Ueberschreitungen |
| R6 Halter | Jedes Rohr ueber Flur (Achse > Z 400) hat Halter; Abstand d20 bis d32 <= 600 mm, d40 bis d63 <= 800 mm, d75 bis d110 <= 1000 mm (senkrecht x 1,5); zusaetzlich je Hahn und Verteiler ein Halter <= 300 mm daneben; Schlauch <= 400 mm. Unterflur (Bettung im Graben) ohne Halter | Halter-Instanzen entlang jeder Achse | 0 Luecken (heute 0 Halter) |
| R7 Befestigungsgrund | Halter sitzen nur an Tischbein (`lt_schelle_vk_d32/_d63`), Boden/Fundament/Tank-/Pumpentafel/Pool-Wandkrone (`lt_klemme_d20` bis `_d110`); nie an Strebe, Knoten, Haut, Plane | Halter-Kasten beruehrt ein erlaubtes Bauteil, keins mit `strebe`, `knoten`, `haut`, `plane` im Namen | 0 Verstoesse |
| R8 Buendel | Parallele Leitungen eines Korridors liegen auf gemeinsamer Halterebene, lichter Abstand 30 mm [A] (Muffen passen), nach Nennweite geordnet, Gefaelle-Leitungen unten | lichter Abstand paralleler Nachbarn im selben Korridor | 25 bis 60 mm |
| R9 Gaenge | Im Gang (Gangkarte `scripts/check_walkways.py`) liegt keine Leitung frei zwischen Z 400 und 2500; Kreuzung nur im Graben KG | Schnitt Rohrachse mit Gangflaeche | 0 Verstoesse; `check_walkways.py` unveraendert PASS |

**Grenzwerte, Belegstand:** R6-Abstaende sind eine Annahme [A], absichtlich unter der einzigen gefundenen Herstellertabelle (Praher, PVC-U PN16 bei 20 Grad: d20 1188, d25 1296, d32 1458, d40 1566, d50 1728 mm) und innerhalb der Projektregel "Klemmen alle 0,5 bis 1 m" (`docs/packages/m10-leitungen.md` Abschnitt 4 Regel 7). Eine zweite unabhaengige Quelle mit Zahlen fehlt; R3, R5, R8 sind Planer-Annahmen [A] und werden nach dem ersten Bau einmal gegen das Bild geprueft.

## Ausnahmen (abschliessend)
1. **Heber K01/K17:** Laenge und Formstueckzahl duerfen nicht steigen (Reserve >= 85 mm im ungünstigen Fall, Pruefer S2R Auflage A2; `python -X utf8 scripts/r45_heber.py`). Ein Umbau ist erlaubt, wenn beides gleich bleibt oder sinkt.
2. **Bauteil-Ports, die schraeg liegen** (Tangentialzulauf Absetzer): das erste Rohr nach dem Port darf der Port-Richtung folgen, hoechstens 300 mm, dann Uebergang in den Rahmen.
3. **Luft im Becken (KB):** Rohre im Wasser sind gewollt (Kollision mit dem Wasserkoerper ist kein Fehler); keine Durchfuehrung durch Poolwand oder Poolboden.
4. **Verteiler-Buendel (R8, nachgetragen 05.11. in M10-S5-LUFT-B):** Abgaenge eines Verteilers behalten dessen Teilung (luftverteiler_6: 120 mm) bis zu ihrer ersten Richtungsaenderung und duerfen danach eng (nur kollisionsfrei) nebeneinander laufen; Kennzeichen in der Trasse: Feld `buendel` mit gleichem Wert. Grund: eine Teilung von 120 mm ergibt bei d20 bis d40 einen lichten Abstand von 80 bis 100 mm, den R8 sonst verbietet.
5. **Schwanenhals ueber einen Beckenrand (R4, nachgetragen 05.11.):** eine schraege Bauteil-Muffe auf der Beckenkrone (Pool-Verteiler, Muffe A Az 65) ist nur mit zwei Boegen ueber dem Rand plus einem Bogen am Port erreichbar; diese drei Boegen zaehlen nicht als Bogenkette. Kennzeichen: Feld `schwanenhals` in der Trasse.
6. **Aussen (R9, Band AU):** R9 gilt im Dom (Zehneck, Apothem 5706). Leitungen der Technikgruppe vor dem Fundamentring tragen das Band `AU` (Z relativ 0 bis 2100, nur ausserhalb des Zehnecks, `scripts/check_leitungen.py`).

## Werkzeug
`scripts/trassen_linie.py`, `scripts/trassen_luft.py` und neue Trassen-Skripte routen nur noch im Korridor-Rahmen (Manhattan-Wege mit 90-Grad-Ecken, 45 Grad nur in KW); das 15-Grad-Raster entfaellt. Jede Trasse traegt das Feld `korridor` (KG, KH, KW, KT, KS, KB) je Segment; `check_leitungsordnung.py` liest Trassen und Instanzen (`scripts/dome-script.json`) und gibt R1 bis R9 als Tabelle mit Zahl und Ort je Verstoss aus, Exit 1 bei Verstoss.

## Fehlende Halter-Teile (Werkstatt-Notiz)
Vorhanden: `lt_klemme_d20/25/32/40/50/63/110`, `lt_schelle_vk_d32/_d63`, `lt_schlauchschelle_id16/_id25`. Fehlt: `lt_klemme_d75` (nur fuer oberirdische Heber-Steiger), Konsole fuer die Pool-Wandkrone (Halbring d110 sitzt auf der Krone, nicht daneben). Bis zur Lieferung: Montage fuehrt die Stelle als OFFEN (Werkstatt: Halter), kein Eigenbau.

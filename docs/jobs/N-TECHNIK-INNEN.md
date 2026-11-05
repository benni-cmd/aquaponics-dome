# N-TECHNIK-INNEN Technikgruppe in die Kuppel, Rohrwege kurz (Werkstatt + Montage)

Planer: Opus 5.5, 05.11.2026, nach `docs/jobs/vorlagen/planung.md`. Nur gelesen, kein Modell und keine Daten geaendert. Ausnahme: das reine Rechenskript `scripts/n_technik_innen.py`. Es liest nur und liefert jede Zahl dieses Blatts nachrechenbar. Vorgaenger: `docs/jobs/M10-S5-LUFT-B.md` (Runde 74, Gruppe aussen), Pruefbefund `docs/jobs/pruefung/M10-S5-LUFT-B.md`. Paket: `docs/packages/n-technik-innen.md`.

**Problem:** Die Technikgruppe steht seit Runde 74 aussen vor dem Fundamentring neben der Tuer (Schrankmitte x 500 / y -6490). Zur Gruppe gehoeren die 2 Geblaese mit Rueckschlagventilen, der Hauptverteiler `luftverteiler_6`, die Aktivkohle-Station und der Schaltschrank. Die 9 Luft- und Frischwasserkanten laufen von aussen um den Ring und sind zusammen 104,9 m lang. Ben will die Technik innen und die Wege kurz (W72, D84).
**Intent:** Technik dort, wo sie arbeitet: nah an Pool, Filtern und Becken, weniger Rohr und weniger Graben, Wartung von innen.
**Ziel in einem Satz:** Geblaese, Hauptverteiler und Aktivkohle-Station stehen als ein Technikturm (800 x 500 x 2000) innen im Tuerkeil bei x 600 / y -4900; alle 9 Kanten plus K47/K48 sind neu verlegt, zusammen hoechstens 85 m (heute 104,9); die Gaenge bleiben PASS.

## Aktualitaetspruefung (05.11.2026, Regel W44)
Ergebnis: **angepasst** (der Plan gilt als freigegeben; ein Teil ist OFFEN (Ben)).
1. Roadmap `N-TECHNIK-INNEN`: Status laeuft, Reihenfolge 7.2, "Planer bestimmt Platz innen, Montage verlegt um, Kennzahlen vorher/nachher". Gueltig.
2. D84 und W72 (05.11.): Technik nach innen, Schaltschrank "eher auch rein", Brandlast pruefen. **Befund:** Innen gibt es mit den geltenden Gangregeln keinen Platz fuer die ganze Gruppe; Zahlen im Abschnitt "Platz innen". Dieses Blatt bringt alle Teile mit Rohren nach innen. Der Schaltschrank bleibt vorerst aussen am Platz von Runde 74, weil er keine Rohre hat; das ist die Ausnahme aus W72. Schrank innen ist **OFFEN (Ben)**, siehe Abschnitt Schaltschrank.
3. Laufend: M10-S2N baut (Commits 5eaabf4 bis 382b971: Graeben, Schacht KH1, K46-Lage im Build 75). Dieses Blatt startet erst nach der Abnahme von M10-S2N und vor M10-S3. Nur eine Montage zugleich (D80).
4. N-VARIANTEN V1b ist da (0889b7c): Teile nur fuer A+ bekommen `varianten: ["a_plus"]`. Gilt fuer die Technikgruppe nicht, sie gehoert zu beiden Varianten.
5. Pruefer-Auflagen aus Runde 74 werden hier mit erledigt: A1 K47/K48 (Werkstatt-Anschluss am Absetzer), A2 R5 und R8, A3 Schwerpunkt (neuer Bezug: Turmmitte). A4 (Viewer-Export) und A5 (Tuer-Zugang Schrank) bleiben beim Orchestrator bzw. Ben.

## Platz innen (gemessen)
Befehl: `python -X utf8 scripts/n_technik_innen.py suche streng` bzw. `... suche gang300`. Geprueft werden achsparallele Lagen auf einem 100-mm-Raster im Technik-Sektor Az -125 bis -5.
Regeln der Suche:
- 150 mm Luft zu Tanks, Pumpen, Puffer, Filtern und Schlammfass (D70)
- 500 mm Gang zu Beet-Portalen und Becken (D70), 700 mm zum Zentralpool (Laufweg A)
- Tuerachse >= 450 mm (Tuergang 900, D62)
- Bedienzone 650 mm vor der Front frei (D70/D72)
- Huellenluft >= 110 mm, auch in der Hoehe: Die Tuerfacette zieht 0,191 mm je mm Hoehe nach innen (Knoten n25/n23 r 6000 Z 475, n07 r 5104 Z 3629). In 1,2 m Hoehe sind das 215 mm mehr als am Boden.

| Teil (Grundflaeche, Hoehe) | streng (Gang 500) | Gang 300 zur Stirnseite Beet 4 |
|---|---|---|
| Aktivkohle-Station 1700 x 500, H 929 | 0 Lagen | 0 Lagen |
| Schaltschrank 800 x 500, H 1200 | 0 Lagen | 3 Lagen (x 500 bis 600, y -5000 bis -4900) |
| Technikturm 800 x 500, H 2000 | 0 Lagen | 1 Lage (x 600 / y -4900) |
| Geblaese-Paar 532 x 680, H 730 | 1 Lage (x 700 / y -5000) | 12 Lagen |

Folgen:
- Der Tuerkeil westlich der Tuer (zwischen Beet_aussen_800:4, Pumpe_klein:2, Tank_klein:1 und Tuerachse) ist die einzige Flaeche, und dort passt genau EIN Kasten 800 x 500.
- Darum wird gestapelt (Turm) und die Station kompakt gebaut.
- Der Schaltschrank findet daneben keinen zweiten Platz.
- Preis der Lage: Der Turm hat 329 mm zum Portal von Beet 4 statt 500, 157 mm zu Pumpe_klein:2 und 333 mm zu Tank_klein:1 (`python -X utf8 scripts/n_technik_innen.py pruef` nach dem Setzen der Parameter).

## Varianten
| | V0 Runde 74 (aussen) | **V1 Turm innen, Schrank aussen (Empfehlung, Annahme nach D81)** | V2 alles innen | V3 Schrank innen, Turm aussen |
|---|---|---|---|---|
| Lage | Gruppe aussen, Schrank 500/-6490 | Turm 600/-4900 innen, Schrank unveraendert aussen dahinter (1,6 m, Kabel unterm Ring) | wie V1, Schrank im Tuerkeil | Schrank im Tuerkeil, Turm aussen |
| Rohr 9 Kanten | 104,9 m | 77,4 m (-27,5 m, -26 %) | wie V1 | wie V0 |
| dazu K47/K48 | nicht verlegt (Schaetzung 21,4 m) | Schaetzung 15,3 m | wie V1 | wie V0 |
| Boegen 9 Kanten | 66 | gleiche Zahl angenommen, Soll R5 je Kante | wie V1 | wie V0 |
| Voraussetzung | gebaut | Werkstatt Turm und kompakte Station | dazu Pumpe_klein:2 und Tank_klein:1 (Absetzer 1) verschieben, d. h. A+-Leitungen neu | keine |

Zahlen: `python -X utf8 scripts/n_technik_innen.py laengen`. V0 ist aus `data/leitungstrassen.json` gemessen. V1 ist geschaetzt: Grabenstrecke = Manhattan-Abstand vom neuen Port zum gleichen Zielpunkt mal dem Umweg-Faktor von Runde 74, Startstueck neu (+1,1 m je Luftkante, weil der Verteiler oben im Turm bei Z 2150 sitzt), Zielstueck unveraendert.
Je Kante (V0 -> V1, m): K39 8,88 -> 4,41 · K40 12,26 -> 9,37 · K41 13,88 -> 9,97 · K44 13,00 -> 10,38 · K45 17,74 -> 13,79 · K46 8,06 -> 6,64 · K49 10,41 -> 8,39 · K51 8,10 -> 5,96 · K52 12,58 -> 8,45 · K47 8,16 -> 5,13 · K48 13,23 -> 10,20.
Ergebnis nach Medium: Luft 57,3 -> 45,1 m, Frischwasser 47,6 -> 32,2 m.

**Pumpen- und Geblaeseleistung (Bens Annahme "lange Wege = staerkere Pumpe, mehr Strom" stimmt fuer diese Leitungen nicht):** Befehl `python -X utf8 scripts/n_technik_innen.py druck`.
1. Der Geblaesedruck kommt fast ganz aus der Wassertiefe: 21,3 kPa statisch (2,17 m, R45) plus Diffusor 3 kPa [A]. Die Rohrreibung des Pool-Strangs K44 betraegt bei 130 l/min nur 71 Pa (V0) bzw. 64 Pa (V1).
2. Gesamtdruck V0 24,36 kPa, V1 24,35 kPa. Elektrisch bei Wirkungsgrad 0,45 [A]: 117 W in beiden Faellen; bei der Spitze 205 l/min 186 W gegen 185 W. Das Geblaese bleibt gleich gross.
3. Frischwasser laeuft mit Hausdruck, ohne Pumpe. Reibung bei 4 l/min: K40 622 -> 525 Pa, K39 382 -> 232 Pa, K41 616 -> 476 Pa (2 l/min). Vernachlaessigbar gegen rund 3 bar Hausdruck [A].
4. Die Pumpen des Hauptkreislaufs stehen an den Tanks und haengen nicht am Ort der Technikgruppe.
5. Der Gewinn von V1 ist also Material und Bauaufwand: 27,5 m weniger Rohr (33,6 m mit K47/K48) und kuerzere Graeben, nicht Strom. Bens Grund "kurze Wege" gilt voll fuer den Hauptkreislauf, also M10-S3/S4 mit Pumpen und Beet-Zulauf.

## Schaltschrank: Brandlast, Unterlage, Spritzwasser
- **V1 (Annahme):** Der Schrank bleibt aussen am Platz von Runde 74 (Rueckwand 20 mm vor der Fundamentring-Aussenkante). Er steht unter keiner Plane, weil die Facette nach innen zieht. Abstand Schrankrueckseite zur Plane in 1,2 m Hoehe: 5956 + 20 - (5706 - 0,191 x 1125) = rund 485 mm waagerecht, Plane innen. Die Unterlage ist das Fundament bzw. der Erdboden mit Sockel. Geblaese-Kabel: Leerrohr DN100 der `schrank_einfuehrung` unter dem Ring zum Turm, etwa 1,6 m.
- **Schrank innen (V2):** Die beste Lage (x 600 / y -4900) haette in 1200 mm Hoehe nur 284 mm Luft zur Huelle (`python -X utf8 scripts/n_technik_innen.py huelle`). Die strenge Lage (x 800 / y -5100) schneidet die Huelle schon ab 930 mm Hoehe (-12 mm). Innen braucht der Schrank also eine nicht brennbare Platte (Baustoffklasse A1, z. B. Kalziumsilikat) zwischen Schrank und Plane sowie einen Platz, den erst das Verschieben des Absetzers 1 schafft.
- **Werte und Belegstand:**
  - Abstand >= 500 mm zu brennbarer Folie und Holz oder A1-Platte: Annahme [A].
  - Unterlage nicht brennbar (Beton, Stahlsockel): [A].
  - Schutzart IP54 innen wie aussen, also staubgeschuetzt und spritzwassergeschuetzt: [A].
  - Die zustaendigen Normen sind benannt, ihre Zahlenwerte aber nicht gelesen: DIN VDE 0100-705:2007-10 (landwirtschaftliche und gartenbauliche Betriebsstaetten) und DIN VDE 0100-420:2022-06 (Schutz gegen thermische Auswirkungen).
  - Eine zweite Quelle mit Zahlen fehlt. Das ist **OFFEN (Recherche)** und kein Bauhindernis fuer V1, weil der Schrank dort nicht bewegt wird.

## Eingaben (nur diese; Zeilen selbst nachsehen)
- `scripts/technik_e13.py` `gruppe()` (Zeile 25 bis 39), `ABG` (Zeile 45), Router `hindernisse()` (ab Zeile 50): Diese Lagen werden umgestellt.
- `scripts/n_technik_innen.py`: `TURM`, `V1_PORT` (Ports der Schaetzung) und `pruef`.
- `data/params.json` `technik_x`, `technik_y`, `technik_az` (Zeilen um 889 bis 898); `scripts/gen_dome.py` `schrank_fn` (Zeile 494 bis 510).
- `docs/parts/aktivkohle_station.md` (Masse: Behaelter Ø254 x 889, Sediment Ø112 x 290, Kopf 120), `geblaese_luft.md` (Box x -120..412, y -190..90, H 730), `luftverteiler_6.md` (Laenge 710, Teilung 120).
- `docs/leitungsordnung.md` R1 bis R9 und die Ausnahmen 4 bis 6; `docs/jobs/pruefung/M10-S5-LUFT-B.md` Auflagen A1 bis A3.

## Schritte
**Teil A, Werkstatt (darf sofort und parallel zu M10-S2N laufen, beruehrt das Modell nicht):**
1. **Bauteil `technik_turm`:** Stahlrahmen 800 x 500 x 2000, Boden mit Auffangwanne (Wasser unten). Gitterrost bei Z 1000 relativ fuer die zwei Geblaese mit Gummifuessen. Konsole oben fuer `luftverteiler_6` mit der Muffe A bei etwa Z 1750 relativ und Abgaengen nach unten. Halterleiste fuer die Steiger auf der Rueckseite (R7: Halter am Turm = "Pumpentafel"). Bauteilblatt mit Port-Tabelle.
2. **Variante `aktivkohle_station` kompakt:** Sediment, Kohle 1 und Kohle 2 in einer Reihe in 800 x 450, H <= 930 (254 + 254 + 112 + 2 x 60 Luecke = 740 mm). Ein- und Ausgaenge K39, K40, K41, K52 an der Rueckseite, Zaehler-Halter MS50 bleibt. Die alte Station bleibt als Variante erhalten.
3. **Absetzer-Luftanschluss (Pruefer A1):** Stutzen d20 im Deckel von `tank_klein` fuer K47/K48. Fehlt er bei Montagebeginn, bleiben K47/K48 OFFEN wie bisher.

**Teil B, Montage (eigene Runde nach der Abnahme von M10-S2N, vor M10-S3; je Schritt ein Pfad-Commit):**
4. **Parameter:** `data/params.json` neu `turm_x` = 600 und `turm_y` = -4900 (Quelle "N-TECHNIK-INNEN, Platzsuche gang300"). Gegenprobe: `python -X utf8 scripts/n_technik_innen.py pruef` muss PASS melden. Hat M10-S2N neue Hindernisse in den Tuerkeil gesetzt, `suche gang300` neu laufen lassen und den Wert uebernehmen. `technik_x`/`technik_y` bleiben der Schrank (V1).
5. **Gruppe umsetzen:** In `scripts/technik_e13.py` `gruppe()` liegen Station, Geblaese und Verteiler jetzt relativ zu (`turm_x`, `turm_y`) im Turm. Die Station steht unten (Koepfe Z 1240 wie bisher), die Geblaese stehen auf dem Rost (Austritt etwa Z 2110), der Verteiler oben (Z 2150, Schleife ueber dem Spiegel 915). Front +X zum Tuergang. Komponente umbenennen in `14_Technik_Turm`; der Schrank bleibt in seiner Komponente am Platz von Runde 74.
6. **Leitungen neu:** `python -X utf8 scripts/technik_e13.py` routet alle Kanten von den neuen Ports.
   - Fuer R8 (Pruefer A2) bekommt das Frischwasser (K40, K41, K52) einen eigenen Graben mit >= 250 mm Achsabstand zum Luftbuendel; Router-Kosten `NAH` beibehalten.
   - Fuer R5 duerfen die festen Boegen an Port und Steiger als Ausnahme in `docs/leitungsordnung.md` stehen; Kennzeichen-Feld `port_boegen` in der Trasse, Wortlaut im Paket.
   - K47/K48 verlegen, wenn Schritt 3 fertig ist.
   - Der Startpunkt von K39 bleibt das Ende von `T10_Zulaufrohr` (Az -58).
   - Die Kabel Schrank -> Turm (Leerrohr DN100 und DN50) liegen als Trasse im Graben KG, Band U, nur als Leerrohr (Kabelzahl M10-S6).
7. **Build** `sh scripts/build.sh 5 <naechste Runde>` (D82: >= 10 GB freier Arbeitsspeicher vorher). Dann die Pruefpunkte unten, Nahbild `renders/technik-turm-<runde>.png`, `docs/loop-state.md` Abschnitt "N-TECHNIK-INNEN", Paket nachfuehren.

## Nicht anfassen
- Teil A der Luft (`Luftverteiler_4`, 4 Scheiben, `Schwimmerventil_Pool`, K44-S1..S4)
- Wasser-Hauptkreislauf, Heber K01/K17, die Arbeit von M10-S2N (Schacht, Revisionsstutzen, Hahne)
- `data/leitungsnetz.json`, `data/roadmap.json`, `data/katalog.json`, `data/beschaffung/`
- Lage von Tanks, Pumpen, Puffer, Becken und Beeten (V2 erst nach Bens Ja)
- Kabel und Kabelzahl (M10-S6); M10-S2V bleibt geparkt

## Dateiliste (darf schreiben)
- Werkstatt: `designs/components/technik_turm.sc`, `aktivkohle_station*.sc`, `tank_klein.sc` (nur der Stutzen), `scripts/workshop/`, `docs/parts/`, `data/components/`, `data/descriptions.json`.
- Montage: `data/params.json` (nur `turm_x`, `turm_y`), `scripts/technik_e13.py`, `scripts/gen_dome.py` (nur Einbau Turm und Station), `scripts/leitungen.py` (nur falls noetig), `data/leitungstrassen.json`, `docs/leitungsordnung.md` (nur die Ausnahme `port_boegen`), `scripts/check_leitungsordnung.py` (nur diese Ausnahme), `designs/dome.sc`, `scripts/dome-script.json`, erzeugte `designs/components/lt_rohr_d*_L*.sc`, `docs/loop-state.md`, `docs/packages/n-technik-innen.md`, `renders/`.

## Ergebnis
Technikturm innen bei x 600 / y -4900 mit Station, 2 Geblaesen und Verteiler; 9 Kanten (11 mit K47/K48) neu verlegt und kuerzer; Schrank aussen unveraendert (V1, Ben bestaetigt beim Zwischencheck); Kennzahlen vorher/nachher im Paket gemessen statt geschaetzt.

## Pruefpunkte (fremd messbar)
1. **Lage:** `python -X utf8 scripts/n_technik_innen.py pruef` Exit 0 (Beet-Portal >= 300, Tank/Pumpe >= 150, Tuerachse >= 450, Huellenluft in 2000 mm Hoehe >= 110). Zusaetzlich liegen `Aktivkohle_Station:1`, `Geblaese_Luft:1`, `Geblaese_Luft:2` und `Luftverteiler_6:1` mit ihrem Ursprung im Rechteck x 200..1000 / y -5150..-4650 (Instanzmatrizen in `scripts/dome-script.json`). Soll 4 von 4.
2. **Laenge:** Summe der Trassenlaengen aller Trassen mit `linie` in (`luft_b`, `frisch`) in `data/leitungstrassen.json`, ohne K47/K48: <= 85,0 m (V0 104,9 m). Jede der 9 Kanten ist kuerzer als in Runde 74 (Werte im Abschnitt Varianten). Messung: Python ueber `pfad`, Summe `math.dist`.
3. **Leitungsordnung:** `python -X utf8 scripts/check_leitungen.py` nur die 3 Altbefunde (K08 KOLL, K05 und K21 GEFAELLE). `python -X utf8 scripts/check_leitungsordnung.py` R1 bis R9 ohne Befund an K39, K40, K41, K44, K45, K46, K49, K51, K52 (R5 mit der Ausnahme `port_boegen`, R8 Achse >= 250 mm oder lichter Abstand 25 bis 60 mm).
4. **Gaenge:** `python -X utf8 scripts/check_walkways.py` PASS mit Laufweg A >= 700, B >= 600, Wandluft >= 110, Tuergang >= 900 (Runde 74: 3177).
5. **Unveraendert:** `git hash-object data/leitungsnetz.json data/roadmap.json` gleich dem Stand vor der Runde; die Matrizen von `Luftverteiler_4:1`, `Luft_Scheibenbelueftung:1..4` und `Schwimmerventil_Pool:1` sind gleich; `technik_x`/`technik_y` 500/-6490 (Schrank) sind gleich.

## Start-Hinweis fuer die Bau-Sitzungen
1. Werkstatt (Teil A) darf sofort starten; die Montage (Teil B) erst nach der Abnahme von M10-S2N, nur eine Montage zugleich (D80), D82 Arbeitsspeicher.
2. Der Tuerkeil ist knapp: nach M10-S2N zuerst `suche gang300` und `pruef` laufen lassen, weil neue Graeben, Schaechte oder Stutzen den Platz verschieben koennen. Ist die Lage weg, nicht ausweichen, sondern melden.
3. Falle Runde 74: K46 wurde in Build 75 "deckungsgleich", Router-Ziele nicht auf fremde Trassen legen. Falle W37-3: `insert_design` kennt nur `translate`, drehen per `occurrence.move` mit Matrix.
4. Die Laengen in diesem Blatt sind Schaetzungen [A]; das Paket bekommt die gemessenen Werte aus `data/leitungstrassen.json` nach dem Routing.
5. Limit: ein Paket je Sitzung; Stand in `docs/loop-state.md`, Meldung hoechstens sechs Zeilen, dann STOPP.

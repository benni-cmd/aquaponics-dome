# N-AUTOBAHN-FIX: Wasserautobahn (Ring B2) realistisch machen: Einspeisung aus dem Gang, Aussen-Ausleger unter die Kuppelhaut, Ruecklauf ueber dem Pool-Spiegel

Planer 05.11.2026 (Opus 5.5). Paket: `docs/packages/n-autobahn-v2.md` (Montage-Befunde 1, 4, 5). Vorgaenger-Blatt: `docs/jobs/N-AUTOBAHN-V2.md`. [Q] Quelle im Repo · [E] eigene Messung oder Rechnung dieses Blatts · [A] Annahme dieses Blatts. Z relativ zum Innenboden, absolut = relativ + 400.

**Problem:** Die Wasserautobahn steht im Viewer, ist aber an drei Stellen nicht baubar: (1) Pegelschacht, Podest und Booster beider Linien stehen in Gang A bzw. B und schneiden den Rundgang ab; (2) die 8 Aussen-Ausleger und ihre Schlaeuche ragen 61 bis 254 mm durch die Kuppelhaut; (3) der geplante Schlauch-Ruecklauf in der Bodenrinne muendet unter dem Pool-Spiegel, deshalb wurde er nicht gebaut, und Ring-Ende und Notueberlauf enden offen ueber dem Boden.
**Intent:** Ben und Leon sehen die Autobahn so, wie sie gebaut wuerde, und vergleichen sie fair mit dem Hauptweg (A+ bzw. Zielbild S). Ein Fehler im Modell darf den Vergleich nicht verzerren.
**Ziel (ein Satz):** Nach der Montage-Runde N-AUTOBAHN-FIX steht in `designs/dome-ring_b2.sc` keine Einspeisung im Gang, kein Ausleger oder Schlauch naeher als 100 mm an der Kuppelhaut und keine Autobahn-Leitung mit offenem Ende oder mit Muendung unter dem Pool-Spiegel; die Pruefpunkte in Abschnitt 5 sind gruen und A+ bleibt byte-gleich.

## Aktualitaetspruefung (W44), 05.11.2026
Ergebnis: **angepasst** (Plan gilt als freigegeben). Eine Reihenfolge-Frage geht an den Orchestrator (Abschnitt 8, Punkt 1).
1. Leitungsordnung v2 ist gepusht (`git log -1 -- docs/leitungsordnung.md` = 5a3da4d). Sie gilt fuer jede Leitung in diesem Blatt. Fuer den Ring selbst sagt sie: Die Autobahn ist ein eigener Korridor mit eigenen Stelzen und steht nicht in der Ordnung [Q leitungsordnung.md Abschnitt Korridore]. Die Schlaeuche von Ring zu Abnehmer sind Art B (Druckschlauch), Ring-Ende und Notueberlauf sind Art C (Schwerkraft).
2. D88 (Zielbild S) aendert den gemeinsamen Bestand, auf dem Ring B2 steht [Q `docs/jobs/M10-ZIELBILD-S.md` Abschnitt 1]: Pool-Spiegel von Z 515 auf -150, Aufkantung bis Z 150; Feinfilter, Absetzer (`Tank_klein`), `Pumpe_klein` und die Bodenpumpen `Pumpe_gross` verschwinden vom Flur (Z1, Z2); Beete stehen 162 bis 209 mm hoeher; je Linie kommt eine Wasserstation an den Biofilter (Z3). **Das bestimmt Befund 1 und 3** (Abschnitt 1).
3. D91 (Scherenknoten, Rundrohr 42,4 x 2,6): Die Montage `montage-knoten` laeuft gerade. Die Rohrachse geht durch den Knotenpunkt, der Achsversatz ist auf 5 mm begrenzt [Q `docs/jobs/N-VERBINDER.md` Pruefpunkte 1 und 4]. Das Rundrohr ist 6 mm dicker im Radius als das alte 30er-Profil. Die Haut verschiebt sich also um wenige Zentimeter. Dieses Blatt plant 100 mm Abstand als Reserve und misst am gebauten Knotenmodell.
4. Warteschlange [Q `docs/packages/bis-zwischencheck.md` Zeile 44]: (1) Knoten, (2) dieser Fix, (3) Zielbild S Z1 bis Z7. Befund 1 laesst sich vor Z1 nicht loesen (Abschnitt 1 Punkt 1). Deshalb teilt dieses Blatt die Runde in drei Teile mit eigenem Startzeitpunkt (Abschnitt 4).
5. Nicht in diesem Blatt (Ben nannte drei Befunde): Clip-Abstand und Clip-Lage (R2 FAIL 2 und 3) sowie Abzweige auf dem PE-Bogen (Montage-Befund 2). Sie stehen als eigene Frage in Abschnitt 8.

## 1. Die drei Befunde, gemessen
**F1 Einspeisung im Gang.** Pegelschacht Linie 1 liegt bei r 2581 und ragt 464 mm in Gang A (r 2195 bis 2795). Linie 2 liegt bei r 4134 und ragt 425 mm in Gang B (r 3959 bis 4492). Die Gangkarte zeigt als NICHT erreichbar: 6 Aussenbeete, 4 Booster, `Pumpe_gross:1/:4` und `Pumpe_klein:3`; bei A+ ist nichts davon gesperrt [Q Paket, Pruefpunkte R1].
Platzsuche [E, Planer-Skript im Scratchpad; Hindernisse wie `scripts/check_walkways_voll.py`, Kniescheibe, Kreis um die Gruppe plus 50 mm Luft, ausserhalb beider Gangbaender, Azimut Biofilter +-60 Grad]:
1. Die heutige Gruppe aus Podest, Fass und 2 Boostern mit Saugleitung braucht einen Kreis mit Radius 1012 mm. Dafuer gibt es weder im heutigen Bestand noch nach Zielbild S einen Platz (0 Treffer).
2. **Heutiger Bestand:** Auch eine kompakte Gruppe mit Radius 500 mm hat 0 Plaetze bei Linie 1 und 0 Plaetze bei Linie 2 nahe dem Biofilter. Nur Radius 350 mm passt: Bei Linie 1 liegt der naechste Platz 2,4 m vom Biofilter entfernt, bei Azimut -45.
3. **Nach Zielbild S Z1 und Z2** (ohne Feinfilter, Absetzer und Flurpumpen): Fuer eine kompakte Gruppe mit Radius 500 mm gibt es 21 Plaetze bei Linie 1 und 33 bei Linie 2. Die naechsten liegen bei Linie 1 bei r 3300, Azimut -27 (1,28 m von der Biofilter-Mitte) und bei Linie 2 bei r 3300, Azimut -78 (1,16 m).
Folgerung: Die Einspeisung bekommt ihren Platz erst nach Z1/Z2. Sie braucht eine kompakte Bauform, Abschnitt 3 W-FIX-2.

**F2 Aussen-Ausleger durch die Haut.** Die 8 Aussen-Ausleger enden bei r 5187 bis 5239 auf Z 2677 absolut [E, Lagen aus `trassen_ring.fallleitungen()`: Flansch r 3997 (Joch, 7 Stueck) bzw. 3869 (Stelze -17,7), Laenge 1210 bzw. 1370]. Die Montage hat gemessen, dass sie 61 bis 254 mm hinausragen; die Schlaeuche ragen bis 209 mm hinaus [Q Paket R2].
**Schluesselmass:** Der Zulauf-Port jedes Aussentischs liegt bei r 4732, Z 1491 absolut, also nur 240 mm hinter Gang B. Der Port jedes Aussenbeets liegt bei r 5580, Z 850 absolut [E, gleiche Quelle]. Die langen Arme reichen also unnoetig weit nach aussen. Schon ein Arm bis knapp hinter Gang B genuegt.

**F3 Ruecklauf unter dem Spiegel.** Die Bodenrinne der Gangquerung hat ihre Schlauchsohle bei Z -98. Das liegt unter dem heutigen Pool-Spiegel Z 515 [Q `docs/parts/autobahn.md` WA-S Befund 4]. Ring B2 nutzt deshalb heute den starren Ruecklauf K15/K31 von A+. Ring-Ende (K66/K74) und Notueberlauf (K67/K75) enden offen ueber dem Boden [Q Paket, Montage-Befund 4].
Physik dazu:
1. Der NFT- und Beet-Ruecklauf ist in beiden Varianten derselbe: gleiche Tische, gleiche Beete, gleicher Pool. Zielbild S plant ihn fuer beide neu, und zwar als freie Schwerkraft-Leitungen, Gangquerung als Art F und Einmuendung ueber dem Ruhepegel [Q M10-ZIELBILD-S 2.3, 2.4 Punkte 4 und 6].
2. Ein eigener Autobahn-Ruecklauf (Blatt N-AUTOBAHN-V2 2.5, Runde R2c) ist deshalb kein Unterschied zwischen den Varianten, sondern doppelte Arbeit.
3. Variantenspezifisch sind nur Ring-Ende und Notueberlauf.

## 2. Loesung je Befund (fachlich festgelegt)

### 2.1 F1: Einspeisung am Stationsplatz, kompakt, Ring-Ende zurueck in den Schacht
1. **Platz:** Die Einspeisung jeder Linie steht dort, wo im Hauptweg nach Zielbild S die Wasserstation am Biofilter steht (Designprinzip 4: je Linie eine Station am Biofilter). Die Station gibt es nur in A+ bzw. Zielbild S, die Einspeisung nur in Ring B2. Beide schliessen sich aus, deshalb duerfen sie denselben Platz belegen. Hat Z3 den Stationsplatz noch nicht festgelegt, sucht die Montage den Platz mit den Bedingungen aus Pruefpunkt P1. Startwerte [E]: Linie 1 r 3300, Azimut -27; Linie 2 r 3300, Azimut -78.
2. **Kompakte Bauform (W-FIX-2):** Die 2 Booster stehen in einer Pumpen-Etage unter dem Fass im Podest, statt daneben auf eigener Saugleitung. Die Gruppe passt dann in einen Kreis mit Radius 500 mm, Fass-Stutzen eingeschlossen. Der Fassboden bleibt auf Z 820. Die Saugleitung wird kuerzer (heute 200 + 330 mm waagerecht [Q `trassen_ring.py` L_SAUG1/2]).
3. **K10/K26:** frei fallend vom Biofilter-Ueberlauf (Z 1570) in den Fassdeckel, Art C, Gefaelle mindestens 1 %. Ab 1,2 m Laenge sinkt das Podest um 10 mm je weiteren Meter [Q autobahn.md WA-T Befund 4]. Bei 1,16 bis 1,28 m Abstand zum Biofilter bleibt es bei etwa Z 820.
4. **Ring-Ende (K66/K74) zurueck in den eigenen Pegelschacht, nicht in den Ruecklauf.** Der Ueberschuss-Hahn sitzt am Ringende, das dem Schacht der eigenen Linie am naechsten liegt: Linie 1 an der Ecke -53,7, Linie 2 an der Ecke -89,7. Ein Schlauch Art C faellt von Z 2145 in den Fassdeckel (etwa Z 1395), ohne einen Gang zu queren, denn Ring und Schacht liegen beide in der Mittelzone. Soll-Durchfluss 14,5 bzw. 17,5 l/min [Q Netz K13/K29, gleiche Aufgabe]. Am anderen Ringende (Ecken 90,3 und 126,3) bleibt nur der Entleerungshahn mit Schlauchtuelle und Kappe. Das ist ein Zugang zum Ablassen, keine feste Leitung.
   Vorteil: Fuer das Ring-Ende ist keine Leitung zum Pool noetig, das spart Teile (Designprinzip 3). Der Ueberschuss kreist kurz und sauber zum Booster zurueck.
5. **Kein Einlauf unter dem Spiegel:** Ring-Ende und K10 enden im Fass ueber dessen hoechstem Pegel, also ueber dem Notueberlauf-Stutzen [Q `docs/hydraulics.md` Abschn. 2.9].

### 2.2 F2: Kurze Aussen-Ausleger, Fall gleich hinter Gang B
1. **Arm-Laenge aussen:** Der Arm endet so, dass die senkrechte Fallachse des Schlauchs bei r 4732 +- 30 liegt, also ueber dem Port des Aussentischs. Mindestens muss sie bei r 4560 liegen (Gang B endet bei 4492, dazu halber Schlauch-Aussendurchmesser und 50 mm Luft [A]). Ueberschlag [E]: Bei 7 Armen am Joch etwa 0,55 bis 0,65 m statt 1,21 m, beim Arm an der Stelze -17,7 etwa 0,7 bis 0,8 m statt 1,37 m. Die genaue Laenge rechnet die Werkstatt (W-FIX-1) aus Flanschradius, Endbuegel und Biegeradius (R14: Radius mindestens 6 mal Schlauch-Aussendurchmesser).
2. **Tisch aussen:** Der Schlauch faellt senkrecht vom Armende auf den Regelhahn und laeuft dann in den Port. Fallhoehe: Arm Z 2677 bis Port Z 1491 absolut = 1186 mm, das ist unter der Grenze von 1500 mm [Q N-AUTOBAHN-V2 2.6 Punkt 3].
3. **Beet aussen:** Gleicher Fall bis auf Beetrand-Hoehe, dann waagerecht etwa 850 mm am Beetrand bzw. Tischbein entlang bis zum Port bei r 5580. Halter hoechstens alle 400 mm oder Feld `aufliegend` (R6); Befestigung nur an Beetrand oder Tischbein (R7). Nach Z1 steht das Beet 162 bis 209 mm hoeher; `trassen_ring.py` rechnet die Wege aus den Instanzen und folgt dem von selbst.
4. **Haut-Reserve:** Mit Armende bei etwa r 4650 bleiben auf Z 2677 etwa 400 mm Abstand zur Facettenebene [E, Ueberschlag: Die Montage mass bei Armende r 5196 bis 5239 einen Ueberstand von 61 bis 254 mm]. Das Soll sind 100 mm [A]: Scherenknoten mit 6 mm dickerem Rohr plus Durchhang der Folie. Gemessen wird am gebauten Knotenmodell (P2), nicht an der Rechnung.
5. Innen-Ausleger und Mittelzone bleiben unveraendert.

### 2.3 F3: gemeinsamer Ruecklauf, Notueberlauf ueber die Ueberlauf-Trasse der Station
1. **R2c entfaellt fuer Ring B2:** Kein eigener Schlauch-Ruecklauf d50, keine Ruecklauf-Rinne und keine 6 Bodenrinnen im Modell. Die Bauteile bleiben im Werkstatt-Bestand (`docs/parts/autobahn.md` WA9). Ring B2 erbt den Ruecklauf des Hauptwegs: heute K15/K31 starr (so gebaut), nach Zielbild S Z4 dessen freie Leitungen. Das Feld `varianten` faellt bei gemeinsamen Ruecklauf-Trassen weg.
2. **Notueberlauf (K67/K75) = Ueberlauf-Trasse der Station.** Die Station leitet in Zielbild S ihren Ueberlauf K13/K29 als Art C in den Pool (Z3) [Q M10-ZIELBILD-S Abschnitt 4]. Der Pegelschacht steht am selben Platz (2.1 Punkt 1), also nutzt der Notueberlauf diese Trasse ab dem Schacht-Stutzen. Gangquerung als Art F, Einmuendung durch die Poolwand ueber dem Ruhepegel Z -150 mit Belueftungsloch, wie der Beet-Ruecklauf (M10-ZIELBILD-S 2.3: Muendung Z -60; bei Stromausfall steigt der Pegel auf Z -39, deshalb ist das Loch Pflicht).
3. **Bemessung:** Faellt der Booster aus, laeuft der ganze Biofilter-Ablauf ueber den Notueberlauf: 110 l/min je Linie [Q Netz K10/K26 Soll]. Rechnung nach Manning mit n 0,009 [A, glattes Kunststoffrohr], Gefaelle 1 %, voll laufend [E]: d63 (Innendurchmesser etwa 57) schafft etwa 100 l/min, zu wenig; d75 (etwa 69) schafft etwa 166 l/min, das reicht. **Festlegung: Notueberlauf d75, oder d63 mit mindestens 2 % Gefaelle.** Die Montage rechnet mit dem echten Gefaelle der Trasse nach (P4). Ist die Z3-Trasse kleiner bemessen, bekommt Ring B2 eine eigene Kopie mit `varianten: ["ring_b2"]`, und die Montage meldet die Abweichung an den Z3-Planer.
4. **Vor Z3/Z4 (Rueckfall, nur wenn der Orchestrator die Reihenfolge nicht aendert):** Der Notueberlauf faellt als Art C in den Ruecklauf-Sammler K15/K31 der eigenen Linie am naechsten Mitteltisch. Der Sammler muss 110 l/min aufnehmen; ist er d63 mit unter 2 % Gefaelle, ist das ein FAIL mit Befund. Ein offenes Ende ueber dem Boden ist in keinem Fall erlaubt.

## 3. Werkstatt-Vorlauf (eine Werkstatt-Sitzung, parallel zur laufenden Knoten-Montage, baut kein Gesamtmodell)
| Teil | Inhalt | Pruefung im Check |
|---|---|---|
| **W-FIX-1** `ausleger_schlauch_<L>` kurz (zwei Laengen: Joch, Stelze) | neuer Laengenwert im vorhandenen Generator `scripts/workshop/autobahn_t.py`; Laenge so, dass die Fallachse nach Biegeradius bei r 4732 +- 30 liegt (Flansch r 3997 bzw. 3869 [E]); Clip-Raster neu | Fallachse r (Soll 4732 +- 30, mindestens 4560); Durchbiegung am Ende <= 10 mm; Ports |
| **W-FIX-2** `pegelschacht_podest_b` (WA7 Rev. B) | Podest mit Pumpen-Etage: 2 `pumpe_gross` unter der Deckplatte, Fassboden Z 820, Saugleitung vom Fass-Stutzen nach unten; Grundriss so, dass ein Kreis mit Radius 500 mm alles einschliesst (Fass-Stutzen eingeschlossen) | Huellkreis <= 500; Booster ohne Werkzeug herausziehbar (eine Seite frei, Designprinzip 8); Interferenz 0 zwischen Podest, Fass und Boostern; Haltering bleibt |

Dateien: `scripts/workshop/autobahn_t.py`, `scripts/workshop/check_autobahn_t.py`, `designs/components/ausleger_schlauch_<L>.sc`, `designs/components/pegelschacht_podest_b.sc`, `data/components/autobahn_teile.json` (Schluessel `tragwerk`), `docs/parts/autobahn.md` (neuer Abschnitt W-FIX), `renders/components/autobahn/`.

## 4. Montage-Runde N-AUTOBAHN-FIX (eine Montage-Sitzung, drei Teile)
Nur EINE Sitzung baut das Gesamtmodell (D80). Gebaut wird nur `ring_b2`; A+ bleibt byte-gleich.

| Teil | Inhalt | Start, wenn |
|---|---|---|
| **FIX-a** Ausleger aussen | 8 Aussen-Ausleger durch W-FIX-1 ersetzen; Wege der 16 Aussen-Fallleitungen (8 Tische, 8 Beete) nach 2.2 in `trassen_ring.schlauch_weg()`; Haut-Abstand messen (P2); Bau | Knoten-Montage gepusht und W-FIX-1 fertig. **Sofort danach moeglich** |
| **FIX-b** Einspeisung | Podest Rev. B am Stationsplatz (2.1); K10/K26 neu; Ring-Ende-Hahn an Ecke -53,7 / -89,7 mit Schlauch in den Fassdeckel; Entleerungshahn mit Kappe am anderen Ende; Gangkarte (P1); Bau | Zielbild S Z2 gebaut (Flur frei) und W-FIX-2 fertig |
| **FIX-c** Ruecklauf | R2c-Trassen und Bodenrinnen aus `ring_b2` entfernen bzw. nie setzen; Notueberlauf nach 2.3 Punkt 2 (oder Rueckfall Punkt 4); Ruecklauf-Trassen gemeinsam ohne Feld `varianten`; Pruefung P4; Bau, Viewer-Export, Screenshots | Zielbild S Z4 gebaut; zusammen mit FIX-b, wenn Z3/Z4 schon stehen |

**Dateiliste Montage (schreibt):**
1. `scripts/trassen_ring.py` (Einspeisung, Ring-Ende, Fallleitungen aussen, Notueberlauf)
2. `scripts/gen_dome.py` (nur `ring_b2()`)
3. `data/leitungstrassen.json` (nur Eintraege mit `quelle: trassen_ring` und die Ruecklauf-Felder `varianten`)
4. `scripts/check_autobahn_montage.py` (neue Pruefungen aus Abschnitt 5) und neu `scripts/interf_ring_b2.py` (gezielte Interferenz, heute nur im Scratchpad der Montage)
5. `designs/dome-ring_b2.sc`, `scripts/dome-script-ring_b2.json`, `renders/ring_b2/`, `docs/walkway-map-ring_b2.md`, `docs/loop-state.md` (Abschnitt Ring B2), `docs/packages/n-autobahn-v2.md` (Stand)

**Liest:** dieses Blatt; `docs/leitungsordnung.md`; `docs/designprinzipien.md`; `docs/jobs/M10-ZIELBILD-S.md` 2.3, 2.4 und Abschnitt 4; `docs/parts/autobahn.md` (WA-T, WA-S, W-FIX); `data/components/autobahn_teile.json`; `docs/hydraulics.md` Abschn. 2.9.

## 5. Pruefpunkte (fremd nachmessbar)
1. **P1 Einspeisung ausserhalb der Gaenge:** `python -X utf8 scripts/check_autobahn_montage.py r1`: Pegelschacht beider Linien 0 mm Ueberdeckung mit Gang A/B; dazu neu: Podest-Grundriss und Booster 0 mm. `python -X utf8 scripts/check_walkways_voll.py --variante ring_b2`: Die Liste NICHT erreichbar ist leer wie bei A+; rote Engstellen Knie und Kopf nicht mehr als bei A+ auf demselben Bestand.
2. **P2 Haut-Abstand:** neue Pruefung in `check_autobahn_montage.py r2`: kleinster Normalabstand jedes Auslegers (Huelle des Teils) und jedes Schlauchs (Achse plus halber Aussendurchmesser) zu den Facettenebenen durch die gebauten Knotenpunkte, minus halben Rohrdurchmesser 21,2 mm, **>= 100 mm**. Dazu `python -X utf8 scripts/interf_ring_b2.py`: Ausleger und Schlaeuche gegen Streben, Knoten und Folie = 0 Treffer, **alle** Paare geprueft (R2 liess 2.054 Paare aus Zeitgruenden aus; das ist hier nicht erlaubt, notfalls in Teilen laufen lassen).
3. **P3 Gang und Fall:** Schlauch-Unterkante ueber Gang A/B >= Z 2100 (bestehende Pruefung); jede senkrechte Fallachse aussen bei r >= 4560; freier Fall <= 1500 mm; Schlauchende am Port <= 1 mm.
4. **P4 Ablaeufe:** `python -X utf8 scripts/check_leitungsordnung.py --nur-v2` mit Variante `ring_b2`: 0 Verstoesse R11, R12, R13 auf K10/K26, Ring-Ende und Notueberlauf. Zusaetzlich:
   1. Keine `ring_b2`-Trasse endet offen; jedes Ende sitzt an einem Port (Fassdeckel oder Pool-Einmuendung).
   2. Jeder Einlauf liegt ueber dem hoechsten Spiegel seines Ziels oder hat ein Belueftungsloch (hydraulics 2.9).
   3. Notueberlauf: Rechnung nach Manning mit dem gemessenen kleinsten Gefaelle >= 110 l/min, voll laufend.
   4. Im Bau-Skript gibt es 0 Instanzen `Bodenrinne*`, `Ruecklauf_Rinne*` und `Lt_Schlauch_d50` fuer `ring_b2`.
5. **P5 Nichts kaputt:** `python -X utf8 scripts/check_varianten.py --a-plus-gleich` Exit 0; SHA-256 von `gen_dome.py 5 <scratch>/a.json` vorher gleich nachher. Alle R1/R2-Pruefpunkte, die heute PASS sind, bleiben PASS (`check_autobahn_montage.py r2`). Viewer-Screenshot beider Varianten im echten Browser (`docs/ui-standard.md`).

## 6. Nicht anfassen
`designs/dome.sc` und alle A+-Eintraege; `data/leitungsnetz.json`, `data/roadmap.json` (Orchestrator); `docs/leitungsordnung.md`; die Blaetter M10-ZIELBILD-S und Z1 bis Z7 (FIX-b/c lesen deren Ergebnis, aendern es nicht); Innen-Ausleger, Ring, Joche, Stelzen; fremde unversionierte Dateien (`designs/components/*-ring_b2.sc` anderer Builds, `viewer/extras.json`, `viewer/varianten/`, `viewer/detail/`).

## 7. Pflicht-Check Designprinzipien (`docs/designprinzipien.md`)
1. **Physik vor Strom:** Ring-Ende, K10/K26 und Notueberlauf laufen per Schwerkraft. Die Booster bleiben, weil Wasser Gang A und B ueber Kopf nur gepumpt queren kann [Q N-AUTOBAHN-V2 Abschn. 5 Punkt 1]. Das Blatt aendert daran nichts. Erfuellt.
2. **Wenig graben:** Die Ruecklaeufe bleiben die des Hauptwegs, die Bodenrinnen entfallen. Der Notueberlauf quert einen Gang als Art F, wie es Zielbild S fuer alle Querungen vorsieht. Erfuellt.
3. **Wenig Teile:** Es entfallen 6 Bodenrinnen, die Ruecklauf-Rinnen, der Schlauch d50, 2 eigene Booster-Saugleitungen und die Ring-Ende-Leitungen zum Pool. Die Aussen-Ausleger werden kuerzer. Neu sind nur 2 Teilevarianten (W-FIX-1, W-FIX-2). Erfuellt.
4. **Technik in die Kuppel, eine Station je Linie am Biofilter:** Die Einspeisung steht am Stationsplatz. Erfuellt.
5. **Leitungen:** Druck und Verteilung starr (Ring, Steigleitung), Abzweig zum Abnehmer als Schlauch Art B, Ablaeufe als Art C mit Gefaelle und ohne Hochpunkt. Erfuellt.
6. **Lebensmittelecht:** keine neuen Werkstoffe; die Schlaeuche bleiben wie WA-S (D85). Das Podest beruehrt kein Wasser. Erfuellt.
7. **Kaufen vor Selbstbau:** Das Podest bleibt ein Selbstbau-Stahlgestell wie WA7, jetzt mit einer Etage mehr. Ein Kaufteil fuer zwei Pumpen unter einem Fass wurde nicht gesucht. **Abweichung, begruendet:** einfache Schweiss- oder Schraubkonstruktion aus 40 x 40 x 3, wie bisher.
8. **Wartbar:** Die Booster sind von einer Seite herausziehbar (W-FIX-2-Pruefung). Hahn und Regler bleiben auf Greifhoehe; der Entleerungshahn hat eine Kappe. Erfuellt.
9. **Sicherheit:** Der Notueberlauf ist fuer den vollen Biofilter-Ablauf bemessen. Er sorgt dafuer, dass bei Booster-Ausfall nichts ueberlaeuft und Wasser in den Pool kommt; die Fische haengen davon nicht ab, Notluft ist Sache von Zielbild S. Erfuellt.
10. **Ehrlich messen:** Die Plaetze und Armlaengen in diesem Blatt sind Planer-Ueberschlaege [E] aus einem Scratchpad-Skript. Gueltig werden sie erst durch P1 bis P4 aus Repo-Skripten. Annahmen: 100 mm Haut-Reserve, 50 mm Luft am Gang, Manning n 0,009. **Offen:** Die Annahmen stehen noch nicht in `docs/decisions.md`; das macht der Orchestrator (Abschnitt 8).

## 8. OFFEN
1. **OFFEN (Orchestrator) Reihenfolge:** Empfehlung: FIX-a gleich nach der Knoten-Montage; FIX-b nach Z2, FIX-c nach Z4, als Ring-B2-Teilschritte in der Z-Kette. Grund: Im heutigen Bestand gibt es fuer die Einspeisung keinen Platz ausserhalb der Gaenge (Abschnitt 1, F1 Punkt 2), und Z1 entfernt genau die Teile, die ihn blockieren. Gegenoption: alles jetzt, mit der Einspeisung im Tuer-Korridor; dann wird K10 laenger als 2 m, das Podest sinkt [Q Paket Befund 1], und nach Z1 muss die Einspeisung noch einmal umziehen.
2. **OFFEN (Orchestrator):** Annahmen aus Abschnitt 7 Punkt 10 in `docs/decisions.md` eintragen; Netz-Delta: K66/K74 endet am Pegelschacht statt am Ruecklauf, K67/K75 wird d75.
3. **OFFEN (Z3-Planer):** Stationsplatz je Linie so waehlen, dass ein Kreis mit Radius 500 mm hineinpasst. Der Platz wird spaeter in Ring B2 von der Einspeisung genutzt. Die Ueberlauf-Trasse K13/K29 auf 110 l/min bemessen (gilt physikalisch auch fuer die Station, wenn alle Strang-Haehne zu sind).
4. **OFFEN (Orchestrator, eigene Frage, nicht in diesem Blatt):** Clip-Abstand und Clip-Lage (R2 FAIL 2 und 3) und Abzweige auf dem PE-Bogen (Montage-Befund 2). Durch FIX-a aendern sich die Aussen-Clips; die Innen-Clips bleiben FAIL.
5. **OFFEN (Ben, unveraendert):** E20 (welche Variante gebaut wird).

## Start-Hinweis fuer die Bau-Sitzungen
1. Python immer `python -X utf8`; Skripte per Write, keine Heredocs mit `!` oder Backslashes.
2. Vor FIX-a `git log -3` an `scripts/gen_dome.py` und an den Knoten-Dateien pruefen: Die Haut-Pruefung P2 laeuft nur auf dem gebauten Knotenmodell.
3. Z-Falle: Blatt und Netz relativ, Trassen und Skripte absolut (+400). Pool-Spiegel steht in `data/layout.json` `pool.water_z` (heute 515, nach Z1 -150).
4. Die gezielte Interferenz (P2) war in R2 durch ein Zeitbudget abgeschnitten. Sie laeuft in Teilen und in einer Scratchpad-Kopie, nie im Arbeitsbaum.
5. Limit: vor jedem Start `get_usage`. FIX-a ist kurz (etwa 150 bis 250 Nachrichten), FIX-b und FIX-c zusammen ein normaler Montage-Lauf. Werkstatt W-FIX-1 und W-FIX-2 laufen in einer Sitzung.

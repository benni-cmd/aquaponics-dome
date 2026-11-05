# R56 Scherenknoten mit Lochplatte (W74): Funktion, Teile, Rohrform, Statik, Bezug

Stand 05.11.2026 · Paket `docs/packages/n-verbinder.md` · Rechnung `python -X utf8 scripts/r56_scherenknoten.py` (Selbsttest 6/6) · Prototyp `designs/components/knoten_schere_proto.sc` (Check 6/6) · **Gesamtmodell unveraendert.**
**Nachtrag Werkstatt 05.11.2026:** Der Prototyp `knoten_schere_proto` ist ersetzt durch das Bauteil `knoten_schere` (Platte + Arm A/B, `docs/parts/knoten_schere.md`); der Vorentwurf bleibt in Git (927d171).
Kennzeichnung: **[Q]** Quelle · **[E]** eigene Rechnung oder Beobachtung im Foto · **[A]** Annahme.

## Kurzantwort
1. **Funktion:** Je Strebe zwei gekreuzte Flachstahl-Laschen mit einer Drehpunktschraube. Liegen die beiden Augen aussen deckungsgleich auf der Lochplatte und sind mit EINER Schraube verschraubt, stehen innen im Rohr die zwei Nasen durch zwei gegenueberliegende Wandloecher nach aussen. Ohne Plattenschraube laesst sich die Schere um etwa 6,5 Grad je Seite oeffnen; dann ziehen die Nasen ein und das Rohr laesst sich aufschieben [E].
2. **Rohrform:** Empfehlung **Rundrohr 42,4 x 2,6 verzinkt (EN 10255)**. Es wiegt so viel wie das heutige 30 x 30 x 3 (2,55 gegen 2,54 kg/m), traegt aber gegen Knicken 1,6-mal so viel (B: 10,9 gegen 6,7 kN Euler). In das 30 x 30 x 3 passt die Schere nicht (Innenmass 24 mm) [E].
3. **Engpass:** Der Knick der Laschen um die Strebenneigung (A 15,9 Grad, B 18,0 Grad). Mit 5-mm-Laschen beginnen sie bei rund 4,6 kN Strebenkraft zu fliessen; mit 8-mm-Laschen bei rund 11,8 kN [E]. Nasen, Rohrwand und Schrauben tragen 13,6 kN oder mehr.
4. Der Prototyp zeigt eine Lochplatte und eine B-Schere im Rohrstueck, Nasen ausgefahren. Bilder: `renders/components/knoten_schere_proto/`.

## 1. Funktionsweise und Kraftweg
### Was das Foto zeigt (alles [E], Ausschnitte vergroessert)
- **Unten Mitte, Einzelteil:** zwei lasergeschnittene Laschen, gekreuzt, mit einer Flanschschraube im Kreuzungspunkt. Jede Lasche hat ein rundes Ende mit Loch (das Auge) und ein abgestuftes Ende mit einem seitlichen Lappen, der Nase. Die Nasen der beiden Laschen zeigen zueinander, wenn die Schere offen liegt.
- **Oben rechts, Rohr mit Schere:** Die Drehpunktschraube mit Mutter sitzt kurz vor dem Rohrende ausserhalb des Rohrs. Eine Lasche ragt mit dem Auge heraus und ist leicht abgekantet. In der Rohrwand sitzt etwa einen Rohrdurchmesser hinter dem Ende ein rundes Loch, in dem die Nase steht.
- **Knoten links:** sechs Streben. Je Strebe zwei Schrauben: eine auf dem Lochkreis der Platte (Augen) und eine am Rohrmund (Drehpunkt). Von oben sieht man nur EINE Laschenbreite, weil die zwei Laschen deckungsgleich uebereinanderliegen. Seitlich an den Rohren stehen kleine Nasen aus der Wand.
- **Unten rechts, Lochplatte:** rund, 6 Loecher auf einem Lochkreis und eine groessere Mittelbohrung.
- **Korrektur zu R41:** R41 las eine Lasche je Strebe mit Querschraube durch das Rohr. Eine Querschraube gibt es nicht; die Verbindung zum Rohr machen allein die zwei Nasen in den Wandloechern.

### Wie die Schere arbeitet (Ableitung [E], deckt sich mit Bens Beschreibung)
1. Die zwei Laschen kreuzen sich im Drehpunkt. Auf der Rohrseite traegt jede Lasche ihre Nase auf der Seite, die zur anderen Lasche zeigt.
2. **Geschlossen** (Augen deckungsgleich, Laschen uebereinander): Die Nasen zeigen in entgegengesetzte Richtungen quer zur Rohrachse und stehen 3 mm ueber die Rohraussenwand [A]. Das ist der eingerastete Zustand.
3. **Offen** (Augen auseinander): Jede Lasche dreht um den Drehpunkt, ihr Rohrende wandert zur Gegenseite und nimmt die Nase von der Wand weg. Bei Rohr 42,4 x 2,6 und Abstand Drehpunkt-Nase 58 mm reichen 6,5 Grad je Seite, die Rueckkante der Lasche bleibt dabei 1,5 mm frei [E: Skript, Abschnitt Nasen].
4. **Montage:** Schere offen ins Rohr schieben, bis die Nasen vor den Wandloechern stehen; Augen zusammenfuehren, die Nasen rasten ein; Augen mit der Plattenschraube auf den Lochkreis schrauben. Solange die Plattenschraube locker ist, dreht die Strebe um diese Schraube in der Plattenebene: das ist die Bewegungsfreiheit beim Aufbau. Angezogen kann sich die Schere nicht mehr oeffnen: unter Last fest.
5. **Neigung:** Die Streben stehen um 15,9 Grad (A) und 18,0 Grad (B) gegen die Plattenebene geneigt [E: asin(L/2R), wie R41]. Die Laschen sind ausserhalb der Platte um genau diesen Winkel abgekantet. Liegt die Platte um 25,5 mm unter dem Knotenpunkt [E: Prototyp], geht die Rohrachse durch den Knotenpunkt (Check: Abstand 0,000 mm).

### Kraftweg (je Strebenende)
Rohr (Druck oder Zug) → Lochrand der Rohrwand → 2 Nasen (Abscheren, Lochleibung) → 2 Laschen (Normalkraft, am Knick Biegung) → Plattenschraube M10 (einschnittig, Augen auf Platte) → Lochplatte → die anderen Streben. Die Drehpunktschraube haelt nur die Schere zusammen und traegt planmaessig nichts [E].

## 2. Teile je Knoten und je Strebenende
**Massstab im Foto [A]:** Es gibt keinen Massstab. Bezug sind die Flanschschrauben: Flanschdurchmesser etwa 17 mm bei M8 oder etwa 22 mm bei M10. Daraus ergeben sich Spannen; der Prototyp nimmt den Wert in Klammern.

| Teil | Foto-Spanne [A] | Prototyp [A] | Anzahl je Strebenende | Anzahl Kuppel (65 Streben, 26 Knoten) |
|---|---|---|---|---|
| Lochplatte, rund, 6 Loecher auf Lochkreis, Mittelbohrung | D 80 bis 105, Lochkreis r 30 bis 40, Mitte D 15 bis 20 | D 110 x 8, r 37, Loecher D 11, Mitte D 20 | (1 je Knoten) | 26 (4-, 5-, 6-wertig: Lochbild je Wertigkeit oder 6 Loecher fuer alle) |
| Lasche mit Auge, Drehloch und Nase | Breite 18 bis 24, Dicke 3 bis 5 | 20 x 5, Auge bis Drehpunkt 50, Drehpunkt bis Nase 58, Nase 10 breit | 2 | 260 |
| Plattenschraube (Augen auf Platte) | M8 oder M10 | M10 x 35 8.8 mit 2 Scheiben, Mutter | 1 | 130 |
| Drehpunktschraube | M8 | M8 x 25 mit 2 Scheiben, Mutter | 1 | 130 |
| Wandloch im Rohr, rund | D etwa 0,3 x Rohr | D 13 je Seite, 46 mm hinter dem Rohrende | 2 | 260 |

Masse [E, Skript]: Platte 0,54 kg, Lasche 0,11 kg; 6-wertiger Knoten ohne Schrauben 1,84 kg; alle 26 Knoten etwa **42 kg** gegen 155 kg Kugelknoten (knoten.md, gemessen). Keine Schweissnaht, kein Drehteil.

**Rohrlaengen mit Scherenknoten [E]:** Knotenpunkt bis Rohrende 101,5 (A) und 102,2 mm (B), Rohr A 3076 mm, B 3504 mm. A + B + Saegeschnitt = 6583 mm, also passt ein A und ein B in eine 7-m-Stange; in eine 6-m-Stange passt nur je ein Stueck. Die R34-Variante V2c (eine Laenge 2995 fuer alle) gibt es mit der Schere nicht ohne ueberlange B-Laschen, und genau die waeren der Knick-Schwachpunkt aus R41.

## 3. Rundrohr gegen Vierkantrohr
**Warum nachts Vierkant gewaehlt wurde:** Die Einkaufsliste nannte 30 x 30, und der Kugelknoten-Steckarm 23 x 23 musste in das Innenmass 24 des 30 x 30 x 3 passen (`docs/parts/strebe.md`, `knoten.md`); das OBJ hat ebenfalls 30 x 30 (D09). **Mit der Schere faellt der Steckarm weg, damit auch dieser Grund.**

| Profil | kg/m | Innen mm | Euler A/B kN | Nb,Rd A/B kN (Kurve c) | Schere 20 x 5 passt? |
|---|---|---|---|---|---|
| Vierkant 30 x 30 x 2 | 1,76 | 26,0 | 6,4 / 5,0 | 5,5 / 4,3 | nein |
| Vierkant 30 x 30 x 3 (heute) | 2,54 | 24,0 | 8,7 / 6,7 | 7,5 / 5,9 | nein |
| Vierkant 40 x 40 x 3 | 3,49 | 34,0 | 22,3 / 17,2 | 17,9 / 14,2 | knapp, mit Lasche 18 breit ja |
| Rund 33,7 x 2,6 | 1,99 | 28,5 | 6,8 / 5,2 | 5,8 / 4,6 | nein |
| **Rund 42,4 x 2,6** | **2,55** | **37,2** | **14,2 / 10,9** | **11,5 / 9,1** | **ja, 1,5 mm Luft** |
| Rund 48,3 x 3,2 | 3,56 | 41,9 | 25,4 / 19,6 | 20,0 / 16,0 | ja |
Quelle der Zahlen: Skript, Laengen A 3076 / B 3504, gelenkig K = 1; Vierkant scharfkantig gerechnet (Eckradien senken I um rund 10 %, [A]).

**Empfehlung: Rund 42,4 x 2,6 verzinkt.**
1. Gleiches Gewicht wie heute, 1,6-fache Knicklast.
2. Die Schere passt mit Luft; Platz fuer eine 8-mm-Lasche (siehe Statik).
3. Wasser laeuft ab, kein Eckenrost; Standardrohr der Wasser- und Geruestwelt, in Europa verzinkt in 6 m vorraetig (Abschnitt 5).
4. Das Foto zeigt genau diese Bauart mit Rundrohr.

**Was dagegen spricht:**
1. Die Keilschiene der Folienhuelle sitzt heute flach auf der Strebe (`docs/parts/keilschiene.md`); auf Rundrohr braucht sie einen Sattel oder ein dickeres Schaumband. Das ist eine offene Frage an Ben.
2. Die Wandloecher auf der Rundung brauchen eine Bohrlehre (Prisma), sonst verlaeuft der Bohrer.

Rueckfall bei flachen Flaechen als Muss: Vierkant 40 x 40 x 3 (37 % schwerer, Lasche 18 breit).

## 4. Statik grob
| Glied (je Strebenende) | Widerstand | Rechenweg |
|---|---|---|
| Rohr B 42,4 x 2,6 Knicken | 9,1 kN (Euler 10,9) | EN 1993-1-1 Knickkurve c, alpha 0,49; Euler wie R34/R41 |
| 2 Nasen 10 x 5 Abscheren | 13,6 kN | fy/sqrt(3), EN 1993-1-1 6.2.6 |
| Lochleibung Rohrwand an 2 Nasen | 18,7 kN | Schraubenformel 2,5 fu d t / gM2 sinngemaess, d = Laschendicke [A] |
| Plattenschraube M10 8.8, einschnittig | 22,3 kN | R34 nach EN 1993-1-8 Tab. 3.4 |
| Laschenpaar plastisch | 47,0 kN | 2 x 20 x 5 x 235 |
| **Knick der Laschen (B, 5 mm)** | **4,6 kN bis Fliessen** | Exzentrizitaet 8,4 mm an der Plattenschraube, 2 Laschen flach W = 167 mm3; Platte stuetzt nur einseitig |
| Knick der Laschen (B, 8 mm) | etwa 11,8 kN | W waechst mit t2: 4,6 x (8/5)2 |

**Einordnung:** R41 schaetzte die Strebenkraft grob auf 8,5 kN (A, aus dem Chemnitz-Bericht mit L2 hochgerechnet, ohne Wind). Mit 5-mm-Laschen waere der Knick unterhalb davon, mit 8-mm-Laschen darueber. Eine echte Lastannahme (Schnee, Wind, Standort) fehlt weiterhin (Statik ruht, D09); diese Zahlen sind Groessenordnungen.
**Quellen der Rechenwege:** Euler-Formel [Q: Wikipedia „Buckling", R34]; Knickkurven und Schubwiderstand [Q: EN 1993-1-1 Abschnitte 6.2.6 und 6.3.1, Werte wie in R34 verwendet, Normtext nicht neu gelesen]; Schraube und Lochleibung [Q: EN 1993-1-8 Tab. 3.4 ueber R34, dort zwei Formelsammlungen gelesen: IDEA StatiCa und steelcalculator]; S235 fy 235, fu 360 [Q: R34, Tata-Leistungserklaerung und Applus].

## 5. Kauf- und Laserteile (Bezug Europa, D76)
| Teil | Art | Quellen | Stand |
|---|---|---|---|
| Rundrohr 42,4 x 2,6 verzinkt, EN 10255, 6 m | Kaufteil | eHorst (DE): [42,4 x 2,6 S195T, 6,1 m](https://www.ehorst.de/en/VERZ-swivelled-tube-O-O-EN10255-L2-42-4-x-2-60-mm-S195T-11-4-1703771.html); Van Marcke (BE): [Rohr verzinkt 5/4", 6 m, EN 10255](https://blue.vanmarcke.com/fr_FR/Leidingen-en-installatiemateriaal/Aanvoer%3A-staal/Buizen-in-staal/Staal%3A-galva-buizen/Galva-buis---DIN-2440---per-lengte-6-m/p/20014796); metallshopper (DE): [42,4 x 2,65 verzinkt, Zuschnitt](https://metallshopper.de/Verzinkte-Rundrohre-oe42-4x2-65), laut Suchtreffer ab 16,91 EUR/m netto | zwei unabhaengige Haendler in DE und BE; Seiten nur als Suchtreffer, **Preise nicht gelesen** |
| Lochplatte D 110 x 8, Laschen 5 oder 8 mm, S235 | Laserteil per DXF | Laserteile4you (DE, DXF-Upload, Plasma erst ab 8 mm) [Q: Prospekt LT4U 2025-09, Suchzusammenfassung]; Metalxact (Blechzuschnitt online) [Q: Suchtreffer] | Anbieter belegt, **Stueckpreis offen** |
| Schrauben M10 x 35 und M8 x 25, 8.8 verzinkt, Scheiben, Muttern | Normteil | ISO 4017 / ISO 7089 / ISO 4032, ueberall in Europa | Standard |
| Feuerverzinken der Laserteile | Dienst | 0,50 bis 2,50 EUR/kg [Q: R41, zwei Ratgeberseiten] | Spanne |
Der Prototyp-Satz (1 Platte, 2 Laschen, 2 Schrauben, 250 mm Rohr) kostet bei einem Online-Laser eine Mindestbestellung; Preis nicht ermittelt.

## 6. Offene Fragen an Ben
1. **Funktion:** Stimmt die Lesart „Augen zusammen und verschraubt = Nasen aussen; Augen auseinander = Nasen innen"? Der Prototyp zeigt den eingerasteten Zustand.
2. **Rohr:** Rund 42,4 x 2,6 verzinkt statt 30 x 30 x 3? Folge fuer alle 65 Streben, Stueckliste, Keilschiene.
3. **Folienbefestigung:** Keilschiene auf Rundrohr mit Sattel oder Schaumband, oder ist Vierkant 40 x 40 x 3 dafuer Pflicht?
4. **Laschendicke:** 8 statt 5 mm wegen des Knicks (Masse +0,07 kg je Lasche)? Haeltst du das Foto-Teil fuer duenner?
5. **Masse aus Chemnitz:** Kannst du beim Forscher Laschendicke, Schraubengroesse, Rohrmass und Lochabstand erfragen? Damit wuerden die [A]-Werte zu [Q].

## Konfidenz und Luecken
- **Hoch:** Funktionsprinzip (Foto, Bens Beschreibung und Prototyp-Geometrie stimmen ueberein); Neigung und Rohrlaengen (Geometrie).
- **Mittel:** Querschnittswerte und Knicklasten der Profile (Formel, Tabellenwert 42,4 x 2,6 = 6,46 cm4 trifft).
- **Niedrig:** alle Kopfmasse (Foto ohne Massstab); Knick-Fliessgrenze (vereinfachtes Modell ohne Plattenstuetzung); Lochleibung an der Nase (Schraubenformel sinngemaess).
- **Keine:** Preise; Lastannahme; Verhalten unter Wechsellast (Klappern der Nasen im Loch).

## Recherche-Kritiker
1. Die Lesart der Nasenrichtung (Nasen zeigen zueinander) ist aus einem schraegen Foto abgeleitet. Waeren sie aussen, muesste die Schere umgekehrt schliessen; der Prototyp waere dann nur in der Nasenseite zu spiegeln.
2. Die Knickstelle ist im Foto (flach liegender Knoten) kaum zu sehen; vielleicht kommt das Original ohne Knick aus, weil Chemnitz eine flachere Kuppel hat (3V, kleinere Neigung).
3. Nur Haendler-Suchtreffer fuer das Rohr, keine gelesenen Preise.

## Quellen
1. Foto `reference/chemnitz/laschenknoten-foto.jpg` (vier vergroesserte Ausschnitte, selbst angesehen).
2. `docs/research/R41.md`, `docs/research/R34.md`, `docs/parts/knoten.md`, `docs/parts/strebe.md`, `docs/parts/keilschiene.md`, D09.
3. Haendler (Suchtreffer 05.11.2026): eHorst, Van Marcke, metallshopper, ArcelorMittal e-steel ([Welded steel pipe EN 10255](https://e-steel.arcelormittal.com/FR/en/Tube/Steel/Round/Welded-steel-pipe-EN-10255/p/000000000002117413)), Mecafluid ([42,4 x 2,6 galva](https://www.mecafluid.eu/en/catalog/tube-acier-soude-din-2458-ø-424-x-26-rainure-2-extrem-galva~f851fe17-7c7b-46a1-b8bb-180e5569cb92)).
4. Laser: [Laserteile4you Prospekt](https://www.laserteile4you.de/fileadmin/user_upload/Downloads/LT4U_DE_online_2025-09.pdf), [Metalxact](https://www.metalxact.com/en/sheets-plates-made-to-measure/sheet-steel/) (Suchtreffer).

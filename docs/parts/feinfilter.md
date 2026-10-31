# Bauteilblatt T55 feinfilter (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/feinfilter.json` und `designs/components/feinfilter.sc`, nicht von Hand aendern)

**Funktion:** Mechanischer Feinfilter je Linie (Schritt 3 der Kette in docs/filter-konzept.md, D51): Das Klaerwasser des Swirl-Absetzers (12,5 l/min je Linie, Schwerkraft) laeuft ueber ein senkrechtes Einlaufrohr in einen Siebkorb aus Edelstahlgewebe (ca. 150 Mikrometer) und tritt durch das Gewebe in die Ablaufkammer, aus der der Auslauf zur Saugseite der grossen Pumpen fuehrt. Der Korb faengt die feinen Schwebstoffe, die der Absetzer durchlaesst (Absetzer nur ca. 23 % der Feststoffmasse; FAO 589 verlangt ab 15 kg/m3 Fisch einen zusaetzlichen mechanischen Filter, wir haben 17 kg/m3). Zum Reinigen alle 1-2 Wochen (SRAC 454): Deckel per Spannverschluss oeffnen, Korb an den Buegelgriffen herausheben und ausspuelen, Behaelter ueber den Kugelhahn ablassen.

**Datei:** `designs/components/feinfilter.sc` · **Teilenummer:** T55 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche am Boden (Fussplatten-Unterkante z 0); X Laengsachse (Einlauf -X, Auslauf +X), Y Tiefe (Ablass -Y), Z hoch

**Anzahl (Instanzen):** 2 (Quelle: data/leitungsnetz.json: Knoten feinfilter_1 (Linie 1) und feinfilter_2 (Linie 2); layout.json kennt das Bauteil nicht)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `tank_l` | 400 | mm | [A] Blatt W31: Behaelter 400 x 300 x 500 (aussen) |
| `tank_w` | 300 | mm | [A] Blatt W31 |
| `tank_h` | 500 | mm | [A] Blatt W31 (Behaelterhoehe aussen, ohne Deckel und Standrahmen) |
| `wall` | 5 | mm | [A] PP-Platte 5 mm, geschweisst; Boden zwischen den Auflagestegen (100 mm Spannweite) rechnerisch ca. 1,3 MPa Biegespannung (E) |
| `foot_h` | 250 | mm | [A] Standhoehe Behaelterunterkante: Eimer (ca. 220 mm) unter den Ablass-Kugelhahn und Gefaelle zur Pumpen-Saugseite; Hoehenlage Montage M10 |
| `leg` | 30 | mm | [A] Vierkantrohr 30 x 30 x 2 verzinkt (Handelsprofil) |
| `leg_wall` | 2 | mm | [A] |
| `plate` | 60 | mm | [A] Fussplatte 60 x 60 |
| `plate_t` | 5 | mm | [A] |
| `brace_z` | 110 | mm | [A] Mitte der unteren Querstege ueber dem Boden |
| `bar_dx` | 100 | mm | [A] Abstand der Mittelstege in X (Boden-Spannweite 100 mm) |
| `ledge_w` | 12 | mm | [A] Auflageleiste PP an der langen Innenwand, traegt den Korbflansch |
| `ledge_t` | 12 | mm | [A] |
| `ledge_z` | 430 | mm | [A] Oberkante der Leiste ueber der Behaelterunterkante |
| `basket_l` | 340 | mm | [A] Korb aussen 340 x 240 (Spalt zur Wand 25 mm, Flansch 3 mm Spalt) |
| `basket_w` | 240 | mm | [A] |
| `basket_d` | 330 | mm | [A] Korbtiefe; Boden 98 mm ueber dem Behaelterboden (Ablaufkammer) |
| `flange_t` | 3 | mm | [A] Edelstahl 1.4301, Flansch 22 mm breit |
| `flange_ring` | 22 | mm | [A] |
| `mesh_t` | 1 | mm | [A] Modellierte Huellendicke des Gewebes; reale Gewebedicke ca. 0,1-0,2 mm |
| `mesh_density` | 0.55 | g/cm3 | [A] Ersatzdichte, damit die Huelle der realen Gewebemasse (ca. 0,5 kg/m2) entspricht; nicht die Werkstoffdichte |
| `rod` | 6 | mm | [A] Edelstahl-Flachstab 6 x 6 als Stuetzrahmen des Gewebes (4 Eckstaebe, Bodenrahmen) |
| `handle_h` | 40 | mm | [A] Buegelgriff 2 je langer Seite, Edelstahl-Rundstab 8 (Pfosten), 10 (Buegel) |
| `handle_d` | 10 | mm | [A] |
| `handle_dx` | 60 | mm | [A] |
| `gasket_t` | 3 | mm | [A] EPDM-Flachdichtung auf dem Behaelterrand |
| `lid_t` | 6 | mm | [A] PP-Deckel 6 mm |
| `lid_over` | 4 | mm | [A] Deckelueberstand je Seite |
| `latch_w` | 30 | mm | [A] Spannverschluss: Haken am Behaelter (Bock) und Spannhebel; Handelsteil (Exzenterspanner Edelstahl), Fabrikat offen |
| `latch_t` | 14 | mm | [A] |
| `latch_h` | 24 | mm | [A] |
| `latch_dx` | 110 | mm | [A] Lage der vier Verschluesse in X (je lange Seite zwei) |
| `inlet_d` | 50 | mm | [Q] data/leitungsnetz.json K05: dn 50 = Aussendurchmesser d50 (Blatt W31 nennt 'DN 50'; Netzliste-Konvention gilt) |
| `inlet_z` | 468 | mm | [A] Mitte Einlauf ueber der Behaelterunterkante (oben seitlich, 10 mm Luft zum Korbflansch) |
| `inlet_out` | 60 | mm | [A] Stutzenlaenge aussen |
| `inlet_in` | 75 | mm | [A] Mitte des senkrechten Einlaufrohrs im Korb (x vom Behaeltermittelpunkt) |
| `inlet_down` | 90 | mm | [A] senkrechtes Einlaufrohr ragt 90 mm unter die Einlaufmitte in den Korb |
| `wall_d50` | 2.4 | mm | [Q] data/components/leitungsteile.json sizes 50: Wand 2,4 |
| `wall_d40` | 1.9 | mm | [Q] data/components/leitungsteile.json sizes 40: Wand 1,9 |
| `outlet_d` | 50 | mm | [Q] data/leitungsnetz.json K06: dn 50 = d50 |
| `outlet_z` | 52 | mm | [A] Mitte Auslauf unten seitlich (Boden 5 mm, Ablaufkammer unter dem Korb) |
| `outlet_out` | 70 | mm | [A] Stutzenlaenge aussen ab Behaelterwand |
| `outlet_collar_d` | 75 | mm | [A] Dichtflansch und Gegenmutter der Durchfuehrung |
| `outlet_collar_t` | 5 | mm | [A] |
| `drain_d` | 40 | mm | [A] Ablassstutzen d40 (= DN32, wie Schlammablass K07 des Absetzers) |
| `drain_z` | 30 | mm | [A] Mitte Ablass ueber der Behaelterunterkante (Unterkante 10 mm: Rest unter dem Stutzen bleibt stehen) |
| `drain_x` | 120 | mm | [A] Lage des Ablasses in X an der Vorderwand (-Y) |
| `drain_in` | 5 | mm | [A] Stutzen ragt 5 mm in den Behaelter |
| `drain_stub` | 40 | mm | [A] Stutzenlaenge aussen bis Kugelhahn |
| `valve_d` | 56 | mm | [A] Kugelhahn d40 PVC, Gehaeuse D56, Durchgang 28 (Ersatzform) |
| `valve_l` | 50 | mm | [A] |
| `valve_lever` | 90 | mm | [A] Hebel quer zur Durchflussrichtung = zu |
| `barb_l` | 30 | mm | [A] Schlauchtuelle am Ablass |

Gesamt-Box (Messung): X -260.0 bis 270.0, Y -270.0 bis 170.0, Z 0.0 bis 793.0 mm; Koerper: 49.

**Toleranzen / Spiel:** Spalt Korbflansch zur Wand 3 mm je Seite (Entnahme ohne Klemmen); Einlaufrohr 10 mm ueber dem Korbflansch; Korbboden 98 mm ueber dem Behaelterboden; Auslauf-Dichtflansch 14 mm unter dem Korbboden; Pruefung check_feinfilter.py (Masse +-0,5 mm).

## Werkstoff und Gewicht

- Werkstoff: PP (Behaelter, Deckel), Edelstahl 1.4301 (Korb, Spannverschluesse), Stahl verzinkt (Standrahmen), PVC-U (Rohre, Kugelhahn), EPDM (Dichtung), Dichte PP 0,91 / Edelstahl 7,9 / Stahl 7,85 / PVC 1,4 / EPDM 1,1 / Gewebe-Ersatzdichte 0,55 g/cm3, Farbe #cfd3d6 (Handbuchwerte, Annahme)
- Volumen (Messung, `solidcraft-cli eval`): 6770.6 cm3 · Masse leer: 14021 g (14.02 kg)
- Gefuellt/in Betrieb: im Betrieb mit Wasser bis zur Unterkante des Einlaufs (z 443, ca. 49 l Wasser) ca. 63 kg [E]; Standrahmen und Untergrund muessen das tragen (Montage).

## Querschnitt / Profil

Behaelter PP-Platte 5 mm geschweisst, innen 390 x 290 x 495; 12 x 12 Auflageleisten an den langen Innenwaenden tragen den Korbflansch (Edelstahl 3 mm, 22 mm breit). Korb 340 x 240 x 330: Gewebehuelle mit Stuetzrahmen aus Edelstahl 6 x 6 (4 Eckstaebe, Bodenrahmen). Ablaufkammer unter dem Korb 98 mm hoch. Standrahmen Vierkantrohr 30 x 30 x 2 verzinkt mit Fussplatten 60 x 60 x 5.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Einlauf (Stutzen links, Winkel in den Korb) | PVC-U d50 (DN40), Wand 2,4 | x -260, y 0, z 718 (Oeffnungsebene aussen, Mitte); senkrechtes Rohr endet bei z 628, x -75 | Wasser tritt ein (Schwerkraft vom Absetzer, K05/K21), Oeffnung zeigt -X |
| Auslauf (Durchfuehrung rechts, unter dem Korb) | PVC-U d50 (DN40), Wand 2,4; Dichtflansch und Gegenmutter D75 | x 270, y 0, z 302 (Oeffnungsebene aussen, Mitte) | Wasser tritt aus zur Saugseite der grossen Pumpen (K06/K22), Oeffnung zeigt +X |
| Ablass mit Kugelhahn (Vorderwand, unten) | PVC-U d40 (DN32), Kugelhahn D56, Schlauchtuelle | x 120, y -270, z 280 (Ende der Tuelle, Mitte) | Wasser tritt aus zum Spuelen, Oeffnung zeigt -Y; Hebel quer = zu |

## Verbindungen und Befestigungen

- Rohrdurchfuehrungen in der PP-Wand: Auslauf mit Dichtflansch innen (D75 x 5), Gegenmutter aussen (D75 x 5) und Flachdichtung (nicht modelliert), Einlauf und Ablass als PP-Schweissstutzen oder Tankdurchfuehrungen d50/d40 (Hersteller offen) [A]
- Rohre PVC-U nach DIN 8062, Anschluss an die Leitungen der Montage ueber Muffe oder Verschraubung (leitungsteile)
- Spannverschluesse: 4 Stueck (je lange Seite 2) Edelstahl-Exzenterspanner mit Haken am Behaelter und Bock-Hebel am Deckel (Handelsteil, Fabrikat offen) [A]; Deckel liegt auf EPDM-Flachdichtung 3 mm
- Standrahmen: Vierkantrohr 30 x 30 x 2 geschweisst oder verschraubt (M8), Fussplatten 60 x 60 x 5; Behaelterboden liegt auf Ring und drei Auflagestegen (Spannweite 100 mm, Biegespannung PP rechnerisch ca. 1,3 MPa) [E]

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Funktion Feinfilter, Zweck, Reinigung alle 1-2 Wochen | Schritt 3 der Kette | Q | docs/filter-konzept.md Schritt 3 (FAO 589; SRAC 454), Befund 1 | hoch |
| Anzahl 2 (eine je Linie) | 2 | Q | data/leitungsnetz.json knoten feinfilter_1/2 | hoch |
| Anschluesse d50 (Ein-/Auslauf), 12,5 l/min | d50, 12,5 l/min | Q | data/leitungsnetz.json K05, K06, K21, K22 | hoch |
| Behaelter 400 x 300 x 500 | 400 x 300 x 500 | A | Blatt W31 (Masse E/A: Annahme) | niedrig |
| Behaelterwand PP 5, Deckel 6, Dichtung EPDM 3 | 5 / 6 / 3 mm | A | Konstruktionspraxis PP-Behaelter | niedrig |
| Siebkorb 340 x 240 x 330, Flansch 22 x 3, Spalt 3 mm | siehe Parameter | A | Entnahmespiel; Flanschauflage auf Leisten | niedrig |
| Gewebe 100-200 Mikrometer | ca. 150 | A | Blatt W31 (Hinweis); nicht modelliert | niedrig |
| Standhoehe 250 mm | 250 | A | Eimer unter dem Ablass; Hoehenlage Montage M10 | niedrig |
| Rohrwand d50 2,4 / d40 1,9 | mm | Q | data/components/leitungsteile.json | mittel |
| Ablassstutzen d40, Kugelhahn D56 | d40, D56 | A | wie Schlammablass K07 (dn 40) | niedrig |
| Dichten PP 0,91 / Edelstahl 7,9 / Stahl 7,85 / PVC 1,4 / EPDM 1,1 / Gewebe 0,55 | g/cm3 | A | Handbuchwerte; Gewebe-Ersatzdichte aus 0,5 kg/m2 Gewebemasse | niedrig |
| Port-Koordinaten (Einlauf, Auslauf, Ablass) | siehe Ports | E | gemessen aus den Stutzen-Boxen (check_feinfilter.py) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein Referenzbild (Bauteil fehlt im OBJ); docs/filter-konzept.md Schritt 3; data/leitungsnetz.json feinfilter_1/2
- Quelle der Masse: Blatt W31 (Behaelter 400 x 300 x 500 [A]); docs/filter-konzept.md Schritt 3 (Funktion), data/leitungsnetz.json feinfilter_1/2 und Kanten K05/K06/K21/K22 (d50, 12,5 l/min); Rohrmasse data/components/leitungsteile.json (d40 Wand 1,9, d50 Wand 2,4)
- Abweichung zum OBJ: Das Bauteil kommt nicht aus dem OBJ; es ist eine Empfehlung der Filteranalyse (R28, D51). Das Blatt W31 nennt Einlauf und Auslauf 'DN 50'; die Netzliste (K05, K06) meint mit dn 50 den Aussendurchmesser d50 (DN40). Das Bauteil folgt der Netzliste, damit der Anschluss an Absetzer-Auslass und Pumpen-Saugstutzen (beide d50) passt. Ablass d40 entspricht dem Blatt 'DN 32'.

## Montage (L4)

1. Standrahmen aufstellen, ausrichten (Wasserwaage), Fussplatten auf tragfaehigem Untergrund befestigen
2. Behaelter auf den Rahmen setzen und gegen Verrutschen sichern
3. Einlauf-, Auslauf- und Ablassstutzen mit den Leitungen verbinden (Einlauf vom Absetzer mit Gefaelle, Auslauf zur Saugseite der grossen Pumpen)
4. Siebkorb einsetzen (Flansch auf den Leisten), Deckel mit Dichtung auflegen und die vier Spannverschluesse schliessen
5. Probelauf mit 12,5 l/min; Wasserstand im Behaelter pruefen (steigt der Spiegel ueber den Einlauf, ist der Korb verstopft)

**Werkzeug:** Wasserwaage, Schluessel M8, Rohrschneider, PVC-Kleber, ggf. Kunststoffschweissgeraet

## Stueckliste-Zeile

- Behaelter PP 400 x 300 x 500, Wand 5, mit 2 Auflageleisten, 3 Durchfuehrungen: 1
- Siebkorb Edelstahl (Flansch 384 x 284 x 3, Gewebehuelle 340 x 240 x 330, 4 Eckstaebe, Bodenrahmen, 2 Buegelgriffe): 1
- Deckel PP 408 x 308 x 6 mit Griff: 1, EPDM-Flachdichtung 3 mm: 1, Spannverschluesse Edelstahl: 4
- Einlaufwinkel PVC-U d50 (waagerecht 210 mm, senkrecht 115 mm): 1, Auslaufrohr PVC-U d50 mit Dichtflansch D75 und Gegenmutter D75: 1
- Ablassstutzen PVC-U d40: 1, Kugelhahn d40: 1, Schlauchtuelle d40: 1
- Standrahmen: 4 Beine, 4 Ringstege, 3 Auflagestege, 2 Querstege (Vierkantrohr 30 x 30 x 2), 4 Fussplatten 60 x 60 x 5
- Gesamt: 2 Stueck (Linie 1 und 2)

## Alternative lokale Fertigung

Handelsueblicher Sieb-/Netzfilter: Regentonnen- oder Teichfilter-Behaelter mit Vlies- oder Netzsack statt Edelstahlkorb; Standrahmen aus Kantholz.

## Renders

- `renders/components/feinfilter/feinfilter-01-iso.png`
- `renders/components/feinfilter/feinfilter-02-vorn.png`
- `renders/components/feinfilter/feinfilter-03-einlauf.png`
- `renders/components/feinfilter/feinfilter-04-ablass.png`
- `renders/components/feinfilter/feinfilter-05-schnitt.png`

## Pruefung

- Gauntlet-Urteil: kein Pruefer-Lauf (Auftrag W31: Selbstcheck)
- scripts/workshop/check_feinfilter.py: Ergebnis in renders/components/feinfilter/check.txt (Masse, Wand, Korb im Behaelter, Ports, Hoehenfolge, Standrahmen, Interferenz)
- Kein Bild-Kritiker und kein Spec-Pruefer (Auftrag W31)

## Offene Fragen

- Hoehenlage: Der Einlauf liegt bei z 718 im Bauteil-KS (Standhoehe 250); damit das Wasser per Schwerkraft vom Absetzer-Auslass (100 mm unter Rand) kommt, muss der Absetzer-Auslass hoeher liegen. Montage M10 prueft Hoehen und passt foot_h an
- Kein Notueberlauf/Bypass: verstopft der Korb, steigt der Wasserstand ueber den Einlauf und staut im Absetzer zurueck; Ueberlauf in den Pool oder Bypass ist Sache der Hydraulik
- Gewebe-Maschenweite 100-200 Mikrometer ist ein Hinweis (nicht modelliert); die Huelle ist 1 mm mit Ersatzdichte 0,55; Gewebe-Fabrikat und Standzeit bis zum Verstopfen offen
- Spannverschluesse, Durchfuehrungen und Kugelhahn sind Ersatzformen (Handelsteile, Fabrikat offen)
- 12,5 l/min je Linie ist nur der Absetzer-Teilstrom; wird der Feinfilter in den Hauptstrom (110 l/min) gelegt, sind Korbflaeche und Verweilzeit neu zu rechnen
- Das Bauteil steht nicht in layout.json: Montage setzt die zwei Instanzen nach leitungsnetz.json

# Bauteilblatt T55 feinfilter (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/feinfilter.json` und `designs/components/feinfilter.sc`, nicht von Hand aendern)

**Funktion:** Mechanischer Feinfilter je Linie im HAUPTSTROM (Schritt 3 der Kette in docs/filter-konzept.md, D51, neu bemessen in W32/D55): Das Wasser der Linie (110 l/min, vom Pool zu den grossen Pumpen) laeuft ueber ein senkrechtes Einlaufrohr d63 in einen Siebkorb aus Edelstahlgewebe (Maschenweite 100 Mikrometer) und tritt durch das Gewebe in die Ablaufkammer, aus der der Auslauf d63 zur Saugseite der grossen Pumpen fuehrt. Die Siebflaeche folgt aus der Rechnung A = Q / Siebbelastung = 6.6 m3/h / 8 m/h = 0.825 m2; der Korb 560 x 370 x 400 mm liefert 0.840 m2 benetzte Flaeche (7.86 m/h). Gewebe 100 Mikrometer hielt im Versuch von Mortensen 21 % der Schwebstoffe zurueck (R30). Zum Reinigen alle 1-2 Wochen: Spuelanschluss mit Spritzrohr oeffnen, Deckel per Spannverschluss oeffnen, Korb an den Buegelgriffen herausheben und ausspuelen, Behaelter ueber den Kugelhahn ablassen.

**Datei:** `designs/components/feinfilter.sc` · **Teilenummer:** T55 · **Revision:** B · **Bezugspunkt:** Mitte der Standflaeche am Boden (Fussplatten-Unterkante z 0); X Laengsachse (Einlauf -X, Auslauf +X), Y Tiefe (Ablass -Y), Z hoch

**Anzahl (Instanzen):** 2 (Quelle: data/leitungsnetz.json: Knoten feinfilter_1 (Linie 1) und feinfilter_2 (Linie 2); layout.json kennt das Bauteil nicht)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `tank_l` | 630 | mm | [E] Korbflansch + 2 x 3 mm Spalt + 2 x Wand |
| `tank_w` | 440 | mm | [E] Korbflansch + 2 x 3 mm Spalt + 2 x Wand |
| `tank_h` | 610 | mm | [E] Einlaufrohr-Oberkante + 6 mm, aufgerundet auf 10 mm |
| `wall` | 10 | mm | [E] PP-Platte 10 mm (W31: 5 mm): Behaelter jetzt 620 x 430 x 610; Wandbiegung bei 0,5 m Wasserhoehe (5 kPa) ca. 5 MPa ohne Rippen; reale Behaelter mit Rippen/Rahmen |
| `foot_h` | 250 | mm | [A] Standhoehe Behaelterunterkante: Eimer (ca. 220 mm) unter den Ablass-Kugelhahn und Gefaelle zur Pumpen-Saugseite; Hoehenlage Montage M10 |
| `leg` | 40 | mm | [A] Vierkantrohr 40 x 40 x 3 verzinkt: Standrahmen traegt ca. 200 kg gefuellt |
| `leg_wall` | 3 | mm | [A] |
| `plate` | 80 | mm | [A] Fussplatte 80 x 80 |
| `plate_t` | 6 | mm | [A] |
| `brace_z` | 110 | mm | [A] Mitte der unteren Querstege ueber dem Boden |
| `bar_dx` | 125 | mm | [E] Raster der Auflagestege: Spannweite des PP-Bodens <= 125 mm, Biegespannung ca. 2,5 MPa bei 5,5 kPa |
| `ledge_w` | 12 | mm | [A] Auflageleiste PP an der langen Innenwand, traegt den Korbflansch |
| `ledge_t` | 12 | mm | [A] |
| `ledge_z` | 522 | mm | [E] Wand + Ablaufkammer + Korbtiefe - Flanschdicke (Flansch liegt oben auf der Leiste) |
| `basket_l` | 560 | mm | [E] aus Siebflaeche 0.825 m2 = Q 110 l/min / Siebbelastung 8 m/h: wet_frac x 2 x (l + w) x d + l x w, w = 0.65 x l, aufgerundet auf 10 mm |
| `basket_w` | 370 | mm | [E] Korbbreite = Seitenverhaeltnis x Korblaenge, aufgerundet auf 10 mm |
| `basket_d` | 400 | mm | [A] Korbtiefe (Wassertiefe im Korb) |
| `flange_t` | 3 | mm | [A] Edelstahl 1.4301, Flansch 22 mm breit |
| `flange_ring` | 22 | mm | [A] |
| `mesh_t` | 1 | mm | [A] Modellierte Huellendicke des Gewebes; reale Gewebedicke ca. 0,1-0,2 mm |
| `mesh_density` | 0.55 | g/cm3 | [A] Ersatzdichte, damit die Huelle der realen Gewebemasse (ca. 0,5 kg/m2) entspricht; nicht die Werkstoffdichte |
| `rod` | 8 | mm | [A] Edelstahl-Flachstab 8 x 8 als Stuetzrahmen des Gewebes |
| `handle_h` | 40 | mm | [A] Buegelgriff 2 je langer Seite, Edelstahl-Rundstab 8 (Pfosten), 10 (Buegel) |
| `handle_d` | 10 | mm | [A] |
| `handle_dx` | 100 | mm | [A] Pfosten des Buegelgriffs +-100 aus der Mitte |
| `gasket_t` | 3 | mm | [A] EPDM-Flachdichtung auf dem Behaelterrand |
| `lid_t` | 6 | mm | [A] PP-Deckel 6 mm |
| `lid_over` | 4 | mm | [A] Deckelueberstand je Seite |
| `latch_w` | 30 | mm | [A] Spannverschluss: Haken am Behaelter (Bock) und Spannhebel; Handelsteil (Exzenterspanner Edelstahl), Fabrikat offen |
| `latch_t` | 14 | mm | [A] |
| `latch_h` | 24 | mm | [A] |
| `latch_dx` | 205.0 | mm | [E] Spannverschluesse 110 mm vom Behaelterende |
| `inlet_d` | 63 | mm | [Q] W32: Ports DN 63 = Aussendurchmesser d63 der Rohrbibliothek (leitungsteile 63, DN50); v = 110 l/min / 2551 mm2 = 0,72 m/s <= 1,0 m/s Saugseite |
| `inlet_z` | 566.5 | mm | [E] 10 mm Luft ueber dem Korbflansch + Rohrradius |
| `inlet_out` | 60 | mm | [A] Stutzenlaenge aussen |
| `inlet_in` | 100 | mm | [A] Mitte des senkrechten Einlaufrohrs im Korb (x vom Behaeltermittelpunkt) |
| `inlet_down` | 120 | mm | [A] senkrechtes Einlaufrohr ragt 120 mm unter die Einlaufmitte in den Korb |
| `wall_d50` | 2.4 | mm | [Q] data/components/leitungsteile.json sizes 50: Wand 2,4 |
| `wall_d40` | 1.9 | mm | [Q] data/components/leitungsteile.json sizes 40: Wand 1,9 |
| `outlet_d` | 63 | mm | [Q] W32: d63 |
| `outlet_z` | 60.0 | mm | [E] Wand + Radius des Dichtflanschs + 5 mm: Flansch stoesst nicht an den Boden |
| `outlet_out` | 70 | mm | [A] Stutzenlaenge aussen ab Behaelterwand |
| `outlet_collar_d` | 90 | mm | [A] Dichtflansch und Gegenmutter der d63-Durchfuehrung |
| `outlet_collar_t` | 5 | mm | [A] |
| `drain_d` | 40 | mm | [A] Ablassstutzen d40 (= DN32, wie Schlammablass K07 des Absetzers) |
| `drain_z` | 35.0 | mm | [E] Wand + Rohrradius + 5 mm Restwasser-Kante |
| `drain_x` | 225.0 | mm | [E] Ablass 90 mm vom Behaelterende |
| `drain_in` | 5 | mm | [A] Stutzen ragt 5 mm in den Behaelter |
| `drain_stub` | 40 | mm | [A] Stutzenlaenge aussen bis Kugelhahn |
| `valve_d` | 56 | mm | [A] Kugelhahn d40 PVC, Gehaeuse D56, Durchgang 28 (Ersatzform) |
| `valve_l` | 50 | mm | [A] |
| `valve_lever` | 90 | mm | [A] Hebel quer zur Durchflussrichtung = zu |
| `barb_l` | 30 | mm | [A] Schlauchtuelle am Ablass |
| `q_lmin` | 110 |  | [Q] D55/W32: Hauptstrom 110 l/min je Linie (leitungsnetz.json: Pumpen gross 2 x 55 l/min) |
| `sieve_load` | 8 |  | [A] Siebbelastung 8 m/h (benetzte Flaeche): R30 / docs/filter-konzept.md Art 2 nennt keine belegte Auslegungsgroesse (Hersteller-Datenblaetter ungelesen); der Bestand W31 rechnete nur 1,6 m/h bei 12,5 l/min. Bei 4 m/h waere die Siebflaeche doppelt so gross |
| `wet_frac` | 0.85 |  | [A] Anteil der Korb-Seitenflaeche unter Wasser (Wasserstand unter dem Flansch) |
| `basket_ratio` | 0.65 |  | [A] Seitenverhaeltnis Korbbreite / Korblaenge |
| `mesh_um` | 100 |  | [Q] D55/W32: Gewebe <= 100 Mikrometer (R30: 100 Mikrometer = 21 % Schwebstoffe, Variante 60 Mikrometer mit haeufigerer Reinigung); nicht modelliert, Huelle 1 mm |
| `chamber` | 115 | mm | [A] Ablaufkammer unter dem Korb (Hoehe zwischen Behaelterboden und Korbboden): Dichtflansch D90 des Auslaufs passt darunter |
| `flange_gap` | 3 | mm | [A] Spalt Korbflansch zur Behaelterwand je Seite (Entnahme) |
| `inlet_air` | 10 | mm | [A] Luft zwischen Korbflansch und Einlaufrohr |
| `wall_d63` | 3.0 | mm | [Q] data/components/leitungsteile.json sizes 63: Wand 3,0 |
| `wall_d25` | 1.8 | mm | [Q] data/components/leitungsteile.json sizes 25: Wand 1,8 |
| `spray_d` | 25 | mm | [Q] W32: Spuelanschluss d25 (DN20, leitungsteile) |
| `spray_stub` | 40 | mm | [A] Stutzenlaenge aussen bis Kugelhahn |
| `spray_valve_d` | 40 | mm | [A] Kugelhahn d25 PVC, Gehaeuse D40, Durchgang 16 |
| `spray_valve_l` | 40 | mm | [A] |
| `spray_reach` | -120 | mm | [A] Ende des Spritzrohrs in Y (quer ueber den Korb, Mitte -120); das Rohr ist ein Platzhalter fuer die Spritzduesen (nicht modelliert) |
| `spray_x` | 165.0 | mm | [E] Spritzrohr 150 mm vom Behaelterende, rechts der Griffe |
| `spray_z` | 580 | mm | [E] Spritzrohr 30 mm unter dem Rand |
| `bar_n` | 4 |  | [E] Anzahl Auflagestege zwischen den Endringen, damit die Bodenspannweite <= bar_dx bleibt |
| `bar_pitch` | 118.0 | mm | [E] Abstand der Stege (Mitte zu Mitte, gleichmaessig zwischen den Mitten der Endringe, Abstand der Endringe = Laenge - Rohrbreite) |

Gesamt-Box (Messung): X -375.0 bis 385.0, Y -340.0 bis 325.0, Z 0.0 bis 903.0 mm; Koerper: 55.

**Toleranzen / Spiel:** Spalt Korbflansch zur Wand 3 mm je Seite (Entnahme ohne Klemmen); Einlaufrohr 10 mm ueber dem Korbflansch; Korbboden 115 mm ueber dem Behaelterboden; Dichtflansch des Auslaufs (D90) mindestens 15 mm unter dem Korbboden; Pruefung check_feinfilter.py (Masse +-0,5 mm); Rohrgeschwindigkeit d63 (Innen 57 mm): 0.72 m/s (Saugseite <= 1,0).

## Werkstoff und Gewicht

- Werkstoff: PP (Behaelter, Deckel), Edelstahl 1.4301 (Korb, Spannverschluesse), Stahl verzinkt (Standrahmen), PVC-U (Rohre, Kugelhahn), EPDM (Dichtung), Dichte PP 0,91 / Edelstahl 7,9 / Stahl 7,85 / PVC 1,4 / EPDM 1,1 / Gewebe-Ersatzdichte 0,55 g/cm3, Farbe #cfd3d6 (Handbuchwerte, Annahme)
- Volumen (Messung, `solidcraft-cli eval`): 21734.2 cm3 · Masse leer: 40452 g (40.45 kg)
- Gefuellt/in Betrieb: leer 40.5 kg; im Betrieb mit Wasser bis zur Unterkante des Einlaufs (z 785, ca. 135 l) ca. 175 kg [E]; Standrahmen und Untergrund muessen das tragen (Montage). Hoehe gesamt 903 mm (Deckelgriff), Hub zum Herausheben des Korbs ca. 460 mm ueber dem Deckel noetig.

## Querschnitt / Profil

Behaelter PP-Platte 10 mm geschweisst, innen 610 x 420 x 600; 12 x 12 Auflageleisten an den langen Innenwaenden tragen den Korbflansch (Edelstahl 3 mm, 22 mm breit). Korb 560 x 370 x 400: Gewebehuelle mit Stuetzrahmen aus Edelstahl 8 x 8 (4 Eckstaebe, Bodenrahmen). Ablaufkammer unter dem Korb 115 mm hoch. Standrahmen Vierkantrohr 40 x 40 x 3 verzinkt mit Fussplatten 80 x 80 x 6, 4 Auflagestege im Raster 118 mm.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Einlauf (Stutzen links, Winkel in den Korb) | PVC-U d63 (DN50), Wand 3,0 | x -375, y 0, z 816 (Oeffnungsebene aussen, Mitte); senkrechtes Rohr endet bei z 696, x -100 | Hauptstrom 110 l/min tritt ein (vom Pool, Netz K05/K21 neu zu fuehren), Oeffnung zeigt -X |
| Auslauf (Durchfuehrung rechts, unter dem Korb) | PVC-U d63 (DN50), Wand 3,0; Dichtflansch und Gegenmutter D90 | x 385, y 0, z 310 (Oeffnungsebene aussen, Mitte) | Wasser tritt aus zur Saugseite der grossen Pumpen (K06/K22), Oeffnung zeigt +X |
| Ablass mit Kugelhahn (Vorderwand, unten) | PVC-U d40 (DN32), Kugelhahn D56, Schlauchtuelle | x 225, y -340, z 285 (Ende der Tuelle, Mitte) | Wasser tritt aus zum Spuelen/Entleeren, Oeffnung zeigt -Y; Hebel quer = zu |
| Spuelanschluss mit Kugelhahn (Rueckwand, oben) | PVC-U d25 (DN20), Kugelhahn D40, Schlauchtuelle; innen Spritzrohr d25 quer ueber den Korb | x 165, y 325, z 830 (Ende der Tuelle, Mitte) | Spuelwasser tritt ein (Schlauch), Oeffnung zeigt +Y; das Spritzrohr (Duesen nicht modelliert) spuelt den Korb |

## Verbindungen und Befestigungen

- Rohrdurchfuehrungen in der PP-Wand: Auslauf mit Dichtflansch innen (D90 x 5), Gegenmutter aussen (D90 x 5) und Flachdichtung (nicht modelliert); Einlauf, Ablass und Spuelanschluss als PP-Schweissstutzen oder Tankdurchfuehrungen (Hersteller offen) [A]
- Rohre PVC-U nach DIN 8062 (d63 Hauptstrom, d40 Ablass, d25 Spuelen), Anschluss an die Leitungen der Montage ueber Muffe oder Verschraubung (leitungsteile)
- Spannverschluesse: 4 Stueck Edelstahl-Exzenterspanner mit Haken am Behaelter und Bock-Hebel am Deckel (Handelsteil, Fabrikat offen) [A]; Deckel liegt auf EPDM-Flachdichtung 3 mm
- Standrahmen: Vierkantrohr 40 x 40 x 3 geschweisst oder verschraubt (M8), Fussplatten 80 x 80 x 6; der Behaelterboden liegt auf Ring und 4 Auflagestegen (Spannweite <= 125 mm, Biegespannung PP rechnerisch ca. 2,5 MPa bei 5,5 kPa Wasserdruck) [E]; PP-Wand 10 mm: Biegung bei 525 mm Wasserhoehe ca. 5 MPa ohne Rippen, reale Behaelter mit Rippen/Rahmen [E]

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Funktion Feinfilter, Zweck, Reinigung alle 1-2 Wochen | Schritt 3 der Kette | Q | docs/filter-konzept.md Art 2 (FAO 589; SRAC 454), Befund 1 | hoch |
| Anzahl 2 (eine je Linie) | 2 | Q | data/leitungsnetz.json knoten feinfilter_1/2 | hoch |
| Hauptstrom 110 l/min je Linie | 110 l/min | Q | Auftrag W32/D55; R30 Befund 1 (Feinfilter sah nur 11 % des Stroms) | hoch |
| Gewebe <= 100 Mikrometer | 100 Mikrometer | Q | Auftrag W32/D55; R30: Mortensen 2000: 100 Mikrometer = 21 % Schwebstoffe | mittel |
| Siebbelastung 8 m/h | 8 m/h | A | R30 nennt keine belegte Auslegungsgroesse; Bestand W31 rechnete 1,6 m/h bei 12,5 l/min | niedrig |
| Siebflaeche 0,825 m2 (Soll) / gebauter Korb | 0,825 / 0,840 m2 | E | A = Q / Siebbelastung; wet_frac 0,85; aus den gemessenen Korbmassen (check_feinfilter.py) | mittel |
| Ports d63 (Ein-/Auslauf), Spuelanschluss d25 | d63 / d25 | Q | Auftrag W32 (DN 63 = d63 der Rohrbibliothek); leitungsteile.json sizes 63/25 | mittel |
| Behaelter, Korb, Hoehen aus der Siebflaeche abgeleitet | siehe Parameter | E | scripts/workshop/feinfilter.py derive() | mittel |
| Behaelterwand PP 10, Deckel 6, Dichtung EPDM 3 | 10 / 6 / 3 mm | A | Konstruktionspraxis PP-Behaelter (Wand aus Biegeueberschlag) | niedrig |
| Standrahmen 40 x 40 x 3, Auflagesteg-Raster <= 125 | mm | A | Konstruktionspraxis; Boden-Biegespannung ca. 2,5 MPa | niedrig |
| Rohrwand d63 3,0 / d40 1,9 / d25 1,8 | mm | Q | data/components/leitungsteile.json | mittel |
| Dichten PP 0,91 / Edelstahl 7,9 / Stahl 7,85 / PVC 1,4 / EPDM 1,1 / Gewebe 0,55 | g/cm3 | A | Handbuchwerte; Gewebe-Ersatzdichte aus 0,5 kg/m2 Gewebemasse | niedrig |
| Port-Koordinaten (Einlauf, Auslauf, Ablass, Spuelen) | siehe Ports | E | gemessen aus den Stutzen-Boxen (fix_w32_feinfilter_blatt.py) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein Referenzbild (Bauteil fehlt im OBJ); docs/filter-konzept.md Art 2; docs/research/R30.md; data/leitungsnetz.json feinfilter_1/2
- Quelle der Masse: W32 (Hauptstrom 110 l/min, Gewebe <= 100 Mikrometer, Ports d63, Spuelanschluss); docs/research/R30.md, docs/filter-konzept.md Art 2 (Siebbelastung ohne belegte Auslegungsgroesse: [A]); Blatt W31 (Konstruktion); data/leitungsnetz.json feinfilter_1/2; Rohrmasse data/components/leitungsteile.json (d63 Wand 3,0, d40 1,9, d25 1,8)
- Abweichung zum OBJ: Das Bauteil kommt nicht aus dem OBJ; es ist eine Empfehlung der Filteranalyse (R28, R30, D51, D55). W31 hatte 400 x 300 x 500 fuer den Teilstrom 12,5 l/min (Gewebe 150 Mikrometer); W32 bemisst es fuer den Hauptstrom 110 l/min je Linie und Gewebe 100 Mikrometer neu (Behaelter 630 x 440 x 610, Korb 560 x 370 x 400). Das Blatt W32 nennt 'Ports DN 63': gemeint ist wie in W31 der Aussendurchmesser d63 der Rohrbibliothek (DN50); die Netzliste fuehrt K05/K06 noch mit d50 und 12,5 l/min: Orchestrator/Montage ziehen sie nach. Die Siebbelastung 8 m/h ist eine Annahme: R30 fand keine belegte Auslegungsgroesse (Hersteller-Datenblaetter ungelesen); der Bestand aus W31 (1,6 m/h) haette bei 110 l/min 4,1 m2 Sieb verlangt.

## Montage (L4)

1. Standrahmen aufstellen, ausrichten (Wasserwaage), Fussplatten auf tragfaehigem Untergrund befestigen
2. Behaelter auf den Rahmen setzen und gegen Verrutschen sichern
3. Einlauf-, Auslauf-, Ablass- und Spuelstutzen mit den Leitungen verbinden (Einlauf mit Gefaelle vom Pool, Auslauf zur Saugseite der grossen Pumpen, Spuelanschluss mit Schlauch)
4. Siebkorb einsetzen (Flansch auf den Leisten), Deckel mit Dichtung auflegen und die vier Spannverschluesse schliessen
5. Probelauf mit 110 l/min; Wasserstand im Behaelter pruefen (steigt der Spiegel ueber den Einlauf, ist der Korb verstopft: spuelen)

**Werkzeug:** Wasserwaage, Schluessel M8, Rohrschneider, PVC-Kleber, ggf. Kunststoffschweissgeraet

## Stueckliste-Zeile

- Behaelter PP 630 x 440 x 610, Wand 10, mit 2 Auflageleisten, 4 Durchfuehrungen: 1
- Siebkorb Edelstahl (Flansch 604 x 414 x 3, Gewebehuelle 560 x 370 x 400, Gewebe 100 Mikrometer, 4 Eckstaebe, Bodenrahmen, 2 Buegelgriffe): 1
- Deckel PP 638 x 448 x 6 mit Griff: 1, EPDM-Flachdichtung 3 mm: 1, Spannverschluesse Edelstahl: 4
- Einlaufwinkel PVC-U d63: 1, Auslaufrohr PVC-U d63 mit Dichtflansch D90 und Gegenmutter D90: 1
- Ablassstutzen PVC-U d40: 1, Kugelhahn d40: 1, Schlauchtuelle d40: 1
- Spuelstutzen PVC-U d25: 1, Kugelhahn d25: 1, Schlauchtuelle d25: 1, Spritzrohr PVC-U d25: 1
- Standrahmen: 4 Beine, 4 Ringstege, 4 Auflagestege, 2 Querstege (Vierkantrohr 40 x 40 x 3), 4 Fussplatten 80 x 80 x 6
- Gesamt: 2 Stueck (Linie 1 und 2)

## Alternative lokale Fertigung

Handelsueblich: Beutel-/Taschenfilter-Gehaeuse oder Siebkorbfilter fuer Teichtechnik (Edelstahl, 100 Mikrometer Filterbeutel) statt Eigenbau; Standrahmen aus Kantholz.

## Renders

- `renders/components/feinfilter/feinfilter-01-iso.png`
- `renders/components/feinfilter/feinfilter-02-vorn.png`
- `renders/components/feinfilter/feinfilter-03-einlauf.png`
- `renders/components/feinfilter/feinfilter-04-ablass.png`
- `renders/components/feinfilter/feinfilter-05-schnitt.png`

## Pruefung

- Gauntlet-Urteil: kein Pruefer-Lauf (Auftrag W32: Selbstcheck)
- scripts/workshop/check_feinfilter.py: Ergebnis in renders/components/feinfilter/check.txt (Siebflaeche aus gemessenem Korb gegen Q / Siebbelastung, Masse, Wand, Korb im Behaelter, Ports, Hoehenfolge, Spuelanschluss, Rohrgeschwindigkeit, Standrahmen, Interferenz)
- Kein Bild-Kritiker und kein Spec-Pruefer (Auftrag W32)

## Offene Fragen

- Siebbelastung 8 m/h ist [A]: R30 nennt keine belegte Auslegungsgroesse; Hersteller-Datenblatt des 100-Mikrometer-Gewebes und die Standzeit bis zum Verstopfen offen (bei 4 m/h waere die Siebflaeche doppelt so gross, bei 12 m/h zwei Drittel)
- Netzliste data/leitungsnetz.json fuehrt K05/K06 und K21/K22 noch mit d50 und 12,5 l/min; der Feinfilter sitzt jetzt im Hauptstrom d63 mit 110 l/min je Linie (Orchestrator/Montage M10: Strom vor den grossen Pumpen, Seitenablauf des Pools muss durch den Filter)
- Platz: Behaelter 630 x 440 (mit Stutzen ca. 770 x 680) und 903 mm hoch plus Hub zum Herausheben des Korbs; Hoehe gegen Pool-Spiegel (Z 515) und Pumpen-Saugseite prueft die Montage; foot_h 250 anpassbar
- Kein Notueberlauf/Bypass: verstopft der Korb, steigt der Wasserstand ueber den Einlauf und staut zum Pool; Ueberlauf in den Pool oder Bypass ist Sache der Hydraulik
- Gewebe-Maschenweite 100 Mikrometer ist ein Hinweis (nicht modelliert); die Huelle ist 1 mm mit Ersatzdichte 0,55; Gewebe-Fabrikat offen
- Spannverschluesse, Durchfuehrungen, Kugelhaehne und das Spritzrohr (Duesen) sind Ersatzformen (Handelsteile, Fabrikat offen)
- PP-Wand 10 mm und Auflagestege sind eine Ueberschlagsrechnung (Biegung), kein Festigkeitsnachweis; reale Behaelter mit Rippen
- Das Bauteil steht nicht in layout.json: Montage setzt die zwei Instanzen nach leitungsnetz.json

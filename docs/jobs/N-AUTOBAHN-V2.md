# N-AUTOBAHN-V2: Wasserautobahn (Ring B2) wirklich bauen, mit Stelzen, Schlauch-Fallleitungen und Schlauch-Ruecklauf (W78)

Planer 05.11.2026 (Opus 5.5). Paket: `docs/packages/n-autobahn-v2.md`. Ersetzt die Schritte R1 und R2 aus `docs/jobs/N-VARIANTEN.md` Abschnitt 4; alles andere aus N-VARIANTEN (Schalter, Pfade, V1a, V1b, VV, V2, O1, P1 bis P5) gilt weiter. [Q] Quelle im Repo · [E] eigene Rechnung · [A] Annahme dieses Blatts. Jede Zahl [E] kommt aus `python -X utf8 scripts/n_autobahn_rechnung.py` (nur lesend, Abschnittsnummer in Klammern). Z relativ zum Innenboden, absolut = relativ + 400.

**Problem:** Die Wasserautobahn existiert bisher nur als Bauteile (V2, 721b607) und als Rechnung in R47c. Im Modell fehlt sie ganz. Der alte Plan R1/R2 kannte weder Stelzen, die zwischen Tischen und Beeten stehen koennen, noch Schlauch-Abzweige, noch einen Schlauch-Ruecklauf. Ausserdem fehlte eine faire Zahlentabelle A+ gegen Autobahn.
**Intent:** Ben und Leon sollen beide Kreislaeufe im Viewer sehen und umschalten koennen, und zwar so, wie sie gebaut wuerden: A+ als Empfehlung, die Autobahn als Ring auf Stelzen mit frei haengenden Schlaeuchen wie Druckluftschlaeuche in einer Fabrik. Die Empfehlung soll auf gemessenen Zahlen stehen, nicht auf Gewohnheit.
**Ziel (ein Satz):** `sh scripts/build.sh 5 <runde> ring_b2` baut `designs/dome-ring_b2.sc` mit Ring, 10 Stuetzpunkten, 18 Auslegern, 38 Schlauch-Fallleitungen, Einspeisung je Linie und Schlauch-Ruecklauf; die Pruefpunkte in Abschnitt 6 sind fuer beide Varianten gruen; Abschnitt 5 traegt die Empfehlung mit Zahlen.

## Aktualitaetspruefung (W44), 05.11.2026
Ergebnis: **angepasst** (Plan gilt als freigegeben).
1. Roadmap: Kein eigener Eintrag `N-AUTOBAHN-V2`. Der Eintrag `N-VARIANTEN` (Status laeuft, Reihenfolge 9.5) deckt den Inhalt ab. Der Orchestrator legt den Eintrag an.
2. Entscheidungen: D84 (Technik innen) aendert die Biofilter-Lage NICHT. `Tank_gross:1` steht bei r 3385 / Az -5, `Tank_gross_t3:1` bei r 3365 / Az -98 [E, `scripts/dome-script.json`]. Die Technik-Turm-Planung N-TECHNIK-INNEN betrifft nur Geblaese, Verteiler und Aktivkohle. D85 (lebensmittelecht) gilt fuer alle Schlaeuche, Kupplungen und den Ring (Abschnitt 3). D86 (Ordnung v2, Schlaeuche erlaubt) ist die Grundlage fuer die Schlauchfuehrung. D87 betrifft das Thema nicht.
3. Leitungsordnung v2 ist **noch nicht gepusht**: Der letzte Commit an `docs/leitungsordnung.md` ist acc89b7, die Systemreview-Sitzung arbeitet noch. Dieses Blatt nennt deshalb in Abschnitt 2.6 die Ausnahmen, die die Autobahn von v1 braucht. Pflicht fuer die Montage: Vor dem Start `git log -3 -- docs/leitungsordnung.md` pruefen. Ist v2 da, gelten ihre Regeln, und die Ausnahmen aus 2.6 werden nur uebernommen, wenn v2 sie nicht ohnehin erlaubt.
4. Netz-Delta O1 (K60 bis K75) steht noch nicht in `data/leitungsnetz.json` (hoechste Kante K59). Abschnitt 2.7 nennt die Aenderungen gegen N-VARIANTEN 2.6.
5. V2-Bauteile liegen vor und bleiben gueltig (`docs/parts/ring_b2.md`): Pegelschacht, Ringstuetze, Entluefter, Ring-Abzweig d40/d32. Neu ist nur, was 2.2 bis 2.5 dazu verlangen.

## 1. Lage im Modell (gemessen)
1. Die Zonen sind Zehneck-Ringe [Q `docs/parts/nft_tisch.md` Tischmitte ap_c]: Innentische ap 1864 (10 Stueck), Mittelzone ap 3277 (6 Mitteltische mit Innenbeeten darunter), Aussenzone ap 4874 (8 Aussentische mit Aussenbeeten darunter). Gaenge dazwischen: A 600 mm (innen/Mitte), B 500 mm (Mitte/aussen) [Q D29].
2. Der Ring liegt als Zehneck auf der Mittellinie der Mittelzone: Eckradius 3446 mm, Seite 2130 mm, Umfang 21,30 m [E Abschn. 2]. Damit liegt er **nirgends ueber einem Gang**, sondern ueber den Mitteltischen und den Technik-Sektoren.
3. Beide Biofilter liegen direkt unter dem Ring (Seite -18/18 bzw. -90/-126). Die Steigleitung ist dadurch kurz: 2,08 m d63 je Linie [E Abschn. 2].
4. Jeder Tisch hat seinen Zulauf am -X-Ende, also an der Sektorgrenze im Uhrzeigersinn [Q nft_tisch.md]. Alle 38 Abnehmer haengen deshalb an den 10 Ringecken (Az -162, -126, -90, -54, -18, 18, 54, 90, 126, 162).
5. Linienzuordnung [A, symmetrisch nach D67]: Linie 1 = Sektoren 0, 36, 72, 108 plus Innentisch -36; Linie 2 = Sektoren 144, 180, -144, -108 plus Innentisch -72. Ergebnis: je Linie 7 Beete und 12 Tische [E Abschn. 1].

## 2. Bauweise (fachlich festgelegt)

### 2.1 Wasserweg je Linie
Biofilter-Ueberlauf (Z 1570, gebaut) -> K10/K26 frei fallend -> **Pegelschacht auf Podest** (Fassboden Z 950, Pegel EIN Z 1290) -> 2 Booster `pumpe_gross` parallel auf der Plattform Z 570, je mit Rueckschlagventil -> **Steigleitung d63** -> **Ring d75** auf 4 Seiten der eigenen Linie -> an jeder Ecke Abzweig -> **Schlauch-Fallleitung** zum Abnehmer -> Ruecklauf -> Pool. Ring-Ende je Linie mit Kugelhahn d63 als Ueberschuss in den Ruecklauf (ersetzt K13/K29), Tiefpunkt mit Entleerungshahn, Hochpunkt mit `entluefter_d75`.

**Warum Podest:** Steht der Pegelschacht am Boden, braucht jeder Booster 2,25 m Foerderhoehe; die 4 Booster ziehen dann 324 W statt 187 W (eta 25 %) [E Abschn. 5]. Das Podest kostet ein Stahlteil (2.5 Teil WA7) und spart 137 W Dauerlast. Pruefen muss die Werkstatt, ob K10 mit Gefaelle von Z 1570 in den Fassdeckel (Fassboden 950 + 575 = Z 1525) passt; reicht das nicht, sinkt das Podest, und die Leistung steigt entsprechend.

### 2.2 Ring und Kupplungsstrecken
1. Ring als **geschlossenes Zehneck** (Bens Bild). Je Linie 4 Seiten = 8,52 m. Die zwei Seiten zwischen den Linien (Az 90 bis 126 und -54 bis -90, zusammen 4,26 m) sind **Kupplungsstrecken** mit je einem Kugelhahn d63, im Betrieb **geschlossen**. Geoeffnet kann eine Linie bei Booster-Ausfall die NFT-Tische der anderen mitspeisen: 2 x 38 l/min NFT = 76 l/min < 110 l/min eines Booster-Paars [Q K12/K28]. Leckage nimmt trotzdem nur eine Linie (Hahn zu), wie R47 Abschnitt 1 verlangt.
2. Werkstoff [A, Werkstatt prueft mit zwei Quellen]: **PE-100 d75 SDR17, Trinkwasser-Zulassung** (D85), an den Ecken kalt gebogen (36 Grad). Grund: Fuer 36 Grad gibt es kein PVC-Formteil (Bibliothek und Leitungsordnung R2 kennen nur 45 und 90 Grad). Faellt PE durch (Biegeradius, Bezug in Europa D76), dann PVC-U d75 mit zwei 18-Grad-Gehrungen je Ecke als Klebebogen oder Ring-Ecke `ring_ecke_d75` (Teil WA4).
3. Traeger: Die freie Spannweite zwischen zwei Ecken betraegt 2,13 m, mehr als die 1,65 m fuer d75 [Q R47 Abschnitt 1]. Der Ring liegt deshalb auf einer **Montageschiene 41 x 41** (Installationsstandard) von Ecke zu Ecke, mit einer Rohrschelle d75 hoechstens alle 1,0 m (Leitungsordnung R6): 22 Schellen [E Abschn. 2]. `lt_klemme_d75` fehlt in der Bibliothek [Q leitungsordnung.md "Fehlende Halter-Teile"], Teil WA3.
4. Hoehe: Unterkante Z 2100, Achse 2145, Hochpunkt etwa 2190 [Q N-VARIANTEN 2.1]; nichts haengt unter dem Rohr ausser den Fallschlaeuchen an den Ecken.

### 2.3 Stuetzpunkte (Stelzen)
10 Stuetzpunkte, je einer an jeder Ecke, nie im Gang [E Abschn. 2]:
1. **7 Portal-Joche** an den Ecken -162, -126, 18, 54, 90, 126, 162. Dort steht mindestens ein Mitteltisch-Portalbock (Beine 40 x 40 x 3, radial bei ap 2731 und 3823 [Q nft_tisch.md Zeile 92]). Das Joch verlaengert beide Beine des eckseitigen Portals auf Z 2100 und traegt oben einen Querriegel mit Schienenauflage und den zwei Ausleger-Anschluessen. Befestigung am Tischbein ist nach Leitungsordnung R7 erlaubt. Grund gegen eine eigene Stelze dort: Zwischen benachbarten Innenbeeten bleiben nur etwa 100 mm (Gangkarte: Beet_innen_933:2 x :3, Weite 100 mm bei -161 Grad [Q `docs/walkway-map.md`]); eine Fussplatte 200 x 200 passt nicht.
2. **3 eigene Stelzen** an den Ecken -90, -54, -18 (Technik-Sektoren, kein Mitteltisch): Bauteil `ringstuetze_d75` (T95), erweitert um Ausleger-Anschluss (Teil WA2b). Standort je Ecke darf um hoechstens 300 mm entlang der Ringseite wandern, wenn Tank, Pumpe oder Bedienzone (D70, 650 mm vor der Front) im Weg sind; dann waechst die Schiene, nicht die Spannweite.
3. Statik: R47 nannte Aufsaetze auf Tischbeine "nicht empfohlen" wegen Kragarm-Wirkung. Das Joch ist kein Kragarm, sondern ein verlaengerter Rahmen mit Querriegel; die Last ist klein (Ring voll 4,74 kg/m [Q R47] mal 2,13 m = 10 kg je Ecke plus Schlaeuche). Die Werkstatt rechnet Kopfverschiebung und Kippen wie bei T95 und gibt den Grenzwert an; N-STATIK prueft spaeter.

### 2.4 Ausleger und Schlauch-Fallleitungen
1. **Mittelzone (12 Abnehmer: 6 Mitteltische, 6 Innenbeete):** Der Schlauch faellt direkt an der Ringecke senkrecht zum Tisch-Zulaufverteiler bzw. zum Beet-Tropfrohr [E Abschn. 3].
2. **Innen- und Aussenzone (26 Abnehmer):** Radiale **Ausleger** am Joch oder an der Stelze, Oberkante Ring-Achse: 10 nach innen je 1,49 m, 8 nach aussen je 1,68 m [E Abschn. 3]. Die Schlaeuche liegen auf dem Ausleger in Haltern hoechstens alle 400 mm (R6 Schlauch), zusammen 80 Halterplaetze, und queren die Gaenge A und B oberhalb Z 2100. Am Auslegerende faellt der Schlauch frei zum Abnehmer, wie ein Druckluftschlauch an einer Werkbank.
3. Je Abnehmer: oben Ring-Abzweig (V2-Teil `ring_abzweig_d40` fuer Beete, `_d32` fuer Tische, Hahn dort = Absperrung fuer Reparatur) -> Schlauchtuelle -> Schlauch **lebensmittelecht, lichtdicht (schwarz, gegen Algen), UV-fest** -> unten **Kugelhahn als Regler auf Greifhoehe** -> **Schnellkupplung** -> Abnehmer. Beete: Schlauch ID25, Tische ID16 [Q `lt_schlauchschelle_id16/_id25` vorhanden].
4. Schlauchmengen: ID25 38,6 m, ID16 60,8 m, je Abnehmer 1,35 bis 3,47 m einschliesslich 300 mm Schlaufe [E Abschn. 3].
5. Durchhang: Ein frei haengender Schlauch darf zwischen Ring und Auslegerende nicht unter Z 2100 sinken (Gang). Nur der letzte senkrechte Fall ab Auslegerende haengt frei.

### 2.5 Ruecklauf als Schlauch-Autobahn (D86)
1. **NFT-Ruecklauf (K15/K31) als Schlauch d50 in einer Tragrinne:** Je Zone und Linie ein Sammelschlauch unter den Tischreihen (Korridor KT, Kabelrinne 100 mm am Tischbein, R7), Gefaelle 1 %, dann je Zone eine Radiale zur Poolkrone (Halbring K16/K32 bleibt starr, KW). Innentische laufen auf kurzem Weg (0,5 m) direkt in den Pool. Summe 53,2 m Schlauch d50 [E Abschn. 4]. Gefaellebedarf des laengsten Wegs 128 mm, verfuegbar mindestens 225 mm (Rinnenende Z 955 bis Poolkrone Z 650 bis 730) [E Abschn. 4].
2. **Gangquerung des Ruecklaufs:** Schwerkraft kann einen Gang nicht ueberkopf queren (Rinnenende Z 955 liegt unter Z 2100). Deshalb **6 Bodenrinnen mit Gitterrost**, buendig, zusammen 7,0 m [E Abschn. 4]: offen und begehbar statt vergraben (W75, W79). Das gilt physikalisch genauso fuer A+; ob A+ sie uebernimmt, entscheidet die Leitungsordnung v2.
3. **Beet-Ruecklauf (K14/K30) bleibt unter Flur bis zum Beet-Sumpf.** Grund: Der Beetablauf liegt 615 mm unter dem Poolspiegel [Q R47 Gesamturteil 7]; das kann kein Schlauch aendern. Ab der Sumpfpumpe (K58/K59, Druck) darf der Weg als Schlauch d40 der Ruecklauf-Autobahn folgen.
4. Kennzeichen in `data/leitungstrassen.json`: Feld `varianten: ["ring_b2"]` an den Schlauch-Trassen; die starren A+-Fassungen von K15/K31 tragen `["a_plus"]`. Erklaert v2 den Schlauch-Ruecklauf fuer beide Varianten, entfaellt das Feld.

### 2.6 Ausnahmen gegen Leitungsordnung v1 (bis v2 da ist)
1. Neuer Korridor **KR (Ring)**: Z 2100 bis 2300 relativ (absolut 2500 bis 2700), nur auf eigenen Stuetzpunkten und Tischbeinen. v1 sperrt "ueber Kopf ab Z 2500 absolut" wegen der Statik der **Kuppel**; die Autobahn befestigt nichts an Streben, Knoten, Haut oder Plane (R7 bleibt).
2. R1/R2 im Korridor KR: Ringseiten folgen dem Zehneck (Rahmen = Sektor), Ecken 36 Grad.
3. Schlauch: R1 (Richtung) und R3 bis R5 (Boegen) gelten nicht fuer Schlauch. Es gelten R6 (Halter <= 400 mm, ausser im letzten freien Fall <= 1,5 m) und R9 (kein Durchhang unter Z 2100 relativ im Gang).
4. Bodenrinne mit Rost ist eine zulaessige Gangquerung (heute nur Graben KG).

### 2.7 Netz-Delta (Vorschlag an den Orchestrator, er besitzt `data/leitungsnetz.json`)
Gegen N-VARIANTEN 2.6 aendert sich:
1. K64/K72 (Ring -> Beete) und K65/K73 (Ring -> NFT): Medium Wasser, Ausfuehrung **Schlauch ID25 / ID16 je Abnehmer**, Abzweig d40/d32.
2. K66/K74 (Ring-Ende -> Ruecklauf) d63 statt d50; K67/K75 (Notueberlauf) d63 [Q V2-Befund 721b607].
3. Neu **K76** Kupplungsstrecke Ring 1 <-> Ring 2, d75, Soll 0 l/min, Hahn normal geschlossen (zwei Strecken, eine Kante, Feld `strecken: 2`).
4. Neu Kabel: Schwimmer x 2 und Booster x 4 wie 2.6; die Rueckschlagventile brauchen kein Kabel.

## 3. Fehlende Bauteile (Werkstatt)
Vorhanden und weiter genutzt: `pegelschacht` (T94), `ringstuetze_d75` (T95), `entluefter_d75` (T96), `ring_abzweig_d40/_d32` (T97), `pumpe_gross`, `lt_kugelhahn_d63`, `lt_schlauchschelle_id16/_id25`. Neu:

| Teil | Inhalt | Pruefung (im Check) |
|---|---|---|
| WA1 `portal_joch_mitte` | Aufsatz auf den Portalbock des Mitteltischs: 2 Beinverlaengerungen 40 x 40 x 3 bis Z 2100, Querriegel mit Schienenauflage, 2 Ausleger-Flansche (innen, aussen); Klemmanschluss am Bestandsbein, kein Schweissen am Tisch | Ports Schiene/Ausleger; Interferenz 0 mit `nft_tisch` Typ mitte und `ibc_beet` innen_933; Kopfverschiebung <= L/300 bei Ring voll + 2 Auslegern voll; Kippen |
| WA2 `ausleger_schlauch` (Laenge parametrisch 1490 / 1680) und WA2b Ausleger-Flansch an `ringstuetze_d75` Rev. B | Kragarm 40 x 40 x 3 mit Kopfband, Halterraster 400 mm, Endbuegel fuer den freien Fall | Biegespannung, Durchbiegung Ende <= 10 mm, Halterabstand <= 400, Unterkante >= Z 2100 |
| WA3 `montageschiene_41` + `lt_klemme_d75` | Schiene 41 x 41, Laenge 2130 (Ecke zu Ecke); Rohrschelle d75 auf Schiene | Durchbiegung bei 2,13 m und 6 kg/m [A]; Schelle umschliesst d75 |
| WA4 `ring_ecke_d75` | 36-Grad-Ecke: PE kalt gebogen (Radius nach Herstellerangabe, zwei Quellen) oder PVC-Ersatz aus zwei 18-Grad-Gehrungen | Biegeradius belegt; Ports d75 |
| WA5 `schlauch_fall_id16` / `_id25` | Baugruppe: Tuelle oben, Schlauch als Polylinie (Ausleger-Lage plus freier Fall plus Schlaufe), Kugelhahn unten, Schnellkupplung, Anschluss Tisch-Zulaufverteiler bzw. Tropfrohr; Laenge aus `data/components/ring_b2_teile.json` je Abnehmer | Laenge = Rechnung +- 50 mm; Biegeradius Schlauch; Kupplung lebensmittelecht (D85) im Teileblatt belegt |
| WA6 `lt_schnellkupplung_id16/_id25` | Kupplungspaar (Bibliothek), lebensmittelechter Kunststoff oder Edelstahl, kein Messing mit Blei | Ports; Werkstoffangabe mit Quelle |
| WA7 `pegelschacht_podest` | Stahlgestell, Fassboden Z 950, Fussplatten | K10-Gefaelle >= 1 % zum Fasszulauf; Interferenz mit Biofilter, Pumpen, Bedienzone 0 |
| WA8 `lt_rsv_d50` | Rueckschlagventil d50 hinter jedem Booster (heute nur d20/d25/d40) | Ports, Baulaenge aus Herstellerblatt |
| WA9 `ruecklauf_rinne` + `bodenrinne_rost` + `lt_schlauch_d50` | Kabelrinne 100 mm am Tischbein mit Gefaelle-Haltern; buendige Bodenrinne mit Gitterrost fuer 500/600-mm-Gang; Schlauch d50 lebensmittelecht | Gefaelle >= 1 % moeglich; Rost-Oberkante = Boden +- 2 mm |

Ablauf: zwei Werkstatt-Sitzungen parallel, weil sich die Dateien nicht ueberschneiden: **WA-T Tragwerk** (WA1 bis WA4, WA7) und **WA-S Schlauch** (WA5, WA6, WA8, WA9). Jede liefert Teileblatt in `docs/parts/autobahn.md` (je Sitzung ein eigener Abschnitt), Check-Skript `scripts/workshop/check_autobahn_<t|s>.py`, Teiledaten in `data/components/autobahn_teile.json`, Bild in `renders/components/autobahn/`.

## 4. Montage-Runden (ersetzt R1 und R2)
Nur EINE Sitzung baut das Gesamtmodell (D80). Beide Montagen bauen nur `ring_b2` und lassen A+ unveraendert (P1 aus N-VARIANTEN). Dateien: `scripts/gen_dome.py` (nur `ring_b2()`), neu `scripts/trassen_ring.py`, `data/leitungstrassen.json` (nur Eintraege `ring_b2`), `designs/dome-ring_b2.sc`, `renders/ring_b2/`, `docs/loop-state.md` (Abschnitt Ring B2).

**R1 Tragwerk, Ring und Einspeisung (beide Linien)**, nach WA-T:
1. Runde a: 7 Joche und 3 Stelzen setzen; `check_walkways.py --variante ring_b2` (keine neue rote Engstelle) und Interferenz gegen Tische, Beete, Tanks, Pumpen.
2. Runde b: Schienen, Ring mit Ecken und 22 Schellen, 2 Entluefter, 2 Entleerungshaehne, 2 Kupplungshaehne.
3. Runde c: Pegelschacht auf Podest, 4 Booster mit Rueckschlagventil, Steigleitungen, Ring-Ende-Haehne, Notueberlauf; Kabel Schwimmer und Booster.
4. Runde d: Bau `sh scripts/build.sh 5 <runde> ring_b2`; `check_leitungen.py --variante ring_b2`; `check_netz.py --variante ring_b2` (nach O1); Bilder Draufsicht und Schnitt durch eine Ecke.

**R2 Schlaeuche, Ausleger und Ruecklauf**, nach R1 und WA-S:
1. Runde a: 18 Ausleger setzen; Interferenz gegen Streben und Haut, besonders aussen (Kuppel-Innenhoehe bei r 5,1 m nur grob 2,6 m relativ [E grob aus Huellenlagen], also knapp).
2. Runde b: 38 Fallleitungen aus `trassen_ring.py` (Koordinaten aus Instanzmatrizen und Port-Tabellen, nie von Hand), Halter am Ausleger.
3. Runde c: Ruecklauf-Rinnen, Schlauch d50, 6 Bodenrinnen; K15/K31-A+-Eintraege `["a_plus"]` markieren, falls noch nicht geschehen.
4. Runde d: Bau, alle Pruefungen aus Abschnitt 6, `check_walkways_voll.py --variante ring_b2`, Viewer-Export `viewer/export_model.py --variante ring_b2`, Screenshots beider Varianten im Browser (`docs/ui-standard.md`).

Reihenfolge-Empfehlung an den Orchestrator: WA-T und WA-S sofort parallel. R1/R2 direkt nach dem Push der Leitungsordnung v2, im Slot vor M10-S3, weil M10-S3 ebenfalls auf v2 wartet und R1/R2 kein A+-Teil aendern. Danach baut CHECK beide Varianten neu (etwa 3 min je Bau, `docs/jobs/N-VARIANTEN.md` 1.6).

## 5. Vergleich A+ gegen Wasserautobahn (Zulauf-Verteilung, nach dem Biofilter)
Gleich in beiden und deshalb nicht in der Tabelle: Pool, Heber, Feinfilter, Hauptpumpen, Biofilter, Absetzerkreis, Notbypass, Beet-Ruecklauf bis Sumpf, 30,3 m vergrabenes Rohr vor dem Verteiler bzw. Pegelschacht [Q R47b 6.0], je Abnehmer ein Abzweig mit Hahn.

| Kennzahl | A+ | Wasserautobahn | Herkunft |
|---|---|---|---|
| Rohr Zulauf-Verteilung | 80,3 m (d40 58,9 + d32 21,4) | Ring 21,3 m d75 + Steig 4,2 m d63 = 25,5 m | [Q R47 Abschn. 4 (`r47_rechnung.py`)], [E Abschn. 2] |
| Schlauch Zulauf | 0 | 99,4 m (ID25 38,6 + ID16 60,8) | [E Abschn. 3] |
| Ruecklauf NFT | 32,0 m Rohr d63 starr | 53,2 m Schlauch d50 in Rinne | [Q R47], [E Abschn. 4] |
| Pumpenleistung gesamt, eta 25 % | 430 W, 10,3 kWh/Tag | 617 W, 14,8 kWh/Tag (Booster bei eta 18 %: 690 W); mit Schacht am Boden 754 W | [Q R47c 7.5], [E Abschn. 5] |
| Pumpstufen nach dem Biofilter | 0 (Schwerkraft) | 1 (2 Booster je Linie) | [Q R47c 7.5] |
| Teilezahl Zulauf (Stueck, ohne Meterware) | 267 | 540 | [E Abschn. 7] |
| Kosten der Unterschiede (Einkaufsliste brutto) | Basis | mindestens +2.769 EUR, 6 Posten ohne Preis (Schlaeuche, Fass, Schiene, Kupplungen, Verteiler d50) | [E Abschn. 6] |
| Grabenmeter Zulauf | 4,6 m gebuendelt bis 29,6 m je Abnehmer | 0 m | [E Abschn. 8] |
| Gangquerung Ruecklauf | Graben (wie heute) oder Bodenrinne, falls v2 sie erlaubt | 6 Bodenrinnen, 7,0 m, offen | [E Abschn. 4] |
| Wartung ueber Kopf (Leiter) | 0 Stellen | 38 Abzweig-Koepfe, 2 Entluefter, 21,3 m Ring | [E Abschn. 9] |
| Wartung am Boden | Verteiler je Linie, Haehne an einer Stelle | Regler unten am Abnehmer, Schnellkupplung: Abnehmer ohne Werkzeug abtrennbar | Abschn. 2.4 |
| Aktive Glieder nach dem Biofilter je Linie | 0 | 2 Booster, 1 Schwimmerschalter, 2 Rueckschlagventile | [E Abschn. 9] |
| Ausfall einer Booster-Paarung | – | Ring der Linie steht; Kupplungshahn auf: NFT der Linie aus der anderen weiter (76 < 110 l/min) | Abschn. 2.2 |
| Schlauchverbindungen unter Druck ueber Pflanzen | 0 | 76 | [E Abschn. 9] |
| Sichtbarkeit und Umbau | Leitungen unter Tischen und im Boden | alles sichtbar; Tisch oder Beet umsetzen = Kupplung loesen, Schlauch umhaengen | Abschn. 2.4 |

**Empfehlung: A+ bleibt die Empfehlung fuer den Bau. Die Autobahn wird als vollwertige Anschauungs-Variante gebaut.** Die Begruendung in fuenf Punkten:
1. **Physik:** Der Biofilter-Ueberlauf liegt bei Z 1570, die Gaenge muessen bis Z 2100 frei bleiben. Wasser, das einen Gang ueberkopf queren soll, muss also gepumpt werden. A+ quert stattdessen unten und braucht deshalb 4,6 bis 29,6 m Graben. Die Autobahn spart diesen Graben, bezahlt ihn aber mit einer Pumpstufe: +187 W Dauerlast, also +4,5 kWh am Tag.
2. **Bens Mass W76** (selbstregulierend, so wenig Teile wie noetig): A+ hat nach dem Biofilter kein aktives Glied, die Autobahn hat je Linie zwei Booster und einen Schwimmerschalter. Die Teilezahl der Verteilung steigt von 267 auf 540, die Kosten um mindestens 2.769 EUR.
3. **Wartbarkeit (Bens Sorge R47b):** Die 30,3 m vergrabenes Rohr bleiben in beiden Varianten gleich. Die Autobahn macht nur den kleineren Teil (Zulauf hinter dem Biofilter) sichtbar und bringt dafuer 40 Stellen, an denen man auf die Leiter muss.
4. **Was die Autobahn wirklich besser kann:** Kein Zulauf-Graben, Regler auf Greifhoehe am Abnehmer, Tische und Beete ohne Werkzeug abkoppelbar, eine Linie kann die andere stuetzen. Das sind echte Vorteile fuer einen Versuchs- und Lehrdom, in dem oft umgebaut wird.
5. **Was die Empfehlung umkehren wuerde:** (a) Die Gangkarte zeigt, dass die A+-Graeben gebuendelt nicht gehen und je Abnehmer gegraben werden muss (29,6 m). (b) Der Dom wird vor allem als wechselnder Versuchsaufbau genutzt. (c) Strom kostet am Standort wenig. Liegt einer davon vor, ist die Autobahn vertretbar; liegen (a) und (b) vor, ist sie besser.

Die Zahlen in dieser Tabelle sind Rechnungen. Nach R2 ersetzt die Montage die Meter durch Messwerte aus den Trassen (`system_specs.py --variante ring_b2`, Block `kreislauf`) und traegt sie hier nach.

## 6. Pruefpunkte (fremd nachmessbar)
**Beide Varianten:**
1. **A+ unberuehrt:** `python -X utf8 scripts/check_varianten.py --a-plus-gleich` Exit 0; SHA-256 von `scripts/dome-script.json` vor und nach R1/R2 gleich (aus `python -X utf8 scripts/gen_dome.py 5 <scratch>/a.json`).
2. **Ordnung:** `python -X utf8 scripts/check_leitungsordnung.py` (bzw. v2-Pruefung) fuer `a_plus` und `ring_b2`: 0 Verstoesse ausser den in 2.6 benannten Ausnahmen, jede mit Trassen-Feld gekennzeichnet.

**Wasserautobahn:**
3. **Vollstaendig:** `check_varianten.py --abzweige` (oder Zaehlung in `scripts/dome-script-ring_b2.json`): 38 Fallleitungen (je Linie 7 Beete, 12 Tische), 10 Stuetzpunkte (7 Joche, 3 Stelzen), 18 Ausleger, 4 Booster, 2 Pegelschaechte auf Podest, 2 Entluefter, 2 Kupplungshaehne, 6 Bodenrinnen.
4. **Gaenge frei:** `check_walkways_voll.py --variante ring_b2`: keine neue rote Engstelle gegen A+; Ring- und Schlauch-Unterkante im Gang >= Z 2100 relativ (Skript misst die tiefste Schlauchkoordinate je Ausleger); kein Stuetzpunkt in einer Gangflaeche.
5. **Kollision und Masse:** Interferenz Joch, Stelze, Ausleger, Ring, Schlaeuche gegen Streben, Haut, Tische, Beete, Tanks = 0; Halterabstand Schlauch <= 400 mm, Ring <= 1000 mm; Ruecklauf-Gefaelle >= 1 % auf jeder Schlauch-Trasse; Kennzahlen-Panel im Viewer zeigt fuer Ring B2 die gemessene Pumpenleistung (Soll 617 W +- 10 %) und Rohr- und Schlauchmeter aus den Trassen.

## 7. Nicht anfassen
`designs/dome.sc` und alle A+-Eintraege; `data/leitungsnetz.json` und `data/roadmap.json` (Orchestrator); `docs/leitungsordnung.md` (Systemreview); die Blaetter M10-S2N bis S7; V2-Bauteile nur erweitern (Rev. B), nicht umbauen; `data/beschaffung/*.json` nur lesen; E20 selbst (Ben entscheidet beim Zwischencheck).

## 8. OFFEN
1. OFFEN (Ben): E20 bleibt offen; dieses Blatt liefert Bauplan und Vergleich.
2. OFFEN (Werkstatt): PE-100 d75 kalt biegen oder PVC-Ersatz (2.2 Punkt 2), mit zwei Quellen.
3. OFFEN (Werkstatt): Pegelschacht-Podest gegen K10-Gefaelle (2.1); davon haengen 617 W oder bis 754 W ab.
4. OFFEN (Beschaffung, N-PREIS-PRUEF): Preise fuer Schlauch ID16/ID25/d50 lebensmittelecht, Fass 60 l, Montageschiene, Schnellkupplungen, Verteiler d50.
5. OFFEN (Orchestrator): Netz-Delta 2.7 und Roadmap-Eintrag; Abgleich mit Leitungsordnung v2, sobald gepusht.

## Start-Hinweis fuer die Bau-Sitzungen
1. Python immer `python -X utf8`; Skripte per Write, keine Heredocs mit `!` oder Backslashes.
2. Vor dem Start `git log -3 -- docs/leitungsordnung.md`: Ist v2 da, gilt sie vor 2.6.
3. Z-Falle: Netz und dieses Blatt relativ, Trassen und Skripte absolut (+400). Ring-Unterkante absolut 2500.
4. Nie `viewer/extras.json`, `designs/dome.sc` oder fremde `*-ring_b2.sc` mitcommitten; nur Pfad-Commits mit `git -C`.
5. Limit: vor jedem Start `get_usage`; R1 und R2 sind Montage-Laeufe (etwa 600 Nachrichten = 35 %), WA-T und WA-S Werkstatt-Laeufe.

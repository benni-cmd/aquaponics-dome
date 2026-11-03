# R48: Filterreihenfolge und Höhenprofil (Vortex, Feinfilter, Pumpe/Sumpf, Biofilter), Wunsch W54

**Auftrag:** `docs/jobs/R48-filterreihenfolge-hoehenprofil.md` · **Bearbeitet:** 03.11.2026 · **Rolle:** Fachrecherche, nur lesen/rechnen/schreiben; nichts umgebaut, `gen_dome.py`, `data/*`, Netzliste und Roadmap unverändert.
**Herkunft:** [Q] Quelle gelesen · [E] eigene Rechnung (`python -X utf8 scripts/r48_rechnung.py`) · [A] Annahme. Z in mm relativ zum Innenboden (Skript-Z minus 400), wie R47. **Zwei-Quellen-Regel:** eine Behauptung gilt als belegt, wenn zwei voneinander unabhängige Dokumente sie tragen; sonst steht sie als [A] oder „Einzelquelle“ da.

**Problem/Intent/Goal:** Ben fragt, ob der Vortex (Absetzer) über den Biofilter gehört, die Pumpe in einen Subtank wandert, wo der Feinfilter sitzt und ob zwischen den Stufen per Überlauf gearbeitet werden kann. Ziel: belegte Empfehlung, ob die Filterkette vor M10 S3 umgebaut wird; Eingang in E20/E21.

**Wie ich „Subtank“ gelesen habe:** als **Zwischen- oder Sumpftank**, in den die Pumpe verlegt wird: ein Behälter, dessen Wasserspiegel dem Heber-Ende folgt (Z ≈ 320), mit **Tauchpumpen** darin; aus ihm geht nur die Druckleitung nach oben. Nicht gelesen als: Hochbehälter, zweiter Biofilter oder Schlammtank. Wenn Ben etwas anderes meint, ändert sich Abschnitt 2 (V1, V4), die übrigen nicht.

## 0. Antwort (fünf Punkte)

1. **Reihenfolge nicht umbauen: V0 (heutige Kette) bleibt Rang 1.** Grob vor fein, Teilstrom-Vortex am Bodenablauf und Sieb im Hauptstrom vor der Pumpe ist das Muster der Fachliteratur (Abschnitt 4.1). Bens V1 (Pumpe zuerst, Vortex hoch) bricht „Feststoffe vor der Pumpe“ und macht den Vortex im Vollstrom nur halb so wirksam.
2. **Zu Bens drei Fragen:** (a) Vortex über dem Biofilter und Pumpe im Subtank gehen hydraulisch (Vortex-Spiegel Z 1700, Förderhöhe 2,2 m statt 2,0 m, +29 W für vier Pumpen); (b) der Feinfilter gehört als **Siebkorb an den Einlauf des Subtanks, also vor die Pumpe**; (c) Überlauf zwischen allen Stufen geht nur, wenn man ganz am Anfang pumpt (V3): Pumpe sieht Rohwasser, Förderhöhe 2,4 m, 475 kg zusätzlich in der Höhe, Feinfilter über Kopf.
3. **Der echte Wartungsgewinn ist V4 (Subtank mit Siebkorb und Tauchpumpen, Höhen unverändert):** 7,1 m (23 %) der 30,3 m vergrabenen Rohre und zwei der kritischen Einzelpfade (Filter-Stamm je Linie) entfallen, Korb und Pumpe liegen unter einem Deckel. Rang 2. M10 S3 (Verteiler/Beete/NFT) hängt nicht davon ab und kann starten.
4. **Bodenablauf per Schwerkraft ist möglich** (2,2 m Wassersäule am Ablauf, Absetzer-Spiegel zwischen Z 340 und 455): die vier kleinen Pumpen (34 W) entfallen, dafür steht der Absetzer 0,75 m tiefer (Spitze Z −575) und das Schlammfass braucht eine Grube von etwa 1,8 m (V5, Rang 3).
5. **EINHEIT (alles durch den Biofilter) bleibt in allen Varianten erfüllt**, solange jeder Überlauf in den Biofilter mündet, nie in den Pool. Neuer Befund: Der Filterbehälter hat keine Rückstausicherung (Abschnitt 4.3), unabhängig von der Variante.

## 1. Eingaben und Rechenweg

**Heutiger Wasserweg (V0) mit Höhen** [Q `data/leitungsnetz.json` K01 bis K10, K56/K57; `docs/parts/tank.md`; `docs/parts/feinfilter.md`; `scripts/dome-script.json` Befehle 435/436 und 9442/9443]:

| Stufe | Z | Quelle |
|---|---|---|
| Pool-Spiegel / Seitenablauf Mitte | 515 / 340 | K01 |
| Heber-Ende = Filter-Einlauf (195 mm Heberverlust, Reserve 85/88 mm) | 320 | K01, R47 Abschn. 3 |
| Feinfilter: Standfläche in Grube / Auslauf | −496 / −186 | `dome-script.json` Z −96 absolut, fehlt 400; Bauteilblatt Auslauf 310 über Standfläche |
| Hauptpumpen: Saug / Druck | 120 / 255 | R47 |
| Biofilter: Zulauf / Überlauf-Rohr / Spiegel / Deckel | 1420 / 1570 / ≈ 1600 / 1676 | tank.md, K10 („Tankspiegel ca. Z 1600“) |
| Absetzer (Vortex) 267 l: Zulauf / Auslass / Rand / Spitze / Schlammhahn / Plattform | 997 / 1147 / 1247 / 172 / 80 / 428 | tank.md, klein |
| Bodenablauf Pool (11 %, 12,5 l/min) | −1685 | K03 |

**Abweichung gegen R47:** R47 rechnet die statische Höhe bis zum Zulauf (1420, 1,10 m). Der Zulauf liegt aber 150 mm unter dem Spiegel; physikalisch zählt der Spiegel (1600). Ich rechne **statisch 1,28 m, Rest (Reibung, 20 % Reserve) 0,72 m, Summe 2,0 m** wie die Netzliste. Die Summe von V0 bleibt 2,0 m, nur die Aufteilung ändert sich [E]. Der Rest wird bei den anderen Varianten übernommen und bei längeren Rohrwegen um 0,10 m erhöht [A].
**Leistung:** `P = ρ·g·Q·H/η`, Q = 55 l/min je Pumpe, vier Hauptpumpen, η 25 % (Netzliste) und 18 % (R47c, untere Klammer) [E]. Pumpe: die Premium-6000-Klasse liefert nach der R47c-Näherung 3,49 m bei 55 l/min [E], reicht damit für alle Varianten bis 2,4 m.

## 2. Varianten

Zusätzlich zu V0 bis V4 aus dem Auftrag: **V5** (V0 mit Absetzer tief, Bodenablauf per Schwerkraft), weil Prüffrage 3 sie verlangt. Ben nennt drei Lagen des Feinfilters in V1; V1a und V1c stehen unten, V1b ist hydraulisch **identisch mit V3** und dort bewertet.

| Variante | Wasserweg (Z mm) | Subtank/Sumpf |
|---|---|---|
| **V0** heute | Pool 515 → Heber → Feinfilter-Einlauf 320 (Grube −496) → Saugstamm K02/K06 → 2 Pumpen (120/255) → Biofilter (Spiegel 1600) → Verteiler. Teilstrom: Bodenablauf −1685 → kleine Pumpe → Absetzer-Zulauf 997 → Auslass 1147 → Schwerkraft zum Filter-Einlauf 320 | – |
| **V1a** | Pool → Heber → Feinfilter (wie gebaut) → **Subtank** (Spiegel ≈ 320, Pumpen darin) → Druckleitung → **Vortex hoch** (Spiegel 1700, Rand 1800, Zulauf 1550, Spitze 725, Hahn 633, Plattform 981) → Überlauf-Leitung → Biofilter 1600 → Verteiler | ja |
| **V1c** | wie V1a, aber der **Siebkorb sitzt am Einlauf des Subtanks** (Feinfilter-Kasten entfällt, Korb zieht in den Subtank) | ja |
| **V3** (= V1b) Kaskade | Pool → Heber → Subtank (Rohwasser, nur Pumpen-Grobsieb [A]) → **einmal pumpen** → Vortex (Spiegel 1900, Rand 2000, Spitze 925, Plattform 1181) → Feinfilter-Einlauf ≈ 1750 (Standfläche ≈ 930 auf Gestell, Behälteroberkante ≈ 1800) → Biofilter 1600 → Verteiler | ja |
| **V2** Vortex zuerst, tief | Pool → Heber → **Vortex in Grube** (Spiegel 300, Rand 400, Zulauf 150, Spitze −675, Hahn −767) → Feinfilter-Einlauf ≈ 260 (Standfläche ≈ −556, also 60 mm tiefer) → Pumpen → Biofilter. Bodenablauf per Schwerkraft in denselben Vortex | nein |
| **V4** Sieb im Sumpf | Pool → Heber → **Subtank mit Siebkorb am Einlauf, Tauchpumpen im Subtank** (Spiegel ≈ 320) → Druckleitung → Biofilter 1600 → Verteiler. Absetzerkreis wie V0 (K05 mündet in den Subtank) | ja |
| **V5** Absetzer tief | wie V0, aber Absetzer mit Spiegel 400 (Rand 500, Spitze −575, Hahn −667): Bodenablauf fließt per Schwerkraft zu (Druckhöhe 115 mm), Auslass fließt per Schwerkraft zum Filter-Einlauf 320; **kleine Pumpen entfallen** | – |

**Vortex „über dem Biofilter“ heißt hier: neben ihm auf eigenem Gestell**, Wasserspiegel 100 mm über dem Biofilter-Spiegel. Gestapelt (Vortex auf dem Biofilter-Deckel 1676, Spiegel ≈ 2775) ist es nicht sinnvoll: die Dom-Innenhöhe bei r = 3,4 m liegt nicht vor (R47c offen), das Gewicht (300 kg) sitzt auf einem PE-Tankdeckel, für den keine Traglast vorliegt [A].

## 3. Vergleichstabelle

Zahlen: `python -X utf8 scripts/r48_rechnung.py`. Leistung = vier Hauptpumpen, η 25 % (η 18 % in Klammern); kleine Pumpen getrennt.

| | V0 heute | V1a/V1c Vortex hoch | V3 Kaskade | V2 Vortex tief | V4 Sieb+Pumpe im Sumpf | V5 Absetzer tief |
|---|---|---|---|---|---|---|
| Förderhöhe H | 2,00 m | 2,20 m | 2,40 m | 2,12 m (Saug 200) | 2,00 m | 2,00 m |
| Leistung Hauptpumpen | 288 W (400) | 317 (440), +29 | 345 (480), +58 | 305 (424), +17 | 288 (400), ±0 | 288 (400) |
| Kleine Pumpen | 34 W | 34 W [A] (Teilstrom bleibt, Hub 1,2 m statt 0,5 m) | wie V1 | **entfallen** (−34 W) | 34 W | **entfallen** (−34 W) |
| Pumpe sieht | Wasser nach Sieb | V1a: nach Sieb; V1c: nach Sieb im Sumpf | **Rohwasser** | nach Vortex und Sieb | nach Sieb im Sumpf | nach Sieb |
| Vortex im Betrieb | Teilstrom 12,5 l/min: 2,5 m/h, Verweilzeit 20 min, Eintritt 0,13 m/s (wirkt als Absetzbecken) | Vollstrom 110 l/min hinter dem Sieb: kaum noch Fracht | Vollstrom Rohwasser: 21,7 m/h, 2,3 min, Eintritt 1,14 m/s | Vollstrom Rohwasser | wie V0 | wie V0 |
| Wartung: Zugang | Korb in Grube (Hub 460 mm über Deckel), Pumpen bei Z 0, Absetzer-Hahn Z 80, Fass in Grube 0,95 m | Pumpe im Subtank gut (Tauchpumpe), Vortex und Hahn auf Stehleiterhöhe (Rand 1800) | Vortex (Rand 2000) und Feinfilter (Korb-Hub bis ≈ Z 2300) über Kopf | Vortex-Deckel auf Bodenhöhe (Rand 400), Hahn und Fass 0,8 bis 1,9 m tief | Deckel auf: Korb, Pumpen, Schwimmer an **einer** Stelle | Absetzer in Grube 0,6 m unter Boden, Fass bis Z −1767 |
| Vergrabenes Rohr | 30,3 m | 30,3 m, Stamm entfällt (V1c) | 30,3 m, Stamm entfällt | weniger (K05, K03/K04 Teile) [A] | **23,2 m** (−7,1 m Stamm K02/K06/K18/K22) | 30,3 m minus Teile von K03 bis K05 [A] |
| Ausfall | Korb verstopft: Rückstau am Heber, Notbypass K56/K57 (nie getestet); eine von zwei Pumpen fällt aus: halber Umlauf | Pumpe fällt aus: Vortex und Biofilter laufen leer; 254 l Puffer = 2,3 min | zusätzlich: Korb verstopft oben, Überlauf muss in den Biofilter münden; Leck über Kopf | Vortex passiv, kein neuer Ausfallpunkt; Heber-Reserve unverändert 85 mm [A, ±50 mm Spiegel im Vortex] | Korb verstopft: Spiegel im Subtank sinkt, Schwimmer schaltet Pumpen ab; Korb-Überlauf in den Sumpf = eingebauter Bypass (statt K56/K57) [A] | wie V0, ohne Pumpenpaar am Bodenablauf |
| Umbau gegen Gebautes (gebaute Kanten) | keiner | K02, K05, K06, K08, K09, Pumpen, Absetzer neu aufstellen | wie V1 plus Feinfilter-Gestell hoch, K10-Anschluss | K01/K17-Ende, K03/K04/K05 neu, K02/K06-Riser, Absetzer und Fass neu | K02, K06, K08, K09, K18, K22 entfallen/neu, Pumpentafel, K05-Ziel | K03, K04, K05, K07 neu, Absetzer und Fass neu |
| EINHEIT | ja | ja | ja (Überlauf in den Biofilter) | ja | ja | ja |

## 4. Prüffragen

### 4.1 Frage 1: Reihenfolge grob vor fein, Vortex im Vollstrom

**Befund: Die Reihenfolge Wirbelabscheider/Absetzer vor Siebfilter ist Stand der Technik, der Wirbelabscheider sitzt aber im Teilstrom des Bodenablaufs, nicht im Vollstrom.** Das entspricht genau V0.

- [Q] SRAC 453 (Malone 2013): „Traditionally a clarification device is placed upstream of the biofilter“; Rundtanks mit Doppelablauf und Wirbelabscheider entlasten das Mikrosieb. [`srac.msstate.edu` PDF](https://www.srac.msstate.edu/pdfs/Fact%20Sheets/453%20Recirculating%20Aquaculture%20Tank%20Production%20Systems-%20A%20Review%20of%20Current%20Design%20Practice.pdf), gelesen.
- [Q] Davidson & Summerfelt 2005, Zusammenfassung bei [Global Seafood](https://www.globalseafood.org/advocate/settler-evaluation-radial-flow-vs-tangential-flow/): Wirbelabscheider (1 bis 2 m) am Bodenablauf mit 7 bis 8 % des Stroms, Mikrosieb im **gesamten** Strom; das Mikrosieb entfernt 40 bis 45 % der täglichen Feststoffmasse, der Wirbelabscheider 23 %.
- [Q] Khater et al. (Benha-Universität), „Solids removal in a recirculating aquaculture system“: Aufbau Fischtank → Hydrozyklon → Siebfilter → Biofilter, Doppelablauf mit 1 bis 10 % zum Hydrozyklon, 90 bis 99 % zum Siebfilter. (gelesen, PDF)
- Drei unabhängige Dokumente tragen die Aussage; die Netzliste (K03: „Dual-Drain-Teilstrom 5–20 %, Davidson/Summerfelt“) folgt demselben Muster.

**Auslegungswerte, V0 gegen Vollstrom** [E, Fläche 0,305 m², Inhalt 254 l bis Rand]:

| | Teilstrom 12,5 l/min (heute) | Vollstrom 110 l/min |
|---|---|---|
| Oberflächenbeschickung | 0,68 mm/s = 2,5 m/h | 6,01 mm/s = 21,7 m/h (1,9-fach des Davidson-Versuchs mit 3,1 mm/s) |
| Verweilzeit | 20,3 min | 2,3 min (die 2,4 min des Auftrags rechnen mit 267 l) |
| Eintrittsgeschwindigkeit d50 | 0,13 m/s | 1,14 m/s |

- **Der heutige Absetzer wirkt hydraulisch als Absetzbecken**, nicht als Wirbel: bei 0,13 m/s Eintritt entsteht kein nennenswerter Drall. Seine Verweilzeit von 20 min liegt im Bereich, den SRAC 453 für Absetzbecken nennt (15 bis 30 min) [Einzelquelle für den Bereich].
- **Abscheidegrad:** [Q] Davidson/Summerfelt 37,1 ± 3,3 % der Schwebstoffe bei 3,1 mm/s (Global Seafood); [Q] Khater 27,4 bis 57,8 % der absetzbaren Feststoffe (Zusammenfassung). Beide gelten für den Teilstrom des Bodenablaufs. Die Übertragung auf den Vollstrom bei 6 mm/s ist eine **Extrapolation [A]**: nach dem gleichen Mechanismus (Schwerkraft, Beschickung und Sinkgeschwindigkeit, Global Seafood) sinkt die Leistung mit steigender Beschickung; eine Zahl dafür liegt nicht vor.
- **Mindestdurchfluss und Verweilzeit eines Wirbelabscheiders:** die Auslegungsmethode steht bei Veerapen, Lowry und Couturier 2005 (Aquacultural Engineering 33, 21 bis 45); ich habe nur den Titel und die Zusammenfassung gefunden, **nicht den Volltext**. Keine Zahl dafür belegt: **offen**.
- **Vollstrom-Wirbelabscheider als erste Stufe mit Pumpe danach** gibt es in einer Laboranlage: [Q] Orellana 2006 (Dissertation Kiel, Abschnitt 2.2.1): Wirbelabscheider als erste Stufe, Wasser 3,5 m³/h, danach Airlift zum Biofilter. Einzelquelle, Laborgröße, **Kandidat**.
- **Ergebnis für den Vortex vor dem Feinfilter (V2/V3):** machbar und mit Orellana belegbar, aber im Vollstrom bei doppelter Beschickung nur noch von geringem Nutzen, weil die Fracht ohnehin zu über 95 % aus Teilchen unter 20 µm besteht: [Q] Chen u. a. 1993 (Zusammenfassung bei [WSU](https://rex.libraries.wsu.edu/esploro/outputs/journalArticle/Suspended-solids-characteristics-from-recirculating-aquacultural/99900583053301842)): über 95 % der Teilchen kleiner 20 µm, 40 bis 70 % der Masse; [Q] Orellana 2006, Diskussion: Libey 1993 67 % unter 30 µm, Langer u. a. 1996 Hauptanteil unter 20 µm. Zwei Quellen. Das 100-µm-Gewebe des Feinfilters hält diese Feinfracht ebenfalls kaum zurück (Mortensen 21 %, R30, im Bauteilblatt); der Vortex ändert daran nichts.

### 4.2 Frage 2: Pumpe vor der Feststoffabscheidung

**Befund: Die Regel „Feststoffe zuerst, Pumpe danach“ stützt sich auf zwei Dokumente, die denselben Primärbeleg zitieren; für eine Quelle ist sie damit stark, für zwei unabhängige noch ein Kandidat.**

- [Q] Unger, Schumann und Brinker 2015 (Aquaculture Environment Interactions 7, 223 bis 238, gelesen): Feststoffe sind Turbulenz und Scherkräften „induced by pumps and fish motion“ ausgesetzt, was die Kotballen zerlegt (McMillan u. a. 2003); Feststoffe müssten „as quickly and gently as possible“ entfernt werden, die Anlage nutzt eine Pumpe mit minimaler Turbulenz und Scherung.
- [Q] Orellana 2006 (Diskussion, gelesen): Pumpen, Gasaustauscher, Siebe und Kaskaden können „Partikel zerstörende Einheiten“ sein; die Entfernung sei am wirksamsten **direkt hinter dem Fischtank**, „whichever pumping system“ verwendet wird.
- **Gegenstimme (gleicher Primärbeleg):** McMillan u. a. 2003, nach Orellana zitiert: Propellerpumpen zerlegen größere Teilchen in mittlere, ändern aber die Zahl der Teilchen unter 60 µm nicht. Die Primärquelle habe ich nicht gelesen.
- **Folgerung:** Die Scherung erzeugt vor allem mittlere, noch absetzbare und siebbare Teilchen; die dominierende Feinfracht unter 20 µm ist ohnehin da (4.1). Sie ist ein Argument **gegen V3 und gegen V1b**, aber kein Verbot. Die gebaute Kette V0 folgt der Regel (Sieb vor der Pumpe).
- **Verstopfungsrisiko der Pumpe (Rohwasser):** keine Quelle gefunden. Das Oase-Datenblatt (Aquarius Universal Premium 6000, gelesen) nennt weder maximale Partikelgröße noch Vorfilter. **[A]** Ein Grobsieb vor der Pumpe (Teichtechnik-Pumpenvorfilter) ist für V3 Pflicht.
- **Pumpe im Sumpf (Subtank):** [Q] Oase-Datenblatt: „Nass- und Trockenaufstellung“, „Ansaugend auch bei geringem Wasserstand“; dieselbe Bauart steht bereits im Plan als Beet-Sumpfpumpe (Netzliste, Teichpumpe 5300 l/h). Einzelquelle für die Nassaufstellung dieses Fabrikats; Fabrikat bleibt offen. **Sump nach dem Sieb als übliche Praxis:** nur schwache Hinweise (Teichfilter-Beschreibung bei [Play It Koi](https://playitkoi.com/blogs/pond-filtration-basics/gravity-fed-vs-pump-fed-rdf-koi-pond), Patente zu Pumpensümpfen): **Kandidat**.

### 4.3 Frage 3: Höhenbilanz, Förderhöhe, Bodenablauf

Höhen und Förderhöhen: Tabellen in Abschnitt 2 und 3.

- **Warum der Biofilter nicht tiefer kann:** sein Spiegel 1600 ist der Druckkopf für NFT (1000 bis 1090) und Beete; deshalb wird davor gepumpt. Jede Variante, die den Biofilter am Ende lässt, braucht die Höhe zwischen Pumpe und Biofilter.
- **Überlauf zwischen Feinfilter und Biofilter (Bens dritte Frage):** nur möglich, wenn die Pumpe **vor** dem Feinfilter sitzt und höher fördert als der Biofilter-Spiegel plus Sieb-Aufstau: Vortex-Spiegel ≈ 1900 (1600 + 100 Rohr + 150 Sieb-Reserve [A] + 50), also H = 2,40 m (V3). Der Feinfilter-Kasten (Einlauf 816 über Standfläche, Behälter 610 hoch auf 250 Füßen) muss dann mit seiner Oberkante über 1750 stehen, die Standfläche liegt bei etwa Z 930, der Korb wird bis etwa Z 2300 gehoben.
- **Bodenablauf per Schwerkraft (Frage ausdrücklich):** **Ja**, der Ablauf liegt 2,2 m unter dem Spiegel (515 − (−1685)). Der aufnehmende Behälter braucht einen Spiegel **unter 515**; soll sein Auslass außerdem ohne Pumpe zum Filter-Einlauf (320) laufen, liegt das Fenster bei **Spiegel 340 bis etwa 455** (Rest 60 mm Rohr- und Ventilverlust [A]). Dann entfällt die kleine Pumpe (V5, V2). Der Teilstrom von 12,5 l/min muss gedrosselt werden: Drosselventil in der Leitung verstopft leicht, besser eine höhenverstellbare Auslassklappe oder ein Standrohr am Vortex-Auslass [A, kein Beleg]. Die kleinen Pumpen heben heute nur 0,48 m (997 − 515) [E], ihr Wegfall spart 34 W und vier Pumpen, kostet aber den Absetzer in der Grube.
- **Heber-Reserve:** Der Heber trägt bei Spiegel 320 das Limit (Reserve 85/88 mm, K01 ohne Marge im ungünstigsten Fall, Pitch B02). In V2 darf der Vortex-Spiegel höchstens 320 betragen, besser 300; höher bremst den Heber, tiefer erhöht den Durchfluss und ist unkritisch. Eine Messung am gebauten Heber steht aus.

### 4.4 Frage 4: Tragfähigkeit und Konstruktion des hohen Vortex

[E, Überschlag, Bauteilblatt: Vortex gefüllt ≈ 300 kg, Gestell Rechteckrohr 30 × 30, Wand 2 mm [A]; Beinlänge = Plattformhöhe.]

| | V1 (Plattform 981) | V3 (Plattform 1181) |
|---|---|---|
| Knicklast je Bein, gelenkig / Kragarm | 63,4 / 15,8 kN | 43,7 / 10,9 kN |
| Last je Bein | 0,83 kN | 0,83 kN |
| Sicherheitsfaktor gegen Knicken | 76 / 19 | 52 / 13 |
| Schwerpunkt, Kippen ab | Z 1251, 0,24 g | Z 1451, 0,20 g |

- **Knicken ist kein Problem, Kippen ist das Thema.** Das gilt wie beim Biofilter heute (0,23 g, R47c). Ein Gestell mit Fußplatten (je 2 × M8 wie T40), Querstreben und Diagonalen reicht als Konzept. Anstoßlast, Befüllen mit Schwall und Erdbeben **nicht bewertet** [offen].
- **Tank ist ein PE-Konus-Tank mit Kegelsitz in einer Plattform** (tank.md); der hohe Vortex ist dasselbe Bauteil mit längeren Beinen (751 → ca. 1000 bis 1200 mm). Ein neues Bauteil entsteht nur beim Feinfilter-Gestell (V3).
- **Bens Frage „ist das nötig“:** nur in V1 und V3. V3 bringt zusätzlich 475 kg (Vortex 300 plus Feinfilter 175) neben den Biofilter (857 kg), das sind +55 % Last in der Höhe [E].

### 4.5 Frage 5: Schlammablass und Grube

Schlammfass heute: Spannringfass 0,95 m tief in Grube (K07). Rechnung: Fass-Oberkante höchstens 150 mm unter dem Hahn (Fallrohr und Bogen 100 mm, Luft 50 mm [A]).

| | V0 | V1 | V3 | V2 | V5 |
|---|---|---|---|---|---|
| Hahn Z | 80 | 633 | 833 | −767 | −667 |
| Fass-Boden höchstens | −1020 | −467 | −267 | −1867 | −1767 |
| Grube nötig | 1,0 m (Plan: 0,95 m) | 0,47 m | 0,27 m | 1,9 m | 1,8 m |

**Die Grube entfällt bei hohem Vortex nicht, sie wird nur flacher (0,3 bis 0,5 m statt 0,95 m).** Ebenerdig würde ein Fass erst bei Hahn ≥ 1100 stehen (Vortex-Spiegel über 2100) oder bei kleinerem Fass (z. B. 100 l, 0,55 m) und V3. Bei V2 und V5 wird die Grube **tiefer als der Poolboden** (−1685) und damit eine Standortfrage (Grundwasser, offen); Alternativen sind ein kleiner Sammelbehälter mit Tauchpumpe [A].

### 4.6 Frage 6: Wartung je Variante, Handgriffe je Woche

Handgriffe sind Schätzungen aus den Intervallen der Netzliste und des Bauteilblatts [A]: Korb alle 1 bis 2 Wochen (0,5 bis 1× je Woche), Absetzer-Spülung alle 2 bis 3 Tage (2 bis 3×), Schlammfass 1× je Woche.

| | Korb ziehen | Pumpe tauschen | Absetzer-Spülung und Fass | Bemerkung |
|---|---|---|---|---|
| V0 | Grube, Deckel, Hub 460 mm | Rohrverschraubungen lösen, Pumpen Z 0 | Hahn Z 80, Fass Grube | Stamm K02/K06 blind vergraben |
| V1 | wie V0 (V1a) oder im Subtank (V1c) | im Subtank herausheben | Hahn Z 633: Stehleiter, Fass Grube 0,5 m | zwei Behälter mit Pumpen/Wasser in Gruppe |
| V3 | **über Kopf**, Korb-Hub bis ≈ Z 2300 | im Subtank | Hahn Z 833 über Kopf | alle drei Teile oben; Leck tropft auf Technik |
| V2 | Grube, wie V0 | Pumpen Z 0 | Hahn Z −767: nur mit Sammelbehälter sinnvoll | Vortex-Deckel bodennah, gut |
| **V4** | **Deckel auf, Korb heben** | **Deckel auf, heben** | wie V0 | **eine Stelle, kein Stamm** |
| V5 | wie V0 | wie V0 | Absetzer in Grube, Fass bis −1,8 m | spart Kleinpumpen |

### 4.7 Frage 7: Einheitlicher Fluss (W53)

Alle sechs Varianten führen **das gesamte Linienwasser durch den Biofilter** und münden in den einen Pool; nichts geht an ihm vorbei. Bedingungen: (1) jeder Überlauf (Vortex, Feinfilter-Korb, Sumpf) mündet in den Biofilter oder in den Subtank davor, **nie in den Pool**; (2) in V3 muss der Korb-Überlauf in den Biofilter münden; (3) der Notbypass K56/K57 bleibt Pool → Pumpe → Biofilter. **Kein Verstoß** in keiner Variante. V2 und V5 verschieben nur den Teilstrom des Absetzers.

**Neuer Befund (alle Varianten, V0 eingeschlossen):** Der Feinfilter-Kasten hat nach dem Bauteilblatt „keinen Notüberlauf/Bypass“. Bleibt bei laufendem Heber die Pumpe stehen, steigt der Spiegel im Behälter Richtung Pool-Spiegel 515. Die Oberkante des Behälters liegt bei Z 364 (Standfläche −496 + foot_h 250 + 610) [E], also 151 mm darunter; die Deckeldichtung wird belastet oder das Wasser tritt in die Grube. Gegenmittel stehen schon in A+: Hoch-Schwimmer mit Alarm (M5) und Absperrhahn am Heber (M3); **ich schlage vor, beide an den Heber-Absperrhahn zu koppeln** (Hoch-Schwimmer schließt den Hahn), statt nur zu melden. Bei V4 ist das Rand-Maß des Subtanks entscheidend: Behälterrand ≥ 520 oder Überlauf mit Weg.

## 5. Empfehlung und Rangfolge

| Rang | Variante | Begründung | Bedingung |
|---|---|---|---|
| **1** | **V0 behalten (mit A+)** | folgt dem Muster der Literatur (4.1), Sieb vor der Pumpe (4.2), kein Umbau, keine Höhenänderung, 288 W | Rückstausicherung am Heber ergänzen (4.7) |
| **2** | **V4 Subtank mit Siebkorb und Tauchpumpen** | −7,1 m vergrabene Rohre (23 % von 30,3 m), −2 kritische Einzelpfade je Linie (R47b 6.2), Wartung an einer Stelle, Höhen unverändert, Korb-Überlauf ersetzt den ungetesteten Totast K56/K57 | Umbau von K02/K06/K08/K09/K18/K22 und Pumpentafel; Entscheidung Ben; blockiert M10 S3 nicht |
| 3 | V5 Absetzer tief, kleine Pumpen entfallen | −34 W, −4 Pumpen | Grube bis −1,8 m (Standort offen), Absetzerkreis neu |
| 4 | V2 Vortex zuerst, tief | passiv, kein neuer Ausfallpunkt, aber Vortex im Vollstrom wenig wirksam und Heber-Reserve ohne Messung | Grube 1,9 m, Rückbau K03 bis K05 |
| 5 | V1 (a/c) Vortex hoch, Pumpe im Subtank | hydraulisch lösbar (+29 W), aber Vortex nach dem Sieb ohne Aufgabe oder Pumpe vor dem Vortex | Gestell, Vortex in 1,0 bis 1,8 m Höhe |
| 6 | V3 Kaskade (= V1b) | Überlauf zwischen allen Stufen; Preis: Pumpe sieht Rohwasser, 2,4 m, 475 kg und Feinfilter über Kopf | nur wenn Überlauf-Kaskade Selbstzweck ist |

**Antwort auf Bens Ausgangsfrage:** „Vortex über den Biofilter, Pumpe in einen Subtank“ ist machbar, bringt aber keinen Wartungsgewinn, solange der Vortex im Vollstrom nach dem Sieb sitzt oder vor der Pumpe Rohwasser sieht. Der Teil von Bens Idee, der trägt, ist der **Subtank mit der Pumpe darin, der Siebkorb davor** (V4).
**Folgen:** M10 S3 bis S7 laufen mit V0 unverändert. Bei V4 sind nur Kanten vor dem Biofilter betroffen (K02, K06, K08, K09, K18, K22), also nichts in S3. Netzlisten-Änderung nur, wenn Ben V4 oder V5 wählt (Wunsch an den Orchestrator, hier nicht geändert).

**Folgerung für E20/E21:** E20 (Wasserkreislauf A+ gegen Ring) wird von der Filterreihenfolge nicht berührt. E21 (Filterkette): Empfehlung V0 behalten; V4 als Option „Wartungs-Umbau vor oder nach S3“ vorlegen.

## 6. Beschaffbarkeit der genannten Teile

| Teil | Standardteil / Selbstbau | Beleg |
|---|---|---|
| Vortex (Konus-Tank PE, 250 bis 270 l, Leitrohr d110) | Tank Standard (Konus-Boden-Tank 500 bis 1000 l, Größe anpassen), Leitrohr PVC Standard; Plattform und Gestell Selbstbau (Metallbauer) | tank.md „Beschaffbarkeit“ |
| Gestell für hohen Vortex | Selbstbau, Rechteckrohr verzinkt | tank.md |
| Feinfilter-Kasten T55 | Handel: Beutel- oder Siebkorbfilter der Teichtechnik (100 µm); Bauteil als Eigenbau PP | feinfilter.md „Handelsüblich“ |
| Subtank/Sumpf | Standard: PE-Rundtank oder IBC-Zuschnitt (Bauart wie Beet-Sumpf, Netzliste) | Netzliste |
| Tauchpumpen | Standard: Teichpumpe 5000 bis 6000 l/h (Oase u. a.), Fabrikat offen | Datenblatt Premium 6000; Netzliste |
| Schwimmerschalter, Absperrhähne | Standard | Netzliste |
| Grobsieb vor Pumpe (V3) | Standard (Pumpenvorfilter) [A] | – |
| Schlammfass 100 bis 220 l | Standard (Spannringfass) | K07 |
| Standrohr/Auslassklappe für Teilstrom (V5/V2) | Selbstbau aus PVC-Teilen [A] | – |

## 7. Belegstand je Aussage

| Aussage | Quellen | Stand |
|---|---|---|
| Absetzer/Wirbelabscheider vor Sieb, im Teilstrom des Bodenablaufs | SRAC 453; Davidson/Summerfelt (Global Seafood); Khater | belegt (3) |
| Abscheidegrad Wirbelabscheider 27 bis 58 % (Teilstrom) | Davidson/Summerfelt (37 %); Khater (27 bis 58 %, absetzbare Feststoffe) | belegt (2), Übertragung auf Vollstrom [A] |
| Pumpen zerlegen Partikel; Entfernung vor der Pumpe | Unger u. a. 2015; Orellana 2006 (beide nach McMillan 2003) | Kandidat stark, Primärquelle nicht gelesen |
| Feinfracht unter 20 µm dominiert | Chen u. a. 1993; Orellana 2006 (Libey, Langer) | belegt (2) |
| Absetzbecken 15 bis 30 min Verweilzeit | SRAC 453 | Einzelquelle |
| Wirbelabscheider als erste Stufe, Pumpe danach, Vollstrom | Orellana 2006 | Einzelquelle, Labor |
| Pumpe im Sumpf (Nassaufstellung) | Oase-Datenblatt; Beet-Sumpf in der Netzliste | Einzelquelle + interner Vorgänger |
| Sumpf nach dem Sieb als übliche Praxis | Teichfilter-Beschreibung, Patente (nicht gelesen) | Kandidat |
| Auslegung Wirbelabscheider (Veerapen 2005) | nur Zusammenfassung gefunden | offen |
| Heber-Reserve, Höhen, Leitungsdaten | Netzliste, R47, loop-state S2R | [Q] intern |
| Förderhöhen, Leistungen, Traglasten, Fass-Gruben | `scripts/r48_rechnung.py` | [E] |

**Geprüft gegen:** `docs/jobs/R48-filterreihenfolge-hoehenprofil.md`; `docs/arbeitsweise-sitzungen.md` Abschn. 4 und 6; `docs/research/R47-wasserkreislauf-neu.md` (ganz, R47b und R47c); `data/leitungsnetz.json` (Knoten, K01 bis K10, K19 bis K23, K56/K57, F1 bis F3); `scripts/dome-script.json` (Lagen der Tank- und Filter-Instanzen); `docs/parts/tank.md`, `docs/parts/feinfilter.md`; `python -X utf8 scripts/r48_rechnung.py`; Volltexte gelesen: SRAC 453, Khater u. a., Orellana 2006, Unger u. a. 2015, Oase-Datenblatt; Zusammenfassungen gelesen: Davidson/Summerfelt (Global Seafood), Chen u. a. 1993. **Nicht gelesen:** Davidson/Summerfelt und Veerapen im Volltext, McMillan 2003, Timmons/Ebeling, `docs/research/R45` und `R44` (nur über R47 zitiert), `docs/walkway-map.md`.
**Offen:** (1) Auslegungswerte Wirbelabscheider (Mindestdurchfluss, Verweilzeit, Abscheidegrad im Vollstrom): Fachquelle fehlt, ICH (nächste Recherche mit Volltext Veerapen 2005). (2) Messung der Heber-Reserve am gebauten Heber und Rückstausicherung des Filterbehälters: DEINE ENTSCHEIDUNG (Hahn mit Schwimmer koppeln?), Montage setzt um. (3) E21: V0 behalten, V4 als Option: DEINE ENTSCHEIDUNG (Ben). (4) Grube tiefer als Poolboden (V2/V5): Standort offen, DEINE HANDLUNG (Grundwasser klären). (5) Kippen und Anstoß des hohen Gestells, Dom-Innenhöhe: ICH, nur falls V1/V3 gewählt.

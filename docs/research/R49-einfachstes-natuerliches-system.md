# R49: Das einfachste natürliche System (Schwerkraft, Siphon): Biofilter höher? Alles vergraben? Beet-Rückführung im Kreis?

**Auftrag:** `docs/jobs/R49-einfachstes-natuerliches-system.md` (Frage Ben, 03.11.2026) · **Bearbeitet:** 03.11.2026 · **Rolle:** Fachrecherche, nur lesen/rechnen/schreiben; `gen_dome.py`, `data/*`, Netzliste, Roadmap und Modell unverändert.
**Herkunft:** [Q] Quelle/Datei gelesen · [E] eigene Rechnung (`python -X utf8 scripts/r49_rechnung.py`) · [A] Annahme. Z in mm relativ zum Innenboden (Skript-Z minus 400), wie R47/R48. **Zwei-Quellen-Regel:** belegt heißt zwei voneinander unabhängige Dokumente; sonst steht „Einzelquelle“, [A] oder [E].
**Problem/Intent/Goal:** Ben will das einfachste, naturnahe (Schwerkraft, Siphon), wartungsarme und überschaubare System und fragt: Biofilter höher oder kleinere Anpassungen? Muss alles vergraben sein? Kann die Beet-Rückführung als Kreisleitung ohne Pumpe laufen? Ziel: gemessene Gegenüberstellung der Konzepte und eine Empfehlung für E20/E21.

## 0. Antwort (fünf Punkte)

1. **Den Biofilter höher zu setzen vereinfacht nichts.** Der Zulauf zu Beeten (Kopf 950 mm) und Tischen (600 mm) läuft heute schon ohne Ring und ohne Pumpe. Anheben müsste man nur für einen Ring über dem Gang: mindestens **717 bis 807 mm** (R47c: 725), +95 bis +104 W, ein zweiter Hochbau. Ein Ring auf Tischhöhe (Idee I5) braucht **0 mm**, erreicht aber die Beete nicht. Tische und Biofilter tiefer bringt höchstens 70 bis 100 mm. [E, Abschn. 2]
2. **Die Beet-Rückführung ohne Pumpe geht nur mit Beeten um 0,8 bis 0,95 m höher** (Ablauf ab Z 715 bis 845, Beetrand Z 1375; Außenbeete haben dann 0,44 m bis zur Kuppel, 16,9 t auf Gestellen). Ein Sammelring ändert daran nichts: die Höhenlücke ist der Beetablauf (Z −100) gegen Pool-Spiegel 515, nicht die Leitungsform. Der Ring gehört, wenn überhaupt, in einen **Bodenkanal mit Rost**. [E, Abschn. 3]
3. **Mammutpumpe für die Beete: nein; für den Absetzer-Teilstrom: ja, als Kandidat.** Beete: Hub 0,8 bis 1,0 m bei 0,8 m Eintauchtiefe = 44 bis 50 % Eintauchverhältnis (Leitfaden: über 80 %, Hub höchstens 0,3 m), Luftbedarf 140 bis 320 l/min je Linie, mehr als die ganze Anlage hat (130 Mittel, 205 Spitze). Absetzer-Teilstrom: Hub 0,48 m, Eintauchtiefe 2,55 m (das schon gebaute Steigrohr K03), **84 %**, 6 bis 26 l/min Luft; vier Kleinpumpen entfielen. [E, Q Global Seafood]
4. **Vergraben muss nur wenig:** von 30,3 m auf **12,7 m** (Heber 2,4 m und Bodenablauf-Kreis 10,2 m) mit dem Subtank V4 und K05 direkt in den Subtank; auf 2,4 m, wenn der Absetzerkreis ganz entfällt. Der Heber darf wegen Spiegel und Gangregel nicht oberirdisch, wohl aber in einen **Kanal mit Rost** statt in Erde. Die größte künftige Erdmenge ist nicht das Gebaute, sondern der Beet-Sammler K14 (58,9 m). [E, Abschn. 4]
5. **Empfehlung E20/E21: A+ bleibt, V4 (Subtank) jetzt mitnehmen, K05 direkt, Bodenkanal für Heber und K14.** Die einzige Variante mit nur einer Pumpstufe ist ein **Tiefsumpf (T)**, in den auch der Beet-Ablauf fließt: Dauerstrom gleich (436 gegen 430 W), aber der Pool-Durchsatz **halbiert sich**; ohne Fachprüfung nicht wählen (Rang 2, bedingt). [Abschn. 5]

## 1. Kriterien und Messgrößen

Ben nennt: **simpel, wartungsarm, überschaubar** (wenige verschiedene Teile, wenige Einzelpfade, wenig Vergrabenes), **effizient** (Dauerstrom). Gemessen wird je Konzept (Zeilen der Tabelle in Abschnitt 2):

| Größe | Rechenweg |
|---|---|
| Pumpen laufend / Pumpstufen für Beetwasser | Netzliste K08 bis K10, K58; vier Hauptpumpen à 55 l/min, zwei Absetzer-Kleinpumpen in Betrieb, zwei Beet-Sumpf-Pumpen [Q] |
| Förderhöhe | statisch = Biofilter-Spiegel 1600 − Saugspiegel (320), plus Rest 0,72 m (Reibung, 20 % Reserve) wie R48 [Q R48, E] |
| Dauerstrom | `P = ρ·g·Q·H/η`, η 25 % (Netzliste) und 18 % (untere Klammer, R47c) [E]; Absetzer 34 W, Beet-Sumpf 108 W [Q R47] |
| Vergrabene Meter | Segmente der Trassen mit Mitte unter Z 0 rel. (`data/leitungstrassen.json`), plus künftige Gräben [E] |
| Meter über Kopf | Ring-Länge über Z 2100 [Q R47] |
| Einzelpfade / Teilearten | Zählung R47b (Heber, Stamm, Zweig, Bypass, Absetzerkreis je Linie) plus Beet-Kette Kollektor, Sumpf, Pumpe; Teilearten = verschiedene Sonderbauteile [A, Zählung im Skript Abschn. 5] |
| Umbau am Gebauten | Kanten und Bauteile, die gegen den Stand Runde 66 neu werden [Q R47c, R48] |

## 2. Naturprinzip-Konzepte gegeneinander

### 2.1 Höhen einzeln gerechnet (Z rel., mm)

| Punkt | Z | Quelle |
|---|---|---|
| Pool-Spiegel / Heber-Ende am Filter | 515 / 320 | K01, R48 |
| Biofilter Überlauf / Spiegel | 1570 / 1600 | K10, R48 |
| NFT-Rinne / Tisch-Zulauf / Beet-Tropfrohr | 1000 / 1090 / 650 | K12, R47 (Bauteilblatt `ibc_beet` gibt 450, siehe Abweichungen) |
| Druckkopf vom Spiegel: Rinne / Tisch-Zulauf / Beet | 600 / 510 / 950 | [E] |
| Beetablauf / Halbring Tiefpunkt–Hochpunkt | −100 / 660–720 | K14, R47 |
| Ring Unterkante / Achse / Hochpunkt | 2100 / 2145 / 2245 | Trassenregel Ü-Band [Q m10-leitungen 4.1, R47] |

**Befund: Das Wasser fließt hinter dem Biofilter heute schon ohne Pumpe zu allen 38 Abnehmern.** Gepumpt wird zweimal: Hauptpumpen (2,0 m) und, nur wegen der Höhenlage, der Beet-Sumpf. Eine Anhebung des Biofilters ändert an der zweiten Stufe nichts (Abschn. 3).

### 2.2 Kleinste Anhebung für Schwerkraft ohne Ring und mit Ring

| Frage | Ergebnis [E] |
|---|---|
| Biofilter anheben, damit Beete und Tische **ohne Ring** per Schwerkraft laufen | **0 mm.** Läuft heute (Kopf 950 und 600 mm gegen die Forderung ≥ 500 mm, K12) |
| Ring auf Tischhöhe (I5), Achse Z 1000 am Tischbein, gespeist aus dem Überlauf 1570 | **0 mm**, Kopf 570 mm. Er kreuzt keinen Gang (frei ist dort nur ab Z 2100) und erreicht die Beete (Z 650, r 3,3 und 5,2 m) nicht ohne Graben: das ist K12 mit anderem Namen (R47c B4) |
| Ring **über dem Gang** (Unterkante 2100), Überlauf mindestens | **2287 bis 2377**: Anhebung **717 mm** (0,3 %, d75) bis **807 mm** (1 %, d90); R47c rechnet 725. Flacher als 0,3 % ist nicht sinnvoll (Entlüftung) |
| Biofilter **tiefer** | höchstens **100 mm** (Spiegel ≥ Rinne 1000 + 500) |
| Tische **tiefer** | höchstens **69 mm** (Sektorsammler d63 muss über dem Halbring-Hochpunkt 720 + 48 + 63 münden) |

Tiefer statt höher lohnt nicht: 70 mm weniger Förderhöhe sparen 10 W (430 → 420 W) und lösen den Beetablauf nicht.

### 2.3 Konzepte (gesamte Anlage, zwei Linien)

Drei Konzepte nach Auftrag, dazu der Vergleich mit den Ring-Varianten. **(a)** A+ mit Subtank V4 (R48). **(b)** Biofilter höher: b1 = 725 mm (R47c), b2 = 660 mm, b3 = Ring auf Tischhöhe. **(c)** T = Tiefsumpf: V4-Subtank um 0,7 m tiefer, in den **auch die Beet-Siphons per Schwerkraft** entwässern; der Beet-Sumpf mit zweiter Pumpe entfällt, die vier Hauptpumpen im Subtank heben alles einmal.

| | A+ heute | (a) A+ + V4 + K05 direkt | (b1) B1 Biofilter +725 | (b2) +660 flach | (b3) I5 Tischhöhe | **(c) T Tiefsumpf** |
|---|---|---|---|---|---|---|
| Pumpen laufend | 8 | 8 | 8 | 8 | 8 | **6** |
| Pumpstufen Beetwasser | 2 | 2 | 2 | 2 | 2 | **1** |
| Förderhöhe Hauptpumpe | 2,00 m | 2,00 m | 2,73 m | 2,66 m | 2,00 m | 2,79 m |
| Dauerstrom η 25 % (η 18 %) | 430 W (597) | 430 (597) | 534 (742) [R47c: 549] | 525 (729) | 430 (597) | **436 (606)** |
| kWh/Tag | 10,3 | 10,3 | 12,8 | 12,6 | 10,3 | 10,5 |
| Vergraben, gebaute Kanten | 30,3 m | **12,7 m** | 30,3 m | 30,3 m | 30,3 m | 12,7 m |
| Vergraben, künftige Gräben | 79 m (K14 58,9; K58/59 8; K11 ~12) | 12 m + K14 im Kanal | wie A+, K11 entfällt | wie b1 | wie A+ | K14 im Kanal (58,9 m), kein K58/59 |
| Meter über Kopf | 0 | 0 | Ring 21 + Abgänge 85 | wie b1 | 0 | 0 |
| Einzelpfade | 12 | 6 | 12 | 12 | 12 | **4** |
| Teilearten | 14 | 13 | 17 | 17 | 14 | 13 |
| Umbau am Gebauten | keiner | K02, K06, K08, K09, K18, K22 (vor dem Biofilter), K05 | K08–K10, 2 Plattformen, Biofilter | wie b1 | keiner | wie (a) plus Subtank tiefer, Heber-Ende |

Zahlen: `python -X utf8 scripts/r49_rechnung.py`, Abschnitte 2 und 5. Dauerstrom enthält Absetzer 34 W und (außer T) Beet-Sumpf 108 W; η 18 % rechnet alle Pumpen auf die untere Klammer um. Einzelpfade, Teilearten und die künftigen Gräben (K14 und K58/K59 aus R47 ±25 %; K11 ≈ 8 Außenbeete × 1,5 m) sind [A]-Zählungen.

**Lesart.** (b1/b2) erhöhen Strom (+95 bis +104 W), Höhe und Bauteile und vereinfachen nichts. (b3) und (a) kosten keinen Strom; (a) spart vergrabene Meter und Einzelpfade. (c) ist die einzige Variante, die eine Pumpstufe und die Beet-Sumpf-Behälter streicht, **bei gleichem Strom**. Der Preis steht in 2.4.

### 2.4 Konzept T (Tiefsumpf): was es bringt und was es kostet

**Funktion [E].** Subtank je Linie mit Siebkorb und zwei Tauchpumpen (V4), Betriebsspiegel −600 bis −150, Mittel −375. Der Beetablauf (Z −100) liegt über dem EIN-Spiegel (−150) und entwässert frei in den Subtank. Der Heber vom Pool (Spiegel 515) hat dann 890 mm Druckhöhe (heute 195) und muss gedrosselt werden (Schwimmerventil im Subtank): er fördert nur noch 43 statt 97,5 l/min. Dafür steigt die statische Höhe um 0,695 m; weil das Beetwasser nicht mehr zweimal gehoben wird, bleibt der Strom gleich (307 gegen 300 m·l/min Hubarbeit).

**Gewinn.** Beet-Sumpf (500 l, Grube 1,0 m, Pumpe, Schwimmer) und K58/K59 entfallen; die Heber-Reserve (heute 85 mm, Pitch B02) wird zur Drossel-Frage statt zur Knappheit; zwei Pumpstufen werden eine; bei Pumpenausfall bleibt N+1 an einer Stelle.

**Preis, der gegen die EINHEIT-Idee läuft [E].** Der Pool bekommt nur noch NFT, Bypass und Messkreis zurück: **55,5 statt 110 l/min je Linie**. Das System wälzt 4,7 statt 9,3 Mal am Tag um. Im Durchsatzmodell (Biofilter-Wirkung je Durchgang E = 0,3 bis 0,5 [A]) steigt der TAN im Pool von 0,8 bis 1,4 auf **1,6 bis 2,7 mg/l** (130 g/Tag [Q R47b]). Alles Wasser läuft weiter durch den Biofilter (Buchstabe W53 erfüllt), aber die Hälfte kreist an den Fischen vorbei. Die Gegenmaßnahme (dritte Pumpe je Linie, 164 l/min, Verteiler d63) kostet +50 % Pumpenstrom. **Offen: Fachfrage nach dem nötigen Pool-Durchsatz** (kein Beleg gelesen, ICH, nächste Recherche) und Entscheidung Mitgründer.

## 3. Beet-Rückführung

Ausgangslage [Q]: Beetablauf Z −100 (Port −192 im Bauteilblatt), 615 mm unter Pool-Spiegel; Halbring Tiefpunkt 660, Hochpunkt 720; Beetablauf 47 bis 54 l/min je Beet, höchstens drei Beete gleichzeitig, Mittel 54,5 l/min je Linie (R45, K14).

### 3.1 (i) Sammelring als Schwerkraftleitung

Rechnung [E, Skript Abschn. 3]: Ablauf ≥ Einlaufhöhe + Gefälle × Länge + Rohr d90 + 50 mm.

| Einlauf in den Pool | Weg | Ablauf mindestens | Beet höher um (Ablauf −100) |
|---|---|---|---|
| Halbring-Tiefpunkt Z 660 | direkt 3,5 m, 1 % | 835 | 935 mm |
| Halbring-Tiefpunkt Z 660 | über Sammelring 9 m, 0,5 % | 845 | 945 mm |
| Wanddurchführung Z 540 (25 mm über Spiegel) | direkt | 715 | 815 mm |
| Wanddurchführung Z 540 | Sammelring | 725 | 825 mm |

Bens Schätzung (Ablauf ≥ Z 800) stimmt: **715 bis 845**, also die Beete **0,8 bis 0,95 m höher** (Port-Maß aus dem Bauteilblatt: 0,91 bis 1,04 m). Folgen bei 0,9 m:

- **Beetrand Z 1375, Medium Z 1300:** über Arbeitshöhe (Tritt nötig) [A, Ergonomie ohne Quelle].
- **Außenbeete (r 5,19, Außenkante r 5,72):** Dom-Innenhöhe dort 1818 mm (Kugel R 6,0 m [A, Scheitel 5986, Basis −14, `layout.md`]); über dem Beetrand bleiben **443 mm** statt 1343 mm heute. Fruchtgemüse (Beet 300 mm Medium) hat keinen Platz. Innenbeete (r 3,3) hätten 3257 mm.
- **Gewicht:** 8 Außenbeete (≈1311 kg [A]) + 6 Innenbeete (1065 kg [Q]) = **16,9 t** auf Gestellen von 0,9 m; Gänge (700/600 mm) unverändert, Stützen stehen in den Beeten.
- **NFT-Tische (Z 1000):** unberührt; ein gemeinsamer Sammelring auf Z 725–845 läge unter dem Tischsammler (900) und könnte diesen aufnehmen.

**Ein Sammelring im Kreis ändert die Höhenlücke nicht, nur die Länge.** Ring um r ≈ 4,3 m (27 m Umfang, je Linie ein Halbring 13,5 m) mit Stichen zu 14 Beeten ≈ 44 bis 49 m Rohr gegen 58,9 m K14 radial [E ±25 %, A]. Das ist der Gewinn: −10 bis −15 m, Zugang an einer Stelle. Nur als **glattwandiges Rohr oder Schlauch** (kein Spiralschlauch, Schlamm) und im Bodenkanal.

**Bewertung (i):** Ausfall: keine Pumpe, nur Verstopfung (Siphon-Fehler = Beet voll, Ablaufwächter nötig); Wartung: einfach. **Aber nur mit Beeten 0,9 m höher: nicht empfohlen.**

### 3.2 (ii) Sammelring plus eine zentrale Hebestelle

Statt zwei Beet-Sümpfen ein Sumpf mit drei Pumpen (2 + 1, je 61 l/min, Gesamtspitze 109 l/min). Spart einen Behälter und eine Grube, ersetzt aber zwei unabhängige Linien durch eine gemeinsame Ausfallstelle (bei Leckage fallen beide Linien) und widerspricht der Symmetrie D67 (R47: „zwei Halbringe, nicht ein Ring“). Der Ring liegt unterflur (Kanal): der Ring-Teil verkürzt K14, der Sumpf bleibt unter dem Beetablauf. Wartung: eine Stelle, aber eine Gemeinschaftspumpe. **Nicht einfacher als T.**

### 3.3 (iii) Hebung ohne Elektropumpe: Mammutpumpe/Airlift

Quellen: [Global Seafood, „Airlifts combine pumping, water treatment in recirculation systems“](https://www.globalseafood.org/advocate/airlifts-combine-pumping-water-treatment-recirculation-systems/) (gelesen: Eintauchverhältnis > 80 %, statischer Hub höchstens 30,5 cm, Luft:Wasser > 1 bringt keinen weiteren Sauerstoffeintrag, Niedrigdruck-Airlifts sparen Energie gegenüber Kreiselpumpen); [Patent US 6171480](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6171480) (nur Suchausschnitt: Wirkungsgrad sinkt, wenn das Rohrende über den Spiegel angehoben wird; unter ca. 80 % Eintauchtiefe stark eingeschränkter Durchfluss); [ETASR-Studie, Airlift-Pumpe](https://distantreader.org/stacks/journals/etasr/etasr-1207.pdf) (nur Suchausschnitt: Mindestwert 80 %); [Preßluft-Heber, Charlottenburg 1907](https://ekeving.se/ext/Organ/1907/12.pdf) (nur Suchausschnitt: Wirkungsgrad nicht über 45 %). **Die Grenze „über 80 %, Hub ≤ 0,3 m“ ist belegt (drei Dokumente, eines gelesen); der Wirkungsgrad ist Einzelquelle mit 45 % als Obergrenze.**

Rechnung [E, isotherme Verdichtung, Skript Abschn. 3]:

| Fall | Hub | Eintauchtiefe → Verhältnis | Luft bei η 45 / 25 / 10 % |
|---|---|---|---|
| Beet-Sumpf Linie, Hub bis Halbring (61 l/min) | 1,0 m | 0,8 m → **44 %** | **176 / 317 / 792 l/min** je Linie |
| dito, Hub 0,8 m | 0,8 m | 0,8 m → **50 %** | 141 / 253 / 633 l/min |
| dito, mit 80 %: Sumpf 4 m tief | 1,0 m | 4,0 m → 80 % | 40 / 72 / 180 l/min |
| **Absetzer-Teilstrom (12,5 l/min), Steigrohr K03 bis Zulauf 997** | 0,48 m | 2,55 m → **84 %** | **6 / 11 / 26 l/min** |

- **Beete: nicht tragbar.** Selbst im besten Fall (45 %) braucht eine Linie 176 l/min, mehr als die ganze Anlage fördert (130 Mittel, 205 Spitze, zwei Membranpumpen N+1, 100 bis 215 W [Q Netzliste]). Elektrisch 88 bis 176 W je Linie gegen 54 W der Teichpumpe: **zwei- bis dreimal mehr Strom** (0,5 bis 1,0 W je l/min Luft [A]). Ein Sumpf von 4 m Tiefe (80 %) ist im Dom nicht zu graben.
- **Absetzer-Teilstrom: Kandidat.** Das Steigrohr K03 steht schon, 2,55 m unter dem Spiegel; es müsste von Z 120 bis zum Absetzer-Zulauf (997) verlängert werden und bekäme am Fuß Luft: vier Kleinpumpen (34 W, K04) entfielen, Luftbedarf ≈ 5 bis 11 W Strom. Der Hub (0,48 m) liegt allerdings über den 0,3 m des Leitfadens, und der Rohrdurchmesser d50 ist für 12,5 l/min zu weit [A]: **am Muster messen**, nicht festlegen.
- **Belüftung als Nebeneffekt:** bei den Beeten wertlos (das Wasser geht in den Pool zurück), beim Absetzer vernachlässigbar.
- **Ausfall/Wartung:** kein Laufrad, nichts verstopft durch Schlamm; ein Luftausfall stoppt den Hub, der Absetzer-Teilstrom fällt aus (Hauptkreislauf nicht), N+1 der Luftpumpen gilt.
- **Strahlpumpe aus dem Treibwasser der Beet-Zufuhr:** Treibhöhe 940 mm kleiner als Hub 960 mm, Förderverhältnis null [E].

### 3.4 (iv) Kleiner Pegel- oder Siphonkreislauf

| Form | Wirkung | Urteil |
|---|---|---|
| Schwimmerpumpe im Beet-Sumpf (heute) | zuverlässig, eine Stufe | Standard, bleibt A+ |
| Siphon-Kaskade der Beete in Reihe | nur Gefälle, hebt nicht | gleiche Höhenlücke |
| Siphon als Heber über den Beckenrand | Wasser steigt nie über seinen Quellspiegel (Beet-Wasserstand Z 176 gegen 660) | physikalisch ausgeschlossen [E] |
| Widder-/Strahlpumpe | braucht Treibgefälle ins Freie, es gibt keinen tieferen Auslass | nicht anwendbar |
| **Pegelkreislauf in den Subtank (T)** | Beetwasser fließt frei in den Pumpensumpf der Hauptpumpen, der Pegel (Schwimmer) steuert die Pumpen | funktioniert, Preis siehe 2.4 |

**Ergebnis Abschnitt 3:** Die zweite Pumpstufe ist keine Planungsschwäche, sondern Folge von 615 mm Höhenlücke zwischen Beetablauf und Pool-Spiegel. Streichen lässt sie sich nur, indem man sie in die erste verlegt (T) oder die Beete um 0,9 m anhebt.

## 4. Vergrabungs-Audit

Quelle: `data/leitungstrassen.json`, Segment-Mitte unter Z 0 rel., zwei Linien [E, Skript Abschn. 4]. Summe **30,3 m** (wie R47b). Trassenregel: nichts liegt frei quer im Gang zwischen Z 0 und 2100 [Q m10-leitungen 4.1]; „vergraben“ heißt hier unterflur bei Z −186 bis −2035.

| Abschnitt | m | Muss unterflur? Grund | Oberirdisch / Kanal / Schacht / entfällt | Empfehlung | Folge fürs Gebaute |
|---|---|---|---|---|---|
| **Heber K01/K17** | 2,4 | **ja**: bleibt unter Spiegel (Seitenablauf Z 340, Rohr voll) und quert den Gang (Z −250); direkt oberirdisch bei Z 320–340 läge es 0,34 m hoch quer im Gang | **Kanal mit Gitterrost** (trittfest, bündig); Erde nicht nötig. Alternative Filter an die Poolwand (Heber 0,3 m statt 3,1): Umbau, Gangkarte offen | Kanal + Absperrhahn + Schwimmer (R48 4.7) | Graben-Boolean wird Kanal-Bauteil; Rohr bleibt |
| **Filter-Stamm K06/K22** | 5,5 | nur weil der Filterkasten in der Grube (Z −496) und die Pumpen höher stehen; Stamm bei Z −186 | **entfällt** mit V4 (Korb und Pumpen im Subtank) | V4 | K02, K06, K18, K22 und T-Stücke entfallen |
| **Zweigstücke K02/K18** | 1,6 | zweite Pumpe der Linie | **entfällt** mit V4 | V4 | wie oben |
| **Notbypass K56/K57** | 3,2 | Tiefleitung (Z −659) unter dem Stamm; Totast, Hahn ungetestet | **entfällt** mit V4 (Korb-Überlauf in den Sumpf) [R48: „ersetzt den ungetesteten Totast“; R48 rechnet 23,2 m inkl. dieser 3,2 m, ohne sie 20,0 m] | V4 | K56/K57 und Hähne entfallen |
| **Bodenablauf-Kreis K03/K19** | 10,2 | **ja**: Bodenablauf liegt unter der Pool-Bodenplatte (real Z −1975, nicht −1685 wie Netzliste/R48), das Rohr muss unter dem Becken hinaus (1,35 + 2,4 m bei −2035) und im Steigrohr hoch | Schacht/Revisionsstutzen am Steigrohr (Linie-2-Stumpf ist ein halber Stutzen); **Hub per Luftheber** statt Kleinpumpe (3.3); entfällt nur mit R44 Kandidat A | bleibt; Revision + Luftheber prüfen | nichts, Steigrohr verlängern |
| **Absetzer-Auslauf K05/K21** | 7,3 | **nein**: Auslass liegt auf Z 1147, fällt nur zum Heber-Graben (Z −250), weil die Einmündung dort liegt | **oberirdisch** in der Technikgruppe (Band W erlaubt) direkt in den Subtank/Filter-Einlauf; **0 m** | direkt einleiten | K05/K21 neu verlegen (kürzer) |

**Ergebnis gebaut:** 30,3 m → **20,0 m** (V4) → **12,7 m** (zusätzlich K05 direkt) → **2,4 m** (zusätzlich Absetzerkreis ganz weg, R44 A, Rückbau von K03 bis K05, K19 bis K21).

**Künftige Gräben (noch nicht gebaut) [Q R47 Abschn. 2, E ±25 %]:**

| Strecke | m | Muss unter dem Boden? | Möglichkeit | Empfehlung |
|---|---|---|---|---|
| **K14 Beet-Ablauf-Sammler** (Z −100 bis −192, Gefälle ≥ 0,5 %) | 58,9 | **ja**: liegt unter dem Beetablauf, Schwerkraft zum Sumpf | **Bodenkanal/Sammelrinne mit Rost** (R47b M6), Ring + Stiche statt radialem Fischgräten-Netz (−10 bis −15 m) | Kanal; größte Einzelposition der künftigen Erdarbeit |
| **K58/K59 Beet-Sumpf → Rücklauf** (Druckleitung d40) | 8 | **nein**: Druckleitung | Sumpf an die Poolwand, Förderleitung an der Wandkrone (Band W) | oberirdisch; **entfällt in T** |
| **K11 Beet-Zufuhr, Gangkreuzungen** | ≈ 12 (8 Außenbeete × 1,5 m) [A] | Gang quert: unterflur oder Z ≥ 2100 | Kanal mit Rost (Leerrohr) oder Zufuhr an der Wandseite der Außenbeete entlang [A, Gangkarte nicht geprüft] | Kanal, später prüfen |
| **K13 Bypass** (Verteiler → Halbring, d50) | 2 bis 4 [A] | Gang quert | Kanal | mit K11 |
| K12, K15, K16 (Tischbein, Sektorsammler, Halbring) | – | **nein** | oberirdisch | wie geplant |

Mit allen künftigen Gräben stünden bei A+ heute **109 m** unterflur (30,3 + 58,9 + 8 + 12); mit V4, K05 direkt und Kanal für Heber und K14 bleiben **25 m Erde** (Bodenablauf-Kreis 10,2, Heber 2,4 falls doch in Erde, K11 12) und der Rest liegt zugänglich im Kanal. **Das ist die ehrliche Antwort auf „müssen wir alles vergraben“: nein, nur den Bodenablauf-Kreis (10,2 m) und die Gangquerungen müssen unter den Boden, und selbst die lassen sich als Kanal ausführen.**

## 5. Empfehlung für E20/E21

| Rang | Konzept | Begründung | Bedingung |
|---|---|---|---|
| **1** | **A+ + V4 (Subtank mit Siebkorb und Tauchpumpen) + K05/K21 direkt + Bodenkanal für Heber und K14** | gleicher Strom (430 W), vergrabene Meter 30,3 → 12,7, Einzelpfade 12 → 6, kein Hochbau, M10 S3 nicht blockiert; knüpft an R48 (Rang 2) an | Ben entscheidet E21 (V4 ja/nein); Kanal-Bauteil vor S4 (K14), Heber später nachrüstbar |
| **2** (bedingt) | T Tiefsumpf (Beet-Siphons in den Pumpen-Subtank) | einzige Variante mit **einer** Pumpstufe, 6 statt 8 Pumpen, 4 Einzelpfade, kein Beet-Sumpf, Strom 436 W | nur wenn die Fachprüfung zeigt, dass **halber Pool-Durchsatz** (4,7 Umwälzungen/Tag, TAN-Modell 1,6 bis 2,7 mg/l) reicht |
| 3 | Luftheber für den Absetzer-Teilstrom | −4 Kleinpumpen, passt in den 80-%-Bereich | Muster-Messung (Hub 0,48 m, d50), kein Beleg für diese Größe |
| 4 | Ring-Varianten (B1/b2 Biofilter +660 bis +807 mm) | +95 bis +104 W, Hochbau, vereinfacht nichts | nur falls Gräben K11 nicht lösbar (R47 Auslöser) |
| 5 | Beete auf Stelzen (Schwerkraft-Rückführung); Luftheber für Beete | Außenbeete unbrauchbar, 16,9 t; Luftbedarf über dem Anlagenvorrat | – |

**Als Erstes zu tun:** (1) Ben entscheidet E21: V4 ja/nein (R48 bot es als Option an; dieser Bericht begründet „ja“ über den Vergrabungs-Audit). (2) Vor M10 S4: Entscheidung Kanal mit Rost für K14 statt Erdgraben (neues Bauteil, ICH nach Freigabe, Planer). (3) Absetzer-Luftheber am Muster messen (DEINE HANDLUNG, falls Muster gebaut wird). (4) Fachfrage Pool-Durchsatz für T (ICH).

**Zur Frage „einfachstes naturnahes System“:** Das einfachste, was die Daten tragen, ist **Rang 1**; die Natürlichkeit ist hier schon erreicht (Heber, Verteiler, Beete, NFT und Rücklauf laufen frei, gepumpt wird nur 2,0 m plus 1,47 m). Weiter vereinfachen lässt sich nur, indem man die zweite Stufe in die erste verlegt (T), und das kostet Pool-Durchsatz.

## 6. Abweichungen und Hinweise aus dem Lesen

1. **Bodenablauf real Z −1975** (Trasse abs −1575 minus 400), nicht −1685 wie Netzliste K03 und R48; die Druckhöhe zum Pool-Spiegel ist 2490 statt 2200 mm. Die Schwerkraft-Aussage von R48 (4.3) gilt erst recht [E].
2. **Beet-Tropfrohr:** R47 rechnet Z ~650, das Bauteilblatt `ibc_beet` gibt −162 + 612 = Z 450. Der Kopf wäre 1150 statt 950 mm; ändert nichts am Ergebnis, nur an der Zahl.
3. **R48 V4:** „23,2 m vergraben“ enthält den Notbypass (3,2 m), den der Korb-Überlauf ersetzen soll: ohne ihn **20,0 m**.
4. **B1:** Anhebung rechne ich zu 717 bis 807 mm je nach Ring-Gefälle (R47c: 725); Leistung 534 W (R47c: 549 W, anderer Aufschlag).
5. **Ergebnis T-Pool-Durchsatz und Absetzer-Luftheber:** neue Befunde, nicht in R47/R48.

## 7. Belegstand

| Aussage | Quellen | Stand |
|---|---|---|
| Airlift: Eintauchverhältnis > 80 %, Hub ≤ 0,3 m | Global Seafood (gelesen); Patent US 6171480 und ETASR (Suchausschnitt) | belegt (3), 1 gelesen |
| Airlift-Wirkungsgrad ≤ 45 % | Charlottenburg 1907 (Suchausschnitt) | Einzelquelle |
| Luftbedarf Beet-Heber, Absetzer-Heber | `r49_rechnung.py`, isotherme Verdichtung, η 10 bis 45 % | [E] |
| Höhen, Köpfe, Anhebung Ring | Netzliste, R47/R47c, R48, Skript | [Q]/[E] |
| Trassenregel „nichts frei im Gang“ | `m10-leitungen.md` 4.1, R47 | intern, 2 Dokumente |
| Dom als Kugel R 6,0 m | `layout.md` (Scheitel 5986, Basis −14) | [A] |
| Pool-Durchsatz, TAN-Modell, E je Durchgang | eigene Durchsatzrechnung | [E]/[A], keine Fachquelle |
| Teilearten, Einzelpfade, künftige Gräben, Gewicht Außenbeete | Zählung im Skript | [A] |

**Geprüft gegen:** `docs/arbeitsweise-sitzungen.md` Abschn. 4 und 5; `docs/research/R48-filterreihenfolge.md` (ganz); `docs/research/R47-wasserkreislauf-neu.md` (ganz, R47b, R47c); `docs/berichte/wasserkreislauf-szenarien.artifact.html` Abschn. 5 bis 9; `data/leitungsnetz.json` (Knoten, Kanten K01 bis K59); `data/leitungstrassen.json` (alle Pfade Linie 1 und 2); `scripts/r47_zugang.py`; `docs/parts/ibc_beet.md`, `docs/layout.md`, `docs/packages/m10-leitungen.md` (Auszüge); `python -X utf8 scripts/r49_rechnung.py`; Global Seafood (Volltext), Websuche Airlift (drei Ausschnitte). **Nicht gelesen:** Volltexte von US 6171480, ETASR, Charlottenburg 1907; `docs/walkway-map.md` (Gangkarte); `docs/research/R45` (nur über R47); `scripts/dome-script.json` (Höhen aus Netzliste, Trassen und `layout.md` statt direkt aus dem Skript).
**Offen:** (1) E21: V4 ja/nein und Kanal für K14: DEINE ENTSCHEIDUNG (Ben). (2) Pool-Durchsatz für T (Mindestumwälzung, Biofilter-Wirkung E): Fachquelle fehlt, ICH. (3) Absetzer-Luftheber am Muster: DEINE HANDLUNG, falls ein Muster gebaut wird. (4) Gangkarte für Kanal-Verlauf, K11-Kreuzungen und Stützen: ICH (Planer) nach Freigabe. (5) Dom-Innenhöhe aus dem Modell statt Kugel-Näherung, nur falls Stelzen-Beete weiter betrachtet werden: ICH.

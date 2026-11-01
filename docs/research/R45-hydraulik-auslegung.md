# R45: Hydraulik und Auslegung der Lücken L01, L03, L10, L04, L06, L05

**Auftrag:** `docs/jobs/R45-hydraulik-auslegung.md` · **Rolle:** Fachrecherche (liest, rechnet, schreibt nur diese Datei und `scripts/r45_*.py`) · **Begonnen:** 01.11.2026
**Stand der Fragen:** 0 Schlammkonzept ✔ · 1 Beet-Ablauf ✔ · 2 Heber-Reserve ✔ · 3 Beet-Sumpf ✔ · 4 Belüftung ✔ · 5 Aktivkohle offen
**Kennzeichnung:** [A] Annahme · [E] Schätzung/Rechnung · [Q] belegt mit Quelle. Koordinaten: Z relativ zum Innenboden (Bauskript Z − 400).

---

## 0. Schlammkonzept (L01, Kanten K07 und K23)

**Problem:** Die zwei Absetzer enden mit d40-Kugelhahn im Nichts (`schlammsammler` ist ein Platzhalter ohne Ort). **Intent:** Die Verrohrung soll weitergehen, ohne dass Ben erst entscheiden muss. **Goal:** Eine Standardannahme mit Konzept, Ort, Volumen, Anschluss und Bauteil-Skizze, die der Orchestrator festlegen kann, solange Ben nicht widerspricht.

### Empfehlung (Standardannahme)

**Ein Schlammfass je Linie, in einer Grube neben dem Absetzer, wöchentlich von Hand geleert; Klarwasser zurück in den Pool, Dickschlamm in Wurmkompost/Kompost außerhalb des Kreislaufs. Keinen Reaktor bauen.**

1. **Konzept:** Absetzer spülen alle 2–3 Tage über den Kugelhahn in ein offenes, abgedecktes Fass. Im Fass setzt sich der Schlamm ab. Einmal pro Woche: Klarwasser abheben und in den Pool zurückgeben, den Dickschlamm im Eimer zum Wurmkompost bringen.
2. **Warum kein Reaktor:** Die einzige gelesene Messung (Goddek 2018) zeigt für rein belüftete Reaktoren die schwächste Rückgewinnung (siehe R30, Art 6). Das Fass mineralisiert nichts; es lagert und dickt ein.
3. **Standort:** je Absetzer eine Grube seitlich, **0,7–0,8 m Mitte zu Mitte vom Kegelspitzen-Hahn**. Bauskript-Prüfung (`scripts/r45_schlamm.py`): Absetzer 1 (Tank_klein:1, x 906 / y −3944) frei Richtung tangential Ost (+0,97 / +0,22); Absetzer 2 (Tank_klein:2, x 2842 / y −1652) frei Richtung radial außen (+0,86 / −0,50). Die Pumpen Pumpe_klein stehen auf der Gegenachse, 0,31 bzw. 0,18 m seitlich. **Nur Bauteil-Mittelpunkte geprüft**, Plattformen, Beine und eingegrabene Rohre (z. B. `LT_Rohr_d50_L1451:1` bei Z −188 am Absetzer 2) sind nicht gegengeprüft → Montage prüft die Grube mit `check_leitungen.py`. [E]
4. **Entleerung:** Hand (Klarwasser per Schlauch-Heber oder Tauchpumpe, Dickschlamm per Eimer). Keine Pumpe, keine Schwerkraftleitung nach außen: spart Durchführung durch Fundamentring und Plane und das Frostproblem.

### Zahlen

| Wert | Ergebnis | Rechenweg / Quelle |
|---|---|---|
| Feststoffe je kg Futter | 0,15–0,30 (0,2–0,5) kg TS | [Q] Patentschrift RAS: 150 g TS/kg Futter gesamt, davon 50 g aus Biofiltern ([US 11484015](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11484015)); [Q] Fort Valley/Chen 1997 laut R30: 0,3 (0,2–0,5). Zwei Gruppen, Faktor 2 Spanne |
| Anteil, den der Swirl fängt | 23 % der Tagesmasse | [Q] Davidson & Summerfelt 2005 (über R30, Zusammenfassung gelesen); Original nicht gelesen |
| TS im Swirl | **0,24 kg/Tag** (0,11–0,44) beide Linien | [E] 3,46 kg Futter × 0,30 × 0,23 (`r45_schlamm.py`) |
| Konzentration Frischschlamm | 8,6–10,8 g TS/l | [Q] Goddek u. a. 2018 Tab. 2 (über R30); Gegenprobe: Patent nennt Biofilterschlamm 0,3 % TS, Norwegische Smolt-Anlage 0,7 l **abgesetzter** Schlamm/kg Futter bei 10 % TS (Patent-Suchtreffer, nicht im Volltext gelesen) |
| Schlammvolumen | **22–28 l/Tag beide Linien, 11–14 l/Tag je Linie** (Obergrenze 26 l je Linie bei 0,5 kg TS/kg Futter) | [E] 0,239 kg ÷ 8,6–10,8 g/l → deckt sich mit dem Auftragsblatt (22–28). Bestätigt, aber beide Eingaben haben nur je eine Quelle für die Konzentration |
| Spülwassermenge je Spülung | 20–40 l je Linie | [A] Hahn nicht auf Sekunden steuerbar; 30 l in 13–16 s bei 133 bzw. 112 l/min (Torricelli d40, Innen-Ø 34 mm, Cd 0,6 [A]) |
| Wochenmenge im Fass | 70–105 l je Linie (Spülung 30 l alle 2–3 Tage), Spanne 47–140 l | [E] `r45_schlamm.py` |
| TS je Woche | 1,67 kg beide, 0,84 kg je Linie | [E] |
| Wurmbett | **≥ 1,25 m², empfohlen 2,5 m²** (beide Linien) | [Q] Mishra 2003, Virginia Tech: Sandfilterbett mit *Eisenia fetida* arbeitete bei 1000 g flüchtiger Feststoffe/m²/Woche, höhere Raten nicht getestet; [A] VS = 75 % der TS, Sicherheit 2 |
| Mischung | 15–50 % Schlamm-TS (trocken) mit Karton, 80 % Feuchte; bei 25 %: 5 kg Karton trocken/Woche → 33 kg Mischung | [Q] Mishra 2003: 15/25/50 % Fischschlamm + Karton, Wurmbiomasse stieg mit dem Schlammanteil, Sterblichkeit null im zweiten Versuch |
| Wurm-Randbedingungen | 15–25 °C, Optimum 25 °C; 70–85 % Feuchte; Ammoniak und Salz sind giftig | [Q] Mishra 2003 (Literaturteil); [Q] Suchtreffer PMC7084763 (*E. fetida* an Klärschlamm, 15/20/25 °C, schnellste Stabilisierung bei 25 °C) |

**Zweite Quelle für Wurmkompost von RAS-Schlamm:** Studie mit *Eisenia andrei* an RAS-Fischschlamm, Aquaponik-Salatresten und Eierkartons: Schwermetalle sanken, Produkt als sicher für Landwirtschaft bewertet (Agronomy 2026, 16(4):473, [MDPI](https://www.mdpi.com/2073-4395/16/4/473); beste Mischung Schlamm : Eierkarton : Salat = 4 : 5 : 1). **Nur über Suchzusammenfassung gelesen, Volltext offen.**

### Gefahr und Absicherung (wichtig für Steuerung/Werkstatt)

**Bleibt der Kugelhahn offen, läuft der Pool leer:** Pumpe_klein fördert 12,5 l/min in den Absetzer, ein offener d40-Hahn leert ihn in ca. 2 min und der Pool verliert danach 750 l/h [E, `r45_schlamm.py`]. Gegenmaßnahme als Standardannahme: **Kugelhahn mit Federrückzug oder Totmann-Hebel** [A: Verfügbarkeit im Standardmaß nicht geprüft] und Pegelschalter im Pool (Steuerung). Entscheidung Orchestrator/Werkstatt.

### Bauteil-Skizze für die Werkstatt: `schlammfass` (zwei Stück)

| Merkmal | Maß | Anmerkung |
|---|---|---|
| Behälter | Kunststoff-Spannringfass 200–220 l, Ø ≈ 0,58–0,60 m, H ≈ 0,88–0,92 m | [A] Handelsmaß, nicht gegengeprüft (W43: Standard). Fassung: 105 l/Woche plus Reserve |
| Grube | Ø 0,8 m, Tiefe ≈ 0,95 m, Fassoberkante ≈ Z 0…+20 | Hahn sitzt bei Z ≈ +150 (Tank_klein.json Fitting 166 / 177) |
| Einlauf | Deckel mit Stutzen d40, Mitte; Rohr d40 von Hahn waagerecht 0,7 m mit Gefälle 5 % (35 mm), Bogen 90°, Fallrohr 0,1 m | Gefälle ≥ 2 % genügt [A, Foren uneinig, Norm nicht gelesen]; hier genug Höhe |
| Entlüftung/Luft | Deckel mit Bohrung Ø8 für Luftschlauch (optional Luftstein, Menge offen → Frage 4) und Entlüftung Ø20 | Geruch: nur bei Luft aerob; Luft dient nicht der Mineralisierung |
| Auslass | keiner; Entleerung von oben | spart Durchführung und Frostschutz |
| Material | PE (Fass), PVC-U (Rohr/Hahn) | |

### Netz-Änderung (Vorschlag, nicht von mir geändert)

`schlammsammler` → `schlammfass_1` und `schlammfass_2` (Linien bleiben getrennt, Abstand der Absetzer 3,0 m). K07/K23: d40, 0,7 m, Gefälle 5 %, Soll 30 l je Spülung statt „0,5 l/min“ (0,5 l/min ergibt 720 l/Tag und ist falsch gegen 11–14 l/Tag).

### Offene Punkte Frage 0

1. Konzentration des **Swirl**-Schlamms im Fass gemessen (Goddek-Wert gilt für Frischschlamm anderer Anlagen); messen in der ersten Betriebswoche (Besitzer: Betrieb).
2. Davidson & Summerfelt (23 %) und Agronomy 2026 im Original lesen (ICH, nur bei Bedarf).
3. Federrückzug-Hahn: Fabrikat und Maß (Werkstatt).
4. Ort der Wurmkiste (Außenbereich/Nebengebäude): D69, Ben/Orchestrator; 2,5 m² nur als Flächenbedarf.
5. Kollision der Grube mit eingegrabenen Rohren (Montage, `check_leitungen.py`).

**Geprüft gegen:** `docs/filter-konzept.md` Art 6, `docs/research/R30.md`, `data/leitungsnetz.json` (K05–K07, K23, Knoten), `data/components/tank.json`, `data/layout.json`, `scripts/dome-script.json`, `docs/loop-state.md`, Mishra 2003 (Volltext), Patent-/Such-Zusammenfassungen · **Rechnung:** `python -X utf8 scripts/r45_schlamm.py`, `scripts/r45_umgebung.py`

---

## 1. Beet-Ablauf d25 gegen d40 (L03, K14/K30)

**Problem:** `ibc_beet.md` hat Port/Standrohr d25, die Netzkanten K14/K30 rechnen d40; bei d25 liegen 36 l/min bei 1,58 m/s (Grenze 1,5). **Intent:** Blockade für S3/S4 lösen. **Goal:** Eine Maßentscheidung mit Geschwindigkeit, Verlust und Standardmaßen.

### Empfehlung

**Bauteil bleibt d25. Das Netz ändert sich: Einzelabgang d40 direkt unter dem Bulkhead, Sammelleitung K14/K30 von d40 auf d50.** Zwei Befunde tragen das:

1. **Die Grenze 1,5 m/s gilt nicht für das Standrohr.** Sie ist die Netzkonvention für Druckleitungen [A, `leitungsnetz.json` Konventionen]. Das Standrohr eines Glockensiphons läuft voll und seine Geschwindigkeit folgt aus der Druckhöhe: 1,7–2,4 m/s bei h = 0,3–0,6 m ist Siphon-Physik, kein Auslegungsfehler. Rechnung: Energiegleichung mit Eintritt K 0,5, Austritt K 1,0, Darcy-Weisbach (λ nach Swamee-Jain, PVC k 0,0015 mm [A]) in `scripts/r45_beetablauf.py`.
2. **Die d25-Standrohr-Kapazität passt zum Beet, die Spitze ist aber höher als im Netz:** d25 (Innen-Ø 22,0 mm) lässt **38 l/min (h 0,30 m), 47 l/min (0,45 m), 54 l/min (0,60 m)** durch, 234 l laufen in 4,3–6,1 min ab. Das Netz rechnet mit 36 l/min; **zu rechnen ist 47–54 l/min je Beet** [E].

| Variante | Ablauf Beet (234 l) | Standrohr-Geschwindigkeit | Folge |
|---|---|---|---|
| **A: d25 Standrohr (Bauteil heute)** | 4,3–6,1 min, 38–54 l/min | 1,7–2,4 m/s | Bauteil unverändert; passt zu R03 (Glocke d75, Verhältnis 3 : 1) |
| B: d32 Standrohr | 2,4–3,4 min, 68–97 l/min | 1,7–2,5 m/s | Bulkhead, Glocke und Medienschutz ändern sich; Spitze 70–100 l/min je Beet im Sumpf; kein Gewinn |
| C: d40 Standrohr | 1,5–2,1 min, 111–158 l/min | 1,8–2,6 m/s | Glocke ≥ d90–110, Medienschutz wächst, Bett wird zu schnell leer; abgelehnt |

Variante A gewinnt, weil nur das Netz sich ändert. Die Geschwindigkeit sinkt nicht durch ein größeres Rohr, sondern wird von der Druckhöhe bestimmt (B und C laufen genauso schnell, nur mit mehr Wasser).

### Maße für Werkstatt und Montage (Standardmaße, W43)

| Strecke | Maß | Innen-Ø | v bei 1 Beet (47 l/min) | Quelle |
|---|---|---|---|---|
| Standrohr im Beet | PVC-U d25 × 1,5 | 22,0 mm | 2,06 m/s (Siphon) | [Q] EN 1452 SDR 21: [Engineering Toolbox](https://www.engineeringtoolbox.com/EN-1452-PVC-U-pipes-d_2142.html) 1,5 mm; Händlerblatt PN10 25 × 1,5 ([Bevo](https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-5-mm-glue-socket-x-plain-10bar-iso-pn10-grey-5m-0309025)) |
| Einzelabgang je Beet | PVC-U d40 × 1,9, ≤ 0,5 m, Gefälle ≥ 2 % [A] | 36,2 mm | 0,76 m/s | EN 1452 (Engineering Toolbox) |
| Sammelleitung K14/K30 | **PVC-U d50 × 2,4** (statt d40) | 45,2 mm | 0,49 m/s; 2 Beete 0,98 m/s; 3 Beete 1,46 m/s | EN 1452 (Engineering Toolbox), Rechnung |
| Übergang unter dem Boden | Reduzierung d40/d25 (Bibliothek hat d40/d32 und d32/d25 → zwei Stück, oder Muffe d25/d40 als Sonderteil) | | | `data/components/leitungsteile.json` |

Die Sammelleitung braucht d50, weil sich Abläufe überlappen: 7 Beete je Linie × 2 Flutungen/h × 5 min Ablauf = 70 min Ablaufzeit je Stunde → mindestens zwei Siphons laufen oft gleichzeitig. In d40 ergeben 2 Beete 1,5–1,7 m/s, 3 Beete 2,3 m/s; in d50 bleibt es bis 3 Beete bei 1,46 m/s (`r45_beetablauf.py`). **Steuerung/Staffelung: höchstens 3 gleichzeitig.**

### Verlust

Stutzen d25 0,1 m + Aufweitung auf d40: ca. 0,2 m Wassersäule bei 36 l/min [E]; sie zehrt von der Siphon-Druckhöhe, ist in der Kapazitätsrechnung oben bereits als Austrittsverlust enthalten und verlängert den Ablauf um wenige Sekunden. Entscheidend ist, dass **hinter dem Bulkhead kein Rückstau entsteht**: Einzelabgang und Sammler laufen mit Gefälle und Lüftung nach unten frei in den Beet-Sumpf (Frage 3), nicht voll.

### Zweite Quelle für die Siphon-Auslegung

Glockensiphon-Faustregeln: Glocke etwa doppelt so groß wie das Standrohr; Zulauf muss kleiner sein als die maximale Ablaufrate ([my-aquaponics-experiment](https://my-aquaponics-experiment.blogspot.com/2016/01/research-bell-siphons.html), [vectree.io](https://vectree.io/pdf/c/auto-siphon-physics-and-fluid-mechanics-of-bell-siphons-in-flood-and-drain-systems), beide Suchzusammenfassungen); Voll-Lauf-Schwelle für luftgeregelte Siphons Q > 10,2 · D^2,5 (gpm, D in Zoll): d25 ≈ 27 l/min, wir liegen mit 38–54 l/min darüber ([industrialmonitordirect](https://industrialmonitordirect.com/blogs/knowledgebase/sizing-air-regulated-covered-siphons-for-water-treatment-pilot-plants), Wasseraufbereitung, nur grobe Näherung). **Zwei schwache Quellen, die Physik (Bernoulli/Darcy-Weisbach) trägt die Zahl.** Messung am gebauten Beet ersetzt sie.

### Offene Punkte Frage 1

1. Echte Druckhöhe h im Beet (Wasserstand Z 365 bis Austritt) aus dem Modell: Austrittshöhe hängt vom Sumpf-Deckel (Frage 3).
2. Rauheit und Verlustbeiwerte [A] (Lehrbuchwerte, nicht im Volltext belegt).
3. Staffelung max. 3 gleichzeitig: Steuerung.
4. `leitungsnetz.json` K14/K30 auf d50 und Spitze 47–54 l/min: Orchestrator (ich ändere die Datei nicht).

**Geprüft gegen:** `docs/parts/ibc_beet.md` (Standrohr d25, Bulkhead D36, Glocke d75), `data/leitungsnetz.json` K11–K15, F3, EN 1452 (Engineering Toolbox), Bevo-Datenblatt, Siphon-Zusammenfassungen · **Rechnung:** `python -X utf8 scripts/r45_beetablauf.py`

---

## 2. Heber-Reserve K01/K17 (L10)

**Problem:** Der Seitenablauf Pool (Z 740) führt über einen Graben (Z 150) zum Feinfilter-Einlauf (Z 720); `heber_rechnung.py` nennt 27–81 mm Reserve gegen 195 mm Druckhöhe (Grenze 30 mm). **Intent:** Entscheidung für Ben (E14), ob das so gebaut bleibt. **Goal:** Nachrechnung mit dem verlegten Stand, zwei Quellen für die Verlustbeiwerte, Varianten mit Wirkung in mm.

### Ergebnis

**Die Reserve hängt fast allein vom Bogen-Verlustbeiwert ab, und der ist für verklebte PVC-Bögen in keiner meiner Quellen belegt. Bauen auf „es reicht“ ist nicht gedeckt. Empfehlung: durchgehend d75 statt d63 für K01/K17.**

Verlegter Stand (`data/leitungstrassen.json`): K01 3036 mm Rohr (1366 vor, 1671 hinter dem Absetzer-T), K17 2245 mm (1116 + 1130); je Linie **4 Bögen 90°, 2 T im Durchgang**, Strom 97,5 l/min vor und 110 l/min hinter dem Absetzer-T, Rohr d63 × 3,0 (Innen-Ø 57,0 mm), Eintritt 0,5, Austritt 1,0. Rechnung `scripts/r45_heber.py` (Darcy-Weisbach, Swamee-Jain, Rauheit neu 0,0015 mm / gealtert 0,05 mm).

| Fall (Bogen / T) | Quelle | K01 Reserve | K17 Reserve |
|---|---|---|---|
| Langbogen flanschgleich 0,2 / T 0,2 | [Q] [Engineering Toolbox](https://www.engineeringtoolbox.com/minor-loss-coefficients-pipes-d_626.html) | 99–102 mm | 107–110 mm |
| Standardbogen 0,3 / T 0,2 | [Q] Engineering Toolbox | 89–93 mm | 98–100 mm |
| glatter Bogen 30 fT = 0,57 / T 20 fT = 0,38 | [Q] Crane TP-410 (fT 0,019 [A]; Bogen nach [MathWorks-Doku](https://www.mathworks.com/help/hydro/ref/elbowil.html), T-Wert nicht gegengelesen) | **56–59 mm** | **64–66 mm** |
| Langbogen gewindet 0,7 / T 0,9 | [Q] Engineering Toolbox | **19–22 mm** | **27–30 mm** |
| Gehrungsbogen 60 fT = 1,14 / T 0,9 | [Q] Crane (Gehrung), Engineering Toolbox (T) | **−22…−19 mm** | **−14…−11 mm** |

Die Spanne je Zelle ist neu gegen gealtert. **Befund:** In den zwei ungünstigen Fällen (scharfkantige Klebebögen mit großem Beiwert) reicht die Druckhöhe nicht; der Ablauf würde dann weniger als 110 l/min liefern. Die tatsächlichen Beiwerte der gebauten Teile (Klebebögen SDR 21, Innenkante scharf) liegen vermutlich zwischen „glatt“ und „Gehrung“ [A]. Der Herstellerwert (Georg Fischer, PVC-U-Planungsgrundlagen) ist **nicht abrufbar gewesen** (PDF zu groß, Suchtreffer ohne Zahlen) → offen.

### Varianten (Rauheit gealtert, Reserve in mm; „schlecht“ = Gehrungsbogen/T 0,9, „Mittel“ = Crane glatt)

| Variante | K01 schlecht | K01 Mittel | K17 schlecht | K17 Mittel | Aufwand |
|---|---|---|---|---|---|
| Ist (d63, 4 Bögen) | −22 | 56 | −14 | 64 | — |
| **d75 × 3,6 durchgehend** (Innen-Ø 67,8; 2 Reduzierungen d75/d63 an Pool-Stutzen und Filter-Einlauf, K 0,3 [A]) | **85** | **124** | **88** | **127** | Rohr, Bögen, T und Muffen von d63 auf d75 (Standardmaß, Bibliothek d20–d110) |
| Langbogen (Beiwert 0,2) statt Klebebogen | 66 | 90 | 74 | 99 | gebogene Rohrstücke oder 2 × 45° mit Zwischenstück; mehr Platz im Graben |
| Filtergrube 100 mm tiefer | 78 | 156 | 86 | 164 | Modelländerung Grube/Filter-Stamm K06; Saugleitung zur Pumpe liegt tiefer |
| d75 + Langbogen | 129 | 141 | 132 | 145 | beide Aufwände |
| Pumpe statt Heber | — | — | — | — | ca. 18 W je Linie bei 0,25 m und 25 % Wirkungsgrad [E], dazu Trockenlaufschutz, Steuerung, weitere Fehlerquelle |

### Entscheidungsvorlage für Ben (E14)

1. **Empfohlen: d75 durchgehend.** Reserve ≥ 85 mm auch im ungünstigsten Fall, ändert keine Höhenlage, nur Rohrmaß. d75 ist Standardmaß (W43). Folgen: Reduzierung an Pool-Stutzen (d63) und Feinfilter-Einlauf (d63); K05-T (Absetzer-Zulauf d50) und Notbypass-T K56 werden d75/d50/d75 bzw. d75/d63/d75.
2. Alternative: Filtergrube 100 mm tiefer, kein neues Rohrmaß, aber Eingriff in Filter-Stamm und Pumpen-Saugseite.
3. Nicht empfohlen: Pumpe (Energie und Ausfallrisiko ohne Not), unveränderter Bau (ungedeckte Reserve).
4. Zu beachten: Der Seitenablauf Z 740 bleibt, weil die Überdeckung gegen Wirbel 171 mm bei d63 verlangt (Frage F2 der Netzliste); bei d75 ist der Einlauf langsamer (Fr kleiner), also kein neues Problem.

### Offene Punkte Frage 2

1. Verlustbeiwert verklebter PVC-U-Bögen/T d63 vom Hersteller (Georg Fischer Planungsgrundlagen oder Datenblatt des gekauften Fabrikats): Besitzer Beschaffung/Werkstatt; dieser Wert entscheidet, ob d63 doch reicht.
2. Crane-Werte nur über Zusammenfassung belegt (MathWorks), T-Durchgang 20 fT unbestätigt.
3. Grenze 30 mm ist Projektannahme; Spiegelschwankung (Verdunstung, Beet-Flutung) nicht berücksichtigt: 10 mm Spiegelabsenkung kosten 10 mm Reserve.
4. Messung am gebauten Heber (Wasserstandsdifferenz Pool/Filter bei 110 l/min) ersetzt die Rechnung.

**Geprüft gegen:** `scripts/heber_rechnung.py`, `data/leitungstrassen.json` (K01, K01-m, K01-b, K17, K17-m, K17-b), `docs/loop-state.md` (Befund 3), Engineering Toolbox Verlustbeiwerte, MathWorks/Crane-Zusammenfassung, EN 1452-Wandstärken (Engineering Toolbox) · **Rechnung:** `python -X utf8 scripts/r45_heber.py`

---

## 3. Beet-Sumpf (L04, F3)

**Problem:** Der Beet-Ablauf liegt ca. 600 mm unter dem Pool-Spiegel (Beetablauf Z −100, Rücklauf-Sammelrohr oberhalb Z 515); ohne Sumpf mit Pumpe kommt das Beetwasser nicht zurück. **Intent:** Werkstatt (W37) baut den Sumpf, Montage (S4) legt ihn an. **Goal:** Volumen, Pumpe, Förderhöhe, Schwimmerhöhen, Abdeckung und Leistung für `system_specs.py` (nur melden).

### Empfehlung

**Je Linie ein eingegrabener Rundtank 500 l (nicht 300 l), eine Teichpumpe 5300 l/h / 60 W (Hmax 2,8 m) mit Rückschlagventil, drei Schwimmerschalter (AUS, EIN, Alarm), dichter lichtdichter begehbarer Deckel. Die Flutsperre bei „Alarm“ ist Pflicht.**

| Punkt | Wert | Herleitung / Quelle |
|---|---|---|
| Volumen | **500 l nutzbar-brutto** (z. B. Ø 0,8 m × 1,0 m, 1 cm Pegel = 5 l); 300 l reichen nur bei einzeln gestaffelten Abläufen | [E] `r45_sumpf.py`: 1 Beet je 4,3 min Spitze 25 l; **2 Beete gleichzeitig** Spitze 168 l; 3 gleichzeitig 405 l; dazu Totvolumen ca. 50 l und Schalthysterese 100 l → 318–590 l je nach Staffelung |
| Pumpe | Teichpumpe **5300 l/h bei 0 m, Hmax 2,8 m, 60 W**, Korn ≤ 8 mm (Beispiel: OASE AquaMax Eco Classic 5500) | [Q] Händlerangaben ([OBI](https://www.obi.de/p/1358613/oase-filter-und-bachlaufpumpe-aquamax-eco-classic-5500), [topratgeber24](https://www.topratgeber24.de/amp/teichpumpe/oase-51096-filter-und-bachlaufpumpe-aquamax-eco-classic-5500)); Kennlinie nicht gefunden, parabolisch angenommen [A] |
| Arbeitspunkt | **61 l/min bei 1,47 m** (statisch 1,25 m, Förderleitung d40 4 m, 2 Bögen + Rückschlagventil); Spanne 56–66 l/min für 1,0–1,5 m statisch | [E] Pumpenkennlinie gegen Anlagenkurve (Darcy-Weisbach, `r45_sumpf.py`) |
| Förderhöhe statisch | 1,0–1,5 m | [A] vom Sumpf-Wasserspiegel bis zum Rücklauf-Sammelrohr oberhalb Z 515; Lage des Rohrs an der Einspeisestelle ist M10 S4 |
| Leistung elektrisch | **60 W je Pumpe; Laufanteil 90 % → 54 W Mittel je Linie, 108 W beide, 2,6 kWh/Tag** | [E] Netzannahme war 36 W (25 %, 54,5 l/min bei 1,0 m): trägt nur bei η 25 % und ohne Rohrverlust; hier hydraulisch 14,6 W bei 24 % Wirkungsgrad |
| Förderleitung | PVC-U d40 × 1,9 (v 0,99 m/s), Kugelrückschlagventil d40, ≤ 4 m | EN 1452 (siehe Abschnitt 1) |
| Schaltspiel | Hysterese 100 l (200 mm) → 3,4 Starts/h, Pumpe 16 min an, 1,8 min aus | [E]; Praxis: Hysterese über Schwimmerkabel/Gewicht einstellbar ([HTWK-Leipzig-Pumpensumpf-Unterlage](https://ing-ebit.htwk-leipzig.de/fileadmin/portal/m_feit_ebit/Bilder/Forschung/Kompetenzen/Elektromedizinische_Technik/Unterlagen-Sammlung/Abpumpanlage.pdf), Forenbeiträge); keine Norm-Grenze für Starts/h gefunden |

### Pegelhöhen (Ø 0,8 m, Pegel über Tankboden)

1. **AUS** bei 120 mm (60 l): Pumpe bleibt eingetaucht, Totvolumen.
2. **EIN** bei 320 mm (160 l): Hysterese 200 mm = 100 l.
3. **ALARM / Flutsperre** bei 620 mm (310 l): Steuerung sperrt die Beet-Zufuhr (K11/K27) und meldet; bei Pumpenausfall laufen sonst ca. 705 l in 12 min zu (3 Beete), das ist mehr als der Tank fasst.
4. Einlauf-Rohrsohle (Sektorsammler) bei 800 mm; **höchster Wasserstand bleibt darunter**, damit nichts zurückstaut in die Beet-Siphons (Gegendruck bremst den Siphon, Abschnitt 1).

Es gibt **keinen Schwerkraft-Notüberlauf** (der Sumpf liegt tiefer als der Pool). Deshalb: Alarmschwimmer an die Steuerung, optional Doppelschwimmer und eine zweite Pumpe als Reserve (50 % Redundanz, +60 W Stillstand) [Empfehlung, Entscheidung Ben].

### Abdeckung (Geruch, Algen)

Deckel dicht, lichtdicht (kein Licht → keine Algen), begehbar (Standard-Pumpenschacht mit Deckel, [A] Handelsmaß nicht gegengeprüft). Verdrängungsluft über Entlüftung d32 mit Insektengitter; wegen Umsatz von 55 l/min bleibt das Wasser frisch, Geruch entsteht nur bei Pumpenausfall. Kabel- und Förderleitungsdurchführung mit Dichtung. Aktivkohle-Entlüftung nicht nötig [E].

### Bauteil-Skizze `beet_sumpf` (je Linie)

| Merkmal | Maß |
|---|---|
| Tank | PE rund Ø 0,8 m × H 1,0 m, ca. 500 l; Grube Ø 1,0 m, Tiefe 1,0 m, Deckel bündig oder + 0,05 m |
| Zulauf | d63 Sektorsammler (M10 S4) bei 800 mm, Gefälle ≥ 1 % [A] |
| Auslauf | Förderleitung d40 oben aus dem Deckel, Rückschlagventil, Weiterführung zum Sammelrohr (Abschnitt 1 Maße) |
| Einbauten | 1 Pumpe, 3 Schwimmerschalter an Stange, Kabeldurchführung, Entlüftung d32 |
| Anschluss Strom | 230 V, 60 W; Steuerung Pegel + Flutsperre (Schaltschrank) |

### Meldung für `scripts/system_specs.py` (nicht geändert)

2 zusätzliche Verbraucher à 60 W (Mittel 54 W), also **108–120 W, 2,6–2,9 kWh/Tag** gegen 72 W in der Netzliste (2 × 36 W).

### Offene Punkte Frage 3

1. Echte Pumpenkennlinie (OASE-Datenblatt) und tatsächliche Förderhöhe (Einspeisehöhe am Sammelrohr): Werkstatt/Montage.
2. Zwei Beete gleichzeitig ist der Planfall; Steuerung muss die Staffelung erzwingen (max. 2 gleichzeitig).
3. Redundanz-Pumpe: Entscheidung Ben (Kosten/Verfügbarkeit D69 nicht Thema).
4. Pumpenschacht-Fabrikat und Deckelklasse: Werkstatt.

**Geprüft gegen:** `data/leitungsnetz.json` (K14/K16/K30/K32, F3), `data/roadmap.json` (L04), `docs/parts/ibc_beet.md`, Abschnitte 1 und 2, Händlerseiten Pumpe, HTWK-Unterlage · **Rechnung:** `python -X utf8 scripts/r45_sumpf.py`

---

## 4. Belüftung (L06, K44 bis K51, F4)

**Problem:** F4 der Netzliste hat zwei Rechnungen für den Pool-Luftbedarf, 70–130 l/min (R28) und 25–63 l/min (Gegenrechnung mit OTE 13 %). **Intent:** Gebläse und Verteiler festlegen, ohne dass der Pool bei Ausfall oder Spitze unterversorgt ist. **Goal:** Welche Rechnung stimmt, Gebläseart, Druck, Leistung, Verteiler, Ventile, Ausströmer.

### Ergebnis

**Die 130 l/min für den Pool sind plausibel (Mittelfall), die 25–63 l/min sind zu klein.** Der Fehler der Gegenrechnung: OTE 13 % ist die Reinwasser-Kennzahl (SOTE, 20 °C, 0 mg/l Sauerstoff). Im Fischwasser bei 28 °C und 5 mg/l Sollwert sinkt sie auf ca. 2–4 % (AOTE). Rechnung `scripts/r45_luft.py`:

| Annahme | Wert | Quelle |
|---|---|---|
| SOTE feinblasig | 6–7,5 % je m Einblastiefe (Reinwasser, Vollbelegung); Pool-Tiefe 2,17 m → 13–16 % | [Q] [wastewater.com](https://wastewater.com/field-performance-of-fine-and-ultra-fine-bubble-diffusers/); Gegenprobe Default 6 %/m in [aquakin-Doku](https://aquakin.readthedocs.io/en/latest/generated/aquakin.AerationSystem.html) |
| alpha (Abwasser/Membran) | 0,49 bis 0,8 | [Q] wastewater.com 0,49; Obergrenze 0,8 [A, gereinigte Membran] |
| Temperatur/Sauerstoff-Korrektur | (β·Cs,28 − 5) / Cs,20 · 1,024⁸ = 0,32 | [A] Cs 7,83/9,09 mg/l (Tabellenwerte, nicht neu gelesen), β 0,95, θ 1,024 (wastewater.com) |
| Sauerstoff je Liter Luft | 0,27 g | [E] 23,2 % × 1,16 kg/m³ |
| AOTE | 2,1–4,2 % | [E] |

| Sauerstoffbedarf (system-specs) | Luft Pool l/min | mit Spitze ×1,5 |
|---|---|---|
| nur Fisch 0,7 / **1,1** / 1,6 kg/Tag | 43–87 / **67–137** / 97–199 | 64–131 / 101–205 / 146–298 |
| Fisch + Nitrifikation 1,3 / 1,7 / 2,2 kg/Tag | 79–162 / 104–211 / 134–273 | bis 410 |

Der Pool belüftet den **Fisch** (Nitrifikation läuft in Biofilter und Beeten, die eigene Luft haben). Mittelfall 67–137 l/min, also trägt **130 l/min Planwert**; die Spitze braucht bis 205 l/min. Beide Unsicherheiten (alpha, Cs) sind [A]; der Wert gilt bis zur Messung des Sauerstoffs im Betrieb.

### Empfehlung

1. **Gebläseart:** Linear-Membranpumpe (Teich-/Klärtyp), **nicht** Seitenkanal. Seitenkanalgebläse beginnen bei deutlich größeren Mengen [A, nicht belegt]; Membranpumpen decken 100–250 l/min bei 17–30 kPa, 42–48 dB, ca. 100–250 W ([Hiblow-Daten HP-200 / HP-120LL, Händlerseiten](https://hydrobuilder.com/products/hiblow-hp-200-linear-air-pump-200-liters-per-minute) und [septicsolutions](https://www.septicsolutions.com/septic-parts/pond-aeration/pond-aeration-pumps/hp200p_hiblow-hp-200-linear-air-pump-for-pond-aeration): HP-200 200 l/min bei 20 kPa, 250 W; HP-120LL 120 l/min bei 17,7 kPa, max. 30 kPa, 100 W).
2. **Zwei Gebläse (N+1), jedes allein für den Pool-Planwert ausreichend.** Ausfall ohne Luft: **0,8–1,2 h** bis 3 mg/l bei 5–6 mg/l Start und 1,7 kg O₂/Tag (28,5 m³) [E], bei Spitze 0,5–0,8 h. Ohne Redundanz und Notstrom ist das ein Totalverlust-Risiko.
3. **Druck:** statisch 21,3 kPa (2,17 m) + Ausströmer/Leitung 3–5 kPa = **24–26 kPa** [E]. Das liegt **über dem Nennpunkt 20 kPa** der Katalogwerte; die Menge bei 26 kPa ist nicht belegt (Kennlinie nur als Grafik). Elektrisch grob 100–140 W für 130 l/min, 150–215 W für 200 l/min [E, adiabat, Wirkungsgrad 40–50 %] gegen 204 W in `system_specs.py`.
4. **Auslegung:** zwei Geräte der Klasse 200 l/min bei ≥ 26 kPa. Die Kennlinie bei 26 kPa ist **offen** und entscheidet, ob HP-200 genügt (200 l/min sind bei 20 kPa belegt, bei 26 kPa weniger [A]); falls nicht, nächste Größe oder Ausströmer höher setzen (jeder halbe Meter weniger Tiefe spart 5 kPa, kostet aber SOTE).
5. **Verteiler:** Hauptverteiler **6-fach** am Gebläse (Pool, Biofilter 1, Biofilter 2, Drittbecken, Zweitbecken, Puffer/Absetzer), je Abgang Kugelhahn und Rückschlagventil; Pool-Verteiler **4-fach** am Becken (vier Scheibenbelüfter, je ca. 33 l/min). Absetzer-Anschlüsse K47/K48 bleiben optional.
6. **Ausströmer:** EPDM-Membran-Scheibenbelüfter Ø 215–270 mm [A, Handelsmaß] (Pool 4 Stück, Biofilter Rohr-/Plattenbelüfter); Membranausströmer arbeiten feinblasig, wie in der SOTE-Rechnung vorausgesetzt.
7. **Rückschlagventil und Schleife:** Luftleitung vom Gebläse **über dem höchsten Wasserspiegel** (Z > 515 + Reserve) führen und zusätzlich Rückschlagventil, sonst läuft Wasser bei Stillstand in das Gebläse zurück (Gebläse liegt im Schaltschrankbereich unter dem Spiegel) [A, übliche Regel, zweite Quelle offen].

### Kanten K44–K51 (Vorschlag)

| Kante | heute | Vorschlag |
|---|---|---|
| K44 Pool | d40, 120 l/min [A] | d40, **Planwert 130, Spitze 205 l/min** (3,2 m/s bei 200 l/min, Innen-Ø 36,2 mm); Pool-Verteiler 4-fach |
| K45/K46 Biofilter | d25, offen | **offen**: Nitrifikationsbedarf wird großteils vom Umlauf gedeckt (110 l/min je Linie × 6 mg/l = 0,95 kg O₂/Tag je Linie [E]); Luft dient Durchmischung und Restsauerstoff, Menge nach Trägerhersteller (K1) |
| K47/K48 Absetzer | d20 optional | optional (Schlammfass-Luftstein siehe Abschnitt 0) |
| K49 Drittbecken | d20, 2 l/min | bleibt; **Notstrom** (nicht am Hauptgebläse) |
| K51 Zweitbecken | d20, offen | offen, wenige l/min [A] |

### Offene Punkte Frage 4

1. Kennlinie des gewählten Gebläses bei 26 kPa (Datenblatt): Werkstatt/Beschaffung.
2. alpha und Cs durch Messung im Betrieb ersetzen (ersten Sauerstoff-Verlauf ohne Gebläse messen).
3. Biofilter-Luft (K45/K46) und Zweitbecken: Hersteller der Träger.
4. Notstromkonzept (Batterie/Aggregat) für das Gebläse und das Drittbecken: Ben/Orchestrator.
5. Zweite Quelle für die Rückschlagventil-Regel.

**Geprüft gegen:** `data/leitungsnetz.json` (K44–K51, F4), `data/system-specs.json` (Sauerstoff, Fischwasser, Leistung), Abschnitt 0–3, wastewater.com, aquakin-Doku, Hiblow-Händlerdaten · **Rechnung:** `python -X utf8 scripts/r45_luft.py`

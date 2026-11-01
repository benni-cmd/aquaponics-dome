# R45: Hydraulik und Auslegung der Lücken L01, L03, L10, L04, L06, L05

**Auftrag:** `docs/jobs/R45-hydraulik-auslegung.md` · **Rolle:** Fachrecherche (liest, rechnet, schreibt nur diese Datei und `scripts/r45_*.py`) · **Begonnen:** 01.11.2026
**Stand der Fragen:** 0 Schlammkonzept ✔ · 1 Beet-Ablauf ✔ · 2 Heber-Reserve offen · 3 Beet-Sumpf offen · 4 Belüftung offen · 5 Aktivkohle offen
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

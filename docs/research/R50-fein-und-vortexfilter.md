# R50: Fein- und Vortexfilter: Funktion, Kaufgeräte, Selbstbau, Empfehlung

**Auftrag:** `docs/jobs/R50-fein-und-vortexfilter.md` · **Bearbeitet:** 03.11.2026 · **Rolle:** Fachrecherche, nur lesen, suchen, rechnen, schreiben; nichts umgebaut, `gen_dome.py`, `data/*`, Netzliste und Roadmap unverändert.
**Herkunft:** [Q] Quelle gelesen (Datenblatt oder Seite geöffnet) · [Q-Treffer] nur Suchergebnis oder Händlerseite, Datenblatt nicht selbst gelesen · [E] eigene Rechnung (`python -X utf8 scripts/r50_rechnung.py`) · [A] Annahme. **Zwei-Quellen-Regel:** eine Behauptung gilt als belegt, wenn zwei voneinander unabhängige Dokumente sie tragen; sonst steht „Einzelquelle“ oder [A] daneben. Preise: Händler-Listenpreise vom 03.11.2026, nur Größenordnung (Scope D69).

**Ben-Frage:** Fein- und Vortexfilter genauer ausarbeiten, Standardgeräte finden und nachbauen, kaufen statt selbst bauen, außer Selbstbau ist super simpel; damit Filter und danach der Subtank (M10-S2V, geparkt) besser beurteilt werden können.

## 0. Antwort (fünf Punkte)

1. **Kein Kaufgerät erfüllt beim Feinfilter alle drei Bedingungen zugleich** (100 µm, 110 l/min im Schwerkraftzulauf mit nur 85 mm Reserve, Netz-Anschlüsse d75/d63). Es gibt gute, selbstreinigende Trommelfilter der Teichtechnik, aber mit 120 µm (EPS Entry 25), 60 µm (AquaForte ATF-1) oder 125/60 µm (Oase BioTec Premium), 3,8-fach bis 15,6-fach zu groß und mit 110-mm-Anschlüssen. Bogensiebe sind Standard bei 300 µm, nicht 100 µm. Beutelfilter-Gehäuse (100 µm) sind Druckbehälter für Pumpendruck, nicht für 85 mm Gefälle (Abschnitt 1, 3).
2. **Was der Feinfilter wirklich leistet:** bei 100 µm hält er nur etwa ein Fünftel der Schwebstoffmasse (21 % Mortensen; 34 % nach Gewicht bei 60 µm in einer Praxisanlage), weil die Fracht fast nur aus Teilchen unter 20 µm besteht. Er ist ein **Schutzsieb** für Pumpen, Beete und NFT-Rinnen, kein Reiniger. Das ist für Bens Urteil der wichtigste Satz.
3. **Der Vortex (Absetzer) arbeitet im Teilstrom als Absetzbecken, nicht als Wirbel** (Eintritt 0,14 m/s). Fertige Teich-Vortexfilter sind für 4 bis 40 m³/h gebaut (PP Vortex: mindestens 10 m³/h = 13-faches unseres Teilstroms) und taugen bei 0,75 m³/h nur als überdimensioniertes Becken. Standardteil ist der **Kegelboden-Tank** (PE, 100 bis 125 US-Gallonen, 1½ bis 2 Zoll Bodenanschluss; gefunden nur bei US-Händlern, in Europa nicht); die Einbauten (Leitrohr, tangentialer Zulauf, Hahn) sind aus PVC super simpel.
4. **Selbstbau:** Feinfilter in heutiger Form (PP-Behälter geschweißt, Edelstahlkorb, Standrahmen, vier Durchführungen) **nein**; eine einfache Form (Standard-Behälter mit Siebkorb oder Siebbeutel 100 µm, ein Überlauf) **ja**. Vortex: Tank selbst bauen **nein**, Tank kaufen und Einbauten selbst **ja**.
5. **Empfehlung:** Absetzer **behalten** (D71), Tank als Standard-Kegelboden-Tank beschaffen. Feinfilter: **Siebkorb behalten** (auch im Subtank, D75), aus Standardteilen vereinfachen und um eine Rückstausicherung ergänzen. Trommelfilter nur als Option, wenn Ben automatisches Reinigen will; dann Heber auf d90 oder d110 weiten (rechnerisch 186 bis 250 mm Reserve statt 85 mm).

## 1. Feinfilter (Hauptstrom 110 l/min je Linie, 100 µm)

### 1.1 Wirkprinzip und Fracht
- **Prinzip:** Das Wasser strömt durch ein Gewebe mit 100 µm Öffnung; was größer ist, bleibt im Korb. Mit dem Rückstand baut sich ein Filterkuchen auf, der den Durchfluss bremst, bis der Wasserstand im Behälter steigt.
- **Was ankommt:** Die Fracht besteht zu über 95 % aus Teilchen unter 20 µm [Q Chen u. a. 1993; Q Orellana 2006, Zusammenfassungen, aus R48 4.1 übernommen, zwei Quellen]. Ein Gewebe von 100 µm hielt im Versuch 21 % der Schwebstoffe zurück, 60 µm 48 %, 30 µm 99 % [Q Mortensen, Global Seafood 2000, nach R30 gelesen]. Eine Praxisanlage mit 60-µm-Trommel erreichte nur 34 % nach Gewicht [Q NMBU-Studie, R30; Suchzusammenfassung, niedrige Qualität]. Zwei unabhängige Befunde: 100 µm fängt nur den gröberen Rest.
- **Schlammfracht, Gegenprobe [E]:** Der Auftrag nennt 130 g/Tag je Anlage. Meine Rechnung aus 3,46 kg Futter/Tag für beide Linien (R45) mal 0,15 bis 0,30 kg Trockenmasse je kg Futter gibt 260 bis 520 g/Tag je Linie, nach dem Absetzer (77 %) 200 bis 400 g/Tag. In den gelesenen Dateien steht 130 g nur als TAN (D61); die Herkunft der 130 g als Feststofffracht habe ich nicht gefunden. Beide Werte liegen im gleichen Zehnerbereich; die Aussagen unten gelten für beide.
- **Was der Korb sammelt [E, `r50_rechnung.py`]:** bei 130 g/Tag und 21 % Rückhalt 27 g/Tag = 191 g Trockenmasse je Woche; als Kuchen mit 50 g/l [A] sind das 3,8 l je Woche oder 4,5 mm auf der Korbfläche 0,84 m². Das saubere Gewebe selbst bremst kaum: etwa 0,3 mm Wassersäule bei 7,9 m/h (Kapillarmodell, offene Fläche 35 % und Dicke 0,15 mm [A]). **Den Spiegelanstieg bis zur Spülung bestimmt der Kuchen und nicht das Gewebe; seine Durchlässigkeit ist nicht belegt** (Messung nach der ersten Betriebswoche).

### 1.2 Bauarten im Vergleich
| Bauart | Maschenweite im Handel | Antrieb, Wasserstandsbedarf | Reinigung | Ausfallart | Passt zu 110 l/min im Schwerkraftzulauf? |
|---|---|---|---|---|---|
| **Siebkorb / Korbfilter** (heute, T55) | frei wählbar (Gewebe 100 µm Meterware: Aquagart Edelstahlgewebe [Q-Treffer]) | keiner; sauberes Gewebe 0,3 mm Verlust [E] | von Hand, alle 1 bis 2 Wochen [Q SRAC 454] | Korb verstopft → Spiegel steigt → staut zum Pool (R48 4.7), kein Notüberlauf im Bauteil | **ja**, braucht nur wenige mm Gefälle, solange der Kuchen dünn ist |
| **Beutel-/Taschenfilter-Gehäuse** | 100 µm Beutel Größe 2, 80 gpm Nennleistung [Q-Treffer Zoro] | Druckbehälter, Gehäuse bis 88 psi [Q-Treffer PRM] | Beutel tauschen oder auswaschen | Beutel platzt oder verstopft; geschlossener Behälter | **nein im Schwerkraftzulauf** (geschlossenes Druckgehäuse); denkbar nur auf der Druckseite hinter den Pumpen [E: Pumpen sähen dann alles, was kleiner als der Grobabscheider ist, R48 4.2] |
| **Trommelfilter / Mikrosieb** | 60, 100 (FIAP), 120, 125 µm | Motor 80 W, Spülpumpe, Schwimmschalter; **Überstand 160 mm** (Entry 25) [Q] | automatisch, Spülrinne; Spülwasser nur 0,06 % (100 µm) bis 0,23 % (30 µm) des Durchflusses [Q Global Seafood, norwegischer Versuch, Suchzusammenfassung] | Antrieb oder Spülpumpe fällt aus → Trommel verstopft → Wasser läuft über den **eingebauten Trommel-Bypass** (Entry 25: 2 × 90 mm) [Q] | **nur mit mehr Gefälle**: 160 mm Überstand gegen 85 mm Reserve (Abschnitt 1.4) |
| **Bogensieb** | 300 µm Standard, 700 µm grob [Q-Treffer Koi-Company, Cotswold] | keiner, aber Fall über den Bogen; „Pumpengespeister“ Bauart bei AquaForte [Q-Treffer] | Bürste, Spülung | Siebspalt setzt sich mit Biofilm zu | **nein**: 300 statt 100 µm und pumpengespeist; die Spaltweite lässt sich nicht verkleinern ohne Verstopfung |
| **Bürsten-/Mattenfilter** | grob (über 100 µm) | keiner | Mattenwäsche | Matte verschlammt, Biofilm, anaerobe Stellen | **nein** als 100-µm-Stufe [A, keine Quelle gesucht]; nur als Grobvorstufe |

### 1.3 Was passt zu 110 l/min
Zuordnung nach Nennleistung [E]: 110 l/min = 6,6 m³/h. Die Trommelfilter der Teichtechnik sind für 25 m³/h gebaut (3,8-fach), der FIAP 80.000 für 103 m³/h bei 100 µm (15,6-fach). Die Fläche ist kein Problem; das Problem ist, dass sie Gefälle (Überstand) und Strom brauchen. Der Siebkorb (0,84 m², 7,9 m/h) braucht nichts davon und ist die einzige Bauart, die **ohne Pumpe und ohne Strom** mit 85 mm Reserve geht. Der Preis dafür ist die Handarbeit alle 1 bis 2 Wochen.

### 1.4 Gravitationszulauf aus dem Heber (nur 85 mm Reserve)
- **Befund [Q Datenblatt gelesen]:** DVS/EPS Entry 25 braucht 16 cm „Wasserspiegel Überstand“ (Schwerkraft/Airlift/Pumpversion; gepumpte Version mit 30 % Kapazitätsverlust). AquaForte ATF-1: Oberkante höchstens 10 cm über dem Wasserspiegel im Schwerkraftbetrieb [Q Händlerseite Toppy; Einzelquelle, Bedeutung der „10 cm“ nicht eindeutig]. FIAP: Schwerkraftversion nur mit elektrischem Kugelhahn DN100 (1.690 €) [Q Datenblatt gelesen]. **Fehlbetrag Entry 25: 160 − 85 = 75 mm.**
- **Möglicher Ausweg [E, Annahme reine Rohrreibung, nicht gemessen]:** der Heberverlust (195 mm bei d75) skaliert grob mit d⁻⁴ bis d⁻⁴,⁸⁷. Bei d90 wären es 80 bis 94 mm Verlust, die Reserve stiege auf 186 bis 200 mm; bei d110 auf 238 bis 250 mm. Teichtechnik ist ohnehin d110 (KG-Rohr). **Das ist eine Folge, die Montage messen muss (Heber-Messung ist offen, R47/R48); ich ändere nichts.**
- **Rückstausicherung:** Entry 25 hat den Trommel-Bypass [Q]; Siebkorb hat keinen. Vorschlag aus R48 4.7 gilt weiter: Hoch-Schwimmer, der den Heber-Absperrhahn schließt, plus Überlauf mit Weg in den Biofilter-Zulauf, nie in den Pool.

### 1.5 Verstopfungsverhalten, Intervall, Ausfall (Einordnung)
- **Verstopfen:** zuerst durch Biofilm und Fettfilm auf dem Gewebe und durch gröbere Teile (Futterbrocken, Pflanzenreste), erst danach durch Schlamm [A, nicht belegt]. Zum Vergleich der Flächenbelastung [E]: Der Korb arbeitet mit 7,9 m/h, die Trommel des Entry 25 bei Nennleistung mit 52 m/h (andere Bauart, nur Größenordnung); unser Bedarf liegt bei 26 % ihrer Nennleistung.
- **Intervall:** Korb 1 bis 2 Wochen [Q SRAC 454 über R30]; Trommel automatisch. Nach Masse wären es nur etwa 191 g Trockenmasse je Woche (Abschnitt 1.1); bestimmend ist der Biofilm, und dazu liegt keine Messung vor.
- **Ausfallart:** Korb stirbt sanft (Spiegel steigt, Alarm möglich); Trommel stirbt über den Bypass sanft, aber ohne Alarm bleibt die Siebwirkung unbemerkt aus [A].

## 2. Vortex / Absetzer (Teilstrom 12,5 l/min am Bodenablauf)

### 2.1 Wirkprinzip, drei Bauarten
- **Swirl (Wirbelabscheider):** Wasser tritt tangential ein, die Rotation führt schwere Teilchen zur Mitte und zum Kegel; die Abscheidung hängt nach Davidson/Summerfelt vor allem von der Oberflächenbelastung ab, nicht vom Drall [Q Global Seafood, gelesen]. Gedacht für dichte Teilchen; Kot und Futter sind kaum schwerer als Wasser.
- **Absetzbecken (Klärer):** Verweilzeit und Fläche entscheiden; SRAC 453 nennt 15 bis 30 min [Q, R48; Einzelquelle für den Bereich], Aquaponik-Richtwert mindestens 20 min [Q-Treffer aquaponics411, Einzelquelle].
- **Hydrozyklon:** braucht Druck und hohe Eintrittsgeschwindigkeit, bestimmt für Sand und dichte Teilchen (Bewässerungs-Sandabscheider, z. B. 6-Zoll-Vortexfilter 150 mesh, 20 gpm [Q-Treffer Pace Supply]); für leichten Fischschlamm ungeeignet [A, keine Fischquelle gelesen].
- **Unser Absetzer:** Eintritt d50 mit 0,137 m/s bei 12,5 l/min [E]: kein nennenswerter Drall, er **wirkt als Absetzbecken** (R48 4.1 mit gleicher Zahl).

### 2.2 Auslegung (Zahlen [E], `r50_rechnung.py`)
| Größe | heute Tank_klein (267 l) | Davidson-Versuch | Vollstrom 110 l/min im selben Tank |
|---|---|---|---|
| Oberflächenbeschickung | 2,17 m/h (0,60 mm/s) | 11,2 m/h (3,1 mm/s) [Q] | 19 m/h; für 11,2 m/h bräuchte man 0,59 m² statt 0,35 m² |
| Verweilzeit | 21 min | – | 2,4 min (254 l: 2,3 min) |
| Eintrittsgeschwindigkeit d50 | 0,137 m/s | – | 1,21 m/s |
- **Abscheidegrad:** Swirl 37,1 ± 3,3 % der Schwebstoffe, Radial-Flow-Absetzer 77,9 ± 1,6 % [Q Davidson/Summerfelt 2005, Global Seafood, gelesen]; Hydrotech-Mikrosieb zusätzlich 40 bis 45 % der Masse [dieselbe Quelle]. Ein Radial-Flow-Absetzer ist damit die in der Literatur bessere Stufe; kaufbar sind Pentair Radial Flow Settler 45 und 60 [Q-Treffer, Datenblatt nicht gelesen, Maße offen] und Selbstbau-Anleitungen [Q-Treffer ecofilms.com.au]. **Offen, nicht Teil dieses Auftrags.**
- **Kegel und Schlammablass:** Der Tank_klein hat einen Kegel mit Kugelhahn an der Spitze (Z 80). Kegelböden im Handel haben 15° (Norwesco 43161) oder 30° (Tanks Supply Direct, „bis 99 % entleerbar“) [Q-Treffer]; steilere Kegel (45° und mehr) rutschen Schlamm besser [A]. Das Bauteil T40 hat aus dem Kegelvolumen (33 l bei Radius 336,5 mm, tank.md) gerechnet eine Kegelhöhe von etwa 0,28 m, also rund 40° zur Waagerechten [E]; die 15°- und 30°-Handelstanks sind flacher, bei ihnen hilft die Spülung über den Hahn mehr als der Kegel.
- **Schlammanfall und Intervall:** 11 bis 14 l/Tag je Linie = 77 bis 98 l/Woche; Spülen alle 2 bis 3 Tage mit 20 bis 40 l, Fass einmal je Woche (R45 Abschnitt 0).
- **Ausfallarten:** Schlammhahn oder Ablassrohr verstopft (Schlamm sammelt sich, Kegel läuft voll, Feststoffe gehen in den Feinfilter); kleine Pumpe fällt aus (Absetzerkreis steht, Hauptstrom läuft weiter, R48); Verstopfen des tangentialen Zulaufs d50 (Futterbrocken) [A].

### 2.3 Was ändert der Teilstrom gegen Vollstrom
Der Vollstrom macht aus dem Absetzbecken einen echten Wirbel (1,2 m/s Eintritt), verkürzt aber die Verweilzeit auf 2,3 min und verdoppelt die Beschickung über den Prüfwert hinaus (R48 4.1); der Nutzen für Teilchen unter 20 µm ist dann gering. Der Teilstrom ist die in der Literatur übliche Anordnung (SRAC 453, Davidson/Summerfelt, Khater, R48). **Folge für Kaufgeräte:** Fertige Wirbelfilter sind für den Vollstrom ausgelegt (Mindestdurchfluss 10 m³/h bei PP Vortex 950 [Q]); im Teilstrom arbeiten sie als große Becken.

## 3. Standardgeräte-Katalog

Anschlüsse der Netzliste: Heber d75 (K01), Feinfilter-Einlauf d63, Auslauf d63/d50, Absetzer-Zulauf d50 (K04), Auslass d50 (K05), Schlammablass d40 (K07). Teichtechnik ist fast durchgängig **110 mm** (KG-Rohr), Beutelgehäuse **2 Zoll**; mit Reduzierstücken passt jedes Gerät, nur der Wert „Schwerkraft-Überstand“ ist die harte Grenze.

### 3.1 Feinfilter

| Bauart | Gerät (Hersteller, Modell) | Maße | Anschlüsse | Durchsatz laut Datenblatt | Maschenweite | Material | Quelle | Preis (grob) | Passt zur Netzliste? |
|---|---|---|---|---|---|---|---|---|---|
| Trommel | **DVS/EPS ENTRY 25** | Trommel Ø380 × 400; Gehäuse nicht genannt | 1 × 110 Schmutz, 2 × 90 Trommel-Bypass, Ein-/Ausgänge nach Zeichnung | 25 m³/h, Überstand 16 cm | **120 µm** | PP 10/15 mm, Edelstahl 316/304, Silikon | [Q Datenblatt dvs-filtertechniek.com gelesen] | nicht genannt | Überstand 160 mm > Reserve 85 mm; Maschenweite 120 statt 100 µm |
| Trommel | **AquaForte ATF-1** | 500 × 700 × 430 | 3 × 110 Ein, 2 × 110 Aus, 110 Schmutz, 50 innen | 25 m³/h | **60 µm** (Elemente tauschbar) | nicht genannt | [Q Toppy gelesen; Einzelquelle, „nicht mehr lieferbar“] | 1.229 € | Schwerkraft ab 100 mm über Wasserspiegel; Strom 80 W; Modell derzeit nicht lieferbar |
| Trommel (Filtersystem mit Biokammern) | **Oase BioTec Premium 80000** | 885 × 675 × 820, 65 kg | DN110 [Q-Treffer, nicht bestätigt] | 12,5 bis 15 m³/h | 125 µm (Ersatzsieb), 60 µm als Zubehör | nicht genannt | [Q-Treffer Oase Katalog, Händler; Datenblatt nicht gelesen] | nicht erhoben | wie oben |
| Trommel | **FIAP TrommelSieve Active 80.000** | 1177 × 850 × 1026, 148 kg | DN150 Ein, DN200 Aus, DN100 Schmutz | 80 m³/h (60 µm 25,4 l/s, **100 µm 28,6 l/s**) | **60/100 µm** | Edelstahl | [Q Katalogseite gelesen] | 9.490 € | 100 µm vorhanden, aber 15,6-fach zu groß, 400 V Spülpumpe, Schwerkraft nur mit el. Kugelhahn |
| Bogensieb | **Koi-Company / Cotswold SuperSieve** | je Modell ca. 660 × 350 × 745 bis 660 × 680 × 745 (Tabelle ohne klare Zuordnung) | 3 × 110 Zulauf, 2 × 90 Ablauf | nicht genannt | **300 µm** (700 µm grob) | nicht genannt | [Q-Treffer, Anleitung nur teilweise gelesen] | 522 £ | 300 µm, Rand 4 cm über Wasserstand |
| Bogensieb | **AquaForte CompactSieve II** | nicht erhoben | nicht erhoben | nicht erhoben | **300 µm** | nicht genannt | [Q-Treffer eBay] | 300 € | pumpengespeist |
| Beutel | **PRM PPH #2** Beutelgehäuse | nicht gelesen (Seite nicht abrufbar) | 2 Zoll Flansch | max. 125 gpm (28 m³/h) | Beutel 100 µm Größe 2 lieferbar | PP | [Q-Treffer PRM, Zoro, Shelco] | nicht erhoben | Druckgehäuse, nur hinter den Pumpen |
| Beutel | **Shelco BFS-2C-2** | nicht erhoben | 2 Zoll FNPT | 150 gpm (34 m³/h) | Beutel 100 µm | nicht genannt | [Q-Treffer] | nicht erhoben | wie oben |

Weitere Teile: Edelstahl-Siebgewebe als Meterware (Aquagart, 30 × 40 bis 110 × 50 cm) [Q-Treffer Galaxus]; Monofilament-Siebbeutel 100 µm (15 × 25 cm) [Q-Treffer monopoel.de].

### 3.2 Vortex / Absetzer

| Typ | Gerät | Maße | Anschlüsse | Durchsatz laut Hersteller | Material | Quelle | Preis (grob) | Passt zur Netzliste? |
|---|---|---|---|---|---|---|---|---|
| Teich-Vortex | **PP Vortex 950** (Bavaria / Koiteichbedarf) | Ø950 × 1000 | 3 × 110 Zulauf, 1 × 200 Ablauf, 1 × 110 Schmutz (Zugschieber, Schrägboden, Bürstenkranz) | **10 bis 30 m³/h**, Schwerkraft oder gepumpt | PP-CO schwarz | [Q Händlerseite gelesen] | 1.099 € | Anschlüsse größer; Mindestdurchfluss 13-fach Teilstrom → Becken, kein Wirbel |
| Teich-Vortex | **AquaLogistik Center-Vortex C20** (bis C115) | 850 × 850 × 650; Vortex Ø450 | 110/110, Schmutz 5 × 50 | 4 m³/h (C20) bis 18 m³/h (C115) | GFK | [Q Händlerseite gelesen] | ab 990 € (Serie) | Schmutzablass d50 passt; 5,3-fach Teilstrom |
| Teich-Vortex | **AquaLogistik/Tripond Vortex 65** | Ø650 × 750 | Zulauf 110, 2 × 110 Ablauf, Schmutz 63 | nicht genannt | PP [A] | [Q-Treffer, Einzelquelle] | nicht erhoben | Zulauf d110 |
| Teich-Vortex | **AquaForte Turbo Vortex** | Ø350 × 1250 | nicht genannt | max. 25 m³/h | nicht genannt | [Q Toppy gelesen] | 951 € (nicht lieferbar) | Pumpenvorfilter für Rohre |
| Aquaponik-Swirl | **Swirl Filter GFK 750 l** (aquaponics.net.au) | 1100 hoch × 1450 Ø (Baugruppe), 750 l | nicht genannt, Löcher vorgebohrt | 2.250 l/h | Fiberglas | [Q Händlerseite gelesen, nicht lieferbar] | 1.280 AUD | 60 min Verweilzeit bei 12,5 l/min |
| Kegel-Tank (Standardteil für das Bauteil) | **Norwesco 43161** 125 gal | Ø1219 × 1041, 142 lb | Bodenanschluss | – | PE | [Q-Treffer Snyder] | nicht erhoben | 473 l, 15°-Kegel |
| Kegel-Tank | **Cone-Bottom 100 gal** (Protank, Chemical Containers) | Ø584 × 1651 (mit Stand 1980) | 1½ Zoll PP-Bulkhead | – | PE | [Q-Treffer] | nicht erhoben | 378 l, 15°-Kegel |
| Kegel-Tank | **Tanks Supply Direct 100-OTCB** | Ø762 × 1016 (30 × 40 in) | 2 Zoll PP-Auslass, EPDM | – | PE, 30°-Kegel | [Q-Treffer] | nicht erhoben | 378 l, offene Oberseite |
| Absetzer (Literatur-Bessere) | **Pentair Radial Flow Settler 45/60** | nicht gelesen | nicht gelesen | nicht gelesen | nicht gelesen | [Q-Treffer, Seite 403 nicht lesbar] | nicht erhoben | **offen** |

Ungeeignet gefunden: Deschacht/WISY Wirbel-Feinfilter WFF100 (Regenwasser, Gewebe 0,28 mm, Anschlüsse 110, Höhenunterschied Zulauf zu Ablauf 2110/2790 mm) [Q Datenblatt gelesen]: Regenwasserfilter, kein Absetzer und braucht 2 m Höhe.

### 3.3 Ehrlicher Befund zur Beschaffbarkeit
Für **Europa fand die Suche keinen Kegelboden-Tank** der Größe 250 bis 300 l in PE; die Treffer sind aus den USA (Norwesco, Chemical Containers). Der heutige Tank_klein (Ø673, 267 l) ist ein Maß aus dem OBJ, kein Handelsmaß. Zu klären: Händler in Europa oder Versandkosten aus den USA (D69: keine Kostenrechnung hier).

## 4. Selbstbau-Bewertung

| Frage | Feinfilter | Vortex / Absetzer |
|---|---|---|
| **Super simpel?** | **Heutige Form: nein.** 55 Körper, 40,5 kg, geschweißter 10-mm-PP-Behälter, Edelstahlkorb mit Rahmen und Flansch, 4 Durchführungen, Deckel mit Spannverschlüssen, Standrahmen (Bauteilblatt T55). **Einfache Form: ja** (Standardbehälter mit Deckel, Korb oder Siebbeutel 100 µm, zwei Bulkheads, ein Überlauf). | **Tank: nein** (Kegel roto-formen oder schweißen). **Einbauten: ja** (Leitrohr d110, Zulaufbogen, Kugelhahn d40, vier Standardteile, Werkzeug Säge und Kleber). |
| Eigenmodell (heute) | Funktion belegt in Mortensen-Rate (21 %); Teile viele; Wartung: Grube, Hub 460 mm; Risiko: kein Notüberlauf, Dichtungen, Spannverschlüsse | Funktion Absetzbecken 21 min, 2,2 m/h; Teile 33 Körper, Plattform und Beine Stahl (Selbstbau), Tank PE (Standard); Wartung: Hahn Z 80, Grube; Risiko: Kegel als Sondermaß |
| Kauf | Trommel: selbstreinigend, bis auf Schwerkraft-Überstand alle Anschlüsse; **zu groß, Mehrstufen, Strom**; Siebkorb gibt es nicht als Fertiggerät für 110 l/min und 100 µm | Kegel-Tank: Standard; Teich-Vortex: Fehlkauf im Teilstrom; Radial-Flow: bessere Funktion, Maße offen |
| Selbstbau (einfach) | Wartung wie heute; Risiko: Dichtheit des Deckels und Rückstau; Funktion gleich | Wartung wie heute; Risiko: Zulauf verstopft |
| **Ehrliches Urteil** | Das heutige Eigenmodell **schneidet beim Aufwand schlecht ab**: ein Kaufteil mit gleicher Siebfläche gibt es nicht, aber die Eigenform ist reicher als nötig (Standrahmen, Spüllanze, Spannverschlüsse). Die funktionale Mindestform ist einfach. | Das Eigenmodell ist **gut**, weil sein Tank Standard sein darf; die Plattform ist der Selbstbau-Anteil. |

## 5. Empfehlung je Filterart

**Feinfilter: Siebkorb behalten, aus Standardteilen vereinfachen.**
- Funktion bleibt: Schutzsieb, kein Reiniger. Gewebe 100 µm [Q: Mortensen 21 %, Praxis 34 % bei 60 µm]; wer mehr Feinabscheidung will, muss auf 60 µm gehen (48 %, Reinigung häufiger) und bleibt bei unter der Hälfte.
- **Option B (Ben entscheidet): Trommelfilter** (ATF-1 oder Entry 25 als Vorbild; FIAP wenn 100 µm Pflicht): lohnt, wenn das wöchentliche Korbziehen stört. Bedingung: Heber d90 oder d110 und Strom (80 W je Gerät). Kein Auftrag, nur Vorschlag.
- **Folge D75 (Subtank):** Siebkorb am Subtank-Einlauf bleibt die passende Form; die Rückstausicherung (Hoch-Schwimmer schließt den Heber-Hahn, Überlauf in den Biofilter) gehört in M10-S2V. Ein Trommelfilter säße über dem Subtank-Spiegel (Z 320) und braucht dort 160 mm Überstand; das klärt die Montage mit der Heber-Messung. **Ich ändere D75 nicht.**
- **Folge D71:** keine; der Feinfilter bleibt in der Kette.

**Vortex / Absetzer: behalten (D71), Tank als Standard-Kegelbodentank beschaffen.**
- Kegelboden-Tank PE (100 bis 125 gal) statt Sondermaß; Leitrohr, tangentialer Zulauf d50 und Schlammhahn aus PVC selbst (Abschnitt 4).
- **Kein** fertiger Teich-Vortex für den Teilstrom (Mindestdurchfluss 10 m³/h, 1.000 € und mehr, nur Beckenfunktion).
- Wer mehr Abscheidung will, prüft den Radial-Flow-Absetzer (77,9 % gegen 37,1 %) als eigenen Auftrag; Beschaffbarkeit offen (Datenblatt Pentair nicht gelesen).
- **Folge D71/D75:** Absetzer bleibt; der Auslass K05 d50 mündet in den Subtank-Korb (R49 Abschnitt 4: „direkt einleiten“).

## 6. Modellier-Spezifikation je empfohlenem Gerät

Nur Spezifikation, kein Bau. Die Maße aus dem heutigen Bauteilblatt gelten weiter; die Tabellen nennen, was für die Standard-Variante dazukommt. Bezug: Z in mm, Bezugspunkt wie im Bauteilblatt.

### 6.1 Feinfilter, Siebkorb (heutiges T55 `feinfilter`, vereinfacht)
| Eigenschaft | Wert | Herkunft |
|---|---|---|
| Außenmaß Behälter | 630 × 440 × 610 (innen 610 × 420 × 600), PP-Platte 10 mm, Deckel 638 × 448 × 6 | `docs/parts/feinfilter.md` |
| Korb / Einsatz | 560 × 370 × 400, Gewebe 100 µm, Siebfläche 0,84 m², Flansch 604 × 414 × 3, 2 Bügelgriffe | [E] Bauteilblatt |
| Einlauf | PVC-U d63, Stutzen links, Mitte z 816, senkrechtes Einlaufrohr endet z 696, 10 mm über dem Korbflansch | Bauteilblatt |
| Auslauf | d63, rechts, Mitte z 310 (unter dem Korb), Dichtflansch D90 | Bauteilblatt |
| Ablass | d40 mit Kugelhahn D56, Vorderwand x 225, z 285 | Bauteilblatt |
| Spülanschluss | d25 mit Kugelhahn, Rückwand z 830 | Bauteilblatt |
| **Neu (Spezifikation):** Überlauf/Rückstausicherung | Überlauf d50 in der Rückwand, Unterkante 20 mm unter dem Behälterrand (z 590), Rohr führt in den Biofilter-Zulauf, nicht in den Pool; Hoch-Schwimmer | [A] aus R48 4.7 |
| Gewicht | leer 40,5 kg, in Betrieb ca. 175 kg | Bauteilblatt [E] |
| Beschaffbarkeit | **Selbstbau** (vereinfachte Form: Standardbehälter + Korb Edelstahlgewebe 100 µm, Gewebe und Siebbeutel Standard) | Abschnitte 3 und 4 |

### 6.2 Option B: Trommelfilter (Modell nach AquaForte ATF-1, nur wenn Ben Option B wählt)
| Eigenschaft | Wert | Herkunft |
|---|---|---|
| Außenmaß | 500 × 700 × 430 (L × B × H) | [Q Toppy] |
| Stutzen | 3 × d110 Zulauf, 2 × d110 Ablauf, 1 × d110 Schmutz (Spülrinne), 50 mm innere Anschlüsse; **Lage der Stutzen nicht in der Quelle** (offen, Zeichnung beim Hersteller) | [Q] |
| Deckel | Edelstahl [A] | – |
| Korb/Einsatz | Trommel mit austauschbaren Siebelementen 60 µm | [Q] |
| Antrieb | Motor 80 W, Spülpumpe, Schwimmschalter | [Q] |
| Gewicht | nicht genannt (offen) | – |
| Beschaffbarkeit | **Standard** (ATF-1 derzeit nicht lieferbar; Entry 25 als Alternative, Maße nicht genannt) | [Q] |

### 6.3 Absetzer, Tank_klein mit Standard-Kegelboden-Tank (T40 `tank_klein`)
| Eigenschaft | Wert | Herkunft |
|---|---|---|
| Außenmaß Tank | Ø673 × 1075 (Rand bis Spitze), Randwulst 25 × 40 | `docs/parts/tank.md` |
| Zulauf | tangential d50, 250 mm unter dem Rand (Z 997) | Bauteilblatt |
| Auslass | d50 am Leitrohr, 100 mm unter dem Rand (Z 1147) | Bauteilblatt |
| Leitrohr | d110, Wand 3, reicht 420 mm unter den Deckel | Bauteilblatt |
| Deckel / Revision | Deckel 6 mm, Revisionsöffnung D200 | Bauteilblatt |
| Schlammhahn | Kugelhahn d40 an der Kegelspitze (Z 80), Federrückzug (Netz K07) | tank.md, Netzliste |
| Ports | Zulauf d50 (K04), Auslass d50 (K05), Schlamm d40 (K07) | Netzliste |
| Gewicht | 46 kg leer, gefüllt bis Rand 254 l = 300 kg | tank.md |
| Alternative Standard-Tank statt Sondermaß | Tanks Supply Direct 100-OTCB, Ø762 × 1016, 378 l, 30°-Kegel, 2-Zoll-Auslass, offene Oberseite; Folge: Beschickung 1,6 m/h, Verweilzeit 30 min; Plattform und Zulaufhöhe neu | [Q-Treffer], [E] |
| Beschaffbarkeit | **Tank Standard, Einbauten Selbstbau (PVC), Plattform und Beine Selbstbau** (Metallbau) | tank.md, Abschnitt 4 |

## 7. Belegstand und Grenzen
| Aussage | Stand |
|---|---|
| 100 µm hält 21 % der Schwebstoffmasse; 60 µm 48 %; Praxis 34 % nach Gewicht | Mortensen (R30, gelesen) und NMBU-Studie (Suchzusammenfassung): zwei Quellen, Original von Mortensen nicht von mir gelesen |
| Fracht zu über 95 % unter 20 µm | Chen 1993 und Orellana 2006 (R48): zwei Quellen, nur Zusammenfassungen |
| Trommel Entry 25: 120 µm, 25 m³/h, 16 cm Überstand, 2 × 90 Bypass | Datenblatt gelesen, Einzelquelle |
| FIAP 100 µm: 28,6 l/s; DN150/200/100; 9.490 € | Katalogseite gelesen, Einzelquelle |
| AquaForte ATF-1: 60 µm, 25 m³/h, 110er Anschlüsse | Händlerseite gelesen, Einzelquelle, nicht lieferbar |
| Bogensieb 300 µm Standard | Koi-Company und Cotswold: zwei Händlerseiten, Suchtreffer |
| Beutelfilter 100 µm, 2-Zoll-Gehäuse | drei Händler, Datenblatt nicht gelesen; Druckgehäuse-Aussage [Q-Treffer PRM 88 psi] |
| Teich-Vortex Mindestdurchfluss 10 m³/h (PP 950) | Händlerseite gelesen, Einzelquelle |
| Kegel-Tanks PE (Norwesco, Chemical Containers) | Händlerseiten, Suchtreffer |
| Auslegung Wirbelabscheider (Veerapen 2005) | Titel und Zusammenfassung, Volltext nicht gelesen: keine Zahl für Eintrittsgeschwindigkeit |
| Heber-Aufweitung d90/d110 | [E] Skalierung des gemessenen 195 mm, nicht gemessen |
| Spülwasser Trommel 0,06 bis 0,23 % | Suchzusammenfassung eines norwegischen Versuchs, Einzelquelle |

**Abweichungen und Lücken:** (1) Die 130 g/Tag der Aufgabe stehen in meinen Dateien nur als TAN; Feststofffracht gerechnet 200 bis 400 g/Tag je Linie. (2) Pentair-Seiten und einzelne PDFs waren nicht lesbar (403, 429). (3) Keine Quelle gefunden, die für einen kleinen Teilstrom-Wirbelabscheider (12,5 l/min) ein Fertiggerät nennt. (4) Oase BioTec 80000 Anschlussgröße und Spiegelbedarf nicht aus dem Datenblatt bestätigt (Datei zu groß).

**Geprüft gegen:** `filter-konzept.md` (Art 1 und 2), `parts/feinfilter.md`, `parts/tank.md`, R48 (4.1, 4.6, 4.7, 6), R49 Abschnitt 4, D55, D71, D72, D75, Roadmap `N-FILTER`, Netzliste K01 bis K07 und K21; Datenblätter EPS Entry 25, FIAP TrommelSieve Active 80.000, Deschacht WFF100; Händlerseiten Toppy, koiteichbedarf, koico, aquaponics.net.au; Suchtreffer für die übrigen.
**Offen:** (ICH) Pentair Radial Flow Settler und Oase BioTec 80000 Datenblatt lesen, europäischer Kegelboden-Tank-Händler, Maße Entry 25 beim Hersteller; (DEINE ENTSCHEIDUNG) Siebkorb behalten oder Trommelfilter als Option B; Absetzer-Tank Standard-Kegelboden statt Sondermaß; Radial-Flow-Absetzer prüfen lassen; (DEINE HANDLUNG) beim Hersteller (DVS/EPS, AquaForte) Anschlusslage und Gewicht anfragen, wenn Option B gewählt wird; Montage: Heber-Messung und Rückstausicherung vor M10-S2V.

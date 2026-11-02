# R47: Wasserkreislauf und Verteilung neu denken — Machbarkeitsprüfung (Wunsch W51)

**Auftrag:** `docs/jobs/R47-wasserkreislauf-neu.md` · **Bearbeitet:** 02.11.2026 · **Rolle:** Fachrecherche, nur lesen/rechnen/schreiben; nichts umgesetzt, kein Modell, keine Netzliste, kein Roadmap-Eintrag geändert.
**Herkunft:** [Q] Quelle · [E] eigene Rechnung (`python -X utf8 scripts/r47_rechnung.py`, liest `data/leitungsnetz.json`) · [A] Annahme. Z-Werte relativ zum Innenboden (Skript-Z minus 400). Schwache Belege sind als „Kandidat“ oder „offen“ markiert.

**Problem/Intent/Goal:** Ben will vor dem Weiterbau wissen, ob eine hängende Ringleitung, Anlagenteile näher am Kreislauf, mehr Schwerkraft und ein verstopfungssicheres Flood-and-Drain besser sind als der heutige Plan (Verteiler d50 je Linie, Beete d40, NFT d32, Rücklauf über Halbringe d110 und Sektorsammler d63). Ziel: Einschätzung je Idee, Zahlenvergleich A/B/C, Empfehlung, Folgen für M10 S3–S7 und W37.

## Gesamturteil (zehn Zeilen)

1. **Empfehlung: Variante A (heutiger Plan, gestrafft). Variante B (ein Ring für alles) nicht bauen. Variante C (Ring nur für Beete) nur, wenn die Gräben für K11 zum Problem werden.**
2. **Hängender Ring: teilweise machbar.** Statisch einfach (Ring d90 voll 6,8 kg/m, 146 kg gesamt, 12 Stützen, Durchhang 3–9 mm), hydraulisch ein Rückschritt: Der Biofilter-Überlauf (Z 1570) liegt 530 mm **unter** der Ring-Unterkante (Z 2100). Schwerkraftspeisung braucht den Biofilter 725 mm höher; Druckspeisung hebt die Pumpenhöhe von 2,0 auf 2,83 m.
3. **Zahlen (A / B / C):** Pumpen elektrisch 430 / 548 / 503 W; Zulauf-Verteilrohr 80 / 109 / 81 m; Formteile+Armaturen 214 / 220 / 232; Pumpstufen 2 / 2 / 3; Gangkreuzungen Zulauf (Gräben) ≈ 1 je Außenbeet / 0 / 0 [E, A].
4. **Der Ring spart keine Teile:** 38 Abnehmer (14 Beete, 24 Tische) brauchen jeder ein T, Bögen, Hahn, Reduzierung. Der Ring ersetzt nur die zwei Verteilstränge je Linie und kostet 28 m mehr Rohr.
5. **Der einzige echte Gewinn des Rings:** Beete ohne Graben über die Gänge erreichen. Das lässt sich billiger lösen (Abschnitt 2 und 5).
6. **Teile nah am Kreislauf:** Der Hauptkreislauf ist bereits kurz (eine Pumpstufe, dann alles frei). Größte offene Rohrmenge ist der Rücklauf der Beete (K14, ca. 59 m d50 [E]); Beet-Sumpf im Beet-Schwerpunkt spart rechnerisch 14,5 m. „Sumpf als Saugsumpf der Hauptpumpen“ ist verworfen (Saughöhe).
7. **Schwerkraft:** wird heute schon genutzt (Heber Pool→Filter, Biofilter→Verteiler→Beete/NFT→Pool frei). Gepumpt wird nur zweimal: Hauptpumpen (2,0 m) und Beet-Sumpf (1,47 m), Letzteres zwingend, weil der Beetablauf (Z −100) 615 mm unter dem Spiegel (Z 515) liegt.
8. **Flood-and-Drain:** Bens Wunsch ist im Bauteil `ibc_beet` **schon erfüllt** (Siebboden 8 mm auf 60-mm-Klötzen, 640 l Wasserraum darunter, Siphon leert bis zum Boden). Zu ändern sind nur drei Kleinigkeiten: Medienschutz-Löcher 12 mm gegen Korn ab 8 mm, Reinigungszugang, Korn ≥ 12 mm festlegen.
9. **Folgen:** M10 S3–S7 und W37 können mit A **unverändert** weiterlaufen; W37 (Beet-Sumpf, Schlammfass) bleibt. Bei B/C entfielen K11/K12 als Rohrstränge, es kämen Biofilter-Anhebung oder Booster-Pumpe, Stützen und ein neues Bauteil „Ringstück“ dazu.
10. **Offen:** Stützen-Statik (Kragarm 2,2 m), Gangkarte für Stützenstandorte (nicht gerechnet), Pumpenkennlinien, Frost bei Heizungsausfall (Standort offen). Entscheidung liegt bei Ben.

## 1. Hängender Leitungsring („Wasserautobahn“)

**Einschätzung: teilweise machbar** (bauen ginge, lohnt aber nicht als einziger Ring).

**Höhe und Gang.** Trassenregel Ü-Band: frei ab Z 2100 [Q `m10-leitungen.md` 4.1]. Ring d90: Unterkante 2100, Achse 2145, Hochpunkt (1 % Gefälle über einen Halbring ≈ 107 mm) ca. 2245 [E]. Das erfüllt „Gang ≥ 2100 frei“ ohne Reserve; jede Konsole oder Klemme unter dem Rohr bricht die Regel, also Auflage oben auf Konsolen oder Hängebügel an der Stütze, nicht unter dem Rohr.

**Befestigung nur an erlaubten Punkten [Q Regel 7].** (a) Tisch- und Portalbeine reichen nur bis ca. Z 1100–1400 (Tischoberkante Z 1000 + Rinne), bräuchten 0,8–1,1 m Aufsatz als Kragarm: nicht empfohlen, neues Bauteil, Last auf Möbel. (b) Tank- und Pumpentafeln: nur in den zwei Technikgruppen. (c) Eigene Stützen im Boden: einzige Lösung für die Strecke dazwischen. 12 Stützen bei 1,8 m Abstand [E]; Gangkarte (58 rote, 72 gelbe Engstellen) noch nicht gegen die Stützenorte geprüft: **offen**, Skript `check_walkways.py` läuft erst nach Bens Entscheidung. Statik der Stützen (Kragarm 2,2 m, Anstoßlast, Wasserschlag) ist **nicht** bewertet: offen, Standardmaß Gerüstrohr d48,3 nur als [A] (W43).

**Last und Abstand [E, Skript Abschnitt 1].**

| Rohr | Di mm | kg/m voll | Stützabstand max. | Durchhang kurz / Dauerlast |
|---|---|---|---|---|
| d63 | 57,0 | 3,34 | 1,5 m | 2,8 / 8,5 mm |
| d75 | 67,8 | 4,74 | 1,65 m | 2,9 / 8,7 mm |
| d90 | 81,4 | 6,82 | 1,8 m | 2,9 / 8,6 mm |
| d110 | 99,4 | 10,2 | 2,0 m | 2,9 / 8,7 mm |

Stützabstand: kleinerer von zwei Quellen: [Georg Fischer PVC-U Planning Fundamentals](https://www.gfps.com/content/dam/gfps/com/planning-fundamentals/en/gfps-planning-fundamentals-material-pvc-u-en.pdf) (≤ 20 °C: d63 1,8 m, d75 2,0, d90 2,2, d110 2,4) und [plasticpipeshop.co.uk Pipe Clip Spacing](https://www.plasticpipeshop.co.uk/Pipe-Clip-Spacing_ep_52-1.html) (d63 1,5 m, d75 1,65, d90 1,8, d110 2,0); beide gelten für 20 °C, im warmen Dom unter der Decke sinkt der Wert (GF: d63 1,3 m bei 60 °C). E-Modul PVC-U 3000 MPa kurz, 1000 MPa Dauer [A]. Ring d90 voll: 146 kg gesamt, 12 kg je Stütze: Gewicht ist kein Problem, Seitensteifigkeit ist es.

**Druck oder Schwerkraft? Der entscheidende Befund.** Das Wasser kommt aus dem Biofilter. Überlauf Z 1570 (Skript-Z 1970 − 400 [E]); Ring-Unterkante 2100: der Überlauf liegt **530 mm darunter**. Zwei Auswege:

1. **Schwerkraftring:** Biofilter-Überlauf auf ≥ Z 2295 anheben, also 725 mm höher als heute. Tank samt Plattform höher, Deckel und Belüftung auf ca. Z 2400 (heute 1676 + 725), Wartung nur mit Tritt. Folge: Bauteile Plattform/Beine, gebaute Leitungen K08–K10 (Zulauf Z 1820, Überlauf Z 1970 gebaut) alle neu.
2. **Druckring:** Pumpen speisen den Ring (Hochpunkt Z 2245 + Entlüfter). Höhe: statisch 1,93 m statt 1,10 m (Saugspiegel Pool minus Heberverlust Z 320, [Q R45]); Gesamthöhe 2,83 m statt 2,0 m [E]; je Pumpe 102 statt 72 W bei η 25 % [Q Netzliste Kabelliste]. Der Biofilter müsste vor den Ring (Pumpe → Biofilter → Ring) oder parallel; bei Reihenschaltung hebt der Tank-Überlauf nichts, es braucht dann einen Druckbehälter oder Booster.

**Kapazität (Manning, n 0,010 PVC [A], Vollrohr, im Betrieb halbvoll rechnen):** d75 143 l/min bei 1 % (101 bei 0,5 %), d90 233 / 165, d110 396 / 280. Ein Ring für beide Linien (220 l/min) braucht als Schwerkraftrohr d110, als Druckrohr d63 (1,44 m/s, an der Grenze 1,5) bis d75 (1,02 m/s).

**Entlüftung/Entleerung.** Schwerkraftring: Gefälle ≥ 0,5–1 %, Hochpunkt mit Belüftungsventil, Tiefpunkt mit Kugelhahn zum Rücklauf. Druckring: Entlüfter am Hochpunkt, Absperrungen je Segment. Beides nicht neu erfunden, aber 3 zusätzliche Bauteile je Linie [A].

**Abzweige und Regler.** Je Abnehmer: T (Ring d90 → d32/d40), 2 Bögen für die Fallleitung, Kugelhahn als Regler, Reduzierung. Fallleitung Ring→Beet-Tropfrohr (Z ~650) 1,5 m, Ring→Tischzulauf (Z ~1090) 1,05 m [E]. Regler direkt am Element sind damit machbar und besser zugänglich als am Verteiler; Durchflussbegrenzer/Dosierventil wären Handelsteile (Fabrikat offen).

**Frost.** „Entfällt im Dom“ stimmt nur mit Heizung. Heizlast 0,83 kW/K [Q `system-concept.md`], Standort offen: fällt die Heizung aus, kühlt der Dom auf Außentemperatur; ein stehender Ring friert dann zuerst (Plane, UV, Rohr dünn). Warme Luft sammelt sich oben (hilft), aber Wasser im Ring muss bei Stillstand ablaufen können (Entleerungsventil). Außerdem altert PVC im UV-Licht: Ring in grauem/schwarzem Rohr, nicht klar [A, keine Quelle geholt].

**Ein Ring für alle gegen zwei Ringe.**

| | Ein Ring | Zwei Halbringe (Linie Ost/West) |
|---|---|---|
| Länge | 21,4 m (r 3,4 m) | 2 × 10,7 m |
| Ausfall | Bruch/Leckage nimmt beide Linien | wie heute: eine Linie bleibt |
| Redundanz | Pumpen müssten quer koppeln | passt zu D67 (symmetrisch) und 2 Pumpen je Linie |
| Durchfluss je Abgang | Quer-Verteilung unklar, Druckverlust über 10 m | je Halbring 110 l/min, d75 reicht |
| Fehlersuche | ein Rohr, ein Fehlerbild | wie heute |

**Fazit Abschnitt 1:** Technisch möglich, aber der Ring zwingt entweder den Biofilter um 725 mm höher oder die Pumpen auf 2,83 m. Wenn Ring, dann zwei Halbringe, nicht ein Ring.

## 2. Anordnung der Anlagenteile nah am Kreislauf

**Einschätzung: machbar, aber der Spielraum ist klein; der Hauptkreislauf ist schon kompakt.**

**Befund zum verlegten Stand.** Pool → Heber (K01/K17, unterflur) → Feinfilter in der Grube → Pumpen → Biofilter → Überlauf Z 1570 sind die zwei Technikgruppen je Linie bei r ≈ 3,4 m, Absetzerkreis (K03–K05) und Notbypass (K56/K57) daneben; gebaut bis zum Verteiler-Eingang (Runde 66) [Q `loop-state.md`]. Hier gibt es **keine Umleitung zu streichen**, ohne gebaute Teile abzubauen.

**Wo Rohr entsteht (Konzept, Polarkoordinaten, ±25 % [E, Skript Abschnitt 4]; Technikgruppen Linie 2 bei az ≈ −100° aus `loop-state.md`, Linie 1 an der Türachse −54° gespiegelt [A]).**

| Strecke | Länge beide Linien | Hinweis |
|---|---|---|
| K11 Verteiler → Beete d40 | 58,9 m | 7 Beete je Linie, Gangkreuzungen unterflur |
| K12 NFT-Strang d32 | 21,4 m | am Tischbein, kein Graben |
| K14 Beet-Abläufe → Sumpf d50 | 58,9 m | größter Rücklaufast |
| K15 Sektorsammler d63 | 32,0 m | 5 je Linie, radial ca. 3,2 m [A] |
| K16 Halbringe d110 | 12,6 m | Wandkrone Pool |
| K58/K59 Sumpf → Rücklauf d40 | 8 m | ≤ 4 m je Linie [Q R45] |

**Alternativkonzept (nur Konzept, nicht berechnet gegen das Modell): zwei Sümpfe oder ein Sumpf im Beet-Schwerpunkt.** Liegt der Sumpf im Schwerpunkt der 7 Beete einer Linie statt an der Technikgruppe, sinkt K14 von 58,9 auf 44,4 m (−14,5 m, −25 %) [E]. Der Schwerpunkt fällt aber in die Nähe der Pool/Tisch-Zone (Platz, Gangkarte nicht geprüft): **offen**. Gegenrechnung: die Förderleitung K58 (d40, bis 4 m) wird dort länger.

**Idee „Beet-Sumpf als Saugsumpf der Hauptpumpen“: verworfen.** Sie sparte rechnerisch 2 Teichpumpen (108 W) und K58/K59. Die Hauptpumpen saugen aber auf Z 120 (geflutet vom Pool, Z 320–515), der eingegrabene Sumpf steht tiefer (Pegel unter Z 0): die Pumpen müssten ansaugen; Selbstansaugung der Pumpen ist nirgends belegt. [E/A: eine Prüfung der Pumpenkennlinie fehlt].

**Idee „Absetzerkreis streichen“** ist Gegenstand von R44 (Kandidat A: Absetzer entfällt, ein Biofilter-Tank, spart 1,77 m² Fläche [Q R44 Überblick]); sie ist unabhängig vom Ring und trifft K03–K05, K07, K19–K21, K23 und 4 kleine Pumpen (je 17 W, zwei in Betrieb), die bereits verlegt sind: Rückbau, nicht Einsparung am Bau. Nicht von mir bewertet.

**Schlammfass und Puffer** (W37, K07/K23) hängen an den Absetzern; fällt der Absetzer, entfällt das Fass.

**Vergleich mit B/C.** Der Ring kürzt weder Hauptkreislauf noch Rücklauf. Er ersetzt nur K11/K12 (80,3 m) durch Ring + Abgänge (108,7 m bei B, 80,7 m bei C): B ist 28 m länger.

**Fazit Abschnitt 2:** Verkürzung gibt es nur beim Beet-Rücklauf (Sumpf-Lage), sonst ist der Plan eng. Nächster Schritt wäre ein Platzcheck der Sumpf-Lage in M10 S4 (ICH, wenn Ben A wählt).

## 3. Schwerkraft nutzen

**Einschätzung: der heutige Plan nutzt sie schon; der Ring verschlechtert die Bilanz.**

**Höhenbilanz heutiger Plan (Z relativ, mm) [Q `leitungsnetz.json`, `m10-leitungen.md`, R45; E].**

| Stufe | Z | Antrieb |
|---|---|---|
| Pool-Spiegel | 515 | Ausgang |
| Seitenablauf → Feinfilter-Auslauf (Heber K01/K17) | Spiegel am Filter 320 (195 mm Heberverlust) | **frei** (Pipe voll, Reserve 85/88 mm nach S2R) |
| Hauptpumpen (4 × 55 l/min) | Saug 120, Druck 255 | **gepumpt**, H 2,0 m |
| Biofilter Zulauf 1420 → Überlauf 1570 | | gepumpt bis hier |
| Verteiler → NFT (Rinne 1000) | 570 mm Druckkopf | **frei** |
| Verteiler → Beete (Tropfrohr ~650) | 920 mm Kopf | **frei** |
| Beetablauf −100 | 615 mm unter Spiegel | Beet-Sumpf, **gepumpt** 1,47 m |
| Rücklauf Halbring 660–720 → Pool | über Spiegel | **frei** |

Gepumpt wird an zwei Stellen: Hauptpumpen und Beet-Sumpf. Jede weitere Stufe kommt nur durch die Höhenlage, nicht durch Planung. Die Beet-Stufe ist **zwingend**, solange der Beetablauf unter dem Pool-Spiegel liegt [Q R45 Abschnitt 3]. Entfällt sie nur durch Anheben der Beete um ≥ 0,7 m oder Absenken des Spiegels: beides Eingriffe in D26/Dom, nicht Teil dieser Prüfung.

**Pumpenleistung je Variante [E, Skript Abschnitt 3; η 25 %, Netzliste].**

| | A heute | B Ring (Druck) | C Hybrid (Booster Beete) |
|---|---|---|---|
| Hauptpumpen 4 × | 72 W (H 2,0 m) = 288 | 102 W (H 2,83 m) = 406 | 288 |
| Absetzer klein (2 in Betrieb) | 34 | 34 | 34 |
| Beet-Sumpf 2 × 60 W × 0,9 | 108 | 108 | 108 |
| Booster Beete (H 1,02 m) | – | – | 2 × 37 = 74 |
| **Summe** | **430 W** (10,3 kWh/Tag) | **548 W** (13,2) | **503 W** (12,1) |
| Pumpstufen (Beetwasser) | 2 | 2 | 3 |

Mehrverbrauch gegen A: B +118 W (+27 %), C +73 W (+17 %). Rechenweg: Hauptpumpe A stimmt mit der Netzliste überein (72 W je Pumpe bei 55 l/min, H 2,0 m). Ring-Hochpunkt 2245 + 50 mm Reserve. Hinweis: Die Netzliste nennt H 2,0 m für 1,1 m statischen Anteil; der Rest (0,9 m) ist Reibung plus 20 % Reserve [E]; für den Ring habe ich ihn unverändert übernommen, der Ring hat aber mehr Rohrweg: reale Mehrleistung eher höher.

**Schwerkraft-Variante des Rings.** Biofilter +725 mm: Pumpen bleiben bei H 2,0 m + 0,725 m = 2,73 m (gleiche Größenordnung wie B). Keine Schwerkraft gewonnen, nur verlagert.

**Fazit Abschnitt 3:** A bleibt die niedrigste Pumpenlast (430 W), und die Schwerkraft-Strecke (Biofilter → Verteiler → Beete/NFT → Rücklauf → Pool) ist bereits vollständig frei.

<!-- ENDE -->

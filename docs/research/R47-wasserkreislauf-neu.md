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

## 4. Flood-and-Drain für die Substratbeete

**Einschätzung: machbar, und zu 80 % schon im Bauteil `ibc_beet` enthalten.** Nur drei Kleinigkeiten sind zu ändern.

**Was das Bauteil heute hat [Q `docs/parts/ibc_beet.md`].**

| Teil | Heute | Wirkung |
|---|---|---|
| Boden | Siebboden PP 8 mm auf 60 × 60-Klötzen (15 innen, 24 außen), Abstand ≤ 420 mm | Medium steht trocken über einem freien Wasserraum (aussen_933: 640 l) |
| Siphon | Standrohr d25, Glocke d75 × 295 (2 Schlitze 10 × 40, Luftloch 10), Medienschutz d110 × 320 (12 Durchbrüche 12 × 12) | leert bis zur Bodenplatte, Ablauf 234 l in 4,3–6,1 min [Q R45 Abschn. 1] |
| Zulauf | Tropfrohr d20, 200–500 l/h = 3,3–8,3 l/min | Siphon-Spitze 38–54 l/min, Faktor 4,6–16: der Siphon springt sicher an |
| Medium | Blähton/Kies 8–20 mm gewaschen, 300 mm tief | Porenraum ca. 40 % [A] |

**Bens Wunsch („Abstandshalter oder Sieb am Boden“) ist damit erfüllt.** Das Bett leert bis zur Bodenplatte, der Raum unter dem Sieb ist frei durchspülbar. Offene Risiken sind andere.

**Befund 1: Löcher zu groß für das kleinste Korn.** Medienschutz-Durchbrüche 12 × 12 mm, Siebboden real D8 (im Modell 12 vereinfacht) gegen Medium ab 8 mm: Körner 8–12 mm fallen durch den Schutz bis in den Siphonbereich und unter den Siebboden. Als Faustregel nennen Hobby-Seiten Korn 10–20 mm und einen Kiesschutz, der Medium aus dem Siphon hält: [Go Green Aquaponics, Gravel](https://gogreenaquaponics.com/blogs/news/how-to-use-gravel-in-aquaponics-systems) (Richtwert 10–20 mm; Feinkorn verstopft den Siphon), [Aquifarm Bell Siphon Physics](https://aquifarm.com/bell-siphon-physics/) (Guard verhindert Eindringen des Mediums; große inerte Medien wie Blähton). Beide sind Hobby-Quellen, also **Kandidat**; die Maße des Schutzlochs gegen das Korn sind eigene Geometrie [E]. **Empfehlung:** Korn 12–20 mm festlegen und Medienschutz-Löcher 8 × 8 mm (oder Siebboden D6) [A]; Bauteil-Parameter `guard_hole` und `grid_hole` ändern. Das ist eine **Bauteiländerung** (Werkstatt), kein Aufbau.

**Befund 2: Schlamm sammelt sich unter dem Sieb.** Feststoffe, die in das Bett laufen (NFT-Anteil wird mechanisch gefiltert, die Beete nicht, vgl. R44), setzen sich im Wasserraum und am Einlauf ab; bei hoher Last bilden sich anaerobe Stellen. Die Quellen sind hobbymäßig und teils gemischt: [Oklahoma State Extension](https://extension.okstate.edu/fact-sheets/recirculating-aquaculture-tank-production-systems-aquaponics-integrating-fish-and-plant-culture) (Sand/Kies verstopfen leicht, Bett-Bearbeitung oder Medienwechsel nötig), [Kentucky State Aquaponics Handbook](https://www.kysu.edu/documents/school-of-agriculture-communities-and-the-environment/aquaponics_handbook_2021_final_022421.pdf) (regelmäßig Feststoffe entfernen); [Upstart University](https://university.upstartfarmers.com/blog/aquaponic-media-surface-area) (große Körnung lässt Feststoffe selten stauen). Bei unserer Last (12,1 kg/m³ Fisch, unter dem FAO-Auslöser 15 [Q R44]) bleibt das Risiko gering, bis NFT nicht mehr filtert. **Gegenmaßnahmen:** (a) Bodenplatte mit 1–2 % Gefälle zum Ablauf: kein Eingriff am IBC-Boden, stattdessen die Stützklötze zum Ablauf hin um 10–20 mm niedriger [A]; (b) Sumpfzone: 30–40 mm tiefe Mulde im Wannenboden um das Standrohr, Medienschutz sitzt darin [A]; (c) **Reinigungszugang:** Steckverbindung (Verschraubung) im Ablauf unter dem Boden, Siphon samt Medienschutz ohne Medienausbau ziehen, Spülstutzen d25 mit Kugelhahn am Sammler.

**Befund 3: Beet-Sumpf unter dem Spiegel.** Der Ablauf (Z −100, Rohrende unter dem Boden) fließt in den Sumpf mit Pumpe. Verstopfung des Siphons wirkt sich aus als „Bett leert nicht“: der Alarmschwimmer (Z 620 mm Pegel) deckt das nicht ab. Zusatz: Bett-Ablaufwächter (Schwimmer im Beet, 12 V) [A].

**Alternativen zum Glockensiphon (Zeitschaltuhr, Dauerstau, Kipp-Mechanik).**

| Option | Vorteil | Nachteil | Fazit |
|---|---|---|---|
| Glockensiphon (heute) | passiv, kein Strom | Anspringen hängt an Zulauf/Luft [Q Aquaponics411: Gleichgewichtsfluss, Siphon startet nicht] | behalten |
| Zeitschaltuhr + Magnetventil im Ablauf | zuverlässig (Foren: „100 %“, ein Nutzer 65.000 Zyklen ohne Ausfall; anekdotisch) | 14 Ventile + Steuerung, bei Stromausfall bleibt Bett voll → Wurzeln ertrinken [Q Foren] | als Rückfall, nicht als Standard |
| Dauerstau mit Standrohr | einfach | kein Fluten/Entleeren, Algen, kaum Sauerstoff im Medium | verworfen (widerspricht Bens Wunsch) |
| Kipp-Mechanik | passiv | in der Recherche **kein** Beleg für Substratbeete gefunden | offen, nicht bewertet |

Quellen: [Aquaponics411 Bell Siphon Tuning](https://aquaponics411.com/how-a-bell-siphon-works-in-aquaponics-systems/), [Aquaponic Gardening Forum, Alternativen](https://aquaponicgardening.ning.com/forum/topics/alternatives-to-bell-siphon-systems). Beides schwach (Forum). Die Siphon-Physik für unsere Maße stammt aus R45 (Bernoulli/Darcy-Weisbach).

**Was am Bauteil zu ändern ist, was nur Aufbau ist.**

1. **Bauteiländerung (Werkstatt):** `guard_hole` und `grid_hole` kleiner als das gewählte Korn; Verschraubung im Ablauf (Reinigungszugang); optional Sumpfmulde und Stützklötze mit Gefälle.
2. **Nur Aufbau (Montage):** Korn 12–20 mm, gewaschen, bis 300 mm; Sicht-/Reinigungsintervall festlegen; Ablaufwächter im Sumpf-Alarm.

**Fazit Abschnitt 4:** Flood-and-Drain gelingt mit dem vorhandenen Bauteil; zwei Maße ändern und einen Reinigungszugang ergänzen. Es hängt nicht an der Frage Ring oder nicht Ring.

## 5. Gesamturteil: Varianten A, B, C

**Definition.** **A** = heutiger Plan, gestrafft (Sumpf-Lage prüfen, Beet-Bauteil ändern, Rest unverändert). **B** = ein Ring d90 (Druck) bei Z 2100/2245 für Beete, NFT und Becken-Frischwasser, Biofilter vor dem Ring, Rücklauf wie heute. **C** = zwei Halbringe nur für die 14 Beete, Booster-Pumpe je Linie, NFT-Strang K12 bleibt, Rücklauf wie heute. Zahlen: `python -X utf8 scripts/r47_rechnung.py` (Rohrmeter ±25 %, Polarkoordinaten, nicht aus dem Modell; Teilezahl = Formteile+Armaturen der Zulaufseite, ohne gerade Rohrstücke).

| | A | B | C |
|---|---|---|---|
| Pumpen elektrisch (W) | 430 | 548 | 503 |
| Pumpstufen für Beetwasser | 2 | 2 | 3 |
| Zulauf-Verteilrohr (m) | 80,3 | 108,7 | 80,7 |
| Formteile+Armaturen Zulauf | 214 | 220 | 232 |
| Gangkreuzungen Zulauf | unterflur, ca. 1 je Außenbeet [A] | 0 (Ü-Band) | 0 für Beete, NFT wie A |
| Stützen im Boden | 0 | 12 | 12 |
| Rücklauf (K14–K16) | 111,5 m | gleich | gleich |
| Höhenänderung | keine | Biofilter +725 mm oder Pumpe H 2,83 m | wie B für Booster |
| Wartung | wie heute | Ring überkopf, Leiter nötig | Halbringe überkopf |
| Risiko | gering, Planstand | hoch: Stützenstatik, Gangkarte, Frost, UV, Leitungsbruch über Gang | mittel |
| Aufwand Modell | Beet-Bauteil ändern (Werkstatt) | Ringstück, Stützen, Plattform/Leitungen K08–K10 neu | Halbringstücke, Booster, Stützen |

**Folgen für M10 S3–S7 und W37.**

| Schritt | A | B/C |
|---|---|---|
| S3 Verteiler, Beete, NFT (K11–K13, K27–K29) | läuft wie geplant | K11 (B auch K12) entfällt als Rohrstrang, dafür Ring und Abgänge |
| S4 Rücklauf, Sumpf, Halbringe | Sumpf-Lage prüfen | unverändert |
| S5, S6 | unverändert | unverändert |
| S7 Abschluss | unverändert | Gangkarte mit Stützen und Ring zusätzlich |
| W37 Beet-Sumpf, Schlammfass | bleibt | bleibt (der Sumpf ist unabhängig vom Ring) |
| Bereits gebaut | nichts betroffen | Biofilter-Anhebung würde K08–K10 (Runde 64–66) und Plattformen treffen |

**Empfehlung: A.** Begründung: (1) Die Schwerkraft-Strecke ist bereits vollständig frei; der Ring macht sie unfreier (Biofilter-Überlauf 530 mm unter Ring-Unterkante). (2) Der Ring spart weder Teile noch Rohr, nur die Gräben zu den Beeten. (3) Mehrleistung +118 W (B) / +73 W (C) gegen 430 W. (4) Er stellt die Stützen-Statik und die Gangkarte zusätzlich offen, während die Regeln (nichts an Streben/Knoten/Haut) schon heute eng sind. (5) Flood-and-Drain braucht keinen Ring und ist im Bauteil fast erledigt.

**Wann C trotzdem sinnvoll wäre:** wenn der Graben-Befund bei S3 zeigt, dass die Beet-Zuleitungen K11 die Gangkarte verschlechtern oder Kollisionen im Graben erzeugen. Dann Halbringe nur für Beete prüfen.

**Zur Idee „Subtanks nah am Kreislauf“:** Absetzerkreis, Schlammfass und Puffer-Station sind schon in der Netzliste; der Hebel liegt bei R44 (Kandidat A), nicht beim Ring.

**Nicht „nicht machbar“.** Keine der Ideen ist physikalisch ausgeschlossen. Der Ring ist machbar mit Mehrkosten in Pumpenhöhe oder Biofilter-Höhe, die der Plan nicht braucht.

**Offene Fragen.**

1. Pumpenkennlinien (Hauptpumpe, Sumpfpumpe): Fabrikat offen [E, `scripts/r47_rechnung.py` rechnet mit η 25 %].
2. Stützen-Statik und Gangkarte-Lauf `check_walkways.py` mit Stützenorten: nicht gerechnet.
3. Rohrlängen aus Polarkoordinaten, nicht aus dem Modell; Technikgruppe Linie 1 an der Türachse gespiegelt [A].
4. Frost und UV: Standort offen, keine Quelle geholt.
5. Entscheidung Ben: A (empfohlen), B oder C.

**Geprüft gegen:** `docs/jobs/R47-wasserkreislauf-neu.md`, `docs/packages/m10-leitungen.md` Abschn. 3, 4, 7, `docs/hydraulics.md`, `data/leitungsnetz.json` (Kanten K01–K59, Kabel, Bilanz), `docs/layout.md`, `docs/system-concept.md`, `docs/parts/ibc_beet.md`, `docs/research/R45-hydraulik-auslegung.md` Abschn. 1 und 3, `docs/research/R44-filter-gegenpruefung.md` Überblick, `docs/loop-state.md` S2b/S2c/S2R; `python -X utf8 scripts/r47_rechnung.py`; Websuche (Stützabstand PVC-U, Flood-and-Drain, Medienbett). Nicht gelesen: `docs/walkway-map.md` über die ersten 25 Zeilen hinaus.

**Offen:** siehe Liste oben; Besitzer: Entscheidung A/B/C liegt bei Ben; Gangkarte und Statik bei Orchestrator/Montage nach Entscheidung.


---

## 6. Nachtrag R47b: Wartbarkeit und Ausfallsicherheit (Wunsch W52, 02.11.2026)

**Problem:** Ben sorgt sich: Verstopft ein vergrabenes Rohr, steht die Anlage still und alles kann sterben. **Intent:** E20 auch nach Wartbarkeit und Ausfallsicherheit entscheiden. **Goal:** Inventar, Risiko, Maßnahmen, ehrliche Bilanz Ring gegen heute, neue Empfehlung. Nichts umgesetzt.

### 6.0 Gesamturteil (zehn Zeilen)

1. **Neue Empfehlung: A+ (heutiger Plan plus Zugänglichkeitsmaßnahmen).** Der Ring ändert an Bens Sorge nichts.
2. **Bens Befund stimmt:** 30,3 m von 54,0 m verlegtem Rohr (56 %) liegen unter Bodenniveau [E, `python -X utf8 scripts/r47_zugang.py`, Z < 400 absolut]. Der Ring betrifft **0 m davon**: alle 30,3 m sind Hauptkreislauf, Absetzerkreis und Notbypass vor dem Verteiler; der Ring ersetzt nur K11/K12 dahinter.
3. **Größter Block ist nicht der kritischste:** Der Absetzerkreis (K03, K05, K19, K21) liegt mit 17,7 m (58 % des Vergrabenen) bei nur 0,13–0,2 m/s, weit unter 0,6 m/s Selbstreinigung (Kandidat, nur Abwasserquellen). Fällt er aus, fehlt nur der Absetzer-Teilstrom, nicht der Umlauf.
4. **Kritische Einzelpfade je Linie:** Heber K01/K17 (1,6 und 0,8 m vergraben, pipe-voll), Filter→Pumpe-Stamm K06/K22 (3,4 und 2,1 m, Strömung 0,36 m/s), dazu der Notbypass K56/K57 (3,2 m), der im Normalbetrieb zu ist und als Totast nie getestet wird.
5. **Ausfallzeit:** Wasserumlauf-Stillstand tötet nicht in Minuten: Luft läuft getrennt; TAN steigt um ca. 4,6 mg/l je Tag bei 130 g/Tag in 28,5 m³ [E, Giftgrenze nicht belegt]. Der harte Termin ist die Luft: 0,8–1,2 h [Q R45 Abschn. 4].
6. **Wirksamste Einzelmaßnahme:** Revisionsstutzen (T mit Stopfen) und Schächte an den vergrabenen Strecken, Durchflusswächter je Linie. Der offene Linie-2-Stumpf (300 mm, K03) ist schon ein halber Stutzen.
7. **Alternative mit dem größten Hebel:** R44 Kandidat A (Absetzerkreis streichen) entfernt 17,7 der 30,3 m, ist aber Rückbau des Gebauten und Bens Entscheidung.
8. **Ring-Bilanz ehrlich:** Vorteil Sichtkontrolle und Elementregler greifbar, Nachteil Leiter, Leckage über dem Gang, Kondensat, UV, Frost. Netto kein Wartungsgewinn für das, was Ben fürchtet.
9. **Folgen:** M10 S3–S7 laufen weiter, mit zusätzlichen Revisionsteilen; W37 unverändert plus Ablaufwächter; Gebautes bleibt, wird nachgerüstet.
10. **Offen:** Mindestgeschwindigkeit und Reinigungsstutzen-Abstand für Aquakultur nicht belegt; Notstrom und Alarm-Schaltschrank offen.

### 6.1 Inventar der unzugänglichen Abschnitte (Frage 1)

Nachgeprüft: `python -X utf8 scripts/r47_zugang.py` liest `data/leitungstrassen.json` (Segment-Mitte Z < 400 absolut = unter Bodenniveau), Durchfluss aus `data/leitungsnetz.json`, Geschwindigkeit mit Innendurchmesser PVC-U SDR 21 und dem größten Durchmesser der Kante. Ergebnis deckt sich mit dem Vorbefund: **30,3 m von 54,0 m.**

| Kante | vergraben m | Rohr | Funktion | l/min | v m/s |
|---|---|---|---|---|---|
| K03 / K19 | 6,3 / 4,0 | d40–50 | Bodenablauf Pool → kleine Pumpe | 12,5 | ≤ 0,2 |
| K05 / K21 | 4,3 / 3,1 | d50 | Absetzer → Feinfilter | 12,5 | 0,13 |
| K06 / K22 | 3,4 / 2,1 | d50–63 | Feinfilter → Hauptpumpe | 55 | 0,36 |
| K02 / K18 | 0,7 / 0,9 | d50 | Feinfilter → zweite Pumpe | 55 | 0,57 |
| K56 / K57 | 1,0 / 2,2 | d63 | Notbypass Pool → Pumpe (Normalbetrieb zu) | 110 | 0,72 |
| K01 / K17 | 1,6 / 0,8 | d75 | Heber Pool → Feinfilter (pipe-voll) | 97,5 | 0,45 |

Bei K03/K19 und den Absetzer-Strecken tragen die Rohre Feststoffe. **Mindestgeschwindigkeit gegen Absetzen:** 2 ft/s ≈ 0,61 m/s Selbstreinigung bei Abwasser: [Iowa SUDAS 3C-1](https://www.iowasudas.org/wp-content/uploads/sites/15/2020/03/3C-1.pdf), [PM Engineer, Sanitary Drainage](https://www.pmmag.com/articles/105924-back-to-basics-sanitary-drainage-systems). Zwei unabhängige Quellen, aber aus der Abwassertechnik, nicht aus der Aquakultur: **Kandidat** für 0,6 m/s. Eine Aquakultur-Quelle fand die Suche nicht. Feste Zusatzbedingung: Das Wasser nach dem Feinfilter (K06, K22) ist feststoffarm (R44), dort ist 0,36 m/s weniger kritisch als am Bodenablauf.

### 6.2 Risiko je Abschnitt (Frage 2)

| Abschnitt | Risiko | Folge bei Ausfall | Pfad | Erkennung heute |
|---|---|---|---|---|
| **K01/K17 Heber** | Luftsack, Biofilm, Fremdkörper; Reserve nur 85/88 mm [Q S2R] | Filterkasten läuft leer, Pumpen trocken, Umlauf der Linie steht | Einzelpfad je Linie; Gegenlinie läuft, Bypass K56 | keine (Hoch-Schwimmer am Korb nur geplant) |
| **K06/K22 Stamm** | Feinfilter-Durchbruch, Biofilm bei 0,36 m/s | Pumpen saugen nichts, Linie steht | Einzelpfad je Linie; K56/K57 umgeht den Filter, nicht den Stamm | keine |
| K02/K18 | wie Stamm, einseitig | eine von zwei Pumpen fällt aus: halber Umlauf der Linie | parallel | keine |
| **K56/K57 Bypass** | Totast, Hahn festgesetzt, Biofilm; nie getestet | Notweg im Notfall nicht verfügbar | Redundanz nur auf dem Papier | keine |
| K03/K19, K05/K21 Absetzerkreis | Verstopfung durch Fest- und Schlammteile bei 0,13–0,2 m/s | Absetzer-Teilstrom fällt aus; Feststoffe nehmen zu | Reserve-Pumpe (K04), sonst Einzelpfad | keine |

**Zeit bis Schaden [Q/E].** Luftausfall 0,8–1,2 h bis 3 mg/l [Q R45 Abschn. 4]. Wasserumlauf steht, Luft läuft: TAN +4,6 mg/l je Tag (130 g/Tag ÷ 28,5 m³) [E, R44-Last D61]; der Grenzwert für Fische ist pH- und temperaturabhängig und hier nicht belegt: **offen**. Biofilter ohne Durchströmung: die Bakterien verbrauchen Sauerstoff weiter, Luft im Biofilter (K45/K46) hält sie am Leben. Bei Pumpenausfall sammelt sich das Wasser im Pool-Filterbereich; das Gesamtrisiko steigt nach Stunden bis Tagen, nicht nach Minuten. Quellenlage: die RAS-Quellen nennen „plötzlichen, katastrophalen Fischverlust“ durch Pumpen- oder Stromausfall [Aquamaof, Redundanz](https://www.aquamaof.com/ras-blog-post/redundancies-and-back-up-systems/) und doppelte Zuleitungen sowie Durchflussmesser je Leitung mit Alarm; Zahlen zu Ammoniak/Nitrit nach Stillstand fand die Suche **nicht**.

**Kritische Einzelpfade zuerst:** (1) Heber je Linie, (2) Filter→Pumpe-Stamm je Linie, (3) Bypass als ungetestete Reserve. Redundanz heute: zwei Linien (Ausfall einer Linie halbiert den Umlauf), zwei Hauptpumpen je Linie, Notbypass.

### 6.3 Maßnahmen mit Standardteilen (Frage 3)

Alle Teile aus der Bibliothek oder PVC-Standard (W43); Abstände sind **[A]**, eine Aquakultur-Quelle zu Reinigungsabständen fand die Suche nicht.

| # | Maßnahme | Wirkung | Teile | Platz | Aufwand Modell | Gangkarte |
|---|---|---|---|---|---|---|
| M1 | **Revisionsstutzen** (T mit Stopfen/Kappe) an jedem Bogen ≥ 45° und alle ca. 3 m der vergrabenen Strecken | Rohr ohne Aufgraben spül- und stoßbar | T d50/d63, Kappe d63 (W39) | 0,1 m neben dem Rohr | ca. 1 Instanz je Stutzen | keine |
| M2 | **Schächte mit Deckel** an Heber-Ende, Bypass-Hahn, Stamm | Hähne und Revision erreichbar | `lt_schacht_kugelhahn_d63` (vorhanden), Deckel trittfest | Schacht ≈ Ø 300 [A] | 1 Schacht je Hahn | trittfest bündig |
| M3 | **Absperrhähne** am Pumpen-Saug und am Stamm | Pumpe oder Filter tauschbar, ein Pfad isolierbar | Kugelhahn d50/d63 | Bibliothek | 2 je Linie | keine |
| M4 | **Bypass-Probelauf** (Hahn monatlich öffnen, Durchfluss prüfen) | Totast bleibt funktional | keine, Betriebsregel | – | Doku | keine |
| M5 | **Durchfluss-/Pegelwächter mit Alarm** je Linie (Pumpen-Druckseite) und Hoch-Schwimmer am Filterkorb | Erkennung in Minuten statt Sichtkontrolle | Handelsteile, Fabrikat offen | Schaltschrank-Signal (E4 offen) | Kabel, 2 Sensoren | keine |
| M6 | **Bodenkanal mit Gitterrost** statt Erdgraben auf den Strecken unter Gängen | Rohr sichtbar und erreichbar, Gang trittfest | Kanal, Gitterrost bündig | Grabenbreite | neues Bauteil | gleich, wenn bündig |
| M7 | **Spülstoß:** Kugelhahn-Spülanschluss an den Absetzer-Kanten, Spitzenfluss 133 l/min [Q R45 Abschn. 0] | löst Ablagerungen | T d50 + Hahn | gering | 1 je Kante | keine |
| M8 | **Zweite parallele Leitung** zum Heber (nicht empfohlen) | verdoppelt Einzelpfad | 2,4 m d75, 2 Muffen | Graben breiter | Rückbau | evtl. eng |

**Zum Gebauten:** Der Stumpf von Linie 2 bei x 0 / y −1649 / Z −1635 (300 mm, offen) kann mit Kappe sofort Revisionsstutzen für K03 werden [Q loop-state S2b]. M1–M3 sind Zusätze an gebauten T und Hähnen, kein Rückbau.

### 6.4 Oberirdisch statt vergraben (Frage 4)

| Strecke | heute | oberirdisch möglich? |
|---|---|---|
| Heber K01/K17 | Graben, pipe-voll | **nein**, muss unter dem Spiegel Z 340 bleiben |
| Bodenablauf K03/K19 | unter dem Pool Z −1635 | **nein**, liegt unter dem Beckenboden |
| Filter-Stamm K06/K22 | Grube | teilweise: Filterkasten steht in Grube Z −496; Grube mit Deckel statt Verfüllen |
| Notbypass K56/K57 | Tiefleitung Z −159 | nein (Filter-Unterkante −96) |
| Absetzer K05/K21 | Gefälle 1,5 % Tiefe | ja, wenn der Absetzer-Auslass höher läge: Rückbau |
| Verteiler → Beete, NFT | U-Graben / Tischbein | NFT ja (am Tischbein), Beete: Graben oder Brücke Z ≥ 2100 |

**Vergleich Graben / Bodenkanal / Brücke:**

| | Graben (Leerrohr) | Bodenkanal mit Rost | Brücke ab Z 2100 |
|---|---|---|---|
| Zugang | Aufgraben | Rost heben | Leiter |
| Gang | frei | trittfest, 700/600 mm bleiben | frei, aber Stützen im Gang |
| Rohrlänge | kurz | wie Graben | länger (Ring: +28 m) |
| Aufwand | gebaut | neues Bauteil | Ring/Stützen |

Gangbreiten A 700 / B 600 / Wandluft 110 mm: Ein bündiger Rost verändert sie nicht, Stützen der Brücke stehen im Gang oder an der Wand und können eine Engstelle verschlechtern (nicht geprüft: Gangkarte nicht gerechnet).

### 6.5 Ring: ehrliche Wartungsbilanz (Frage 5)

| Pro | Contra |
|---|---|
| Sichtkontrolle am Ring (Leckage, Bewuchs) | Leiter für jeden Handgriff; Rohr über dem Gang |
| Elementregler (Kugelhahn) direkt am Beet und Tisch | Leckage tropft auf Gang/Pflanzen |
| Zulauf ohne Graben | Entlüftung, Kondensat und UV im warmen Dach |
| | Frost bei Heizungsausfall (Standort offen) |
| | Stützen: Statik und Gangkarte offen |

**Welche der kritischen Abschnitte aus Frage 1 betrifft der Ring?** Keinen. Alle 30,3 m vergrabenes Rohr liegen vor dem Verteiler. Vergraben bleibt: Heber, Bodenablauf, Filter-Stamm, Bypass, Absetzerkreis, Beet-Sumpf und alle Rücklaufstrecken unter Z 400.

### 6.6 Neue Empfehlung (Frage 6)

A+ = A plus M1 (Revisionsstutzen), M2 (Schächte), M3 (Absperrhähne), M4 (Bypass-Probelauf), M5 (Durchfluss/Pegel-Alarm), M7 (Spülanschluss).

| | A | B | C | **A+** |
|---|---|---|---|---|
| Meter unzugänglich ohne Aufgraben | 30,3 | 30,3 | 30,3 | 30,3 geometrisch, aber mit Revision erreichbar |
| Meter über Kopf (Leiter) | 0 | 21 (+ Abgänge 85) | 21 + 36 | 0 |
| Einzelpfade (Zählung Abschnitt 6.2) | 10 | 7, davon einer für beide Linien | 10 | 10, aber mit Bypass-Probe und Alarm |
| Erkennungszeit | Sichtkontrolle | Sichtkontrolle | Sichtkontrolle | Minuten (Alarm) |
| Aufwand je Wartung | Aufgraben | Leiter für Ring, sonst Aufgraben | wie B | Stopfen ziehen, Hahn schließen |
| Zusätzliche Teile | 0 | Ring, Stützen, Booster | Halbringe, Booster | ca. 20 Stutzen, 4–6 Schächte, 2 Sensoren [A] |
| Pumpenlast | 430 W | 548 | 503 | 430 + Sensoren |
| Risiko | Verstopfung blind | + Ring | + Ring | niedrig |
| Folgen Gebautes/Geplantes | – | Biofilter hoch, K08–K10 neu | wie B | Zusätze an vorhandene T |

**Empfehlung: A+.** Begründung: (1) Bens Sorge gilt den vergrabenen Hauptkreislauf-Strecken, der Ring ändert sie nicht. (2) Revisionsstutzen, Schächte und Alarm sind Standardteile ohne Eingriff in die Höhen. (3) Die Erkennungszeit sinkt von „Sichtkontrolle“ auf Minuten. (4) Der Ring blieb in 5.1 aus anderen Gründen unterlegen und fügt hier keinen Vorteil hinzu.

**Optional, Entscheidung Ben:** R44 Kandidat A (Absetzerkreis streichen) entfernt 17,7 der 30,3 vergrabenen Meter und zwei Einzelpfade; Rückbau des in S2b/S2c Gebauten (K03–K05, K19–K21).

**Folgen.**
1. **M10 S3–S7:** weiter, mit zusätzlichen Instanzen für M1–M3 und Schächten in S3/S4; Alarmkabel in S6.
2. **W37:** Beet-Sumpf und Schlammfass bleiben; Ablaufwächter am Beet-Sumpf (in 4.1 schon genannt).
3. **Neue Bauteile (Planer-Blätter):** Revisionsstutzen d50/d63 (T + Kappe, vorhanden), Schacht-Deckel trittfest, Bodenkanal-Rost (nur wenn M6 gewählt), Handelsteile Durchflusswächter.
4. **Schon Gebautes:** nur Nachrüstung (T mit Stopfen an vorhandenen Bögen, Schächte an Bypass-Hähnen, Kappe auf Linie-2-Stumpf).

**Offen.** (a) Mindestgeschwindigkeit für Aquakultur und Reinigungsabstände sind **nicht** aus Aquakultur-Quellen belegt (Abwasserquellen als Kandidat). (b) Giftgrenze von TAN/Nitrit nach Stillstand nicht belegt. (c) Schaltschrank, Notstrom, Alarm offen (E4). (d) Gangkarte nicht gerechnet. (e) Anzahl und Lage der Stutzen noch nicht geplant (Planer).

**Geprüft gegen:** `docs/jobs/R47b-wartbarkeit.md`; `data/leitungstrassen.json`; `data/leitungsnetz.json`; `docs/packages/m10-leitungen.md` Abschn. 4; `docs/research/R45-hydraulik-auslegung.md` Abschn. 4 (Luftausfall, aus früherem Lesen); `scripts/r47_zugang.py` (Befehl `python -X utf8 scripts/r47_zugang.py`); Websuchen Iowa SUDAS, PM Engineer, Aquamaof. Nicht gelesen: `docs/walkway-map.md`, `docs/jobs/pruefung/W36-W39.md` nur Schlagwortsuche Rohrschelle.
**Offen:** siehe oben. DEINE ENTSCHEIDUNG (Ben): A+ (empfohlen) und ob R44 Kandidat A (Absetzerkreis streichen) geprüft wird.


---

## 7. Nachtrag R47c: Ring mit einheitlichem Fluss (Rückfrage Mitgründer, 02.11.2026)

**Problem:** Der Mitgründer fragt: (1) Wie würde ein Ring die Höhenunterschiede lösen, ohne den Fluss aufzuteilen (alles Wasser durch die Biofilter, ein Pool, ein Nährstoffkreislauf)? (2) Sind 2,83 m Förderhöhe bei Standardpumpen nicht nur eine Energiefrage? **Intent:** E20 auf einer fairen Gegenüberstellung A+ gegen Ring mit einheitlichem Fluss (EINHEIT) entscheiden. **Goal:** ausgearbeitete Ring-Varianten, ehrliche Neubewertung des Höhenarguments, Gesamtempfehlung. Nichts umgesetzt; Aktualitätsprüfung 02.11.: Stand A+, Gebautes bis Verteiler-Eingang (Runde 66) bleibt.
Rechnung: `python -X utf8 scripts/r47_pumpen.py`. Z relativ zum Innenboden.

### 7.0 Gesamturteil (zehn Zeilen)

1. **Der Mitgründer hat bei der Pumpe recht:** 2,83 m und 3,2 m bei 55 l/min sind Standardklasse (Oase Aquarius Premium 6000 liefert nach Parabel-Näherung ≈ 3,5 m bei 55 l/min [Q Datenblatt, E]). Mehrleistung nur +119 W (η 25 %) bis +166 W (η 18 %) = 2,9 bis 4,0 kWh/Tag gegen heute. Als Ausschlusskriterium taugt die Höhe nicht.
2. **Was vom Höhenargument bleibt, ist nicht die Pumpe, sondern der Ort:** Der Biofilter (Überlauf Z 1570) liegt 675 mm unter dem Ring-Hochpunkt (Z 2245). Mit EINHEIT (alles durch den Biofilter, dann Ring) muss das Wasser entweder VOR dem Biofilter auf 2295 oder NACH dem Biofilter um 725 mm gehoben werden. Es gibt keine dritte Möglichkeit.
3. **Drei Ring-Varianten erfüllen EINHEIT (a) bis (e):** B1 Biofilter 725 mm höher (Pumpen heben auf 2,73 m); B2 Booster nach dem Biofilter in einen Druckring; B3 Hochbehälter nach dem Biofilter, Ring per Schwerkraft. Heute erfüllt A+ EINHEIT schon: Verteiler und Beete hängen nur am Biofilter-Überlauf, alle Rückflüsse münden in den einen Pool.
4. **B1 ist die sauberste Variante hydraulisch** (eine Pumpstufe, +119 bis 166 W), aber der teuerste Umbau: 857 kg gefüllter Biofilter auf 1733 mm Beinen (statt 1008), Deckel auf Z 2401, K08 bis K10 und beide Plattformen neu.
5. **B2 lässt das Gebaute stehen** (K10-Ende wird die Saugleitung des Boosters), kostet aber den GANZEN Linienstrom (110 l/min) eine zweite Pumpstufe (+147 bis 205 W) und braucht Pegelregelung am Biofilter.
6. **B3 ist die schwächste:** B2 plus Hochbehälter auf Z 1600 bis 2400 mit 300 l; mehr Teile, mehr Last in der Höhe, kein Gewinn gegen B2 außer Puffer.
7. **Der Ring gewinnt weiterhin nur die Gräben zu den Beeten.** Die 30,3 m vergrabenes Rohr (R47b) berührt er nicht. Ein Ring auf Tischhöhe (unterhalb 1570, per Schwerkraft, am NFT-Strang entlang) löst das Höhenproblem ohne Pumpenmehrleistung, spart dann aber die Gräben nicht (Beete bleiben am Boden).
8. **Verteilung auf mehrere Biofilter:** Heute gibt es EINEN Biofilter je Linie; die Frage stellt sich nur beim dritten Tank (Empfehlung R37) oder zwischen den Linien. Standard: gleiche Zu- und Ablaufhöhen und -längen (Parallelbetrieb) oder Reihe. „Unterschiedlich gut laufen“ ist biologisch, nicht hydraulisch: Der Durchfluss wird von Pumpe und Widerstand bestimmt, nicht von der Leistung des Bettes. Gilt für heute und Ring gleich; belegt nur schwach (Patente, Praxisregel).
9. **Rangfolge:** A+ > B2 > B1 > B3. „Ring ja oder nein“ bleibt **nein**, aber mit anderer Begründung als in R47: nicht Höhe/Energie, sondern Aufwand (zweite Pumpstufe oder Umbau des Gebauten) bei null Gewinn für Wartbarkeit und Fluss-Einheit, die A+ schon hat.
10. **Offen:** Pumpenkennlinien nur als Parabel-Näherung aus Nenndaten; zweiter unabhängiger Hersteller nicht belegt (Pontec ist Oase); Biofilter-Verteilung ohne Fachquelle; Statik/Gangkarte/Dome-Höhe nicht gerechnet. Entscheidung Ben.

### 7.1 Pumpenfrage (Frage 1)

**Datenlage.** [Q] Oase Aquarius Universal Premium 6000: 110 W, 6000 l/h, 5,0 m max. (Hersteller-Datenblatt vom 02.08.2017, [teichfolie.de-PDF](https://teichfolie.de/media/products/Produktdatenblatt_Aquarius_Universal_Premium_6000.pdf), gelesen). [Q] Eco Classic 5500: 60 W, 5300 l/h, 2,8 m max.; Pontec PondoMax Eco 5000: 60 W, 5000 l/h, 2,6 m max. (Händlerangaben, [Kaufland-Listung](https://www.kaufland.at/product/221417471/), [koempf24](https://www.koempf24.de/pontec-pondomax-eco-11000)); beide Marken gehören zu Oase: **kein zweiter unabhängiger Hersteller**. Wilo Yonos PARA und Grundfos UPM3 (Heizungspumpen, Datenblätter gefunden, Kurven nicht auslesbar) sind für ein offenes Becken keine Standardwahl und nicht bewertet. **Kennlinien liegen nicht als Tabelle vor:** ich nähere sie als Parabel H = H0·(1 − (Q/Qmax)²) [A].

**Gegenprobe der Näherung.** Eco Classic 5500 bei 61 l/min: Näherung 1,46 m; R45 nennt 1,47 m [E, Skript Abschnitt 1]. Die Näherung trifft den vorhandenen Messpunkt.

| Pumpe (55 l/min = 3300 l/h) | Förderhöhe nach Näherung | passt für 2,0 / 2,83 / 3,2 m? |
|---|---|---|
| Aquarius Premium 6000 (110 W Nenn) | 3,49 m | ja / ja / ja (knapp) |
| Eco Classic 5500 (60 W) | 1,71 m | nein / nein / nein |
| PondoMax Eco 5000 (60 W) | 1,47 m | nein / nein / nein |

**Folgerung:** Schon die heutigen 2,0 m verlangen die Premium-Klasse (6000 l/h, 5 m), nicht die 60-W-Eco-Klasse; 2,83 und 3,2 m liegen in derselben Pumpenklasse. Der Sprung von 2,0 auf 2,83 m ist ein Größen-, kein Klassensprung. Die Fabrikatsfrage bleibt offen (Netzliste führt „Pumpe_gross“ ohne Fabrikat).

**Leistung je Pumpe bei 55 l/min [E].**

| Förderhöhe | hydraulisch | elektrisch η 18 % | η 25 % | η 30 % |
|---|---|---|---|---|
| 2,0 m (heute) | 18,0 W | 100 W | 72 W | 60 W |
| 2,83 m | 25,4 W | 141 W | 102 W | 85 W |
| 3,2 m | 28,8 W | 160 W | 115 W | 96 W |

**Wirkungsgrad, Quellenprüfung.** Die 25 % der Netzliste (R47) lassen sich aus den Datenblättern als **bester Punkt** (Qmax/2, 0,75·H0) nachrechnen: Premium 6000 ≈ 28 %, Eco Classic 5500 ≈ 25 %, PondoMax 5000 ≈ 22 % [E]. Abseits des besten Punktes, besonders bei gedrosselter Förderung, sinkt η; 18 % ist die untere Klammer [A]. Damit ist 25 % **nicht falsch, aber optimistisch**; ich gebe beide Klammern an.

**Mehrleistung des Rings gegen heute (4 Hauptpumpen) [E].**

| | η 25 % | η 18 % |
|---|---|---|
| H 2,83 m | +119 W = +2,9 kWh/Tag | +166 W = +4,0 kWh/Tag |
| H 3,2 m | +173 W = +4,1 kWh/Tag | +240 W = +5,8 kWh/Tag |

Gegen den Gesamtverbrauch 430 W (R47, 10,3 kWh/Tag) sind das +28 % bzw. +39 %, bei 2,83 m.

**Was vom Höhenargument bleibt.** (1) Nicht die Pumpenhöhe, sondern der **Ort des Biofilters**: Der Biofilter steht zwischen Pumpe und Ring. Eine Pumpe, die mit 2,83 m direkt in den Ring drückt, umgeht ihn und verletzt EINHEIT (c); läuft sie durch ihn, muss der Tank druckdicht sein (er ist ein offener PE-Tank mit Deckel und Belüftung). (2) Die Mehrleistung von etwa 120 bis 170 W ist real und bleibt, egal wie man hebt (B1 mit einer Stufe, B2 und B3 in zwei Stufen). (3) Eine **zweite Pumpstufe** ist ein Ausfallpunkt mehr (B2, B3).

**Sicherung.** `scripts/r47_pumpen.py` und dieser Abschnitt, Commit „R47c: Pumpenfrage“.

### 7.2 Ring-Varianten mit einheitlichem Fluss (Frage 2)

**Ausgangslage heute (A+), gegen EINHEIT geprüft [Q `leitungsnetz.json` K06 bis K16, K58/K59].** Pool → Heber K01/K17 → Feinfilter → 2 Pumpen je Linie (K06, K08/K09) → ein Biofilter je Linie (Zulauf 1420, Überlauf 1570) → K10 → Verteiler → Beete (K11) und NFT (K12) und Überschuss (K13) → Rücklauf (K14 bis K16, Beet-Sumpf K58/K59) → Pool. (a) ja: Verteiler hängt nur am Biofilter-Überlauf. (b) ja: alle Rückflüsse münden in den einen Pool (K16). (c) ja: kein Pumpenweg zu Beeten/NFT außer über den Biofilter (der Notbypass K56/K57 führt Pool → Pumpe, nicht zu den Abnehmern). (d) trivial erfüllt: ein Tank je Linie. (e) ja: der Absetzerkreis ist ein Teilstrom Pool → Absetzer → Feinfilter, Beet-Sumpf und Schlammfass hängen am Rücklauf bzw. am Absetzer. **EINHEIT ist heute schon Stand.** Der Ring muss sie nur halten.

**Gemeinsame Randbedingung Ring:** Unterkante Z 2100 (Gang frei, Regel 4.1), Achse 2145, Hochpunkt 2245 (Schwerkraftring mit 1 % Gefälle); Biofilter-Überlauf also **mindestens Z 2295** für Schwerkraft, oder Druckring mit Entlüfter (Hochpunkt dann ≈ 2190 + Entlüfter [A]). Ring als zwei Halbringe je Linie (R47 Abschn. 1).

**B1: Biofilter angehoben (Schwerkraftring).**
Wasserweg: Pool → Heber → Feinfilter → Pumpen (H 2,73 m) → Biofilter (Zulauf 2145, Überlauf 2295) → Halbring (Gefälle 1 %) → Abnehmer (Beete Tropfrohr 650, Tische 1090) → Rücklauf → Pool.
EINHEIT: (a) ja. (b) ja. (c) ja. (d) wie heute. (e) wie heute.
Pumpen: eine Stufe, H 2,73 m (R47: 2,83 m für B; hier ohne Ring-Hochpunkt-Reserve 100 mm: 1,83 m statisch plus 0,9 m Rest) [E].

**B2: Booster nach dem Biofilter (Druckring).**
Wasserweg: Pool → Heber → Feinfilter → Pumpen (H 2,0 m wie heute) → Biofilter (Überlauf 1570, gebaut) → Saugleitung K10 (heutiges Ende, Z 1970 Skript) → Booster (110 l/min je Linie, H ≈ 1,0 m) → Druck-Halbring (Hochpunkt 2190 mit Entlüfter) → Abnehmer → Rücklauf → Pool.
EINHEIT: (a) ja, der Booster sitzt hinter dem Biofilter. (b) ja. (c) ja, **sofern der Booster den GANZEN Linienstrom fördert** (R47 Variante C lieferte nur den Beet-Anteil, das war EINHEIT-konform nur, weil der NFT-Strang ebenfalls hinter dem Biofilter hing; bei einem gemeinsamen Ring hängen alle Abnehmer am Booster). (d) wie heute. (e) ja. **Neu: Pegelführung.** Der Biofilter hat einen freien Überlauf; eine Pumpe dahinter braucht entweder einen Puffer (Sammelschacht, dann ein Tank mehr) oder Schwimmerregelung, sonst läuft der Überlauf über, wenn der Booster steht. Der Überlauf bliebe als Notweg in den Rücklauf: das Wasser hat den Biofilter durchlaufen und mündet in den Pool, EINHEIT (c) bleibt gewahrt. Ein Booster-Ausfall stoppt den Ring, nicht den Kreislauf.

**B3: Hochbehälter nach dem Biofilter (Schwerkraftring).**
Wasserweg: Pool → Heber → Feinfilter → Pumpen (2,0 m) → Biofilter (1570) → Booster (H ≈ 1,4 m) → Hochbehälter (Spiegel ≥ 2295, ≈ 300 l) → Halbring per Schwerkraft → Abnehmer → Rücklauf → Pool.
EINHEIT: wie B2; zusätzlich ist der Hochbehälter ein Pufferglied im Wasserweg, kein Nebenstrom, solange der Überlauf des Hochbehälters in den Rücklauf geht (e) erfüllt.

**B4 (ergänzend): Ring auf Tischhöhe.** Ringleitung unterhalb 1570 am bestehenden NFT-Strang (Tischbeine, kein Gang), gespeist per Schwerkraft aus dem Biofilter-Überlauf wie K12. Löst die Höhe ohne Mehrleistung. Die Beete (Z 650, Außenring r ≈ 5,2 m) bleiben aber unerreicht ohne Querung der Gänge: das Argument „kein Graben“ entfällt, B4 ist technisch A mit längerem K12 [A, nicht gerechnet, keine Quelle]. Nur zur Vollständigkeit.

| | B1 | B2 | B3 | B4 |
|---|---|---|---|---|
| EINHEIT (a) bis (e) | ja | ja, Pegelführung nötig | ja, Hochbehälter im Weg | ja |
| Pumpstufen für das Linienwasser | 1 | 2 | 2 | 1 |
| Änderung am Gebauten | K08 bis K10, Plattform, Biofilter | K10-Ende wird Saugleitung | wie B2 | keine |
| Neue Teile | Ring, Stützen | Ring, Stützen, 2 Booster, Pegel | + Hochbehälter, Konsole | Ring-Strang |

### 7.3 Höhenplan und Bauteile (Frage 3)

**Z-Plan relativ, mm [E aus `leitungsnetz.json`, `docs/parts/tank.md`, R47].**

| Punkt | A+ / heute | B1 | B2 | B3 |
|---|---|---|---|---|
| Saugspiegel Feinfilter | 320 | 320 | 320 | 320 |
| Hauptpumpe saug / druck | 120 / 255 | 120 / 255 | 120 / 255 | 120 / 255 |
| Biofilter-Zulauf | 1420 | **2145** | 1420 | 1420 |
| Biofilter-Überlauf | 1570 | **2295** | 1570 | 1570 |
| Deckel / Belüftung | 1676 | **2401** | 1676 | 1676 |
| Plattform-Oberkante / Beinlänge | 570 / 1008 | **1295 / 1733** | 570 / 1008 | 570 / 1008 |
| Booster | – | – | auf Plattform, Saug 1570 | auf Plattform |
| Hochbehälter-Spiegel | – | – | – | ≥ 2295 (Boden ≈ 1600) |
| Ring Unterkante / Achse / Hochpunkt | – | 2100 / 2145 / 2245 | 2100 / 2145 / ≈ 2190 + Entlüfter | 2100 / 2145 / 2245 |
| Abnehmer Beet / Tisch | 650 / 1090 | wie A | wie A | wie A |
| Rücklauf Halbring | 660 bis 720 | wie A | wie A | wie A |

**Folgen.**
1. **Gebaute Leitungen K08 bis K10 (Runde 64 bis 66):** B1 verlegt sie vollständig neu (Zulauf 1820 → 2545 im Skript-Z; Überlauf 1970 → 2695), dazu beide Plattformen und Biofilter-Instanzen. B2/B3: K10 bleibt, wird Saugleitung; K08/K09 bleiben. K01 bis K06/K22 sind in allen Varianten unberührt (Heber-Reserve 85/88 mm [Q S2R] unabhängig).
2. **Tankhöhe (Bauteilblatt `tank.md`):** Tank gross 1444 mm hoch + Randwulst; Biofilter gefüllt ≈ 857 kg [Q tank.md] auf 4 Beinen 40 × 40 × 2,5 mm. Bei B1 wachsen die Beine von 1008 auf 1733 mm (+72 %).
3. **Statik B1 (Überschlag [E, Annahmen: Stahl E = 210 GPa, Gelenklager, Streben nicht angerechnet]):** Knicklast je Bein ≈ 61 kN (≈ 6,2 t) gegen 214 kg Last je Bein: Faktor ≈ 29, Knicken ist kein Problem. Kippen ist das Thema: Schwerpunkt ≈ 1,7 m über Boden, Standbreite ±390 mm (Fußplatten, je 2 × M8): Kippen ab ≈ 0,23 g Seitenlast [E]; Anstoßlast, Erdbeben und Befüllung bei Schwall sind **nicht bewertet** (offen). Plattform-Bodenlast bleibt gleich (857 kg je Fuß-Quartett).
4. **Zugang zum Biofilter:** Revisionsöffnung D200 im Deckel (Z 1676 heute, A: bereits erhöht, Tritt nötig); B1: Deckel Z 2401 → Leiter oder Podest, Medienwechsel (K1-Träger) über Kopf, Belüftung Ø16 im Deckel ebenfalls hoch. B2/B3: Zugang wie heute; Booster auf der Plattform (Z 570) leicht erreichbar.
5. **Kreuzung mit Gang / Ü-Band:** Ring in allen B-Varianten auf Z 2100 bis 2245 (Ü-Band, Stützen 12 Stück [E, R47]); Gangkarte nicht geprüft. B2 braucht zusätzlich einen Aufstieg vom Booster (Plattform Z 570) auf 2190: Steigleitung d63 (110 l/min: v 0,9 m/s [E]) in der Technikgruppe, außerhalb des Gangs [A].
6. **Deckenhöhe des Doms:** an r = 3,4 m ist die Dom-Innenhöhe nicht in den gelesenen Eingaben; B1 Deckel 2401 und B3 Hochbehälter (oben ≈ 2400) brauchen sie: **offen**, Planer prüft aus dem Modell.
7. **Plattform B3:** Hochbehälter 300 l + Behälter ≈ 330 kg auf Z 1600 an der Technikgruppe: eigene Konsole oder Standfüße; nicht an Tank- oder Pumpentafeln (Regel 7).

**Sicherung.** Commit „R47c: Ring-Varianten und Höhenplan“.

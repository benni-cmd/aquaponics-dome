# R60: Stärkere Pumpe mit Venturi-Injektoren statt Gebläse und Luftleitungen: spart das Teile, Strom und Risiko?

**Priorität:** H · **Auftrag seit:** 05.11.2026 (Start-Auftrag `docs/jobs/start/R60-pumpe-statt-geblaese.md`, Commit 55117c1; Idee von Ben) · **Bearbeitet:** 05.11.2026 · **Rolle:** Fachrecherche, nur lesen und eine Datei schreiben; nichts gekauft, nirgends angemeldet, kein Modell, `data/` unverändert · **Zielparameter:** keiner in `data/params.json`; berührt T85 bis T88 (Gebläse, Verteiler, Scheiben), Netz K44 bis K51, `docs/jobs/M10-S5-LUFT.md`, R54, R55.
**Problem:** Ben schlägt vor: eine stärkere Wasserpumpe, die im Normalbetrieb mit niedriger Grundlast läuft und genug Druck für Venturi-Injektoren hat; dann entfallen Linear-Membranpumpen, Luftverteiler und Luftleitungen. R54 und R55 lehnten Venturi ab, weil der Pumpendruck (0,2 bis 0,4 bar) zu klein ist und die Luft mit der Pumpe ausfällt. **Intent:** weniger Teile und Leitungen (Designprinzip 3), ohne die Fische zu gefährden (Prinzip 9). **Goal:** belegte Gegenüberstellung "Gebläse + Scheiben (heute)" gegen "stärkere Pumpe + Venturi" mit Strom pro Jahr, Teilezahl, Sauerstoffbilanz (46 bis 71 g O₂/h), Ausfallsicherheit und einer Entscheidungsfrage.
**Herkunft:** [Q] Seite oder PDF selbst gelesen (PDF mit `pdftotext` lokal ausgelesen) · [Q-Treffer] nur Suchausschnitt oder Zusammenfassung · [E] eigene Rechnung (Befehl daneben oder in Anhang B) · [A] Annahme. Zwei unabhängige Quellen je Aussage nur dort, wo der Text zwei Quellen nennt; Hersteller-Unterlagen desselben Herstellers zählen als **eine** Quelle.

## Antwort in sechs Sätzen
1. **Nein, nicht als Ersatz.** Das Umlaufwasser (220 l/min) kann bei 28 °C und 5 mg/l im Pool höchstens **37 g O₂/h** tragen (bei 110 % Gesamtgasdruck 48 g/h), also 53 bis 67 % von 71 g/h, selbst wenn der Injektor alles perfekt löst [E, Abschnitt 2.3]. Ein Luftsystem bliebe nötig.
2. **Strom pro Jahr:** heute 492 W = **4 310 kWh** (288 W Pumpen + 204 W Gebläse, 8 760 h). Venturi nach der gelesenen Mazzei-Tabelle: **606 W = 5 310 kWh** bei nur 34 l/min Luft (26 % der 130 l/min des Plans), oder **rund 840 bis 1 220 W = 7 300 bis 10 700 kWh** bei 68 l/min Luft (52 %). Nur der günstigste Literaturwert (SAE 2,3) läge bei 3 560 bis 4 210 kWh; für diese Anlage ist er nicht belegt.
3. **Pumpe und "Grundlast":** Eine belegbare Pumpe gibt es (Grundfos CRNE 10-1: 12,1 m³/h bei 10 m, Edelstahl, Trinkwasser-Zulassung WRAS und ACS), aber ein Venturi braucht den Druck dauernd; drosselt man auf 90 % Drehzahl, sinkt die Leistung auf 72 % (606 auf 436 W), die Luft aber auf 67 % (34 auf 23 l/min), und darunter bricht die Ansaugung ein.
4. **Teile netto:** nicht weniger, sondern **+5 bis +10** (13 entfallen, 18 bis 23 kommen dazu); die Gebläse bleiben, weil Biofilter, Drittbecken und Zweitbecken Luft brauchen (K45, K46, K49, K51).
5. **Ausfall:** schlechter. Pumpen- oder Netzausfall nimmt Wasser und Luft zugleich; Verkalkung oder Verstopfung trifft alle Injektoren mit demselben Wasser; Reserve bliebe ein 12-V-Notluftsatz (Rettungszeit 3,1 bis 4,7 h statt 2,4 h ohne Luft bei 71 g/h) oder eine zweite Pumpe.
6. **Offen bleibt eine Messung**, nicht eine Rechnung: die Sauerstoffübertragung eines Injektors in 2,17 m Wasser ist nirgends belegt; Entscheidungsfrage unten.

## Kurzvergleich
| | **Heute (Plan)** | **V-A: Ben wörtlich** (1 Edelstahlpumpe + 4 × Mazzei 1583 in der Umlaufleitung, Volllast, Eingang 0,94 bar) | **V-B: 784-Klasse, Eingang 1,38 bar** (alle 220 l/min über Injektoren; braucht 11,9 m Hub, mehr als die CRNE 10-1 liefert) |
|---|---|---|---|
| Luft | 130 l/min (Spitze 205) | 34 l/min | 68 l/min |
| O₂ im Luftstrom (Luft × 16,2 g/h je l/min) | 2 106 g/h | 549 g/h | 1 095 g/h |
| nötige Übertragung im Becken für 71 g/h (46 g/h) | 3,4 % (2,2 %) | 12,9 % (8,4 %) | 6,5 % (4,2 %) |
| elektrische Leistung | 492 W (288 + 204) | 606 W | rund 840 bis 1 220 W |
| kWh pro Jahr | 4 310 | 5 310 | 7 300 bis 10 700 |
| Teile Luft- und Pumpenseite | Bezugswert | +5 bis +10 | +17 bis +22 (7 Injektoren statt 4) |
| Ausfall | N+1 Gebläse, Pumpen einzeln | Pumpe weg = Wasser und Luft weg | wie V-A |
| Anschaffung grob (Abschnitt 4.2) | rund 2 100 € (2 Gebläse 745 € netto, 4 Tauchpumpen rund 1 380 €) | mindestens 4 500 € (1 CRNE 10-1), mit Reservepumpe 9 000 €, plus 4 Injektoren (EU-Preis offen) | wie V-A, aber zweistufige Pumpe (Preis offen) |

Belegt für Scheiben ist eine Feldübertragung von **2,1 bis 4,2 %** (R45); für Injektoren in 2,17 m Wasser gibt es **keinen** Feldwert (Abschnitt 2.4). Rechnung der Spalte "Heute": `python -X utf8 -I -c "print(130*16.2, 71/(130*16.2)*100, 46/(130*16.2)*100)"` ergibt 2106, 3,4 und 2,2.

## Suchplan
- Anfragen (de/en): 1) Mazzei injector performance table air suction SCFH; 2) Mazzei troubleshooting, installation, solids; 3) venturi aeration SAE, air intake l/min, aquaculture; 4) total gas pressure fish culture recirculating; 5) variable speed pumping static head affinity laws; 6) Grundfos CRNE 10-1, Speck BADU Eco VS Datenblatt und Preis; 7) venturi noise, CO₂ stripping; 8) Mazzei Händler Europa.
- Quellenarten in Rangfolge: Herstellertabellen und Datenblätter (Zahlen) > Fachartikel und Messungen (Gegenprobe) > Händlerseiten (Preise, Bezug) > Suchzusammenfassungen (nur als [Q-Treffer]).
- Grenze: die Mazzei-Tabelle kam als PDF; `WebFetch` lieferte nur Binärdaten, `pdftotext -raw` las sie lokal. Mazzei TB 12 (Partikeltabelle) war ein eingebettetes Bild und wurde mit Python entpackt und angesehen. Energies, Laval, DOE-Merkblatt und electrical-engineering-portal waren gesperrt oder leer. Kennlinien (Grundfos P1, Speck Q-H) liegen nur als Bild vor.

## 1 Welche Pumpe? (Frage 1)
**Anforderung:** 220 l/min Umlauf und 0,7 bis 1,4 bar Differenz am Injektor; Gegendruck am Austritt 0,34 bar (Pool-Boden 0,21 bar [E] `python -X utf8 -I -c "print(2.17*0.0981)"` plus 0,13 bar Leitung [A]). Bei 5 psi Ausgang entspricht das **15 bis 23 psi Eingangsdruck** (1,03 bis 1,6 bar); die Tabellen unten sind nach Eingangsdruck sortiert. Die heutigen Tauchpumpen (R59: Oase Eco Premium, 55 l/min bei 2,3 m) liefern 0,23 bar und **keinen** Injektordruck; das bestätigt R54.

| Pumpe | Daten (Quelle) | Leistung | Lebensmittel und Fisch (D85) | Europa und Preis | Urteil |
|---|---|---|---|---|---|
| **Grundfos CRNE 10-1 N-FGJ-A-E-HQQE**, Art. 98390335 | 12,1 m³/h bei 10 m, Hmax 14,3 m, 3 400 min⁻¹ (Bereich 360 bis 4 000), 1×230 V, Umrichter und PI-Regler im Klemmenkasten, Drucksensor [Q, Datenblatt 30.11.2022] | Motor 0,75 kW, Motorwirkungsgrad 85,2 % (Volllast) [Q]; hydraulisch 330 W [E]; P1 etwa 0,65 kW [E, A: Pumpe 60 %]; Kennlinie nur als Bild | Edelstahl EN 1.4408 und 1.4401 (AISI 316), SiC/SiC-Gleitring, EPDM; **"Trinkwasser: WRAS, ACS"**, kein KTW genannt [Q] | Hersteller Dänemark; Datenblatt über UK-Händler; **Preis für 98390335 nicht gefunden**; Preisniveau 4 484 € netto bei anderer Variante (1×200 bis 240 V, 60 Hz) [Q-Treffer, Partao] | **Empfehlung, falls Venturi gebaut würde** |
| Speck BADU Prime Eco VS, Art. 219.0208.138 | 1~230 V, P2 1,10 kW, P1 0,03 bis 1,40 kW, 600 bis 3 000 min⁻¹ [Q, Katalog BADU GREEN] | Q-H-Kennlinie nur als Bild; Q bei 7 bis 14 m nicht ablesbar | Gehäuse und Laufrad PP-GF30, Gleitring Kohle/Keramik/NBR, Elastomere NBR/Viton, Saugsieb 3,2 × 2,6 mm [Q]; kein Lebensmittelnachweis | 1 149 bis 1 418 € brutto [Q-Treffer, Check24, guide-piscine.fr] | Rückfall, Betriebspunkt offen |
| Oase Eco Premium 8000 (R59) | ≤ 2,3 m | ≤ 65 W je Pumpe | keine Teichpumpe hat einen Nachweis (R59) | Händler: nicht mehr erhältlich [Q-Treffer] | kein Injektordruck |

**Betriebspunkt der CRNE 10-1:** Mit der Näherung H = x²·14,3 m − 0,02937·Q² (aus Hmax und dem Nennpunkt, [E, A]) liefert sie bei 13,2 m³/h etwa 9,2 m. Mit 2,17 m Saugdruck am Poolboden und 5 psi Ausgang trägt das einen Injektor-Eingangsdruck von rund 16 psi (1,1 bar), also die **15-psi-Zeilen** (Differenz 0,7 bar). Die 20-psi-Zeilen (Eingang 1,38 bar, Differenz 1,0 bar) brauchen 11,9 m bei 13,2 m³/h [E] `python -X utf8 -I -c "print(20*0.70307-2.17)"`, also die zweistufige CRNE 10-2 (nicht gelesen, [A]); Bens obere Grenze von 1,4 bar Differenz liegt noch darüber.
**D85:** Anders als jede Teichpumpe in R59 hat die CRNE einen belegten Trinkwassernachweis (WRAS, ACS); KTW fehlt in der Angabe.

### Leistung bei Volllast und bei gedrosselter Grundlast
Betriebspunkt: 4 × Mazzei 1583 (14,5 gpm gleich 55 l/min bei 10 psi), Pumpe am Poolboden, Ausgang 5 psi, Wirkungsgrad gesamt 0,51 (Pumpe 60 % [A] mal Motor und Umrichter 85,2 % [Q]); Rechnung in Anhang B.
| Drehzahl | Eingangsdruck am Injektor | Umlauf | Luft | Leistung P1 | Luft je W |
|---|---|---|---|---|---|
| 100 % | 13,6 psi (0,94 bar) | 256 l/min | 33,9 l/min | 606 W | 0,056 |
| 90 % | 11,4 psi (0,79 bar) | 233 l/min | 22,6 l/min | 436 W | 0,052 |
| 80 % | 9,3 psi (0,64 bar), unter dem Tabellenbereich | 213 l/min | etwa 12 bis 14 l/min [A] | etwa 300 W | etwa 0,04 |
| 70 % | 7,4 psi (0,51 bar), unter dem Tabellenbereich | 194 l/min | etwa 3 bis 8 l/min [A], nahe dem Nullpunkt der Ansaugung | etwa 190 W | etwa 0,02 bis 0,04 |

**Gilt "niedrige Grundlast", wenn das Venturi dauernd Druck braucht? Nein.**
1. Die Leistung folgt der Kubikregel (0,8³ = 0,51; Rechnung 300/606 = 0,495), die **Luft aber nicht**: bei 90 % Drehzahl fällt sie auf 67 %, bei 80 % auf etwa 36 bis 40 % (Extrapolation unter 10 psi), weil der Injektor ein Mindestgefälle verlangt (Ansaugen beginnt bei etwa 20 %, wirksam ab 25 bis 30 % Differenz [Q, Mazzei TB 10, Installation Notes; R54: Mundoriego, Pumps & Systems]). Luft je Watt wird bei Drosselung **schlechter**, nicht besser; die Mazzei-Tabelle zeigt den besten Wert bei 15 bis 30 psi.
2. Der Sauerstoffbedarf hat **keine Grundlast unter Spitze**: der Fischanteil allein (46 g/h) ist 65 % der Spitze (71 g/h) und läuft rund um die Uhr; die Pumpe liefe also fast dauernd am Injektorpunkt.
3. Die Kubikregel stimmt für Kreise ohne statische Höhe; bei statischer Höhe warnt der Europump/Hydraulic-Institute-Leitfaden vor Fehlern [Q-Treffer, zwei Suchzusammenfassungen; Volltext nicht lesbar]. Der Speck-Katalog gibt für den Poolkreis 100, 60, 30, 12 und 5 % Leistung bei 3 000, 2 500, 2 000, 1 500 und 1 100 min⁻¹ an [Q], das ist die Kubikregel für einen Reibungskreis.
4. **Nebenbefund (unabhängig vom Venturi):** Ohne Injektor liefe eine Kreiselpumpe den Umlauf (13,2 m³/h bei 2,3 m, hydraulisch 83 W [E] `python -X utf8 -I -c "print(13.2/3600*9.81*1000*2.3)"`) mit etwa 220 W [E, A: Pumpe 50 %, Umrichter 75 % bei Teillast] statt 288 W. Die P1-Kurve ist nur ein Bild; der Gewinn von etwa 70 W wäre bei rund 4 500 € gegen etwa 1 400 € für vier Tauchpumpen (4 × 345 €, R59) nicht wirtschaftlich.

## 2 Injektor-Daten und Sauerstoff (Frage 2)
### 2.1 Die gelesene Mazzei-Tabelle (schließt Lücke 2 aus R54)
Quelle: Mazzei Injector Company, "Injector Performance Table, Air Suction Capacity", REV 2014 (Copyright 2018), `oxidationtech.com/downloads/Mazzei/Injector-Performance-Table.pdf` [Q]. Der PDF-Text kam mit `pdftotext -raw` in lesbarer Zeilenfolge; die Zuordnung ist geprüft: (a) für 584, 684, 784, 1078-03 und 1583 steigt die Luft mit dem Eingangsdruck und fällt mit dem Ausgangsdruck monoton, (b) die **metrische Tabelle im selben PDF** (kg/cm², l/min) gibt für 20 psi und 5 psi Ausgang 10,0 / 10,4 / 16,8 l/min für 784 / 1078-03 / 1583, gleich der Umrechnung der imperialen Werte (21,2 / 22,1 / 35,6 SCFH) [E] `python -X utf8 -I -c "print(21.2*0.471947,22.1*0.471947,35.6*0.471947)"`. Fußnote der Tabelle: Klammerwerte sind der Ausgangsdruck, bei dem die Ansaugung stoppt. **Nicht verwendet:** die Spalte 885X-03 (in Mazzeis eigener Tabelle nicht stimmig: 21,8 / 12,9 / 18,5 l/min bei 30 / 35 / 40 psi Eingang). Eine zweite, unabhängige Tabelle desselben Herstellers gibt es nicht; die Größenordnung bestätigt eine **unabhängige Messung** an einem anderen 1"-Venturi: 26 l/min Wasser, 22,5 l/min Luft bei 0,75 bar vor dem Venturi, Düse 15 bis 45 cm tief [Q, Demeekul u. a., Int J Agric & Biol Eng 18(3):58 bis 62, 2025, DOI 10.25165/j.ijabe.20251803.8962; Zeitschrift und Einheiten der KLa-Werte von mäßiger Qualität]. Dieses Venturi saugt je Wasser etwa doppelt so viel Luft wie ein Mazzei 784 bei gleichem Druck (0,87 gegen 0,39 bei 0 psi Ausgang); ein besserer Injektor ist also denkbar, aber nicht belegt.

Auszug (Wasserstrom unabhängig vom Ausgangsdruck; Luft bei Ausgang 5 psi und 0 psi):
| Modell | Eingang | Wasser (gpm gleich l/min) | Luft bei 5 psi (SCFH gleich l/min) | Luft bei 0 psi (SCFH) |
|---|---|---|---|---|
| 584 (3/4", PP) | 20 psi (1,38 bar) | 4,0 gleich 15,1 | 8,2 gleich 3,9 | 20,5 |
| 584 | 30 psi (2,07 bar) | 4,9 gleich 18,5 | 13,6 gleich 6,4 | 26,1 |
| 784 (3/4") | 15 psi (1,03 bar) | 7,5 gleich 28,4 | 16,5 gleich 7,8 | 28,8 |
| 784 | 20 psi | 8,6 gleich 32,6 | 21,2 gleich 10,0 | 33,7 |
| 784 | 30 psi | 10,6 gleich 40,1 | 32,5 gleich 15,3 | 48,2 |
| 1078-03 (1") | 20 psi | 10,5 gleich 39,7 | 22,1 gleich 10,4 | 55,0 |
| 1078-03 | 30 psi | 12,9 gleich 48,8 | 46,4 gleich 21,9 | 70,6 |
| 1583 (1,5") | 10 psi (0,69 bar) | 14,5 gleich 54,9 | 8,3 gleich 3,9 | 85,3 |
| 1583 | 20 psi | 20,6 gleich 78,0 | 35,6 gleich 16,8 | 133 |

Umrechnung: 1 gpm = 3,785 l/min, 1 SCFH = 0,4719 l/min. Der Injektor erzeugt den Druckunterschied nicht selbst; er braucht den Wasserstrom der Tabelle, sonst fällt die Ansaugung ab oder weg [Q, Mazzei TB 10].

### 2.2 Alle 220 l/min über Injektoren (Ausgang 5 psi, Pumpe am Poolboden)
Pumpenhub = Eingangsdruck − 3,09 psi (Saugdruck am Poolboden); hydraulische Leistung = 220 l/min mal Hub; elektrisch bei Gesamtwirkungsgrad 0,51 (Grundfos-Klasse [A]) und 0,35 (gemessen am Speck-Energielabel: 125 l/min bei 2,8 m, 171 W [Q], hydraulisch 57 W, also 33 % [E]). Beispielbefehl für die 784 bei 20 psi: `python -X utf8 -I -c "G=3.78541;S=0.471947;q=8.6*G;a=21.2*S;print(round(q,1),round(a,1),round(220/q*a,1),round(220/60000*(20-3.09)*6.89476*1000))"` ergibt 32,6 l/min, 10,0 l/min, 67,6 l/min Luft gesamt und 428 W hydraulisch.
| Modell | Eingang | Luft gesamt | O₂ im Luftstrom | nötige Übertragung 71 / 46 g/h | P hydraulisch | P elektrisch (0,51 / 0,35) |
|---|---|---|---|---|---|---|
| 584 (EU kaufbar) | 20 psi | 56 l/min | 910 g/h | 7,8 / 5,0 % | 428 W | 838 / 1 222 W |
| 784 | 15 psi (1,03 bar) | 60 l/min | 977 g/h | 7,3 / 4,7 % | 301 W | 591 / 860 W |
| 784 | 20 psi (1,38 bar) | 68 l/min | 1 095 g/h | 6,5 / 4,2 % | 428 W | 838 / 1 222 W |
| 784 | 30 psi (2,07 bar) | 84 l/min | 1 362 g/h | 5,2 / 3,4 % | 680 W | 1 334 / 1 944 W |
| 1078-03 | 40 psi (2,76 bar) | 107 l/min | 1 738 g/h | 4,1 / 2,6 % | 933 W | 1 830 / 2 666 W |
| 1583 | 20 psi | 47 l/min | 768 g/h | 9,2 / 6,0 % | 428 W | 838 / 1 222 W |

Die elektrische Leistung enthält den Umlauf (die Pumpe fördert die 220 l/min ohnehin). Gegen heute (492 W, 130 l/min) liegt die günstigste Zeile (784, Eingang 1,03 bar) bei **1,2- bis 1,7-fachem Strom mit 46 % der Luft**; bei 1,38 bar sind es 1,7- bis 2,5-facher Strom mit 52 % der Luft, bei 2,07 bar 2,7- bis 4-facher Strom mit 65 %. Die 20- und 30-psi-Zeilen brauchen mehr Hub, als die CRNE 10-1 liefert (Abschnitt 1). **Luft je zusätzlichem Watt** (Venturi-Leistung minus 288 W Umlauf): Gebläse 0,64 l/min je W; Venturi 0,05 bis 0,12, also **5- bis 14-mal weniger** [E] `python -X utf8 -I -c "print(130/204, 67.6/(838-288), 84.1/(1944-288))"`.

### 2.3 Wie viel Sauerstoff kann der Umlauf überhaupt tragen?
Das ist die stärkste Aussage gegen "Venturi in der Umlaufleitung", unabhängig vom Injektortyp. Das Wasser, das mit gelöstem Sauerstoff aus dem Kreislauf in den Pool zurückkehrt, trägt nur die Differenz zum Pool-Wert. Cs bei 28 °C 7,83 mg/l, Pool-Soll 5 mg/l, Umlauf 13,2 m³/h (alle aus R45 und `system-specs`).
| Rückwasser enthält | Aufnahme | Sauerstoff je Stunde | Anteil von 71 g/h | Anteil von 46 g/h |
|---|---|---|---|---|
| 100 % Sättigung (idealer Injektor) | 2,83 mg/l | 37,4 g/h | 53 % | 81 % |
| 103 % Gesamtgasdruck (empfindliche Fische) | 3,06 mg/l | 40,5 g/h | 57 % | 88 % |
| 110 % Gesamtgasdruck (EPA-Richtwert) | 3,61 mg/l | 47,7 g/h | 67 % | 104 % |
Für 71 g/h müsste das Rückwasser **10,4 mg/l** haben, gleich **133 %** der Sättigung; Luft enthält 78 % Stickstoff, der Gesamtgasdruck läge dann bei etwa 133 % [E, Annahme: Gleichgewicht mit Luft]. Rechnung: `python -X utf8 -I -c "Cs=7.83;print((Cs-5)*13.2,(Cs*1.10-5)*13.2,5+71/13.2,(5+71/13.2)/Cs*100)"` ergibt 37,4, 47,7, 10,4 und 132,6. Der freie Fall am Beckenzulauf (7 bis 11 g/h, R55) liegt **innerhalb** dieser Grenze, nicht zusätzlich. Ein Injektor in der Umlaufleitung kann den Pool also höchstens zu 53 bis 67 % versorgen; der Rest muss als Luftblasen **im Pool** ankommen (Belüftungsschleife oder Scheiben), und das ist wieder ein Luftsystem. **Empfindlichkeit:** bei einem Pool-Wert von 4 mg/l statt 5 mg/l steigt die Grenze auf 51 g/h (71 %), bei 3 mg/l auf 64 g/h (90 %), dann aber ohne Reserve bis zur Fischgrenze [E] `python -X utf8 -I -c "print((7.83-4)*13.2,(7.83-3)*13.2)"`.

### 2.4 Reicht das für 71 g O₂/h bei 2,17 m und 28 °C?
1. **In der Umlaufleitung: nein** (Abschnitt 2.3, höchstens 37 bis 48 g/h).
2. **Als Belüftungsschleife im Pool** (Pumpe zieht aus dem Pool, Injektor bläst am Poolboden ein): Luft 34 bis 107 l/min je nach Druck (Tabelle 2.2); nötig sind 4 bis 13 % Übertragung im Becken. **Belegt** ist für Scheiben 2,1 bis 4,2 % im Feld (R45); die Reinwasser-Übertragung feinblasiger Scheiben bei 2,17 m ist 13 bis 16 % (R45). Für Injektoren in 2 bis 4 m Wasser fand ich **keine** Messung der Übertragung oder der Blasengröße (Yadav u. a. 2024 messen die Blasengröße nicht, IJABE nennt keine) [Lücke]. Schon bei 1,38 bar Eingangsdruck bräuchte es 6,5 % oder mehr, also das 1,5- bis 3-fache der belegten Scheibenwerte, bei 1,7- bis 2,5-fachem Strom.
3. **Strom-Gegenprobe über die Messwerte (SAE):** Venturi-Messungen liegen bei 0,105 kg O₂/kWh (Reinwasser, 1-PS-Pumpe, 220-l-Tank [Q, Yadav u. a. 2024, Frontiers in Water 6:1401689]), 0,54 bis 0,74 (Alabama-Arbeiten [Q-Treffer]) und 0,5 bis 2,3 in einer Übersicht [Q-Treffer, R54]; feinblasige Scheiben 2 bis 3 [Q, Boyd 2015, R54]. Mit dem Feldfaktor 0,16 bis 0,26 aus R54 ergibt sich für 71 g/h eine Leistung von 119 bis 193 W (SAE 2,3), 369 bis 822 W (SAE 0,54 bis 0,74) und 2 600 bis 4 200 W (SAE 0,105) [E] `python -X utf8 -I -c "print(71/(2.3*0.26),71/(2.3*0.16),71/(0.74*0.26),71/(0.54*0.16),71/(0.105*0.26),71/(0.105*0.16))"`. Die Scheiben-Gegenprobe (SAE 3 und 2) liefert 91 bis 222 W und umfasst die 204 W des Plans: `python -X utf8 -I -c "print(71/(3*0.26),71/(2*0.16))"`.

## 3 Strom pro Jahr (Frage 3)
Alle Werte bei 8 760 h Dauerbetrieb: `python -X utf8 -I -c "print((288+204)*8.76)"` ergibt 4 310 kWh. Die Umlaufpumpen laufen bei Venturi weiter (288 W) oder sind in der Venturi-Leistung enthalten (V-A, V-B, Abschnitt 2.2).
| Fall | Leistung | kWh pro Jahr | Luft | Grundlage |
|---|---|---|---|---|
| **Heute:** vier Tauchpumpen 288 W + Gebläse 204 W | 492 W | **4 310** | 130 l/min | `data/system-specs.json` (R59: Pumpen höchstens 260 bis 328 W) |
| Venturi, bester Literaturwert (SAE 2,3, Feldfaktor 0,16 bis 0,26) + Umlauf 288 W | 407 bis 481 W | 3 560 bis 4 210 | nicht angegeben | [Q-Treffer, R54] |
| **V-A, Ben wörtlich:** CRNE 10-1 + 4 × 1583, 0,94 bar, Volllast | 606 W | **5 310** | 34 l/min | Tabelle, Anhang B |
| Venturi, Messwerte SAE 0,54 bis 0,74 + Umlauf 288 W | 657 bis 1 110 W | 5 760 bis 9 720 | nicht angegeben | [Q-Treffer] |
| **V-B:** 784-Klasse, 1,38 bar, alle 220 l/min | 838 bis 1 222 W | **7 340 bis 10 700** | 68 l/min | Tabelle 2.2 |
| gleiche Übertragung wie Scheiben (AOTE 4,2 %), Schleife, 104 l/min Luft | 288 W + 1 088 W | 12 050 | 104 l/min | [E, 14 Injektoren der 784-Klasse bei 15 psi, Gesamtwirkungsgrad 0,5] |
Betriebskosten nicht bewertet (ein Strompreis steht nicht in `data/`).

## 4 Ausfall und Teile netto (Frage 4)
### 4.1 Ausfallsicherheit
| Fall | Heute | Venturi (V-A oder V-B) |
|---|---|---|
| eine Umlaufpumpe fällt aus | Umlauf −25 %, Luft unberührt | bei vier Pumpen und vier Injektoren: Umlauf −25 % **und** Luft −25 %; bei einer Zentralpumpe: **alles weg** |
| Gebläse fällt aus | N+1: die zweite läuft | nicht vorhanden |
| Netzausfall | alles weg (Notstrom offen, D45 e) | alles weg |
| Verkalkung, Biofilm, Feststoffe | Membranen werden langsam dichter | Injektor kann **vollständig** die Ansaugung verlieren (CaCO₃, Eisen, Mangan, Sulfide, Silica, Biofilm) und muss chemisch gereinigt werden [Q, Mazzei TB 10]; alle Injektoren am selben Wasser fallen gemeinsam aus |
| Sauerstoffreserve ohne Luft (170 g Vorrat von 8 auf 3 mg/l) | 2,4 h bei 71 g/h, 3,7 h bei 46 g/h [R55, E] | gleich, **und** der freie Fall fällt mit der Pumpe weg |
**Notluft bleibt nötig** und muss vom Wasserkreis unabhängig sein: 12-V-Pumpe mit Akku und Luftstein; 55 l/min Notluft tragen 17 bis 35 g/h (24 bis 49 % von 71 g/h) und verlängern die Rettungszeit bei Pumpenausfall (ohne freien Fall) von 2,4 h auf rund 3,1 bis 4,7 h [E, aus R55] `python -X utf8 -I -c "print(170/(71-17),170/(71-35))"`. Teile und Preise laut R55: Resun MPQ-905 106,77 € + Versand, LiFePO₄ 12 V 100 Ah 105 bis 830 €, Netzüberwachung/Relais ohne Beleg. Mit Notluftsatz hat die Venturi-Variante zwei unabhängige Luftquellen wie heute, aber ihre Hauptquelle hängt am Wasserkreis.

### 4.2 Teile netto
Zählung nach `data/stueckliste.json` und `data/leitungsnetz.json` (Luftnetz K44 bis K51: Pool, Biofilter 1 und 2, Absetzer optional, Drittbecken 2 l/min mit Notstrom, Zweitbecken) [E, A: Mindestzählung].
| Entfällt (Pool-Anteil) | Stück | Kommt dazu (Venturi, 4 × Mazzei 1583) | Stück |
|---|---|---|---|
| Scheibenbelüfter T88 | 4 | Injektoren (EU: 584 gleich 15 Stück) | 4 |
| Stutzen d25 | 4 | Siebe vor dem Injektor (Partikel ≤ 2 bis 5 mm) | 4 |
| Pool-Verteiler T87 | 1 | Absperrhähne und Unions (Mazzei: ein und aus) | 8 |
| Pool-Abgang am 6-fach-Verteiler: Kugelhahn und Rückschlagventil | 2 | Manometer ein und aus | 2 |
| Umlaufpumpen 4 → 2 (Zentralpumpe + Reserve) | 2 | Notluftsatz (Pumpe, Akku, Relais, Luftstein, Schlauch) | 5 |
| **Summe entfällt** | **13** | **Summe kommt dazu** | **23** |
**Netto +10 Teile** (ohne Notluftsatz +5). Mit dem in Europa kaufbaren Mazzei 584 (15 Injektoren für 220 l/min bei 20 psi, 15 × 40,76 € = 611 €) wären es rund +50 (15 Injektoren, 15 Siebe, 30 Absperrorgane, 2 Manometer, 5 Notluftteile gleich 67, minus 13). **Kosten (grob, Preise gemischt netto und brutto, nur Größenordnung):** heute 2 Secoh JDK-S-200 gleich 745 € netto (R53, tanks.ie) und 4 Tauchpumpen etwa 1 380 € (4 × 345 €, R59), ohne Scheiben und Verteiler (in `data/stueckliste.json` ohne Preis). Venturi V-A: eine CRNE 10-1 rund 4 500 € netto (Partao, andere Variante, [Q-Treffer]), mit Reservepumpe 9 000 €; Mazzei 1583 ohne Europa-Preis (Vergleich US: 1584A, 1,5", PP, 135,99 $ [Q-Treffer]); Notluftsatz rund 210 bis 370 € (R55). **Bleiben:** 2 Gebläse, 6-fach-Verteiler, Luftstein Drittbecken, 12 Ventile und die Leitungen K45, K46, K49, K51. Die Luftleitung d40 zum Pool (K44) entfällt; es kommen Druckwasserleitungen zu den Injektoren dazu.

## 5 Verstopfung, Lärm, Wartung, CO₂, Gasübersättigung (Frage 5)
| Thema | Befund | Quelle | Status |
|---|---|---|---|
| Partikel im Treibstrom | größte Partikelgröße nach Einlauf: 15 mm ≤ 1 mm; 20 mm ≤ 2 mm; 25 mm ≤ 4 mm; 40 mm ≤ 5 mm; sonst Verschmutzung des Injektors | Mazzei TB 12 (2014), Tabelle 1 [Q] | eine Quelle (Hersteller); Fischkot und Futter über 2 mm im Umlauf vor dem Absetzer sind plausibel [A], also Sieb nötig |
| Verkalkung, Biofilm | kann die Ansaugung ganz abschalten; nur chemisch reinigen (30 %ige Salzsäure, 30 min, nicht mechanisch) | Mazzei TB 10 (2019) [Q]; R54: Patente [Q-Treffer] | eine Quelle; Wasserhärte der Anlage unbekannt (E15) |
| Wartung | Injektor ein- und ausbaubar (Absperrhähne, Unions), Ansaugleitung und Rückschlagventil prüfen, Manometer empfohlen; Einbau waagerecht oder Austritt nach oben; für Injektoren bis 1,5" ist ein Rückschlagventil im Saugstutzen eingebaut | Mazzei Installation Notes (07.2019) und TB 10 [Q] | eine Quelle |
| Lärm | **keine Messung** zu Injektoren; Hersteller wirbt mit "keine Gebläse oder Kompressoren"; Linear-Membranpumpen 44 bis 48 dB(A) (R53) | Mazzei (Suchtreffer) [Q-Treffer] | **Lücke** |
| CO₂-Entgasung | **kein Venturi-Wert**; Vergleich: Luft-zu-Wasser-Verhältnis 5 bis 8 gibt 80 bis 92 % Austrag je Durchgang (Gerätestudie), 2 und 5 getestet (Freshwater Institute 2022) [Q-Treffer]; hier liegt das Verhältnis bei **0,07 bis 0,5** (Tabelle 2.1) | [Q-Treffer] × 2; [E] | **Lücke**; ein Venturi ersetzt keine Entgasungskolonne (R54) |
| Gasübersättigung bei Druck-Injektion | EPA-Richtwert 110 % Gesamtgasdruck; 103 % können für Jungfische und flache Becken gefährlich sein; Luft in einer Pumpe führte in unter 5 min auf 110 % (unveröffentlichte Daten des Autors); Gasinjektionssysteme sind als Ursache aufgeführt; 1 % wird durch etwa 10 cm Wassertiefe ausgeglichen (2,17 m gleich etwa 21 %, nur am Boden); Grenzwerte hängen von Art und Expositionsdauer ab | Rogers 2005, Int J Recirculating Aquaculture 6:39 bis 48 [Q]; Bouck 1980, Trans Am Fish Soc 109, Abstract [Q]; Stickstoff wirkt ab 103 bis 118 %, Sauerstoff erst bei 200 bis 285 % [Q-Treffer, Übersichtsarbeit] | zwei Quellen für die Richtwerte; **kein** Messwert für Injektor-Systeme; Warmwasserfische (Wels, Tilapia) nicht belegt |

## Designprinzipien-Pflichtcheck (alle 10 Punkte, `docs/designprinzipien.md`)
| # | Prinzip | Urteil Venturi-Variante |
|---|---|---|
| 1 | Physik vor Strom | **Widerspruch:** 1,2- bis 4-facher Strom bei halber bis zwei Drittel Luft; der freie Fall (kein Teil, bis 11 g/h) bleibt die physikalische Lösung |
| 2 | wenig graben | neutral |
| 3 | so wenige Teile wie nötig | **Widerspruch:** netto +5 bis +10 Teile (Abschnitt 4.2) |
| 4 | Technik in die Kuppel, kurze Wege | neutral; Druckwasser zu vier Injektoren statt einer Luftleitung |
| 5 | Leitungen | Druckleitungen sind erlaubt (rechtwinklig unter Druck); keine Luftleitung d40 mehr, dafür Wasserverteiler |
| 6 | lebensmittelecht | Pumpe CRNE: WRAS und ACS belegt [Q]; Injektor PP oder PVDF: kein Lebensmittelnachweis gelesen [Lücke]; Gebläseluft berührt das Wasser nur über Scheiben |
| 7 | Kaufen vor Selbstbau, Europa-Bezug | **offen:** Mazzei 584-PP (40,76 €) und 885X-PP (70,07 €) bei Mundoriego (Spanien, Versand laut Seite "only in the peninsula") [Q]; 784, 1078 und 1583 nur US belegt; Preis der CRNE 10-1 (50 Hz) nicht belegt |
| 8 | wartbar, rückbaubar | **schlechter:** Säurereinigung bei Verkalkung, Siebe; Scheiben sind seltener ein Problem |
| 9 | Sicherheit, Notluft | **Widerspruch:** gemeinsame Ursache Wasser und Luft; Notluftsatz zwingend |
| 10 | ehrlich messen | Zahlen mit Befehl; Lücken benannt (Abschnitt Konfidenz); Annahmen A in `docs/decisions.md` erst nach Bens Entscheidung |

## Quellen (gelesen, nicht nur Suchtreffer)
| # | Titel / URL | Art | Abruf | Qualität | Unabhängig von |
|---|---|---|---|---|---|
| 1 | Mazzei, Injector Performance Table, Air Suction, REV 2014, `oxidationtech.com/downloads/Mazzei/Injector-Performance-Table.pdf` | Herstellertabelle | 05.11.2026, `pdftotext -raw`, imperial und metrisch geprüft | hoch für die Werte, Hersteller | 2, 3 |
| 2 | Mazzei TB 10 "Troubleshooting Mazzei Injectors", 28.10.2019, `.../Injector-MAZ-Trouble-Shooting.pdf`; Installation Notes 07.2019, `.../Injector-Installation.pdf` | Hersteller | gelesen | mittel | 1, 3 |
| 3 | Mazzei TB 12, Maximum Solid/Particle Size, 25.08.2014, `.../Injector-Guidelines.pdf` (Tabelle als Bild, mit Python aus dem PDF entpackt und angesehen) | Hersteller | gelesen | mittel | 1, 2 |
| 4 | Grundfos Product Centre, CRNE 10-1 N-FGJ-A-E-HQQE, Art. 98390335, 30.11.2022, `pumpsalesdirect.co.uk/pub/media/data_sheets/98390335.pdf`; CRN 10-3 Datenblatt 2022 (WRAS, ACS) | Herstellerdatenblatt | gelesen, Kennlinie nur als Bild | hoch (Daten), Hersteller | 5, 6 |
| 5 | Speck BADU GREEN, Prime Eco VS und Delta Eco VS Katalog, `pooldigital.de/downloads/speck/prime_eco_vs/Kat_BADU_PrimeEcoVS.pdf`; Speck Eco Touch VS Datenblatt (Energielabel) `cdn.shopify.com/s/files/1/0428/0572/3300/files/PDSPBETVS-Badu-Eco-Touch-VS-CWS-Data-Sheet-Sept-2017-1.pdf` | Hersteller | gelesen, Kennlinien nur als Bild | mittel | 4 |
| 6 | Rogers, "Total Gas Saturation Considerations for Recirculating Aquatic Systems", Int J Recirculating Aquaculture 6:39 bis 48 (2005), `vtechworks.lib.vt.edu/server/api/core/bitstreams/d3c4846a-4ba0-4cb8-afdc-c1af7cb52616/content` | Fachartikel | gelesen | hoch | 7 |
| 7 | Bouck 1980, "Etiology of gas bubble disease", Trans Am Fish Soc 109, `osti.gov/biblio/6642479` | Abstract | gelesen (nur Abstract) | mittel | 6 |
| 8 | Demeekul u. a., Int J Agric & Biol Eng 18(3):58 bis 62 (2025), `ijabe.org/index.php/ijabe/article/download/8962/pdf/32053` | Messung | gelesen | niedrig bis mittel (KLa-Einheit unklar) | 1 |
| 9 | Yadav u. a. 2024, Frontiers in Water 6:1401689, `doi.org/10.3389/frwa.2024.1401689` | Messung | gelesen (Zusammenfassung, Abschnitt teils) | mittel | 1, 8 |
| 10 | Mundoriego (ES): 3/4" PP Venturi MAZZEI 584-PP 40,76 €, 1" PP MAZZEI 885X-PP 70,07 € (brutto), `mundoriego.es/en/product/pp-34-venturi-injector/` und `.../pp-1-venturi-injector/` | Händler | gelesen, Seitenteile per Zusammenfassung | niedrig (Preis) | 1 |
| 11 | R45 (Abschnitt 4), R53, R54, R55, R59, `data/system-specs.json`, `data/stueckliste.json`, `data/leitungsnetz.json` | Repo | gelesen | – | – |
**Nur Suchtreffer:** Europump/Hydraulic-Institute "Variable speed pumping" (Statikhöhe und Affinitätsgesetze, Scribd-Kopien; DOE-Merkblatt und electrical-engineering-portal waren nicht lesbar: leere Seite und 403); Energies 17(7):1733 (403); Univ. Laval Mazzei 584 (403); Alabama-Dissertation (PDF über 10 MB); Freshwater Institute 2022 und Gerätestudie zum CO₂-Austrag; Übersichtsarbeit zu N₂ und O₂ bei Gasübersättigung; Partao, Check24, guide-piscine.fr (Preise).

## Widersprüche
| Aussage A | Aussage B | mögliche Ursache | gewählte (konservative) Seite |
|---|---|---|---|
| Venturi SAE bis 2,3 (Übersicht) | gemessen 0,105 (Yadav) und 0,54 bis 0,74 (Alabama) | bester Aufbau gegen Labor mit 1-PS-Pumpe | Messwerte für die Mitte, 2,3 nur als Untergrenze der Kosten |
| 1"-Venturi saugt 22,5 l/min bei 26 l/min Wasser und 0,75 bar (IJABE) | Mazzei 784: 9,1 l/min bei 23 l/min und 10 psi, Ausgang 0 | anderes Düsendesign, Messung gegen Herstellertabelle | Mazzei-Tabelle (belegt, zählbar); besseres Design als Chance, nicht belegt |
| Mazzei-Spalte 885X: 21,8 / 12,9 / 18,5 l/min bei 30 / 35 / 40 psi | Spalten 784, 1078, 1583 monoton | Druckfehler der Tabelle oder Spaltenvertauschung | 885X nicht verwendet |
| Pumpenleistung P2 0,75 kW (Motor) | hydraulisch 330 W im Nennpunkt | Motornennwert gegen Betriebsleistung | P1 etwa 0,65 kW aus 60 % Pumpenwirkungsgrad [A]; Kennlinie nachlesen |

## Konfidenz und Lücken
**Mittel für die Richtung "kein Ersatz", niedrig für Einzelwerte der Übertragung und der Pumpenleistung.** Gesichert: die Mazzei-Tabelle (eine Quelle, Gegenprobe imperial gegen metrisch), die Sauerstoff-Obergrenze des Umlaufs (Physik plus R45-Werte), die Gasübersättigungs-Richtwerte (zwei Quellen). Lücken:
1. Feldübertragung eines Injektors in 2 bis 4 m Wasser und Blasengröße: keine Messung gefunden.
2. P1-Kennlinie der CRNE 10-1 und Q-H-Kennlinie der Speck-Pumpe liegen nur als Bild vor; CRNE-10-2-Daten nicht gelesen; Preis der CRNE 10-1 (50 Hz) nicht belegt.
3. Europa-Bezug für Mazzei 784, 1078, 1583; Lebensmittelnachweis des Injektors (PP, PVDF).
4. Lärm und CO₂-Austrag speziell für Venturi; Wasserhärte der Anlage (Verkalkung).
5. Statikhöhe und Affinitätsgesetze: nur Suchzusammenfassungen und eigene Rechnung, Volltext des Europump-Leitfadens nicht gelesen.

## Folge
- **Kein Parameter** in `params.json`; Plan K44 bis K51, T85 bis T88 und `docs/jobs/M10-S5-LUFT.md` bleiben; R54 Empfehlung A (Gebläse und Scheiben behalten) wird bestätigt und mit der gelesenen Tabelle, der Sauerstoff-Obergrenze und den Stromzahlen belegt. E13 und E20 unberührt.
- **Offene Lücke 2 aus R54** (Mazzei-Tabelle unlesbar) ist geschlossen (Abschnitt 2.1).
- **Nebenbefund:** eine Kreiselpumpe mit Umrichter statt vier Tauchpumpen spart rechnerisch etwa 70 W, wirtschaftlich nicht; kein Auftrag.
- Entscheidung D<NN> offen (Frage unten).

**DEINE ENTSCHEIDUNG (Ben):** Gebläse plus Scheiben behalten und Venturi nicht bauen, oder zuerst einen Messversuch mit einem Injektor machen?
- **A (Empfehlung):** Plan unverändert; Venturi nicht bauen. Begründung: der Umlauf trägt höchstens 53 bis 67 % des Sauerstoffs, der Strom steigt auf das 1,2- bis 2,5-fache bei halber Luftmenge, die Teile steigen, der Ausfall wird gemeinsam.
- **B:** A, dazu ein Messversuch an einem getrennten Becken mit einem Mazzei 584-PP (40,76 €, Spanien), einer vorhandenen Pumpe und einem O₂-Sensor, um die Übertragung im Feld zu messen (schließt Lücke 1). Nutzen: klärt, ob ein besseres Venturi-Design die 4 bis 13 % erreicht; ändert den Plan nur bei einem Messwert über 13 %.
- **C:** Venturi statt Gebläse (V-A oder V-B); nicht empfohlen (Abschnitte 2 bis 4).

## Recherche-Kritiker
Datum 05.11.2026. Lücken (höchstens 5):
1. Feldübertragung und Blasengröße von Injektoren in 2 bis 4 m Wasser (Messversuch Option B, ICH planen, wenn Ben B wählt).
2. P1-Kennlinie CRNE 10-1 (Grundfos Product Centre, Bildansicht) und Preis über einen Grundfos-Händler in der EU (DEINE HANDLUNG nur bei C).
3. Mazzei-Bezug in der EU für 784, 1078, 1583 (Anfrage an Mazzei, `www.mazzei.net`); Lebensmittelnachweis PP und PVDF.
4. Lärm- und CO₂-Messung für Venturi; Wasserhärte (E15).
5. Volltext Europump-Leitfaden zur Statikhöhe.
Behebung: Nr. 1 bis 5 als eigener Auftrag, nur falls Ben B oder C wählt.

## Anhang A: Rechenwege (alle Befehle mit `python -X utf8 -I -c`)
1. Strom heute: `python -X utf8 -I -c "print((288+204)*8.76)"` ergibt 4 310 kWh.
2. Hydraulik Umlauf heute: `python -X utf8 -I -c "print(220/60000*2.0*9.81*1000)"` ergibt 72 W (`system-specs`).
3. O₂ je l/min Luft: `python -X utf8 -I -c "print(0.27*60)"` ergibt 16,2 g/h (0,27 g O₂ je l Luft aus R45).
4. Umlauf-Kapazität und nötiges Rückwasser: Abschnitt 2.3.
5. Wirkungsgrad Speck Eco Touch VS: `python -X utf8 -I -c "print(125/60000*2.8*9.81*1000/171)"` ergibt 0,33.
6. Hydraulik CRNE 10-1 im Nennpunkt: `python -X utf8 -I -c "print(12.1/3600*9.81*1000*10, 330/(0.6*0.852))"` ergibt 330 W und 646 W.
7. Kubikregel gegen Rechnung: `python -X utf8 -I -c "print(0.8**3, 300/606)"` ergibt 0,512 und 0,495.
8. Notluft-Reserve: `python -X utf8 -I -c "print(170/71,170/46)"` ergibt 2,4 h und 3,7 h (170 g Vorrat, R55).

## Anhang B: Betriebspunkt Pumpe + 4 × Mazzei 1583 (Skript)
Daten: Mazzei 1583, Wasser (gpm) und Luft bei 5 psi Ausgang (SCFH) bei 10, 15, 20, 30, 40, 50 psi Eingang; Pumpenkennlinie der CRNE 10-1 genähert durch Hmax 14,3 m und den Nennpunkt 12,1 m³/h bei 10 m [A]; Gesamtwirkungsgrad 0,51 [A].
```
python -X utf8 -I - <<'EOF'
pin=[10,15,20,30,40,50]; q=[14.5,17.8,20.6,25.2,29.1,32.5]; a=[8.3,21.7,35.6,56.6,79.2,109.0]
G,S,M=3.78541,0.471947,0.70307
def ip(x,xs,ys):
    for i in range(len(xs)-1):
        if xs[i]<=x<=xs[i+1]: return ys[i]+(ys[i+1]-ys[i])*(x-xs[i])/(xs[i+1]-xs[i])
    return ys[0]+(ys[1]-ys[0])*(x-xs[0])/(xs[1]-xs[0])
k=(14.3-10)/12.1**2
for x in (1.0,0.9,0.8,0.7):
    lo,hi=7,50
    for _ in range(50):
        p=(lo+hi)/2; Q=4*ip(p,pin,q)*G*0.06
        lo,hi=(p,hi) if x*x*14.3-k*Q*Q>p*M-2.17 else (lo,p)
    Q=4*ip(p,pin,q)*G; H=p*M-2.17; ph=Q/60000*H*9810
    print(x,round(p,1),'psi',round(Q),'l/min',round(H,2),'m',round(4*ip(p,pin,a)*S,1),'l/min Luft',round(ph/0.51),'W')
EOF
```
Ergebnis: 100 %: 13,6 psi, 256 l/min, 7,39 m, 33,9 l/min Luft, 606 W; 90 %: 11,4 psi, 233 l/min, 22,6 l/min, 436 W; 80 % und 70 % liegen unter dem kleinsten Tabellenwert (10 psi) und sind Extrapolation.

**Geprüft gegen:** Mazzei-Tabelle (`pdftotext -raw`, imperial gegen metrisch, Monotonie), Mazzei TB 10, TB 12 und Installation Notes, Grundfos-Datenblatt CRNE 10-1 und CRN 10-3, Speck-Katalog, Rogers 2005, Bouck 1980 (Abstract), IJABE 2025, Yadav 2024, Mundoriego-Seiten, R45 Abschnitt 4, R53, R54, R55, R59, `data/system-specs.json`, `data/stueckliste.json`, `data/leitungsnetz.json`, `docs/designprinzipien.md` · Rechnungen: `python -X utf8 -I -c` (Anhang A und B, Abschnitte 1 bis 3).

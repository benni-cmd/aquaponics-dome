# R54: Sind Venturi-Injektoren an Absetzer, Biofilter, Sumpf, Leitungen und Beckenzulauf eine einheitliche, effiziente Belüftung für diese Anlage?

**Priorität:** H · **Auftrag seit:** 04.11.2026 (Start-Auftrag `docs/jobs/start/R54-venturi-recherche.md`, Wunschbuch W67) · **Bearbeitet:** 04.11.2026 · **Zielparameter:** keiner in `data/params.json`; berührt `docs/jobs/M10-S5-LUFT.md`, Bauteile `geblaese_luft`, `luft_scheibenbelueftung`, Recherche R45 Abschnitt 4 und R53.
**Problem:** Ben fragt, ob Venturi-Injektoren (Wasserstrahl saugt Luft an) überall eingesetzt werden können, statt oder neben Gebläse plus Belüftungsscheiben. **Intent:** Eine Entscheidung, ob der Plan K44 bis K51 (zwei Linear-Membranpumpen N+1, Hauptverteiler 6-fach, Pool-Verteiler 4-fach, vier Scheiben) bleibt. **Goal:** Zahlen und je Einbaustelle ein Ja, Nein oder "nur als Ergänzung", mit Folgen für E13 und E20 und einer Entscheidungsfrage.
**Herkunft:** [Q] Seite oder Datenblatt selbst geöffnet und gelesen · [Q-Treffer] nur Suchergebnis oder Zusammenfassung, nicht selbst gelesen (Seite nicht abrufbar oder PDF-Tabelle unlesbar) · [E] eigene Rechnung · [A] Annahme. Zwei unabhängige Quellen je Aussage sind nur dort erreicht, wo die Tabelle es sagt.

## Suchplan
- Anfragen (en/de): 1) venturi injector aeration SAE kg O2/kWh aquaculture; 2) Mazzei injector pressure differential air suction; 3) Venturi Injektor Belüftung Teich Vordruck; 4) venturi clogging solids fish waste; 5) venturi CO2 stripping RAS; 6) Mazzei Injektor kaufen Europa.
- Quellenarten in Rangfolge: Boyd und Fachartikel > Hersteller und Händler > Übersichtsarbeiten per Suchzusammenfassung > Praxisberichte (nur Gegenprüfung).
- Grenze: WebFetch liefert PDFs nur als Binärdatei (lokal mit `pdftotext` gelesen); die Mazzei-Leistungstabelle ist als Text verschoben und nicht verwertbar, ein Luftansaugverhältnis (Luft je Wasser) habe ich **nicht** belegt.

## Befund
**Nein, nicht als einheitliche Belüftung: Venturi-Injektoren brauchen Wasser unter deutlich mehr Druck, als diese Anlage hat, und sie sind im Sauerstoffeintrag je kWh nicht besser als feinblasige Scheiben, sondern im Mittel schlechter.** Die Anlage fördert Wasser nur 2 bis 4 m hoch (0,2 bis 0,4 bar); ein Injektor braucht ein Druckgefälle von etwa der Hälfte seines Eingangsdrucks (Händlerseite; ein Ozon-Anbieter empfiehlt 20 psi gleich 1,4 bar [Q-Treffer]). Ein Venturi in jedem Rohr hängt damit an der Umwälzpumpe und nimmt der Luft die Unabhängigkeit, die R45 verlangt (Luftausfall: 0,8 bis 1,2 h bis 3 mg/l). **Empfehlung: Plan Gebläse plus Scheiben bleibt; Venturi höchstens als zusätzliches Zubehör, nie als Ersatz.**

## Zahlen
| Wert | Einheit | Quelle(n) | Randbedingung |
|---|---|---|---|
| Sauerstoffbedarf Fisch / Fisch + Nitrifikation | 1,1 / 1,7 kg/Tag, gleich 46 / 71 g/h | `data/system-specs.json` Abschnitt `sauerstoff`; [E] `python -X utf8 -I -c "print(1100/24, 1700/24)"` | Mittelfall, 346 kg Fisch, 34 m³ |
| SAE Feinblasen-Scheiben (Reinwasser) | 2 bis 3 kg O2/kWh | Hatchery International 2014, Teknologisk Institut: Membrandiffusor 2 bis 3, bester Prototyp 2,7 [Q]; Energies-Übersicht 2024 (fein bis 4,56, grob 1,22 bis 2,13) [Q-Treffer] | Seewasser, ohne Fisch, 20 °C |
| SAE Venturi (Reinwasser) | 0,5 bis 2,3 (Übersicht) bis 3,0 (anderer Übersichtsartikel); eigene Laborwerte 0,1 bis 1,0 | Yadav 2024, Frontiers in Water: 0,996 vorhergesagt, 0,105 beobachtet, 220-l-Becken [Q]; Energies-Übersicht 0,5 bis 2,3 [Q-Treffer]; Übersicht 0,5 bis 3,0, bester Rundbecken-Fall 1,7 bis 2,05 [Q-Treffer] | kleine Labor-Tanks, stark vom Aufbau abhängig; Mazzei-584 gegen Druckluft "vergleichbar" (Univ. Laval) [Q-Treffer, Seite 404] |
| SAE mechanische Belüfter (Vergleich) | 0,5 bis 2,0; Schaufelrad gut etwa 2, üblich höchstens 1 | Boyd, Responsible Seafood Advocate, 05.11.2015 [Q] | Teich, Feldwerte |
| Feldfaktor Reinwasser zu Fischwasser | 0,16 bis 0,26 | [E] aus R45 Abschnitt 4: AOTE 2,1 bis 4,2 % gegen SOTE 13 bis 16 % bei 2,17 m | 28 °C, 5 mg/l Soll, alpha 0,49 bis 0,8 [A] |
| Elektrische Leistung nur für den Sauerstoff (Fisch) | Scheibe SAE 2 bis 3: 58 bis 142 W; Venturi SAE 2,3: 76 bis 123 W; SAE 1,0: 175 bis 284 W; SAE 0,5: 349 bis 567 W | [E] `python -X utf8 -I -c` Bedarf 45,8 g/h geteilt durch SAE mal Feldfaktor | Fisch + Nitrifikation: 1,5-fach (Scheibe 90 bis 219 W, Venturi SAE 1,0 270 bis 438 W); Plan R45: 204 W Gebläse |
| Druckgefälle am Injektor | etwa halber Eingangsdruck; Ansaugen beginnt, wenn Ausgang rund 20 % unter Eingang liegt; Anbieterempfehlung 20 psi gleich 1,4 bar | Mundoriego (ES) Seite zu Mazzei 584-PP [Q]; Pumps & Systems, Lagune [Q]; Ozon-Anbieter [Q-Treffer] | Gegendruck am Austritt senkt die Luftmenge (Patent, [Q-Treffer]) |
| Gegendruck Pool-Tiefe 2,17 m | 0,21 bar | [E] `python -X utf8 -I -c "print(2.17*0.0981)"` | Austritt am Beckenboden |
| Mehr-Pumpenleistung, wenn der ganze Umlauf (220 l/min) über Injektoren läuft | 0,35 bar: 320 bis 510 W; 0,7 bar: 640 bis 1030 W; 1,4 bar: 1280 bis 2050 W | [E] `python -X utf8 -I -c`, Wirkungsgrad 25 bis 40 % (FAO 589 nach `filter-konzept.md`) | Basis `system-specs`: 144 W je Linie, zwei Linien (288 W); SAE-Zahlen oben enthalten die Pumpenleistung bereits, beide Zeilen **nicht** addieren |
| Seitenstrom statt Umlauf | 40 l/min bei 1,4 bar: rund 270 W für den Antrieb allein | [E] `python -X utf8 -I -c`, Wirkungsgrad 35 % [A] | Luftmenge je Wasser unbelegt |

## Bewertung nach den Fragen des Auftrags
1. **Sauerstoff je kWh:** Feinblasige Scheiben liegen belegt bei 2 bis 3 kg O2/kWh, Venturi in Laborarbeiten bei 0,1 bis 2,3, in der Übersicht bis 3,0 in einem Einzelfall. Venturi gewinnt nur im besten Aufbau; im Mittel ist die Leistung 2- bis 5-mal höher als bei den Scheiben (Zahlen oben). **Venturi schlägt Membranbelüftung nicht.**
2. **Druckverlust und Pumpenmehrleistung:** Bei 2 bis 4 m Förderhöhe liefert die Pumpe 0,2 bis 0,4 bar; Injektoren wollen 0,7 bis 1,4 bar Differenz. Im Umlauf bedeutet das 320 bis 2050 W zusätzlich (oben) bei heutigen 288 W. Das macht den Vorteil von W53 (Wasser nur einmal hochgepumpt) zunichte. Ein Seitenstrom mit eigener Pumpe vermeidet das, ist aber ein zweites Pumpensystem.
3. **Mindestdurchfluss und Vordruck je Injektor:** Datenblätter nennen Differenz, nicht Mindestdurchfluss; der kleine Mazzei 584-PP (3/4") saugt Flüssigkeit mit 30 bis 95 l/h [Q, Mundoriego]; ein **Luft**-Ansaugwert fehlt. Ein einzelner Injektor ersetzt kein Gebläse mit 130 l/min.
4. **Verstopfung:** Anbieter nennen "keine kleinen Öffnungen" [Q-Treffer]; Patentschriften nennen Zusetzen und Reinigung bei untergetauchter Anordnung und sinkende Ansaugung bei steigendem Gegendruck [Q-Treffer]. Für Luftloch oder Saugstutzen im Feststoffwasser fand ich **keine** Quelle. Vor einem Filter/Absetzer ist Fischkot im Strom [A]; hinter dem Feinfilter weniger.
5. **Lärm:** keine Quelle gefunden; [A] Zischen und Pumpengeräusch statt der 44 bis 48 dB(A) der Linear-Membranpumpe (R53). Offen.
6. **Ausfallsicherheit:** Bei Venturi fällt Luft mit der Pumpe aus; der Plan hat zwei unabhängige Gebläse und rechnet 0,8 bis 1,2 h Reserve für Luftausfall (R45 Abschnitt 4). Bei Pumpenausfall in der Umlaufkette gäbe es gleichzeitig keine Strömung und keine Luft (gemeinsame Ursache). Das ist die stärkste Aussage gegen "Ersatz".
7. **CO2-Entgasung:** Venturi strippt wie jede Blasenbelüftung etwas CO2; eine venturi-spezifische Zahl habe ich nicht belegt. Belegt für andere Verfahren: gepackte Kolonnen 40 bis 60 % im RAS, DTU 67 bis 89 % je Durchgang; Schaufelrad 1,2 kg CO2/kWh; Airlift 20 bis 130 g CO2/kWh [alle Q-Treffer]. Ein Venturi ersetzt keine Entgasungskolonne.
8. **Wartung:** Pumpen und Injektor außerhalb des Beckens halten die Wartung klein ("nur Pumpen bewegen sich"; Pumps & Systems [Q]); Reinigungsbedarf bei Feststoffen unbelegt.
9. **Bezug Europa (D76):** Mazzei 584-PP, 3/4", **40,76 € inkl. MwSt.**, Mundoriego (Spanien) [Q]; Versand in die EU nicht genannt. Irritec Venturi Injector PRO 1" (350 l/h) 49,20 € und 3/4" (100 l/h) 42,55 € bei DVS Beregnung (DE) [Q-Treffer, Bewässerungsgerät, kein Belüfter]. Mazzei 1078 und 784 nur US belegt (Newegg 124,99 $) [Q-Treffer]. **Status: Kleinmodell beschaffbar (zwei Quellen, eine nur Treffer); ein Belüftungs-Injektor für 130 l/min Luft nicht belegt.**

## Empfehlung je Einbaustelle
| Stelle | Empfehlung | Grund |
|---|---|---|
| Pool (Fischbecken, Scheiben K44) | **nein** | Sauerstoff für Fische muss unabhängig von der Umwälzpumpe sein (R45); Scheiben liefern 2 bis 3 kg O2/kWh |
| Beckenzulauf | **nur als Ergänzung** | Austritt flach, Gegendruck klein: Ansaugen möglich, aber Menge unbelegt; kein Ersatz, höchstens Zusatz am Rücklauf; Pumpenleistung unverändert, wenn nur das vorhandene Gefälle genutzt wird |
| Absetzer / Filter (K47/K48) | **nein** | Feststoffe, Luftblasen stören die Absetzung [A]; Plan hat dort Luft nur optional |
| Biofilter (K45/K46) | **nein** | Luft dient Durchmischung des Trägerbetts, Menge nach Trägerhersteller (R45); ein Strahl liefert das nicht gezielt [A] |
| Sumpf / Subtank V4 (D75, geparkt) | **nur als Ergänzung, später** | Tauchpumpen im Subtank könnten einen Injektor am Auslauf tragen; Bau geparkt, kein Belegwert |
| Leitungen (Ringleitung, Rohre) | **nein** | Lufttaschen, Druckverlust, Kavitationsrisiko an Pumpen [A, ohne Quelle]; zusätzlicher Druck im ganzen Umlauf |

## Folgen für E13 und E20
- **E13 (Gebläse- und Schrank-Ort):** unverändert. Das Gebläse bleibt; Venturi verschiebt keinen Ort. Nur bei der Variante "Venturi statt Gebläse" würde Luft an den Pumpen entstehen und der Technikbereich-Ort an Gewicht verlieren.
- **E20 (Kreislaufvariante):** Variante B (Ring) und C erhöhen den Pumpendruck (548 W bzw. 503 W gegen 430 W in A, R47); ein Injektor im Ring würde darauf aufbauen, aber den Strom weiter erhöhen. A+ bleibt vom Venturi unberührt.
- **M10-S5-LUFT:** Teile A und B bleiben bauen/gesperrt wie geplant; kein Teil entfällt.

## Quellen (gelesen, nicht nur Suchtreffer)
| # | Titel / URL | Art | Abruf | Qualität | Unabhängig von |
|---|---|---|---|---|---|
| 1 | Boyd, "Efficiency of mechanical aeration", Responsible Seafood Advocate, 05.11.2015, `globalseafood.org/advocate/efficiency-of-mechanical-aeration/` | Fachartikel | 04.11.2026 gelesen | hoch | 2, 3 |
| 2 | Scarratt, Hatchery International 11.10.2014, Teknologisk Institut (AirX), `hatcheryinternational.com/a-new-diffused-aeration-concept-for-aquaculture-1196/` | Fachpresse, EU-Projekt | gelesen | mittel | 1, 3 |
| 3 | Yadav et al. 2024, Frontiers in Water 6, DOI 10.3389/frwa.2024.1401689 | Fachartikel, Labor | gelesen (nur Modellierung) | mittel | 1, 2 |
| 4 | Pumps & Systems, "Injectors boost efficiency, safety in lagoon aeration", `pumpsandsystems.com/injectors-boost-efficiency-safety-lagoon-aeration` | Hersteller-Fachpresse | gelesen | niedrig bis mittel | 1 bis 3 |
| 5 | Mundoriego, Mazzei 584-PP und Artikel "Venturi-type injectors", `mundoriego.es` | Händler, ES | gelesen | niedrig (Preis, Druckregel) | 1 bis 4 |
| 6 | Energies 17(7), 1733 (2024), Übersicht Belüfter | Fachartikel | **403**, nur Suchzusammenfassung | mittel | 1 bis 5 |
| 7 | Univ. Laval, Mazzei 584 gegen Druckluft (`modeleau.fsg.ulaval.ca/.../pvr1259.pdf`) | Testbericht | **404**, nur Suchzusammenfassung | mittel | 1 bis 5 |
| 8 | Patente (Gegendruck, Zusetzen), DVS Beregnung (Irritec), Mazzei-Tabelle (PDF, Text verschoben) | Patent, Händler | nicht verwertbar gelesen | niedrig | – |

## Widersprüche
| Aussage A | Aussage B | mögliche Ursache | gewählte (konservative) Seite |
|---|---|---|---|
| Venturi SAE 0,5 bis 3,0, "beste Belüftung" (Übersicht) | eigene Laborwerte 0,1 bis 1,0 (Frontiers) | Rundbecken-Bestwert gegen Optimierungsstudie, Test-Aufbau | untere Hälfte (0,5 bis 1,0) für die Rechnung; 2,3 nur als Obergrenze |
| Mazzei 584 "vergleichbar mit Druckluft" (Laval) | Scheiben 2 bis 3 gegen Venturi unter 1 im Mittel | Messung bei gleichem Luftstrom, nicht je kWh | je kWh rechnen (Zahlen oben) |
| Diffusoren schwach in flachem Wasser (Boyd, Teich) | Scheiben 2 bis 3 in Versuchstanks | Teichtiefe gegen 2,17 m Pool | Pool 2,17 m ist tief genug, 6 bis 7,5 % je m (R45) |

## Konfidenz und Lücken
**Mittel für die Richtung (Venturi nicht besser, hängt an der Pumpe), niedrig für exakte kWh-Werte** (Laborwerte kleiner Tanks, zwei Übersichtsarbeiten nur als Zusammenfassung). Fehlt: Luft-Ansaugverhältnis eines geeigneten Injektors (Datenblatt Mazzei 1078/784, Tabelle unlesbar), Lärm, Verstopfung im Fischwasser, venturi-spezifische CO2-Zahl, ein europäischer Händler für größere Belüftungs-Injektoren.

## Folge
- Kein Parameter in `params.json`; Plan K44 bis K51 und M10-S5-LUFT bleiben.
- Optional: ein Kleinmodell als Versuchs-Ergänzung am Rücklauf (Beckenzulauf), nur auf Bens Ja.
- Entscheidung D<NN> offen (Entscheidungsfrage unten).

**DEINE ENTSCHEIDUNG (Ben):** Gebläse plus Scheiben behalten?
- **A (Empfehlung):** ja, Plan unverändert; Venturi nicht bauen. Begründung: unabhängig von der Pumpe, 2 bis 5-mal weniger Strom je Sauerstoff, Bauteile liegen vor.
- **B:** A, dazu ein Kleinmodell (Mazzei 584-PP oder Irritec) am Beckenzulauf als Versuch; kostet etwa 40 €, Nutzen unbelegt, kein Ersatz.
- **C:** Venturi statt Gebläse im Pool; nicht empfohlen (Pumpenmehrleistung 320 bis 2050 W, Luft und Wasser fallen zusammen aus).

## Recherche-Kritiker
Datum 04.11.2026. Lücken (max. 5):
1. Energies-Übersicht und Laval-Bericht nur als Suchzusammenfassung; Volltext nachlesen (ICH, wenn Seiten wieder abrufbar sind).
2. Mazzei-Leistungstabelle (Luft- und Wasserwerte) für 584/784/1078 lesbar machen (Bildansicht der PDF-Seite).
3. Europäischer Händler für Belüftungs-Injektoren (Mazzei AirJection, Hydro-Systems) und Preis.
4. Lärm- und Verstopfungsangaben aus Herstellerunterlagen.
5. Venturi-CO2-Austrag je kWh.
Behebung: Nr. 1 bis 5 als eigener Auftrag, nur falls Ben B oder C wählt.

**Geprüft gegen:** Quellen 1 bis 5 geöffnet, 6 bis 8 nur Suchzusammenfassung (oben markiert) · `docs/research/R45-hydraulik-auslegung.md` Abschnitt 4, `docs/research/R53-europa-frischwasser-luft.md`, `data/system-specs.json` (Sauerstoff, Flüsse, Leistung), `docs/decisions.md` D75 bis D77, `data/roadmap.json` E13 und E20 · Rechnungen: `python -X utf8 -I -c` (Bedarf, Leistung, Pumpenmehrleistung).

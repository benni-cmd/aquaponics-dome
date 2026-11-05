# R58: Zielbild S, zwei Recherchen: ZR1 Tauchpumpe mit Kennlinie bei 2,3 m, ZR2 Geländerhöhe am Pool

**Priorität:** H · **Auftrag seit:** 05.11.2026 (`docs/jobs/M10-ZIELBILD-S.md` Abschnitt 9 Punkt 4, Recherche vor ZW4 und ZW1) · **Bearbeitet:** 05.11.2026 · **Rolle:** Fachrecherche, nur lesen und schreiben; Modell, `data/`, Blätter unverändert.
**Problem:** Zielbild S (D88) setzt 4 Tauchpumpen auf den Poolboden (je 55 l/min bei 2,28 m, Plan 328 W gesamt, also 82 W je Pumpe) und ein Geländer auf der 150 mm hohen Aufkantung; für beides fehlen Belege. **Intent:** Die Montage-Kette M10-Z2 (Pumpen) und M10-Z1 (Geländer) soll mit belegten Werten bauen. **Goal:** ZR1: ein Pumpenmodell mit Kennlinie, Eintauchtiefe, Lebensmitteleignung und Bezug in Europa. ZR2: eine Geländerhöhe mit zwei Quellen.
**Herkunft:** [Q] Seite oder PDF selbst geöffnet und gelesen · [Q-Treffer] nur Suchtreffer · [E] eigene Rechnung (Befehl daneben) · [A] Annahme. Pumpen- und Geländerseiten wurden von Hilfsrecherchen gelesen; ihre Kennzeichnung ist übernommen.

## Antwort in vier Sätzen
1. **ZR1 ist nicht erfüllt: für keine Pumpe liegt eine Kennlinie als Zahlen vor,** nur Maximalwerte (Qmax, Hmax) oder Grafiken; die Eintauchtiefe nennt kein Kandidat außer dem ausgeschiedenen Aquaforte DM-Vario (1,5 m), und für keinen Kandidaten gibt es einen Lebensmittelnachweis (D85).
2. **Bestes Zwischenergebnis:** Aquaforte EC-10000 (kupferfrei, 129 €, Hornbach DE) und Jebao DCP-8000 (24 V DC, 65 W, Händler NL) tragen 55 l/min bei 2,3 m auch bei pessimistischer Schätzung; Oase AquaMax Eco Premium 5000 (35 W, 385 €) liegt je nach Näherung unter oder über dem Ziel und ist ohne Kennlinie nicht belegbar.
3. **ZR2: 750 mm über der Aufkantung (Oberkante Z 900) sind nicht normbelegbar;** die belegten Nennwerte sind 1,00 m (ASR A2.1 und BGV C5), 1000 bis 1100 mm (DIN EN ISO 14122-3, Sekundärquelle). Eine Pflicht für den Eigenbetrieb ist nicht belegt; sie entsteht über die Gefährdungsbeurteilung, die Wasser („versinken, ertrinken") ausdrücklich nennt.
4. **Korrektur zum Teilbericht:** 1000 mm über Flur sind unter den Kragarmen (Unterkante Z 940) **nicht** möglich (150 mm Aufkantung + 850 mm Geländer = Z 1000); der Weg dorthin geht nur in den Lücken zwischen den Tischen oder über die Brüstungs-Ausnahme (Optionen unten).

## ZR1: Tauchpumpe 55 l/min bei 2,3 m

### Anforderung
Je Pumpe 55 l/min (3,3 m³/h) bei 2,28 m, 82 W elektrisch (Plan); hydraulisch 20,5 W, also 25 % Gesamtwirkungsgrad [E] `python -X utf8 -I -c "print(55/60*9.81*2.28)"`. Am Boden eines Beckens mit 2,2 bis 2,4 m Wasser: Eintauchtiefe mindestens 2,5 m oder IP68; Dauerbetrieb, Fischwasser mit Schwebstoff hinter dem Ansaugkorb, 20 bis 30 °C; Werkstoffe mit Wasserkontakt lebensmittelecht (D85); bestellbar mindestens in Europa (D76).

### Kandidaten und Schätzung
Die Kennlinienpunkte unten sind **keine Messwerte**: sie folgen aus Qmax und Hmax der Quelle und drei Näherungen für die Kurvenform (linear, Parabel, Ellipse). Die echte Kurve liegt dazwischen [A]; Ziel sind 55 l/min.
[E] `python -X utf8 -I -c "x=2.3/Hmax;print(Qmax*(1-x), Qmax*(1-x*x), Qmax*(1-x*x)**0.5)"` mit Q in l/h, durch 60 geteilt.
| Kandidat | Qmax, Hmax | Q bei 2,3 m linear / Parabel / Ellipse (l/min) | Leistung (4 Stück) | Preis, Händler | Status |
|---|---|---|---|---|---|
| **Aquaforte EC-10000** | 10000 l/h, 5 m; kupferfrei; Schmutz bis 6 mm | 90 / 131 / 148 | 68 oder 85 W je Pumpe (Datenblatt und Beschreibung widersprechen sich) = 272 bis 340 W | 129,00 €, Hornbach (Marktplatz), DE | [Q] Seite gelesen; Eintauchtiefe unbelegt; Schwester-Pumpe DM-Vario hat nur 1,5 m |
| **Jebao DCP-8000** (24 V DC, regelbar) | 8000 l/h, 5,2 m; 65 W höchste Stufe; Keramikwelle | 74 / 107 / 120 | 260 W | 189,99 € (Angebot von 2021, veraltet), Ocean Store, NL | [Q] Händlerseite; zweite Quelle Handbuch nur Treffer (403); Meerwasser-Aquaristik; Tiefe/IP offen |
| **Oase AquaMax Eco Premium 5000** (Art. 75923) | 5000 l/h, 3,5 m; 10 bis 35 W; Schmutz bis 11 mm; Kunststoff | 29 / 47 / 63 | 140 W | 384,95 €, Hornbach, DE | [Q] Seite gelesen, zweite Quelle Treffer; **je nach Kurve unter 55 l/min**; Tiefe offen |
| **SunSun CDF-6000** (24 V DC) | 6000 l/h, 3,8 m; 40 W; IPX8; ABS/PC; Partikel bis 8 mm; Kabel H05RN-F | 39 / 63 / 80 | 160 W | 120,99 €, teichtip.de, DE (nicht auf Lager) | [Q]; IPX8 ohne Tiefenzahl; Lebensmittelangabe fehlt |
| Oase Aquarius Universal Premium 5000 (Art. 56617) | 5000 l/h, 4,5 m; 85 W | 41 / 62 / 72 | 340 W (über Plan 328 W) | rund 400 € (DE/NL) | [Q-Treffer] |
| Eheim universal 3400 | 3400 l/h, 3,6 m; 80 W | 20 / 34 / 44 | 320 W | – | [Q] Herstellerseite; **zu schwach** |
Ausgeschieden: Aquaforte DM-Vario S 10000 (Handbuch gelesen: Betriebstiefe höchstens 1,5 m); Pontec PondoMax Eco 8000 (Hmax 2,8 m, bei 2,3 m kaum Durchfluss); Sicce Syncra, Aqua Medic Ocean Runner, Jebao DCP-5000/10000 (Zahlen widersprüchlich oder Seite gesperrt, [Q-Treffer]).
Quellen-Links: Hornbach Oase `hornbach.de/p/oase-aquamax-eco-premium-5000/12714129/`, Oase `oase.com/en/products-a-z/family/f/aquamax-eco-premium.1000877224.html` [Q-Treffer], Hornbach Aquaforte `hornbach.de/p/aquaforte-ec-10000-teichpumpe/12355610/`, Jebao-Händler `reef-aquarium-store.com/jebao-boost-pump-dcp8000-incl-controller`, SunSun `teichtip.de/en/sunsun-cdf-6000-24v-dc-pond-pump-6000l-h-40w-with-built-in-blocking-and-dry-running-protection/52019`, Eheim `eheim.com/en_GB/aquatics/technology/pumps/universal/universal-3400`, Aquaforte-Handbuch (DM-Vario, 1,5 m) über `toppy.nl/product/12271/aquaforte-dm-10000-vario-s-vijverpomp.html` [Q].

### Urteil ZR1
1. **Kein Kandidat ist bau-bereit belegt.** Fehlt: Kennlinie als Zahlen, Eintauchtiefe ≥ 2,5 m, Lebensmitteleignung. Es gibt keine zweite unabhängige Quelle für Leistung und Hmax außer den Händlerseiten.
2. **Aufbauhinweise:** Die Pumpen laufen mit Reserve (Qmax weit über 55 l/min) und werden am Hahn oder per Regler gedrosselt [A]; das senkt die Leistung unter den Nennwert. Der Druckschlauch zum Siebkorb hat Reibungsverlust zusätzlich zu den 2,28 m [A, nicht gerechnet].
3. **Nächster Schritt (ICH, auf Freigabe):** Hersteller-Anfrage an Aquaforte (Hornbach-Marktplatz) und Oase mit drei Fragen: Q bei 2,3 m, maximale Betriebstiefe, Materialien mit Wasserkontakt (Lebensmittel/KTW). Alternativ die Kennlinien-Grafik im Betriebshandbuch per Bildansicht ablesen (Oase-Katalog Seite 303 bis 306 laut Treffer; die Oase-Seiten waren gesperrt, HTTP 429).
4. **Folge für M10-Z2:** Der Parameter „Pumpe" bleibt Platzhalter (Ø und Höhe nach Gehäusemaß), bis eine Kennlinie vorliegt.

## ZR2: Geländerhöhe am Pool

### Belege
| Regel | Zahl | Quelle 1 | Quelle 2 | Status |
|---|---|---|---|---|
| Absturz schließt das Hineinfallen und Versinken in Flüssigkeiten ein; Wasser ist zu beurteilen, auch unter 1 m Höhe | Gefährdungsbeurteilung entscheidet über Maßnahmen | ASR A2.1 (BAuA, Ausgabe 2012, geändert GMBl 2014 S. 284), Punkt 3.1 und 4.1 [Q] `dguv.de/rundschreiben/dokcenterimport/2014/0195_2014_anlage_3_asr_a2.1_2014_04.pdf` | komnet.nrw.de/_sitetools/dialog/42412 [Q-Treffer] | Pflicht nur über Beurteilung |
| Mindesthöhe Umwehrung | **1,00 m**; über 12 m Absturzhöhe 1,10 m; Brüstung (geschlossene Wandscheibe) bis 0,80 m erlaubt bei mindestens 0,20 m Tiefe | ASR A2.1 Punkt 5.1 Abs. 2 [Q] (gleiches PDF) | forum-verlag.com/fachwissen/arbeitsschutz/asr-a2-1/ [Q] (bestätigt die Baustellenregel) | belegt |
| Becken und Gerinne | Absturzsicherung, Beispiel Geländer oder hochgezogene Wand **mindestens 1 m**; Ausnahme, wo ein Sturz unter 1 m keine Gefahr erwarten lässt | BGV C5 (Abwassertechnische Anlagen) §6 [Q] `vorschriften.bgn-branchenwissen.de/daten/dguv/21/6.htm` | – | Analogiefall Kläranlage, kein Fischzucht-Regelwerk |
| Geländer an maschinellen Anlagen | Handlauf-Oberkante 1000 bis 1100 mm; Kugel von 500 mm darf nicht durch; Fußleiste mindestens 100 mm | DIN EN ISO 14122-3 über Suva `suva.ch/de-ch/praevention/...gelander-auf-die-hohe-kommt-es-an` [Q-Treffer] | komnet.nrw.de/_sitetools/dialog/14348 (DGUV Information 208-005) [Q-Treffer] | Norm kostenpflichtig, nicht gelesen; ob ein Fischbecken eine „maschinelle Anlage" ist, offen |
| Landesbauordnung | Umwehrung 0,90 m bis 12 m Absturzhöhe, 1,10 m darüber | anwalt24.de/gesetze/lbo-4/38 [Q-Treffer] | mw.niedersachsen.de FAQ Umwehrungen [Q-Treffer] | gilt für Gebäude und Verkehrsflächen, nicht für Becken |
| Baustellen-Regel | an und über Wasser unabhängig von der Höhe sichern, Mindesthöhe 1,00 m, 0,80 m nicht zulässig | ASR A2.1 Punkt 8.2 [Q] | forum-verlag.com [Q] | gilt für Baustellen, Übertragung ist Auslegung |
Lücken: keine DGUV- oder SVLFG-Vorschrift speziell für Aquakultur-Becken mit Höhenangabe; DIN EN 15288 nicht geprüft; Alternativen (Kette, Abdeckgitter, Gitterrost) ohne belegte Normmaße; ob die Höhe ab Flur oder ab Oberkante Aufkantung zählt, steht im gelesenen Text nicht ausdrücklich [A: ab Standfläche, also ab Flur].

### Maße im Modell (`docs/jobs/M10-ZIELBILD-S.md` Abschnitt 2.1)
Aufkantung 150 mm hoch, 150 mm breit; Kragarm-Unterkante Z 940; 40 mm Luft: Oberkante Geländer unter den Kragarmen höchstens **Z 900** (750 mm über der Aufkantung). Eine Umwehrung von 1000 mm ab Flur endet bei **Z 1000**, also 60 mm **über** der Kragarm-Unterkante [E] `python -X utf8 -I -c "print(150+850, 940-900)"`. Der Teilbericht der Hilfsrecherche („passt unter die Kragarme") war hier falsch.

### Optionen
| Option | Maß ab Flur | Norm-Lage | Kosten und Teile |
|---|---|---|---|
| **(a) 750 mm Geländer auf der Aufkantung, Oberkante Z 900** (Stand der Werkstatt) | 900 | unter allen Nennwerten; nur über dokumentierte Gefährdungsbeurteilung (ASR A2.1 4.1) mit Zusatz (Knieleiste, Rinnen der 10 Innentische als Abschirmung [A]) | wenig Teile; Rechtslage Eigenbetrieb offen |
| **(b) 1000 mm in den Lücken zwischen den Tischen, 750 mm unter den Kragarmen** | 1000 / 900 | Nennwert in den Lücken erfüllt, unter den Kragarmen weiter Beurteilung | zwei Geländer-Typen, mehr Teile |
| **(c) Brüstung statt Geländer:** geschlossene Wandscheibe 800 mm ab Flur, Tiefe mindestens 200 mm (Aufkantung von 150 auf 200 mm verbreitern) | 800 | ASR A2.1 5.1 Abs. 2 erlaubt Brüstung bis 0,80 m bei ≥ 0,20 m Tiefe [Q]; ob die Pflanztisch-Rinnen die Sicht und den Zugang stören, ist offen | eine durchgehende Scheibe (Lochblech oder Platte), weniger Stäbe; Auslegung „Tiefe" ist [A] |
| (d) Abdeckgitter oder begehbarer Rost über dem Pool | – | Abdeckung zählt als Absturzsicherung (Punkt 3.5, Treffer); Maße nicht belegt | zusätzlich 26,4 m³ Wasserfläche abzudecken; Zugang zu Pumpen und Siebkorb |

## Widersprüche und Konfidenz
| Aussage A | Aussage B | gewählte Seite |
|---|---|---|
| Aquaforte EC-10000: 85 W (Beschreibung) | 68 W (Datenblatt) | 85 W (konservativ für die Leistungssumme) |
| Teilbericht ZR2: 850 mm Geländer passt unter die Kragarme | Z 1000 liegt über Z 940 (Auftragsblatt) | Auftragsblatt, [E] |
| Geländer unter 1,00 m nicht normkonform | Pflicht im Eigenbetrieb nicht belegt | beides: Nennwert 1,00 m, Pflicht über die Beurteilung |
**Konfidenz:** ZR1 niedrig (Maximalwerte, keine Kennlinie, keine Lebensmittelnachweise); ZR2 mittel für die Nennwerte (ASR A2.1 Primärtext gelesen, zweite Regel BGV C5 gelesen, nur Analogiefall), niedrig für die Pflicht im Eigenbetrieb.

## Entscheidungsfragen
**DEINE ENTSCHEIDUNG (Ben), Q1:** Welche Geländer-Option baut die Werkstatt: (a) 750 mm wie heute mit dokumentierter Gefährdungsbeurteilung, (b) 1000 mm in den Lücken, (c) Brüstungsscheibe 800 mm mit 200 mm breiter Aufkantung? **Empfehlung: (c),** weil sie als einzige Option einen belegten Normwert (ASR A2.1 5.1) mit der Kragarm-Höhe vereint; sie braucht die Verbreiterung der Aufkantung um 50 mm (Statik und Auftrieb, Punkt 5 der offenen Liste) und die Auslegung „Tiefe", die ich nicht verbindlich belegen kann.
**DEINE ENTSCHEIDUNG (Ben), Q2:** Darf ich Hersteller-Anfragen für die Pumpen-Kennlinie vorbereiten (Aquaforte, Oase; Text als Entwurf, Versand durch dich)?

## Recherche-Kritiker
Datum 05.11.2026. Lücken:
1. Kennlinie als Zahlen für jede Pumpe (Rückfrage oder Bildansicht der Datenblatt-Grafik).
2. Eintauchtiefe und Lebensmittelnachweis (D85) für alle Kandidaten.
3. Auslegung „Tiefe 0,20 m" der Brüstung in ASR A2.1 5.1 (Primärtext Wortlaut zur Messung).
4. DIN EN 15288 und DGUV/SVLFG zu Aquakultur-Becken.
5. Zweite unabhängige Quelle für Pumpenleistung (Händlerseiten zählen nur als eine Art Quelle).
Behebung: Nr. 1 und 2 als eigener Auftrag nach Q2.

**Geprüft gegen:** Pumpen-Berichte der Hilfsrecherche (Hornbach-Seiten, teichtip.de, Jebao-Händler, Eheim-Herstellerseite, Aquaforte-Handbuch per `pdftotext`), ASR A2.1 PDF, BGV C5 Seite, forum-verlag.com · `docs/jobs/M10-ZIELBILD-S.md` Abschnitte 2.1, 2.4, 9 · Rechnungen: `python -X utf8 -I -c` (Hydraulikleistung, drei Kurvennäherungen, Höhen).

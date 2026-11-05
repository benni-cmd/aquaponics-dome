# R55: Woher kommt das Nachspeisewasser (und braucht es Aktivkohle), und macht Venturi die Anlage leichter?

**Priorität:** H · **Auftrag seit:** 05.11.2026 (Wunsch W81 Wasserquelle, W77 Venturi von Leon) · **Bearbeitet:** 05.11.2026 · **Rolle:** Fachrecherche, nur lesen und schreiben; Modell, `data/`, Blätter unverändert. Fließt in den Systemreview N-MINIMAL ein.
**Problem:** Ben und Leon wollen ein möglichst natürliches, selbstregulierendes, günstiges System. Offen sind (1) die Wasserquelle der Nachspeisung samt Aktivkohle (heute Station T83: 2 Kompositbehälter, Sediment, Begrenzer, Probehahn, 4 Kugelhähne) und (2) ob Venturi die Belüftung ersetzt oder vereinfacht. **Intent:** Der Systemreview soll Bauteile streichen oder vereinfachen können. **Goal:** je Quelle Risiko, Aufbereitung, Kosten und eine Empfehlung; ein Venturi-Urteil mit Sauerstoffbilanz, Ausfallsicherheit, Teilezahl und Kosten; eine Entscheidungsfrage.
**Herkunft:** [Q] Seite oder PDF selbst geöffnet und gelesen · [Q-Treffer] nur Suchtreffer oder Zusammenfassung · [E] eigene Rechnung (Befehl daneben) · [A] Annahme. **Unabhängig** heißt: nicht aus derselben Ursprungsquelle abgeleitet (FAO 589 und das daraus modifizierte Texas-A&M-Merkblatt zählen als **eine** Quelle).
**Eingangsdaten:** Verlust bis 0,68 m³/Tag (2 % von 34 m³; `data/system-specs.json` Abschnitt `puffer`, SRAC 454; bei 1 %: 0,34 m³), Umlauf 4 × 55 l/min = 220 l/min, 346 kg Fisch, Sauerstoffbedarf 46 g/h (Fisch) bis 71 g/h (mit Nitrifikation), Nachspeisung heute 4 l/min begrenzt (R45), kein Vorrat im Dom (D66).

## Antwort in fünf Sätzen
1. **Wasserquelle: Leitungswasser, ohne Dauer-Aktivkohle, wenn der Versorger Chlor (kein Chloramin) liefert.** In Deutschland steht Chloramin nicht in der UBA-Liste der Desinfektionsstoffe ([Q] eine Quelle), Chlor ist auf höchstens 0,3 mg/l nach Aufbereitung begrenzt. Bei 4 l/min Nachspeisung in 220 l/min Umlauf verdünnt sich das auf rund 5 µg/l, unter dem EPA-Dauerwert von 11 µg/l [E] — die Verdünnung ist belegt gerechnet, die Chlorzehrung durch Fischkot im Kreislauf bleibt [A].
2. **Aktivkohle ist nicht zwingend, aber sie ist der Rückfall:** Ein einzelner Einweg-Kohleblock (10 Zoll, 15 bis 99 €) statt zwei Kompositbehältern mit katalytischer Kohle, nur falls der Versorger Chloramin meldet oder die Messung im Pool Chlor zeigt. Chloramin verfliegt weder durch Stehen noch durch Belüftung (zwei unabhängige Quellen).
3. **Regenwasser deckt nur 29 % (71 m³ von 248 m³/Jahr) und ist als alleinige Quelle nicht tragfähig; Brunnen und Fluss lohnen nicht** (Genehmigung, Eisen/CO₂/Sauerstofflosigkeit beim Brunnen; Keime, Schwebstoffe und UV-Durchlass beim Fluss).
4. **Venturi: nein als Belüftung, nein als Bauteil an vielen Stellen.** Gratis ist nur das frei fallende Wasser an den Einläufen (0 zusätzliche Teile): 7 bis 11 g O₂/h bei 0,5 m Fall, also 10 bis 15 % des Bedarfs von 71 g/h [E]. Ein Venturi-Teil an jedem Einlauf fügt Teile hinzu, ohne belegten Luftgewinn, und ist in Europa als Fallrohr-Lösung nicht belegt.
5. **Was die Anlage wirklich leichter macht:** die zweite Linear-Membranpumpe (N+1, rund 373 € netto) durch eine 12-V-Notpumpe mit Akku ersetzen — Option, nur mit geprüfter Förderkurve bei 0,25 bar (offen).

## Suchplan
- Anfragen (en/de): Chlor-Verflüchtigung im stehenden und belüfteten Wasser; Chloramin; EPA-Chlorkriterien Süßwasser; Fisch-LC50 Chlor; Wasserquellen in der Aquaponik (FAO 589, SRAC 4607, Texas A&M, Iowa State); UBA-Liste § 20 TrinkwV; BDEW-Wasserfakten; DWD-Niederschlag; Regenwasser-Tankpreise; Wehrbelüftung (Gameson); Mazzei-Bulletin; Notbelüftung mit Akku (SRAC 452, Global Seafood Alliance).
- Quellen-Rangfolge: Behörden und Normen > Fachveröffentlichung > Hersteller/Händler > Forum (nur als Hinweis).
- Grenze: die FAO-589-PDF (zu groß) und die EPA-Scans habe ich nicht im Volltext gelesen; die Fassungen auf FarmHub und epa.gov sind gelesen. Drei Teilberichte wurden von Hilfsrecherchen gelesen und hier zusammengeführt; Aussagen sind mit [Q] oder [Q-Treffer] so übernommen, wie die Hilfsrecherche sie gekennzeichnet hat.

## Befund Teil 1: Wasserquelle

### Vergleich der vier Quellen
| Quelle | Risiken | nötige Aufbereitung | Jahreskosten bei 248 m³ (nur Wasser) | Urteil |
|---|---|---|---|---|
| **Leitungswasser** | Chlor oder (selten) Chloramin; Härte ortsabhängig; meist keimfrei | bei Chlor: Verdünnung im Umlauf, Test (DPD) ; bei Chloramin: Aktivkohle | 462 bis 643 € [E] (1,86 bis 2,59 €/m³); mit Abwassergebühr bis 1258 € [E], sofern kein Gartenwasserzähler | **Empfehlung** |
| **Regenwasser** | sehr weich (wenig Puffer), Dachmaterial (Zink, Kupfer), Vogelkot, Erstabfluss, Mengenschwankung | Erstablauf-Abscheider, Filter, dunkler kühler Tank; Aufhärtung (KH) nötig | Wasser 0 €; Tank 3000 l ab 949 € (Hornbach AT); Ertrag 71,5 m³/Jahr [E], 29 % des Bedarfs; 3000 l decken 4,4 Tage | nur Ergänzung |
| **Brunnenwasser** | oft sauerstofflos, hoher CO₂-Gehalt, Eisen, H₂S, übersättigter Stickstoff; Anzeige- oder Genehmigungspflicht | Belüftung/Entgasung, Haltetank, Eisenoxidation und Filter, Wasseranalyse (rund 80 €) | Wasser 0 €; Anlage 300 bis 4000 € je nach Tiefe | nein, außer das Grundstück hat schon einen |
| **Flusswasser** | Schwebstoffe, Keime, Fisch- und Insektenlarven, Krankheitseinschleppung, Pestizide (nicht belegt); Entnahme genehmigungspflichtig | Siebe, Absetzbecken, mechanische und biologische Filter, UV (Oberflächenwasser lässt UV schlecht durch) | Wasser 0 €; Technik 4 Stufen (Aufwand > Leitungswasser) | **nein** |

### Belegte Zahlen
| Wert | Zahl | Quelle 1 | Quelle 2 | Unabhängig? |
|---|---|---|---|---|
| Freies Chlor verfliegt im stehenden Wasser | bis 48 h, mit Luftstein schneller; „ein paar Tage" Belüften | FAO 589 Kap. 3.4 (FarmHub-Wiedergabe) [Q] `learn.farmhub.ag/resources/small-scale-aquaponic-food-production/3-water-quality-in-aquaponics/sources-of-aquaponic-water/` | Aquarium Co-Op (Blog): 12 bis 24 h mit Luftstein, 1 bis 5 Tage Stehen [Q] `aquariumcoop.com/blogs/faqs/does-letting-water-sit-remove-chlorine`; Texas A&M EHT-147 (aus FAO abgeleitet) [Q] | **ja** (FAO und Blog), Blog nur Hinweisniveau |
| Chloramin verflüchtigt sich kaum, Belüftung bricht die Bindung nicht | stabil, chemische Behandlung nötig | MacQuarrie und Wilton, Hatchery International 2002 (Syndel) [Q] `syndel.com/wp-content/uploads/2019/01/Ins-and-Outs-Of-Dechlorination.pdf` | Masabni und Sink, Texas A&M EHT-147, 10/2020 [Q] `extension.rwfm.tamu.edu/wp-content/uploads/sites/8/2020/10/Water-Quality-In-Aquaponics-Sink-Masabni.pdf` | **ja** |
| Chlor-Grenze für Fische | EPA Süßwasser 19 µg/l akut, 11 µg/l chronisch (1986); Syndel: giftig ab 0,05 mg/l frei, 0,2 mg/l gebunden; Nil-Tilapia 96-h-LC50 0,7 mg/l | EPA National Recommended Water Quality Criteria [Q] `epa.gov/wqc/national-recommended-water-quality-criteria-aquatic-life-criteria-table` | Syndel (s. o.) [Q]; Tran, Truong, Do 2011, Can Tho Univ. J. Sci. [Q] `ctujsvn.ctu.edu.vn/index.php/ctujsvn/article/view/1005` | **ja** |
| Deutschland: Chlorgrenzen | Chlor max. 1,2 mg/l Zugabe, 0,3 mg/l nach Aufbereitung (min. 0,1); Chlordioxid max. 0,2 mg/l nach Aufbereitung; **Chloramin nicht gelistet** | UBA-Liste § 20 TrinkwV, BAnz AT 27.01.2023 B12 (PDF volltextdurchsucht) [Q] `bundesanzeiger.de/pub/publication/IH2o2fSsV5YvYknFqru/...BAnz%20AT%2027.01.2023%20B12.pdf` | zweite Quelle zu „Chloramin nicht üblich" **fehlt** (nur UBA-Ausnahme nach § 21 möglich) | **nein, eine Quelle** |
| Weniger als 10 % Wassertausch auf einmal | Risiko durch Chlor stark verringert; nie mehr als 10 % ohne Test | Texas A&M EHT-147 [Q] | FAO 589 über FarmHub [Q] | **nein** (gleiche Ursprungsquelle) |
| Wasserhärte | weich < 1,5 mmol/l (< 8,4 °dH), mittel 1,5 bis 2,5, hart > 2,5 mmol/l | DVGW [Q] `dvgw.de/themen/wasser/verbraucherinformationen/wasserhaerte` | Verteilung in Prozent **nicht gefunden** | Lücke |
| Alkalinität/Härte, die die Fische brauchen | Alkalinität mind. 20, optimal 50 bis 150 mg/l CaCO₃ (Aquaponik); 75 bis 200 (Fischzucht allgemein) | Texas A&M EHT-147 [Q] | SRAC 4607 (Cassiano, Univ. Florida, 07/2020) [Q] `srac.msstate.edu/pdfs/Fact Sheets/4607 GroundwaterTreatment.pdf` | **ja** (Aquaponik gegen Fischzucht), Zahlen weichen ab |
| Regenwasser: weich, kaum Salz, gut zum Nachfüllen; Zink-Dach niedrigerer pH | pH Zink 6,27 bis 6,8 gegen Ziegel 7,15 bis 7,25 | FAO 589/FarmHub [Q] | watersa.net `watersa.net/article/download/6569/7802` [Q-Treffer] | schwach |
| Regenwasser: Dachmetalle | unbeschichtete Kupfer-, Zink-, Bleidächer nicht für Nutzgarten; Filter und Sedimentation binden Zink/Kupfer; Tank kühl und dunkel | LfU Bayern `lfu.bayern.de/wasser/umgang_mit_niederschlagswasser/regenwassernutzung/index.htm` [Q] | BauNetz `baunetzwissen.de/flachdach/...niederschlagswasser-2266679` [Q] | **ja** |
| Jahresniederschlag Deutschland | 791 mm (1991 bis 2020) | DWD Pressemitteilung 30.12.2024 [Q] `dwd.de/DE/presse/pressemitteilungen/DE/2024/20241230_deutschlandwetter_jahr_2024_news.html` | zweite Quelle nicht geholt | eine Quelle |
| Wasserpreis | Trinkwasser 1,86 €/m³ (NRW, 01.2025), Abwasser 3,21; Sachsen-Anhalt 2,01 und 3,45; Mittel BDEW rund 2,43 [E aus 108 €/Jahr bei 122 l/Tag] | ZFK `zfk.de/wasser-abwasser/wasser-und-abwasserpreise-steigen-und-steigen` [Q] | BDEW Wasserfakten 04/2025 `bdew.de/media/documents/Wasserfakten_im_Ueberblick_April_o_MW_05052025_1.pdf` [Q] | **ja** |
| Regentank | Erdtank 3000 l 949 €, 5000 l 1289 € | Hornbach AT (Europa) [Q] `hornbach.at/shop/Gartenbau-Landschaftsbau/Regenwassernutzung/Regenwassertanks/S2974/artikelliste.html` | eBay.de 899 bis 1199 € [Q-Treffer] | schwach |
| Brunnen-Anzeige | Anzeige mindestens einen Monat vor dem Bau (München, § 49 WHG, Art. 30 BayWG) | Stadt München [Q] `stadt.muenchen.de/service/info/anzeige-fur-einen-gartenbrunnen/10175162/` | NRW „meist Genehmigung" [Q-Treffer, Forum] | schwach; Landesrecht abhängig |
| Grundwasser-Gase | H₂S schädlich schon in Spuren; CO₂-Ziel unter 15 mg/l; Eisen unter 0,1 mg/l unkritisch; Belüftung/Entgasung | SRAC 4607 [Q] | Texas A&M EHT-147 [Q], UF/IFAS-Tabelle [Q-Treffer] | **ja** |
| Oberflächenwasser höchstes Risiko | Schwebstoffe, Larven, Keime; Aufbereitung: Absetzbecken, Filter, UV/Ozon | Iowa State CFSPH Source Water Tip Sheet 2025 [Q] `cfsph.iastate.edu/Assets/water_tipsheet-aqua.pdf` | Texas A&M EHT-147 [Q]; UV-Durchlass bei Flusswasser schlecht (Praxisleitfaden, Treffer) [Q-Treffer] | **ja** |

### Eigene Rechnungen
| Wert | Ergebnis | Rechnung / Annahme |
|---|---|---|
| Wasserbedarf | 248 m³/Jahr (bei 1 %: 124) | [E] `python -X utf8 -I -c "print(0.68*365)"` |
| Verdünnung am Zulauf | 0,3 mg/l Leitungswasser (Obergrenze) ergibt 5,4 µg/l nach dem Mischen, wenn 4 l/min in den Umlauf von 220 l/min laufen; unter dem EPA-Dauerwert 11 µg/l | [E] `python -X utf8 -I -c "print(0.3*4/224*1000)"`; **Annahme [A]:** der Zulauf mündet in den Umlauf und wird sofort durchmischt, nicht in eine tote Ecke |
| Aufsummierung im ganzen System ohne jede Zehrung | 6 µg/l je Tag (0,68 m³ × 0,3 mg/l in 34 m³) | [E] `python -X utf8 -I -c "print(0.68*0.3/34*1000)"`; Chlor zehrt in der Praxis an organischer Last und Ammonium (Gebundenes Chlor entsteht dabei); **Zehrung im Kreislauf: keine Messquelle gefunden, [A]** |
| Kosten Kohleblock (Einweg, 10 Zoll) | 1,9 €/m³ (15 € je 8000 l) bis 12,4 €/m³ (99 €); 465 bis 3071 €/Jahr | [E] `python -X utf8 -I -c "print(15/8*248.2, 99/8*248.2)"`; Händlerangabe 8000 l oder 6 Monate [Q-Treffer] |
| Kosten Wasseraufbereiter flüssig (Tetra AquaSafe) | rund 16,5 €/m³, 4095 €/Jahr | [E] 5 ml je 10 l Packungsangabe; 16,48 bis 16,99 € je 500 ml (Kaufland.at, aio.lv) [Q-Treffer]; **unwirtschaftlich** |
| Regenertrag | 71,5 m³/Jahr gleich 29 % | [E] `python -X utf8 -I -c "print(113*0.791*0.8)"`; Abflussbeiwert 0,8 [A]; Fläche 113 m² (Grundfläche der Kuppel); ob sich Regen von der Plane fassen lässt: offen (R37) |

### Antworten auf die Einzelfragen
1. **Baut sich Chlor durch Standzeit und Belüftung im Puffer ab?** Ja, nur bei Chlor: bis 48 h Stehen oder 12 bis 24 h mit Luftstein (Quellen oben). Chloramin: nein. Ein Standtank (2 Tage = 1,4 m³) wurde in D66 bewusst gestrichen; das System selbst übernimmt die Rolle des Puffers, siehe nächster Punkt.
2. **Was puffert das System selbst bei kleiner Nachspeisemenge?** Zwei Wirkungen: Verdünnung (5,4 µg/l statt 300 µg/l [E]) und Zehrung (nicht belegt, [A]). Die 10-%-Regel (FAO 589 und Texas A&M, nicht unabhängig) liegt bei uns weit unterschritten (2 % am Tag). Ein Haken: Chlor trifft im Pool auf Ammonium und bildet gebundenes Chlor, das nach Syndel schon ab 0,2 mg/l giftig ist; bei 5 µg/l Gesamtchlor ist das weit unterschritten [E], aber der Wert gilt nur bei durchmischtem Zulauf.
3. **Ist Aktivkohle zwingend?** Nein bei Chlor, ja bei Chloramin. Welcher Fall gilt, klärt eine Anfrage beim Versorger (kostenlos, E15) oder ein DPD-Test Gesamtchlor am Hahn.

## Befund Teil 2: Venturi

### Einbaustellen
| Stelle | Urteil | Begründung |
|---|---|---|
| Venturi an jedem Rücklauf-Einlauf in den Pool | **nein** | Gefälle 0,2 bis 0,5 m gleich 0,02 bis 0,05 bar am Eingang; Mazzei saugt erst ab etwa 20 % Differenz, wirksam ab 25 bis 30 % (Technical Bulletin 10) [Q, eine Quelle]; Absolutwerte unter 0,05 bar nennt kein Hersteller; kein europäischer Händler für ein Fallrohr mit Lufteinzug gefunden [Q-Treffer, Lücke]. Frei fallendes Wasser belüftet ohne Teil (siehe unten) |
| Venturi an Beet- und NFT-Abläufen | **nein** | Kleine Durchflüsse (NFT je Rinne gering [A]), Kanalstrecken mit Feststoffen; Verstopfung ohne unabhängige Zahl (Hersteller sagt: keine kleinen Öffnungen, kaum Verstopfung [Q-Treffer, werbend]); mehr Teile je Ablauf, Sauerstoffgewinn klein, weil Beete und Rinnen schon Sauerstoff aus der Luft aufnehmen [A] |
| Venturi plus Notluftpumpe statt Gebläse | **nein** | Venturi hängt an der Umwälzpumpe: Pumpenausfall nimmt Strömung und Luft zugleich weg (gemeinsame Ursache, R54); die Notluft muss also allein tragen, dann braucht es das Venturi nicht |
| Freier Fall am Beckenzulauf (kein Bauteil) | **ja, als Zusatz, kostenlos** | 7 bis 11 g O₂/h bei 0,5 m Fall und 220 l/min, 4,8 bis 21,6 g/h über 0,3 bis 1,5 m Fall (Tabelle) |

### Zahlen
| Wert | Ergebnis | Quelle 1 | Quelle 2 | Unabhängig? |
|---|---|---|---|---|
| Wehrbelüftung E20 | 0,13 bis 0,23 bei 0,35 bis 0,535 m Fall, 0,030 bis 0,063 m²/s; Gameson: 1/(1−E20) = 1 + 0,62 h | Küçükali 2023, J. Anatolian Env. Animal Sci. 8(4), `dergipark.org.tr/en/download/article-file/3587822` [Q]; Labor-V-Wehr, Gameson-Lesart aus verstümmeltem Text rekonstruiert | TU Delft OCW Kaskadenbelüftung `ocw.tudelft.nl/wp-content/uploads/Aeration2.pdf` [Q]: nur Systematik, keine Zahlen | nur teilweise; Aquakultur-Messwert fehlt |
| Sauerstoffeintrag bei 220 l/min | 0,3 m: 4,8 bis 7,0; 0,5 m: 7,3 bis 10,6; 1,0 m: 11,8 bis 17,1; 1,5 m: 14,9 bis 21,6 g O₂/h (28 bis 10 °C) | [E] `python -X utf8 -I -c "Q=13.2;E=1-1/(1+0.62*h);print(E*0.3*Cs*Q)"` (Defizit 30 % der Sättigung [A]) | Küçükali-Messwerte E20 0,15 bis 0,22 geben 5,4 bis 7,9 g/h bei 20 °C [E] | Rechnung gegen Messbereich |
| Anteil am Bedarf bei 0,5 m Fall | 10 bis 15 % von 71 g/h; 15 bis 24 % von 46 g/h | [E] 7,3 bis 10,6 geteilt durch 71 oder 46 | – | [E] |
| Venturi, Pumpendruck, SAE | 0,1 bis 2,3 kg O₂/kWh (Labor), eine Studie bester Fall 0,542 | R54 (Quellen 1 bis 7 dort) | Energies 17(7), 1733 (2024) [Q-Treffer, 403] | siehe R54 |
| Venturi-Differenz | Ansaugen ab etwa 20 % des Eingangsdrucks, wirksam ab 25 bis 30 %, Maximum bei 50 % | Mazzei Technical Bulletin No. 10 `oxidationtech.com/downloads/Mazzei/Injector-MAZ-Trouble-Shooting.pdf` [Q] | R54: Mundoriego, Pumps & Systems [Q] | **ja** |
| Kreispool-Kaskade (Aquakultur) | SAE bis 4,56 kg O₂/kWh bei 0,016 m³/s (Pumpenenergie) | Roy et al. 2024, Heliyon 10(5) e26367 [Q-Treffer, nur Abstract] | – | schwach |
| O₂-Verlust bei Stromausfall | bei 30 kg/m³ und 29 °C fällt gesättigtes Wasser in 16 min auf 3 ppm; bei doppelter Dichte unter 6 min | SRAC 452 (Masser, Rakocy, Losordo) [Q] `srac.msstate.edu/pdfs/Fact Sheets/452 ...Management of Recirculating Systems.pdf` | Global Seafood Alliance, Ebeling und Hightower, Notsauerstoff-Systeme [Q] `globalseafood.org/advocate/backup-oxygen-power-systems-essential-insurance/` | **ja** (beide fordern Notsauerstoff) |

### Sauerstoffbilanz bei Stromausfall (eigene Rechnung)
Grundlage: 34 m³, Abfall von 8 auf 3 mg/l gleich 170 g O₂ Vorrat [E] `python -X utf8 -I -c "print(34*5)"`; Luft hat 250 g O₂/m³ [A]; Feldwirkungsgrad AOTE 2,1 bis 4,2 % aus R45 Abschnitt 4 (nicht die 5 bis 15 % der Hilfsrecherche: das wäre Reinwasser).
| Fall | Bedarf g/h | Notluft 55 l/min (Eintrag) | Freier Fall 0,5 m | Rest-Defizit | Zeit von 8 auf 3 mg/l |
|---|---|---|---|---|---|
| keine Luft | 71 | 0 | 0 | 71 | 2,4 h |
| keine Luft, nur Fisch | 46 | 0 | 0 | 46 | 3,7 h |
| Notluft schwach, Fall | 71 | 17 | 7 | 47 | rund 3,6 h |
| Notluft stark, Fall | 71 | 35 | 11 | 25 | rund 6,8 h |
| nur Fisch, Notluft stark, Fall | 46 | 35 | 11 | 0 | unbegrenzt |
Die Tabelle gilt nur, solange die Umwälzpumpe läuft (sonst fällt auch der freie Fall weg) und das Futter im Notbetrieb nicht oder wenig gegeben wird [A]. 55 l/min Notluft decken 17 bis 35 g O₂/h gleich 24 bis 49 % des Bedarfs von 71 g/h [E] `python -X utf8 -I -c "print(55*60/1000*250*0.021, 55*60/1000*250*0.042)"`. **Eine kleine Notpumpe hält das System nicht gleich wie das Plan-Gebläse (130 l/min: 41 bis 82 g/h), verlängert aber die Rettungszeit von 2,4 auf rund 4 bis 7 Stunden.**

### Notluft mit Akku: Teile und Preise
| Teil | Zahl | Quelle | Status Europa (D76) |
|---|---|---|---|
| Resun MPQ-905 (12 V, 6000 l/h gleich 100 l/min) | 106,77 € + 6,95 € Versand | eBay.de [Q] `ebay.de/p/26036914691` | Händler DE; Leistung W nicht angegeben |
| Hailea ACO-003 (12 V Kolbenpumpe) | 25 W, 55 bis 60 l/min, max. 0,08 MPa; Händler: als Reserve, im Dauerbetrieb nur 2 bis 4 Wochen | practicalgardenponds.com [Q-Treffer] | UK, Preis nicht gefunden |
| LiFePO₄ 12 V 100 Ah | 105 bis 830 € (Foursun 105,54 €, Vatrer 253,63 €, Patona 599,95 €, Wattstunde 663 €) | solaranlage-tipps.de, vatrerpower.com [Q-Treffer] | DE/PL-Lager |
| Laufzeit des Akkus | 38 h bei 25 W, 24 h bei 40 W (1200 Wh, 80 % nutzbar) | [E] `python -X utf8 -I -c "print(1200*0.8/25)"` | – |
| Automatik bei Stromausfall | nicht belegt; Relais oder Netzüberwachung nötig | [A] | Lücke |
Ersatzvergleich: zweite Secoh JDK-S-200 gleich 372,70 € netto (R53, tanks.ie) gegen Resun 106,77 € + Akku 105 bis 254 € + Relais [A] gleich etwa 210 bis 370 €: **kein klarer Kostenvorteil, aber unabhängig vom Netz.** Die Förderkurve einer 12-V-Pumpe bei 0,25 bar (2,17 m Tiefe) ist für keine Pumpe belegt; deshalb offen.

## Gesamturteil Venturi (W77)
**Venturi macht die Anlage nicht an vielen Stellen leichter.** Begründung in fünf Zeilen:
1. Sauerstoff: Freier Fall bringt gratis 10 bis 15 % des Bedarfs; ein Venturi an denselben Stellen liefert keinen belegten Mehrwert (Gefälle zu klein, Luftmenge unbelegt).
2. Ausfallsicherheit: Venturi fällt mit der Pumpe aus; Notluft muss ohnehin getrennt vorhanden sein.
3. Teilezahl: ein Venturi je Einlauf und Ablauf ergibt mehr Teile, Schläuche und Reinigungsstellen (Verstopfung), nicht weniger.
4. Kosten: Kleinmodell etwa 40 € (R54), mal Zahl der Stellen; kein Gewinn gegenüber den heutigen Scheiben (2 bis 3 kg O₂/kWh gegen 0,1 bis 2,3).
5. **Was sich vereinfachen lässt:** die Einläufe so legen, dass das Wasser frei fällt (0,3 bis 0,5 m, kein Teil), und die zweite Linear-Pumpe gegen Akku-Notluft prüfen.

## Folgen für den Systemreview (nur Liste; Blätter nicht geändert)
1. **T83 Aktivkohle-Station:** bei Chlor von 2 Kompositbehältern, Sediment, Begrenzer, Probehahn und 4 Kugelhähnen auf **einen Einweg-Kohleblock mit Gehäuse** (oder ganz weg) reduzieren; Rückfall bei Chloramin: Station wie heute, Beschaffung über UK-Händler (R53).
2. **Zulauf-Lage:** Nachspeisung in den Umlauf mit Durchmischung (Pool-Zulauf oder Pumpensumpf), nicht in einen toten Winkel [A].
3. **Pool-Einläufe:** freier Fall 0,3 bis 0,5 m als Planwert, kein Venturi.
4. **N+1 der Belüftung:** zweite Linear-Pumpe gegen 12-V-Notpumpe mit Akku prüfen; Entscheidung erst nach Förderkurve.
5. **E20 und Kreislaufvarianten:** unberührt.

## Widersprüche
| Aussage A | Aussage B | mögliche Ursache | gewählte Seite |
|---|---|---|---|
| Sauerstoffübertragung 5 bis 15 % (Hilfsrecherche, Reinwasser) | AOTE 2,1 bis 4,2 % (R45, Fischwasser) | Reinwasser gegen Fischwasser | R45 (konservativ) |
| Chlor verfliegt in 24 h (Blog) | bis 48 h und „ein paar Tage" (FAO) | Temperatur, Konzentration, Rühren | 48 h, bei Belüftung 12 bis 24 h |
| Venturi-SAE bis 3,0 | Labor 0,1 bis 1,0 | Aufbau | R54 Seite (untere Hälfte) |
| Hailea „Reserve, 2 bis 4 Wochen Dauerbetrieb" | als Notpumpe tauglich | Dauerbetrieb gegen Bereitschaft | als Bereitschaftspumpe tauglich, nicht als Hauptpumpe |

## Konfidenz und Lücken
**Mittel für die Richtung beider Fragen, niedrig für Einzelwerte.** Gesichert (zwei unabhängige Quellen): Chlor entweicht beim Stehen, Chloramin nicht; Fischgrenzen für Chlor; Mazzei-Mindestdifferenz (mit R54). Nur eine Quelle: Chloramin in Deutschland nicht gelistet; Niederschlag 791 mm; Wehrbelüftung. Lücken (alle als [A] geführt):
1. Halbwertszeit von freiem Chlor in Stunden: keine belastbare Quelle.
2. Chlorzehrung durch organische Last im Kreislauf: keine Messstudie.
3. Anteil der Wasserwerke, die chloren; Härteverteilung in Prozent; pH und Nitrat als Typwerte.
4. Regenwasser-Analysewerte (pH, Leitwert, Zink) und Erstablauf-Abscheider mit Zahlen.
5. Flusswasser-Recht (WHG §§ 8, 25) nicht geprüft.
6. Förderkurve 12-V-Pumpe bei 0,25 bar; Notstrom-Automatik in Europa; Preis Hailea.
7. Boyd-Wehrdaten (kg O₂ je m³ je m Fall) und Aquakultur-Messung des freien Falls.
8. Venturi-SAE unter 0,5 bar und unabhängige Zahl zur Verstopfung.
9. Preis Kompositbehälter 10 × 35 und Chlor-Kapazität des Kohleblocks in Litern vom Hersteller.

## Entscheidungsfrage an Ben und Leon
**DEINE ENTSCHEIDUNG (Ben, mit Leon): Soll die Nachspeisung direkt aus der Hausleitung kommen, ohne Dauer-Aktivkohle, und die Station auf einen Kohle-Rückfall schrumpfen?**
- **A (Empfehlung):** Leitungswasser direkt, am Zulauf durchmischt; Station T83 schrumpft auf einen Einweg-Kohleblock oder entfällt, sobald der Versorger „Chlor, kein Chloramin" bestätigt oder der DPD-Test am Hahn Chlor zeigt. Kosten: Wasser 462 bis 643 €/Jahr [E], Test und Kohle-Ersatz nach Bedarf; spart Behälter, Kohle (UK-Bezug), Begrenzer, Probehahn und Kugelhähne. Freier Fall 0,3 bis 0,5 m am Pool-Zulauf als Planwert, kein Venturi.
- **B:** wie heute (2 Kompositbehälter mit katalytischer Kohle, auf Chloramin ausgelegt); sicher, aber Kohle nur UK belegt und die meisten Teile sind in Deutschland vermutlich überflüssig.
- **C:** Regenwasser als Hauptquelle; deckt nur 29 %, Tank ab 949 €, Dachmetall und Härte offen; nicht empfohlen.
**Folgefrage (ICH nach Ja zu A):** zweite Linear-Pumpe gegen 12-V-Notpumpe mit Akku prüfen, sobald eine Förderkurve bei 0,25 bar vorliegt.
**DEINE HANDLUNG (Ben):** E15 beim Versorger klären (Chlor, Chloramin oder keine Desinfektion; Härte in °dH; Gesamtchlor am Hausanschluss).

## Recherche-Kritiker
Datum 05.11.2026. Lücken (max. 5):
1. Zweite Quelle für „Chloramin in Deutschland nicht üblich" (DVGW, Verbraucherzentrale).
2. Chlorzehrung im Kreislauf (Messung oder Studie) fehlt; sie trägt die Aussage „System puffert selbst".
3. Förderkurve 12-V-Notpumpe bei 0,25 bar und Netzausfall-Automatik.
4. Aquakultur-Messung für den freien Fall (Boyd, Gameson-Original).
5. Regenwasser-Analysewerte und Flusswasser-Genehmigung.
Behebung: Nr. 1 bis 4 als eigener Auftrag, nur falls Ben A wählt.

**Geprüft gegen:** Quellen mit [Q] oben (EPA-Tabelle, Texas A&M EHT-147, FarmHub/FAO 589, Syndel 2002, SRAC 4607 und 452, Global Seafood Alliance, Küçükali 2023, TU Delft, Mazzei-Bulletin 10, BAnz-PDF UBA-Liste, BDEW, ZFK, DWD, LfU Bayern, BauNetz, DVGW, Stadt München, Hornbach AT, eBay.de Resun) · `docs/research/R54-venturi-belueftung.md`, R53, R45 Abschnitt 4 und 5, R37, `docs/parts/aktivkohle_station.md`, `data/system-specs.json` (Abschnitte `puffer`, `sauerstoff`), `docs/packages/wunschbuch-ben.md` W77 und W81 · Rechnungen: `python -X utf8 -I -c` (Bedarf, Verdünnung, Kosten, Regenertrag, Notluft-Bilanz, Akku-Laufzeit).

# Paket: Aquaponik-Konzept wissenschaftlich pruefen (Ben, 30.10.2026 00:30)
**Problem:** `scripts/system_specs.py` rechnet mit Bens Tabelle (1839 Tilapia, 10,7 kg Futter/Tag, 609 Pflanzen) und mit Annahmen (A). Ben: nichts blind uebernehmen (weder Tabelle noch Simulator), eigene Recherche, biologisch und wissenschaftlich stimmig, Fischbesatz auf die Beckengroesse bezogen. Die erste Rechnung zeigt Widersprueche (Pumpen 12/30 gegen 72 l/min je Linie, Pflanzflaeche deckt nur 38 % des Futters).
**Intent:** Ein Konzept, dessen Zahlen belegt zusammenpassen und im Viewer als Kennzahlen stehen.
**Goal:** (1) Besatz und Futter aus Beckenvolumen, Sauerstoff, Ammonium und Filterkapazitaet hergeleitet, mit Quellen; (2) Pflanzenzahl und -flaeche aus der Futterbilanz; (3) Pumpen, Belueftung, Strom aus Fluessen gerechnet; (4) jede [A]-Zahl in `system_specs.py` durch Quelle (mindestens zwei unabhaengige) ersetzt oder als Annahme mit Spannweite gekennzeichnet; (5) Viewer-Kennzahlen und Beschreibungen aktualisiert; (6) offene Konzeptentscheidungen fuer Ben benannt.

## Plan (Recherche parallel, je Block ein Agent, Ergebnis `docs/research/R17..R22.md`)
| Block | Frage | zu pruefen (heutiger Stand) |
|---|---|---|
| R17 Besatz | Tilapia: sinnvolle Besatzdichte kg/m³ in Aquaponik/RAS bei 26 m³ Pool (und Zuchtbecken), Endgewicht, Wachstumsrate, Temperatur; welche Dichte haelt das System bei Sauerstoff- und Ammoniumgrenzen | Tabelle: 1839 x 0,7 kg = 45 kg/m³; Tabellenbereich 60-150 |
| R18 Futter und Ammonium | Futterrate % Koerpergewicht/Tag, Proteingehalt, TAN-Anfall je kg Futter, Nitrit/Nitrat-Grenzen | 10,7 kg/Tag, TAN 9,2 % x 35 % [A] |
| R19 Filter | Nitrifikation je m² Oberflaeche und je m³ Medium (Bioballs/Hel-X/Kies), Absetzer-Auslegung, Verweilzeit, Spuelrate | 0,5 l/g und 1 l/g Regeln, Biofilter 0,52 m³ Medium |
| R20 Pflanzen | Futter-zu-Pflanzflaeche-Verhaeltnis (g/m²/Tag) fuer Blatt und Frucht, Naehrstoffe (K, Fe, Ca), Pflanzdichte NFT/Beet, Artenwahl | 40-50 g/m²/Tag, 80 m² Flaeche |
| R21 Hydraulik | Umwaelzrate (Beckenvolumen pro Stunde), Flutzyklen Glockensiphon, NFT-Durchfluss, Pumpenwirkungsgrad, Foerderhoehe | 143 l/min, 2 Zyklen/h [A], 0,5 l/min je Rinne |
| R22 Belueftung, Strom | Sauerstoffbedarf je kg Futter/Fisch, Belueftungswirkungsgrad kg O2/kWh, Heizbedarf Tilapia 26-28 °C in der Kuppel | 4,3 kg O2/Tag, 1 kg/kWh [A], Heizung nicht modelliert |

## Vorgehen
1. Je Block ein unabhaengiger Recherche-Agent (zwei Quellen mindestens, bevorzugt Extension-Dienste, Peer-Review, FAO), Ergebnis mit Zahl, Spannweite, Quelle, Konfidenz.
2. Orchestrator fuehrt zusammen: Besatz aus dem engsten Engpass (Sauerstoff, Ammonium, Filter, Pflanzflaeche) bestimmen, dann Futter, Pflanzen, Pumpen, Strom neu rechnen; `system_specs.py` auf Q-Quellen umstellen.
3. Widersprueche zu Bens Tabelle und zum Simulator offen benennen (nicht still korrigieren): Entscheidungsvorlage fuer Ben.
4. Viewer: Kennzahlen und Beschreibungen (data/descriptions.json) nachziehen.

## Stand
Plan steht, Recherche noch nicht gestartet (Wochenlimit 98 %, Reset 30.10. 03:00 Ortszeit). Start nach Freigabe mit frischem Limit: sechs Agenten, danach Zusammenfuehrung.

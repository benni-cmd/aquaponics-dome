# Aquaponik-Werte: Gesamttabelle und Stand der Recherche (30.10.2026)

> **STAND: Stop sauber am Wochenlimit (99 %, Reset 30.10. 03:00 Ortszeit).** Fertig: R17 und R18 als **Teilergebnis** (je zwei gelesene Primaerquellen, siehe unten). Offen: R19, R20, R21, R22 (nur Vorab-Werte aus den schon gelesenen Quellen, keine eigene Suche) sowie `aquaponik-empfehlung.md`. Alle "Vorab"-Zeilen sind ausdruecklich nicht abgeschlossen.
> Gelesen im Volltext: **SRAC 454** (Rakocy, Masser, Losordo 2006) und **FAO TP 589** (Somerville u. a. 2014); Fundstellen in `R17.md`. Zahlen nicht aus Bens Tabelle (`reference/Kuppelberechnung-neu-2.xlsx`) und nicht aus dem Simulator uebernommen, beide stehen nur als Vergleich in der Spalte "Abweichung".

## Gesamttabelle
| Wert | Spannweite | Quelle 1 | Quelle 2 | Konfidenz | Abweichung von Bens Tabelle / Annahme (A) / Simulator (S) |
|---|---|---|---|---|---|
| Besatzdichte Tilapia | 15-22 kg/m3 Auslegung; 20 kg/m3 FAO-Max.; 60 kg/m3 UVI-Absolutgrenze | FAO TP 589 Tab. 8.1 | SRAC 454 | mittel-hoch | Tabelle 45 kg/m3 (1287 kg) liegt dazwischen, nur mit UVI-Technik belegt; S: 15 kg/m3 (417 kg) passt zu FAO |
| Endgewicht Nile-Tilapia | 500 g (FAO, 6-8 Monate) bis 814 g (UVI, 24 Wochen) | FAO TP 589 | SRAC 454 Tab. 1 | mittel-hoch | Tabelle 0,7 kg: im Bereich |
| Futterrate | 1 % KG/Tag (1-2 %) bei >100 g | FAO TP 589 | (SRAC FCR 1,7) | mittel | Tabelle 10,7 kg/Tag = 0,83 % von 1287 kg: plausibel, aber Biomasse selbst ueberhoeht |
| TAN je kg Futter | 3,75 % (FAO-Beispiel, 32 % Protein); 3,0-4,0 % | FAO TP 589 | zweite Quelle OFFEN | mittel | A: 3,2 % ist 14 % niedriger; 401 statt 345 g TAN/Tag bei 10,7 kg |
| Nitrifikation je m2 Medium | 0,57 g TAN/m2/Tag konservativ (Bereich 0,2-2) | FAO TP 589 | OFFEN | mittel | nicht in der Rechnung bisher |
| Biofilter-Medium je g Tagesfutter | 1 l (Kies) / 0,5 l (Bioballs), Tab. in FAO: Bioballs 150-400 m2/m3 | FAO TP 589 | SRAC 454 (Standardformeln RAS) | mittel | wie A in `system_specs.py` |
| Volumen Absetzer + Biofilter | 10-30 % des Fischtankvolumens (Kleinanlage) | FAO TP 589 Tab. 8.1 | OFFEN | niedrig-mittel | Modell: Tanks 1,94 m3 = 7 % von 28,5 m3 |
| Futter je m2 Pflanzflaeche (Raft) | 60-100 g/m2/Tag | SRAC 454 | (UVI) | hoch | nicht verwendet |
| Futter je m2 (Substrat/NFT) | SRAC: ca. 25 % des Raft-Werts = 15-25 g/m2/Tag; FAO: Blatt 40-50, Frucht 50-80 | SRAC 454 | FAO TP 589 | mittel (Quellen widersprechen sich um Faktor 2) | A: 40-50; SRAC liegt bei Substrat/NFT deutlich niedriger |
| Medienbeet : Fischtank | 2 : 1 Volumen (Kies, ohne Feststoffabzug) | SRAC 454 | OFFEN | mittel | Modell: 8,2 m3 Substrat gegen 28,5 m3 Fischwasser = 0,29 : 1 |
| Umwaelzung Fischwasser | UVI: Retention Fischtank 82 min; FAO: gesamtes Fischtankvolumen je Stunde durch die Beete | SRAC 454 | FAO TP 589 | mittel | Modell 143 l/min = 8,6 m3/h bei 28,5 m3 -> Umwaelzzeit 3,3 h; die Quellen verlangen 1-1,4 h = 350-475 l/min |
| Flutzyklen Beet | FAO: Fischtankvolumen je Stunde durch die Beete; Zyklenzahl nicht belegt | FAO TP 589 | OFFEN | niedrig | A: 2/h bleibt Annahme |
| O2-Verbrauch Tilapia | Suchzusammenfassung: 400 g Fische 69/116/236 mg/kg/h bei 20/25/30 °C; Fuetterungspeak 111-161 | Koreanische Studie (nur Abstract) | niob (nur Suchtreffer) | **niedrig (nicht gelesen)** | A: 0,25 kg O2/kg Futter gleich 2,7 kg/Tag Fische; mit 100-160 mg/kg/h x 1287 kg = 3,1-4,9 kg/Tag |
| DO-Zielwert | 4-8 mg/l (Nitrifikation, Fische, Pflanzen); Nitrifikation stoppt <2 mg/l | FAO TP 589 5.1.4 | SRAC 454 (80 % Saettigung = 6-7 mg/l) | hoch | |
| Stromverbrauch Belueftung | nicht recherchiert | | | offen | A 1 kg O2/kWh unbelegt |
| Heizung | nicht recherchiert | | | offen | in Tabelle 219 EUR/Monat Strom; Modell ohne Heizung |

## Vorab-Engpassrechnung (aus gelesenen Quellen, nicht abgeschlossen)
Fischwasser 28,5 m3 (Pool 26,15 + Becken 2,4). Pflanzflaeche laut Tabelle 80,4 m2 (Substrat 37,97 + NFT 42,41).
- **Dichte (FAO 20 kg/m3):** 570 kg; Simulator 15 kg/m3: 428 kg; UVI 60 kg/m3: 1710 kg.
- **Pflanzflaeche (Futterbilanz bei 1 % KG/Tag):** SRAC 15-25 g/m2: 1,2-2,0 kg Futter/Tag = 120-200 kg Fisch; FAO Blatt 40-50: 3,2-4,0 kg/Tag = 320-400 kg; FAO Frucht 50-80: 4,0-6,4 kg/Tag = 400-640 kg.
- **Zwischenfazit:** Der engste Engpass ist die Pflanzflaeche (und die Annahme, dass sie die ganze Futterfracht verbraucht), nicht das Beckenvolumen. Eine tragfaehige Auslegung liegt bei etwa **320-640 kg Fisch (15-22 kg/m3), 3-6 kg Futter/Tag**; Bens Tabelle (1287 kg, 10,7 kg/Tag) braucht rund die doppelte bis vierfache Pflanzflaeche oder einen anderen Naehrstoffsenke (Wasserwechsel, Denitrifikation). Das ist ein Zwischenstand, kein Endergebnis.
- **Flaechenfrage Substratbeet:** Modellmasse ergeben 8 x (0,80 x 2,64) + 6 x (0,933 x 1,865) = **27,3 m2**, die Tabelle rechnet **37,97 m2** (Nennmasse 3,0/1,8 x 1,0). Die Pflanzflaeche ist also im Modell um rund 28 % kleiner. Und 2160 Toepfe auf 27,3 m2 sind rund 79 Toepfe/m2 (Raster ca. 11 cm), das ist fuer die meisten Fruchtgemuese und Blattgemuese zu dicht (R20 offen).

## Offene Fragen fuer Ben (entstanden bis jetzt)
1. Soll die Anlage wie Bens Tabelle bei 45 kg/m3 laufen (UVI-Niveau, braucht starke Belueftung, Klaerer und Netzfilter, mehr Pflanzflaeche) oder wie die Kleinanlagen-Leitfaeden bei 15-20 kg/m3?
2. Wird die Pflanzflaeche mit Modellmassen (27,3 m2 Substrat) oder Nennmassen (37,97 m2) gerechnet, und sind 2160 Toepfe auf den Beeten gewollt?
3. Heizung (Tilapia 26-28 °C in der Kuppel) im Strombudget: ja/nein.

## Reihenfolge fuer die Fortsetzung (nach Reset)
1. R19 Filter (TAN je Oberflaeche, Bioball-/Hel-X-Daten, Absetzer-Verweilzeit; Zweitquelle zu FAO).
2. R20 Pflanzen (SRAC 454 und FAO sind gelesen; fehlt eine dritte Quelle zu NFT-Futter-Verhaeltnis, Naehrstoffe K/Ca/Fe, Pflanzdichte).
3. R21 Hydraulik (UVI: 100 GPM/4 Tanks, FAO Tab. 8.1: 2000 l/h je 1000 l; Pumpen-Wirkungsgrad, Flutzyklen).
4. R22 Belueftung (Volltext zum O2-Verbrauch, kg O2/kWh der Belueftung; Heizlast) und Strom.
5. `aquaponik-empfehlung.md` mit Fischzahl, Futter, Pflanzflaeche, Pumpen.
6. Vergleichsspalte Simulator je Block (Seitenabruf zeigt nur Besatz 15 kg/m3 bei 27,8 m3 und Medienliste SSA, Rest per JavaScript).

Geprueft gegen: SRAC 454 (Volltext), FAO TP 589 (Volltext), `scripts/system_specs.py`, `data/system-specs.json`, `reference/oasis-simulator-notes.md` · Offen: R19-R22, Empfehlung, Zweitquellen fuer TAN-Faktor und O2-Verbrauch

# Aquaponik-Werte: Gesamttabelle R17-R22 (Stand 30.10.2026, alle sechs Bloecke bearbeitet)

> Quellen im Volltext gelesen: **SRAC 454** (Rakocy, Masser, Losordo 2006), **FAO TP 589** (Somerville u. a. 2014), **SRAC 451** (Losordo, Masser, Rakocy), **Losordo/DeLong 2015** (Global Seafood Alliance), **Fort Valley State Extension** (Duncan), **Aly 2007** (Egyptian J. Aquat. Res.), **Purdue CEA** (Miller/Nemali 2019); Abstract/Seite gelesen: **Kim & Jo 1999a/b** (Korean Fisheries Journals). Nur als Suchzusammenfassung (niedrige Konfidenz): UVI-Basilikum/Okra-Versuche, Aquaculture America 2023, HortTechnology/Horticultura Brasileira zu NFT, Colt & Orwicz 1991.
> Bens Tabelle (`reference/Kuppelberechnung-neu-2.xlsx`) und der Oasis-Simulator (`reference/oasis-simulator-notes.md`, nur 15 kg/m³ bei 27,8 m³ und Medienkatalog sichtbar) wurden nicht uebernommen, nur verglichen. Details und Fundstellen je Block in `R17.md` bis `R22.md`. Empfehlung: `aquaponik-empfehlung.md`.

## Gesamttabelle
Konfidenz: hoch = zwei Primaerquellen gelesen und uebereinstimmend; mittel = zwei Quellen mit Spanne oder eine Primaerquelle plus Sekundaerquelle; niedrig = nur Zusammenfassung oder Eigenableitung.

| Wert | Spannweite | Quelle 1 | Quelle 2 | Konfidenz | Abweichung (T = Bens Tabelle, A = unsere Annahme `system_specs.py`, S = Simulator) |
|---|---|---|---|---|---|
| **R17** Besatzdichte Beckenwasser | 15-22 kg/m³ Auslegung; 20 FAO-Maximum; 60 UVI-Obergrenze | FAO TP 589 Tab. 8.1 | SRAC 454 | mittel-hoch | T 45 kg/m³ (1287 kg) nur mit UVI-Technik belegt; S 15 kg/m³ (417 kg) passt zu FAO |
| Endgewicht Nil-Tilapia | 500 g (6-8 Monate, FAO) bis 814 g (24 Wochen, UVI) | FAO TP 589 | SRAC 454 Tab. 1 | mittel-hoch | T 0,7 kg im Bereich |
| Wachstum / FCR | 4,4 g/Tag; FCR 1,7 | SRAC 454 Tab. 1 | (FAO Wachstum 50 -> 500 g) | mittel | nicht in T/A |
| **R18** Futterrate | 1 % (1-2 %) KG/Tag bei >100 g; 3 % bei 50 g | FAO TP 589 | SRAC 454 (FCR) | mittel | T 10,7 kg/Tag = 0,83 % von 1287 kg plausibel, Biomasse zu hoch |
| TAN je kg Futter | 3-5 % (Mitte 3,75 %) | SRAC 451 | FAO 589; Losordo/DeLong 2015 | mittel-hoch | A 3,2 % am unteren Rand |
| Nitrit / Nitrat | Problem ab 0,25 mg/l Nitrit; Nitrat-N >200 mg/l vertraeglich | FAO TP 589 | SRAC 451 | mittel | nicht modelliert |
| **R19** Nitrifikation je Flaeche | 0,57 (0,2-2) g TAN/m²/Tag | FAO TP 589 | Losordo/DeLong (0,45 g/m² Tropfkoerper) | mittel | nicht in A |
| Bioballs-Kapazitaet (SSA 400) | 3-5 kg Futter/Tag je 0,52 m³ (FAO-Rechnung 6 g/l; Losordo 350 g TAN/m³/Tag) | FAO TP 589 | Losordo/DeLong 2015 | mittel | A 0,5 l/g = 1,0 kg/Tag (rund 3-fach Reserve) |
| Substrat-Kapazitaet (Blaehton/Kies) | 19-31 kg Futter/Tag fuer 8,2 m³ (2,3-3,8 g/l) | FAO TP 589 | SRAC 454 (Kies als alleiniger Biofilter) | mittel | A 1 l/g = 8,2 kg/Tag |
| Absetzer + Biofilter, Volumen | 10-30 % des Fischtankvolumens | FAO TP 589 Tab. 8.1 | SRAC 454 (UVI-Klaerer 3,8 m³/Paar) | niedrig-mittel | Modell 6,8 % (Tanks 1,94 m³) |
| Absetzer-Verweilzeit | ca. 20 min (UVI) | SRAC 454 | Fort Valley (1 ft²/gpm) | mittel | Modell 3,7 min bei 72 l/min; 20 min nur als Teilstrom ca. 13 l/min |
| **R20** Futter je m² Raft | 60-100 g/m²/Tag | SRAC 454 | Fort Valley State | hoch | nicht verwendet |
| Futter je m² Substrat/NFT | 15-25 (SRAC: 25 % Raft) bis 40-50 Blatt, 50-80 Frucht (FAO) | SRAC 454 | FAO TP 589 | mittel (Quellen widersprechen sich) | A 40-50; T rechnet 134 g/m² (10,7 kg auf 80 m²) |
| Volumenverhaeltnis Fisch : Kiesbeet | 1 : 2 (bis 1 : 4) | SRAC 454 | Fort Valley State | mittel | Modell 1 : 0,29 |
| Pflanzdichte | Blatt 20-25, Frucht 4-8 /m² | FAO TP 589 | (FAO Pflanzenblaetter) | mittel | Modell 79 Toepfe/m² Beet; T 7,6/m² |
| Zusatz | K, Ca, Fe (Fe-Chelat 2 mg/l ca. alle 3 Wochen); pH 7,0-7,5 | SRAC 454 | Fort Valley State | hoch | nicht modelliert |
| **R21** Umwaelzung Fischwasser | 60-82 min Retention = 350-475 l/min fuer 28,5 m³ (bei Bens Besatz); TAN-Formel: 121 l/min (3,5 kg Futter) bis 372 l/min (10,7 kg) | SRAC 454; FAO TP 589 | Losordo/DeLong 2015 (rekonstruiert) | mittel | Modell-Kreislauf 143 l/min (3,3 h) |
| NFT-Durchfluss | 1-2 l/min je Rinne | FAO TP 589 | HortTech/Horticultura Brasileira (Abstract) | mittel | A 0,5 l/min zu niedrig |
| Flutzyklus Beet | 5-8 min offen, 2 x/h | Fort Valley State | TCF Freshwater Institute (ueber Fort Valley) | niedrig-mittel | A 2 x/h bestaetigt |
| Pumpen-Wirkungsgrad Kleinpumpe | 16-33 % (abgeleitet aus 25-50 W fuer 2000 l/h bei 1,5 m) | FAO TP 589 | (Sulzer gross 85-88 %, nicht uebertragbar) | niedrig-mittel | A 35 % optimistisch |
| **R22** O2-Verbrauch Tilapia | 80-190 mg/kg/h (Mittel), Spitze 111-161 und +40-60 % | Kim & Jo 1999a | Kim & Jo 1999b; Aly 2007 | mittel | A entspricht ca. 88 mg/kg/h (unterer Rand) |
| O2 fuer Nitrifikation | 4,57 g O2 je g TAN | Stoechiometrie (nicht aus Quelle gelesen) | | niedrig | wie A |
| DO-Ziel | 4-8 mg/l, Nitrifikation stoppt <2 mg/l | FAO TP 589 | SRAC 454 (6-7 mg/l) | hoch | |
| Belueftungsleistung | SAE fein 1,2-2,0 kg O2/kWh; UVI 0,59 W/kg Fisch | Colt & Orwicz 1991 (sekundaer) | SRAC 454 (UVI) | niedrig-mittel | A 1 kg O2/kWh; UVI-Wert gibt hoeher |
| Temperatur Tilapia | 27-30 °C ideal; <17 °C kein Wachstum; <12 °C Tod | FAO TP 589 | SRAC 454 | hoch | Heizung nicht modelliert |
| Heizlast Huelle (R22, **ersetzt durch R24 unten**) | 3,1-6,8 W/m²K; Kuppel 0,7-0,9 kW/K (Halbkugel 226 m², Paneel-U) | Purdue CEA | (Huellmaterial offen) | mittel (Standort offen) | T 219 EUR/Monat reichen nicht |

## R24 Huelle als Plane (D39), Heizlast, Fruchtgemuese (30.10.2026, Details `R24.md`)
| Wert | Spannweite | Quelle 1 | Quelle 2 | Konfidenz | Abweichung |
|---|---|---|---|---|---|
| Huellflaeche netto | 208 m² (40 Dreiecke 209,9 − Tuerfeld) | E aus `haut_paneel.md` | | hoch (Rechnung) | R22 226 m² (ideale Halbkugel) |
| U Folie einlagig / doppelt luftgepolstert | 6,8 / 4,0 (2,8–5,7) W/m²K | Kentucky State Univ. (FarmHub 9.2) | Purdue CEA | mittel | R22 3,1–4,0 (Paneel-U) |
| **Heizlast PE doppelt** | **0,83 (0,59–1,18) kW/K**; Spitze 25 kW bei ΔT 30 K (−10/20 °C, Annahme Mitteleuropa); Jahres-Obergrenze ca. 70 MWh ohne Sonne | E aus Quelle 1+2; Gt20/15 3500 Kd (DWD ueber Rechnerportal) | | mittel (UA) / niedrig (Jahr) | R22 0,7–0,9 kW/K; Standort offen |
| Einsparung Doppel- gegen Einfachfolie | 25–60 % | Virginia Tech HORT-284 (Zusammenfassung) | Sherry u. a.; Domerama | niedrig-mittel | nicht eingerechnet |
| Lichtdurchlass einlagig / doppelt | 90 % / 75–80 % | Kentucky State Univ. | UMass (Suchzusammenfassung) | mittel | nicht in A/T |
| Lebensdauer UV-Gewaechshaus-PE | 4 Jahre (Standard 1–2, Baumarkt 1) | Domerama | UMass (Zusammenfassung) | mittel | |
| ETFE | 93–95 % Licht, 25–35 Jahre, 10–15-fach Preis, U-Wert nicht gefunden | Hersteller (Ceres) | HortiDaily | niedrig | |
| Folienpreis (PE doppelt mit Montage) | ca. 5 USD/m² (nur Haendlerangabe) | Prospiant | | niedrig | |
| Befestigung | Alu-Keilschiene + Federdraht auf allen 65 Streben (ca. 228 m); Zuschnitt je Dreieck mit Ueberlappung | Domerama | Northern Homestead; Haendler | mittel | D39 offen |
| Futter Fruchtgemuese | 50–80 g/m²/Tag (⅓ mehr als Blatt); Bens Mix ca. 55 g/m² = 3,8 kg Futter/Tag | FAO TP 589 | UVI-Okra 95,6 g (Zusammenfassung) | mittel | R20 45 g Blatt-Mitte |
| Suesskartoffel | in Aquaponik **nicht belegt**; NFT-Rinnenabstand ≥ 25–38 cm | Mortley u. a. 1991 (Abstract) | | niedrig | Topfraster 11 cm zu eng (E) |
| Kondenswasser | Doppelfolie reduziert, Anti-Drip + Anti-Fog senkt Pilzdruck; Aquaponik-Messwerte nicht belegt | Kentucky State Univ. | Univ. Thessalien (Abstract) | niedrig-mittel | |

## R26 Pflanzmix fuer D40 (31.10.2026, Details `R26.md`)
| Wert | Spannweite | Quelle 1 | Quelle 2 | Konfidenz | Abweichung |
|---|---|---|---|---|---|
| Artenzuordnung | Beete: Tomate, Paprika, Gurke, Knollen; NFT: Blatt und Kraeuter; Fruchtgemuese im NFT nur mit grossen Rohren | FAO TP 589 (Kap. 6.4, Pflanzenblaetter) | SRAC 5009 (Zusammenfassung) | mittel | Bens Liste: Kohlrabi 100, Sellerie 50 weichen (Knollen nur Beet) |
| Pflanzdichte Beete | Tomate 3–5, Paprika 3–4, Gurke 2–5 /m²; Suesskartoffel 8/m² [A] | FAO TP 589 | Mortley u. a. 1991 (hydroponisch) | mittel / niedrig | Modell 79 Topfplaetze/m², Mix 4,8 Pflanzen/m² |
| Bepflanzte Topfplaetze | 806 von 2834 (Beete 132 = 6 %, NFT 674 = 100 %) | E | | hoch (Rechnung) | Topfzahl = Kapazitaet |
| Futter Empfehlungsmix | Beete 80, NFT 50 g/m² = **4,67 kg/Tag = 467 kg Fisch** (nur obere FAO-Werte) | FAO TP 589 | | mittel-niedrig | D40 4,75 kg; Ziel 4,3–5,0 |
| Rueckfall | 335 (untere FAO) – 420 kg (Mitte, Bens Mix); SRAC-NFT 302 kg | FAO TP 589 | SRAC 454 | mittel-niedrig | D45: 380–430 |
| Steuerregel | Nitrat 5–150 mg/l: unter 5 Futter erhoehen, ueber 150 Wasser teilweise wechseln | FAO TP 589 Kap. 8 | | mittel | Besatz stufenweise statt sofort 475 kg |
| Suesskartoffel | in Aquaponik **nicht belegt** | Mortley u. a. 1991 (Abstract) | | niedrig | Bens 151 Pflanzen -> Mix 62 |

## R27 Puffer-Station und Drittbecken (31.10.2026, Details `R27.md`)
| Wert | Spannweite | Quelle 1 | Quelle 2 | Konfidenz | Abweichung |
|---|---|---|---|---|---|
| Sumpf / Basentank gegen Systemwasser | UVI: Sumpf 160 gal + Basentank 50 gal von 29 375 gal = 0,7 %; FAO: Sumpf mindestens 70 % des Medienbett-Volumens (nur bei Sumpf-Bauweise) | SRAC 454 (UVI-Daten) | FAO TP 589 Kap. 4.3 | mittel | Puffer 2,0 m³ = 5 % (rund das 7-fache der UVI-Station); Beete laufen in den Pool, nicht in den Puffer |
| Wasserverlust | unter 2 %/Tag Wasserwechsel (geschlossene Anlage) | SRAC 454 | (zweite Quelle offen) | niedrig-mittel | Puffer deckt 2,9 Tage |
| Frischwasser | 2 Tage stehen lassen (Chlor), nur entchlort einsetzen | FAO TP 589 | SRAC 454 | mittel | Puffer als Vorrat |
| Alkalinitaetsverbrauch | 7,14 g CaCO₃ je g TAN-N (Theorie); praktisch etwa 50 % (250 gegen 500 g NaHCO₃ je kg Futter) | Boyd 2016 (GAA, gelesen) | Timmons u. a. 2018 / Brune (Suchzusammenfassung) | mittel / niedrig | nicht in A; 25 Aequivalente/Tag theoretisch |
| Basenmenge | 0,6 kg/Tag je halb Ca(OH)₂ und KOH (praktisch); KOH allein 0,71, Ca(OH)₂ allein 0,47, NaHCO₃ 1,07 kg/Tag | E aus Boyd und Brune | SRAC 454 (UVI wechselt KOH/Ca(OH)₂) | niedrig-mittel | Kaliumbedarf der Pflanzen viel kleiner |
| pH-Ziel | 7,0–7,5 (UVI) gegen 6–7 (FAO-Kompromiss) | SRAC 454 / Fort Valley State | FAO TP 589 | mittel | |
| Eisen | 2 mg/l Chelat ca. alle 3 Wochen ≈ 74 g Fe | SRAC 454 | Fort Valley State | hoch | |
| Quarantaene | Neufische 45 Tage isolieren; Besatz 77 Fische/m³ à 79 g, FAO-Max 20 kg/m³ | FAO TP 589 | SRAC 454 Tab. 1 | mittel | Drittbecken 72 Fische, 5,7 kg |
| Sensorstrom | pH-Kreis 18 mA, EC-Kreis 50 mA bei 5 V (0,1 und 0,25 W); Kit pH+DO+EC 310 mA | Atlas Scientific Datenblaetter | Haendlerseite Kit | mittel | Station ca. 17 W insgesamt |
| Dosierpumpe | 12 V, 5–10 W, 4,5–220 ml/min | Kamoer-Datenblaetter (Haendler) | | niedrig-mittel | 2 Stueck, 25 % Laufzeit |

## Zusammenfassung der Abweichungen von Bens Tabelle
1. **Fischbiomasse 1287 kg (45 kg/m³)** liegt ueber dem FAO-Wert (20 kg/m³) und braucht UVI-Technik; Pflanzflaeche und Substrat tragen davon nur 180-640 kg.
2. **Futter 10,7 kg/Tag** ist 2-6-fach ueber dem, was 80 m² Pflanzflaeche (Modell: 27,3 m² Substrat + 42,4 m² NFT) verbrauchen koennen (1,8-6,4 kg/Tag).
3. **Substratflaeche 37,97 m² (Tabelle) gegen 27,3 m² (Modellmaß)**; 2160 Toepfe = 79/m².
4. **Pumpen:** 143 l/min decken nur ca. 4 kg Futter/Tag nach TAN-Rechnung; Pflanzenstrom allein 177-245 l/min.
5. **Strom** ohne Heizung 0,26-1,3 kW; Heizung 0,7-0,9 kW je Kelvin Differenz, bei Ben 219 EUR/Monat nicht gedeckt (Standort offen).

## Offene Punkte (nicht erfunden)
UVI-Volltexte (401), SRAC 453 (Fehlerseite), Boyd-SAE-Primaertabelle, Peer-Review-Volltexte NFT-Durchfluss, Temperaturangabe Kim & Jo 1999a, Hel-X-Daten, Standort/Huelle der Kuppel, Suesskartoffel/Kohlrabi/Sellerie im Aquaponik, Winterbetrieb Nitrifikation.

Geprueft gegen: SRAC 454, SRAC 451, FAO TP 589 (Volltexte), Losordo/DeLong 2015, Fort Valley State, Aly 2007, Purdue CEA, Kim & Jo 1999 (Abstracts), `scripts/system_specs.py`, `data/system-specs.json`, `reference/oasis-simulator-notes.md` · Offen: siehe oben und Fragen in `aquaponik-empfehlung.md`

# Empfehlung: Fischzahl, Futter, Pflanzflaeche, Pumpen (30.10.2026)

Grundlage: `aquaponik-werte.md` und `R17.md` bis `R22.md`. Alle Zahlen sind Auslegungsvorschlaege aus Literaturwerten, keine fachliche Freigabe; Ben entscheidet. Eigene Ableitungen sind als (E) markiert.

## 1. Engpassrechnung (Fischwasser 28,5 m³: Pool 26,15 + zweites Becken 2,4)
Futter 1 % der Biomasse je Tag (FAO), Biomasse = Futter / 0,01:

| Engpass | Grenze Futter kg/Tag | entspricht Fisch | Quelle |
|---|---|---|---|
| Sauerstoff / Dichte, FAO-Klein 20 kg/m³ | 5,7 | 570 kg | FAO TP 589 |
| Sauerstoff / Dichte, UVI-Technik 60 kg/m³ | 17 | 1710 kg | SRAC 454 |
| Sauerstoff-Belueftung (E): 80-190 mg/kg/h + Nitrifikation | je Belueftung loesbar, kein fester Deckel | | R22 |
| Ammonium / Biofilter 0,52 m³ + 8,2 m³ Substrat | 9,2 (Faustregel) bis >20 (FAO-Tabelle) | 920 kg bis >2000 kg | R19 |
| Ammonium / Pumpenstrom (heute 143 l/min, TAN 1,5 mg/l, 50 %) | 4,1 | 410 kg | Losordo/DeLong (E) |
| **Pflanzflaeche (Substrat 27,3 m² + NFT 42,4 m²)**, 25-65 g/m²/Tag | **1,7-4,6** (bis 6,4 bei 80 g auf Tabellenflaeche) | **170-460 kg** (bis 640) | SRAC 454, FAO TP 589 |
| **Substratvolumen 8,2 m³** nach SRAC 1 : 2 (E) | 2,5 | 250 kg | SRAC 454 |

**Engster Engpass: die Pflanzen** (Pflanzflaeche und Substratvolumen). Beckenvolumen, Sauerstoff und Filter sind es nicht, wenn die Belueftung gross genug ist.

## 2. Empfehlung
| Groesse | Bens Tabelle / heute | Empfehlung | Spanne | Begruendung |
|---|---|---|---|---|
| Fischbiomasse (stehend) | 1287 kg (45 kg/m³) | **350 kg (12 kg/m³)** | 250-570 kg (9-20 kg/m³) | Mitte der Pflanzengrenze 170-460 kg; Simulator 417 kg bei 15 kg/m³ liegt im Band; FAO-Maximum 570 kg |
| Fischzahl bei Endgewicht 0,7 kg | 1839 | **ca. 500 (gestaffelt 3 Altersgruppen: ca. 700 Fische insgesamt)** | 360-810 | Biomasse / 0,7 kg; Besatzstaffel nach SRAC 454 |
| Futter | 10,7 kg/Tag | **3,5 kg/Tag** | 2,5-5 kg/Tag | 1 % der Biomasse; deckt sich mit der Pflanzengrenze |
| Pflanzflaeche fuer 10,7 kg/Tag (falls Ben die Fischmenge behalten will) | 80 m² | **165-240 m²** bei 45-65 g/m², oder 107-178 m² Raft (60-100 g) | | Flaeche = Futter / (g/m²) |
| Hauptkreislauf (Pool -> Filter -> Pflanzen -> Pool) | 143 l/min; Modellpumpen 12/30 l/min | **180-250 l/min gesamt, 90-125 l/min je Linie** | 177-245 (Pflanzenstrom) | NFT 68 Rinnen x 1-2 l/min = 68-136; Beete 109 (2 Zyklen/h); deckt nach TAN-Rechnung 5-7 kg Futter/Tag |
| Absetzer | 267 l je kleiner Tank, bei 72 l/min = 3,7 min | **Teilstrom ca. 13 l/min je Tank (20 min) oder Volumen 1,4 m³ je Linie** | | UVI-Klaerer ca. 20 min |
| Pumpenleistung elektrisch | 134 W | **230-320 W** (bei 245 l/min, 2 m, 25-35 %) | | FAO-Wirkungsgrad 16-33 % |
| Belueftung | 177 W | **200-300 W Geblaese, Reserve 1 + 1** | 90-760 W | UVI 0,59 W/kg Fisch = 207 W bei 350 kg |
| Strom ohne Heizung | 351 W | **470-660 W (11-16 kWh/Tag)** | 0,26-1,3 kW | Summe |
| Heizung | nicht modelliert | **Zeile ergaenzen, 0,7-0,9 kW je Kelvin Differenz zur Aussenluft** | | Purdue-U-Werte, Halbkugel 226 m² (E); Standort offen |

## 3. Was sich im Modell/Viewer aendern wuerde (nur Vorschlag, Orchestrator entscheidet)
- `system_specs.py`: Biomasse nicht 1839 x 0,7, sondern Auslegungswert; TAN 3,75 % (3-5 %); NFT 1 l/min; PUMP_EFF 0,25; Flaeche Substrat 27,3 m²; Konsistenz "Pflanzflaeche deckt Futter" gegen 45 g/m²; Filterkapazitaet Faustregel *und* FAO-Tabelle; O2 aus Biomasse x 80-190 mg/kg/h + 4,57 x TAN; Heizung als eigene Zeile.
- Pumpenbeschreibungen im Viewer: Kreislauf 180-250 l/min statt 12/30 l/min, Absetzer als Teilstrom.

## 4. Offene Fragen an Ben
1. **Fischmenge:** Biomasse an die Pflanzflaeche anpassen (350 kg, 3,5 kg Futter/Tag) **oder** Pflanzflaeche auf 165-240 m² vergroessern (z. B. Raft/DWC in den Beeten, Kuppel hat nur ca. 80 m²)? Alternative: Naehrstoffsenke ausserhalb der Pflanzen (Wasserwechsel, Denitrifikation), nicht recherchiert.
2. **Pflanzflaeche:** Zaehlen 27,3 m² (Modell) oder 37,97 m² (Tabelle) Substratflaeche? Wollen wir die 2160 Topfplaetze (79/m²) bepflanzen oder nur 20-25 Blatt- bzw. 4-8 Fruchtpflanzen je m²?
3. **Standort und Huelle der Kuppel** (Aussenklima, Folie/Polycarbonat/Glas): bestimmt die Heizlast; Ben nennt 219 EUR/Monat Strom, das deckt die Heizung im Winter nicht.
4. **Fisch im zweiten Becken (2,4 m³, 1 m tief)** getrennt (Brutbecken/Quarantaene) oder im Gesamtbesatz?
5. **Pumpen:** zwei Linien mit je 90-125 l/min oder weiterhin Modellpumpen 12/30 l/min als Filter-Teilstrom plus eigene Hauptpumpen?
6. **Notstrom/Alarm:** Belueftungsausfall fuehrt in Intensivsystemen zum Totalverlust (SRAC 451, FAO); Notstrom/Alarm einplanen?

## 5. Grenzen dieser Empfehlung
Konfidenz mittel. Die Futter-Pflanzenflaechen-Verhaeltnisse widersprechen sich zwischen SRAC (25 % von Raft) und FAO (40-80 g/m²) um den Faktor 2-3; die Empfehlung nimmt die Mitte. Nicht belegt: Suesskartoffel/Kohlrabi/Sellerie, Winterbetrieb, SAE im Feld, Pumpenkennlinien, Peer-Review-Volltexte. Die Eigenableitungen (E) sind nachrechenbar, aber nicht gegenpruefbar durch eine Quelle.

Geprueft gegen: `aquaponik-werte.md`, `R17.md`-`R22.md` (Quellen dort), `scripts/system_specs.py`, `reference/oasis-simulator-notes.md` · Offen: Fragen 1-6 oben, UVI-Volltexte, SRAC 453, Standort

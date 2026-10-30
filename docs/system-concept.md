# Systemkonzept: passt die Rechnung zusammen? (Stand 30.10.2026 nach Fachrecherche R17–R22, Auftrag R23)
Rechnung: `python scripts/system_specs.py` -> `data/system-specs.json` (der Viewer zeigt sie, wenn nichts ausgewaehlt ist). Herkunft je Zahl: Q Quelle (R-Nummer in `docs/research/`, Gesamttabelle `docs/research/aquaponik-werte.md`), E eigene Rechnung, A Annahme, B Bens Tabelle (R15). Grundlage der Auslegung: `docs/research/aquaponik-empfehlung.md`. **Vorlaeufig**, bis Ben die Fragen 1–6 der Empfehlung beantwortet hat. Keine fachliche Freigabe.

## Ergebnis auf einen Blick (Auslegung | Bens Tabelle B)
| Groesse | Auslegung (Quelle) | Bens Tabelle / vorher |
|---|---|---|
| Wasser gesamt | 34 m³ (Pool 26,2 · zweites Becken 2,4 · Tanks 1,9 · Beete 3,3 · NFT 0,1 · Rohre 0,2); Fischwasser 28,5 m³ [E] | B: 25 m³ Systemwasser, Zisterne 5 m³ ausserhalb |
| Fisch | **350 kg** = 12 kg/m³, ca. **500 Fische** a 0,7 kg [E aus R20; FAO 589 max. 20 kg/m³; Simulator 15 kg/m³] | B: 1839 Fische, 1287 kg = 45 kg/m³ (nur mit UVI-Technik belegt, SRAC 454) |
| Futter | **3,5 kg/Tag** = 1 % KG [Q FAO 589] | B: 10,7 kg/Tag |
| Ammonium (TAN) | **131 g/Tag** = 3,75 % des Futters [Q SRAC 451, FAO 589, Losordo/DeLong] | vorher 3,2 %: B-Futter ergibt 402 statt 345 g/Tag |
| Pflanzflaeche | **69,7 m²** (Substrat 27,3 nach Modellmassen + NFT 42,4) [E/B] | B: 80,4 m² (Substrat 37,97) |
| Hauptkreislauf | **220 l/min** (4 grosse Pumpen a 55, je Linie 110) [D38]; Bedarf Pflanzen 177 l/min (NFT 1 l/min x 68 + Beete 109) bis 245 (NFT 2 l/min) [Q FAO 589, Fort Valley State] | vorher 143 l/min (NFT 0,5) |
| Absetzer-Teilstrom | **4 x 12,5 l/min** (je Tank eine in Betrieb) -> 21 min Verweilzeit [Q UVI ca. 20 min] | vorher 12/30 l/min als Modellwerte |
| Strom (ohne Heizung) | **ca. 570 W = 13,6 kWh/Tag = 408 kWh/Monat** (Pumpen 321 W, Belueftung 206 W, Steuerung 40 W); Spanne 0,26–1,3 kW [Q R21, R22] | B: 219 EUR/Monat, Aufteilung unbekannt; vorher 351 W |
| Heizung | **0,7–0,9 kW je Kelvin** Differenz zur Aussenluft (Halbkugel 226 m², U 3,1–4,0 W/m²K); Beispiel dT 20 K: 14–18 kW; Wasserspeicher 40 kWh je K [E aus Purdue CEA, R22] | nicht modelliert |
| Sauerstoff | 1,3–2,2 kg O₂/Tag (Fische 80–190 mg/kg/h + Nitrifikation 4,57 g/g TAN) [Q Kim & Jo, Aly] | vorher 4,3 kg/Tag bei B-Futter |

## Was die Konsistenzpruefung zeigt (Viewer: ✔ / ⚠)
✔ Besatzdichte unter 20 kg/m³ · ✔ Biofilter/Substrat deckt das Futter (Faustregel 9,2 von 3,5 kg/Tag; FAO-Tabelle noch hoeher) · ✔ Hauptkreislauf 220 l/min deckt Pflanzenstrom (NFT 1 l/min) und das Futter (TAN-Durchfluss 122 l/min, traegt bis 6,3 kg Futter/Tag) · ✔ Absetzer 21 min · ✔ Belueftung deckt Sauerstoff mit Spitzenfaktor.
⚠ **Pflanzflaeche deckt das Futter nur zu 90 %** bei 45 g/m²/Tag (Spanne 50 % bei 25 g, SRAC 454, bis 130 % bei 65 g, FAO Frucht): Auslegung ist knapp.
⚠ **Substratvolumen traegt nach SRAC-Regel (Fisch : Kies = 1 : 2) nur ca. 250 kg Fisch** gegen 350 kg Auslegung (Raft-/NFT-Flaechen nicht angerechnet).
⚠ **Bens Tabellenfutter (10,7 kg/Tag)** wird von der Pflanzflaeche nur zu 29 % gedeckt; noetig waeren ca. 238 m² statt 70 m², oder ein Hauptkreislauf von 372 l/min und mehr Pflanzflaeche.
Hinweis zu NFT 2 l/min je Rinne (oberes Ende der Quellen): Bedarf 245 l/min liegt ueber den 220 l/min der Hauptpumpen.

## Offene Konzeptentscheidungen fuer Ben (aus `aquaponik-empfehlung.md`, nicht erfunden)
1. **Fischmenge:** an die Pflanzflaeche anpassen (350 kg, 3,5 kg Futter/Tag) oder Pflanzflaeche auf 165–240 m² vergroessern (Raft/DWC)? Die Kuppel hat ca. 80 m².
2. **Pflanzflaeche und Topfzahl:** 27,3 m² (Modell) oder 37,97 m² (Tabelle) Substratflaeche; 2160 Topfplaetze (79/m²) bepflanzen oder nur 20–25 Blatt / 4–8 Frucht je m²?
3. **Standort und Huelle** (Aussenklima, Folie/Polycarbonat/Glas) fuer die Heizlast; 219 EUR/Monat decken die Heizung im Winter nicht.
4. **Zweites Becken (2,4 m³):** getrennter Besatz (Brut/Quarantaene) oder im Gesamtbesatz?
5. **Pumpen:** D38 (4 grosse = Hauptkreislauf 220 l/min, 4 kleine = Absetzer-Teilstrom) bestaetigen oder eigene Hauptpumpen?
6. **Notstrom und Alarm:** Belueftungsausfall fuehrt in Intensivsystemen zum Totalverlust.

## Naechste Schritte
Ben beantwortet die Fragen 1–6; danach `data/system.json` und `scripts/check_hydraulics.py` auf diese Zahlen stellen (M4). Offene Recherche: UVI-Volltexte, SRAC 453, Standort/Huelle, Suesskartoffel/Kohlrabi/Sellerie im Aquaponik, Winterbetrieb Nitrifikation.

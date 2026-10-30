# Systemkonzept: passt die Rechnung zusammen? (Stand 30.10.2026 nach Fachrecherche R17–R24, Entscheidungen D38–D40, Auftrag R25)
Rechnung: `python scripts/system_specs.py` -> `data/system-specs.json` (der Viewer zeigt sie, wenn nichts ausgewaehlt ist). Herkunft je Zahl: Q Quelle (R-Nummer in `docs/research/`, Gesamttabelle `docs/research/aquaponik-werte.md`), E eigene Rechnung, A Annahme, B Bens Tabelle (R15), D Entscheidung. Grundlage: `docs/research/aquaponik-empfehlung.md`, Huelle `docs/research/R24.md`. **Vorlaeufig** (Standort offen, 4. Aussenrinne ungeprueft). Keine fachliche Freigabe.

## Auslegung (Ben, D40): 475 kg Fisch (Spanne 450–500) — Bedingungen
| Groesse | Auslegung | Bens Tabelle B |
|---|---|---|
| Wasser gesamt | 34 m³ (Pool 26,2 · zweites Becken 2,4 · Tanks 1,9 · Beete 3,3 · NFT 0,1 · Rohre 0,2); Fischwasser 28,5 m³ [E] | 25 m³ Systemwasser |
| Fisch | **475 kg** [D40] = 17 kg/m³ [FAO 589 max. 20 = 570 kg], **ca. 680 Fische** a 0,7 kg gestaffelt [E] | 1839 Fische, 1287 kg = 45 kg/m³ (nur mit UVI-Technik, SRAC 454) |
| Futter / Ammonium | **4,75 kg/Tag** (1 % KG, Q FAO 589); **178 g TAN/Tag** (3,75 %, Q SRAC 451, FAO 589) | 10,7 kg/Tag; TAN 402 g |
| Pflanzflaeche | 69,7 m² mit 3 Aussenrinnen (Substrat 27,3 + NFT 42,4); **76,3 m² mit 4. Aussenrinne** (+8 Rinnen, ca. 148 m, ca. 677 Toepfe [A], W24 prueft) | 80,4 m² (Substrat 37,97) |
| noetiges Futter je m² | **68 g** (3 Rinnen) bzw. **62 g** (4 Rinnen); Blatt 45, Frucht 72,5 g (Q FAO 589) | 134 g |
| noetiger Fruchtgemuese-/Knollenanteil | **ca. 84 %** (3 Rinnen) bzw. **ca. 63 %** (4 Rinnen); Bens Pflanzmix hat 35 % | |
| tragbar mit Bens Mix | **381 kg** (3 Rinnen) bzw. **417 kg** (4); nur Blatt 314/344 kg; nur Frucht 506/554 kg [E] | |
| Hauptkreislauf | **220 l/min** (4 grosse Pumpen a 55, je Linie 110) [D38]; Bedarf Pflanzen 177 l/min (NFT 1 l/min), mit 4. Rinne 185; bei NFT 2 l/min 245 [Q FAO 589, Fort Valley State]; trägt nach TAN-Rechnung bis 6,3 kg Futter/Tag (Bedarf bei 4,75 kg: 165 l/min) [Q Losordo/DeLong, rekonstruiert] | vorher 143 l/min |
| Absetzer-Teilstrom | 4 kleine Pumpen a 12,5 l/min, je Tank eine in Betrieb → 21 min Verweilzeit [Q UVI ca. 20 min]; mit beiden 11 min | |
| Sauerstoff | 1,7–3,0 kg O₂/Tag (Fisch 80–190 mg/kg/h + Nitrifikation) [Q Kim & Jo, Aly] | |
| Strom (ohne Heizung) | **ca. 720 W = 17,3 kWh/Tag = 519 kWh/Monat** (Pumpen 321 W, Belueftung 280 W [UVI 0,59 W/kg], Geblaese Luftpolster 80 W [A], Steuerung 40 W); Spanne 0,38–0,92 kW | B: 219 EUR/Monat, Aufteilung unbekannt |

## Huelle: Plane (D39, Empfehlung R24)
Doppelte, luftgepolsterte UV-PE-Folie (6 mil, IR-Sperre, Anti-Drip/Anti-Fog), **208 m² netto** (40 ebene Dreiecke minus Tuerfeld) [E], Alu-Keilschiene mit Federdraht auf allen 65 Streben (ca. 228 m) [Q Domerama], Lebensdauer ca. 4 Jahre, Licht 75–80 % [Q Kentucky State Univ., Purdue CEA]. **Heizlast 0,83 kW je Kelvin** (0,58–1,19; U 4,0, 2,8–5,7 W/m²K), bei ΔT 30 K (Annahme Mitteleuropa −10/20 °C) **ca. 25 kW Spitze**, Jahres-Obergrenze ca. 70 MWh ohne Sonnengewinn, Infiltration und Thermoschirm (Gradtagzahl 3500 Kd [A/Q Rechnerportal nach DWD]). Wasser speichert 40 kWh je Kelvin. Die Doppelstegplatten (W19/W20) bleiben als ruhende Variante. **Standort ist offen**, die Heizung steht nicht in den Stromwerten.

## Was die Konsistenzpruefung zeigt (Viewer: ✔ / ⚠)
✔ Besatzdichte 17 kg/m³ unter 20 · ✔ Biofilter/Substrat deckt das Futter (Faustregel 9,2 von 4,75 kg/Tag) · ✔ Hauptkreislauf deckt Pflanzenstrom (NFT 1 l/min) und Futter (TAN) · ✔ Absetzer 21 min · ✔ Belueftung deckt den Sauerstoff mit Spitzenfaktor.
⚠ **Pflanzflaeche deckt das Futter nicht mit Bens Mix** (381 kg statt 475 kg; mit 4. Rinne 417 kg): D40-Bedingung ist hoher Fruchtanteil (63–84 %) und die 4. Rinne.
⚠ **Substratvolumen traegt nach SRAC (1 : 2) nur ca. 252 kg Fisch**; die uebrigen ca. 225 kg tragen NFT-Flaechen und Fruchtgemuese (NFT-Futter-Verhaeltnis ist der Unsicherheitsfaktor: SRAC 25 g gegen FAO 40–80 g).
⚠ **Bens Tabellenfutter (10,7 kg/Tag)** wird von der Pflanzflaeche nur zu 29 % gedeckt (nötig ca. 238 m²).
⚠ **Standort/Heizlast offen.** NFT mit 2 l/min je Rinne (obere Quellgrenze) brauchte 245 l/min, mehr als die 220 l/min der Hauptpumpen.

## Neue Schluessel in `system-specs.json` (fuer den Viewer)
`huelle` (Material, Flaeche, U, Befestigung, Lebensdauer), `szenario` (`drei_rinnen`, `vier_rinnen`, Schalter `AUSSEN_RINNEN`), `leistung.heizung` (w_je_k, beispiel_dT30_kw, jahr_obergrenze_mwh), `leistung.geblaese_luftpolster_w`, `sauerstoff`, `fische.bedingung`, `fische.obergrenze_fao_kg`, `pflanzen.noetig_g_m2`, `pflanzen.noetiger_fruchtanteil`, `pflanzen.tragbar_bens_mix_kg`, `kapazitaet.pflanzen_kg_futter_tag_bens_mix`, `offene_fragen`, `herkunft`.

## Offene Konzeptentscheidungen fuer Ben
1. **Fruchtgemuese-Anteil** im Pflanzplan: D40 braucht 63–84 %, der Plan hat 35 % (62 Tomaten, 151 Suesskartoffeln von 609); Suesskartoffel in Aquaponik nicht belegt. Alternativ Fisch auf ca. 380–420 kg.
2. **4. Aussenrinne** (W24): Radialbudget, Laufwege; bis dahin Annahme.
3. **Standort und Aussenklima** (Heizlast, Jahresenergie; 219 EUR/Monat decken die Heizung nicht).
4. **Zweites Becken (2,4 m³):** Besatz oder Brut/Quarantaene.
5. **Notstrom und Alarm** fuer die Belueftung; Geblaese und Windlast der Plane.

## Naechste Schritte
Ben beantwortet die Fragen; danach `data/system.json` und `scripts/check_hydraulics.py` auf diese Zahlen stellen (M4). Offene Recherche: UVI-Volltexte, SRAC 453, Standort/Huelle-Datenblatt, Suesskartoffel im Aquaponik, Winterbetrieb Nitrifikation.

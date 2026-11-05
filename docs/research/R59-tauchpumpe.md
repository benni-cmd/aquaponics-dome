# R59: Tauchpumpe für den Poolboden, 55 l/min bei 2,3 m (Nachfolge R58 ZR1)

**Priorität:** H · **Bearbeitet:** 05.11.2026 · **Rolle:** Fachrecherche, nur lesen und eine Datei schreiben; nichts gekauft, Modell und `data/` unverändert.
**Problem:** R58 ZR1 fand keine Tauchpumpe, die 55 l/min bei 2,3 m, eine Kennlinie als Zahlen, ≥ 2,5 m Eintauchtiefe, Lebensmitteleignung (D85) und Bezug in Europa (D76) zugleich belegt. **Intent:** Die Montage (Zielbild S, D88) soll vor dem Bau eine konkret benannte Pumpe haben. **Goal:** eine Empfehlung mit Rückfall; jede Lücke benannt mit dem Weg, sie zu schließen.
**Herkunft:** [Q] Seite oder PDF selbst gelesen · [Q-Treffer] nur Suchausschnitt · [E] eigene Rechnung (Befehl daneben) · [A] Annahme. Physik vor Strom (`docs/designprinzipien.md`): zuerst Durchfluss bei 2,3 m, dann Leistung.

## Antwort in vier Sätzen
1. **Auch diese zweite Runde findet keine Pumpe mit Hersteller-Kennlinie als Zahlen:** Oase, Eheim, Aquaforte und Jebao zeigen die Kurve nur als Bild oder gar nicht, Händler und Hersteller (oase.com, water-garden.co.uk) sperrten Abrufe (HTTP 429/403, Bot-Schutz). Die Kennlinie liegt also nur als Grafik vor und muss per Bildansicht oder Hersteller-Anfrage geholt werden.
2. **Empfehlung (bedingt): Oase AquaMax Eco Premium 8000** (65 W bei Qmax, regelbar, Einbautiefe 4 m laut Baureihen-Handbuch). Sie liefert bei 2,3 m auch mit der pessimistischen linearen Näherung noch rund 58 l/min [E]; die kleinere Eco Premium 5000 (35 W) liegt je nach Kurvenform bei 29 bis 63 l/min und ist damit nicht belegbar.
3. **Rückfall:** Aquaforte EC-10000 (kupferfrei, 68 W bei Qmax, 129 €, Hornbach DE); Eintauchtiefe aber unbelegt (Handbuch nur als Bild-PDF).
4. **Zwei kleinere Pumpen je Linie sind keine Verbesserung:** acht statt vier Pumpen und Kabel, dieselbe Förderhöhe, und kleine Pumpen laufen bei 2,3 m nahe am Schließpunkt. Nur als Ausfallreserve (Abschnitt 4) sinnvoll.

**Nicht belegt, bleibt offen (ehrlich):** Q bei 2,3 m als Herstellerzahl, Leistung im Arbeitspunkt, Lebensmittel-/Fischsicherheitsnachweis jeder Teichpumpe (D85). Die Empfehlung ist deshalb **nicht bau-bereit**, sondern „kaufbar nach Prüfschritt" (Abschnitt 5).

## 1. Anforderung
Je Pumpe 55 l/min (3,3 m³/h) bei 2,3 m. Hydraulische Leistung 20,7 W [E] `python -X utf8 -I -c "print(55/60*9.81*2.3)"`; der Plan sieht 82 W je Pumpe (328 W gesamt, R58). Poolboden bei 2,2 bis 2,4 m Wasser: Eintauchtiefe ≥ 2,5 m, Dauerbetrieb, Fischwasser mit Schwebstoff, 20 bis 30 °C; alles mit Wasserkontakt lebensmittelecht (D85); mindestens in Europa bestellbar (D76).

## 2. Kandidaten
Q bei 2,3 m folgt nur aus Qmax und Hmax mit drei Kurvenformen (linear = pessimistisch, Parabel, Ellipse = optimistisch); die echte Kurve einer Kreiselpumpe liegt dazwischen [A]. Keine Messwerte.
[E] `python -X utf8 -I -c "x=2.3/H;print(Q*(1-x)/60,Q*(1-x*x)/60,Q*(1-x*x)**.5/60)"` mit Q in l/h.

| Pumpe | Qmax, Hmax, Leistung bei Qmax | Q bei 2,3 m linear / Parabel / Ellipse (l/min) | Tiefe | Bezug Europa | Urteil |
|---|---|---|---|---|---|
| **Oase AquaMax Eco Premium 8000** | 8000 l/h, 4,1 m [A: Zuordnung der Hmax-Spalte im Handbuch-Text unsicher], 65 W | **58 / 91 / 110** | 4 m (Baureihe 4000 bis 20000) | Oase-Handel DE/NL | **Empfehlung**, Kurve noch zu bestätigen |
| Oase AquaMax Eco Premium 5000 (Art. 75923) | 5000 l/h, 3,5 m, 10 bis 35 W | 29 / 47 / 63 | 4 m | 384,95 € Hornbach DE; 369,99 € Olibetta; rund 345 € vijverleven.nl | Spar-Option, **unter 55 l/min möglich** |
| Oase AquaMax Eco Premium 6000 (Vorgänger) | 6000 l/h, 3,7 m, 45 bis 50 W | 38 / 61 / 78 | 4 m | laut Seite nicht lieferbar | nicht beschaffbar |
| Oase AquaMax Eco Premium 4000 (alt) | 4000 l/h, 3,3 m, 40 W | 20 / 34 / 48 | 4 m | – | zu schwach |
| **Aquaforte EC-10000** (RD744) | 10000 l/h, 4,5 m, 68 W (Händler teils 5 m, 85 W) | 82 / 123 / 143 | unbelegt | 129 € Hornbach DE | **Rückfall** |
| Jebao DCP-8000 (24 V DC) | 8000 l/h, 5,2 m, 65 W | 74 / 107 / 120 | **nur 1,5 m** (Handbuch) | NL | **ausgeschieden** (Tiefe) |
| SunSun CDF-6000 (24 V DC) | 6000 l/h, 3,8 m, 40 W | 39 / 63 / 80 | IPX8, Tiefenzahl fehlt | 120,99 € teichtip.de, ausverkauft | Tiefe unbelegt |
| Eheim compactON 5000 | 5000 l/h, 3,6 m, 70 W; nicht regelbar | 29 / 49 / 66 | unbelegt | – | unsparsam (70 W) |
| Sicce Syncra 5.0 | 5000 l/h, 3,8 m, 105 W | 31 / 52 / 69 | unbelegt | – | unsparsam |
| Oase Aquarius Universal Premium Eco 4000 | Hmax 4,4 m; 40 W bei Eco 3000 | Qmax unbelegt | 4 m | – | Qmax fehlt |

**Ausgeschieden, weil nicht sparsam:** Industrie- und Hauspumpen aus Edelstahl. Sie fahren bei 55 l/min mit 8 bis 9 m Kopf und brauchen 0,4 bis 0,8 kW [Q] Motralec/Grundfos-Datenblatt, [Q] Anglian-Pumping/Lowara-Datenblatt:
1. Grundfos Unilift AP12.40.04: 10 m Tiefe, Edelstahl, Leistung widersprüchlich (0,4 oder 0,7 kW), Kopf bei 3,3 m³/h rund 9,5 m [A]
2. Lowara Domo 7VX: 5 m Tiefe, 0,79 kW, Kopf bei 55 l/min rund 8 m [A]
3. Pedrollo VXm 10/35, Wilo Drain TSW 32/11-A: 0,6 bis 0,75 kW
Hydraulisch wären das 20,7 W aus 400 bis 700 W, also unter 5 % Gesamtwirkungsgrad; ein Faktor 5 bis 10 über dem Plan (82 W) und gegen die Designregel „Physik vor Strom". Die Grundfos-Tiefe und die Edelstahl-Werkstoffe sprechen für D85, aber nicht für den Stromplan.

Aquakultur-Hersteller: kein Treffer für etwa 3 m³/h bei 2,3 m mit Fisch- oder Lebensmittelnachweis; belegt sind nur Großanlagen (Sulzer-Fallstudie, Propellerpumpen AISI 316) und Aquarienpumpen (JBL ProFlow u800+, TÜV-geprüft, aber 800 l/h) [Q-Treffer]. Keine Aquaponik-spezifischen Pumpenberichte gefunden.

## 3. Leistung im Arbeitspunkt (Obergrenze, keine Messung)
Bei Radialpumpen sinkt die Leistung, wenn man von Qmax Richtung kleineren Durchfluss drosselt [A, Kreiselpumpen-Grundlage]. Die Nennleistung bei Qmax ist damit eine Obergrenze: Eco Premium 8000 höchstens 65 W, vier Stück 260 W, unter dem Plan von 328 W. Eco Premium 5000: höchstens 35 W, vier Stück 140 W. Ein Messwert im Arbeitspunkt liegt bei keinem Modell vor.

## 4. Zwei kleinere Pumpen je Linie?
1. **Durchfluss:** Parallelpumpen addieren bei gleicher Förderhöhe; zwei Pumpen mit je 27,5 l/min bei 2,3 m. Das wäre z. B. die Eco Premium 4000 (20 bis 48 l/min je Pumpe, Kurvenform entscheidet), also kein belegter Vorteil.
2. **Leistung:** Eine Pumpe mit Hmax 3,3 m arbeitet bei 2,3 m bei 70 % ihrer Hmax, im steilen Teil der Kurve mit schlechtem Wirkungsgrad. Hydraulisch 10,3 W je Pumpe [E] `python -X utf8 -I -c "print(27.5/60*9.81*2.3)"`. Ein Gewinn gegenüber einer größeren, gedrosselten Pumpe ist ohne Kennlinie nicht belegbar.
3. **Kosten und Aufwand:** 8 statt 4 Pumpen, 8 Kabel, 8 Siebkörbe, 8 Wartungspunkte (rund 8 × 345 € bei Eco Premium 5000-Klasse, Händlerpreis).
4. **Nutzen:** Ausfallsicherheit (eine Pumpe fällt aus, die Linie läuft mit halber Menge). Das ist ein Betriebsargument, kein Energieargument; Entscheidung bei Ben (Abschnitt 6).

## 5. Prüfschritte vor dem Kauf (ICH, nicht gekauft)
1. **Kennlinie holen:** Oase-Kennlinienbild der Eco Premium 8000 und 5000 per Browser-Pane oder Oase-Support (die Oase-Seiten blocken automatisierte Abrufe). Ablesen: Q bei 2,3 m und P bei diesem Punkt. Ziel: ≥ 55 l/min.
2. **Tiefe bestätigen:** Typenschild-Angabe „wasserdicht bis 4 m" stammt aus dem Handbuch der Baureihe von 2013 und aus der Eco-Premium-5000-Anleitung (zwei Handbücher desselben Herstellers); Herstellerbestätigung für die 8000 einholen.
3. **D85-Nachweis:** Oase nach Werkstoffliste mit Wasserkontakt und Konformität (EU 1935/2004, KTW) fragen. Die Händlerseiten nennen nur „Kunststoff"; ein Nachweis fehlt bei jeder Teichpumpe.
4. **Zweite Quelle** für Hmax und Leistung der Eco Premium 8000 beschaffen (Händlerseite mit Datenblatt, nicht nur das Handbuch).

## 6. Entscheidungsfragen
1. **E1, D85 (strenge Lesart):** Reicht Bens „lebensmittelecht" als Herstellerauskunft (Oase, schriftlich), oder muss ein Zertifikat vorliegen? Ohne Zertifikat erfüllt **keine** Teichpumpe D85 belegt; dann bleibt nur die Edelstahl-Industriepumpe mit 5- bis 10-fachem Stromverbrauch. Empfehlung: schriftliche Herstellerauskunft genügt, wenn Oase sie gibt.
2. **E2, acht kleine statt vier mittlere Pumpen:** nur wenn Ausfallsicherheit je Linie gewünscht ist. Empfehlung: nein.

## Abweichungen zu R58
| R58 ZR1 | R59 | Entscheidung |
|---|---|---|
| Bestes Zwischenergebnis Aquaforte EC-10000 / Jebao DCP-8000 | Jebao DCP-8000 nur 1,5 m Tiefe laut Handbuch (maritex.eu) | Jebao ausgeschieden |
| Oase Eco Premium 5000 „je nach Näherung unter oder über dem Ziel" | bestätigt (29 bis 63 l/min); Eco Premium 8000 trägt auch linear | 8000 als Empfehlung |
| Eintauchtiefe für keinen Kandidaten belegt | Oase Eco Premium Baureihe 4 m (Handbuch) | Aquaforte weiter unbelegt |

## Quellen
- Oase Handbuch AquaMax Eco Premium 4000 bis 20000, technische Daten (Leistung, Qmax, Hmax-Spalte, Eintauchtiefe 4 m) [Q]: `cdn.oase-teichbau.de/product/d2b3cd/gebrauchsanleitung-oase-aquamax-eco-premium-filterpumpe-bachlaufpumpe/bedienungsanleitung-oase-aquamax-eco-premium-4000.pdf`
- Oase AquaMax Eco Premium 5000, Handbuch Seite 41 (Tiefe 4 m, IP68) [Q-Treffer]: `manualslib.mx/manual/851868/Oase-Aquamax-Eco-Premium-5000.html?page=41`
- Hornbach, Eco Premium 5000 (5000 l/h, 3,5 m, 10 bis 35 W, 384,95 €) [Q]: `hornbach.de/p/oase-aquamax-eco-premium-5000/12714129/`
- Oase-Teichbau, Eco Premium 6000 (Daten, nicht lieferbar) [Q]: `oase-teichbau.de/oase-aquamax-eco-premium-6000`
- Olibetta und vijverleven.nl (Preise Eco Premium 5000) [Q-Treffer]: `olibetta.com/oase/aquamax-eco-premium?sai=18439`, `vijverleven.nl/en/products/oase-aquamax-eco-premium-5000-vijverpomp`
- Aquaforte EC-Serie (68 W, 4,5 m, kupferfrei, „fisch- und pflanzensicher") [Q]: `aqua-forte.com/products/pond-and-swimming-pond-pumps/energy-efficient-pond-pumps/ec-6500-p`, Händler-Gegenwert Hornbach `hornbach.de/p/aquaforte-ec-10000-teichpumpe/12355610/`
- Jebao DCP, Handbuch (Wassertiefe 1,5 m) [Q]: `static.maritex.eu/file/display/EHgU1ZkcM52M7bgTa61sXdFGhfFpQD6V/Jebao_DCP_Instrukcja_PL_EN.pdf`
- SunSun CDF-6000: `teichtip.de/sunsun-cdf-6000-teichpumpe-24v-dc-6000-l-h-40-w-bachlaufpumpe-mit-integriertem-blockier-und-trockenlaufschutz-gartenteichpumpe-gleichstrompumpe/52019`, `service.wiltec.de/manuals/52/52019/EN/52019-doc-en.pdf`
- Eheim compactON 5000: `eheim.com/en_GB/aquatics/technology/pumps/compacton/compacton-5000`
- Sicce Syncra 5.0: `warehouse-aquatics.co.uk/sicce-syncra-5-0-5000lph-aquarium-pump.html`
- Grundfos Unilift AP12 [Q]: `motralec.com/public/fichiers/docs/Grundfos_AP_12.pdf`; zweite Quelle [Q-Treffer]: `digitalassets.reecegroup.com.au/m/bc1c8f9bb6e34067/original/Flyer-Grundfos-UNILIFT-AP12.pdf`
- Lowara Domo [Q]: `anglianpumping.com/app/uploads/2023/03/Lowara-Domo.pdf`; zweite Quelle [Q-Treffer]: `pumpsukltd.com/manufacturers/lowara-pumps/lowara-domo-pumps.html`
- Pedrollo VX [Q-Treffer]: `pedrollo.com/public/allegati/VX_DE_50Hz.pdf`
- Kupfer/Messing für Fische [Q-Treffer]: `247garden.com/blog/2025/07/26/why-brass-fittings-dont-belong-in-your-aquarium`, `houzz.com/discussions/1582635/copper-fountain-and-pond-life`

**Konfidenz:** niedrig bis mittel. Die Empfehlung folgt aus Physik und Maximalwerten, nicht aus einer Herstellerkennlinie; die Hmax-Zuordnung der Eco Premium 8000 ist [A]. Lebensmitteleignung: nicht belegt.

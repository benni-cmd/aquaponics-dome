# Änderungsprotokoll Netzliste (R40, Version 2, 31.10.2026)

Netzliste `data/leitungsnetz.json` von Version 1 (R28) auf den Modellstand gebracht: kleiner Puffer (D66, R37, T82), Drittbecken klein (T14k), Messstellen (D65, R39), Hauptstrom-Feinfilter (D55, W32), Linienteilung (D67). Prüfung: `python scripts/check_netz.py` (Schritt 6). Quelle je Zeile: R-/D-Nummer; Herkunftsbuchstabe wie in der Netzliste (Q/E/A).

## Zusammenfassung (gezählt gegen Version 1, Commit 171ef45)
- **Kanten:** 51 → 55. Technisch geändert (Ziel, Durchmesser, Durchfluss) **17**: K01, K02, K06, K13, K16, K17, K18, K22, K35, K37, K38, K39, K40, K41, K42, K43, K49. Nur Text/Höhe geändert **9**: K05, K12, K14, K15, K21, K28, K30, K31, K44. **Neu 6**: K52–K55 (Stammlösung, Eisen, Dosierleitungen), K56/K57 (Notüberlauf/Bypass Feinfilter, nur Störfall). **Entfallen 2**: K36 (Stapel), K50 (Belüftung Standwasser).
- **Knoten:** 32 → 34 (neu `puffer_messzelle`, `puffer_stammfass`, `puffer_eisen`, `aktivkohle`; entfallen `puffer_oben`, `puffer_unten`).
- **Kabel:** 8 → 23 Zeilen (7 Trunks, 7 Stichleitungs-Bündel, Alarmwähler, Blitzleuchte/Summer; `sonden_signal` entfällt).
- **Messstellen:** `data/messstellen.json` auf die neuen Knoten umgestellt (MS46–MS49, MS55, MS08, MS11, MS50; Pflichtliste); `scripts/messstellen_plan.py` besteht weiter.
- **Fragen für M10:** 7 (F1–F7, Block `fragen_m10` in der Netzliste).

## Schritt 1: Puffer klein (K35–K41, D66, R37 Befund 9, T82)
Der Stapel aus zwei IBC (Messtank oben, Vorrat unten) entfällt. Im Dom stehen die Messzelle (20 l), das Stammlösungsfass (120 l), der Eisen-Kanister (20 l) und die zwei Schlauchpumpen auf dem Stand T82. Frischwasser läuft über Aktivkohle direkt in den Pool, ohne Standvorrat.

| Element | alt | neu | Begründung / Quelle |
|---|---|---|---|
| Knoten `puffer_oben` | obere IBC, Messtank | `puffer_messzelle` (T82) | Messzelle 20 l Acryl, Messkreis 3 l/min = 6,7 min Verweilzeit; D66, R37 Befund 1 |
| Knoten `puffer_unten` | untere IBC, Vorrat/Frischwasser 2 Tage | `puffer_stammfass` (T82) | 120-l-HDPE-Fass mit Base-Stammlösung, 15–35 Tage Vorrat; R37 Befund 8 |
| Knoten `puffer_eisen` | — (neu) | Eisenchelat-Kanister 20 l | 74 g Fe alle 3 Wochen; R37 Befund 1, T82 |
| Knoten `dosierkonsole` | Bauteil `puffer_station` | Bauteil `puffer_klein` | Schlauchpumpen auf dem Regalboden T82 |
| Knoten `aktivkohle` | — (neu) | Aktivkohlefilter im Frischwasser | entfernt Chlor und Chloramin, ersetzt 2 Tage Standzeit; D66, R37 Befund 3 |
| Knoten `frischwasser` | „Chlor entweicht 2 Tage“ | Aktivkohle direkt | D66; Standort/Versorger kein offener Punkt mehr (D69) |
| Knoten `drittbecken` | Bauteil `becken_dritt` (0,94 m³) | `becken_dritt_klein` T14k, 0,4 m³ | D66, R37 Befund 10 |
| Knoten `biofilter_dritt` | ca. 85 l Bioballs | ca. 37 l Bioballs | 73 g Futter/Tag × 0,5 l/g; R37 Befund 10 |
| K35 | `verteiler_1` → `puffer_oben`, d20, 3 l/min, Förderhöhe ca. 3 m (Stapel 2,5 m) | → `puffer_messzelle`, d20, 3 l/min, Förderhöhe 1,5 m | Messpumpe 5,9 W → 2,9 W; R37 Befund 9 |
| K36 | `puffer_oben` → `puffer_unten` Schwerkraft | **entfällt** | kein Stapel |
| K37 | `puffer_unten` → `pool` d25 | `puffer_messzelle` → `pool` d25 | Ablaufstutzen d25 der Messzelle (T82-Port) |
| K38 | `dosierkonsole` → `pool`, d20, 0,4 l/min | d9 (Schlauch 6/9), 0,003 l/min | Base 4,3 l/Tag bei 100 g/l: 0,43 kg/Tag (D61, 130 g TAN/Tag); Pumpe 4,5–220 ml/min |
| K39 | `frischwasser` → `puffer_unten` d25 10 l/min | `frischwasser` → `aktivkohle` d25 10 l/min | Spitze 10 l/min beim Nachspeisen, Mittel 0,47 l/min (0,68 m³/Tag, SRAC 454) |
| K40 | `puffer_unten` → `pool` d20 0,5 l/min | `aktivkohle` → `pool` d25 10 l/min Spitze | Schwimmerventil am Pool; Spitze statt Mittel, damit d20 nicht bei 10 l/min 0,83 m/s fährt |
| K41 | `puffer_unten` → `drittbecken` d20 2 l/min | `aktivkohle` → `drittbecken` d20 2 l/min | Wasserwechsel Quarantäne aus der Frischwasserleitung; R37 Befund 9 |
| K50 | Luft → `puffer_unten` | **entfällt** | kein Standwasser, keine belüftete Vorratsstufe |
| K52 (neu) | — | `aktivkohle` → `puffer_stammfass` d25 | Ansetzen von Hand, kein Dauerfluss |
| K53 (neu) | — | `puffer_stammfass` → `dosierkonsole` d12 (Schlauch) 0,003 l/min | Entnahme Stammlösung zur Base-Pumpe; T82-Port „Entnahme“ |
| K54 (neu) | — | `puffer_eisen` → `dosierkonsole` d12 0,0004 l/min | Eisen-Pumpe saugt aus dem Kanister |
| K55 (neu) | — | `dosierkonsole` → `pool` d9 0,0004 l/min | Dosierleitung Eisen |
| Kabel `puffer_station` | 17 W | `puffer_klein` 11,5 W | R37 Befund 9: Messkreis nur 1,5 m, Umpumpen entfällt |
| `messstellen.json` | `puffer_oben`, `puffer_unten` | `puffer_messzelle`, `puffer_stammfass` (MS46–49, MS55, Pflichtliste); MS08 Text 2,8 g TAN/0,4 m³; MS49 Füllstand Stammlösung | damit `scripts/messstellen_plan.py` weiter besteht; zwei neue Einträge unter `ohne_messstelle` (`aktivkohle`, `puffer_eisen`) |


## Schritt 2: Drittbecken klein (K41–K43, K49, K44, D66, R37 Befund 10)
| Element | alt | neu | Begründung / Quelle |
|---|---|---|---|
| K42, K43 | Umlauf Biofilter 10 l/min, d25 (0,48 m/s) | 5 l/min, d25 (0,24 m/s) | TAN-Mindestdurchfluss 2,6 l/min bei 2,8 g TAN/Tag (Ziel 1,5 mg/l, Biofilter 50 %, Rechenweg R21/system_specs); 5 l/min = 2fach; 0,4 m³ in 80 min umgewälzt; R37 Befund 10 |
| K49 | Luft Drittbecken ohne Menge | 2 l/min | O2-Bedarf 0,7–1,0 g/h (2,4 kg Fisch, 80–190 mg/kg/h, R22, plus Nitrifikation 0,5 g/h) = 0,3–0,5 l/min bei 0,036 g O2/l Luft (OTE 13 %); 2 l/min als Reserve [A] |
| K44 | Luftbedarf Pool 90–180 l/min aus 1,7–3,0 kg O2/Tag | Bemerkung: nach D61 1,3–2,2 kg O2/Tag, auf R28-Ansatz zurückgerechnet 70–130 l/min; Gegenrechnung OTE 13 % gibt 25–63 l/min | Widerspruch zwischen R28-Ansatz und Gegenrechnung bleibt offen (Frage M10) |
| Kabel `geblaese_fisch` | 280 W | 204 W | UVI 0,59 W/kg × 346 kg (D61), `system-specs.json` leistung.belueftung_w |
| `messstellen.json` MS11 | Probenahmehahn K42 | Text „Umlauf zum Biofilter 37 l“ | Konsistenz |
| Hinweis | | `system-specs.json` führt `leistung.puffer_station_w` weiter mit 17 W (Standard bleibt Station 2 IBC bis zur Orchestrator-Umstellung); die Netzliste rechnet mit 11,5 W (T82) | R37, D66 |

## Schritt 3: Messstellen als Signalkabel (D65, R39 Signalweg, `data/messstellen.json`)
`sonden_signal` (3 Adern, nur Puffer) entfällt. Je Messknoten ein Trunk zur Zentrale (Schaltschrank): RS-485/Modbus RTU 4 Adern + 24 V DC 2 Adern, dazu die Stichleitungen der Sonden. Zahlen aus `python scripts/messstellen_plan.py` (zaehlen()).

| Messknoten | Messstellen | Stichleitungen | Adern der Stichleitungen | Leistung W |
|---|---|---|---|---|
| mk_kuppel | 4 | 5 | 18 | 2 |
| mk_l1 | 12 | 12 | 27 | 3 |
| mk_l2 | 12 | 12 | 27 | 3 |
| mk_pool | 10 | 14 | 25 | 3 |
| mk_puffer | 8 | 11 | 21 | 5 |
| mk_schrank | 16 | 17 | 36 | 10 |
| mk_zd | 5 | 4 | 5 | 2 |

| Element | alt | neu | Begründung / Quelle |
|---|---|---|---|
| Kabel `sonden_signal` | 3 Adern pH/EC/DO zum Messrechner | **entfällt**, ersetzt durch 7 Trunks und 7 Stichleitungs-Bündel | R39 Signalweg: Messknoten neben dem Halter, weil die Atlas-Sondenkabel kurz sind |
| Kabel Trunk je Messknoten | — | 6 Adern (4 Bus + 2 × 24 V), Länge Montage M10 | R39 signalweg, [A] Entwurf |
| Kabel `steuerung_alarm` | Platzhalter 40 W | + Alarmwähler-Eingänge 5 Adern (4 Schaltkontakte + gemeinsamer Leiter) und Blitzleuchte/Summer 2 × 2 Adern | MS67, R39 alarmwege Stufe 1 und 2 |
| `hinweis` | R28 | Version 2 mit Verweis auf dieses Protokoll | |
| Offen für M10 | | Trunk-Längen und Weg (Kabeltrasse), Spannungsabfall 24 V auf langen Strecken, Notstrom der Zentrale | nicht gerechnet |

## Schritt 4: Feinfilter im Hauptstrom, Durchmesser, Notüberlauf (K01/K02/K05/K06, K17/K18/K21/K22, K56/K57, D55, T55)
Der Feinfilter sitzt seit D55 im Hauptstrom (110 l/min je Linie, Einlauf d63, Auslauf d63), nicht mehr im Absetzer-Teilstrom (12,5 l/min). Pool-Seitenablauf und Absetzer-Klarwasser laufen durch den Filter, erst dann die zwei großen Pumpen. Geschwindigkeiten mit den PVC-PN10-Innendurchmessern der Netzliste (d50 44,0 mm, d63 55,7 mm).

| Element | alt | neu | Begründung / Quelle |
|---|---|---|---|
| K01 / K17 | Pool → Pumpe gross 1 bzw. 3, d50, 48,75 l/min | Pool → `feinfilter_1` bzw. `_2`, **d63**, 97,5 l/min (0,67 m/s) | Filterstutzen d63 (T55), Saugseite ≤ 1,0 m/s; d50 hätte 1,03 m/s bei 97,5 l/min; D55 |
| K02 / K18 | Pool → Pumpe gross 2 bzw. 4, d50, 48,75 | `feinfilter` → Pumpe gross 2 bzw. 4, d50, **55** l/min (0,60 m/s) | Auslauf d63 teilt sich auf zwei d50 (Pumpenanschluss Saugseite d50) |
| K05 / K21 | Absetzer → Feinfilter, d50, 12,5 | unverändert d50, 12,5 l/min (0,14 m/s); Text: Einlauf d63 mit T-Stück | geprüft: Tankanschluss Ø50, Schwerkraft, langsam |
| K06 / K22 | Feinfilter → Pumpe gross 1 bzw. 3, **12,5 l/min** (0,14 m/s) | **55 l/min**, d50 (0,60 m/s) | R30: Sieb sah nur 11 % des Stroms; nun 100 % (D55) |
| K56 / K57 (neu) | — | `pool` → `pumpe_gross_1` bzw. `_3`, d63, 110 l/min, **nur Störfall** (`betrieb: stoerfall`) | Notüberlauf/Bypass am Filter vorbei, Kugelhahn im Normalbetrieb zu; bei verstopftem Korb (MS14/MS15 Hoch-Schwimmer, Alarm) öffnen, damit die Pumpen nicht trockenlaufen; offene Frage des Bauteilblatts T55 |
| Knoten `feinfilter_1/2` | „Empfehlung, nicht im Modell“, Siebkorb am Biofilter-Einlauf | Bauteil `feinfilter` (T55): 0,84 m², Gewebe ≤ 100 µm, 7,9 m/h [A] | W32, D55 |
| Knoten `biofilter_1` | „Medium 0,26 m³“ | lose K1-Träger 0,47 m³ bei 67 % Füllung | D55 |
| K12, K28 (Höhe), K15, K31 (Höhe) | Rinnenende Z ca. 1300 | Rinnenunterkante Z 1000 (W33), Gefälle 1,5 % bis 45 mm | R35/D60, W33 |
| weitere d50-Kanten geprüft | K10, K13, K29, K33 d50 | unverändert (K10 1,21 m/s ≤ 1,5; die übrigen < 0,3 m/s) | Skript `check_netz.py` (Schritt 6) |

## Schritt 5: Linienteilung 12 + 7 und Höhenlagen (D67, offene Punkte R28/W32)
| Element | alt | neu | Begründung / Quelle |
|---|---|---|---|
| Knoten `nft_linie_1/2` | „Hälfte … [A]“ | 12 von 24 Tischen, 38 von 76 Rinnen je Linie, Quelle D67; Tischzuordnung Montage M10 | D67 (b) symmetrisch 12/12; 38 Rinnen je Linie = 7 Außen-/Mitteltische (4 Rinnen) + 5 Innentische (2 Rinnen): 4·7 + 2·5 = 38 (a + b + c = 12 und 4(a + b) + 2c = 38 ergibt c = 5); Zuordnung Montage; Summe 76 aus `system-specs.json` |
| Knoten `beete_linie_1/2` | „7 von 14 [A]“ | 7 von 14, Quelle D67, 54,6 l/min Mittel (234 l je Beet × 7 × 2/h) | D67, `system_specs.py` Substrat 8,2 m³ × 0,4 / 14 Beete |
| K01 / K17 `hoehe` | Pool-Seitenablauf Z ca. 450 | Vorschlag Z 340 (Überdeckung 175 mm gegen Wirbel) | Frage F2: S = d(1 + 2,3·Fr) = 171 mm bei d63 und 97,5 l/min, Fr 0,90 (Faustformel, nicht aus Quelle gelesen) [E] |
| K14 / K30 | Höhe „offen“ | Beetablauf ca. Z −100 [A] gegen Pool Z 515; Beet-Sumpf mit Pumpe nötig, Zahlen für M10 | Frage F3 |
| neuer Block `fragen_m10` | — | F1–F7 mit Zahlen | Feinfilter-Höhenlage, Seitenablauf, Beetabläufe, Luftbedarf, Signaltrassen, Aktivkohle, Biofilter-Bett |

Die Linienwerte der Netzliste (38 l/min NFT je Linie bei 1 l/min je Rinne) bleiben damit gültig; die Tischzuordnung legt die Montage fest.

### Fragen an M10 (aus `fragen_m10`)
1. **F1** Feinfilter liegt zu hoch für Schwerkraftzulauf (Einlauf 816 über Standfläche; Grube ≈ 500 mm oder Pumpe vor dem Filter).
2. **F2** Pool-Seitenablauf Z 340 statt 450 (Wirbelgefahr bei 65 mm Überdeckung).
3. **F3** Beetabläufe unter dem Pool-Spiegel: Beet-Sumpf je Linie mit Pumpe (≈ 36 W, 36 l/min gestaffelt).
4. **F4** Luftbedarf Pool: 25–63 gegen 70–130 l/min.
5. **F5** Trunk-Längen, 24-V-Abfall, Notstrom der Zentrale.
6. **F6** Aktivkohle: Fabrikat, Kontaktzeit.
7. **F7** Biofilter-Bett 67 % gegen 68–75 % im Modell.

## Schritt 6: Selbsttest `scripts/check_netz.py`
Neues Prüfskript (Standardbibliothek, ändert nichts, Exit 1 bei Fehler): IDs und Endknoten, Durchflussbilanz je Knoten (Störfallkanten ausgenommen, Nachspeisen mit Mittelwert), Geschwindigkeit aus dem PVC-PN10-Innendurchmesser gegen den eingetragenen Wert und die Grenzen (Druckseite ≤ 1,5, Saugseite ≤ 1,0 m/s), Linienwerte, Kabelleistungen gegen `data/system-specs.json`, 7 Trunks, Fragen für M10. Der erste Lauf fand drei Bilanzfehler aus R28, die damit korrigiert sind:

| Element | alt | neu | Begründung / Quelle |
|---|---|---|---|
| K13 | Bypass Linie 1 17,5 l/min | 14,5 l/min (v 0,16 m/s) | Verteiler 1 gibt zusätzlich den Messkreis K35 (3 l/min) ab: 110 − 54,5 − 38 − 3 = 14,5; Linie 2 bleibt 17,5 (K29) |
| K16 | Sammelrinne 1 → Pool 110 l/min | 102 l/min (v 0,22 m/s) | Rücklauf 1 erhält 107 l/min (14,5 + 54,5 + 38) und gibt 5 l/min an das Zweitbecken (K33) ab; K34 bringt sie zurück in den Pool |
| K39, K40 | nur Spitze 10 l/min | zusätzlich `mittel_l_min` 0,47 | Bilanz des Pools mit dem Tagesmittel (0,68 m³/Tag); Dimensionierung bleibt an der Spitze |
| K41 | | Bemerkung: Ablauf des Wechselwassers (Überlauf zum Abwasser/Pool) offen | Quarantäne-Wasserwechsel braucht einen Ablauf |
| `bilanz_je_linie_l_min` | Bypass 17,5 | Bypass 17,5 (Linie 2), 14,5 (Linie 1 mit Messkreis), Messkreis 3 | s. K13 |
| Prüfung | — | `check_netz.py` PASS | Poolbilanz: Abfluss 220 l/min (2 × 97,5 + 2 × 12,5), Zufluss 220,5 (102 + 110 + 5 + 3 + 0,47 + Dosierung) |

## Version 3 (R45, 01.11.2026, Orchestrator)

| Stelle | vorher | nachher | Grund |
|---|---|---|---|
| K01, K17 | d63 | d75 (Stutzen bleiben d63, Reduziermuffe) | E14: Heber-Reserve, R45 Abschnitt 2 |
| Knoten `schlammsammler` | Platzhalter | `schlammfass_1`, `schlammfass_2` (Fass 200-220 l in Grube) | E12 Standardannahme, R45 Abschnitt 0 |
| K07, K23 | 0,5 l/min, nach schlammsammler | 0,01 l/min Wochenmittel, 30 l je Spuelung, 0,7 m, 5 % Gefaelle, nach schlammfass | 0,5 l/min ergab 720 l/Tag gegen 11-14 l/Tag |
| K14, K30 | d40, nach ruecklauf | d50, nach `beet_sumpf_1/2`, Spitze 54 l/min | R45 Abschnitt 1 |
| neu K58, K59, Knoten `beet_sumpf_1/2` | - | Foerderleitung d40, 54,5 l/min Mittel, Pumpe 60 W, Sumpf 500 l | R45 Abschnitt 3 (statt 300 l / 36 W) |
| K39, K40 | 10 l/min | 4 l/min begrenzt (Mittel 0,47 unveraendert) | R45 Abschnitt 5 |
| K44 | 120 l/min, Widerspruch offen | 130 l/min, Spitze 205, Widerspruch geloest | R45 Abschnitt 4 |
| K12, K28 | nur Bemerkung | Auslegung 1 l/min je Rinne, Betrieb 0,5 (19 l/min) vermerkt | L24, R06 |
| Pruefung | - | `check_netz.py` PASS (57 Kanten) | |

# Pruefung M10-UMBAU (Runde 71) und M10-S5-LUFT Teil A — Befund

Pruefer: frische Sitzung, hat nichts davon gebaut. 05.11.2026. Start-Auftrag `docs/jobs/start/M10-UMBAU-LUFT-pruefer.md` (8e27b6b). Gegenstand: Build e881f56 und Vorlaeufer 45af03b, e71e9dd; Blatt `docs/jobs/M10-UMBAU.md` Pruefpunkte 1 bis 5 gegen `docs/leitungsordnung.md` R1 bis R9; Blatt `docs/jobs/M10-S5-LUFT.md` Teil A Pruefpunkte 1 bis 5; Maengel M03 bis M10 aus `docs/model-maengel.md`.
Nur diese Befund-Datei geschrieben. Schwere Laeufe (Viewer-Export, `check_latte 71`) in einer Scratchpad-Kopie (`git archive HEAD` plus `scripts/dome-script.json`), freier RAM vorher 19,7 GB. Alle Befehle aus `user-projects/aquaponics-dome`.

## Urteil (Stand Runde 71, Erstpruefung)

**Neues Urteil nach Nachpruefung Runde 73: PASS mit Auflagen** (Abschnitt "Nachpruefung Runde 73" am Ende). Der Text dazwischen ist der Erstbefund und bleibt als Beleg stehen.

| Blatt / Teil | Urteil | Begruendung |
|---|---|---|
| M10-UMBAU Pruefpunkte 1 bis 5 | **FAIL gegen den Wortlaut, erwarteter Teilstand** | Montage hat nur Schritte 1 bis 3 (Linie 1) gebaut; Linie 2, Schlammfass K07/K23, Verteiler K10/K26, Luft K44, M09, Halter (Schritte 4 bis 9) sind laut Paket Abschnitt 14b offen. Alle fuenf Pruefpunkte verfehlen ihr Soll |
| M10-UMBAU Teilziel Linie 1 | **PASS mit Auflagen** | Montage-Zahlen reproduziert (R1/R2/R3/R5/R7/R8 fuer Linie 1 ohne Verstoss), Heber unveraendert, Gang-Pruefung PASS; offen Halter (R6), K05-Gefaelle, K08-Kasten, Heber-Reserve |
| M10-S5-LUFT Teil A | **PASS mit Auflagen** | Instanzen, Lagen, Ebenen im Soll; zwei Soll-Zeilen nicht belegbar (Rohrenden-Fluchtung, `check_leitungen` 0) |
| Behauptung "Luft Teil A durch den Umbau veraendert" | **nicht belegt** | e881f56 aendert keine `lt_rohr_d25`-Datei und keine K44-Trasse (siehe Teil A, Zeile 3) |

## M10-UMBAU: Messung je Pruefpunkt

| Nr | Pruefpunkt | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|---|
| 1 | Leitungsordnung | `python -X utf8 scripts/check_leitungsordnung.py` (Exit 1) | R1 33 Verstoesse, R2 0, R3 0, R4 1 (K18), R5 0, R6 17, R7 0, R8 0, R9 9 (T15, K24, K25, K26); schraege Rohre 54 (vorher 74), Boegen 80, Halter-Instanzen 0, waagerechte Richtungen 4; R10 meldet 36 Kanten ohne Trasse (K07, K23 inklusive) | R1 bis R9 0; R10 genau 34 | FAIL (Verstoesse liegen in Linie 2 und Luft; aus Linie 1 nennt die Ausgabe nur K08 R6; die Liste je Regel ist gekuerzt) |
| 2a | Rohrenden ins Leere | `python -I -X utf8 renders/maengel/inventur.py <Kopie> <aus.json>` auf dem neuen Export (Kopie, 4922 Instanzen, `viewer/export_model.py` Exit 0, 2311 s) | `frei_ins_leere` 1 (`LT_Rohr_d50_L481:1` bei -127/-4338/1970 = K26); vorher 2 | 0 | FAIL, halb behoben (K10 Linie 1 ist angeschlossen) |
| 2b | Tank-Anschluesse | dieselbe Inventur, Schluessel `tank_anschluesse` | Abstand Schlamm- und Ablaufstutzen zum naechsten Leitungsteil 293, 295, 315, 315, 349, 369, 372, 383 mm; vorher 290 bis 379 mm | <= 25 mm | FAIL (Schlammfass fehlt) |
| 3 | Heber | `python -X utf8 scripts/r45_heber.py` | K01 Laenge 1322 + 1754 = 3076 mm, 4 Boegen; K17 1078 + 1137 = 2216 mm, 4 Boegen; Reserve "GEBAUT, schlechter Fall": K01 **65 mm**, K17 **68 mm** | Reserve K01 >= 85 und K17 >= 88; Laenge <= 3076 / 2216 | Laenge PASS, Reserve FAIL (war vor dem Umbau gleich: 38d2300 nennt 65/68) |
| 4a | Leitungen | `python -X utf8 scripts/check_leitungen.py` (Exit 1) | 2 Verstoesse: KOLL K08 (Rohr d40 trifft `Tank_gross:1`, etwa 360 mm Achslaenge), GEFAELLE K05 (Teilstueck 6 steigt um 250 mm gegen die Fliessrichtung); EINGABE, BAND, GANG 0; Kanten mit Trasse 21 von 57 | 0 | FAIL |
| 4b | Gaenge | `python -X utf8 scripts/check_walkways.py` (Exit 0) | A 700, B 600, Wandluft 110, Nachbarportale 307, Tuer-Gang 3177 mm | A >= 700 (Blatt) bzw. >= 600, B >= 600, Wandluft >= 110 | PASS |
| 5 | Instanzen | eigenes Zaehlskript (`script_zaehlen.py`, Scratchpad, `python -X utf8 -I`) ueber `scripts/dome-script.json`: `component.insert_design` plus `occurrence.copy` je Entwurf | `schlammfass`, `lt_kugelhahn_feder_d40`, `lt_verteiler_d50`: **keine Instanz** | je 2 | FAIL (Schritte 5 und 6 nicht gebaut) |
| 5b | Gerade je Stamm >= 262 mm mit >= 100 mm Luft | nicht gemessen (Stamm-Umbau Linie 2 fehlt, Paket nennt keinen Messwert) | | | nicht belegt |
| — | `check_latte.py 71` | `python -X utf8 scripts/check_latte.py 71` in der Kopie, Laufzeit rund 2 h (parallel zum Export), Exit 1 | 29 PASS, 2 FAIL (beide Kollision): Kollisionen 94 (Soll 0; Runde 69: 115 Altbestand), Vollstaendigkeit 70 Paare ungeprueft. Aufschluesselung 94: 51 Bogen, 11 Reduzierung, 10 Rohr, 5 Saugstutzen, 3 Kupplung, 4 mit Montagetafel, 7 mit `Strebe_` (Tank-Rahmenstreben, B1), 0 mit `T1_Strebe`, 12 Leitungsteil gegen Leitungsteil. Offen gezaehlt: W-M1 49, M2b 504, Teil-A gewollt 45; exakt geprueft 2378 Paare | PASS ohne Kollision | FAIL, besser als Runde 69 (115 auf 94) |
| — | Tuer, Hoehe Kuppel | gleiche Ausgabe | `Tuer_Komplett` 1 Instanz, 27 Koerper; Kuppelhoehe 5937 (Soll 6000); Strebenzahl 64; Pool zentriert 0 mm | im Soll | PASS |

## Maengel M03 bis M10: welche sind behoben

Grundlage: Inventur auf dem Runde-71-Export (`inventur.py`) und `check_leitungsordnung.py`. Vorher-Werte aus `docs/model-maengel.md`.

| Mangel | Gegenstand | Befund Runde 71 | Behoben? |
|---|---|---|---|
| M03 | Schlammablass endet blind | Abstand 293 bis 383 mm (vorher 290 bis 379) | nein |
| M04 | kein Halter | `halter_leitung_instanzen` 0; R6 17 Rohre ohne Halter | nein |
| M05 | wirre Verlegung | schraege Rohre 54 (vorher 74), Boegen 80 (vorher 79), waagerechte Richtungen 4; Linie 1 ordentlich, Linie 2 und Luft nicht | teilweise |
| M06 | Bogenketten | Inventur `bogenketten_ab3` 3 (vorher 4); Leitungsordnung R4 1 (K18) | teilweise |
| M07 | Luft K44 im Poolvolumen | K44-Trasse unveraendert (Z -1237 bis 1180, 6 Punkte, `data/leitungstrassen.json`); Schritt 7 nicht gebaut | nein |
| M08 | Ueberlauf K10/K26 frei | `frei_ins_leere` 1 (K26); K10 angeschlossen, Verteiler fehlt weiter | teilweise (K10) |
| M09 | Rohr d75 im Tisch-Kasten | nicht neu gemessen; Schritt 8 offen | nicht belegt |
| M10 | Bogenkette d25 am Tisch | nicht neu gemessen; Schritt 8 offen | nicht belegt |

## M10-S5-LUFT Teil A: Messung je Pruefpunkt

| Nr | Pruefpunkt | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|---|
| 1 | Verteiler und Scheiben | Zaehlskript ueber `scripts/dome-script.json`; Bauteil-Eval `solidcraft-cli.exe eval designs/components/luft_scheibenbelueftung.sc` | `luftverteiler_4` 1, `luft_scheibenbelueftung` 4; Scheibenmitten bei (+-707,1 / +-707,1), also 1000 mm von der Beckenmitte; Scheibe Ursprung Z -1205, Membran-Oberkante Z -1089 (Stapelhoehe 116) | 1 und 4; Abstand < 1810; Membran unter dem Spiegel | PASS |
| 2 | Schwimmerventil | gleiche Skriptmatrix; `eval schwimmerventil_pool.sc` (Hebelarm mit Kugel Z -230 bis -26,5, Mitte -175 unter der Rohrachse); `eval pool_zentral.sc` (`T5_Wasser` Z -1305 bis 915) | Port A bei Z 1110 (= 710 plus Flur-Offset 400), Spiegel 915 (= 515 plus 400), Kugelmitte 1110 - 175 = 935 = Spiegel + 20 | Rohrachse Z 710 und Kugelmitte Z 535 (Blatt rechnet flur-relativ) | PASS im absoluten Rahmen; das Blatt sollte den Rahmen nennen |
| 3a | Rohre d25 Verteiler zu Scheiben, Enden fluchten | nicht gemessen (Port- und Rohrendenvergleich fehlt in dieser Pruefung) | | < 1 mm | nicht belegt |
| 3b | `check_leitungen.py` 0 | siehe M10-UMBAU 4a | 2 Verstoesse (K08, K05), beide nicht Teil A | 0 | FAIL, ohne Bezug zu Teil A |
| 3c | `inspect.interference`, 0 neue Treffer | `check_latte 71` | "Teil-A gewollt" 45 (Wasserkoerper, Steckverbindung Luft d25), als gewollt gefuehrt; 0 weitere mit Luft-Bauteilen genannt | 0 neue | PASS mit Vorbehalt (45 gewollt, nicht einzeln pruefbar) |
| 4 | Variantenbefund | `grep -cE "OFFEN \(E20\)\|OFFEN \(E13\)" docs/jobs/M10-S5-LUFT.md docs/packages/m10-s5-luft.md` | 7 und 7 | >= 4 | PASS |
| 5 | nichts Fremdes veraendert | `git diff 8e27b6b~3 HEAD --stat` auf die Teil-A-Bauteile, `gen_dome.py`, `params.json`, `leitungsnetz.json`, `schaltschrank.sc` | Bauteile Teil A unveraendert; `gen_dome.py` +3/-1 (nur die Text-Schalter-Zeile aus e881f56, `d0819fe`), `schaltschrank.sc` 2 Byte (Werkstoff-Neuanwendung); `params.json`, `leitungsnetz.json` unveraendert | gleiche Hashes wie vor der Sitzung | PASS (Vorher-Hash nicht gesichert, Vergleich ueber Commits) |
| — | "Luft Teil A durch Umbau veraendert" | `git show --stat e881f56` (48 Dateien): keine `lt_rohr_d25_*`, keine `luft_*`, `luftverteiler_4`, `schwimmerventil_pool`; `data/leitungstrassen.json` +17/-10 ohne K44-Zeile | | | nicht belegt; die Teil-A-Trasse K44 bleibt, was sie war |

## Viewer-Screenshots

Eigener Port 4522 aus der Kopie, kein Export (Export war vorher beendet). Gemessen und gesehen: Kopfzeile "Kreislauf: A+", 4922 Instanzen, 179 Definitionen, 282,7 MB, Aufbau 17,0 s; Ansicht "Oben" lud ohne Fehlerzeile.
**Nicht gelungen:** Nahaufnahmen der umgebauten Strecken (Linie 1, Technikgruppe) und der Luft am Pool. Ursache: der Viewer hat keine Kamera-Funktion, die Gruppen-Haken in der Bauteilliste reagierten auf die Klicks im Browser-Pane nicht zuverlaessig (Pane-Rahmen 800 x 600 gegen emuliert 1600 x 900), Leitungen liegen unter Huelle, Pflanzen, Beeten. Gegen `docs/ui-standard.md` daher **nicht belegt**.

## Stichproben ausserhalb der Pruefpunkte

1. **Zahl aus der Meldung gegen Datei:** Montage meldet "check_leitungen 2 Verstoesse (K08 im Grobkasten, K05-Gefaelle)" und "check_latte Runde 69: 115 KOLL Altbestand": gemessen 2 (K08, K05) und 94 KOLL (Runde 71). PASS.
2. **Teil gegen sein Blatt:** Paket 14b nennt R1 33, R4 1, R6 17, R9 9, schraege Rohre 54: gemessen identisch. PASS.
3. **Commit gegen Diff:** `git show --stat e881f56`: nur Trassen-Daten, `gen_dome.py` (+1), `leitungen.py`, `trassen_linie.py`, 38 neue `lt_rohr_*`-Entwuerfe, Werkstoff-Neuschreibungen, `dome.sc`, Bilder `round-71/section-71`. Nichts Fremdes. PASS.

## Behauptungen, die sich nicht belegen lassen

1. "Luft Teil A durch den Umbau veraendert" (Auftrag): im Diff von e881f56 nicht zu finden.
2. "R6 6 Rohre ohne Halter in Linie 1" (Paket): die Ausgabe von `check_leitungsordnung.py` zeigt je Regel nur gekuerzte Listen; die Aufteilung nach Linie ist nicht nachgemessen.
3. Strebe-/Tuer-Nahaufnahmen und umgebaute Strecken im Bild: nicht herstellbar (siehe oben).
4. Rohrenden-Fluchtung Teil A (< 1 mm): nicht gemessen.

## Auflagen

| Nr | Auflage | Owner |
|---|---|---|
| A1 | Umbau-Schritte 4 bis 9 abarbeiten (Linie 2, Schlammfass K07/K23, Verteiler K10/K26, Luft K44, M09, Halter); danach diese Pruefung fuer das ganze Blatt wiederholen. Bis dahin kein "M10-UMBAU fertig" melden | ICH (Montage, naechste Runde) |
| A2 | Heber-Reserve K01 65 und K17 68 mm gegen Soll 85/88: Blatt-Soll oder Heber aendern (B3 des Pakets, vom Umbau unabhaengig); Entscheidung ueber Langbogen 0,2 oder tiefere Filtergrube (r45_heber: +99 bis +164 mm) | DEINE ENTSCHEIDUNG (Ben), Empfehlung: Variante mit Langbogen, weil sie die Laenge nicht aendert |
| A3 | K05-Gefaelle (Befund B2 des Pakets): Band U um 5 mm erweitern und K05 von oben fuehren, oder Tiefpunkt hinnehmen | DEINE ENTSCHEIDUNG (Ben), Empfehlung (a) wie im Paket |
| A4 | Kollisionen 94: davon 7 mit Tank-Rahmenstreben (B1: Pumpe 20 mm nach innen oder Strebe aendern), 12 Leitungsteil gegen Leitungsteil, 4 gegen Montagetafel einzeln aufloesen; `check_latte` Soll 0 | ICH (Werkstatt Pumpentafel, Montage) |
| A5 | `check_leitungen.py` K08: Grobkasten-Pruefung gegen Koerperpruefung abgleichen (Montage nennt "frei"), Pruefskript auf Koerpergeometrie umstellen oder Kasten verkleinern | ICH (Montage) |
| A6 | Viewer: Kamera-Hilfe (`window.setzeKamera(pos, ziel)`) oder Ansicht "Technikgruppe"/"Pool-Luft" einbauen, damit Screenshots der Leitungen moeglich werden; Haken-Klicks im Pane pruefen | ICH (Viewer-Werkstatt) |
| A7 | `check_latte.py` braucht rund 2 h bei gleichzeitigem Export (Nachtmodus D82): als Hintergrundlauf mit Ausgabedatei und Ende-Marke fuehren, nicht im Vordergrund | ICH (Orchestrator) |
| A8 | Blatt M10-S5-LUFT Pruefpunkt 2: Rahmen nennen (flur-relativ 710/535 gegen absolut 1110/935) | ICH (Planer) |
| A9 | Pruefer-Vorlage: Laenge von `check_latte` und `export_model.py` als Warnung aufnehmen (zusammen 2 h bis 2,5 h, 12 GB RAM) | ICH (Orchestrator) |

## Abschluss

Geprueft gegen: `check_leitungsordnung.py`, `check_leitungen.py`, `check_walkways.py`, `r45_heber.py`, `renders/maengel/inventur.py` auf neuem Export, `check_latte.py 71` in der Kopie (29/31, 94 KOLL), Zaehlskript ueber `scripts/dome-script.json`, Bauteil-Evals (Scheibe, Schwimmerventil, Pool), `git show --stat e881f56`, `git diff` der Guard-Dateien, Paket 14b.
Offen: A1 bis A9 (siehe oben); Screenshots der umgebauten Strecken und der Luft am Pool nicht belegt.


## Nachpruefung Runde 73 (Pruefer, 05.11.2026)

Gegenstand: Build Runde 72 (c8be3f4) und Runde 73 (ab3d425), Folge-Commits d1e415d und 6f0bdd0; Start-Auftrag `docs/jobs/start/M10-UMBAU-LUFT-pruefer.md` (Wiederanlauf). Alle Messungen in dieser Sitzung neu, in einer Kopie des Stands 6f0bdd0 (`git archive 6f0bdd0` im Scratchpad, `scripts/dome-script.json` per `gen_dome.py 5` neu erzeugt: 10400 Befehle, gleich der Montage-Zahl). Schwere Laeufe (Viewer-Export, `check_latte`) liefen nur in der Kopie, freier RAM vorher 22 GB. Der Arbeitsbaum des Repos blieb unberuehrt; geschrieben ist nur diese Datei. Ich habe nichts davon gebaut.

### Urteil: PASS mit Auflagen (Teilziel erreicht, Blatt nicht voll)

M10-UMBAU ist gegenueber Runde 71 deutlich weiter: R1 und R6 sind 0, `frei_ins_leere` 0, alle vier Ablaufstutzen 0 mm, die Instanzen stehen im Soll, Laufwege PASS. Nicht erfuellt nach Wortlaut des Blatts bleiben der Schlammstutzen-Abstand (49 bis 54 mm gegen <= 25), Heber-Reserve, `check_leitungen` (3 Verstoesse), R4 K20, R9 K24-K25 und `check_latte` (86 Kollisionen, davon 3 neu am Verteiler und an der Klemme d50). Pruefpunkt 5 Stamm-Gerade Linie 1 meldet die Montage selbst als nicht erfuellt.

### Messung je Pruefpunkt (Blatt M10-UMBAU)

| Nr | Pruefpunkt | Befehl | Messwert | Soll | Ergebnis |
|---|---|---|---|---|---|
| 1 | Leitungsordnung | `python -X utf8 scripts/check_leitungsordnung.py` (Exit 1) | R1 0, R2 0, R3 0, R4 **1** (3 Boegen K20 bei 928/-3636/718), R5 0, R6 0, R7 0, R8 0, R9 **1** (K24-K25-Stamm Rohr d50 bei -1018/-3942/1443 frei im Gang; ohne `viewer/instances.json` nur "nicht messbar", mit dem neuen Export gemessen); R10 34 Kanten ohne Trasse (K11 bis K16, K27 bis K35, K37 bis K43, K45 bis K49, K51 bis K55, K58, K59); schraege Rohre 21, Boegen 95, Halter 14 | R1 bis R9 0; R10 genau 34 | R1, R2, R3, R5, R6, R7, R8 PASS; R10 PASS (34); R4 und R9 FAIL (je 1) |
| 2a | Rohrenden ins Leere | `python -I -X utf8 renders/maengel/inventur.py . <aus.json>` auf dem neuen Export (`viewer/export_model.py`, Exit 0, "export 2287s defs=195 instanzen=4988") | `frei_ins_leere` **0**; `rohrenden_gesamt` 86, davon 86 an Leitungsteil (vorher 1 frei) | 0 | PASS |
| 2b | Tank-Anschluesse | gleiche Inventur, Schluessel `tank_anschluesse` | Ablaufstutzen aller vier Tanks **0 mm** (Kugelhahn Feder d40 bzw. Kugelhahn d50); Schlammstutzen **54, 54, 49, 49 mm** zum naechsten Leitungsteil (Hahn); Zulauf 62 bis 64 mm (nicht im Soll) | Schlamm/Ablauf aller vier Tanks <= 25 mm | Ablauf PASS; Schlamm nach Wortlaut FAIL. Die Montage deutet den Schlammstutzen als tankeigenen inneren Stutzen zum Hahn, "kein Leitungsanschluss"; das ist plausibel, steht aber nicht im Blatt (Auflage A10) |
| 3 | Heber | `python -X utf8 scripts/r45_heber.py` | K01 1322 + 1754 = 3076 mm, 4 Boegen; K17 1078 + 1137 = 2216 mm, 4 Boegen; Reserve gebaut, schlechter Fall: K01 **65 mm**, K17 **68 mm** | Reserve >= 85 / >= 88; Laenge <= 3076 / 2216 | Laenge PASS; Reserve FAIL (unveraendert seit Bestand) |
| 4a | Leitungen | `python -X utf8 scripts/check_leitungen.py` (Exit 1) | **3** Verstoesse: KOLL K08 (Rohr d40 trifft `Tank_gross:1`, etwa 360 mm), GEFAELLE K05 (Teilstueck 6 steigt 250 mm) und K21 (Teilstueck 5 steigt 239 mm); EINGABE, BAND, GANG 0; Kanten mit Trasse 23 von 57 | 0 | FAIL (gleich Montage-Zahl; vorher 2) |
| 4b | Gaenge | `python -X utf8 scripts/check_walkways.py` (Exit 0) | A 700, B 600, Wandluft 110, Nachbarportale 307, Tuer-Gang 3177 | A >= 700, B >= 600, Wandluft >= 110 | PASS |
| 5a | Instanzen | Zaehlung der `occurrence.move` je Namen ueber `scripts/dome-script.json` (Skript im Scratchpad) | `Schlammfass` 2, `LT_Kugelhahn_Feder_d40` 2, `LT_Verteiler_d50` 2; dazu `LT_Kappe_d20` 2, `LT_Kappe_d50` 4, `LT_Klemme_d32` 4, `LT_Klemme_d40` 4, `LT_Klemme_d50` 6 (Halter 14, gleich Inventur) | je 2 | PASS |
| 5b | Gerade je Stamm >= 262 mm mit >= 100 mm Luft | nicht nachgemessen; Montage-Angabe (Paket 14b): Linie 2 K22-T-b 164 mm, Linie 1 hoechstens 67 mm | >= 100 mm | Linie 1 nach Montage selbst FAIL; Linie 2 nicht belegt |

### Weitere Messungen

1. `python -X utf8 scripts/check_latte.py 73` in der Kopie, Laufzeit rund 3 h wegen Parallellauf des Exports, Exit 1: 29 PASS, 2 FAIL (Kollisionen **86**, Soll 0; Vollstaendigkeit **64** Paare ungeprueft). Vorher: Runde 71 94, Runde 69 115. Aufschluesselung der 86: 41 Bogen, 16 Rohr, 8 Kupplung, 7 Reduzierung, 5 Druckstutzen, 4 Saugstutzen, 2 Einlaufrohr, 2 Klemmenring, 1 T10_Zulaufrohr; 11 mit Tank-Rahmenstreben (`Strebe_`), 0 mit `T1_Strebe`. Offen gezaehlt: W-M1 49, M2b 504, "Teil-A gewollt" 47; exakt geprueft 2555 Paare, "EXAKT Erde 617 Paare, Fundamentring offen 0".
2. **Neu gegenueber Runde 69 (Normalisierung der Zeilen, `Counter`-Differenz):** `Rohr x Verteiler` 1, `Klemmenring x Rohr` 2 (Klemme d50 auf `LT_Rohr_d50_L162`, beide am neuen Verteiler), dazu mehrere Leitung-gegen-Tank-Zeilen (Bogen/Rohr x `Tank`, `Biomedium`, `Stuetzrippe_5`, `Diagonale_4`, `Bein_3`); die Tank-Zeilen gehoeren zu K08 (Rohr d40 im Grobkasten von `Tank_gross:1`, gleiche Stelle wie `check_leitungen`). Weggefallen sind 29 Bogen x Rohr, 11 Reduzierung x Rohr, 5 Rohr x T-Stueck, 7 Montagetafel-Treffer und weitere (Altbestand der Linie 1 und 2 nach Neuverlegung).
3. **Luft K44 (M07):** Inventur `rohre_durch_bauteile` 6: die vier Luft-Steiger `LT_Rohr_d25_L2353` laufen weiter durch `Pool:1` (je 54 Proben) und `Tisch_innen:6` (je 18 Proben) sowie die zwei Heber-Steiger d75 durch `Tisch_mitte:4` und `:3` (je 5 Proben). Die Leitungsordnung Ausnahme 3 erlaubt Luft im Wasser, verbietet aber Durchfuehrung durch Poolwand oder Poolboden; ob die Steiger die Wand durchstossen, ist hier nicht belegt (siehe Auflage A12).
4. **Viewer-Bilder:** Die drei Montage-Bilder (`renders/m10-umbau-absetzer-fass-73.png`, `m10-umbau-poolrand-luft-73.png`, `m10-umbau-draufsicht-73.png`) habe ich angesehen: Fass in der Grube neben dem Absetzer mit durchsichtiger Erde, vier rechtwinklige Luftstraenge am Poolboden ohne Kreuzung. Es sind Montage-Aufnahmen, keine eigenen; ein eigener Viewer-Screenshot gegen `docs/ui-standard.md` wurde nicht gemacht (Kamerafunktion fehlt weiter, Auflage A6 aus dem Erstbefund).

### Maengel M03 bis M10 nach Runde 73

| Mangel | Gegenstand | Befund Runde 73 | Behoben? |
|---|---|---|---|
| M03 | Schlammablass endet blind | Ablaufstutzen 0 mm, Schlammfass 2 mit Federhahn 2, K07/K23 mit Trasse; Schlammstutzen 49 bis 54 mm zum Hahn | ja fuer den Ablass, Schlammstutzen offen (A10) |
| M04 | kein Halter | 14 Klemmen (`halter_leitung_instanzen`), R6 0; Konsole oder Staender nicht modelliert (Montage B7) | teilweise (Klemme ja, Auflager nein) |
| M05 | wirre Verlegung | schraege Rohre 21 (vorher 54, Bestand 74), Boegen 95, waagerechte Richtungen 4; alle 21 laut Montage in Ausnahme 1 und 2 | weitgehend (die 21 sind nicht einzeln nachgemessen) |
| M06 | Bogenketten | `bogenketten_ab3` 2 (beide unterirdisch an den Heber-T, d50/d63/d75, Ausnahme 1), R4 1 (K20) | teilweise |
| M07 | Luft K44 im Poolvolumen | Luft laeuft weiter im Pool (Ausnahme 3), neue Fuehrung nur X/Y am Boden; Wanddurchfuehrung offen | nicht eindeutig (A12) |
| M08 | Ueberlauf K10/K26 frei | `frei_ins_leere` 0, Verteiler 2 gesetzt; Abgaenge 1 und 2 (d40, d32) offene Zapfen bis S3 (B5) | ja (K10/K26 geschlossen), Abgaenge offen |
| M09 | Rohr d75 im Tisch-Kasten | Inventur zeigt weiter 2 Rohre mit je 5 Proben im Kasten; Montage-Abstand 609 und 492 mm zu den naechsten Tischkoerpern (Kasten hohl); `check_latte` meldet keinen Treffer Rohr d75 x Tisch | geschlossen nach `check_latte`, Montage-Abstand nicht nachgemessen |
| M10 | Bogenkette d25 am Tisch | 4 Luft-Steiger durch `Tisch_innen:6`; `bogenketten_ab3` meldet nur noch 2 Ketten (beide d50/d63/d75), also keine d25-Kette | ja (nach Inventur) |

### Stichproben

1. **Zahl aus der Meldung gegen die Messung:** Montage meldet R1 0, R6 0, R4 1, R9 1, R10 34, schraege Rohre 21, `check_leitungen` 3, Heber 65 mm, `frei_ins_leere` 0, Ablaufstutzen 0 mm, Halter 14, Instanzen 2/2/2: alle gleich gemessen. PASS.
2. **Meldung gegen Datei:** loop-state schreibt "check_walkways PASS (gleich)" und "Viewer-Export Exit 0": gemessen PASS (700/600/110/307/3177) und Export Exit 0 mit 195 Definitionen und 4988 Instanzen (Montage nennt dieselben Zahlen). PASS.
3. **Teil gegen sein Blatt:** Blatt-Pruefpunkt 2 nennt "Schlamm/Ablauf aller vier Tanks <= 25 mm"; gemessen Schlamm 49 bis 54 mm: im Paket als "innerer Stutzen" gerechtfertigt, im Blatt nicht definiert. Teilweise.
4. **Kollisionen:** Die Montage-Meldung (loop-state, Paket 14b) nennt keinen `check_latte`-Lauf fuer Runde 72 oder 73; gemessen 86, davon 3 neu am Verteiler. Dass die uebrigen 83 Altbestand sind, folgt nur aus dem Vergleich der Typen mit Runde 69.

### Nicht belegt

1. Pruefpunkt 5b (Stamm-Gerade): Linie 1 und Linie 2 nicht nachgemessen; Montage-Angaben 67 mm und 164 mm.
2. Die 21 schraegen Rohre als "Ausnahme 1 und 2": nicht einzeln gegen Heber und Ports geprueft.
3. Wanddurchfuehrung der Luft-Steiger durch Poolwand oder Poolboden.
4. Eigene Viewer-Screenshots der umgebauten Strecken.
5. Rohrenden-Fluchtung Luft Teil A (< 1 mm) und `check_leitungen` 0 fuer Teil A: wie im Erstbefund nicht gemessen; `check_leitungen` bleibt bei 3 Verstoessen ohne Bezug zu Teil A.

### Auflagen (Nachpruefung)

| Nr | Auflage | Owner |
|---|---|---|
| A10 | Blatt M10-UMBAU Pruefpunkt 2b praezisieren: Schlammstutzen (innerer Stutzen zum tankeigenen Hahn) ausnehmen oder Hahn naeher an den Stutzen legen; bis dahin "FAIL nach Wortlaut" | ICH (Planer) |
| A11 | Die 3 neuen Kollisionen am Verteiler (`Rohr x Verteiler`, `Klemmenring d50 x Rohr L162` zweimal) einzeln klaeren: Einstecktiefe der Muffe A und Klemmen-Bohrung d50 gegen Rohr-Aussen-d; entweder Bauteil oder Check (Steckverbindung als gewollt fuehren, wie bei Luft d25) anpassen | ICH (Werkstatt, Montage) |
| A12 | M07: pruefen, ob die vier Luft-Steiger Poolwand oder Poolboden durchstossen (Ausnahme 3 verbietet das); Messung per CAD (`inspect.interference` Rohr gegen `Pool:1` mit Wandkoerper) oder Trassen-Z gegen Wand | ICH (Montage) |
| A13 | Rest aus Runde 71 bleibt: Heber-Reserve 65/68 mm (A2), K05/K21-Gefaelle (A3), K08-Grobkasten (A5), R4 K20, R9 K24-K25; Halter-Konsole (B7), Kappen d40/d32 (B5), Schlammfass tiefer als im Bauteilblatt (B4) laut Paket | Entscheidungen bei Ben (A2, A3), Rest Montage/Werkstatt |
| A14 | Pruefpunkt 5b mit Befehl nachweisen (Skript der Montage ins Repo, `scripts/` oder `docs/`), damit ein Pruefer die Stamm-Gerade nachmessen kann | ICH (Montage) |
| A15 | `check_latte` auf 0 Kollisionen: 86 sind noch zu klaeren; Prioritaet die 11 Tank-Rahmenstreben (B1) und die 3 am Verteiler | ICH (Montage, Werkstatt Pumpentafel) |

Geprueft gegen: `check_leitungsordnung.py`, `check_leitungen.py`, `check_walkways.py`, `r45_heber.py`, `renders/maengel/inventur.py` auf neuem Export (Kopie), `check_latte.py 73` (Kopie, 29/31, 86 KOLL), Zaehlung ueber `scripts/dome-script.json`, Differenz der KOLL-Zeilen gegen `renders/check_latte-69.txt`, Montage-Bilder, Paket 14b, `docs/leitungsordnung.md`, `docs/model-maengel.md`.
Offen: Auflagen A10 bis A15; nicht belegt: Stamm-Gerade, Wanddurchfuehrung Luft, eigene Viewer-Screenshots.

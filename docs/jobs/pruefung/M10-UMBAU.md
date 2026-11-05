# Pruefung M10-UMBAU (Runde 71) und M10-S5-LUFT Teil A — Befund

Pruefer: frische Sitzung, hat nichts davon gebaut. 05.11.2026. Start-Auftrag `docs/jobs/start/M10-UMBAU-LUFT-pruefer.md` (8e27b6b). Gegenstand: Build e881f56 und Vorlaeufer 45af03b, e71e9dd; Blatt `docs/jobs/M10-UMBAU.md` Pruefpunkte 1 bis 5 gegen `docs/leitungsordnung.md` R1 bis R9; Blatt `docs/jobs/M10-S5-LUFT.md` Teil A Pruefpunkte 1 bis 5; Maengel M03 bis M10 aus `docs/model-maengel.md`.
Nur diese Befund-Datei geschrieben. Schwere Laeufe (Viewer-Export, `check_latte 71`) in einer Scratchpad-Kopie (`git archive HEAD` plus `scripts/dome-script.json`), freier RAM vorher 19,7 GB. Alle Befehle aus `user-projects/aquaponics-dome`.

## Urteil

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

# Pruefung M10-S5-LUFT-B (Technikgruppe aussen, Runde 74; Pruefer, 05.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md`. Gegenstand: Commit 651bc17 (Montage Runde 74), Blatt `docs/jobs/M10-S5-LUFT-B.md` (Pruefpunkte 1 bis 5), Paket `docs/packages/m10-s5-luft.md` Abschnitt "Teil B, Runde 74". Die Selbstauskunft habe ich nicht als Beweis genommen.

Vorgehen: Schwere Laeufe nur in einer Kopie: `git archive 651bc17` nach `scratchpad/lb` (dazu die ignorierten Dateien `scripts/dome-script.json` 08:35, `.compbox.json`, `.segs.json`, `.latte-cache.json` aus dem Arbeitsbaum; `dome-script.json` und `designs/dome.sc` sind aelter als der Commit 08:41, also gleicher Stand), Vergleichsstand `git archive 97a379e` (Zustand vor Teil B). Im Repo liegt nur diese Datei. `dome.sc` (18 MB) wurde nicht mit dem CAD-Werkzeug ausgewertet: Instanzen und Matrizen kommen aus `scripts/dome-script.json`. `viewer/instances.json` im Repo ist der Export von 02:12:59 (Runde 70); er kennt Runde 74 nicht.

## Urteil: FAIL gegen das Blatt (Punkte 2 und 3, Teil von Punkt 1); Selbstauskunft stimmt, Bau als Zwischenstand brauchbar

Jede Zahl der Montage-Meldung habe ich nachgerechnet und gefunden. Das Blatt-Soll verfehlt der Bau aber an drei Stellen: (a) K47 und K48 fehlen, (b) `check_leitungen` meldet 3 Verstoesse (alles Altbestand, Soll war 0), `check_leitungsordnung` meldet neu 9 Verstoesse (R5 4, R8 5), (c) der Schwerpunkt der Gruppe liegt bei Az -97,2 Grad statt -85 +- 5. Die Montage hat (a) bis (c) selbst als Befund gemeldet ("nicht geloest"), nicht verschwiegen.

## Pruefpunkte

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | 1/1/1/1/2 Instanzen (Schaltschrank, Einfuehrung, Verteiler, Aktivkohle, Geblaese) unter einer Komponente mit "E13"; Schwerpunkt Az -85 +- 5 | `python -I` ueber `scripts/dome-script.json` (Komponente `14_Technik_E13`, `component.insert_design`, `occurrence.copy`, `occurrence.move`) | Komponente `14_Technik_E13`; `Schaltschrank` 1, `Schrank_Einfuehrung` 1, `Luftverteiler_6` 1, `Aktivkohle_Station` 1, `Geblaese_Luft` 2 (1 `insert_design` + 1 `copy`): **1/1/1/1/2 erfuellt**. Lagen: Schrank und Einfuehrung bei 500/-6490, Geblaese bei -2300/-6460 und -2300/-6860, Verteiler -1300/-6860 (z 1110), Station -300/-7900. Schwerpunkt der sechs Teile 867 / -6843 = **Az -97,2 Grad, Soll -85 +- 5: verfehlt** (der Schrank allein liegt bei Az -85,6, die Gruppe laeuft von dort nach Westen/Sueden) | Zahlen PASS, Schwerpunkt FAIL |
| 2 | Trassen fuer 11 Kanten (K39, K40, K41, K44, K45, K46, K47, K48, K49, K51, K52); R10 meldet 10 Kanten weniger | `python -I` ueber `data/leitungstrassen.json` (`kante`/Id-Praefix); `check_leitungsordnung.py` in der Kopie von 651bc17 und von 97a379e | **9 von 11**: K39, K40, K41, K44 (9 Trassen), K45, K46, K49, K51, K52 sind verlegt; **K47 und K48 haben keine Trasse** (Montage: Absetzer-Deckel ohne Luftanschluss im Bauteil). R10: vorher 34 Kanten ohne Trasse (97a379e), nachher 26: **8 weniger statt 10**. Laengen nachgerechnet gleich der Meldung: K39 8,88 m, K40 12,26, K41 13,88, K45 17,74, K46 8,06, K49 10,41, K51 8,10, K52 12,58 | FAIL (2 Kanten) |
| 3 | `check_leitungen.py` 0 Verstoesse (dokumentierte dn erlaubt), `check_leitungsordnung.py` R1 bis R9 0 | beide Skripte in der Kopie | `check_leitungen`: **3 Verstoesse**, alle Altbestand und gleich dem Stand 97a379e: KOLL K08 (Rohr d40 trifft `Tank_gross:1`, Az -14 / r 2850 / Z 900, rund 360 mm), GEFAELLE K05 (250 mm gegen die Fliessrichtung, Az 16 / r 2999), GEFAELLE K21 (239 mm, Az -120 / r 2747); EINGABE, BAND, GANG 0; dn-Abweichungen K44-S, K44-GA/GB u. a. dokumentiert. `check_leitungsordnung`: R1, R2, R3, R6 (0 Rohre ueber Flur ohne Halter), R7 PASS; R4 1 (K20, Altbestand); **R5 neu 4** (K44-V 11 Boegen auf 12,0 m, Soll 7; K45 9 auf 17,7 m, Soll 8; K46 8 auf 8,1 m, Soll 6; K40 10 auf 12,3 m, Soll 7); **R8 neu 5** (K44-V/K40 68 mm bei -1225/-5856/290, K44-V/K52 100 mm bei 1904/-3447/290, K45/K40 123 mm bei -1105/-5960/290, K51/K40 226 mm bei -745/-6860/240, K51/K40 94 mm bei -745/-5957/240; Soll 25 bis 60 oder Achse >= 250 mm); R9 in der Kopie nicht messbar (`viewer/instances.json` fehlt dort, im Repo ist sie von Runde 70). Vorher (97a379e): R5 0, R8 0. Die Zahlen decken sich mit dem Paket ("R5 11, 9, 8, 10", "R8 68 bis 226") | FAIL (3 Altbestand, 9 neu) |
| 4 | `check_walkways.py` PASS (A >= 700, B >= 600, Wandluft >= 110, Tuer-Gang >= 3177) | `python -X utf8 scripts/check_walkways.py` in der Kopie | Laufweg A 700, B 600, Wandluft 110, Aussenbeete-Ecken 307, Tuer-Gang 3177; Exit 0; Bodenauslastung 50 % | PASS |
| 5 | `git hash-object` von `data/leitungsnetz.json` und `data/roadmap.json` gleich dem Stand vor der Sitzung; Teil-A-Instanzen unveraendert | `git rev-parse 97a379e:<datei>` gegen `651bc17:<datei>`; Matrizen aus `dome-script.json` gegen `viewer/instances.json` (Runde 70) | `leitungsnetz.json` 2920ca05 gleich, `roadmap.json` 14c8ff75 gleich; `Luftverteiler_4:1`, `Luft_Scheibenbelueftung:1..4`, `Schwimmerventil_Pool:1`: Matrix gleich (Toleranz 0,001) | PASS |

## Stichproben ausserhalb der Pruefpunkte

1. **Ort:** Die Gruppe steht **aussen** am Fundamentring, nicht innen wie im Blatt als Annahme; die Montage meldet den Grund (zwischen Tuer Az -72 und Ecke bleiben innen 1,35 x 1,2 m). Das Blatt-Soll "Wandluft >= 110" ist davon nicht beruehrt (PASS). Der Schrank sitzt neben der Tuer: seine naechste Ecke liegt 1072 mm seitlich der Tuermitte (Tuerrahmen -549 bis 538 mm), also etwa 520 mm vom Tuerrahmen entfernt, in Hoehe der Tuerschwelle. Zugang und Wetterschutz der Gruppe sind offen (Ben, Zwischencheck).
2. **Bild:** `renders/round-74.png` und `section-74.png` angesehen: Schrank (grau) neben der Tuer, Geblaese und Station westlich davon ausserhalb, Leitungen unterflur im Graben; das Bild zeigt keine Ueberschneidung des Tuerbereichs mit dem Schrank.
3. **Selbstauskunft gegen Daten:** "9 Kanten verlegt": gleich (K39, K40, K41, K44, K45, K46, K49, K51, K52); Geometrie der Laengen gleich; `check_leitungen` "nur 3 Altbefunde": gleich; R5/R8-Zahlen gleich.
4. **Vergleichszahlen vorher/nachher (`check_leitungsordnung`, 97a379e gegen 651bc17):** Rohr-Instanzen 139 auf 218, Boegen 95 auf 161, Rohre schraeg > 3 Grad 21 auf 23, Halter-Instanzen 18 auf 18, waagerechte Richtungen (5-Grad-Klassen) in der neuen Trassenmenge 4.

## Auflagen

1. **A1, K47/K48:** Absetzer-Luftanschluss (Kappe/Stutzen am Deckel von `Tank_klein:1` und `:2`) fehlt im Bauteil; Werkstatt-Aufgabe, dann K47/K48 verlegen (Blatt: d20 zu den Absetzerdeckeln). Bis dahin R10 26 statt 24.
2. **A2, R5 und R8 neu:** Die Bogenzahl ist in der Leitungsordnung ohne feste Bogen an Port und Steigleitung gerechnet (R5-Annahme [A]); entweder Ordnung anpassen und im Blatt festhalten oder die Strecken K44-V, K45, K46, K40 kuerzen. R8: K40 liegt im selben Graben 68 bis 226 mm unter dem Luftbuendel; Frischwasser (K40, K52) in einen eigenen Graben legen oder Achsabstand >= 250 mm.
3. **A3, Schwerpunkt der Gruppe:** Das Blatt misst die Gruppe, die Montage bezieht Az -85 auf die Schrankmitte. Eine der beiden Definitionen im Blatt streichen (Vorschlag: Bezug Schrankmitte, dann PASS mit -85,6).
4. **A4, `viewer/instances.json` nach Runde 74:** nicht exportiert; R9 und der Viewer kennen die Technikgruppe nicht. Export nach dem naechsten Modellspeichern abwarten (mehrere `serve.py` exportieren dann gleichzeitig, siehe `docs/jobs/pruefung/V-MESS-VV.md` V3).
5. **A5, Zugang Tuer:** der Schrank steht rund 520 mm neben dem Tuerrahmen; Ben prueft beim Zwischencheck, ob die Tuer von aussen frei zugaenglich bleibt.

## Nicht belegt oder nicht nachgemessen

1. `designs/dome.sc` (18 MB) nicht mit dem CAD-Werkzeug ausgewertet (kein schwerer Lauf); die Gruppe ist am Befehlsstrom `dome-script.json` gemessen, nicht im Modell selbst. Die Meldung "Build Exit 0" habe ich nicht wiederholt.
2. `check_latte` (Kollisionspruefung, rund 67 Minuten) nicht gelaufen; der Stand Runde 69 liegt in `renders/check_latte-69.txt` und kennt die neuen Teile nicht.
3. Rueckwand 20 mm vor der Fundamentring-Aussenkante (Angabe im Paket): nicht nachgemessen.
4. Wetterschutz der Technikgruppe und Uebergang d25 auf Luftschlauch 16 an den Biofiltern: offen laut Paket (Werkstatt), nicht Gegenstand.

Geprueft gegen: `scripts/dome-script.json` (Runde 74), `data/leitungstrassen.json`, `data/leitungsnetz.json`, `data/roadmap.json`, `check_leitungen.py`, `check_leitungsordnung.py`, `check_walkways.py` je in Kopie von 651bc17 und (Ordnung, Leitungen) von 97a379e, `git rev-parse` der zwei Hash-Dateien, `renders/round-74.png`, `renders/section-74.png`, `data/bom_koerper.json` (Tuerbreite).
Offen: A1 bis A5 (Werkstatt, Montage, Planer, Ben); `dome.sc`-Auswertung und `check_latte` fuer Runde 74 (Pruefer, nur auf Auftrag).

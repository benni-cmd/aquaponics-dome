# Pruefung N-VERBINDER Montage (Pruefer, 05.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md` und Auftrag der Orchestrator-Sitzung (Wiederanlauf). Gegenstand: Montage D91 laut `docs/packages/n-verbinder.md` Abschnitt "Montage D91": Commits 38e537a, a22d4ad, 55ab3e0, df2f39d (A+ Runde 77), 7d64888 (Ring B2 Runde 3), 14865bc (Paket, loop-state). Ziel laut Paket: Beide Varianten tragen an den 26 Knoten ein Plattenpaar und je Strebe einen Scherenarm; die Streben sind Rundrohr 42,4 x 2,6; `check_verbinder_montage`, `check_walkways`, `check_huelle` gruen, `check_latte` in Kopie gelaufen. Ich habe nichts davon gebaut. Alle Messungen in dieser Sitzung neu, in einer Kopie `git archive 14865bc` im Scratchpad; geschrieben ist nur diese Datei. Das Befehlsskript A+ habe ich per `gen_dome.py 5` neu erzeugt (`scripts/.segs.json` ist gleich der im Arbeitsbaum); das Ring-B2-Skript stammt aus dem Arbeitsbaum (Neuerzeugung scheiterte an der fehlenden Hilfsdatei `scripts/_comp.json`, die nicht versioniert ist).

## Urteil: PASS mit Auflagen

Alle Pruefskripte bestehen, die Zaehlungen stimmen, und die Strebenachsen treffen die Knotenpunkte ausser an den 5-wertigen Knoten. Dort liegen 24 von 30 Strebenenden bis 15,9 mm neben dem Knotenpunkt; das ist die Folge von D91 (eine 6-Loch-Platte), steht im Bauteilblatt als Achsversatz, nicht aber als Modellfolge im Montage-Befund. `check_latte` fuer Runde 77 ist in meiner Kopie nicht zu Ende gelaufen (4701 Paare gegen 2555 in Runde 73): das Ergebnis fehlt, die Montage hat ihn ebenfalls nicht gemeldet.

## Messung

| Nr | Pruefung | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | Montage-Check beide Varianten | `python -X utf8 scripts/check_verbinder_montage.py` und `... --variante ring_b2` (Kopie) | je 14/14 PASS: Knoten_Platte 26, Schere_A 60, Schere_B 68, Strebe_A 30, Strebe_B 34, Arme 128 = 2 x 64; Kugelknoten im Skript 0; 256 Nasen geprueft, groesste Nasenecke 0,29 mm innerhalb des Gegenloch-Rands (D15); Folie: hoechster Punkt 39,3 mm gegen foil_z0 40,2; CAD-Proben n01 (6-wertig), n02 (5-wertig), n17 (4-wertig) je 0 Durchdringungen ueber 0,1 mm3 und 0 ungepruefte Paare | PASS |
| 2 | Zaehlung unabhaengig | eigenes Python ueber `scripts/dome-script.json` (`occurrence.move` je Namen, `insert_design`-Pfade) | Knoten_Platte 26, Schere_A 60, Schere_B 68, Strebe_A 30, Strebe_B 34; Dateien `knoten_schere_arm_a_montage.sc`, `..._b_montage.sc`, `knoten_schere_platte.sc`, `strebe_a.sc`, `strebe_b.sc` je 1 `insert_design`; Kugelknoten-Dateien `knoten_<n>_nNN.sc` 0. Gegenprobe: `layout.json` hat 30 kurze und 35 lange Streben; minus 1 lange Basiskante an der Tuer = 30 A, 34 B; 130 Tabellenarme minus 2 = 128. Auch die committeten `designs/dome.sc` und `designs/dome-ring_b2.sc` (Zip) tragen die Namen Knoten_Platte, Schere_A/B, Strebe_A/B und kein "Kugelknoten" | PASS |
| 3 | Gaenge | `python -X utf8 scripts/check_walkways.py` (Kopie) | A 700, B 600, Wandluft 110, Nachbarportale 307, Tuer-Gang 3177 mm, alle PASS (gleich Runde 73) | PASS |
| 4 | Huelle | `python -X utf8 scripts/workshop/check_huelle.py` (Kopie) | 68/68 PASS, 0 FAIL; Innere Lage liegt ueber Strebe + Schaumband + Kanal (21,2 + 3 + 15 < 40,2), Luft 1 mm | PASS |
| 5 | Scherenknoten-Check | `python -X utf8 scripts/workshop/check_knoten_schere.py` (Kopie) | 35/35 PASS; Probe n02 (5-wertig) mit eingeschlossen (die Auflage 5 meiner Pruefung N-VERBINDER ist damit erfuellt); BEFUND-MESSUNG Achsversatz 5-wertig 15,07 mm unveraendert | PASS |
| 6 | Strebenteile | `python -X utf8 scripts/workshop/check_parts.py strebe_a strebe_b` (Kopie) | je 22/22 PASS | PASS |
| 7 | Strebenlaenge | `scripts/.segs.json` (Knoten-zu-Knoten) gegen Bauteilblatt | A 3279,2 mm, B 3708,2 mm je alle gleich; Rohrmund-Abstand nominal A 3075,4 (Mundversatz 101,9 je Seite), B 3503,8 (102,2). Gebaut A 3077,1 (Montage: Mitte der Spanne 3075,5 bis 3078,7 durch die Lochdrehung), B 3503,8 | PASS mit Hinweis (A 1,7 mm laenger als nominal, im Paket als Spanne begruendet) |
| 8 | Achsen treffen die Knoten | eigenes Python: je Strebe die Achse (Instanzursprung + Matrixspalte), Abstand der zwei Knotenpunkte aus `.segs.json` zur Achse, gruppiert nach Wertigkeit (Zahl der Segmente je Knoten) | 3-wertig (6 Enden) max 1,2 mm, 4-wertig (32) max 1,21 mm, 6-wertig (60) max 1,4 mm, **5-wertig (30 Enden) max 15,85 mm, 24 davon ueber 3 mm** | Befund, siehe Auflage 1 |
| 9 | `check_latte.py 77` in der Kopie | `python -X utf8 scripts/check_latte.py 77` (Hintergrund, Start 18:36) | geometrische Teile PASS (Abstaende Beet/Tisch 94 / 45 / 186 mm, 0 Verletzungen); "EXAKT ohne Fundamentring/Erde: 4701 Paare" (Runde 73: 2555), nach rund 45 min noch keine Runde ausgewertet. Zum Schreibzeitpunkt **kein Ergebnis** | nicht belegt |
| 10 | Aenderung an `check_latte.py` (Commit a22d4ad) | `git diff 38e537a~1 14865bc -- scripts/check_latte.py` | Strebenenden im Umkreis von 40 mm werden zu einem Knoten zusammengefasst (wegen der 15 mm Achsversatz); das Zaehlen der Streben am Scheitel ist damit toleranter als vorher (vorher exakt gerundete Punkte) | PASS mit Hinweis (Auflage 3) |

## Stichproben

1. **Zahl aus der Meldung gegen die Messung:** Paket meldet "check_verbinder_montage 14/14", "Nase im Gegenloch groesste Ecke 0,29 mm innerhalb", "Folie 39,3 < 40,2", "check_huelle 68/68", "check_knoten_schere 35/35", "check_parts strebe_a/b je 22/22": alle gemessen gleich. PASS.
2. **Teil gegen sein Blatt:** Paket nennt 26 x 1083 g + 128 x 394 g = 78,6 kg. Rechnung: 28 158 g + 50 432 g = 78 590 g. Das Plattenpaar 1083 g = 2 x 541,5 g, passt zur Platte aus meiner Pruefung (541 g). Das Gewicht der Arme (394 g) habe ich nicht nachgewogen. Teilweise.
3. **Commit gegen Blatt ("nicht anfassen"):** `git diff --stat 38e537a~1 14865bc` (ohne Bilder und `.sc`): 20 Dateien, alle im Montage-Umfang (Skripte, `params.json`, `knoten_schere.json`, `huelle_folie.json`, Teiledaten, Paket); `data/parts/strebe_a.json` und `strebe_b.json` von je 53 auf 1 Zeile (Umformatierung, `check_parts` 22/22 PASS). PASS.
4. **Zahl im Paket gegen Rechnung:** Paket nennt "A-Rohre muessten 3075,5 / 3076,3 / 3078,6 mm lang sein": nominal aus `.segs.json` 3075,4 (ohne Lochdrehung); die drei Werte liegen innerhalb der angegebenen Spanne und die gebaute 3077,1 in der Mitte. Plausibel, nicht einzeln nachgerechnet.

## Nicht belegt

1. **`check_latte` Runde 77:** zum Schreibzeitpunkt nicht fertig (siehe Zeile 9). Das Paket-Ziel nennt "`check_latte` in Kopie gelaufen"; in `docs/packages/n-verbinder.md` und `loop-state.md` steht kein Ergebnis.
2. **Viewer-Export beider Varianten:** nicht nachgemessen (die Montage nennt 273 Definitionen / 5353 Instanzen A+, 299 / 5570 B2 und "im Browser angesehen"). Eigene Ansicht im Viewer nicht gemacht.
3. **CAD-Neubau selbst** (`build.sh 5 77`, `build.sh 5 3 ring_b2`, Exit 0): nicht neu gebaut; stuetzt sich auf das committete `dome.sc` und `dome-ring_b2.sc`, deren Bauteilnamen ich im Zip gefunden habe, und auf den neu erzeugten Befehlssatz.
4. **Ring B2 mit eigenem Skript:** Neuerzeugung scheiterte an `scripts/_comp.json` (nicht versioniert); der Check lief auf dem Skript des Arbeitsbaums.
5. Festigkeit der Schere (Laschen 8 mm), Einrasten der Nasen am Muster, Kopfmasse am echten Teil: wie in der Pruefung N-VERBINDER; nicht Gegenstand der Montage.

## Auflagen

1. **Achsversatz an den 5-wertigen Knoten als Modellfolge nennen und entscheiden:** Messung 8: 24 von 30 Strebenenden an den sechs 5-wertigen Knoten liegen 3 bis 15,85 mm neben dem Knotenpunkt; die Streben treffen sich dort nicht mehr in einem Punkt. Nach D91 (eine 6-Loch-Platte) erwartet; im Montage-Befund steht nur die Laengenfolge, nicht der Querversatz. Entscheidung Ben: 5-Loch-Platte fuer die sechs Knoten (dann alle <= 1,4 mm) oder Querversatz hinnehmen. Owner: DEINE ENTSCHEIDUNG (Ben); Empfehlung 5-Loch-Platte, weil die Messung 1,4 mm als obere Grenze an allen anderen Knoten zeigt.
2. **`check_latte` Runde 77 zu Ende fahren:** das Paket-Ziel verlangt es; Laufzeit mit 4701 Paaren mehrere Stunden, deshalb als Hintergrundlauf mit Ende-Marke (Hinweis A7 meiner Pruefung M10-UMBAU). Ergebnis ins Paket und in `loop-state.md`. Owner: ICH (Montage).
3. `check_latte.py`: Zusammenfassung der Strebenenden im Umkreis 40 mm hat keine Gegenprobe; pruefen, dass 40 mm nicht echte Fehler (Strebe 20 bis 40 mm verschoben) verdeckt, zum Beispiel Umkreis 20 mm und gesonderte Zeile fuer die 5-wertigen Knoten. Owner: ICH (Montage).
4. Ring-B2-Befehlsskript reproduzierbar machen: `scripts/_comp.json` erzeugen oder versionieren, damit ein Pruefer `gen_dome.py --variante ring_b2` ohne Arbeitsbaum laufen lassen kann. Owner: ICH (Montage).
5. Montage-Befunde aus dem Paket, nicht Gegenstand dieser Pruefung, bleiben offen: Katalog (`PRF-st-strebe30x30` und Kugelknoten-Artikel in `data/katalog.json`, Stueckliste auf Rundrohr und Scherenknoten), Keilschiene mit 120 mm Endversatz (`keilschiene.json`: node_clear 130; Scherenknoten Rohrmund 102 mm), `strut_cutting.py` mit `E_NOM = 120`. Owner: ICH (Werkstatt/Montage).

Geprueft gegen: `check_verbinder_montage.py` (beide Varianten, 14/14), `check_walkways.py`, `check_huelle.py` (68/68), `check_knoten_schere.py` (35/35), `check_parts.py strebe_a strebe_b` (22/22), neu erzeugtes `dome-script.json` A+ (eigene Zaehlung), `.segs.json`, `designs/dome.sc` und `dome-ring_b2.sc` (Namen im Zip), `git diff --stat 38e537a~1 14865bc`, `docs/packages/n-verbinder.md`.
Offen: Auflagen 1 bis 5; `check_latte` Runde 77 ohne Ergebnis; nicht belegt: Viewer-Export, CAD-Neubau, Gewicht der Arme.

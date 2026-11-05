# Pruefung N-VERBINDER (Pruefer, 05.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md` und Auftrag der Orchestrator-Sitzung (Wiederanlauf). Gegenstand: Blatt `docs/jobs/N-VERBINDER.md` (Pruefpunkte 1 bis 5), Commit 70c5a72 (Scherenknoten als ein Bauteil), Foto `reference/chemnitz/laschenknoten-foto.jpg`. Ich habe nichts davon gebaut. Alle Messungen in dieser Sitzung neu, in einer Kopie `git archive 70c5a72` im Scratchpad; geschrieben ist nur diese Datei. Leichte Laeufe (kein Gesamtmodell, kein `check_latte`).

## Urteil: PASS mit Auflagen

Die Pruefpunkte 1, 2, 3 und 5 sind erfuellt. Pruefpunkt 4 (Achsversatz <= 5 mm) ist bei den 6 fuenfwertigen Knoten verfehlt (15,07 mm); das Blatt verlangt hier "Befund melden, nicht umbauen", die Werkstatt hat das getan. Der Scherenknoten ist damit abnahmereif fuer Ben, aber nicht einbaureif: Die Entscheidung ueber die zweite Platte (5 Loecher, 72 Grad) steht aus. Der Bildvergleich mit dem Foto zeigt dieselbe Ordnung; die Bilder sind aber Modellansichten, ein Funktionsbeleg (Einrasten der Nasen) ist das nicht.

## Pruefpunkte

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | `check_knoten_schere.py` Exit 0: Koerper geschlossen, Nasen = Rohraussenradius + 3,0 mm (+-0,05), Rohrachse durch den Knotenpunkt <= 0,01 mm | `python -X utf8 scripts/workshop/check_knoten_schere.py` (Kopie, 2 min 40 s) | Exit 0, Schlusszeile "29/29 PASS". Platte 1, Arm A 11, Arm B 11 Koerper, alle geschlossen. Nasenspitze |Y| max 24,2 mm = 21,2 + 3,0 (Lasche 1 und 2, A und B). Rohrachse zum Knotenpunkt A 0,0037 mm, B 0,0012 mm; Neigung A 15,856 Grad, B 17,998 Grad | PASS |
| 2 | `inspect.interference` im Probe-Knoten n01 (Platte + 6 Arme): 0 Durchdringungen ueber 0,1 mm3 (Gewindeberuehrung ausgenommen) | gleicher Lauf, Zeile "interference n01" | 67 Koerper (1 + 6 x 11); 6 Paare gemeldet, alle `Dreh_Schraube` x `Dreh_Mutter` im eigenen Arm (je rund 171 mm2 Flaeche, Gewinde), kein Paar mit Platte, Lasche oder Rohr; ungeprueft 0; Durchdringungen > 0,1 mm3: 0 | PASS (die Ausnahme der Gewindepaare ist im Blatt vorgesehen) |
| 3 | `knoten_schere.json`: 26 Knoten, Armzahl = Wertigkeit aus `layout.json` (10 x 4, 6 x 5, 10 x 6), 130 Arme, Typ A 60 / B 70 | eigenes Python ueber `data/components/knoten_schere.json` und `data/layout.json` (`nodes_list`, `strut_len_mm`) | 26 Knoten; Armzahl 10 x 4, 6 x 5, 10 x 6; 130 Arme; A 60, B 70; kein Loch doppelt belegt. Gegenprobe unabhaengig: jeder Knoten liegt <= 1 mm an einem `layout.json`-Knoten mit gleicher Wertigkeit (0 Abweichungen); `layout.json` fuehrt 30 Streben zu 3279 mm und 35 zu 3708 mm, also 60 kurze und 70 lange Enden (3708 = 3504 + 2 x 102, 3279 = 3075 + 2 x 102) | PASS |
| 4 | Groesster Achsversatz nach Drehung um die Plattenschraube im Bauteilblatt mit Befehl; Soll <= 5 mm, sonst Befund | Blatt `docs/parts/knoten_schere.md` Abschnitt Lochbild; `python -X utf8 scripts/workshop/knoten_schere.py --table`; Check-Zeile "BEFUND-MESSUNG Achsversatz"; eigene Formel 37 mm x sin(Drehung) ueber alle 130 Arme | Blatt nennt Wert und Befehl. Check: groesster 15,07 mm (5-wertig, Drehung 23,999 Grad), 4-wertig 1,11 mm, 6-wertig 1,12 mm. Eigene Formel: 15,05 mm (Knoten n08, gleiche Drehung; Abweichung 0,02 mm), die Werkstatt nennt n02 | Dokumentation PASS; Soll 5 mm bei den 6 fuenfwertigen Knoten **nicht erfuellt** (Befund, Blatt: kein FAIL) |
| 5 | Mindestens 5 Bilder inkl. Explosionsbild unter `renders/components/knoten_schere/`, optisch gegen das Foto geprueft | `ls renders/components/knoten_schere/`; Foto und 3 der 8 Bilder angesehen (02, 04, 06) | 8 Bilder (iso, Draufsicht, Seite, Explosion iso und Draufsicht, Nase im Gegenloch, Arm A und B Seite). Draufsicht: Platte mit Schraubenkranz, je Arm eine Drehpunktschraube kurz vor dem Rohrmund, Nasen seitlich am Rohr, wie links im Foto. Explosion: Platte, Schraube, Scheibe, zwei Laschen mit Nase und Knick, Rohr mit Gegenloch. Bild 06: die Nase steht durch das Gegenloch aus dem Rohr. Platte zu Rohr: Foto etwa 2,45 : 1, Modell 110 : 42,4 = 2,6 : 1 (aus den Bildern gemessen, Foto mit Perspektive) | PASS |

## Stichproben ausserhalb der Pruefpunkte

1. **Teil gegen sein Blatt:** Platte laut Bauteilblatt D 110 x 8, 6 Loecher D 11 auf r 37, Mittelbohrung D 20, 541 g. Gemessen (`solidcraft-cli.exe eval designs/components/knoten_schere_platte.sc`): Box +-55 x +-55, Dicke 8,0 mm, Volumen 68 951 mm3 gegen erwartet 68 952 mm3 (Kreisscheibe minus 6 Loecher minus Mittelbohrung), 0,541 kg bei 7,85 g/cm3. PASS.
2. **Zahl aus der Meldung gegen die Messung:** Commit und Paket melden "Check 29/29": gemessen 29/29 PASS. `check_parts.py knoten_schere` 22/22 PASS wie gemeldet. PASS.
3. **Commit gegen Blatt ("Nicht anfassen"):** `git show --stat 70c5a72` beruehrt kein `gen_dome.py`, `dome.sc`, `build.sh`, `docs/parts/knoten.md`, `data/params.json`, `data/roadmap.json`; `data/katalog.json` (+2 Zeilen) ist Teil der Bauteil-Anmeldung. Vorentwurf `knoten_schere_proto` geloescht und im Blatt begruendet. PASS.
4. **Abweichung vom Blatt, im Bauteilblatt offen genannt:** Das Blatt sagt "A und B unterscheiden sich NUR im Knickwinkel"; gebaut ist auch die Knicklinie verschieden (A r 72,1, B r 63,0), damit die Rohrachse bei gemeinsamer Plattenhoehe durch den Knotenpunkt geht. Das ist plausibel (Check zeigt 0,004 / 0,001 mm), aendert den Laserzuschnitt nicht, aber die Biegelinie; Ben soll das wissen.

## Nicht belegte oder nicht nachgemessene Behauptungen

1. Funktion des Einrastens: Nasen in den Gegenloechern, Oeffnen der Schere ohne Plattenschraube, Abziehen des Rohrs: nur an Modell und Bildern, nicht kinematisch gemessen und nicht am Muster.
2. Festigkeit: Knick 4,6 kN bei Lasche 5 mm gegen 11,8 kN bei 8 mm (R56 Abschnitt 4) nicht nachgerechnet; R56 selbst nennt diese Werte, ich habe sie nicht geprueft.
3. Kopfmasse (Laschen 20 x 5, Lochkreis 37, Gegenloecher D13) sind laut Blatt [A] aus dem Foto ohne Massstab geschaetzt; ein Massbeleg am echten Teil fehlt.
4. Viewer-Detailansicht `#detail=knoten_schere`: nicht aufgerufen (braucht `export_detail.py` und laufenden Viewer); die Teiledaten sind per `check_parts` 22/22 geprueft, die Ansicht nicht gesehen.
5. Rohrlaengen A 3075 / B 3504 mm in der Kuppel: aus `layout.json` (Knoten-zu-Knoten 3279 / 3708 minus 2 x 102) bestaetigt, nicht gegen das Gesamtmodell gebaut (Blatt verbietet den Einbau).

## Auflagen

1. **DEINE ENTSCHEIDUNG (Ben):** Zweite Platte mit 5 Loechern im 72-Grad-Raster fuer die 6 fuenfwertigen Knoten, sonst 15 mm Achsversatz an diesen Knoten (4- und 6-wertige 1,1 mm). Empfehlung: zweite Platte, weil sie den Versatz auf 1,1 mm bringt und das Teil nicht aendert.
2. **DEINE ENTSCHEIDUNG (Ben):** die vier Blatt-Fragen: Lesart der Funktion (Nasen aussen), Rohr Rund 42,4 x 2,6 statt Vierkant 30 x 30 x 3 (Schere passt nicht in das Vierkant), Laschendicke 5 oder 8 mm, Keilschiene der Folie auf Rundrohr. Sie sind weiter offen.
3. Bauteilblatt und Blatt in Einklang bringen: "A und B nur im Knickwinkel" im Blatt auf "Knickwinkel und Knicklinie" korrigieren. Owner: Orchestrator.
4. Vor dem Einbau durch die Montage: Viewer-Detailansicht ansehen (Teiledaten 22/22 PASS, Ansicht nicht gesehen) und Einrasten der Nasen mit einem Muster aus Rohr und Laschen pruefen (Blatt R56 offene Fragen). Owner: Werkstatt, Ben.
5. Probe-Knoten n01 prueft nur den 6-wertigen Knoten; ein fuenfwertiger Knoten (n02) mit gedrehten Armen ist nicht auf Durchdringung geprueft. Check um `--knoten n02` als Pflicht-Lauf erweitern. Owner: Werkstatt.

Geprueft gegen: `python -X utf8 scripts/workshop/check_knoten_schere.py` (29/29, Exit 0, Kopie 70c5a72), `python -X utf8 scripts/workshop/check_parts.py knoten_schere` (22/22), `solidcraft-cli.exe eval` der Platte, eigenes Python ueber `data/components/knoten_schere.json` und `data/layout.json`, Foto und drei Bilder (Draufsicht, Explosion, Nase im Gegenloch) angesehen, die uebrigen fuenf nur als Dateien gezaehlt, `git show --stat 70c5a72`, `docs/parts/knoten_schere.md`.
Offen: Auflagen 1 bis 5; nicht belegt: Einrasten der Nasen am Muster, Festigkeit, Viewer-Detailansicht, Kopfmasse am echten Teil.

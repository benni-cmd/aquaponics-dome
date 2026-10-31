# Reihenfolge aller offenen Wuensche und Vorgaben (Orchestrator, Stand 31.10. 19:10)

**Problem:** Es sind viele Wuensche von Ben offen (Plane durchsichtig und simples Schnittmuster, kleiner Puffer im Dom, Messstellen an mehreren kritischen Stellen, Laufwege, Leitungen, Bauanleitung/Detailansicht, Roadmap B1-B10); ohne feste Reihenfolge stoeren sie sich gegenseitig (Leitungsplan braucht Puffer und Messstellen).
**Intent:** Eine sichtbare, abhaengigkeitsgerechte Reihenfolge, damit jede Sitzung nur ihren Auftrag liest und das Limit reicht.
**Goal:** Jede Zeile hat Besitzer-Sitzung, Auftragsblatt, Abhaengigkeit und Status; der Orchestrator pflegt sie bei jeder Abnahme.

| # | Auftrag | Sitzung | Blatt | Wartet auf | Status |
|---|---|---|---|---|---|
| 1 | Laufwegkarte gruen (D62, Ringe verschoben, Build 55) | Montage | next-steps-montage | - | laeuft (Karte rechnet) |
| 2 | R37 Puffer klein, Faesser, transparent, alles im Dom | Fachrecherche-3 | jobs/R37 | - | laeuft |
| 3 | R38 Plane Schnitt-/Nahtmuster | Fachrecherche-4 | jobs/R38 | - | laeuft |
| 4 | R39 Messstellenkonzept | Fachrecherche-5 | jobs/R39 | - | startet |
| 5 | W34 Puffer neu (Werkstatt) | Werkstatt | wird nach R37 geschrieben | R37, Bens Okay kleiner Puffer | offen |
| 6 | W35 Sondenhalter/Messstellen-Bauteile | Werkstatt | wird nach R39 geschrieben | R39 | offen |
| 7 | Montage: Puffer und Messstellen setzen, Karte erneut gruen | Montage | wird geschrieben | 1, 5, 6 | offen |
| 8 | Plane: Zuschnitt in Bauplan und Modell (Keilschienen, Fussrand, Tuerzarge) | Werkstatt + Montage | wird nach R38 geschrieben | R38 | offen |
| 9 | M10 Leitungsplan (Plan vorab, Orchestrator liest gegen), dann Leitungen und Kabel inkl. Signalkabel Messstellen | Montage | jobs/M10 | 7 | offen |
| 10 | EIN check_latte mit allem, Draufsicht/Seitenansicht, PAUSE und Zwischencheck mit Ben | Montage + Orchestrator | - | 9 | offen |
| 11 | Docs: Folgedokumente 475 -> 346 kg, Specs-Zaehlung aus Modell (D52), model-description, integration-board | Orchestrator | - | laufend | offen |
| 12 | Nach Zwischencheck: Roadmap B1-B10 (Detailansicht, Teile, Katalog, Meterware, R31 Materialien, R32 Becken, R33 Beete, B9b Statik, V2c Streben, B10 Bauanleitung), Notstrom/Alarm konkret | verschiedene | packages/bauanleitung-teileliste-detailansicht | 10 | zurueckgestellt |

## Rest-Befunde aus den Sitzungen (Pruefung 31.10. 20:00, nach Bens Sorge um unsauberes Ende bei Limit)
Alle sieben Sitzungen gelesen (Montage, Werkstatt-2/-3/-4, Fachrecherche-aquaponik/-3, Viewer). Nichts ist wegen eines Limit-Resets halb abgebrochen: die Sitzungen haben sauber gesichert und gepusht; die zuletzt gestoppten Hintergrundlaeufe von Werkstatt-3 waren Reste NACH W27/W31/W32 (alle committet: 7cbe695, 7ca71f9, fca0290). Unbeantwortet war EINE Frage (Viewer), dazu stehen Befunde, die in keinem Auftrag lagen. Eingeordnet:

| # | Befund | Herkunft | Besitzer | Wohin |
|---|---|---|---|---|
| a | `walk_z` in `viewer/export_model.py` schreiben (FPV-Hoehe haengt sonst am Rueckfall 400) | Viewer-Sitzung (Frage unbeantwortet) | Viewer-Sitzung | JA entschieden (D67), Nachricht gesendet |
| b | Pool-Seitenablauf; Hoehenlage der Beetablaeufe unter dem Pool-Spiegel (Z 515); Aufteilung Tische/Beete auf zwei Linien (12 Tische + 7 Beete je Linie angenommen) | Fachrecherche-aquaponik R28 | Montage M10-Plan | Linienaufteilung 12/7 entschieden (D67); Ablaeufe als Punkte im M10-Plan vorab |
| c | Pumpentafeln seitlich am Tankstand setzen, `tank_offsets` pruefen (Plattform klein 619, gross 821) | Werkstatt-2 W30 | Montage | in Schritt 7 (Puffer/Messstellen setzen) mitnehmen |
| d | Netzliste K05/K06/K21/K22 noch d50; Bett 68-75 % des Modellwassers; Siebbelastung 8 m/h ohne Datenblatt; Notueberlauf Feinfilter | Werkstatt-3 W32 | Fachrecherche | neuer Auftrag R40 "Netzliste auf Stand bringen" nach W34/W35 (Puffer klein, Drittbecken, Messstellen, Linien), VOR M10-Plan |
| e | Querstrebe Z 650 statt 800 an den Tischen (Beetzugang unter der Strebe enger, Statik der kuerzeren Beine nicht nachgewiesen) | Werkstatt-4 W33 | Orchestrator | vorlaeufig akzeptiert (D67), im FPV beim Zwischencheck pruefen, Statik B9b |
| f | Kegelsitz Tank, Beine Tisch, Strebenkonzept: Statik nicht nachgewiesen | W30, W33, R34 | Roadmap B9b | nach Zwischencheck |
| g | check_latte seit Plane, Tuer und Ringverschiebung nicht gelaufen; Skript umstellen (Tuer_Komplett statt T4_Blatt, Plane/Figuren ausnehmen, W-M4 gegen Fase) | Montage | Montage | Schritt 10 |
| h | Keilschienen (65), Planenausschnitt-Zarge, Bodenbefestigung der Basisueberstaende nicht eingesetzt; W-M1 (Druckstutzen Pumpe_klein:4 x Tank-Strebe), M2b Querbolzen x Strebe 517 | Montage | Montage/Werkstatt | nach R38 (Plane) bzw. Schritt 10 |
| i | Pointer Lock/Mausblick im FPV nicht im echten Browser getestet | Viewer-Sitzung | Ben | DEINE HANDLUNG, beim Zwischencheck |

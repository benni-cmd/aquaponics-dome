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
